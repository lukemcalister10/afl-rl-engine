# BAKE v2.7 — gate suite verdict (from the fresh BAKE-mode bootstrap, PRE-RESEAL) · 2026-07-10

Candidate head `2aee085` · engine `7a07e369` · store `a2fbc9a0` · band `34faa865` · register `652d83e8`
· config `69ead79b944d…` · board `e2c9bc51`. All entry identities asserted byte-exact (Guard 5 PASS).

## Bootstrap + config gates (BAKE mode)
- boot-store guard (Guard 5): **PASS** — store a2fbc9a0 == pinned.
- config-manifest CHECK: **PASS** (hash 69ead79b944d; 40 vars; pin+stored consistent).
- ruling-config: **PASS** — RL_PVCFIT=0 (engine+env) + R3 export bake-guard active; RL_LTI_CLOCK=advance
  (engine default + env + manifest pin, owner ruling R-i).

## Single-source + canary
- one_source_selftest: **PASS** — single source; guards 1-3; F1 board==engine; F2 book==board;
  Kako+Bontempelli ground-truth; DPP blend stripped; collision sentry (King pair) clean.
- guard_correction_canary (Guard 4): **PASS** — a source correction sticks all the way to board + book.

## Regeneration (bake mode)
- board rl_app_data.json regenerated md5 = **e2c9bc51 == shipped e2c9bc51** (B4 byte-agree; no value moved).
- book s4_matrix stable-sha = **2a74c731e9ce603ecfa29aefbb6e3756a3fd886bbaaca55e8eb03033812d2c66**
  (2649 players) == the blind audit's `2a74c731…` (TRIPWIRE PASS).

## ship_gates_check.py — VERDICT (600s)
`DIFFERS-BY-DESIGN=1  FAIL=3  FEATURE=1  PASS=16  PENDING=4  STRUCK=1`
- **reds (CURRENT column) EXACTLY {A2, A3, A12}** — the three frozen data-caused gates; no other red.
  - A2 Curtis≥0.90×Ward 0.821 (UNCHANGED at 0.90 by owner ruling D7).
  - A3 [DC] Rozee 0.54 (out for 2026; AMENDED 0.80→0.75, knife-edge by design).
  - A12 [DC] Travaglia>Moraes / Smillie>Retschko.
- B1 PASS (AVG peak 130, path_ok). B2 PASS (leakage 0.000). B4 CURRENT PASS (e2c9bc51 byte-agree; the
  lone other "FAIL" string is B4's PREVIOUS column vs the prior candidate — CURRENT is PASS). B6 PASS.
  D14a/b/c PASS. B5 FEATURE. B3 DIFFERS-BY-DESIGN (candidate 2a74c731 vs sealed ff6cf9d8 — re-seal at
  the bake, next step). PVC stages PENDING (not run, expected). Convexity STRUCK (V_NEXT).
- panel: **PASS 10/10** (Guard 5 clean; store a2fbc9a0).

VERDICT: candidate reproduces the audit fingerprint byte-for-byte; reds exactly {A2, A3, A12}. Cleared
to re-seal + stamp state strings.
