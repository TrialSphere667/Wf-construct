# CSR Drafting Agent PoC: Next Steps

**Format:** Informal working session (~60 min)
**Participants:** Medical Writing (MW), Scribbler / agent development team
**Owner:** Adam (MW)

---

## 1. Meeting Purpose

Agree what is needed to build and test a **proof-of-concept (PoC) CSR drafting agent** on the existing orchestrator, MCP and file pool. The agent will be driven by the MW **protocol-to-CSR dependency map**.

### Intended outcomes
By the end of the meeting we should have:

1. **The input contract:** what format and granularity the agent needs for the dependency map, the protocol (CSP) and the CSR template.
2. **The architecture:** how the agent workflow will be structured, and which controls the platform can enforce.
3. **The test:** one protocol, a defined set of CSR sections, agreed evaluation criteria and a target date.
4. **Action items:** a named owner for each item and a next checkpoint.

### Roles
| Area | Owner |
|---|---|
| Orchestrator, agent configuration, MCP, file pool, Scribbler integration | Dev team |
| Dependency map, section scope, test data, reference text, evaluation and scoring | MW |
| Joint | PoC scope, acceptance criteria, review of results |

---

## 2. Suggested Agenda

| # | Topic | Time |
|---|---|---|
| 1 | Purpose, scope and roles | 5 min |
| 2 | Walkthrough of the dependency map | 10 min |
| 3 | Dev team: current platform setup | 10 min |
| 4 | Discussion: inputs, architecture, controls | 15 min |
| 5 | PoC test design | 15 min |
| 6 | Actions, owners, next checkpoint | 5 min |

---

## 3. Topic Detail

### 3.1 Purpose, Scope and Roles (5 min)
- The PoC tests whether the agent can draft **protocol-driven CSR sections** from the final CSP, using the dependency map.
- The output is a **draft for MW review**, never final document content.
- **In scope for v1:** sections whose content comes directly from the protocol (see 3.5).
- **Out of scope for v1:**
  - Sections that need SAP, TFL or clinical-database input (results, statistical outcomes).
  - Sections that need clinical or narrative judgement (discussion, conclusions, patient narratives).
  - Amendment history reconciliation (covered by a separate workflow).

### 3.2 Walkthrough of the Dependency Map (10 min)
- **What it is:** maps each CSR section (ICH E3 / company template) to the CSP section(s) its content comes from.
- **How it is structured:**
  - CSR section ID and title
  - Source CSP locator(s)
  - Type of content relationship (e.g., carried over near-verbatim, restated in past tense, summarised)
  - Content that is precision-critical (doses, timepoints, sample size, visit windows, criteria wording)
  - Known gaps (content the CSR template needs that the protocol does not provide)
- **Supporting material available:** the MW Step 1–4 prompt series (map → verification → extraction → drafting). It can serve as a reference design for the agent steps.
- **Question for devs:** is the map usable as it stands, or does it need converting (see 3.4a)?

### 3.3 Dev Team: Current Platform Setup (10 min)
Let the dev team describe what already exists:
- Orchestrator: how agents/steps are defined, sequenced and triggered.
- MCP: which tools or actions Scribbler exposes to the agents (read document, read a section, write, comment, etc.).
- File pool: what it is, what goes into it, who can read or write it.
- Model(s) available and any limits (context window, token, rate or cost limits).
- Logging and run history.

### 3.4 Discussion: Inputs, Architecture and Controls (15 min)

#### a) Input contract
- What format should the dependency map be in: Word table, Excel, JSON or YAML?
- Do map entries need stable IDs so the agent can reference them?
- How is the protocol supplied: whole document, split into sections, or retrieved by locator through the MCP?
- Is the CSR template supplied as structure only (headings and instructions), or as a Word document to populate?
- Who maintains the map as the template or protocols change?

#### b) Agent workflow structure
- **Option A (baseline):** a single agent reads the protocol and the map and drafts each section directly.
- **Option B (staged):**
  1. **Extract:** pull the relevant protocol content per section as cited, tagged items, with gaps listed explicitly.
  2. **Draft:** write the CSR text **from the extracted items only**.
  3. **Check:** verify that citations are present and precision-critical values are correct.
- **Why Option B matters:** if the drafting step only receives cited items, every sentence can be traced to a source item, and the model cannot fill gaps with plausible but unsupported text. Instructing the model is not a guarantee. Controlling what each step receives is.
- **Suggestion:** run Option A as the baseline and Option B as the comparison. Measure whether the split improves accuracy and traceability.
- **Question for devs:** can the orchestrator control which files or data each step can see?

#### c) Traceability and output controls
- Can each drafted sentence or paragraph carry a **source reference** (CSP section or item ID)?
- How are **gaps** shown, e.g., `[GAP: not specified in protocol]`, rather than filled in by the model?
- How are **flags** (ambiguity, inconsistency in the protocol) surfaced: Word comments, highlights, or a separate report?
- Can **precision-critical values** be checked automatically against the source text?
- Is there a **run log** (inputs, prompt version, model, outputs) for auditability?

#### d) Output delivery into Scribbler
- Where does the output go: a new document, sections inserted into the CSR shell, or tracked changes?
- Is AI-generated text visibly marked as unverified?
- What does MW review look like in practice (accept/reject, comment, edit)?

#### e) House style parameters
- Tense: protocol future tense ("will be") → CSR past tense ("were").
- How to handle content that may not reflect what actually happened in the study (e.g., planned procedures). Flag it, don't assume.
- Abbreviations and terminology: is there a standard to apply?

### 3.5 PoC Test Design (15 min)

#### a) Test protocol
- One approved, final protocol (de-identified if required).
- Ideally a study with an existing final CSR, so there is a ground-truth comparison.
- Confirm which data classifications are allowed on the platform.

#### b) Candidate sections (3–5 to start)
| CSR section (ICH E3) | Why it is a good candidate |
|---|---|
| Synopsis (protocol-derived elements only) | Many fields, quick to verify |
| 9.1 Overall study design and plan | Mostly protocol-derived |
| 9.3 Selection of study population (inclusion/exclusion) | Precision-critical, near-verbatim |
| 9.4 Treatments (dose, regimen, administration) | Precision-critical values |
| 8 Study objectives / 9.5 endpoints and assessments | Direct mapping, clear structure |

#### c) Evaluation criteria
| Criterion | What is measured |
|---|---|
| Completeness | Mapped content present in the draft versus the dependency map |
| Accuracy | Precision-critical values correct (doses, timepoints, n, criteria) |
| Traceability | Share of sentences with a valid source reference |
| Grounding | No content that the source does not support (hallucinations or inferences) |
| Gap handling | Gaps shown as placeholders, not filled in |
| Style | Tense, voice and terminology follow house style |
| Usability | MW time to bring the draft to review-ready |

- Scoring: MW scores each section with a scoring template (MW to provide).
- Optional: compare against the final CSR text, or against a reference draft written by an MW.

#### d) Iteration plan
- Run 1: baseline (Option A).
- Run 2: staged design (Option B), if feasible.
- Review results jointly, then refine the map, the prompts or the workflow.

### 3.6 Actions, Owners and Next Checkpoint (5 min)
Record each action with an owner and a date.

---

## 4. What MW Can Provide

- [ ] The dependency map in the agreed format, with stable IDs
- [ ] A test protocol (final, de-identified as needed) and the CSR template shell
- [ ] Reference text for the PoC sections (final CSR or MW reference draft)
- [ ] The PoC section scope and a list of out-of-scope sections
- [ ] The Step 1–4 prompt series as a reference design for the agent steps
- [ ] House style rules (tense, voice, gap placeholder wording)
- [ ] Acceptance criteria and the scoring template
- [ ] Scoring and review of PoC runs
- [ ] Availability for quick domain questions during the build

---

## 5. Questions to Ask the Dev Team (Quick List)

1. What format and structure do you need for the dependency map?
2. How do agents read the protocol: whole file, by section, or by locator?
3. What exactly is in the file pool, and can access be limited per agent or step?
4. Can the workflow be split into extract → draft → check steps, with the drafting step not receiving the protocol?
5. Which MCP actions are available (read, write, comment, tracked changes)?
6. Which model(s) are used, and what are the context or token limits?
7. How are outputs delivered into Scribbler, and how is AI text marked?
8. Is there run logging (inputs, prompt version, model, outputs)?
9. What data is allowed on the platform for testing?
10. What timeline is realistic for a first test run?

---

## 6. Constraints to Agree On

- AI output is a **draft for MW review** and is never merged without review.
- Every drafted statement must be **traceable** to a protocol location.
- **Gaps are shown, not filled.** Missing information becomes a placeholder.
- **Ambiguities and inconsistencies are flagged**, not resolved by the model.
- **Precision-critical values** are checked against the source.
- Sections that need clinical judgement are **human-first** and out of PoC scope.

---

## 7. Action Log

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Next checkpoint:** ____________
