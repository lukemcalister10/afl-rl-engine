#!/usr/bin/env python3
"""ARM 1 — THE MOVERS REPORT. Candidate board vs the live board, and the T1 attribution.

The board's player values live in the 'active' list, keyed by 'key', with the present-lens value in
'v' (and the forward lenses in vP1/vP2, the back lenses in vM1/vM2). Everything below is computed
from the two board files; nothing is typed.

Usage: movers.py LIVE.json CAND.json [NOT1.json] [--json OUT]
"""
import argparse, json, sys
from collections import Counter


def rows(p):
    return {r['key']: r for r in json.load(open(p))['active']}


def moves(a, b, field='v'):
    """(key, old, new, delta, pct) for every row present in both, plus the row-universe diff."""
    ka, kb = set(a), set(b)
    out = []
    for k in sorted(ka & kb):
        o, n = a[k].get(field), b[k].get(field)
        if o is None or n is None:
            continue
        d = n - o
        out.append((k, o, n, d, (100.0 * d / o) if o else float('inf') if d else 0.0))
    return out, sorted(ka - kb), sorted(kb - ka)


def pct(x):
    return '%+.2f%%' % x if abs(x) != float('inf') else 'n/a'


def summarise(tag, mv, only_a, only_b, top=10):
    up = [m for m in mv if m[3] > 0]
    dn = [m for m in mv if m[3] < 0]
    flat = [m for m in mv if m[3] == 0]
    print('\n=== %s ===' % tag)
    print('  rows compared      : %d   (only in live: %d ; only in candidate: %d)'
          % (len(mv), len(only_a), len(only_b)))
    print('  UP / DOWN / FLAT   : %d / %d / %d' % (len(up), len(dn), len(flat)))
    if not mv:
        return {}
    tot_o = sum(m[1] for m in mv); tot_n = sum(m[2] for m in mv)
    absd = sorted(abs(m[3]) for m in mv)
    abspct = sorted(abs(m[4]) for m in mv if m[4] != float('inf'))
    med = absd[len(absd) // 2]
    medp = abspct[len(abspct) // 2] if abspct else 0.0
    print('  pool total         : %d -> %d   (%+d, %+.4f%%)  <-- LAW-9 MINT, reported not gated (v830)'
          % (tot_o, tot_n, tot_n - tot_o, 100.0 * (tot_n - tot_o) / tot_o))
    print('  sum |move|         : %d   (mean %.1f, median %.1f)'
          % (sum(abs(m[3]) for m in mv), sum(abs(m[3]) for m in mv) / len(mv), med))
    print('  median |move| pct  : %.2f%%   ;  90th pct |move| : %.2f%%   ; max |move| pct : %.2f%%'
          % (medp, abspct[int(0.9 * len(abspct))] if abspct else 0, abspct[-1] if abspct else 0))
    for name, sel, key in (('BIGGEST UP (by size)', up, lambda m: -m[3]),
                           ('BIGGEST DOWN (by size)', dn, lambda m: m[3])):
        print('  --- %s, top %d ---' % (name, top))
        for k, o, n, d, p in sorted(sel, key=key)[:top]:
            print('      %-28s %7d -> %7d  %+7d  %s' % (k, o, n, d, pct(p)))
    return {'up': len(up), 'down': len(dn), 'flat': len(flat), 'n': len(mv),
            'total_old': tot_o, 'total_new': tot_n,
            'mint_abs': tot_n - tot_o, 'mint_pct': 100.0 * (tot_n - tot_o) / tot_o,
            'sum_abs_move': sum(abs(m[3]) for m in mv),
            'median_abs_pct': medp,
            'top_up': [(m[0], m[1], m[2], m[3], m[4]) for m in sorted(up, key=lambda m: -m[3])[:top]],
            'top_down': [(m[0], m[1], m[2], m[3], m[4]) for m in sorted(dn, key=lambda m: m[3])[:top]]}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('live'); ap.add_argument('cand'); ap.add_argument('not1', nargs='?')
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])
    L, C = rows(a.live), rows(a.cand)
    res = {}
    mv, oa, ob = moves(L, C)
    res['candidate_vs_live'] = summarise('CANDIDATE vs LIVE  (present lens, v)', mv, oa, ob)

    # where the movement sits — by tenure and by evidence, the prereg's P4
    print('\n  --- |move| by tenure T = 2026 - debut + 1 (candidate vs live) ---')
    by = {}
    for k, o, n, d, p in mv:
        r = C[k]
        t = r.get('T') or r.get('ten') or (2026 - (r.get('dy') or 0) + 1 if r.get('dy') else None)
        g = r.get('g', 0)
        bucket = ('games<=22' if g <= 22 else 'games 23-80' if g <= 80 else 'games>80')
        by.setdefault(bucket, []).append(abs(p) if p != float('inf') else 0.0)
    for b in sorted(by):
        v = sorted(by[b])
        print('      %-14s n=%4d  median |move| %6.2f%%  90th %6.2f%%  max %7.2f%%'
              % (b, len(v), v[len(v) // 2], v[int(0.9 * len(v))], v[-1]))
    res['by_experience'] = {b: {'n': len(by[b]), 'median_abs_pct': sorted(by[b])[len(by[b]) // 2]}
                            for b in by}

    print('\n  --- |move| by position group ---')
    bypos = {}
    for k, o, n, d, p in mv:
        bypos.setdefault(C[k].get('grp', '?'), []).append(abs(p) if p != float('inf') else 0.0)
    for g in sorted(bypos):
        v = sorted(bypos[g])
        print('      %-8s n=%4d  median |move| %6.2f%%  max %7.2f%%' % (g, len(v), v[len(v) // 2], v[-1]))

    if a.not1:
        N = rows(a.not1)
        mvn, _, _ = moves(N, C)                 # T1-off candidate -> T1-on candidate: T1's OWN effect
        res['t1_effect'] = summarise('T1 ATTRIBUTION  (same store, same everything; T1 off -> T1 on)',
                                     mvn, [], [])
        mvs, _, _ = moves(L, N)                 # live -> T1-off candidate: the STORE's effect alone
        res['store_effect_only'] = summarise('STORE ALONE, T1 EXCLUDED  (live -> candidate with T1 off)',
                                             mvs, [], [])
        tot_c = res['candidate_vs_live']['sum_abs_move']
        tot_t1 = res['t1_effect']['sum_abs_move']
        tot_s = res['store_effect_only']['sum_abs_move']
        print('\n=== ATTRIBUTION ===')
        print('  total |movement| live -> candidate          : %d' % tot_c)
        print('  |movement| attributable to T1 alone         : %d  (%.2f%% of the total)'
              % (tot_t1, 100.0 * tot_t1 / tot_c if tot_c else 0))
        print('  |movement| store alone, T1 held out         : %d  (%.2f%% of the total)'
              % (tot_s, 100.0 * tot_s / tot_c if tot_c else 0))
        print('  (the two legs do not sum to the whole: the effects are not additive on a')
        print('   non-linear pricing chain. They bound the attribution, they do not decompose it.)')
        res['attribution'] = {'total_abs_move': tot_c, 't1_abs_move': tot_t1,
                              't1_share_pct': 100.0 * tot_t1 / tot_c if tot_c else 0,
                              'store_only_abs_move': tot_s}

    if a.json:
        with open(a.json, 'w') as f:
            json.dump(res, f, indent=1, sort_keys=True, default=float)
            f.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
