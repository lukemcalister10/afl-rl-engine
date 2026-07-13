#!/usr/bin/env python3
"""Independent verification of the July-8 construction on a freshly regenerated matrix.

Regenerates the walk-forward matrix at the CURRENT head (s4_matrix_M1v7.py, gate mode) to a temp
path, then computes the OWNER-RULED July-8 construction (NOT the demoted indexed reading):

  population : incurve (type in {ND,RD}) AND draft class 2004..2020
  per class  : raw class-year SUM of Vpath at each career year N  (N=1 == end of calendar Yr1 = C+1)
  avg row    : UNWEIGHTED mean of those raw sums across classes observed at that N
  denominator: min(y1_avg, y2_avg)
  ratios     : y4/y5/y6 avg / denominator, each vs hard <= 1.30 (guide 1.20-1.25 advisory)

Prints the five class sums, the denominator, and the three ratios to 4dp, plus the matrix md5, so
they can be checked against acceptance A1 (69840.0/79298.2/88002.4/86652.9/80460.5; 1.2601/1.2407/1.1521).
"""
import os, sys, json, hashlib, subprocess, tempfile
import numpy as np

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'

def july8(mpath):
    m = json.load(open(mpath))
    S = {}                                   # S[(class, N)] = raw sum of Vpath over that class at year N
    for k, v in m.items():
        if k.startswith('__'):
            continue
        C = int(v['year'])
        if not v['incurve'] or not (2004 <= C <= 2020):
            continue
        for i, _ in enumerate(v['yrs']):
            N = i + 1
            if N > 7:
                break
            S[(C, N)] = S.get((C, N), 0.0) + float(v['Vpath'][i] or 0.0)
    classes = sorted({c for c, _ in S})
    # UNWEIGHTED average of raw class sums across classes observed at each N (NO yr1=100 renorm)
    AVGSUM = {N: float(np.mean([S[(C, N)] for C in classes if (C, N) in S]))
              for N in range(1, 8) if any((C, N) in S for C in classes)}
    return AVGSUM, classes, S

def main():
    md5 = hashlib.md5(open(os.path.join(RA, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]
    head = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
    print(f"store md5 (loaded): {md5}   engine head md5: {head}")
    fd, mpath = tempfile.mkstemp(prefix='s4_verify_', suffix='.json', dir=os.environ.get('TMPDIR', '/tmp'))
    os.close(fd)
    env = dict(os.environ, S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT,
               PYTHONPATH=f'{RA}:/home/claude/rl_vendor')
    print("regenerating matrix (gate mode) ...", flush=True)
    r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env,
                       capture_output=True, text=True, timeout=1800)
    if not os.path.exists(mpath) or os.path.getsize(mpath) == 0:
        print("MATRIX REGEN FAILED. exit", r.returncode)
        print(r.stderr[-2000:])
        sys.exit(2)
    mat_md5 = hashlib.md5(open(mpath, 'rb').read()).hexdigest()
    meta = json.load(open(mpath)).get('__meta__', {})
    print(f"matrix: {mpath}")
    print(f"matrix md5: {mat_md5}")
    print(f"matrix __meta__: engine={meta.get('engine_head_md5','?')[:8]} store={meta.get('store_md5','?')[:8]} n_players={meta.get('n_players')}")
    AVGSUM, classes, S = july8(mpath)
    den = min(AVGSUM[1], AVGSUM[2])
    den_src = 'y1' if AVGSUM[1] <= AVGSUM[2] else 'y2'
    print(f"\nclasses (2004-2020, incurve ND+RD): n={len(classes)} {classes}")
    print("class-year AVG-of-raw-sums per career year N:")
    for N in sorted(AVGSUM):
        print(f"  y{N} = {AVGSUM[N]:.4f}")
    print(f"\ndenominator = min(y1,y2) = {den_src} = {den:.4f}")
    print("ratios vs hard <= 1.30 (guide 1.20-1.25):")
    for N in (4, 5, 6):
        rr = AVGSUM[N] / den
        print(f"  y{N}: {rr:.4f}  {'PASS' if rr <= 1.30 else 'BREACH'}  (guide margin: {rr-1.25:+.4f} vs 1.25)")
    # 4dp acceptance check
    exp = {1: 69840.0, 2: 79298.2, 4: 88002.4, 5: 86652.9, 6: 80460.5}
    print("\nA1 4dp check (sum, |expected|):")
    allok = True
    for N, e in exp.items():
        got = round(AVGSUM[N], 1)
        ok = abs(got - e) < 0.05
        allok &= ok
        print(f"  y{N}: got {got} expect {e}  {'OK' if ok else 'MISMATCH'}")
    rexp = {4: 1.2601, 5: 1.2407, 6: 1.1521}
    for N, e in rexp.items():
        got = round(AVGSUM[N] / den, 4)
        ok = abs(got - e) < 5e-5
        allok &= ok
        print(f"  y{N} ratio: got {got} expect {e}  {'OK' if ok else 'MISMATCH'}")
    print("\nVERDICT:", "ALL MATCH" if allok else "MISMATCH — investigate")
    os.remove(mpath)

if __name__ == "__main__":
    main()
