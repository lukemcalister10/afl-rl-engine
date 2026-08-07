"""#334 stage B / STAGE 5 — THE FULL ENUMERATION OF EVERY MOVED PLAYER (the QUIET-STARTER REPRICE).

Every player whose BOARD price the taught anchor factor G moves, vs the ruled baseline board
b56bbdde (stage 4 amendment 1). No cap. Mechanism fields per the directive: old, new, abs, rel,
tau, CUMULATIVE career games, season games gy, the taught G AT HIS OWN CELL, lam before/after,
the anchor and its taught form, and e_full.

Board values are the EXPORTED board `v` (numeraire-rebased, the number the owner reads); the engine
ev() figure is carried beside it so the two rulers are never confused. READ-ONLY.
"""
import os, sys, io, json, contextlib, csv
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
OLD_BOARD, NEW_BOARD = sys.argv[1], sys.argv[2]

sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s5_enum'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; Y = 2026


def rows(d):
    r = d['active'] if isinstance(d, dict) and 'active' in d else d
    return list(r.values()) if isinstance(r, dict) else r


A = {p['key']: p for p in rows(json.load(open(OLD_BOARD))) if p.get('v') is not None}
B = {p['key']: p for p in rows(json.load(open(NEW_BOARD))) if p.get('v') is not None}
bykey = {p.get('key'): p for p in MA.data if p.get('key')}


def entry_label(p):
    t = p.get('type') or '?'
    if MA.is_pool(p):
        d = '%s%s' % (t, ':' + MA.gfut(p) if t == 'RD' else '')
        return '%s (pool, effpk %d)' % (d, MA.effpk(p))
    return '%s pick %s' % (t, p.get('pick') if p.get('pick') is not None else 'none')


def mech(p):
    fe = G['_fEy'](Y, p)
    tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
    cls = G['_sitout_cls'](MA.gfut(p)); pk = MA.effpk(p)
    R = G['_R_surf'](cls, pk, tau); A0 = G['entry_anchor'](p)
    gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
    gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
    gp = min(gy / fe, 6.0)
    lam0 = float(np.interp(gp, [0, 1, 2, 3, 4, 5, 6], G['LAM_SIT']))
    q = G['_ped_prior'](p, Y, fe, tau, cls, pk)
    with contextlib.redirect_stdout(io.StringIO()): e_full = G['_prod_path'](p, Y)
    g5 = G['_g5'](p, Y, tau, cls, pk) if G['G5_W'] else 1.0
    base_exp = 1.0 + G['PED_BAR'] * (1.0 - q)
    anch_before = R * A0
    anch_after = anch_before * g5
    lam_before = lam0 ** (base_exp + G['_surprise'](e_full, anch_before, gp))
    lam_after = lam0 ** (base_exp + G['_surprise'](e_full, anch_after, gp))
    return dict(fe=fe, tau=tau, cls=cls, pk=pk, R=R, anchor=A0, gy=gy, gcum=gcum, gp=gp,
                lam_raw=lam0, q=q, e_full=e_full, g5=g5,
                anchor_leg_before=anch_before, anchor_leg_after=anch_after,
                lam_before=lam_before, lam_after=lam_after,
                price_before=(1 - lam_before) * anch_before + lam_before * e_full,
                price_after=(1 - lam_after) * anch_after + lam_after * e_full,
                on_sitout_path=(G['nseas_pro'](p, Y) == 0))


recs = []
for k in sorted(set(A) & set(B)):
    if A[k]['v'] == B[k]['v']: continue
    p = bykey.get(k); old, new = A[k]['v'], B[k]['v']
    m = mech(p)
    sc = sorted([(int(x['year']), int(x['games']), float(x['avg'])) for x in p['scoring']])
    with contextlib.redirect_stdout(io.StringIO()): evb = G['ev'](p, Y)
    recs.append(dict(
        key=k, player=p.get('player'), pos=MA.gfut(p), sitout_class=m['cls'],
        entry=entry_label(p), effpk=m['pk'], draft_year=p.get('year'),
        pathway=(p.get('type') or '?'), pool=bool(MA.is_pool(p)),
        old=old, new=new, abs=new - old, rel=(new - old) / old if old else 0.0,
        ev_this_build=evb,
        tau=round(m['tau'], 6), career_games_cumulative=int(m['gcum']), games_2026=int(m['gy']),
        games_at_pace=round(m['gy'] / m['fe'], 4), games_at_pace_clamped=round(m['gp'], 4),
        G_at_his_cell=round(m['g5'], 6),
        entry_anchor=round(m['anchor'], 2), retention_R=round(m['R'], 6),
        anchor_leg_before=round(m['anchor_leg_before'], 2), anchor_leg_after=round(m['anchor_leg_after'], 2),
        lam_before=round(m['lam_before'], 6), lam_after=round(m['lam_after'], 6),
        e_full=round(m['e_full'], 2), q_pedigree=round(m['q'], 6),
        engine_price_before=round(m['price_before'], 3), engine_price_after=round(m['price_after'], 3),
        career_by_season='; '.join('%d:%dg@%.1f' % s for s in sc) or '(no rows)',
        on_sitout_path=m['on_sitout_path']))

recs.sort(key=lambda r: -abs(r['rel']))
with open(os.path.join(OUT, 'movers_full.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0].keys())); w.writeheader()
    for r in recs: w.writerow(r)
json.dump(recs, open(os.path.join(OUT, 'movers_full.json'), 'w'), indent=1)

ups = [r for r in recs if r['abs'] > 0]; downs = [r for r in recs if r['abs'] < 0]
shared = sorted(set(A) & set(B))
ta, tb = sum(A[k]['v'] for k in shared), sum(B[k]['v'] for k in shared)

L = []
L.append('#334 stage B / STAGE 5 — FULL ENUMERATION OF EVERY MOVED PLAYER (the QUIET-STARTER REPRICE)')
L.append('board b56bbddea15fd48e35b5794b1b5e9e23 (stage 4 amendment 1, the RULED BASELINE)  ->  %s'
         % os.environ.get('RL_NEWBOARD', '(new board)'))
L.append('mechanism: the sit-out anchor leg becomes  G * R * entry_anchor  at BOTH anchor sites')
L.append('           (the blend term and _surprise\'s anchor argument). RL_G5_W = %.4g.' % G['G5_W'])
L.append('           G = G(retention class, log-pick, CUMULATIVE career games, tau) — the taught surface,')
L.append('           frozen in engine/rl_after/g5_table.json, re-evaluated from his record at every build.')
L.append('')
L.append('SCOPE OF THE MOVE')
L.append('  board rows compared            : %d' % len(shared))
L.append('  MOVED                          : %d  (%.2f%% of the board)' % (len(recs), 100.0 * len(recs) / len(shared)))
L.append('    lifts (price up)             : %d' % len(ups))
L.append('    cuts (price down)            : %d' % len(downs))
L.append('  board total                    : %d -> %d  (%+d, %+.4f%%)' % (ta, tb, tb - ta, 100.0 * (tb - ta) / ta))
L.append('  every mover on the sit-out path: %s' % all(r['on_sitout_path'] for r in recs))
L.append('  mean |rel| across movers       : %.4f%%' % (100.0 * float(np.mean([abs(r['rel']) for r in recs]))))
L.append('  largest lift %+.2f%%   largest cut %+.2f%%'
         % (100.0 * max(r['rel'] for r in recs), 100.0 * min(r['rel'] for r in recs)))
L.append('  G at the movers\' own cells     : min %.4f  median %.4f  max %.4f'
         % (min(r['G_at_his_cell'] for r in recs), float(np.median([r['G_at_his_cell'] for r in recs])),
            max(r['G_at_his_cell'] for r in recs)))
L.append('')
L.append('WHY A PLAYER CAN MOVE DOWN. G never falls below 1, so the anchor leg never shrinks. But the anchor')
L.append('is ALSO the reference the surprise statistic measures a re-rate against: lifting it changes')
L.append('s = |log(e_full/anchor)| and therefore lam. For a player whose e_full sits BELOW his anchor, a')
L.append('higher anchor means a LARGER surprise, a higher evidence bar, a smaller lam — more weight on the')
L.append('anchor leg, which for him is the lower number. That is the stage-4-amendment-1 machinery doing')
L.append('exactly what it was built to do, composed with, not deleted. Every such row is listed below.')
L.append('')
L.append('=' * 168)
L.append('EVERY MOVED PLAYER, SORTED BY |relative move|  (n=%d, NO CAP)' % len(recs))
L.append('=' * 168)
L.append('%-26s %-5s %-21s %7s %7s %7s %8s | %6s %5s %4s %7s %7s %7s %9s | %s'
         % ('player', 'pos', 'entry', 'old', 'new', 'abs', 'rel', 'tau', 'gcum', 'g26', 'G cell', 'lam bef',
            'lam aft', 'e_full', 'career by season'))
L.append('-' * 168)
for r in recs:
    L.append('%-26s %-5s %-21s %7d %7d %+7d %+7.2f%% | %6.3f %5d %4d %7.4f %7.4f %7.4f %9.1f | %s'
             % (r['player'][:26], r['pos'], r['entry'][:21], r['old'], r['new'], r['abs'], 100.0 * r['rel'],
                r['tau'], r['career_games_cumulative'], r['games_2026'], r['G_at_his_cell'],
                r['lam_before'], r['lam_after'], r['e_full'], r['career_by_season']))
L.append('')
L.append('=' * 168)
L.append('THE TRIGGERING RECORD IN FULL, same order')
L.append('=' * 168)
for i, r in enumerate(recs, 1):
    L.append('%3d. %s  (%s, %s, drafted %s, retention class %s)'
             % (i, r['player'], r['pos'], r['entry'], r['draft_year'], r['sitout_class']))
    L.append('     price            : %d -> %d   (%+d, %+.2f%%)   [engine ev() on this build %d]'
             % (r['old'], r['new'], r['abs'], 100.0 * r['rel'], r['ev_this_build']))
    L.append('     career by season : %s   (CUMULATIVE career games %d; season-2026 games %d, %.2f at pace)'
             % (r['career_by_season'], r['career_games_cumulative'], r['games_2026'], r['games_at_pace']))
    L.append('     his cell         : tau %.4f   class %s   effpk %d   cumulative games %d   ->   TAUGHT G = %.6f'
             % (r['tau'], r['sitout_class'], r['effpk'], r['career_games_cumulative'], r['G_at_his_cell']))
    L.append('     the anchor leg   : entry anchor %.2f x R %.6f = %.2f   ->  x G = %.2f'
             % (r['entry_anchor'], r['retention_R'], r['anchor_leg_before'], r['anchor_leg_after']))
    L.append('     the evidence leg : e_full %.2f   lam %.6f -> %.6f   (the surprise statistic re-reads the lifted anchor)'
             % (r['e_full'], r['lam_before'], r['lam_after']))
    L.append('     engine price     : %.3f -> %.3f  (pre-numeraire, pre-M3; the board figures above are the shipped ones)'
             % (r['engine_price_before'], r['engine_price_after']))
    L.append('')
open(os.path.join(OUT, 'MOVERS_FULL.txt'), 'w').write('\n'.join(L) + '\n')
print('movers %d (up %d, down %d) ; board total %d -> %d (%+.4f%%)'
      % (len(recs), len(ups), len(downs), ta, tb, 100.0 * (tb - ta) / ta))
