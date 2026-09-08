import { useEffect, useState } from "react";
import { Clock } from "lucide-react";
import { useI18n } from "@/providers/I18nProvider";
import { CONSULTATION_SECONDS, consultationsInElapsed } from "./statistics";

/**
 * A live figure derived from the cited 2-minute average.
 *
 * It is explicitly arithmetic, not an event feed: "a doctor working at
 * India's 2-minute average would have seen N patients while you read this."
 * That keeps it truthful — we are not claiming to observe anything.
 */
export function LiveTicker() {
  const { t } = useI18n();
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const started = Date.now();
    // One tick per consultation, not per second: a number that changes every
    // second reads as a live feed, which this is not.
    const id = window.setInterval(
      () => setElapsed(Math.floor((Date.now() - started) / 1000)),
      1000,
    );
    return () => window.clearInterval(id);
  }, []);

  const consultations = consultationsInElapsed(elapsed);
  const minutes = Math.floor(elapsed / 60);
  const seconds = elapsed % 60;
  const readable = minutes > 0 ? `${minutes} min ${seconds} s` : `${seconds} s`;

  return (
    <div className="rounded-2xl border-2 border-primary/25 bg-primary-soft px-5 py-4">
      <p className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-primary-ink">
        <Clock className="h-4 w-4" aria-hidden="true" />
        {t("landingTickerLabel")}
      </p>
      {/* aria-live so the change is announced, but politely and rarely. */}
      <p className="mt-2 text-lg text-primary-ink" aria-live="polite">
        {t("landingTickerBefore")}{" "}
        <strong className="tabular-nums">{readable}</strong>{" "}
        {t("landingTickerMiddle")}{" "}
        <strong className="text-2xl tabular-nums">{consultations}</strong>{" "}
        {t("landingTickerAfter")}
      </p>
      <p className="mt-2 text-xs text-primary-ink/80">
        {t("landingTickerBasis")} ({CONSULTATION_SECONDS / 60} min · Irving et al., BMJ Open 2017)
      </p>
    </div>
  );
}
