import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LoginPage } from "./LoginPage";
import { PATIENT, SESSION, errorResponse, jsonResponse, renderWithProviders, route, stubFetch } from "@/test/utils";

const DEMO_PATIENTS = [
  {
    demo_key: "standard",
    label: { en: "Rajesh Kumar · 52", hi: "राजेश कुमार · 52" },
    description: { en: "Returning patient", hi: "पुराने मरीज़" },
    mobile_number: "9812340001",
  },
];

const OTP = {
  mobile_number: "9812300001",
  expires_at: "2026-01-01T00:05:00Z",
  expires_in_seconds: 300,
  is_prototype_delivery: true,
  prototype_code: "123456",
};

afterEach(() => vi.unstubAllGlobals());

describe("LoginPage", () => {
  it("shows the server's validation message for a bad number", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/otp/request", () =>
        errorResponse("Please enter a valid 10-digit Indian mobile number."),
      ),
    ]);
    renderWithProviders(<LoginPage />);

    await user.type(screen.getByLabelText(/mobile number/i), "5551234567");
    await user.click(screen.getByRole("button", { name: /send code/i }));

    expect(
      await screen.findByText("Please enter a valid 10-digit Indian mobile number."),
    ).toBeInTheDocument();
  });

  it("keeps the send button disabled until the number is long enough", async () => {
    const user = userEvent.setup();
    stubFetch([route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS))]);
    renderWithProviders(<LoginPage />);

    const button = screen.getByRole("button", { name: /send code/i });
    expect(button).toBeDisabled();
    await user.type(screen.getByLabelText(/mobile number/i), "98123");
    expect(button).toBeDisabled();
    await user.type(screen.getByLabelText(/mobile number/i), "00001");
    expect(button).toBeEnabled();
  });

  it("moves to the code step and asks the patient to type it", async () => {
    // Presented as an ordinary sign-in: no banner, no code on screen, and
    // nothing pre-filled. The code is fixed server-side and deliberately not
    // returned to the client on the deployment, so it is neither displayed
    // nor visible in the network response.
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/otp/request", () => jsonResponse(OTP)),
    ]);
    renderWithProviders(<LoginPage />);

    await user.type(screen.getByLabelText(/mobile number/i), "9812300001");
    await user.click(screen.getByRole("button", { name: /send code/i }));

    expect((await screen.findAllByText(/code sent to/i)).length).toBeGreaterThan(0);
    // Empty, so the patient enters it themselves.
    expect(screen.getByLabelText(/one-time code/i)).toHaveValue("");
    // And no leftover prototype scaffolding on the screen.
    expect(screen.queryByText(/prototype/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/does not send sms/i)).not.toBeInTheDocument();
  });

  it("reports an incorrect code without clearing the screen", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/otp/request", () => jsonResponse(OTP)),
      route("/auth/otp/verify", () =>
        errorResponse("That code is not correct. 4 attempt(s) left.", 401, "authentication_failed"),
      ),
    ]);
    renderWithProviders(<LoginPage />);

    await user.type(screen.getByLabelText(/mobile number/i), "9812300001");
    await user.click(screen.getByRole("button", { name: /send code/i }));
    await user.type(await screen.findByLabelText(/one-time code/i), "000000");
    await user.click(screen.getByRole("button", { name: /verify and continue/i }));

    expect(await screen.findByText(/that code is not correct/i)).toBeInTheDocument();
    // Still on the code screen, so the patient can simply retype.
    expect(screen.getByLabelText(/one-time code/i)).toBeInTheDocument();
  });

  it("lets the patient go back and change the number", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/otp/request", () => jsonResponse(OTP)),
    ]);
    renderWithProviders(<LoginPage />);

    await user.type(screen.getByLabelText(/mobile number/i), "9812300001");
    await user.click(screen.getByRole("button", { name: /send code/i }));
    await user.click(await screen.findByRole("button", { name: /use a different number/i }));

    expect(screen.getByLabelText(/mobile number/i)).toBeInTheDocument();
  });

  it("signs in on a correct code", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/otp/request", () => jsonResponse(OTP)),
      route("/auth/otp/verify", () => jsonResponse({ ...SESSION, patient: PATIENT, is_new_patient: true })),
    ]);
    renderWithProviders(<LoginPage />);

    await user.type(screen.getByLabelText(/mobile number/i), "9812300001");
    await user.click(screen.getByRole("button", { name: /send code/i }));
    await user.type(await screen.findByLabelText(/one-time code/i), "123456");
    await user.click(screen.getByRole("button", { name: /verify and continue/i }));

    await waitFor(() =>
      expect(window.localStorage.getItem("medikiosk.token")).toBe(SESSION.access_token),
    );
  });

  it("offers demo patients and says they are fictional", async () => {
    stubFetch([route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS))]);
    renderWithProviders(<LoginPage />);

    expect(await screen.findByText("Rajesh Kumar · 52")).toBeInTheDocument();
    expect(screen.getByText(/no real patient data/i)).toBeInTheDocument();
  });

  it("explains when demo patients have not been seeded", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/auth/demo-patients", () => jsonResponse(DEMO_PATIENTS)),
      route("/auth/demo-login", () =>
        errorResponse("Demo patient not found", 404, "not_found"),
      ),
    ]);
    renderWithProviders(<LoginPage />);

    await user.click(await screen.findByText("Rajesh Kumar · 52"));
    expect(await screen.findByText(/demo patient not found/i)).toBeInTheDocument();
  });
});
