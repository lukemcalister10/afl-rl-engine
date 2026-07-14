import sys; sys.path.insert(0,'/tmp/smooth')
import load; sys.path.insert(0,'/tmp/smooth'); import overlay, copy, numpy as np
G=load.G; MA=G['MA']; ev=G['ev']; cp=G['cp']; F=1.0524
reals=[p for p in MA.data if G['_isreal'](p)]
def num(p): return round(ev(p)/F)
def sweep(p,span=(0,3,6,9,12)):
    avs=[x['avg'] for x in p['scoring'] if x['games']>0]
    if not avs: return None
    av=next((x['avg'] for x in p['scoring'] if x['year']==2026),None)
    if av is None: av=float(np.mean(avs))
    vals=[]
    for g in span:
        q=copy.deepcopy(p); sc=[x for x in q['scoring'] if x['year']!=2026]
        if g>0: sc=sc+[{'year':2026,'games':g,'avg':av}]
        q['scoring']=sc; vals.append(num(q))
    return vals
def mstep(v,span=(0,3,6,9,12)):
    m=0;w=None
    for i in range(len(v)-1):
        if max(v[i],v[i+1])>50:
            s=abs(v[i+1]-v[i])/max(v[i],v[i+1])
            if s>m: m=s;w=(span[i],span[i+1],v[i],v[i+1])
    return m,w
def scan(cfg):
    overlay.apply(G,cfg); out=[]
    for p in reals:
        if G['_nqual'](p,2026)>4: continue
        v=sweep(p)
        if v is None: continue
        m,w=mstep(v)
        if m>0.20: out.append((p['player'],round(m*100)))
    overlay.apply(G,{'f1':False,'f2':False,'f3':False}); return out
sb=scan({'f1':False,'f2':False,'f3':False}); sa=scan({'f1':True,'f2':True,'f3':True})
print('BASE steppers>20%%: %d   F1+F2+F3 steppers>20%%: %d'%(len(sb),len(sa)))
print('worst BASE:',sorted(sb,key=lambda t:-t[1])[:8])
print('worst ALL :',sorted(sa,key=lambda t:-t[1])[:8])
# which players still step under ALL:
print('ALL steppers list:',sorted(sa,key=lambda t:-t[1]))
print('A6BOARD_DONE')
