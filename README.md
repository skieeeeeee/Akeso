# MediKiosk

Patient case-taking and medical-history platform for Indian healthcare settings.

A patient shares their health information at a kiosk before their appointment,
so the clinician already has their history when the consultation begins. The
product's core promise is what happens on the **second** visit: a returning
patient describes only what is wrong today. They never repeat their history.

| Area | Scope | Status |
| --- | --- | --- |
| 1 | Onboarding, accessibility engine, patient profile | Complete |
| 2 | Conversational history, voice, document intelligence, timeline | Complete |
| 3 | Returning-patient visits, red-flag safety, review & submission | Complete |
| 4 | Care-system choice — allopathy stays short, Ayurveda adds Dashavidha and Ashtasthana | Complete |
| 5 | Six languages end to end, including the deterministic clinical narratives | Complete |
| 6 | Public landing page with sourced statistics | Complete |

**639 tests pass** — 446 backend (pytest, against real PostgreSQL) and 193
frontend (vitest + React Testing Library).

---

## What it does

**First-time patient.** Welcome → language → mobile/OTP or demo login →
mock ABHA → progressive personal info → accessibility assessment →
rule-based experience recommendation → accept or customise → consent →
conversational medical history (voice/text/touch) → document upload with OCR →
timeline → review → confirm.

**Returning patient.** Login → recognised → personalised home with their
health summary → "what brings you here today?" → follow-up questions about
today only → continuous red-flag screening → review → submit.

**Safety.** Every answer is screened for presentations that need prompt
attention. A flagged visit is marked urgent, the patient is shown a hedged
emergency screen, and **the patient cannot clear the flag** — continuing to
answer is not an escape route.

---

## Requirements

- **PostgreSQL 14+** — required; there is no SQLite fallback
- **Python 3.11+**
- **Node 18.18+** (Node 18 supported: Vite 6 / Tailwind 3 / react-router 6)

Optional:

- `AI_PROVIDER=grok` for AI assistance. Everything works without it.
- Local OCR (`rapidocr-onnxruntime`, `pillow`, `numpy`) is the largest
  dependency here, ~130 MB with its models. It is declared in
  `backend/requirements.txt` and imported lazily: set `OCR_PROVIDER=off` and
  skip it, and uploads are still stored for the clinician to read.

---

## Run it locally

Five commands, from a clean clone:

```bash
cp .env.example backend/.env     # adjust DATABASE_URL if needed
make setup                       # venv + backend deps + frontend deps
make db-create                   # createdb medikiosk, medikiosk_test
make migrate                     # apply every migration
make seed                        # four fictional demo patients
```

Then, in two terminals:

```bash
make api    # http://127.0.0.1:8000  (API docs at /docs)
make web    # http://127.0.0.1:5173
```

Open **http://127.0.0.1:5173**. The web app proxies `/api` to the backend, so
there is no CORS setup and no absolute URLs anywhere in the client.

To sign in, open `/login` and click **Show** under "Or explore with a demo
patient" — the list is collapsed so the sign-in form stays the primary action.
No SMS is sent: if you use a real mobile number instead, the one-time code is
displayed on screen.

### Without make

`make` only wraps these. The same thing by hand:

```bash
# Backend
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
createdb medikiosk && createdb medikiosk_test
.venv/bin/alembic upgrade head
.venv/bin/python -m app.cli seed
.venv/bin/python -m uvicorn app.main:app --reload --port 8000

# Frontend, in another terminal
cd frontend
npm install
npm run dev
```

### Routes

| Path | Audience |
| --- | --- |
| `/` | Public landing page — what the product does, sourced statistics, log in / register |
| `/start` | The kiosk screen a clinic pins a tablet to (language, then begin) |
| `/login` | Mobile + one-time code, or a demo patient |
| `/home` | A recognised returning patient's personalised home |

### Resetting the demo

```bash
make reset && make seed     # or: python -m app.cli reset && python -m app.cli seed
```

Useful after a walkthrough leaves a visit half-finished or a language changed.

### Or with Docker

```bash
make docker-up      # Postgres + API + web on http://localhost:8080, seeded
make docker-down
```

The API container applies migrations on boot, so a fresh managed database is
usable immediately.

### Tests

```bash
make test            # everything (639)
make test-backend    # 446 tests, against medikiosk_test
make test-frontend   # 193 tests
make check           # typecheck the frontend
make build           # production build of the web app
```

---

## Demo patients

`make seed` creates four fictional patients with histories, medications,
allergies, submitted visits and **real processed documents** (23 extracted
findings in total). No real person, ABHA number or record is represented.

| Key | Patient | Demonstrates |
| --- | --- | --- |
| `standard` | Rajesh Kumar, 52 | Returning patient: 2 past visits, 2 processed records, full history. The main returning-patient demo. |
| `easy` | Kamla Devi, 71 | Easy Mode + audio guidance + Hindi, 1 past visit |
| `low_vision` | Anil Sharma, 45 | Extra-large text, high contrast, 1 previously-urgent visit |
| `incomplete` | Sunita Devi, 34 | Abandoned onboarding; resumes at the assessment |

Signing in with your own mobile number also works. No SMS is sent — the code
is returned by the API and shown inside an explicit "prototype" notice.

---

## Architecture

A modular monolith on each side of one HTTP boundary.

```
backend/app/
├── config/            settings (the only place env vars are read)
├── database/          declarative base, session, model registry
├── shared/            enums, errors, security, validators, storage, clinical
├── modules/           one folder per feature: models/schemas/service/router
│   ├── auth/          mocked OTP, JWT, demo sign-in
│   ├── patient/       identity, personal info, onboarding, home aggregate
│   ├── abha/          mock registry + linking
│   ├── accessibility/ assessment + deterministic recommendation engine
│   ├── consent/       versioned consent text, decisions, revocation
│   ├── medical_history/  the standing profile + structured history
│   ├── interview/     the conversation state engine + profile script
│   ├── encounter/     new-visit script, service, summary
│   ├── red_flags/     PRIVATE criteria, safety service, hedged content
│   ├── documents/     upload, OCR pipeline, extraction, findings
│   ├── ayush/         Dashavidha Pariksha, Ahara, Vihara
│   └── timeline/      chronological aggregation
└── services/
    ├── ai/            provider abstraction: null + Grok, strict schemas
    └── ocr/           provider boundary: plaintext, local ONNX, AI vision

frontend/src/
├── components/ui/     the design system (shadcn-compatible)
├── components/layout/ AppShell, StepLayout, AccessibilityBar
├── providers/         I18n, Auth, Preferences
├── features/          onboarding, interview, encounter, documents
├── pages/             one per screen
├── routes/            routing + auth/progress guards
├── services/          the single API client
└── types/api.ts       the API contract, mirrored from Pydantic
```

### Decisions worth knowing

**One engine, two scripts.** The conversation state machine
(`interview/engine.py`) is pure and takes a pluggable `Script`. The Phase 2
medical-history script and the Phase 3 encounter script are two
implementations, so branching, normalisation, retry and progress logic exist
once. It is fully testable without a model, a network or a database.

**A visit never rewrites history.** Encounter answers are written to
`Encounter.structured_history`; the medical profile is read-only during a
visit. There is a test asserting the profile is byte-for-byte unchanged after
a full visit that reports a medication change. Today's answers and existing
history stay visually distinct all the way to the summary.

**Red-flag criteria are private, by design.** `red_flags/rules.py` is the
only place the triggering patterns live. Nothing serialises them — not the
schemas, not error messages, not the OpenAPI document (there is a test that
greps the generated schema for trigger phrases). Publishing them would let a
patient dodge screening or fake an emergency, and would invite screening
heuristics to be read as diagnostic criteria.

**Priority ratchets one way.** There is no endpoint to clear a flag or lower
priority — a test enumerates every route to prove it. "Continue answering
while waiting" only records an acknowledgement, so triggering the emergency
path is never a way out of the interview.

**Age is derived, never stored.** `Patient.age` is computed from
`date_of_birth`. The assessment separately records `age_at_assessment`,
because the recommendation depended on it.

**The server owns progression.** Every step response carries
`onboarding_status`/`next_route` (or the next question). The client never
computes where to go, so a refresh, a back button or a different device all
resume in the same place. Progress only moves forward.

**Accessibility is applied once, at the document root.** `data-font-size`,
`data-contrast` and `data-mode` on `<html>` drive a rem scale and a CSS
custom-property palette. Easy Mode is a presentation change over the same
components and data — not a second copy of the UI.

**Localised clinical copy lives on the server.** Assessment questions,
consent text, interview questions, AYUSH factors and emergency wording are all
served by the API in both languages, so the clients cannot drift on clinical
wording. Only UI chrome is in the frontend string table.

**Every clinical fact carries provenance.** `ClinicalItem` records `source`,
`confidence`, `verified` and `document_id`. Patient statements, document
findings and prior records stay distinguishable end to end.

**Failures are states, not nulls.** `ProcessingStatus`,
`AbhaVerificationStatus` and `RedFlagStatus` are explicit, and a failed step
keeps whatever the patient entered. A rejected ABHA number stays in the field
with its reason; an unreachable registry offers "continue without it".

---

## Degradation

No workflow depends on an external service.

| Subsystem | Without it |
| --- | --- |
| **AI** (`AI_PROVIDER=none`, timeout, malformed output, refusal) | Rule-based question selection, regex document extraction, template summaries. `ai_fallback_active` tells the UI to say assistance is unavailable and that nothing was lost. |
| **Voice** (unsupported browser, denied mic, silence, network) | Typing and touch are always rendered; every failure gives an actionable message plus "type instead". Voice is never required. |
| **TTS** | Every instruction is on screen as text; the control simply hides. |
| **OCR** (no engine, unreadable scan) | The document is stored and shown to the clinician, marked `failed`/`needs_review` with a retry. Raw text is kept even when extraction finds nothing. |
| **ABHA** (invalid, rejected, registry down) | The entered value is preserved with its reason, and "continue without it" is always available. |
| **Network** | Typed `ApiError` with a patient-readable message and a retry; server-side progress is already saved. |
| **Duplicate submission** | Submit is idempotent — a repeat call returns the same encounter and timestamp. |

---

## Statistics on the landing page

Every figure is rendered with its source and year, because an unsourced health
number on a health product is worse than none: the 2-minute average
consultation *(Irving et al., BMJ Open 2017)*, diabetes and hypertension
prevalence *(ICMR-INDIAB 2023)*, NCD share of deaths *(WHO)* and out-of-pocket
share of health spending *(National Health Accounts)*.

The live ticker is **arithmetic, not a measurement** — the cited 2-minute
average divided into the visitor's time on the page — and the UI says so.

There is deliberately **no "deaths per minute from missed check-ups" counter**.
Nothing measures that, so it could only be invented, and a test asserts the
page contains no such implied mortality claim. Re-verify all figures against
the latest releases before presenting.

## Medical safety

The application collects and organises information. It does not diagnose,
prescribe, or claim certainty.

- Emergency wording says *"may require urgent medical attention"* and
  explicitly *"this does not confirm a medical condition"*. Tests assert no
  condition is ever named (no "heart attack", "stroke", "you have").
- Document findings are labelled *"information found in this document"*, start
  as `unreviewed`, and are **never** copied into the medical profile
  automatically.
- Lab flags are computed only against a range **printed on the document**. No
  range means no flag; an unparseable range means `unclear`.
- Narratives are generated from already-structured data, so prose cannot
  introduce a fact, and every one ends by stating it is not a diagnosis.
- **Drug-interaction flagging is deliberately not implemented.** Without a
  reliable interaction dataset, a fabricated warning is worse than none. The
  architecture is ready for it.

---

## Accessibility

Built for roughly 10–80+ year-olds, and it does not assume age implies
difficulty.

- The recommendation engine is **deterministic and rule-based** — never a
  model deciding someone's accessibility settings.
- **Age alone can never force Easy Mode.** The maximum age contribution (2) is
  below the Easy Mode threshold (3); low digital comfort alone does reach it.
- **Hearing difficulty disables audio guidance outright**, so nothing depends
  on sound, while visual accommodations still apply.
- Voluntary disclosures only; nothing sensitive is inferred or required.
- Every recommendation is explained in the patient's language and can be
  overridden immediately, then changed again from Settings without retaking
  the assessment.
- Status is never conveyed by colour alone — every badge carries text.
- Keyboard navigation, visible focus rings, semantic landmarks, `aria-invalid`
  and `aria-describedby` on every field, a skip link, and ≥44px touch targets.
- English and Hindi across buttons, instructions, questions, errors and
  emergency guidance. Adding a language means extending the `Language` enum
  and the two string tables.

---

## API

Base path `/api/v1`; interactive docs at `/docs`. **56 endpoints.**

### Auth & patient
| Method | Path |
| --- | --- |
| `POST` | `/auth/otp/request`, `/auth/otp/verify`, `/auth/demo-login` |
| `GET` | `/auth/demo-patients`, `/auth/me` |
| `GET`/`PATCH` | `/patients/me` |
| `GET` | `/patients/me/profile`, `/patients/me/home` |

### Onboarding
| Method | Path |
| --- | --- |
| `GET`/`POST` | `/patients/me/abha`, `/patients/me/abha/link`, `/patients/me/abha/skip` |
| `GET`/`POST` | `/accessibility/content`, `/accessibility/assessment` |
| `GET`/`PUT` | `/accessibility/preferences`, `/accessibility/recommendation` |
| `GET`/`POST` | `/consents/content`, `/consents`, `/consents/revoke` |

### Medical history & documents
| Method | Path |
| --- | --- |
| `GET`/`PUT` | `/patients/me/medical-profile`, `.../content`, `.../structured` |
| `POST` | `/interview/start`, `/interview/{id}/answer`, `/interview/{id}/back`, `/interview/{id}/confirm` |
| `GET` | `/interview/current`, `/interview/{id}`, `/interview/{id}/transcript`, `/interview/ai-status` |
| `GET`/`POST`/`DELETE` | `/patients/me/documents`, `.../{id}`, `.../{id}/file` |
| `POST` | `.../{id}/process`, `.../{id}/retry`, `.../{id}/findings/{item}` |
| `GET` | `.../{id}/status`, `/timeline` |
| `GET`/`PUT` | `/ayush/content`, `/ayush` |

### Visits & safety (Phase 3)
| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/encounters/start` | Begin or resume today's visit |
| `GET` | `/encounters/current`, `/encounters/{id}` | Current question + read-only history |
| `POST` | `/encounters/{id}/answer` | Record an answer; re-screens for red flags |
| `POST` | `/encounters/{id}/back` | Reopen the previous question |
| `GET` | `/encounters/{id}/safety` | Safety state (never the criteria) |
| `POST` | `/encounters/{id}/safety/acknowledge` | Patient continues; **does not clear the flag** |
| `POST` | `/encounters/{id}/safety/assistance` | Patient asks for immediate help |
| `GET` | `/encounters/{id}/review` | Pre-submission review |
| `POST` | `/encounters/{id}/submit` | Idempotent submission |

Errors always return `{"error": {"code", "message", "details"}}` with a
message safe to show a patient. Validation messages are specific — "Please
enter a valid 10-digit Indian mobile number", not "invalid input".

---

## Database

15 tables across three migrations. Each drops its own ENUM types on downgrade,
so `alembic downgrade base && alembic upgrade head` round-trips.

| Migration | Adds |
| --- | --- |
| `phase 1 foundation` | `patients`, `abha_profiles`, `accessibility_assessments`, `patient_preferences`, `consents`, `medical_profiles`, `encounters`, `documents`, `otp_challenges` |
| `phase 2 interview documents ayush` | `conversation_sessions`, `conversation_answers`, `extracted_medical_data`, `ayush_assessments`; 4 clinical sections on `medical_profiles` (12 total); OCR columns on `documents` |
| `phase 3 encounters red flags` | `red_flags`; `red_flag_status`, `red_flag_acknowledged_at`, `assistance_requested_at`, `submitted_at`, `patient_confirmed` on `encounters` |

Medical facts are provenance-carrying JSONB items, so patient statements,
document extraction and clinician verification share one shape.

---

## Environment variables

All optional except `DATABASE_URL`. See [.env.example](.env.example).

| Variable | Default | Notes |
| --- | --- | --- |
| `DATABASE_URL` | — | **Required.** PostgreSQL only. |
| `TEST_DATABASE_URL` | — | Used when `ENVIRONMENT=test`. |
| `ENVIRONMENT` | `development` | `development` \| `test` |
| `JWT_SECRET` | dev placeholder | **Change before any deployment.** |
| `ACCESS_TOKEN_TTL_MINUTES` | `720` | |
| `EXPOSE_MOCK_OTP` | `true` | Returns the OTP in the response. **Must be false with real patients.** |
| `OTP_TTL_SECONDS` / `OTP_MAX_ATTEMPTS` | `300` / `5` | |
| `ABHA_MOCK_MODE` | `true` | No ABDM call exists in this codebase. |
| `AI_PROVIDER` | `none` | `none` \| `grok`. `grok` with an empty key degrades to `none` with a warning; an unknown name fails loudly. |
| `AI_API_KEY` / `AI_MODEL` / `AI_BASE_URL` | — / `grok-4` / x.ai | Server-side only; never sent to the frontend. |
| `OCR_PROVIDER` | `auto` | `auto` \| `local` \| `ai` \| `off` |
| `MAX_UPLOAD_BYTES` | `10485760` | |
| `UPLOAD_DIR` | `backend/var/uploads` | Mount a volume here. |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Only needed for a cross-origin frontend. |

---

## Deploying

Compatible with Vercel (frontend), Railway/Render (backend) and managed
PostgreSQL.

**Backend** — deploy `backend/` with its Dockerfile. Set `DATABASE_URL`,
`JWT_SECRET`, `EXPOSE_MOCK_OTP=false`, and `CORS_ORIGINS` to the frontend
origin. Migrations run on boot. Mount a volume at `/app/var` so uploaded
documents survive restarts. Health check: `GET /health`.

**Frontend** — `npm run build` and serve `dist/`. On Vercel, add a rewrite
from `/api/:path*` to the backend so the browser stays same-origin. With the
bundled Dockerfile, set `API_URL` and nginx proxies `/api` for you.

**Secrets** — nothing is baked into the image; every value comes from the
environment. `.env` files are git-ignored, and no key is exposed to the client.

---

## Known limitations

- **Drug-interaction flagging is not implemented** (see Medical safety).
- **Backend speech-to-text is not implemented.** Voice uses the browser's
  Web Speech API, so it depends on browser support (Chrome/Edge are reliable;
  Firefox is not). The provider boundary for a server-side Whisper is in
  place. This is why voice is never mandatory.
- **Red-flag screening is a triage heuristic**, tuned to over- rather than
  under-refer. It screens the patient's own free text; it is not a clinical
  scoring instrument and has not been clinically validated.
- **Mock ABHA only.** Format validation with reserved identifiers for the
  failure paths; no ABDM network call anywhere.
- **No doctor-facing UI.** The schema, provenance and review states are shaped
  for one, but the clinician view is not built.
- **Prototype authentication.** OTP delivery is mocked and there is no RBAC;
  every endpoint is scoped to the signed-in patient, which is the right
  boundary but not a substitute for production auth.
- **AI cost/latency is untuned.** With `AI_PROVIDER=grok` each answer may
  trigger a model call; there is no batching or caching.
- **PDF uploads are stored but not OCR'd** — the local engine handles images
  and text. A PDF is preserved and shown to the clinician as-is.
