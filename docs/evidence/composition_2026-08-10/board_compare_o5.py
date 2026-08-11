"""ORDER 5 — PER-PLAYER LIVE-BOARD COMPARISON across FULL / FULL+XW / FULL+V5 / FULL+STACK.

    ===================================================================================
    THESE NUMBERS ATTRIBUTE MOVERS. THEY DECIDE NOTHING.
    The deciding instrument for this act is the COHORT BOOK on noarb_table_338.py. The
    live board is a CROSS-SECTION, and this project has a standing finding that live-board
    cross-sections were the wrong basis for the cohort and no-arb readings. These files
    exist because the owner asked what happens to INDIVIDUAL players, which a pooled ratio
    cannot show. No candidate is selected, ranked or recommended on a board number here.
    ===================================================================================

Writes: board_compare_o5.csv  (all 804 active rows)
        board_compare_o5.txt  (owner-readable summary)
"""
import json, os, sys, csv, statistics

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o3'
EV = '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10'
REPO = '/home/user/afl-rl-engine'
LAW = ("THESE NUMBERS ATTRIBUTE MOVERS. THEY DECIDE NOTHING. The deciding instrument is the COHORT "
       "BOOK\n  on noarb_table_338.py (MENU.txt). The live board is a CROSS-SECTION and no candidate "
       "is selected,\n  ranked or recommended on a board number here.")

CFG = [('FULL', SP+'/o5_FULL.json'), ('XW', SP+'/o5_XW.json'),
       ('V5', SP+'/o5_V5.json'), ('STACK', SP+'/o5_STACK.json')]
B = {}
for lab, f in CFG:
    B[lab] = {r['key']: r for r in json.load(open(f))['active']}
MAIN = {r['key']: r for r in json.load(open(REPO+'/data/rl_build/rl_app_data.json'))['active']}

keys = sorted(B['FULL'], key=lambda k: -B['FULL'][k]['v'])
print("active rows:", len(keys))

rows = []
for k in keys:
    f = B['FULL'][k]
    rec = dict(player=f.get('name'), key=k, position=f.get('grp'), age=f.get('age'),
               club=f.get('club'), pick=f.get('pk'), draft_year=f.get('yr'),
               main=(MAIN[k]['v'] if k in MAIN else ''),
               FULL=f['v'], XW=B['XW'][k]['v'], V5=B['V5'][k]['v'], STACK=B['STACK'][k]['v'])
    rec['delta_XW'] = rec['XW'] - rec['FULL']
    rec['delta_V5'] = rec['V5'] - rec['FULL']
    rec['delta_STACK'] = rec['STACK'] - rec['FULL']
    rows.append(rec)

COLS = ['player', 'key', 'position', 'age', 'club', 'pick', 'draft_year',
        'main', 'FULL', 'XW', 'V5', 'STACK', 'delta_XW', 'delta_V5', 'delta_STACK']
with open(EV+'/board_compare_o5.csv', 'w', newline='') as fh:
    fh.write("# ORDER 5 per-player live-board comparison. " + LAW.replace('\n', ' ').replace('  ', ' ') + "\n")
    fh.write("# main = the currently shipped board (data/rl_build/rl_app_data.json). "
             "deltas are vs FULL, the composition package as it stands. All dials DEFAULT OFF in FULL.\n")
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader()
    for r in rows: w.writerow(r)
print("wrote board_compare_o5.csv", len(rows), "rows")

L = []
def P(s=''): L.append(s); print(s)

P("=" * 100)
P("ORDER 5 — WHAT HAPPENS TO INDIVIDUAL PLAYERS UNDER XW, V5 AND THE STACK")
P("=" * 100)
P("  " + LAW)
P()
P("  FULL   = the composition package as it stands today (every new dial OFF)")
P("  XW     = FULL + the exposure-weighted par sample        (RL_336_XW=1)")
P("  V5     = FULL + the owner's fifth discount ladder       (RL_AGE_DISC_MODE=5)")
P("  STACK  = FULL + both together")
P("  main   = the board shipped today, for reference only — it is NOT the comparison baseline")
P()

P("-" * 100)
P("### SANITY — board totals and mover counts")
P("-" * 100)
tot = {lab: sum(r[lab] for r in rows) for lab in ('main', 'FULL', 'XW', 'V5', 'STACK') if lab != 'main'}
tot['main'] = sum(r['main'] for r in rows if r['main'] != '')
P(f"  {'config':8} {'board total':>14} {'vs FULL':>12} {'movers vs FULL':>16} {'up':>7} {'down':>7}")
for lab in ('main', 'FULL', 'XW', 'V5', 'STACK'):
    mv = [r for r in rows if lab not in ('FULL', 'main') and r['delta_' + lab] != 0]
    if lab == 'main':
        P(f"  {'main':8} {tot['main']:14,} {'(not a baseline)':>12} {'-':>16} {'-':>7} {'-':>7}")
    elif lab == 'FULL':
        P(f"  {'FULL':8} {tot['FULL']:14,} {'baseline':>12} {'-':>16} {'-':>7} {'-':>7}")
    else:
        up = sum(1 for r in mv if r['delta_' + lab] > 0)
        P(f"  {lab:8} {tot[lab]:14,} {100*(tot[lab]/tot['FULL']-1):+11.2f}% {len(mv):16} {up:7} {len(mv)-up:7}")
P()

P("-" * 100)
P("### THE TOP 25 MOVERS BY |delta_STACK|")
P("-" * 100)
P(f"  {'player':24} {'pos':5} {'age':>3} {'FULL':>7} {'XW':>7} {'V5':>7} {'STACK':>7} {'dXW':>7} {'dV5':>7} {'dSTACK':>8} {'%':>7}")
for r in sorted(rows, key=lambda r: -abs(r['delta_STACK']))[:25]:
    pc = 100*r['delta_STACK']/r['FULL'] if r['FULL'] else 0
    P(f"  {str(r['player'])[:24]:24} {str(r['position'])[:5]:5} {r['age']:3} {r['FULL']:7} {r['XW']:7} "
      f"{r['V5']:7} {r['STACK']:7} {r['delta_XW']:+7} {r['delta_V5']:+7} {r['delta_STACK']:+8} {pc:+6.1f}%")
P()

P("-" * 100)
P("### THE NAMED LINES")
P("-" * 100)
NAMED = ['mraz', 'dovaston', 'bontempelli', 'gawn', 'king']
P(f"  {'player':24} {'pos':5} {'age':>3} {'main':>7} {'FULL':>7} {'XW':>7} {'V5':>7} {'STACK':>7} {'dSTACK':>8} {'%':>7}")
for r in rows:
    nm = str(r['player']).lower()
    if any(t in nm for t in NAMED):
        pc = 100*r['delta_STACK']/r['FULL'] if r['FULL'] else 0
        P(f"  {str(r['player'])[:24]:24} {str(r['position'])[:5]:5} {r['age']:3} {str(r['main']):>7} {r['FULL']:7} "
          f"{r['XW']:7} {r['V5']:7} {r['STACK']:7} {r['delta_STACK']:+8} {pc:+6.1f}%")
P()

P("-" * 100)
P("### MOVEMENT BY AGE BAND — where each lever actually lands")
P("-" * 100)
BANDS = [('<=19', lambda a: a <= 19), ('20-21', lambda a: 20 <= a <= 21), ('22-24', lambda a: 22 <= a <= 24),
         ('25-27', lambda a: 25 <= a <= 27), ('28+', lambda a: a >= 28)]
P(f"  {'band':6} {'n':>5} {'FULL total':>12} | " + " | ".join(f"{lab+' tot %':>11} {lab+' med %':>10}" for lab in ('XW','V5','STACK')))
for lab, sel in BANDS:
    sub = [r for r in rows if r['age'] is not None and sel(r['age'])]
    if not sub: continue
    tf = sum(r['FULL'] for r in sub)
    cells = []
    for c in ('XW', 'V5', 'STACK'):
        td = sum(r['delta_'+c] for r in sub)
        med = statistics.median([100*r['delta_'+c]/r['FULL'] for r in sub if r['FULL']])
        cells.append(f"{100*td/tf:+10.2f}% {med:+9.2f}%")
    P(f"  {lab:6} {len(sub):5} {tf:12,} | " + " | ".join(cells))
P()
P("  'tot %' is the band's aggregate move as a share of the band's own FULL total; 'med %' is the")
P("  median individual move in the band. They differ where a few big players carry the aggregate.")
P()

P("-" * 100)
P("### THE DISAGREEMENT SET — players XW and V5 move in OPPOSITE directions")
P("-" * 100)
dis = [r for r in rows if r['delta_XW'] * r['delta_V5'] < 0]
P(f"  COUNT: {len(dis)} of {len(rows)} active players ({100*len(dis)/len(rows):.1f}%)")
P("  These are the rows where the two levers genuinely disagree about a player — the clearest proof")
P("  that XW and V5 are different mechanisms and not one lever wearing two names.")
P()
P(f"  {'player':24} {'pos':5} {'age':>3} {'FULL':>7} {'dXW':>8} {'dV5':>8} {'dSTACK':>8}  which wins")
for r in sorted(dis, key=lambda r: -max(abs(r['delta_XW']), abs(r['delta_V5'])))[:10]:
    winner = 'XW' if (r['delta_STACK'] > 0) == (r['delta_XW'] > 0) else 'V5'
    P(f"  {str(r['player'])[:24]:24} {str(r['position'])[:5]:5} {r['age']:3} {r['FULL']:7} "
      f"{r['delta_XW']:+8} {r['delta_V5']:+8} {r['delta_STACK']:+8}  {winner}")
P()

P("-" * 100)
P("### SUPER-ADDITIVITY CHECK (pre-registered P5.3 — the sign was NOT assumed)")
P("-" * 100)
sup = [r for r in rows if abs(r['delta_STACK']) > abs(r['delta_XW']) + abs(r['delta_V5']) + 0.5
       and r['delta_STACK'] != 0]
same = [r for r in sup if (r['delta_STACK'] > 0) == (r['delta_XW'] + r['delta_V5'] > 0)]
P(f"  rows where |dSTACK| exceeds |dXW| + |dV5|: {len(sup)} of {len(rows)}  ({len(same)} in the same direction)")
P("  The mechanical route to this is real: XW raises the par levels, and par feeds the peak estimate")
P("  and ITEM C's Q = sa/par, which is part of what V5's age-keyed discount is then applied to.")
if sup:
    P(f"\n  {'player':24} {'age':>3} {'FULL':>7} {'dXW':>8} {'dV5':>8} {'sum':>8} {'dSTACK':>8} {'excess':>8}")
    for r in sorted(sup, key=lambda r: -(abs(r['delta_STACK'])-abs(r['delta_XW'])-abs(r['delta_V5'])))[:10]:
        s = r['delta_XW'] + r['delta_V5']
        P(f"  {str(r['player'])[:24]:24} {r['age']:3} {r['FULL']:7} {r['delta_XW']:+8} {r['delta_V5']:+8} "
          f"{s:+8} {r['delta_STACK']:+8} {abs(r['delta_STACK'])-abs(r['delta_XW'])-abs(r['delta_V5']):+8.0f}")
P()
P("=" * 100)
P("  " + LAW)
P("=" * 100)
open(EV+'/board_compare_o5.txt', 'w').write('\n'.join(L) + '\n')
print("\nwrote board_compare_o5.txt")
