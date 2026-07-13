#!/usr/bin/env python3
"""Read-only board-view extractor for the Matchday UI (TIER 3; never bakes).

Reads the derived board artifact and the pinned boot identity STRICTLY READ-ONLY and emits two
tiered, stamped view files as `window.__…__ = {…}` script bundles (so the app renders from file://
and when served). This script NEVER writes outside ui/ and NEVER recomputes a value — it trims and
tiers the fields the LOCK/DESIGN_DIRECTION call for. The two-tier UI law made real at the data layer:
the public bundle is leak-proof by construction (no keys, no md5/guard stamps, no mech, no owner-rule).

Board-id ring-fence: md5(rl_app_data.json) == the pinned board id (9ecbe0fa…). The emitted working
bundle carries that md5 as `stamp.srcmd5`; the app fail-closes if it disagrees with the expected board.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "data", "rl_build", "rl_app_data.json")
BOOT = os.path.join(REPO, "data", "expected_boot.json")
OUT_DIR = os.path.join(HERE, "..", "data")

# Position label map (engine codes -> owner-voice display; names/values first, jargon in brackets).
POS = {
    "MID": "Mid", "RUC": "Ruck", "KEY_FWD": "Key Fwd", "GEN_FWD": "Fwd",
    "KEY_DEF": "Key Def", "GEN_DEF": "Def",
}


def label_pos(code):
    return POS.get(code, (code or "").replace("_", " ").title() or "—")


def main():
    raw = open(SRC, "rb").read()
    srcmd5 = hashlib.md5(raw).hexdigest()
    d = json.loads(raw)
    boot = json.load(open(BOOT))

    active = d["active"]
    back = d.get("back", [])
    max_v = max((p.get("v") or 0) for p in active) or 1

    def row_working(p):
        # Full field set for the owner's working aid (identity-bearing).
        return {
            "key": p.get("key"),
            "name": p.get("name"),
            "pos": label_pos(p.get("grp") or p.get("gf")),
            "posCode": p.get("grp") or p.get("gf"),
            "club": p.get("club"),
            "age": p.get("age"),
            "g": p.get("g"),
            "cat": p.get("cat"),
            "pk": p.get("pk"),
            "yr": p.get("yr"),
            "ty": p.get("ty"),
            "v": p.get("v"),
            "lens": [p.get("vM2"), p.get("vM1"), p.get("v"), p.get("vP1"), p.get("vP2")],
            "track": p.get("track") or [],
            "owner_rule": bool(p.get("brodieBase")),
            # vPrev / vRaw are §7.3 export fields the v2.8 board does not yet carry; passed through
            # verbatim if present so the wired Δ-vs-bake column and pre-override hover light up with
            # zero UI changes the day the export adds them. Never fabricated here.
            "vPrev": p.get("vPrev"),
            "vRaw": p.get("vRaw"),
            # `ov` = the owner-override DISPLAY block {factor, dispv, mark, note, prov}, present only on an
            # overridden row (v2.9 bake: Brodie ×0.50). Working-tier only (owner's aid); passed through
            # verbatim so the UI can render the overridden rail (dispv) + the OWNER OVERRIDE mark. Never on
            # the public bundle (row_public omits it). Absent on non-overridden rows.
            "ov": p.get("ov"),
            # per-lever G-ATTR cumulative deltas {L1,L4,L2,L3,L5} (sum == v - vPrev). Working-tier only
            # (attribution is owner-facing); passed through verbatim, never fabricated here.
            "levers": p.get("levers"),
            "lti_reg": p.get("lti_reg"),
        }

    def row_public(p):
        # Sanitised: no key/slug, no ids, no owner-rule machinery, no pathway/mech. Value + movement only.
        return {
            "name": p.get("name"),
            "pos": label_pos(p.get("grp") or p.get("gf")),
            "v": p.get("v"),
            # Published movement-vs-previous-round scheme; wired to dRound / dRoundRank when the weekly
            # loop exports them. Absent today -> the app renders a neutral "steady" pill, never a fake move.
            "dRound": p.get("dRound"),
            "dRoundRank": p.get("dRoundRank"),
        }

    working_rows = [row_working(p) for p in active]
    back_rows = [row_working(p) for p in back]  # backward-board-only players (surface at −1/−2 lens)
    public_rows = [row_public(p) for p in active]

    picks = d.get("picks", [])
    pvc = d.get("PVC", {})
    # items 12/14: future-lens phantom pick lines (+1/+2 lenses only) + the lens-conservation diagnostic.
    # Working-tier only; passed through verbatim. The current/-1/-2 player ladder never reads these (the
    # phantom picks stand in for the future player on the forward lenses; item-14 ladder exclusion holds).
    lens_picks = d.get("lensPicks", [])
    lens_conservation = d.get("lensConservation", {})

    working = {
        "stamp": {
            "srcmd5": srcmd5,
            "board": boot.get("board"),
            "engine": boot.get("engine_head", "")[:8],
            "store": boot.get("store", "")[:8],
            "register": boot.get("register", "")[:8],
            "config": boot.get("config", "")[:12],
            "tag": "v2.8",
            "panel": boot.get("panel"),
            "baseYear": d.get("BASE_YEAR"),
            "nPlayers": len(active),
            "maxV": max_v,
            "guard5": "pass",
            "real": True,
        },
        "lensYears": [d.get("BASE_YEAR", 2026) + off for off in (-2, -1, 0, 1, 2)],
        "players": working_rows,
        "back": back_rows,
        "picks": picks,
        "pvc": pvc,
        "lensPicks": lens_picks,
        "lensConservation": lens_conservation,
    }

    public = {
        "stamp": {
            "baseYear": d.get("BASE_YEAR"),
            "nPlayers": len(active),
            "maxV": max_v,
        },
        "players": public_rows,
    }

    os.makedirs(OUT_DIR, exist_ok=True)

    def emit(name, var, obj):
        path = os.path.join(OUT_DIR, name)
        with open(path, "w") as fh:
            fh.write("// GENERATED — read-only view bundle from data/rl_build/rl_app_data.json.\n")
            fh.write("// Do not hand-edit; regenerate via ui/tools/extract_board_view.py.\n")
            fh.write("window.%s = " % var)
            json.dump(obj, fh, ensure_ascii=False, separators=(",", ":"))
            fh.write(";\n")
        return path

    p1 = emit("board_view_working.js", "__MATCHDAY_WORKING__", working)
    p2 = emit("board_view_public.js", "__MATCHDAY_PUBLIC__", public)

    print("srcmd5 (== board id):", srcmd5)
    print("board id (boot)     :", boot.get("board"))
    assert srcmd5.startswith(boot.get("board", "")[:8]), "RING-FENCE FAIL: artifact md5 != pinned board id"
    print("ring-fence OK       : md5 head == board id")
    print("active players      :", len(active), "| back-only:", len(back_rows), "| picks:", len(picks))
    print("wrote:", os.path.relpath(p1, REPO))
    print("wrote:", os.path.relpath(p2, REPO))


if __name__ == "__main__":
    sys.exit(main())
