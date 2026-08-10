import lib2, json, numpy as np, collections
FZ = lib2.build('pe_frozen.json'); S5 = lib2.build('pe_stage5.json')
fz = {x['key']: x for x in FZ}
OF, OS = lib2.outc(FZ), lib2.outc(S5)
assert [x['key'] for x in OF] == [x['key'] for x in OS]
Z = lambda x: x['leg'] == 'sit0'; Q = lambda x: x['leg'] == 'quiet'; E = lambda x: x['leg'] == 'established'
CELLS = [
 ('POOL WHOLE',                      lambda x: True),
 ('sitters gy==0 (all)',             Z),
 ('  sit x age<=18',                 lambda x: Z(x) and x['age'] is not None and x['age'] <= 18),
 ('  sit x age 19-20',               lambda x: Z(x) and x['age'] is not None and 19 <= x['age'] <= 20),
 ('  sit x age 21-22',               lambda x: Z(x) and x['age'] is not None and 21 <= x['age'] <= 22),
 ('  sit x age 23+',                 lambda x: Z(x) and x['age'] is not None and x['age'] >= 23),
 ('  sit x age UNKNOWN (RD gap)',    lambda x: Z(x) and x['age'] is None),
 ('  sit x IRE',                     lambda x: Z(x) and x['typ'] == 'IRE'),
 ('  sit x MSD',                     lambda x: Z(x) and x['typ'] == 'MSD'),
 ('  sit x RD',                      lambda x: Z(x) and x['typ'] == 'RD'),
 ('  sit x ND65+',                   lambda x: Z(x) and x['typ'] == 'ND'),
 ('  sit x UNR',                     lambda x: Z(x) and x['typ'] == 'UNR'),
 ('  sit x PDA',                     lambda x: Z(x) and x['typ'] == 'PDA'),
 ('  sit x PDN',                     lambda x: Z(x) and x['typ'] == 'PDN'),
 ('  sit x PDS',                     lambda x: Z(x) and x['typ'] == 'PDS'),
 ('  sit x SSP',                     lambda x: Z(x) and x['typ'] == 'SSP'),
 ('  sit x age21+ ROUTE-POOLED',     lambda x: Z(x) and x['age'] is not None and x['age'] >= 21),
 ('  sit x 23+/IRE/MSD UNION',       lambda x: Z(x) and ((x['age'] is not None and x['age'] >= 23) or x['typ'] in ('IRE', 'MSD'))),
 ('quiet gy>0 (all)',                Q),
 ('  quiet x RD',                    lambda x: Q(x) and x['typ'] == 'RD'),
 ('  quiet x ND65+',                 lambda x: Q(x) and x['typ'] == 'ND'),
 ('  quiet x MSD',                   lambda x: Q(x) and x['typ'] == 'MSD'),
 ('  quiet x IRE',                   lambda x: Q(x) and x['typ'] == 'IRE'),
 ('  quiet x age<=18',               lambda x: Q(x) and x['age'] is not None and x['age'] <= 18),
 ('established (yr1 production)',    E),
]
h = "%-30s %5s %6s | %7s %8s %7s | %8s %8s | %7s %7s" % (
    'cell', 'n', 'eff-n', 'F_froz', 's5 dPrc', 'F_s7', 'CI_lo', 'CI_hi', 'p/A', 'hon/A')
print(h); print('-' * len(h))
OUT = {}
for nm, f in CELLS:
    rs = [x for x in OS if f(x)]; rf = [x for x in OF if f(x)]
    if len(rs) < 2: continue
    Ff, Fs = lib2.aggF(rf), lib2.aggF(rs)
    lo, hi = lib2.ci(rs, B=20000)
    dP = sum(x['v1'] for x in rs) / sum(x['v1'] for x in rf) - 1
    pA = sum(x['v1'] for x in rs) / sum(x['A'] for x in rs)
    hA = sum(x['v4'] for x in rs) / lib2.HURDLE ** 3 / sum(x['A'] for x in rs)
    en = lib2.effn(rs)
    OUT[nm.strip()] = dict(n=len(rs), effn=en, Ffroz=Ff, Fs7=Fs, lo=lo, hi=hi, dP=dP, pA=pA, hA=hA)
    print("%-30s %5d %6.1f | %7.4f %+7.2f%% %7.4f | %8.4f %8.4f | %7.4f %7.4f"
          % (nm, len(rs), en, Ff, 100 * dP, Fs, lo, hi, pA, hA))
json.dump(OUT, open('r1_cells.json', 'w'), indent=1)
print("\ntau convention (measured, live board fe=0.88): non-MSD sitter tau = %.4f ; MSD sitter tau = %.4f"
      % (np.median([x['tau'] for x in S5 if x['leg'] == 'sit0' and x['typ'] != 'MSD' and x['C'] == 2025]),
         np.median([x['tau'] for x in S5 if x['leg'] == 'sit0' and x['typ'] == 'MSD' and x['C'] == 2025] or [float('nan')])))
