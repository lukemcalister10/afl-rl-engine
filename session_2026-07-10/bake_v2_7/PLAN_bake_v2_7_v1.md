# PLAN — BAKE v2.7 EXECUTION (auto-mode first artifact) — v1 · 2026-07-10

_Job-scoped: the BAKE SEAT executes the bake mechanics against the CONFIRMED CANDIDATE. No tag, no
main, no value moves. Owner tags v2.7 + fast-forwards main after supervisor prescreen. Effort High,
MODE auto, TIME band 1–2h (confirmed; will flag if >2× or <½×)._

## SCOPE PIN (entry facts — VERIFIED, not re-derived)
- Candidate branch `claude/new-session-uc4i63`, head `2aee085fa8fbe8cd4593ca5e25bd65656c9013e5`
  (confirmed via `git ls-remote` full URL). Candidate = main `99941f1` (#56 merge) + 4 R-i flip commits;
  `99941f1` is an ancestor ⇒ fast-forward, no force-push.
- Working/push branch: **`claude/bake-v2-7-execution-qxmyoj`** (owner-confirmed 2026-07-10: bake seat on
  its own branch per the v2.6 precedent; the directive's `new-session-uc4i63` push target is superseded
  on this one point; a pointer comment goes on PR #57). Branch reset onto `2aee085` (verified ancestry).
- Identities asserted byte-exact on entry: store `a2fbc9a0` · engine head `7a07e369` · band(cm_400)
  `34faa865` · register `652d83e8` · config manifest `69ead79b944d…`. All match the directive.
- Expected reds EXACTLY `{A2, A3, A12}`. Book stable-sha re-seal TARGET (audit-computed) = `2a74c731…`.
- Rulings in force: R-i = advance (asserted) · RL_PVCFIT = 0 (asserted).

## STEPS (per-step commits, in order)
1. **Fresh bootstrap in BAKE MODE.** `RL_CONFIG_MODE=bake`; ambient model env cleared (config_manifest
   enforce — bake ≡ gate behaviour); `bootstrap.sh` seeds workspace + Guard-5 boot-store assertion (halt
   on mismatch); ruling-config gate green (R-i=advance + RL_PVCFIT=0) + config-manifest check.
2. **Full gate suite from the fresh bootstrap.** one_source_selftest (five single-source guards + F1/F2
   + collision sentry) + guard-4 correction canary + ship_gates (panel 10/10 + B1/B2/B4/B6/D14 + frozen
   A-gates). REQUIRED: reds EXACTLY `{A2, A3, A12}`; any other red ⇒ HALT + return the numbers.
3. **Regenerate board + book** from the bake-mode bootstrap. Assert B4 byte-agreement (regenerated ==
   shipped `e2c9bc51`). Recompute book stable-sha. **TRIPWIRE:** stable-sha ≠ `2a74c731…` ⇒ HALT + return
   both values (no seal on a fingerprint that disagrees with the blind audit).
4. **RE-SEAL** `data/book_stable_seal.json` at the recomputed (== `2a74c731…`) stable-sha; carry
   head/store/config identities; `sealed_by` cites "v2.7 bake, owner written word 2026-07-10, DECISIONS
   v90 §36 ladder (prescreen + 9/9 blind audit + owner viewing)".
5. **State strings → BAKED v2.7.** `data/expected_boot.json` tag → "BAKED v2.7 2026-07-10" (lineage …→
   4b08796c → 7a07e369; board/store/config identities); `START_HERE.md` masthead → BAKED v2.7 same
   identities; grep same-class strings and list them in the return. Guard-5 coherence: expected_boot
   changes ride the SAME commit as any identity they pin.
6. **Re-run the suite once more** on the final head (post-seal, post-strings): everything green, reds
   exactly `{A2, A3, A12}` (B3 now flips DIFFERS-BY-DESIGN → PASS at the new seal). CI green on the head.
7. **Push** `claude/bake-v2-7-execution-qxmyoj`. Final head = THE BAKE HEAD (stated unmissably). No tag;
   no main; no new PR; pointer comment on PR #57.

## OUT OF SCOPE (halt-if-hit)
No player value / lever / surface / data / config-semantics change — this job moves NO value (board
stays `e2c9bc51`; if any board value differs from the candidate's, HALT) · tags + main (owner-only) ·
frozen gate text/thresholds · docs pack · force-push · second copies of any data file (SSI binds).

## RETURN: build-reported until supervisor prescreen.
