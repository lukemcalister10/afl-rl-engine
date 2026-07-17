#!/usr/bin/env python3
"""viewing_pack.py --base <board.json> --cand <board.json> [--names <file>] --out <dir>

SEAT TOOLS · the OWNER VIEWING PACK. Turns two board files into ONE self-contained, owner-readable
HTML page (plus a plain-text .md twin) that the owner reads INSTEAD of the raw JSON. Every headline
number is computed here, at generation time, from the two boards — the tool NEVER accepts a count as
an argument — and each page is stamped with both input md5s so the reader can prove which two boards
it summarises.

What it lays out, in order (league-manager language up top, jargon confined to the footnotes):
  1. The bottom line — net change in total value, how many players rose vs fell, and the three
     biggest risers and fallers, each with per-stage (lever) attribution when the boards carry it.
  2. The named players — a table of value before -> after and rank before -> after (positional
     ranks, ties broken by key: the item-295 convention, restated in the footer), with position bars.
  3. Where value didn't pay off — the players whose value went UP but whose rank went DOWN.
  4. The full movement ledger — every active player who moved, in a collapsible appendix.

SCHEMA — this tool ingests the data/rl_build/rl_app_data.json board schema ONLY: a top-level object
whose `active` array holds rows carrying `key`, `name`, `v` (value), `grp`, `age`, `pk`, and (optional)
`levers`. Positional ranks are derived here from `v`. It does NOT ingest the led_default.json
measurement artifact ({key:{num,…}}) — that is not a board and is refused.

RED-PATH (loud, non-zero exit, writes nothing): a board that does not match the schema above, or two
inputs whose bytes are md5-identical (nothing to view).

House laws: reads two files into memory and writes only into --out. Reuses board_diff's by_key/fnum
(one source, per the SSI spirit). python3 stdlib only.
"""
import hashlib
import html
import json
import os
import sys

# --- one source: reuse board_diff's keying + numeric coercion rather than re-writing them ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board_diff import by_key, fnum  # noqa: E402

TOOL = "viewing_pack"
BOARD_HINT = "data/rl_build/rl_app_data.json schema (top-level object with an `active` array)"


def die(msg):
    sys.stderr.write("%s: FAIL — %s\n" % (TOOL, msg))
    raise SystemExit(1)


def read_bytes(path):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as e:
        die("cannot read %s: %s" % (path, e))


def load_board(path, raw):
    """Parse + schema-guard a single board file. RED-PATH refuse on anything not this schema."""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        die("%s is not valid JSON: %s" % (path, e))
    if not isinstance(obj, dict):
        die("%s is not a board — expected the %s, got a %s at top level"
            % (path, BOARD_HINT, type(obj).__name__))
    active = obj.get("active")
    if not isinstance(active, list) or not active:
        die("%s is not a board — the %s has no non-empty `active` array "
            "(is this the led_default.json measurement artifact? that is not a board)"
            % (path, BOARD_HINT))
    for i, row in enumerate(active):
        if not isinstance(row, dict) or "key" not in row or "v" not in row:
            die("%s: active[%d] is not a board row (needs at least `key` and `v`)" % (path, i))
    return obj


def positional_ranks(board):
    """Item-295 convention: rank 1 = highest value; ties broken by key (ascending). Returns key->rank."""
    rows = sorted(board.get("active", []),
                  key=lambda r: (-(fnum(r.get("v")) or 0.0), str(r.get("key"))))
    return {r.get("key"): i + 1 for i, r in enumerate(rows)}


def lever_keys(*boards):
    """The per-stage attribution columns, if BOTH boards carry `levers`. Union of lever names, sorted."""
    seen = set()
    carry = True
    for b in boards:
        any_lever = False
        for r in b.get("active", []):
            lv = r.get("levers")
            if isinstance(lv, dict) and lv:
                any_lever = True
                seen.update(lv.keys())
        carry = carry and any_lever
    if not carry:
        return []
    return sorted(seen, key=lambda s: (len(s), s))


def dlever(base_row, cand_row, lk):
    b = (base_row.get("levers") or {}) if base_row else {}
    c = (cand_row.get("levers") or {}) if cand_row else {}
    out = {}
    for name in lk:
        bv, cv = fnum(b.get(name)) or 0.0, fnum(c.get(name)) or 0.0
        out[name] = cv - bv
    return out


def gnum(x):
    """Terse number for display: ints without a trailing .0, floats to <=2 dp."""
    if x is None:
        return "—"
    f = float(x)
    return "%d" % round(f) if abs(f - round(f)) < 1e-9 else "%.2f" % f


def signed(x):
    if x is None:
        return "—"
    f = float(x)
    return "%+d" % round(f) if abs(f - round(f)) < 1e-9 else "%+.2f" % f


def compute(base, cand):
    """All the facts of record, computed here from the two boards. No count is ever an input."""
    A, B = by_key(base), by_key(cand)
    rank_a, rank_b = positional_ranks(base), positional_ranks(cand)
    lk = lever_keys(base, cand)

    common = set(A) & set(B)
    added, removed = sorted(set(B) - set(A)), sorted(set(A) - set(B))

    rows = []
    for k in common:
        va, vb = fnum(A[k].get("v")), fnum(B[k].get("v"))
        if va is None or vb is None:
            continue
        dv = vb - va
        ra, rb = rank_a.get(k), rank_b.get(k)
        rows.append({
            "key": k,
            "name": B[k].get("name") or A[k].get("name") or k,
            "grp": B[k].get("grp"),
            "age": B[k].get("age"),
            "pk": B[k].get("pk"),
            "va": va, "vb": vb, "dv": dv,
            "ra": ra, "rb": rb,
            "drank": (rb - ra) if (ra is not None and rb is not None) else None,
            "dlev": dlever(A[k], B[k], lk),
        })

    movers = [r for r in rows if r["dv"] != 0]
    ups = [r for r in movers if r["dv"] > 0]
    downs = [r for r in movers if r["dv"] < 0]
    net = sum(r["dv"] for r in rows)
    gross = sum(abs(r["dv"]) for r in movers)

    # failure ledger: value UP, positional rank DOWN (rank NUMBER larger = worse position).
    failures = [r for r in rows
                if r["dv"] > 0 and r["drank"] is not None and r["drank"] > 0]
    failures.sort(key=lambda r: (r["drank"], -r["dv"]))

    rises = sorted(movers, key=lambda r: (-r["dv"], str(r["key"])))[:3]
    falls = sorted(movers, key=lambda r: (r["dv"], str(r["key"])))[:3]

    v_all = [fnum(r.get("v")) or 0.0 for r in cand.get("active", [])]
    return {
        "rows": rows, "movers": movers, "ups": ups, "downs": downs,
        "net": net, "gross": gross, "common": common,
        "added": added, "removed": removed,
        "failures": failures, "rises": rises, "falls": falls,
        "lever_keys": lk, "n_active_cand": len(cand.get("active", [])),
        "n_active_base": len(base.get("active", [])),
        "vmax": max(v_all) if v_all else 0.0, "vmin": min(v_all) if v_all else 0.0,
        "rank_max": len(cand.get("active", [])),
    }


def resolve_names(names_arg, rows):
    """Map a --names file (one name-or-key per line, # comments allowed) to computed rows.

    Default when no file: the biggest movers by absolute value change (top 24)."""
    if not names_arg:
        return sorted([r for r in rows if r["dv"] != 0],
                      key=lambda r: (-abs(r["dv"]), str(r["key"])))[:24], True
    try:
        with open(names_arg, "r") as fh:
            wants = [ln.strip() for ln in fh
                     if ln.strip() and not ln.strip().startswith("#")]
    except OSError as e:
        die("cannot read --names file %s: %s" % (names_arg, e))
    by_k = {r["key"]: r for r in rows}
    picked, order = [], []
    seen = set()
    for want in wants:
        hit = None
        if want in by_k:
            hit = by_k[want]
        else:
            cands = [r for r in rows if want.lower() in (r["name"] or "").lower()]
            hit = min(cands, key=lambda r: str(r["key"])) if cands else None
        if hit is None:
            picked.append({"missing": want})
            continue
        if hit["key"] in seen:
            continue
        seen.add(hit["key"])
        picked.append(hit)
    return picked, False


# ----------------------------------------------------------------------------- rendering: MARKDOWN

def bar_ascii(frac, width=12):
    frac = max(0.0, min(1.0, frac))
    n = int(round(frac * width))
    return "#" * n + "·" * (width - n)


def render_md(c, named, named_default, meta):
    L = c["lever_keys"]
    out = []
    w = out.append
    w("# Board Viewing Pack — %s → %s" % (meta["base_name"], meta["cand_name"]))
    w("")
    w("_Base md5 `%s` · Candidate md5 `%s` · generated by %s_" %
      (meta["base_md5"], meta["cand_md5"], TOOL))
    w("")
    # 1. bottom line
    w("## The bottom line")
    w("")
    w("- **Net change in total value:** **%s** across %d players on both boards."
      % (signed(c["net"]), len(c["common"])))
    w("- **Who moved:** %d players moved — **%d up**, **%d down** (%d unchanged)."
      % (len(c["movers"]), len(c["ups"]), len(c["downs"]),
         len(c["common"]) - len(c["movers"])))
    if c["added"] or c["removed"]:
        w("- **Roster change:** %d added, %d dropped." % (len(c["added"]), len(c["removed"])))
    w("")
    lh = (" | " + " | ".join(html_l(x) for x in L)) if L else ""
    lsep = ("|" + "|".join(["---:"] * len(L))) if L else ""
    w("### Three biggest risers")
    w("")
    w("| Player | Group | Value | Change" + lh + " |")
    w("|---|---|---:|---:" + lsep + "|")
    for r in c["rises"]:
        w(mdrow(r, L))
    w("")
    w("### Three biggest fallers")
    w("")
    w("| Player | Group | Value | Change" + lh + " |")
    w("|---|---|---:|---:" + lsep + "|")
    for r in c["falls"]:
        w(mdrow(r, L))
    w("")
    # 2. named
    title = "the biggest movers (default)" if named_default else "your named players"
    w("## The named players — %s" % title)
    w("")
    w("| Player | Group | Age | Value before → after | Rank before → after | Position |")
    w("|---|---|---:|---:|---:|:--|")
    for r in named:
        if "missing" in r:
            w("| %s | — | — | _not on both boards_ | — | — |" % html_l(r["missing"]))
            continue
        w("| %s | %s | %s | %s → %s (%s) | %s → %s (%s) | `%s` |" % (
            html_l(r["name"]), html_l(r["grp"]), gnum(r["age"]),
            gnum(r["va"]), gnum(r["vb"]), signed(r["dv"]),
            rk(r["ra"]), rk(r["rb"]), rank_delta(r["drank"]),
            bar_ascii(rank_frac(r["rb"], c["rank_max"]))))
    w("")
    # 3. failure ledger
    w("## Where value didn't pay off")
    w("")
    w("_Players whose value went **up** but whose rank went **down** — %d of them._"
      % len(c["failures"]))
    w("")
    if c["failures"]:
        w("| Player | Group | Value before → after | Rank before → after |")
        w("|---|---|---:|---:|")
        for r in c["failures"]:
            w("| %s | %s | %s → %s (%s) | %s → %s (%s) |" % (
                html_l(r["name"]), html_l(r["grp"]),
                gnum(r["va"]), gnum(r["vb"]), signed(r["dv"]),
                rk(r["ra"]), rk(r["rb"]), rank_delta(r["drank"])))
    else:
        w("_None — every player who gained value held or improved their rank._")
    w("")
    # 4. full movement ledger
    w("## The full movement ledger")
    w("")
    w("_All %d players who moved, biggest change first._" % len(c["movers"]))
    w("")
    w("| Player | Group | Value before → after | Change | Rank before → after |")
    w("|---|---|---:|---:|---:|")
    for r in sorted(c["movers"], key=lambda r: (-abs(r["dv"]), str(r["key"]))):
        w("| %s | %s | %s → %s | %s | %s → %s (%s) |" % (
            html_l(r["name"]), html_l(r["grp"]),
            gnum(r["va"]), gnum(r["vb"]), signed(r["dv"]),
            rk(r["ra"]), rk(r["rb"]), rank_delta(r["drank"])))
    w("")
    w("---")
    w("")
    w("### Footnotes (the fine print)")
    w("")
    w("- **Value** is the board's num-SCAR figure (`active[].v`).")
    w("- **Rank** is a *positional* rank: players sorted by value, highest first; equal values are "
      "broken by player key in ascending order (the item-295 convention). Rank 1 is the top player.")
    w("- **Net change / ΣΔ** is the signed sum of value change over the %d players present on both "
      "boards." % len(c["common"]))
    if L:
        w("- **Per-stage columns (%s)** are the change in each lever's contribution "
          "(`levers[Lx]` candidate − base)." % ", ".join(L))
    w("- This pack summarises **base md5 `%s` → candidate md5 `%s`**; every count above was computed "
      "from those two boards at generation time." % (meta["base_md5"], meta["cand_md5"]))
    return "\n".join(out) + "\n"


def html_l(x):
    return html.escape("" if x is None else str(x))


def mdrow(r, L):
    cells = "| %s | %s | %s | %s" % (
        html_l(r["name"]), html_l(r["grp"]), gnum(r["vb"]), signed(r["dv"]))
    for name in L:
        cells += " | %s" % signed(r["dlev"].get(name, 0.0))
    return cells + " |"


def rk(x):
    return "#%d" % x if x is not None else "—"


def rank_delta(d):
    if d is None:
        return "—"
    if d == 0:
        return "±0"
    # rank number down (larger) = a WORSE position; show a down-arrow for clarity
    return ("%+d ▼" % d) if d > 0 else ("%+d ▲" % d)


def rank_frac(rank, rank_max):
    if rank is None or rank_max <= 1:
        return 0.0
    return 1.0 - (rank - 1) / (rank_max - 1)  # rank 1 -> full bar


# --------------------------------------------------------------------------------- rendering: HTML

CSS = """
:root{color-scheme:light dark;--bg:#fff;--fg:#1a1c20;--mut:#5b6470;--line:#e2e6eb;
--card:#f6f8fa;--up:#137a3f;--down:#b3261e;--bar:#d7dee7;--barfill:#3b6ea5;--accent:#274b78}
@media(prefers-color-scheme:dark){:root{--bg:#14171c;--fg:#e7ebf0;--mut:#9aa4b1;--line:#2a2f37;
--card:#1c2128;--up:#4ac57e;--down:#f2857c;--bar:#2a313b;--barfill:#5b8fd0;--accent:#8fb4e6}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:32px 20px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:36px 0 12px;
border-bottom:2px solid var(--line);padding-bottom:6px}h3{font-size:16px;margin:20px 0 8px}
.stamp{color:var(--mut);font-size:13px;margin-bottom:8px}
.cards{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0}
.card{flex:1 1 180px;background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:14px 16px}.card .k{color:var(--mut);font-size:13px}.card .val{font-size:26px;font-weight:700;margin-top:2px}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px;margin:6px 0}
th,td{padding:7px 10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
th{color:var(--mut);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.03em}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.up{color:var(--up);font-weight:600}.down{color:var(--down);font-weight:600}
.bar{display:inline-block;width:120px;height:12px;background:var(--bar);border-radius:6px;
overflow:hidden;vertical-align:middle}.bar>span{display:block;height:100%;background:var(--barfill)}
.rk{color:var(--mut);font-variant-numeric:tabular-nums}
details{margin:8px 0}summary{cursor:pointer;font-weight:600;color:var(--accent)}
.foot{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--mut);font-size:13px}
.foot li{margin:4px 0}code{background:var(--card);padding:1px 5px;border-radius:4px;font-size:.9em}
.miss{color:var(--mut);font-style:italic}
"""


def bar_html(frac):
    frac = max(0.0, min(1.0, frac))
    return '<span class="bar"><span style="width:%.1f%%"></span></span>' % (frac * 100)


def cls(dv):
    return "up" if dv > 0 else ("down" if dv < 0 else "")


def dv_html(dv):
    return '<span class="%s">%s</span>' % (cls(dv), signed(dv)) if dv else signed(dv)


def render_html(c, named, named_default, meta):
    L = c["lever_keys"]
    o = []
    w = o.append
    w("<div class='wrap'>")
    w("<h1>Board Viewing Pack</h1>")
    w("<div class='stamp'>%s &rarr; %s</div>" % (html_l(meta["base_name"]), html_l(meta["cand_name"])))
    w("<div class='stamp'>Base md5 <code>%s</code> &middot; Candidate md5 <code>%s</code></div>"
      % (meta["base_md5"], meta["cand_md5"]))

    # 1. bottom line
    w("<h2>The bottom line</h2>")
    w("<div class='cards'>")
    w(card("Net change in value", '<span class="%s">%s</span>' % (cls(c["net"]), signed(c["net"]))))
    w(card("Players who rose", str(len(c["ups"])), "up"))
    w(card("Players who fell", str(len(c["downs"])), "down"))
    w(card("Players who moved", "%d of %d" % (len(c["movers"]), len(c["common"]))))
    w("</div>")

    for title, group in (("Three biggest risers", c["rises"]), ("Three biggest fallers", c["falls"])):
        w("<h3>%s</h3>" % title)
        w("<div class='tw'><table><thead><tr><th>Player</th><th>Group</th>"
          "<th class='num'>Value</th><th class='num'>Change</th>")
        for name in L:
            w("<th class='num'>%s</th>" % html_l(name))
        w("</tr></thead><tbody>")
        for r in group:
            w("<tr><td>%s</td><td>%s</td><td class='num'>%s</td><td class='num'>%s</td>"
              % (html_l(r["name"]), html_l(r["grp"]), gnum(r["vb"]), dv_html(r["dv"])))
            for name in L:
                w("<td class='num'>%s</td>" % signed(r["dlev"].get(name, 0.0)))
            w("</tr>")
        w("</tbody></table></div>")

    # 2. named
    title = "the biggest movers" if named_default else "your named players"
    w("<h2>The named players &mdash; %s</h2>" % title)
    w("<div class='tw'><table><thead><tr><th>Player</th><th>Group</th><th class='num'>Age</th>"
      "<th class='num'>Value before &rarr; after</th><th class='num'>Rank before &rarr; after</th>"
      "<th>Position</th></tr></thead><tbody>")
    for r in named:
        if "missing" in r:
            w("<tr><td>%s</td><td colspan='5' class='miss'>not on both boards</td></tr>"
              % html_l(r["missing"]))
            continue
        w("<tr><td>%s</td><td>%s</td><td class='num'>%s</td>"
          "<td class='num'>%s &rarr; %s (%s)</td>"
          "<td class='num'><span class='rk'>%s &rarr; %s</span> %s</td><td>%s</td></tr>" % (
              html_l(r["name"]), html_l(r["grp"]), gnum(r["age"]),
              gnum(r["va"]), gnum(r["vb"]), dv_html(r["dv"]),
              rk(r["ra"]), rk(r["rb"]), rank_delta_html(r["drank"]),
              bar_html(rank_frac(r["rb"], c["rank_max"]))))
    w("</tbody></table></div>")

    # 3. failure ledger
    w("<h2>Where value didn't pay off</h2>")
    w("<p class='stamp'>Players whose value went <b>up</b> but whose rank went <b>down</b> "
      "&mdash; %d of them.</p>" % len(c["failures"]))
    if c["failures"]:
        w("<div class='tw'><table><thead><tr><th>Player</th><th>Group</th>"
          "<th class='num'>Value before &rarr; after</th>"
          "<th class='num'>Rank before &rarr; after</th></tr></thead><tbody>")
        for r in c["failures"]:
            w("<tr><td>%s</td><td>%s</td><td class='num'>%s &rarr; %s (%s)</td>"
              "<td class='num'><span class='rk'>%s &rarr; %s</span> %s</td></tr>" % (
                  html_l(r["name"]), html_l(r["grp"]),
                  gnum(r["va"]), gnum(r["vb"]), dv_html(r["dv"]),
                  rk(r["ra"]), rk(r["rb"]), rank_delta_html(r["drank"])))
        w("</tbody></table></div>")
    else:
        w("<p class='miss'>None &mdash; every player who gained value held or improved their rank.</p>")

    # 4. full movement ledger (collapsible)
    w("<h2>The full movement ledger</h2>")
    w("<details><summary>Show all %d players who moved</summary>" % len(c["movers"]))
    w("<div class='tw'><table><thead><tr><th>Player</th><th>Group</th>"
      "<th class='num'>Value before &rarr; after</th><th class='num'>Change</th>"
      "<th class='num'>Rank before &rarr; after</th></tr></thead><tbody>")
    for r in sorted(c["movers"], key=lambda r: (-abs(r["dv"]), str(r["key"]))):
        w("<tr><td>%s</td><td>%s</td><td class='num'>%s &rarr; %s</td><td class='num'>%s</td>"
          "<td class='num'><span class='rk'>%s &rarr; %s</span> %s</td></tr>" % (
              html_l(r["name"]), html_l(r["grp"]),
              gnum(r["va"]), gnum(r["vb"]), dv_html(r["dv"]),
              rk(r["ra"]), rk(r["rb"]), rank_delta_html(r["drank"])))
    w("</tbody></table></div></details>")

    # footnotes
    w("<div class='foot'><h3>Footnotes (the fine print)</h3><ul>")
    w("<li><b>Value</b> is the board's num-SCAR figure (<code>active[].v</code>).</li>")
    w("<li><b>Rank</b> is a <i>positional</i> rank: players sorted by value, highest first; equal "
      "values are broken by player key in ascending order (the item-295 convention). Rank 1 is the "
      "top player. A rank change marked &#9660; means the player slid down the order.</li>")
    w("<li><b>Net change / &Sigma;&Delta;</b> is the signed sum of value change over the %d players "
      "present on both boards.</li>" % len(c["common"]))
    if L:
        w("<li><b>Per-stage columns (%s)</b> are the change in each lever's contribution "
          "(<code>levers[Lx]</code> candidate &minus; base).</li>" % ", ".join(html_l(x) for x in L))
    w("<li>This pack summarises <b>base md5 <code>%s</code> &rarr; candidate md5 <code>%s</code></b>; "
      "every count above was computed from those two boards at generation time.</li>"
      % (meta["base_md5"], meta["cand_md5"]))
    w("</ul></div></div>")
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Board Viewing Pack — %s → %s</title><style>%s</style></head><body>%s</body></html>"
            % (html_l(meta["base_name"]), html_l(meta["cand_name"]), CSS, "".join(o)))


def rank_delta_html(d):
    if d is None:
        return '<span class="rk">—</span>'
    if d == 0:
        return '<span class="rk">&plusmn;0</span>'
    if d > 0:
        return '<span class="down">%+d &#9660;</span>' % d
    return '<span class="up">%+d &#9650;</span>' % d


def card(k, val, klass=""):
    return ("<div class='card'><div class='k'>%s</div>"
            "<div class='val %s'>%s</div></div>" % (html_l(k), klass, val))


# ------------------------------------------------------------------------------------------- driver

def parse_args(argv):
    a = {"base": None, "cand": None, "names": None, "out": None}
    rest = argv[1:]
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok in ("--base", "--cand", "--names", "--out"):
            if i + 1 >= len(rest):
                die("%s needs a value" % tok)
            a[tok[2:]] = rest[i + 1]
            i += 2
        elif tok in ("-h", "--help"):
            sys.stdout.write(__doc__)
            raise SystemExit(0)
        else:
            die("unknown argument: %s" % tok)
    for req in ("base", "cand", "out"):
        if not a[req]:
            die("--%s is required "
                "(usage: viewing_pack.py --base B.json --cand C.json [--names f] --out dir)" % req)
    return a


def main(argv):
    a = parse_args(argv)
    base_raw, cand_raw = read_bytes(a["base"]), read_bytes(a["cand"])
    base_md5 = hashlib.md5(base_raw).hexdigest()
    cand_md5 = hashlib.md5(cand_raw).hexdigest()
    # RED-PATH: nothing to view if the two inputs are byte-identical.
    if base_md5 == cand_md5:
        die("--base and --cand are md5-identical (%s) — there is nothing to view" % base_md5[:8])

    base = load_board(a["base"], base_raw)
    cand = load_board(a["cand"], cand_raw)

    c = compute(base, cand)
    named, named_default = resolve_names(a["names"], c["rows"])
    meta = {
        "base_name": os.path.basename(a["base"]),
        "cand_name": os.path.basename(a["cand"]),
        "base_md5": base_md5[:8], "cand_md5": cand_md5[:8],
    }

    out_dir = a["out"]
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        die("cannot create --out %s: %s" % (out_dir, e))
    html_path = os.path.join(out_dir, "viewing_pack.html")
    md_path = os.path.join(out_dir, "viewing_pack.md")
    with open(html_path, "w") as fh:
        fh.write(render_html(c, named, named_default, meta))
    with open(md_path, "w") as fh:
        fh.write(render_md(c, named, named_default, meta))

    # terse operator summary to stderr — every figure computed above, none accepted as input.
    sys.stderr.write(
        "%s OK — %s(%s) -> %s(%s): net ΣΔ %s · movers %d (up %d / down %d) · "
        "value-up-rank-down %d · %d common\n  wrote %s\n  wrote %s\n" % (
            TOOL, meta["base_name"], meta["base_md5"], meta["cand_name"], meta["cand_md5"],
            signed(c["net"]), len(c["movers"]), len(c["ups"]), len(c["downs"]),
            len(c["failures"]), len(c["common"]), html_path, md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
