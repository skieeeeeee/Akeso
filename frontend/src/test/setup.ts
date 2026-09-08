import { afterEach } from "vitest";
import "@testing-library/jest-dom/vitest";
import { configure } from "@testing-library/react";

// Raised from the 1s default: test files run in parallel, and a slow
// resolution under load is not a product failure.
configure({ asyncUtilTimeout: 5_000 });

// The interface language is remembered in localStorage, so a test that
// switches language would otherwise leak it into every test after it in the
// same file. Reset it, rather than making each test defend itself.
afterEach(() => {
  try {
    window.localStorage.clear();
  } catch {
    /* not available in every environment */
  }
});
