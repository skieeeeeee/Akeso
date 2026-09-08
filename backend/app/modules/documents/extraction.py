"""Turning OCR text into reviewable clinical findings.

Two layers, in this order:

1. A deterministic regex extractor. Always runs, needs no network, and is what
   makes the demo reproducible.
2. The AI layer, which can find things the regexes miss. Its output is
   schema-validated and merged; a failure leaves the rule-based result in
   place.

Nothing here concludes anything. A lab flag is only ever computed by comparing
a printed value against a printed reference range — if either is missing or
unparseable the flag stays `None`/`unclear` rather than guessing.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import date

from app.services.ai import get_provider, structured
from app.services.ai import prompts
from app.services.ai.schemas import DocumentExtraction
from app.shared.enums import DocumentType, ExtractedEntityType, LabFlag

log = logging.getLogger("medikiosk.documents.extract")

DOSE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|iu|units?)\b", re.I)
FREQUENCY = re.compile(
    r"\b(od|bd|bid|tds|tid|qid|hs|sos|stat|once daily|twice daily|thrice daily|\d-\d-\d)\b",
    re.I,
)
DURATION = re.compile(r"\b(?:x|for)\s*(\d+)\s*(day|days|week|weeks|month|months)\b", re.I)
MED_PREFIX = re.compile(
    r"^(?:\d+[.)]\s*)?(?:tab|tabs|tablet|cap|caps|capsule|syp|syrup|inj|injection|oint|drops?)\b\.?\s*",
    re.I,
)
LAB_LINE = re.compile(
    r"^([A-Za-z][A-Za-z0-9 ()/.'%-]{2,40}?)\s*[:\-]?\s+(\d+(?:\.\d+)?)\s*"
    r"([A-Za-z/%µ]+(?:/[A-Za-z]+)?)?\s*"
    r"(?:\(?\s*(?:ref(?:erence)?\.?\s*(?:range)?\s*[:\-]?\s*)?"
    r"(\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?)\s*\)?)?\s*$"
)
DEMOGRAPHIC = re.compile(r"^(date|age|sex|phone|mobile|id|uhid|abha|reg|bill|room|bed)", re.I)

DATE_PATTERNS = (
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"\b(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})\b"),
    re.compile(
        r"\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4})\b",
        re.I,
    ),
)

LAB_HINTS = ("lab", "laborator", "haemoglobin", "hemoglobin", "reference", "specimen",
             "pathology", "biochemistry", "cbc", "hba1c", "creatinine", "report")
RX_HINTS = ("rx", "prescription", "tab.", "tablet", "cap.", "syp", "advice", "dosage")
DISCHARGE_HINTS = ("discharge", "admitted", "admission", "operated", "hospital course")

LABELLED = {
    ExtractedEntityType.DIAGNOSIS: ("diagnosis", "dx", "impression", "provisional diagnosis",
                                    "final diagnosis", "condition"),
    ExtractedEntityType.SURGERY: ("surgery", "operation", "procedure performed", "operated for"),
    ExtractedEntityType.ALLERGY: ("allergy", "allergies", "allergic to"),
    ExtractedEntityType.NOTE: ("advice", "advise", "remarks", "note", "notes",
                               "follow up", "follow-up", "plan"),
}


@dataclass(slots=True)
class Finding:
    """One extracted entity, before it becomes a database row."""

    entity_type: ExtractedEntityType
    value: str
    attributes: dict[str, str] = field(default_factory=dict)
    numeric_value: str | None = None
    unit: str | None = None
    reference_range: str | None = None
    flag: LabFlag | None = None
    event_date: date | None = None
    confidence: float = 0.6
    extractor: str = "rules"

    @property
    def dedupe_key(self) -> tuple[str, str]:
        return (self.entity_type.value, self.value.strip().lower())


def _title(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().title() if text.islower() else re.sub(r"\s+", " ", text).strip()


def parse_date(raw: str | None) -> date | None:
    """Parse a printed date. Indian documents are day-first."""
    if not raw:
        return None
    candidate = raw.strip().replace(".", "/").replace("-", "/")
    iso = re.match(r"^(\d{4})/(\d{2})/(\d{2})$", candidate)
    if iso:
        try:
            return date(int(iso[1]), int(iso[2]), int(iso[3]))
        except ValueError:
            return None
    dmy = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})$", candidate)
    if dmy:
        day, month, year = int(dmy[1]), int(dmy[2]), int(dmy[3])
        year += 2000 if year < 100 else 0
        try:
            return date(year, month, day)
        except ValueError:
            return None
    for pattern in ("%d %b %Y", "%d %B %Y", "%d %b %y"):
        try:
            from datetime import datetime

            return datetime.strptime(raw.strip(), pattern).date()
        except ValueError:
            continue
    return None


def detect_type(text: str) -> DocumentType:
    lowered = text.lower()
    scores = {
        DocumentType.DISCHARGE_SUMMARY: sum(h in lowered for h in DISCHARGE_HINTS) * 2,
        DocumentType.LAB_REPORT: sum(h in lowered for h in LAB_HINTS),
        DocumentType.PRESCRIPTION: sum(h in lowered for h in RX_HINTS),
    }
    best = max(scores, key=lambda key: scores[key])
    return best if scores[best] >= 2 else DocumentType.OTHER


def document_date(text: str) -> date | None:
    labelled = re.search(
        r"\b(?:date|dated|reported on|collected on|admitted on|discharged on)\s*[:\-]?\s*([^\n]{4,24})",
        text,
        re.I,
    )
    for candidate in ([labelled[1]] if labelled else []) + [text]:
        for pattern in DATE_PATTERNS:
            match = pattern.search(candidate)
            if match:
                parsed = parse_date(match[1])
                if parsed:
                    return parsed
    return None


def compute_flag(value: str | None, reference_range: str | None) -> LabFlag | None:
    """Compare a value against a PRINTED range. Never infers a range."""
    if not value or not reference_range:
        return None
    try:
        numeric = float(re.sub(r"[^\d.]", "", value))
    except ValueError:
        return LabFlag.UNCLEAR
    bounds = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", reference_range)
    if not bounds:
        return LabFlag.UNCLEAR
    low, high = float(bounds[1]), float(bounds[2])
    if low > high:
        return LabFlag.UNCLEAR
    if numeric < low:
        return LabFlag.LOW
    if numeric > high:
        return LabFlag.HIGH
    return LabFlag.NORMAL


def _medication(line: str) -> Finding | None:
    cleaned = re.sub(r"\s+", " ", line).strip().lstrip("-•* ")
    if not MED_PREFIX.match(cleaned) and not DOSE.search(cleaned):
        return None
    body = MED_PREFIX.sub("", cleaned)
    dose, freq, dur = DOSE.search(body), FREQUENCY.search(body), DURATION.search(body)
    cut = min((m.start() for m in (dose, freq, dur) if m), default=len(body))
    name = re.sub(r"[,:;]+$", "", body[:cut]).strip()
    if len(name) < 3 or name.isdigit():
        return None
    attributes = {}
    if dose:
        attributes["dose"] = f"{dose[1]} {dose[2].lower()}"
    if freq:
        attributes["frequency"] = freq[1].upper()
    if dur:
        attributes["duration"] = f"{dur[1]} {dur[2].lower()}"
    return Finding(
        entity_type=ExtractedEntityType.MEDICATION,
        value=_title(name),
        attributes=attributes,
        confidence=0.75 if attributes else 0.55,
    )


def _investigation(line: str) -> Finding | None:
    cleaned = re.sub(r"\s+", " ", line).strip()
    match = LAB_LINE.match(cleaned)
    if not match:
        return None
    name, value, unit, ref = match[1], match[2], match[3], match[4]
    if DEMOGRAPHIC.match(name.strip()):
        return None
    if not unit and not ref:
        return None
    return Finding(
        entity_type=ExtractedEntityType.INVESTIGATION,
        value=_title(name.strip()),
        numeric_value=value,
        unit=unit.strip() if unit else None,
        reference_range=re.sub(r"\s+", "", ref) if ref else None,
        flag=compute_flag(value, ref),
        confidence=0.8 if ref else 0.6,
    )


def _labelled(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for entity_type, labels in LABELLED.items():
        pattern = re.compile(rf"^\s*(?:{'|'.join(labels)})\s*[:\-]\s*(.+)$", re.I | re.M)
        for match in pattern.finditer(text):
            for part in re.split(r"[,;]", match[1]):
                value = re.sub(r"\s+", " ", part).strip()
                if len(value) > 2:
                    findings.append(
                        Finding(entity_type=entity_type, value=value, confidence=0.8)
                    )
    return findings


# A lab unit is compound ("g/dL", "mg/dL", "/uL", "%"); a drug dose is not
# ("500 mg", "18 units"). This is what separates "Haemoglobin 10.2 g/dL" from
# "Metformin 500 mg", which both otherwise match a dose pattern.
LAB_UNIT = re.compile(r"[/%]")


def classify_line(line: str) -> Finding | None:
    """Decide what a single line is, most-certain signal first."""
    cleaned = re.sub(r"\s+", " ", line).strip()
    if not cleaned:
        return None

    # 1. An explicit dosage-form prefix means a medication, unambiguously.
    if MED_PREFIX.match(cleaned.lstrip("-•* ")):
        return _medication(cleaned)

    lab = _investigation(cleaned)
    # 2. A printed reference range means a lab result, unambiguously.
    if lab and lab.reference_range:
        return lab
    # 3. A compound unit means a measurement, not a dose.
    if lab and lab.unit and LAB_UNIT.search(lab.unit):
        return lab

    # 4. A dose with a frequency or duration reads as a prescription line.
    med = _medication(cleaned)
    if med and med.attributes.keys() & {"frequency", "duration"}:
        return med

    # 5. Otherwise prefer the lab reading if we got one, else the medication.
    return lab or med


def extract_by_rules(text: str) -> list[Finding]:
    """The always-available deterministic extractor."""
    findings = [
        finding
        for finding in (classify_line(line) for line in text.splitlines())
        if finding is not None
    ]
    findings.extend(_labelled(text))
    return _dedupe(findings)


def _dedupe(findings: list[Finding]) -> list[Finding]:
    seen: dict[tuple[str, str], Finding] = {}
    for finding in findings:
        existing = seen.get(finding.dedupe_key)
        # Keep whichever version carries more structure.
        if existing is None or finding.confidence > existing.confidence:
            seen[finding.dedupe_key] = finding
    return list(seen.values())


async def extract_with_ai(text: str) -> list[Finding]:
    """AI-assisted extraction. Returns [] on any failure."""
    provider = get_provider()
    if provider.name == "none":
        return []
    system, prompt = prompts.extract_document(ocr_text=text)
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=3000)
    except Exception as exc:  # noqa: BLE001 - never fatal
        log.warning("AI extraction failed: %s", exc)
        return []
    parsed = structured(DocumentExtraction, raw)
    if parsed is None:
        return []

    findings: list[Finding] = []
    for entity in parsed.entities:
        findings.append(
            Finding(
                entity_type=entity.entity_type,
                value=entity.value,
                attributes=dict(entity.attributes),
                numeric_value=entity.numeric_value,
                unit=entity.unit,
                reference_range=entity.reference_range,
                # Recompute the flag ourselves — never trust a model's reading
                # of a reference range.
                flag=compute_flag(entity.numeric_value, entity.reference_range),
                event_date=parse_date(entity.event_date),
                confidence=min(entity.confidence, 0.9),
                extractor="ai",
            )
        )
    return findings


async def extract(text: str) -> tuple[list[Finding], str]:
    """Rule-based findings, enriched by AI when it is available.

    @returns (findings, extractor_label)
    """
    rules = extract_by_rules(text)
    ai = await extract_with_ai(text)
    if not ai:
        return rules, "rules"
    # Rules win ties: they are reproducible and were computed from the text.
    merged = _dedupe([*ai, *rules])
    return merged, "rules+ai"


# --- Letterhead ------------------------------------------------------------
# Printed letterheads survive OCR well even when the handwriting below them
# does not, so they are worth reading properly: a scanned prescription can at
# least present its clinic, doctor and date cleanly.
#
# Every pattern here is deliberately strict. A wrong doctor's name shown as a
# fact is worse than a blank field, so anything that does not match a labelled
# or strongly-shaped line is left out and offered to the patient to fill in.

FACILITY_WORDS = (
    "hospital", "clinic", "polyclinic", "laboratory", "labs", "diagnostic",
    "institute", "centre", "center", "nursing home", "medical college",
    "health centre", "health center", "dispensary",
)

DEPARTMENT_WORDS = (
    "orthopaedics", "orthopedics", "cardiology", "medicine", "paediatrics",
    "pediatrics", "dermatology", "ophthalmology", "retina", "surgery",
    "gynaecology", "gynecology", "neurology", "ent", "dental", "out-patient",
    "outpatient", "opd", "radiology", "pathology",
)

# Indian medical qualifications, used to recognise a clinician line.
QUALIFICATIONS = (
    "MBBS", "MD", "MS", "DNB", "DM", "MCh", "DGO", "DCH", "DLO", "DVL",
    "BAMS", "BHMS", "BUMS", "BNYS", "DHMS", "MRCP", "FRCS", "DPM",
)

_DOCTOR = re.compile(
    r"\bDr\.?\s+([A-Z][A-Za-z.'\-]*(?:\s+[A-Z][A-Za-z.'\-]*){0,3})",
)
_QUALIFICATION = re.compile(
    r"\b(" + "|".join(QUALIFICATIONS) + r")\b(?:\s*\([^)]{1,30}\))?",
)
# A labelled patient name. Never inferred from an unlabelled line: on a
# prescription the handwritten name is exactly what OCR gets wrong.
_PATIENT = re.compile(
    r"^\s*(?:patient(?:'?s)?\s*name|patient|name)\s*[:\-]\s*([^\n]{2,60})$",
    re.I | re.M,
)
_PHONE = re.compile(r"\b(?:\+?91[\s-]?)?([6-9]\d{9})\b")


def _clean(value: str) -> str:
    return re.sub(r"\s{2,}", " ", value).strip(" .,:;-–—")


_FACILITY_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(w) for w in FACILITY_WORDS) + r")\b", re.I
)
_DEPARTMENT_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(w) for w in DEPARTMENT_WORDS) + r")\b", re.I
)


def letterhead(text: str) -> dict[str, str]:
    """Who issued this document, and when.

    @returns only the fields that could be read. A caller must treat a missing
             key as "not found", never as empty — the UI asks the patient to
             supply those rather than displaying a blank.
    """
    if not text:
        return {}

    lines = [_clean(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    found: dict[str, str] = {}

    # Facility: a line naming one, else an all-caps line near the top, which is
    # how nearly every Indian letterhead is set.
    for line in lines[:6]:
        if _FACILITY_RE.search(line):
            found["facility"] = line
            break
    else:
        for line in lines[:3]:
            letters = [c for c in line if c.isalpha()]
            if len(letters) >= 6 and all(c.isupper() for c in letters):
                found["facility"] = line.title()
                break

    # Clinician: requires an explicit "Dr", so a mangled name on its own is
    # never promoted to a doctor's name.
    for line in lines[:8]:
        match = _DOCTOR.search(line)
        if match:
            name = _QUALIFICATION.sub("", match[1])
            found["clinician"] = _clean(f"Dr. {_clean(name)}")
            quals = _QUALIFICATION.findall(line)
            if quals:
                found["qualifications"] = ", ".join(dict.fromkeys(quals))
            found["_clinician_line"] = line
            break

    # Department or clinic, when the letterhead names one separately.
    for line in lines[:8]:
        if line in (found.get("facility"), found.get("_clinician_line")):
            continue
        if _PATIENT.match(line):
            continue
        if _DEPARTMENT_RE.search(line) and len(line) <= 60:
            found["department"] = line
            break
    found.pop("_clinician_line", None)

    labelled_patient = _PATIENT.search(text)
    if labelled_patient:
        found["patient_name"] = _clean(labelled_patient[1])

    phone = _PHONE.search(text)
    if phone:
        found["phone"] = phone[1]

    return {key: value for key, value in found.items() if value}
