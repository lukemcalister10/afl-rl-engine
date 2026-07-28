#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STDLIB-ONLY .xlsx READER — the live lane must not need a wheel (#232).

WHY THIS EXISTS.  `ingest_inputs.py` is the whole of the LIVE lane: the owner edits his sheet, runs one
command, and a trade is visible.  It read the pick workbook with `openpyxl`, so on any seat without that
wheel installed the live lane did not run slowly — it HALTED.  Measured 2026-07-28 on a bare container:
27 checks PASSed and the run then stopped at `openpyxl not available`.  A lane that halts wherever a
third-party wheel is absent is not an edit path.  This is the same shape as `bootstrap_env.sh` invoking
bare `python3` against a cp312-pinned lock, which CURRENT_STATE records as having cost two seats.

The fix is to remove the dependency, not to satisfy it.  An .xlsx is a zip of XML, and `zipfile` +
`xml.etree` are in the standard library, so the owner's authored format does not change at all.

WHAT IT REPRODUCES.  `openpyxl.load_workbook(path, data_only=True)` followed by
`ws.iter_rows(values_only=True)`, for the cell kinds the pick workbook actually contains: shared
strings, inline strings, formula string results, numbers and booleans.  Rows are padded to the sheet's
used width and absent rows inside the used range are yielded blank, so positional row/column indexing
matches openpyxl exactly.

WHERE IT DELIBERATELY DIFFERS — and this is the point.  `data_only=True` returns **None** for a formula
cell that carries no cached value, which is indistinguishable from an empty cell.  A pick band or a
multiplier silently read as empty is precisely the class of defect this project keeps paying for: a
value that reads clean for the portion it missed.  So this reader REFUSES.  A formula with no cached
`<v>`, and a cached error value (`#REF!`, `#N/A`, …), both raise `XlsxCellError` naming the sheet and
the cell reference.  `ingest_inputs.py` maps that to its own HALT.

NOT IMPLEMENTED, deliberately, because nothing in `docs/inputs/` needs it: date/time deserialisation
(a date-formatted cell returns its raw serial number, not a `datetime`), styles, merged-cell expansion.
If an input ever grows a date column, teach this reader about it rather than reaching for the wheel.
"""
import zipfile
import xml.etree.ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RELNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKGREL = "http://schemas.openxmlformats.org/package/2006/relationships"


class XlsxCellError(Exception):
    """A cell whose value cannot be established without guessing.  Raised, never returned as None —
    an unreadable cell must stop the ingest, not flow into it as an empty one."""


class XlsxStructureError(Exception):
    """The workbook is not shaped like a workbook (missing part, unnamed sheet, bad rel)."""


def _q(tag):
    return "{%s}%s" % (MAIN, tag)


def _col_index(ref):
    """'AB12' -> 27 (0-based column).  Letters only; the row digits are ignored."""
    n = 0
    for ch in ref:
        if ch.isdigit():
            break
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def _row_index(ref):
    """'AB12' -> 12 (1-based row), or None when the ref carries no digits."""
    d = "".join(ch for ch in ref if ch.isdigit())
    return int(d) if d else None


def _shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall(_q("si")):
        # a shared string is either one <t> or a run of <r><t>…</t></r> fragments; join the runs.
        out.append("".join(t.text or "" for t in si.iter(_q("t"))))
    return out


def _sheet_map(z):
    """name -> zip part path, resolved through the workbook rels (sheet order in workbook.xml does NOT
    have to match the sheetN.xml filenames, so the rel is the only correct route)."""
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {}
    for r in rels.findall("{%s}Relationship" % PKGREL):
        t = r.get("Target") or ""
        if t.startswith("/"):
            t = t[1:]
        elif not t.startswith("xl/"):
            t = "xl/" + t
        target[r.get("Id")] = t
    out = {}
    for s in wb.iter(_q("sheet")):
        name, rid = s.get("name"), s.get("{%s}id" % RELNS)
        if not name:
            raise XlsxStructureError("workbook carries a sheet with no name")
        if rid not in target:
            raise XlsxStructureError("sheet %r points at unknown relationship %r" % (name, rid))
        out[name] = target[rid]
    return out


def _number(txt):
    """Excel stores every number as text.  Return an int when it is integral so the ingest's int() casts
    and equality checks behave exactly as they did under openpyxl."""
    f = float(txt)
    return int(f) if f.is_integer() else f


def _cell_value(c, shared, sheet):
    ref = c.get("r") or "?"
    t = c.get("t")
    v = c.find(_q("v"))
    f = c.find(_q("f"))

    if t == "inlineStr":
        is_ = c.find(_q("is"))
        return "".join(x.text or "" for x in is_.iter(_q("t"))) if is_ is not None else None

    if v is None or v.text is None:
        # A formula that was never calculated, or whose cache the writer stripped.  openpyxl's
        # data_only would hand back None here and the ingest would read it as an empty cell.
        if f is not None:
            raise XlsxCellError(
                "%s!%s holds a formula with no cached value — the workbook was written without "
                "calculating.  Refusing to read it as empty; open the file, let it calculate, and save."
                % (sheet, ref))
        return None

    txt = v.text

    if t == "e":
        raise XlsxCellError(
            "%s!%s holds the cached error value %r — refusing to ingest an error as data."
            % (sheet, ref, txt))
    if t == "s":
        i = int(txt)
        if i >= len(shared):
            raise XlsxStructureError("%s!%s references shared string %d of %d" % (sheet, ref, i, len(shared)))
        return shared[i]
    if t == "str":
        return txt
    if t == "b":
        return txt not in ("0", "", None)
    # default / t="n"
    try:
        return _number(txt)
    except ValueError:
        return txt


def sheet_names(path):
    with zipfile.ZipFile(path) as z:
        return list(_sheet_map(z).keys())


def rows(path, sheet):
    """Yield each row of `sheet` as a tuple of values, padded to the sheet's used width — the
    `iter_rows(values_only=True)` contract, so callers index positionally as before."""
    with zipfile.ZipFile(path) as z:
        smap = _sheet_map(z)
        if sheet not in smap:
            raise XlsxStructureError("no sheet named %r (have: %s)" % (sheet, sorted(smap)))
        shared = _shared_strings(z)
        root = ET.fromstring(z.read(smap[sheet]))

        parsed, max_col, max_row = {}, 0, 0
        for r in root.iter(_q("row")):
            cells = {}
            rn = r.get("r")
            rn = int(rn) if rn else (max_row + 1)
            for c in r.iter(_q("c")):
                ref = c.get("r") or ""
                ci = _col_index(ref) if ref else len(cells)
                if ci < 0:
                    continue
                cells[ci] = _cell_value(c, shared, sheet)
                if ci + 1 > max_col:
                    max_col = ci + 1
            parsed[rn] = cells
            if rn > max_row:
                max_row = rn

        out = []
        for rn in range(1, max_row + 1):
            cells = parsed.get(rn, {})
            out.append(tuple(cells.get(i) for i in range(max_col)))
        return out
