#!/usr/bin/env python3
"""LEG B UNFUNDED — per-point deliverables from two ledger dumps (OFF = RL_UNCOMP=0 == board 8d90c9ac,
ON = RL_UNCONSERVE=1 map at s, C≡1). Produces, per point:
  SINCERITY_all804_s<s>.csv  — id,player,pos,num_off,num_on,delta_scar,delta_pct,rank_off,rank_on,
                               delta_rank,rho_num,rho_ratio,w  (item 256 sincerity ledger, all active rows)
  POINT_s<s>.md              — pool re-rate (Σ Δnum per pos), census/unearned reading, E/B vs 1.75,
                               Bontempelli (SCAR up AND rank up?), top-20 rank gainers/losers,
                               SCAR-up-rank-DOWN roster (sincerity failures), net board SigmaD.
Rank = position by num DESCENDING over the active-804 (rank 1 = highest priced). "rank up" = rank number
falls (Δrank<0). Sincerity failure (item 256) = SCAR rises while rank falls (ΔSCAR>0 AND Δrank>0).
usage: python3 analyze_unfunded.py <off.json> <on.json> <s>
"""
import json, sys, csv, os
OFF = json.load(open(sys.argv[1])); ON = json.load(open(sys.argv[2])); S = sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
ACT = set(r['key'] for r in json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))['active'])
def good(d): return isinstance(d, dict) and 'error' not in d
akeys = [k for k in ON if k in ACT and good(ON.get(k)) and good(OFF.get(k))]

# ranks over the active board (num descending; deterministic tiebreak by key) --------------------------
def ranks(src):
    order = sorted(akeys, key=lambda k: (-src[k]['num'], k))
    return {k: i + 1 for i, k in enumerate(order)}
ro, rn = ranks(OFF), ranks(ON)

rows = []
for k in akeys:
    o, n = OFF[k], ON[k]
    dsc = n['num'] - o['num']; dpct = (100.0 * dsc / o['num']) if o['num'] else 0.0
    drank = rn[k] - ro[k]
    rows.append(dict(key=k, sid=n.get('sid') or '', player=n['player'], pos=n['pos'],
                     num_off=o['num'], num_on=n['num'], dscar=dsc, dpct=round(dpct, 2),
                     rank_off=ro[k], rank_on=rn[k], drank=drank,
                     rho_num=n.get('rho_num'), rho_ratio=n.get('rho_ratio'), w=n.get('w')))
# SINCERITY CSV (all active rows), sorted by delta_scar ascending (biggest cuts first)
csvp = os.path.join(OUT, 'SINCERITY_all804_s%s.csv' % S)
with open(csvp, 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['stable_player_id', 'player', 'pos', 'num_off', 'num_on', 'delta_scar', 'delta_pct',
                 'rank_off', 'rank_on', 'delta_rank', 'rho_num', 'rho_ratio', 'w'])
    for r in sorted(rows, key=lambda r: r['dscar']):
        wr.writerow([r['sid'], r['player'], r['pos'], r['num_off'], r['num_on'], r['dscar'], r['dpct'],
                     r['rank_off'], r['rank_on'], r['drank'], r['rho_num'], r['rho_ratio'], r['w']])

by = {r['key']: r for r in rows}
out = []
def wln(s=''): out.append(s)
sigmaD = sum(r['dscar'] for r in rows)
movers = [r for r in rows if r['dscar'] != 0]
lifts = [r for r in movers if r['dscar'] > 0]; cuts = [r for r in movers if r['dscar'] < 0]
wln("# LEG B CONSERVED — POINT s=%s (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)" % S)
wln("active-804: %d rows · %d movers (%d lift / %d cut) · net board SigmaD %+d num-SCAR" %
    (len(rows), len(movers), len(lifts), len(cuts), sigmaD))
wln()

# ---- POOL RE-RATE (position-pool Δ totals) ----
wln("## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)")
wln("    %-9s %6s %10s %10s %8s" % ('pos', 'n', 'ΣΔnum', 'Σ|Δ|', 'movers'))
POS = ['MID', 'GEN_FWD', 'KEY_FWD', 'GEN_DEF', 'KEY_DEF', 'RUC']
for p in POS:
    pr = [r for r in rows if r['pos'] == p]
    net = sum(r['dscar'] for r in pr); gross = sum(abs(r['dscar']) for r in pr)
    mv = sum(1 for r in pr if r['dscar'] != 0)
    wln("    %-9s %6d %+10d %10d %8d" % (p, len(pr), net, gross, mv))
wln("    %-9s %6d %+10d %10d %8d" % ('ALL', len(rows), sigmaD,
    sum(abs(r['dscar']) for r in rows), len(movers)))
wln()

# ---- CENSUS / UNEARNED GAUGE (available reading; full census-v2 cell-gate is bake-mode, fenced out) ----
# The map is production-side only (_uncomp_prod at the price6 hook); pedigree/iso/pick priors are nominal
# by construction. CONSERVED (C[pos] applied): the memo §3 per-position renorm recycles value within each
# pool, so the net board SigmaD is the RESIDUAL re-rate (the conserved family should move value AROUND, not
# inject it) — reported by SIZE for comparison against the unfunded injection, not as a pass/fail. base sum for scale.
base_sum = sum(OFF[k]['num'] for k in akeys)
wln("## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)")
wln("    net board residual SigmaD = %+d num-SCAR  (%.2f%% of the %d active-804 baseline sum)" %
    (sigmaD, 100.0 * sigmaD / base_sum if base_sum else 0.0, base_sum))
wln("    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this")
wln("     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)")
wln()

# ---- E/B ----
a, b = 'timothy-english', 'kieren-briggs'
wln("## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())")
if a in ON and b in ON:
    eb_off = OFF[a]['num'] / OFF[b]['num']; eb_on = ON[a]['num'] / ON[b]['num']
    wln("    OFF: %d / %d = %.3fx     ON: %d / %d = %.3fx   => %s 1.75" %
        (OFF[a]['num'], OFF[b]['num'], eb_off, ON[a]['num'], ON[b]['num'], eb_on,
         'PASS >=' if eb_on >= 1.75 else 'FAIL <'))
else:
    wln("    (english/briggs keys not both present)")
wln()

# ---- BONTEMPELLI (owner's own test: SCAR up AND rank up) ----
wln("## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)")
bk = 'marcus-bontempelli'
if bk in by:
    r = by[bk]
    up_scar = r['dscar'] > 0; up_rank = r['drank'] < 0
    verdict = 'PASS (SCAR up AND rank up)' if (up_scar and up_rank) else \
        ('FAILURE — SCAR %s but rank %s' % ('up' if up_scar else ('flat' if r['dscar'] == 0 else 'down'),
         'up' if up_rank else ('flat' if r['drank'] == 0 else 'DOWN')))
    wln("    %s  SCAR %d->%d (%+d, %+.1f%%)  rank %d->%d (%+d)  => %s" %
        (r['player'], r['num_off'], r['num_on'], r['dscar'], r['dpct'],
         r['rank_off'], r['rank_on'], r['drank'], verdict))
else:
    wln("    (bontempelli key absent)")
wln()

# ---- SINCERITY FAILURES: SCAR rises while rank falls ----
sinc_fail = sorted([r for r in rows if r['dscar'] > 0 and r['drank'] > 0], key=lambda r: -r['drank'])
wln("## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=%d" % len(sinc_fail))
if sinc_fail:
    wln("    %-24s%-8s%4s%10s%9s%12s" % ('player', 'pos', 'age', 'ΔSCAR', 'Δ%', 'rank Δ'))
    for r in sinc_fail:
        o = OFF[r['key']]
        wln("    %-24s%-8s%4s%+10d%+9.1f%7d->%-4d(%+d)" % (r['player'][:23], r['pos'], o.get('age'),
            r['dscar'], r['dpct'], r['rank_off'], r['rank_on'], r['drank']))
else:
    wln("    (none — no player's SCAR rose while its rank fell)")
wln()

# ---- top-20 rank gainers / losers ----
wln("## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)")
wln("    %-24s%-8s%10s%12s" % ('player', 'pos', 'ΔSCAR', 'rank Δ'))
for r in sorted(rows, key=lambda r: r['drank'])[:20]:
    wln("    %-24s%-8s%+10d%7d->%-4d(%+d)" % (r['player'][:23], r['pos'], r['dscar'], r['rank_off'], r['rank_on'], r['drank']))
wln()
wln("## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)")
wln("    %-24s%-8s%10s%12s" % ('player', 'pos', 'ΔSCAR', 'rank Δ'))
for r in sorted(rows, key=lambda r: -r['drank'])[:20]:
    wln("    %-24s%-8s%+10d%7d->%-4d(%+d)" % (r['player'][:23], r['pos'], r['dscar'], r['rank_off'], r['rank_on'], r['drank']))

txt = '\n'.join(out)
open(os.path.join(OUT, 'POINT_s%s.md' % S), 'w').write(txt + '\n')
# machine-readable summary line + sidecar for aggregate.py
_pt = dict(s=S, movers=len(movers), sigmaD=sigmaD,
      eb_on=(ON[a]['num'] / ON[b]['num']) if (a in ON and b in ON) else None,
      bont=dict(dscar=by['marcus-bontempelli']['dscar'], drank=by['marcus-bontempelli']['drank']) if 'marcus-bontempelli' in by else None,
      sinc_fail=len(sinc_fail),
      pool={p: sum(r['dscar'] for r in rows if r['pos'] == p) for p in POS})
json.dump(_pt, open(os.path.join(OUT, 'PT_%s.json' % S), 'w'))
print('PTJSON ' + json.dumps(dict(s=S, movers=len(movers), sigmaD=sigmaD,
      eb_on=(ON[a]['num'] / ON[b]['num']) if (a in ON and b in ON) else None,
      bont=dict(dscar=by['marcus-bontempelli']['dscar'], drank=by['marcus-bontempelli']['drank']) if 'marcus-bontempelli' in by else None,
      sinc_fail=len(sinc_fail),
      pool={p: sum(r['dscar'] for r in rows if r['pos'] == p) for p in POS})))
print("wrote SINCERITY_all804_s%s.csv (%d rows) + POINT_s%s.md" % (S, len(rows), S))
