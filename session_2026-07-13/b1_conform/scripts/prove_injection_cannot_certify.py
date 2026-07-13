#!/usr/bin/env python3
"""RED-PATH PROOF A1 — THE DOOR CANNOT GREEN-LIGHT (owner-ruled Option B, 2026-07-13).

Feeds the SGC_B1_MATRIX seam a CLEAN, valid, non-breaching, correct-meta candidate matrix — the exact
case that BEFORE the fail-close would have produced a clean B1 PASS and a zero-exit certification. Asserts
the seam can no longer certify:
  * the LOUD banner "INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION" is present in the output,
  * B1's verdict is stamped INJECTED (never a bare PASS),
  * the suite EXITS NON-ZERO despite the clean, valid, non-breaching matrix.
Run in dev-shell mode (no RL_CONFIG_MODE) — this is a PROOF, not a bake; B2/B3/B4 skipped for speed.

Exits 0 iff banner present AND B1==INJECTED (not PASS) AND the suite exits non-zero.
"""
import os, sys, json, subprocess, tempfile, hashlib, re

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OUT = os.path.join(ROOT, 'session_2026-07-13/b1_conform/out')
ENV_BASE = dict(os.environ, RL_REPO=ROOT, PYTHONHASHSEED='0',
                PYTHONPATH=RA + ':/home/claude/rl_vendor',
                PATH='/root/rl_venv312/bin:' + os.environ.get('PATH', ''),
                SGC_SKIP='B2,B3,B4', SGC_REPORT_DIR='session_2026-07-13/b1_conform/out')
BANNER = 'INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION'

def regen_clean():
    fd, mp = tempfile.mkstemp(prefix='s4_clean_A1_', suffix='.json', dir=OUT); os.close(fd)
    env = dict(ENV_BASE, S4_MATRIX=mp, RL_CONFIG_MODE='gate')
    print("regenerating a clean candidate matrix (gate mode) ...", flush=True)
    r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env,
                       capture_output=True, text=True, timeout=1800)
    if not os.path.exists(mp) or json.load(open(mp)).get('__meta__') is None:
        print("clean regen FAILED", r.returncode, r.stderr[-1500:]); sys.exit(2)
    return mp

def run_suite(matrix_path):
    # dev-shell (NO RL_CONFIG_MODE): the suite RUNS; the fail-close comes from B1=INJECTED + non-zero exit.
    env = dict(ENV_BASE, SGC_B1_MATRIX=matrix_path)
    r = subprocess.run([sys.executable, 'ship_gates_check.py'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=900)
    log = os.path.join(OUT, 'proof_injection_cannot_certify.log')
    open(log, 'w').write(r.stdout + '\n===STDERR===\n' + r.stderr)
    b1 = next((ln for ln in r.stdout.splitlines() if re.match(r'\s*B1\b', ln)), '')
    return r.returncode, b1, r.stdout, log

def main():
    clean = sys.argv[1] if len(sys.argv) > 1 else regen_clean()
    print(f"clean matrix: {clean}  md5={hashlib.md5(open(clean,'rb').read()).hexdigest()[:8]}")
    rc, b1, out, log = run_suite(clean)

    banner_present = out.count(BANNER) >= 2            # banner tops AND tails the board
    # The board prints three columns: CONTROL | PREVIOUS | CURRENT. The historical CONTROL/PREVIOUS columns
    # legitimately read PASS (that is what B1 scored before the fail-close); the CURRENT verdict is what the
    # seam produces now. Parse the CURRENT column (after the 2nd '|') and require it is INJECTED, not PASS.
    _cols = b1.split('|')
    current = _cols[2].strip() if len(_cols) >= 3 else b1.strip()
    b1_injected = current.startswith('INJECTED')
    b1_not_bare_pass = not current.startswith('PASS')
    suite_nonzero = rc != 0
    ok = banner_present and b1_injected and b1_not_bare_pass and suite_nonzero

    print("\n--- INJECTED (clean, valid, non-breaching matrix) ---")
    print(f"  exit={rc}")
    print(f"  B1: {b1.strip()[:200]}")
    print(f"  banner occurrences (top+bottom expected>=2): {out.count(BANNER)}")
    print(f"  log: {log}")
    print("\n=== A1 RESULT ===")
    print(f"  banner 'NOT A CERTIFICATION' present ......... {banner_present}")
    print(f"  B1 stamped INJECTED (never a bare PASS) ...... {b1_injected and b1_not_bare_pass}")
    print(f"  suite EXITS NON-ZERO on clean matrix ......... {suite_nonzero} (exit={rc})")
    print("VERDICT:", "A1 PROVEN — the seam CANNOT green-light a clean matrix" if ok else "A1 FAILED")
    if clean.startswith(OUT) and len(sys.argv) <= 1 and os.path.exists(clean):
        try: os.remove(clean)
        except OSError: pass
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
