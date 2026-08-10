import json, statistics as st, random
random.seed(20260810)
DF = 1.0939**3

d = json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/matrix.json'))['recs']
S = [r for r in d if r['type']=='ND' and 2004<=r['year']<=2022 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]

def v4(r): return float(r['vpath'][3]) if len(r['vpath'])>=4 else 0.0
def p0(r): return float(r['vpath'][0])

for r in S:
    r['_w']  = p0(r)                 # year-1 price = the weight
    r['_o']  = v4(r)/DF              # realized discounted year-4 value at the year-1 evaluation
    r['_r']  = r['_o']/r['_w']
    r['_np'] = (r['games_total']==0)
    r['_pk'] = r['peak']/r['v0']
    r['_g2'] = r['games_by'].get('2',0)   # cumulative games by end of year 2 (= year-2 games, since yr1=0)

def eff_n(ws):
    s=sum(ws); return (s*s)/sum(w*w for w in ws) if ws else 0.0

def boot(rows, B=10000):
    ws=[r['_w'] for r in rows]; os_=[r['_o'] for r in rows]
    n=len(rows)
    if n==0: return (float('nan'),)*3
    pt=sum(os_)/sum(ws)
    out=[]
    idx=range(n)
    for _ in range(B):
        sw=0.0; so=0.0
        for _ in idx:
            j=random.randrange(n); sw+=ws[j]; so+=os_[j]
        out.append(so/sw)
    out.sort()
    return pt, out[int(0.025*B)], out[int(0.975*B)-1]

def band(r):
    p=r['pick']
    if p<=12: return '1-12'
    if p<=20: return '13-20'
    if p<=27: return '21-27'
    if p<=35: return '28-35'
    if p<=48: return '36-48'
    return '49-64'

def agecell(r):
    a=r.get('age_draft')
    if a is None: return 'unk'
    if a<=17: return '17'
    if a==18: return '18'
    if a==19: return '19'
    return '20+'

def row(name, rows):
    if not rows: return None
    pt,lo,hi = boot(rows)
    ws=[r['_w'] for r in rows]
    return dict(cell=name, n=len(rows), effn=eff_n(ws), F=pt, lo=lo, hi=hi,
                never=sum(r['_np'] for r in rows)/len(rows),
                medpk=st.median(r['_pk'] for r in rows),
                medr=st.median(r['_r'] for r in rows),
                meanr=st.mean(r['_r'] for r in rows),
                play2=sum(1 for r in rows if r['_g2']>0)/len(rows),
                mass=sum(ws))

def show(title, groups):
    print('\n== '+title)
    print(f"{'cell':<16}{'n':>5}{'effn':>7}{'F':>7}{'CI95':>16}{'clear':>7}{'never':>7}{'medpk':>7}{'medR':>7}{'ply2':>7}{'mass':>9}")
    for name, rows in groups:
        z=row(name, rows)
        if z is None: continue
        clear = 'yes' if (z['hi']<1.0 or z['lo']>1.0) else 'no'
        f8 = clear=='yes' and z['effn']>=35
        print(f"{z['cell']:<16}{z['n']:>5}{z['effn']:>7.1f}{z['F']:>7.3f}  [{z['lo']:.3f},{z['hi']:.3f}]{clear:>7}{z['never']:>7.2f}{z['medpk']:>7.2f}{z['medr']:>7.2f}{z['play2']:>7.2f}{z['mass']:>9.0f}" + ('  F8' if f8 else ''))

def grp(keyf, order=None):
    m={}
    for r in S: m.setdefault(keyf(r), []).append(r)
    ks = order if order else sorted(m)
    return [(k, m[k]) for k in ks if k in m]

show('ALL', [('ALL', S)])
show('POSITION', grp(lambda r: r['pos'], ['KPD','KPF','RUCK','MID','SD','SF']))
show('PICK BAND', grp(band, ['1-12','13-20','21-27','28-35','36-48','49-64']))
show('DRAFT AGE', grp(agecell, ['17','18','19','20+','unk']))
show('KPP vs SMALL', [('KPP(KPD/KPF/RUCK)', [r for r in S if r['pos'] in ('KPD','KPF','RUCK')]),
                      ('SMALL(MID/SD/SF)',  [r for r in S if r['pos'] in ('MID','SD','SF')])])
show('YEAR-2 SPLIT', [('play yr2', [r for r in S if r['_g2']>0]),
                      ('sit yr2',  [r for r in S if r['_g2']==0])])
show('ERA', grp(lambda r: ('2004-2012' if r['year']<=2012 else ('2013-2017' if r['year']<=2017 else '2018-2022'))))
