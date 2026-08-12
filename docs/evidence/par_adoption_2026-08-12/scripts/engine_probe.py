"""ORDER 20B — ENGINE PROBE. One process, one tree, one JSON.

Emits, for the tree named by RL_REPO:
  * per-row v0 (`v0_start`, `_v0_uncapped`, `_v0_raw`) for EVERY row the engine carries, BOTH arms,
    with the arm/position/pick keys the deltas are cut by;
  * the board value the export would write for that row  (board v == round(ev(p,2026) / F), the
    numéraire identity asserted by rl_export.py:617 — reproduced here, not re-derived);
  * `_v0_curve_assert()` — the D14 gates — verbatim;
  * `_ruc_prior_cap` binding: which RUCK rows the V0 prior-scaffold cap actually binds on, and by how much;
  * the par surface itself, position x pick x tenure, so the per-cell direction is on the record.

It execs the engine head exactly as rl_export.py:68 and the ORDER 20 instruments do
(`exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)`), so every number is the
engine's own and no valuation logic is re-implemented here.

Run:  RL_REPO=<tree> OUT=<path.json> python3 engine_probe.py
"""
import os, sys, io, json, contextlib, collections

REPO = os.environ['RL_REPO']
OUT = os.environ.get('OUT', '/tmp/probe.json')
WORKDIR = REPO + '/engine/rl_after'
sys.path.insert(0, REPO + '/vendor')
os.chdir(WORKDIR); sys.path.insert(0, '.'); sys.path.insert(0, REPO)

_src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20b_probe'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

MA = G['MA']; PR = G['PR']; cp = G['cp']
ev = G['ev']; v0_start = G['v0_start']; _v0_uncapped = G['_v0_uncapped']; _v0_raw = G['_v0_raw']
_ruc_prior_cap = G['_ruc_prior_cap']; _isreal = G['_isreal']; _ageR = G['_ageR']
_ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; _cap_basis = G['_cap_basis']
_ruc_head_v0 = G['_ruc_head_v0']; RUC_PRIOR_CAP = G['RUC_PRIOR_CAP']
iso_corr = G['iso_corr']; nseas_pro = G['nseas_pro']; bestlvl = G['bestlvl']

F_NUM = json.load(open('pick_redenomination.json'))['factor']   # rl_export.py:132

# ---------------------------------------------------------------- the population
# `players` is the exported ACTIVE board population (rl_export.py:114 takes it from this same MA);
# `back_extra` are the recall rows the board carries on the -1/-2 lenses. BOARD_DELTA_par_armsplit.json
# scored `active + back`, so both are emitted and each row is tagged with which set it came from.
players = MA.players
back = list(G.get('back_extra') or MA.__dict__.get('back_extra') or [])
ROWS = [('active', p) for p in players] + [('back', p) for p in back]


def _f(x):
    try:
        x = float(x)
        return x if x == x and abs(x) != float('inf') else None
    except Exception:
        return None


def band(pk):
    """The #338 pick bands, quoted from rl_export.py:1 — not re-cut here."""
    if pk is None: return 'none'
    for lo, hi in ((1, 3), (4, 7), (8, 12), (13, 20), (21, 27), (28, 35), (36, 48), (49, 99)):
        if lo <= pk <= hi: return '%d-%d' % (lo, hi)
    return 'none'


out_rows = []
for src, p in ROWS:
    try:
        pool = bool(MA.is_pool(p))
    except Exception:
        pool = None
    try:
        epk = MA.effpk(p)
    except Exception:
        epk = None
    r = {'set': src, 'key': p.get('key'), 'name': p.get('player'), 'ty': p.get('type'),
         'pk': p.get('pick'), 'ep': epk, 'pos': MA.gfut(p), 'pool': pool,
         'real': bool(_isreal(p)), 'band': band(epk),
         'ageR': None, 'Eq26': None,
         'v0_start': None, 'v0_uncapped': None, 'v0_raw': None, 'ev26': None, 'v': None}
    try: r['ageR'] = int(_ageR(p))
    except Exception: pass
    try: r['Eq26'] = _f(_ev_qual(p, 2026))
    except Exception: pass
    try: r['pw26'] = _f(_ev_pw(_ev_qual(p, 2026)))
    except Exception: r['pw26'] = None
    for nm, fn in (('v0_start', v0_start), ('v0_uncapped', _v0_uncapped), ('v0_raw', _v0_raw)):
        try:
            with contextlib.redirect_stdout(io.StringIO()): r[nm] = _f(fn(p))
        except Exception as e:
            r[nm + '_err'] = repr(e)[:90]
    try:
        with contextlib.redirect_stdout(io.StringIO()): e26 = float(ev(p, 2026))
        r['ev26'] = e26; r['v'] = int(round(e26 / F_NUM))     # the numéraire identity, rl_export.py:617
    except Exception as e:
        r['ev_err'] = repr(e)[:90]
    # iso_corr is the ONLY par-fed factor in v0 (see PREREG §0) — record it so P3 can be tested directly
    try: r['iso'] = _f(iso_corr(MA.gfut(p), epk))
    except Exception: r['iso'] = None
    # tenure / stalled-bar state, for the dead-zone cross-check
    try: r['ten26'] = int(PR.tenure(p, 2026))
    except Exception: r['ten26'] = None
    try: r['nseas_pro'] = int(nseas_pro(p, 2026))
    except Exception: r['nseas_pro'] = None
    out_rows.append(r)

# ---------------------------------------------------------------- the D14 gates, verbatim
gates = {}
try:
    with contextlib.redirect_stdout(io.StringIO()): gates['v0_curve_assert'] = G['_v0_curve_assert']()
except Exception as e:
    gates['v0_curve_assert'] = {'ERROR': repr(e)[:300]}
try:
    with contextlib.redirect_stdout(io.StringIO()): gates['v0_surface_assert'] = G['_v0_surface_assert']()
except Exception as e:
    gates['v0_surface_assert'] = {'ERROR': repr(e)[:300]}

# ---------------------------------------------------------------- _ruc_prior_cap binding
# The cap is `min(v, RUC_PRIOR_CAP*_cap_basis(p)*_ruc_head_v0(p))` for REAL RUCK rows only (:1219).
# "Binding" = the ceiling is BELOW the uncapped V0, i.e. the min() actually cut.
ruc = []
for src, p in ROWS:
    if not (_isreal(p) and MA.gfut(p) == 'RUCK'): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            u = float(_v0_uncapped(p)); ceil = float(RUC_PRIOR_CAP * _cap_basis(p) * _ruc_head_v0(p))
    except Exception as e:
        ruc.append({'name': p.get('player'), 'ERROR': repr(e)[:90]}); continue
    ruc.append({'set': src, 'name': p.get('player'), 'key': p.get('key'), 'ep': MA.effpk(p),
                'pool': bool(MA.is_pool(p)), 'v0_uncapped': u, 'ceiling': ceil,
                'binds': bool(ceil < u), 'cut': (u - ceil) if ceil < u else 0.0})

# ---------------------------------------------------------------- the par surface itself
GROUPS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
par_cells = {}
for g in GROUPS:
    for pk in list(range(1, 71)):
        for T in range(1, 7):
            try: par_cells['%s|%d|%d' % (g, pk, T)] = _f(PR.par_at(g, pk, T))
            except Exception: par_cells['%s|%d|%d' % (g, pk, T)] = None
iso_tbl = {}
for g in GROUPS:
    for pk in range(1, 71):
        try: iso_tbl['%s|%d' % (g, pk)] = _f(iso_corr(g, pk))
        except Exception: iso_tbl['%s|%d' % (g, pk)] = None
# ramp_shr — the PICK-INDEPENDENT leg of par_at. Its arm split moves every pick in a (pos,T) cell equally.
ramp = {}
try:
    for g in GROUPS:
        ramp[g] = [_f(x) for x in PR.F['ramp_shr'][g]]
except Exception as e:
    ramp['ERROR'] = repr(e)[:200]

# ---------------------------------------------------------------- BASE_RATE (the no-pick-axis channel)
base_rate = {}
try:
    for k, v in PR.BASE_RATE.items(): base_rate[str(k)] = _f(v)
except Exception as e:
    base_rate['ERROR'] = repr(e)[:200]

meta = {'repo': REPO, 'F_numeraire': F_NUM, 'n_active': len(players), 'n_back': len(back),
        'par_arm_split': bool(getattr(PR, 'F', {}).get('ARM_POOL') is not None),
        'KMAX': int(cp.KMAX), 'POOL_PICK': int(MA.POOL_PICK)}
json.dump({'meta': meta, 'rows': out_rows, 'gates': gates, 'ruc_prior_cap': ruc,
           'par_cells': par_cells, 'iso': iso_tbl, 'ramp_shr': ramp, 'BASE_RATE': base_rate},
          open(OUT, 'w'))
sys.stderr.write('PROBE OK  %s  rows=%d  arm_split=%s\n' % (OUT, len(out_rows), meta['par_arm_split']))
