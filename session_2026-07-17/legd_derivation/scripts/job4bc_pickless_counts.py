"""JOB 4(b) pickless _eff derivation + provenance + flex-sensitivity, and 4(c) per-band sample counts
smoothed at the finest resolution (CORE rule 7). One engine load for 4(b); 4(c) reads per_entrant.json.

4(b) provenance (rl_model.py:813-843): for each pickless mechanism, pool the mechanism players' backward
realised value (_nv_bwd via the _ce estimator, MOST-FAVOURABLE cohort cutoff 2021-26), invert it through
the FROZEN v3.4 national curve _natcv34 (cumulative-min non-increasing) -> pick_equiv -> _eff. Consumed as
min(_eff, KMAX=70) downstream. FLEX-SENSITIVITY: the pooled value reads realised production, which reads
gfut(p)=future_position; so a flex future-position write on a pickless mechanism player WOULD move that
mechanism's pooled value -> pick_equiv -> _eff. This script checks whether any pickless player is flex-targeted.
"""
import os, sys, io, contextlib, json, collections
sys.path.insert(0, '/home/user/afl-rl-engine/vendor')
os.chdir('/home/user/afl-rl-engine/engine/rl_after')
sys.path.insert(0, '.')
import numpy as np
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_legd_j4'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']
rlm = sys.modules.get('rl_model')
PICKEQ = getattr(rlm, 'PICKEQ', {}) if rlm else {}
MECH_STATS = getattr(rlm, 'MECH_STATS', {}) if rlm else {}
# fallback: pull from the loaded module namespace via MA if needed
if not PICKEQ:
    for k in ('PICKEQ',):
        PICKEQ = G.get(k, PICKEQ)
if not MECH_STATS:
    MECH_STATS = G.get('MECH_STATS', MECH_STATS)

# flex-sensitivity: which pickless players have future_position != drafted/present, and are any flex-targeted
pickless = [p for p in MA.data if p.get('_pickless')]
flex_touched = []
for p in pickless:
    fp = p.get('future_position'); dp = p.get('drafted_position'); pp = p.get('present_position')
    if fp and fp not in (dp, pp):
        flex_touched.append(dict(player=p['player'], type=p.get('type'), drafted=dp, present=pp, future=fp,
                                 gfut=MA.gfut(p)))

j4b = dict(
    _doc="Job 4(b): pickless mechanism pick-equivalents (_eff) — current values, provenance, flex-sensitivity.",
    derivation="pooled _nv_bwd realised value -> _pick_equiv inverted vs FROZEN v3.4 _natcv34 -> PICKEQ -> _eff; "
               "consumed as min(_eff, KMAX=70). rl_model.py:813-843.",
    PICKEQ=PICKEQ,
    mech_stats=MECH_STATS,
    flex_sensitivity=dict(
        input_that_flex_could_move="pooled realised value reads gfut(p)=future_position (ev/_nv_bwd)",
        frozen_inputs="_natcv34 inversion curve is FROZEN v3.4; PATH_ALPHA fixed — flex does NOT touch these",
        n_pickless=len(pickless),
        n_pickless_flex_touched=len(flex_touched),
        flex_touched_rows=flex_touched,
        verdict=("NO pickless player carries a flex future-position write => the flex-era store leaves every "
                 "pickless _eff UNCHANGED" if not flex_touched else
                 "SOME pickless players carry a flex future-position write => their mechanism pooled value "
                 "(hence pick_equiv/_eff) MOVES under the flex-era store — named above"),
    ),
)
json.dump(j4b, open(BASE + '/out/job4b_pickless_eff.json', 'w'), indent=1)

# ---- 4(c) per-band sample counts at FINEST resolution (per pick), kernel-smoothed (CORE rule 7) ----
recs = json.load(open(BASE + '/out/per_entrant.json'))
P = [r for r in recs if r['incurve'] and r['pick'] and 2004 <= r['year'] <= 2024]
per_pick = collections.Counter(min(r['pick'], 99) for r in P)
picks = list(range(1, 100))
raw = np.array([per_pick.get(k, 0) for k in picks], float)
lg = np.log(picks)
# Nadaraya-Watson smoother over log-pick (the engine's own kernel convention), adaptive-ish fixed bw
def ksmooth(bw=0.28):
    out = []
    for i, x in enumerate(lg):
        w = np.exp(-0.5 * ((lg - x) / bw) ** 2)
        out.append(float((w * raw).sum() / w.sum()))
    return out
sm = ksmooth()
BANDS = ["1-3", "4-7", "8-12", "13-20", "21-27", "28-35", "36-48", "49-99"]
def bidx(pk):
    for lo, hi in [(1,3),(4,7),(8,12),(13,20),(21,27),(28,35),(36,48),(49,99)]:
        if lo <= pk <= hi: return f"{lo}-{hi}"
    return None
band_n = collections.Counter(bidx(min(r['pick'],99)) for r in P)
j4c = dict(
    _doc="Job 4(c): per-band sample counts at the finest resolution the sample supports (per exact pick), "
         "kernel-smoothed per CORE rule 7. Band aggregates are PRESENTATION-ONLY (never a single wide-bin number).",
    core_rule_7="Statistics at the finest resolution the sample supports, smoothed (kernel/local regression) — "
                "never wide bins as one number across a band. (docs/CORE_v2_8.md:99-100)",
    pool_n=len(P),
    per_pick_raw={str(k): int(per_pick.get(k, 0)) for k in picks},
    per_pick_smoothed={str(k): round(sm[i], 2) for i, k in enumerate(picks)},
    band_counts_presentation_only={b: int(band_n.get(b, 0)) for b in BANDS},
    thin_slices=[k for k in picks if per_pick.get(k, 0) <= 3 and k <= 60],
)
json.dump(j4c, open(BASE + '/out/job4c_sample_counts.json', 'w'), indent=1)

print("=== 4(b) PICK-EQUIVALENTS (_eff) ===")
for t, s in sorted(MECH_STATS.items(), key=lambda x: x[1]['pick_equiv']):
    print(f"  {t:4} {s['name']:24} n={s['n']:3} played={s['played_n']:3} hit={s['hit_rate']:5}%  "
          f"pooled={s['pooled_value']:5} pick_equiv/_eff={s['pick_equiv']}  cutoff={s['cutoff']}")
print(f"  flex-touched pickless players: {len(flex_touched)}  -> {j4b['flex_sensitivity']['verdict'][:70]}")
print("\n=== 4(c) per-pick counts (1-20) raw|smoothed ===")
for k in range(1, 21):
    print(f"  pick {k:2}: raw={per_pick.get(k,0):3}  smoothed={sm[k-1]:.2f}")
print("  band counts (presentation-only):", {b: band_n.get(b,0) for b in BANDS})
print("wrote out/job4b_pickless_eff.json, out/job4c_sample_counts.json")
