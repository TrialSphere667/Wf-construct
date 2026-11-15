#!/usr/bin/env python3
"""
extract_comments.py - Pull all Word review comments out of a .docx into a
triage tracker, plus per-section batch files ready to paste into Scribbler.

Standard library only (openpyxl used for .xlsx if installed, else CSV).

Usage:
    python extract_comments.py PROTOCOL.docx
    python extract_comments.py PROTOCOL.docx --out tracker.xlsx --batches batches --batch-level 1

Output:
    - Tracker (one row per comment thread; replies folded in), with empty
      triage columns: Category / Priority / Owner / Action / Status.
    - comment_batches/: open comments by section, capped at --max-per-batch,
      with duplicate and dependency hints.
    - section_text/: plain text per section, so a consistency check can be
      given only the sections an edit affects.

Dependency codes in "Dependent Sections":
    X = that section cross-references this one ("Section 6.2")
    T = that section repeats the commented text verbatim (often the Synopsis)
    V = that section contains a dose/timepoint/value from the commented text

Notes:
    - Section numbers are computed by counting headings (outline levels) in
      document order. They match auto-numbered protocols in most cases, but
      check them against the TOC once.
    - Works with English and German style names (Heading / Ueberschrift).
    - Text in tracked deletions is ignored; tracked insertions are included.
    - Comments anchored in headers/footers/footnotes are not located (reported
      with section "UNLOCATED").
"""
import argparse
import csv
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"


def q(ns, tag):
    return "{%s}%s" % (ns, tag)


def read_xml(z, name):
    try:
        return ET.fromstring(z.read(name))
    except KeyError:
        return None


def para_text(p):
    """Visible text of a paragraph (insertions kept, deletions skipped)."""
    out = []
    for el in p.iter():
        if el.tag == q(W, "t") and el.text:
            out.append(el.text)
        elif el.tag == q(W, "tab"):
            out.append(" ")
        elif el.tag in (q(W, "br"), q(W, "cr")):
            out.append(" ")
    return re.sub(r"\s+", " ", "".join(out)).strip()


# ---------------------------------------------------------------- styles ----
def load_style_outline_levels(z):
    """styleId -> outline level (0-based) for heading-like styles."""
    root = read_xml(z, "word/styles.xml")
    levels, based_on, names = {}, {}, {}
    if root is None:
        return levels
    for st in root.findall(q(W, "style")):
        sid = st.get(q(W, "styleId"))
        name_el = st.find(q(W, "name"))
        names[sid] = (name_el.get(q(W, "val")) if name_el is not None else "") or ""
        b = st.find(q(W, "basedOn"))
        if b is not None:
            based_on[sid] = b.get(q(W, "val"))
        ol = st.find("%s/%s" % (q(W, "pPr"), q(W, "outlineLvl")))
        if ol is not None:
            levels[sid] = int(ol.get(q(W, "val")))

    def resolve(sid, depth=0):
        if sid in levels:
            return levels[sid]
        nm = names.get(sid, "").lower()
        m = re.match(r"(heading|überschrift|ueberschrift)\s*(\d)", nm)
        if m:
            return int(m.group(2)) - 1
        if sid in based_on and depth < 10:
            return resolve(based_on[sid], depth + 1)
        return None

    return {sid: resolve(sid) for sid in names if resolve(sid) is not None}


def para_outline_level(p, style_levels):
    ppr = p.find(q(W, "pPr"))
    if ppr is None:
        return None
    ol = ppr.find(q(W, "outlineLvl"))
    if ol is not None:
        lvl = int(ol.get(q(W, "val")))
        return lvl if lvl < 9 else None
    ps = ppr.find(q(W, "pStyle"))
    if ps is not None:
        return style_levels.get(ps.get(q(W, "val")))
    return None


# -------------------------------------------------------------- comments ----
def load_comments(z):
    root = read_xml(z, "word/comments.xml")
    comments = {}
    if root is None:
        return comments
    for c in root.findall(q(W, "comment")):
        cid = c.get(q(W, "id"))
        paras = c.findall(q(W, "p"))
        text = "\n".join(t for t in (para_text(p) for p in paras) if t)
        last_para_id = paras[-1].get(q(W14, "paraId")) if paras else None
        comments[cid] = {
            "id": cid,
            "author": c.get(q(W, "author"), ""),
            "date": (c.get(q(W, "date"), "") or "")[:10],
            "text": text,
            "para_id": last_para_id,
            "parent": None,
            "done": False,
            "anchor": "",
            "context": "",
            "section_no": "UNLOCATED",
            "section_title": "",
            "order": 10**9,
        }
    # threading + resolved state
    ext = read_xml(z, "word/commentsExtended.xml")
    if ext is not None:
        by_para = {c["para_id"]: c for c in comments.values() if c["para_id"]}
        for ce in ext.findall(q(W15, "commentEx")):
            c = by_para.get(ce.get(q(W15, "paraId")))
            if not c:
                continue
            c["done"] = ce.get(q(W15, "done")) == "1"
            parent_pid = ce.get(q(W15, "paraIdParent"))
            if parent_pid and parent_pid in by_para:
                c["parent"] = by_para[parent_pid]["id"]
    return comments


# -------------------------------------------------------------- document ----
def locate_comments(z, comments, style_levels):
    doc = read_xml(z, "word/document.xml")
    body = doc.find(q(W, "body"))
    counters = [0] * 9
    state = {"sec_no": "0", "sec_title": "(front matter)", "order": 0}
    open_ranges = {}
    sections = {"0": {"title": "(front matter)", "paras": []}}

    def heading_update(lvl, title):
        counters[lvl] += 1
        for i in range(lvl + 1, 9):
            counters[i] = 0
        nums = [str(n) for n in counters[: lvl + 1]]
        # trim leading zeros for documents whose first heading is level>0
        while len(nums) > 1 and nums[0] == "0":
            nums.pop(0)
        state["sec_no"] = ".".join(nums)
        state["sec_title"] = title
        sections.setdefault(state["sec_no"], {"title": title, "paras": []})

    def stamp(cid, ptext):
        c = comments.get(cid)
        if c and c["section_no"] == "UNLOCATED":
            c["section_no"] = state["sec_no"]
            c["section_title"] = state["sec_title"]
            c["context"] = ptext
            state["order"] += 1
            c["order"] = state["order"]

    def walk(el, ptext):
        for child in el:
            tag = child.tag
            if tag == q(W, "p"):
                txt = para_text(child)
                lvl = para_outline_level(child, style_levels)
                if lvl is not None and txt:
                    heading_update(lvl, txt)
                elif txt:
                    sections[state["sec_no"]]["paras"].append(txt)
                walk(child, txt)
                for cid in open_ranges:
                    open_ranges[cid].append(" ")
            elif tag == q(W, "commentRangeStart"):
                cid = child.get(q(W, "id"))
                open_ranges[cid] = []
                stamp(cid, ptext)
            elif tag == q(W, "commentRangeEnd"):
                cid = child.get(q(W, "id"))
                buf = open_ranges.pop(cid, None)
                if buf is not None and cid in comments:
                    comments[cid]["anchor"] = re.sub(r"\s+", " ", "".join(buf)).strip()
            elif tag == q(W, "commentReference"):
                stamp(child.get(q(W, "id")), ptext)
            elif tag == q(W, "t"):
                if child.text:
                    for buf in open_ranges.values():
                        buf.append(child.text)
            elif tag == q(W, "del"):
                continue  # skip tracked deletions
            else:
                walk(child, ptext)

    walk(body, "")
    return sections



# ------------------------------------------------- dependency map (LEDGER) --
XREF_RE = re.compile(r"\b(?:Sections?|Abschnitte?|Kapitel)\s+(\d+(?:\.\d+)*)", re.I)
VALUE_RE = re.compile(
    r"\b(?:(?:Day|Visit|Week|Tag|Woche|Cycle|Zyklus)\s+-?\d+"
    r"|\d+(?:[.,]\d+)?\s?(?:mg/kg|mg|µg|mcg|g|mL|ml|L|kg|h|hours?|hrs?|days?|weeks?|months?|%|mmHg|bpm|msec|ms|years?))\b",
    re.I)


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def related(a, b):
    return a == b or a.startswith(b + ".") or b.startswith(a + ".")


def build_dependencies(threads, sections):
    """For each thread, list other sections likely affected by an edit:
    - X: sections that cross-reference this section ("Section 6.2")
    - T: sections repeating the anchored text verbatim (e.g. Synopsis)
    - V: sections containing a precision-critical value found in the anchor."""
    sec_text = {k: norm(" ".join(v["paras"])) for k, v in sections.items()}
    xrefs = {}  # referenced section -> set(referencing sections)
    for k, v in sections.items():
        for m in XREF_RE.finditer(" ".join(v["paras"])):
            xrefs.setdefault(m.group(1), set()).add(k)
    for t in threads:
        sec = t["section_no"]
        hits = {}
        if sec != "UNLOCATED":
            for ref, srcs in xrefs.items():
                if related(ref, sec):
                    for src in srcs:
                        if not related(src, sec):
                            hits.setdefault(src, set()).add("X")
        anchor = norm(t["anchor"])
        if len(anchor) >= 25:
            for k, txt in sec_text.items():
                if not related(k, sec) and anchor in txt:
                    hits.setdefault(k, set()).add("T")
        vals = {norm(m.group(0)) for m in VALUE_RE.finditer(t["anchor"])}
        t["values"] = sorted(vals)
        for v in vals:
            pat = re.compile(r"(?<![\w.,])" + re.escape(v) + r"(?![\w])")
            for k, txt in sec_text.items():
                if not related(k, sec) and pat.search(txt):
                    hits.setdefault(k, set()).add("V")
        def sk(x):
            return [int(n) if n.isdigit() else 0 for n in x.split(".")]
        t["deps"] = ["%s (%s)" % (k, "".join(sorted(h))) for k, h in sorted(hits.items(), key=lambda kv: sk(kv[0]))]


def find_duplicates(threads, threshold=0.8):
    """Flag likely duplicate comments: near-identical text, or same anchor."""
    import difflib
    for t in threads:
        t["dups"] = []
    open_t = [t for t in threads if not t["done"]]
    for i, a in enumerate(open_t):
        ta, aa = norm(a["text"]), norm(a["anchor"])
        for b in open_t[i + 1:]:
            tb, ab = norm(b["text"]), norm(b["anchor"])
            same_anchor = aa and aa == ab and a["section_no"] == b["section_no"]
            similar = len(ta) > 15 and difflib.SequenceMatcher(None, ta, tb).ratio() >= threshold
            if same_anchor or similar:
                a["dups"].append(b["ref"]); b["dups"].append(a["ref"])


def export_sections(sections, outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, v in sections.items():
        if not v["paras"]:
            continue
        fn = os.path.join(outdir, "sec_%s.txt" % re.sub(r"[^\w.-]", "_", k))
        with open(fn, "w", encoding="utf-8") as f:
            f.write("SECTION %s %s\n\n%s\n" % (k, v["title"], "\n\n".join(v["paras"])))


# ------------------------------------------------------- Ph1 residue scan --
RESIDUE_TERMS = [
    r"healthy (?:volunteers?|subjects?|participants?)", r"\bvolunteers?\b", r"\bsubjects?\b",
    r"\bDDI\b", r"drug[- ]drug interaction", r"\bperpetrator\b", r"\bvictim drug\b",
    r"\bprobe (?:drug|substrate)\b", r"\bmidazolam\b", r"\bitraconazole\b", r"\brifampi(?:c)?in\b",
    r"\bperiod [12]\b", r"\bwash-?out\b", r"\bconfin(?:ed|ement)\b", r"\bcheck-in\b", r"\bdomicil",
    r"clinical (?:research|pharmacology) unit", r"\bCRU\b", r"\bPhase (?:1|I)\b(?!b)",
    r"\bfirst[- ]in[- ]human\b", r"\bsingle dose\b",
]
RESIDUE_RE = re.compile("|".join(RESIDUE_TERMS), re.I)


def residue_scan(sections, path):
    """Flag likely leftover Ph1 DDI / healthy-volunteer wording per section.
    Heuristic: review hits, don't auto-delete (some terms are legitimate in Ph2,
    or shared with the Ph1b draft)."""
    rows = []
    for k, v in sections.items():
        for para in v["paras"]:
            for m in RESIDUE_RE.finditer(para):
                a, b = max(0, m.start() - 60), min(len(para), m.end() + 60)
                rows.append((k, v["title"], m.group(0), "…" + para[a:b] + "…"))
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Section No.", "Section Title", "Term", "Context"])
        w.writerows(rows)
    return rows

# ---------------------------------------------------------------- output ----
def build_threads(comments):
    roots = [c for c in comments.values() if not c["parent"]]
    replies = {}
    for c in comments.values():
        if c["parent"]:
            replies.setdefault(c["parent"], []).append(c)
    for r in roots:
        kids = sorted(replies.get(r["id"], []), key=lambda k: (k["date"], int(k["id"])))
        r["replies"] = kids
    roots.sort(key=lambda c: (c["order"], int(c["id"])))
    return roots


def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


COLUMNS = [
    "Ref", "Comment ID", "Section No.", "Section Title", "Author", "Date",
    "Resolved in Word", "Anchored Text", "Paragraph Context", "Comment",
    "Replies", "Reply Count", "Possible Duplicates", "Dependent Sections",
    "Category", "Priority", "Owner", "Action / Response", "Status",
]


def rows_for(threads):
    for i, t in enumerate(threads, 1):
        reps = " | ".join("%s (%s): %s" % (r["author"], r["date"], r["text"]) for r in t["replies"])
        yield [
            t["ref"], t["id"], t["section_no"], t["section_title"], t["author"],
            t["date"], "Yes" if t["done"] else "No", clip(t["anchor"], 1000),
            clip(t["context"], 1500), t["text"], reps, len(t["replies"]),
            ", ".join(t["dups"]), " | ".join(t["deps"]),
            "", "", "", "", "Open" if not t["done"] else "Closed",
        ]


def write_tracker(threads, path):
    if path.lower().endswith(".xlsx"):
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Alignment, Font, PatternFill
            from openpyxl.worksheet.datavalidation import DataValidation
        except ImportError:
            print("openpyxl not installed - writing CSV instead.", file=sys.stderr)
            path = path[:-5] + ".csv"
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "Comments"
            ws.append(COLUMNS)
            for row in rows_for(threads):
                ws.append(row)
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="1F4E78")
            widths = [7, 9, 9, 28, 16, 11, 9, 40, 50, 60, 45, 7, 14, 30, 14, 10, 14, 50, 10]
            for idx, w in enumerate(widths):
                ws.column_dimensions[ws.cell(1, idx + 1).column_letter].width = w
            for r in ws.iter_rows(min_row=2):
                for cell in r:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
            ws.freeze_panes = "C2"
            ws.auto_filter.ref = ws.dimensions
            n = ws.max_row
            dv_specs = {
                "O": '"A-Editorial,B-Consistency,C-Content,D-Decision,E-Decline,F-Duplicate,G-Query"',
                "P": '"High,Medium,Low"',
                "S": '"Open,Drafted,Applied,For meeting,Closed"',
            }
            for col, formula in dv_specs.items():
                dv = DataValidation(type="list", formula1=formula, allow_blank=True)
                ws.add_data_validation(dv)
                dv.add("%s2:%s%d" % (col, col, max(n, 2)))
            wb.save(path)
            return path
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")  # semicolon: opens cleanly in German Excel
        w.writerow(COLUMNS)
        for row in rows_for(threads):
            w.writerow(row)
    return path


def write_batches(threads, outdir, level, max_per_batch):
    """Small, self-contained batches: only open, non-duplicate-secondary
    comments, trimmed context, and the dependency hints for each."""
    os.makedirs(outdir, exist_ok=True)
    groups = {}
    for t in threads:
        if t["done"]:
            continue
        parts = t["section_no"].split(".")
        key = ".".join(parts[:level]) if t["section_no"] != "UNLOCATED" else "UNLOCATED"
        groups.setdefault(key, []).append(t)
    written = []
    for key, items in groups.items():
        chunks = [items[i:i + max_per_batch] for i in range(0, len(items), max_per_batch)]
        for n, chunk in enumerate(chunks, 1):
            safe = re.sub(r"[^\w.-]", "_", key)
            suffix = "_part%d" % n if len(chunks) > 1 else ""
            fn = os.path.join(outdir, "section_%s%s__%02d.txt" % (safe, suffix, len(chunk)))
            with open(fn, "w", encoding="utf-8") as f:
                f.write("REVIEW COMMENTS - SECTION %s%s (%d comments: %s to %s)\n\n"
                        % (key, suffix.replace("_", " "), len(chunk), chunk[0]["ref"], chunk[-1]["ref"]))
                for t in chunk:
                    f.write("=== %s | Section %s %s | %s ===\n" % (t["ref"], t["section_no"], t["section_title"], t["author"]))
                    f.write("ANCHORED TEXT: %s\n" % (clip(t["anchor"], 600) or "(none - point comment)"))
                    f.write("PARAGRAPH: %s\n" % clip(t["context"], 600))
                    f.write("COMMENT: %s\n" % t["text"])
                    for r in t["replies"]:
                        f.write("REPLY (%s): %s\n" % (r["author"], r["text"]))
                    if t["dups"]:
                        f.write("POSSIBLE DUPLICATE OF: %s\n" % ", ".join(t["dups"]))
                    if t["deps"]:
                        f.write("MAY AFFECT SECTIONS: %s\n" % " | ".join(t["deps"]))
                    f.write("\n")
            written.append(fn)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--out", default=None, help="tracker path (.xlsx or .csv)")
    ap.add_argument("--batches", default="comment_batches", help="folder for per-section batch files ('' to skip)")
    ap.add_argument("--batch-level", type=int, default=1, help="group batches by heading level (1 = top-level sections)")
    ap.add_argument("--max-per-batch", type=int, default=12, help="max comments per batch file (keeps each Scribbler run small)")
    ap.add_argument("--sections", default="section_text", help="folder for per-section plain text ('' to skip)")
    a = ap.parse_args()

    with zipfile.ZipFile(a.docx) as z:
        comments = load_comments(z)
        if not comments:
            print("No comments found.")
            return
        sections = locate_comments(z, comments, load_style_outline_levels(z))

    threads = build_threads(comments)
    for i, t in enumerate(threads, 1):
        t["ref"] = "C%03d" % i
    build_dependencies(threads, sections)
    find_duplicates(threads)
    out = a.out or os.path.splitext(os.path.basename(a.docx))[0] + "_comment_tracker.xlsx"
    out = write_tracker(threads, out)

    n_open = sum(1 for t in threads if not t["done"])
    n_unloc = sum(1 for t in threads if t["section_no"] == "UNLOCATED")
    print("%d comments -> %d threads (%d open, %d resolved in Word)" % (len(comments), len(threads), n_open, len(threads) - n_open))
    if n_unloc:
        print("  %d threads not located in body (headers/footers/footnotes?)" % n_unloc)
    print("Tracker: %s" % out)

    if a.batches:
        files = write_batches(threads, a.batches, a.batch_level, a.max_per_batch)
        print("Batches: %d files in %s/" % (len(files), a.batches))
    if a.sections:
        export_sections(sections, a.sections)
        print("Section text: %s/" % a.sections)
    hits = residue_scan(sections, "ph1_residue_report.csv")
    print("Ph1 residue scan: %d hits in %d sections -> ph1_residue_report.csv"
          % (len(hits), len({h[0] for h in hits})))
    n_dup = sum(1 for t in threads if t["dups"] and not t["done"])
    n_dep = sum(1 for t in threads if t["deps"] and not t["done"])
    print("%d open threads have possible duplicates; %d may affect other sections" % (n_dup, n_dep))

    # per-section and per-author counts
    by_sec, by_auth = {}, {}
    for t in threads:
        if t["done"]:
            continue
        k = t["section_no"].split(".")[0] if t["section_no"] != "UNLOCATED" else "UNLOCATED"
        by_sec[k] = by_sec.get(k, 0) + 1
        by_auth[t["author"]] = by_auth.get(t["author"], 0) + 1
    print("\nOpen threads by top-level section:")
    for k, v in sorted(by_sec.items(), key=lambda kv: -kv[1]):
        print("  %-10s %d" % (k, v))
    print("\nOpen threads by reviewer:")
    for k, v in sorted(by_auth.items(), key=lambda kv: -kv[1]):
        print("  %-30s %d" % (k, v))


if __name__ == "__main__":
    main()
