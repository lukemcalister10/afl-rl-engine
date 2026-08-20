import json, sys
d = json.load(open(sys.argv[1]))
for nm in d:
    R = d[nm]['rows']
    print('=' * 100)
    print(nm, 'shipped', d[nm]['v_before'])
    keys = ['v_board', 'ev_prefloor', 'ev_click', 'ev_pin', 'prod_path', 'raw_ev', 'price6',
            'lvl_eff', 'lvlcurr', 'coreM1', 'lvl_wt', 'exposure', 'bestlvl', 'A_e_pre', 'A_blend',
            'A_anch', 'A_s', 'A_w', 'h_cut', 'iso_eff']
    # biggest v steps
    steps = sorted(range(len(R) - 1), key=lambda i: -abs(R[i + 1]['v_board'] - R[i]['v_board']))[:6]
    for i in sorted(steps):
        a, b = R[i], R[i + 1]
        print('-- step score %d->%d  avg %.4f->%.4f' % (a['score'], b['score'], a['avg'], b['avg']))
        for k in keys:
            va, vb = a.get(k), b.get(k)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                rel = (vb - va) / abs(va) * 100 if va else float('nan')
                print('     %-14s %14.5f -> %14.5f   %+10.5f  (%+.3f%%)' % (k, va, vb, vb - va, rel))
        print('     bb  %s' % ['%.2f' % x for x in a['bb']])
        print('     ->  %s' % ['%.2f' % x for x in b['bb']])
        print('     feat %s' % ['%.4f' % x for x in a['feat']])
        print('     ->   %s' % ['%.4f' % x for x in b['feat']])
