# AccessPath AI

> **"Don't just test a website. Test whether a real person can actually complete the task."**

A task-level accessibility and usability testing platform built for **HackIIITD 2026**, powered by the **TinyFish Web Agent**.

---

## 1. What is AccessPath AI?

Traditional accessibility tools (such as Lighthouse, axe-core, or static DOM checkers) inspect website code, HTML element structures, and rule-based contrast formulas in isolation.

However, a website can technically pass every automated WCAG check and still be confusing or impossible for a real human to use:
* Instructions filled with dense legalistic jargon.
* Critical progression buttons buried inside unlabelled collapsible accordions.
* Destructive "Reset" buttons visually dominant over "Submit".
* File upload inputs labelled "Attachment 1" with no guidance on formats or size limits.

**AccessPath asks a fundamental question:**
> *"Can this specific user actually complete this specific task on the live website?"*

---

## 2. Architecture

```
User Input (URL, Task, Persona)
             ↓
     Frontend (React + Vite)
             ↓
Backend Orchestration (Node.js + Express)
             ↓
     TinyFish Web Agent (Live Browser Sandbox)
             ↓
     Live Website Interaction (Multi-Step Journey)
             ↓
Structured Result (`output_schema` SSE Stream)
             ↓
  AccessPath Analysis & Normalization Engine
             ↓
Deterministic Task Success Score (0–100)
             ↓
Evidence-First Diagnosis & Before/After Retest
```

### The Role of TinyFish
TinyFish serves as the live web execution layer:
1. **Headless Browser Sandbox**: Navigates live web pages, expands interactive sections, fills forms, and checks document uploads without human intervention.
2. **Streaming Events & Live View**: Emits real-time SSE lifecycle events (`STARTED`, `STREAMING_URL`, `PROGRESS`, `COMPLETE`), giving judges a live browser window to watch the agent interact in real time.
3. **Structured Outputs**: Executes with a strictly typed JSON Schema (`output_schema`) to capture step-by-step actions, results, barrier detections, and evidence cleanly.
4. **Safety Compliance**: Enforces non-destructive test mode—withholding real logins, financial transactions, or irreversible form submissions.

---

## 3. Core Features

* **5 Tailored User Personas**:
  * **First-Time User**: Limited familiarity with complex institutional portals.
  * **Mobile-First User**: High touch friction, small viewports, desktop-biased controls.
  * **Hindi-Speaking Student**: Vulnerable to dense bureaucratic English jargon.
  * **Low Digital-Literacy User**: Needs obvious linear paths; misses hidden collapsibles.
  * **Screen-Reader User**: Relies on semantic names, accessible labels, and keyboard order.
* **Live Agent View**: Embedded browser window stream displaying live navigation as the agent executes.
* **Deterministic Task Success Score (0–100)**:
  * Base: 100 points
  * Transparent deductions: Critical blocker (-25), Major blocker (-15), Moderate barrier (-10), Minor barrier (-5), Dead end (-10), Unclear instruction (-5).
* **8 Barrier Classifications**:
  * Navigation, Language, Form Usability, Accessibility, Mobile Usability, Information Architecture, Error Recovery, Dead End.
* **4-Stage Evidence Pipeline**:
  $$\text{Observation} \longrightarrow \text{Evidence} \longrightarrow \text{User Impact} \longrightarrow \text{Recommended Fix}$$
* **Retest Comparison**:
  * Re-runs the identical task and persona against the improved site.
  * Quantifies score improvement (e.g., $62 \rightarrow 100$, $+38$ delta) and confirms barrier resolution.

---

## 4. Controlled Demo Environment

The project includes an authentic 5-page scholarship application portal (`/demo-site`):
* **Page 1: Overview** — Dense notices, ambiguous CTA button.
* **Page 2: Eligibility** — Academic jargon ("post-baccalaureate Schedule IV"), low-contrast income ceiling.
* **Page 3: Requirements** — Mandatory document list, hidden next step accordion without ARIA attributes.
* **Page 4: Application** — Missing `<label>` tags, hazardous primary-red "Reset Application Form" button.
* **Page 5: Document Upload** — Ambiguous inputs titled "Attachment 1" and "Supplementary Record 2" without format or size specifications.

> **Toggle Mode**: The demo site includes an instant toggle between **Baseline (Flawed)** and **Improved (Fixed)** state to demonstrate before/after re-testing live during judging.

---

## 5. Local Setup & Running

### Prerequisites
* Node.js v18+ installed
* TinyFish connected (`~/.tinyfish/config.json` or `TINYFISH_API_KEY` environment variable)

### Quick Start (Single Command)
Run from the root directory:
```bash
# 1. Install dependencies
npm run build

# 2. Start the unified platform (serves frontend, backend API, and demo site on port 5000)
npm run start
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 6. Live Hackathon Demo Walkthrough (Step-by-Step)

1. Open **[http://localhost:5000](http://localhost:5000)**.
2. Click **Try Demo** (or navigate to **New Test** &rarr; **Auto-Fill Controlled Demo**).
3. Notice prefilled values:
   * **URL**: `http://localhost:5000/demo-site/index.html`
   * **Task**: `Apply for a scholarship and identify everything required before starting the application.`
   * **Persona**: `First-Time User`
4. Click **Start Task Simulation**.
5. Watch the **Live Agent View** and lifecycle status progress through the 5 pages of the fellowship portal.
6. Observe the generated Baseline report:
   * **Task Success Score**: **62 / 100**
   * **Status**: Completed with barriers
   * **Total Steps**: 9 (7 Completed, 2 Blocked)
   * **Barriers Detected**: 4 (1 Major, 2 Moderate, 1 Minor)
7. Inspect the **Evidence-First Diagnostic** on Step 9 (Ambiguous Document Upload Requirements) and Step 5 (Hidden Next Step in Unlabelled Collapsible).
8. Click **Re-test After Fix** in the top action bar.
9. Watch the re-test execute against the improved interface state.
10. Confirm the **Verified Retest Improvement**:
    * **Before**: 62 / 100
    * **After**: 100 / 100
    * **Improvement**: **+38 points** (0 remaining barriers).

---

## 7. Project Structure

```
├── shared/
│   └── types.ts             # Shared domain data models & contracts
├── backend/
│   ├── src/
│   │   ├── index.ts         # Express entrypoint, static SPA and demo-site server
│   │   ├── config.ts        # Secure TinyFish credential loader
│   │   ├── types.ts         # Backend data types
│   │   ├── db/
│   │   │   └── database.ts  # File-persisted atomic local database
│   │   ├── services/
│   │   │   ├── tinyfishService.ts  # Live TinyFish Web Agent integration & SSE runner
│   │   │   ├── scoreService.ts     # Deterministic scoring engine
│   │   │   ├── analysisService.ts  # Persona insights & impact synthesizer
│   │   │   └── normalizer.ts       # normalizeTinyFishResult() isolator
│   │   └── routes/
│   │       └── testRoutes.ts       # REST & SSE streaming endpoints
├── demo-site/
│   └── public/              # 5-stage realistic scholarship testing benchmark
│       ├── index.html       # Step 1: Overview
│       ├── eligibility.html # Step 2: Eligibility
│       ├── requirements.html# Step 3: Requirements (hidden accordion)
│       ├── apply.html       # Step 4: Candidate form (reset button hazard)
│       └── upload.html      # Step 5: Document upload (unclear formats)
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # React Router layout
│   │   ├── api.ts           # REST & EventSource client
│   │   ├── components/      # ScoreCard, JourneyTimeline, BarrierCard, LiveBrowserView
│   │   └── pages/           # LandingPage, CreateTestPage, LiveTestPage, ResultsPage, HistoryPage
└── package.json             # Root unified build & execution scripts
```

---

## 8. Security & Safety Principles

* **Secret Hygiene**: TinyFish API keys are loaded strictly on the backend and are never sent to the browser or client bundle.
* **Observation Mode**: The Web Agent executes in safe audit mode, disallowing credential entry, actual fund transfers, or irreversible submissions.
* **Transparent Scoring**: Scores are calculated deterministically from explicit deduction rules rather than arbitrary AI numbers.
