import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import {
  AlertTriangle,
  ClipboardList,
  FileText,
  History,
  Leaf,
  Stethoscope,
} from "lucide-react";

import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";

/**
 * What a clinician sees after scanning the patient's code.
 *
 * Deliberately outside the signed-in app. The person holding the phone has no
 * account here, and the token in the URL is their authorisation — it names one
 * visit and expires within the hour. So this page reads nothing from the
 * session, writes nothing back, and offers no navigation into the rest of the
 * product.
 *
 * It is in English only, and that is not an oversight: the interface language
 * belongs to the patient, and the reader here is a different person whose
 * language we do not know. English is the language of the prescriptions and
 * signage around them.
 */

type Scanned = {
  medikiosk: number;
  generated: string;
  patient: { name: string | null; age: number | null; sex: string | null };
  visit: {
    date: string | null;
    type: string | null;
    care_system: string | null;
    priority: string;
  };
  complaint: string | null;
  severity: string | null;
  safety: { status: string; flags: { category: string; reported: string }[] };
  answers: [string, string][] | string[];
  history: { conditions: string[]; medications: string[]; allergies: string[] };
  ayurveda: [string, string][] | string;
  documents: string[] | string;
  unanswered: number;
  note: string;
  trimmed?: string[];
};

const humanise = (value: string | null) =>
  value ? value.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase()) : null;

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-0.5 border-b border-line py-2 last:border-0">
      <dt className="text-sm text-ink-muted">{label}</dt>
      <dd className="text-base font-medium text-ink">{value}</dd>
    </div>
  );
}

function List({ items }: { items: string[] }) {
  if (items.length === 0) {
    return <p className="text-base text-ink-muted">None recorded</p>;
  }
  return (
    <ul className="flex flex-wrap gap-2">
      {items.map((item, index) => (
        <li
          key={`${item}-${index}`}
          className="rounded-full border border-line bg-surface-muted px-3 py-1 text-sm font-medium text-ink"
        >
          {item}
        </li>
      ))}
    </ul>
  );
}

export function ScannedVisitPage() {
  const { token = "" } = useParams();

  const scanned = useQuery({
    queryKey: ["scanned-visit", token],
    queryFn: () => api.get<Scanned>(`/encounters/handoff/${token}`),
    enabled: Boolean(token),
    retry: false,
  });

  if (scanned.isLoading) return <LoadingPanel label="Opening the visit…" />;

  if (scanned.isError) {
    return (
      <div className="mx-auto max-w-2xl p-4">
        <ErrorPanel
          title="This code cannot be opened"
          message={
            scanned.error instanceof ApiError
              ? scanned.error.message
              : "Please ask the patient to show a new code."
          }
        />
      </div>
    );
  }

  const data = scanned.data!;
  const urgent = data.safety.status === "active" || data.visit.priority === "urgent";
  const pairs = data.answers.every((entry) => Array.isArray(entry))
    ? (data.answers as [string, string][])
    : (data.answers as string[]).map((answer, index) => [`Answer ${index + 1}`, answer] as [string, string]);

  return (
    <div className="mx-auto max-w-2xl space-y-4 p-4 pb-12">
      <header className="space-y-1">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary">
          MediKiosk · pre-consultation
        </p>
        <h1 className="text-2xl font-bold text-ink">
          {data.patient.name ?? "Patient"}
        </h1>
        <p className="text-base text-ink-muted">
          {[
            data.patient.age !== null ? `${data.patient.age} years` : null,
            humanise(data.patient.sex),
            humanise(data.visit.type),
            humanise(data.visit.care_system),
          ]
            .filter(Boolean)
            .join(" · ")}
        </p>
      </header>

      {/* States the limit of what this is before any content is read. */}
      <Alert tone="info">{data.note}</Alert>

      {urgent && (
        <Alert tone="danger" title="Flagged for early review">
          The patient reported something that raised a safety flag during
          screening. This is a prompt to look sooner, not an assessment.
        </Alert>
      )}

      <Card>
        <CardHeader
          title="Today's concern"
          icon={<Stethoscope className="h-5 w-5" />}
        />
        <CardBody>
          <p className="text-lg font-medium text-ink">
            {data.complaint ?? "Not recorded"}
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            {data.severity && (
              <Badge tone="neutral">Severity {data.severity}</Badge>
            )}
            <Badge tone={urgent ? "danger" : "neutral"}>
              {humanise(data.visit.priority)}
            </Badge>
            {data.unanswered > 0 && (
              <Badge tone="neutral">{data.unanswered} not answered</Badge>
            )}
          </div>
          {data.safety.flags.length > 0 && (
            <dl className="mt-4">
              {data.safety.flags.map((flag, index) => (
                <Row
                  key={`${flag.category}-${flag.reported}-${index}`}
                  label={humanise(flag.category) ?? "Flag"}
                  value={`“${flag.reported}”`}
                />
              ))}
            </dl>
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader
          title="What the patient said"
          icon={<ClipboardList className="h-5 w-5" />}
        />
        <CardBody>
          <dl>
            {pairs.map(([question, answer], index) => (
              <Row key={`${question}-${index}`} label={question} value={answer} />
            ))}
          </dl>
        </CardBody>
      </Card>

      <Card>
        <CardHeader
          title="Standing history"
          icon={<History className="h-5 w-5" />}
        />
        <CardBody className="space-y-4">
          <div className="space-y-2">
            <p className="text-sm font-semibold text-ink-subtle">Allergies</p>
            <List items={data.history.allergies} />
          </div>
          <div className="space-y-2">
            <p className="text-sm font-semibold text-ink-subtle">Medications</p>
            <List items={data.history.medications} />
          </div>
          <div className="space-y-2">
            <p className="text-sm font-semibold text-ink-subtle">Conditions</p>
            <List items={data.history.conditions} />
          </div>
        </CardBody>
      </Card>

      {Array.isArray(data.ayurveda) && data.ayurveda.length > 0 && (
        <Card>
          <CardHeader
            title="Ayurvedic examination"
            icon={<Leaf className="h-5 w-5" />}
          />
          <CardBody>
            <dl>
              {data.ayurveda.map(([term, answer], index) => (
                <Row key={`${term}-${index}`} label={term} value={answer} />
              ))}
            </dl>
          </CardBody>
        </Card>
      )}

      {Array.isArray(data.documents) && data.documents.length > 0 && (
        <Card>
          <CardHeader
            title="Records on file"
            icon={<FileText className="h-5 w-5" />}
          />
          <CardBody>
            <List items={data.documents} />
          </CardBody>
        </Card>
      )}

      {data.trimmed && data.trimmed.length > 0 && (
        <Alert tone="warning" title="Not everything is shown">
          {`Left out to fit: ${data.trimmed.join(", ")}.`}
        </Alert>
      )}

      <footer className="flex items-start gap-2 px-1 pt-2 text-sm text-ink-subtle">
        <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
        <p>
          Recorded by the patient before the consultation, and shown here
          because they chose to share it. This link expires shortly.
        </p>
      </footer>
    </div>
  );
}
