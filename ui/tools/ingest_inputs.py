#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI v1.2 — THE INPUTS INGEST (items 178(2)/(3)/(4), 180, 181(2)).  Directive:
docs/DIRECTIVE_UI_v1_2_club_valuation_2026-07-16.md.

The no-LLM pipeline's deterministic half: read the owner's authored input files under docs/inputs/
STRICTLY READ-ONLY, VALIDATE-OR-HALT (halt, never guess/warn-and-continue), price every held draft
pick off the SHIPPED engine's canonical pick curve, aggregate a per-club valuation, and emit the
committed view bundle ui/data/club_valuation.js (window.__CLUB_VALUATION__ = {...}).

FENCE: ui/-only + read-only reads of docs/inputs/ and the shipped board bundle + the engine curve
file (for the stamp cross-check only).  NO value is recomputed here — a pick's price is a MEAN of the
engine's own curve; a player's value is the stamped board `v`, only summed/greedily selected.  Values
from the pick workbook (Raw Value / Value (counted) / Pick Values tab) are NEVER ingested.

Run:  python3 ui/tools/ingest_inputs.py         (exit 0 = clean bundle written; exit 2 = HALT)
"""
import csv, json, os, sys, collections, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
INPUTS = os.path.join(ROOT, "docs", "inputs")
UI_DATA = os.path.join(ROOT, "ui", "data")
BOARD_BUNDLE = os.path.join(UI_DATA, "board_view_working.js")
ENGINE_CURVE = os.path.join(ROOT, "engine", "rl_after", "pvc_curve_L1b.json")
OUT = os.path.join(UI_DATA, "club_valuation.js")

EXPECTED_BOARD = "790136a3"      # ui/app/config.js EXPECTED_BOARD — the shipped board (v2.10)
PICK_FUTURE_DISCOUNT = 0.10      # R104.5 balanced posture — the ONLY posture in this build
BASE_YEAR = 2026
# Best-23 positional structure (item 178(3)); posCode vocab is the board's CURRENT posCode.
SLOTS = [("KEY_DEF", 2), ("GEN_DEF", 4), ("MID", 5), ("GEN_FWD", 4), ("KEY_FWD", 2), ("RUC", 1)]
BENCH = 5
FREE_AGENTS = "Free Agents"

verdicts = []   # [(check, ok, detail)]
notes = []


def check(name, ok, detail=""):
    verdicts.append((name, bool(ok), detail))
    return bool(ok)


def halt(reason):
    """Print the verdict table + the halt reason, write a HALTED bundle (so the overlay refuses), exit 2."""
    _print_verdicts()
    print("\n■ HALT — %s" % reason)
    print("  The club-valuation overlay refuses to render on this ingest.  Nothing is guessed.")
    payload = {
        "stamp": {"expectedBoard": EXPECTED_BOARD, "generated": _now()},
        "halt": {"reason": reason, "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts]},
        "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts],
        "clubs": [], "picksByTeam": {}, "notes": notes,
    }
    _write(payload)
    sys.exit(2)


def _now():
    # deterministic-enough provenance stamp; no bearing on any value
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def readcsv(path):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return list(csv.reader(f)), enc
        except UnicodeDecodeError:
            continue
    halt("could not decode %s as utf-8/cp1252/latin-1" % os.path.basename(path))


def nkey(s):
    """Normalised name join key: collapse whitespace + casefold.  Resolves the 5 case-only surname
       variants (MacDonald/Macdonald, DeMattia/Demattia, …) between the board and the owner's CSVs
       without guessing; still keeps the two Max Kings distinct ('max king' != 'maxwell king')."""
    return " ".join(str(s).strip().split()).casefold()


# ---------------------------------------------------------------------------- load the shipped board
def load_board():
    if not os.path.exists(BOARD_BUNDLE):
        halt("board bundle missing: %s" % BOARD_BUNDLE)
    s = open(BOARD_BUNDLE, encoding="utf-8").read()
    try:
        obj = json.loads(s[s.index("{"): s.rindex("}") + 1])
    except Exception as e:
        halt("board bundle is not parseable JSON: %s" % e)
    stamp = obj.get("stamp", {})
    board = str(stamp.get("board", ""))
    check("board id ring-fence", board[:8] == EXPECTED_BOARD,
          "bundle board %s vs expected %s" % (board[:8], EXPECTED_BOARD))
    if board[:8] != EXPECTED_BOARD:
        halt("board id mismatch — bundle %s != EXPECTED_BOARD %s (regenerate board_view or re-pin)"
             % (board[:8], EXPECTED_BOARD))
    pvc = {int(k): v for k, v in obj.get("pvc", {}).items()}
    return obj, stamp, pvc


# ------------------------------------------------------- canonical pick curve stamp-assert (S5 guard)
def assert_pvc(pvc):
    if not pvc:
        halt("no PVC in the board bundle — cannot locate the canonical pick curve (HALT-AND-ASK)")
    if not os.path.exists(ENGINE_CURVE):
        halt("engine canonical curve file missing: %s (HALT-AND-ASK on provenance)" % ENGINE_CURVE)
    doc = json.load(open(ENGINE_CURVE))
    eng = {int(k): int(v) for k, v in doc["curve"].items()}
    shared = [k for k in pvc if k in eng]
    bytematch = bool(shared) and all(pvc[k] == eng[k] for k in shared)
    check("PVC == engine pvc_curve_L1b.json (over %d shared picks)" % len(shared), bytematch)
    if not bytematch:
        halt("STALE-CURVE GUARD: the board bundle's PVC does not byte-match the engine's adopted "
             "pvc_curve_L1b.json — provenance ambiguous (the S5 failure).  HALT-AND-ASK.")
    check("PVC numeraire anchor pick1 == 3000", pvc.get(1) == 3000, "pick1 = %s" % pvc.get(1))
    if pvc.get(1) != 3000:
        halt("PVC pick1 != 3000 — numeraire drift; refusing to price picks against a drifted ruler")
    # monotone non-increasing (the curve is a ruler)
    ks = sorted(pvc)
    mono = all(pvc[ks[i]] >= pvc[ks[i + 1]] for i in range(len(ks) - 1))
    check("PVC monotone non-increasing", mono)
    if not mono:
        halt("PVC is not monotone non-increasing — not a valid pick ruler")
    return pvc


# ----------------------------------------------------------------------------------- price one pick
def price_pick(pvc, lo, hi, year):
    vals = [pvc[p] for p in range(lo, hi + 1)]
    mean = sum(vals) / len(vals)
    if year == 2027:
        mean *= (1.0 - PICK_FUTURE_DISCOUNT)
    return mean


# ----------------------------------------------------------------------------------------- the picks
def load_picks(pvc, affl_teams):
    try:
        import openpyxl
    except ImportError:
        halt("openpyxl not available — cannot read AFFL_Pick_Locations.xlsx")
    path = os.path.join(INPUTS, "AFFL_Pick_Locations.xlsx")
    if not os.path.exists(path):
        halt("pick workbook missing: %s" % path)
    import warnings
    warnings.filterwarnings("ignore")
    wb = openpyxl.load_workbook(path, data_only=True)

    # --- Ladder: the 2027 multiplier cell (read + reconcile against R104.5's governing 0.10) ---
    mult = None
    if "Ladder" in wb.sheetnames:
        for row in wb["Ladder"].iter_rows(values_only=True):
            if row and row[0] and str(row[0]).startswith("2027 value multiplier"):
                mult = row[1]
    governing = round(1.0 - PICK_FUTURE_DISCOUNT, 6)
    agree = mult is not None and abs(float(mult) - governing) < 1e-6
    check("ladder 2027 multiplier reconciles to R104.5 balanced (1-0.10=0.90)", agree,
          "sheet cell = %s · governing = %s" % (mult, governing))
    if not agree:
        halt("2027 MULTIPLIER DISAGREEMENT: the sheet says %s but R104.5 balanced governs %s — "
             "reconcile the sheet or the ruling (HALT-AND-FLAG, never silently pick)" % (mult, governing))

    # --- Picks ledger ---
    if "Picks" not in wb.sheetnames:
        halt("pick workbook has no 'Picks' sheet")
    picks = []
    for i, row in enumerate(wb["Picks"].iter_rows(values_only=True)):
        if i < 2 or row[0] is None:   # rows 0-1 are title+header
            continue
        pid, yr, rnd, orig, owner, lo, hi = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        picks.append(dict(id=pid, year=int(yr), rnd=rnd, orig=str(orig).strip(),
                          owner=str(owner).strip(), lo=int(lo), hi=int(hi)))

    check("pick ledger row count == 160", len(picks) == 160, "%d rows" % len(picks))

    # bands 1..80, low <= high
    band_ok = all(1 <= p["lo"] <= 80 and 1 <= p["hi"] <= 80 and p["lo"] <= p["hi"] for p in picks)
    bad = [p["id"] for p in picks if not (1 <= p["lo"] <= 80 and 1 <= p["hi"] <= 80 and p["lo"] <= p["hi"])]
    check("all bands within 1-80 and low <= high", band_ok, "offenders: %s" % (bad or "none"))
    if not band_ok:
        halt("band violation on pick ids %s (out of 1-80 or low>high)" % bad)

    # draft year <= one year ahead
    yrs = sorted({p["year"] for p in picks})
    yr_ok = all(BASE_YEAR <= y <= BASE_YEAR + 1 for y in yrs)
    check("both drafts <= one year ahead (%d/%d)" % (BASE_YEAR, BASE_YEAR + 1), yr_ok, "years=%s" % yrs)
    if not yr_ok:
        halt("draft year out of [%d, %d]: %s" % (BASE_YEAR, BASE_YEAR + 1, yrs))

    # every Owner + Origin joins to exactly one AFFL club (Free Agents permitted)
    club_set = set(affl_teams) | {FREE_AGENTS}

    def join_club(short):
        if short in club_set:
            return [short]
        cand = [t for t in affl_teams if t == short or t.startswith(short + " ")]
        return cand

    omap = {}
    for field in ("owner", "orig"):
        for p in picks:
            v = p[field]
            c = join_club(v)
            if len(c) != 1:
                check("%s '%s' joins to exactly one AFFL club" % (field, v), False,
                      "candidates: %s" % c)
                halt("%s '%s' does not join to a unique AFFL club (candidates %s)" % (field, v, c))
            omap[v] = c[0]
    check("every pick Owner + Origin joins to exactly one AFFL club (+Free Agents)", True,
          "%d distinct owners+origins" % len(omap))

    # price + attach the joined team
    for p in picks:
        p["team"] = omap[p["owner"]]
        p["origin_team"] = omap[p["orig"]]
        p["value"] = round(price_pick(pvc, p["lo"], p["hi"], p["year"]))
        p["band"] = "#%d-%d" % (p["lo"], p["hi"]) if p["lo"] != p["hi"] else "#%d" % p["lo"]

    # pick-count conservation (the Dashboard convention): ledger == Sum per-owner counts == 160
    per_owner = collections.Counter(p["team"] for p in picks)
    conserved = sum(per_owner.values()) == len(picks) == 160
    check("pick-count conservation (Sum per-club == ledger == 160)", conserved,
          "sum=%d ledger=%d" % (sum(per_owner.values()), len(picks)))
    if not conserved:
        halt("pick-count conservation failed")
    check("all 160 picks priced off the canonical curve", all("value" in p for p in picks),
          "priced=%d" % sum(1 for p in picks if "value" in p))
    return picks


# ---------------------------------------------------------------- the CSV validations (name -> id)
def validate_csvs(board_by_nkey):
    loc, lenc = readcsv(os.path.join(INPUTS, "AFFL_Player_Locations.csv"))
    pos, penc = readcsv(os.path.join(INPUTS, "AFFL_Future_Positioning.csv"))
    loc_rows = [r for r in loc[1:] if r and r[0]]
    pos_rows = [r for r in pos[1:] if r and r[0]]

    # normalised-key uniqueness within each source (zero ambiguity)
    loc_by = collections.defaultdict(list)
    for r in loc_rows:
        loc_by[nkey(r[0])].append(r)
    pos_by = collections.defaultdict(list)
    for r in pos_rows:
        pos_by[nkey(r[1])].append(r)   # positioning col1 = player_name, col0 = stable_player_id
    loc_dups = [k for k, v in loc_by.items() if len(v) > 1]
    pos_dups = [k for k, v in pos_by.items() if len(v) > 1]
    check("player names unambiguous in Player_Locations.csv (normalised)", not loc_dups,
          "dups: %s" % (loc_dups or "none"))
    check("player names unambiguous in Future_Positioning.csv (normalised)", not pos_dups,
          "dups: %s" % (pos_dups or "none"))
    if loc_dups or pos_dups:
        halt("ambiguous player name(s) in the input CSVs: %s" % (loc_dups + pos_dups))

    # every location name joins to exactly one stable id via positioning, and to exactly one board row
    unmatched_pos = [r[0] for r in loc_rows if nkey(r[0]) not in pos_by]
    unmatched_board = [r[0] for r in loc_rows if nkey(r[0]) not in board_by_nkey]
    check("every Player_Locations name -> a unique stable_player_id (positioning join)",
          not unmatched_pos, "unmatched: %s" % (unmatched_pos or "none"))
    check("every Player_Locations name -> a unique board player (name join)",
          not unmatched_board, "unmatched: %s" % (unmatched_board or "none"))
    if unmatched_pos or unmatched_board:
        halt("player name(s) fail the id/board join: %s" % (unmatched_pos + unmatched_board))

    # the two Max Kings asserted distinct by name
    mk, mxk = nkey("Max King"), nkey("Maxwell King")
    distinct = (mk != mxk and mk in pos_by and mxk in pos_by
                and pos_by[mk][0][0] != pos_by[mxk][0][0])
    check("the two Max Kings are distinct by name (assert)", distinct,
          "Max King=%s · Maxwell King=%s" % (
              pos_by.get(mk, [["?"]])[0][0], pos_by.get(mxk, [["?"]])[0][0]))
    if not distinct:
        halt("the two Max Kings failed the distinctness assertion")

    # 5 case-only surname variants: reconciled by the normalised key, recorded (not a halt)
    exact_board_names = {rows[0]["name"].strip() for rows in board_by_nkey.values()}
    variants = sorted({r[0] for r in loc_rows
                       if r[0].strip() not in exact_board_names and nkey(r[0]) in board_by_nkey})
    if variants:
        notes.append("case-only name variants reconciled by the normalised join key (not halted): "
                     + ", ".join(variants))
        check("case-only name variants reconciled by normalised key", True,
              "%d reconciled: %s" % (len(variants), ", ".join(variants)))

    # authored-ownership vs the stamped board (agreement report; board is the display membership source)
    def normt(t):
        return FREE_AGENTS if str(t).strip().lower() == "free agents" else str(t).strip()
    mismatch = []
    for r in loc_rows:
        bp = board_by_nkey.get(nkey(r[0]))
        if bp:
            ct, bt = normt(r[1]), bp[0]["affl_team"]
            if ct != bt:
                mismatch.append((r[0], ct, bt))
    check("authored CSV ownership agrees with the stamped board affl_team", not mismatch,
          "%d mismatch(es)%s" % (len(mismatch), ("" if not mismatch else ": " + str(mismatch[:5]))))
    if mismatch:
        notes.append("CSV ownership differs from the stamped board for %d player(s); the board rides "
                     "one bake behind for player club-moves (pick trades update on re-ingest). "
                     "First few: %s" % (len(mismatch), mismatch[:5]))
    return loc_enc_note(lenc, penc)


def loc_enc_note(lenc, penc):
    notes.append("input encodings: Player_Locations=%s · Future_Positioning=%s" % (lenc, penc))
    return True


# -------------------------------------------------------------------------- per-club valuation
def build_clubs(players, picks, affl_teams):
    picks_by_team = collections.defaultdict(list)
    for p in picks:
        picks_by_team[p["team"]].append(p)

    roster_by = collections.defaultdict(list)
    for p in players:
        t = p.get("affl_team")
        if t and t != FREE_AGENTS:
            roster_by[t].append(p)

    clubs = []
    for team in affl_teams:
        roster = sorted(roster_by.get(team, []), key=lambda x: -x["v"])
        total_player = sum(p["v"] for p in roster)
        top5 = sum(p["v"] for p in roster[:5])
        top10 = sum(p["v"] for p in roster[:10])

        # Best-23: greedy positional fill by highest board v per slot (CURRENT posCode), then best-5 bench.
        used = set()
        best23_keys = []
        best23 = 0
        for pos, n in SLOTS:
            picked = [p for p in roster if p["posCode"] == pos and id(p) not in used][:n]
            for p in picked:
                used.add(id(p)); best23 += p["v"]; best23_keys.append(p["key"])
        bench = [p for p in roster if id(p) not in used][:BENCH]
        for p in bench:
            used.add(id(p)); best23 += p["v"]; best23_keys.append(p["key"])

        tp = [t for t in picks_by_team[team]]
        total_picks = sum(p["value"] for p in tp)
        clubs.append({
            "team": team,
            "display": DISPLAY.get(team, team),
            "overall": total_player + total_picks,
            "totalPlayer": total_player,
            "totalPicks": total_picks,
            "top5": top5, "top10": top10,
            "best23": best23, "nonBest23": total_player - best23,
            "nRoster": len(roster), "nPicks": len(tp),
            "best23Keys": best23_keys,
        })
    clubs.sort(key=lambda c: -c["overall"])
    return clubs, picks_by_team


# ---------------------------------------------------------------------------------------- output
def _write(payload):
    body = ("// GENERATED by ui/tools/ingest_inputs.py — the no-LLM VALIDATE-OR-HALT club-valuation\n"
            "// ingest.  DO NOT hand-edit; regenerate after any docs/inputs/ change (see\n"
            "// ui/HOW_TO_UPDATE_INPUTS.md).  Pick prices are the engine's canonical PVC evaluated over\n"
            "// each band; no sheet value is ingested; no player value is recomputed.\n"
            "window.__CLUB_VALUATION__ = " + json.dumps(payload, ensure_ascii=False, sort_keys=True) + ";\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)


def _print_verdicts():
    print("\n  VALIDATION VERDICTS")
    print("  " + "-" * 72)
    for c, ok, d in verdicts:
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", c, ("  (%s)" % d) if d else ""))


# DISPLAY map mirrors ui/app/config.js CLUB_DISPLAY (display-only; long name stays the join key).
DISPLAY = {
    "North Melbourne Kangaroos": "North Melbourne",
    "Collingwood Magpies": "Collingwood",
    "Port Adelaide Power": "Port Adelaide",
}


def main():
    obj, stamp, pvc = load_board()
    players = obj.get("players", [])
    pvc = assert_pvc(pvc)

    board_by_nkey = collections.defaultdict(list)
    for p in players:
        board_by_nkey[nkey(p["name"])].append(p)
    check("board name-join keys unambiguous (normalised)",
          all(len(v) == 1 for v in board_by_nkey.values()),
          "dups: %s" % [k for k, v in board_by_nkey.items() if len(v) > 1])

    affl_teams = sorted({p["affl_team"] for p in players
                         if p.get("affl_team") and p["affl_team"] != FREE_AGENTS})
    check("AFFL club count", True, "%d clubs (+ Free Agents pool)" % len(affl_teams))

    validate_csvs(board_by_nkey)
    picks = load_picks(pvc, affl_teams)
    clubs, picks_by_team = build_clubs(players, picks, affl_teams)

    payload = {
        "stamp": {
            "board": stamp.get("board"), "engine": stamp.get("engine"), "store": stamp.get("store"),
            "tag": stamp.get("tag"), "expectedBoard": EXPECTED_BOARD, "baseYear": BASE_YEAR,
            "pvcSource": "engine/rl_after/pvc_curve_L1b.json (adopted; == rl_app_data PVC; pick1=3000)",
            "pvcOk": True, "discount2027": PICK_FUTURE_DISCOUNT, "mult2027": 1.0 - PICK_FUTURE_DISCOUNT,
            "posture": "balanced (canonical; the only posture in this build)",
            "nPicks": len(picks), "nClubs": len(clubs), "generated": _now(),
        },
        "halt": None,
        "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts],
        "notes": notes,
        "clubs": clubs,
        "picksByTeam": {t: [{"id": p["id"], "year": p["year"], "round": p["rnd"],
                             "origin": p["origin_team"], "originDisplay": DISPLAY.get(p["origin_team"], p["origin_team"]),
                             "low": p["lo"], "high": p["hi"], "band": p["band"], "value": p["value"]}
                            for p in sorted(picks_by_team[t], key=lambda x: (x["year"], -x["value"]))]
                        for t in picks_by_team},
    }
    _write(payload)
    _print_verdicts()
    print("\n  CLEAN INGEST — %d picks priced, %d clubs.  Bundle: ui/data/club_valuation.js" %
          (len(picks), len(clubs)))
    print("\n  TOP-3 CLUBS BY OVERALL VALUE:")
    for c in clubs[:3]:
        print("    %-18s overall %s  (players %s + picks %s)" %
              (c["display"], f"{c['overall']:,}", f"{c['totalPlayer']:,}", f"{c['totalPicks']:,}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
