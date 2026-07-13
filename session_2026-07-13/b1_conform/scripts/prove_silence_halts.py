#!/usr/bin/env python3
"""RED-PATH PROOF A3 — SILENCE HALTS THE SUITE (the item-38 defect can no longer happen).

The item-38 failure: the cohort gate was invoked with no matrix, raised IndexError, PRINTED NOTHING
(swallowed behind `| tail -8`), the exit code was never checked, and the suite reported PASS. This proof
forces B1 to produce NO result and asserts the REAL suite HALTs, names B1, and exits NON-ZERO.

Two silence variants, both fed to the REAL ship_gates_check.py via the SGC_B1_MATRIX seam
(B2/B3/B4 skipped for speed — irrelevant to this proof):
  (i)  MISSING matrix  — SGC_B1_MATRIX points at a path that does not exist.
  (ii) UNREADABLE matrix — SGC_B1_MATRIX points at a non-JSON garbage file.
For each, asserts: B1 verdict == HALT, the suite prints a HALT/silent-gate line NAMING B1, and the
process exits NON-ZERO. A run in which B1 prints nothing and the suite says PASS would FAIL this proof.

Exits 0 iff BOTH silence variants HALT the suite with B1 named and a non-zero exit.
"""
import os, sys, re, subprocess, tempfile

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OUT = os.path.join(ROOT, 'session_2026-07-13/b1_conform/out')
ENV_BASE = dict(os.environ, RL_REPO=ROOT, PYTHONHASHSEED='0',
                PYTHONPATH=RA + ':/home/claude/rl_vendor',
                PATH='/root/rl_venv312/bin:' + os.environ.get('PATH', ''),
                SGC_SKIP='B2,B3,B4', SGC_REPORT_DIR='session_2026-07-13/b1_conform/out')

def run_suite(matrix_path, tag):
    env = dict(ENV_BASE, SGC_B1_MATRIX=matrix_path)
    r = subprocess.run([sys.executable, 'ship_gates_check.py'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=900)
    log = os.path.join(OUT, f'proof_silence_{tag}.log')
    open(log, 'w').write(r.stdout + '\n===STDERR===\n' + r.stderr)
    b1 = next((ln for ln in r.stdout.splitlines() if re.match(r'\s*B1\b', ln)), '')
    # the suite-level HALT / silent-gate line that names B1
    halt_line = next((ln for ln in r.stdout.splitlines()
                      if ('SUITE HALT' in ln or 'HALT' in ln) and 'B1' in ln), '')
    return r.returncode, b1, halt_line, r.stdout, log

def check(tag, matrix_path):
    rc, b1, halt_line, out, log = run_suite(matrix_path, tag)
    b1_halt = ('HALT' in b1)
    named = ('B1' in b1) or ('B1' in halt_line)
    nonzero = rc != 0
    # the exact defect guard: the suite must NOT report an all-green pass while B1 is silent
    not_false_pass = not (rc == 0)
    ok = b1_halt and named and nonzero and not_false_pass
    print(f"\n--- {tag} ---  (SGC_B1_MATRIX={matrix_path})")
    print(f"  exit={rc}")
    print(f"  B1 line: {b1.strip()[:200] or '(B1 PRINTED NOTHING — would be the item-38 defect)'}")
    print(f"  suite HALT line naming B1: {halt_line.strip()[:200]}")
    print(f"  B1==HALT={b1_halt}  B1 named={named}  exit!=0={nonzero}")
    print(f"  log: {log}")
    return ok

def main():
    missing = os.path.join(OUT, 'does_not_exist_ITEM38.json')
    if os.path.exists(missing):
        os.remove(missing)
    fd, garbage = tempfile.mkstemp(prefix='s4_garbage_', suffix='.json', dir=OUT); os.close(fd)
    open(garbage, 'w').write('this is not json {{{ broken — an unreadable matrix\n')

    ok_missing = check('missing_matrix', missing)
    ok_garbage = check('unreadable_matrix', garbage)

    os.remove(garbage)
    ok = ok_missing and ok_garbage
    print("\n=== A3 RESULT ===")
    print(f"  MISSING matrix    -> suite HALTs, B1 named, non-zero : {ok_missing}")
    print(f"  UNREADABLE matrix -> suite HALTs, B1 named, non-zero : {ok_garbage}")
    print("VERDICT:", "A3 PROVEN — SILENCE HALTS the suite (item-38 defect closed)" if ok else "A3 FAILED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
