# Ph2 CSP — Review Comment Resolution Pipeline (v3)

A context-managed pipeline for resolving 250+ team-review comments on the Ph2 CSP draft. It runs in Scribbler; the only context is the Ph2 draft (full document), the cursor selection and the Ph1b protocol draft.

It is separate from `../Ph2_CSP_Comment_Triage/` (T1–T3 CRL + meeting-pack series).

| File | What it is |
|---|---|
| `extract_comments.py` | Stdlib-only extractor (openpyxl optional). Turns .docx comments into a tracker (.xlsx/.csv), ≤12-comment section batches, per-section text, a dependency map (X cross-ref / T repeated text / V shared value), duplicate hints, and a Ph1-residue keyword report. |
| `scribbler_comment_prompts.md` | P1 Triage → P2 Evidence extract (read-only) → P3 Draft revisions → P4 Dependency check → P5 Meeting log, plus the source-authority table and session hygiene rules. |
| `decisions_ledger.md` | Append-only, fixed-schema ledger carried between sessions (ACE-style deltas, never rewritten). Placeholder rows L-001–L-003 are examples; replace them before the first P3 run. |

## Quick start
```
python extract_comments.py Ph2_CSP_draft.docx
```
Outputs `<name>_comment_tracker.xlsx`, `comment_batches/`, `section_text/` and `ph1_residue_report.csv`.

## Design principles applied
Small active context; just-in-time selection (cursor + locators); reading kept apart from writing (P2 vs P3); state lives outside the window in a fixed-schema ledger; dependency-scoped consistency checks; one batch per fresh session (clearing over compaction). Ph1b is treated as unverified precedent (`[PRECEDENT]`), never as evidence.
