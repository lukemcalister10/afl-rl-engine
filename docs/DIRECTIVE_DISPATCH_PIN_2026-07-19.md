# DIRECTIVE — DISPATCH PIN · FORCE ONE ARITHMETIC PATH ON EVERY CPU · seat 14 · 2026-07-19
### The LAST layer. Item 394 proved the software is byte-identical across containers (pinned wheel +
### identical OpenBLAS .so) and the board STILL flips → the divergence is RUNTIME CPU DISPATCH: numpy
### ufuncs + OpenBLAS (both DYNAMIC_ARCH) select machine-code paths per CPU at import/run time. Force
### both layers to ONE fixed path via env, permanently, in bootstrap — so every container,今 and all
### season (the weekly loop included), computes the same bytes. Owner ruled A, 2026-07-19. This is
### PERMANENT INFRASTRUCTURE, not a viewing unblock: the pin + asserts ride into the v2.11 bake and
### every compute after it.

## ★ PRE-STATED OUTCOME LOGIC (item 395 — every branch lands useful; follow it exactly) ★
Build the balanced board UNDER THE FULL PIN, 5× consecutive, and record its md5:
- **(i) pinned board == `06d8af60`** → board of record preserved. Done: commit pin + proofs.
- **(ii) pinned board == a NEW md5, stable 5/5** → NOT a failure. Record the full pinned QUARTET
  (default / balanced / forward / RL_PVC2=0) — it becomes THE CANDIDATE reference set, sealed by the
  owner at the viewing (which renders the pinned board). Report the row-level diff vs `06d8af60`
  (expect near-tie scale, Sheezel-class ±95) — NAMED rows, so the owner sees exactly what shifted.
- **(iii) pinned board NOT stable 5/5 on this container** → the dispatch pin has FAILED. STOP — do not
  iterate, do not try a 4th pinning strategy (standing guardrail, item 394). Commit the evidence + HALT.

## THE JOB (PLAN FIRST — commit #1)
1. **HARDWARE FINGERPRINT (the gap item 395 named — from now on, always):** CPU model + flags
   (/proc/cpuinfo), `np.show_runtime()` / `__cpu_features__` (baseline + dispatched), effective
   OpenBLAS kernel (`OPENBLAS_VERBOSE=2` or corename API). Commit it. This is the standing spec for
   every determinism-relevant proof hereafter.
2. **DIGIT PROBE (see the moving op at last):** a tiny committed script printing full-precision
   samples of np.interp + the upstream ufunc/reduction chain that feeds it (star/recover/iso_corr
   inputs), run UNPINNED then PINNED. On any container where the two differ, the probe shows WHICH op
   moves and at what ULP. Cheap, decisive, committed either way.
3. **THE PIN:** extend `bootstrap_env.sh`/`bootstrap.sh` to EXPORT, permanently:
   `NPY_DISABLE_CPU_FEATURES` = every runtime-dispatched feature above numpy's compile baseline
   (enumerate empirically from np.show_runtime; the goal = the BASELINE path on every x86-64) ·
   `OPENBLAS_CORETYPE=HASWELL` (the build's own DYNAMIC_ARCH target per the banner; one fixed kernel)
   · threads already 1. EXTEND THE FAIL-CLOSED ASSERT: bootstrap must now verify AT RUNTIME that the
   dispatch actually matches the pin (query np.show_runtime + the BLAS corename and HALT on mismatch)
   — an env var that didn't take is a silent board mover, same disease as an unverified store.
4. **TOGGLE DEMONSTRATION (the in-container proof):** build the balanced board UNPINNED vs PINNED on
   this container. If the md5s DIFFER → dispatch-sensitivity is demonstrated live and the pin is
   proven to control the board. If they MATCH → this container's natural path == the pinned path;
   state it plainly (the cross-container proof then rests on the render's gate re-run) — do NOT
   overclaim.
5. **OUTCOME LOGIC** above → (i)/(ii)/(iii). Under (i)/(ii): 5/5 consecutive + the identity quartet
   under the pin + dormancy F3/F4/F5 PASS + untouched stamps (store 968de0c7 · curve 56dd7a7b · q97m
   cfdc7321 · v0surf 3af2b725 · rl_model cc626d7d · zero engine/store/value/docs edits — env + probe
   + proofs ONLY).
6. **THE GATE RE-RUN IS THE NEXT BUILD:** the viewing render (re-fired after this lands) runs under
   the pin on a DIFFERENT container and must reproduce THIS build's pinned md5 — that is the
   two-container gate for the dispatch pin. State the expected md5 in your RETURN so the render
   directive can pin to it.

## GIT ENTRY (item-338 law)
`git fetch origin main claude/env-pin-2026-07-19-4y4w0p`; ls-remote must return
`3055ea5ffdc390f81d5e17476a60fbb841f24cff` STRICT (the env-pin head, #123), HALT on mismatch. STACK on
#123 (branch parent = the env-pin branch). Run `bash bootstrap.sh` (current asserts) at entry. Balanced
board recipe: `RL_LEGE=0 RL_LEGF=0`, threads=1, PYTHONHASHSEED=0, v0surf LOAD. DO NOT touch or build
from fc7045d6 (deleted v0surf.pkl; do-not-merge) or the stale iso-corr branch.

## EFFORT: High (the risk is proving the pin GRIPS — the runtime-verified assert + the toggle demo —
not the env lines; a Medium-grade "exported the vars" is exactly how a silent non-grip ships). Why not
Extra: one file pair + probes, no value logic. MODE: auto, PLAN first. TIME: ~1.5–2.5 h (flag >2×/<½×).
## FENCE: IN = bootstrap.sh · bootstrap_env.sh · requirements-lock.txt (comment-only if needed) ·
session_2026-07-19/dispatchpin/. HARD-OUT: every engine/store/curve/value file + docs + v0surf.pkl —
this changes WHERE arithmetic runs, never a value; HALT on any HARD-OUT need. Outcome (ii)'s new md5s
are RECORDED IN PROOFS, never written into engine/docs (the supervisor re-pins the render directive).
## EXIT (RETURN ≤25 lines): outcome branch (i/ii/iii) FIRST + the pinned balanced md5 + the toggle-demo
result + the probe's verdict (which op moved, or "none moved here") + hardware fingerprint summary +
5/5 + quartet + untouched stamps; branch · head SHA · PR stacked on #123. SILENCE IS A RED ·
halt-not-warn · findings not verdicts.
