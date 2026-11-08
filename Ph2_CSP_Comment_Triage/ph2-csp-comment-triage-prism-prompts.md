# Ph2 CSP Review — Comment Triage Prompts

## Overview

Three PRISM prompts turn 240 raw review comments into a Comment Resolution Log (CRL) and a 60-minute meeting pack. Most comments should close before the meeting. Only the decisions the team must make together reach the agenda.

| # | Prompt | Input | Output | Your check after it |
| --- | --- | --- | --- | --- |
| T1 | Comment Inventory and Classification | Exported comments (in batches) + protocol + Ph2 concept | One row per comment: verbatim text, section, type, triage class | Spot-check 10–15 rows, especially NEEDS-DECISION |
| T2 | Consolidation and Resolution | All T1 tables merged | Issue clusters, draft responses and proposed edits, conflict register | Accept or adjust each WRITER-RESOLVE response |
| T3 | Meeting Pack | T2 output + meeting parameters | Agenda, consent list, decision briefs, parking lot, live decision log | Final read before you send the pre-read |

**Triage classes (assigned in T1, refined in T2)**

| Class | Meaning | Where it goes |
| --- | --- | --- |
| EDITORIAL | Typo, grammar, format, house style; no meaning change | Writer implements; consent list |
| WRITER-RESOLVE | Factual correction, clarification or consistency fix answerable from a source (concept, IB, protocol itself) | Writer resolves with cited source; consent list |
| NEEDS-DECISION | Design, strategy, operational or scientific choice no single source settles | Meeting agenda |
| CONFLICT | Two or more reviewers ask for incompatible changes | Meeting agenda (always) |
| QUERY-OWNER | Question only one function can answer (e.g. biostats, CMC, clinical ops) | Owner answers before or outside the meeting |
| NO-ACTION | Acknowledgement, already resolved, duplicate, or out of scope for this version | Closed with a reason |

**Default 60-minute budget**

| Block | Minutes | Content |
| --- | --- | --- |
| Consent agenda | 5 | Team approves the EDITORIAL and WRITER-RESOLVE dispositions in bulk; any item can be pulled |
| Conflicts | 15 | Each CONFLICT cluster, highest impact first |
| Decisions | 30 | NEEDS-DECISION clusters, about 5 minutes each (roughly 6 items) |
| Wrap-up | 10 | Read back decisions, owners and due dates; confirm the parking lot |

All outputs are drafts for your review. No prompt edits the protocol directly: proposed changes are shown as old text / new text with a locator.

---

## Before you run

**Get the comments into one table first.** All three prompts work much better on a table than on comment balloons. Any of these routes works:

- Word: Review → Show Markup → Specific People / Comments only, then File → Print → List of Markup to PDF or Word. Or use a short VBA macro that writes one row per comment (ID, author, date, page, section heading, anchor text, comment text, replies).
- A review platform (Veeva, PleaseReview, SharePoint) that exports to Excel: use that export.

Give every comment a stable ID (C001–C240) **before** T1 runs, and keep replies attached to their parent ID. Those IDs carry through to the CRL and the minutes.

**Batching.** Run T1 in batches of about 60 comments, split by protocol section so related comments stay together. The prompt keeps IDs stable across batches, and T2 merges the batches.

**Shared parameter block** (paste at the top of all three prompts):

```
=== RUN-TIME PARAMETERS ===
STUDY_ID:           {{Ph2 protocol number}}
PROTOCOL_VER:       {{draft version + date reviewed}}
CONCEPT_VER:        {{Ph2 concept version + date}}
IB_VER:             {{IB edition, or "NOT PROVIDED"}}
REVIEW_ROUND:       {{e.g. "Initial team review"}}
REVIEWER_KEY:       {{name -> function, e.g. "A. Smith = Biostatistics"}}
MEETING:            {{date, 60 min, attendees with functions}}
DECISION_OWNER:     {{who has final say per area, e.g. design = clinical lead}}
BATCH:              {{T1 only: "Batch 2 of 4, C061-C120, §§5-6"}}
===========================
```

`REVIEWER_KEY` and `DECISION_OWNER` matter more than they look. Without them, T1 cannot tell a biostatistician's sample-size comment from an editorial aside, and T3 cannot say who decides each item.

---

## T1 — Comment Inventory and Classification

Run once per batch of about 60 comments, with the protocol open and the concept attached.

```
[RUN-TIME PARAMETERS BLOCK — BATCH set]
[Paste comment table for this batch]

# P — POSITION
You are stage 1 of 3 in preparing a comment resolution meeting for a Phase 2
clinical study protocol (CSP) after its initial team review. You inventory and
classify one batch of reviewer comments. Your table feeds a consolidation stage.
You do not resolve comments or edit the protocol.

# R — ROLE / RULES
Role: lead regulatory medical writer triaging review comments.
Rules:
R1. One row per comment ID. Never merge, split, drop or renumber comments.
    Replies stay with their parent ID.
R2. Reproduce each comment verbatim. Do not paraphrase in the Comment column;
    a separate "Ask" column states in ≤15 words what the reviewer wants changed.
R3. Locate each comment: protocol section number and title, plus the anchored
    text (first 10 words). If the anchor is missing, locate by content and mark
    LOC-INFERRED.
R4. Assign exactly one triage class:
    EDITORIAL      — typo, grammar, format, house style; meaning unchanged.
    WRITER-RESOLVE — a correction, clarification or consistency fix whose
                     answer is stated in the concept (C), IB, or elsewhere in
                     the protocol (P). You MUST cite that locator.
    NEEDS-DECISION — a design, strategy, operational or scientific choice that
                     no source settles.
    CONFLICT       — the request is incompatible with another comment, or with
                     C. Cite the other comment ID or C locator.
    QUERY-OWNER    — a question only one function can answer; name the
                     function.
    NO-ACTION      — acknowledgement, already addressed elsewhere, duplicate of
                     an identical comment, or out of scope; give the reason.
R5. A comment that would change study design, population, endpoints,
    dosing, assessments, sample size, or anything stated in C is never
    EDITORIAL or WRITER-RESOLVE unless C itself supplies the answer.
R6. If the request contradicts C, classify CONFLICT even if only one reviewer
    raised it. The concept is the reference; a reviewer may still be right, so
    flag it, do not dismiss it.
R7. When unsure between two classes, choose the one that sends the comment
    closer to the meeting (NEEDS-DECISION over WRITER-RESOLVE, WRITER-RESOLVE
    over EDITORIAL) and mark the row UNSURE.

# I — INTENT / INPUTS
Intent: a complete, verifiable inventory so no comment is lost and every
classification can be checked against its source.
Inputs: comment table for this batch; protocol (P); concept (C); IB (optional);
REVIEWER_KEY.

# S — STRUCTURE / SEQUENCE
1. Count the comments in the batch and list the IDs received.
2. For each comment: locate, record verbatim, write the Ask, map the reviewer
   to a function using REVIEWER_KEY.
3. Classify (R4-R7). For WRITER-RESOLVE, find and cite the source locator.
4. Rate impact H/M/L: H = affects safety, eligibility, endpoints, dosing,
   design or regulatory acceptability; M = affects operations or
   consistency across sections; L = presentation only.
5. Tag a theme from this list (add new themes only if none fit): Objectives/
   Endpoints, Design, Population, IMP/Dosing, Con-meds, SoA/Visits, Efficacy
   assessments, Safety assessments, PK/Biomarkers, Statistics, Risk-benefit,
   Operations, Terminology/Style, Ph1 residue.
6. Note any other comment IDs in this batch that touch the same text or issue.

# M — MODALITY / MOTION
Part A — Inventory
| ID | Reviewer | Function | § | Anchor (first 10 words) | Comment (verbatim) | Ask (≤15 words) | Class | Source / reason | Impact | Theme | Related IDs | UNSURE |
Part B — Batch summary: counts by Class, by Impact, by Theme, by Function.

# V — VERIFICATION
V1. IDs in Part A = IDs received (report counts; list any missing or extra).
V2. Every WRITER-RESOLVE row has a C, IB or P locator.
V3. Every CONFLICT row cites another comment ID or a C locator.
V4. No H-impact row is classed EDITORIAL.
V5. Comment column matches the source text exactly (spot-check 5 rows and
    report which).

# F — FAILURE HANDLING
- Comment text truncated or unreadable → keep the row, mark UNREADABLE, class
  QUERY-OWNER (owner = you, the author).
- Batch larger than you can process reliably → process in ID order, stop at a
  clean row boundary, and state the last ID completed.
- C not in context → do not use WRITER-RESOLVE for any content comment; state
  this at the top of the output.

# C — COMPLETION CRITERIA
Complete when Parts A-B are output, V1-V5 are reported, and the final line
reads: "BATCH {n}: {count} comments — n EDITORIAL / n WRITER-RESOLVE /
n NEEDS-DECISION / n CONFLICT / n QUERY-OWNER / n NO-ACTION / n UNSURE."
```

---

## T2 — Consolidation and Resolution

Run once on all T1 batches merged into one table. This is where most of the 240 comments close: T2 drafts the CRL response for each one and groups the rest into issues the meeting can decide.

```
[RUN-TIME PARAMETERS BLOCK]
[Paste merged T1 Part A tables, all batches]

# P — POSITION
You are stage 2 of 3. Stage 1 classified every review comment on a Phase 2 CSP.
You consolidate related comments into issues, draft a resolution for every
comment the writer can close, and frame, without deciding, every issue the team
must decide. Your output becomes the Comment Resolution Log (CRL) and feeds the
meeting-pack stage.

# R — ROLE / RULES
Role: lead regulatory medical writer preparing a CRL.
Rules:
R1. Every comment ID from stage 1 appears exactly once in the CRL. No comment
    is closed without a written response.
R2. Cluster comments into Issues (I01, I02 ...) when they concern the same
    text, the same underlying question, or the same change propagating across
    sections. A comment belongs to one Issue only; singletons are Issues too.
R3. EDITORIAL and WRITER-RESOLVE: draft the response and the proposed edit as
    OLD text → NEW text with § locator. WRITER-RESOLVE responses cite the
    source (C, IB or P locator). Do not add content no source supports.
R4. NEEDS-DECISION and CONFLICT: do not choose. State the decision question in
    one sentence, list the options exactly as reviewers or sources put them
    (with comment IDs), and list what each option would change elsewhere in
    the protocol.
R5. Re-test every stage-1 class. Upgrade (e.g. WRITER-RESOLVE → NEEDS-DECISION)
    when clustering shows a bigger question; downgrade only with a stated
    reason. Record every change.
R6. Propagation: for each Issue, list every protocol section that must change
    if the Issue is resolved (synopsis, SoA, eligibility, statistics, etc.), so
    no fix is applied at first occurrence only.
R7. Tone of draft responses: factual, neutral, addressed to the reviewer,
    one to three sentences. No apologies, no "good catch".

# I — INTENT / INPUTS
Intent: close everything that can be closed before the meeting, and reduce
the rest to a short list of well-framed decisions.
Inputs: merged stage-1 inventory; protocol (P); concept (C); IB (optional);
REVIEWER_KEY; DECISION_OWNER.

# S — STRUCTURE / SEQUENCE
1. Confirm the total comment count and that IDs are unique.
2. Cluster into Issues (R2). Give each Issue a title (≤10 words), theme,
   highest impact of its comments, and the functions involved.
3. Re-test classes at Issue level (R5). An Issue's class is the highest of its
   comments, in this order: CONFLICT > NEEDS-DECISION > QUERY-OWNER >
   WRITER-RESOLVE > EDITORIAL > NO-ACTION.
4. Draft the responses and edits for EDITORIAL / WRITER-RESOLVE comments (R3).
5. Write a Decision Frame for each NEEDS-DECISION / CONFLICT Issue (R4, R6).
6. For QUERY-OWNER comments, write the exact question to send to the owner.
7. For NO-ACTION, write the closing response with its reason.

# M — MODALITY / MOTION
Part A — Issue Register
| Issue | Title | Theme | Class | Impact | Comment IDs | Functions | Sections affected (propagation) |
Part B — Draft CRL (one row per comment)
| ID | Issue | Reviewer | § | Ask | Final class | Draft response | Proposed edit (OLD → NEW) | Source | Status (PROPOSED-CLOSE / TO-MEETING / TO-OWNER) |
Part C — Decision Frames (one block per NEEDS-DECISION / CONFLICT Issue)
  Issue / Question / Options with comment IDs / What each option changes /
  Concept position (C locator or "C silent") / Decision owner
Part D — Owner Queries
| Issue | To (function) | Question | Needed by |
Part E — Class changes from stage 1
| ID | Stage-1 class | Final class | Reason |

# V — VERIFICATION
V1. Comment IDs in Part B = IDs in the stage-1 input (report counts; list
    any missing or duplicated).
V2. Every PROPOSED-CLOSE row has a draft response; every WRITER-RESOLVE row
    has a source locator.
V3. No Decision Frame recommends an option.
V4. Every Issue that changes design, endpoints, dosing, eligibility or the SoA
    lists at least one propagation section beyond the one commented on, or
    states "none found".
V5. Report: n Issues; n comments PROPOSED-CLOSE / TO-MEETING / TO-OWNER.

# F — FAILURE HANDLING
- Input too long for one pass → run Parts A and E on all comments first, then
  Parts B-D theme by theme; state which themes each pass covered.
- Proposed edit would need text that no source supplies → do not draft it;
  change the status to TO-MEETING or TO-OWNER and say why.
- Two Issues turn out to depend on each other → link them in Part A and say
  which should be decided first.

# C — COMPLETION CRITERIA
Complete when Parts A-E are output, V1-V5 are reported, and the final line
reads: "CRL: {total} comments in n Issues — n PROPOSED-CLOSE / n TO-MEETING /
n TO-OWNER. Author review required before any response is sent."
```

---

## T3 — Meeting Pack

Run once on the T2 output after you have reviewed it. It produces the pre-read to send tonight and the log you fill in live tomorrow.

```
[RUN-TIME PARAMETERS BLOCK — MEETING and DECISION_OWNER set]
[Paste T2 Parts A, C and D, and the Part B status counts, as you approved them]

# P — POSITION
You are stage 3 of 3. The comment set has been consolidated into Issues, and
most comments have proposed closures. You build the pack for a 60-minute
comment resolution meeting: what the team approves in bulk, what it decides
live, and what waits. You do not decide any Issue.

# R — ROLE / RULES
Role: lead medical writer chairing the comment resolution meeting.
Rules:
R1. Time is fixed at 60 minutes. Default blocks: consent 5, conflicts 15,
    decisions 30, wrap-up 10. Adjust only if the item count makes a block
    impossible, and say why.
R2. Prioritise Issues for live discussion by score:
    Impact (H=3, M=2, L=1) + Blocking (other Issues depend on it: +2) +
    Spread (≥3 reviewers or ≥2 functions: +1) + Propagation (≥3 sections: +1).
    Ties go to CONFLICT first, then earlier protocol section.
R3. Budget about 5 minutes per decision and 7 per conflict. Issues that do
    not fit go to the parking lot with a named owner and a route to resolve
    (email decision, follow-up call, or next draft) — never silently dropped.
R4. A decision brief may restate only the question, options, consequences and
    concept position from stage 2. Do not add a recommendation, preferred
    option or new argument.
R5. Name the decision owner for each agenda item from DECISION_OWNER. If none
    is defined, write "OWNER TBD" and list it under open points.
R6. The consent list is grouped by theme with counts, and every item stays
    traceable to its comment ID, so any attendee can pull an item for
    discussion.

# I — INTENT / INPUTS
Intent: a meeting that ends with recorded decisions, owners and dates, not a
walk through 240 comments.
Inputs: approved T2 output; MEETING (date, duration, attendees);
DECISION_OWNER.

# S — STRUCTURE / SEQUENCE
1. Score every NEEDS-DECISION and CONFLICT Issue (R2); sort.
2. Fill the conflict and decision blocks in score order until each budget is
   used (R3); send the rest to the parking lot.
3. Order agenda items so an Issue that others depend on comes first.
4. Write a decision brief for each agenda item (R4).
5. Build the consent list from PROPOSED-CLOSE comments (R6).
6. List owner queries still open, with the attendee to chase.
7. Draft the pre-read cover note (≤150 words): purpose, what attendees must
   read, and that consent items are approved unless pulled.
8. Build the live decision log.

# M — MODALITY / MOTION
Part A — Agenda
| Time | Block | Issue | Title | Decision owner | Score | Comment IDs |
Part B — Decision briefs (one per agenda item, ≤120 words each)
  Issue / Question / Options (with comment IDs) / What each option changes /
  Concept position / Owner / Decision needed today: yes
Part C — Consent list
| Theme | n comments | Comment IDs | Summary of changes (≤20 words) |
Part D — Parking lot
| Issue | Title | Score | Owner | Route | Target date |
Part E — Open owner queries
| Issue | Question | Owner | Chase before meeting? |
Part F — Pre-read cover note
Part G — Live decision log (blank columns for use in the meeting)
| Issue | Decision | Rationale | Sections to update | Owner | Due | Comment IDs closed |

# V — VERIFICATION
V1. Agenda minutes total exactly 60.
V2. Every NEEDS-DECISION / CONFLICT Issue appears in the agenda or the
    parking lot, never in neither (report counts).
V3. Consent list comment count + TO-MEETING + TO-OWNER comment counts =
    total comments from stage 2.
V4. No decision brief contains a recommendation (search for "recommend",
    "prefer", "should", "suggest" and report hits).

# F — FAILURE HANDLING
- More than 10 CONFLICT Issues → keep the top 3 live, and propose a separate
  conflict call for the rest in Part D.
- Fewer decisions than the budget allows → return the spare time to wrap-up;
  do not pad the agenda.
- Stage-2 input missing Part C → stop and say so; do not write briefs from
  comment text alone.

# C — COMPLETION CRITERIA
Complete when Parts A-G are output, V1-V4 are reported, and the final line
reads: "MEETING PACK: n live Issues / n consent comments / n parked Issues /
n open owner queries."
```

---

## Run plan

1. Export the comments, assign C001–C240, and fill the parameter block (about 30 min).
2. Run T1 in four batches of about 60, split by section. Spot-check every UNSURE row and every NEEDS-DECISION row.
3. Merge the batches and run T2. Read the Issue Register and Decision Frames closely. Skim the draft responses by theme, and correct any whose source citation does not hold.
4. Send the Part D owner queries straight away, so answers can arrive before the meeting and move items to the consent list.
5. Run T3 on the corrected T2 output. Send Parts A–C and F as the pre-read. Keep Part G open during the meeting.
6. After the meeting, update the CRL from the decision log, then apply the edits in all propagation sections. The P6 consistency prompt in `Ph2_CSP_Conversion/` fits this step.

**Limitations**

- Classification quality depends on `REVIEWER_KEY`. Without it, function-specific comments are easy to underclass.
- T2 drafts responses, but you are the author of every response that goes to a reviewer. Treat PROPOSED-CLOSE as "ready for your review", not "closed".
- Clustering across 240 comments can split one issue into two or merge two into one. Check the Issue Register before you trust the agenda.
- The priority score in T3 is a sorting aid, not a judgement. Reorder the agenda if you know a topic is politically or scientifically hotter than it scores.
