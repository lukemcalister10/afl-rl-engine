#!/usr/bin/env python3
"""WORD B — the candidate-board movers between the STATIC and CONDITIONED peak-model fits.

Both boards are built on the SAME band, the SAME ceiling, the SAME store and the SAME v838 modernized
bust-prior table. The ONLY difference is whether the peak model's bust_prior feature is conditioned on
early-career cameo evidence — at training AND at inference. So every mover here is the lever and
nothing else.

Reported: the whole-board summary, the 51-row cameo census the seam study defined (its own in-scope
rows), and the named rows the coordinator asked for. Rows are reported whether they moved or not —
a named row that did NOT move is a result, and dropping it would be selection.
"""
import argparse, json, sys


def rows(p):
    return {r['key']: r for r in json.load(open(p))['active']}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('static')
    ap.add_argument('conditioned')
    ap.add_argument('--census', required=True, help='the seam study census_rel.json (its in-scope rows)')
    ap.add_argument('--named', default='james-leake,harrison-oliver,jesse-dattoli')
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])

    S, C = rows(a.static), rows(a.conditioned)
    keys = sorted(set(S) & set(C))
    mv = []
    for k in keys:
        o, n = S[k].get('v'), C[k].get('v')
        if o is None or n is None:
            continue
        mv.append((k, o, n, n - o, (100.0 * (n - o) / o) if o else 0.0))

    up = [m for m in mv if m[3] > 0]
    dn = [m for m in mv if m[3] < 0]
    flat = [m for m in mv if m[3] == 0]
    tot_o = sum(m[1] for m in mv)
    tot_n = sum(m[2] for m in mv)
    absp = sorted(abs(m[4]) for m in mv)
    R = {'rows': len(mv), 'up': len(up), 'down': len(dn), 'flat': len(flat),
         'pool_static': tot_o, 'pool_conditioned': tot_n, 'pool_delta': tot_n - tot_o,
         'pool_delta_pct': round(100.0 * (tot_n - tot_o) / tot_o, 4) if tot_o else 0.0,
         'sum_abs_move': sum(abs(m[3]) for m in mv),
         'median_abs_pct': round(absp[len(absp) // 2], 4) if absp else 0.0,
         'p90_abs_pct': round(absp[int(0.9 * len(absp))], 4) if absp else 0.0,
         'max_abs_pct': round(absp[-1], 4) if absp else 0.0}
    print('=== WORD B — CONDITIONED vs STATIC peak model, same band/ceiling/store/table ===')
    print('  rows compared      : %d' % R['rows'])
    print('  UP / DOWN / FLAT   : %d / %d / %d' % (R['up'], R['down'], R['flat']))
    print('  pool total         : %d -> %d   (%+d, %+.4f%%)'
          % (tot_o, tot_n, R['pool_delta'], R['pool_delta_pct']))
    print('  sum |move|         : %d' % R['sum_abs_move'])
    print('  median |move| pct  : %.3f%%   90th %.3f%%   max %.3f%%'
          % (R['median_abs_pct'], R['p90_abs_pct'], R['max_abs_pct']))
    for name, sel, key in (('BIGGEST UP', up, lambda m: -m[3]), ('BIGGEST DOWN', dn, lambda m: m[3])):
        print('  --- %s, top 10 ---' % name)
        for k, o, n, d, p in sorted(sel, key=key)[:10]:
            print('      %-28s %7d -> %7d  %+7d  %+.2f%%' % (k, o, n, d, p))
    R['top_up'] = [(m[0], m[1], m[2], m[3], round(m[4], 3)) for m in sorted(up, key=lambda m: -m[3])[:10]]
    R['top_down'] = [(m[0], m[1], m[2], m[3], round(m[4], 3)) for m in sorted(dn, key=lambda m: m[3])[:10]]

    # ---- the seam study's OWN 51-row cameo census -------------------------------------------
    cen = json.load(open(a.census))
    ck = [r['key'] for r in cen]
    byk = {m[0]: m for m in mv}
    live_in_census = [k for k in ck if k in byk]
    cmv = [byk[k] for k in live_in_census]
    cup = len([m for m in cmv if m[3] > 0])
    cdn = len([m for m in cmv if m[3] < 0])
    cfl = len([m for m in cmv if m[3] == 0])
    print('\n=== THE SEAM STUDY\'S 51-ROW CAMEO CENSUS (its own in-scope rows) ===')
    print('  census rows          : %d   of which on this board: %d' % (len(ck), len(cmv)))
    print('  UP / DOWN / FLAT     : %d / %d / %d' % (cup, cdn, cfl))
    if cmv:
        print('  pool                 : %d -> %d  (%+d)'
              % (sum(m[1] for m in cmv), sum(m[2] for m in cmv),
                 sum(m[2] for m in cmv) - sum(m[1] for m in cmv)))
        print('  %-28s %8s %8s %8s %8s  %s' % ('key', 'static', 'cond', 'delta', 'pct', 'cameo/pick/t'))
        meta = {r['key']: r for r in cen}
        for k, o, n, d, p in sorted(cmv, key=lambda m: m[3]):
            r = meta.get(k, {})
            print('  %-28s %8d %8d %+8d %+7.2f%%  c=%s pk=%s t=%s'
                  % (k, o, n, d, p, r.get('cameo'), r.get('pick'), r.get('tenure')))
    R['cameo_census'] = {'census_rows': len(ck), 'on_board': len(cmv),
                         'up': cup, 'down': cdn, 'flat': cfl,
                         'rows': [{'key': m[0], 'static': m[1], 'conditioned': m[2],
                                   'delta': m[3], 'pct': round(m[4], 3)} for m in cmv]}

    print('\n=== THE NAMED ROWS ===')
    R['named'] = {}
    for k in [x.strip() for x in a.named.split(',') if x.strip()]:
        if k in byk:
            _, o, n, d, p = byk[k]
            R['named'][k] = {'static': o, 'conditioned': n, 'delta': d, 'pct': round(p, 3),
                             'in_cameo_census': k in ck}
            print('  %-28s %7d -> %7d  %+6d  %+.2f%%   %s'
                  % (k, o, n, d, p, 'in the census' if k in ck else 'not in the census'))
        else:
            R['named'][k] = 'NOT ON THE BOARD'
            print('  %-28s NOT ON THE BOARD (reported, not dropped)' % k)

    if a.json:
        json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
