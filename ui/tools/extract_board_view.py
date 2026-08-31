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
def _entry_inputs_sig_of_store():
    """The signature of the live store's v0-determining fields — the reader's half of the one
    function shared with the generator. No engine: it reads raw JSON, which is exactly why one
    definition can serve both sides instead of a mirrored pair."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from v0_identity import entry_inputs_sig_of_store
    return entry_inputs_sig_of_store(STORE)


def join_v0(board_md5, store_md5, active_keys=()):
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
    # AUTHENTICATE ON THE INPUTS, NOT THE CALENDAR (2026-08-31).
    #
    # This used to compare the sidecar's stamped board and store md5 against the bundle's. Both move
    # on every round advance, and an entry price does not: v0 is a draft-time constant off a frozen
    # surface whose slot key depends only on (future position, draft age, pick), which the
    # generator's own docstring states. The gate therefore contradicted the invariant of the file it
    # was guarding, and the contradiction had teeth — FW1 moved the store, this refused, and all 804
    # rows published v0:null for a day. Measured across that same move: 804 of 804 entry prices were
    # byte-identical. The refusal protected nothing.
    #
    # It is replaced by two checks that are about whether this sidecar can answer for THIS board:
    #   (1) the v0-determining store fields are the ones it was cut from (v0_identity, one function
    #       shared with the generator so the writer and the reader cannot drift apart), and
    #   (2) it covers every active row — a roster addition is the one way a sidecar can be complete
    #       for its own cut and incomplete for this one.
    # Both are milliseconds. Regenerating instead would be 580 seconds, measured, on every landing.
    if not stamp.get("entryInputsSig"):
        return {}, ("The v0 sidecar predates entry-input authentication (no entryInputsSig), so it "
                    "cannot be authenticated against this store. Re-run ui/tools/gen_v0_sidecar.py.")
    want_sig = _entry_inputs_sig_of_store()
    if stamp["entryInputsSig"] != want_sig:
        return {}, ("The v0 sidecar was cut from a store whose entry-price inputs (pick / dob / "
                    "future position / type / roster) differ from this one, so no entry price is "
                    "published. Re-run ui/tools/gen_v0_sidecar.py.")
    missing = [k for k in active_keys if k not in by_key]
    if missing:
        return {}, ("The v0 sidecar does not cover %d row(s) on this board (e.g. %s), so no entry "
                    "price is published. Re-run ui/tools/gen_v0_sidecar.py."
                    % (len(missing), ", ".join(missing[:3])))
    return by_key, None


def v0_of(by_key, key):
    """One row's (entry price, origin). An unjoinable row gets (None, "unrecoverable") — the same
    explicit absent state the sidecar itself uses for a player whose entry price could not be
    recovered, which the card renders as an em-dash WITH ITS REASON. Never an invented figure."""
    rec = by_key.get(key) if by_key else None
    if not rec or rec.get("v0") is None:
        return None, "unrecoverable"
    return rec["v0"], rec.get("origin") or "unrecoverable"


#: The owner's display overrides, couriered like his other inputs (docs/inputs/). Absent file =
#: no overrides, which is the ordinary case and must never be an error.
OWNER_OVERRIDES = os.path.join("docs", "inputs", "OWNER_DISPLAY_OVERRIDES.json")


def _apply_pool_override(pvc, repo):
    """Publish the owner's ruled pool-pick figure over the board's derived one. DISPLAY ONLY.

    WHY THIS IS A PUBLISH-TIME OVERRIDE AND NOT AN EDIT TO THE NUMBER
    ----------------------------------------------------------------
    The pool level exists in two copies: `engine/rl_after/pvc_curve_v2.json` -> `pool_value` (237.2,
    which the engine loads as MA.PVC[65]) and `data/rl_build/rl_app_data.json` -> PVC["65"] (237,
    baked into the board). The owner ruled the DISPLAYED figure to 150 and, asked directly, ruled the
    derived one correct and left standing:

        "Yes, 237.2 is accurate so fine to stay, just good for the cosmetic override on the trade
         desk."   (2026-08-31)

    So the engine keeps deriving what it derives. Only what the app SHOWS moves, and it moves here,
    at the seam between the two — which is the one place that touches neither the engine artifact nor
    the board.

    THE ALTERNATIVE, AND WHY IT WAS NOT TAKEN. Editing PVC["65"] in the board changes the board md5,
    and that md5 IS the board identity — pinned in data/expected_boot.json, data/release_contract.json,
    both UI bundles and Guard 5. It is a full landing for a figure no player price reads. Worse, it
    would also have to touch the curve artifact to stay coherent, and THAT copy is the one the engine
    loads: `draftval(p) = MA.PVC[min(effpk(p), KMAX))` with KMAX 70 reads index 65 for a pool
    entrant. `pool_value` is retired from pricing (owner ruling, _merged_recover.py:3342, with a hard
    assert that every pool entrant's anchor is his own division level) so the expectation is zero
    movers — but an expectation is not a measurement, and the only way to MEASURE it is the rebuild
    this override exists to avoid. Overriding at publish time makes the question moot instead of
    answering it expensively.

    WHAT IT REACHES: `ui/data/board_view_working.js` and its public sibling, and nothing else. The
    two consumers are the trade desk's pool item (ui/app/trade.js) and the Pick value page's pool
    line (ui/app/pickvalue.js). It does not reach the club ratings: those price picks through
    ui/tools/ingest_inputs.price_pick off the CURVE ARTIFACT, and in a 16-club league rounds 1-4 are
    picks 1-64 exactly while round 5 (65-80) prices 0 before the pool value is ever consulted —
    measured on the shipped ledger, 48 of 240 picks reach past 64 and all 48 are round-5 zeroes.

    TWO DIFFERENT FAILURES, TWO DIFFERENT ANSWERS. A MALFORMED override — no owner_word, or a value
    that is not a positive number — HALTS the publish: that is a broken input, and an undocumented
    override on a served figure is indistinguishable from a bug. A board that does not derive the
    figure the ruling superseded is NOT a broken input; it is a different board, and the extractor
    must be able to publish any board. That case SKIPS and says so in the stamp. A missing file is
    neither — it is the ordinary case, and it is silent.
    """
    path = os.path.join(repo, OWNER_OVERRIDES)
    if not os.path.exists(path):
        return pvc, None
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    entry = doc.get("pool_pick_value")
    if entry is None:
        return pvc, None

    # A BOARD WITH NO CURVE IS NOT A BROKEN INPUT EITHER — it is a board with no curve, and the
    # extractor publishes it. (The synthetic movement board in ui/tests/extract_seam.test.py is
    # exactly that, and the first cut of this halted on it too.) Nothing is invented; the override
    # is declared unapplied, with its reason, and the bundle ships without a pool index.
    pool_key = str(max(int(k) for k in pvc)) if pvc else None
    if pool_key is None:
        return pvc, {"index": None, "applied": False, "value": entry.get("value"), "derived": None,
                     "date": entry.get("date"), "authority": entry.get("authority"),
                     "owner_word": entry.get("owner_word"),
                     "source": OWNER_OVERRIDES.replace(os.sep, "/"),
                     "why_skipped": "this board publishes no pick-value curve, so there is no pool "
                                    "index to override — nothing is invented in its place"}
    derived = pvc.get(pool_key)
    value = entry.get("value")
    if not isinstance(value, (int, float)) or value <= 0:
        raise SystemExit("HALT: the owner pool override's value is %r, which is not a positive "
                         "number." % (value,))
    if not entry.get("owner_word"):
        raise SystemExit("HALT: the owner pool override carries no owner_word. An override on a "
                         "served figure must say whose it is and in whose words; an undocumented "
                         "one cannot be told apart from a defect.")
    # THE SUPERSEDED FIGURE IS ASSERTED, AND A MISMATCH SKIPS RATHER THAN HALTS.
    #
    # An owner display ruling is about a SPECIFIC NUMBER he was shown — here, "the pool reads 237
    # and pick 64 reads 177, that can't be right". If the board no longer derives that number, the
    # ruling was made about something that no longer exists and applying it would be putting his
    # name to a decision he did not take.
    #
    # THE FIRST CUT OF THIS RAISED. It halted the publish, and it was wrong within the hour:
    # ui/tests/extract_seam.test.py runs this extractor against a schema FIXTURE whose pool index is
    # 463, and the whole seam proof died on an owner ruling that had nothing to do with that board.
    # The extractor must be able to publish ANY board — that is what it is for.
    #
    # But the two obvious repairs are both worse. Applying it anyway puts 150 on a board that never
    # derived 237. Skipping it quietly is the failure this whole session has been closing: a thing
    # that stops working and says nothing. So it SKIPS AND DECLARES — the bundle carries the
    # override with `applied: false` and the reason, the published figure is the board's own, and
    # ui/tests/release_seam.test.js asserts that exact pairing. A skip is visible in the artifact
    # that skipped it.
    #
    # Deliberately NOT pinned to a board md5: that would drop the override at the next landing, on a
    # board that still derives 237, which is the "goes dark on a landing" defect this estate has now
    # been bitten by three times. It is pinned to the NUMBER, which is what he actually ruled about.
    claimed = entry.get("supersedes_derived")
    if claimed is not None and derived is not None and float(claimed) != float(derived):
        return pvc, {"index": pool_key, "applied": False, "value": value, "derived": derived,
                     "date": entry.get("date"), "authority": entry.get("authority"),
                     "owner_word": entry.get("owner_word"),
                     "source": OWNER_OVERRIDES.replace(os.sep, "/"),
                     "why_skipped": "the override supersedes %s but this board derives %s — the "
                                    "ruling was made about a figure this board does not carry, so "
                                    "it is NOT applied and the derived figure is published"
                                    % (claimed, derived)}

    out = dict(pvc)
    out[pool_key] = value
    return out, {"index": pool_key, "applied": True, "value": value, "derived": derived,
                 "date": entry.get("date"), "authority": entry.get("authority"),
                 "owner_word": entry.get("owner_word"),
                 "source": OWNER_OVERRIDES.replace(os.sep, "/")}


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

    # the active keys are passed so the join can prove COVERAGE — a sidecar can be complete for the
    # roster it was cut on and incomplete for this one, which is the one staleness that still matters
    v0_by_key, v0_note = join_v0(srcmd5, store_md5, [p.get("key") for p in active])

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
    pvc, pool_override = _apply_pool_override(pvc, REPO)
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
            # THE OWNER'S DISPLAY OVERRIDE, DECLARED IN THE BUNDLE ITSELF (None when there is none).
            # A published figure that differs from what the engine derived must SAY SO where the
            # figure is served, not only in a document nobody loads with the app.
            "pvcPoolOverride": pool_override,
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
