#!/usr/bin/env python3
"""RED-PATH PROOF A2 — A B1 BOUND BREACH HALTS THE SUITE (exits non-zero).

Regenerates a CLEAN candidate matrix (valid __meta__), then DOCTORS a copy so the July-8 year-4
class-sum average exceeds 1.30 x den. Feeds the doctored matrix to the REAL ship_gates_check.py via
the SGC_B1_MATRIX seam (B2/B3/B4 skipped for speed — they are irrelevant to this proof) and asserts:
  * B1's verdict is HALT and its detail names the BREACH,
  * the suite process exits NON-ZERO.
A CONTROL run feeds the CLEAN (undoctored) matrix through the identical path and asserts B1 == INJECTED
(non-breaching; the seam stamps INJECTED, never a bare PASS, per the Option-B fail-close 2026-07-13) — so
the ONLY thing that flips B1 to HALT is the breach, not the harness.

Usage: prove_breach_halts.py [clean_matrix.json]   (regenerates one if not supplied)
Exits 0 iff the breach HALTs the suite and the control passes B1.
"""
import os, sys, json, shutil, subprocess, tempfile, hashlib, re

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OUT = os.path.join(ROOT, 'session_2026-07-13/b1_conform/out')
ENV_BASE = dict(os.environ, RL_REPO=ROOT, PYTHONHASHSEED='0',
                PYTHONPATH=RA + ':/home/claude/rl_vendor',
                PATH='/root/rl_venv312/bin:' + os.environ.get('PATH', ''),
                SGC_SKIP='B2,B3,B4', SGC_REPORT_DIR='session_2026-07-13/b1_conform/out')

def regen_clean():
    fd, mp = tempfile.mkstemp(prefix='s4_clean_', suffix='.json', dir=OUT); os.close(fd)
    env = dict(ENV_BASE, S4_MATRIX=mp, RL_CONFIG_MODE='gate')
    print("regenerating a clean candidate matrix (gate mode) ...", flush=True)
    r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env,
                       capture_output=True, text=True, timeout=1800)
    if not os.path.exists(mp) or json.load(open(mp)).get('__meta__') is None:
        print("clean regen FAILED", r.returncode, r.stderr[-1500:]); sys.exit(2)
    return mp

def doctor_breach(clean, out):
    """Inflate incurve 2004-2020 Vpath at career year N=4 (index 3) so y4 avg breaches 1.30 x den."""
    m = json.load(open(clean))
    n = 0
    for k, v in m.items():
        if k.startswith('__'):
            continue
        if v.get('incurve') and 2004 <= int(v['year']) <= 2020 and len(v.get('Vpath', [])) >= 4 and v['Vpath'][3] is not None:
            v['Vpath'][3] = float(v['Vpath'][3]) * 3.0    # 3x at N=4 -> ratio far above 1.30
            n += 1
    json.dump(m, open(out, 'w'))
    return n

def run_suite(matrix_path, tag):
    env = dict(ENV_BASE, SGC_B1_MATRIX=matrix_path)
    r = subprocess.run([sys.executable, 'ship_gates_check.py'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=900)
    log = os.path.join(OUT, f'proof_breach_{tag}.log')
    open(log, 'w').write(r.stdout + '\n===STDERR===\n' + r.stderr)
    b1 = next((ln for ln in r.stdout.splitlines() if re.match(r'\s*B1\b', ln)), '')
    return r.returncode, b1, r.stdout, log

def main():
    clean = sys.argv[1] if len(sys.argv) > 1 else regen_clean()
    print(f"clean matrix: {clean}  md5={hashlib.md5(open(clean,'rb').read()).hexdigest()[:8]}")
    doctored = os.path.join(OUT, 's4_breach_doctored.json')
    n = doctor_breach(clean, doctored)
    print(f"doctored a copy: 3x Vpath at N=4 for {n} incurve 2004-2020 records -> {doctored}")

    # CONTROL: clean matrix -> B1 PASS
    rc_c, b1_c, _, log_c = run_suite(clean, 'control')
    # BREACH: doctored matrix -> B1 HALT + suite non-zero
    rc_b, b1_b, out_b, log_b = run_suite(doctored, 'breach')

    print("\n--- CONTROL (clean matrix) ---")
    print(f"  exit={rc_c}  B1: {b1_c.strip()[:160]}")
    print(f"  log: {log_c}")
    print("--- BREACH (doctored matrix) ---")
    print(f"  exit={rc_b}  B1: {b1_b.strip()[:200]}")
    print(f"  log: {log_b}")

    # FAIL-CLOSE (Option B, 2026-07-13): a clean INJECTED matrix is stamped INJECTED, never a bare PASS
    # (the seam can no longer certify). The control still proves B1 did NOT breach — it is INJECTED, not HALT.
    ctrl_pass = ('INJECTED' in b1_c) and ('HALT' not in b1_c)
    breach_halt = ('HALT' in b1_b) and ('BREACH' in b1_b.upper())
    suite_nonzero = rc_b != 0
    ok = ctrl_pass and breach_halt and suite_nonzero
    print("\n=== A2 RESULT ===")
    print(f"  control B1 INJECTED (non-breach) on clean matrix ... {ctrl_pass}")
    print(f"  B1 HALT + BREACH on doctored matrix ..... {breach_halt}")
    print(f"  suite exits NON-ZERO on breach .......... {suite_nonzero} (exit={rc_b})")
    print("VERDICT:", "A2 PROVEN — a B1 breach HALTS the suite" if ok else "A2 FAILED")
    if clean.startswith(OUT) and len(sys.argv) <= 1 and os.path.exists(clean):
        try: os.remove(clean)
        except OSError: pass
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
