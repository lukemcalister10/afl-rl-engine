"""WIRE-IN (cont.27 BOARD SWITCH): inject the VALIDATED PAR-CENTRED redesign into the engine board.

The board now runs the par-centred router TR.production_value, not rd.redesign_value with the default-feature cm.
TWO coupled changes vs the cont.25 wire (BOTH required):
  1. cm source: PR.retrain() (par-centred feature cp._lvl_eff=lvl_par), NOT rd.build() (default feature). The validated
     pre-debut numbers REQUIRE the par-centred cm; a naive redesign_value->production_value swap WITHOUT the cm switch
     silently breaks pre-debut. (Established is byte-exact at a given tree count: the router calls redesign_value verbatim.)
  2. value fn: TR.production_value (router). PRE-DEBUT -> par-path (rval / RUC scorer-borrow pool); ESTABLISHED ->
     rd.redesign_value (verbatim). Routes at the tail_restore level (option B; the dep graph forbids editing redesign_value).

Shipped fidelity = 400 trees (RL_PRIOR_TREES=400, PAR_RAMPS=22). Pre-debut blend = 2086/1473/1126/635/396 (the 200-tree
2176/1505/1131/647/392 is the SUPERSEDED mock). Year-shifts (_vP1/2,_vM1/2) stay FLAT=_v (stage-2 slider deferred).

_bands: the GBM band (cond_prior_band peak + at-draft pole) is captured as a NAMED intermediate (computed, NOT serialized)
so a future Option-1->2 hybrid is purely additive (serialize p['_bands'] in player_rec + add the ~40-line JS pricing layer).

  An orchestrator imports rl_model -> wire_redesign -> rl_export so the export reads the wired values.
"""
import io, contextlib, importlib.util, os, pickle
_FV = '/home/claude/rl_workspace/forward_valuation'
def _ld(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m); return m

# par_redesign (PR) is the par-centred chain; tail_restore (TR) holds the router. One consistent module set (PR's).
PR = _ld('PR', os.path.join(_FV, 'par_redesign.py'))
TR = _ld('TR', os.path.join(_FV, 'tail_restore.py'))
TR.bind(PR)
rd = PR.rd; cp = PR.cp; dp = PR.dp; MA = PR.MA

_CM = None
def build():
    """Train (or load cached) the PAR-CENTRED cm at the env's RL_PRIOR_TREES. The cache is a pure speed optimisation:
    PR.retrain() is deterministic (PYTHONHASHSEED=0 + random_state=0 + fixed trees), so cache==retrain byte-for-byte."""
    global _CM
    if _CM is None:
        trees = os.environ.get('RL_PRIOR_TREES', '400')
        cache = f'/home/claude/cm_{trees}.pkl'
        cp._lvl_eff = PR.lvl_par                       # par-centred feature for INFERENCE (PR.retrain sets this for training)
        if os.path.exists(cache):
            with open(cache, 'rb') as fh: _CM = pickle.load(fh)
        else:
            with contextlib.redirect_stdout(io.StringIO()): _CM = PR.retrain()
            try:
                with open(cache, 'wb') as fh: pickle.dump(_CM, fh)
            except Exception: pass
    return _CM

def _capture_bands(p, cm):
    """NAMED intermediate: the GBM Q-vectors a future hybrid ships as data + prices in JS. Computed-not-serialized.
    Redundant with the band computed inside production_value (kept separate so the validated pricing path stays untouched)."""
    try:
        b = {'peak': [round(float(x), 4) for x in cp.cond_prior_band(p, cm)]}
        if MA.level_now(p) is not None:
            b['adraft'] = [round(float(x), 4) for x in rd._adraft_band(p, cm)]
        return b
    except Exception:
        return None

def wire(players=None, lens='bal'):
    """Overwrite p['_v'] with the par-centred router value for every player. Returns the trained models."""
    cm = build(); MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    if players is None: players = MA.players
    for p in players:
        if '_vpt_engine' not in p: p['_vpt_engine'] = p.get('_vpt')
        v = TR.production_value(p, cm, lens=lens)
        p['_v'] = v
        p['_vP1'] = p['_vP2'] = p['_vM1'] = p['_vM2'] = v   # FLAT placeholder until stage-2 slider
        p['_cvx'] = 1.0                                      # redesign band already carries the upside; no separate cvx
        p['_bands'] = _capture_bands(p, cm)                 # FUTURE 1->2: serialize this in player_rec (purely additive)
    return cm

if __name__ == '__main__':
    import sys; _so = sys.stdout; sys.stdout = io.StringIO()
    try: import compute
    except Exception: pass
    sys.stdout = _so
    cm = wire()
    def f(nm):
        c = [p for p in MA.players if nm.lower() in p['player'].lower()]; return c[0] if c else None
    print('WIRED _v (par-centred router):')
    for nm in ['Nick Daicos', 'Marcus Bontempelli', 'Max Gawn', 'Jeremy Cameron', 'Harry Sheezel']:
        p = f(nm)
        if p: print('  %-22s _v=%-6d  _vpt_engine=%-6s  bands=%s' % (nm[:22], p['_v'], str(p.get('_vpt_engine')), p['_bands']['peak'] if p.get('_bands') else None))
    print('  board: %d active players wired' % len(MA.players))
