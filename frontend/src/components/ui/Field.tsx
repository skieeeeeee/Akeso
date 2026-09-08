import * as LabelPrimitive from "@radix-ui/react-label";
import { AlertCircle } from "lucide-react";
import { forwardRef, useId, type ReactNode } from "react";
import { cn } from "@/lib/cn";

/**
 * A labelled form control. The label, hint and error are wired to the input
 * with `aria-describedby`/`aria-invalid` so screen readers announce them,
 * which is why every form in the app goes through this component.
 */
export function Field({
  label,
  hint,
  error,
  required,
  children,
  htmlFor,
  className,
}: {
  label: ReactNode;
  hint?: ReactNode;
  error?: string | null;
  required?: boolean;
  children: (ids: { inputId: string; describedBy: string | undefined; invalid: boolean }) => ReactNode;
  htmlFor?: string;
  className?: string;
}) {
  const generated = useId();
  const inputId = htmlFor ?? generated;
  const hintId = `${inputId}-hint`;
  const errorId = `${inputId}-error`;
  const describedBy = [hint ? hintId : null, error ? errorId : null]
    .filter(Boolean)
    .join(" ") || undefined;

  return (
    <div className={cn("space-y-2", className)}>
      <LabelPrimitive.Root
        htmlFor={inputId}
        className="block text-base font-semibold text-ink"
      >
        {label}
        {required && (
          <span className="ml-1 text-danger" aria-hidden="true">
            *
          </span>
        )}
        {!required && (
          <span className="ml-2 text-sm font-normal text-ink-subtle">(optional)</span>
        )}
      </LabelPrimitive.Root>

      {hint && (
        <p id={hintId} className="text-sm text-ink-muted">
          {hint}
        </p>
      )}

      {children({ inputId, describedBy, invalid: Boolean(error) })}

      {error && (
        <p id={errorId} role="alert" className="flex items-start gap-1.5 text-sm font-medium text-danger-ink">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
          {error}
        </p>
      )}
    </div>
  );
}

export const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "min-h-touch w-full rounded-xl border-2 border-line bg-surface px-4 py-3 text-lg text-ink",
        "placeholder:text-ink-subtle",
        "aria-[invalid=true]:border-danger",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";

export const Textarea = forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn(
      "w-full rounded-xl border-2 border-line bg-surface px-4 py-3 text-base text-ink",
      "placeholder:text-ink-subtle aria-[invalid=true]:border-danger",
      className,
    )}
    {...props}
  />
));
Textarea.displayName = "Textarea";

export const Select = forwardRef<
  HTMLSelectElement,
  React.SelectHTMLAttributes<HTMLSelectElement>
>(({ className, children, ...props }, ref) => (
  <select
    ref={ref}
    className={cn(
      "min-h-touch w-full rounded-xl border-2 border-line bg-surface px-4 py-3 text-lg text-ink",
      "aria-[invalid=true]:border-danger",
      className,
    )}
    {...props}
  >
    {children}
  </select>
));
Select.displayName = "Select";
