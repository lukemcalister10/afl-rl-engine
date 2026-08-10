import pickle, numpy as np, json
from collections import defaultdict
from a1_lib import load, SC

S = pickle.load(open(SC+'v0surf_branch.pkl','rb'))['3e8e50de51030297c99cf367161c161f']
G = list(range(1,91)); L = np.log(G)
A = {int(k): float(v) for k, v in json.load(open(SC+'pvc2.json'))['curve'].items()}
POS = ['MID','KPF','KPD','SF','SD','RUCK']

def star(pos, ag, pk):
    a = int(min(max(ag,16),30)); lp = np.log(min(max(pk,1),90))
    if a <= 18: return float(np.interp(lp, L, S['c18']['%s|%d'%(pos,a)]))
    surf = S['surfR'] if pos == 'RUCK' else S['surfN']
    return float(np.interp(lp, L, surf['%s|%d'%(pos,a)]))

# ---- 1. SURFACE-LEVEL INVERSION MAP over picks 1..64 -------------------------------------
inv = []
for pos in POS:
    for ag in range(16,31):
        for p in range(1,64):
            a, b = star(pos,ag,p), star(pos,ag,p+1)
            if b > a + 1e-9:
                inv.append(dict(pos=pos, age=ag, p=p, q=p+1, v_p=round(a,2), v_q=round(b,2),
                                rise=round(b-a,2), pct=round(100*(b/a-1),3),
                                anch_p=A[p], anch_q=A[p+1],
                                anch_ratio=round(A[p+1]/A[p],6),
                                lens_p=round(a/A[p],6), lens_q=round(b/A[p+1],6),
                                lens_ratio=round((b/A[p+1])/(a/A[p]),6)))
json.dump(inv, open(SC+'inv_surface.json','w'), indent=1)
print('SURFACE INVERSIONS (pos x age x adjacent pick, picks 1-64):', len(inv))
print('by position:', {p: sum(1 for x in inv if x['pos']==p) for p in POS})
print('by seam pick:', sorted(set((x['p'],x['q']) for x in inv)))

# ---- 2. ASSIGN EACH ND RECORD ITS SURFACE CELL --------------------------------------------
recs = load()
cells = {}
unres = []
for x in recs:
    if x['type'] != 'ND' or x.get('pickless'): continue
    if (x.get('epk') or 99) > 64: continue
    cand = []
    for pk in sorted(set(v for v in (x.get('pick'), x.get('raw_pick'), x.get('epk'),
                                     x.get('pick_stored'), x.get('pick_slid')) if v and 1 <= v <= 64)):
        for ag in range(16,31):
            if abs(star(x['pos'],ag,pk) - x['v0']) < 0.051:
                cand.append((ag,pk))
    if not cand: unres.append(x); continue
    # prefer the candidate whose age is closest to the recorded age_draft, pick closest to epk
    ad = x['age_draft'] if x['age_draft'] is not None else 18
    cand.sort(key=lambda t: (abs(t[0]-ad), abs(t[1]-(x.get('epk') or 0))))
    cells[x['key'] + '|' + str(x['year'])] = (x, cand[0][0], cand[0][1])
print('ND 1-64 records placed on the surface:', len(cells), ' unresolved:', len(unres))
for x in unres[:10]:
    print('   unresolved', x['key'], x['year'], x['pos'], x['age_draft'], x['pick'], x['epk'], x['v0'])

# ---- 3. PLAYER-LEVEL ADJACENT INVERSIONS --------------------------------------------------
grp = defaultdict(list)
for k,(x,ag,pk) in cells.items():
    grp[(x['pos'],ag)].append((pk,x))
out = []
for key in sorted(grp):
    lst = sorted(grp[key], key=lambda t: t[0])
    picks = sorted(set(p for p,_ in lst))
    for i in range(len(picks)-1):
        p, q = picks[i], picks[i+1]
        vp = star(key[0],key[1],p); vq = star(key[0],key[1],q)
        if vq > vp + 1e-9:
            earlier = [x for pp,x in lst if pp == p]
            later   = [x for pp,x in lst if pp == q]
            out.append(dict(pos=key[0], age=key[1], p=p, q=q, v_p=round(vp,1), v_q=round(vq,1),
                            rise=round(vq-vp,1), pct=round(100*(vq/vp-1),2),
                            earlier=[(e['player'], e['year']) for e in earlier],
                            later=[(e['player'], e['year']) for e in later]))
json.dump(out, open(SC+'inv_players.json','w'), indent=1)
print()
print('PLAYER-LEVEL ADJACENT INVERSIONS:', len(out))
for o in out:
    print('%-5s age%-3d pick %2d -> %2d   %8.1f -> %8.1f  (+%.1f, +%.2f%%)' %
          (o['pos'],o['age'],o['p'],o['q'],o['v_p'],o['v_q'],o['rise'],o['pct']))
    print('        earlier(lower price): ' + '; '.join('%s %d'%t for t in o['earlier']))
    print('        later  (higher price): ' + '; '.join('%s %d'%t for t in o['later']))
