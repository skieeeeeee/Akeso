import { useEffect, useRef, useState } from "react";
import { Maximize2, X } from "lucide-react";

import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/States";
import { apiBase, authHeaders } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";

/**
 * The finished visit as a QR code for the clinician to scan.
 *
 * This replaces being told the visit had been "sent" and asked to wait.
 * Nothing was actually delivered anywhere a clinician could see, so the
 * patient waited for something that was never going to arrive. Now they hold
 * up their screen and it is in the clinician's hand.
 *
 * The code is fetched as SVG rather than drawn in the browser: the payload is
 * assembled server-side from the visit record, so there is one definition of
 * what a handoff contains, and SVG scales without blurring — which matters,
 * because a full visit produces a dense 161x161 module grid that needs to be
 * displayed large to scan comfortably. Hence the enlarge button.
 *
 * It carries the visit itself, not a link, so the clinician's phone needs no
 * network and no app beyond its camera.
 */
export function HandoffCode({
  encounterId,
  onKind,
}: {
  encounterId: string;
  /** Reports whether the code carries a link or the visit data itself. */
  onKind?: (kind: "link" | "data") => void;
}) {
  const { t } = useI18n();
  const [svg, setSvg] = useState<string | null>(null);
  // "link" opens a page on the clinician's phone; "data" carries the visit
  // inside the code itself. The two make different promises to the patient,
  // so the screen must not guess.
  const [kind, setKind] = useState<"link" | "data" | null>(null);
  const [failed, setFailed] = useState(false);
  const [enlarged, setEnlarged] = useState(false);

  const onKindRef = useRef(onKind);
  onKindRef.current = onKind;

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setFailed(false);
      try {
        const response = await fetch(
          `${apiBase}/encounters/${encounterId}/handoff.svg`,
          { headers: authHeaders() },
        );
        if (!response.ok) throw new Error(String(response.status));
        const markup = await response.text();
        const header = response.headers.get("x-handoff-kind");
        if (!cancelled) {
          setSvg(markup);
          const resolved = header === "link" || header === "data" ? header : null;
          setKind(resolved);
          if (resolved) onKindRef.current?.(resolved);
        }
      } catch {
        if (!cancelled) setFailed(true);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [encounterId]);

  // The SVG comes from our own API and contains only a generated path, but it
  // is still markup: rendering it through an <img> data URL rather than
  // innerHTML means nothing inside it can execute. encodeURIComponent rather
  // than btoa because the payload carries names in Indic scripts, which btoa
  // cannot encode.
  const source = svg ? `data:image/svg+xml;utf8,${encodeURIComponent(svg)}` : null;

  if (failed) {
    return (
      <Alert tone="warning" title={t("handoffFailedTitle")}>
        {t("handoffFailedBody")}
      </Alert>
    );
  }

  if (!source) {
    return (
      <div className="py-6">
        <Spinner label={t("loading")} />
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Sized deliberately, not aesthetically. Decoding the rendered output
          showed this code reading reliably at about 4 device pixels per
          module and not at all at 3, which for its 133-module grid means
          roughly 530px. So it takes the full column width up to 34rem and
          the enlarge view goes edge to edge. */}
      <div className="mx-auto w-full max-w-[34rem] rounded-2xl border-2 border-line bg-white p-3">
        {/* White background regardless of theme: a QR needs the contrast, and
            a dark-mode inversion is not reliably scannable. */}
        <img
          src={source}
          alt={t("handoffCodeAlt")}
          className="h-auto w-full"
          width={544}
          height={544}
        />
      </div>

      {kind === "data" && (
        <p className="text-center text-sm text-ink-subtle">{t("handoffOfflineNote")}</p>
      )}

      <div className="flex flex-wrap items-center justify-center gap-2">
        <Button variant="secondary" size="md" onClick={() => setEnlarged(true)}>
          <Maximize2 className="h-4 w-4" aria-hidden="true" />
          {t("handoffEnlarge")}
        </Button>
      </div>

      {enlarged && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={t("handoffCodeAlt")}
          className="fixed inset-0 z-50 flex flex-col items-center justify-center gap-4 bg-white p-4"
        >
          <img
            src={source}
            alt={t("handoffCodeAlt")}
            className="h-auto w-full max-w-[min(96vw,96vh)]"
          />
          <Button size="lg" onClick={() => setEnlarged(false)}>
            <X className="h-5 w-5" aria-hidden="true" />
            {t("close")}
          </Button>
        </div>
      )}
    </div>
  );
}