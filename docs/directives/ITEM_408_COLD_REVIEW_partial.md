ITEM 408 — COLD BLIND REVIEW (partial)

Candidate: a2c27471d5eabe3c268099346b1ba021a4a89c3d · branch claude/item-408-fixture-repair-e2o53i
Seat: cold, review-only. No writes, no merges, no pushes performed. Repo working tree left clean; all adversarial testing done on a detached scratch copy.

Standing caveat: I hit the tool-use limit mid-review. Several planned verifications did not complete. The verdict below reflects that, and I have marked every unverified item explicitly rather than inferring it from the claims note.

Provenance assertion (phantom-repo protocol)

Repo, branch, and SHA are real and independently asserted: git cat-file -t a2c2747 → commit; origin/claude/item-408-fixture-repair-e2o53i resolves exactly to a2c2747; candidate is not an ancestor of main (not yet merged); 83ed3bb is an ancestor (R3 lineage holds); origin/ci/r19-provenance-migration (at 1606d134) is an ancestor. main has advanced 30+ commits since the merge base, all register-only, docs-only pen.

FINDINGS

1 — Protected-artifact fence: HELD. [verified, severity: none]
Base 83ed3bb → candidate a2c2747, blob-identical on every frozen artifact, and md5s recomputed from candidate bytes match the claimed values exactly: store f37d9716, board of record 6f07f7cb, curve 56dd7a7b, curve contract 676ad2b7, per_entrant 40d7da7c, score ledger 1d9faae5, plus model_config.json and season_state.json. docs/OPEN_ITEMS_REGISTER.md, docs/RULEBOOK.md and docs/acceptance_v2_0.json are byte-untouched — the supervisor pen and Law-10 fences held.

2 — Negative controls fire on the REAL keys. [verified live, severity: none]
Re-ran ui/tests/club_curve_provenance.test.py in a reconstructed pinned env (py 3.12.3 / numpy 2.4.4 / scipy 1.17.1 / sklearn 1.8.0 / openpyxl 3.1.5 — matches the pin spec). 35/35 pass, all 18 fail-closed controls rc=2 with guard-specific reasons. The three regressed controls are genuinely restored onto live keys: CASE3b halts on curve_source_store_md5 (binds store 968de0c7 != release store deadbeef), CASE5a on live round enforcement (bundle R18 != current release R19), CASE5b on manifest completeness (lacks … ['as_of_round']). CASE1's re-aim is real — the stamp is compared to the manifest-derived board/round/release (6f07f7cb / R19 / v2.11-final-rc1-PROVISIONAL), no hardcoded 2ab73a6f / R14. Directive step 2 and item-5(a) are satisfied on evidence, not assertion.

3 — Item-5 sidecar is genuinely DERIVED, not a second authored source. [verified adversarially, severity: none]
This was the pre-flagged centrepiece and it survives scrutiny.

Every field in sibling_repin_state.json reproduces from an independent artifact: balanced pin vs expected_boot and release_contract.identities; source_store_md5 vs a recomputed md5 of the store; contract_sha256 vs the contract's own seal; active/total/Sheezel vs reference_vector_1373e824.json (804 / 760253 / 9542 — all match).
Grep of the entire tree shows no consumer treats it as authority. sidecar_doc() derives from the freshly-built sibling; the only read (sc_live) is a drift comparand against desired values derived from that build.
Adversarial control A: tampered the sidecar's balanced_board_md5 → verify returns ok:false, fails: ["sidecar balanced_board_md5 != expected_boot"], exit 1; check exit 2. Critically it still reported the true 1373e824 — it did not adopt the tampered value. That is the SSI property the flag demanded.

4 — The two-gate design is real and honestly described. [verified adversarially, severity: none]
check --full rebuilt the sibling from the R19 store in 84s and reproduced 1373e824 exactly — an independent reconstruction of the STOP-1 pin. I then injected the sum-preserving corruption the claims note describes (aaron-cadman +1 / aaron-naughton −1, sum held at 760253): the no-build verify passes (exactly as §6.b states it must) and check --full fails, exit 2, naming EXACT-VECTOR MISMATCH … at 2 key(s). The claims note does not overstate ordinary coherence as build-and-compare — a distinction it could easily have blurred and didn't.

5 — Single-transaction architecture confirmed by code read. [verified statically, severity: none]
_stage_sibling is invoked at step (c3), before _validate_staged (e), _collect_staged (f), _backup_originals (g), _commit. SIBLING_STAGED is journaled before COMMIT_BEGIN — no externally-committed stale-sibling interval. The mandatory-target invariant raises MANDATORY TARGET MISSING before commit before backup or commit, and asserts collected set == declared manifest set exactly; _commit journals COMMIT_VERIFIED. The withdrawn two-step framing is correctly superseded.

6 — CI-never-commits rule: HELD. [verified, severity: none]
Workflow scan across all four files at the candidate finds no permissions:, no GITHUB_TOKEN, no secrets., no git commit/push, no create-pull-request action. The only matches are two actions/upload-artifact steps, both present at base 83ed3bb — pre-existing, not introduced.

7 — Workflows are NOT at byte parity with 83ed3bb. [verified; disclosed; severity: LOW — note]
Register v386 recorded workflow byte-parity at 1606d134; that no longer holds at the candidate. final-integration.yml (+30/−12) and live-scoring.yml (+9) changed. I read the full diff: all changes are read-only and each is disclosed (§7.3 fetch-depth:0; §12.6 step-17 rename; §8.1 season-state oracle). The FI change is behavioural, not cosmetic — the R14 season-state assertion now derives from git show 93bd01af:… (the R14 anchor store, 0.58/0.545) and additionally asserts the current R19 store derives 0.79/0.727. That is a strengthening, not a loosening. Flagged only because "workflows change only as deliberate reviewed work" (v382) makes this reviewable surface, and the register header still carries the older byte-parity language.

8 — Commit 044a34e (declared deviation) is clean. [verified, severity: none]
Two files, +75/−0: ui/styles/matchday.css (+10, one @media(max-width:360px) block) and the claims note (+65). No board data, no test file, no assertion touched. The rule is name-generic (no Nasiah special-case, no <wbr>), keeps the full name, scoped to ≤360px, placed after the 560px block so it wins by source order. Assertion count stays 72 — the existing real-board first-five-name assertion remains the regression guard, so the fix was made to the product, not the ruler. This is the correct shape for an acceptance repair.

9 — Claims-note staleness. [verified, severity: LOW — note]
The note header still reads **Branch:** ci/r19-provenance-migration, contradicting the actual branch of record — disclosed in §7.0/§8.5 and acknowledged in register v419 ("stale branch name ignored"), but it is the first line a reader sees. Separately, §7.5 row 5 records movers.test.js 47 PASS while §8.3, §9.4, §12.9 and the commit message all record 62/62 — §7.5 is an earlier-state table that was not re-stamped. Both are presentational, not substantive; neither is load-bearing on any gate.

10 — 2e49963 discrepancy stands unresolved. [verified, severity: LOW — carry]
The claims note (§3) correctly reports that the directive's cited commit 2e49963 does not exist in the repository, and attributes the STAMP assertion to 15a9abd by git log -S / blame. The candidate handled this correctly — reported, not silently reconciled. It remains open for supervisor adjudication and should not be lost at merge.

NOT VERIFIED — work I did not reach

I want to be exact about what I did not confirm, because the difference between "verified" and "claimed" is the whole point of this seat:

The four-suite CI green on a2c2747 is only 3/4 independently confirmed. Via the Actions API I confirmed on the exact candidate SHA, event=push, branch correct: CI Guards 30066612174 success, Final Integration 30066612219 success, FV Provenance 30066612186 success. Live Scoring 30066612171 I could not confirm — GitHub rate-limited the unauthenticated request. Register v419 asserts it success; I did not independently see it.
Issue #147 (the formal hand-back) — not read. Rate-limited.
Item-5 proof harnesses — started, not collected. staged_sibling_integration_proof.py (claimed 60/60) and sibling_repin_proof.py (claimed 26/26) were launched in the background; I hit the limit before reading their logs. advance_chain_proof.py (claimed 15/15) not started.
Not run: invariant_proof.py (33/33), build_final_board.py / the §12 clean-room migration (10/10), acceptance_matrix.py, season_progress_test.py (25/25), extract_seam.test.py (42/42), movers.test.js (62/62), test_movers_transition.py (25/25), responsive_layout.test.mjs (72/72), prescreen.sh.
§12 forward-lens deferral — read, not adjudicated. §8.2 and §12 are candid that the DEFERRED treatment is a builder judgment the owner declined to rule on, and §8.2 states plainly that a supervisor preferring a hard blocker "would leave Final Integration RED and this candidate NOT ready." That is an owner/supervisor call, not a reviewer's, and I have not seen an owner word ratifying it. The self-flagging is to the candidate's credit; the gap is real.
§9 movers provenance bridge — the twelve properties and ten negative controls are read but unexecuted.
VERDICT
BLOCKED — pending completion of verification, not on defect found

To be precise about what this verdict means, because it is not an adverse finding on the work:

Everything I was able to re-run, passed, and the two deepest pre-flagged risks came back clean. The sidecar is derived, not a second source. The pin reproduces from the store by genuine build-and-compare. The negative controls fire on real keys. The protected fence held byte-for-byte. 044a34e fixed the product rather than the ruler. On the evidence I gathered, the substance of this candidate looks sound, and the claims note is unusually honest — it distinguishes its two gates rather than blurring them, withdraws its own superseded verdicts, and flags its own judgment calls as judgments.

But the acceptance bar in the directive is "four suites green, zero waivers" and the seam pattern requires one blind review. A review that verified 3 of 4 suites and none of the item-5 proof harnesses is not that review. I will not convert "consistent with everything I checked" into CLEAR — that is precisely the two-chats-agreeing failure the register warns against, and I would be the third seat doing it.

To clear this, a continuing cold seat needs to close exactly five things: (1) Live Scoring run 30066612171 confirmed success on a2c2747 via an authenticated API call; (2) issue #147 read and its enumerated deviations reconciled against the branch; (3) the three item-5 proof harnesses re-run and their counts confirmed; (4) the §12 clean-room build_final_board.py re-run to confirm overall_ok=True and that ok_present genuinely gates against the committed reference vector rather than the rebuilt board; (5) an explicit supervisor or owner ratification of the forward-lens DEFERRED treatment — because if that is ruled a hard blocker, Final Integration is RED and nothing else matters.

Findings 7, 9 and 10 are notes, not blockers — they should ride to merge as recorded carries, not gate it.

No writes, no merges, no ref moves were made by this seat.