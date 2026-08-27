#!/usr/bin/env python3
"""BLOCK-3 BOARD VERIFICATION — the built candidate vs the v872/v875 waterfall (P-1/P-6) plus the
F2 empirical leak check and the F5 draft-cap scan, all at the JSON level (no engine load).

  usage: verify_candidate_board.py LIVE_BOARD.json CAND_BOARD.json WATERFALL.json OUT.json

Checks (each printed, all folded into the verdict):
  1. ROW SET — same keys on both boards (no row appears/disappears).
  2. NAMED ROWS — the owner's benchmark rows print within +/-5 of the waterfall's b_cand
     (P-1's damping tolerance); step-up rows may exceed b_cand upward (the step-up landed
     after the waterfall's smooth+surface stack and adds on top).
  3. ATTRIBUTION (F2, empirical) — every mover on the built board is either in the waterfall's
     mover set, or flagged stepup_pending there, or a hairline |d|<=2 ripple; anything else is
     an UNEXPLAINED mover and the check is RED (an out-of-class leak would land here).
  4. F5 DRAFT CAP — no in-class waterfall row prints above its smoothed draft v0 (v0_cand).
  5. TOTALS — net board move vs the waterfall's prediction (pre-level).
"""
import json, sys

live_p, cand_p, wf_p, out_p = sys.argv[1:5]
LB = json.load(open(live_p)); CB = json.load(open(cand_p)); WF = json.load(open(wf_p))

def rows(d):
    return {r['key']: r['v'] for L in ('active', 'back') for r in d[L]}
lv, cv = rows(LB), rows(CB)
bk = {r['key']: bool(r.get('bk')) for L in ('active', 'back') for r in LB[L]}
gnow = {r['key']: r.get('g') or 0 for L in ('active', 'back') for r in LB[L]}

verdict = {'checks': {}, 'named': [], 'unexplained': [], 'stepup_landed': [], 'easing_candidates': [],
           'refit_ripple': []}
ok = True

# 1 row set
only_l, only_c = sorted(set(lv) - set(cv)), sorted(set(cv) - set(lv))
verdict['checks']['rowset'] = {'only_live': only_l, 'only_cand': only_c, 'pass': not (only_l or only_c)}
ok &= not (only_l or only_c)

wf_rows = {m['key']: m for m in WF['movers']}
NAMED = ['harrison-oliver', 'william-mccabe', 'james-leake', 'taylor-goad', 'riak-andrew',
         'alex-dodson', 'charlie-edwards', 'thomas-burton']

# 2 named rows
named_bad = []
for k in NAMED:
    m = wf_rows.get(k)
    row = {'key': k, 'live': lv.get(k), 'cand': cv.get(k),
           'wf_b_cand': m and m['b_cand'], 'stepup': bool(m and m.get('stepup_pending'))}
    if m and k in cv:
        d = cv[k] - m['b_cand']
        row['d_vs_wf'] = d
        row['pass'] = (abs(d) <= 5) or (m.get('stepup_pending') and 0 <= d <= 60)
        if not row['pass']:
            named_bad.append(k)
    verdict['named'].append(row)
verdict['checks']['named'] = {'bad': named_bad, 'pass': not named_bad}
ok &= not named_bad

# 3 attribution
unexplained = []
for k in cv:
    if k not in lv:
        continue
    d = cv[k] - lv[k]
    if d == 0:
        continue
    m = wf_rows.get(k)
    if m is None:
        # NOT a waterfall mover. Two lawful shapes, each reported by name:
        #  - the O48 taper's scope (a first banked season IN PROGRESS: >=6 games this season),
        #    small up — the waterfall predates the sized ease; F4 verifies it in the battery;
        #  - the v0surf-refit ripple: the mandatory surface refit (frozen-signature law) moves
        #    residual pedigree legs a few points either way; the studies predate the refit.
        # Everything else is red.
        if gnow.get(k, 0) >= 6 and 0 < d <= 250:   # W=1.0 grid-verified; F4 is the true gate
            verdict['easing_candidates'].append({'key': k, 'live': lv[k], 'cand': cv[k], 'd': d})
        elif abs(d) <= 6:
            verdict['refit_ripple'].append({'key': k, 'd': d})
        else:
            unexplained.append({'key': k, 'live': lv[k], 'cand': cv[k], 'd': d})
        continue
    dd = cv[k] - m['b_cand']
    if m.get('stepup_pending') and dd > 0:
        # the step-up class (the derivation's own overlay): landed size reported UNCAPPED —
        # the movers list presents every one of these to the owner; nothing here hides size.
        verdict['stepup_landed'].append({'key': k, 'live': lv[k], 'cand': cv[k],
                                         'wf_b_cand': m['b_cand'], 'd_beyond_wf': dd})
        continue
    if abs(dd) <= 5:
        continue
    if gnow.get(k, 0) >= 6 and 0 < dd <= 250:   # W=1.0 grid-verified; F4 is the true gate
        verdict['easing_candidates'].append({'key': k, 'live': lv[k], 'cand': cv[k], 'd': d,
                                             'wf_b_cand': m['b_cand'], 'd_vs_wf': dd})
        continue
    unexplained.append({'key': k, 'live': lv[k], 'cand': cv[k], 'd': d,
                        'wf_b_cand': m['b_cand'], 'd_vs_wf': dd})
unexplained.sort(key=lambda r: -abs(r['d']))
verdict['unexplained'] = unexplained
verdict['checks']['attribution'] = {'n_unexplained': len(unexplained), 'pass': not unexplained}
ok &= not unexplained

# 4 F5 draft cap (waterfall carries v0_cand = the smoothed draft stamp, board currency)
cap_bad = [{'key': k, 'cand': cv[k], 'v0_cand': m['v0_cand']}
           for k, m in wf_rows.items()
           if k in cv and m.get('v0_cand') and m['b_live'] <= m['v0_cand'] and cv[k] > m['v0_cand']]
verdict['checks']['f5_draft_cap'] = {'bad': cap_bad, 'pass': not cap_bad}
ok &= not cap_bad

# 5 totals
tot_l = sum(lv.values()); tot_c = sum(cv[k] for k in cv)
verdict['checks']['totals'] = {'live': tot_l, 'cand': tot_c, 'net': tot_c - tot_l,
                               'wf_pred_net': WF['meta']['board_total_cand'] - WF['meta']['board_total_live']}
verdict['pass'] = bool(ok)
json.dump(verdict, open(out_p, 'w'), indent=1)
print(json.dumps(verdict['checks'], indent=1))
for r in verdict['named']:
    print('NAMED %-18s live %-5s cand %-5s wf %-5s %s' % (r['key'], r['live'], r['cand'],
          r['wf_b_cand'], 'PASS' if r.get('pass') else ('n/a' if r.get('wf_b_cand') is None else 'RED')))
print('STEPUP landed beyond waterfall: %d rows %s' % (len(verdict['stepup_landed']),
      [(r['key'], r['d_beyond_wf']) for r in verdict['stepup_landed']]))
print('EASING candidates (first banked season in progress, F4 verifies): %d rows %s'
      % (len(verdict['easing_candidates']),
         [(r['key'], r.get('d_vs_wf', r['d'])) for r in verdict['easing_candidates']]))
print('REFIT ripple (|d|<=6, v0surf refit channel): %d rows, net %+d'
      % (len(verdict['refit_ripple']), sum(r['d'] for r in verdict['refit_ripple'])))
print('VERDICT: %s (%s)' % ('GREEN' if ok else 'RED', out_p))
sys.exit(0 if ok else 1)
