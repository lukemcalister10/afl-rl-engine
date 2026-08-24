#!/usr/bin/env python3
"""REBAKE WEEK · ARM 2 · THE DESIGN REFIT — the ONE committed, versioned entry point.

WHAT THIS IS
  Ruled at register v831 (all six decisions, owner words verbatim), v833 (the binding handover), v834
  (ARM 1 landed and verified). Directive docs/directives/REBAKE_ARM2_DESIGN_2026-08-24.md; prereg
  docs/evidence/rebake_arm2_design_2026-08-24/PREREG.md, committed at e4a078f BEFORE this file existed (P9).

  It refits the scoped fitted artifacts with the RULED DESIGN construction — the exact-monotone estimator,
  the age hill at the out-of-sample-selected a*, the window-anchored recency weight — on the CURRENT store,
  and writes them to CANDIDATE paths with an in-repo provenance stamp beside each one. It never touches a
  live pickle, a live pin, data/expected_boot.json, /home/claude/cm_400.pkl or /home/claude/q97m.pkl.

  It is ARM 1's orchestrator with ONE structural difference and it is worth naming: ARM 1 refit the
  INCUMBENT constructions and therefore read every setting out of the source. This arm's settings are not
  in the source and must not be — they are SELECTED OUT OF SAMPLE by tools/rebake/select_arm2.py on grids
  the prereg declared, and this entry point READS THAT SELECTION FILE. Typing a selected number in here
  would be exactly the thing v831 D2/D3 forbid.

WHERE EACH CONSTRUCTION IS READ FROM (never re-implemented here)
  cm_400          conditional_prior.build_cond_prior(cap=2026, resolved_cut=2021) under a BOUND design
                  contract — the same function the incumbent path calls, taking the design branch. The
                  feature bind is par_redesign.retrain()'s own (cp._lvl_eff = lvl_par), asserted from
                  retrain's source rather than assumed, exactly as ARM 1 asserted it.
  q97m            refit_q97m._engine_Xy() + refit_q97m._fit() — the committed refit entry point's own
                  fit-inputs and its own fit, imported, not copied. Its X comes from the ENGINE, built
                  through the design-bound cp._feat, so the ceiling cannot be fitted on a different
                  feature vector from the band it will be composed with.
  peak_model_v4   engine/forward_valuation/build_peak_model_v4.py, run as its own process with
                  RL_ARM2_OUT set. pvc_snapshot.json CO-EMITS from that run by design (v831 D6).
  bust_prior_table  NOT REFITTED, and NOT A BLOCKER THIS TIME. The directive rules it explicitly: the peak
                  model trains on the FROZEN table for now, because the rederivation ruling is with the
                  owner and ARM 1 already established (falsifier FA2, fired as predicted) that NO PRODUCER
                  FOR IT EXISTS ANYWHERE IN THE REPOSITORY. The frozen table's md5 is recorded in the peak
                  model's stamp as a training INPUT, so the one cheap refit pass the directive anticipates
                  can be scoped exactly when the owner rules.

THE ORDER IS LOAD-BEARING, NOT ALPHABETICAL
  cm_400 must be fitted and written FIRST, because q97m's fit-inputs come from the engine, and the engine
  builds them through the feature contract the BAND declares. Fitting the ceiling first would fit it on
  the incumbent's 11 columns and then compose it with a 12-column band — which is the mixed-artifact class
  register v834's F7 exposed, and which the engine's coherence HALT now refuses at load.

USAGE (single-thread BLAS, pinned venv, RL_REPO/RL_FV bound to a root, RL_WS to the seat's own workspace —
never the shared /home/claude/rl_workspace):
    python3 tools/rebake/refit_arm2_design.py --out <dir> --selection <select_arm2.json> --artifact all
    python3 tools/rebake/refit_arm2_design.py --out <dir> --selection <json> --artifact cm_400 --t1 off --tag noT1
"""
import argparse, contextlib, hashlib, importlib.util, io, json, os, pickle, platform, subprocess, sys, time

import numpy as np

VERSION = 'arm2-design/1'


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    with open(p, 'rb') as f:
        return md5_bytes(f.read())


def repo_root():
    for c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
              os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))):
        if c and os.path.exists(os.path.join(c, 'data', 'expected_boot.json')):
            return os.path.abspath(c)
    raise SystemExit('refit_arm2 HALT: no checkout root (set RL_REPO).')


def workspace():
    ws = os.environ.get('RL_WS')
    if not ws:
        raise SystemExit("refit_arm2 HALT: set RL_WS to the SEAT'S OWN engine workspace (a copy of the "
                         'checkout). This entry point deliberately has no default: the shared '
                         '/home/claude/rl_workspace must never be a build seat\'s implicit target (P3).')
    if not os.path.exists(os.path.join(ws, '_merged_recover.py')):
        raise SystemExit('refit_arm2 HALT: RL_WS=%s carries no _merged_recover.py.' % ws)
    return os.path.abspath(ws)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def env_stamp(root, sel_path, sel):
    import scipy, sklearn
    boot = json.load(open(os.path.join(root, 'data', 'expected_boot.json')))
    return {
        'entry_point': 'tools/rebake/refit_arm2_design.py',
        'entry_point_version': VERSION,
        'entry_point_md5': md5_file(os.path.abspath(__file__)),
        'ts_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'python': platform.python_version(), 'numpy': np.__version__,
        'scipy': scipy.__version__, 'sklearn': sklearn.__version__,
        'training_store_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')),
        'training_store_pin_at_build': boot.get('store'),
        'selection_file': os.path.relpath(sel_path, root),
        'selection_file_md5': md5_file(sel_path),
        'selection_rule': sel['selection_rule'],
        'declared_grids': sel['declared_grids'],
        'blas_threads_env': {k: os.environ.get(k) for k in
                             ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                              'NUMEXPR_NUM_THREADS')},
    }


def write_stamp(out, name, doc):
    p = os.path.join(out, 'training_stamp_%s.json' % name)
    with open(p, 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print('  stamp -> %s' % p)
    return p


# --------------------------------------------------------------------------- cm_400
def refit_cm400(ctx, tag, t1):
    root, ws, out, EM, sel = ctx['root'], ctx['ws'], ctx['out'], ctx['EM'], ctx['sel']
    fv = ctx['fv']
    sys.path[:0] = [ws, fv]
    os.chdir(ws)
    PR = load_module('PR_arm2', os.path.join(fv, 'par_redesign.py'))
    rd, cp = PR.rd, PR.cp

    # P4 — assert the relationship, never a hand-typed constant (ARM 1's assertion, carried unchanged).
    import inspect
    d = inspect.signature(rd.build).parameters
    cap, cut = d['cap'].default, d['resolved_cut'].default
    assert (cap, cut) == (2026, 2021), 'dist_redesign.build defaults moved: %r' % ((cap, cut),)
    src = inspect.getsource(PR.retrain)
    assert 'cp._lvl_eff=lvl_par' in src.replace(' ', '') and 'rd.build()' in src.replace(' ', ''), \
        'par_redesign.retrain() is no longer `cp._lvl_eff=lvl_par; return rd.build()`: %r' % src

    S = sel['SELECTION']
    spec = EM.design_spec(a_star=S['a_star'], hp=S['hyperparameters'],
                          halflife=S['recency_halflife_years'], n_features=S['n_features'],
                          quantiles=cp.Q,
                          note='cm_400 — the five-quantile PAR-centred band. Settings SELECTED OUT OF '
                               'SAMPLE on the grids declared in the prereg; never carried as literals.')
    fo_before = cp.first_observable_season()
    t1_disabled = (t1 == 'off')
    if t1_disabled:
        cp.first_observable_season = lambda: None
        print('  T1 DISABLED for attribution (first_observable_season -> None; store value was %r)' % fo_before)

    cp._lvl_eff = PR.lvl_par                    # the PAR-CENTRED level feature, exactly as retrain() binds it
    cp.bind_design(spec)                        # the design contract, for BOTH _feat and build_cond_prior
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        models, nrows = cp.build_cond_prior(cap=cap, resolved_cut=cut)
    secs = time.time() - t0
    blob = pickle.dumps(models, protocol=pickle.DEFAULT_PROTOCOL)
    art = os.path.join(out, 'cm_400.%s.pkl' % tag)
    with open(art, 'wb') as f:
        f.write(blob)

    m0 = models[sorted(models)[0]]
    old = os.path.join(root, 'data', 'cm_400.pkl')
    doc = dict(env_stamp(root, ctx['sel_path'], sel))
    doc.update({
        'artifact': 'cm_400 (the five-quantile PAR-centred band forests) — REBAKE ARM 2, exact-monotone',
        'candidate_path': os.path.relpath(art, root),
        'candidate_md5': md5_file(art),                       # MEASURED from the artifact (P4)
        'shipped_path': 'data/cm_400.pkl',
        'shipped_md5': md5_file(old),
        'construction': 'exact_monotone.GradOnlyPinball on HistGradientBoostingRegressor, monotonic_cst '
                        'level=+1 / u=-1 / v=-1, via conditional_prior.build_cond_prior(cap=%d, '
                        'resolved_cut=%d) under a bound design contract' % (cap, cut),
        'design_spec': spec,
        'estimator': type(m0).__name__,
        'quantiles': sorted(models),
        'hyperparameters': {str(q): {k: (v if isinstance(v, (int, float, str, type(None))) else str(v))
                                     for k, v in models[q].get_params().items()} for q in sorted(models)},
        'training_rows': int(nrows),
        'n_features_in': int(m0.n_features_in_),
        'feature_layout': 'oh[0..5] + [log(effpk), exposure, tenure, LEVEL(9), u(10), v(11)] — raw age '
                          'REMOVED, age hill APPENDED; the level index is UNMOVED at 9',
        'T1_fabricated_zero_rule': ('APPLIED (conditional_prior.py:154-155)' if not t1_disabled
                                    else 'DISABLED — attribution variant, NOT the candidate'),
        'first_observable_season': fo_before,
        'fit_seconds': round(secs, 1),
        'walk_forward_at_selection': sel['final_walk_forward'],
        'incumbent_same_splits': sel['incumbent_same_splits'],
    })
    write_stamp(out, 'cm_400_%s' % tag, doc)
    print('  cm_400 candidate %s  rows=%d  feat=%d  md5=%s  (%.1fs)'
          % (art, nrows, m0.n_features_in_, doc['candidate_md5'], secs))
    if t1_disabled:
        cp.first_observable_season = lambda: fo_before
    cp.bind_design(None)
    return doc


# --------------------------------------------------------------------------- q97m
def refit_q97m_candidate(ctx, tag):
    """The ceiling. Fitted through the committed refit entry point, on the engine's own X/yy, with the
    BAND's feature contract and the CEILING'S OWN out-of-sample-selected settings.

    The band candidate must already exist and RL_CM_PKL must point at it — asserted, not assumed, because
    the failure mode if it does not is silent (the engine falls through to the pinned live band, and the
    ceiling is fitted on 11 columns for a 12-column world). That is precisely the fall-through that made
    ARM 1's screen produce a mixed board."""
    root, ws, out, EM, sel = ctx['root'], ctx['ws'], ctx['out'], ctx['EM'], ctx['sel']
    band = os.environ.get('RL_CM_PKL')
    if not band or not os.path.exists(band):
        raise SystemExit('refit_arm2 HALT: q97m must be fitted AFTER cm_400, with RL_CM_PKL bound to the '
                         'CANDIDATE band — the ceiling takes its feature contract from the band the engine '
                         'loads. RL_CM_PKL=%r' % band)
    sys.path.insert(0, root)
    os.environ['RL_WS'] = ws
    RQ = load_module('refit_q97m_arm2', os.path.join(root, 'refit_q97m.py'))
    X, yy, YR, bound = RQ._engine_Xy(with_meta=True)
    if bound is None:
        raise SystemExit('refit_arm2 HALT: the engine bound NO design contract while building the '
                         "ceiling's fit-inputs — RL_CM_PKL=%s is an incumbent band. Refusing to fit a "
                         'design ceiling against an incumbent band.' % band)

    # THE CEILING SELECTS ITS OWN SETTINGS, on the same declared grid and the same declared rule. It is a
    # different fit on a different row population (MSD excluded, no T1), so inheriting the band's
    # capacity would be an assumption, not a measurement. The FEATURE contract is shared and is not
    # re-selected — that is what specs_agree asserts at load.
    Q97 = 0.97
    SPL = (2014, 2017, 2020)
    LRS = list(sel['declared_grids']['stage1_learning_rate'])
    ITS = list(sel['declared_grids']['stage1_max_iter'])
    FIX = sel['declared_grids']['stage1_fixed']

    def score(hp):
        per = {}
        for T in SPL:
            tr = YR <= T
            te = (YR > T) & (YR <= T + 3)
            w = EM.recency_weight(YR[tr], bound.get('recency_halflife_years'), T)
            yp = EM.make_estimator(Q97, X.shape[1], bool(bound.get('age_hill')), hp) \
                .fit(X[tr], yy[tr], sample_weight=w).predict(X[te])
            d = yy[te] - yp
            per[str(T)] = round(float(np.mean(np.maximum(Q97 * d, (Q97 - 1.0) * d))), 4)
        per['mean'] = round(float(np.mean([per[str(T)] for T in SPL])), 4)
        per.update({'_lr': hp['learning_rate'], '_it': hp['max_iter'], 'settings': dict(hp)})
        return per

    grid = {}
    for lr in LRS:
        for it in ITS:
            hp = dict(FIX, learning_rate=lr, max_iter=it)
            grid['lr%s_it%d' % (lr, it)] = score(hp)
            print('    q97m grid lr=%-4s it=%-5d  mean %.4f' % (lr, it, grid['lr%s_it%d' % (lr, it)]['mean']),
                  flush=True)
    bk = min(grid, key=lambda k: (grid[k]['mean'], grid[k]['_it'], grid[k]['_lr']))

    # THE DECLARED INTERIOR-OPTIMUM CHECK, and it FIRED here where it did not fire for the band. The
    # prereg's words: "if the selected point sits on any grid edge, the grid is extended one step in that
    # direction and the extension reported. A boundary selection is disclosed as such." Study B's M-58
    # made exactly this mistake's opposite — it noticed its own selection sat on its grid corner and went
    # looking past it. The ceiling's selection lands on BOTH edges of the declared grid, so both are
    # extended, and the extension keeps going while the edge keeps winning (bounded, and every point
    # reported). This is a REAL correction to a boundary selection, not a formality.
    ext = {}
    for _ in range(6):
        hp = dict(grid[bk]['settings'])
        add = []
        if hp['learning_rate'] >= max(LRS):
            add.append(dict(hp, learning_rate=round(max(LRS) * 2.0, 3)))
        if hp['max_iter'] >= max(ITS):
            add.append(dict(hp, max_iter=max(ITS) * 2))
        if hp['learning_rate'] <= min(LRS):
            add.append(dict(hp, learning_rate=round(min(LRS) / 2.0, 3)))
        if hp['max_iter'] <= min(ITS):
            add.append(dict(hp, max_iter=max(50, min(ITS) // 2)))
        add = [h for h in add if 'lr%s_it%d' % (h['learning_rate'], h['max_iter']) not in grid
               and 'lr%s_it%d' % (h['learning_rate'], h['max_iter']) not in ext]
        if not add:
            break
        for h in add:
            k = 'lr%s_it%d' % (h['learning_rate'], h['max_iter'])
            ext[k] = score(h)
            print('    q97m EXTENSION %-16s mean %.4f' % (k, ext[k]['mean']), flush=True)
        merged = dict(grid); merged.update(ext)
        nb = min(merged, key=lambda k: (merged[k]['mean'], merged[k]['_it'], merged[k]['_lr']))
        LRS = sorted(set(LRS) | {merged[k]['_lr'] for k in ext})
        ITS = sorted(set(ITS) | {merged[k]['_it'] for k in ext})
        grid = merged
        if nb == bk:
            break
        bk = nb
    hp = dict(grid[bk]['settings'])
    on_edge = (hp['learning_rate'] in (min(LRS), max(LRS))) or (hp['max_iter'] in (min(ITS), max(ITS)))
    print('  q97m SELECTED %s -> %s  mean %.4f  (interior optimum: %s)'
          % (bk, hp, grid[bk]['mean'], 'NO — BOUNDARY, DISCLOSED' if on_edge else 'yes'))

    spec = dict(bound)
    spec['hyperparameters'] = {k: hp[k] for k in sorted(hp)}
    spec['quantiles'] = [Q97]
    spec['note'] = ('q97m — the frozen q97 CEILING (band[5], price6 weight 0.10). Feature contract SHARED '
                    'with the band (asserted at load); capacity selected on its OWN row population.')
    t0 = time.time()
    model = RQ._fit(X, yy, spec=spec, year=YR)
    secs = time.time() - t0
    blob = pickle.dumps(model, protocol=pickle.DEFAULT_PROTOCOL)
    art = os.path.join(out, 'q97m.%s.pkl' % tag)
    with open(art, 'wb') as f:
        f.write(blob)
    old = os.path.join(root, 'data', 'q97m.pkl')
    doc = dict(env_stamp(root, ctx['sel_path'], sel))
    doc.update({
        'artifact': 'q97m (the frozen q97 CEILING model) — REBAKE ARM 2, exact-monotone',
        'candidate_path': os.path.relpath(art, root),
        'candidate_md5': md5_file(art),
        'shipped_path': 'data/q97m.pkl',
        'shipped_md5': md5_file(old),
        'construction': 'exact_monotone.GradOnlyPinball on HistGradientBoostingRegressor at alpha=0.97, '
                        'fitted on _merged_recover.py X/yy via refit_q97m._engine_Xy/_fit',
        'design_spec': spec,
        'estimator': type(model).__name__,
        'hyperparameters': {k: (v if isinstance(v, (int, float, str, type(None))) else str(v))
                            for k, v in model.get_params().items()},
        'own_selection_grid': grid,
        'own_selected_key': bk,
        'own_selection_interior_optimum': not on_edge,
        'band_pickle_bound_at_fit': band,
        'band_pickle_md5_at_fit': md5_file(band),
        'training_rows': int(X.shape[0]),
        'n_features_in': int(X.shape[1]),
        'training_row_rule': '_merged_recover.py:60-64 — debut<=2021, (pick or _ft), MSD EXCLUDED '
                             '(RL_MSD_POOL_EXCL=%s)' % os.environ.get('RL_MSD_POOL_EXCL'),
        'T1_fabricated_zero_rule': 'NOT PART OF THIS CONSTRUCTION — the X/yy loop carries no '
                                   'first_observable_season skip. ARM 1 filed this and it is UNCHANGED '
                                   'here: moving T1 into the ceiling would be a training-row-rule change '
                                   'the design arm has not been ruled to make (v831 scopes the '
                                   'CONSTRUCTION, not the row rule). Still owed an owner word.',
        'fit_seconds': round(secs, 1),
    })
    write_stamp(out, 'q97m_%s' % tag, doc)
    print('  q97m candidate %s  rows=%d  feat=%d  md5=%s  (%.1fs)'
          % (art, X.shape[0], X.shape[1], doc['candidate_md5'], secs))
    return doc


# --------------------------------------------------------- peak_model_v4 (+ pvc_snapshot co-emit)
def refit_peak_model(ctx, tag):
    """UNCHANGED CONSTRUCTION, DELIBERATELY. v831 D6 scopes the peak model into the rebake, and the
    directive rules it trains on the FROZEN bust_prior table for now. Its 17-feature row rule is a
    different object from the band's and carries no age hill and no level constraint — there is no ruling
    to change it, so it is refit on the current store exactly as ARM 1 refit it. What moves is the store
    underneath it (and, through pvc_snapshot, the curve it freezes at train time)."""
    root, ws, out = ctx['root'], ctx['ws'], ctx['out']
    fv = ctx['fv']
    script = os.path.join(fv, 'build_peak_model_v4.py')
    env = dict(os.environ)
    env['RL_ARM2_OUT'] = out
    env['PYTHONPATH'] = os.pathsep.join([ws, fv, env.get('PYTHONPATH', '')])
    env.pop('RL_CONFIG_MODE', None)   # the builder is not a gate; it must not re-enter enforce()
    t0 = time.time()
    r = subprocess.run([sys.executable, script], cwd=ws, env=env, capture_output=True, text=True)
    secs = time.time() - t0
    log = os.path.join(out, 'build_peak_model_v4.%s.log' % tag)
    with open(log, 'w') as f:
        f.write(r.stdout + '\n----- stderr -----\n' + r.stderr)
    if r.returncode != 0:
        raise SystemExit('refit_arm2 HALT: build_peak_model_v4.py exited %d — see %s\n%s'
                         % (r.returncode, log, r.stderr[-2000:]))
    pkl = os.path.join(out, 'peak_model_v4.pkl')
    snap = os.path.join(out, 'pvc_snapshot.json')
    for p in (pkl, snap):
        if not os.path.exists(p):
            raise SystemExit('refit_arm2 HALT: build_peak_model_v4.py did not emit %s' % p)
    art_pkl = os.path.join(out, 'peak_model_v4.%s.pkl' % tag)
    art_snap = os.path.join(out, 'pvc_snapshot.%s.json' % tag)
    os.replace(pkl, art_pkl)
    os.replace(snap, art_snap)
    m = pickle.load(open(art_pkl, 'rb'))['model']
    doc = dict(env_stamp(root, ctx['sel_path'], ctx['sel']))
    doc.update({
        'artifact': 'peak_model_v4 (+ pvc_snapshot, CO-EMITTED by the same run, by design)',
        'candidate_path': os.path.relpath(art_pkl, root),
        'candidate_md5': md5_file(art_pkl),
        'shipped_path': 'engine/rl_after/peak_model_v4.pkl',
        'shipped_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'peak_model_v4.pkl')),
        'co_emit_candidate_path': os.path.relpath(art_snap, root),
        'co_emit_candidate_md5': md5_file(art_snap),
        'co_emit_shipped_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'pvc_snapshot.json')),
        'construction': 'engine/forward_valuation/build_peak_model_v4.py build(2006,2015) — UNCHANGED',
        'design_spec': None,
        'design_note': 'NOT an exact-monotone artifact. Different row rule, different 17 features, no '
                       'level constraint and no age hill — v831 scopes it into the rebake for its STORE, '
                       'not for a construction change, and none is ruled.',
        'estimator': type(m).__name__,
        'hyperparameters': {k: (v if isinstance(v, (int, float, str, type(None))) else str(v))
                            for k, v in m.get_params().items()},
        'n_features_in': int(m.n_features_in_),
        'n_iter_': int(m.n_iter_),
        'bust_prior_table_input_md5': md5_file(os.path.join(root, 'engine', 'rl_after',
                                                            'bust_prior_table.json')),
        'bust_prior_status': 'FROZEN TABLE, per the directive. No producer exists in the repository (ARM '
                             "1's falsifier FA2, fired as predicted). ONE cheap refit pass is owed when "
                             'the table and the final store are settled.',
        'fit_seconds': round(secs, 1),
        'builder_log': os.path.relpath(log, root),
    })
    write_stamp(out, 'peak_model_v4_%s' % tag, doc)
    print('  peak_model_v4 %s md5=%s ; pvc_snapshot %s md5=%s  (%.0fs)'
          % (art_pkl, doc['candidate_md5'], art_snap, doc['co_emit_candidate_md5'], secs))
    return doc


ARTIFACTS = {'cm_400': refit_cm400, 'q97m': refit_q97m_candidate, 'peak_model_v4': refit_peak_model}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='candidate output directory (never a live artifact path)')
    ap.add_argument('--selection', required=True, help='tools/rebake/select_arm2.py output json')
    ap.add_argument('--artifact', default='all', choices=sorted(ARTIFACTS) + ['all'])
    ap.add_argument('--t1', default='on', choices=['on', 'off'],
                    help="cm_400 only; 'off' is the ATTRIBUTION variant and is never the candidate")
    ap.add_argument('--tag', default='candidate')
    a = ap.parse_args(argv[1:])

    root = repo_root()
    ws = workspace()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)

    forbidden = {os.path.abspath(os.path.join(root, 'data')),
                 os.path.abspath(os.path.join(root, 'data', 'rl_build')),
                 os.path.abspath(os.path.join(root, 'engine', 'rl_after')),
                 os.path.abspath('/home/claude')}
    if out in forbidden:
        raise SystemExit('refit_arm2 HALT: --out %s is a LIVE artifact directory.' % out)

    sys.path.insert(0, root)
    import config_manifest
    chash = config_manifest.enforce('gate')
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path.insert(0, fv)
    import exact_monotone as EM

    # FB4 FIRST, BEFORE ANYTHING ELSE IS TOUCHED. The directive's words: "the bake asserts the subclass
    # contract against the pinned sklearn BEFORE ANY FIT, and HALTs if the internals moved."
    st = EM.selftest_or_halt()
    print('FB4 private-contract self-test: %s  (non-vacuity: stock violates %d steps; exact %d)'
          % (st['verdict'], st['STOCK_negative_steps'], st['EXACT_negative_steps']))

    sel_path = os.path.abspath(a.selection)
    sel = json.load(open(sel_path))
    S = sel['SELECTION']
    print('refit_arm2 %s  root=%s  ws=%s  out=%s  config=%s' % (VERSION, root, ws, out, str(chash)[:12]))
    print('  SELECTED (out of sample, declared grids): hp=%s  a*=%s  half-life=%r  features=%d'
          % (S['hyperparameters'], S['a_star'], S['recency_halflife_years'], S['n_features']))

    ctx = {'root': root, 'ws': ws, 'out': out, 'fv': fv, 'EM': EM, 'sel': sel, 'sel_path': sel_path,
           'selftest': st}
    names = ['cm_400', 'q97m', 'peak_model_v4'] if a.artifact == 'all' else [a.artifact]
    docs = {'_fb4_selftest': st}
    for n in names:
        print('--- %s ---' % n)
        docs[n] = (ARTIFACTS[n](ctx, a.tag, a.t1) if n == 'cm_400' else ARTIFACTS[n](ctx, a.tag))
    with open(os.path.join(out, 'refit_manifest_%s.json' % a.tag), 'w') as f:
        json.dump(docs, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print('refit_arm2 DONE -> %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
