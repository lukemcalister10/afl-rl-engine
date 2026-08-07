"""#334 stage B / STAGE 4 — THE PROBES (b) MRAZ, (c) THE PEDIGREE PAIR, (d) THE BOUNDARY DiD.

Counterfactual pattern carried from docs/evidence/act_336_variant_2026-08-06/ (seam_boundary.py): hold ONE
player fixed and vary ONE property, price both, difference the differences. The two findings that file
recorded are honoured here:
  * _PE_CACHE keys on id(p) -- a freed copy's address can be reused and hit a stale entry. EVERY copy is
    HELD in a list and MA._pe_clear() is called before every price.
  * one engine per process -- nothing is rebound, this file only reads.
ONE ADDITIONAL DISCLOSURE, specific to these probes. `v0_start` reads the FROZEN _V0CURVE, which is keyed on
(player, year, pick, type, dob, pos, effpk) and is prebuilt only for ACTUAL roster members. A counterfactual
with a changed pick would MISS it and silently fall back to the unfrozen `_v0_raw` -- a different ruler from
the one the board uses, which would corrupt exactly the anchor these probes are comparing. So each
counterfactual's curve entry is INSTALLED from the engine's own frozen `star(pos, ageR, pick)` before pricing.
That is the same function the board's own entries were written from (_build_v0_curve's last line), so the
probe and the board are on ONE ruler by construction.

RL_TAG names the build. READ-ONLY on the engine and the store.
"""
import os, sys, io, json, copy, contextlib
import numpy as np

REPO = os.environ.get('RL_REPO'); WORKDIR = '/home/claude/rl_workspace/rl_after'
OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
TAG = os.environ.get('RL_TAG', 'untagged')
sys.path.insert(0, REPO + '/vendor'); os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s4_probe'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; Y = 2026
star = G['_V0CURVE_META']['_star']; _V0CURVE = G['_V0CURVE']; _v0key = G['_v0key']; _ageR = G['_ageR']
HELD = []
L = []
def say(s=''): L.append(s); print(s)

def price(p):
    """Price a (possibly counterfactual) row on the board ruler."""
    HELD.append(p)
    MA._pe_clear()
    _V0CURVE[_v0key(p)] = star(MA.gfut(p), _ageR(p), min(max(MA.effpk(p), 1), 90))
    G['_V0C'].clear(); G['_V0U'].clear()
    return G['ev'](p, Y), G['v0_start'](p)

def variant(base, pick=None, draft_year=None, games=None, avg=None, season=None, by_shift=0, name=None):
    """Build a counterfactual row. EVERY derived field the ev() path reads must move with the property being
    varied, or the probe is silently inert. Three were found the hard way and are set explicitly here:
      `_eff`  -- MA.effpk() reads the LOAD-TIME cached `_eff` FIRST (rl_model.py:214) and only falls back to
                 `pick`. Setting `pick` alone leaves the engine reading the ORIGINAL pedigree: the first cut of
                 this probe returned pick 3 == pick 35 to the point, which is what exposed it.
      `_eyr` / `stream_*` -- the entry-year mirrors written at load (rl_model.py:261).
      `_by` / `_bd` -- MA.age reads `_by`, not a `dob` field.
    `_pr` / `_v` / `_vpt` / `_cvx` are board-side display fields written AFTER pricing and are never read by
    ev(); they are left stale on the copy deliberately rather than faked."""
    p = copy.deepcopy(base)
    if name: p['player'] = name
    if pick is not None:
        p['pick'] = pick
        p['_eff'] = pick if 1 <= pick <= MA.ND_CURVE_LAST else MA.POOL_PICK
        p['_pool'] = pick > MA.ND_CURVE_LAST
        p['stream_pick'] = pick
    if draft_year is not None:
        p['year'] = draft_year; p['_eyr'] = draft_year; p['stream_year'] = draft_year
    if by_shift:
        if p.get('_by'): p['_by'] = int(p['_by']) + by_shift
        if p.get('_bd'): p['_bd'] = '%d%s' % (int(str(p['_bd'])[:4]) + by_shift, str(p['_bd'])[4:])
    if games is not None or avg is not None or season is not None:
        yr = season if season is not None else Y
        p['scoring'] = [dict(year=yr, games=(games if games is not None else 4), avg=(avg if avg is not None else 84.25))]
    return p

MRAZ = next(x for x in MA.data if x.get('key') == 'noah-mraz')
say('=' * 100)
say('#334 stage B / STAGE 4 PROBES   build tag: %s   PED_BAR=%s   engine head in workspace' % (TAG, G.get('PED_BAR', 'n/a (base engine)')))
say('=' * 100)

# ---------------- (b) THE MRAZ PROBE -------------------------------------------------------------
say('')
say('(b) THE MRAZ PROBE')
say('-' * 100)
ev_m, v0_m = G['ev'](MRAZ, Y), G['v0_start'](MRAZ)
fe = G['_fEy'](Y, MRAZ); tau = max(0.0, Y - cp.debutyr(MRAZ)) + fe ** 1.5
cls = G['_sitout_cls'](MA.gfut(MRAZ)); pk = MA.effpk(MRAZ)
R = G['_R_surf'](cls, pk, tau); gy = 4
lam0 = float(np.interp(min(gy / fe, 6.0), [0, 1, 2, 3, 4, 5, 6], G['LAM_SIT']))
efull = G['_prod_path'](MRAZ, Y)
say('  Noah Mraz  KPD  ND pick 35 (2024)  route debut year %d  year-1 sit-out (2025, 0 games)' % cp.debutyr(MRAZ))
say('  record            : 2026 only, 4 games @ 84.25   (season %.0f%% elapsed, so 4 games = %.2f at the prorated 6-game bar)' % (100 * fe, gy / fe))
say('  engine ev()       : %d' % ev_m)
say('  draft-day anchor  : %.2f   retention at depth tau=%.3f : %.5f   anchor leg R*V0 = %.2f' % (v0_m, tau, R, R * v0_m))
say('  production path   : %.2f   (raw_ev x iso x L1c on a 4-game 84.25 season)' % efull)
say('  lam (pedigree-blind): %.6f' % lam0)
if 'PED_BAR' in G:
    q = G['_ped_prior'](MRAZ, Y, fe, tau, cls, pk); ex = 1.0 + G['PED_BAR'] * (1.0 - q)
    ped = 1.0 - float(np.log(min(max(pk, 1), 90)) / np.log(90.0))
    tau0 = fe ** 1.5; sit = G['_R_surf'](cls, pk, tau) / G['_R_surf'](cls, pk, tau0)
    say('  ped(35)=%.6f  x  sit(year-1 sit-out)=%.6f  =  q=%.6f  ->  exponent %.6f' % (ped, sit, q, ex))
    say('  lam (conditioned) : %.6f' % (lam0 ** ex))
say('  blend             : (1-lam)*R*anchor + lam*e_full = %.2f' % G['sitout_ev'](MRAZ, Y, efull))

# ---------------- (c) THE PEDIGREE PAIR ----------------------------------------------------------
say('')
say('(c) THE PEDIGREE PAIR — one record (one season, 4 games @ 84.25, KPD, age/position matched to Mraz),')
say('    priced under four entry histories. Full 2x2: pick {3,35} x {straight year-1 debut, year-1 sit-out}.')
say('-' * 100)
cells = {}
for hold, shift_straight in (('DRAFT-AGE HELD', +1), ('AS-OF-AGE HELD', 0)):
    say('')
    say('  HOLD = %s' % hold)
    if hold == 'DRAFT-AGE HELD':
        say('    the 2025-drafted arms carry a DOB shifted one year later, so every arm is drafted at the SAME')
        say('    draft age as Mraz and the year-zero anchor star(pos, draft-age, pick) differs ONLY by pick.')
        say('    Consequence, disclosed: the sit-out arms are one year older AS OF 2026 (20 vs 19) — real and')
        say('    unavoidable, a player who sat a year IS a year older now.')
    else:
        say('    birth year held at Mraz\'s, so every arm is the SAME age as of 2026 (20). Consequence, disclosed:')
        say('    the 2025-drafted arms were then drafted a year OLDER, which moves the year-zero anchor.')
    say('    %-46s %8s %10s' % ('arm', 'price', 'anchor'))
    for label, pick, dy, sit in (('(i)   pick 3,  straight year-1 debut', 3, 2025, False),
                                 ('(ii)  pick 35, year-1 sit-out  [= Mraz-shaped]', 35, 2024, True),
                                 ('(iii) pick 3,  year-1 sit-out', 3, 2024, True),
                                 ('(iv)  pick 35, straight year-1 debut', 35, 2025, False)):
        p = variant(MRAZ, pick=pick, draft_year=dy, games=4, avg=84.25, season=Y,
                    by_shift=(0 if sit else shift_straight),
                    name='PROBE %s p%d %s' % (hold, pick, 'sit' if sit else 'straight'))
        v, a = price(p)
        cells[(hold, label[:5].strip())] = v
        say('    %-46s %8d %10.1f' % (label, v, a))
    gi = cells[(hold, '(i)')]; gii = cells[(hold, '(ii)')]; giii = cells[(hold, '(iii)')]; giv = cells[(hold, '(iv)')]
    say('    GAP (i) - (ii)  = %+d   ratio (i)/(ii) = %.4f      <-- THE OWNER\'S JUDGMENT NUMBER' % (gi - gii, gi / gii))
    say('    pure pedigree, straight debut  (i)/(iv)   = %.4f' % (gi / giv))
    say('    pure pedigree, after a sit-out (iii)/(ii) = %.4f' % (giii / gii))
    say('    pure sit-out at pick 3  (iii)/(i)  = %.4f      pure sit-out at pick 35 (ii)/(iv) = %.4f' % (giii / gi, gii / giv))

# ---------------- (d) THE BOUNDARY DiD -----------------------------------------------------------
say('')
say('(d) THE BOUNDARY CHECK — the 5g -> 6g step at the establishment bar, seam_boundary DiD style.')
say('    A player crosses the bar when games AT PACE reach 6, i.e. games >= 6*fE = %.2f. The probe steps him' % (6 * G['_fEy'](Y, MRAZ)))
say('    from 5 to 6 RAW games either side of that. If the change introduced a cliff at the bar, the SEAM')
say('    RATIO (the step on this build divided by the step on the base build) would move away from 1.')
say('-' * 100)
PROBE_KEYS = ['noah-mraz', 'josh-smillie', 'charlie-west', 'samuel-swadling']
seam = {}
say('    %-22s %-5s %5s %9s %9s %9s %9s' % ('probe player', 'pos', 'pick', 'ev@5g', 'ev@6g', 'step', 'step/5g'))
for k in PROBE_KEYS:
    b = next((x for x in MA.data if x.get('key') == k), None)
    if b is None: continue
    a5 = price(variant(b, games=5, avg=84.25, season=Y, name='SEAM %s 5g' % k))[0]
    a6 = price(variant(b, games=6, avg=84.25, season=Y, name='SEAM %s 6g' % k))[0]
    seam[k] = dict(g5=a5, g6=a6, step=a6 - a5, rel=(a6 - a5) / max(a5, 1))
    say('    %-22s %-5s %5d %9d %9d %+9d %+8.3f%%' % (b.get('player')[:22], MA.gfut(b), MA.effpk(b), a5, a6, a6 - a5, 100.0 * (a6 - a5) / max(a5, 1)))
say('')
say('    fine sweep of the same players across the bar (raw games 3..8), to show the crossing is smooth:')
for k in PROBE_KEYS:
    b = next((x for x in MA.data if x.get('key') == k), None)
    if b is None: continue
    vals = [price(variant(b, games=g, avg=84.25, season=Y, name='SWEEP %s %dg' % (k, g)))[0] for g in range(3, 9)]
    say('    %-22s %s' % (b.get('player')[:22], '  '.join('%d:%d' % (g, v) for g, v in zip(range(3, 9), vals))))

json.dump(dict(tag=TAG, ped_bar=G.get('PED_BAR'), mraz=dict(ev=ev_m, v0=v0_m, lam=lam0, efull=efull, R=R),
               cells={'%s|%s' % kk: vv for kk, vv in cells.items()}, seam=seam),
          open(os.path.join(OUT, 'probes_%s.json' % TAG), 'w'), indent=1)
open(os.path.join(OUT, 'probes_%s.txt' % TAG), 'w').write('\n'.join(L) + '\n')
