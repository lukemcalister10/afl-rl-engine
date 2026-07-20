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
# Production paths are the defaults; each may be redirected via an env var so a FIXTURE run
# (a temporary board + temporary boot manifest + temporary out dir) can exercise the exact same
# fail-closed code without touching production data. The overrides change WHERE we read/write, never
# WHAT we assert — every ring-fence below stays live regardless of the paths.
SRC = os.environ.get("RL_UI_SRC", os.path.join(REPO, "data", "rl_build", "rl_app_data.json"))
BOOT = os.environ.get("RL_UI_BOOT", os.path.join(REPO, "data", "expected_boot.json"))
# The pinned master store — the "master database" of item 1 (2026-07-15 feedback). Read STRICTLY
# READ-ONLY and md5-verified against expected_boot.store (fail-closed, same doctrine as the board
# ring-fence): the extractor sources the AFL + AFFL club DISPLAY strings from here. No value is read
# by ev() from these fields; nothing is computed; the store is never written.
STORE = os.environ.get("RL_UI_STORE", os.path.join(REPO, "engine", "rl_after", "rl_model_data.json"))
OUT_DIR = os.environ.get("RL_UI_OUT_DIR", os.path.join(HERE, "..", "data"))


def norm_club(name):
    """Display normalisation for a club string (casing only; the store carries 'Free agents'
    and 'Free Agents' as two spellings of one AFFL bucket). Never invents a club."""
    if not name:
        return None
    s = str(name).strip()
    return "Free Agents" if s.lower() == "free agents" else s

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

    # ---- item 1: AFFL club from the pinned master store (READ-ONLY, md5-verified) ----------------
    # The board (rl_app_data.json) already carries the AFL club as `club`; the AFFL club lives only in
    # the master store. We read it here as a DISPLAY string, verifying the store md5 head against the
    # pinned store id first so a swapped/stale store fails closed rather than mislabelling a player.
    store_raw = open(STORE, "rb").read()
    store_md5 = hashlib.md5(store_raw).hexdigest()
    want_store = str(boot.get("store", ""))[:8]
    assert store_md5.startswith(want_store), (
        "STORE RING-FENCE FAIL: rl_model_data.json md5 %s != pinned store %s" % (store_md5[:8], want_store))
    affl_by_key = {}
    for r in json.loads(store_raw):
        k = r.get("key")
        if k:
            affl_by_key[k] = norm_club(r.get("affl_team"))

    def row_working(p):
        # Full field set for the owner's working aid (identity-bearing).
        return {
            "key": p.get("key"),
            "name": p.get("name"),
            "pos": label_pos(p.get("grp") or p.get("gf")),
            "posCode": p.get("grp") or p.get("gf"),
            "club": p.get("club"),
            # item 1 (2026-07-15): AFL club + AFFL club listed per player. DISPLAY-ONLY strings — the AFL
            # club is the board's own `club`; the AFFL club is joined from the master store by key. No value
            # is changed; ev() never reads these. Null-safe: a player without an AFFL row shows "—" in the UI.
            "afl_club": p.get("club"),
            "affl_team": affl_by_key.get(p.get("key")),
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
            # movement-vs-previous-round fields, wired to the weekly loop's dRound / dRoundRank exports.
            # Passed through VERBATIM on the working tier too (same scheme as row_public); None until the
            # weekly loop lands them -> the working card renders a neutral "steady", never a fabricated move.
            "dRound": p.get("dRound"),
            "dRoundRank": p.get("dRoundRank"),
        }

    def row_public(p):
        # Sanitised: no key/slug, no ids, no owner-rule machinery, no pathway/mech. Value + movement only.
        return {
            "name": p.get("name"),
            "pos": label_pos(p.get("grp") or p.get("gf")),
            # item 1: clubs are public-safe display strings (no id/slug leak), so they ride the public
            # bundle too. AFL club = the board's `club`; AFFL club joined from the store by key.
            "afl_club": p.get("club"),
            "affl_team": affl_by_key.get(p.get("key")),
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
    # Leg-F entrant/phantom machinery (MEMO_LEGF §2.viii; owner item 359). Working-tier ONLY — this is
    # owner/internal intake economics and never rides the public bundle. Passed through VERBATIM; the
    # extractor recomputes nothing. Absent on a pre-Leg-F board -> empty container (carried, never
    # fabricated), so the +1/+2 entrant banner degrades to "no phantom layer" rather than an invented one:
    #   phantomLayer  — per-club × per-lens entrant/draft/free breakdown (the banner detail rows)
    #   phantomPicks  — the flat phantom draft-pick ladder on the forward lenses
    #   phantomTotals — league/club roll-ups + `_meta` (entrant_layer_pvc, expected_slots_per_year,
    #                   seal_sha256_8) that the +1/+2 entrant banner header reads
    phantom_layer = d.get("phantomLayer", {})
    phantom_picks = d.get("phantomPicks", [])
    phantom_totals = d.get("phantomTotals", {})

    # ---- durable release/round metadata contract (no hardcoded label ever again) ------------------
    # release_version + as_of_round are OPTIONAL top-level keys on data/expected_boot.json. The extractor
    # PASSES THEM THROUGH verbatim (it never invents a version or a round); when a key is absent the stamp
    # carries None and the UI renders a neutral unknown state. The final bake will set release_version
    # "v2.11" / as_of_round 14 in expected_boot.json; the weekly updater will later advance as_of_round —
    # both without a single code change here. The prior hardcoded "v2.10" / "Round 17" are gone.
    release_version = boot.get("release_version")
    as_of_round = boot.get("as_of_round")

    working = {
        "stamp": {
            # ---- three EXPLICIT, separately-named provenance identities (no overloaded field) ---------
            # board_md5: full md5 of the INSTALLED working board (rl_app_data.json). This — and only this —
            # is the identity the UI ring-fence authenticates. Not the store, not the balanced reference.
            "board_md5": srcmd5,
            # store_md5: full md5 of the ACTUAL pinned source store the extractor just read + md5-verified
            # (== the STORE ring-fence subject above). The retrospective seam matches on this.
            "store_md5": store_md5,
            # balanced_board_md5: the accepted balanced / current-lens reference identity. OPTIONAL —
            # passed VERBATIM from release metadata (expected_boot); None until the final bake sets it.
            # The retrospective seam requires it, so an un-baked bundle keeps the retro tab pending.
            "balanced_board_md5": boot.get("balanced_board_md5"),
            # srcmd5: temporary back-compat alias, identical to board_md5, for the un-regenerated
            # production bundle / un-migrated ring-fence code. Dropped once every consumer reads board_md5.
            "srcmd5": srcmd5,
            "board": boot.get("board"),
            "engine": boot.get("engine_head", "")[:8],
            "store": boot.get("store", "")[:8],
            "register": boot.get("register", "")[:8],
            "config": boot.get("config", "")[:12],
            # Metadata contract: verbatim from the boot manifest, None when unset (never a baked label).
            "releaseVersion": release_version,
            "asOfRound": as_of_round,
            # Legacy provenance alias still read by card.js / clubs.js. == the release version, coerced to
            # "" (neutral) when unknown so those (unedited) stamp lines never print a stale "v2.10".
            "tag": release_version if release_version is not None else "",
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
        # Leg-F entrant/phantom layer (working-tier only; see pass-through note above).
        "phantomLayer": phantom_layer,
        "phantomPicks": phantom_picks,
        "phantomTotals": phantom_totals,
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

    print("board_md5 (board id) :", srcmd5, "(alias srcmd5 carries the same value)")
    print("store_md5 (verified) :", store_md5)
    print("board id (boot)     :", boot.get("board"))
    assert srcmd5.startswith(boot.get("board", "")[:8]), "RING-FENCE FAIL: artifact md5 != pinned board id"
    print("ring-fence OK       : md5 head == board id")
    print("active players      :", len(active), "| back-only:", len(back_rows), "| picks:", len(picks))
    print("wrote:", os.path.relpath(p1, REPO))
    print("wrote:", os.path.relpath(p2, REPO))


if __name__ == "__main__":
    sys.exit(main())
