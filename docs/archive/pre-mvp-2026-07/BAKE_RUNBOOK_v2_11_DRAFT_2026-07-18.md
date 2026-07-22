# BAKE RUNBOOK — v2.11 · DRAFT · seat 13 · 2026-07-18
### ⚠️ STALE — PREDATES THE DETERMINISM SAGA (flagged 2026-07-19, item 398). This draft was written
### before F6/F7/env-pin/dispatch-pin and does NOT yet enforce: the balanced-board REPRODUCTION GATE
### (bake only on an instance reproducing the pinned board), the v0surf pin (3af2b725), the ENV-PIN
### assert, or the dispatch assert; nor the candidate STACK (15a9abd←540b62f←3055ea5←dispatch-pin) or
### the BOARD-OF-RECORD REFRAME (item 395: a pinned md5 may supersede 06d8af60 at the viewing). MUST be
### brought saga-current — once the dispatch-pin OUTCOME is known (which md5 to pin) — BEFORE the owner's
### bake word. Do not bake off this draft as-is.
### **STATUS: DRAFT — executes ONLY on the owner's written bake word, AFTER the full ladder**
### (audit shards reconciled · viewing done · sealed reads scored). ⟦SLOTS⟧ fill at the word.

## THE WORD REQUIRES (the owner sees FIRST): the viewing pack at ⟦FINAL-HEAD⟧ — board + book +
movers (Rozee/Reid named rows re-rendered) + riders (i)–(iv) + retro bridge + phantom-split
totals + THE RATIFICATION LIST: tail read stand/retire · R=207 free-intake seal · entrant-slot
structure seal ⟦⟧ · φ pedigree-carry `fd92b6fc` · r_pop seal ⟦⟧ · posture presets `c2e17c49`.

## THE BAKE (one build, from the confirmed candidate, THREADS=1 throughout)
1. Base = ⟦FINAL-HEAD⟧ STRICT (ls-remote assert) · boot-store assert · full frozen suite GREEN.
2. **THE GUARD-5 RE-PIN (the standing red, cured here on the word):** `data/expected_boot.json`
   engine-file md5s re-pinned to the candidate's (`rl_model` ⟦⟧ · `_merged_recover` ⟦⟧ ·
   `rl_export` ⟦⟧ · others per the manifest's own list) — the ONE sanctioned pin edit, owner-worded.
3. **INFRA_ALLOW / manifest entries ride the word (the RL_FLEX pattern):** `RL_PVC2` · `RL_LEGE`
   · `RL_LEGF` (defaults ON as shipped).
3b. **LAND THE DOCS-ON-MAIN-ONLY FILES ONTO THE BAKE HEAD (items 372/375 — the two lineage
   splits):** `docs/acceptance_v1_21.json` and `docs/inputs/CLEANROOM_GPT_section5_failure_modes_
   2026-07-18.md` exist on the docs/MAIN lineage but NOT on the candidate engine lineage. At the
   bake, bring both onto the bake head (they carry only already-ruled content — verified harmless
   to every gate at item 372) so v2.11 ships carrying its own acceptance bar + the §5 record. This
   is a docs-carry, not a value change; the store/board are untouched by it.
4. Bake → tag **v2.11** (owner pushes tags) → boards/book stamped (S1) → **clean fast-forward
   promote of `main` to the bake head — never force** (owner's act).
5. POST: seam docs (HANDOVER/DECISIONS/manifest rev) · convenience-copy sync (owner) ·
   round-entry GO-LIVE on his separate word (GO_LIVE runbook) · the post-v2.11 queue opens
   (backward-eval Y-awareness fix · stack-pinning option · 326/327 · 307/308 · entry-pricing
   chapter if the tail read stands).
