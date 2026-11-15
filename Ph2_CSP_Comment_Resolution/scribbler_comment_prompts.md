# Scribbler pipeline: Ph2 CSP review-comment resolution (v3)

## What is in context
| Source | Always present? | Authority | How to use it |
|---|---|---|---|
| **Ph2 CSP draft** (open document) | Yes, the full document, every session | The text under revision | Internal consistency only. It is not evidence that something is correct. |
| **Cursor selection** | Whatever you select before running | n/a | **Main targeting tool:** it sets the scope of each run |
| **Ph1b protocol draft** | Only when you attach it | **Precedent, unverified** (it is a draft too) | Programme wording and harmonisation. Any value from it gets marked `[PRECEDENT]` and must be confirmed. |
| Ph2 concept, IB, approved Ph1 DDI protocol | **Not available** | n/a | Anything that needs them becomes `[TBD]` or category D, with an owner |

### Consequences for the design
1. **Isolation can't be enforced by the setup.** The full Ph2 draft is always in context, so in P3 the "work from the evidence packet only" rule rests on the instruction alone. Mechanical backstops: P2 extracts are verbatim and numbered, P3 must cite every substantive change, and P4 re-checks.
2. **The whole draft is the main distractor.** Every prompt therefore sets its scope explicitly ("the selected text and the sections listed below; ignore the rest"). Select the target section before every run.
3. **The Ph1b draft is a near-duplicate document.** Attach it only for P2, and only when P1's locator asks for it. Never attach it for P3 or P4.
4. **Without the concept, few comments can be resolved from evidence.** Expect more D items and TBDs than usual. That is correct behaviour, not a failure: the meeting log (P5) is where they get resolved.
5. **Ph1 residue can't be checked against the Ph1 protocol.** Use `ph1_residue_report.csv` from the extractor (keyword scan) instead. Some hits will be legitimate wording shared with Ph1b; judge each one.

## Pipeline at a glance
| Step | Prompt | Cursor selection | Attach Ph1b? | Paste | Output |
|---|---|---|---|---|---|
| 0 | `extract_comments.py` | n/a | n/a | n/a | tracker, batches (≤12), section_text/, residue report |
| 1 | P1 Triage | none | **No** | 1 batch file | category + locator per Ref |
| 2 | P2 Evidence extract | the CSP section(s) named in the locators | **Only if a locator names Ph1b** | locator list | numbered verbatim packet |
| 3 | P3 Draft revisions | **the target section** | **No** | batch + packet + ledger | revisions + ledger deltas |
| 4 | P4 Dependency check | each `MAY AFFECT` section in turn (or paste from `section_text/`) | **No** | P3 output | knock-on edits |
| 5 | P5 Meeting log | none | No | D/E/G rows + packet + ledger | decision table |

## Session hygiene
- **One batch per fresh session.** Carry only `decisions_ledger.md` forward.
- **Select before you run.** If the selection is empty or wrong, the model drifts across the whole draft.
- **Category A (editorial):** fix it by hand in Word. No pipeline needed.
- **Category F (duplicate):** resolve the first Ref of the group; reply to the others with a pointer to it.
- **The ledger is append-only.** Never ask the model to rewrite or summarise it.

---

## P1: Triage
**Position:** You are a senior regulatory medical writer triaging team-review comments on the open Phase 2 CSP draft. The draft was converted from a Phase 1 DDI protocol, so leftover Phase 1 content is a known risk.

**Available sources:** the Ph2 draft (open document) and, on request, a **Ph1b protocol draft** (unverified precedent). The study concept, IB and Ph1 protocol are **not available**.

**Rules**
- Classify every Ref in the batch below. Do not skip, merge or renumber any of them.
- Do not draft text and do not answer scientific questions.
- **Scope:** read only the sections the batch names. Do not survey the rest of the document.
- Treat `POSSIBLE DUPLICATE OF` and `MAY AFFECT SECTIONS` as hints. Confirm or reject each one.

**Output:** one table:
`Ref | Category | Priority | Rationale (≤20 words) | Locator | Duplicate of | Ph1 residue (Y/N)`

- **Categories:**
  - A-Editorial
  - B-Consistency: resolvable from elsewhere in the Ph2 draft
  - C-Precedent: Ph1b may offer harmonised wording or a value, to be confirmed
  - D-Decision: needs the concept, IB, or a team/sponsor call
  - E-Decline
  - F-Duplicate
  - G-Query to reviewer
  - R-Residue removal: Ph1 content with no Ph2 role
- **Locator:**
  - `CSP §x.y` for B
  - `Ph1b §x.y` for C
  - `Needs: concept / IB / <function>` for D
  - `none` otherwise

**Verification:** first line `Comments in batch: N | Rows: N`.
**Completion:** finish with counts per category, then a de-duplicated locator list split into **CSP sections** and **Ph1b sections**.

---

## P2: Evidence extract (read-only)
**Position:** You extract evidence. You do not write protocol text and you make no decisions.

**Scope:** the selected text, the CSP sections listed below, and (if attached) the listed Ph1b sections. Ignore everything else.

**Rules**
- For each locator, copy the **verbatim** text, values and units relevant to the listed Refs.
- Tag every extract with its authority: `CSP` (current draft wording, consistency only) or `Ph1b-PRECEDENT` (unverified draft).
- If the expected information isn't there, record it under NOT FOUND. Do not look elsewhere and do not infer.
- If the CSP and Ph1b differ on the same parameter, extract **both** and mark the pair `DIVERGENT`.

**Output:**
```
EVIDENCE PACKET – batch <id>
[E1] Refs: C012 | CSP §5.1 | Verbatim: "…" | Values: …
[E2] Refs: C014 | Ph1b-PRECEDENT §6.3 | Verbatim: "…" | Values: …
[E3] DIVERGENT with E1 | …
NOT FOUND: <locator> – <expected> – Refs
```
**Verification:** every Ref with category B or C appears in an E-entry or under NOT FOUND.

---

## P3: Draft revisions
**Position:** You are a senior regulatory medical writer revising the **selected section** of the Phase 2 CSP draft.

**Scope:** revise **only the selected text**. Base every change on the evidence packet and the decisions ledger pasted below. The rest of the open document is visible to you but is **not a source**. Do not draw on it.

**Rules**
- Make the minimum change needed. Keep house style, tense and defined abbreviations.
- Every substantive change cites `[E#]` or `[L-###]`. An uncited substantive change is a failure.
- A value that comes only from a `Ph1b-PRECEDENT` extract is written as `[PRECEDENT: <value>, Ph1b §x – confirm]`, never as plain text.
- Where evidence is missing, write `[TBD: <what is needed> – <owner>]`. Never invent doses, timepoints, criteria or limits.
- **Residue removal (R):** delete the text only if the ledger or the comment confirms it has no Ph2 role. Otherwise write `[FLAG: possible Ph1 residue]`.
- **A ledger decision overrides your judgement.** If a comment conflicts with the ledger, flag it; do not revise.

**Output:** for each Ref:
```
Ref: C0xx | Cat: B/C/R
CURRENT: <exact text>
REVISED: <text, changes in **bold**>
BASIS: [E#] / [L-###] / editorial
REVIEWER RESPONSE: <one sentence>
FLAGS: none | …
```
Then:
```
PRECISION-CRITICAL CHANGES: <old → new | Ref | basis>   (or "none")
LEDGER DELTAS (append only):
ADD  L-NEW | <type> | <statement ≤25 words> | Refs | Basis
MOD  L-### | <change and reason> | Refs | Basis
```
**Completion:** Refs addressed / Refs not addressed (with the reason for each).

---

## P4: Dependency check
**Position:** You check consistency. Do not polish or restyle.

**Scope:** the selected section (one of the `MAY AFFECT SECTIONS` targets), or the pasted `section_text/` files, compared against the P3 output below.

**Rules**
- Find text that contradicts a revision, or that still carries the old wording or value.
- Hint codes:
  - X = cross-reference
  - T = repeated text (often the Synopsis)
  - V = shared value
- If a hint is a false positive, say so in one line.

**Output:**
`Section | Current text | Conflicts with (Ref) | Required edit | Type (value / wording / cross-ref)`

---

## P5: Comment resolution meeting log (D, E, G and DIVERGENT items)
**Output:**
`Ref | Reviewer | Issue (≤15 words) | Missing source or decision | Options (2–3, implications cited to E#/L-###) | Suggested position | Owner`

**Rules**
- Present options neutrally; never present a suggestion as decided.
- Put conflicting comments in adjacent rows marked **CONFLICT**.
- Group the items that need the **concept** or the **IB**, so one owner can clear them in a single pass.
- After the meeting, record each decision as an `ADD` line in the ledger.
