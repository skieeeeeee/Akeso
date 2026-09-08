/// <reference types="vite/client" />

/**
 * Build-time configuration read by the client.
 *
 * Declared explicitly rather than relying on Vite's index signature, so a
 * typo in a variable name is a type error rather than `undefined` at runtime.
 */
interface ImportMetaEnv {
  /**
   * Origin of the API, e.g. `https://medikiosk-api.onrender.com`.
   *
   * Empty or unset keeps every request same-origin, which is what the dev
   * proxy and a single-origin deployment both want. Set it only when the
   * frontend and the API are hosted separately.
   */
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
