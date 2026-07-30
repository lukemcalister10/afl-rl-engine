"""#279 FOUR-FITTER PVC PANEL — the SHARED, FROZEN harness. Phase 1.

Every fitter imports this and MUST NOT modify it. It fixes, once, for all four fitters:
  * the matrix loader, asserting the committed identity and a NONEMPTY population
  * the establishment definition — the matrix's OWN existing classification, not a new one
  * the structural year-0 values under the ruled basis (VOR, structural completion, class cut 2022)
  * the deterministic held-out folds: seeded, key-sorted, identical for all four fitters
  * the single output schema
  * the pin/descent step, carried verbatim from #271's monotone_strict

alpha = 1 THROUGHOUT this experiment (owner word). No CE aggregator here: the panel is about the FITTER,
not the dial. The six-way alpha evidence rebuilds once, later, on whichever fitter is ruled.

A fitter supplies exactly two things:
    full_fit(vals)                 -> raw[64]        (trained on everything; becomes the ladder)
    fold_fit(train_vals, picks)    -> preds[len(picks)]  (trained on K-1 folds; predicts held-out picks)
"""
import os, json, math, hashlib, collections
import numpy as np

# ---- the committed identity this panel is pinned to ----
EXPECT_STORE = '6b9d00a7'
EXPECT_V0SURF = 'b781ed253bff'
EXPECT_N = 1197                     # ND teaching rows after the class cut
CLASS_CUT = 2022
K_FOLDS = 5
FOLD_SEED = 20260730
MIN_STRATUM = 20
PIN1 = 3000
ND_LAST = 64
YR_LO = 2004
PW_FLOOR = 0.11
QUAL_GAMES = 6                      # the matrix's own establishment threshold (derive_271 QUAL_GAMES)
# the SHIPPED kernel's dials, carried verbatim from #271's fit_year0 — shared by every fitter so that
# "the current kernel" is unambiguous and any departure from it is visible as a departure.
NMIN = 35.0
HMIN, HMAX = 0.10, 0.60
RANGES = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]   # the engine's own board RANGES

_HERE = os.path.dirname(os.path.abspath(__file__))


# ================= establishment: the matrix's OWN classification =================
def never_established(r):
    """Carried from derive_271.never_established — no games>=QUAL_GAMES in any season.
    This is the matrix's existing classification. The panel does not invent a new one."""
    return not any(s['games'] >= QUAL_GAMES for s in r.get('seasons', []))


def concluded(r):
    """Emitter-derived concluded-career marker. The store carries no retired_now (#279 amendment C1);
    the emitter synthesises it from _retired / _last_listed via the engine's own helper."""
    return bool(r.get('retired_now'))


def depth(r):
    return sum(1 for v in (r.get('vpath') or []) if v is not None)


def _es(pwk):
    if pwk is None:
        pwk = 1.0
    return max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))


def realised_at(r, t):
    pw = r.get('pw', {}); vp = r.get('vpath') or []
    num = den = 0.0
    for k in range(1, min(t, len(vp)) + 1):
        v = vp[k - 1]
        if v is None:
            continue
        e = _es(pw.get(str(k), pw.get(str(min(k, 6)))))
        if e <= 0:
            continue
        num += e * v; den += e
    return float(num / den) if den > 0 else 0.0


def realised_full(r):
    if never_established(r):
        return 0.0
    return realised_at(r, len(r.get('vpath') or []))


def sofar(r, t):
    return 0.0 if never_established(r) else realised_at(r, t)


# ================= loader: asserts identity AND nonempty =================
def load_matrix(path):
    M = json.load(open(path))
    meta = M['meta']
    assert meta['store_md5'] == EXPECT_STORE, \
        "matrix store %s != committed identity %s" % (meta['store_md5'], EXPECT_STORE)
    assert meta['v0surf_sig'][:12] == EXPECT_V0SURF, \
        "matrix v0surf %s != expected %s" % (meta['v0surf_sig'][:12], EXPECT_V0SURF)
    ND = [r for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
          and 1 <= r['pick'] <= ND_LAST and YR_LO <= r['year'] <= CLASS_CUT]
    assert ND, "EMPTY ND teaching population — loader refuses to return nothing"
    assert len(ND) == EXPECT_N, "ND population %d != expected %d" % (len(ND), EXPECT_N)
    return meta, ND


# ================= structural year-0 values under the ruled basis =================
def structural_values(ND):
    """Returns (rows, counts) where rows = [{'key','pick','value','concluded','how'}].
    Fallback share is COUNTED and returned — never silent."""
    S = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for r in ND:
        if not concluded(r):
            continue
        T = depth(r)
        if T <= 0:
            continue
        f = realised_full(r)
        for t in range(1, T + 1):
            e = S[(r['pos'], t)]
            e[0] += f; e[1] += sofar(r, t); e[2] += 1
    rows = []; c = collections.Counter()
    for r in ND:
        if concluded(r):
            c['concluded_realised'] += 1
            rows.append({'key': r['key'], 'pick': r['pick'], 'value': realised_full(r),
                         'concluded': True, 'how': 'concluded_realised'}); continue
        T = depth(r)
        if T <= 0:
            c['prior_fallback_no_written'] += 1
            rows.append({'key': r['key'], 'pick': r['pick'], 'value': float(r['v0']),
                         'concluded': False, 'how': 'prior_fallback_no_written'}); continue
        e = S.get((r['pos'], T))
        if e is None or e[2] < MIN_STRATUM or e[1] <= 0:
            c['prior_fallback_thin'] += 1
            rows.append({'key': r['key'], 'pick': r['pick'], 'value': float(r['v0']),
                         'concluded': False, 'how': 'prior_fallback_thin'}); continue
        c['completed'] += 1
        rows.append({'key': r['key'], 'pick': r['pick'],
                     'value': sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2])),
                     'concluded': False, 'how': 'completed'})
    fb = c['prior_fallback_thin'] + c['prior_fallback_no_written']
    assert c['concluded_realised'] + c['completed'] + fb == len(ND), \
        "provenance counts do not sum to population"
    return rows, {'counts': dict(c), 'fallback_rows': fb, 'of_population': len(ND),
                  'fallback_share_pct': round(100.0 * fb / len(ND), 3)}


# ================= deterministic folds: seeded, key-sorted, identical for all fitters =================
def folds(rows, k=K_FOLDS, seed=FOLD_SEED):
    """Key-sorted then permuted by a fixed-seed RandomState, so the assignment is byte-identical for
    every fitter and every re-run, independent of dict ordering or PYTHONHASHSEED."""
    keys = sorted(r['key'] for r in rows)
    idx = np.random.RandomState(seed).permutation(len(keys))
    out = {}
    for pos, j in enumerate(idx):
        out[keys[j]] = pos % k
    return out


def folds_fingerprint(fa):
    """A hash of the fold assignment. Every fitter must report this; a mismatch means the folds moved."""
    s = json.dumps(sorted(fa.items()), separators=(',', ':'))
    return hashlib.md5(s.encode()).hexdigest()[:12]


# ================= the SHIPPED kernel, carried verbatim — the panel's common reference =================
def kernel_raw(rows, picks, nmin=NMIN, hmin=HMIN, hmax=HMAX):
    """The shipped year-0 aggregator at alpha=1: Gaussian kernel over log(pick), bandwidth grown from
    hmin until the effective n reaches nmin, then a weighted MEAN. Returns (raw, effn) at each pick.
    This is fit_year0's inner loop with the time kernel dropped (structural rows are all ty=0)."""
    lp = np.array([math.log(r['pick']) for r in rows], float)
    v = np.array([max(r['value'], 0.0) for r in rows], float)
    raw, effn = [], []
    for p in picks:
        Lp = math.log(p); h = hmin
        while h < hmax:
            if np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2)) >= nmin:
                break
            h += 0.02
        W = np.exp(-0.5 * ((lp - Lp) / h) ** 2)
        raw.append(float(np.sum(W * v) / np.sum(W)))
        effn.append(float(np.sum(W)))
    return raw, effn


def bandwidth_at(rows, p, nmin=NMIN, hmin=HMIN, hmax=HMAX):
    """The bandwidth the shipped kernel would choose at pick p, for fitters that need it."""
    lp = np.array([math.log(r['pick']) for r in rows], float)
    Lp = math.log(p); h = hmin
    while h < hmax:
        if np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2)) >= nmin:
            break
        h += 0.02
    return h


# ================= the pin / descent step, carried verbatim =================
def pava_ni(vals, wts):
    n = len(vals)
    v = [float(x) for x in vals]; w = [float(x) for x in wts]
    sv = []; sw = []; sn = []
    for j in range(n):
        cv, cw, cn = v[j], w[j], 1
        while sv and sv[-1] < cv - 1e-12:
            pv, pw_, pn = sv.pop(), sw.pop(), sn.pop()
            cv = (pv * pw_ + cv * cw) / (pw_ + cw); cw = pw_ + cw; cn = pn + cn
        sv.append(cv); sw.append(cw); sn.append(cn)
    out = []
    for bv, bn in zip(sv, sn):
        out += [bv] * bn
    return np.array(out)


def pin_and_check(raw, effn):
    """monotone_strict carried verbatim from #271 (fit[0]=PIN1 is a HARD SET, not a rescale),
    then a post-pin strict-descent guard whose firings are reported."""
    fit = pava_ni(raw, effn).copy()
    fit[0] = PIN1
    EPS = 1e-3
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS:
            fit[i] = fit[i - 1] - EPS
    ic = [int(round(x)) for x in fit]
    ic[0] = PIN1
    forced = []
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]:
            forced.append(i + 1); ic[i] = ic[i - 1] - 1
    return ic, forced


def raw_monotone_violations(raw):
    return int(sum(1 for i in range(1, len(raw)) if raw[i] >= raw[i - 1]))


def payload(ladder):
    return hashlib.md5(json.dumps({str(i + 1): v for i, v in enumerate(ladder)},
                                  sort_keys=True).encode()).hexdigest()[:8]


# ================= the ONE output schema =================
SCHEMA_VERSION = 'pvc-panel-1'

def save_result(outdir, name, description, ladder, fold_preds, diagnostics, can_fail, prov, fa):
    """fold_preds: [{'key','pick','fold','actual','predicted'}] — one row per held-out observation."""
    assert len(ladder) == 64, "ladder must be 64 points, got %d" % len(ladder)
    assert ladder[0] == PIN1, "ladder must be pinned at %d, got %s" % (PIN1, ladder[0])
    assert all(ladder[i] < ladder[i - 1] for i in range(1, 64)), "ladder must be strictly descending"
    assert fold_preds, "EMPTY fold predictions"
    got = {p['key'] for p in fold_preds}
    assert len(got) == len(fold_preds), "duplicate keys in fold predictions"
    res = {'schema': SCHEMA_VERSION, 'fitter': name, 'description': description,
           'alpha': 1.0, 'basis': 'structural, class cut %d, VOR' % CLASS_CUT,
           'folds': {'k': K_FOLDS, 'seed': FOLD_SEED, 'fingerprint': folds_fingerprint(fa)},
           'ladder': ladder, 'ladder_payload': payload(ladder),
           'ladder_total': int(sum(ladder)),
           'diagnostics': diagnostics, 'can_fail_proof': can_fail, 'provenance': prov,
           'n_fold_predictions': len(fold_preds), 'fold_predictions': fold_preds}
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, 'fitter_%s.json' % name)
    json.dump(res, open(p, 'w'), indent=1, sort_keys=True)
    open(p, 'a').write("\n")
    return p


if __name__ == '__main__':
    import sys
    meta, ND = load_matrix(sys.argv[1])
    rows, prov = structural_values(ND)
    fa = folds(rows)
    print("HARNESS SELF-CHECK")
    print("  store %s  v0surf %s  n=%d" % (meta['store_md5'], meta['v0surf_sig'][:12], len(ND)))
    print("  provenance:", json.dumps(prov))
    print("  folds k=%d seed=%d fingerprint=%s" % (K_FOLDS, FOLD_SEED, folds_fingerprint(fa)))
    print("  fold sizes:", dict(collections.Counter(fa.values())))
    print("  establishment: never_established true on %d of %d"
          % (sum(1 for r in ND if never_established(r)), len(ND)))
    print("  mean structural value: %.1f" % float(np.mean([r['value'] for r in rows])))
