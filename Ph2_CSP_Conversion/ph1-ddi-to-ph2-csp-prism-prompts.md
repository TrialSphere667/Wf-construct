# PRISM Prompt Series — Ph1 DDI CSP → Ph2 CSP Conversion

## Overview

Six PRISM prompts convert the approved Ph1 DDI protocol into the Ph2 CSP one section at a time, with the Ph2 study concept as the only source of study-specific content. The series mirrors the protocol-to-CSR pipeline (map → verify → extract → draft), adds a residue check because the dominant failure mode here is **template contamination**: Ph1 healthy-volunteer and DDI content surviving into a Ph2 patient protocol.

**Source hierarchy (applies to every prompt)**

| Code | Source | Authoritative for | Never used for |
| --- | --- | --- | --- |
| C | Ph2 study concept | All study-specific content: objectives, design, population, dosing, assessments, statistics | — |
| IB | Current IB (strongly recommended) | Compound facts that may have changed since Ph1 approval | Study design |
| T | Ph1 DDI CSP (approved) | Structure, house style, and content classified RETAIN | Any study-specific fact |

Precedence is C > IB > T. A conflict between sources is flagged, never resolved by the model.

**Section disposition classes (assigned in P1, used by P3–P5)**

| Class | Meaning | Ph1 text reusable? | Typical sections |
| --- | --- | --- | --- |
| RETAIN | Study-independent sponsor/compound/admin text | Verbatim | Sponsor details, regulatory and ethics, data handling, publication policy |
| RETAIN-VERIFY | Compound-level but time-sensitive | Only after currency check against IB/C | IMP description, nonclinical summary, clinical experience to date, known risks |
| ADAPT | Structure reusable, content study-specific | Structure only | AE/SAE reporting, safety labs, concomitant medication section shell |
| REPLACE | Section exists in both, DDI content inapplicable | No | Objectives, design, population, SoA, PK sampling, statistics |
| DELETE | DDI-only, no Ph2 counterpart | No | Probe/perpetrator drug, confinement, period washout, crossover sequences |
| NEW | Ph2 element absent from Ph1 structure | No | Efficacy assessments, randomization and blinding, unblinding, DMC, interim analysis, sample size, rescue medication, estimands |

**Prompt series and human gates**

| Prompt | Scope | Runs | Gate after |
| --- | --- | --- | --- |
| P1 Section Disposition Map | Whole document | Once | — |
| P2 Map Verification and Readiness | Whole document | Once, fresh session | Author approves map and gap register |
| P3 Section Extraction Inventory | One section | Per section | — |
| P4 Section Drafting | One section | Per section | — |
| P5 Residue and Fidelity Check | One section | Per section | Author reviews draft + check report |
| P6 Cross-Section Consistency | Whole document | At milestones and before QC | Author resolves inconsistency register |

All outputs are drafts for author review, never final protocol text.

---

## Run-time parameters

Set these once and paste the block at the top of every prompt so all six runs share the same frame.

```
=== RUN-TIME PARAMETERS ===
COMPOUND:            {{compound code / INN}}
PH1_STUDY_ID:        {{Ph1 DDI protocol number}}
PH2_STUDY_ID:        {{Ph2 protocol number or "TBD"}}
INDICATION:          {{Ph2 indication}}
PH1_PROTOCOL_VER:    {{version + date of approved Ph1 CSP}}
CONCEPT_VER:         {{Ph2 concept version + date}}
IB_VER:              {{current IB edition + date, or "NOT PROVIDED"}}
TARGET_STRUCTURE:    {{"Ph1 structure" | "company Ph2 CSP template" | "ICH M11"}}
PARTICIPANT_TERM:    {{"participant" | "patient" | "subject"}}
TENSE_STYLE:         {{e.g. "future tense for planned procedures ('will'); present tense for background"}}
SECTION_UNDER_WORK:  {{section number + title, for P3-P5 only}}
===========================
```

`TARGET_STRUCTURE` matters most: if the Ph2 CSP must follow a different template than the Ph1 protocol, P1 maps Ph1 sections to target sections rather than converting in place.

---

## P1 — Section Disposition Map

Run once on the whole Ph1 protocol with the concept attached. Its output drives every later prompt, including the Ph1 Residue Lexicon that P5 checks against.

```
[RUN-TIME PARAMETERS BLOCK]

# P — POSITION
You are step 1 of 6 in a controlled conversion of an approved Phase 1 drug-drug
interaction (DDI) clinical study protocol (CSP) into a Phase 2 CSP for the same
compound. Your output is a planning artefact reviewed by a regulatory medical
writer. You do not draft protocol text.

# R — ROLE / RULES
Role: senior regulatory medical writer experienced in Phase 1 clinical
pharmacology and Phase 2 patient protocols.
Rules:
R1. Source codes: C = Ph2 study concept; T = Ph1 DDI CSP; IB = Investigator's
    Brochure (if attached). Every locator you cite uses these codes plus a
    section/paragraph/table reference (e.g. C:§3.2, T:§5.1 para 2, T:Table 2).
R2. Assign exactly one disposition per Ph1 section, at the lowest heading level
    that changes disposition: RETAIN | RETAIN-VERIFY | ADAPT | REPLACE | DELETE.
    Ph2 elements with no Ph1 home are listed separately as NEW.
R3. RETAIN only for content that is genuinely study-independent. If any
    sentence in the section is study-specific, the section is ADAPT or REPLACE.
    Compound-level content that could have changed since Ph1 approval
    (nonclinical, clinical experience, risks, IMP formulation) is RETAIN-VERIFY,
    never RETAIN.
R4. Do not judge whether the concept is scientifically adequate. Record what it
    states and where it is silent.
R5. Do not resolve conflicts between C and T. Record them as flags.
R6. Treat the Ph1 DDI study's own outcome as unknown unless C or IB states it.
    Any Ph2 element that depends on that outcome (e.g. concomitant medication
    restrictions for CYP/transporter inhibitors or inducers) is flagged
    DEPENDS-ON-DDI-RESULT.

# I — INTENT / INPUTS
Intent: give the author a complete, auditable plan of what happens to every Ph1
section and what the Ph2 CSP needs that Ph1 never had.
Inputs: T (the open document), C (attached in Scribbler), IB (optional),
TARGET_STRUCTURE.

# S — STRUCTURE / SEQUENCE
1. Build the Ph1 section inventory: every numbered heading in T, in order.
2. If TARGET_STRUCTURE is not "Ph1 structure", map each T section to its target
   section; mark T sections with no target home.
3. For each T section assign disposition (R2-R3), cite the C locators that will
   supply Ph2 content, and rate residue risk H/M/L (likelihood that DDI or
   healthy-volunteer content survives a careless edit).
4. List dependencies: other sections that must stay consistent with it.
5. Scan C for every Ph2 element with no T home; list as NEW.
6. Build the Ph1 Residue Lexicon (see output Part C).
7. List C/T/IB conflicts and DEPENDS-ON-DDI-RESULT items.

# M — MODALITY / MOTION
Output as Markdown tables, no narrative beyond one line per table.
Part A — Disposition Map
| T § | T title | Target § | Disposition | Rationale (≤20 words) | C locators | Residue risk | Depends on §§ |
Part B — NEW Sections
| Proposed § | Element | C locator | Note |
Part C — Ph1 Residue Lexicon (terms that must not appear in the Ph2 CSP unless
C uses them)
| Term / value | Category | T locator |
Categories: STUDY-ID, DDI-DRUG (probe, perpetrator, inhibitor, inducer,
substrate names and doses), DESIGN (period, sequence, treatment A/B, washout,
confinement, in-house, clinical unit, crossover, fixed sequence), POPULATION
(healthy, volunteer, subject, BMI and age limits, non-smoker), PK-SCHEDULE
(sampling days/times specific to the DDI design), NUMERIC (sample size,
study duration, dose levels, visit days), PHASE ("Phase 1", "first", "single
centre" etc. where design-specific).
Part D — Flags
| Flag ID | Type (CONFLICT | DEPENDS-ON-DDI-RESULT | CURRENCY) | Locators | Description |

# V — VERIFICATION (perform before output; report results at the end)
V1. Every T heading appears exactly once in Part A (report count T vs Part A).
V2. No section containing a study-specific fact is marked RETAIN.
V3. Every REPLACE/ADAPT row has ≥1 C locator or is flagged CONCEPT-SILENT.
V4. Every DDI drug named anywhere in T appears in Part C.
V5. NEW list checked against this minimum set; for each, state present in C /
    absent from C: efficacy endpoints, efficacy assessments, randomization,
    blinding/unblinding, sample size justification, interim analysis, DMC/safety
    review, rescue medication, estimands/intercurrent events, disease-specific
    inclusion/exclusion, participant discontinuation for lack of efficacy,
    contraception for the Ph2 population.

# F — FAILURE HANDLING
- Heading structure unreadable or numbering inconsistent → list what you could
  parse and stop; do not guess structure.
- C not found in context → stop and say so; do not proceed from T alone.
- Disposition genuinely ambiguous → choose the more conservative class (ADAPT
  over RETAIN, REPLACE over ADAPT) and raise a flag.

# C — COMPLETION CRITERIA
Complete when Parts A-D are output, V1-V5 results are reported with counts,
and the final line reads: "MAP STATUS: DRAFT — requires P2 verification and
author approval."
```

---

## P2 — Map Verification and Readiness

Run in a **fresh Scribbler session without the P1 output in context**, then paste the P1 map in only at step 4. This keeps the re-derivation as close to blind as Scribbler allows (the same limitation noted for the CSR pipeline's Step 2).

```
[RUN-TIME PARAMETERS BLOCK]

# P — POSITION
You are step 2 of 6. Step 1 produced a section disposition map for converting a
Ph1 DDI CSP (T) into a Ph2 CSP using the Ph2 concept (C). You independently
re-derive the map, compare it with Step 1, and assess whether each section is
ready for extraction and drafting. You do not draft protocol text.

# R — ROLE / RULES
Role: independent QC reviewer (regulatory medical writing).
Rules:
R1. Same source codes, disposition classes and locator format as Step 1.
R2. Derive your own map BEFORE reading the Step 1 map. Do not revise your
    derivation after seeing Step 1; record disagreements instead.
R3. A gap is any element a Ph2 CSP section requires that C does not state.
    Gaps are recorded, never filled, estimated or proposed.
R4. Do not adjudicate disagreements. Present both positions with locators.

# I — INTENT / INPUTS
Intent: catch misclassified sections (especially false RETAINs), missing NEW
elements and concept gaps before any drafting starts.
Inputs: T, C, IB (optional). Step 1 map supplied only at Sequence step 4.

# S — STRUCTURE / SEQUENCE
1. Re-derive Part A (disposition) and Part B (NEW) independently.
2. For every REPLACE / ADAPT / NEW element, list what the Ph2 section needs
   (e.g. Study Design needs: design type, arms, randomization ratio,
   stratification, blinding, treatment duration, follow-up, study duration,
   number of sites/countries) and mark each element STATED (C locator) or GAP.
3. Assign readiness per section: READY | READY-WITH-GAPS | BLOCKED.
   BLOCKED = a gap that makes the section's core content undraftable
   (e.g. no primary endpoint definition for Objectives/Endpoints).
4. [Author pastes Step 1 map here.] Compare row by row.
5. Re-check Step 1 Residue Lexicon for missing terms.

# M — MODALITY / MOTION
Part A — Agreement Table
| T § | Step 1 disposition | Step 2 disposition | Agree? | If not: both rationales with locators |
Part B — Concept Gap Register
| Gap ID | Target § | Required element | Why required (≤15 words) | Severity (BLOCKING / NON-BLOCKING) |
Part C — Readiness
| Target § | Readiness | Blocking gap IDs | Flags carried from Step 1 |
Part D — Residue Lexicon additions
| Term / value | Category | T locator |

# V — VERIFICATION
V1. Agreement rate reported as n agreed / n total.
V2. Every RETAIN in either map re-checked sentence by sentence for
    study-specific content; report any found.
V3. Every BLOCKED section has ≥1 BLOCKING gap ID.
V4. No gap row contains a proposed value.

# F — FAILURE HANDLING
- Step 1 map not supplied at step 4 → output Parts B-D from your own derivation
  and state that comparison was not performed.
- Disagreement rate >20% → state that the map should not be approved without
  author reconciliation.

# C — COMPLETION CRITERIA
Complete when Parts A-D are output, V1-V4 reported, and the final line reads:
"READINESS: n READY / n READY-WITH-GAPS / n BLOCKED — author gate required
before P3."
```

**Gate 1:** the author reconciles disagreements, closes or accepts each gap (with the study team where needed), and freezes the map and Residue Lexicon as the reference for P3–P6.

---

## P3 — Section Extraction Inventory

Run per section. The output is the only content source P4 may draft from, plus a section-level kill list for P5.

```
[RUN-TIME PARAMETERS BLOCK — SECTION_UNDER_WORK set]
[Paste approved map row(s), gap register rows and lexicon for this section]

# P — POSITION
You are step 3 of 6, run for one section: SECTION_UNDER_WORK. You extract
every content item the Ph2 version of this section needs, each with provenance.
The drafting step will see only your inventory, so anything you omit will not
appear and anything you mis-tag will propagate.

# R — ROLE / RULES
Role: regulatory medical writer performing source extraction.
Rules:
R1. Item classes:
    GROUNDED  — stated in C (or IB); quote the source text verbatim.
    CARRIED   — reused from T; allowed ONLY if the approved map marks this
                section/sub-section RETAIN, or RETAIN-VERIFY with the currency
                check passed (R4).
    GAP       — required, not stated in any permitted source; no value given.
    CONFLICT  — sources disagree; quote both; do not choose.
R2. Item ID format: {§}-{nnn} (e.g. 6.2-004). IDs are stable; never renumber.
R3. Precision-critical flag (PC) on every item containing a dose, unit,
    frequency, route, number of participants, ratio, age, lab threshold,
    timepoint, visit day/window, duration or study ID. PC values are copied
    character-for-character from source.
R4. Currency check for RETAIN-VERIFY content: compare the T statement with C and
    IB. If IB is not provided, or IB/C contains newer or different information,
    tag the item CONFLICT or GAP ("currency unverified"), not CARRIED.
R5. Never extract study-specific content from T, even if C is silent. Silence
    in C produces a GAP.
R6. Do not paraphrase GROUNDED items. Verbatim quote + locator only.

# I — INTENT / INPUTS
Intent: a complete, provenance-tagged item list that makes the section
draftable without the drafter consulting T for content.
Inputs: T section text, C, IB (optional), approved map rows, gap register rows,
frozen Residue Lexicon.

# S — STRUCTURE / SEQUENCE
1. List the elements this Ph2 section must contain (from the P2 element list
   for this section; add any further element the section requires).
2. For each element, search C, then IB, then (RETAIN/RETAIN-VERIFY only) T.
3. Create one item per discrete fact; tag class, PC, locator.
4. Read the T section sentence by sentence. Every sentence not CARRIED goes on
   the Section Kill List with the residue terms it contains.
5. Cross-check the Kill List against the frozen Residue Lexicon; add
   section-specific values (numbers, days, doses) the Lexicon lacks.

# M — MODALITY / MOTION
Part A — Inventory
| Item ID | Element | Class | PC | Content (verbatim for GROUNDED/CARRIED) | Locator(s) |
Part B — Section Kill List
| T locator | T sentence (first 12 words …) | Residue terms/values |
Part C — Open items carried forward
| Item ID | Type (GAP / CONFLICT / DEPENDS-ON-DDI-RESULT) | Description |

# V — VERIFICATION
V1. Every required element from step 1 maps to ≥1 item (report coverage n/n).
V2. Every PC item: re-read source and confirm character match; report n checked.
V3. No CARRIED item comes from a section not marked RETAIN/RETAIN-VERIFY.
V4. Every T sentence is either CARRIED or on the Kill List (report counts).

# F — FAILURE HANDLING
- Section marked BLOCKED in P2 → output Part C only and stop.
- Locator cannot be pinned below section level → give section level and flag
  LOCATOR-COARSE.
- Item could be GROUNDED or inferred → tag GAP and describe; never infer.

# C — COMPLETION CRITERIA
Complete when Parts A-C are output, V1-V4 reported with counts, and the final
line reads: "INVENTORY {§}: n GROUNDED / n CARRIED / n GAP / n CONFLICT."
```

---

## P4 — Section Drafting

Run per section, with the P3 inventory as the sole content source. In Scribbler the Ph1 section sits in the open document, so isolation from T is **instruction-enforced, not structural** — P5 exists to catch what leaks through.

```
[RUN-TIME PARAMETERS BLOCK — SECTION_UNDER_WORK set]
[Paste P3 Parts A-C for this section]

# P — POSITION
You are step 4 of 6. You draft the Ph2 CSP text for SECTION_UNDER_WORK from the
Step 3 inventory alone. The Ph1 section in the document is a reference for
heading structure, sub-section order and house style only.

# R — ROLE / RULES
Role: regulatory medical writer drafting a Phase 2 protocol section.
Rules:
R1. Content sources: inventory items only. You may not take any fact, number,
    term or criterion from T unless it is a CARRIED item.
R2. CARRIED items may be reproduced verbatim. GROUNDED items may be rephrased
    into protocol prose, but PC values are reproduced character-for-character.
R3. Every sentence ends with its trace tag: [ID] or [ID, ID]. A sentence
    without a tag is a gate failure.
R4. GAP items appear as: [[GAP {ID}: {element} — not specified in concept]].
    CONFLICT items appear as: [[FLAG {ID}: {short description}]].
    Never write around a gap or merge conflicting values.
R5. Connective or structural sentences that carry no fact (e.g. "The following
    assessments will be performed:") are tagged [STRUCT].
R6. Apply TENSE_STYLE and PARTICIPANT_TERM throughout.
R7. Do not add content that a Ph2 protocol "usually" contains. If it is not in
    the inventory, it is not in the draft.
R8. Cross-references to other sections are written as [[XREF: {title}]];
    section numbers are resolved in P6.

# I — INTENT / INPUTS
Intent: a section draft the author can review line by line against sources.
Inputs: P3 inventory; T section (structure and style only); TENSE_STYLE;
PARTICIPANT_TERM.

# S — STRUCTURE / SEQUENCE
1. Outline the section headings (keep T sub-section order where the map allows;
   insert NEW sub-sections where the inventory requires them).
2. Assign each inventory item to a heading; every item must be used once.
3. Draft sentence by sentence, tagging as you go.
4. Insert GAP/FLAG placeholders at the point the content would appear.

# M — MODALITY / MOTION
Part A — Draft section (Word-ready text, headings numbered as in target).
Part B — Trace Table
| Item ID | Used in sentence # | Reproduced as (verbatim / rephrased) |
Part C — Unused items (must be empty; otherwise explain).

# V — VERIFICATION
V1. Count sentences; count tagged sentences; must be equal.
V2. Every inventory item appears in Part B or Part C.
V3. Every PC value in the draft matches the inventory character-for-character.
V4. Scan the draft against the Section Kill List; report 0 hits or list each hit.

# F — FAILURE HANDLING
- Inventory has BLOCKING gaps → draft the remaining sub-sections and leave the
  blocked sub-section as a single [[GAP]] placeholder.
- You notice yourself needing a T fact to make a sentence work → stop that
  sentence, insert [[GAP]], and list it under Part C.

# C — COMPLETION CRITERIA
Complete when Parts A-C are output, V1-V4 reported, and the final line reads:
"DRAFT {§}: n sentences / n tagged / n GAP / n FLAG / Kill List hits: n."
```

---

## P5 — Residue and Fidelity Check

Run per section on the P4 draft, ideally in a fresh session. It is a gate, not an editor: it reports, it does not rewrite.

```
[RUN-TIME PARAMETERS BLOCK — SECTION_UNDER_WORK set]
[Paste: P4 Part A draft, P3 inventory, P3 Kill List, frozen Residue Lexicon]

# P — POSITION
You are step 5 of 6, the quality gate for one drafted section. You check the
draft for Ph1 residue, traceability and value fidelity, and return PASS or FAIL.
You do not edit the draft.

# R — ROLE / RULES
Role: QC reviewer for regulated documents.
Rules:
R1. Any of the following is a FAIL: an untagged sentence; a PC value that does
    not match its source; a residue hit that is not justified by a GROUNDED
    item; a CARRIED item from a section not marked RETAIN/RETAIN-VERIFY; a
    placeholder removed or filled without an inventory item.
R2. A residue term is justified only if C itself uses it in the Ph2 context
    (e.g. "PK sampling" stated in C). Cite the C locator.
R3. Report each finding once with its sentence number. Do not propose rewrites;
    you may state what the source says.

# I — INTENT / INPUTS
Intent: catch template contamination and silent inference before author review.
Inputs: draft, inventory, Kill List, Residue Lexicon, C (for justification
checks).

# S — STRUCTURE / SEQUENCE
1. Residue sweep: scan the draft for every Lexicon term and Kill List value,
   including near variants ("volunteer(s)", "subject(s)", "Period 1",
   "Treatment A", "Day -1 admission", Ph1 study ID, DDI drug names and doses).
2. Semantic residue: flag statements that only make sense in a Ph1 DDI healthy-
   volunteer study even if no Lexicon term appears (e.g. confinement, fixed
   dosing sequence, eligibility limited to healthy status, no efficacy
   assessment, contraception rules written for a different population).
3. Trace audit: confirm every sentence has a tag and every tag resolves to an
   inventory item whose content supports the sentence.
4. PC audit: compare every PC value against the inventory.
5. Inference audit: flag any claim that goes beyond its tagged items.

# M — MODALITY / MOTION
| Finding # | Check (RESIDUE / SEMANTIC / TRACE / PC / INFERENCE) | Sentence # | Excerpt (≤12 words) | Expected (source) | Severity (FAIL / REVIEW) |
Then: Summary counts per check type.

# V — VERIFICATION
V1. Report n Lexicon terms searched and n Kill List values searched.
V2. Report n sentences audited = n sentences in draft.

# F — FAILURE HANDLING
- Inventory or Kill List not supplied → run checks 2, 3 (tags present only)
  and 5; mark the result INCOMPLETE, never PASS.

# C — COMPLETION CRITERIA
Final line: "GATE {§}: PASS" only if zero FAIL findings; otherwise
"GATE {§}: FAIL — n findings". REVIEW findings never block PASS but are
listed for the author.
```

**Gate 2 (per section):** the author reviews the draft with the P5 report, then accepts the text into the document. Trace tags are stripped only after acceptance; keep a tagged copy as the audit record.

---

## P6 — Cross-Section Consistency and Propagation

Run on the whole converted document at milestones (after the core design sections, after the synopsis, before QC). This is the propagation-completeness problem from CSP_AMD_WF applied to a full conversion.

```
[RUN-TIME PARAMETERS BLOCK]
[Paste: frozen Residue Lexicon, open-items list from all P3 runs]

# P — POSITION
You are step 6 of 6. Sections have been converted individually; you check that
the document is internally consistent, that no Ph1 residue survives anywhere
(including unconverted sections, tables, appendices, headers and footers),
and that cross-references resolve.

# R — ROLE / RULES
Role: protocol QC reviewer.
Rules:
R1. Report inconsistencies; never choose which version is correct. Where C
    states the value, cite it.
R2. Every finding cites both (all) locations in the document.
R3. Open GAP/FLAG placeholders are listed, not counted as errors.

# I — INTENT / INPUTS
Intent: a single register of everything that must agree but does not.
Inputs: the converted document, C, Residue Lexicon, open-items list.

# S — STRUCTURE / SEQUENCE
Check each chain and record every mismatch:
1. Synopsis ↔ body: title, phase, design, population, n, arms, doses, duration,
   objectives and endpoints wording.
2. Objectives ↔ endpoints ↔ statistical analyses ↔ estimands: every objective
   has an endpoint; every endpoint has an analysis; no orphan analyses.
3. Schedule of Activities ↔ assessment sections: every SoA row described in
   the body; every body assessment in the SoA; visit names, days and windows
   identical.
4. IMP: dose, regimen, route, formulation and duration identical in all
   sections; dose-modification and stopping rules consistent with safety
   sections.
5. Population: n randomized/enrolled, ratio, stratification identical in design,
   statistics and synopsis.
6. Eligibility ↔ concomitant medication ↔ contraception sections consistent;
   DEPENDS-ON-DDI-RESULT items still flagged.
7. Terminology: PARTICIPANT_TERM used throughout; abbreviations list complete
   and free of DDI-only abbreviations.
8. Cross-references: every [[XREF]] and every "Section x.y" points to an
   existing heading with the right title.
9. Global residue sweep with the full Lexicon, including tables, appendices,
   title page, headers/footers and document properties.

# M — MODALITY / MOTION
Part A — Inconsistency Register
| Finding # | Chain (1-9) | Location 1 | Location 2 | Discrepancy | Source value (C locator) or "not in C" |
Part B — Open Placeholders
| Placeholder ID | Section | Description |
Part C — Summary counts per chain.

# V — VERIFICATION
V1. Report n sections examined and list any section still in Ph1 form
    (not yet converted).
V2. Report n Lexicon terms searched globally and n hits.

# F — FAILURE HANDLING
- Document too long for one pass → run chains 1-5 and 6-9 as two calls and
  state which chains each covered; never report a chain as clean if it was
  not run.

# C — COMPLETION CRITERIA
Final line: "CONSISTENCY: n findings / n open placeholders / n residue hits —
author resolution required."
```

**Gate 3:** the author resolves the register; after any change, re-run the affected chains.

---

## Section order, limitations and open decisions

**Recommended conversion order** — upstream sections first, so later sections draft against settled design:

1. Objectives, endpoints and estimands
2. Study design (including randomization, blinding, NEW sections)
3. Study population (eligibility, discontinuation)
4. Study intervention and concomitant medication
5. Assessments (efficacy, safety, PK), then the Schedule of Activities
6. Statistics and sample size
7. Background, rationale and benefit-risk (RETAIN-VERIFY heavy)
8. Synopsis last, generated from converted body sections
9. RETAIN administrative sections at any point; run P6 after steps 3, 6 and 8

**Known limitations**

- Isolation of P4 from the Ph1 text is instruction-enforced in Scribbler; P5 is the compensating control. In a LangGraph build, P4 would receive the inventory only.
- P2 is only near-blind if run in a fresh session; the agreement rate is weaker evidence than a programmatic comparison of two independent maps.
- Residue detection beyond the Lexicon (P5 check 2) relies on model judgement and should be treated as REVIEW-grade, not exhaustive.
- Without the current IB, every RETAIN-VERIFY section produces currency GAPs by design.

**Open decisions**

- `TARGET_STRUCTURE`: convert in place within the Ph1 heading structure, or remap to the company Ph2 template?
- Whether the Ph1 DDI study's results are available to inform Ph2 concomitant medication restrictions, or stay as DEPENDS-ON-DDI-RESULT flags.
- House style for trace tags in Word (inline brackets vs Scribbler comments) during review.
