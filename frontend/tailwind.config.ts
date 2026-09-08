import type { Config } from "tailwindcss";

/**
 * Government-healthcare-inspired system: calm, high-contrast, familiar.
 * Colours are declared as CSS custom properties in index.css so high-contrast
 * mode can swap the whole palette without touching a single component.
 */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "rgb(var(--c-canvas) / <alpha-value>)",
        surface: "rgb(var(--c-surface) / <alpha-value>)",
        "surface-muted": "rgb(var(--c-surface-muted) / <alpha-value>)",
        line: "rgb(var(--c-line) / <alpha-value>)",
        ink: "rgb(var(--c-ink) / <alpha-value>)",
        "ink-muted": "rgb(var(--c-ink-muted) / <alpha-value>)",
        "ink-subtle": "rgb(var(--c-ink-subtle) / <alpha-value>)",
        primary: {
          DEFAULT: "rgb(var(--c-primary) / <alpha-value>)",
          hover: "rgb(var(--c-primary-hover) / <alpha-value>)",
          soft: "rgb(var(--c-primary-soft) / <alpha-value>)",
          ink: "rgb(var(--c-primary-ink) / <alpha-value>)",
        },
        success: {
          DEFAULT: "rgb(var(--c-success) / <alpha-value>)",
          soft: "rgb(var(--c-success-soft) / <alpha-value>)",
          ink: "rgb(var(--c-success-ink) / <alpha-value>)",
        },
        warning: {
          DEFAULT: "rgb(var(--c-warning) / <alpha-value>)",
          soft: "rgb(var(--c-warning-soft) / <alpha-value>)",
          ink: "rgb(var(--c-warning-ink) / <alpha-value>)",
        },
        danger: {
          DEFAULT: "rgb(var(--c-danger) / <alpha-value>)",
          soft: "rgb(var(--c-danger-soft) / <alpha-value>)",
          ink: "rgb(var(--c-danger-ink) / <alpha-value>)",
        },
      },
      borderRadius: {
        lg: "0.625rem",
        xl: "0.875rem",
        "2xl": "1.125rem",
      },
      boxShadow: {
        card: "0 1px 2px rgb(15 42 66 / 0.06), 0 1px 3px rgb(15 42 66 / 0.04)",
        lifted: "0 4px 12px rgb(15 42 66 / 0.08), 0 1px 3px rgb(15 42 66 / 0.06)",
      },
      // Minimum comfortable touch target on a kiosk.
      minHeight: { touch: "3.25rem", "touch-lg": "4.5rem" },
      maxWidth: { kiosk: "56rem", form: "34rem" },
    },
  },
  plugins: [],
} satisfies Config;
