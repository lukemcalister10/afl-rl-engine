#!/usr/bin/env python3
"""LEG B SEGMENT-5 — per-player board dump for the ALL-804 MOVEMENT LEDGER (R105.5 item 241) + the value-flow
/ decomposition deliverables. Adapts isofade/measurement/dump.py, adding the ρ-axis fields the ledger names:
rho_num (ρ_num=rho_out), rho_ratio (ρ=ρ_num/RHO_DEN), w (=s·E·ramp, the applied evidence weight), E, ramp,
and games_in_window (Σ games over played seasons — the games that enter the games×recency weighting).

usage:  RL_UNCOMP=0 python3 ledger_dump.py <out.json>          # OFF board (A/B baseline; map inert)
        RL_UNCOMP_S=<s> python3 ledger_dump.py <out.json>      # ON board at strength s (map active)
Model vars = pinned gate values (setdefault). Currency num = round(ev/F), F=1.0524 (L7 numéraire)."""
import os, io, contextlib, sys, json, math
os.environ['PYTHONHASHSEED'] = '0'
for k, v in dict(RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                 RL_PRIOR_TREES='400', PAR_RAMPS='22').items():
    os.environ.setdefault(k, v)
out = sys.argv[1]
WS = '/home/claude/rl_workspace/rl_after'
os.environ.setdefault('RL_REPO', '/home/user/afl-rl-engine')
os.environ.setdefault('RL_Q97M_PKL', '/home/user/afl-rl-engine/data/q97m.pkl')
sys.path.insert(0, '/home/claude/rl_vendor'); sys.path.insert(0, WS); os.chdir(WS)
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(WS, '_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']; ev = g['ev']; _lvlcurr = g['_lvlcurr']; _par_prior = g['_par_prior']
_ev_qual = g['_ev_qual']; rho_out = g['rho_out']; raw_ev = g['raw_ev']; _isreal = g['_isreal']
_UC_RHODEN = g.get('_UC_RHODEN', {}); _UC_VREFB = g.get('_UC_VREFB', {})
F = 1.0524; Y = 2026
_S = MA.UNCOMP_S            # None when off; the strength dial when on
_DELTA = MA.UNCOMP_DELTA; _TAU = MA.UNCOMP_TAU

def _wfields(p, pos):
    """Reproduce the map's ρ/w for the ledger (mirrors _uncomp_prod, read-only)."""
    if not _isreal(p):
        return dict(rho_num=None, rho_ratio=None, E=0.0, ramp=0.0, w=0.0)
    _ro = rho_out(p, pos)
    Eq = float(_ev_qual(p, Y)); E = 1.0 - math.exp(-Eq/_TAU) if Eq > 0.0 else 0.0
    if _ro is None or _ro <= 0.0:
        return dict(rho_num=(None if _ro is None else round(_ro, 4)), rho_ratio=None, E=round(E, 4), ramp=0.0, w=0.0)
    ramp = 1.0 if _ro >= _DELTA else _ro/_DELTA
    Rden = _UC_RHODEN.get(pos)
    rho_ratio = (_ro/Rden) if (Rden and Rden > 0.0) else None
    w = (_S*E*ramp) if _S is not None else 0.0
    return dict(rho_num=round(_ro, 4), rho_ratio=(round(rho_ratio, 4) if rho_ratio is not None else None),
                E=round(E, 4), ramp=round(ramp, 4), w=round(w, 4))

priced = [p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows = {}
for p in priced:
    k = p.get('key')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            v = ev(p, Y); gf = MA.gfut(p); Lc = _lvlcurr(p, Y); par = _par_prior(p, Y)
            Eq = _ev_qual(p, Y); rawe = raw_ev(p, Y); wf = _wfields(p, gf)
        gw = sum((x.get('games', 0) or 0) for x in (p.get('scoring') or []) if (x.get('games', 0) or 0) > 0)
        rows[k] = dict(key=k, sid=p.get('stable_player_id'), player=p['player'], pos=gf,
                       ev=float(v), num=int(round(v/F)), age=cp._age_asof(p, Y), effpk=int(MA.effpk(p)),
                       Eq=round(float(Eq), 3), rawev=repr(float(rawe)),
                       pormargin=round(float(Lc-par), 2), games_window=int(gw),
                       real=bool(_isreal(p)), **wf)
    except Exception as e:
        rows[k] = dict(key=k, player=p.get('player'), error=repr(e))
json.dump(rows, open(out, 'w'))
_on = 'OFF' if _S is None else ('s=%.4f' % _S)
print("LEDGER DUMP %s: %d players  map=%s  RHO_DEN=%s" % (os.path.basename(out), len(rows), _on,
      {kk: round(vv, 2) for kk, vv in _UC_RHODEN.items()}))
