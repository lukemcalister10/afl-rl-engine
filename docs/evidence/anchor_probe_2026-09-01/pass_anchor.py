"""THE ANCHOR PROBE — is the player/pick exchange rate double-applying the numeraire? READ ONLY.

WHY THIS IS THE RIGHT TEST. value() blends TWO legs that are quoted in DIFFERENT currencies:

    pedigree   unpl_eq = _PVC2M[ep] * decu * debut_factor      rl_model.py:1941
               -> reads the ADOPTED PICK CURVE directly: PUBLISHED pick money, pick 1 = 3000.
    production prod_v  = val(player_raw(p))                    rl_model.py:1949
               -> val = round(SCALE * r**GAMMA): SCALE money.

They are added together, so SCALE must be calibrated to put the production leg in pick money. That
calibration is the whole job of

    BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s ; SCALE = SCALE * BOARD_FACTOR    rl_model.py:1574

and PVC[1] is pick 1 measured IN PLAYER MONEY — build_pvc_v34 anchors its top band to build_pvc,
which is _ce() over peakval(), and peakval is itself val(), i.e. SCALE money. So (RL_PICK1/PVC[1])
alone already converts player money to published pick money. The open question is what the extra
`* s` is doing, and whether it leaves the production leg ~6% short of the pedigree leg.

THE MEASUREMENT, and it needs no counterfactual build. The engine can price a pick TWICE:

    A)  val(pick_raw(k))   the expected baseline draftee at pick k, through the PRODUCTION leg's
                           own currency (rl_model.py:1372-1382 — the same val() prod_v uses)
    B)  _PVC2M[k]          the same pick, in PUBLISHED pick money, off the adopted artifact

Same object, two currencies, on one loaded engine. If the exchange rate is right, A/B is 1 (up to
the modelling difference between a baseline draftee and the curve's own level). If the `* s` is a
double application, A/B should sit near s = 0.9401 — i.e. the production leg systematically ~6%
light against the pedigree leg it is added to.

A ratio near 1.0 clears the construction and the suspicion is withdrawn.
A ratio near 0.94 is the double count, and it is worth what it costs to fix.

READ ONLY: prices nothing into any file, mutates no engine state, writes one JSON verdict.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def run(ns):
    G, MA = ns['G'], ns['MA']
    out = {}
    out['SCALE_post_anchor'] = float(MA.SCALE)
    out['BOARD_FACTOR'] = float(MA.BOARD_FACTOR)
    out['numeraire'] = {k: float(v) for k, v in MA._NUM.items()}
    out['GAMMA'] = float(MA.GAMMA)

    # the v3.4 pre-anchor head, recovered exactly: BOARD_FACTOR = (P1/head)*s  =>  head = P1*s/BF
    p1 = float(os.environ.get('RL_PICK1', '3000'))
    head = p1 * MA._NUM['s'] / MA.BOARD_FACTOR
    out['v34_pre_anchor_head'] = head

    # A vs B, pick by pick
    rows = []
    for k in range(1, 21):
        a = float(MA.val(MA.pick_raw(k)))          # production-leg currency
        b = float(MA._PVC2M[k])                    # published pick money
        rows.append({'pick': k, 'A_val_pick_raw': a, 'B_published_curve': b,
                     'ratio_A_over_B': (a / b) if b else None})
    out['per_pick'] = rows
    rs = [r['ratio_A_over_B'] for r in rows if r['ratio_A_over_B']]
    rs_sorted = sorted(rs)
    out['ratio_summary'] = {
        'n': len(rs), 'min': min(rs), 'max': max(rs),
        'median': rs_sorted[len(rs_sorted) // 2],
        'mean': sum(rs) / len(rs),
    }
    out['reference'] = {'s': float(MA._NUM['s']), 'one_over_s': 1.0 / float(MA._NUM['s'])}

    ns['T']('anchor: BOARD_FACTOR %.9f  v3.4 head %.1f  s %.6f'
            % (MA.BOARD_FACTOR, head, MA._NUM['s']))
    ns['T']('anchor: A/B over picks 1-20 — median %.4f  (s = %.4f, 1.0 = coherent)'
            % (out['ratio_summary']['median'], MA._NUM['s']))
    json.dump(out, open(os.path.join(HERE, 'ANCHOR_PROBE.json'), 'w'), indent=1)
    return out
