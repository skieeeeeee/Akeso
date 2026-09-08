import { cva, type VariantProps } from "class-variance-authority";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-semibold",
  {
    variants: {
      tone: {
        neutral: "bg-surface-muted text-ink-muted border border-line",
        info: "bg-primary-soft text-primary-ink",
        success: "bg-success-soft text-success-ink",
        warning: "bg-warning-soft text-warning-ink",
        danger: "bg-danger-soft text-danger-ink",
      },
    },
    defaultVariants: { tone: "neutral" },
  },
);

export function Badge({
  children,
  tone,
  icon,
  className,
}: VariantProps<typeof badgeVariants> & {
  children: ReactNode;
  icon?: ReactNode;
  className?: string;
}) {
  return (
    <span className={cn(badgeVariants({ tone }), className)}>
      {icon && <span aria-hidden="true">{icon}</span>}
      {children}
    </span>
  );
}

/** Maps every backend status value onto one consistent visual language. */
const STATUS_TONES: Record<string, VariantProps<typeof badgeVariants>["tone"]> = {
  verified: "success",
  completed: "success",
  granted: "success",
  linked: "success",
  pending: "warning",
  processing: "warning",
  needs_review: "warning",
  sometimes: "warning",
  unverified: "neutral",
  skipped: "neutral",
  declined: "neutral",
  revoked: "neutral",
  failed: "danger",
  yes: "danger",
};

export function StatusBadge({ status, label }: { status: string; label?: string }) {
  return (
    <Badge tone={STATUS_TONES[status] ?? "neutral"}>
      {label ?? status.replace(/_/g, " ")}
    </Badge>
  );
}
