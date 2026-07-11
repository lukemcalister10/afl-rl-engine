# RETURN — PICK-CONVENTION REMEDIATION (candidate) — 2026-07-11

- **Branch:** `claude/pick-convention-remediation-yidlbm` (owner-chosen; re-based onto candidate 0166ecf so all kept (a)/(c)/(f) work carries forward). **Head:** set at push.
- **PR #59 status:** untouched / not continued — owner directed this remediation to land on the designated `yidlbm` branch, not the `ywqmdi` candidate. No force-push, no bake/tag/main merge.
- **(i) Rows reverted: EXACTLY 190** rookie renumbers → original database-universe store ordinals (byte-restored from pre-correction a2fbc9a0; `_pick_source` stamps dropped; treacy 7→5). Kept intact: 325 `_draft` fills, 8 PSD splits (type/_draft/pick/_pick_source), (a) band-pool fix, (f) re-denomination. Verified surgical: post-revert store differs from a2fbc9a0 only by _draft(331)/pick(8 PSD)/type(8 PSD)/_pick_source(8 PSD).
- **(ii) Chain-table basis = the store's own MAX National ordinal (the database's ND end).** 21/23 years gapless (max==count, unambiguous); only 2010 moves **77→93** (reverts the forbidden real-world override — 77 was the external selection count) and 2011 stays **89** (already store-max). All other 22 years unchanged. Engine comment corrected (comment-only; no logic).
- **2010–11 flag outcomes:** all **42 tail rows CLEAR as intentional** — legitimate database-universe ND ordinals (unique per year, all type=National, real players e.g. Lachie Neale 73, Jarryd Lyons 74). Zero within-convention anomalies (0 duplicate ordinals). Gaps below the max = excluded/redrafted players that never consume numbering.
- **(iii) Flags cleared:** 495 "unverifiable" rookie flags + 42 tail flags CLEARED (never suspect under the convention). Owner law recorded in `engine/rl_after/pick_semantics_schema.md` (canonical exclusion sentence verbatim). Ledger updated with the remediation record.
- **New store md5:** `04f38dad7c03ae2ba8d060ffdbdd1bdf` (was 1a969d95). Board `8f3675f3`; book-seal `e35744c7` (candidate re-seal; baked/main seal 2a74c731 untouched). expected_boot re-pinned.
- **Re-measured factor: 1.052440 → 1.0524** (SCALE-ratio 4.68336/4.45). **Delta +0.00004 vs the pre-remediation pin — UNCHANGED to 4dp** (caps crush rookie-pick effects, as expected). Per-player median ratio 1.0503. `pick_redenomination.json` factor held; provenance re-stamped.
- **Gates:** VERDICT **FAIL=3 · FEATURE=1 · PASS=17 · PENDING=4 · STRUCK=1**. Reds **EXACTLY {A2, A3, A12}** (data-caused, unchanged). B3 book-seal PASS, B4 board-parity PASS (regen 8f3675f3 == shipped), B5 raise-only intact (lowered=0). Full log: `out/gate_suite_result_remediation.txt`.
- **Three narrowest margins:** G-COHORT y4 **1.29 vs hard 1.30** (1.0 pt, BINDING; B1 remediated avg row y4=129 — UNCHANGED) · A10 Curnow 0.55 vs 0.50 (+0.05) · A8 Berry 2.14x vs 2.00x (+0.14x).
- **Eyeball list regenerated:** `session_2026-07-11/pick_corrections/EYEBALL_LIST.md`.
- **⚠️ G-FLOOR STOP FLAG (owner ruling required before ANY promotion):** the eyeball floor-dipper lens shows **16 dips >5 SCAR (worst 13: Robert Hansen 174→161)** vs baked v2.7 — this exceeds the ≤5-SCAR dispensation ((d) had worst 1). **Every >5-SCAR dip is on an MSD/UNR PICKLESS fringe player** (empirical pick-equivalent), NOT a first-year national draftee. **The designated floor anchors (A5: Ginnivan/Bowey/Blakey) are all fine, well above floor.** Attribution (isolated by fast board regen): identical whether 2010 chain=77 or 93, so it is NOT the chain change — it is the already-accepted **(a) band-pool fix's true effect on empirical pick-equivalents, unmasked** by reverting the wrong real-world rookie renumbers (which had lifted these players). The board is correct per the owner's law; the dip is a real, non-anchor consequence. The BINDING G-FLOOR gate (B5) PASSED. Owner ruling requested on whether these non-anchor pickless dips clear the dispensation.
- **Time actual:** ~1.9h (within the 0.5–1.5h band's ~1.3× — the diagnostic + attribution of the G-FLOOR dip added a regen cycle; flagged).

## UPDATED SSI CHAINING-CONTRACT WORDING (for the supervisor's pen — SINGLE_SOURCE_INVARIANT.md)
> **Pick numbering is DATABASE-UNIVERSE, owner-authoritative.** Store `pick` values are database-universe
> ordinals, not AFL official numbering. Players previously listed are excluded when redrafted, and only their
> initial entry is recorded — one row per player at initial entry; redrafts never consume numbering, so a
> store ordinal deliberately sits below its real-world number by the count of excluded players ahead of it.
> The rookie draft chains onto the database's national end: first rookie pick of year Y = last_national_pick[Y]
> + 1, and PSD chains after national before rookie, both counted in the database's universe. `last_national_pick[Y]`
> is the database's own national end = the store's MAX National ordinal for year Y (the ND row COUNT only where
> the sequence is gapless). **No build may "correct" store pick numbers against external / AFL-official sources
> without an explicit owner ruling.** Store numbers deliberately differing from official numbering is expected,
> not a data error.

## IN PLAIN TERMS
Your database numbers players by where they land in *your* draft universe — recycled/redrafted players are left
out of the count, so your pick numbers sit lower than the real-world ones on purpose (Treacy is your pick 5,
not the official 7). The previous build "fixed" 190 rookie numbers to the real-world values and bumped the
2010 offset to 77 to match the real draft — both broke your rule, so I put all 190 back to your original
numbers and set 2010 back to your database's own last national pick (93). I cleared the 495+42 "couldn't
verify" flags because there was never anything to verify against — your database is the authority. Everything
regenerated; the money-numbers barely moved (currency factor 1.0524, unchanged) and all the usual gates are
green with the same three known-red players. **One thing needs your eye:** putting the rookie numbers back
nudged ~16 fringe *pickless* players (mid-season/unregistered types, e.g. Robert Hansen) down a bit more than
the small allowance — none of your real "floor" reference players moved, and it's a side-effect of the earlier
band-pooling fix showing through once the numbers were corrected. Nothing was baked or merged; it's a
candidate waiting on your ruling about those fringe dips.
