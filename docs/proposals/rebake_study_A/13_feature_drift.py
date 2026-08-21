"""FEATURE-LEVEL DRIFT — not "how many store columns changed", but "how many of the eleven numbers
the band actually reads would be different if it were refitted today". A rookie pick that moved
from 5 to 4 does NOT move the band, because every pool entrant is pinned at effpk = POOL_PICK = 65.
An absent date of birth that became a real one DOES move it, because _age_asof falls back to a
GUESSED age (18 + years since debut) when the store carries none."""
import json,os,collections
import numpy as np
S=os.environ['STUDY']; OUT=os.path.join(S,'out')
OLD={};
for p in json.load(open(os.path.join(OUT,'stores','2026-07-15_0cf723a.json'))):
    if p.get('key'): OLD[p['key']]=p
NEW={p['key']:p for p in json.load(open('/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'))}
d=np.load(os.path.join(OUT,'design.npz'),allow_pickle=True)
keys=d['key'].astype(str); uniq=sorted(set(keys.tolist()))
VOCAB={'MID':'MID','GFWD':'SF','GDEF':'SD','KFWD':'KPF','KDEF':'KPD','RUC':'RUCK','DEF':'SD'}
POOL_PICK=65; ND_LAST=64
def effpk(p):
    t,pk=p.get('type'),p.get('pick') or 0
    if t=='ND' and 1<=pk<=ND_LAST: return pk
    return POOL_PICK
def dob(p): return p.get('_bd') or None
def byr(p): return p.get('_by') or None
def pos(p): return VOCAB.get(p.get('future_position') or p.get('present_position') or p.get('drafted_position') or p.get('pos'),
                            p.get('future_position') or p.get('present_position') or p.get('drafted_position') or p.get('pos'))
c=collections.Counter(); ex=collections.defaultdict(list)
for k in uniq:
    a,b=OLD.get(k),NEW.get(k)
    if a is None or b is None: c['unmatched']+=1; continue
    c['matched']+=1
    if effpk(a)!=effpk(b): c['FEATURE effpk (log pick)']+=1; ex['effpk'].append((b['player'],effpk(a),effpk(b)))
    if pos(a)!=pos(b): c['FEATURE position one-hot']+=1; ex['pos'].append((b['player'],pos(a),pos(b)))
    da,db=dob(a),dob(b)
    if da!=db:
        if da is None and db is not None:
            c['FEATURE age: GUESSED -> real DOB']+=1; ex['age_fill'].append(b['player'])
        elif da is not None and db is None: c['FEATURE age: real -> guessed']+=1
        else: c['FEATURE age: DOB corrected']+=1; ex['age_corr'].append((b['player'],da,db))
    so={x['year']:(x.get('games'),x.get('avg')) for x in (a.get('scoring') or [])}
    sn={x['year']:(x.get('games'),x.get('avg')) for x in (b.get('scoring') or [])}
    diff=sorted(set(so)^set(sn))+sorted(y for y in set(so)&set(sn) if so[y]!=sn[y])
    if [y for y in diff if y<=2021]: c['FEATURE+TARGET pre-2022 scoring']+=1
    if [y for y in diff if y>2021]:  c['FEATURE+TARGET post-2021 scoring']+=1
    if diff: c['any scoring change']+=1
n=c['matched']
print('band training players matched: %d\n'%n)
for k,v in sorted(c.items(),key=lambda kv:-kv[1]):
    if k in ('matched','unmatched'): continue
    print('  %-38s %5d  (%5.1f%% of training players)'%(k,v,100.0*v/n))
print('\n  UNCHANGED on every read attribute: ', end='')
unch=sum(1 for k in uniq if OLD.get(k) and NEW.get(k)
         and effpk(OLD[k])==effpk(NEW[k]) and pos(OLD[k])==pos(NEW[k]) and dob(OLD[k])==dob(NEW[k])
         and {x['year']:(x.get('games'),x.get('avg')) for x in (OLD[k].get('scoring') or [])}
          =={x['year']:(x.get('games'),x.get('avg')) for x in (NEW[k].get('scoring') or [])})
print('%d of %d (%.1f%%)'%(unch,n,100.0*unch/n))
print('\nexamples:')
for k in ('effpk','pos','age_corr'):
    if ex.get(k): print(' %s (%d):'%(k,len(ex[k])), ex[k][:8])
if ex.get('age_fill'): print('  age GUESSED->real (%d), e.g.'%len(ex['age_fill']), ex['age_fill'][:8])
json.dump(dict(counts=dict(c),unchanged=unch,examples={k:v[:20] for k,v in ex.items()}),
          open(os.path.join(OUT,'feature_drift.json'),'w'),indent=1,default=str)
