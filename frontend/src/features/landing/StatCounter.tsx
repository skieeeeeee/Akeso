import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/cn";
import { useI18n } from "@/providers/I18nProvider";
import type { Statistic } from "./statistics";

/**
 * A figure that counts up when it scrolls into view.
 *
 * Two accessibility properties matter here:
 *
 * 1. `prefers-reduced-motion` skips the animation entirely and shows the
 *    final number — an animating number is genuinely unpleasant for some
 *    vestibular conditions.
 * 2. The accessible name is always the *final* value, so a screen reader
 *    announces "101 million people…" once rather than every intermediate
 *    frame.
 */
export function StatCounter({
  statistic,
  className,
}: {
  statistic: Statistic;
  className?: string;
}) {
  const { s, t } = useI18n();
  const ref = useRef<HTMLDivElement>(null);
  const [shown, setShown] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node || done) return;

    const reduceMotion =
      typeof window !== "undefined" &&
      window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    if (reduceMotion) {
      setShown(statistic.value);
      setDone(true);
      return;
    }

    // IntersectionObserver is missing in jsdom and some older browsers; show
    // the final value rather than leaving a zero on screen.
    if (typeof IntersectionObserver === "undefined") {
      setShown(statistic.value);
      setDone(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries[0]?.isIntersecting) return;
        observer.disconnect();
        setDone(true);

        const duration = 1100;
        const start = performance.now();
        const tick = (now: number) => {
          const progress = Math.min(1, (now - start) / duration);
          // Ease-out: fast at first, settling on the real number.
          const eased = 1 - (1 - progress) ** 3;
          setShown(Math.round(statistic.value * eased));
          if (progress < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      },
      { threshold: 0.4 },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [statistic.value, done]);

  const unit = s(statistic.unit);
  // Screen readers get the whole sentence, so the "~" glyph has to be read
  // as a word — and that word needs translating like any other.
  const accessibleValue = `${statistic.approximate ? `${t("statApproximately")} ` : ""}${
    statistic.value
  }${unit ? ` ${unit}` : ""}`;

  return (
    <div ref={ref} className={cn("space-y-2", className)}>
      <p className="flex items-baseline gap-1.5">
        {/* The live number is hidden from assistive tech; the label below
            carries the full sentence instead. */}
        <span aria-hidden="true" className="text-4xl font-bold tabular-nums text-primary sm:text-5xl">
          {statistic.approximate && <span className="text-2xl align-top">~</span>}
          {shown.toLocaleString("en-IN")}
        </span>
        {unit && (
          <span aria-hidden="true" className="text-lg font-semibold text-primary-ink">
            {unit}
          </span>
        )}
      </p>
      <p className="text-base font-medium text-ink">
        <span className="sr-only">{accessibleValue} — </span>
        {s(statistic.label)}
      </p>
      <p className="text-sm text-ink-muted">{s(statistic.detail)}</p>
      {/* The source is part of the claim, so it is rendered with it. */}
      <p className="text-xs text-ink-subtle">
        {statistic.source} · {statistic.year}
      </p>
    </div>
  );
}
