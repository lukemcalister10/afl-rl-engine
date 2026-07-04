#!/usr/bin/env python3
# FLAG (b) DPP forward-eligibility — MERGE + REPORT
# Joins the baked-engine optionality gap and the old-engine forward-eligibility
# premium per DPP (by ID/key), filters YOUNG (age<=24), sorts by old premium.
# Identity is ID(key).pick.cohort throughout — never surname alone.
import json, os
OUT='/home/user/afl-rl-engine/evidence/flags/dpp'
baked=json.load(open(os.path.join(OUT,'dpp_baked.json')))
old=json.load(open(os.path.join(OUT,'dpp_old.json')))
B=baked['rows']; O=old['rows']
YOUNG=24

rows=[]
for k,b in B.items():
    o=O.get(k,{})
    rows.append(dict(**b, v_dual=o.get('v_dual'), v_bare=o.get('v_bare'),
                     prem_fut=o.get('prem_fut'), prem_2nd=o.get('prem_2nd'),
                     gf_bare=o.get('gf_bare')))
young=[r for r in rows if r['age'] is not None and r['age']<=YOUNG]
young.sort(key=lambda r:-(r['prem_fut'] if r['prem_fut'] is not None else -1e9))

lines=[]
def P(s=''): lines.append(s); print(s)
P("="*118)
P("FLAG (b) DPP FORWARD-ELIGIBILITY  —  young dual-position players (age<=%d)" % YOUNG)
P("BAKED  cur$/opt$/dOPT = current(gfut, max-weight) -> optionality(best eligible)  [BAKED c47cb43d]")
P("OLD    prem_fut = value(_fut) - value(bare listed pos)   [reads dual/FUTURE role vs listed]  <- Serong anchor")
P("OLD    prem_2nd = value(_fut) - value([[max-wt,100]])    [SECOND-position blend only, gfut held]")
P("       both OLD cols are [OLD rl_model pre-merge] scale; NEVER subtracted vs baked cols. id = ID.pick.cohort.")
P("baked REPL bars: %s" % baked['repl'])
P("="*118)
P("%-24s %4s %6s %4s %4s | %6s %7s %6s | %7s %8s %8s" %
  ("ID(key)","pick","cohort","FWD","age","cur$","opt$","dOPT","dual$","premFUT","prem2nd"))
P("-"*118)
for r in young:
    fw='FWD' if r['fwd_elig'] else ' - '
    def fmt(x): return ('%+.0f'%x) if x is not None else '-'
    P("%-24s %4s %6d %4s %4.0f | %6d %7d %+6d | %7s %8s %8s" %
      (r['key'], (r['pick'] if r['pick'] else 'FT'), r['cohort'], fw, r['age'],
       r['cur'], r['opt_ev'], r['gap_opt'],
       ('%.0f'%r['v_dual']) if r['v_dual'] is not None else '-',
       fmt(r['prem_fut']), fmt(r['prem_2nd'])))

# aggregates
fwd_young=[r for r in young if r['fwd_elig']]
lift=[r for r in young if r['prem_fut'] and r['prem_fut']>0]
tot_lift=sum(r['prem_fut'] for r in lift)
tot_2nd=sum(r['prem_2nd'] for r in young if r['prem_2nd'])
tot_gapopt=sum(r['gap_opt'] for r in young)
P("")
P("YOUNG DPPs (age<=%d): %d   of which forward-eligible: %d" % (YOUNG,len(young),len(fwd_young)))
P("OLD dual/future-role LIFT (prem_fut>0): %d players, Sigma=+$%.0f   [value the bake's max-weight-only pricing omits]"
  % (len(lift),tot_lift))
P("OLD second-position blend (prem_2nd) net across young: %+d   (near-zero for genuine ties like Serong)" % round(tot_2nd))
P("BAKED optionality gap (dOPT) net across young: %+d   (the only forward-eligibility signal the bake expresses)" % tot_gapopt)

# Serong anchor
P("")
P("="*112)
P("SERONG ANCHOR — name-collision guard (2 Serongs; only ONE is a young DPP)")
P("="*112)
for k in ('jai-serong','caleb-serong'):
    r=next((x for x in rows if x['key']==k),None)
    if not r:
        P("  %s: not a DPP (len(_fut)<=1) — excluded by construction" % k); continue
    P("  %-14s | pick %-3s | cohort %d | age %.0f | elig %s | gfut(max-wt) %s"
      % (r['key'], (r['pick'] if r['pick'] else 'FT'), r['cohort'], r['age'],
         "/".join("%s:%.0f%%"%(gg,w*100) for gg,w in r['egroups'].items()), r['gfut']))
    P("     BAKED [c47cb43d]:  current $%d (as %s)  ->  optionality best $%d (as %s)  =  gap +$%d"
      % (r['cur'], r['gfut'], r['opt_ev'], r['opt_best'], r['gap_opt']))
    P("     OLD [rl_model]:    value(dual)=$%.0f  |  value(bare listed pos %s)=$%.0f  ->  prem_fut +$%.0f"
      % (r['v_dual'], r['gf_bare'], r['v_bare'], r['prem_fut']))
    P("                        value([[max-wt,100]])=%s (gfut held) -> prem_2nd %s"
      % (('$%.0f'%(r['v_dual']-r['prem_2nd'])) if r['prem_2nd'] is not None else '-',
         ('+$%.0f'%r['prem_2nd']) if r['prem_2nd'] is not None else '-'))
jai=next(x for x in rows if x['key']=='jai-serong')
P("")
P("  ANCHOR RECONCILIATION: task cites Serong ~+$320 raw.  jai-serong (pick 53, cohort 2022, listed KEY_DEF,")
P("  _fut=GDEF/MID) carries an OLD-engine dual/future-role LIFT of +$%.0f: value(dual)=$%.0f vs value(bare" % (jai['prem_fut'], jai['v_dual']))
P("  listed KEY_DEF)=$%.0f. His stored _vpt=377 == value(dual). The SECOND-position blend (prem_2nd=+$%.0f)" % (jai['v_bare'], jai['prem_2nd']))
P("  is ~zero — the lift is the engine reading his dual/forward role off the bare key-defender tag, not a")
P("  blend. The BAKE DROPPED this: futblend + dual-premium are gone (gfut is the sole _fut reader), so the")
P("  baked engine credits Serong only +$%d (optionality). ~$%.0f of forward/dual-eligibility value is now unpriced."
  % (jai['gap_opt'], jai['prem_fut']-jai['gap_opt']))

with open(os.path.join(OUT,'dpp_forward_eligibility.txt'),'w') as f:
    f.write("\n".join(lines)+"\n")
with open(os.path.join(OUT,'dpp_merged.json'),'w') as f:
    json.dump(dict(young_cutoff=YOUNG, n_young=len(young), n_fwd_young=len(fwd_young),
                   n_lifted=len(lift), sum_prem_fut_lift=round(tot_lift,1),
                   sum_prem_2nd_young=round(tot_2nd,1),
                   sum_baked_optgap_young=tot_gapopt, rows=young), f, indent=2)
P("")
P("wrote dpp_forward_eligibility.txt + dpp_merged.json")
