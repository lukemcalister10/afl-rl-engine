#!/usr/bin/env python3
"""#306 — THE POOL-LEVEL RE-RUN (seam order 5179598225, owner rulings 2026-08-04).

WHAT THE OWNER RULED, AND WHAT THIS DOES NOT DO
  Per-division levels replace the single blend at the landing · positional differentiation is ROOKIE
  DRAFT ONLY · final levels are confidence-weighted so small samples pull toward the pool-wide
  MEASURED aggregate.  **NOTHING HERE SETS A LEVEL.**  The exact numbers are UNRULED; they return to
  the owner through the seam, decomposed, and he signs.  The pool stays NAMED UNRESOLVED (N37.5).

THE ONE CHANGE FROM THE FIRST RUN — POOLED COMPLETION STRATA
  The basis definitions are untouched (concluded realized in full · never-established at 0.0 · busts
  at FULL WEIGHT · model prior ONLY as a counted fallback).  The completion strata (position x tenure,
  min stratum 20) are now built from ALL POOL CONCLUDED CAREERS ACROSS DIVISIONS rather than within
  each division separately.  A thin division could not previously find 20 concluded look-alikes of its
  own, so it fell back to the model's prior -- 59.4% of MSD rows, 53.8% of SSP.  Pooling the strata
  gives those rows real look-alikes.  The prior share is reported BEFORE and AFTER so the improvement
  is itself measured rather than asserted.

  The late-ND 46-64 REFERENCE keeps its own strata: it is not a pool division, and its prior share was
  already 11.2%.  Stated so the comparison's basis is not silently mixed.

READ-ONLY.  No engine act, no fit, no bake, nothing written outside this directory.  N35's fit-path
assert governs FIT figures; nothing here fits a surface, and no engine act is performed -- named
rather than silently skipped.  Matrix pinned by md5; HALT if it moves.

    python3 pool_levels_rerun.py
"""
import hashlib, json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PANEL = os.path.join(REPO, 'session_2026-07-30/item279/panel')
MATRIX = os.path.join(REPO, 'session_2026-07-30/item279/out/per_entrant_279_vor.json')
MATRIX_MD5 = '77eba4d308a27a881b36a5424d3bb389'
KS = [15, 25, 50]
MIN_CELL = 20
OPTIMISM = ('+4.7% to +8.4% optimistic (completion method) — inherited from the ruled curve\'s own '
            'basis, reported with every result, never silently corrected')
DIV = {'RD': 'rookie draft', 'MSD': 'mid-season draft', 'SSP': 'supplemental selection',
       'PDA': 'post-draft academy', 'PDN': 'post-draft next-gen', 'PDS': 'post-draft scholarship',
       'ND': 'national selection at 65+', 'IRE': 'post-draft Ireland', 'UNR': 'post-draft unregistered'}


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def main():
    got = md5(MATRIX)
    if got != MATRIX_MD5:
        raise SystemExit('HALT: matrix %s, pinned %s.' % (got, MATRIX_MD5))
    sys.path.insert(0, PANEL)
    import harness_pvc as H
    recs = json.load(open(MATRIX))['recs']
    pool = [r for r in recs if r.get('is_pool')]
    lateND = [r for r in recs if not r.get('is_pool') and r.get('teaches_curve')
              and r.get('pick') and 46 <= r['pick'] <= 64]

    def strata(rows):
        S = {}
        for r in rows:
            if not H.concluded(r): continue
            T = H.depth(r)
            if T <= 0: continue
            f = H.realised_full(r)
            for t in range(1, T + 1):
                e = S.setdefault((r['pos'], t), [0.0, 0.0, 0]); e[0] += f; e[1] += H.sofar(r, t); e[2] += 1
        return S

    def values(rows, S):
        out, c = [], {}
        for r in rows:
            if H.concluded(r):
                c['concluded'] = c.get('concluded', 0) + 1
                out.append((r, H.realised_full(r))); continue
            T = H.depth(r); e = S.get((r['pos'], T)) if T > 0 else None
            if T <= 0 or e is None or e[2] < H.MIN_STRATUM or e[1] <= 0:
                c['prior_fallback'] = c.get('prior_fallback', 0) + 1
                out.append((r, float(r['v0']))); continue
            c['completed'] = c.get('completed', 0) + 1
            out.append((r, H.sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2]))))
        return out, c

    S_pooled = strata(pool)                       # THE CHANGE: strata across ALL pool divisions
    groups = {}
    for r in pool:
        groups.setdefault(r.get('type') or 'UNTAGGED', []).append(r)

    def lvl(vals):
        v = [x for _, x in vals]
        return {'n': len(v), 'mean': round(sum(v) / len(v), 1),
                'median': round(statistics.median(v), 1),
                'zero_share_pct': round(100.0 * sum(1 for x in v if x == 0.0) / len(v), 1)}

    # pool-wide MEASURED aggregate — the shrink target. Never the model's 435.63.
    all_pool, prov_all = values(pool, S_pooled)
    POOLWIDE = sum(x for _, x in all_pool) / len(all_pool)

    out = {'what': 'pool levels re-run with POOLED completion strata + confidence-weighted presentation',
           'NOTHING_HERE_SETS_A_LEVEL': 'exact levels are UNRULED; the owner signs. Pool NAMED UNRESOLVED.',
           'the_change': 'completion strata built from ALL POOL concluded careers across divisions, not '
                         'within each division. Basis definitions otherwise untouched.',
           'late_nd_note': 'the late-ND 46-64 REFERENCE keeps its own strata — it is not a pool division '
                           'and its prior share was already 11.2%. Named so the basis is not silently mixed.',
           'OPTIMISM': OPTIMISM, 'matrix_md5': got, 'min_stratum': H.MIN_STRATUM,
           'pool_wide_measured_aggregate': round(POOLWIDE, 1),
           'shrink_target': 'the pool-wide MEASURED aggregate above — never the model prior (435.63)',
           'K_values': KS, 'divisions': {}, 'rookie_positional': {}, 'recency_controls': {}}

    print('THE CHANGE  %s' % out['the_change'])
    print('OPTIMISM    %s' % OPTIMISM)
    print('SHRINK TARGET  pool-wide MEASURED aggregate = %.1f  (never the model prior)' % POOLWIDE)
    print('NOTHING HERE SETS A LEVEL — the owner signs.\n')

    hdr = ('%-34s %5s %8s %8s %7s %7s %7s   %8s %8s %8s'
           % ('division', 'n', 'raw', 'median', 'zero%', 'prior%', 'was%', 'K=15', 'K=25', 'K=50'))
    print(hdr); print('  ' + '-' * (len(hdr) - 2))
    ref_v, ref_c = values(lateND, strata(lateND))
    for label, rows, vals, cnt in ([('late-ND 46-64 (REFERENCE)', lateND, ref_v, ref_c)] +
                                   [('%s — %s' % (k, DIV.get(k, 'UNDOCUMENTED TAG')), v) + tuple([None, None])
                                    for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1]))]):
        if vals is None:
            vals, cnt = values(rows, S_pooled)
            _, was = values(rows, strata(rows))          # BEFORE: per-division strata
            was_pct = round(100.0 * was.get('prior_fallback', 0) / len(rows), 1)
        else:
            was_pct = round(100.0 * cnt.get('prior_fallback', 0) / len(rows), 1)
        d = lvl(vals)
        d['prior_share_pct'] = round(100.0 * cnt.get('prior_fallback', 0) / len(rows), 1)
        d['prior_share_pct_before_pooling'] = was_pct
        d['provenance'] = cnt
        for K in KS:
            w = d['n'] / (d['n'] + K)
            d['shrunk_K%d' % K] = round(w * d['mean'] + (1 - w) * POOLWIDE, 1)
        out['divisions'][label] = d
        print('%-34s %5d %8.1f %8.1f %6.1f%% %6.1f%% %6.1f%%   %8.1f %8.1f %8.1f'
              % (label[:34], d['n'], d['mean'], d['median'], d['zero_share_pct'],
                 d['prior_share_pct'], d['prior_share_pct_before_pooling'],
                 d['shrunk_K15'], d['shrunk_K25'], d['shrunk_K50']))
    print('  prior%% = model-prior share AFTER pooling · was%% = BEFORE (per-division strata)')

    # ---- the ruled differentiation: ROOKIE DRAFT ONLY
    rd = groups.get('RD', [])
    rd_v, _ = values(rd, S_pooled)
    RDLVL = sum(x for _, x in rd_v) / len(rd_v)
    bypos = {}
    for r, v in rd_v: bypos.setdefault(r.get('pos') or 'UNTAGGED', []).append(v)
    print('\nROOKIE-DRAFT POSITIONAL LEVELS (the ONLY ruled differentiation) — shrunk toward the RD '
          'division level %.1f' % RDLVL)
    print('  %-10s %5s %8s   %8s %8s %8s' % ('position', 'n', 'raw', 'K=15', 'K=25', 'K=50'))
    for p, v in sorted(bypos.items()):
        m = sum(v) / len(v); e = {'n': len(v), 'raw': round(m, 1)}
        for K in KS:
            w = len(v) / (len(v) + K); e['shrunk_K%d' % K] = round(w * m + (1 - w) * RDLVL, 1)
        out['rookie_positional'][p] = e
        print('  %-10s %5d %8.1f   %8.1f %8.1f %8.1f%s'
              % (p, e['n'], e['raw'], e['shrunk_K15'], e['shrunk_K25'], e['shrunk_K50'],
                 '' if e['n'] >= MIN_CELL else '   << n<%d' % MIN_CELL))
    out['rookie_division_level'] = round(RDLVL, 1)

    # ---- same-window recency controls, committed
    print('\nSAME-WINDOW RECENCY CONTROLS — is a division low on QUALITY or just YOUNGER?')
    print('  %-34s %5s %8s' % ('cohort', 'n', 'level'))
    for lo in (2016, 2018, 2019):
        sub = [r for r in rd if (r.get('year') or 0) >= lo]
        if sub:
            vv, cc = values(sub, S_pooled); m = sum(x for _, x in vv) / len(vv)
            out['recency_controls']['RD %d+' % lo] = {'n': len(vv), 'level': round(m, 1),
                'prior_share_pct': round(100.0 * cc.get('prior_fallback', 0) / len(sub), 1)}
            print('  %-34s %5d %8.1f' % ('RD %d+' % lo, len(vv), m))
    for tag in ('PDN', 'SSP', 'MSD'):
        g = groups.get(tag, [])
        if not g: continue
        yrs = [r.get('year') for r in g if r.get('year')]
        vv, cc = values(g, S_pooled); m = sum(x for _, x in vv) / len(vv)
        out['recency_controls']['%s own window %d-%d' % (tag, min(yrs), max(yrs))] = {
            'n': len(vv), 'level': round(m, 1),
            'prior_share_pct': round(100.0 * cc.get('prior_fallback', 0) / len(g), 1)}
        print('  %-34s %5d %8.1f' % ('%s own window %d-%d' % (tag, min(yrs), max(yrs)), len(vv), m))

    with open(os.path.join(HERE, 'pool_levels_rerun.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')
    print('\nwrote pool_levels_rerun.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
