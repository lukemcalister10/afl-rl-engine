"""STUDY B / M1 — the band-model artifact census. READ-ONLY."""
import pickle, hashlib, json, os, sys, io, collections
import numpy as np

REPO = '/home/user/afl-rl-engine'
OUT = {}

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def stored_sklearn_version(path):
    """The sklearn version recorded IN THE PICKLE BYTES at the time the object was pickled."""
    import re
    b = open(path, 'rb').read()
    hits = set()
    for m in re.finditer(rb'_sklearn_version', b):
        mm = re.search(rb'(\d+\.\d+(?:\.\d+)?)', b[m.end():m.end() + 40])
        if mm:
            hits.add(mm.group(1).decode())
    return sorted(hits) or None

def probe(obj, name):
    d = {'py_type': type(obj).__name__}
    if hasattr(obj, '__dict__'):
        pass
    for attr in ('n_features_in_', 'n_estimators_', 'n_estimators', 'loss', 'alpha',
                 'learning_rate', 'max_depth', 'min_samples_leaf', 'random_state',
                 'criterion', 'subsample', 'max_features', 'n_iter_', '_n_features',
                 'monotonic_cst', 'n_trees_per_iteration_'):
        if hasattr(obj, attr):
            v = getattr(obj, attr)
            try:
                json.dumps(v)
            except Exception:
                v = repr(v)
            d[attr] = v
    # NOTE (measurement trap): do NOT read _sklearn_version off a LOADED object. sklearn sets it in
    # __getstate__, so calling __getstate__ on an already-unpickled estimator re-stamps it with the
    # CURRENT version and tells you nothing about the fit. The stored value is read from the raw
    # pickle BYTES in stored_sklearn_version() below.
    if hasattr(obj, 'estimators_'):
        try:
            est = np.asarray(obj.estimators_)
            d['estimators_shape'] = list(est.shape)
            trees = [e.tree_ for e in est.ravel()]
            d['n_trees'] = len(trees)
            d['total_nodes'] = int(sum(t.node_count for t in trees))
            d['max_depth_seen'] = int(max(t.max_depth for t in trees))
            # training-set size proxy: root weighted_n_node_samples of tree 0
            d['root_n_samples'] = float(trees[0].weighted_n_node_samples[0])
            d['n_features_from_tree'] = int(trees[0].n_features)
            # feature usage census
            uc = collections.Counter()
            thr = collections.defaultdict(set)
            for t in trees:
                for f, th in zip(t.feature, t.threshold):
                    if f >= 0:
                        uc[int(f)] += 1
                        thr[int(f)].add(float(th))
            d['split_counts_by_feature'] = {str(k): v for k, v in sorted(uc.items())}
            d['distinct_thresholds_by_feature'] = {str(k): len(v) for k, v in sorted(thr.items())}
            d['threshold_range_by_feature'] = {str(k): [min(v), max(v)] for k, v in sorted(thr.items())}
        except Exception as e:
            d['tree_probe_error'] = repr(e)
    if hasattr(obj, 'init_'):
        d['init_'] = type(obj.init_).__name__
        try:
            d['init_constant'] = float(np.ravel(obj.init_.constant_)[0])
        except Exception:
            pass
    return d


for rel in ('data/cm_400.pkl', 'data/q97m.pkl', 'data/v0surf.pkl',
            'engine/rl_after/peak_model_v4.pkl'):
    p = os.path.join(REPO, rel)
    rec = {'path': rel, 'md5': md5(p), 'bytes': os.path.getsize(p),
           'stored_sklearn_version': stored_sklearn_version(p)}
    try:
        obj = pickle.load(open(p, 'rb'))
    except Exception as e:
        rec['load_error'] = repr(e)
        OUT[rel] = rec
        continue
    rec['container_type'] = type(obj).__name__
    if isinstance(obj, dict):
        rec['keys'] = [repr(k) for k in obj.keys()]
        rec['members'] = {repr(k): probe(v, repr(k)) for k, v in obj.items()
                          if hasattr(v, 'predict') or hasattr(v, 'estimators_')}
        rec['non_model_members'] = {repr(k): (type(v).__name__,
                                              (v if isinstance(v, (int, float, str, bool, type(None)))
                                               else (len(v) if hasattr(v, '__len__') else repr(v)[:120])))
                                    for k, v in obj.items()
                                    if not (hasattr(v, 'predict') or hasattr(v, 'estimators_'))}
    else:
        rec['members'] = {'<root>': probe(obj, rel)}
    OUT[rel] = rec

print(json.dumps(OUT, indent=1, sort_keys=True, default=str))
