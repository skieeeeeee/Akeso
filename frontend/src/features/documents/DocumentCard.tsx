import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Check,
  ChevronDown,
  FileText,
  RefreshCw,
  ScanLine,
  Trash2,
  TriangleAlert,
  X,
} from "lucide-react";
import { useState } from "react";
import { Alert } from "@/components/ui/Alert";
import { Badge, StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { Spinner } from "@/components/ui/States";
import { api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { LAB_FLAG_TONE, labFlagLabel } from "@/lib/enumLabels";
import type { MedicalDocument, ReviewState } from "@/types/api";

/**
 * One uploaded record: its processing state, and the findings read from it.
 *
 * Findings are presented as "information found in this document" with an
 * explicit accept/reject, never as confirmed clinical facts.
 */

const ENTITY_LABELS: Record<string, { en: string; hi: string }> = {
  diagnosis: { en: "Condition mentioned", hi: "उल्लिखित बीमारी" },
  medication: { en: "Medicine", hi: "दवा" },
  investigation: { en: "Test result", hi: "जाँच परिणाम" },
  surgery: { en: "Operation", hi: "ऑपरेशन" },
  procedure: { en: "Procedure", hi: "प्रक्रिया" },
  allergy: { en: "Allergy", hi: "एलर्जी" },
  vital: { en: "Vital sign", hi: "जीवन संकेत" },
  note: { en: "Note", hi: "टिप्पणी" },
};

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function DocumentCard({
  document,
  onDelete,
}: {
  document: MedicalDocument;
  onDelete?: (id: string) => void;
}) {
  const { t, s, v, language } = useI18n();
  const queryClient = useQueryClient();
  const [showText, setShowText] = useState(false);

  const invalidate = () => {
    void queryClient.invalidateQueries({ queryKey: ["documents"] });
    void queryClient.invalidateQueries({ queryKey: ["timeline"] });
    void queryClient.invalidateQueries({ queryKey: ["structured-history"] });
  };

  const process = useMutation({
    mutationFn: () => api.post(`/patients/me/documents/${document.id}/process`),
    onSuccess: invalidate,
  });

  const retry = useMutation({
    mutationFn: () => api.post(`/patients/me/documents/${document.id}/retry`),
    onSuccess: invalidate,
  });

  const review = useMutation({
    mutationFn: ({ itemId, state }: { itemId: string; state: ReviewState }) =>
      api.post(`/patients/me/documents/${document.id}/findings/${itemId}`, {
        review_state: state,
      }),
    onSuccess: invalidate,
  });

  const findings = document.extracted_items ?? [];

  // Only the fields that were actually read, in reading order.
  const head = document.extracted_data?.letterhead ?? {};
  const details = (
    [
      [t("docFacility"), head.facility],
      [
        t("docClinician"),
        head.clinician && head.qualifications
          ? `${head.clinician} · ${head.qualifications}`
          : head.clinician,
      ],
      [t("docDepartment"), head.department],
      [t("docPatientName"), head.patient_name],
      [t("docDate"), document.document_date ?? undefined],
      [t("docPhone"), head.phone],
    ] as const
  )
    .filter((entry): entry is readonly [string, string] => Boolean(entry[1]))
    .map(([label, value]) => ({ label, value }));
  const status = document.processing_status;
  const busy = process.isPending || retry.isPending;


  return (
    <Card>
      <CardBody className="space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex min-w-0 items-start gap-3">
            <span
              aria-hidden="true"
              className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"
            >
              <FileText className="h-5 w-5" />
            </span>
            <div className="min-w-0">
              <p className="truncate font-semibold text-ink">
                {document.title || document.file_name}
              </p>
              <p className="text-sm text-ink-muted">
                {v(document.document_type)} · {formatSize(document.size_bytes)}
                {document.document_date ? ` · ${document.document_date}` : ""}
              </p>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <StatusBadge status={status} label={v(status)} />
            {onDelete && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onDelete(document.id)}
                aria-label={`${t("remove")}: ${document.title || document.file_name}`}
              >
                <Trash2 className="h-5 w-5" aria-hidden="true" />
              </Button>
            )}
          </div>
        </div>

        {/* Explain the state rather than showing a bare spinner. */}
        {busy && <Spinner label={t("docProcessing")} />}

        {!busy && status === "pending" && (
          <Button variant="secondary" onClick={() => process.mutate()}>
            <ScanLine className="h-5 w-5" aria-hidden="true" />
            {t("docRead")}
          </Button>
        )}

        {!busy && (status === "failed" || status === "needs_review") && (
          <Alert
            tone={status === "failed" ? "warning" : "info"}
            title={status === "failed" ? undefined : t("docNoFindings")}
          >
            {status === "failed" && document.processing_error && (
              <p>{document.processing_error}</p>
            )}
            <Button variant="secondary" size="md" className="mt-3" onClick={() => retry.mutate()}>
              <RefreshCw className="h-5 w-5" aria-hidden="true" />
              {t("docRetry")}
            </Button>
          </Alert>
        )}

        {/* What the printed letterhead says. Shown for any document that
            yielded something, including one whose handwriting was unreadable —
            the clinic, doctor and date are usually still legible and are worth
            presenting properly instead of leaving the patient with raw text.
            Absent fields are omitted rather than shown blank. */}
        {details.length > 0 && (
          <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
            <p className="font-semibold text-ink">{t("docDetailsHeading")}</p>
            <p className="text-sm text-ink-muted">{t("docDetailsNote")}</p>
            <dl className="mt-3 grid gap-x-6 gap-y-2 sm:grid-cols-2">
              {details.map(({ label, value }) => (
                <div key={label} className="min-w-0">
                  <dt className="text-xs uppercase tracking-wide text-ink-subtle">
                    {label}
                  </dt>
                  <dd className="break-words text-base font-medium text-ink">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
        )}

        {findings.length > 0 && (
          <div className="space-y-3">
            <div>
              <p className="font-semibold text-ink">{t("docFindings")}</p>
              <p className="text-sm text-ink-muted">{t("docFindingsNote")}</p>
            </div>

            <ul className="space-y-2">
              {findings.map((item) => (
                <li
                  key={item.id}
                  className="flex flex-wrap items-start justify-between gap-3 rounded-xl border border-line bg-surface-muted px-4 py-3"
                >
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="font-medium text-ink">{item.value}</p>
                      {item.flag && (
                        <Badge tone={LAB_FLAG_TONE[item.flag]}>
                          {labFlagLabel(item.flag, language)}
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-ink-subtle">
                      {s(ENTITY_LABELS[item.entity_type] ?? { en: item.entity_type, hi: item.entity_type })}
                      {item.numeric_value
                        ? ` · ${item.numeric_value} ${item.unit ?? ""}`
                        : ""}
                      {item.reference_range ? ` · ref ${item.reference_range}` : ""}
                      {item.attributes.dose ? ` · ${item.attributes.dose}` : ""}
                      {item.attributes.frequency ? ` · ${item.attributes.frequency}` : ""}
                    </p>
                  </div>

                  {item.review_state === "unreviewed" ? (
                    <div className="flex w-full flex-wrap gap-2 sm:w-auto sm:flex-nowrap">
                      <Button
                        variant="secondary"
                        size="md"
                        className="flex-1 sm:flex-none"
                        disabled={review.isPending}
                        onClick={() => review.mutate({ itemId: item.id, state: "accepted" })}
                      >
                        <Check className="h-4 w-4" aria-hidden="true" />
                        {t("docAccept")}
                      </Button>
                      <Button
                        variant="ghost"
                        size="md"
                        className="flex-1 sm:flex-none"
                        disabled={review.isPending}
                        onClick={() => review.mutate({ itemId: item.id, state: "rejected" })}
                      >
                        <X className="h-4 w-4" aria-hidden="true" />
                        {t("docReject")}
                      </Button>
                    </div>
                  ) : (
                    <Badge tone={item.review_state === "accepted" ? "success" : "neutral"}>
                      {item.review_state === "accepted" ? t("docAccepted") : t("docRejected")}
                    </Badge>
                  )}
                </li>
              ))}
            </ul>

            {findings.some((item) => item.entity_type === "investigation" && item.flag) && (
              <p className="flex items-start gap-2 text-sm text-ink-subtle">
                <TriangleAlert className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                {t("labDisclaimer")}
              </p>
            )}
          </div>
        )}

        {/* Raw OCR text stays available even when extraction found nothing. */}
        {document.ocr_text && (
          <div>
            <Button variant="ghost" size="md" onClick={() => setShowText((current) => !current)}>
              <ChevronDown
                className={`h-5 w-5 transition-transform ${showText ? "rotate-180" : ""}`}
                aria-hidden="true"
              />
              {t("docRawText")}
            </Button>
            {showText && (
              <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap rounded-xl border border-line bg-surface-muted p-4 text-sm text-ink-muted">
                {document.ocr_text}
              </pre>
            )}
          </div>
        )}
      </CardBody>
    </Card>
  );
}
