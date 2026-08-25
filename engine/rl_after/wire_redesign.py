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
# CANONICAL FORWARD-VALUATION SOURCE SELECTION (fail-closed): resolved by the ONE canonical selector
# fv_provenance.resolve_fv — the SAME function Guard 5 uses, so the production loader and the guard can never
# resolve differently (fv-provenance remediation 2026-07-20; corrective C2). No ambient-workspace default: a
# canonical build never silently imports /home/claude/rl_workspace/forward_valuation (the 06d8af60 -> d7a95e8d
# hole). If fv_provenance is not importable, fail closed rather than guess a source.
try:
    import fv_provenance as _FVP
except Exception as _e:
    raise SystemExit("wire_redesign: the canonical resolver fv_provenance is not importable (%r) — cannot "
                     "select the forward_valuation source (fail-closed; fv-provenance remediation)." % _e)
_FV = _FVP.resolve_fv()
def _ld(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m); return m

# par_redesign (PR) is the par-centred chain; tail_restore (TR) is the bound namespace spine (rd/cp/dp).
PR = _ld('PR', os.path.join(_FV, 'par_redesign.py'))
TR = _ld('TR', os.path.join(_FV, 'tail_restore.py'))
TR.bind(PR)
rd = PR.rd; cp = PR.cp; dp = PR.dp; MA = PR.MA

_CM = None
def cm_load_path():
    """THE ONE cm LOAD-PATH RESOLVER. Guard 5 (boot_guard._resolve_cm_load) mirrors this precedence
    byte-for-byte — a guard that resolves differently from the engine certifies a path the engine does
    not take, which is the exact hole register item 91 opened on the just-frozen q97m.

      $RL_CM_PKL  ->  /home/claude/cm_<RL_PRIOR_TREES>.pkl

    RL_CM_PKL is a PATH var (config_manifest.INFRA_ALLOW), never a model input: UNSET reproduces the
    shipped resolution exactly, and the shipped board is byte-identical across its introduction. It
    exists because the band is the one fitted artifact loaded from an absolute out-of-repo path with
    no override — its two frozen siblings already have theirs (RL_Q97M_PKL, RL_V0SURF_PKL) — so a
    candidate board could not read a candidate band without either overwriting the pinned cache in
    place (destroying the thing Guard 5 asserts) or inventing an undeclared name."""
    p = os.environ.get('RL_CM_PKL')
    if p:
        return p
    return '/home/claude/cm_%s.pkl' % os.environ.get('RL_PRIOR_TREES', '400')

def build():
    """LOAD the PAR-CENTRED cm from the pinned cache resolved by cm_load_path(). The cache is the
    AUTHORITATIVE, Guard-5-asserted forest — NOT byte-reproducible by a fresh fit (see CACHE HONESTY in
    the module docstring): PR.retrain() runs through DYNAMIC_ARCH OpenBLAS and is not bit-stable.

    THE SILENT-REFIT FALLBACK IS DELETED (rebake week ARM 1, 2026-08-24; ruled at register v831/v833,
    named by BOTH blind design studies as the one-line fix riding the rebake). WAS: on a cache miss this
    function called PR.retrain() and pickled the result over the cache path — a fit at build time,
    unpinned, not bit-stable, silently producing a NON-canonical forest that Guard 5's load-path block
    would then assert against the pin of a file this branch had just written. That is precisely the
    defect the q97m freeze (2026-07-14) and the v0surf freeze (2026-07-18) removed from the two sibling
    artifacts; the band kept it for another five weeks. It now HALTS, exactly as _load_q97m does.

    A cold bake regenerates the band through the committed refit entry point, never through a load."""
    global _CM
    if _CM is None:
        cache = cm_load_path()
        cp._lvl_eff = PR.lvl_par                       # par-centred feature for INFERENCE (PR.retrain sets this for training)
        if not os.path.exists(cache):
            raise SystemExit(
                "cm FROZEN-LOAD HALT: no band pickle at %s (precedence: $RL_CM_PKL -> "
                "/home/claude/cm_<RL_PRIOR_TREES>.pkl). The engine NEVER fits the band at build time — a "
                "silent refit produces a non-canonical, non-bit-stable forest and then pins it to itself. "
                "Re-run bootstrap.sh to seed the pinned cache, or regenerate the band through the committed "
                "refit entry point at a bake." % cache)
        with open(cache, 'rb') as fh: _CM = pickle.load(fh)
        # ---- REBAKE ARM 2 — BIND THE DESIGN CONTRACT THE ARTIFACT ITSELF DECLARES ------------------
        # THE ONE SITE. The band pickle is the thing that knows which construction it is: the exact
        # monotone arm (register v831 D1, "Exact it is.") moves the feature dimension 11 -> 12 and the
        # estimator class, and both ride inside the pickle as _rl_design_spec. Reading it HERE — the one
        # place that loads the band and already rebinds cp._lvl_eff — means no environment variable can
        # ever disagree with the bytes on disk, and no second site can bind a different contract.
        # An INCUMBENT band declares nothing, binds nothing, and every expression downstream is
        # byte-identical to the shipped path. This is deliberately NOT a switch; see
        # docs/evidence/rebake_arm2_design_2026-08-24/PREREG.md section 2.
        import sys as _sys
        if _FV not in _sys.path: _sys.path.insert(0, _FV)
        import exact_monotone as _EM
        cp.bind_design(_EM.spec_of(_CM))
    return _CM
