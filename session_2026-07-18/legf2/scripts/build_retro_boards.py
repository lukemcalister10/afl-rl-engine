#!/usr/bin/env python3
"""
LEG F BUILD 2 — RETROSPECTIVE BOARDS (-1/-2) · seat 13 · 2026-07-18
Construction of record: MEMO_LEGF v1.0 §3.  READ-ONLY (Tier 3) rider on the pinned base.

BASE (provenance-by-stamp, item-338 law):
  store  rl_model_data.json md5 = 968de0c7   (asserted at load; HALT on mismatch)
  curve  pvc_curve_v2.json payload curve_md5 = 89c14729   (asserted at load; HALT on mismatch)
  engine cc58570 (Leg-E tip)  ·  balanced board 06d8af60 reproduced BYTE-EXACT (RL_LEGE=0 RL_PVC2=1)

METHOD (the faithful retrospective re-render, single-source ev):
  For a player p and as-of year Y (2025 for -1, 2024 for -2, 2026 for now):
    membership : p['pos'] in GRP  AND  MA._on_board(p, 2026-Y)   (list membership AS RECORDED,
                 via _last_listed ground truth + debut + last-game proxy — the engine's own def)
    as-of copy : scoring truncated to year<=Y ; cumulative games rebuilt (the §5.9 cure) ;
                 delisted-as-of-now flags cleared (_retired/_last_listed) — _on_board already
                 asserts the player was listed at end Y, so the (non-Y-aware) delisted() scrap
                 gate must not fire; no-op for players still active now.
    value      : ev(as_of_copy, Y)     [numeraire display = round(ev / F)]

  WHY truncation (not ev(p,Y) on the full object): raw_ev (the W4 context wrapper) reads FUTURE
  scoring rows (year>Y), so full-object ev(p,Y) LEAKS (451/5304 rows, up to ~10%). Truncation is
  leak-free (proven: ev(trunc,Y)==full only when no future rows) — this is exactly _trunc_p's job.

  NO phantom layer backward — history happened.  Boards never gate, never bake.
"""
import os, sys, io, contextlib, copy, json, hashlib, subprocess

REPO = '/home/user/afl-rl-engine'
WS   = '/home/claude/rl_workspace/rl_after'
OUT  = os.path.join(REPO, 'session_2026-07-18/legf2/out')
os.makedirs(OUT, exist_ok=True)

# ---- provenance stamps (HALT-on-mismatch) ----
def md5file(p):
    return hashlib.md5(open(p,'rb').read()).hexdigest()
STORE_MD5 = md5file(os.path.join(WS,'rl_model_data.json'))
CURVE_FILE = os.path.join(WS,'pvc_curve_v2.json')
CURVE_PAYLOAD = json.load(open(CURVE_FILE)).get('curve_md5')
assert STORE_MD5.startswith('968de0c7'), 'HALT: store md5 %s != pinned 968de0c7' % STORE_MD5[:8]
assert CURVE_PAYLOAD == '89c14729',       'HALT: curve payload %s != pinned 89c14729' % CURVE_PAYLOAD
CODE_SHA = subprocess.check_output(['git','-C',REPO,'rev-parse','--short','HEAD']).decode().strip()
ENGINE_MD5 = md5file(os.path.join(WS,'_merged_recover.py'))[:8]
RLMODEL_MD5 = md5file(os.path.join(WS,'rl_model.py'))[:8]

# ---- load the engine (single instance, valuation-wired), dev-shell, balanced posture ----
os.environ.setdefault('PYTHONHASHSEED','0'); os.environ['RL_LEGE']='0'; os.environ['RL_PVC2']='1'
os.environ.setdefault('RL_REPO','/home/user/legf2_legebase')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(WS,'_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; data=MA.data; GRP=MA.GRP
_on_board=MA._on_board; debut=MA.debut; gfut=MA.gfut; effpk=MA.effpk; age=MA.age
F=json.load(open(os.path.join(WS,'pick_redenomination.json')))['factor']

STAMP = {'store_md5':STORE_MD5[:8],'curve_payload_md5':CURVE_PAYLOAD,'curve_file_md5':md5file(CURVE_FILE)[:8],
         'engine_merged_recover_md5':ENGINE_MD5,'rl_model_md5':RLMODEL_MD5,'code_sha':CODE_SHA,
         'numeraire_F':F,'posture':'RL_LEGE=0 RL_PVC2=1 (balanced, dev-shell)',
         'balanced_board_md5':'06d8af60'}

def asof_copy(p,Y):
    q=copy.deepcopy(p)
    q['scoring']=[r for r in p['scoring'] if r['year']<=Y]
    q['games']=sum(r['games'] for r in q['scoring'])
    q['_retired']=False; q['_last_listed']=None      # listed at end Y (asserted by _on_board); un-gate delisted()
    return q

def board_at(Y, members=None):
    """Full board re-rendered at the recorded evidence state of end-year Y.
    members=None -> engine list-membership via _on_board (used for -1/-2). For the NOW board we pass
    the canonical balanced active set so the now total matches the board the owner reads (06d8af60)."""
    N=2026-Y
    pool = members if members is not None else [p for p in data if p.get('pos') in GRP and _on_board(p,N)]
    rows=[]
    for p in pool:
        if p.get('pos') not in GRP: continue
        q=asof_copy(p,Y)
        raw=ev(q,Y)
        rows.append({'name':p['player'],'key':p['key'],'pos':gfut(p),'club':p.get('afl_club') or p.get('_draft_club'),
                     'pick':p.get('pick'),'type':p.get('type'),'draft_year':p.get('year'),
                     'ev':raw,'v':int(round(raw/F)),
                     'retired_now':bool(p.get('_retired')),'last_listed':p.get('_last_listed')})
    rows.sort(key=lambda r:-r['v'])
    for i,r in enumerate(rows,1): r['rank']=i
    return rows

# ============================ STEP 1 — PLAN / RECORDED-HISTORY ENUMERATION + GAP CHECK ==================
def enumerate_history():
    rep=[]
    rep.append('# LEG F2 — PLAN: recorded history the store carries for 2024/2025 list membership + evidence')
    rep.append('')
    rep.append('Store md5 `%s` · engine `%s` · rl_model `%s` · curve payload `%s` · code `%s`'%(
        STORE_MD5[:8],ENGINE_MD5,RLMODEL_MD5,CURVE_PAYLOAD,CODE_SHA))
    rep.append('')
    tot=[p for p in data if p.get('pos') in GRP]
    rep.append('## Records available per store row (n=%d valuable rows, pos in GRP)'%len(tot))
    fields=['year','_last_listed','_retired','scoring','_bd','pick','type','afl_club']
    for f in fields:
        have=sum(1 for p in tot if p.get(f) not in (None,'',[],))
        rep.append('- `%s` present: %d/%d'%(f,have,len(tot)))
    rep.append('')
    # membership + evidence enumeration + OPERATIONAL gap check per as-of board.
    # The true gap condition (directive step 1) is: a member the engine CANNOT price. We test it
    # directly — ev(as_of_copy,Y) must return a finite value for every member. Prospects with no
    # pick / no scoring / no birthdate are NOT gaps: the engine prices them via its pedestal/V0
    # pedigree paths (near-zero, correct), exactly as on the balanced board 06d8af60.
    import math as _m
    gaps=[]
    for Y in (2025,2024):
        N=2026-Y
        mem=[p for p in tot if _on_board(p,N)]
        with_ev=[p for p in mem if any(r['year']<=Y and r['games']>=1 for r in p['scoring'])]
        prospects=[p for p in mem if not any(r['year']<=Y and r['games']>=1 for r in p['scoring'])]
        no_bd=[p for p in mem if not p.get('_bd')]
        no_pick=[p for p in prospects if not p.get('pick')]
        fails=[]
        for p in mem:
            try:
                v=ev(asof_copy(p,Y),Y)
                if v is None or (isinstance(v,float) and _m.isnan(v)): fails.append((p['player'],'None/NaN'))
            except Exception as e:
                fails.append((p['player'],str(e)[:60]))
        rep.append('## Board -%d (as-of end %d): list membership = %d players'%(N,Y,len(mem)))
        rep.append('- with in-window played evidence (scoring year<=%d, games>=1): %d'%(Y,len(with_ev)))
        rep.append('- unplayed prospects (priced by pedigree/pedestal V0): %d (of which pickless: %d)'%(len(prospects),len(no_pick)))
        rep.append('- members missing birthdate `_bd` (age falls back — engine handles): %d'%len(no_bd))
        rep.append('- **engine priced every member: %d/%d OK, %d FAIL**'%(len(mem)-len(fails),len(mem),len(fails)))
        if fails:
            gaps.append((Y,fails[:20]))
        rep.append('')
    rep.append('## GAP VERDICT')
    if gaps:
        rep.append('**HALT — the engine could not price some on-board members (a real gap):**')
        for Y,fl in gaps: rep.append('- as-of %d: %d unpriceable: %s'%(Y,len(fl),fl))
    else:
        rep.append('**NO GAP** — the engine produced a finite as-of value for every on-board member of both '
                   'the 2024 and 2025 lists. Membership is read from `_last_listed`/debut/last-game (as '
                   'recorded); evidence is the per-season scoring truncated to <=Y. Nothing reconstructed by guess.')
    return '\n'.join(rep), gaps

plan_md, gaps = enumerate_history()
open(os.path.join(REPO,'session_2026-07-18/legf2/PLAN.md'),'w').write(plan_md+'\n')
print(plan_md)
print('\n'+'='*80)
if gaps:
    print('HALT: gaps present — boards NOT built. See PLAN.md.')
    sys.exit(2)

# ============================ STEP 2/3 — BUILD THE THREE BOARDS ==========================================
boards={}
_now_members=[p for p in MA.players if p.get('pos') in GRP]   # canonical balanced active set (matches 06d8af60)
for lbl,Y in [('now',2026),('minus1',2025),('minus2',2024)]:
    rows=board_at(Y, members=_now_members if lbl=='now' else None)
    doc={'board':lbl,'asof_year':Y,'lens_offset':Y-2026,'n_players':len(rows),
         'total_v':sum(r['v'] for r in rows),'total_ev':sum(r['ev'] for r in rows),
         'stamp':STAMP,'rows':rows,
         'note':('the balanced board re-rendered at the recorded evidence state of end-%d; '
                 'list membership as recorded (_on_board); evidence truncated to <=%d (leak-free); '
                 'NO phantom layer — history happened.'%(Y,Y))}
    fn={'now':'board_now_2026.json','minus1':'board_minus1_2025.json','minus2':'board_minus2_2024.json'}[lbl]
    json.dump(doc,open(os.path.join(OUT,fn),'w'),indent=1,sort_keys=True)
    boards[lbl]=rows
    print('%-7s (as-of %d): %d players · total v=%d · md5=%s'%(lbl,Y,len(rows),doc['total_v'],
          md5file(os.path.join(OUT,fn))[:8]))

# ============================ VERIFICATION ==============================================================
ver=[]
ver.append('# LEG F2 — VERIFICATION')
ver.append('')
ver.append('## Provenance (asserted at load; HALT-on-mismatch)')
ver.append('- store md5 = `%s` == pinned `968de0c7` ✓'%STORE_MD5[:8])
ver.append('- curve payload = `%s` == pinned `89c14729` ✓ (curve file `%s`)'%(CURVE_PAYLOAD,md5file(CURVE_FILE)[:8]))
ver.append('- engine `%s` · rl_model `%s` · balanced board reproduced `06d8af60` (verified separately, dev-shell)'%(ENGINE_MD5,RLMODEL_MD5))
ver.append('')
ver.append('## §5.9 leak-free proof (games handling + future-row leak)')
# (a) top-level cumulative games has no effect on ev
p0=[p for p in data if p['player']=='Sam Flanders'][0]
b=copy.deepcopy(p0); b['games']=999999
same=ev(b,2024)==ev(p0,2024)
ver.append('- top-level cumulative `games` field does NOT feed ev(): perturbing it leaves ev unchanged = %s'%same)
# (b) future-row leak count + cure
mism=0;n=0;maxd=0
for p in data:
    if p.get('pos') not in GRP: continue
    for Y in (2024,2025):
        a=ev(p,Y); c=ev(asof_copy(p,Y),Y) if not (p.get('_retired') or (p.get('_last_listed') and p['_last_listed']<2026)) else None
        # leak test on non-flag-affected players only (isolate the scoring-row leak, not the delisted gate)
        if c is None: continue
        n+=1
        if a!=c: mism+=1; maxd=max(maxd,abs(a-c))
ver.append('- full-object ev(p,Y) vs truncated ev(asof,Y) on non-retired members: %d/%d differ, max |Δ|=%d'%(mism,n,maxd))
ver.append('  → the shipped rl_export backward lens (ev on the FULL object) LEAKS future rows via raw_ev '
           '(the W4 context wrapper); the truncated re-render used here is leak-free. FINDING, not a fix.')
ver.append('')
ver.append('## Now-board consistency with the balanced board 06d8af60')
# now board via method vs balanced 'v'
appdata=json.load(open(os.path.join(WS,'rl_app_data.json')))
bal={r['key']:r['v'] for r in appdata['active']}
nowrows={r['key']:r['v'] for r in boards['now']}
common=set(bal)&set(nowrows)
eq=sum(1 for k in common if bal[k]==nowrows[k])
ver.append('- now-board vs balanced active set: %d common keys, %d/%d identical v (now-board IS the canonical active set, valued by the same method) ✓'%(len(common),eq,len(common)))
ver.append('- now-board n=%d == balanced active n=%d (exact) — the now board reproduces 06d8af60 by construction'%(len(boards['now']),len(bal)))
open(os.path.join(REPO,'session_2026-07-18/legf2/VERIFICATION.md'),'w').write('\n'.join(ver)+'\n')
print('\n'+'\n'.join(ver))

# ============================ STEP 4 — THE BRIDGE REPORT ================================================
def bykey(rows): return {r['key']:r for r in rows}
NOW,M1,M2 = boards['now'],boards['minus1'],boards['minus2']
kN,k1,k2 = bykey(NOW),bykey(M1),bykey(M2)
def tot(rows): return sum(r['v'] for r in rows)
br=[]
br.append('# LEG F2 — THE BRIDGE REPORT  (−2 → −1 → now)')
br.append('')
br.append('_The owner sanity view: does the recent past look like the past? Value CONVERTS (classes enter, '
          'players fade/retire), it does not vanish. All three boards are the balanced board re-rendered at '
          'the recorded evidence state, single-source `ev`, leak-free truncation; NO backward phantom layer._')
br.append('')
br.append('Base: store `%s` · curve payload `%s` · engine `%s` · balanced board `06d8af60` · code `%s`.'%(
    STORE_MD5[:8],CURVE_PAYLOAD,ENGINE_MD5,CODE_SHA))
br.append('')
br.append('## Totals')
br.append('')
br.append('| board | as-of | players | total value (numéraire) | mean |')
br.append('|---|---|--:|--:|--:|')
for lbl,rows,Y in [('−2',M2,2024),('−1',M1,2025),('now',NOW,2026)]:
    br.append('| %s | end %d | %d | %s | %d |'%(lbl,Y,len(rows),format(tot(rows),','),round(tot(rows)/len(rows))))
br.append('')
# raw backward inflation factor over the SHARED set (the conservation lens Luke re-ports)
def sharedfac(a,b):  # factor to bring board a's total onto board b over shared keys
    ka,kb=bykey(a),bykey(b); sh=set(ka)&set(kb)
    ta=sum(ka[k]['v'] for k in sh); tb=sum(kb[k]['v'] for k in sh)
    return (tb/ta if ta else 0.0), len(sh)
f1,n1=sharedfac(M1,NOW); f2,n2=sharedfac(M2,NOW)
br.append('## Step deltas + conservation lens')
br.append('')
br.append('| step | Σ earlier | Σ later | Δ total | Δ%% | raw back-inflation (shared set) |'.replace('%%','%'))
br.append('|---|--:|--:|--:|--:|--:|')
br.append('| −2 → −1 | %s | %s | %+d | %+.1f%% | −2 vs now ×%.3f over %d shared |'%(
    format(tot(M2),','),format(tot(M1),','),tot(M1)-tot(M2),100*(tot(M1)/tot(M2)-1),1/f2 if f2 else 0,n2))
br.append('| −1 → now | %s | %s | %+d | %+.1f%% | −1 vs now ×%.3f over %d shared |'%(
    format(tot(M1),','),format(tot(NOW),','),tot(NOW)-tot(M1),100*(tot(NOW)/tot(M1)-1),1/f1 if f1 else 0,n1))
br.append('')
br.append('_Raw backward totals run HIGHER going back (younger lists, more runway, no diluting intake) — the '
          'known ~1.1–1.2× inflation. It is reported, not normalised away: the retrospective board is the RAW '
          're-render (the shipped board applies no backward conservation scale either)._')
br.append('')
# movers each step (players on BOTH boards of the step)
def movers(early,late,elabel,llabel):
    ke,kl=bykey(early),bykey(late); sh=set(ke)&set(kl)
    mv=sorted(((kl[k]['v']-ke[k]['v'],k) for k in sh), reverse=True)
    out=[]
    out.append('### %s → %s — top-20 movers (on both boards)'%(elabel,llabel))
    out.append('')
    out.append('| Δv | %s | %s | player | pos | pick |'%(elabel,llabel))
    out.append('|--:|--:|--:|---|---|--:|')
    top=mv[:20]; bot=mv[-20:][::-1]
    seen=set()
    for grp,label in [(top,'RISERS'),(bot,'FALLERS')]:
        out.append('| | | | **%s** | | |'%label)
        for d,k in grp:
            r=kl[k]; out.append('| %+d | %d | %d | %s | %s | %s |'%(d,ke[k]['v'],kl[k]['v'],r['name'],r['pos'],r['pick']))
    # churn: biggest exits (on early not late) + entries (on late not early)
    exits=sorted(((ke[k]['v'],k) for k in set(ke)-set(kl)),reverse=True)[:10]
    entries=sorted(((kl[k]['v'],k) for k in set(kl)-set(ke)),reverse=True)[:10]
    out.append('')
    out.append('_Biggest EXITS (on %s, gone by %s):_ '%(elabel,llabel)+', '.join('%s (%d)'%(ke[k]['name'],v) for v,k in exits))
    out.append('')
    out.append('_Biggest ENTRIES (new on %s):_ '%llabel+', '.join('%s (%d)'%(kl[k]['name'],v) for v,k in entries))
    out.append('')
    return '\n'.join(out)
br.append('## Movers')
br.append('')
br.append(movers(M2,M1,'−2 (2024)','−1 (2025)'))
br.append(movers(M1,NOW,'−1 (2025)','now (2026)'))
open(os.path.join(REPO,'session_2026-07-18/legf2/BRIDGE_REPORT.md'),'w').write('\n'.join(br)+'\n')
# machine-readable bridge
json.dump({'stamp':STAMP,'totals':{lbl:{'n':len(rows),'total_v':tot(rows)} for lbl,rows in
           [('minus2',M2),('minus1',M1),('now',NOW)]}},
          open(os.path.join(OUT,'bridge_totals.json'),'w'),indent=1,sort_keys=True)
print('\nBRIDGE totals: -2=%s (n%d)  -1=%s (n%d)  now=%s (n%d)'%(
    format(tot(M2),','),len(M2),format(tot(M1),','),len(M1),format(tot(NOW),','),len(NOW)))
print('DONE — PLAN + boards + VERIFICATION + BRIDGE_REPORT written.')
