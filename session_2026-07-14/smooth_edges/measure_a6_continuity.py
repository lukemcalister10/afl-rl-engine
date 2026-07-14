import sys; sys.path.insert(0,'/tmp/smooth')
import load; sys.path.insert(0,'/tmp/smooth'); import overlay, copy, numpy as np
G=load.G; MA=G['MA']; ev=G['ev']; cp=G['cp']; F=1.0524
reals=[p for p in MA.data if G['_isreal'](p)]
# A6: for each real player, sweep his LAST-season game count across the old boundaries {5,7,9,11,13} extra
# to probe the nqual 10-bar and thin-season edges; flag any 3-game step > 20%.
# Practical: for players with a recent thin/edge season, vary that season's games +/-3 and check value step.
# We sweep the in-progress (2026) season games from 0..14 in steps that change career games by 3, for
# players who HAVE a 2026 season, and report max 3-game step.
def num(p): return round(ev(p)/F)
def sweep_last(p, span=(0,3,6,9,12)):
    vals=[]
    for g in span:
        q=copy.deepcopy(p); sc=[x for x in q['scoring'] if x['year']!=2026]
        # use his real 2026 avg if present else career-ish; keep avg fixed, vary games
        av=next((x['avg'] for x in p['scoring'] if x['year']==2026), None)
        if av is None:
            av=float(np.mean([x['avg'] for x in p['scoring'] if x['games']>0]) or 0)
        if g>0: sc=sc+[{'year':2026,'games':g,'avg':av}]
        q['scoring']=sc; vals.append(num(q))
    return vals,span
def maxstep(vals,span):
    m=0; wg=None
    for i in range(len(vals)-1):
        dg=span[i+1]-span[i]
        if dg<=3 and max(vals[i],vals[i+1])>50:  # ignore tiny-value noise
            step=abs(vals[i+1]-vals[i])/max(vals[i],vals[i+1])
            if step>m: m=step; wg=(span[i],span[i+1],vals[i],vals[i+1])
    return m,wg

def run(cfg,label,names):
    overlay.apply(G,cfg)
    print(f'--- {label} ---')
    for nm in names:
        c=[p for p in MA.data if p['player']==nm] or [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
        if not c: print(f'  {nm}: NOT FOUND'); continue
        p=c[0]; vals,span=sweep_last(p); m,wg=maxstep(vals,span)
        print(f'  {nm:20s} sweep(0/3/6/9/12g 2026)={vals} maxstep={m*100:.0f}% at {wg}')
    overlay.apply(G,{'f1':False,'f2':False,'f3':False})

names=['Jamarra Ugle-Hagan','Nick Blakey','Timothy English','Tristan Xerri','Max Holmes','Bailey Smith','Harley Reid','Marcus Bontempelli']
run({'f1':False,'f2':False,'f3':False},'BASE',names)
run({'f1':True,'f2':True,'f3':True},'F1+F2+F3',names)

# Board-wide A6: count real players whose 2026-season +/-3g sweep steps >20% (BASE vs ALL)
def board_scan(cfg):
    overlay.apply(G,cfg); steppers=[]
    for p in reals:
        # only players with an actual 2026 season or on the thin/proven edge (nqual 2-4)
        nq=G['_nqual'](p,2026)
        if nq>4: continue
        vals,span=sweep_last(p); m,wg=maxstep(vals,span)
        if m>0.20: steppers.append((p['player'],round(m*100),wg))
    overlay.apply(G,{'f1':False,'f2':False,'f3':False})
    return steppers
sb=board_scan({'f1':False,'f2':False,'f3':False}); sa=board_scan({'f1':True,'f2':True,'f3':True})
print(f'\nBOARD A6 (nqual<=4 pop): BASE steppers>20%={len(sb)}  ALL steppers>20%={len(sa)}')
print('  worst BASE:', sorted(sb,key=lambda t:-t[1])[:5])
print('  worst ALL :', sorted(sa,key=lambda t:-t[1])[:5])
print('A6_DONE')
