#!/usr/bin/env python3
"""L1b — the DECLARED local-linear smoothing pass over the isotonic PVC steps.

Input : the adopted derived curve `pinned_d15_H10` (icbhpu 3c1d610f), picks 1-90 — isotonic
        (PAVA), pinned pick-1=3000, with flat plateaus (PAVA pooling artifacts: 6-9, 10-12,
        15-18, 32-40, 58-86).
Method: LOCAL-LINEAR (LOESS degree 1) in log-pick with tricube weights, bandwidth h (in log-pick
        units). Dissolves the flat plateaus into gentle declines WITHOUT erasing the genuine large
        concentrations (e.g. the -26% 5->6 the owner confirmed real, register v28 item 16 D1-ii).
        Then re-impose monotone non-increasing (cummin) and re-pin pick-1 = RL_PICK1 = 3000
        (presentation-only uniform rescale). Every deviation vs the raw isotonic is tabulated.
Output: out/pvc_curve_smoothed.json (chosen h), out/pvc_smoothing_deviation.csv, and it can emit
        the engine artifact. This module prints a bandwidth sweep for the choice; --emit finalizes.
"""
import csv, json, math, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.dirname(HERE)
SP   = "/tmp/claude-0/-home-user-afl-rl-engine/72def78e-fad9-5e00-8811-33840b8a19ea/scratchpad"

def load_iso():
    rows = list(csv.DictReader(open(os.path.join(SP, "derived_curve.csv"))))
    return {int(float(r["pick"])): float(r["pinned_d15_H10"]) for r in rows}

def loess_linear(picks, y, h):
    """degree-1 local regression in log-pick, tricube weights, bandwidth h (log units)."""
    x = [math.log(p) for p in picks]
    out = []
    for xi in x:
        # tricube weights within +/- h; points beyond h get 0
        ws = []
        for xj in x:
            d = abs(xj - xi) / h
            ws.append((1 - d**3)**3 if d < 1 else 0.0)
        sw  = sum(ws)
        swx = sum(w*xj for w, xj in zip(ws, x))
        swy = sum(w*yj for w, yj in zip(ws, y))
        swxx = sum(w*xj*xj for w, xj in zip(ws, x))
        swxy = sum(w*xj*yj for w, xj, yj in zip(ws, x, y))
        den = sw*swxx - swx*swx
        if abs(den) < 1e-12:
            out.append(swy/sw if sw else yj)
        else:
            b = (sw*swxy - swx*swy) / den      # slope
            a = (swy - b*swx) / sw             # intercept
            out.append(a + b*xi)
    return out

def monotone_pin(vals):
    """cummin (non-increasing), then uniform rescale so pick-1 == 3000."""
    m = list(vals)
    for i in range(1, len(m)):
        if m[i] > m[i-1]:
            m[i] = m[i-1]
    scale = 3000.0 / m[0]
    return [v*scale for v in m]

def diag(picks, isovals, sm, hi=50):
    """isovals/sm are value LISTS aligned to picks. Flat runs counted in the PRICED range picks<=hi
    (past ~KMAX the floor is legitimately flat and past the 30 displayed pick assets)."""
    d = dict(zip(picks, sm)); r = dict(zip(picks, isovals))
    def flat_run_maxlen(cur):
        best = cur_len = 1
        for i in range(1, len(picks)):
            if picks[i] > hi: break
            if abs(cur[picks[i]] - cur[picks[i-1]]) < 0.5:
                cur_len += 1; best = max(best, cur_len)
            else:
                cur_len = 1
        return best
    step56 = (r[5]-r[6])/r[5]*100, (d[5]-d[6])/d[5]*100      # genuine concentration, want preserved
    mono = all(d[picks[i]] <= d[picks[i-1]] + 1e-9 for i in range(1, len(picks)))
    return dict(iso_maxflat_le50=flat_run_maxlen(r), sm_maxflat_le50=flat_run_maxlen(d),
                step56_iso_pct=round(step56[0],1), step56_sm_pct=round(step56[1],1), monotone=mono)

def main():
    iso = load_iso()
    picks = sorted(iso)                       # 1..90
    y = [iso[p] for p in picks]
    if "--emit" not in sys.argv:
        print("bandwidth sweep (h in log-pick units); iso raw max-flat-run(<=50) = %d:"
              % diag(picks, y, y)["iso_maxflat_le50"])
        for h in [0.16, 0.18, 0.20, 0.22, 0.26]:
            sm = monotone_pin(loess_linear(picks, y, h))
            dg = diag(picks, y, sm)
            print(f"  h={h}: {dg}")
            if h in (0.18, 0.20):
                print("     picks 1-20:", [round(v) for v in sm[:20]])
                print("     picks 30-42:", [round(v) for v in sm[29:42]])
        return
    # FINALIZE at the chosen bandwidth: h=0.20 = lightest touch that cuts the priced-range max flat
    # run 9->2 while preserving the genuine 5->6 concentration (26.5%->25.8%) and monotonicity.
    H = 0.20
    sm = monotone_pin(loess_linear(picks, y, H))
    smi = [int(round(v)) for v in sm]
    # enforce int monotone after rounding
    for i in range(1, len(smi)):
        if smi[i] > smi[i-1]: smi[i] = smi[i-1]
    assert smi[0] == 3000, smi[0]
    assert all(smi[i] <= smi[i-1] for i in range(1, len(smi))), "G-MONO fail"
    curve = {p: v for p, v in zip(picks, smi)}
    # extend 91-99 flat at the pick-90 floor (past KMAX=70; schema parity with the 1-99 artifact)
    for p in range(91, 100):
        curve[p] = curve[90]
    # deviation table vs raw isotonic
    dev_path = os.path.join(SESS, "out", "pvc_smoothing_deviation.csv")
    with open(dev_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["pick", "raw_isotonic_d15_H10", "smoothed", "delta", "delta_pct"])
        for p in picks:
            raw = iso[p]; s = curve[p]
            w.writerow([p, round(raw,2), s, round(s-raw,2), round((s-raw)/raw*100,2)])
    json.dump({str(p): curve[p] for p in sorted(curve)},
              open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"), "w"), indent=0)
    dg = diag(picks, y, [curve[p] for p in picks])
    print("FINALIZED h=%.2f  monotone=%s  iso_maxflat(<=50)=%d -> sm_maxflat=%d  step5->6 %.1f%%->%.1f%%"
          % (H, dg["monotone"], dg["iso_maxflat_le50"], dg["sm_maxflat_le50"], dg["step56_iso_pct"], dg["step56_sm_pct"]))
    print("curve 1-20:", [curve[p] for p in range(1,21)])
    print("curve 30-45:", [curve[p] for p in range(30,46)])
    print("curve 58-70:", [curve[p] for p in range(58,71)])
    print("wrote:", dev_path, "and out/pvc_curve_smoothed.json")

if __name__ == "__main__":
    main()
