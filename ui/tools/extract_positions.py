#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI v1.3 — POSITIONS MAP EXTRACT (item 196(2)).  Directive:
docs/DIRECTIVE_UI_v1_3_pocket_profiles_2026-07-16.md.

Emits a VALUES-FREE position map for the positional-value breakdown.  Read-only over
docs/inputs/AFFL_Player_Locations.csv and the SHIPPED board bundle; carries ONLY canonical position
codes keyed by the board player key.  It computes NO value — the board bundle stays the sole value
source, and ui/data/ + ui/tools/ingest_inputs.py are untouched.

REUSES the ESTABLISHED name->id join (the same `nkey` normalisation and the two-Max-Kings distinctness
assertion the ingest uses); HALT-AND-ASK on any join ambiguity or missing coverage.

Run:  python3 ui/tools/extract_positions.py     (exit 0 = clean map written; exit 2 = HALT)
"""
import csv, json, os, sys, collections, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUTS = os.path.join(ROOT, "docs", "inputs")
UI_DATA = os.path.join(ROOT, "ui", "data")
BOARD_BUNDLE = os.path.join(UI_DATA, "board_view_working.js")
LOC_CSV = os.path.join(INPUTS, "AFFL_Player_Locations.csv")
OUT = os.path.join(ROOT, "ui", "app", "positions_data.js")
# NO HAND-TYPED BOARD PIN HERE — retired 2026-07-28 with the one in ui/app/config.js (issue #231).
# This file used to carry `EXPECTED_BOARD = "06d8af60"` and halt when the bundle disagreed with it.
# The board moved three times and the constant did not, so the tool refused to run at all:
#     ■ HALT — board id mismatch — bundle 8a38cca4 != EXPECTED_BOARD 06d8af60
# It authenticates the bundle the same way ringFence() does instead — see load_board().

# REUSE the ingest's established join key rather than reimplementing it.
_spec = importlib.util.spec_from_file_location(
    "ingest_inputs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ingest_inputs.py"))
_ing = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ing)   # ingest_inputs.py has no top-level side effects (guarded main)
nkey = _ing.nkey

# CSV Position/s token -> board posCode vocabulary (6 canonical rows).
TOK2CODE = {"K-DEF": "KPD", "G-DEF": "SD", "MID": "MID",
            "G-FWD": "SF", "K-FWD": "KPF", "RUCK": "RUCK", "RUC": "RUCK"}


def halt(msg):
    sys.stderr.write("\n■ HALT — %s\n  Nothing is guessed; the positional breakdown refuses.\n" % msg)
    sys.exit(2)


def readcsv(path):
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(path, newline="", encoding=enc) as f:
                return list(csv.reader(f))
        except UnicodeDecodeError:
            continue
    halt("could not decode %s" % os.path.basename(path))


def load_board():
    if not os.path.exists(BOARD_BUNDLE):
        halt("board bundle missing: %s" % BOARD_BUNDLE)
    s = open(BOARD_BUNDLE, encoding="utf-8").read()
    obj = json.loads(s[s.index("{"): s.rindex("}") + 1])
    stamp = obj.get("stamp", {})
    # Authenticate the bundle exactly as the UI ring-fence does: the board of record the bundle
    # declares (stamp.board, copied verbatim from data/expected_boot.json by extract_board_view.py)
    # against the md5 of the board artifact it was actually built from. That relationship holds for
    # whatever is staged — a held bundle, an adopted one, a candidate mid-baseline — so this tool
    # tracks the board instead of having to be re-pinned every time it moves.
    #
    # It deliberately does NOT compare against the live manifest. The UI bundles are held behind the
    # engine on purpose while a board change is in flight, and halting on that would make this tool
    # unusable for the whole baseline. "Has the UI caught up?" is the adoption gate's question:
    # ui/tests/adoption_gate.test.js.
    board = str(stamp.get("board", ""))
    built = str(stamp.get("board_md5") or stamp.get("srcmd5") or "")
    if not board or not built:
        halt("bundle stamp carries no board identity (board=%r board_md5=%r) — cannot authenticate"
             % (board[:8], built[:8]))
    if board[:8] != built[:8]:
        halt("bundle is internally inconsistent — declares board %s but was built from %s"
             % (board[:8], built[:8]))
    return obj, board


def main():
    board, board_md5 = load_board()
    players = board.get("players", [])
    board_by = collections.defaultdict(list)
    for p in players:
        board_by[nkey(p["name"])].append(p)

    rows = [r for r in readcsv(LOC_CSV)[1:] if r and r[0]]

    # unambiguous within the CSV (the established zero-ambiguity requirement)
    loc_by = collections.defaultdict(list)
    for r in rows:
        loc_by[nkey(r[0])].append(r)
    dups = [k for k, v in loc_by.items() if len(v) > 1]
    if dups:
        halt("ambiguous player name(s) in Player_Locations.csv (normalised): %s" % dups)

    # the two Max Kings stay distinct by the established name key
    mk, mxk = nkey("Max King"), nkey("Maxwell King")
    if mk == mxk:
        halt("the two Max Kings collapsed under the normalised key — join is unsafe")

    # every board player joins to exactly one CSV row (full coverage, no ambiguity)
    by_key = {}
    unmatched = []
    for p in players:
        cand = loc_by.get(nkey(p["name"]))
        if not cand:
            unmatched.append(p["name"]); continue
        toks = [t.strip() for t in cand[0][2].split(",") if t.strip()]
        codes, seen = [], set()
        for t in toks:
            if t not in TOK2CODE:
                halt("unknown Position/s token %r for %s" % (t, p["name"]))
            c = TOK2CODE[t]
            if c not in seen:
                seen.add(c); codes.append(c)
        if not codes:
            halt("no position listed for %s" % p["name"])
        by_key[p["key"]] = codes
    if unmatched:
        halt("board player(s) have no Player_Locations row (join gap): %s" % unmatched[:10])

    payload = {
        # `expectedBoard` keeps its key and its meaning — the 8-hex head of the board this map was
        # built against — but is now derived from that board rather than typed. Nothing reads it;
        # the key is retained so the generated artifact's shape does not move under #232.
        "stamp": {"board": board_md5, "expectedBoard": board_md5[:8], "n": len(by_key),
                  "source": "docs/inputs/AFFL_Player_Locations.csv (Position/s), values-free"},
        "byKey": by_key,
    }
    body = ("// GENERATED by ui/tools/extract_positions.py — VALUES-FREE position map (item 196(2)).\n"
            "// Canonical posCodes per board player, from the owner's AFFL_Player_Locations.csv\n"
            "// `Position/s` column via the established normalised-name join.  NO dollar value is carried;\n"
            "// the board bundle remains the sole value source.  Regenerate if the CSV changes.\n"
            "window.__CLUB_POSITIONS__ = " + json.dumps(payload, ensure_ascii=False, sort_keys=True) + ";\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote %s — %d players, board %s (values-free)" % (
        os.path.relpath(OUT, ROOT), len(by_key), board_md5[:8]))


if __name__ == "__main__":
    main()
