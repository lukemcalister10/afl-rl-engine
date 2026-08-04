#!/usr/bin/env python3
"""#306 L-A — THE LENS, MEASURED BEFORE IT IS REDESIGNED.

THE QUESTION
  The owner's steer (N29) says year-zero values ANCHOR to the measured pick outcomes, and that position
  and age MODULATE within bounds -- they redistribute around the anchor, they never inflate it.  The
  current surface is not built that way at all: `_build_v0_curve` fits `_v0_raw` (the model's own V0
  estimate) over log(recorded pick) and never references the pick curve.  The curve enters only through
  the config SIGNATURE.  So the surface is free to sit wherever the model's estimates sit.

  Before designing a construction that anchors it, this measures the modulation the CURRENT surface
  actually applies:  m = v0 / curve[pick].  Under N29 a lawful lens has m distributed around 1 with a
  bounded spread; an inflating lens has m drifting up where evidence thins.

  It also measures the two structural facts L-A must carry: the pool's position against the last
  national band (requirement 2), and the bust inversion the construction must NOT depend on
  (requirement 4).

READ THIS BEFORE QUOTING ANY NUMBER BELOW
  **FIT population** -- the matrix's own `teaches_curve` rows at picks 1-64.  NOT the G-Y0 gate's
  ~1,326-row population; the gate runs inside `one_source_selftest.py` over its own set and prints its
  own figure.  Numbers here land near the gated ones and ARE NOT THEM.  The SHAPE is what this is for.

INPUTS ARE ASSERTED BY md5, and the curve by its N32 PAYLOAD identity (string-keyed, int(round(v))) --
the file md5 of a working-tree substrate file is not a stable identity, the payload is.  HALTs rather
than reporting a number against an unnamed substrate.  Read-only: no engine act, no bake, nothing
written outside this directory.

    python3 lens_shape.py
"""
import json, hashlib, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
MATRIX = os.path.join(REPO, 'docs/evidence/rehearsal_290_2026-07-31/L6_convergence/pass0_matrix.json')
CURVE  = os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')

MATRIX_MD5   = '9c4bca53b738452739c353d94fe99928'   # the pass-0 matrix, installed curve e69a3f38
CURVE_PAYLOAD = 'e69a3f38'                          # N32 identity of the installed anchor
BANDS = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def payload_md5(curve):
    """N32: string-sorted keys, default separators, int(round(v)).  The key type is load-bearing."""
    d = {str(k): int(round(v)) for k, v in curve.items()}
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()[:8]


def band_of(pick):
    for lo, hi in BANDS:
        if lo <= pick <= hi:
            return '%d-%d' % (lo, hi)
    return None


def main():
    got = md5(MATRIX)
    if got != MATRIX_MD5:
        raise SystemExit('HALT: pass0_matrix.json is %s, pinned %s — an input moved.' % (got, MATRIX_MD5))
    curve = json.load(open(CURVE))['curve']
    gotp = payload_md5(curve)
    if gotp != CURVE_PAYLOAD:
        raise SystemExit('HALT: the installed curve payload is %s, expected %s — the anchor moved. '
                         'Reconstruct the pass-0 substrate before measuring.' % (gotp, CURVE_PAYLOAD))
    C = {int(k): float(v) for k, v in curve.items()}
    recs = json.load(open(MATRIX))['recs']

    teach = [r for r in recs
             if r.get('teaches_curve') and r.get('v0') is not None
             and r.get('pick') is not None and 1 <= r['pick'] <= 64]
    out = {'what': 'the modulation m = v0 / curve[pick] the CURRENT surface applies, before redesign',
           'POPULATION_WARNING': 'FIT population (teaches_curve rows, picks 1-64) — NOT the G-Y0 gate\'s '
                                 '~1,326-row population. Never quote a figure from here as a gated G-Y0.',
           'anchor_curve_payload': gotp, 'matrix_md5': got, 'rows': len(teach)}

    # ---- 1. aggregate neutrality: sum(v0) / sum(anchor).  N30's first limb reads on exactly this.
    sv, sc = sum(r['v0'] for r in teach), sum(C[r['pick']] for r in teach)
    out['aggregate'] = {'sum_v0': round(sv, 1), 'sum_anchor': round(sc, 1),
                        'ratio': round(sv / sc, 6), 'gap_pct': round(100 * (sv / sc - 1), 4),
                        'reading': 'a lens that redistributes nets to 1.0; this is what it nets to'}

    # ---- 2. the lens by band: where does m sit, and how wide is it?
    by = {}
    for lo, hi in BANDS:
        rows = [r for r in teach if lo <= r['pick'] <= hi]
        m = sorted(r['v0'] / C[r['pick']] for r in rows)
        sv_b = sum(r['v0'] for r in rows); sc_b = sum(C[r['pick']] for r in rows)
        by['%d-%d' % (lo, hi)] = {
            'rows': len(rows),
            'band_ratio': round(sv_b / sc_b, 6),          # the band's own aggregate m
            'band_gap_pct': round(100 * (sv_b / sc_b - 1), 4),
            'm_median': round(statistics.median(m), 4),
            'm_p10': round(m[int(0.10 * (len(m) - 1))], 4),
            'm_p90': round(m[int(0.90 * (len(m) - 1))], 4),
            'm_min': round(m[0], 4), 'm_max': round(m[-1], 4)}
    out['by_band'] = by

    # ---- 3. what bound would contain the current lens, per band and overall?
    allm = sorted(r['v0'] / C[r['pick']] for r in teach)
    out['bound_required_by_todays_lens'] = {
        'overall_m_max': round(allm[-1], 4), 'overall_m_min': round(allm[0], 4),
        'overall_m_p99': round(allm[int(0.99 * (len(allm) - 1))], 4),
        'worst_band_aggregate_m': round(max(v['band_ratio'] for v in by.values()), 4),
        'reading': 'a symmetric bound B containing every ROW is far wider than one containing every '
                   'BAND AGGREGATE. N30 bounds the band, not the row — these are the two candidate '
                   'readings and the design must state which it adopts.'}

    # ---- 4. the lens by position and by draft age — is the spread positional, or is it pick-depth?
    def group(keyfn, label):
        g = {}
        for r in teach:
            k = keyfn(r)
            if k is None:
                continue
            g.setdefault(k, []).append(r)
        return {label: {str(k): {'rows': len(v),
                                 'ratio': round(sum(x['v0'] for x in v) / sum(C[x['pick']] for x in v), 4)}
                        for k, v in sorted(g.items(), key=lambda kv: str(kv[0]))}}
    out.update(group(lambda r: r.get('pos'), 'by_position'))
    out.update(group(lambda r: r.get('age_draft'), 'by_draft_age'))

    # ---- 5. L-A requirement 2: the pool against the LAST national band. Structural coherence.
    pool = [r for r in recs if r.get('is_pool') and r.get('v0') is not None]
    if pool:
        pv = [r['v0'] for r in pool]
        out['pool_coherence'] = {
            'n': len(pool), 'mean_v0': round(sum(pv) / len(pv), 2),
            'median_v0': round(statistics.median(pv), 2),
            'curve_64': C[64],
            'mean_above_curve64': (sum(pv) / len(pv)) > C[64],
            'share_above_curve64': round(100.0 * sum(1 for v in pv if v > C[64]) / len(pv), 2),
            'reading': 'one_source_selftest records "the pool sits BELOW the curve, by construction" as '
                       'a structural truth. Measured here against curve[64] on this substrate.'}

    # ---- 6. L-A requirement 4: the bust inversion, carried forward and re-measured, never depended on.
    mat = [r for r in pool if (r.get('age_draft') or 0) >= 19] or pool
    never = [r['v0'] for r in mat if not (r.get('games_total') or 0)]
    played = [r['v0'] for r in mat if (r.get('games_total') or 0) > 0]
    if never and played:
        out['bust_inversion'] = {
            'never_played': {'n': len(never), 'mean_v0': round(sum(never) / len(never), 1)},
            'played':       {'n': len(played), 'mean_v0': round(sum(played) / len(played), 1)},
            'inverted': (sum(never) / len(never)) > (sum(played) / len(played)),
            'reading': 'a quantity where busts outscore contributors cannot set an entry level. The '
                       'construction is CHECKED against this and must not DEPEND on it.'}

    with open(os.path.join(HERE, 'lens_shape.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print(out['POPULATION_WARNING'] + '\n')
    print('anchor curve payload %s | matrix %s | teaching rows %d\n' % (gotp, got[:8], len(teach)))
    a = out['aggregate']
    print('AGGREGATE     sum(v0)/sum(anchor) = %.6f   (%+.4f%%)   <- N30 limb 1 reads here' %
          (a['ratio'], a['gap_pct']))
    print('\nTHE LENS BY BAND        rows   aggregate m        m median    p10 .. p90        min .. max')
    for k in ('1-10', '11-20', '21-30', '31-45', '46-64'):
        v = by[k]
        print('  %-8s %12d   %8.4f (%+7.2f%%)   %7.4f   %6.3f..%-7.3f  %6.3f..%.3f'
              % (k, v['rows'], v['band_ratio'], v['band_gap_pct'], v['m_median'],
                 v['m_p10'], v['m_p90'], v['m_min'], v['m_max']))
    print('\nBY POSITION   ' + '  '.join('%s %.3f' % (k, v['ratio']) for k, v in out['by_position'].items()))
    print('BY DRAFT AGE  ' + '  '.join('%s %.3f' % (k, v['ratio']) for k, v in out['by_draft_age'].items()))
    if 'pool_coherence' in out:
        p = out['pool_coherence']
        print('\nPOOL COHERENCE  n=%d  mean v0 %.2f  vs curve[64] %.0f  ->  mean ABOVE the last band: %s'
              % (p['n'], p['mean_v0'], p['curve_64'], p['mean_above_curve64']))
        print('                %.2f%% of pool rows sit above curve[64]' % p['share_above_curve64'])
    if 'bust_inversion' in out:
        b = out['bust_inversion']
        print('\nBUST INVERSION  never-played %.1f (n=%d)  vs  played %.1f (n=%d)  ->  inverted: %s'
              % (b['never_played']['mean_v0'], b['never_played']['n'],
                 b['played']['mean_v0'], b['played']['n'], b['inverted']))
    print('\nwrote lens_shape.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
