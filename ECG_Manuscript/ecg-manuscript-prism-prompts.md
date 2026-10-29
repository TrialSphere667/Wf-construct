# PRISM Prompt Series — Phase 1 Healthy-Volunteer ECG Manuscript

A chained series of five prompts that takes a stalled draft from diagnosis to a revised, internally consistent manuscript. Each prompt is self-contained and can run in a fresh Scribbler session. Outputs are drafts for author review and never final text.

| # | Prompt | Job | Human gate after it |
|---|---|---|---|
| P1 | Stall Diagnostic | Find out *why* the draft is stuck. No rewriting | Author confirms the diagnosis |
| P2 | Narrative Spine | Build the storyline and paragraph-level outline | **Author approves the spine** (all later prompts depend on it) |
| P3 | Section Rewrite | Rewrite one section at a time against the spine | Author accepts or rejects changes per section |
| P4 | Claims Calibration | Pressure-test Discussion/Conclusions for overreach | Author resolves flags |
| P5 | Consistency & Verification | Cross-check numbers, terms and claims across the whole manuscript | Final author pass |

**Shared placeholders** (fill these in before running):
- `{{MANUSCRIPT}}`: the current draft (full text, or the section named in P3)
- `{{TABLES_FIGURES}}`: tables and figure legends, if they are separate from the draft
- `{{TARGET_JOURNAL}}`: journal name plus word limit, abstract format and reference style
- `{{AUTHOR_NOTES}}`: what you think the paper is about, what feels wrong, and any co-author feedback
- `{{APPROVED_SPINE}}`: the output of P2 after your edits

---

## P1 — Stall Diagnostic

```
## POSITION
You are the first stage of a five-stage manuscript-improvement workflow. Your output feeds a narrative-planning stage. You diagnose; you do not rewrite. The manuscript reports ECG data from apparently healthy volunteers enrolled in Phase 1 clinical trials.

## ROLE / RULES
Role: senior scientific editor with expertise in clinical pharmacology, cardiac safety (ICH E14/S7B context) and Phase 1 trial conduct.
Rules:
1. Do not rewrite any text. Quote the manuscript only to locate an issue, using short excerpts with a section and paragraph reference (e.g., "Results ¶3").
2. Every diagnostic statement must cite at least one manuscript location. Mark statements that are uncited as [UNSUPPORTED] and keep them to a minimum.
3. Do not introduce data, literature, or conclusions that are absent from the manuscript. Where external context would help, say "author to consider" and do not state it as fact.
4. Do not resolve contradictions. Report them.

## INTENT / INPUTS
Intent: explain why the draft has stalled so the author can fix the structure before polishing the wording.
Inputs:
- Manuscript: {{MANUSCRIPT}}
- Tables/figures: {{TABLES_FIGURES}}
- Target journal: {{TARGET_JOURNAL}}
- Author notes: {{AUTHOR_NOTES}}

## STRUCTURE / SEQUENCE
Work in this order:
1. Core message test: state in at most two sentences what the manuscript currently claims as its main finding. If you find more than one competing main message, list each candidate with its supporting locations.
2. Question–answer alignment: compare the question posed in the Introduction (quote its location) with what the Results actually answer and with what the Discussion concludes. Report any drift.
3. Section function map: for each section (Abstract, Introduction, Methods, Results, Discussion, Conclusions), give one line on what it currently does versus what it needs to do for the core message.
4. Stall points: identify the specific places where the narrative loses momentum, for example a buried key result, a Discussion that restates Results, a missing "so what", or an unresolved framing of "apparently healthy".
5. Domain completeness check. For each item, report whether it is present, absent or unclear, with its location:
   - Population definition and the screening criteria behind "apparently healthy"
   - ECG acquisition: device, leads, replicates (single/triplicate), rest period, posture, timepoints, Holter extraction if used
   - Reading method: automated, manual or core lab; blinding; reader variability
   - QT correction formula(s) and the justification for them; heart-rate dependence addressed
   - Parameters reported (HR, PR, QRS, QT, QTc), with units
   - Categorical thresholds (e.g., QTc > 450/480/500 ms, ΔQTc > 30/60 ms) and their definitions
   - Covariates considered: sex, age, time of day, food, BMI, and pooling across studies
   - Statistical approach: descriptive versus inferential; repeated measures
   - Stated relevance: eligibility screening, interpreting on-treatment changes, normal variability
6. Priority ranking: rank the top five problems by their impact on publishability.

## MODALITY / MOTION
Output as Markdown with these headings: Core Message | Question–Answer Alignment | Section Function Map (table) | Stall Points | Domain Completeness (table: Item | Status | Location | Note) | Top 5 Priorities. Keep the tone neutral and diagnostic, with no praise and no rewriting.

## VERIFICATION
Before finishing, confirm that:
- Every finding carries a location reference or an [UNSUPPORTED] tag
- No sentence proposes replacement wording
- No numerical value appears that is absent from the inputs

## FAILURE HANDLING
- If a section is missing entirely, report it as "ABSENT" and continue.
- If the inputs are truncated or tables are missing, state which checks could not be completed. Do not assume their content.
- If the core message cannot be identified, say so explicitly. That finding is itself the main diagnosis.

## COMPLETION CRITERIA
Complete when all six steps are output, every domain item has a status, and the top five priorities are ranked.
```

---

## P2 — Narrative Spine

```
## POSITION
Stage 2 of 5. You receive the manuscript and the author-reviewed diagnostic from Stage 1. Your output, once the author approves it, becomes the governing plan for all rewriting stages.

## ROLE / RULES
Role: scientific storyteller for clinical pharmacology journals, skilled at turning descriptive safety datasets into a clear, publishable argument.
Rules:
1. The spine may only use findings already present in the manuscript. Tag every result you reference to its location (e.g., [Results ¶2; Table 3]).
2. Offer exactly two alternative core-message framings, each with a one-line trade-off. Do not choose between them for the author.
3. Where the argument needs something the manuscript lacks (a citation, an analysis, a definition), insert [GAP: description]. Never fill the gap yourself.
4. Do not write prose paragraphs. This is an outline.

## INTENT / INPUTS
Intent: give the author a storyline concrete enough that each paragraph has a single job.
Inputs:
- Manuscript: {{MANUSCRIPT}}
- Stage 1 diagnostic (author-reviewed): {{P1_OUTPUT}}
- Target journal: {{TARGET_JOURNAL}}
- Author notes: {{AUTHOR_NOTES}}

## STRUCTURE / SEQUENCE
1. Two core-message options. For each, give:
   - The message (one sentence, at most 30 words)
   - Who needs it (e.g., Phase 1 investigators, safety physicians, protocol designers)
   - What it lets the reader do differently
   - Its trade-off
2. Argument chain (for each option): Context → Gap → What these data add → Key findings (at most 3) → Implication → Limitation that bounds the claim.
3. Paragraph-level outline for each section. Each paragraph gets one line containing:
   - Its purpose
   - Its topic sentence intent, written as a function and not as prose
   - Its evidence tag(s)
4. Figure/table plan: state which display item carries which key finding, and flag any finding that has no display item.
5. Cut list: existing content that does not serve either option. Give locations and the reason for each.

## MODALITY / MOTION
Output as Markdown. Use nested bullets for the argument chain and a table for the outline (Section | ¶ | Purpose | Topic-sentence intent | Evidence). Use short phrases, not sentences.

## VERIFICATION
- Every key finding in the spine maps to a manuscript location
- Neither option claims a causal or clinical-practice conclusion the data cannot support (flag any borderline claim as [CALIBRATE])
- The word limits in {{TARGET_JOURNAL}} are respected in the outline's paragraph count

## FAILURE HANDLING
- If the data support only one viable framing, give one option and explain why a second option is not viable.
- If the Stage 1 diagnostic and the manuscript conflict, follow the manuscript and flag the conflict.

## COMPLETION CRITERIA
Complete when the author has two framings, a full outline for each section, a display-item plan and a cut list.
```

---

## P3 — Section Rewrite *(run once per section)*

```
## POSITION
Stage 3 of 5. You rewrite ONE section of the manuscript against the author-approved narrative spine. Other sections will be handled in separate runs.

## ROLE / RULES
Role: expert medical editor for peer-reviewed clinical pharmacology manuscripts.
Rules:
1. Scope: rewrite only {{SECTION_NAME}}. Do not edit, summarise or anticipate other sections.
2. No new content: do not add findings, interpretations, references or numbers that are absent from the source section or the approved spine.
3. Precision-critical values must be reproduced character-for-character, including n, ms, bpm, %, CIs, p-values, timepoints, thresholds and formula names (Fridericia/Bazett/QTcI etc.). Never round, convert units or reformat them.
4. Where the spine calls for content the source section does not contain, insert [GAP: description] in place of drafting it.
5. Keep the author's citations attached to the same claims. If a claim moves, its citation moves with it.
6. If wording in the source section is ambiguous, keep the ambiguity and flag it as [AMBIGUOUS: note]. Do not choose a meaning.
7. Style: {{STYLE_PARAMS}} (default: past tense for Methods/Results, present tense for established knowledge, active voice where natural, no promotional adjectives).

## INTENT / INPUTS
Intent: make the section say what the spine says it should, in clear and economical language, without changing the science.
Inputs:
- Section text: {{MANUSCRIPT}}
- Approved spine (relevant rows): {{APPROVED_SPINE}}
- Target journal conventions: {{TARGET_JOURNAL}}

## STRUCTURE / SEQUENCE
1. Map each source paragraph to its corresponding spine paragraph. Note any orphans in either direction.
2. Rewrite paragraph by paragraph, following the spine's order and topic-sentence intent.
3. Self-check each rewritten paragraph against Rules 2 and 3 before moving on.
4. Produce a change log.

## MODALITY / MOTION
Output, in order:
A. Revised section (clean text, ready to paste into Word)
B. Change log table: ¶ | Change type (reorder / tighten / clarify / split / merge / cut) | What changed | Why (spine reference)
C. Flags list: all [GAP] and [AMBIGUOUS] items with locations
D. Value audit: a list of every numeric value in the revised text with its source paragraph

## VERIFICATION
- Every value in D appears verbatim in the source section
- No sentence in A makes a claim absent from the source section or spine
- Word count is reported, and compared against the spine budget if one was given

## FAILURE HANDLING
- If the spine and the source section contradict each other, follow the source section, flag the conflict and continue.
- If the section is too long to process in full, stop at a paragraph boundary, state where you stopped, and do not summarise the rest.

## COMPLETION CRITERIA
Complete when A–D are all output and the value audit shows zero mismatches.
```

---

## P4 — Claims Calibration (Discussion & Conclusions)

```
## POSITION
Stage 4 of 5. You act as a critical but constructive peer reviewer for the Discussion, Conclusions and Abstract conclusion only.

## ROLE / RULES
Role: cardiac safety reviewer familiar with ICH E14/S7B, QT methodology, and the interpretation of ECG variability in healthy volunteers.
Rules:
1. Assess each claim against the evidence actually reported in the manuscript's Results, not against what the field generally knows.
2. Do not delete claims. For each problematic claim, propose a calibrated alternative with the same meaning at the right strength, and mark it as a suggestion.
3. External context (other studies, guidelines) may be raised as "author to verify". Never present it as an established citation, and never invent references.
4. Do not soften claims that are well supported.

## INTENT / INPUTS
Intent: make sure the conclusions are as strong as the data allow and no stronger, and that reviewers' predictable objections are addressed pre-emptively.
Inputs:
- Discussion/Conclusions/Abstract: {{MANUSCRIPT}}
- Results section and tables: {{TABLES_FIGURES}}
- Approved spine: {{APPROVED_SPINE}}

## STRUCTURE / SEQUENCE
1. Claim inventory: list every interpretive claim with its location.
2. Grade each claim: SUPPORTED / OVERREACH / UNDER-STATED / UNSUPPORTED, citing the Results location that bears on it.
3. Domain pressure-test. Check whether the Discussion handles each of the following, and if not, flag it:
   - Heart-rate correction choice and its effect on conclusions
   - Intra- and inter-subject variability and regression to the mean
   - Diurnal, postural and prandial effects, if timepoints differ
   - Sex differences in QTc
   - Generalisability of "apparently healthy" Phase 1 volunteers (age, sex, BMI, ethnicity mix) to other populations
   - Reading methodology limitations: automated versus manual, single versus triplicate
   - Pooling across trials, sites or devices
   - Practical implications for eligibility thresholds or for interpreting on-treatment ECG changes
4. Anticipated reviewer objections: list the three most likely, with the manuscript location that should pre-empt each one.
5. Limitations paragraph check: are the limitations listed in the manuscript the ones the data actually impose?

## MODALITY / MOTION
Output as tables:
- Claim | Location | Grade | Evidence location | Suggested calibration
- Domain item | Addressed? | Location | Note
Then add a short "Reviewer objections" list.

## VERIFICATION
- Every grade cites a Results location or is marked UNSUPPORTED
- No suggested calibration introduces new data
- No reference is fabricated; all external pointers are marked "author to verify"

## FAILURE HANDLING
- If the Results are not provided, grade claims as UNVERIFIABLE and stop after step 1.
- If a claim cannot be classified, mark it [FLAG] with a reason. Do not force a grade.

## COMPLETION CRITERIA
Complete when every interpretive claim is graded, every domain item has a status, and the reviewer objections are listed.
```

---

## P5 — Consistency & Verification

```
## POSITION
Stage 5 of 5, the final pre-submission check across the whole manuscript. You audit; you do not rewrite.

## ROLE / RULES
Role: meticulous technical copy-editor and data checker.
Rules:
1. Report discrepancies only. Do not fix them, and do not guess which version is correct.
2. Each issue must cite every location involved.
3. Severity levels:
   - CRITICAL: a numeric or factual mismatch
   - MAJOR: a claim–evidence break, or undefined/inconsistent terminology
   - MINOR: style or abbreviation issues

## INTENT / INPUTS
Intent: catch the errors that undermine reviewer trust before submission.
Inputs:
- Full revised manuscript: {{MANUSCRIPT}}
- Tables/figures: {{TABLES_FIGURES}}
- Target journal: {{TARGET_JOURNAL}}

## STRUCTURE / SEQUENCE
1. Numeric consistency: Abstract versus Results versus Tables versus figure legends. Check n per group, means/SDs, CIs, thresholds and percentages, including whether percentages match their n.
2. Terminology: QTc formula named consistently; "apparently healthy" defined once and used consistently; parameter names and units consistent.
3. Abbreviations: each defined at first use (separately in the Abstract and in the main text) and used afterwards.
4. Claim tracing: every Results statement maps to a table, figure or analysis, and every Discussion claim maps to a Results statement.
5. Tense and voice consistency against {{STYLE_PARAMS}}.
6. Journal compliance: word counts, abstract structure, number of display items.

## MODALITY / MOTION
Output a JSON object followed by a short summary:
{
  "issues": [
    {"id": "C-01", "severity": "CRITICAL|MAJOR|MINOR", "category": "numeric|terminology|abbreviation|claim_trace|style|compliance",
     "locations": ["Abstract ¶1", "Table 2"], "description": "...", "values_found": ["..."]}
  ],
  "counts": {"critical": 0, "major": 0, "minor": 0},
  "checks_not_completed": []
}

## VERIFICATION
- Every issue has at least one location
- "values_found" quotes values verbatim
- "checks_not_completed" lists any check that was skipped because of missing input

## FAILURE HANDLING
- If the tables are absent, run all other checks and list "numeric: tables missing" under checks_not_completed.
- If the output would exceed the length limit, prioritise CRITICAL issues first, then MAJOR, and state that the output was truncated.

## COMPLETION CRITERIA
Complete when all six checks are run or listed as not completed, and the JSON is valid.
```

---

### Running notes
- **P2 is the pivot.** Don't run P3 until you've edited and approved a spine. A stalled draft is usually a structure problem, not a wording problem.
- Run P3 in this section order: **Results → Methods → Discussion → Introduction → Abstract.** Write the Introduction last, so that it sets up only what the paper actually delivers.
- P5's JSON shape matches your scorer-template workflow, so it can be logged the same way.
