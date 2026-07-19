# DIRECTIVE — R106.7 WIRING (the leg-blind bar: the floor half) + item-284 behaviours + the two owner data corrections
**v1.1** · 2026-07-17 · supervisor seat 11 · build model: Opus · ONE JOB, ONE CHAT (S2)
### v1.1 (same day): re-issued for a FRESH chat after the first firing cut from MAIN (the third
### wrong-base of its class — register item 298; the prior branch `claude/r1067-wiring-item-284-c37vsh`
### @ `f2bf728` is QUARANTINED, content reference only, owner deletes). ONE structural change: the
### base commands moved from prose to the literal block below — EXECUTE IT BEFORE READING FURTHER.
### No job, fence, target, or deliverable changed.
STATUS: ISSUED — fire when pasted by the owner. Do not fire from the repo alone.

## ⛔ EXECUTE FIRST — BEFORE READING ANYTHING ELSE (your first committed artifact is this block's proof)
```
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/claude/legc-relay-dpp-law-10c4z7
#   MUST print 6306378691d178551a7f8a461c73811f7a29df4e — anything else: HALT, report, stop.
git fetch origin claude/legc-relay-dpp-law-10c4z7
git checkout -B claude/r1067-wiring-v11 6306378691d178551a7f8a461c73811f7a29df4e
git merge-base --is-ancestor 6306378691d178551a7f8a461c73811f7a29df4e HEAD && echo ANCESTOR-PROOF-PASS
md5sum engine/rl_after/rl_model_data.json     # MUST begin 0efdc5d6 — anything else: HALT.
grep -c y0dpp_bar engine/rl_after/rl_model.py # MUST be >=2 — if 0 you are on the wrong tree: HALT.
```
Commit this block's output as `session_2026-07-17/r1067_wiring/FIRST_COMMANDS_PROOF.txt` — your
FIRST commit, before the PLAN. You are NOT on main. Main carries only docs; every engine target
in this directive exists on the base you just checked out (supervisor live-verified, item 295).

## THE FIVE (CORE)
- **EFFORT: High.** Why not Medium: this is the chapter's store/engine writer; it touches the §1b
  pricing site, a floor mechanism the probe must first locate, and produces the board the owner
  views at the ladder. Why not Extra: the scope is fully enumerated below, the projection half is
  already wired and verified (item 295), and the site question is answered by a mandatory probe
  before any wiring.
- **MODE: auto.** First committed artifact = the PLAN. Scope limits are the FENCE below, nothing else.
- **TIME: 3–6 h.** Confirm up front; flag >2× or <½×; report actual.
- **FEED (documents, not restatements):** DECISIONS v121 · CONSTRAINTS v1.18 · acceptance_v1_20.json
  (assert the JSON entries named below; ⚠ its `s_dial_selection` field is STALE per R106.3 — it is
  NOT a thing to assert or act on) · SPEC_PVC_FLEX_CHAPTER v1.3 (§1 + §1b) · register items 269 ·
  270 · 281 · 282 · 284 · 287 · 290 · 295 · 296 · the item-283 F13 note (the spec β/CI gate is a
  KNOWN queued-re-seal matter — a red there is a REPORTED finding, not a halt, cite F13).
- **FENCE.** IN: `engine/rl_after/rl_model.py` · `engine/forward_valuation/distribution_pricing.py`
  · `engine/rl_after/one_source_selftest.py` · `engine/rl_after/rl_export.py` (labels only, if
  needed) · the store `engine/rl_after/rl_model_data.json` (EXACTLY the two rows in job 1) ·
  derived artifacts + `data/expected_boot.json` re-pin · your `session_2026-07-17/r1067_wiring/`
  dir. OUT: docs/ (always) · every Leg-B dial and constant · `_merged_recover.py` — **if the
  ACT-1 probe names the floor site in a file outside this fence, HALT at the checkpoint and ask;
  do NOT extend the fence yourself** (the item-281 law: this exact halt-and-ask worked last time).

## BASE PIN (store/engine base ⇒ STRICT equality)
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/claude/legc-relay-dpp-law-10c4z7`
must return **`6306378691d178551a7f8a461c73811f7a29df4e`** exactly; branch from that SHA (stacked on
the candidate line, PR on top of #104). FIRST COMMANDS per item 270: fetch → checkout -B → 
`merge-base --is-ancestor` proof committed. Store md5 at base = `0efdc5d6`. Any drift ⇒ HALT.

## THE JOB (in this order)
1. **THE TWO OWNER DATA CORRECTIONS (item 296, owner-worded; stable-ID only — item 269; name-matching
   over the 2,652-row store is FORBIDDEN).** In the SOURCE store (SSI: never a copy):
   - Colby McKercher → `eligibilities: "G-DEF,MID"`
   - Jake Lloyd → `eligibilities: "G-DEF,G-FWD"`
   Validate-or-halt: token vocabulary as the store carries it (hyphenated, comma-joined, no spaces);
   present_position ∈ the collapsed set must now hold for BOTH rows; every other field byte-equal;
   every other row byte-equal. Commit as its own change with a two-row diff artifact.
2. **ACT 1 — THE prod_floor PROBE (before ANY wiring; item 281: the site is named FROM THE CODE).**
   Locate, by reading and empirical probe, exactly where the DEMONSTRATED-FLOOR leg produces the
   year-0 number (the `max(prod, MA.prod_floor(p,lens))` hook in `v_at_peak` and whatever
   `prod_floor` reads beneath it). The probe ANSWERS, from the code, with numbers: (a) how the
   floor's remaining-season component is currently scaled pre-§1b (the year-0-scaling question) and
   (b) how the floor treats age (both PARKED AS DESIGN by the owner — your probe is the evidence
   for his design read, not a license to redesign). **CHECKPOINT HALT here — committed and PUSHED
   (item 282), ≤20 lines**, naming: the site file:line, the two answers, the wiring plan in three
   sentences, and the fence verdict (in/out). The owner's paste-back is the go for job 3.
3. **WIRE THE FLOOR HALF (R106.7 verbatim, DECISIONS v121 §1):** §1b applies to WHICHEVER leg
   produces the year-0 number — projection AND the demonstrated floor. The floor's
   remaining-season component nets against the LOWER replacement bar (`y0dpp_bar`), and NOTHING
   else changes:
   - **THE EXACT FORMULA (item 290):** remaining = `clamp(1 − SEASON_PROG, 0, 1)`; SEASON_PROG =
     elapsed share of the season; ASSERT the endpoints in a committed check (SEASON_PROG=0 ⇒ the
     whole year-0 nets vs the low bar; =1 ⇒ §1b is a no-op). SEASON_PROG itself is UNTOUCHED
     (0.58) — moving it is an owner dial, not this job.
   - **PRESERVATION CLAUSES (BINDING, both explicit in code comments and in a committed test):**
     the banked/played component is untouched; years-1+ remain governed solely by §1 (futblend).
   - RL_FLEX gates the floor half exactly as the projection half: `RL_FLEX=0` ⇒ byte-exact off.
4. **THE ITEM-284 BEHAVIOURS (DECISIONS v121, the rule in full — implement, both classes):**
   - Same-line K/G = the silent listing-artifact collapse (as now; no flag).
   - The four CROSS-CLASS fixtures (K-DEF+G-FWD · K-FWD+G-DEF · RUC+G-FWD · RUC+G-DEF) and
     present_position ∉ the collapsed set are DATA ERRORS: the row is **REPORTED BY NAME** (a
     committed named-row artifact, not a log line), treated **SINGLE-POSITION for §1b (no dual
     bar)**, and the build **CONTINUES — never a halt**.
   - Add both classes to `one_source_selftest.py` as flex-era checks that FLAG-AND-NAME (verdict
     always produced — SILENCE IS A RED) without failing the suite; plus in-session fixture
     unit-proofs of `_collapse_elig`/`y0dpp_bar` on all four cross-class pairs and one
     present∉pair synthetic. (The acceptance-JSON fixture entries ride the queued re-seal — the
     supervisor's pen, not yours.)
5. **DERIVED + BATTERY:** rebuild board/book/panel; re-pin `expected_boot`; full battery.
   **HALT SEMANTICS (item 290, items 258/259 reconciled): the G-COHORT 1.30 cap is the SOLE hard
   HALT; a sub-1.08 floor reading is a REPORTED failure for the owner's conversation — never
   self-halt on it.** Frozen-suite-only measurement (S4); hash-cached reuse per S1.

## DELIVERABLES (assert artifacts, never prose statistics — the Leg-C audit law)
- The PLAN · the two-row store diff · the pushed checkpoint · per-task commits · candidate PR
  stacked on #104.
- **PER-GATE COMMITTED VERDICTS — MANDATORY (item 295's cure):** one committed verdict artifact
  per constituent gate (Guard 4 · Guard 5 · F1/F2 · G-COHORT y-band · earned-component · A-PAIRS
  · E/B · β), each with its exit code. If the ship_gates orchestrator is env-killed again (the
  known exit-144 mode), run every constituent independently AND commit each verdict — the
  orchestrator's death is acceptable ONLY against these files.
- **THE A/B CHAIN on the corrected store:** `RL_FLEX=0` ⇒ EXPECTED `807e6551` (the writes-only
  board — the two eligibility corrections should be invisible at FLEX=0). If it differs, that is
  a FINDING (eligibilities read outside the flex gate) — report at the checkpoint, do not improvise.
  (The deeper kill-switch chain — FLEX=0+UNCOMP=0 ⇒ 8d90c9ac — was proven by the relay ON THE BASE
  STORE and is S1-cached; do NOT re-assert it against the corrected store, where it does not apply.)
- **NAMED ROWS (committed JSON, exact figures):** Petracca pre→post R106.7 (the corrected preview
  — an OWNER-VIEWING artifact; his relay +29/+97 was pre-amendment BY DESIGN) · McKercher (expect
  the bar GEN_FWD→GEN_DEF and most of the item-295 +105 to come back off) · Lloyd (expect ≈
  unchanged, the bar now legitimate) · Sheezel (expect ≈ unchanged — projection-leg, already
  barred; state his number) · Bontempelli · Driscoll (100% MID must HOLD — single-position, NO
  §1b effect; state his number) · any row the item-284 checks name.
- **THE LEDGERS re-emitted on the moved board (item-256 schema):** the all-804 MOVEMENT ledger +
  the value-up-rank-down FAILURE subset (ranks carried; the relay's subset was 115 — restate the
  new count and the tie-break used: POSITIONAL rank).
- RETURN ≤30 lines · branch · head SHA · PR number · "in plain terms" close · actual time.

## STANDING CONDUCT (HANDOVER §3 — binding here)
First commands (270) · stable-ID identity (269) · checkpoint HALTs arrive PUSHED (282) · sites
named from the code (281) · no terminal item-counts · SILENCE IS A RED (a check with no verdict
has FAILED) · one authored source (SSI — the store edit in job 1 is the ONLY store write) ·
Smoothness Law (no threshold may enter the floor wiring) · weight-don't-gate (R105.4).
