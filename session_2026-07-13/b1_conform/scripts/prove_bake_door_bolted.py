#!/usr/bin/env python3
"""RED-PATH PROOF A2 — THE BAKE DOOR IS BOLTED (owner-ruled Option B, 2026-07-13).

With SGC_B1_MATRIX set, runs the REAL suite in gate/bake mode (RL_CONFIG_MODE=gate, then =bake). The
config manifest's SGC_* scan must treat the seam variable as an unknown override and HALT on line one —
before the engine loads, before B1 ever reads the (here fabricated) matrix path. A bake that even smells
of an injected gate input dies immediately.

For each of gate and bake mode, asserts:
  * the suite process exits NON-ZERO,
  * the config manifest emits a NAMED reject for SGC_B1_MATRIX ("CONFIG MANIFEST ... REJECTED — BUILD
    HALTED" and "gate-seam override SGC_B1_MATRIX").

Exits 0 iff BOTH modes HALT at the config manifest with the seam variable named.
"""
import os, sys, subprocess

ROOT = '/home/user/afl-rl-engine'
FAKE_MATRIX = os.path.join(ROOT, 'session_2026-07-13/b1_conform/out', 'fabricated_bake_input.json')
OUT = os.path.join(ROOT, 'session_2026-07-13/b1_conform/out')
ENV_BASE = dict(os.environ, RL_REPO=ROOT, PYTHONHASHSEED='0',
                PATH='/root/rl_venv312/bin:' + os.environ.get('PATH', ''),
                SGC_REPORT_DIR='session_2026-07-13/b1_conform/out')

def run_mode(mode):
    # A real bake/gate sets RL_CONFIG_MODE in the AMBIENT environment. SGC_B1_MATRIX points at a fabricated
    # path — the manifest must HALT before it is ever read.
    env = dict(ENV_BASE, RL_CONFIG_MODE=mode, SGC_B1_MATRIX=FAKE_MATRIX)
    r = subprocess.run([sys.executable, 'ship_gates_check.py'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=300)
    blob = r.stdout + '\n===STDERR===\n' + r.stderr
    log = os.path.join(OUT, f'proof_bake_door_{mode}.log')
    open(log, 'w').write(blob)
    nonzero = r.returncode != 0
    named_reject = ('CONFIG MANIFEST' in blob and 'REJECTED' in blob and 'HALTED' in blob
                    and 'SGC_B1_MATRIX' in blob and 'gate-seam override' in blob)
    reject_line = next((ln for ln in blob.splitlines() if 'gate-seam override SGC_B1_MATRIX' in ln), '')
    print(f"\n--- {mode.upper()} mode (RL_CONFIG_MODE={mode}, SGC_B1_MATRIX set) ---")
    print(f"  exit={r.returncode}")
    print(f"  named reject: {reject_line.strip()[:220]}")
    print(f"  log: {log}")
    print(f"  exit!=0={nonzero}  config-manifest named-reject={named_reject}")
    return nonzero and named_reject

def main():
    # Fabricated matrix — deliberately NOT a valid book; the door must slam before it is read.
    open(FAKE_MATRIX, 'w').write('{"__meta__": "fabricated — a bake must never get this far"}\n')
    ok_gate = run_mode('gate')
    ok_bake = run_mode('bake')
    if os.path.exists(FAKE_MATRIX):
        os.remove(FAKE_MATRIX)
    ok = ok_gate and ok_bake
    print("\n=== A2 RESULT ===")
    print(f"  gate mode HALTs at config manifest, SGC_B1_MATRIX named : {ok_gate}")
    print(f"  bake mode HALTs at config manifest, SGC_B1_MATRIX named : {ok_bake}")
    print("VERDICT:", "A2 PROVEN — the bake door is bolted" if ok else "A2 FAILED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
