import { Loader2 } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { Alert } from "./Alert";
import { Button } from "./Button";

export function Spinner({ className, label }: { className?: string; label?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-ink-muted">
      <Loader2 className={cn("h-5 w-5 animate-spin", className)} aria-hidden="true" />
      {label && <span>{label}</span>}
    </span>
  );
}

/** Full-panel loading state. Announced politely so it is not silent. */
export function LoadingPanel({ label = "Loading…" }: { label?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="flex min-h-[12rem] flex-col items-center justify-center gap-3 rounded-2xl border border-line bg-surface p-8 text-center"
    >
      <Loader2 className="h-8 w-8 animate-spin text-primary" aria-hidden="true" />
      <p className="text-base font-medium text-ink-muted">{label}</p>
    </div>
  );
}

/** Error state with a retry affordance. Never shows a raw technical message. */
export function ErrorPanel({
  title = "Something went wrong",
  message,
  onRetry,
  retryLabel = "Try again",
}: {
  title?: string;
  message: string;
  onRetry?: () => void;
  retryLabel?: string;
}) {
  return (
    <Alert tone="danger" title={title}>
      <p>{message}</p>
      {onRetry && (
        <Button variant="secondary" size="md" onClick={onRetry} className="mt-3">
          {retryLabel}
        </Button>
      )}
    </Alert>
  );
}

/**
 * Empty state. Always carries a next action — an empty panel with no guidance
 * is the thing the design brief rules out.
 */
export function EmptyState({
  icon,
  title,
  description,
  action,
  className,
  /**
   * Render the title as the page heading. Off by default because most empty
   * states sit inside a card that already has a heading above it — but a page
   * whose whole content is an empty state still needs an h1.
   */
  asPageHeading = false,
}: {
  icon?: ReactNode;
  title: string;
  description: string;
  action?: ReactNode;
  className?: string;
  asPageHeading?: boolean;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center gap-3 rounded-2xl border-2 border-dashed border-line bg-surface-muted px-6 py-8 text-center",
        className,
      )}
    >
      {icon && (
        <span
          aria-hidden="true"
          className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-soft text-primary"
        >
          {icon}
        </span>
      )}
      <div>
        {asPageHeading ? (
          <h1 className="text-xl font-bold text-ink">{title}</h1>
        ) : (
          <p className="text-base font-semibold text-ink">{title}</p>
        )}
        <p className="mx-auto mt-1 max-w-md text-sm text-ink-muted">{description}</p>
      </div>
      {action}
    </div>
  );
}
