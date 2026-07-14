import sys; sys.path.insert(0,'/tmp/smooth')
import load; sys.path.insert(0,'/tmp/smooth')
import overlay, json, hashlib, copy, numpy as np
G=load.G; MA=G['MA']; ev=G['ev']; cp=G['cp']; F=1.0524
reals=[p for p in MA.data if G['_isreal'](p)]
def num(p): return round(ev(p)/F)
def board(): return {p['key']: num(p) for p in reals}
def bmd5(b): return hashlib.md5(json.dumps({k:b[k] for k in sorted(b)}).encode()).hexdigest()[:8]
def nseas(p): return sum(1 for x in p['scoring'] if x['games']>=6 and x['year']<=2026)

CFGS=[('BASE',{'f1':False,'f2':False,'f3':False}),
      ('F1',{'f1':True,'f2':False,'f3':False}),
      ('F2',{'f1':False,'f2':True,'f3':False}),
      ('F3',{'f1':False,'f2':False,'f3':True}),
      ('F1+F2+F3',{'f1':True,'f2':True,'f3':True})]
boards={}
for name,cfg in CFGS:
    overlay.apply(G,cfg)
    boards[name]=board()
    print(f'[{name}] ev/F board-md5={bmd5(boards[name])}')
overlay.apply(G,{'f1':False,'f2':False,'f3':False})
base=boards['BASE']

# per-fix effect: movers + net SCAR + by-band
print('\n=== PER-FIX EFFECT (ev/F, board vs BASE 3dc19fbb store 340a7a32) ===')
bands={}
for name,_ in CFGS[1:]:
    b=boards[name]
    dif=[(k,b[k]-base[k]) for k in base if b[k]!=base[k]]
    net=sum(d for _,d in dif); up=sum(1 for _,d in dif if d>0); dn=sum(1 for _,d in dif if d<0)
    print(f'{name:10s} movers={len(dif):4d} (up {up}, down {dn}) netSCAR={net:+d}')
# A2 net SCAR by season band
print('\n=== A2 NET SCAR BY SEASON BAND (nseas 1..9) ===')
keyseas={p['key']:min(nseas(p),9) for p in reals}
hdr='band '+' '.join(f'{n:>9s}' for n in ['F1','F2','F3','ALL'])
print('band   n_players     F1        F2        F3       ALL')
for sb in range(1,10):
    ks=[k for k in base if keyseas.get(k)==sb]
    row=[]
    for name in ['F1','F2','F3','F1+F2+F3']:
        b=boards[name]; row.append(sum(b[k]-base[k] for k in ks))
    print(f'{sb:3d}  {len(ks):8d}  '+' '.join(f'{v:+9d}' for v in row))

# A1 Jamarra sweep across career games (vary 2026 cameo games; and 2024 to hit 60/64/67/70/74)
print('\n=== A1 JAMARRA career-game sweep ===')
jam=load.find('jamarra')
# construct records to hit target total career games. Base(no2026)=67; add 2026 games g26 -> 67+g26.
# also drop below 67 by trimming 2024 games. Build states at totals 60,64,67,70,74.
def jam_with(total):
    p=copy.deepcopy(jam)
    base_no26=[x for x in p['scoring'] if x['year']!=2026]  # 67 games
    cur=sum(x['games'] for x in base_no26)  # 67
    if total>=cur:
        g26=total-cur
        sc=base_no26+([{'year':2026,'games':g26,'avg':26.0}] if g26>0 else [])
    else:
        # trim 2024 games down
        need=cur-total
        sc=[]
        for x in base_no26:
            x=dict(x)
            if x['year']==2024: x['games']=max(1,x['games']-need)
            sc.append(x)
    p['scoring']=sc
    return p
for name in ['BASE','F1','F2','F3','F1+F2+F3']:
    overlay.apply(G,dict(zip(['f1','f2','f3'],[name!='BASE' and 'f1' in name.lower() or name=='F1' or 'F1' in name, False,False])) if False else next(c for n,c in CFGS if n==name))
    vals=[]
    for tot in [60,64,67,70,74]:
        vals.append(round(ev(jam_with(tot))/F))
    # max 3-game step %
    steps=[]
    tots=[60,64,67,70,74]
    for i in range(len(tots)-1):
        d=abs(tots[i+1]-tots[i]); 
        if vals[i]>0:
            steps.append(100*abs(vals[i+1]-vals[i])/max(vals[i],1)/max(d/3,1))
    print(f'{name:10s} '+' '.join(f'{t}g:{v}' for t,v in zip(tots,vals)))
overlay.apply(G,{'f1':False,'f2':False,'f3':False})

# A3 / A4 named players
print('\n=== A3 Blakey/English/Wilmot/Berry & A4 improvers (ev/F) ===')
names_a3=['Nick Blakey','Timothy English','Darcy Wilmot','Joe Berry']
names_a4=['Xerri','Max Holmes','Lachlan Ash','Bailey Smith','Callaghan','Wilmot']
def getp(nm):
    c=[p for p in MA.data if p['player']==nm]
    if c: return c[0]
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
allnames=names_a3+['Tristan Xerri','Max Holmes','Lachlan Ash','Bailey Smith','Jai Newcombe','Darcy Wilmot','Sam Wicks']
seen=set(); rowps=[]
for nm in ['Nick Blakey','Timothy English','Darcy Wilmot','Joe Berry','Tristan Xerri','Max Holmes','Lachlan Ash','Bailey Smith']:
    p=getp(nm)
    if p and p['player'] not in seen: seen.add(p['player']); rowps.append(p)
hdr2='%-22s'%'player'+''.join('%9s'%n for n in ['BASE','F1','F2','F3','ALL'])
print(hdr2)
res={}
for name,cfg in CFGS:
    overlay.apply(G,cfg)
    res[name]={p['player']:round(ev(p)/F) for p in rowps}
overlay.apply(G,{'f1':False,'f2':False,'f3':False})
for p in rowps:
    nm=p['player']
    print('%-22s'%nm[:22]+''.join('%9d'%res[n][nm] for n in ['BASE','F1','F2','F3','F1+F2+F3']))
print('\nDONE_measure')
