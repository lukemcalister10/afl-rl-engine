#!/usr/bin/env python3
# ============================================================================
# FLAG-CLUSTER DIAGNOSTIC (a) — M1 BREAKOUT-CREDITING
# State: [BAKED c47cb43d]  main 389ac39.  READ-ONLY on engine/data.
#
# The M1 up-branch (engine _coreM1) credits a PROVEN player (n>=PROVEN_N=4)
# S_M1=0.46 of the recent-over-career gap (Lc-Lo) when:
#     Lc>=Lo  AND  (Lc-Lo)>=TOL_M1=5.0  AND  _radq  (a season within WIN=2yr,
#     games>=G_ADQ=12, avg>Lo).
#   credited level = Lo + 0.46*(Lc-Lo).
#
# This script:
#   * enumerates EVERY player the M1 up-branch hits at Y=2026,
#   * prints identity as ID(key)·pick·cohort(debutyr) — NEVER surname alone
#     (four Picketts in the store; the name-collision guard is load-bearing),
#   * decomposes the gap  SUM-TO-TOTAL:  gap = credited(0.46g) + withheld(0.54g),
#   * classifies the rise SPIKE vs SUSTAINED via an explicit consecutive-year
#     test on adequate (>=12-game) seasons,
#   * re-prices each hit at S_M1 in {0.0, 0.46(baked), 1.0(full)} to put the
#     under-credit in DOLLARS (nonlinear through band/asc/floor; reported as
#     actual re-priced ev, not a level-scaled proxy).
# ============================================================================
import io, contextlib, os, sys, json
ENG = '/home/claude/rl_workspace/rl_after'
OUT = '/home/user/afl-rl-engine/evidence/flags/m1'
os.chdir(ENG)
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']
_lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; _radq=g['_radq']
PROVEN_N=g['PROVEN_N']; TOL_M1=g['TOL_M1']; S_M1=g['S_M1']; G_ADQ=g['G_ADQ']; WIN=g['WIN']
delisted=g['delisted']
Y=2026

def ident(p): return "%-22s pick%-4s cohort%d" % (p['key'], (p['pick'] if p.get('pick') else 'FT'), cp.debutyr(p))

def reprice(p, s):
    """actual ev with M1 persistence credit set to s (clears eval cache)."""
    g['S_M1']=s; MA._pe_clear()
    try: return ev(p, Y)
    finally: pass

def adq_seasons(p):
    """adequate (>=G_ADQ games) seasons, real career years only, sorted by year."""
    return sorted((x['year'], x['games'], x['avg']) for x in p['scoring']
                  if x['games']>=G_ADQ and (cp.debutyr(p)-1)<x['year']<=Y)

def classify(p, Lo):
    """explicit consecutive-year test on adequate seasons.
       nyr_above = # of consecutive MOST-RECENT adequate seasons with avg>Lo.
       asc_run   = length of terminal strictly-increasing run of adequate avgs.
       SUSTAINED iff nyr_above>=2 (rise held >=2 consecutive years above career)."""
    aq=adq_seasons(p)
    avgs=[a for _,_,a in aq]
    nyr_above=0
    for a in reversed(avgs):
        if a>Lo: nyr_above+=1
        else: break
    asc_run=1 if avgs else 0
    for i in range(len(avgs)-1, 0, -1):
        if avgs[i]>avgs[i-1]: asc_run+=1
        else: break
    kind='SUSTAINED' if nyr_above>=2 else 'SPIKE'
    return kind, nyr_above, asc_run, aq

# ---- enumerate M1 up-branch hits ----
hits=[]
g['S_M1']=S_M1; MA._pe_clear()
for p in MA.data:
    if id(p) not in g['_REAL']: continue
    n=_nqual(p,Y)
    if n<PROVEN_N: continue
    Lo=cp._lvl_eff_orig(p,Y); Lc=_lvlcurr(p,Y)
    if Lc<Lo: continue
    gap=Lc-Lo
    if gap<TOL_M1: continue
    if not _radq(p,Y,Lo): continue
    hits.append((p,Lo,Lc,gap,n))

# re-price each hit at the three credits
rows=[]
for p,Lo,Lc,gap,n in hits:
    base=reprice(p,S_M1); zero=reprice(p,0.0); full=reprice(p,1.0)
    kind,nyr,asc,aq=classify(p,Lo)
    credited=S_M1*gap; withheld=(1.0-S_M1)*gap
    rows.append(dict(key=p['key'], ident=ident(p), age=cp._age_asof(p,Y),
                     pos=MA.gfut(p), n=n, Lo=Lo, Lc=Lc, gap=gap,
                     credited=credited, withheld=withheld,
                     m1_lvl=Lo+credited, delist=delisted(p),
                     base=base, zero=zero, full=full,
                     d_credit=base-zero, d_withheld=full-base,
                     kind=kind, nyr=nyr, asc=asc, aq=aq))
g['S_M1']=S_M1; MA._pe_clear()  # restore baked

rows.sort(key=lambda r: -r['d_withheld'])

# ---- report ----
lines=[]
def P(s=''): lines.append(s); print(s)
P("="*92)
P("FLAG (a) M1 BREAKOUT-CREDITING  —  [BAKED c47cb43d]  main 389ac39")
P("engine constants: PROVEN_N=%d  TOL_M1=%.1f  S_M1(credit)=%.2f  G_ADQ=%d  WIN=%d" %
  (PROVEN_N,TOL_M1,S_M1,G_ADQ,WIN))
P("M1 up-branch credited level = Lo + %.2f*(Lc-Lo);  gap = credited + withheld (SUM-TO-TOTAL)" % S_M1)
P("identity = ID(key)·pick·cohort(debutyr).  never surname alone (4 Picketts in store).")
P("="*92)
n_sust=sum(1 for r in rows if r['kind']=='SUSTAINED')
n_spike=sum(1 for r in rows if r['kind']=='SPIKE')
tot_withheld_lvl=sum(r['withheld'] for r in rows)
tot_withheld_usd=sum(r['d_withheld'] for r in rows)
sust=[r for r in rows if r['kind']=='SUSTAINED']
tot_sust_usd=sum(r['d_withheld'] for r in sust)
P("M1 up-branch HITS: %d   (SUSTAINED %d, SPIKE %d)" % (len(rows),n_sust,n_spike))
P("total WITHHELD level (0.54*gap summed): %.1f pts   |   total $ to restore full credit: $%d" %
  (tot_withheld_lvl, tot_withheld_usd))
P("SUSTAINED-and-under-credited: %d players, $%d withheld (full-credit minus baked)" %
  (n_sust, tot_sust_usd))
P("")
P("%-46s %3s %4s %7s %7s %6s %6s %5s | %5s %5s %5s | %s" %
  ("ID·pick·cohort","age","pos","Lo","Lc","gap","cred","with","base","zero","full","class(nyr/asc)"))
P("-"*140)
for r in rows:
    tag=' [DELIST]' if r['delist'] else ''
    P("%-46s %3.0f %4s %7.2f %7.2f %6.2f %6.2f %5.2f | %5d %5d %5d | %s (%d/%d)%s" %
      (r['ident'], r['age'], r['pos'], r['Lo'], r['Lc'], r['gap'], r['credited'],
       r['withheld'], r['base'], r['zero'], r['full'], r['kind'], r['nyr'], r['asc'], tag))

# ---- sum-to-total guard ----
P("")
P("SUM-TO-TOTAL GUARD (level, per player: credited + withheld == gap):")
bad=0
for r in rows:
    if abs((r['credited']+r['withheld'])-r['gap'])>1e-9: bad+=1
P("  checked %d players; mismatches: %d  -> %s" % (len(rows),bad,"PASS" if bad==0 else "BOUNCED"))

# ---- Pickett exemplar full decomposition ----
P("")
P("="*92)
P("PICKETT EXEMPLAR — NAME-COLLISION GUARD (4 Picketts; disambiguate by ID+cohort)")
P("="*92)
for p in sorted((q for q in MA.data if 'pickett' in q['player'].lower()), key=lambda q:cp.debutyr(q)):
    P("  %-18s | ID=%-18s | pick %-3s | cohort %d | pos %-8s | age %.0f" %
      (p['player'], p['key'], (p['pick'] if p.get('pick') else 'FT'), cp.debutyr(p), MA.gfut(p), cp._age_asof(p,Y)))
P("")
ky=next(p for p in MA.data if p['key']=='kysaiah-pickett')
r=next(x for x in rows if x['key']=='kysaiah-pickett')
P("EXEMPLAR = kysaiah-pickett (pick 12, cohort 2020, GEN_FWD, age %.0f)" % r['age'])
P("  adequate (>=12g) season path:")
for yr,gm,a in r['aq']:
    P("     %d: %2dg  avg %.1f  %s" % (yr,gm,a,"(> career Lo)" if a>r['Lo'] else ""))
P("  classify: %s   nyr_above=%d consecutive adequate seasons > Lo, terminal asc_run=%d" %
  (r['kind'], r['nyr'], r['asc']))
P("")
P("  LEVEL decomposition [BAKED c47cb43d]:")
P("     Lo (career, recency-wtd)      = %.2f" % r['Lo'])
P("     Lc (steep-recency current)    = %.2f" % r['Lc'])
P("     gap = Lc - Lo                 = %.2f" % r['gap'])
P("     credited  = 0.46 * gap        = %.2f   -> M1 level = %.2f" % (r['credited'], r['m1_lvl']))
P("     withheld  = 0.54 * gap        = %.2f   (NOT credited)" % r['withheld'])
P("     GUARD: credited + withheld    = %.2f  == gap %.2f  -> %s" %
  (r['credited']+r['withheld'], r['gap'], "PASS" if abs(r['credited']+r['withheld']-r['gap'])<1e-9 else "BOUNCED"))
P("")
P("  DOLLAR decomposition (actual re-priced ev; nonlinear via band/asc/floor):")
P("     ev @ S_M1=0.00 (no credit,  =Lo)   = $%d" % r['zero'])
P("     ev @ S_M1=0.46 (BAKED)             = $%d" % r['base'])
P("     ev @ S_M1=1.00 (full credit, =Lc)  = $%d" % r['full'])
P("     M1 currently ADDS over Lo          = $%d   (base - zero)" % r['d_credit'])
P("     WITHHELD from full credit          = $%d   (full - base)" % r['d_withheld'])
P("     GUARD (dollar): add + withheld     = $%d  == (full - zero) $%d  -> %s" %
  (r['d_credit']+r['d_withheld'], r['full']-r['zero'],
   "PASS" if (r['d_credit']+r['d_withheld'])==(r['full']-r['zero']) else "BOUNCED"))

with open(os.path.join(OUT,'m1_breakout_credit.txt'),'w') as f:
    f.write("\n".join(lines)+"\n")

# machine-readable dump
dump=[{k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items() if k!='aq'} for r in rows]
with open(os.path.join(OUT,'m1_hits.json'),'w') as f:
    json.dump(dict(state='BAKED c47cb43d', main='389ac39',
                   constants=dict(PROVEN_N=PROVEN_N,TOL_M1=TOL_M1,S_M1=S_M1,G_ADQ=G_ADQ,WIN=WIN),
                   n_hits=len(rows), n_sustained=n_sust, n_spike=n_spike,
                   total_withheld_level=round(tot_withheld_lvl,2),
                   total_withheld_usd=tot_withheld_usd,
                   sustained_withheld_usd=tot_sust_usd,
                   hits=dump), f, indent=2)
P("")
P("wrote m1_breakout_credit.txt + m1_hits.json")
