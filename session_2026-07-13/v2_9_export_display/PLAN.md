# v2.9 EXPORT/DISPLAY BUNDLE — PLAN OF RECORD (first artifact) · 2026-07-13

Seat: export/display writer. Branch `claude/v2-9-export-display-jkcd5e`. Base = candidate
`claude/v2-9-candidate-integration-kq4dae` @ **917e4c4** (head verified unmoved — sole writer).

## BASE-VERIFY (done before any edit)
- `git ls-remote` head of kq4dae == 917e4c4 (not moved). ✅
- Workspace re-seeded from THIS checkout (bootstrap): engine `_merged_recover` **2030e5df** /
  `rl_model` **952ddb3d**, store **b0c39d78**, cm_400 **34faa865**, register **652d83e8**; Guard 5 PASS. ✅
- **Certified board reproduced EXACTLY**: full six-lever refit env ⇒ `rl_app_data.json` md5 **8a66b4ba**,
  n=804, sum_v=**732725**. Matches CERTIFICATION.md and the committed `data/rl_build` pin. This is the
  S1 "before" anchor; a byte copy is held for the zero-EV-mover proof. ✅

## BRANCH RECONCILIATION (owner-ruled)
The designated push branch was 12-ahead/23-behind the candidate; its 12 unique commits are docs +
an OFF-switch ingestion provision (all OUT of the export fence) and it LACKED the refit-cert
prerequisites. Owner ruling: rebuild the push branch from 917e4c4 (Option 1) after a safety gate.
- Safety gate PASS: all 12 discarded commits are reachable from `origin/main` (force-updated to 136e151
  during fetch) — no unique copy destroyed. `checkout -B claude/v2-9-export-display-jkcd5e 917e4c4` done.
- Push MY branch only (force-with-lease). NEVER push to kq4dae (read-only SPEC build pinned there).
- Lineage note for the RETURN: kq4dae@917e4c4 → export-display@<new head>.

## FENCE (hard)
IN: `engine/rl_after/rl_export.py`, `ui/tools/extract_board_view.py`, their tests, the UI view
bundles + EXPECTED_BOARD pin. OUT: `ev()` and every valuation path, the store, `_merged_recover.py`
engine body, the gate suite, docs/. **HARD ACCEPTANCE: every shipped EV identical before/after —
n=804, sum=732725, ZERO EV movers; NEW FIELDS are the only diff.** Any change that would move an EV
STOPs and is returned as a finding (S2).

## THE FIVE JOBS

1. **barker/thredgold `lti_reg` wiring (CONSUMER, in rl_export.py).** Root cause FOUND: on `MA.data`
   both rows carry `_lti_reg` correctly, but the board `players` list holds SEPARATE objects for these
   two first-year (no-scoring-row) players, and those objects never received the tag → export NULL.
   Contrast `max-king-syd`: its board object IS the same object → tag present. FIX: in rl_export build a
   `key → {register+attribution display fields}` map from `MA.data` (the tagged objects) and resolve
   `lti_reg` / `avail_nerf` / `lti_return_hc` from it by key in `player_rec`. **Display-only: `v` is
   read from the already-computed `_v`, never recomputed — EV-neutral by construction.** Prove both
   tags populate with named before/after lines.
   - FINDING (OUT of fence, report only): their shipped `v` (barker 777, thredgold 577) does NOT reflect
     the register availability haircut (L=1.0, out-until-2027) because the RL_AVAIL layer mutated the
     `MA.data` object, not the board object. This is a VALUATION-path defect; NOT fixed here.

2. **Export fields vPrev · vRaw · per-lever.**
   - `vPrev` = per-player value on the last-accepted-bake board = the pre-refit **all-levers-OFF base**
     (de4baef9 lineage, sum 723075 — the board currently on main this refit replaces). Feeds the
     Δ-vs-bake column (`p.v - p.vPrev`), Q-DELTA-BASE default (a). Rows absent from base → null (UI
     renders "awaiting", never a fabricated Δ).
   - `vRaw` = pre-override engine figure for override rows (else null). 0 overrides active today ⇒ null
     everywhere; wired forward-safe. `v` untouched.
   - `levers` = per-row cumulative G-ATTR deltas {L1,L4,L2,L3,L5} from the certified stage boards
     (base→+L1→+L1+L4→…→FULL, regenerated deterministically via the committed `gen_gattr_chain.sh`;
     reproduces gattr.json to the dollar — "from the certified attribution, not a new method").
   All three are NEW display fields; none feed `v`.

3. **+1/+2 phantom-pick lens entries** (items 12 + 14). Add lens-scoped future-draft pick lines
   (the next-EOY-ND class) that appear on the **+1 and +2 lenses ONLY**, never the current/-1/-2 ladder
   (item-14 exclusion already live — not disturbed), at **PVC face value** (entering-class value; no
   unruled future-discount invented — the board's official 15%/yr time-discount view stands), with
   **rolling year labels** (labelYear rolls with the view). Exported as a new top-level `lensPicks`
   structure; UI-transparent (rows flow like existing pick assets).

4. **Lens-conservation diagnostic** (item 12) — report-only committed output: lens totals across
   −2…+2 (players fading out the bottom + classes entering as picks), with the declared caveats
   (unexercised-pick discount + scrap-floor leakage ⇒ future totals run slightly under). NOT a gate.

5. **UI re-extract + EXPECTED_BOARD re-pin.** Regenerate the wired board with the new fields → copy to
   `data/rl_build/rl_app_data.json` → re-pin `data/expected_boot.json` `board` to the new md5 →
   run `ui/tools/extract_board_view.py` → new working/public bundles. Rulings hold: Q-GHOST(b)
   post-override figure+tag, Q-DELTA-BASE(a) last-accepted-bake now, Q-VERDICT(b), Q-THEME(a) dark-only.

## EV-INVARIANCE PROOF
Diff the after-board vs the held 8a66b4ba copy: assert (a) identical key set on `active`+`back`,
(b) identical `v`/`vM2`/`vM1`/`vP1`/`vP2` for every row, (c) n=804, sum_v=732725, (d) the ONLY new
keys are {lti_reg-populated-for-2, vPrev, vRaw, levers, + new top-level lensPicks/lensConservation}.
Zero EV movers or STOP. Committed as `out/ev_invariance_proof.txt`.

## TESTS
Add `engine/rl_after/tests/` (or ui) coverage: lti_reg populated for barker/thredgold; vPrev/vRaw/levers
present & typed; lensPicks appear on +1/+2 only; extract ring-fence passes on the new pin.
