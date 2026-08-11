import json, random
from statistics import NormalDist
SC = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/'
D = 1.0939
random.seed(991)
rows = json.load(open(SC+'s6rows_branch.json'))
y1 = [x for x in rows if x['N'] == 1 and x['nd'] and 1 <= x['pk'] <= 64]
# year-0 counterpart on the SAME population: v(C+4)=F*D**3 ; F0 = v(C+4)/D**4 / v0
for x in y1:
    x['v4d'] = x['F']*(D**3)/D          # = v(C+4)/D**4
nd = NormalDist()

def aggF0(S):
    return sum(x['v4d'] for x in S)/sum(x['v0'] for x in S)

def aggF1(S):
    return sum(x['F'] for x in S)/sum(x['price'] for x in S)

def effn(S, k='v0'):
    w = [x[k] for x in S]
    return sum(w)**2/sum(t*t for t in w)

def ci(S, num, den, B=20000):
    n = len(S)
    a = [num(x) for x in S]; b = [den(x) for x in S]
    reps = []
    ri = random.randrange
    for _ in range(B):
        u = 0.0; v = 0.0
        for _ in range(n):
            j = ri(n); u += a[j]; v += b[j]
        reps.append(u/v)
    reps.sort()
    th = sum(a)/sum(b)
    nl = sum(1 for t in reps if t < th) or 1
    if nl == B: nl = B-1
    z0 = nd.inv_cdf(nl/B)
    ta = sum(a); tb = sum(b)
    jk = [(ta-a[i])/(tb-b[i]) for i in range(n)]
    m = sum(jk)/n; d = [m-t for t in jk]
    s2 = sum(t*t for t in d); s3 = sum(t**3 for t in d)
    acc = s3/(6*s2**1.5) if s2 > 0 else 0.0
    out = []
    for al in (0.025, 0.975):
        za = nd.inv_cdf(al)
        adj = z0 + (z0+za)/(1-acc*(z0+za))
        p = min(max(nd.cdf(adj), 1.0/B), 1-1.0/B)
        out.append(reps[int(p*(B-1))])
    return out

print('cell                 n   effn   F1(yr1 filed)   F0(yr0)  CI0                verdict0   miss/pl  totmiss')
def line(lbl, S):
    if len(S) < 6: return
    f1 = aggF1(S); f0 = aggF0(S)
    lo, hi = ci(S, lambda x: x['v4d'], lambda x: x['v0'])
    v = 'OVERPRICED' if hi < 1 else ('UNDERPRICED' if lo > 1 else 'honest')
    tm = sum(x['v0'] for x in S) - sum(x['v4d'] for x in S)
    print('%-18s %4d %6.1f      %7.4f   %7.4f  [%.3f,%.3f]  %-12s %+8.1f %+9.0f'
          % (lbl, len(S), effn(S), f1, f0, lo, hi, v, tm/len(S), tm))

line('ND1-64 y1leg ALL', y1)
for p in ['MID', 'SF', 'SD', 'KPF', 'KPD', 'RUCK']:
    line(p, [x for x in y1 if x['pos'] == p])
for lo_, hi_, nm in [(1,10,'pick 1-10'),(11,20,'pick 11-20'),(21,40,'pick 21-40'),(41,64,'pick 41-64')]:
    line(nm, [x for x in y1 if lo_ <= x['pk'] <= hi_])
line('age <=18', [x for x in y1 if x['age'] is not None and x['age'] <= 18])
line('age 19-20', [x for x in y1 if x['age'] is not None and 19 <= x['age'] <= 20])
line('age 21+', [x for x in y1 if x['age'] is not None and x['age'] >= 21])
line('age unknown', [x for x in y1 if x['age'] is None])
print()
print('KPD detail')
K = [x for x in y1 if x['pos'] == 'KPD']
for x in sorted(K, key=lambda t: t['pk']):
    print('  %-28s C=%d pk=%-3d v0=%8.1f v1=%8.1f v4disc=%8.1f F0=%6.3f' % (x['key'], x['C'], x['pk'], x['v0'], x['price'], x['v4d'], x['v4d']/x['v0']))
