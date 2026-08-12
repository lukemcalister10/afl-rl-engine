"""ORDER 20B TASK 5 — THE DEAD-ZONE CROSS-CHECK.

For each named mover, evaluate THE ENGINE'S OWN GATING CONDITIONS, in the engine, at the same clock the
engine uses — so the channel attribution in Task 4 can be checked against which consumers were actually
ALLOWED to fire for that player, rather than against a story about which ones sound plausible.

Reported per player:
  Eq              _ev_qual(p,2026) — the evidence axis every weight keys on
  pw = _ev_pw(Eq) the PEDIGREE-PAR blend weight at :590. ~0 => the BLEND channel is DEAD for him.
  pole w          wage x tfade x expgate at :464-472, evaluated at Y=2026 AND at Y=debutyr-1 (the V0
                  clock). The engine asserts w==0 at the V0 clock; that assertion is re-measured here.
  el, ns          the stalled-bar clock `el = PR.tenure(p,_fa_year(Y))` UNDER THE FORM-ANCHOR CLOCK
                  (:2262) and `ns = nseas_pro(p,2026)` — the two the bar actually branches on.
  bar branch      which of the three :2263+ branches he lands in: SIT-OUT (ns==0), STALLED
                  (el>=onset and ns<=1), MEDIOCRE (el>=onset+2 and pr<0.55), or NONE.
  pr              bestlvl/par — the stalled bar's ratio itself.

Run: RL_REPO=<tree> OUT=<json> python3 gating_probe.py
"""
import os, sys, io, json, contextlib

REPO = os.environ['RL_REPO']; OUT = os.environ.get('OUT', '/tmp/gate.json')
sys.path.insert(0, REPO + '/vendor')
os.chdir(REPO + '/engine/rl_after'); sys.path.insert(0, '.'); sys.path.insert(0, REPO)
_src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20b_gate'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

MA = G['MA']; PR = G['PR']; cp = G['cp']
import numpy as np
NAMED = ['Harry Dean', 'Angus Clarke', 'Harvey Johnston', 'James Leake', 'Willem Duursma',
         'Will Hayes', 'Luke Cleary']
rows = {p.get('player'): p for p in MA.players}
res = {}
for nm in NAMED:
    p = rows.get(nm)
    if p is None: res[nm] = {'ERROR': 'not on the board'}; continue
    Y = 2026
    pos = MA.gfut(p); ep = MA.effpk(p)
    with contextlib.redirect_stdout(io.StringIO()):
        Eq = float(G['_ev_qual'](p, Y)); pw = float(G['_ev_pw'](Eq))
        # the stalled-bar clock, under the engine's own form-anchor context (:2262)
        with G['_form_anchor_clock'](): el = int(PR.tenure(p, G['_fa_year'](Y)))
        ns = int(G['nseas_pro'](p, Y))
        par = float(PR.par_at(pos, min(ep, cp.KMAX), min(max(el, 1), 6)))
        bl = float(G['bestlvl'](p, Y))
        v0 = float(G['v0_start'](p))
        # the pole weight, at the live clock and at the V0 clock
        def polew(YY):
            with G['_form_anchor_clock']():
                T = min(max(PR.tenure(p, G['_fa_year'](YY)), 1), 6)
                et = min(max(G['eff_ten'](p, G['_fa_year'](YY), PR.tenure(p, G['_fa_year'](YY))), 1), 6)
                a = MA.age(p)
                wage = float(np.clip(1 - ((a or 21) - 20) / 6, 0, 1)) * (G['RUC_WAGE'] if pos == 'RUCK' else 1.0)
                tfade = float(np.interp(et, [1, 2, 3, 4, 5, 6], [1.00, 0.76, 0.40, 0.16, 0.05, 0.05]))
                eg = float(G['_expgate'](p, YY))
            return wage * tfade * eg, wage, tfade, eg, T, et
        w26 = polew(Y); w0 = polew(cp.debutyr(p) - 1)
    # LVLPAR's own gate. par_redesign.lvl_par:126 is
    #     lvl_par = par + (cp._lvl_wt(p,Y) - par) * w ,   w = min(1, cp._exposure(p,Y)/RAMP)
    # so d(lvl_par)/d(par) = (1 - w): when exposure >= RAMP the weight saturates at 1 and PAR CANCELS
    # EXACTLY — the LVLPAR channel is dead for that player by construction, not by smallness.
    with contextlib.redirect_stdout(io.StringIO()):
        expo = float(cp._exposure(p, Y)); RAMP = float(PR.RAMP)
        lw = float(cp._lvl_wt(p, Y))
    w_lvlpar = min(1.0, expo / RAMP)
    pr = bl / max(1.0, par)
    keyruc = pos in ('KPF', 'KPD', 'RUCK'); onset = (4 if keyruc else 3)
    if ns == 0: branch = 'SIT-OUT (ns==0) -> sitout_ev, V0-anchored'
    elif el >= onset and ns <= 1: branch = 'STALLED (el>=%d and ns<=1)' % onset
    elif el >= onset + 2 and pr < 0.55: branch = 'MEDIOCRE (el>=%d and pr<0.55)' % (onset + 2)
    else: branch = 'NONE — neither staleness branch fires'
    res[nm] = {'pos': pos, 'ep': ep, 'Eq': Eq, 'pw_blend_weight': pw,
               'blend_active': bool(pw > 0.02),
               'el_form_anchor': el, 'ns_pro': ns, 'onset': onset, 'par_at_bar': par,
               'bestlvl': bl, 'pr_ratio': pr, 'bar_branch': branch,
               'v0_start': v0,
               'exposure': expo, 'RAMP': RAMP, 'lvl_wt': lw,
               'lvlpar_w': w_lvlpar, 'lvlpar_sensitivity_1_minus_w': 1.0 - w_lvlpar,
               'lvlpar_active': bool(w_lvlpar < 1.0 - 1e-12),
               'pole_w_2026': w26[0], 'pole_wage_2026': w26[1], 'pole_tfade_2026': w26[2],
               'pole_expgate_2026': w26[3], 'pole_T_2026': w26[4], 'pole_et_2026': w26[5],
               'pole_w_at_V0clock': w0[0], 'pole_expgate_at_V0clock': w0[3]}

json.dump({'repo': REPO, 'arm_split': bool(getattr(PR, 'F', {}).get('ARM_POOL') is not None),
           'movers': res}, open(OUT, 'w'), indent=1, default=float)
sys.stderr.write('GATING OK -> %s\n' % OUT)
