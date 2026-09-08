import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { forwardRef } from "react";
import { cn } from "@/lib/cn";

const buttonVariants = cva(
  cn(
    "inline-flex items-center justify-center gap-2 rounded-xl font-semibold",
    "transition-colors disabled:pointer-events-none disabled:opacity-55",
    // Kiosk-first: never smaller than a comfortable finger target.
    "min-h-touch",
  ),
  {
    variants: {
      variant: {
        primary: "bg-primary text-white hover:bg-primary-hover",
        secondary: "bg-surface text-ink border-2 border-line hover:border-primary hover:bg-primary-soft",
        subtle: "bg-primary-soft text-primary-ink hover:bg-primary-soft/70",
        ghost: "text-ink-muted hover:bg-surface-muted hover:text-ink",
        danger: "bg-danger text-white hover:bg-danger-ink",
      },
      size: {
        md: "px-5 py-3 text-base",
        lg: "px-7 py-4 text-lg",
        xl: "min-h-touch-lg px-8 py-5 text-xl",
        icon: "h-12 w-12 p-0",
      },
      block: { true: "w-full", false: "" },
    },
    defaultVariants: { variant: "primary", size: "md", block: false },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, block, asChild, type = "button", ...props }, ref) => {
    const Component = asChild ? Slot : "button";
    return (
      <Component
        ref={ref}
        type={asChild ? undefined : type}
        className={cn(buttonVariants({ variant, size, block }), className)}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";
