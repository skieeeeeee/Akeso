import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    // The API is same-origin in development, so no CORS handling or absolute
    // URLs are needed anywhere in the client.
    proxy: {
      "/api": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/health": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    css: false,
    // Each file gets its own process. With the default threads pool, files
    // share `globalThis`, so one file's `unstubAllGlobals()` tore down
    // another file's stubbed `fetch` mid-test.
    pool: "forks",
    testTimeout: 15_000,
  },
});
