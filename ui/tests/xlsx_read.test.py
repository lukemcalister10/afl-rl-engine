#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROVES ui/tools/xlsx_read.py — the stdlib .xlsx reader that removed openpyxl from the live lane (#232).

Two things have to hold, and the second is the one that matters:

  PARITY   — reading the real pick workbook reproduces, cell for cell, the ledger that openpyxl
             produced.  The oracle is ui/data/club_valuation.js, generated 2026-07-27 by the openpyxl
             path; the workbook has not changed since 2026-07-16 (d4e9642), so the two are comparable.

  REFUSAL  — the reader HALTS on a formula cell with no cached value, and on a cached error value,
             rather than handing back None.  openpyxl's data_only=True returns None for both, which is
             indistinguishable from an empty cell — a pick band silently read as empty is the
             false-success-signal class this project keeps paying for.

NON-VACUITY.  Every refusal case is asserted BOTH ways: the malformed workbook raises, and a byte-identical
control workbook differing only in the offending cell reads clean.  A refusal test that never sees the
passing case cannot tell "correctly refused" from "refuses everything".
"""
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "ui", "tools"))
import xlsx_read as X  # noqa: E402

FAILURES = []


def check(name, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  (%s)" % detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# --------------------------------------------------------------------------- synthetic workbook maker
CT = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
</Types>"""

ROOTREL = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

WB = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Picks" sheetId="1" r:id="rId1"/></sheets></workbook>"""

WBREL = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>"""


def make_xlsx(sheet_xml):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", ROOTREL)
        z.writestr("xl/workbook.xml", WB)
        z.writestr("xl/_rels/workbook.xml.rels", WBREL)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
    buf.seek(0)
    path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "xlsx_read_fixture.xlsx")
    with open(path, "wb") as fh:
        fh.write(buf.read())
    return path


def sheet(cell_xml):
    return ("""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
<row r="1">%s</row></sheetData></worksheet>""" % cell_xml)


# ------------------------------------------------------------------------------------------ PARITY
def parity():
    print("\nPARITY — stdlib reader vs the openpyxl-generated bundle")
    wbpath = os.path.join(ROOT, "docs", "inputs", "AFFL_Pick_Locations.xlsx")
    cvpath = os.path.join(ROOT, "ui", "data", "club_valuation.js")

    names = X.sheet_names(wbpath)
    check("workbook exposes the sheets the ingest names", "Picks" in names and "Ladder" in names, str(names))

    rows = X.rows(wbpath, "Picks")
    ledger = [r for i, r in enumerate(rows) if i >= 2 and r[0] is not None]
    _exp = 16 * 5 * len({r[1] for r in ledger})   # 16 clubs x 5 rounds x the issued years (S1 form)
    check("ledger row count == %d (16x5xissued years)" % _exp, len(ledger) == _exp, "%d rows" % len(ledger))

    lad = X.rows(wbpath, "Ladder")
    mult = None
    for r in lad:
        if r and r[0] and str(r[0]).startswith("2027 value multiplier"):
            mult = r[1]
    check("Ladder 2027 multiplier reads 0.9", mult == 0.9, "cell = %r" % (mult,))

    s = open(cvpath).read()
    i = s.index("{", s.index("__CLUB_VALUATION__"))
    cv = json.loads(s[i:s.rindex("}") + 1])
    baked = {}
    for team, picks in (cv.get("picksByTeam") or {}).items():
        for p in picks:
            baked[p["id"]] = p

    check("oracle bundle carries every ledger pick", len(baked) == len(ledger), "%d picks vs %d ledger rows" % (len(baked), len(ledger)))

    mism = []
    for r in ledger:
        pid, yr, rnd, orig, owner, lo, hi = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
        b = baked.get(pid)
        if b is None:
            mism.append((pid, "absent from the oracle"))
            continue
        if int(yr) != int(b["year"]) or int(rnd) != int(b["round"]) \
           or int(lo) != int(b["low"]) or int(hi) != int(b["high"]):
            mism.append((pid, "year/round/low/high differ", (yr, rnd, lo, hi),
                         (b["year"], b["round"], b["low"], b["high"])))
    check("every ledger row matches the openpyxl-generated pick, field for field",
          not mism, "%d mismatch(es)%s" % (len(mism), (": " + str(mism[:3])) if mism else ""))

    # the reader must preserve openpyxl's int-vs-str typing, or the ingest's int() casts change meaning
    r2 = ledger[0]
    check("numeric cells read as int, text cells as str (openpyxl typing preserved)",
          all(isinstance(r2[c], int) for c in (0, 1, 2, 5, 6))
          and all(isinstance(r2[c], str) for c in (3, 4)),
          str([type(x).__name__ for x in r2[:7]]))


# ----------------------------------------------------------------------------------------- REFUSALS
def refusals():
    print("\nREFUSAL — uncached formula (asserted both directions)")
    # CONTROL: identical cell, but WITH the cached <v>.  Must read clean.
    ok_path = make_xlsx(sheet('<c r="A1"><f>SUM(B1:C1)</f><v>42</v></c>'))
    try:
        got = X.rows(ok_path, "Picks")[0][0]
        check("control — formula WITH a cached value reads that value", got == 42, "got %r" % (got,))
    except X.XlsxCellError as e:
        check("control — formula WITH a cached value reads that value", False, "raised: %s" % e)

    # THE DEFECT: same formula, cache stripped.  openpyxl data_only would return None here.
    bad_path = make_xlsx(sheet('<c r="A1"><f>SUM(B1:C1)</f></c>'))
    raised = None
    try:
        got = X.rows(bad_path, "Picks")
        check("formula with NO cached value is refused, not read as empty", False,
              "returned %r instead of raising" % (got[0][0],))
    except X.XlsxCellError as e:
        raised = str(e)
        check("formula with NO cached value is refused, not read as empty", True)
    check("the refusal names the sheet and the cell reference",
          bool(raised) and "Picks!A1" in raised, raised or "no exception")

    print("\nREFUSAL — cached error value (asserted both directions)")
    ok2 = make_xlsx(sheet('<c r="A1" t="str"><f>X()</f><v>fine</v></c>'))
    try:
        got = X.rows(ok2, "Picks")[0][0]
        check("control — formula returning a string reads that string", got == "fine", "got %r" % (got,))
    except X.XlsxCellError as e:
        check("control — formula returning a string reads that string", False, "raised: %s" % e)

    bad2 = make_xlsx(sheet('<c r="A1" t="e"><f>1/0</f><v>#DIV/0!</v></c>'))
    raised2 = None
    try:
        got = X.rows(bad2, "Picks")
        check("cached error value is refused, not ingested as data", False,
              "returned %r instead of raising" % (got[0][0],))
    except X.XlsxCellError as e:
        raised2 = str(e)
        check("cached error value is refused, not ingested as data", True)
    check("the error refusal quotes the error text", bool(raised2) and "#DIV/0!" in raised2,
          raised2 or "no exception")

    print("\nSANITY — a genuinely empty cell is still empty, not a refusal")
    empty = make_xlsx(sheet('<c r="A1"/><c r="B1"><v>7</v></c>'))
    try:
        row = X.rows(empty, "Picks")[0]
        check("empty cell reads None while its neighbour reads 7", row[0] is None and row[1] == 7, str(row))
    except X.XlsxCellError as e:
        check("empty cell reads None while its neighbour reads 7", False, "raised: %s" % e)


if __name__ == "__main__":
    print("xlsx_read.test.py — stdlib .xlsx reader (#232)")
    parity()
    refusals()
    print("\n%s — %d failure(s)" % ("FAIL" if FAILURES else "PASS", len(FAILURES)))
    sys.exit(1 if FAILURES else 0)
