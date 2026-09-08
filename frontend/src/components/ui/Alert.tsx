import { AlertTriangle, CheckCircle2, Info, ShieldAlert } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { Button } from "./Button";

type Tone = "info" | "success" | "warning" | "danger";

const TONE_STYLES: Record<Tone, { box: string; icon: ReactNode }> = {
  info: {
    box: "border-primary/30 bg-primary-soft text-primary-ink",
    icon: <Info className="h-5 w-5" aria-hidden="true" />,
  },
  success: {
    box: "border-success/30 bg-success-soft text-success-ink",
    icon: <CheckCircle2 className="h-5 w-5" aria-hidden="true" />,
  },
  warning: {
    box: "border-warning/35 bg-warning-soft text-warning-ink",
    icon: <AlertTriangle className="h-5 w-5" aria-hidden="true" />,
  },
  danger: {
    box: "border-danger/35 bg-danger-soft text-danger-ink",
    icon: <ShieldAlert className="h-5 w-5" aria-hidden="true" />,
  },
};

export function Alert({
  tone = "info",
  title,
  children,
  action,
  className,
}: {
  tone?: Tone;
  title?: ReactNode;
  children?: ReactNode;
  action?: { label: string; onClick: () => void };
  className?: string;
}) {
  const style = TONE_STYLES[tone];
  return (
    <div
      // Errors and warnings must be announced when they appear.
      role={tone === "danger" || tone === "warning" ? "alert" : "status"}
      className={cn("rounded-2xl border-2 p-4", style.box, className)}
    >
      <div className="flex items-start gap-3">
        <span className="mt-0.5 shrink-0">{style.icon}</span>
        <div className="min-w-0 flex-1">
          {title && <p className="font-semibold leading-snug">{title}</p>}
          {children && <div className={cn("text-base", title && "mt-1")}>{children}</div>}
        </div>
        {action && (
          <Button variant="secondary" size="md" onClick={action.onClick} className="shrink-0">
            {action.label}
          </Button>
        )}
      </div>
    </div>
  );
}
