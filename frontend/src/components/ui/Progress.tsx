import { Check } from "lucide-react";
import { cn } from "@/lib/cn";
import { useI18n } from "@/providers/I18nProvider";

export function ProgressBar({
  percent,
  label,
  className,
}: {
  percent: number;
  label?: string;
  className?: string;
}) {
  const clamped = Math.min(100, Math.max(0, Math.round(percent)));
  return (
    <div className={className}>
      <div
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label ?? "Progress"}
        className="h-2.5 w-full overflow-hidden rounded-full bg-line/60"
      >
        <div
          className="h-full rounded-full bg-primary transition-[width] duration-500"
          style={{ width: `${clamped}%` }}
        />
      </div>
      {label && <p className="mt-2 text-sm font-medium text-ink-muted">{label}</p>}
    </div>
  );
}

export type StepperItem = { key: string; label: string };

/**
 * Horizontal step indicator. Collapses to a compact "step N of M" on small
 * screens rather than shrinking to unreadable text.
 */
export function Stepper({
  steps,
  currentIndex,
  className,
}: {
  steps: StepperItem[];
  currentIndex: number;
  className?: string;
}) {
  const { t } = useI18n();
  return (
    <nav aria-label={t("stepperLabel")} className={className}>
      {/* Labelled pills need more room than `md` gives: at exactly 768px six
          of them pushed the page into horizontal scroll. They appear from
          `lg`, and the compact line below covers everything narrower. */}
      <ol className="hidden items-center gap-1 lg:flex">
        {steps.map((step, index) => {
          const done = index < currentIndex;
          const active = index === currentIndex;
          return (
            <li key={step.key} className="flex flex-1 items-center gap-2 last:flex-none">
              <span
                aria-current={active ? "step" : undefined}
                className={cn(
                  "flex items-center gap-2 whitespace-nowrap rounded-full px-3 py-1.5 text-sm font-semibold",
                  active && "bg-primary text-white",
                  done && "text-success-ink",
                  !active && !done && "text-ink-subtle",
                )}
              >
                <span
                  aria-hidden="true"
                  className={cn(
                    "flex h-6 w-6 items-center justify-center rounded-full border-2 text-xs",
                    active && "border-white/70 bg-white/15",
                    done && "border-success bg-success text-white",
                    !active && !done && "border-line",
                  )}
                >
                  {done ? <Check className="h-3.5 w-3.5" strokeWidth={3} /> : index + 1}
                </span>
                {step.label}
              </span>
              {index < steps.length - 1 && (
                <span
                  aria-hidden="true"
                  className={cn("h-0.5 flex-1 rounded", done ? "bg-success" : "bg-line")}
                />
              )}
            </li>
          );
        })}
      </ol>

      <p className="text-sm font-semibold text-ink-muted lg:hidden">
        {t("stepperPosition")
          .replace("{current}", String(Math.min(currentIndex + 1, steps.length)))
          .replace("{total}", String(steps.length))}
        {steps[currentIndex] && ` · ${steps[currentIndex].label}`}
      </p>
    </nav>
  );
}
