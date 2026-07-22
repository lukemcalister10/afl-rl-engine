# AUDIT SHARD — LEG-D ACT-2 (bounded, read-only, independent) — paste into a FRESH chat with repo access, outside the Project
You are a cold auditor. You have no history with this work and must not acquire any: **do NOT read
any file under `session_2026-07-17/legd_derivation/` whose name contains VERDICT, CHECKPOINT, PROOF,
or anything under its `out/` directory** — those carry the build's own reported numbers, and your
value is computing everything yourself. Report what YOU compute; discrepancies are findings, not
problems to resolve.

## INTEGRITY MANIFEST (addresses and pins only)
- Repo: https://github.com/lukemcalister10/afl-rl-engine.git (public; anonymous read-only git).
- AUDIT HEAD: branch `claude/legd-pvc-rederivation-act2-l2hqpl` — `git ls-remote` MUST show
  `e4177c21934148c19d9cec3c015fee5d28480102`; anything else: STOP and report.
- BASE: `33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7` (must be an ancestor of the audit head).
  CHECKPOINT: `12a076179525db21b6e30a37bfe16bb9d904ff47` (must also be an ancestor).
- STORE: `engine/rl_after/rl_model_data.json` md5 must begin `968de0c7` at BOTH the base and the
  audit head (byte-identical — assert with `git diff`).
- GATE DEFINITIONS (fetch, do not paraphrase): `docs/DIRECTIVE_LEGD_ACT2_refire_2026-07-17.md` and
  `docs/acceptance_v1_21.json` from `origin/main` (the acceptance file's md5 must begin `7c12d0d6`).

## THE CHECKS (run in order; ~1 engine load ≈ 60–120 s; two loads total)
1. **SCOPE.** `git diff --name-only 12a0761..e4177c2` — commit the full list in your report. For
   every file OUTSIDE `session_2026-07-17/…` and `data/…`, read the diff and state in one line each
   WHAT it does and how it is gated. Flag anything that writes the store, touches
   `rl_model.py`, or changes behaviour when its kill-switch is OFF.
2. **KILL-SWITCH BYTE-EXACTNESS.** At the audit head, build the board with `RL_PVC2=0`. Separately,
   determine the base board: build at `33c8b52` (or use the base tree's committed board artifact if
   the repo's standing practice commits one — state which you used). Compare md5s. VERDICT: byte-
   exact or not, with both md5s printed.
3. **THE CURVE, INDEPENDENTLY.** From `engine/rl_after/pvc_curve_v2.json` at the audit head, using
   your own arithmetic (not any in-repo report): (a) curve(1) == 3000? (b) strict descent
   curve(p+1) ≤ curve(p) − 1 for p = 1..79 — count violations. (c) print curve(10), curve(40),
   curve(80). (d) confirm the artifact's stamp names store `968de0c7`.
4. **THE POOLED IDENTITY, RE-COMPUTED.** With `RL_PVC2=1` at the audit head, run the frozen-suite
   harness that scores the pooled day-after identity (find it via `one_source_selftest.py`; use the
   FROZEN suite only — write no new measurement code beyond invocation). Report the pooled % YOU
   get and the verdict against the gate definition in the fetched directive. If the harness cannot
   be located or produces no verdict: that is a RED finding (silence is a red), not a skip.
5. **PRE-VIEW SEALS.** md5 of `session_2026-07-17/legd_derivation/MEMO_LEGD_construction.md` at the
   audit head must begin `abe387d9` (reading THIS file's hash is permitted; its content is not needed).

## RETURN FORMAT (≤25 lines)
One line per check: COMPUTED value(s) + PASS/FAIL/RED. Then: any file-scope concerns from check 1.
Then one plain-terms paragraph. Nothing else. Do not push, commit, or write to the repo — you are
read-only; local scratch only.
