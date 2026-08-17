#!/usr/bin/env python3
"""ORDER 32 S5 STEP 5 -- decision framing: the band-monotone counterfactual and its board impact.

NOT A RECOMMENDATION. This estimates what Option B ("relax the owner's strict per-pick monotonicity
to band-level monotonicity: monotone across band means, flexible within band") would do to v0s,
so the owner can see the stakes of his ruling. Construction, per position, from the fit's OWN shrunk
PAVA input surface (S5_INPUTS.posv_pava_input):
    1. band means of the input, share-weighted, bands 1-10/11-20/21-30/31-40/41-64
    2. weighted PAVA (non-increasing) on the 5 band means (weights = band total share)
    3. within-band: v_ctf(p) = input(p) * pooled_band_mean / input_band_mean  (shape kept)
    4. floor: v_ctf = max(v_ctf, 100)
    5. one conservation scalar, same construction as the shipped pipeline
       (v' = 100 + LAM*(v-100), LAM chosen so the share-weighted total equals the curve total)
No -1 tiebreak (within-band shape is deliberately free; strict cross-pick ordering is exactly what
Option B gives up). Board impact: v0 delta per ND pick-1-64 row of the 804-row candidate board
(561 rows; board v0 == fitted surface verified exactly upstream).
Writes S5_BANDCTF.json + s5_step5_out.txt.
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
INP = json.load(open(os.path.join(HERE, 'S5_INPUTS.json')))
BOARD = json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cand31.json'))
_OUT = []
def P(s=''):
    print(s); _OUT.append(s)

import hashlib
POS = sorted(INP['posv_fitted'].keys())
PICKS = list(range(1, 65))
fin = {g: {int(k): v for k, v in INP['posv_fitted'][g].items()} for g in POS}
pin = {g: {int(k): v for k, v in INP['posv_pava_input'][g].items()} for g in POS}
ARTP = os.path.join(os.path.abspath(os.path.join(HERE, '..', '..', '..')), 'engine/rl_after/pvc_curve_v2.json')
J = json.load(open(ARTP))
share = {g: {int(k): float(v) for k, v in J['nd_v0']['share'][g].items()} for g in POS}
curve = {int(k): float(v) for k, v in J['curve'].items()}
CURVE_TOT = sum(curve[p] for p in PICKS)
FLOOR = 100.0
BANDS = [('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)]

def pava_ni(vals, wts):
    blocks = [[i] for i in range(len(vals))]
    bv = list(vals); bw = list(wts); i = 0
    while i < len(blocks) - 1:
        if bv[i] < bv[i + 1] - 1e-15:
            w = bw[i] + bw[i + 1]
            v = (bv[i] * bw[i] + bv[i + 1] * bw[i + 1]) / w if w > 0 else (bv[i] + bv[i + 1]) / 2.0
            blocks[i] += blocks[i + 1]; bv[i] = v; bw[i] = w
            del blocks[i + 1]; del bv[i + 1]; del bw[i + 1]
            if i > 0: i -= 1
        else:
            i += 1
    out = [None] * len(vals)
    for bi, blk in enumerate(blocks):
        for j in blk: out[j] = bv[bi]
    return out, blocks

P('ORDER 32 S5 STEP 5 -- BAND-MONOTONE COUNTERFACTUAL (Option B), from the fit\'s own PAVA input')
ctf = {}
pooled_any = []
for g in POS:
    bm, bw = [], []
    for nm, lo, hi in BANDS:
        w = sum(share[g][p] for p in range(lo, hi + 1))
        m = sum(share[g][p] * pin[g][p] for p in range(lo, hi + 1)) / w
        bm.append(m); bw.append(w)
    fitb, blks = pava_ni(bm, bw)
    pooled = [i for b in blks if len(b) > 1 for i in b]
    if pooled: pooled_any.append((g, [BANDS[i][0] for i in pooled]))
    v = {}
    for bi, (nm, lo, hi) in enumerate(BANDS):
        scale = fitb[bi] / bm[bi]
        for p in range(lo, hi + 1):
            v[p] = max(pin[g][p] * scale, FLOOR)
    ctf[g] = v
    P('  %-5s band means in  : %s' % (g, ' '.join('%8.1f' % x for x in bm)))
    P('        band means pava: %s   %s' % (' '.join('%8.1f' % x for x in fitb),
                                            ('POOLED ' + ','.join(BANDS[i][0] for b in blks if len(b) > 1 for i in b)) if pooled else ''))
A = sum(share[g][p] * FLOOR for g in POS for p in PICKS)
Bx = sum(share[g][p] * (ctf[g][p] - FLOOR) for g in POS for p in PICKS)
LAM = (CURVE_TOT - A) / Bx
ctf = {g: {p: FLOOR + LAM * (ctf[g][p] - FLOOR) for p in PICKS} for g in POS}
sw = sum(share[g][p] * ctf[g][p] for g in POS for p in PICKS)
P('  conservation scalar lambda = %.9f   share-weighted total drift %.3e' % (LAM, abs(sw - CURVE_TOT)))
P('')

P('COUNTERFACTUAL MINUS SHIPPED (v0 points), by pick x position -- the price of relaxing the ruling')
P('  %4s' % 'pick' + ''.join('%9s' % g for g in POS))
for p in PICKS:
    d = [ctf[g][p] - fin[g][p] for g in POS]
    if max(abs(x) for x in d) >= 0.5:
        P('  %4d' % p + ''.join('%+9.1f' % x for x in d))
P('  (picks where every |delta| < 0.5 omitted)')
P('')

# within-band ascents the counterfactual would create (what strictness currently forbids)
P('WITHIN-BAND ASCENTS THE COUNTERFACTUAL CREATES (pick pairs where v0 would INCREASE with pick)')
for g in POS:
    asc = [p for p in PICKS[1:] if ctf[g][p] > ctf[g][p - 1] + 1e-9]
    P('  %-5s %d ascents %s' % (g, len(asc), asc if asc else ''))
P('')

# ---- board impact ---------------------------------------------------------------------------------
rows = [r for r in BOARD['rows'] if r['pathway'] == 'ND' and r['pick'] and 1 <= r['pick'] <= 64]
mism = sum(1 for r in rows if abs(r['v0'] - fin[r['pos']][r['pick']]) > 0.51)
P('BOARD IMPACT -- candidate board, %d ND pick-1-64 rows of 804 (v0==surface check: %d mismatches)' % (len(rows), mism))
deltas = []
for r in rows:
    d = ctf[r['pos']][r['pick']] - fin[r['pos']][r['pick']]
    deltas.append((d, r))
by_band = collections.defaultdict(list)
for d, r in deltas:
    for nm, lo, hi in BANDS:
        if lo <= r['pick'] <= hi: by_band[nm].append(d)
P('  %-6s %6s %12s %12s %12s' % ('band', 'rows', 'mean dv0', 'min dv0', 'max dv0'))
for nm, lo, hi in BANDS:
    ds = by_band[nm]
    P('  %-6s %6d %12.1f %12.1f %12.1f' % (nm, len(ds), sum(ds) / len(ds), min(ds), max(ds)))
moved = sum(1 for d, r in deltas if abs(d) >= 10)
P('  rows with |dv0| >= 10 points: %d of %d' % (moved, len(rows)))
P('')
P('  TWENTY LARGEST |dv0| MOVERS (v0 is the entry stock; live price moves by less -- it is v0 scaled')
P('  by the law\'s D/Phi/beta bracket, so treat these as upper bounds on price moves)')
P('  %-28s %-5s %4s %9s %9s %9s' % ('player', 'pos', 'pick', 'v0 now', 'v0 ctf', 'delta'))
for d, r in sorted(deltas, key=lambda t: -abs(t[0]))[:20]:
    P('  %-28s %-5s %4d %9.1f %9.1f %+9.1f' % (r['name'], r['pos'], r['pick'],
                                               fin[r['pos']][r['pick']], ctf[r['pos']][r['pick']], d))

json.dump(dict(order='ORDER 32 S5 STEP 5 -- band-monotone counterfactual', LAM=LAM,
               ctf_surface={g: {str(p): ctf[g][p] for p in PICKS} for g in POS},
               band_pooling=[(g, b) for g, b in pooled_any],
               board_rows_affected=len(rows),
               board_moves=[dict(key=r['key'], name=r['name'], pos=r['pos'], pick=r['pick'],
                                 v0_now=fin[r['pos']][r['pick']], v0_ctf=ctf[r['pos']][r['pick']],
                                 delta=d) for d, r in sorted(deltas, key=lambda t: -abs(t[0]))]),
          open(os.path.join(HERE, 'S5_BANDCTF.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 's5_step5_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('')
P('S5_BANDCTF.json written.')
