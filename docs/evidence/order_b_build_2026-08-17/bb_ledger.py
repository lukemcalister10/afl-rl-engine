#!/usr/bin/env python3
"""ORDER B — the movers ledger vs BOTH baselines (live 88ce647f, Candidate 31 fe6be9d6) plus the
C32-repair base and the per-mechanism legs, and the board-level acceptance numbers (rank moves 27+,
age profile of moves, tall-anchor gate). Pure JSON reads — no engine run."""
import json, os, collections
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
C31 = json.load(open(SP + '/cand31.json'))
assert C31['boards']['candidate'].startswith('fe6be9d6') and C31['boards']['live'].startswith('88ce647f')
BOARDS = {}
for tag in ('moff', 'mleg1', 'mfull1'):
    BOARDS[tag] = {r['key']: r for r in json.load(open(SP + '/o33/bb_%s/rl_after/rl_app_data.json' % tag))['active']}
import hashlib
md5 = {t: hashlib.md5(open(SP + '/o33/bb_%s/rl_after/rl_app_data.json' % t, 'rb').read()).hexdigest()
       for t in BOARDS}
print('boards:', {t: m[:8] for t, m in md5.items()})

rows = []
for r in C31['rows']:
    k = r['key']
    b = BOARDS['moff'].get(k)
    if b is None:
        continue
    v0, v1, v3 = (BOARDS[t][k]['v'] for t in ('moff', 'mleg1', 'mfull1'))
    rows.append(dict(key=k, name=r['name'], pos=(b.get('gf') or b['grp']), pos_now=b['grp'],
                     age=b['age'], pathway=r['pathway'], pick=r.get('pick'),
                     live=r['live'], cand31=r['cand'], c32base=v0,
                     leg_ladder=v1 - v0, leg_fade=0, leg_taper=v3 - v1,
                     b_preview=v3,
                     d_vs_c32base=v3 - v0, d_vs_cand31=v3 - r['cand'], d_vs_live=v3 - r['live']))
print('ledger rows: %d of %d C31 rows' % (len(rows), len(C31['rows'])))
tot = {f: sum(r[f] for r in rows) for f in ('live', 'cand31', 'c32base', 'b_preview',
                                            'leg_ladder', 'leg_fade', 'leg_taper')}
print('totals:', {k: round(v) for k, v in tot.items()})

# ---- acceptance: rank ordering among 27+ -------------------------------------------------------------
V0 = np.array([r['c32base'] for r in rows]); V3 = np.array([r['b_preview'] for r in rows])
rk0 = rankdata(-V0, method='average'); rk3 = rankdata(-V3, method='average')
sel27 = np.array([r['age'] >= 27 for r in rows])
dmoves = np.abs(rk3 - rk0)[sel27]
tall27 = np.array([r['age'] >= 27 and r['pos'] in ('KPD', 'KPF') for r in rows])


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d)


sp_tall = spear(V0[tall27], V3[tall27])
sp_all27 = spear(V0[sel27], V3[sel27])
biggest = sorted([(abs(b - a), r['key'], int(a), int(b)) for r, a, b in
                  zip(rows, rk0, rk3) if r['age'] >= 27], reverse=True)[:10]
print('rank moves (27+, within the 804-row board): max %.0f mean %.1f' % (dmoves.max(), dmoves.mean()))
print('Spearman base->B: all 27+ %.4f  tall 27+ %.4f' % (sp_all27, sp_tall))

# ---- continuity: age profile of relative moves + the analytic schedules ------------------------------
ageprof = {}
for a in range(18, 38):
    sel = [r for r in rows if r['age'] == a]
    if not sel:
        continue
    sv0 = sum(r['c32base'] for r in sel); sv3 = sum(r['b_preview'] for r in sel)
    tl = [r for r in sel if r['pos'] in ('KPD', 'KPF')]
    ageprof[a] = dict(n=len(sel), rel_move=round(sv3 / sv0 - 1, 4) if sv0 else None,
                      n_tall=len(tl),
                      rel_move_tall=(round(sum(r['b_preview'] for r in tl) / sum(r['c32base'] for r in tl) - 1, 4)
                                     if tl and sum(r['c32base'] for r in tl) > 0 else None))
print('age profile of board moves (all | tall):')
for a in sorted(ageprof):
    ap = ageprof[a]
    print('  age %d n=%3d  %+7.2f%%   tall n=%2d  %s' % (a, ap['n'], 100 * ap['rel_move'], ap['n_tall'],
          ('%+7.2f%%' % (100 * ap['rel_move_tall'])) if ap['rel_move_tall'] is not None else '      —'))

# tall anchor gate re-stated on the final board
anch = [r for r in rows if r['pos'] in ('KPD', 'KPF') and 23 <= r['age'] <= 26]
g0 = sum(r['c32base'] for r in anch)
gl = sum(r['c32base'] + r['leg_ladder'] for r in anch)
print('tall-anchor gate (23-26, ladder leg only): %+.2f%% (bound +-3%%)' % (100 * (gl / g0 - 1)))

# the analytic schedules (continuity exhibits)
LAD = {}
f = 1.0
for j in range(1, 8):
    f *= (1 - min(0.60, 0.03 + 0.025 * (j - 1)))
    LAD[27 + j] = round(f, 4)
FADE = {round(a, 1): round(np.interp(a, [28, 29, 30, 31], [0.14, 0.211, 0.232, 0.246]), 4)
        for a in np.arange(27.0, 32.5, 0.5)}

OUT = dict(meta=dict(boards={t: m for t, m in md5.items()},
                     baselines=dict(live=C31['boards']['live'], cand31=C31['boards']['candidate']),
                     legs='ladder = stage1 - base; taper = full - stage1; the fade leg is 0 BY DELETION (owner ruling c.5316404479)'),
           totals={k: round(v) for k, v in tot.items()},
           acceptance=dict(rank_moves_27plus=dict(max=float(dmoves.max()), mean=round(float(dmoves.mean()), 2),
                                                  biggest=[[k, a, b] for _, k, a, b in biggest]),
                           spearman_base_to_B=dict(all27=round(sp_all27, 4), tall27=round(sp_tall, 4)),
                           tall_anchor_gate_pct=round(100 * (gl / g0 - 1), 3),
                           age_profile={str(a): v for a, v in ageprof.items()},
                           ladder_schedule=LAD, fade_schedule={str(k): v for k, v in FADE.items()}),
           rows=rows)
os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
with open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_B_MOVERS.json'), 'w') as fh:
    json.dump(OUT, fh, indent=1)
with open(os.path.join(HERE, 'LEDGER_B.json'), 'w') as fh:
    json.dump(OUT, fh, indent=1)
print('wrote docs/ledgers/ORDER_B_MOVERS.json (+ evidence copy LEDGER_B.json)')

movers = sorted(rows, key=lambda r: r['d_vs_c32base'])
print('\ntop 12 fallers vs C32 base:')
for r in movers[:12]:
    print('  %-24s %-4s %2d  %+7d (ladder %+d fade %+d taper %+d)' % (
        r['name'][:24], r['pos'], r['age'], r['d_vs_c32base'], r['leg_ladder'], r['leg_fade'], r['leg_taper']))
print('top 12 risers vs C32 base:')
for r in movers[-12:][::-1]:
    print('  %-24s %-4s %2d  %+7d (ladder %+d fade %+d taper %+d)' % (
        r['name'][:24], r['pos'], r['age'], r['d_vs_c32base'], r['leg_ladder'], r['leg_fade'], r['leg_taper']))
NAMED = ['callum-wilkie', 'peter-wright', 'harris-andrews', 'josh-battle', 'harry-mckay', 'charlie-curnow',
         'ned-moyle', 'lachlan-mcandrew', 'sam-de-koning', 'tom-de-koning', 'marcus-bontempelli',
         'jack-sinclair', 'zachary-merrett']
ro = {r['key']: r for r in rows}
print('\nNAMED ROWS (B-preview vs everything):')
print('%-22s %-5s %3s %8s %8s %8s | %7s %7s %7s | %8s %8s %8s %8s' % (
    'row', 'pos', 'age', 'live', 'cand31', 'c32base', 'ladder', 'fade', 'taper', 'B-prev',
    'vs-base', 'vs-C31', 'vs-live'))
for k in NAMED:
    r = ro.get(k)
    if not r:
        print('%-22s (absent)' % k)
        continue
    print('%-22s %-5s %3d %8d %8d %8d | %+7d %+7d %+7d | %8d %+8d %+8d %+8d' % (
        r['name'][:22], r['pos'], r['age'], r['live'], r['cand31'], r['c32base'],
        r['leg_ladder'], r['leg_fade'], r['leg_taper'], r['b_preview'],
        r['d_vs_c32base'], r['d_vs_cand31'], r['d_vs_live']))
