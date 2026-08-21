"""DRIFT ON THE BAND'S OWN TRAINING ROWS — fit-era store (2026-07-15 b1fd0bce, the store the
pickle's own init_ constants identify) vs the current store (b745002e), restricted to the 1,929
players the band trains on and to the attributes a training row actually reads."""
import json,os,collections
import numpy as np
S=os.environ['STUDY']; OUT=os.path.join(S,'out')
OLD=json.load(open(os.path.join(OUT,'stores','2026-07-15_0cf723a.json')))
NEW=json.load(open('/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'))
d=np.load(os.path.join(OUT,'design.npz'),allow_pickle=True)
train_keys=set(d['key'].astype(str).tolist())
VOCAB={'MID':'MID','GFWD':'SF','GDEF':'SD','KFWD':'KPF','KDEF':'KPD','RUC':'RUCK','DEF':'SD'}
def norm(v): return VOCAB.get(v,v)
O={p['key']:p for p in OLD if p.get('key')}
if len(O)<10:   # older schema may key differently
    O={((p.get('player') or '').lower(),p.get('year')):p for p in OLD}
    getold=lambda p: O.get(((p.get('player') or '').lower(),p.get('year')))
else:
    getold=lambda p: O.get(p.get('key')) or None
c=collections.Counter(); ex=collections.defaultdict(list); matched=0
for p in NEW:
    if p.get('key') not in train_keys: continue
    q=getold(p)
    if q is None: c['UNMATCHED']+=1; ex['UNMATCHED'].append(p.get('player')); continue
    matched+=1
    fa=norm(q.get('future_position') or q.get('drafted_position') or q.get('pos'))
    fb=norm(p.get('future_position') or p.get('present_position') or p.get('drafted_position'))
    if fa!=fb: c['position_semantic']+=1; ex['position_semantic'].append((p['player'],fa,fb))
    if q.get('pick')!=p.get('pick'): c['pick']+=1; ex['pick'].append((p['player'],q.get('pick'),p.get('pick')))
    if q.get('type')!=p.get('type'): c['entry_type']+=1; ex['entry_type'].append((p['player'],q.get('type'),p.get('type')))
    if (q.get('_bd') or None)!=(p.get('_bd') or None): c['DOB']+=1; ex['DOB'].append((p['player'],q.get('_bd'),p.get('_bd')))
    so={x['year']:(x.get('games'),x.get('avg')) for x in (q.get('scoring') or [])}
    sn={x['year']:(x.get('games'),x.get('avg')) for x in (p.get('scoring') or [])}
    diff=sorted(set(so)^set(sn))+sorted(yy for yy in set(so)&set(sn) if so[yy]!=sn[yy])
    pre=[yy for yy in diff if yy<=2021]; post=[yy for yy in diff if yy>2021]
    if pre: c['scoring_pre2022_players']+=1; c['scoring_pre2022_seasons']+=len(pre); ex['scoring_pre2022'].append((p['player'],sorted(pre)))
    if post: c['scoring_post2021_players']+=1; c['scoring_post2021_seasons']+=len(post)
    if diff: c['scoring_any_players']+=1
c['MATCHED_TRAINING_PLAYERS']=matched
out=dict(counts=dict(c), examples={k:v[:10] for k,v in ex.items()},
         totals={k:len(v) for k,v in ex.items()},
         fit_era_store='b1fd0bce (git 0cf723a, 2026-07-15) - identified by the pickles own init_ constants',
         current_store='b745002e (git b7ec627, 2026-08-20)')
json.dump(out,open(os.path.join(OUT,'fitera_drift.json'),'w'),indent=1,default=str)
print('training players matched: %d of %d'%(matched,len(train_keys)))
for k,v in sorted(c.items(),key=lambda kv:-kv[1]): print('  %-30s %5d'%(k,v))
print()
for k in ('DOB','position_semantic','pick','entry_type','scoring_pre2022'):
    if ex.get(k):
        print('%s (%d):'%(k,len(ex[k])))
        for e in ex[k][:6]: print('   ',e)
