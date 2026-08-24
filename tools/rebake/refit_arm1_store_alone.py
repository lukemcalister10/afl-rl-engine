#!/usr/bin/env python3
"""REBAKE WEEK · ARM 1 · THE STORE-ALONE REFIT — the ONE committed, versioned entry point.

WHAT THIS IS
  Ruled at register v831 (six rebake decisions) and v833 (the binding handover); directive
  docs/directives/REBAKE_ARM1_STORE_ALONE_2026-08-24.md; prereg
  docs/evidence/rebake_arm1_store_alone_2026-08-24/PREREG.md (committed BEFORE this file existed, P9).

  It refits the scoped fitted artifacts with their INCUMBENT CONSTRUCTIONS — same estimator class, same
  hyperparameters, same feature bind, same training-row rule — on the CURRENT store, and writes them to
  CANDIDATE paths with an in-repo provenance stamp beside each one. It has NO design content: it changes
  no estimator, no hyperparameter, no row rule, and it never touches a live pickle, a live pin,
  data/expected_boot.json, or /home/claude/cm_400.pkl.

  There is exactly ONE deliberate divergence from "run the shipped builder", and it is a divergence of
  DESTINATION, not of construction: nothing is written where the engine would load it.

THE CONSTRUCTIONS, AND WHERE EACH IS READ FROM (never re-implemented here)
  cm_400          par_redesign.retrain() == `cp._lvl_eff = lvl_par; dist_redesign.build()` ==
                  conditional_prior.build_cond_prior(cap=2026, resolved_cut=2021). This file calls
                  build_cond_prior DIRECTLY — solely because rd.build() throws away the row count and the
                  stamp must carry it — and ASSERTS rd.build()'s own default arguments equal the ones
                  passed, so the two can never drift apart (P4: assert the relationship).
  q97m            refit_q97m.Q97M_KW + refit_q97m._engine_Xy() + refit_q97m._fit() — the committed refit
                  entry point's own constants and its own fit, imported, not copied. (--bake is NOT used:
                  it writes data/q97m.pkl and re-pins data/expected_boot.json, both forbidden in this arm.)
  peak_model_v4   engine/forward_valuation/build_peak_model_v4.py, run as its own process with
                  RL_ARM1_OUT set. pvc_snapshot.json CO-EMITS from that same run by design (v831 D6;
                  rl_model.py:1234 loads it as the peak model's FROZEN train-time PVC feature).
  bust_prior_table  NOT REFITTED. No producer for it exists anywhere in this repository — every reference
                  reads it or renames position keys inside it, and git log --follow shows two commits, the
                  initial seed and the #262 vocabulary rename. SHIP_GATES.md:295's claim that
                  build_peak_model_v4.py regenerates it is FALSE AGAINST SOURCE. Declared as prediction P0
                  / falsifier FA2 in the prereg; this entry point HALTS on it rather than inventing one.

T1 — WHERE IT LIVES, MEASURED NOT ASSUMED
  T1 (the owner's fabricated-zeros rule, 2026-07-31) lives in conditional_prior.build_cond_prior and in NO
  other construction. So the cm_400 candidate carries it automatically; q97m's row rule
  (_merged_recover.py:60-64) has never carried it, and applying it there would be a change to a training-row
  rule — design content, which this arm does not have. --t1=off refits cm_400 with the skip disabled, for
  the attribution board only; it is NEVER the candidate.

USAGE (single-thread BLAS, pinned venv, RL_REPO/RL_FV bound to the checkout, RL_WS to the seat's own
workspace — never the shared /home/claude/rl_workspace):
    python3 tools/rebake/refit_arm1_store_alone.py --out <dir> --artifact all
    python3 tools/rebake/refit_arm1_store_alone.py --out <dir> --artifact cm_400 --t1 off --tag noT1
"""
import argparse, contextlib, hashlib, importlib.util, io, json, os, pickle, platform, subprocess, sys, time

VERSION = 'arm1-store-alone/1'


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
    raise SystemExit('refit_arm1 HALT: no checkout root (set RL_REPO).')


def workspace():
    ws = os.environ.get('RL_WS')
    if not ws:
        raise SystemExit('refit_arm1 HALT: set RL_WS to the SEAT\'S OWN engine workspace (a copy of the '
                         'checkout). This entry point deliberately has no default: the shared '
                         '/home/claude/rl_workspace must never be a build seat\'s implicit target (P3).')
    if not os.path.exists(os.path.join(ws, '_merged_recover.py')):
        raise SystemExit('refit_arm1 HALT: RL_WS=%s carries no _merged_recover.py.' % ws)
    return os.path.abspath(ws)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def env_stamp(root):
    import numpy, scipy, sklearn
    boot = json.load(open(os.path.join(root, 'data', 'expected_boot.json')))
    return {
        'entry_point': 'tools/rebake/refit_arm1_store_alone.py',
        'entry_point_version': VERSION,
        'entry_point_md5': md5_file(os.path.abspath(__file__)),
        'ts_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'python': platform.python_version(), 'numpy': numpy.__version__,
        'scipy': scipy.__version__, 'sklearn': sklearn.__version__,
        'training_store_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')),
        'training_store_pin_at_build': boot.get('store'),
        'blas_threads_env': {k: os.environ.get(k) for k in
                             ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                              'NUMEXPR_NUM_THREADS')},
    }


def write_stamp(out, name, doc):
    p = os.path.join(out, 'training_stamp_%s.json' % name)
    with open(p, 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True)
        f.write('\n')
    print('  stamp -> %s' % p)
    return p


# --------------------------------------------------------------------------- cm_400
def refit_cm400(root, ws, out, tag, t1):
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path[:0] = [ws, fv]
    os.chdir(ws)
    PR = load_module('PR_arm1', os.path.join(fv, 'par_redesign.py'))
    rd, cp = PR.rd, PR.cp

    # P4 — assert the relationship, never a hand-typed constant. The construction of record is
    # par_redesign.retrain() -> dist_redesign.build() -> conditional_prior.build_cond_prior. We call the
    # last one directly (rd.build() discards the row count the stamp must carry), so we assert that
    # rd.build's OWN defaults are the arguments we are about to pass.
    import inspect
    d = inspect.signature(rd.build).parameters
    cap, cut = d['cap'].default, d['resolved_cut'].default
    assert (cap, cut) == (2026, 2021), 'dist_redesign.build defaults moved: %r' % ((cap, cut),)
    src = inspect.getsource(PR.retrain)
    assert 'cp._lvl_eff=lvl_par' in src.replace(' ', '') and 'rd.build()' in src.replace(' ', ''), \
        'par_redesign.retrain() is no longer `cp._lvl_eff=lvl_par; return rd.build()` — re-read the ' \
        'construction before refitting: %r' % src

    fo_before = cp.first_observable_season()
    t1_disabled = (t1 == 'off')
    if t1_disabled:
        # ATTRIBUTION ONLY. T1 is the guard `if _fo is not None and d0 < Y < _fo: continue`; disabling it
        # is done by making first_observable_season() report None, which is the construction's own
        # "no T1" state, rather than by editing the row loop.
        cp.first_observable_season = lambda: None
        print('  T1 DISABLED for attribution (first_observable_season -> None; store value was %r)' % fo_before)

    cp._lvl_eff = PR.lvl_par                       # the PAR-CENTRED level feature, exactly as retrain() binds it
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        models, nrows = cp.build_cond_prior(cap=cap, resolved_cut=cut)
    secs = time.time() - t0
    blob = pickle.dumps(models, protocol=pickle.DEFAULT_PROTOCOL)
    art = os.path.join(out, 'cm_400.%s.pkl' % tag)
    with open(art, 'wb') as f:
        f.write(blob)

    import numpy as np
    m0 = models[sorted(models)[0]]
    root_n = int(np.asarray(m0.estimators_).ravel()[0].tree_.n_node_samples[0])
    old = os.path.join(root, 'data', 'cm_400.pkl')
    doc = dict(env_stamp(root))
    doc.update({
        'artifact': 'cm_400 (the five-quantile PAR-centred band forests)',
        'candidate_path': os.path.relpath(art, root),
        'candidate_md5': md5_file(art),                       # MEASURED from the artifact (P4)
        'shipped_path': 'data/cm_400.pkl',
        'shipped_md5': md5_file(old),
        'construction': 'par_redesign.retrain() == cp._lvl_eff=lvl_par; '
                        'conditional_prior.build_cond_prior(cap=%d, resolved_cut=%d)' % (cap, cut),
        'estimator': type(m0).__name__,
        'quantiles': sorted(models),
        'hyperparameters': {str(q): {k: (v if isinstance(v, (int, float, str, type(None))) else str(v))
                                     for k, v in models[q].get_params().items()} for q in sorted(models)},
        'training_rows': int(nrows),
        'training_rows_root_n_in_tree': root_n,
        'n_features_in': int(m0.n_features_in_),
        'T1_fabricated_zero_rule': ('APPLIED (conditional_prior.py:154-155)' if not t1_disabled
                                    else 'DISABLED — attribution variant, NOT the candidate'),
        'first_observable_season': fo_before,
        'fit_seconds': round(secs, 1),
    })
    write_stamp(out, 'cm_400_%s' % tag, doc)
    print('  cm_400 candidate %s  rows=%d  md5=%s  (%.0fs)' % (art, nrows, doc['candidate_md5'], secs))
    if t1_disabled:
        cp.first_observable_season = lambda: fo_before
    return doc


# --------------------------------------------------------------------------- q97m
def refit_q97m_candidate(root, ws, out, tag):
    sys.path.insert(0, root)
    os.environ['RL_WS'] = ws
    RQ = load_module('refit_q97m_arm1', os.path.join(root, 'refit_q97m.py'))
    t0 = time.time()
    X, yy = RQ._engine_Xy()                       # the committed entry point's own fit-inputs
    model = RQ._fit(X, yy)                        # the committed entry point's own fit
    secs = time.time() - t0
    blob = pickle.dumps(model, protocol=pickle.DEFAULT_PROTOCOL)
    art = os.path.join(out, 'q97m.%s.pkl' % tag)
    with open(art, 'wb') as f:
        f.write(blob)
    old = os.path.join(root, 'data', 'q97m.pkl')
    doc = dict(env_stamp(root))
    doc.update({
        'artifact': 'q97m (the frozen q97 CEILING model; band[5], price6 weight 0.10)',
        'candidate_path': os.path.relpath(art, root),
        'candidate_md5': md5_file(art),
        'shipped_path': 'data/q97m.pkl',
        'shipped_md5': md5_file(old),
        'construction': 'refit_q97m.Q97M_KW fitted on _merged_recover.py X/yy (refit_q97m._engine_Xy)',
        'estimator': type(model).__name__,
        'hyperparameters': dict(RQ.Q97M_KW),
        'training_rows': int(X.shape[0]),
        'n_features_in': int(X.shape[1]),
        'training_row_rule': '_merged_recover.py:60-64 — debut<=2021, (pick or _ft), '
                             'MSD EXCLUDED (RL_MSD_POOL_EXCL=%s)' % os.environ.get('RL_MSD_POOL_EXCL'),
        'T1_fabricated_zero_rule': 'NOT PART OF THIS CONSTRUCTION — the X/yy loop carries no '
                                   'first_observable_season skip; applying it here would be a change to '
                                   'the training-row rule, i.e. design content, which ARM 1 has none of',
        'fit_seconds': round(secs, 1),
    })
    write_stamp(out, 'q97m_%s' % tag, doc)
    print('  q97m candidate %s  rows=%d  md5=%s  (%.0fs)' % (art, X.shape[0], doc['candidate_md5'], secs))
    return doc


# --------------------------------------------------------------------------- peak_model_v4 (+ pvc_snapshot)
def refit_peak_model(root, ws, out, tag):
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    script = os.path.join(fv, 'build_peak_model_v4.py')
    env = dict(os.environ)
    env['RL_ARM1_OUT'] = out
    env['PYTHONPATH'] = os.pathsep.join([ws, fv, env.get('PYTHONPATH', '')])
    env.pop('RL_CONFIG_MODE', None)   # the builder is not a gate; it must not re-enter enforce()
    t0 = time.time()
    r = subprocess.run([sys.executable, script], cwd=ws, env=env, capture_output=True, text=True)
    secs = time.time() - t0
    log = os.path.join(out, 'build_peak_model_v4.%s.log' % tag)
    with open(log, 'w') as f:
        f.write(r.stdout + '\n----- stderr -----\n' + r.stderr)
    if r.returncode != 0:
        raise SystemExit('refit_arm1 HALT: build_peak_model_v4.py exited %d — see %s\n%s'
                         % (r.returncode, log, r.stderr[-2000:]))
    pkl = os.path.join(out, 'peak_model_v4.pkl')
    snap = os.path.join(out, 'pvc_snapshot.json')
    for p in (pkl, snap):
        if not os.path.exists(p):
            raise SystemExit('refit_arm1 HALT: build_peak_model_v4.py did not emit %s' % p)
    for src, dst in ((pkl, os.path.join(out, 'peak_model_v4.%s.pkl' % tag)),
                     (snap, os.path.join(out, 'pvc_snapshot.%s.json' % tag))):
        os.replace(src, dst)
    art_pkl = os.path.join(out, 'peak_model_v4.%s.pkl' % tag)
    art_snap = os.path.join(out, 'pvc_snapshot.%s.json' % tag)
    m = pickle.load(open(art_pkl, 'rb'))['model']
    doc = dict(env_stamp(root))
    doc.update({
        'artifact': 'peak_model_v4 (+ pvc_snapshot, CO-EMITTED by the same run, by design)',
        'candidate_path': os.path.relpath(art_pkl, root),
        'candidate_md5': md5_file(art_pkl),
        'shipped_path': 'engine/rl_after/peak_model_v4.pkl',
        'shipped_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'peak_model_v4.pkl')),
        'co_emit_candidate_path': os.path.relpath(art_snap, root),
        'co_emit_candidate_md5': md5_file(art_snap),
        'co_emit_shipped_md5': md5_file(os.path.join(root, 'engine', 'rl_after', 'pvc_snapshot.json')),
        'construction': 'engine/forward_valuation/build_peak_model_v4.py build(2006,2015)',
        'estimator': type(m).__name__,
        'hyperparameters': {k: (v if isinstance(v, (int, float, str, type(None))) else str(v))
                            for k, v in m.get_params().items()},
        'n_features_in': int(m.n_features_in_),
        'n_iter_': int(m.n_iter_),
        'bust_prior_table_input_md5': md5_file(os.path.join(root, 'engine', 'rl_after',
                                                            'bust_prior_table.json')),
        'T1_fabricated_zero_rule': 'NOT PART OF THIS CONSTRUCTION (different row rule; the draft row is a '
                                   'real zero by design and is kept)',
        'fit_seconds': round(secs, 1),
        'builder_log': os.path.relpath(log, root),
    })
    write_stamp(out, 'peak_model_v4_%s' % tag, doc)
    print('  peak_model_v4 candidate %s md5=%s ; pvc_snapshot %s md5=%s  (%.0fs)'
          % (art_pkl, doc['candidate_md5'], art_snap, doc['co_emit_candidate_md5'], secs))
    return doc


# --------------------------------------------------------------------------- bust_prior_table
def refit_bust_prior(root, ws, out, tag):
    raise SystemExit(
        '\n================ ARM 1 HALT — bust_prior_table HAS NO PRODUCER ================\n'
        '  data/expected_boot.json pins bust_prior=%s and boot_guard asserts it on entry, but NOTHING IN\n'
        '  THIS REPOSITORY WRITES engine/rl_after/bust_prior_table.json. Every reference reads it\n'
        '  (build_peak_model_v4.py, rl_model.py:1233, single_source.py:35, boot_guard.py:227) or renames\n'
        '  position keys inside it (session_2026-07-29/item262/migrate_positions.py:128). git log --follow\n'
        '  returns two commits: the initial verified seed and the #262 vocabulary rename.\n'
        '  SHIP_GATES.md:295 states it is "regenerated ONLY by build_peak_model_v4.py at a bake". That is\n'
        '  FALSE AGAINST SOURCE: build_peak_model_v4.py only reads it, as a training INPUT.\n\n'
        '  This arm refits INCUMBENT CONSTRUCTIONS. There is no incumbent construction here to verify, so\n'
        '  there is nothing to refit faithfully — and inventing one would be design content in the arm\n'
        '  that is defined by having none. Declared in advance as prereg prediction P0 / falsifier FA2.\n'
        '  Owed: an owner/supervisor ruling, plus the SHIP_GATES.md correction (process law P11 — the\n'
        '  retirement is recorded where the gate lives).\n'
        '=============================================================================='
        % json.load(open(os.path.join(root, 'data', 'expected_boot.json'))).get('bust_prior'))


ARTIFACTS = {'cm_400': refit_cm400, 'q97m': refit_q97m_candidate,
             'peak_model_v4': refit_peak_model, 'bust_prior_table': refit_bust_prior}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='candidate output directory (never a live artifact path)')
    ap.add_argument('--artifact', default='all',
                    choices=sorted(ARTIFACTS) + ['all', 'scoped'],
                    help="'scoped' = the three artifacts that HAVE a verifiable construction")
    ap.add_argument('--t1', default='on', choices=['on', 'off'],
                    help="cm_400 only; 'off' is the ATTRIBUTION variant and is never the candidate")
    ap.add_argument('--tag', default='candidate')
    a = ap.parse_args(argv[1:])

    root = repo_root()
    ws = workspace()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)

    # FAIL-CLOSED: never emit over a live artifact path or the out-of-repo pinned cache.
    forbidden = {os.path.abspath(os.path.join(root, 'data')),
                 os.path.abspath(os.path.join(root, 'data', 'rl_build')),
                 os.path.abspath(os.path.join(root, 'engine', 'rl_after')),
                 os.path.abspath('/home/claude')}
    if out in forbidden:
        raise SystemExit('refit_arm1 HALT: --out %s is a LIVE artifact directory. Candidates go to a '
                         'distinct candidate path; this arm never overwrites a pinned pickle.' % out)

    sys.path.insert(0, root)
    import config_manifest
    chash = config_manifest.enforce('gate')       # pin the model configuration for the fit
    print('refit_arm1 %s  root=%s  ws=%s  out=%s  config=%s' % (VERSION, root, ws, out, str(chash)[:12]))

    names = (['cm_400', 'q97m', 'peak_model_v4'] if a.artifact in ('all', 'scoped')
             else [a.artifact])
    if a.artifact == 'all':
        names.append('bust_prior_table')

    docs = {}
    for n in names:
        print('--- %s ---' % n)
        docs[n] = (ARTIFACTS[n](root, ws, out, a.tag, a.t1) if n == 'cm_400'
                   else ARTIFACTS[n](root, ws, out, a.tag))
    with open(os.path.join(out, 'refit_manifest_%s.json' % a.tag), 'w') as f:
        json.dump(docs, f, indent=1, sort_keys=True)
        f.write('\n')
    print('refit_arm1 DONE -> %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
