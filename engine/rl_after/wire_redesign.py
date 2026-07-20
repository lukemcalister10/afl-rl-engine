"""ENGINE cm PROVIDER (post ONE-price, D4 2026-07-02).

HISTORY: this module was the cont.27 BOARD SWITCH — its wire() overwrote every p['_v'] with the
TR.production_value router before export. Luke's ONE-price ruling (02/07/2026, in writing) DELETED the
board valuation path: the board now renders engine ev() directly (rl_export.py). Per deleted layer see
BOARD_LAYERS_OBITUARY.md (magnitudes, rationale, deletion commit, resurrection refs).

WHAT REMAINS (engine dependency, unchanged semantics): build() — LOAD the PAR-CENTRED cm from the pinned,
Guard-5-asserted cache (data/cm_400.pkl -> /home/claude/cm_<trees>.pkl). _merged_recover.py imports this
module for W.build() and reaches rd/cp/dp through W.TR (the tail_restore namespace spine).

CACHE HONESTY (measured, 2026-07-14 — corrects a false prior claim): the cached forest is AUTHORITATIVE and is
NOT byte-reproducible by a fresh fit. A prior version of this docstring asserted "cache==retrain byte-for-byte";
that is UNTRUE and was measured untrue (a fresh PR.retrain() yields b271ed2e; the committed cm_400.pkl is
34faa865). PR.retrain() is a RandomForest fit that runs through numpy's OpenBLAS, which is built DYNAMIC_ARCH
(runtime CPU-kernel selection) — so a refit is not bit-stable even on one box, let alone across a mixed-CPU
fleet. The cache is therefore the SINGLE SOURCE OF TRUTH, regenerated ONLY at a bake and pinned — it is not a
speed optimisation over an equivalent recompute. (This is the same freeze q97m now gets, for the same reason.)
"""
import io, contextlib, importlib.util, os, pickle
def _resolve_fv():
    """CANONICAL FORWARD-VALUATION SOURCE SELECTION (fail-closed, fv-provenance remediation 2026-07-20).
    An explicit RL_FV wins (Guard 5's loaded-path assertion verifies its identity == pin, so an explicit-but-
    stale RL_FV HALTS, it is not trusted blindly); otherwise the CHECKED-OUT engine/forward_valuation
    (RL_REPO / CLAUDE_PROJECT_DIR). There is NO ambient-workspace default: a canonical build never silently
    imports /home/claude/rl_workspace/forward_valuation, the persistent copy a previous branch may have seeded
    (the exact hole that produced the 06d8af60 -> d7a95e8d 109-wobble; ROOT_CAUSE.md)."""
    fv = os.environ.get('RL_FV')
    if fv:
        return os.path.abspath(fv)
    for base in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR')):
        if base:
            cand = os.path.join(base, 'engine', 'forward_valuation')
            if os.path.isdir(cand):
                return os.path.abspath(cand)
    raise SystemExit(
        "wire_redesign: cannot resolve forward_valuation source — RL_FV is unset and no checked-out "
        "engine/forward_valuation was found via RL_REPO / CLAUDE_PROJECT_DIR. Refusing to fall back to an "
        "ambient /home/claude/rl_workspace/forward_valuation copy (fail-closed provenance; fv-provenance "
        "remediation). Set RL_FV to the checked-out engine/forward_valuation, or RL_REPO to the checkout root.")
_FV = _resolve_fv()
def _ld(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m); return m

# par_redesign (PR) is the par-centred chain; tail_restore (TR) is the bound namespace spine (rd/cp/dp).
PR = _ld('PR', os.path.join(_FV, 'par_redesign.py'))
TR = _ld('TR', os.path.join(_FV, 'tail_restore.py'))
TR.bind(PR)
rd = PR.rd; cp = PR.cp; dp = PR.dp; MA = PR.MA

_CM = None
def build():
    """LOAD the PAR-CENTRED cm at the env's RL_PRIOR_TREES from the pinned cache. The cache is the AUTHORITATIVE,
    Guard-5-asserted forest — NOT byte-reproducible by a fresh fit (see CACHE HONESTY in the module docstring):
    PR.retrain() runs through DYNAMIC_ARCH OpenBLAS and is not bit-stable. The retrain fallback below exists only
    for a genuine cold bake (no cache present at all); a normal build ALWAYS hits the pinned cache and never fits."""
    global _CM
    if _CM is None:
        trees = os.environ.get('RL_PRIOR_TREES', '400')
        cache = f'/home/claude/cm_{trees}.pkl'
        cp._lvl_eff = PR.lvl_par                       # par-centred feature for INFERENCE (PR.retrain sets this for training)
        if os.path.exists(cache):
            with open(cache, 'rb') as fh: _CM = pickle.load(fh)
        else:
            # COLD-BAKE ONLY: no pinned cache present. This produces a NON-canonical forest (not bit-equal to the
            # shipped cm_400.pkl); it must be re-pinned + re-certified at a bake before it can ship. bootstrap.sh
            # seeds the pinned cache, so a normal build/gate/panel never reaches this branch.
            with contextlib.redirect_stdout(io.StringIO()): _CM = PR.retrain()
            try:
                with open(cache, 'wb') as fh: pickle.dump(_CM, fh)
            except Exception: pass
    return _CM
