#!/usr/bin/env python3
"""LEG B SEGMENT-5 — build the deliverables from two ledger_dump.py dumps (OFF = RL_UNCOMP=0 baseline,
ON = map at the chosen s). Writes:
  MOVEMENT_LEDGER_all804.csv  — id,player,pos,price_off,price_on,delta_scar,delta_pct,rho_num,rho_ratio,w,games_window
  VALUE_FLOW.md               — movers, SigmaD, age-cohort distribution (item-130 no-young-net-strip),
                                young over-performer / earned-component scan (R104.8 / memo §5.5),
                                English/Briggs (captain-in) vs 1.75, watch rows, donor-side top-30.
usage: python3 analyze_legb.py <off.json> <on.json> <s>
"""
import json, sys, csv, os
OFF = json.load(open(sys.argv[1])); ON = json.load(open(sys.argv[2])); S = sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
ACT = set(r['key'] for r in json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))['active'])
def good(d): return isinstance(d, dict) and 'error' not in d
keys = [k for k in ON if good(ON.get(k)) and good(OFF.get(k))]
akeys = [k for k in keys if k in ACT]

# ---------- ALL-804 MOVEMENT LEDGER CSV ----------
led = os.path.join(HERE, 'MOVEMENT_LEDGER_all804.csv')
rows = []
for k in akeys:
    o, n = OFF[k], ON[k]
    doff, don = o['num'], n['num']
    dsc = don - doff; dpct = (100.0*dsc/doff) if doff else 0.0
    rows.append((n.get('sid') or '', n['player'], n['pos'], doff, don, dsc, round(dpct, 2),
                 n.get('rho_num'), n.get('rho_ratio'), n.get('w'), n.get('games_window')))
rows.sort(key=lambda r: r[5])   # by delta_scar ascending (biggest cuts first)
with open(led, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['stable_player_id', 'player', 'pos', 'price_off', 'price_on', 'delta_scar', 'delta_pct',
                'rho_num', 'rho_ratio', 'w', 'games_window'])
    w.writerows(rows)
print("wrote %s (%d active rows)" % (led, len(rows)))

# ---------- VALUE-FLOW ----------
out = []
def wln(s=''): out.append(s)
F_note = "num = round(ev/1.0524) (L7 numéraire)"
movers = [k for k in akeys if ON[k]['num'] != OFF[k]['num']]
sigmaD = sum(ON[k]['num'] - OFF[k]['num'] for k in akeys)
lifts = [k for k in movers if ON[k]['num'] > OFF[k]['num']]
cuts = [k for k in movers if ON[k]['num'] < OFF[k]['num']]
wln("# LEG B — VALUE-FLOW at s=%s  ·  OFF (RL_UNCOMP=0 == 8d90c9ac) -> ON (map at s)  ·  %s" % (S, F_note))
wln("## ACTIVE-804 board: %d movers · SigmaD %+d num-SCAR · %d lifted / %d cut" % (len(movers), sigmaD, len(lifts), len(cuts)))
wln()

def age_of(k): return OFF[k].get('age') or 0
def band(k):
    a = age_of(k)
    return '<=22' if a <= 22 else ('23-26' if a <= 26 else '>=27')
wln("## AGE-COHORT distribution (item-130 no-young-net-strip check)")
for b in ['<=22', '23-26', '>=27']:
    ks = [k for k in movers if band(k) == b]
    net = sum(ON[k]['num'] - OFF[k]['num'] for k in ks)
    gross = sum(abs(ON[k]['num'] - OFF[k]['num']) for k in ks)
    wln("    %-6s %4d movers   netSigmaD %+8d   grossSum|D| %8d" % (b, len(ks), net, gross))
young_net = sum(ON[k]['num'] - OFF[k]['num'] for k in movers if age_of(k) <= 26)
wln("    YOUNG (<=26) net SigmaD = %+d  => %s (>=0 no net-strip)" % (young_net, 'PASS' if young_net >= 0 else 'FAIL'))
wln()

# ---------- EARNED-COMPONENT gate (memo §5.5 / R104.8): young production must not fall ----------
def rawev(d):
    try: return float(d['rawev'])
    except Exception: return None
young = [k for k in akeys if age_of(k) <= 26]
earned_fall = []
for k in young:
    ro, rn = rawev(OFF[k]), rawev(ON[k])
    if ro is not None and rn is not None and rn < ro - 1e-6:
        earned_fall.append((k, ro, rn, rn - ro))
earned_fall.sort(key=lambda t: t[3])
wln("## EARNED-COMPONENT gate (memo §5.5 / R104.8): young (<=26) production raw_ev must NOT fall")
wln("    young players: %d · earned(production) FELL on %d" % (len(young), len(earned_fall)))
if earned_fall:
    wln("    %-24s%-8s%4s%10s%10s%9s" % ('player', 'pos', 'age', 'rawev_off', 'rawev_on', 'd'))
    for k, ro, rn, d in earned_fall[:40]:
        o = OFF[k]
        wln("    %-24s%-8s%4s%10.1f%10.1f%9.1f" % (o['player'][:23], o['pos'], o.get('age'), ro, rn, d))
    wln("    => GATE STATUS: FAIL (%d young earned components fell — BINDING acceptance breach, HALT)" % len(earned_fall))
else:
    wln("    => GATE STATUS: PASS (no young earned component falls)")
wln()

# ---------- English/Briggs (captain-in) ----------
wln("## English/Briggs priced ratio (R104.3 HARD floor 1.75; captain lift IN via ev())")
a, b = 'timothy-english', 'kieren-briggs'
if a in ON and b in ON:
    eb_off = OFF[a]['num']/OFF[b]['num']; eb_on = ON[a]['num']/ON[b]['num']
    wln("    OFF: English %d / Briggs %d = %.3fx" % (OFF[a]['num'], OFF[b]['num'], eb_off))
    wln("    ON : English %d / Briggs %d = %.3fx   => %s 1.75" % (ON[a]['num'], ON[b]['num'], eb_on,
        'PASS >=' if eb_on >= 1.75 else 'FAIL <'))
else:
    wln("    (english/briggs keys not both present)")
wln()

# ---------- watch rows ----------
wln("## WATCH ROWS: Gawn (up>=25) · Bontempelli (up>=25) · Reid (band) · A4 Reid value floor 3650")
for nm in ['max-gawn', 'marcus-bontempelli', 'harley-reid']:
    if nm in ON:
        d = ON[nm]['num'] - OFF[nm]['num']
        wln("    %-22s %d->%d (%+d)  %s" % (OFF[nm]['player'][:22], OFF[nm]['num'], ON[nm]['num'], d,
            'UP' if d > 0 else ('flat' if d == 0 else 'DOWN')))
wln()

# ---------- donor-side top-30 markdowns (memo §8) ----------
wln("## DONOR-SIDE top-30 proven (>=27) markdowns (memo §8): name · d · rho_ratio · w")
prov_cuts = sorted([k for k in cuts if age_of(k) >= 27], key=lambda k: ON[k]['num']-OFF[k]['num'])[:30]
wln("    %-24s%-8s%4s%8s%8s%9s%8s" % ('player', 'pos', 'age', 'off', 'on', 'rho_r', 'w'))
for k in prov_cuts:
    o, n = OFF[k], ON[k]
    wln("    %-24s%-8s%4s%8d%8d%9s%8s" % (o['player'][:23], o['pos'], o.get('age'), o['num'], n['num'],
        ('%.3f' % n['rho_ratio']) if n.get('rho_ratio') is not None else '  -', ('%.3f' % n['w']) if n.get('w') is not None else ' -'))
wln()
wln("## top-15 LIFTS")
for k in sorted(akeys, key=lambda k: OFF[k]['num']-ON[k]['num'])[:15]:
    o, n = OFF[k], ON[k]
    wln("    %-24s%-8s%4s%8d->%-8d(%+d)  rho_r=%s w=%s" % (o['player'][:23], o['pos'], o.get('age'), o['num'], n['num'],
        n['num']-o['num'], ('%.3f' % n['rho_ratio']) if n.get('rho_ratio') is not None else '-', ('%.3f' % n['w']) if n.get('w') is not None else '-'))

txt = '\n'.join(out)
open(os.path.join(HERE, 'VALUE_FLOW.md'), 'w').write(txt + '\n')
print(txt)
