"""ORDER 20 — THE nd_profile LEG OF THE SEPARATION TEST.

`nd_profile` is THE CALIBRATION TARGET: every pathway's lambda is `profile_X / profile_ND1-64`
(phase1_derive.py header). The separation law names it explicitly — a pool change may not move it BY
ANY AMOUNT.

    profile_X = SUM_X structural_value / SUM_X v0        (the ruled D3 measure)

This file measures it under BOTH stratum constructions, on BOTH the base matrix and every perturbed
matrix, and asserts:

    CONTAMINATED (S[(pos,t)])      : the drift is REPORTED, whatever it is.
    ARM-SPLIT    (S[(arm,pos,t)])  : the drift must be EXACTLY 0.0 — not "< 1e-12", exactly 0.0 —
                                     for nd_profile AND for every individual national row's
                                     structural value. A non-zero residue is a BLOCKER.

CONTROL 1: with split=False this file's structural_values must reproduce the pinned
`harness_pvc_REPINNED_pass3.structural_values` VALUE-FOR-VALUE on the same input. Asserted, not
assumed — if it fails, this instrument is not measuring what it claims.

    usage:  python3 nd_profile_test.py <BASE.json> <PERTURBED.json> [<PERTURBED.json> ...]
"""
import json, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness_armsplit as A
import harness_pvc_REPINNED_pass3 as H

# ---- PIN ASSERTIONS AT ENTRY -------------------------------------------------------------------
ROOT = os.environ.get('RL_REPO', os.path.abspath(os.path.join(HERE, '../../../..')))
PINS = {'board  data/rl_build/rl_app_data.json': (ROOT + '/data/rl_build/rl_app_data.json',
                                                  '94f1fec59f99c59d5890d5975c79fa9b'),
        'store  engine/rl_after/rl_model_data.json': (ROOT + '/engine/rl_after/rl_model_data.json',
                                                      'd9a24282357cf3083b1640466e3ecd83'),
        'instr  noarb_table_338.py': (ROOT + '/docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                                      '0f8220351c64c56ccfa90c60edcdfa5f')}


def assert_pins(where):
    for name, (path, want) in PINS.items():
        got = hashlib.md5(open(path, 'rb').read()).hexdigest()
        assert got == want, "PIN MOVED at %s: %s = %s, expected %s" % (where, name, got, want)
    print("  pins asserted at %s: board 94f1fec5 / store d9a24282 / instrument 0f822035 — all UNMOVED" % where)


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def load(path):
    M = json.load(open(path))
    R = M['recs']
    return M, [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]


def nd_rows(elig):
    """THE NATIONAL TEACHING POPULATION, on the ENGINE's own arm classification (see harness_armsplit.arm_of).
    Under the published (slide-derived) `teaches_curve` this set additionally contains daniel-butler,
    who the engine prices as pool. Both readings are computed so the difference is visible, never buried."""
    engine = [r for r in elig if not r['is_pool_engine'] and r.get('type') == 'ND'
              and r.get('raw_pick') and 1 <= r['raw_pick'] <= 64]
    published = [r for r in elig if r.get('teaches_curve')]
    return engine, published


def profile(sub, SV):
    d = sum(float(r['v0']) for r in sub)
    return (sum(SV[r['key']]['value'] for r in sub) / d) if d else float('nan')


def measure(path, split):
    M, elig = load(path)
    rows, prov = A.structural_values(elig, split=split)
    SV = {r['key']: row for r, row in zip(elig, rows)}
    eng, pub = nd_rows(elig)
    return {'nd_profile_engine_arm': profile(eng, SV),
            'nd_profile_published_teaches_curve': profile(pub, SV),
            'n_engine': len(eng), 'n_published': len(pub),
            'per_row': {r['key']: SV[r['key']]['value'] for r in eng},
            'prov': prov, 'store_md5': M['meta'].get('store_md5'),
            'engine_head': M['meta'].get('engine_head')}


P = print
BASE = sys.argv[1]; VARS = sys.argv[2:]
assert_pins('entry')

# ---- CONTROL 1: split=False == the pinned harness, value for value ------------------------------
_M, _elig = load(BASE)
_pin_rows, _pin_prov = H.structural_values(_elig)
_our_rows, _our_prov = A.structural_values(_elig, split=False)
_bad = [(a['key'], a['value'], b['value']) for a, b in zip(_pin_rows, _our_rows) if a['value'] != b['value']]
assert not _bad, "CONTROL 1 FAILED — split=False does not reproduce the pinned harness on %d rows: %s" % (
    len(_bad), _bad[:4])
P("  CONTROL 1 PASS: split=False reproduces harness_pvc_REPINNED_pass3.structural_values on all %d "
  "eligible rows, value for value (0 differences). The instrument measures the SPLIT and nothing else."
  % len(_elig))
P()

RES = {'base': BASE, 'variants': {}}
b_con = measure(BASE, split=False)
b_spl = measure(BASE, split=True)
RES['base_contaminated'] = {k: v for k, v in b_con.items() if k != 'per_row'}
RES['base_armsplit'] = {k: v for k, v in b_spl.items() if k != 'per_row'}

P("=" * 116)
P("nd_profile ON THE BASE MATRIX   %s" % os.path.basename(BASE))
P("=" * 116)
P("  construction          nd_profile (engine arm, n=%d)   nd_profile (published teaches_curve, n=%d)"
  % (b_con['n_engine'], b_con['n_published']))
for tag, d in (('CONTAMINATED S[(pos,t)]', b_con), ('ARM-SPLIT   S[(arm,pos,t)]', b_spl)):
    P("  %-26s %-32.10f %.10f" % (tag, d['nd_profile_engine_arm'], d['nd_profile_published_teaches_curve']))
P()
P("  ONE-TIME DE-CONTAMINATION DELTA on nd_profile (this is a CONSEQUENCE of the fix, not a law breach):")
for k in ('nd_profile_engine_arm', 'nd_profile_published_teaches_curve'):
    x, y = b_con[k], b_spl[k]
    P("    %-38s %.10f -> %.10f   delta %+.10f  (%+.4f%%)" % (k, x, y, y - x, 100.0 * (y - x) / x))
_mv = [(k, b_con['per_row'][k], b_spl['per_row'][k]) for k in b_con['per_row']
       if b_con['per_row'][k] != b_spl['per_row'][k]]
P("    national rows whose structural value moves under the split: %d of %d" % (len(_mv), b_con['n_engine']))
P("    completion provenance  contaminated %s" % b_con['prov']['counts'])
P("                           arm-split    %s" % b_spl['prov']['counts'])
P("    fallback share         contaminated %.3f%%   arm-split %.3f%%"
  % (b_con['prov']['fallback_share_pct'], b_spl['prov']['fallback_share_pct']))
RES['decontamination_delta'] = {
    k: {'contaminated': b_con[k], 'armsplit': b_spl[k], 'delta': b_spl[k] - b_con[k],
        'pct': 100.0 * (b_spl[k] - b_con[k]) / b_con[k]}
    for k in ('nd_profile_engine_arm', 'nd_profile_published_teaches_curve')}
RES['decontamination_row_movers'] = len(_mv)

# ---- THE LAW: a pool perturbation must move nd_profile by EXACTLY ZERO --------------------------
P()
P("=" * 116)
P("THE SEPARATION LAW ON nd_profile — pool perturbations")
P("=" * 116)
FAIL = 0
for V in VARS:
    lab = os.path.basename(V)
    v_con = measure(V, split=False); v_spl = measure(V, split=True)
    d_con = v_con['nd_profile_engine_arm'] - b_con['nd_profile_engine_arm']
    d_spl = v_spl['nd_profile_engine_arm'] - b_spl['nd_profile_engine_arm']
    dp_con = v_con['nd_profile_published_teaches_curve'] - b_con['nd_profile_published_teaches_curve']
    dp_spl = v_spl['nd_profile_published_teaches_curve'] - b_spl['nd_profile_published_teaches_curve']
    rmv_con = sum(1 for k in b_con['per_row'] if b_con['per_row'][k] != v_con['per_row'].get(k))
    rmv_spl = sum(1 for k in b_spl['per_row'] if b_spl['per_row'][k] != v_spl['per_row'].get(k))
    ok = (d_spl == 0.0 and dp_spl == 0.0 and rmv_spl == 0)
    FAIL |= (not ok)
    P("  %-28s CONTAMINATED delta %+.10f (%+.4f%%)  national rows moved %d"
      % (lab, d_con, 100.0 * d_con / b_con['nd_profile_engine_arm'], rmv_con))
    P("  %-28s   published-teaches_curve delta %+.10f (%+.4f%%)" % ('', dp_con,
      100.0 * dp_con / b_con['nd_profile_published_teaches_curve']))
    P("  %-28s ARM-SPLIT    delta %+.10f                national rows moved %d   -> %s"
      % ('', d_spl, rmv_spl, 'EXACTLY ZERO — LAW HOLDS' if ok else '*** NON-ZERO RESIDUE — BLOCKER ***'))
    RES['variants'][lab] = {'contaminated_delta': d_con, 'contaminated_pct': 100.0 * d_con / b_con['nd_profile_engine_arm'],
                            'contaminated_published_delta': dp_con,
                            'contaminated_rows_moved': rmv_con,
                            'armsplit_delta': d_spl, 'armsplit_published_delta': dp_spl,
                            'armsplit_rows_moved': rmv_spl, 'law_holds': bool(ok)}
    P()

assert_pins('exit')
RES['verdict'] = 'LAW HOLDS UNDER ARM-SPLIT' if not FAIL else 'BLOCKER — NON-ZERO RESIDUE'
P("  VERDICT: %s" % RES['verdict'])
json.dump(RES, open(os.path.join(HERE, 'ND_PROFILE_TEST.json'), 'w'), indent=1, default=float)
sys.exit(0 if not FAIL else 2)
