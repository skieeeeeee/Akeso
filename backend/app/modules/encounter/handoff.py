"""The visit as a QR code the clinician scans.

Why this exists: the patient finished answering and was told their visit had
been "sent", then asked to wait. Nothing was actually delivered anywhere a
clinician could see it. A QR closes that loop with no shared network, no
integration and no waiting — the patient holds up their screen and the
clinician's phone has the visit.

Three decisions worth knowing.

**The payload is plain JSON, not compressed.** Compressing it would fit about
three times more data, but a compressed payload shows a generic phone camera
nothing but base64. Plain JSON means any camera app displays something a
clinician can read, which is the entire point of scanning rather than
integrating. It costs capacity, so the payload is built to a budget instead.

**A QR holds very little.** About 2.3 KB at the error correction level worth
using on a screen, and the full review payload is nearly 10 KB — mostly
six-language UI labels and legal text a clinician's phone does not need. So
this builds a separate clinician-facing document and, when a long visit still
overflows, sheds the least clinically useful parts in a fixed order and says
in the payload what it dropped. Nothing is ever silently lost.

**It carries no generated prose.** The review screen shows an AI-written
narrative; this deliberately does not. Handing a clinician a generated
paragraph invites reading it as a clinical impression, and the app must never
appear to diagnose. Structured patient-reported answers cannot be mistaken
for one.

Privacy, stated plainly: this is unencrypted health information in an image.
Anyone who photographs the screen has all of it. That is an acceptable trade
for a patient showing their own screen to their own clinician in the room —
the same exposure as handing over a paper prescription — and it is the reason
the mobile number and ABHA id are left out, since those are what would make a
leaked image linkable to other records. A deployment serving real patients
should put a signed, short-lived URL in the QR instead of the data.
"""

from __future__ import annotations

import io
import json
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.modules.ayush import service as ayush_service
from app.modules.encounter import service
from app.modules.encounter.models import Encounter
from app.modules.encounter.script import ENCOUNTER_SCRIPT
from app.modules.patient.models import Patient
from app.modules.red_flags import service as red_flag_service
from app.shared.enums import AnswerKind, Language

# Well under the ~2.2 KB a QR can physically hold, and deliberately so.
#
# Capacity is not the binding constraint — scannability is. Payload size sets
# the QR version, and version sets the module count: a full visit at 1868
# bytes produces a 169-module grid, which on a phone screen leaves barely two
# device pixels per module. Decoding the rendered output showed those large
# codes failing to read at all while codes around this size read dependably.
#
# So the budget is set where a code scans on the first try, and `_fit` sheds
# the least clinically useful parts to reach it. A clinician who scans and
# gets the visit beats one who gets a slightly fuller payload after three
# attempts at re-aiming.
QR_BUDGET_BYTES = 1200

# Said on the clinician's phone, not only on the patient's screen: this is
# what the patient reported, and it is not a diagnosis.
DISCLAIMER = "Patient-reported before consultation. Not a diagnosis."

SCHEMA_VERSION = 1


class QrTooLarge(ValueError):
    """The payload exceeds what a QR code can hold."""


def _iso(value: datetime | date | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    return value.isoformat()


def _severity(answer: str | None) -> str | None:
    """Normalise the 1-10 rating to "n/10" exactly once.

    The stored answer already carries the scale, so appending another gave a
    clinician "7/10/10".
    """
    if not answer:
        return None
    value = answer.strip()
    return value if "/" in value else f"{value}/10"


def _encode(payload: dict[str, Any]) -> bytes:
    """Compact separators only — the keys stay readable on a phone."""
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()


def build(db: Session, patient: Patient, encounter: Encounter) -> dict[str, Any]:
    """Assemble the clinician-facing document for one visit.

    @returns a JSON-ready dict that fits `QR_BUDGET_BYTES` once encoded. When
             the visit was too long to fit whole, `trimmed` lists what was
             left out, so the clinician knows to ask rather than assuming
             there was nothing more.
    """
    existing = service.existing_context(db, patient, encounter)

    answers: list[list[str]] = []
    severity: str | None = None
    skipped = 0

    for row in service.answers_for(db, encounter):
        question = ENCOUNTER_SCRIPT.question_by_id(row.question_id)
        answer = (row.normalized_answer or row.raw_answer or "").strip()
        if question is not None and question.target is None:
            continue  # a navigation gate carries no clinical value
        if not answer or answer == service.NONE_REPORTED:
            skipped += 1
            continue
        if question is not None and question.kind == AnswerKind.SCALE:
            severity = answer
            continue
        answers.append([row.question_text, answer])

    # Kept separate from today's answers: it is thirty-odd short findings, and
    # mixing them in buries the complaint the clinician is looking for. Read
    # in English regardless of the patient's language — the payload is for a
    # clinician, and the Sanskrit term travels as the key either way.
    recorded = ayush_service.recorded_for_review(
        ayush_service.get(db, patient), Language.ENGLISH
    )
    ayurveda: list[list[str]] = [
        [entry["term"], entry["answer"]] for entry in (recorded or {}).get("entries", [])
    ]

    state = red_flag_service.state_for(db, encounter)
    safety = {
        "status": state.status.value,
        # The category and the patient's own words, never the criteria that
        # matched them — the same boundary the red-flag API draws. The
        # patient-facing notice is left out too: it is guidance for them, in
        # six languages, and none of it is information for the clinician.
        "flags": [
            {"category": flag.category.value, "reported": flag.evidence}
            for flag in state.flags
        ],
    }

    payload: dict[str, Any] = {
        "medikiosk": SCHEMA_VERSION,
        "generated": _iso(datetime.now(timezone.utc)),
        "patient": {
            "name": patient.full_name,
            "age": patient.age,
            "sex": patient.gender.value if patient.gender is not None else None,
        },
        "visit": {
            "date": _iso(encounter.started_at),
            "type": encounter.visit_type.value if encounter.visit_type else None,
            "care_system": encounter.care_system.value if encounter.care_system else None,
            "priority": encounter.priority.value,
        },
        "complaint": encounter.chief_complaint,
        "severity": _severity(severity),
        "safety": safety,
        "answers": answers,
        "history": {
            "conditions": existing.conditions,
            "medications": existing.medications,
            "allergies": existing.allergies,
        },
        "ayurveda": ayurveda,
        "documents": [document["title"] for document in existing.recent_documents],
        "unanswered": skipped,
        "note": DISCLAIMER,
    }

    return _fit(payload)


def _fit(payload: dict[str, Any]) -> dict[str, Any]:
    """Shed the least clinically useful parts until the payload fits.

    The order is deliberate and the early steps are lossless in clinical
    terms: document titles and the Ayurvedic findings become counts, then the
    question wording goes (a clinician reading "Burning pain in both knees"
    does not need "What brings you here today?"), and only as a last resort
    are the oldest answers dropped.

    Never shed: who the patient is, the complaint, severity, the safety state,
    allergies, medications and conditions. If those alone did not fit there
    would be nothing worth encoding, and `trimmed` would say so.
    """
    trimmed: list[str] = []

    def record(name: str) -> None:
        trimmed.append(name)
        payload["trimmed"] = trimmed

    if len(_encode(payload)) <= QR_BUDGET_BYTES:
        return payload

    if payload.get("documents"):
        count = len(payload["documents"])
        payload["documents"] = f"{count} on file"
        record("document titles")
        if len(_encode(payload)) <= QR_BUDGET_BYTES:
            return payload

    if payload.get("ayurveda"):
        count = len(payload["ayurveda"])
        payload["ayurveda"] = f"{count} findings recorded"
        record("ayurvedic findings")
        if len(_encode(payload)) <= QR_BUDGET_BYTES:
            return payload

    if payload.get("answers"):
        payload["answers"] = [answer for _question, answer in payload["answers"]]
        record("question wording")
        if len(_encode(payload)) <= QR_BUDGET_BYTES:
            return payload

    # Drop from the front: the later answers are the more specific follow-ups.
    while payload.get("answers") and len(_encode(payload)) > QR_BUDGET_BYTES:
        payload["answers"] = payload["answers"][1:]
        if "earlier answers" not in trimmed:
            record("earlier answers")

    return payload


def as_svg(payload: dict[str, Any]) -> bytes:
    """Render the payload as a QR code in SVG.

    SVG rather than PNG for two reasons: it needs no image library, so this
    feature does not depend on the optional OCR extras; and it stays sharp at
    whatever size the screen is, which matters when a clinician is aiming a
    camera at a phone held at arm's length.

    @raises QrTooLarge if the payload still does not fit. `build` keeps it
            inside the budget, so this only fires if a caller hand-rolls a
            payload.
    """
    import qrcode
    import qrcode.image.svg
    from qrcode.exceptions import DataOverflowError

    code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        # Four modules is the quiet zone the QR specification requires, and it
        # is not decoration: at border=2 a decoder could not find this code at
        # all, at any size. Verified by decoding the rendered output.
        border=4,
        box_size=10,
    )
    code.add_data(_encode(payload).decode())
    try:
        code.make(fit=True)
    except DataOverflowError as exc:  # pragma: no cover - build() prevents this
        raise QrTooLarge(
            f"{len(_encode(payload))} bytes will not fit in a QR code."
        ) from exc

    image = code.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    buffer = io.BytesIO()
    image.save(buffer)
    return buffer.getvalue()
