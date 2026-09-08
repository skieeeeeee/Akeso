import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

export function Card({
  children,
  className,
  as: Component = "section",
}: {
  children: ReactNode;
  className?: string;
  as?: "section" | "div" | "article" | "aside";
}) {
  return (
    <Component
      className={cn(
        // min-w-0: a grid/flex item defaults to `min-width: auto`, so without
        // this a card refuses to shrink below its content and overflows a
        // narrow viewport.
        "min-w-0 rounded-2xl border border-line bg-surface shadow-card",
        className,
      )}
    >
      {children}
    </Component>
  );
}

export function CardHeader({
  title,
  description,
  icon,
  action,
  className,
}: {
  title: ReactNode;
  description?: ReactNode;
  icon?: ReactNode;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <header
      className={cn(
        // flex-wrap + min-w-0: without them a long title beside an action
        // button forces the card past a narrow viewport.
        "flex flex-wrap items-start justify-between gap-x-4 gap-y-2 border-b border-line px-5 py-4 sm:px-6",
        className,
      )}
    >
      <div className="flex min-w-0 flex-1 items-start gap-3">
        {icon && (
          <span
            aria-hidden="true"
            className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"
          >
            {icon}
          </span>
        )}
        <div className="min-w-0">
          <h2 className="text-lg font-semibold leading-tight text-ink">{title}</h2>
          {description && <p className="mt-1 text-sm text-ink-muted">{description}</p>}
        </div>
      </div>
      {action}
    </header>
  );
}

export function CardBody({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={cn("px-5 py-5 sm:px-6", className)}>{children}</div>;
}

export function CardFooter({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <footer
      className={cn(
        "flex flex-col-reverse gap-3 border-t border-line px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6",
        className,
      )}
    >
      {children}
    </footer>
  );
}
