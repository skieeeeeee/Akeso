import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { FileText, Info, PlusCircle, Upload } from "lucide-react";
import { useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Field, Input, Select } from "@/components/ui/Field";
import { EmptyState, Spinner } from "@/components/ui/States";
import { DocumentCard } from "@/features/documents/DocumentCard";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { stepperItems } from "@/features/onboarding/steps";
import type { DocumentList, DocumentType } from "@/types/api";

const TYPE_LABELS: Record<DocumentType, "documentTypePrescription" | "documentTypeLabReport" | "documentTypeDischarge" | "documentTypeOther"> = {
  prescription: "documentTypePrescription",
  lab_report: "documentTypeLabReport",
  discharge_summary: "documentTypeDischarge",
  other: "documentTypeOther",
};

export function RecordsPage() {
  const { t, language } = useI18n();
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();
  const fileInput = useRef<HTMLInputElement>(null);

  const isOnboarding = location.pathname.startsWith("/onboarding");
  const [documentType, setDocumentType] = useState<DocumentType>("prescription");
  const [title, setTitle] = useState("");

  const documents = useQuery({
    queryKey: ["documents"],
    queryFn: () => api.get<DocumentList>("/patients/me/documents"),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["documents"] });

  const upload = useMutation({
    mutationFn: (file: File): Promise<{ id: string }> => {
      const form = new FormData();
      form.append("file", file);
      form.append("document_type", documentType);
      if (title.trim()) form.append("title", title.trim());
      return api.upload<{ id: string }>("/patients/me/documents", form);
    },
    onSuccess: async (created) => {
      setTitle("");
      if (fileInput.current) fileInput.current.value = "";
      try {
        await api.post(`/patients/me/documents/${(created as { id: string }).id}/process`);
      } catch {
        // A processing failure is a document state, not an upload failure.
      }
      void invalidate();
    },
  });

  const remove = useMutation({
    mutationFn: (id: string) => api.del(`/patients/me/documents/${id}`),
    onSuccess: invalidate,
  });

  const uploadSection = (
    <div className="space-y-4">
      {upload.error && (
        <Alert tone="danger">
          {upload.error instanceof ApiError ? upload.error.message : t("errorGeneric")}
        </Alert>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label={t("recordsTypeLabel")}>
          {({ inputId }) => (
            <Select
              id={inputId}
              value={documentType}
              onChange={(event) => setDocumentType(event.target.value as DocumentType)}
            >
              {(Object.keys(TYPE_LABELS) as DocumentType[]).map((value) => (
                <option key={value} value={value}>
                  {t(TYPE_LABELS[value])}
                </option>
              ))}
            </Select>
          )}
        </Field>

        <Field label={t("recordsTitleLabel")} hint={t("recordsTitleHint")}>
          {({ inputId, describedBy }) => (
            <Input
              id={inputId}
              aria-describedby={describedBy}
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="e.g. Blood Test, Prescription 2026"
            />
          )}
        </Field>
      </div>

      <div>
        <input
          ref={fileInput}
          type="file"
          accept="image/png,image/jpeg,image/webp,application/pdf"
          className="sr-only"
          id="record-file"
          aria-label={t("recordsChooseFile")}
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) upload.mutate(file);
          }}
        />
        <Button
          size="lg"
          block
          disabled={upload.isPending}
          onClick={() => fileInput.current?.click()}
        >
          {upload.isPending ? (
            <Spinner label={t("recordsUploading")} className="text-white" />
          ) : (
            <>
              <Upload className="h-5 w-5" aria-hidden="true" />
              {t("recordsChooseFile")}
            </>
          )}
        </Button>
      </div>

      {/* Set expectations before the upload, not after it fails: scanning
          reads printed documents well and handwriting usually not at all. */}
      <p className="text-sm text-ink-muted">{t("recordsScanNote")}</p>

      {documents.isLoading ? (
        <Spinner label={t("loading")} />
      ) : documents.data && documents.data.total > 0 ? (
        <div className="space-y-3 pt-2">
          <h2 className="text-base font-semibold text-ink">
            {t("profileRecords")} ({documents.data.total})
          </h2>
          <ul className="space-y-3">
            {documents.data.documents.map((document) => (
              <li key={document.id}>
                <DocumentCard document={document} onDelete={(id) => remove.mutate(id)} />
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <EmptyState
          icon={<FileText className="h-6 w-6" />}
          title={t("recordsEmptyTitle")}
          description={t("recordsEmptyBody")}
        />
      )}
    </div>
  );

  if (isOnboarding) {
    return (
      <AppShell>
        <StepLayout
          steps={stepperItems(language)}
          currentIndex={5}
          title={t("recordsHeading")}
          description={t("recordsBody")}
          onNext={() => navigate("/onboarding/complete")}
          onBack={() => navigate("/onboarding/medical-profile")}
          nextLabel={t("continue")}
          secondaryAction={
            <Button variant="ghost" size="md" onClick={() => navigate("/onboarding/complete")}>
              {t("skip")}
            </Button>
          }
          aside={
            <Card>
              <CardHeader title={t("profileRecords")} icon={<Info className="h-5 w-5" />} />
              <CardBody>
                <p className="text-sm text-ink-muted">{t("recordsStoredNote")}</p>
              </CardBody>
            </Card>
          }
        >
          {uploadSection}
        </StepLayout>
      </AppShell>
    );
  }

  return (
    <AppShell wide backRoute="/home" backLabel={t("backToHome")}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("recordsPortalTitle")}</h1>
          <p className="mt-1 text-base text-ink-muted">{t("recordsPortalBody")}</p>
        </div>

        <Card>
          <CardHeader title={t("recordsHeading")} icon={<PlusCircle className="h-5 w-5" />} />
          <CardBody>
            {uploadSection}
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
