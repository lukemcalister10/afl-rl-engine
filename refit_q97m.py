#!/usr/bin/env python3
"""REFIT ENTRY POINT for the FROZEN q97 CEILING model (q97m) — owner ruling, 2026-07-14.

WHY THIS EXISTS
  q97m is the q97 ceiling (band[5], price6 weight 0.10). It used to be fitted at IMPORT TIME on every board /
  gate / panel run (_merged_recover.py:31) and was pinned by NOTHING. numpy's OpenBLAS is DYNAMIC_ARCH (it
  selects a CPU-specific float kernel at runtime); GitHub runs a mixed-CPU fleet, so the SAME commit trained
  q97m slightly differently per runner — every player moved a little, both directions — the cross-environment
  CI red. The owner froze it: fitted ONCE, pickled to data/q97m.pkl, stamped in data/expected_boot.json, and
  LOADED (never fitted) by the engine.

  Freezing WITHOUT a documented refit path just builds a second cm_400.pkl — a model nobody can legitimately
  update. THIS is that path, and the ONLY one. It is GATED so an ordinary build/gate/panel run cannot trigger a
  refit (silent refit is the defect being fixed). It re-pins the stamp it invalidates and HALTs everything
  downstream until re-certified. It records provenance (what, when, on what inputs, old md5 -> new md5).

USAGE
  Verify (safe, no gate, writes nothing) — refit into memory on THIS box and compare to the committed pin:
      python3 refit_q97m.py --verify
  Refit (BAKE ONLY — must set RL_BAKE_REFIT=1; writes data/q97m.pkl + re-pins expected_boot.json + provenance):
      RL_BAKE_REFIT=1 python3 refit_q97m.py --bake
  Both modes fit from the ENGINE'S OWN X/yy (execing _merged_recover.py from the pinned workspace), so the refit
  uses the identical inputs the frozen model was fit from — no second copy of the training-pool logic.

AFTER A REFIT (the half that is usually forgotten — this script HALTs you here on purpose):
  the new q97m almost certainly moves the board. You MUST, in the SAME commit:
    1. rebuild the board            (rl_export.py) and RE-PIN data/expected_boot.json 'board'
    2. rebuild the book / matrix    (s4_matrix_M1v7.py) and re-seal if n changed
    3. re-run every gate            (.github/workflows/ci-guards.yml + ship_gates_check.py) to GREEN
    4. commit the provenance        (data/q97m_refit_log.json) alongside the moved pins
  Until board/book/gates are re-pinned + re-certified, Guard 5 (boot_guard) stays RED by construction — the
  q97m pin moved but the board pin did not. That RED is the feature: nothing ships on an un-recertified refit.
"""
import os, sys, io, json, time, pickle, hashlib, contextlib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# The exact q97m hyperparameters that _merged_recover.py:31 used before the freeze. Kept HERE, in the one refit
# entry point, so the frozen artifact and its regeneration are a single source (change them here, refit, re-pin).
Q97M_KW = dict(loss='quantile', alpha=0.97, n_estimators=200, max_depth=4,
               learning_rate=0.05, min_samples_leaf=25, random_state=0)

def _repo_root():
    for c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
              os.path.dirname(os.path.abspath(__file__))):
        if c and os.path.exists(os.path.join(c, 'data', 'expected_boot.json')):
            return os.path.abspath(c)
    return os.path.dirname(os.path.abspath(__file__))

def _md5_bytes(b): return hashlib.md5(b).hexdigest()
def _md5_file(p):
    with open(p, 'rb') as f: return _md5_bytes(f.read())

def _engine_Xy(with_meta=False):
    """Fit-inputs, straight from the engine: exec _merged_recover.py (which now LOADS q97m) and read its X/yy.
    Uses the pinned workspace copy the build uses, so the refit trains on the identical pool the freeze did.

    REBAKE ARM 2: the engine's X is built through cp._feat, so if the LOADED BAND declares the design
    contract (exact_monotone), X already carries the 12-feature age-hill layout and the returned spec says
    so. That is the point of binding the contract at the artifact rather than at a switch — the ceiling
    cannot be fitted on a different feature vector from the band it will be composed with, because it is
    literally reading the band's own bound feature builder. with_meta also returns the per-row as-of YEAR,
    which the window-anchored recency weight needs and which the engine's own loop discards."""
    ws = os.environ.get('RL_WS', '/home/claude/rl_workspace/rl_after')
    eng = os.path.join(ws, '_merged_recover.py')
    if not os.path.exists(eng):
        raise SystemExit("refit HALT: engine not found at %s — run bootstrap.sh first (the refit trains on the "
                         "engine's own X/yy)." % eng)
    cwd0 = os.getcwd(); sys.path.insert(0, ws)
    try:
        os.chdir(ws)
        g = {}
        # SPLIT AT THE q97m LOAD, NOT AT THE "=== AFTER" PRINT (rebake ARM 2 correction). X/yy are fully
        # built at _merged_recover.py:58-64, BEFORE q97m=_load_q97m(). Exec'ing past that point made THE
        # REFIT ENTRY POINT REQUIRE A LOADABLE q97m IN ORDER TO PRODUCE ONE — a latent circularity that
        # nobody hit while the artifact existed, and that would have blocked the one legitimate path to
        # regenerate it the moment it did not. Stopping at the load also means the ARM 2 artifact-contract
        # halts (which compare the band's spec to the CEILING'S) are not reached while the ceiling is
        # precisely what is being fitted. The L4 membership tripwire at :65-75 still runs: it is above the
        # split. Strictly less code executes than before, and X/yy are identical.
        src = open(eng).read()
        cut = src.index('q97m=_load_q97m()')
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src[:cut], g)
        X, yy = np.array(g['X']), np.array(g['yy'])
        if not with_meta:
            return X, yy
        cp = g['cp']
        # the as-of year per row, re-enumerated by the engine's OWN row rule (_merged_recover.py:60-64),
        # read out of the exec'd globals so it cannot drift from the loop that built X.
        yr = []
        for p in g['pool']:
            if cp.debutyr(p) > 2021 or not (p.get('pick') or p.get('_ft')) or (g['_L4_MSD'] and p.get('type') == 'MSD'):
                continue
            d0 = cp.debutyr(p) - 1
            last = max([x['year'] for x in p['scoring']] + [d0])
            yr.extend(range(d0, min(last, 2026) + 1))
        assert len(yr) == X.shape[0], 'q97m row re-enumeration %d != engine X %d' % (len(yr), X.shape[0])
        return X, yy, np.array(yr, int), cp.design()
    finally:
        os.chdir(cwd0)

def _fit(X, yy, spec=None, year=None):
    """The incumbent GradientBoostingRegressor, or — when a design contract is bound — the exact-monotone
    construction with the CEILING'S OWN out-of-sample-selected settings. The ceiling and the band select
    separately (they are different fits on different row populations: q97m excludes MSD and carries no T1)
    but they must share the FEATURE contract, which specs_agree asserts at load."""
    if spec is None:
        return GradientBoostingRegressor(**Q97M_KW).fit(X, yy)
    sys.path.insert(0, os.environ.get('RL_FV') or os.path.join(_repo_root(), 'engine', 'forward_valuation'))
    import exact_monotone as EM
    EM.selftest_or_halt()                       # FB4 — before any fit, here as at every other fit site
    w = EM.recency_weight(year, spec.get('recency_halflife_years'), 2026) if year is not None else None
    m = EM.make_estimator(0.97, X.shape[1], bool(spec.get('age_hill')), spec['hyperparameters'])
    return EM.stamp(m.fit(X, yy, sample_weight=w), spec)

def main(argv):
    root = _repo_root()
    pkl_path = os.path.join(root, 'data', 'q97m.pkl')
    boot_path = os.path.join(root, 'data', 'expected_boot.json')
    with open(boot_path) as f: boot = json.load(f)
    pinned = boot.get('q97m')
    old_file_md5 = _md5_file(pkl_path) if os.path.exists(pkl_path) else None

    mode = '--verify'
    for a in argv[1:]:
        if a in ('--verify', '--bake'): mode = a

    X, yy = _engine_Xy()
    model = _fit(X, yy)
    blob = pickle.dumps(model, protocol=pickle.DEFAULT_PROTOCOL)
    new_md5 = _md5_bytes(blob)
    print("refit_q97m: fit on X=%d rows, %d features | new md5 %s | committed pin %s"
          % (X.shape[0], X.shape[1], new_md5, pinned))

    if mode == '--verify':
        same = (new_md5 == pinned)
        print("VERIFY: refit %s the committed pin (%s)."
              % ("REPRODUCES" if same else "DIVERGES from", pinned))
        print("  (a divergence here is EXPECTED on a different CPU/BLAS kernel — that is exactly why q97m is "
              "frozen and loaded, not fitted. It does NOT mean the shipped board is wrong; it means a refit must "
              "happen at a controlled bake, then be re-pinned + re-certified.)")
        return 0 if same else 3

    # --bake
    if os.environ.get('RL_BAKE_REFIT') != '1':
        raise SystemExit("refit HALT: --bake requires RL_BAKE_REFIT=1. This gate exists so an ordinary "
                         "build/gate/panel run cannot trigger a refit (silent refit is the defect being fixed). "
                         "Set it ONLY inside a controlled bake.")
    with open(pkl_path, 'wb') as f: f.write(blob)
    boot['q97m'] = new_md5
    with open(boot_path, 'w') as f: json.dump(boot, f, indent=2, ensure_ascii=False); f.write('\n')
    # provenance (durable, committed beside the artifact): append one record per refit.
    prov_path = os.path.join(root, 'data', 'q97m_refit_log.json')
    log = []
    if os.path.exists(prov_path):
        try: log = json.load(open(prov_path))
        except Exception: log = []
    log.append({
        'ts_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'artifact': 'data/q97m.pkl',
        'hyperparameters': Q97M_KW,
        'inputs': {'engine': 'workspace _merged_recover.py X/yy', 'X_rows': int(X.shape[0]), 'X_features': int(X.shape[1])},
        'old_md5': old_file_md5, 'old_pin': pinned, 'new_md5': new_md5,
        'note': 'refit at a bake; board/book/gates re-pin + re-certify required in the SAME commit',
    })
    with open(prov_path, 'w') as f: json.dump(log, f, indent=2); f.write('\n')
    print("REFIT WRITTEN: data/q97m.pkl md5 %s -> %s ; re-pinned expected_boot.json 'q97m' ; provenance -> "
          "data/q97m_refit_log.json" % (old_file_md5, new_md5))
    print("\n================ DOWNSTREAM HALT — RE-CERTIFY BEFORE SHIPPING ================\n"
          "  q97m moved; the board/book pins are now STALE. In THIS commit you MUST:\n"
          "   1. rebuild the board (rl_export.py) + RE-PIN expected_boot.json 'board'\n"
          "   2. rebuild the book/matrix (s4_matrix_M1v7.py) + re-seal if n changed\n"
          "   3. re-run ci-guards.yml + ship_gates_check.py to GREEN\n"
          "   4. commit data/q97m_refit_log.json alongside the moved pins\n"
          "  Until then Guard 5 (boot_guard) stays RED by construction (q97m pin moved, board pin did not).\n"
          "=============================================================================")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
