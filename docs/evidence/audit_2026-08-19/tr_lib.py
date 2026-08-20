"""THE LATE-BAND YEAR-1 TROUGH — shared loader. READ-ONLY.
Population and value_at are the STANDING INSTRUMENTS' OWN, copied so the reading cannot drift."""
import json, os, statistics, math, random

SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
WT=SP+'/tr-wt'
EXPECT_STORE='cb38ef11'; EXPECT_V0SURF='4405cba2b42f'
EXPECT_N=1200; CLASS_CUT=2022; ND_LAST=64; YR_LO=2004
MATRIX_MD5=None
PRIMARY=(2005,2023); MODERN=(2019,2023)
FLOOR_N=5; VTHIN=10; THIN=30

def wend_of(label='ASMCAND'):
    """THE INSTRUMENT'S OWN inclusion cutoff: the last year any row has an observed vpath cell.
    as_bands.py computes this over the FULL matrix and passes it to band_rows as WEND. The cohort
    window (lo..hi) filters the POPULATION only. Getting this wrong is what a first pass got wrong."""
    import json as _j
    full=_j.load(open(SP+'/per_entrant_%s.json'%label))['recs']
    return max(y for r in full for y,v in zip(r.get('yrs') or [],r.get('vpath') or []) if v is not None)

def load(label='ASMCAND'):
    import hashlib
    _p=SP+'/per_entrant_%s.json'%label
    global MATRIX_MD5
    MATRIX_MD5=hashlib.md5(open(_p,'rb').read()).hexdigest()[:8]
    M=json.load(open(_p))
    meta=M['meta']
    assert meta['store_md5']==EXPECT_STORE, meta['store_md5']
    assert meta['v0surf_sig'][:12]==EXPECT_V0SURF
    ND=[r for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
        and 1<=r['pick']<=ND_LAST and YR_LO<=r['year']<=CLASS_CUT]
    assert len(ND)==EXPECT_N, 'ND population %d != %d'%(len(ND),EXPECT_N)
    return meta,ND

def value_at(r,N):
    if N==0: return float(r['v0']),'v0'
    vp=r.get('vpath') or []; yrs=r.get('yrs') or []
    i=N-1
    if i>=len(vp): return 0.0,'ended'
    assert yrs[i]==r['year']+N
    if vp[i] is None: return 0.0,'null'
    return float(vp[i]),'path'

def cohort(r): return r['year']+1

def band_of(pk):
    if 1<=pk<=10: return '1-10'
    if 11<=pk<=20: return '11-20'
    if 21<=pk<=30: return '21-30'
    if 31<=pk<=40: return '31-40'
    if 41<=pk<=64: return '41-64'
    return None

def flag(n):
    if n<FLOOR_N: return 'NONE'
    if n<VTHIN: return 'VERY THIN'
    if n<THIN: return 'THIN'
    return 'ok'

def peak_ratio(r,wend,maxN=7):
    """best value the row reaches over years 1..maxN that are OBSERVED, over v0."""
    v0=float(r['v0'])
    if v0<=0: return None,None
    best=0.0; bn=None
    for N in range(1,maxN+1):
        if r['year']+N>wend: break
        v,_=value_at(r,N)
        if v>best: best=v; bn=N
    return (best/v0 if bn is not None else None), bn

def boot_ci(vals, keys, B=2000, seed=17, q=(5,95)):
    """player-clustered bootstrap of the mean. keys identify the cluster (one row = one player here,
    so the cluster IS the row; kept explicit so the estimand is stated)."""
    if not vals: return (None,None)
    rnd=random.Random(seed); n=len(vals); ms=[]
    for _ in range(B):
        s=[vals[rnd.randrange(n)] for _ in range(n)]
        ms.append(sum(s)/n)
    ms.sort()
    return (ms[int(q[0]/100*B)], ms[int(q[1]/100*B)-1])

def sep_ci(a,b,B=2000,seed=23):
    """difference of means with a paired-resample CI. Returns (diff, lo, hi)."""
    if not a or not b: return (None,None,None)
    rnd=random.Random(seed); ds=[]
    for _ in range(B):
        sa=[a[rnd.randrange(len(a))] for _ in range(len(a))]
        sb=[b[rnd.randrange(len(b))] for _ in range(len(b))]
        ds.append(sum(sa)/len(sa)-sum(sb)/len(sb))
    ds.sort()
    return (sum(a)/len(a)-sum(b)/len(b), ds[int(0.05*B)], ds[int(0.95*B)-1])
