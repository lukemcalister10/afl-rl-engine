# DIRECTIVE — LEG B: UN-COMPRESS THE OUTPUT→PRICE MAP · 2026-07-16 · seat 9 (Fable)
### FIRES ON THE OWNER'S WRITTEN WORD. One store/engine writer at a time — none is in flight.
### Design of record: `docs/MEMO_LEGB_functional_form_2026-07-16.md` (READ IT FIRST, IN FULL).
### Any design ambiguity mid-build is a HALT-AND-ASK to the supervisor — never an in-build decision,
### never a model escalation. SILENCE IS A RED. S1–S6 operative.

## EFFORT: EXTRA
Why not one lower: this leg re-fits the central pricing surface — every proven value moves and the
young side is triple-guarded; the validation breadth (frozen-suite β/slope/ratio measurement, the
ledger, the kill-switch matrix, the decomposition) is the cost driver, and thinner validation is a
REFUSED LEVER (CORE, SPEED RULES). The design itself is pinned by the memo, so the effort buys
verification, not exploration.

## MODE: auto — the FIRST COMMITTED ARTIFACT IS THE PLAN, **THEN STOP (owner-ruled checkpoint)**
The PLAN commit must contain: (1) the PRE-VIEW HASH MANIFEST — the md5 of
`docs/MEMO_LEGB_functional_form_2026-07-16.md` and of `docs/acceptance_v1_17.json` AS FETCHED AT THE
BASE, recorded BEFORE any candidate metric is computed or rendered (acceptance `leg_b.preview_hashes`;
audit #16/#22/#45); (2) the SITE ENUMERATION (every conversion point the map wraps, file:line, current-
year AND projected-year legs); (3) the ρ FEED (the exact level function consumed + the V_ref
construction); (4) the onset-ramp width; (5) the s-grid measurement plan.
**CHECKPOINT (owner-ruled 2026-07-16): after the PLAN commit, HALT.** Return branch + PLAN-commit SHA
in ≤10 lines and WAIT. The supervisor prescreens the plan against the memo (sites · ρ feed · hashes ·
conservation placement); the owner pastes the PROCEED word into this chat. Only then does
implementation begin. A plan the supervisor rejects comes back as an amended plan commit, not as
improvisation. Scope limits live in the FENCE below, not in mode.

## TIME: 4–7 hours wall-clock BUILD TIME, in two segments (confirm up front; flag >2× / <½×; report actual)
Segment 1 (to the checkpoint): plan + hash manifest ~20–30 min, then HALT. Segment 2 (on the PROCEED
word): site implementation ~1.5–2.5 h · frozen-suite measurement + s-selection ~1–1.5 h · deliverables
(ledger, movers, decomposition, w-export) ~1–1.5 h · return ~30 min.

## FEED (documents, verbatim — never a prose restatement)
1. `docs/MEMO_LEGB_functional_form_2026-07-16.md` — THE DESIGN. Decisions (a)–(e) are settled; you
   implement, you do not redesign.
2. `docs/acceptance_v1_17.json` — assert the JSON entries (`leg_b.*`), never prose.
3. `docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md` (header v1.2) — chapter law, §1 verbatim.
4. `docs/DECISIONS_v110_2026-07-16.md` + `docs/CONSTRAINTS_v1_18.md` — rulings + the registry.
5. This directive.

## BASE PIN (THE BASE PIN rule, CORE)
- **Engine/store base — STRICT:** branch `claude/iso-corr-evidence-fade-jnda76` at
  **`8b8ab7d`** exactly (the Leg-A candidate head; PR #100). Verify:
  `git ls-remote https://github.com/lukemcalister10/afl-rl-engine claude/iso-corr-evidence-fade-jnda76`
  must print `8b8ab7d3772d1d5b653be01a2d76834ea6207b8b`. Any other SHA ⇒ HALT-AND-ASK.
- **Docs base (RE-PINNED at register item 208 — the owner's #99 merge legitimately moved main with
  ui/ files):** `git ls-remote https://github.com/lukemcalister10/afl-rl-engine main` — main AT OR
  AFTER `fcbd03a`, and `git diff --name-only fcbd03a..main` must be `docs/`-ONLY. Fetch the FEED docs
  from that main.
- Boot: Guard 5 asserts store `b1fd0bce` on entry of every gate/panel run. Store is NOT touched by
  this job (see FENCE).

## THE JOB (implement the memo exactly)
1. **The map (memo §2):** `v′ = v^(1−w) · (V_ref·ρ)^w`, `w = s·E` — at the raw_ev/posval site family
   (enumerate the sites in the PLAN exactly as Leg A's directive enumerated `iso_eff`'s six; the map
   wraps above-replacement production→SCAR conversion at current-year AND projected-year legs, each
   with that year's own E from the v2.10 `_ev_qual` family, τ = 1.1).
2. **ρ = the SMOOTHED demonstrated level** (`level_demo`/`level_now` machinery — memo §2.1); the
   positional reference (V_ref, ρ's denominator) from the demonstrated-proven population per position;
   state the exact feed in the PLAN. NEVER single-season points.
3. **Smooth onset (memo §2.2):** w ramps to zero over a declared width above the replacement bar;
   declare the width in the PLAN. No age gates anywhere.
4. **Conservation (memo §3):** production-side load-time calibration renorm, PER POSITION, ACROSS all
   year-depths. Pedigree pedestals + iso premiums NOMINAL. The transfer is explicit in the ledger.
5. **Kill-switch `RL_UNCOMP`** (declared exception, not a manifest dial — the Leg-A `RL_ISOFADE`
   pattern verbatim): `RL_UNCOMP=0` ⇒ board == `8d90c9ac` BYTE-EXACT (config_sha256 unmoved). Prove it.
6. **The s dial — DETERMINISTIC PRE-DECLARED SELECTION (acceptance `leg_b.s_dial_selection`):**
   measure β_c and β(s) with the FROZEN estimator over the grid {0.45, 0.50, 0.55, 0.60};
   **s = the smallest grid value with β point ≥ 0.85.** Never result-conditioned beyond this rule; if
   NO grid value clears, HALT-AND-ASK with the measured table (do not extend the grid yourself).
7. **Hygiene rider (spec §4):** delete the dead `if not _EVW:` branch (`_merged_recover.py:358–372`)
   with an OBITUARY — delete, don't disable.

## DELIVERABLES (committed artifacts; a return without its SHA is incomplete)
- Candidate PR continuing the candidate line from `8b8ab7d` STRICT; per-task commits; PLAN first.
- **A/B identity proof:** RL_UNCOMP=0 board md5 == `8d90c9ac`.
- **Frozen-suite measurements:** β_c and β(s) per grid point (estimator + CI + effective n printed) ·
  ≤22 slope vs 0.111 · English/Briggs (captain in) · **G-COHORT y4/y5/y6 via the frozen July-8
  construction + the committed row-level fixture** · L-SMOOTH census at the declared threshold ·
  census-v2 global gauge + the predeclared cells.
- **The whole-system SCAR ledger** (players + held picks + adjustments; tolerances per acceptance).
- **The donor-side mover report** (memo §8): top-30 proven markdowns with name · Δ · ρ · w · the
  earned/prior split — owner-viewing quality.
- **Value-flow + R104.8 decomposition** (the item-130 standing check): ΣΔ · cohort distribution ·
  over-performer scan · every young trim decomposed, production components byte-identical or HALT.
- **The w-export (item 204):** per-player-year evidence weight w + earned/prior decomposition, one
  committed artifact, schema stated in the PLAN (Leg D consumes it).
- **Gate snapshot** by engine hash + panel/self-test per the standing harness.
- RETURN ≤30 lines + "in plain terms" close, ALWAYS: branch · head git SHA · PR number · actual time.

## FENCE
IN: engine files at the enumerated sites (`_merged_recover.py`, `rl_model.py` if a site requires it),
the kill-switch, the deliverable artifacts, the hygiene rider above.
OUT (HALT if the job seems to need them): the STORE (`rl_model_data.json` — untouched, md5 `b1fd0bce`
at your head) · docs/ (you never author docs) · ui/ · the acceptance JSON · gate/guard code
(`ship_gates_check.py`, `boot_guard.py`, the config manifest) · any other leg's machinery · any
retuning of Leg A's τ. Mid-flight scope growth = a NEW directive (S2), never appended.
