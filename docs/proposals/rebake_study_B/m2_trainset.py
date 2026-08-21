"""STUDY B / M2 — rebuild the cm_400 / q97m training design matrices on the CURRENT store and compare
against the row counts baked into the pinned pickles. READ-ONLY: nothing is written outside scratch."""
import os, sys, io, json, contextlib, hashlib, collections
import numpy as np

os.environ.setdefault('RL_GAMMA', '1.0'); os.environ.setdefault('RL_PICK1', '3000')
WS = '/home/claude/rl_workspace/rl_after'
FV = '/home/claude/rl_workspace/forward_valuation'
for pth in (WS, FV, '/home/claude/rl_vendor'):
    if os.path.isdir(pth) and pth not in sys.path:
        sys.path.insert(0, pth)

os.chdir(WS)   # rl_model.py reads its store by RELATIVE path
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA

import importlib.util
def ld(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m)
    return m

FVDIR = os.environ.get('STUDYB_FV', '/home/user/afl-rl-engine/engine/forward_valuation')
PR = ld('PR', os.path.join(FVDIR, 'par_redesign.py'))
cp = PR.cp

R = {}
store = os.path.join(os.path.dirname(MA.__file__), 'rl_model_data.json')
R['store_path'] = store
R['store_md5'] = hashlib.md5(open(store, 'rb').read()).hexdigest()
R['store_rows'] = len(MA.data)
R['first_observable_season'] = cp.first_observable_season()

def rows(level_fn, apply_t1, excl_msd, pool_filter=None, cap=2026, resolved_cut=2021, collect=False):
    """Reproduce the training-row enumeration under a given switch set."""
    old = cp._lvl_eff
    cp._lvl_eff = level_fn
    try:
        pool = [p for p in MA.data if MA.GRP.get(p['pos'])]
        if pool_filter: pool = [p for p in pool if pool_filter(p)]
        fo = cp.first_observable_season()
        X, y, meta = [], [], []
        for p in pool:
            if cp.debutyr(p) > resolved_cut: continue
            if not (p.get('pick') or p.get('_ft')): continue
            if excl_msd and p.get('type') == 'MSD': continue
            d0 = cp.debutyr(p) - 1
            last = max([x['year'] for x in p['scoring']] + [d0])
            for Y in range(d0, min(last, cap) + 1):
                if apply_t1 and fo is not None and d0 < Y < fo: continue
                X.append(cp._feat(p, Y)); y.append(cp.fwd_best3_from(p, Y, cap))
                if collect:
                    meta.append((p.get('player'), p.get('pos'), Y, d0, bool(MA.is_pool(p)),
                                 p.get('type'), bool(p.get('_by'))))
        return np.array(X), np.array(y), meta
    finally:
        cp._lvl_eff = old

# --- the four switch combinations, on the CURRENT store ---
combos = {}
for tag, (lvl, t1, msd) in {
    'cm400_construction_parlevel_T1on_MSDin':  (PR.lvl_par, True,  False),
    'cm400_construction_parlevel_T1off_MSDin': (PR.lvl_par, False, False),
    'q97m_construction_parlevel_T1off_MSDex': (PR.lvl_par, False, True),
    'q97m_construction_parlevel_T1on_MSDex':  (PR.lvl_par, True,  True),
}.items():
    X, y, _ = rows(lvl, t1, msd)
    combos[tag] = {'rows': int(X.shape[0]), 'features': int(X.shape[1]),
                   'y_mean': float(y.mean()), 'y_zero_frac': float((y == 0).mean())}
R['current_store_row_counts'] = combos
R['pinned_pickle_root_n_samples'] = {'cm_400.pkl': 13226.0, 'q97m.pkl': 13111.0,
                                     '_source': 'measured in M1 from tree_.weighted_n_node_samples[0]'}

# --- population composition of the cm_400-construction training pool ---
X, y, meta = rows(PR.lvl_par, True, False, collect=True)
R['train_pool_composition'] = {
    'rows': len(meta),
    'players': len({m[0] for m in meta}),
    'pool_arm_rows': sum(1 for m in meta if m[4]),
    'national_arm_rows': sum(1 for m in meta if not m[4]),
    'pool_arm_players': len({m[0] for m in meta if m[4]}),
    'national_arm_players': len({m[0] for m in meta if not m[4]}),
    'msd_rows': sum(1 for m in meta if m[5] == 'MSD'),
    'msd_players': len({m[0] for m in meta if m[5] == 'MSD'}),
    'entry_types': dict(collections.Counter(m[5] for m in meta)),
    'rows_missing_birthyear': sum(1 for m in meta if not m[6]),
    'players_missing_birthyear': len({m[0] for m in meta if not m[6]}),
    'draft_year_range': [min(m[3] for m in meta), max(m[3] for m in meta)],
    'asof_year_range': [min(m[2] for m in meta), max(m[2] for m in meta)],
    'rows_by_asof_year': dict(sorted(collections.Counter(m[2] for m in meta).items())),
}

# --- feature matrix summary (cm_400 construction) ---
FN = ['oh_MID','oh_SD','oh_SF','oh_KPD','oh_KPF','oh_RUCK','log_effpk','exposure','tenure','level','age']
R['feature_names'] = FN
R['feature_summary'] = {FN[i]: {'min': float(X[:, i].min()), 'p50': float(np.median(X[:, i])),
                                'max': float(X[:, i].max()), 'mean': float(X[:, i].mean())}
                        for i in range(X.shape[1])}
R['target_summary'] = {'min': float(y.min()), 'p50': float(np.median(y)), 'max': float(y.max()),
                       'mean': float(y.mean()), 'zeros': int((y == 0).sum())}
np.save('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/study_b/X_cm.npy', X)
np.save('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/study_b/y_cm.npy', y)
with open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/study_b/meta_cm.json', 'w') as f:
    json.dump(meta, f)

print(json.dumps(R, indent=1, sort_keys=True, default=str))
