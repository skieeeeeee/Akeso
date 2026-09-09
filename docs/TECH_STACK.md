# MediKiosk — the stack, and why

Every technology in this repository, the alternatives that were on the table,
and the reason this one won. Versions are exact and taken from the lock files,
not from memory.

Two constraints shaped nearly every choice, so they are worth stating first:

1. **Node 18.20.8** is the runtime available here. That is not a preference —
   it rules out Vite 7, Tailwind 4 and react-router 7, all of which require
   Node 20+. Several "why not the newest?" answers below are just this.
2. **A 512 MB free instance** runs the API, with the OCR models loaded. Every
   dependency is weighed against that ceiling.

And one product constraint: the app is for patients on mid-range phones over
mobile data, in six languages including three Indic scripts, and it must
degrade to something useful when the network, the AI provider or the speech
provider is unavailable.

---

## Runtime and language

| Chosen | Version | Alternatives | Why this one |
| --- | --- | --- | --- |
| **Python** | 3.11 | Node/TypeScript backend, Go, Java | The OCR and AI ecosystem is Python-first. `rapidocr-onnxruntime` has no real JS equivalent, and a Node backend would have meant a second service just to read documents. 3.11 rather than 3.12+ because `python:3.11-slim` is what the OCR wheels are reliably built for. |
| **TypeScript** | 5.7.3 | JavaScript, Flow | The API contract is large and localised: `Localised` records, six-language enums, provenance-carrying clinical items. Types caught real bugs here (a wrong enum key is invisible until a patient sees it). |
| **Node** | 18.20.8 | Node 20/22 | Not chosen — imposed. It caps Vite, Tailwind and react-router as noted above. |

**Why not one language for both?** A single TypeScript stack would be
operationally simpler. It was rejected because document reading is the
product's differentiator and lives in Python.

---

## Backend

| Chosen | Version | Alternatives | Why this one |
| --- | --- | --- | --- |
| **FastAPI** | 0.115.6 | Django, Flask, Litestar | Pydantic-native request/response validation, which is the whole point here: a medical payload is validated at the boundary and never trusted. Django's ORM and admin bring weight this doesn't need; Flask would mean assembling validation, OpenAPI and async by hand. |
| **Uvicorn** (standard) | 0.34.0 | Gunicorn + workers, Hypercorn | One async worker fits a 512 MB instance. Gunicorn's process model would multiply the OCR models in memory. |
| **Pydantic** | 2.10.5 | dataclasses + manual validation, attrs, marshmallow | v2's Rust core matters when every response carries six-language records. `structured()` uses it as the gate that stops raw model output reaching the database. |
| **pydantic-settings** | 2.7.1 | `os.environ` reads, python-decouple | Settings are typed and validated at startup, which is how `DATABASE_URL` rewriting and the prototype-auth warnings work. |
| **SQLAlchemy** | 2.0.36 (ORM, typed) | Django ORM, SQLModel, raw psycopg, Tortoise | 2.0's `Mapped[...]` style gives real types on models. SQLModel was tempting (Pydantic + SQLAlchemy in one) but it blurs the line between the API contract and the storage schema — and that line is load-bearing here: `stored` vs `machine` answers must never be conflated. |
| **Alembic** | 1.14.0 | Django migrations, hand-written SQL, no migrations | Needed for a real reason: native Postgres ENUMs. Adding a language requires `ALTER TYPE ... ADD VALUE`, which is exactly the class of change that broke silently once — four languages were added in code and never migrated. `tests/test_migrations.py` now asserts enum parity across 16 enums. |
| **psycopg** | 3.2.3 (binary) | psycopg2, asyncpg | v3 is the maintained line and speaks the same DBAPI SQLAlchemy expects. asyncpg is faster but SQLAlchemy's async ORM would have meant async sessions throughout for no measured gain at this scale. |
| **PostgreSQL** | 16 | SQLite, MySQL, MongoDB | Native ENUMs, JSONB for extracted document data, and real constraints. SQLite was seriously considered for a kiosk — rejected because Render's filesystem is ephemeral on free instances, so a file database would vanish on restart. |
| **PyJWT** | 2.10.1 | python-jose, authlib, opaque DB tokens | Small and does one thing. It also made the handoff capability token trivial: a signed, scoped, short-lived token needed no new table. Opaque DB tokens would be revocable — a real advantage, and the right move if this went live. |
| **httpx** | 0.28.1 | requests, aiohttp | Async, and the same client for the AI provider, ElevenLabs and tests. `requests` is sync-only, which would block the event loop on a 30-second vision call. |
| **qrcode** | 8.0 | segno, python-barcode, client-side JS | Pure Python, and renders SVG without Pillow — which keeps the visit handoff out of the optional OCR extras. Generating server-side means one definition of what a handoff contains. |

**Why a modular monolith and not microservices?** Every feature lives in
`app/modules/<feature>/{models,schemas,service,router}.py`. One deployable, one
database, one transaction boundary. Microservices would add network hops and
partial-failure modes to a product whose hard requirement is working when the
network is unreliable.

---

## Frontend

| Chosen | Version | Alternatives | Why this one |
| --- | --- | --- | --- |
| **React** | 18.3.1 | Vue, Svelte, SolidJS, HTMX | Not for performance — for the ecosystem this app actually leans on: Radix primitives for accessible dialogs and switches, TanStack Query for server state. 19 is out; 18.3 is what the pinned Radix and Testing Library versions are tested against. |
| **Vite** | 6.0.7 | Create React App, Next.js, Webpack, Parcel | Fast builds and native code splitting, which is what took the entry chunk from 205 KB to 121 KB gzipped. **Vite 7 needs Node 20.** Next.js was rejected deliberately: SSR buys nothing for an authenticated kiosk app, and it would have made the frontend a server to run rather than static files on a CDN. |
| **react-router** | 6.28.1 | TanStack Router, Next.js routing, wouter | Route-level code splitting and a public unauthenticated route (`/handoff/:token`) alongside guarded ones. **v7 needs Node 20.** |
| **TanStack Query** | 5.62.11 | Redux Toolkit Query, SWR, useEffect + fetch | Server state is nearly all the state here. It gives caching, retry policy and request deduplication — the reason in-app navigation makes no redundant calls. Redux would add a store for data that is really just a cache. |
| **Tailwind CSS** | 3.4.17 | CSS Modules, styled-components, vanilla CSS, MUI | Accessibility here means real theming: large-text mode, high contrast, Easy Mode. Design tokens plus utility classes make those a variable change rather than a stylesheet fork. **Tailwind 4 needs Node 20.** A component library like MUI was rejected — its opinions fight the large-touch-target, low-literacy layout this needs. |
| **Radix UI** | dialog 1.1.4, label 2.1.1, radio-group 1.2.2, slot 1.1.1, switch 1.1.2 | Headless UI, Ark UI, hand-rolled | Unstyled and genuinely accessible — focus traps, keyboard semantics, ARIA wiring. Hand-rolling a dialog that a screen reader handles correctly is a bad use of effort in a health product. |
| **lucide-react** | 0.469.0 | Heroicons, Font Awesome, react-icons | Tree-shakes to per-icon chunks (visible in the build output as 0.3–1 KB files). `react-icons` would have pulled far more. |
| **clsx** + **tailwind-merge** + **class-variance-authority** | 2.1.1 / 2.6.0 / 0.7.1 | Manual template strings | `tailwind-merge` resolves conflicting utilities so a variant can override a base class predictably; `cva` keeps button/badge variants declarative. |

**Why not a PWA / offline-first with a service worker?** It would suit a
kiosk. It is not here because sign-in, the interview and document upload all
need the API anyway — offline would give a shell with nothing in it. The
handoff QR is the offline story instead: it carries the visit itself.

---

## AI, OCR and speech

| Chosen | Version / model | Alternatives | Why this one |
| --- | --- | --- | --- |
| **OpenAI-dialect AI provider** | `/chat/completions` | Vendor SDKs (openai, anthropic, google-genai) | One HTTP shape, so Gemini, OpenAI and x.ai are three environment variables apart with no code change. A vendor SDK would have locked the provider in — and this project has already switched models three times (2.5-flash retired, 3.6-flash quota, now 3.1-flash-lite). |
| **Google Gemini** | `gemini-3.1-flash-lite` | GPT-4o-mini, Claude Haiku, Grok, self-hosted Llava | Free tier that reads Devanagari and handwriting well. Interchangeable by design, as above. |
| **RapidOCR** (PP-OCRv4 via ONNX) | 1.4.4 | PaddleOCR, Tesseract, EasyOCR, cloud OCR | It *is* PaddleOCR — the bundled models are `ch_PP-OCRv4_det/rec_infer.onnx`. ONNX Runtime is far lighter than `paddlepaddle`, which matters at 512 MB. Tesseract is worse on Indian prescriptions; cloud OCR would send every document to a third party. |
| **AI vision escalation** | — | Local OCR only, cloud OCR only | The core OCR decision. Local OCR runs first (free, private, good on print); a vision model is asked only when the local read looks unreliable. Local-only failed on handwriting, which is most prescriptions here; vision-only would spend quota and privacy on documents that read fine locally. |
| **ElevenLabs** | `eleven_turbo_v2_5` | Browser SpeechSynthesis only, Google/Azure TTS, Coqui | The browser has no voice for Marathi, Gujarati or Punjabi on most devices — exactly the patients who most need text read aloud. Proxied server-side so the key never reaches the client, and it falls back to the browser voice on any failure. |
| **Browser SpeechRecognition** | Web Speech API | Whisper (server), cloud STT | Dictation runs entirely in the browser: no audio leaves the device, no server cost, no key. The trade-off is honest — support varies by platform, so the mic renders only when the browser actually has it. |

**Why not a single "AI does everything" pipeline?** Because of a rule this
project holds: *never save arbitrary model text as structured medical data.*
Deterministic rules extract findings; the model transcribes and summarises;
the patient confirms. On a deliberately illegible test image the vision model
invented plausible drug names at 0.85 confidence — the accept/reject flow is
what stops that reaching a record.

---

## Infrastructure

| Chosen | Alternatives | Why this one |
| --- | --- | --- |
| **Vercel** (static frontend) | Netlify, Cloudflare Pages, S3 + CloudFront, same-origin serving | Edge CDN with 60–70 ms first paint measured from Delhi, auto-deploy on push, and free. The frontend is static files, so the platform is close to interchangeable. |
| **Render** (Docker API + Postgres) | Railway, Fly.io, AWS ECS, Heroku | Blueprint-managed (`render.yaml`) so the whole service is in version control, with a managed Postgres attached. Fly.io would put the API in Mumbai — see the honest note below. |
| **Docker** | Buildpacks, bare Python | The OCR wheels and system libraries need a fixed base image. `docker-entrypoint.sh` runs migrations, optionally seeds, then serves. |
| **docker-compose** | Manual local setup | `make docker-up` gives db + api + web on one port for anyone who does not want to install Python and Node. |
| **GitHub, two remotes** | One remote | Render builds from `skieeeeeee/Akeso`, the shared repo is `utkarshdabral/Akeso`, so `origin` pushes to both. Pushing to one alone leaves the deployment building stale code. |

**Deployment split.** Frontend on a CDN, API on a container host. The
alternative — serving the built frontend from FastAPI — would have been one
service to deploy, but every asset would then travel from Oregon instead of
an edge 6 ms away.

---

## Testing

| Chosen | Version | Alternatives | Why this one |
| --- | --- | --- | --- |
| **pytest** | 8.3.4 | unittest, nose2 | Fixtures make a real Postgres test database per session practical. 537 backend tests. |
| **pytest-asyncio** | 0.25.2 | anyio plugin | The OCR and AI paths are async. |
| **Vitest** | 3.2.7 | Jest, Mocha | Shares Vite's transform pipeline, so there is no second build config. 233 frontend tests. |
| **Testing Library** | react 16.1.0, dom 10.4.0, user-event 14.5.2, jest-dom 6.6.3 | Enzyme, shallow rendering | Queries by role and label, which means the tests exercise the accessibility tree — the thing that actually matters here. |
| **jsdom** | 25.0.1 | happy-dom | Better fidelity for focus and ARIA behaviour. |
| **Playwright** | 1.49.1 | Cypress, Selenium | Drives real Chrome. Used for the checks that only a browser can settle: microphones present on every free-text field, six languages rendering in their own script, no horizontal overflow at 390 px. |
| **OpenCV** (test only) | 5.0.0.93 | pyzbar (needs libzbar), no decode test | Decodes the generated QR so a test can prove a scanner gets back what was encoded. It caught the quiet zone being 2 modules instead of the 4 the spec requires — with which no decoder could find the code at all. Skipped if absent; never imported at runtime. |

---

## Deliberately not used

| Not used | Why |
| --- | --- |
| **Redis** | Nothing needs a cache or a queue yet. OTP challenges live in Postgres with an expiry. |
| **Celery / background workers** | Document processing is a single request the patient waits on with a status endpoint. A worker would add a broker and a second process to a 512 MB instance. |
| **WebSockets** | Nothing is real-time. The interview is request/response. |
| **A component library (MUI, Chakra, shadcn)** | Their layout opinions conflict with large touch targets, Easy Mode and high contrast. Radix primitives give the accessibility without the styling. |
| **An i18n library (i18next, react-intl)** | Translations here are typed records with a language-aware fallback chain (`mr/gu/pa → hi → en`, but `ta → en`, because Devanagari is not read in Tamil Nadu). That chain is the requirement, and it is ~40 lines. i18next would add a runtime and its own file format for less. |
| **GraphQL** | The client wants whole screens' worth of data; REST endpoints shaped per screen are simpler and cacheable. |
| **An ABDM/ABHA integration** | Mocked on purpose. Real ABDM needs sandbox credentials and a compliance process; the UI states plainly that it is a prototype rather than imitating government authentication. |

---

## Honest gaps

Stated because a stack document that only lists strengths is not useful.

- **No Python linter, formatter or type checker.** No ruff, black or mypy is
  configured. `make check` runs the frontend typecheck *only* — despite its
  name it does not lint or test anything. Adding ruff and mypy is the single
  highest-value tooling gap.
- **No ESLint.** TypeScript catches type errors; nothing catches unused
  variables, hook-dependency mistakes or accessibility lint. The i18n
  re-render bug found during the performance work was exactly a stale-memo
  dependency — the class of thing `eslint-plugin-react-hooks` flags.
- **No CI.** Tests run locally and on demand. Nothing stops a push that fails.
- **Sign-in is a prototype.** `DEV_FIXED_OTP=12345` accepts any number. There
  is no SMS gateway in this codebase, and the API logs that warning at every
  startup.
- **The API runs in Oregon.** From Delhi, `/health` — which touches no
  database — answers in 270 ms, against a 6 ms handshake to the edge. Moving
  to Singapore would cut ~265 ms off every request but requires recreating
  the service and database on Render.
- **Uploads do not persist.** Free Render instances have no disk, so
  documents are lost on restart. A paid instance with a mounted disk fixes it.
