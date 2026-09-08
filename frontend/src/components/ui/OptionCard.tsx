import { Check } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

/**
 * The primary way a patient answers anything: a large, tappable card.
 *
 * Rendered as a real radio/checkbox input so keyboard navigation, screen
 * readers and form semantics all work without extra ARIA wiring.
 */
export function OptionCard({
  name,
  value,
  label,
  help,
  icon,
  checked,
  multiple,
  onSelect,
  className,
}: {
  name: string;
  value: string;
  label: ReactNode;
  help?: ReactNode;
  icon?: ReactNode;
  checked: boolean;
  multiple?: boolean;
  onSelect: (value: string) => void;
  className?: string;
}) {
  return (
    <label
      className={cn(
        "group relative flex min-h-touch-lg cursor-pointer items-center gap-4 rounded-2xl border-2 bg-surface p-4 sm:p-5",
        "transition-colors hover:border-primary hover:bg-primary-soft/50",
        "has-[:focus-visible]:ring-4 has-[:focus-visible]:ring-primary/35",
        checked ? "border-primary bg-primary-soft" : "border-line",
        className,
      )}
    >
      <input
        type={multiple ? "checkbox" : "radio"}
        name={name}
        value={value}
        checked={checked}
        onChange={() => onSelect(value)}
        className="sr-only"
      />

      {icon && (
        <span
          aria-hidden="true"
          className={cn(
            "flex h-12 w-12 shrink-0 items-center justify-center rounded-xl transition-colors",
            checked ? "bg-primary text-white" : "bg-surface-muted text-primary",
          )}
        >
          {icon}
        </span>
      )}

      <span className="min-w-0 flex-1">
        <span className="block text-lg font-semibold leading-snug text-ink">{label}</span>
        {help && <span className="mt-1 block text-base text-ink-muted">{help}</span>}
      </span>

      <span
        aria-hidden="true"
        className={cn(
          "flex h-7 w-7 shrink-0 items-center justify-center border-2 transition-colors",
          multiple ? "rounded-md" : "rounded-full",
          checked ? "border-primary bg-primary text-white" : "border-line bg-surface",
        )}
      >
        {checked && <Check className="h-5 w-5" strokeWidth={3} />}
      </span>
    </label>
  );
}

export function OptionGrid({
  children,
  columns = 1,
  className,
}: {
  children: ReactNode;
  columns?: 1 | 2 | 3;
  className?: string;
}) {
  return (
    <div
      role="group"
      className={cn(
        "grid gap-3",
        columns === 2 && "sm:grid-cols-2",
        columns === 3 && "sm:grid-cols-2 lg:grid-cols-3",
        className,
      )}
    >
      {children}
    </div>
  );
}
