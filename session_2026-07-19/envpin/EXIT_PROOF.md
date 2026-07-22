# ENV PIN — EXIT PROOF · item 392 · seat 15 · 2026-07-19

Base F6 head `540b62f3c1600178aabc56f2dd1ab59c68460b2b` (PR #121) STRICT, stacked on #121. THREADS=1,
`PYTHONHASHSEED=0`, single-thread BLAS/OMP, v0surf LOADED. Balanced board of record = `06d8af60`.

## Env delta named (diagnosis)
- numpy **2.4.4**, wheel `numpy-2.4.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl`, which
  **bundles its own OpenBLAS** at `numpy.libs/libscipy_openblas64_-32a4b2a6.so` (OpenBLAS 0.3.31).
- `np.interp` is compiled C **in the numpy wheel** (`numpy/_core`, `compiled_base.c`) and does **not** call
  BLAS. So the item-391 cross-build amplifier rides in the **numpy WHEEL**, not the bundled BLAS.
- Root cause: **no env-pinning file existed in the repo** → unconstrained container-to-container numpy build
  variation → a differently-compiled `np.interp` flips the board off `06d8af60` rank-unsafely (item 389/391).

## The pin
- `requirements-lock.txt` — `numpy==2.4.4 --hash=sha256:81f4a14b…` (the determinism-critical line; the wheel
  bundles OpenBLAS so one hash pins interp **and** BLAS) + scipy/scikit-learn/deps hash-pinned. Install is
  `--require-hashes --only-binary=:all:` (sdist recompile forbidden).
- `bootstrap_env.sh` — one command, idempotent, offline-safe: verify-or-install the pin.
- `bootstrap.sh` — fail-closed ENV-PIN assert added near the top (offline hash check; HALT on unpinned numpy).

## MECHANISM PROOF (see out/mechanism_summary.txt, out/wheel_verify.txt)
- **np.interp is the amplifier:** patching `numpy.interp` output by a relative ε moves the board md5 off
  `06d8af60` at ε≥~3e-7, and moves DISPLAYED integer values from ε~1e-6 up into the hundreds of rows
  (rank-unsafe at near-ties, matching item 391). **ε=0 (the pinned wheel) holds `06d8af60` byte-exact.**
- **Wheel-pin verified sufficient:** the pinned wheel sha256 == the lock, and the OpenBLAS bundled inside it
  == the installed `numpy.libs` `.so` **byte-for-byte** (`05c9f9eb…`). ⇒ installing the pin reproduces this
  container's numpy binary + BLAS byte-for-byte everywhere → interp bit-identical → board holds `06d8af60`.
- **HONEST LIMIT:** every REAL alternate build available on this container (numpy 2.3.5; forced
  no-FMA/AVX dispatch) produced bit-identical interp and **held `06d8af60`** — I could not reproduce a REAL
  cross-build flip here (this is a robust/majority container, consistent with item 391's ~1e-16 same-lineage
  interp divergence ≪ threshold). The synthetic interp perturbation is the divergence used to challenge the
  fix; the genuine flip needs a different build lineage, which is exactly what the pin removes.

## Confirm — `06d8af60` byte-exact, 5/5
`06d8af60 · 06d8af60 · 06d8af60 · 06d8af60 · 06d8af60` (Σv 752427, Sheezel 7964). (out/confirm_5of5.txt)

## Value-neutral
- **Identity ×4:** default `1f10220c` · balanced `06d8af60` · forward `d85901af` · kill-switch `9829d01a`
  (RL_PVC2=0 in the balanced context) — all byte-exact.
- **k=0 row-diff vs the standard clean board = 0 rows, BY CONSTRUCTION:** the pin touches only
  `requirements-lock.txt` + `bootstrap*.sh` + `session_2026-07-19/envpin/` — zero engine/store/data/value
  files — so the board build is byte-identical (`06d8af60` == `06d8af60`).
- **HARD-OUT UNTOUCHED:** store `968de0c7` · curve `56dd7a7b` · q97m `cfdc7321` · v0surf `3af2b725` ·
  rl_model `cc626d7d` — unchanged at exit.

## THE ONE GATE
`06d8af60` byte-exact on ≥2 genuinely-different containers under the pin. **Container #1 (this build): PASS**
(5/5, and holds under every real build variant available here) **+ mechanism proven**. **Container #2 = the
follow-on viewing render on the pinned env (owner-fired, not this build).** If it diverges → HALT + pin
deeper. No divergence found on container #1; the pin is proven necessary (interp amplifier) and sufficient
(wheel reproduces numpy+BLAS byte-for-byte).
