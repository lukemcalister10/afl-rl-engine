#!/usr/bin/env python3
"""#306 — THE WIDENED POOL-DIVISION MEASUREMENT (N37, widened by the seam 2026-08-04).

THE QUESTION THE OWNER RULES ON
  The pool carries ONE blended level today. That level lifts every division sitting below it and
  drags down any sitting above it. Whether MSD / rookie / SSP / PSD entrants genuinely clear late
  national picks is an EMPIRICAL question, not a premise -- the earlier route that assumed the whole
  pool belongs below curve[64] is retired. This measures each division's realized outcomes under the
  RULED BASIS, so the owner rules levels on numbers.

METHOD -- the ruled basis, inherited, never reinvented
  Realized career value per entrant on #279's own definitions, via harness_pvc: concluded careers
  realized in full · NEVER-ESTABLISHED AT 0.0 (busts carry full weight, they are not dropped) ·
  active careers completed by concluded look-alikes · the model prior ONLY as a counted fallback.
  Late-ND (picks 46-64) is the REFERENCE division, on the same basis, so the pool reads against the
  part of the national draft it actually competes with.

RULES OBSERVED
  · every count names its denominator · untagged rows are REPORTED, never imputed
  · per-division AND per-division x position x age · thin cells are named, never smoothed into
    confident numbers -- where n is small the reader is told so rather than shown false precision
  · read-only: no engine act, no bake, nothing written outside this directory
  · NOTHING HERE SETS A LEVEL. The pool stays as-is and NAMED UNRESOLVED until the owner's word.

    python3 pool_divisions.py
"""
import json, hashlib, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PANEL = os.path.join(REPO, 'session_2026-07-30/item279/panel')
MATRIX = os.path.join(REPO, 'session_2026-07-30/item279/out/per_entrant_279_vor.json')
MATRIX_MD5 = '77eba4d308a27a881b36a5424d3bb389'
DIV = {'RD': 'rookie draft', 'MSD': 'mid-season draft', 'SSP': 'supplemental selection',
       'PDA': 'pre-season draft (A)', 'PDN': 'pre-season draft (N)', 'PDS': 'pre-season draft (S)',
       'ND': 'national selection at 65+', 'IRE': 'international rookie', 'UNR': 'untagged / unresolved'}
MIN_SHOW = 20


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def desc(v):
    v = sorted(v); n = len(v)
    return {'n': n, 'mean': round(sum(v) / n, 1), 'median': round(statistics.median(v), 1),
            'zero_share_pct': round(100.0 * sum(1 for x in v if x == 0.0) / n, 1),
            'p25': round(v[int(0.25 * (n - 1))], 1), 'p75': round(v[int(0.75 * (n - 1))], 1)}


def main():
    got = md5(MATRIX)
    if got != MATRIX_MD5:
        raise SystemExit('HALT: matrix is %s, pinned %s.' % (got, MATRIX_MD5))
    sys.path.insert(0, PANEL)
    import harness_pvc as H
    M = json.load(open(MATRIX))
    recs = M['recs']

    def structural(rows):
        """#279's own value definitions, applied to an arbitrary row set."""
        S = {}
        for r in rows:
            if not H.concluded(r): continue
            T = H.depth(r)
            if T <= 0: continue
            f = H.realised_full(r)
            for t in range(1, T + 1):
                e = S.setdefault((r['pos'], t), [0.0, 0.0, 0])
                e[0] += f; e[1] += H.sofar(r, t); e[2] += 1
        out, c = [], {}
        for r in rows:
            if H.concluded(r):
                c['concluded_realised'] = c.get('concluded_realised', 0) + 1
                out.append((r, H.realised_full(r), 'concluded_realised')); continue
            T = H.depth(r)
            e = S.get((r['pos'], T)) if T > 0 else None
            if T <= 0 or e is None or e[2] < H.MIN_STRATUM or e[1] <= 0:
                c['prior_fallback'] = c.get('prior_fallback', 0) + 1
                out.append((r, float(r['v0']), 'prior_fallback')); continue
            c['completed'] = c.get('completed', 0) + 1
            out.append((r, H.sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2])), 'completed'))
        return out, c

    pool = [r for r in recs if r.get('is_pool')]
    lateND = [r for r in recs if not r.get('is_pool') and r.get('teaches_curve')
              and r.get('pick') and 46 <= r['pick'] <= 64]

    groups = {'late-ND 46-64 (REFERENCE)': lateND}
    seen = {}
    for r in pool:
        seen.setdefault(r.get('type') or 'UNTAGGED', []).append(r)
    for k, v in sorted(seen.items(), key=lambda kv: -len(kv[1])):
        groups['%s — %s' % (k, DIV.get(k, 'UNDOCUMENTED TAG'))] = v

    out = {'what': 'per-division realized-outcome levels under the ruled basis (N37, widened)',
           'NOTHING_HERE_SETS_A_LEVEL': 'the pool stays as-is and NAMED UNRESOLVED until the owner rules',
           'basis': 'harness_pvc definitions: concluded realized in full · never-established at 0.0 '
                    '(busts full weight) · active completed by concluded look-alikes (min stratum %d) '
                    '· model prior ONLY as a counted fallback' % H.MIN_STRATUM,
           'OPTIMISM': '+4.7% to +8.4% (completion method) — inherited, reported, never corrected',
           'matrix_md5': got, 'pool_rows': len(pool), 'late_nd_rows': len(lateND),
           'divisions': {}, 'by_division_position': {}, 'by_division_age': {}}

    print('BASIS  %s' % out['basis'])
    print('OPTIMISM  %s' % out['OPTIMISM'])
    print('NOTHING HERE SETS A LEVEL — the pool stays as-is, NAMED UNRESOLVED, until the owner rules.\n')
    print('%-44s %6s %9s %9s %8s %9s %9s' % ('division', 'n', 'mean', 'median', 'zero%', 'p25', 'p75'))
    for name, rows in groups.items():
        vals, prov = structural(rows)
        d = desc([v for _, v, _ in vals]); d['provenance'] = prov
        d['fallback_share_pct'] = round(100.0 * prov.get('prior_fallback', 0) / len(rows), 1)
        out['divisions'][name] = d
        flag = '' if d['n'] >= MIN_SHOW else '   << THIN (n<%d): read as indicative only' % MIN_SHOW
        print('%-44s %6d %9.1f %9.1f %7.1f%% %9.1f %9.1f%s'
              % (name[:44], d['n'], d['mean'], d['median'], d['zero_share_pct'], d['p25'], d['p75'], flag))

    for name, rows in groups.items():
        vals, _ = structural(rows)
        bypos, byage = {}, {}
        for r, v, _h in vals:
            bypos.setdefault(r.get('pos') or 'UNTAGGED', []).append(v)
            a = r.get('age_draft')
            byage.setdefault('UNTAGGED' if a is None else str(int(a)), []).append(v)
        out['by_division_position'][name] = {k: desc(v) for k, v in sorted(bypos.items())}
        out['by_division_age'][name] = {k: desc(v) for k, v in sorted(byage.items())}

    print('\nBY DIVISION x POSITION — n named on every cell; thin cells are marked, never smoothed')
    for name in out['by_division_position']:
        cells = out['by_division_position'][name]
        s = '  '.join('%s %.0f (n=%d)%s' % (k, c['mean'], c['n'], '*' if c['n'] < MIN_SHOW else '')
                      for k, c in cells.items())
        print('  %-30s %s' % (name[:30], s))
    print('  * = n < %d: indicative only, not a level' % MIN_SHOW)

    print('\nBY DIVISION x DRAFT AGE')
    for name in out['by_division_age']:
        cells = out['by_division_age'][name]
        s = '  '.join('%s %.0f (n=%d)%s' % (k, c['mean'], c['n'], '*' if c['n'] < MIN_SHOW else '')
                      for k, c in cells.items())
        print('  %-30s %s' % (name[:30], s))

    with open(os.path.join(HERE, 'pool_divisions.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')
    print('\nwrote pool_divisions.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
