# #306 — THE FULL REHEARSAL HAND-BACK · seat `u8ir65` · 2026-08-05

Assembled on the seam's clearance ([#306 comment 5189242005](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5189242005)).
**L1–L8 are complete.** This is the rehearsal record the seam verifies before the owner's EXECUTION
word. **Bake HELD; EXECUTION word WITHHELD; nothing lands.** The substrate stays uncommitted under R-C.

The landing pair, fixed once here and referenced throughout:
```
adopted curve   payload FULL 01f27f0231929b285de83aaa6713048d   [:8] 01f27f02
converged surf  ebc3d3303a1956a8ec94b4e2c1497bdf                [:8] ebc3d330
store 81d24704 · engine 15525b03 · band 34faa865 · sealed history release_lineage 6925d4b5 (untouched)
```

---

## 1 · THE RUNBOOK — PER LEG

L1–L5 were run by the #290 rehearsal seats (d7bnaa / zlaarm); their evidence stands and is cited, not
re-derived. L6 passes 0–1 were run by seat `2a1xa4`; L6 passes 2–3, the closure, and L7–L8 by this seat
`u8ir65`. Every leg ran strictly serial behind `tools/preboot_assert.sh`, on a box N35-classified from
the pure pass-0 substrate before any fit act.

| leg | what it did | key instrument | substrate / capture | evidence |
|---|---|---|---|---|
| L1 | first lawful in-repo build (player stack) | — | #290 line | `rehearsal_290…/L1_amended` |
| L2 | year-zero window measure | `l2_window_measure.py` | v0surf frozen `84fb0cde` | `L2_window/` |
| L3 | S-1/S-2 carry, T1 bias-1, watched number | `carry_verify.sh` | `79ee8e5` base (N18) | `L3_*` |
| L4 | first ruled in-repo build | — | control rebuilt | `L4_build/L4_BUILD.md` |
| L5 | dial census + dockets | `l5_census.py` | store `81d24704` | `L5_census/L5_DOCKET.md` |
| L6 | convergence loop, 4 passes, bound exhausted → owner closure at ±1 board pt | `install_pass{1,2,3}.py`, `repin_harness_pass{2,3}.py`, `pooled_numeraire.py`, `nonvacuity_probe.py` | passes `bc1001f9`→`e6bc7e9d`→`692b12ff`→closure `96cb79b2` | `exec_306_u8ir65/l6/`, `l6/PASS*`, `L6_RI_BOUND_EXHAUSTED.md` |
| L7 | gates + seals at new totals; F5 re-sealed; G-Y0 exception retired | `seal_structure.py`, `nonvacuity_l7.py` | `2b5e99eb` | `exec_306_u8ir65/l7/` |
| L8 | candidate board beside same-engine baseline; every mover attributed | `attribute_movers.py` | boards `31f7108a` / `46ebfb37` | `exec_306_u8ir65/l8/` |

### L6 — the loop, in one table (all figures from committed artifacts)
| pass | installed | surface | derived | G-Y0 | verdict |
|---|---|---|---|---|---|
| 0 | `e69a3f38` | `b540833b` | `9f7848f4` | 0.035% | not fixed |
| 1 | `9f7848f4` | `6ba4f4c3` | `b61c01b0` | 0.033% | not fixed |
| 2 | `b61c01b0` | `69571649` | `3f5875b5` | 0.033% | not fixed |
| 3 | `3f5875b5` | `b683e2ec` | `01f27f02` | 0.033% | BOUND EXHAUSTED |
| closure | **`01f27f02`** | **`ebc3d330`** | (no derivation) | **0.033%** | CONVERGED AT TOLERANCE ±1 board pt (owner word 5188042722) |

Four distinct payloads — **no cycle proven**; the final two derived ladders differ by **≤1 board point at
any pick** (amplitude map `l6/pass3_amplitude_map.json`). The md5 fixed point was not reached and is not
claimed; the owner closed at tolerance, R-I's test unchanged.

---

## 2 · EVERY GATE FIRED IN ANGER — with its evidence pointer and its fail-direction proof

| gate | fired at | result | able to fail (both directions) | evidence |
|---|---|---|---|---|
| N35 fit-path assert | before every fit act (×4 this seat) | PASS `fb9efdec` 55/76/79/44s | this box PASSes; the seam's box FAILs (`969dba06`) — hazard 15 | `ASSERT_LOG.md` |
| Guard 5 boot-store | every bootstrap | PASS store `81d24704` | fails on a stale boot (checkout-anchored) | boot logs |
| R-I fixed point (full md5) | each L6 pass | not equal ×4 | equal → converged; the test discriminated all 4 | `l6/*fixed_point*`, verdicts |
| channel check 71 / 5.931% | each emit | CONFIRMED | STOP condition, fired the HALT at #290 (5186175269) | `l6/*matrix_identity.json` |
| F-C full-md5 surface binding | each emit | asserted | signature alone can't see the surface (two-surfaces-one-sig ×3) | matrix identity blocks |
| harness re-pin non-vacuity | passes 2,3 | both directions | old pin accepts old/rejects new and vice-versa | `l6/nonvacuity_probe.py` |
| basis byte-identity `25a72f85` | each pass | byte-identical | frozen harness `e0130cc2` never on `sys.path` | derive logs |
| G-Y0 hard bar 2.000% | every selftest | 0.033% GREEN | fired RED at 3.035% pre-#279; exception now retired | `*gy0.log`, selftest |
| selftest 97 checks | every build | 97 PASS / 0 FAIL | one FROZEN-RULER check caught the pass-1 pin defect on its first run | `*selftest.txt` |
| F5 seal-drift | L7 render + gate_f5 | PASS `ed5b7fcc` | one byte → recomputed ≠ pin → HALT | `l7/nonvacuity_l7.py` |
| F5 reconciliation (board == sealed) | L7 render + gate_f5 | MATCH 62726 | stale seal → board 62639 ≠ sealed → HALT (was a printed boolean; now a hard assert) | `l7/` |
| F5 league + F4 roster (±5%) | L7 | both PASS | conservation law | `l7/L7_gate_f5.txt` |
| L8 completeness gate | L8 | PASS on same-engine baseline | HALTs on the 4-axis released board AND on missing flags (§5) | `l8/attribute_movers.py` |

---

## 3 · COST MEASURED PER CYCLE (this seat's own timings, engine compute, strictly serial)

| act | cost | notes |
|---|---|---|
| N35 fit-path assert (`refit --verify`) | 44–79 s | run before every fit act |
| bootstrap (workspace seed + Guard 5) | ~30–60 s | every leg |
| v0surf refit + bake (C.3 step 3) | 97–159 s | the chain's only machine-sensitive act |
| matrix emit (`emit_matrix_271.py`) | 143–158 s | serial |
| board (`rl_export.py`) | 72–127 s | |
| book (`s4_matrix_M1v7.py`) | 135–189 s | |
| selftest (`one_source_selftest.py`) | 76–109 s | 97 checks |
| derivation (`pooled_numeraire.py`) | ~1–2 s | pure over committed JSON |
| L1(b) install (atomic instrument) | ~1 s | dry-run first, all-or-nothing |

**A full L6 pass** (install → refit → emit → basis → derive → fixed-point) ≈ **5 min** of engine compute;
**a gated pass** adding board+book+selftest ≈ **12–13 min** (matches the #290 record). Four passes plus the
closure and the L7/L8 builds were run this seat; the container restarted **four times**, each forcing a full
re-classification (~1 min) before work resumed.

---

## 4 · THE LANDING CHECKLIST — what ships at the landing (the owner's separate act, after the word)

Nothing here is done in rehearsal; it is the ordered set a landing seat installs under the EXECUTION word.

1. **The adopted ruled curve** `01f27f02…` into `pvc_curve_v2.json` via the L1(b) enumerated same-commit
   set (the proven `install_closure.py`), sealed-twin edits by JSON path, contract re-stamped.
2. **The converged surface bytes** `ebc3d330…` shipped as `data/v0surf.pkl`; `expected_boot.v0surf`
   re-stamped inside Addendum C.1's identity set.
3. **N43 signed pool levels** ship **together with** the curve+surface (per-division, AS SIGNED by the
   owner — the levels are his at the landing; `trade_desk_pool_split_2026-07-31/` carries the harness).
4. **The #323 store batch (incl. Addendum 4), fixture `f1e8c9fe…`, and the text cleanup** ride the landing
   commit as the seam's checklist names them — landing-set items, not rehearsal acts.
5. **THE DELIBERATE HARNESS-PIN HALT.** `harness_pvc_REPINNED.py` carries `EXPECT_V0SURF = '1cbbd9b00ff4'`
   (the pass-3 surface), **deliberately not moved at the closure** — no matrix was emitted there, so a new
   pin would have nothing to predict. **Consequence a landing/ingest seat MUST hold:** the next matrix emit
   on this substrate **HALTs the loader by design**, forcing a deliberate, ledgered re-pin against the real
   emitted matrix (non-vacuity both directions, as at passes 2–3). This is correct behaviour, recorded in
   `L6_closure_state.diff.BASE`, endorsed by the seam (5188266553) — not a defect to "fix" by pre-pinning.
6. **G-Y0 dated exception is retired** (L7): `held_checks` empty, `_retired_checks` records the reason,
   `contract_sha256` re-stamped; the 2.000% hard bar itself is untouched.
7. **The candidate board** is regenerated at the landing (byte-deterministic: `46ebfb37`), and the
   before/after per-stage attribution (owner order-1, 5186108632) assembles there across EVERY axis
   (store lag · engine · curve+surface pair · pool) — L8 built the hardest stage and its instrument.

---

## 5 · THE COMPLETENESS-GATE FIX (seam finding 5189242005) — DONE, with its both-directions proof

**The finding:** `attribute_movers.py` compared the caller's `--ids-*` flags; run with flags omitted it
printed `base None cand None OK` and **passed** — a silent false-PASS path (absence read as agreement).
The filed L8 result was unaffected (the seat's runs passed truthful flags and the HALT demo was real), but
a landing-reused instrument must not carry that path.

**The fix (refusal behaviour only — no arithmetic change):** a held-constant identity that is **missing on
either side** now HALTs, exactly as a **difference** does — absence is an unnamed cause. Proven three ways:

```
(a) flags OMITTED                     -> HALT (exit 1)   [was a false PASS; now closed]
(b) truthful same-engine flags        -> PASS (exit 0)   [601 movers, channels unchanged]
(c) released board, 4 axes differ     -> HALT (exit 1)   [store+engine named missing-or-moved]
```

The L8 attribution arithmetic is **unchanged** — 804 common, 601 movers, curve 322 / lens 255 / pool 24,
0 added / 0 dropped (`l8/attribution.json`). A self-inflicted variable-shadowing bug during the fix
(`a,b` locals clobbering the board dict `b`) was caught by a ZeroDivision on the first re-run and corrected
before this filing — recorded because the catch is the reusable part.

---

## 6 · KNOWN DELIBERATE STATES — named so none is mistaken for a defect

1. **The substrate is UNCOMMITTED (R-C).** The working tree carries the L7/L8 rehearsal state `2b5e99eb`,
   preserved losslessly in the sealed captures and round-tripping to them exactly. Committing it is the
   landing act and needs the withheld word. The ~220 restored reference files are the seam-ratified base
   reconstruction (`472c39d` non-docs + the `2a1xa4`/`u8ir65` docs), not re-authored onto this branch.
2. **The harness pin is deliberately stale** (§4 item 5).
3. **THIRTEEN captures stand, none overwritten** — each with a `.BASE` annotation naming its base commit.
   The live one is `L7_state.diff` `2b5e99eb` (L8 changed no product file).
4. **The #279 machinery is a reconstruction** — the operating tree needs zlaarm's non-docs content
   (`session_2026-07-30/item279/…`, `tools/preboot_assert.sh`); the captures apply on base `472c39d` only.
   Both round trips being byte-exact is the proof the reconstruction is right.
5. **The released board `f2df6e0a` is a 4-axis diff** from the landing (store `6b9d00a7`, engine `404e8113`,
   old curve) — never the L8 baseline; the same-engine pre-loop board `31f7108a` is.

---

## 7 · N35 LEDGER — four classifications, four reproductions

`55s / 76s / 79s / 44s`, all reproducing `fb9efdec` on the pure pass-0 substrate, one before each work
phase that followed a restart. On this environment `uptime` moved four times under this seat; the assert is
not a formality. Full detail in `ASSERT_LOG.md`.

---

## HAND-BACK STATUS

L1–L8 complete; every gate fired and shown able to fail; costs measured; the landing checklist enumerated;
the completeness-gate fix done and proven both directions; deliberate states named. **Ready for the seam's
verification, then the owner's EXECUTION word.** Bake HELD; EXECUTION word WITHHELD; nothing lands.
