# PLAN — R-i FLIP TO ADVANCE (bake-candidate finalisation) — v1 · 2026-07-10

Auto-mode first artifact (DIRECTIVE §2). Job charter = DECISIONS v90 §36; FEED = acceptance_v1_6.json ·
CONSTRAINTS_v1_6.md · DECISIONS_v90. Effort MEDIUM, time band 0.5–1.5h (confirmed; will report actual).

## BASE (fetched fresh, DIRECTIVE §Preamble + §31)
- `git fetch origin main claude/new-session-uc4i63` (fresh). Cited SHAs:
  - **origin/main = `00d82dde`** (v2.5/rev115 era, 2026-07-06) — the owner has NOT fast-forwarded main to
    the #56 merge (owner-only promote step, OUT OF SCOPE). `00d82dde` is an ANCESTOR of the #56 merge.
  - **#56 merge = `99941f1`** (= my HEAD = head of branch `claude/new-session-uc4i63`). This carries the
    injury chapter + the clean R-i toggle. It is my base — exactly what §4 means by "was 99941f1 = the
    #56 merge at issue time". The R-i toggle exists ONLY here, not in live main.
- Store `a2fbc9a0` verified UNCHANGED at base; register `652d83e8`; band `34faa865`.

## THE TOGGLE (verified CLEAN — DIRECTIVE §5 gate)
`engine/rl_after/_merged_recover.py:46` → `_LTI_CLOCK=os.environ.get('RL_LTI_CLOCK','pause')`.
Single env var, single behavioural use at line 552 (`if _LTI_CLOCK=='advance' and _AVAIL_ON and Y>=2026`).
A flip is a one-string default change + config assertion + regeneration — NOT a rebuild. Clean → proceed.

## EXPECTED MOVERS (from the #56 R-i table; I re-derive to the digit under the flipped default)
advance − pause, board ev(2026): O'Farrell −206 · Faull −72 · Carroll −32 · Gibcus −17 · Sinn −10 ·
D.Jones −3 · N.Long −2 · O.Lord −1 · T.Pink −1. Darcy/Motlop/Flanders past G0 → Δ0 (ceiling untouched).

## STEPS (per-task commits → ONE candidate PR)
1. **Flip + assertion** (commit 1):
   - `_merged_recover.py:46` default `'pause'` → `'advance'`; update the two toggle comment blocks so
     ADVANCE reads as the ruled default and pause as the retired provisional.
   - `data/model_config.json`: add `"RL_LTI_CLOCK": "advance"` to `vars` (+ var_note); re-stamp
     `config_sha256` to the recomputed canonical hash (rides artifact identity — §5).
   - `data/expected_boot.json`: update `config` pin to the new manifest hash; re-stamp `engine_head`
     (restamp_head.py); update `board`; refresh `tag` to note R-i=advance is the code default.
   - `ruling_config_check.py`: NEW R-i assertion family (same shape as RL_PVCFIT=0):
     (R-i-a) engine default RL_LTI_CLOCK resolves to `advance`; (R-i-b) live env RL_LTI_CLOCK unset or
     `advance` — a bake/gate run with the clock PAUSED fails loudly; (R-i-c) manifest carries
     `RL_LTI_CLOCK=advance`. Any of these paused → FAIL (non-zero), never warn.
2. **Regeneration** (commit 2): rebuild the candidate board (gate mode = advance) into `data/rl_build`;
   regenerate the R-i comparison table; write the mover list + pause→advance deltas to the digit.
3. **Proofs** (commit 3): pause-vs-advance board parity (ONLY the R-i register names move vs the merged
   head `99941f1`, byte-level for everyone else) · full suite green from a fresh bootstrap (five guards +
   sentry + panel + B-gates + ruling-config incl. the NEW assertion + config manifest) · reds exactly
   {A2, A3, A12} · store md5 UNCHANGED `a2fbc9a0`.

## PROOFS / DEFINITION OF DONE (DIRECTIVE §5)
- Movers vs merged head = the R-i register names only; byte parity elsewhere.
- Full suite green (fresh bootstrap); reds exactly {A2, A3, A12}; panel 10/10.
- Ruling-config: a paused clock now FAILS the gate loudly (demonstrated).
- store md5 UNCHANGED `a2fbc9a0`; CI green on the head.
- Head SHA = the AUDIT-PINNED bake candidate, stated unmissably in the return.

## OUT OF SCOPE (held)
Any other value/lever/surface/config · the store + every data file byte-identical · frozen gate
text/tolerances · docs pack · bake/tag/main actions (owner-only) · force-push.
