"""DATASET AUDIT — the band's training population, assembled EXACTLY as conditional_prior does,
counted by entry type / era / position, and the 45.36% pool-career figure re-derived and decomposed.

Also emits the design matrix (features + target + population labels + a time key) to a .npz so the
candidate fits in 05_candidates.py never re-derive it.

READ-ONLY on the repo. Run with cwd = the scratch ws copy and RL_REPO = the scratch repo symlink,
exactly as probe3.py loads the engine.
"""
import io, contextlib, json, os, sys, time, collections
import numpy as np

S = os.environ['STUDY']
OUT = os.path.join(S, 'out')
os.makedirs(OUT, exist_ok=True)

t0 = time.time()
sys.path.insert(0, '.')
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
import importlib.util


def _L(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    with contextlib.redirect_stdout(io.StringIO()):
        sp.loader.exec_module(m)
    return m


FV = os.path.join(os.environ['RL_REPO'], 'engine', 'forward_valuation')
cp = _L('cp', os.path.join(FV, 'conditional_prior.py'))
print('loaded engine %.1fs   store rows=%d' % (time.time() - t0, len(MA.data)), flush=True)

# ---------------------------------------------------------------- the population
# build_cond_prior's own body, re-walked so every row can be LABELLED.
CAP, CUT = 2026, 2021
pool_all = [p for p in MA.data if MA.GRP.get(p['pos'])]
fo = cp.first_observable_season()
print('FIRST_OBSERVABLE season = %r' % fo)

rows = []
for p in pool_all:
    if cp.debutyr(p) > CUT:
        continue
    if not (p.get('pick') or p.get('_ft')):
        continue
    d0 = cp.debutyr(p) - 1
    last = max([x['year'] for x in p['scoring']] + [d0])
    for Y in range(d0, min(last, CAP) + 1):
        t1_drop = (fo is not None and d0 < Y < fo)
        rows.append(dict(p=p, Y=Y, t1_drop=t1_drop))

print('rows before T1 = %d   T1 drops = %d   rows after T1 = %d'
      % (len(rows), sum(r['t1_drop'] for r in rows), sum(not r['t1_drop'] for r in rows)))

live = [r for r in rows if not r['t1_drop']]

# ---------------------------------------------------------------- labels + features
GROUPS = cp.GROUPS


def entry_class(p):
    """The population label the owner reasons in.
       ND-early  national pick 1-18      ND-mid  19-40      ND-late 41-64
       RD        rookie draft / PSD (pool by the ruling)
       SSP       every pickless mechanism (MSD/SSP/IRE/UNR/PD*)
       ND-pool   a NATIONAL selection at 65+ (pool by the ruling, but type ND)"""
    t = p.get('type')
    pk = p.get('pick') or 0
    if t == 'ND':
        if 1 <= pk <= 18:
            return 'ND-early'
        if 19 <= pk <= 40:
            return 'ND-mid'
        if 41 <= pk <= 64:
            return 'ND-late'
        return 'ND-pool'
    if t in ('RD', 'PSD'):
        return 'RD/PSD'
    return 'SSP/other'


X = []
y = []
meta = []
for r in live:
    p, Y = r['p'], r['Y']
    f = cp._feat(p, Y)
    X.append(f)
    y.append(cp.fwd_best3_from(p, Y, CAP))
    meta.append(dict(key=p.get('key'), player=p.get('player'), Y=Y,
                     draft_year=p['year'], debut=cp.debutyr(p), tenure=Y - (cp.debutyr(p) - 1),
                     type=p.get('type'), pick=p.get('pick'), effpk=MA.effpk(p),
                     is_pool=bool(MA.is_pool(p)), grp=p.get('_grp'),
                     pos=MA.gfut(p), cls=entry_class(p)))
X = np.array(X, dtype=float)
y = np.array(y, dtype=float)
print('design matrix %r  target %r' % (X.shape, y.shape))

# ---------------------------------------------------------------- counts
aud = {}
aud['first_observable'] = fo
aud['rows_before_T1'] = len(rows)
aud['rows_after_T1'] = len(live)
aud['T1_dropped'] = len(rows) - len(live)
aud['players'] = len(set(m['key'] for m in meta))
aud['store_md5'] = None
try:
    import hashlib
    aud['store_md5'] = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()
except Exception as e:
    aud['store_md5'] = 'ERR %r' % (e,)


def tab(keyfn, name):
    c = collections.Counter(keyfn(m) for m in meta)
    pl = collections.defaultdict(set)
    for m in meta:
        pl[keyfn(m)].add(m['key'])
    d = {str(k): dict(rows=c[k], pct_rows=round(100.0 * c[k] / len(meta), 2), players=len(pl[k]))
         for k in c}
    aud[name] = dict(sorted(d.items(), key=lambda kv: -kv[1]['rows']))
    return d


tab(lambda m: m['cls'], 'by_entry_class')
tab(lambda m: m['pos'], 'by_position')
tab(lambda m: 'pool' if m['is_pool'] else 'national', 'by_pool_split')
tab(lambda m: '%ds' % (m['draft_year'] // 5 * 5), 'by_draft_era')
tab(lambda m: str(min(m['tenure'], 12)), 'by_tenure')
tab(lambda m: m['grp'] or m['type'], 'by_grp')

# ---- the 45.36% figure, re-derived and decomposed ------------------------------------------
npool = sum(1 for m in meta if m['is_pool'])
aud['pool_row_pct'] = round(100.0 * npool / len(meta), 4)
pool_players = set(m['key'] for m in meta if m['is_pool'])
all_players = set(m['key'] for m in meta)
aud['pool_player_pct'] = round(100.0 * len(pool_players) / len(all_players), 4)
# and on the PRE-T1 population (which is what the shipped artifact was fitted on)
npool_pre = sum(1 for r in rows if MA.is_pool(r['p']))
aud['pool_row_pct_preT1'] = round(100.0 * npool_pre / len(rows), 4)
dec = collections.Counter()
decp = collections.defaultdict(set)
for m in meta:
    if m['is_pool']:
        dec[m['cls']] += 1
        decp[m['cls']].add(m['key'])
aud['pool_decomposition'] = {k: dict(rows=v, pct_of_all_rows=round(100.0 * v / len(meta), 2),
                                     pct_of_pool_rows=round(100.0 * v / npool, 2),
                                     players=len(decp[k]))
                             for k, v in sorted(dec.items(), key=lambda kv: -kv[1])}

# ---- what the pool rows look like in the feature space --------------------------------------
LVL = 9
lvl = X[:, LVL]
ispool = np.array([m['is_pool'] for m in meta])
aud['level_feature'] = {
    'all': dict(mean=float(lvl.mean()), p10=float(np.percentile(lvl, 10)),
                p50=float(np.percentile(lvl, 50)), p90=float(np.percentile(lvl, 90))),
    'pool': dict(n=int(ispool.sum()), mean=float(lvl[ispool].mean()),
                 p50=float(np.percentile(lvl[ispool], 50)),
                 p90=float(np.percentile(lvl[ispool], 90))),
    'national': dict(n=int((~ispool).sum()), mean=float(lvl[~ispool].mean()),
                     p50=float(np.percentile(lvl[~ispool], 50)),
                     p90=float(np.percentile(lvl[~ispool], 90))),
}
# the thin band the diagnosis named: level 42-70
thin = (lvl >= 42) & (lvl <= 70)
aud['thin_band_42_70'] = dict(rows=int(thin.sum()), pct=round(100.0 * thin.sum() / len(lvl), 2),
                              pool_share_pct=round(100.0 * (thin & ispool).sum() / max(thin.sum(), 1), 2))
byc = collections.Counter(m['cls'] for m, t in zip(meta, thin) if t)
aud['thin_band_by_class'] = dict(byc.most_common())

# ---- target by class (the thing the owner's instinct is about) -------------------------------
tb = {}
for cls in set(m['cls'] for m in meta):
    sel = np.array([m['cls'] == cls for m in meta])
    tb[cls] = dict(n=int(sel.sum()), mean_target=round(float(y[sel].mean()), 2),
                   p50=round(float(np.percentile(y[sel], 50)), 2),
                   p90=round(float(np.percentile(y[sel], 90)), 2),
                   zero_share_pct=round(100.0 * float((y[sel] == 0).mean()), 2))
aud['target_by_class'] = dict(sorted(tb.items(), key=lambda kv: -kv[1]['mean_target']))

# ---- effpk: does the pick feature already unify late-ND and pool? ----------------------------
epk = np.array([m['effpk'] for m in meta])
aud['effpk_census'] = {str(int(k)): int(v) for k, v in
                       sorted(collections.Counter(epk[epk >= 55]).items())}
aud['effpk_note'] = ('cp._feat uses log(min(effpk,KMAX=70)). rl_model pins EVERY pool entrant at '
                     'effpk = POOL_PICK = 65, so pool rows sit at log(65)=4.174 and an ND pick 64 '
                     'sits at log(64)=4.159 — 0.015 apart in the feature the trees split on.')

json.dump(aud, open(os.path.join(OUT, 'dataset_audit.json'), 'w'), indent=1, default=str)

np.savez_compressed(os.path.join(OUT, 'design.npz'), X=X, y=y,
                    cls=np.array([m['cls'] for m in meta]),
                    pos=np.array([m['pos'] for m in meta]),
                    ispool=ispool,
                    key=np.array([m['key'] for m in meta]),
                    player=np.array([m['player'] for m in meta]),
                    Y=np.array([m['Y'] for m in meta]),
                    draft_year=np.array([m['draft_year'] for m in meta]),
                    debut=np.array([m['debut'] for m in meta]),
                    tenure=np.array([m['tenure'] for m in meta]),
                    effpk=epk, ptype=np.array([m['type'] for m in meta]))

# ---------------- print ----------------
print()
print('POPULATION: %d rows, %d players, store %s' % (len(meta), aud['players'], aud['store_md5'][:8]))
print('T1: %d rows before, %d dropped, %d after' % (aud['rows_before_T1'], aud['T1_dropped'], len(meta)))
print()
for nm in ('by_entry_class', 'by_pool_split', 'by_position', 'by_draft_era'):
    print(nm.upper())
    for k, v in aud[nm].items():
        print('   %-12s rows %6d (%5.2f%%)  players %4d' % (k, v['rows'], v['pct_rows'], v['players']))
    print()
print('POOL SHARE OF TRAINING ROWS: %.2f%%  (players %.2f%%)  [pre-T1: %.2f%%]'
      % (aud['pool_row_pct'], aud['pool_player_pct'], aud['pool_row_pct_preT1']))
print('DECOMPOSITION:')
for k, v in aud['pool_decomposition'].items():
    print('   %-12s rows %6d = %5.2f%% of all, %5.2f%% of pool, players %4d'
          % (k, v['rows'], v['pct_of_all_rows'], v['pct_of_pool_rows'], v['players']))
print()
print('TARGET BY CLASS')
for k, v in aud['target_by_class'].items():
    print('   %-12s n=%6d  mean %6.2f  p50 %6.2f  p90 %6.2f  zero-target %5.2f%%'
          % (k, v['n'], v['mean_target'], v['p50'], v['p90'], v['zero_share_pct']))
print()
print('THIN BAND (level 42-70): %d rows (%.2f%%), pool share %.2f%%'
      % (aud['thin_band_42_70']['rows'], aud['thin_band_42_70']['pct'],
         aud['thin_band_42_70']['pool_share_pct']))
print('   by class:', aud['thin_band_by_class'])
print()
print(aud['effpk_note'])
print('wrote out/dataset_audit.json + out/design.npz')
