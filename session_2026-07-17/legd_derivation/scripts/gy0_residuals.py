"""G-Y0 RESIDUAL EVIDENCE for the memo's tolerance proposal (audit #37: signed residuals by pick DECILE).
Reads per_entrant.json (v0_start per entrant, base 968de0c7) + the SHIPPED PVC curve (pvc_curve_L1b.json).
G-Y0 identity: comp-weighted mean V0 per pick band == derived PVC per band (population-level, across drafts;
a single class off-curve is NOT a breach). This measures the SIGNED residual (meanV0 - PVC) the CURRENT
(shipped) curve carries, by pick decile and by the standard bands, to MOTIVATE a proposed tolerance.
The NUMBER is the owner's to rule; this only lays out the measured distribution. Nothing is fitted here.
"""
import json, statistics
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
ENG = '/home/user/afl-rl-engine/engine/rl_after'
recs = json.load(open(BASE + '/out/per_entrant.json'))
curve = {int(k): v for k, v in json.load(open(ENG + '/pvc_curve_L1b.json'))['curve'].items()}

# in-curve derivation pool, real pick, ND/RD 2004-2024 (same pool as jobs 2/3)
P = [r for r in recs if r['incurve'] and r['pick'] and 2004 <= r['year'] <= 2024 and r['v0']]

def pvc(pk): return curve[min(pk, 99)]

# --- signed residual per entrant: V0(day-after) - PVC(pick, day-before). G-Y0 wants these to net ~0 per band.
for r in P:
    r['_resid'] = r['v0'] - pvc(r['pick'])
    r['_reld'] = r['_resid'] / pvc(r['pick'])

# --- by PICK DECILE (10 equal-count bins over the pool, ordered by pick) — audit #37's cut ---
Psort = sorted(P, key=lambda r: r['pick'])
n = len(Psort); dec = []
for d in range(10):
    lo = d * n // 10; hi = (d + 1) * n // 10
    g = Psort[lo:hi]
    picks = [r['pick'] for r in g]
    resid = [r['_resid'] for r in g]
    reld = [r['_reld'] for r in g]
    dec.append(dict(decile=d + 1, n=len(g), pick_lo=min(picks), pick_hi=max(picks),
                    mean_V0=round(statistics.mean(r['v0'] for r in g), 1),
                    mean_PVC=round(statistics.mean(pvc(r['pick']) for r in g), 1),
                    mean_signed_resid=round(statistics.mean(resid), 1),
                    median_signed_resid=round(statistics.median(resid), 1),
                    mean_rel_resid_pct=round(100 * statistics.mean(reld), 2),
                    sd_resid=round(statistics.pstdev(resid), 1)))

# --- by the standard bands (presentation cross-check) ---
BANDS = ["1-3", "4-7", "8-12", "13-20", "21-27", "28-35", "36-48", "49-99"]
band = []
for b in BANDS:
    g = [r for r in P if r['band'] == b]
    if not g: continue
    resid = [r['_resid'] for r in g]; reld = [r['_reld'] for r in g]
    band.append(dict(band=b, n=len(g),
                     mean_V0=round(statistics.mean(r['v0'] for r in g), 1),
                     mean_PVC=round(statistics.mean(pvc(r['pick']) for r in g), 1),
                     mean_signed_resid=round(statistics.mean(resid), 1),
                     mean_rel_resid_pct=round(100 * statistics.mean(reld), 2)))

overall_mean = round(statistics.mean(r['_resid'] for r in P), 1)
overall_relpct = round(100 * statistics.mean(r['_reld'] for r in P), 2)
absrel = sorted(abs(d['mean_rel_resid_pct']) for d in dec)
out = dict(
    _doc="G-Y0 signed residuals (meanV0 - shipped_PVC) by pick decile + band, base 968de0c7. Evidence for "
         "the memo's tolerance proposal (audit #37). Number is the owner's; nothing fitted.",
    identity="comp-weighted mean V0 per band == derived PVC per band (population, across drafts). "
             "Single class off-curve NOT a breach; measure across drafts.",
    pool_n=len(P),
    shipped_curve="pvc_curve_L1b.json (the curve being replaced — residuals show the CURRENT gap shape)",
    overall_mean_signed_resid=overall_mean, overall_mean_rel_resid_pct=overall_relpct,
    max_abs_decile_rel_pct=absrel[-1], median_abs_decile_rel_pct=round(statistics.median(absrel), 2),
    by_pick_decile=dec, by_band=band,
    note="V0 > PVC in every band (the draft creates value; the young side is already the high side) — "
         "consistent with acceptance fix_direction_STALE_DO_NOT_APPLY. The NEW curve, derived toward the "
         "comp-weighted V0 target, should shrink these residuals; the tolerance bounds the residual the "
         "gate tolerates per decile AFTER re-derivation.",
)
json.dump(out, open(BASE + '/out/gy0_residuals.json', 'w'), indent=1)
print("G-Y0 signed residuals vs SHIPPED curve (meanV0 - PVC), base 968de0c7")
print(f"pool={len(P)}  overall mean resid={overall_mean} SCAR ({overall_relpct}% rel)")
print(f"\n{'dec':>3}{'picks':>9}{'n':>5}{'meanV0':>9}{'meanPVC':>9}{'resid':>8}{'rel%':>8}{'sd':>8}")
for d in dec:
    print(f"{d['decile']:>3}{str(d['pick_lo'])+'-'+str(d['pick_hi']):>9}{d['n']:>5}{d['mean_V0']:>9}"
          f"{d['mean_PVC']:>9}{d['mean_signed_resid']:>8}{d['mean_rel_resid_pct']:>8}{d['sd_resid']:>8}")
print(f"\nmax |decile rel%|={absrel[-1]}   median |decile rel%|={round(statistics.median(absrel),2)}")
print("\nby band:")
for b in band:
    print(f"  {b['band']:7} n={b['n']:4} meanV0={b['mean_V0']:7} meanPVC={b['mean_PVC']:7} "
          f"resid={b['mean_signed_resid']:7} ({b['mean_rel_resid_pct']}%)")
print("wrote out/gy0_residuals.json")
