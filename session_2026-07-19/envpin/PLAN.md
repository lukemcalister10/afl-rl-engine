# ENV PIN — PLAN (commit #1) · item 392 · seat 15 · 2026-07-19

Base = F6 head `540b62f3c1600178aabc56f2dd1ab59c68460b2b` (PR #121), STRICT. Stack on #121. THREADS=1.
Mode auto, PLAN first. Effort High. FENCE: dependency lock + bootstrap + `session_2026-07-19/envpin/`
(+ one bootstrap touchpoint). HARD-OUT: store / curve / q97m / v0surf.pkl / rl_model.py / every board value.

## 1. DIAGNOSIS (the exact env delta)
- This container: CPython 3.12.3, **numpy 2.4.4**, wheel
  `numpy-2.4.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl`.
- The wheel **bundles its own OpenBLAS** at `numpy.libs/libscipy_openblas64_-32a4b2a6.so`
  (OpenBLAS 0.3.31, DYNAMIC_ARCH). So the runtime BLAS ships *inside* the numpy wheel.
- **`np.interp` is compiled C in the numpy wheel** (`numpy/_core`, `compiled_base.c` `arr_interp`); it does
  **not** call BLAS. Item 391 already cleared all linalg (polyfit/lstsq/solve/dot/matmul/svd) as
  non-amplifying and named `np.interp` as the lone value-path amplifier (25 calls in `_merged_recover.py`
  + ~13 other modules). Therefore the cross-build divergence rides in the **numpy WHEEL** (its compiled
  interp binary — compiler/SIMD/version), **not** the bundled BLAS.
- **Root cause (item 391): nothing in the repo pins the environment.** No requirements/constraints lock,
  no Dockerfile, no pyproject numpy/BLAS pin. Container-to-container numpy build variation is unconstrained,
  so a minority container runs a differently-compiled `np.interp` → a ≥ threshold interp divergence →
  the board flips off `06d8af60`, rank-unsafely (item 389/391).

## 2. THE PIN (smallest that works)
- **`requirements-lock.txt`** — hash-pinned wheels, `numpy==2.4.4 --hash=sha256:81f4a14b…` the
  determinism-critical line. Because the wheel bundles OpenBLAS, this ONE hash pins BOTH the compiled
  `np.interp` and the BLAS. The rest of the compiled stack (scipy 1.17.1, scikit-learn 1.8.0 + deps) is
  pinned for a fully reproducible env. Install is `--require-hashes --only-binary=:all:` so an sdist
  recompile (which would reintroduce the divergence) is forbidden.
- **`bootstrap_env.sh`** — one command, idempotent, offline-safe: verifies the pinned numpy + bundled
  OpenBLAS by sha256 and no-ops if already present; else hash-installs from the lock. Run at build start.
- **`bootstrap.sh`** — a fail-closed ENV-PIN assert (offline hash check) added near the top, mirroring
  Guard 5's store/q97m/v0surf asserts: HALT if the container is on an unpinned numpy.
- Escalation to a full container/image pin is NOT needed: the wheel-hash pin reproduces this container's
  numpy binary + BLAS **byte-for-byte** (proven — see wheel_verify).

## 3. PROOF STRATEGY
- **Mechanism (in-container):** monkeypatch `np.interp` to add a relative perturbation ε to every interp
  output (simulating a different wheel's last-ULP interp), build the balanced board, and show it **diverges**
  off `06d8af60` at ε above a measured threshold; ε=0 (the pinned wheel) **holds** `06d8af60`. Also attempt
  a REAL different build (numpy 2.3.5; forced no-FMA/AVX dispatch) — report honestly whether either flips.
- **Wheel-pin verification:** download the pinned wheel, confirm its sha256 == the lock and its bundled
  OpenBLAS == the installed `.so` byte-for-byte ⇒ the pin reproduces this numpy everywhere.
- **Confirm:** balanced board (`RL_LEGE=0 RL_LEGF=0`, THREADS=1, `PYTHONHASHSEED=0`, v0surf LOAD) ==
  `06d8af60` byte-exact, 5/5.
- **Value-neutral:** k=0 row-diff vs the standard clean board = 0; identity ×4
  (`1f10220c`/`06d8af60`/`d85901af`/`9829d01a`); store/curve/q97m/v0surf/rl_model UNTOUCHED.

## 4. THE ONE GATE (non-trimmable)
`06d8af60` byte-exact on ≥2 genuinely-different containers under the pin. THIS build proves **container #1
+ the mechanism**; **container #2 = the follow-on viewing render on the pinned env** (owner-fired, not this
build). If either diverges → HALT + pin deeper. Results in `EXIT_PROOF.md`.
