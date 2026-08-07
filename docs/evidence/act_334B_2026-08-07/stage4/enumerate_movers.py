"""#334 stage B / STAGE 4 — THE FULL ENUMERATION (the owner's explicit ask).

"The Mraz change probably needs to happen, but we also need to be able to track any other players
 caught in that change too."  -- owner, 2026-08-07

Every player whose BOARD price the pedigree-conditioned reactivity change moves, vs board 6c9f8d3a
(stage 3). No cap on the list. For each mover: player, position, entry pick (or pathway), old, new,
abs, rel, AND the triggering record -- career games by season, best-season games, sit-out years, the
draft-day anchor, and the three mechanism quantities (lam before, lam after, q).

Board values are the EXPORTED board `v` (numeraire-rebased, the number the owner reads). The engine
ev() figure is carried beside it so the two rulers are never confused.

READ-ONLY on the engine and the store.
"""
import os, sys, io, json, contextlib, csv
import numpy as np

REPO = os.environ.get('RL_REPO', '/home/claude/seamcheck_landing')
WORKDIR = os.environ.get('RL_WORKDIR', '/home/claude/rl_workspace/rl_after')
OUT = os.path.dirname(os.path.abspath(__file__))
OLD_BOARD = sys.argv[1]
NEW_BOARD = sys.argv[2]

sys.path.insert(0, REPO + '/vendor'); os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s4_enum'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; Y = 2026


def rows(d):
    r = d['active'] if isinstance(d, dict) and 'active' in d else d
    return list(r.values()) if isinstance(r, dict) else r


A = {p['key']: p for p in rows(json.load(open(OLD_BOARD))) if p.get('v') is not None}
B = {p['key']: p for p in rows(json.load(open(NEW_BOARD))) if p.get('v') is not None}
bykey = {p.get('key'): p for p in MA.data if p.get('key')}

POOLDIV = {}
for k, p in bykey.items():
    if MA.is_pool(p): POOLDIV[k] = '%s%s' % (p.get('type') or '?', ':' + MA.gfut(p) if (p.get('type') or '') == 'RD' else '')


def entry_label(p):
    """The pedigree the mechanism actually reads: the engine's own effpk, plus the human pathway."""
    t = p.get('type') or '?'
    if MA.is_pool(p): return '%s (pool, effpk %d)' % (POOLDIV.get(p.get('key'), t), MA.effpk(p))
    pk = p.get('pick')
    return '%s pick %s' % (t, pk if pk is not None else 'none')


def record(p):
    sc = sorted([(int(x['year']), int(x['games']), float(x['avg'])) for x in p['scoring']], key=lambda z: z[0])
    played = [s for s in sc if s[1] > 0]
    d0 = cp.debutyr(p)
    first_played = played[0][0] if played else None
    # sit-out years = LISTED years from the route's own debut year up to Y with no games played.
    yrs_played = {s[0] for s in played}
    sitout = [y for y in range(d0, Y + 1) if y not in yrs_played]
    lead_sit = (first_played - d0) if (first_played is not None and first_played > d0) else 0
    return sc, played, d0, sitout, lead_sit


def mech(p):
    """The three mechanism quantities, recomputed from the engine's own objects."""
    fe = G['_fEy'](Y, p)
    tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
    cls = G['_sitout_cls'](MA.gfut(p)); pk = MA.effpk(p)
    gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
    lam0 = float(np.interp(min(gy / fe, 6.0), [0, 1, 2, 3, 4, 5, 6], G['LAM_SIT']))
    q = G['_ped_prior'](p, Y, fe, tau, cls, pk)
    ped = 1.0 - float(np.log(min(max(pk, 1), 90)) / np.log(90.0))
    tau0 = (fe ** 1.5) if Y >= cp.debutyr(p) else 0.0
    r0 = G['_R_surf'](cls, pk, tau0)
    sit = (G['_R_surf'](cls, pk, tau) / r0) if r0 > 0 else 1.0
    exp = 1.0 + G['PED_BAR'] * (1.0 - q)
    return dict(fe=fe, tau=tau, gy=gy, atpace=gy / fe, lam_before=lam0, lam_after=lam0 ** exp,
                ped=ped, sit=sit, q=q, exponent=exp,
                R=G['_R_surf'](cls, pk, tau), anchor=G['entry_anchor'](p), on_sitout_path=(G['nseas_pro'](p, Y) == 0))


recs = []
for k in sorted(set(A) & set(B)):
    if A[k]['v'] == B[k]['v']: continue
    p = bykey.get(k)
    old, new = A[k]['v'], B[k]['v']
    sc, played, d0, sitout, lead = record(p)
    m = mech(p)
    recs.append(dict(
        key=k, player=p.get('player'), pos=MA.gfut(p), entry=entry_label(p), effpk=MA.effpk(p),
        draft_year=p.get('year'), pathway=(p.get('type') or '?'), pool=bool(MA.is_pool(p)),
        old=old, new=new, abs=new - old, rel=(new - old) / old if old else 0.0,
        ev_this_build=G['ev'](p, Y),
        career_by_season='; '.join('%d:%dg@%.1f' % s for s in sc) or '(no rows)',
        career_games=sum(s[1] for s in sc), best_season_games=max([s[1] for s in sc], default=0),
        best_season_avg=max([s[2] for s in sc if s[1] > 0], default=0.0),
        route_debut_year=d0, first_played_year=(played[0][0] if played else None),
        sitout_years_n=len(sitout), sitout_years=','.join(str(y) for y in sitout) or '-',
        lead_sitout_years=lead,
        draft_day_anchor=round(m['anchor'], 2), retention_R=round(m['R'], 5),
        games_2026=m['gy'], games_at_pace=round(m['atpace'], 4),
        lam_before=round(m['lam_before'], 6), lam_after=round(m['lam_after'], 6),
        ped=round(m['ped'], 6), sit=round(m['sit'], 6), q=round(m['q'], 6), exponent=round(m['exponent'], 6),
        on_sitout_path=m['on_sitout_path']))

recs.sort(key=lambda r: -abs(r['rel']))

with open(os.path.join(OUT, 'movers_full.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
    w.writeheader()
    for r in recs: w.writerow(r)

ups = [r for r in recs if r['abs'] > 0]; downs = [r for r in recs if r['abs'] < 0]
shared = sorted(set(A) & set(B))
ta, tb = sum(A[k]['v'] for k in shared), sum(B[k]['v'] for k in shared)

L = []
L.append('#334 stage B / STAGE 4 — FULL ENUMERATION OF EVERY MOVED PLAYER')
L.append('board 6c9f8d3a92ca82c29dfaa8273a4f3ada  ->  b490ae8b3bbd28b908ccb923ed8412c1')
L.append('mechanism: lam_eff = lam ** (1 + PED_BAR*(1-q)),  PED_BAR = %.4g,  q = ped(pick) x sit(depth)' % G['PED_BAR'])
L.append('')
L.append('SCOPE OF THE MOVE')
L.append('  board rows compared            : %d' % len(shared))
L.append('  MOVED                          : %d  (%.2f%% of the board)' % (len(recs), 100.0 * len(recs) / len(shared)))
L.append('    cuts (price down)            : %d' % len(downs))
L.append('    lifts (price up)             : %d' % len(ups))
L.append('  board total                    : %d -> %d  (%+d, %+.4f%%)' % (ta, tb, tb - ta, 100.0 * (tb - ta) / ta))
L.append('  every mover is on the sit-out (thin-record) path: %s' % all(r['on_sitout_path'] for r in recs))
L.append('  mean |rel| across movers       : %.4f%%' % (100.0 * float(np.mean([abs(r['rel']) for r in recs]))))
L.append('  largest cut                    : %+.2f%%   largest lift: %+.2f%%'
         % (100.0 * min(r['rel'] for r in recs), 100.0 * max(r['rel'] for r in recs)))
L.append('')
L.append('WHY A PLAYER MOVES UP. The bar is SYMMETRIC (owner law L-SYMMETRY, register item 108). A thin')
L.append('record BELOW its anchor is the same small sample as one above it, so a low-pedigree player whose')
L.append('few games went badly is likewise held nearer his anchor and his price RISES. A one-sided max()')
L.append('would be a branch and is refused under L-SMOOTH. All %d up-movers are listed below like the rest.' % len(ups))
L.append('')
L.append('=' * 152)
L.append('EVERY MOVED PLAYER, SORTED BY |relative move|  (n=%d, NO CAP)' % len(recs))
L.append('=' * 152)
hdr = ('%-26s %-5s %-22s %7s %7s %7s %8s | %6s %6s %6s %6s | %s'
       % ('player', 'pos', 'entry', 'old', 'new', 'abs', 'rel', 'lam0', 'lam1', 'q', 'anchor', 'triggering record'))
L.append(hdr); L.append('-' * 152)
for r in recs:
    L.append('%-26s %-5s %-22s %7d %7d %+7d %+7.2f%% | %6.3f %6.3f %6.3f %6.0f | %s'
             % (r['player'][:26], r['pos'], r['entry'][:22], r['old'], r['new'], r['abs'], 100.0 * r['rel'],
                r['lam_before'], r['lam_after'], r['q'], r['draft_day_anchor'], r['career_by_season']))
L.append('')
L.append('=' * 152)
L.append('THE TRIGGERING RECORD IN FULL, same order')
L.append('=' * 152)
for i, r in enumerate(recs, 1):
    L.append('%3d. %s  (%s, %s, drafted %s)' % (i, r['player'], r['pos'], r['entry'], r['draft_year']))
    L.append('     price            : %d -> %d   (%+d, %+.2f%%)   [engine ev() on this build %d]' % (r['old'], r['new'], r['abs'], 100.0 * r['rel'], r['ev_this_build']))
    L.append('     career by season : %s   (career %dg, best season %dg @ %.1f)'
             % (r['career_by_season'], r['career_games'], r['best_season_games'], r['best_season_avg']))
    L.append('     route debut year : %s   first played: %s   LEAD SIT-OUT YEARS: %d   all listed non-playing years: %s (n=%d)'
             % (r['route_debut_year'], r['first_played_year'], r['lead_sitout_years'], r['sitout_years'], r['sitout_years_n']))
    L.append('     draft-day anchor : %.2f   retention R at depth: %.5f   2026 games: %d (%.2f at pace)'
             % (r['draft_day_anchor'], r['retention_R'], r['games_2026'], r['games_at_pace']))
    L.append('     mechanism        : ped %.4f x sit %.4f = q %.4f  ->  exponent %.4f  ->  lam %.4f -> %.4f'
             % (r['ped'], r['sit'], r['q'], r['exponent'], r['lam_before'], r['lam_after']))
    L.append('')
open(os.path.join(OUT, 'MOVERS_FULL.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(recs, open(os.path.join(OUT, 'movers_full.json'), 'w'), indent=1)
print('\n'.join(L[:40]))
print('... wrote movers_full.csv / movers_full.json / MOVERS_FULL.txt  (%d movers)' % len(recs))
