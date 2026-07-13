"""G-COHORT — the July-8 BINDING construction (class-SUM reading) from an s4 matrix.
For each incurve draft class 2004-2020: SUM Vpath at depth N; figure(N)=mean across classes observed at N;
ratio(N)=figure(N)/min(figure(1),figure(2)); y4/y5/y6 hard bound 1.30. This is the reading that yields the
ratified 1.2601/1.2407/1.1521 (NOT the demoted per-class-indexed 126.8 reading)."""
import sys, json
import numpy as np

def classsum(mpath):
    m = json.load(open(mpath)); S = {}
    for k, v in m.items():
        if k.startswith("__"): continue
        C = int(v["year"])
        if not v["incurve"] or not (2004 <= C <= 2020): continue
        for i, _ in enumerate(v["yrs"]):
            N = i + 1
            if N > 7: break
            S[(C, N)] = S.get((C, N), 0.0) + float(v["Vpath"][i] or 0.0)
    co = sorted({c for c, _ in S})
    figure = {N: float(np.mean([S[(C, N)] for C in co if (C, N) in S]))
              for N in range(1, 8) if any((C, N) in S for C in co)}
    denom = min(figure[1], figure[2]); denom_leg = "year_1" if figure[1] <= figure[2] else "year_2"
    ratios = {N: figure[N] / denom for N in figure}
    return dict(cohorts=co, n_cohorts=len(co),
                figure={N: round(figure[N], 1) for N in figure},
                denom=round(denom, 1), denom_leg=denom_leg,
                y4=round(ratios[4], 4), y5=round(ratios[5], 4), y6=round(ratios[6], 4),
                breach={N: ratios[N] > 1.30 for N in (4, 5, 6)}, any_breach=any(ratios[N] > 1.30 for N in (4, 5, 6)))

if __name__ == "__main__":
    r = classsum(sys.argv[1])
    print(f"=== G-COHORT class-SUM (July-8 binding) | {sys.argv[1]} ===")
    print(f"  cohorts n={r['n_cohorts']} {r['cohorts']}")
    print(f"  figure (mean class-sum) by depth: {r['figure']}")
    print(f"  denom=min(y1,y2)={r['denom']} ({r['denom_leg']})")
    print(f"  y4={r['y4']}  y5={r['y5']}  y6={r['y6']}  (hard 1.30)")
    print(f"  breach: {r['breach']}  any={r['any_breach']}")
