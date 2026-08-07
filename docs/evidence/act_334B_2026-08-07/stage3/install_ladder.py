"""Install the settled stage-3 ladder + the re-based numeraire into pvc_curve_v2.json.

Writes to every path given on argv.  Changes exactly six fields; adds no key, removes no key:
    curve            the 64 settled values
    curve_md5        the in-file pin, re-stamped to the settled payload
    numeraire        pooled_head_pre_scale (x g), s (/ g), _doc  -- published_pin UNCHANGED at 3000
    derived_from     re-pointed to the stage-3 basis
    source           re-pointed to the stage-3 machinery
    _working_substrate_note   the reversal condition, restated
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'settled_ladder.json')))
lad = S['ladder']; N = S['numeraire']; g = S['g']
payload8 = S['payload'][:8]
assert lad[0] == 3000 and len(lad) == 64

NOTE = (
 "#334 STAGE B / STAGE 3 (branch landing/334-stage-b, 2026-08-07). THE BASE CURVE WAS RE-TAUGHT ERA-FREE "
 "and the stage-2 era-free per-pick re-anchor f(p) applied on top, then the whole result re-based to the "
 "numeraire anchor by the ONE global drift factor g = f(1) = 1.121405224905 -- the exporter's own standing "
 "instruction, verbatim: 're-base the CURRENCY to the anchor (L7 / the scale drift), never the anchor to the "
 "drift'. curve(p) = round(base_erafree(p) * f(p) / g), so curve(1) = 3000 EXACTLY and the taught relative "
 "shape across picks is carried unchanged. The SAME g re-bases the numeraire block (pooled_head_pre_scale x g, "
 "s / g), which is the E6 two-sided law in rl_model._load_numeraire: one measured head, one factor, both sides. "
 "SUPERSEDES the #328 re-closure ladder df766dff and the stage-2 teaching ladder 77408ecd. THE #328 REVERSAL "
 "CONDITION IS TRIPPED BY CONSTRUCTION -- this pass moves picks by far more than one board point -- so adoption "
 "re-opens and remains the owner's separate click; nothing here is promoted to main. pool_value and the N43 "
 "signed pool_levels are UNTOUCHED owner data.")

DERIVED = (
 "docs/evidence/act_334B_2026-08-07/stage2_erafree/per_entrant_338_erafree.json (matrix md5 "
 "e4b38436d3890e05c671a0170fde5dfc, store 37ced3ce, engine head a0a20d6e, v0surf signature af556bdca53d) -- "
 "the ERA-FREE walk-forward matrix on the #338 minimum-tenure basis carrying the #336 reference layer. The "
 "per-pick re-anchor f(p) is read from docs/evidence/act_334B_2026-08-07/stage2_erafree/per_pick_reanchor.json "
 "(Gaussian kernel h=8.0 on the pick axis, busts at 0 in every denominator, teaching target 1.40 which lives "
 "in that derivation script alone and in no runtime path).")

SOURCE = (
 "docs/evidence/act_334B_2026-08-07/stage3/base_reteach.py -- the BASE-CURVE RE-TEACH, era-free. Machinery of "
 "record session_2026-07-30/item279/panel/harness_pvc.py (re-pinned copy harness_pvc_REPINNED_pass3.py): "
 "structural_values() under the ruled basis (VOR, structural completion, class cut 2022, QUAL_GAMES 6, "
 "never-established teaching 0.0 and staying in the denominator) -> kernel_raw() (the SHIPPED #271 fit_year0 "
 "kernel verbatim, nmin=35, h 0.10-0.60 over log pick) -> pin_and_check() (#271 monotone_strict verbatim: PAVA "
 "non-increasing, HARD SET fit[0]=3000, strict descent). That hard-set pin is the SAME currency convention the "
 "superseded derive_271.py ladder shipped in, so the base maps into this file's ladder currency by the identity. "
 "settle_ladder.py then applies f(p) and the single re-base by g. Method held constant; every difference is the "
 "data, the era removal, or the re-anchor.")

NUMDOC = (
 "#279 ruled pooled numeraire, RE-BASED at #334 stage B stage 3 (2026-08-07). THE MEASURED HEAD IS PRIMITIVE "
 "(seam ruling 2026-07-31): pooled_head_pre_scale is the lane-measured head and s is DERIVED from it at full "
 "precision; E6 coherence (published_pin / pooled_head_pre_scale == s to 1e-9) holds BY CONSTRUCTION and is "
 "exact here (difference 0.0). THE STAGE-3 ARITHMETIC, in full: the re-anchor lifts the taught head by "
 "g = f(1) = 1.121405224905, so the head re-measures at 3017.9232 x g = %.10f and s re-bases at "
 "0.9940610814748366 / g = %.16f (= 3000 / the new head, identically). published_pin is UNMOVED at 3000 -- the "
 "anchor never moves, the currency does. Both sides of the economy take the same g: the ladder was divided by it "
 "and s was divided by it, so BOARD_FACTOR = (RL_PICK1 / PVC_v34[1]) * s carries the identical re-base to the "
 "player side and the pick-vs-player relativity moves by exactly f(p) -- which IS the re-anchor. Prior values: "
 "head 3017.9232, s 0.9940610814748366 (re-measured at the #328 re-closure on surface e4215093; before that "
 "3060.621)." % (N['H_new'], N['s_new']))


def install(path):
    d = json.load(open(path))
    d['curve'] = {str(i + 1): int(lad[i]) for i in range(64)}
    d['curve_md5'] = payload8
    d['numeraire']['pooled_head_pre_scale'] = N['H_new']
    d['numeraire']['s'] = N['s_new']
    d['numeraire']['published_pin'] = N['published_pin']
    d['numeraire']['_doc'] = NUMDOC
    d['derived_from'] = DERIVED
    d['source'] = SOURCE
    d['_working_substrate_note'] = NOTE
    assert d['pin'] == 3000 and d['numeraire_pin1_3000'] is True
    with open(path, 'w') as fh:
        json.dump(d, fh, indent=1, sort_keys=True)
        fh.write('\n')
    body = json.dumps({str(k): int(d['curve'][str(k)]) for k in range(1, 65)}, sort_keys=True).encode()
    print('%-70s payload %s  file %s'
          % (path, hashlib.md5(body).hexdigest(), hashlib.md5(open(path, 'rb').read()).hexdigest()))


for p in sys.argv[1:]:
    install(p)
