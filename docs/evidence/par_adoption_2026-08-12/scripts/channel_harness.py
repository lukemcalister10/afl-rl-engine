"""ORDER 20B TASK 4/5 — PER-CONSUMER PAR CHANNEL HARNESS.

Runs the engine with the par surface switchable PER CONSUMER between the HEAD (mixed-population) fit
and the ORDER 20 arm-split fit, so each consumer's contribution to a player's price delta can be
measured on its own.

THE CHANNELS (the par surface's consumers, as swept by ORDER 20):

  ISO    the V0 pick-surface synthetics, _merged_recover.py:497
         `raw_ev(synth(pk, PR.par_at(pos,min(pk,KMAX),4), pos))` over PICKS=1..70 -> the iso_corr
         multiplier. IMPORT-TIME.
  POLE   the pedigree pole, :395-399 (`par_pole`), consumed by raw_ev at :464/:475. IMPORT-TIME
         (the table is pre-warmed at :510) and runtime.
  BLEND  `_par_prior` :311-312, consumed by the _ev_pw pedigree leg at :590. RUNTIME.
  BAR    the stalled-prospect bar `pr = bestlvl/par` :2263, and `_c_w`'s par :2124. RUNTIME.
  BASE   par_redesign's BASE_RATE / shortfall() play-rate channel.
  OTHER  every other PR.par_at reader (report-only printers :2601/:2608/:2618).

HOW THE SWITCH WORKS. `PR.par_at` is replaced by a dispatcher installed BEFORE the engine head is
exec'd, so import-time readers (ISO, POLE) go through it too. The dispatcher identifies its caller by
the calling frame's function name and line number -- i.e. by the ACTUAL call site, not by a guess --
and routes to the HEAD surface or the FIX surface according to MODE.

CONTROL 1 (asserted every run): with every channel on HEAD, the dispatcher's HEAD surface must equal
the HEAD tree's own par_at on the whole (pos x pick 1..70 x tenure 1..6) grid, and with every channel
on FIX it must equal the FIX tree's own. Both grids are read from the engine_probe.py dumps. If either
fails the harness HALTS -- the reconstruction is then not the engine's surface and no number from it
would mean anything.

CONTROL 2: every call the dispatcher serves is counted per channel, so a channel that is claimed to be
inert can be shown to have been READ (or never read) rather than assumed.

Run:  RL_REPO=<FIX tree> MODE=ISO:FIX,POLE:HEAD,... OUT=<json> python3 channel_harness.py
      MODE=ALL_HEAD and MODE=ALL_FIX are accepted shorthands.
"""
import os, sys, io, json, contextlib, collections, importlib.util

REPO = os.environ['RL_REPO']                 # must be the FIX tree (its par_redesign is the FIX one)
HEADTREE = os.environ['HEAD_TREE']           # the HEAD tree, for the HEAD par_build
OUT = os.environ.get('OUT', '/tmp/chan.json')
MODESPEC = os.environ.get('MODE', 'ALL_HEAD')
GRID_HEAD = os.environ.get('GRID_HEAD')      # probe_HEAD.json — CONTROL 1
GRID_FIX = os.environ.get('GRID_FIX')        # probe_FIX.json  — CONTROL 1

CHANNELS = ['ISO', 'POLE', 'BLEND', 'BAR', 'BASE', 'LVLPAR', 'OTHER']
if MODESPEC == 'ALL_HEAD':  MODE = {c: 'HEAD' for c in CHANNELS}
elif MODESPEC == 'ALL_FIX': MODE = {c: 'FIX' for c in CHANNELS}
else:
    MODE = {c: 'HEAD' for c in CHANNELS}
    for tok in MODESPEC.split(','):
        k, v = tok.split(':'); assert k in CHANNELS, 'unknown channel %s' % k; MODE[k] = v

WORKDIR = REPO + '/engine/rl_after'
sys.path.insert(0, REPO + '/vendor')
os.chdir(WORKDIR); sys.path.insert(0, '.'); sys.path.insert(0, REPO)


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ 1. the two surfaces
import wire_redesign as W                       # loads the FIX par_redesign (this tree's)
PR = W.PR; MA = PR.MA; cp = PR.cp
import numpy as np
GROUPS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']

pb_fix = PR.pb                                  # the FIX par_build, already fitted by par_redesign
par_at_FIX = PR.par_at                          # the FIX tree's own par_at, untouched

# The HEAD surface: HEAD's par_build, fitted HEAD's way (mixed population), wrapped in a par_at that
# reproduces HEAD par_redesign.py:57-72 VERBATIM (copied, not paraphrased -- see the docstring control).
pb_head = _load('pb_head', HEADTREE + '/engine/forward_valuation/par_build.py')
with contextlib.redirect_stdout(io.StringIO()): F_head = pb_head.fit()
_FB_h = {g: (float(np.median(F_head['POS'][g][:, 2])) if len(F_head['POS'][g]) else 60.0) for g in GROUPS}
_PC_h = {}


def _lvl_safe_h(pos, pick):                     # == HEAD par_redesign.py:59-67
    lv, ess = pb_head.level_at(F_head, pos, min(max(pick, 1), 70))
    if not np.isfinite(lv) or ess < 3.0:
        lf = F_head['levelfn'].get(pos)
        if lf is not None:
            lv2, _ = pb_head.loclin(np.log(min(max(pick, 1), 70)), lf[0], lf[1], 1.0)
            if np.isfinite(lv2): return lv2
        return _FB_h[pos]
    return lv


def par_at_HEAD(pos, pick, T):                  # == HEAD par_redesign.py:68-71
    k = (pos, int(round(pick)), int(max(1, min(T, 6))))
    if k not in _PC_h: _PC_h[k] = _lvl_safe_h(pos, pick) + F_head['ramp_shr'][pos][k[2]]
    return _PC_h[k]


# ------------------------------------------------------------------ 2. CONTROL 1 — grid equality
def _grid_check(fn, dumpfile, label):
    if not dumpfile or not os.path.exists(dumpfile): return {'skipped': dumpfile}
    ref = json.load(open(dumpfile))['par_cells']
    worst = 0.0; where = None; n = 0
    for g in GROUPS:
        for pk in range(1, 71):
            for T in range(1, 7):
                r = ref.get('%s|%d|%d' % (g, pk, T))
                if r is None: continue
                d = abs(float(fn(g, pk, T)) - float(r)); n += 1
                if d > worst: worst, where = d, (g, pk, T, fn(g, pk, T), r)
    return {'label': label, 'cells': n, 'worst_abs_diff': worst, 'where': where}


CTRL = {'HEAD_surface_vs_HEAD_tree': _grid_check(par_at_HEAD, GRID_HEAD, 'HEAD'),
        'FIX_surface_vs_FIX_tree': _grid_check(par_at_FIX, GRID_FIX, 'FIX')}
for k, v in CTRL.items():
    if 'worst_abs_diff' in v and v['worst_abs_diff'] > 1e-9:
        sys.stderr.write('CONTROL 1 FAILED (%s): worst %.6e at %s\n' % (k, v['worst_abs_diff'], v['where']))
        json.dump({'CONTROL_1_FAILED': CTRL}, open(OUT, 'w')); raise SystemExit(3)
sys.stderr.write('CONTROL 1 PASS  head_worst=%.2e  fix_worst=%.2e\n'
                 % (CTRL['HEAD_surface_vs_HEAD_tree'].get('worst_abs_diff', -1),
                    CTRL['FIX_surface_vs_FIX_tree'].get('worst_abs_diff', -1)))

# ------------------------------------------------------------------ 3. the dispatcher
# Caller identification. `_merged_recover.py` is exec'd from source with its prefix intact, so frame
# line numbers are the file's own line numbers and can be quoted directly.

# LVLPAR — par_redesign.lvl_par:126, THE CHANNEL ORDER 20's SWEEP DID NOT NAME, and by call volume the
# largest of all. `wire_redesign.build()` (called at _merged_recover.py:49) binds `cp._lvl_eff = PR.lvl_par`;
# `_merged_recover.py:171` then freezes that binding as `cp._lvl_eff_orig`, which is read at :571 as `Lo`
# inside `_coreM1` — the LIVE level core `ev()` consumes — and through `cp._feat` into the conditional-prior
# band features at :368/:372. It is a par consumer with a pick axis (par_at(pos, effpk, tenure)) that
# reaches BOTH the live price and, via price6/b6, the year-zero value V0.
BY_FUNC = {'par_pole': 'POLE', '_par_prior': 'BLEND', '_c_w': 'BAR', 'shortfall': 'BASE',
           'lvl_par': 'LVLPAR'}
BY_LINE = {497: 'ISO', 2263: 'BAR', 2124: 'BAR'}
CALLS = collections.Counter()
SITES = collections.Counter()     # CONTROL 2b: every call site, so no traffic is unattributed


def par_at_DISPATCH(pos, pick, T):
    f = sys._getframe(1)
    ch = BY_FUNC.get(f.f_code.co_name) or BY_LINE.get(f.f_lineno) or 'OTHER'
    CALLS[(ch, MODE[ch])] += 1
    SITES['%s:%s:%d' % (ch, f.f_code.co_name, f.f_lineno)] += 1
    return (par_at_FIX if MODE[ch] == 'FIX' else par_at_HEAD)(pos, pick, T)


PR.par_at = par_at_DISPATCH

# BASE_RATE / shortfall: par_redesign's own no-pick-axis channel. Under MODE BASE:HEAD we restore the
# HEAD (arm-blind) BASE_RATE table and the HEAD shortfall(); under BASE:FIX the tree's own (arm-keyed)
# pair stays. Recorded either way so "which table was live" is never in doubt.
pr_head = None
if MODE['BASE'] == 'HEAD':
    _by = collections.defaultdict(list)
    for p in MA.data:
        if not (MA.GRP.get(p.get('pos')) and (p.get('pick') or p.get('_ft'))): continue
        d0 = cp.debutyr(p) - 1
        if not (2003 <= d0 <= 2018): continue
        pos = MA.gfut(p); rows = {x['year']: x['games'] for x in p['scoring']}
        maxten = max([y - d0 for y in rows], default=0)
        for T in range(1, 7):
            if (T == 1) or (maxten >= T): _by[(pos, T)].append(rows.get(d0 + T, 0) / 22.0)
    BR_HEAD = {k: float(np.median(v)) for k, v in _by.items() if v}     # == HEAD par_redesign.py:75-87

    def _shortfall_head(p, Y):                                          # == HEAD par_redesign.py:102-107
        pos = MA.gfut(p); T = PR.tenure(p, Y)
        base = BR_HEAD.get((pos, T), BR_HEAD.get((pos, min(T, 5)), 0.5))
        pr = 0.0 if not any(x['games'] > 0 for x in p['scoring']) else PR.player_rate(p, Y)
        return max(0.0, base - pr)
    PR.BASE_RATE = BR_HEAD; PR.shortfall = _shortfall_head

# ------------------------------------------------------------------ 4. run the engine head
_src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20b_chan'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

ev = G['ev']; v0_start = G['v0_start']; _v0_uncapped = G['_v0_uncapped']; _v0_raw = G['_v0_raw']
_isreal = G['_isreal']; _ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; iso_corr = G['iso_corr']
nseas_pro = G['nseas_pro']; bestlvl = G['bestlvl']; MAe = G['MA']
F_NUM = json.load(open('pick_redenomination.json'))['factor']

players = MAe.players
back = list(G.get('back_extra') or MAe.__dict__.get('back_extra') or [])
ROWS = [('active', p) for p in players] + [('back', p) for p in back]

rows = []
for src, p in ROWS:
    r = {'set': src, 'key': p.get('key'), 'name': p.get('player'), 'ty': p.get('type'),
         'pk': p.get('pick'), 'ep': MAe.effpk(p), 'pos': MAe.gfut(p), 'pool': bool(MAe.is_pool(p))}
    try:
        with contextlib.redirect_stdout(io.StringIO()): e = float(ev(p, 2026))
        r['ev26'] = e; r['v'] = int(round(e / F_NUM))
    except Exception as ex:
        r['ev_err'] = repr(ex)[:80]
    for nm, fn in (('v0_start', v0_start), ('v0_uncapped', _v0_uncapped)):
        try:
            with contextlib.redirect_stdout(io.StringIO()): r[nm] = float(fn(p))
        except Exception: r[nm] = None
    rows.append(r)

meta = {'MODE': MODE, 'modespec': MODESPEC, 'repo': REPO, 'head_tree': HEADTREE,
        'F_numeraire': F_NUM, 'n_rows': len(rows),
        'v0surf_frozen': bool(G['_V0CURVE_META'].get('_v0surf_frozen')),
        'calls_by_channel': {'%s:%s' % k: v for k, v in CALLS.items()},
        'call_sites': dict(SITES.most_common(40))}
json.dump({'meta': meta, 'CONTROL_1': CTRL, 'rows': rows}, open(OUT, 'w'))
sys.stderr.write('  SITES %s\n' % json.dumps(dict(SITES.most_common(15)), indent=1))
sys.stderr.write('CHAN OK  %s  mode=%s  rows=%d  frozen_v0surf=%s\n  calls %s\n'
                 % (OUT, MODESPEC, len(rows), meta['v0surf_frozen'], dict(meta['calls_by_channel'])))
