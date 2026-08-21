#!/usr/bin/env python3
"""Read-only board-view extractor for the Matchday UI (TIER 3; never bakes).

Reads the derived board artifact and the pinned boot identity STRICTLY READ-ONLY and emits two
tiered, stamped view files as `window.__…__ = {…}` script bundles (so the app renders from file://
and when served). This script NEVER writes outside ui/ and NEVER recomputes a value — it trims and
tiers the fields the LOCK/DESIGN_DIRECTION call for. The two-tier UI law made real at the data layer:
the public bundle is leak-proof by construction (no keys, no md5/guard stamps, no mech, no owner-rule).

ONE JOIN RIDES THAT LAW RATHER THAN BENDING IT: the v0 ENTRY PRICE (owner's word, 2026-08-21). The
sidecar is keyed and the public row is not, so the join is done HERE — where the keys legitimately
exist — and only the ANSWER is emitted (`v0` + `v0_origin` per row). No identifier is added to the
public bundle to make it possible. See join_v0() for the mirror-law check that gates it.

Board-id ring-fence: md5(rl_app_data.json) == the board id pinned in data/expected_boot.json (read at
run time, never a hex literal here). The emitted working bundle carries that md5 as `stamp.board_md5`
(alias `stamp.srcmd5`); the app fail-closes if it disagrees with the expected board.
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
# The v0 ENTRY-PRICE sidecar (ui/tools/gen_v0_sidecar.py). Read STRICTLY READ-ONLY, and joined to the
# PUBLIC rows here — see join_v0() below for why the join has to happen at generation time and not in
# the browser. Deliberately NOT env-overridable: the other four paths are redirected so a fixture run
# can build a self-consistent temp board, and a fixture board is exactly the case where this sidecar
# must NOT be honoured (its stamped identity will not be the fixture's). A fixture run therefore takes
# the refusal path, which is the correct behaviour rather than a gap in the fixture.
V0_SIDECAR = os.path.join(HERE, "..", "data_aux", "v0.js")


def norm_club(name):
    """Display normalisation for a club string (casing only; the store carries 'Free agents'
    and 'Free Agents' as two spellings of one AFFL bucket). Never invents a club."""
    if not name:
        return None
    s = str(name).strip()
    return "Free Agents" if s.lower() == "free agents" else s

# Position label map (engine codes -> owner-voice display; names/values first, jargon in brackets).
POS = {
    "MID": "Mid", "RUCK": "Ruck", "KPF": "Key Fwd", "SF": "Fwd",
    "KPD": "Key Def", "SD": "Def",
}


def label_pos(code):
    return POS.get(code, (code or "").replace("_", " ").title() or "—")


# ---- v0, THE ENTRY PRICE, ON THE PUBLIC TIER (owner's word, 2026-08-21: "v0 goes on the public board") -
# THE JOIN HAPPENS HERE, AT GENERATION TIME, AND IT CANNOT HAPPEN ANYWHERE ELSE.
# The v0 sidecar is KEYED (`byKey[player key] -> {v0, origin}`) and the public bundle carries NO player
# key — that keylessness is the two-tier law made structural, and it is the reason the public bundle is
# leak-proof by construction rather than by care. So a browser holding only the public bundle has
# nothing to join on, and the only two ways to give the public tier this fact would be (a) put a key on
# the public row, which dismantles the law for one display field, or (b) join here, in the one place
# where the keys legitimately exist, and emit the ANSWER rather than the identifier. (b) is what this
# does: two flat display fields per row, `v0` and `v0_origin`, and no new identifier of any kind.
#
# THE MIRROR LAW APPLIES TO THE JOIN ITSELF (ui/app/ownership.js:25). The sidecar names the board and
# store it was generated from; if either disagrees with the board/store THIS bundle is being generated
# from, the whole join is REFUSED and every row gets the honest absent state. A v0 is a draft-time
# constant, so it goes stale slowly — which makes a stale one more likely to be trusted while wrong,
# not less. Fail closed.
#
# THE REFUSAL REASON CARRIES NO IDENTITY. The detail (which md5 disagreed with which) is printed by
# this generator to the operator's terminal; what rides the public bundle is the state in words. The
# public bundle carries no provenance identity today and this feature does not become the exception.
def join_v0(board_md5, store_md5):
    """-> (by_key, note). `by_key` empty == refused; `note` is the reason, in identity-free words."""
    if not os.path.exists(V0_SIDECAR):
        return {}, "The v0 sidecar was not present when this bundle was generated."
    try:
        text = open(V0_SIDECAR).read()
        bundle = json.loads(text[text.index("window.__V0__"):].split("=", 1)[1].strip().rstrip(";\n").rstrip(";"))
        by_key = bundle["byKey"]
        stamp = bundle.get("stamp") or {}
    except Exception as exc:                                          # noqa: BLE001 - reported, never silent
        return {}, "The v0 sidecar could not be read (%s), so no entry price is published." % type(exc).__name__
    if not stamp.get("board") or not stamp.get("store"):
        return {}, "The v0 sidecar names no board/store identity, so it cannot be authenticated."
    if stamp["board"] != board_md5 or stamp["store"] != store_md5:
        return {}, ("The v0 sidecar was generated from a different board/store identity than this "
                    "bundle, so no entry price is published.")
    return by_key, None


def v0_of(by_key, key):
    """One row's (entry price, origin). An unjoinable row gets (None, "unrecoverable") — the same
    explicit absent state the sidecar itself uses for a player whose entry price could not be
    recovered, which the card renders as an em-dash WITH ITS REASON. Never an invented figure."""
    rec = by_key.get(key) if by_key else None
    if not rec or rec.get("v0") is None:
        return None, "unrecoverable"
    return rec["v0"], rec.get("origin") or "unrecoverable"


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
    # ---- #274 item 2: the ELIGIBILITIES column, carried through as a display/selection field --------
    # The Best-23 law (#271 Addendum 19) selects on the store's ELIGIBILITIES column, with DPP players
    # assignable to either eligible slot. The board (rl_app_data.json) carries only `grp` — the
    # modelling/trajectory axis, one code per player — which cannot see DPP at all; that blindness is
    # what produced the measured axis artifacts (Adelaide 3 MID-grouped against 5 slots with ten
    # dual-eligible covers; Hawthorn 4 with six). So the column rides here, from the SAME read-only
    # md5-verified store this function already opens for affl_team, and by the same doctrine: a display
    # field, joined by key, that no valuation path reads.
    #
    # Emitted as a LIST of canonical slot codes, in the store's own order (the primary first), so the
    # bundle carries the eligibility set rather than a string a consumer would have to re-split.
    # Measured at the adopted store 6b9d00a7: 804 of 804 board players carry a non-empty column, every
    # token is one of the six canonical slot codes (zero strays), lists are length 1 (618) or 2 (186 —
    # the DPP players), and EVERY player's board posCode appears among his own eligibilities, so the
    # eligibility set is a superset of the modelling axis and can never select a worse 23 than `grp`.
    elig_by_key = {}
    for r in json.loads(store_raw):
        k = r.get("key")
        if k:
            affl_by_key[k] = norm_club(r.get("affl_team"))
            elig_by_key[k] = [t.strip() for t in str(r.get("eligibilities") or "").split(",") if t.strip()]

    def row_working(p):
        # Full field set for the owner's working aid (identity-bearing).
        return {
            "key": p.get("key"),
            "name": p.get("name"),
            "pos": label_pos(p.get("grp") or p.get("gf")),
            "posCode": p.get("grp") or p.get("gf"),
            # #274 item 2: the owner-maintained ELIGIBILITIES set (canonical slot codes). `posCode` above
            # stays exactly what it was — the modelling axis — and keeps every use it already had; this is
            # the SLOT-LEGALITY axis the Best-23 selector reads, and the two are deliberately separate.
            "elig": elig_by_key.get(p.get("key")) or [],
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

    v0_by_key, v0_note = join_v0(srcmd5, store_md5)

    def row_public(p):
        # Sanitised: no key/slug, no ids, no owner-rule machinery, no pathway/mech. Value + movement only.
        v0v, v0o = v0_of(v0_by_key, p.get("key"))
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
            # THE ENTRY PRICE, joined from the keyed sidecar above (owner's word 2026-08-21). `v0` is the
            # figure and `v0_origin` is WHICH entry price it is — "pick-slot" (the frozen year-zero pick
            # surface, shared by every same-(future position, draft age, pick) player), "entry-anchor" (a
            # pool entrant's signed division level), or "unrecoverable" (no entry price could be joined:
            # v0 is null and the card prints an em-dash carrying the reason). The gap and the ratio the
            # card shows are arithmetic on this figure and the row's own `v`; neither is precomputed here,
            # because neither is a fact the extractor may invent. NO IDENTIFIER RIDES WITH THEM.
            "v0": v0v,
            "v0_origin": v0o,
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
    # final integration 2026-07-21: the owner-facing visible future-draft asset ladder reconciliation summary
    # (draftAssetTotals: visible 2027/2028 Draft Pick 1-64 at PVC + labelled residual aggregates, reconciled
    # to the sealed F5 entrant layer 77611, adopted). Working-tier ONLY; passed through verbatim (extractor recomputes
    # nothing). The visible pick rows themselves ride lensPicks (kind/asset "pick").
    draft_asset_totals = d.get("draftAssetTotals", {})

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
        "draftAssetTotals": draft_asset_totals,
    }

    # The public tier says, in its own stamp, whether the entry price it carries is real — counted over
    # the rows actually emitted, not over the sidecar's own claim. A reader (or a test) can therefore
    # tell "no player on this board has a recoverable entry price" from "the sidecar did not
    # authenticate" without either being inferred from a screen full of em-dashes. No identity here.
    n_priced = sum(1 for r in public_rows if r.get("v0") is not None)
    public = {
        "stamp": {
            "baseYear": d.get("BASE_YEAR"),
            "nPlayers": len(active),
            "maxV": max_v,
            "v0": {
                "joined": bool(v0_by_key) and v0_note is None,
                "why": v0_note,
                "generator": "ui/tools/gen_v0_sidecar.py",
                "nPriced": n_priced,
                "nAbsent": len(public_rows) - n_priced,
            },
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
    if v0_note is None:
        print("v0 join (public)    : JOINED %d of %d rows priced, %d absent | sidecar board %s store %s"
              % (n_priced, len(public_rows), len(public_rows) - n_priced, srcmd5[:8], store_md5[:8]))
    else:
        # The operator gets the identity detail; the bundle gets the state in words. Never a hard fail:
        # the board itself is unaffected and must still ship — the entry price is what is withheld.
        print("v0 join (public)    : REFUSED —", v0_note)
    print("wrote:", os.path.relpath(p1, REPO))
    print("wrote:", os.path.relpath(p2, REPO))


if __name__ == "__main__":
    sys.exit(main())
