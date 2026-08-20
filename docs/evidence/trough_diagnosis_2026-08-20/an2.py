import json, sys
d = json.load(open(sys.argv[1]))
for nm in d:
    R = d[nm]['rows']
    print('=' * 110)
    print(nm)
    print('%5s %8s %9s %9s %9s %9s %9s | %s' % ('sc', 'avg', 'v', 'price6', 'raw_ev', 'prod', 'lvl_eff', 'bb (6 quantiles)'))
    for r in R:
        if r['score'] % 2:
            continue
        print('%5d %8.3f %9.2f %9.2f %9.2f %9.2f %9.4f | %s' %
              (r['score'], r['avg'], r['v_board'], r['price6'], r['raw_ev'], r['prod_path'], r['lvl_eff'],
               ' '.join('%6.2f' % x for x in r['bb'])))
