import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
W0 = json.load(open(os.path.join(HERE, '../order33_w5_2026-08-17/RESULTS_W5.json')))
WC = json.load(open(os.path.join(HERE, 'RESULTS_W5_O32RFINAL.json')))
WB = json.load(open(os.path.join(HERE, 'RESULTS_W5_O33B.json')))


def cells(W, store, key):
    d = W[store][key]['cells']
    return {int(a): (c.get('B'), c.get('B_ci'), c.get('called')) for a, c in d.items()
            if isinstance(c, dict) and 'B' in c}


def show(title, store, key, ages=(27, 28, 29, 30, 31)):
    print(title)
    for a in ages:
        b0 = cells(W0, store, key).get(a)
        bc = cells(WC, store, key).get(a)
        bb = cells(WB, store, key).get(a)
        if not (b0 and bc and bb):
            print('  %d  (unscored somewhere)' % a)
            continue
        print('  %d   W5(C31) %5.2f   control %5.2f   built %5.2f  ci=%s  called=%s' % (
            a, b0[0], bc[0], bb[0], bb[1], bb[2]))


show('TALL|survivor B (the called bias):', 'positions', 'pos:TALL|survivor')
show('TALL|full B:', 'positions', 'pos:TALL|full')
show('STAR tier|survivor B (the preservation exhibit):', 'tiers', 'tier:star|survivor')
show('ROLE tier|survivor B:', 'tiers', 'tier:role|survivor')
show('RUCK|full B (keep check):', 'positions', 'pos:RUCK|full', ages=(27, 28, 29, 30))
show('ALL|full B:', 'bias', 'ALL|full')
show('SMALL|full B:', 'positions', 'pos:SMALL|full')
