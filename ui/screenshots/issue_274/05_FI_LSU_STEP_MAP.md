# The previously-shadowed CI steps — step → result → classification

Built 2026-07-30 on branch `claude/ui-wave-1-t5dl5v` at `28b3146`, under the owner's "map first, then a
bounded exception" instruction. **No file outside `ui/` and the two granted engine files was edited to
produce this map.** Local runs used the pinned env (`setup_env.sh` → `/root/rl_venv312`, py 3.12.3 ·
numpy 2.4.4 · scipy 1.17.1 · sklearn 1.8.0 · openpyxl 3.1.5) and Chromium via `playwright-core@1.47.2`.

## Why these steps were unmeasured

Final Integration steps 14–22 and Live Scoring steps 13–15 were **SHADOWED** behind the `movers.test.js`
2/58 known-red (#271 A22, declared). A workflow halts at its first failing step, so everything after it
had not run since adoption. #274 item 1 clears that red, which un-shadows them. Everything below is
therefore a **first measurement in this era**, and the classification column says whether each result is
inherited (reproduces without this wave's changes) or caused here.

## Final Integration

| step | what it runs | result | classification |
|---|---|---|---|
| 1–9 | fetch Board B · env pins · config/release identity closure · season-state | **PASS** (CI) | ran before; unchanged |
| 10 | present/forward invariants + F5 reconciliation, per-push lane | **PASS** (CI) | ran before; checks Board B's sealed layer, not the adopted board — see the finding |
| 11 | UI seams (extract · release · counting · club-curve · movers) | **PASS** (CI) — `movers.test.js: ALL 65 PASS` | **item 1's clearance confirmed on the runner** |
| 12 | unified 868-asset ranking + residual panel (Chromium) | **FAIL 38/40** | **INHERITED — adoption-created. Outside the exception. See the finding below.** |
| 13 | responsive layout, all widths (Chromium) | **PASS 72/72** (320 · 360 · 390 · 430 · 720 · 1440) | first run this era; no horizontal page scroll at any width |
| 14 | #222 item acceptance (Chromium) | **PASS 73/73** | 3 assertions were failing on adoption-stale counts — inherited (identical at `f1557b2`), restated in item 1; 9 added by item 3 |
| 15 | bootstrap workspace (Guard 5) | **PASS** — register `652d83e8`, fv `d10aa93e`, vendored unidecode OK | first run this era |
| 16 | clean-room engine rebuild-equality (board + UI bundles byte-identical) | **PASS — gating 9/9, `overall_ok=True`.** Rebuilt board byte-identical to committed (`f2df6e0a2902`); **`board_view_working.js` AND `board_view_public.js` byte-identical to committed HEAD**; rebuilt active key set == reference-vector set exactly (804/804, +0/−0); forward structure complete (804 rows, 0 non-numeric) | first run this era. **This is the strongest evidence for item 2**: a clean-room engine rebuild reproduces my committed bundles — including the new `elig` field — byte-for-byte, so that field is lane-generated, not hand-edited. Two non-gating lines declared by the step itself: `ADOPT-RED` (780 present-v mismatches vs reference vector `5546f278`, which is the PRE-adoption accepted vector — an adoption-lane release condition, explicitly non-gating) and `DEFERRED` Board B forward-lens semantics (historical R14 diagnostic, never an R19 oracle) |
| 17 | season-state anchors + generated-bundle equality | **PASS 9/9** — R14 anchor 0.58/0.545 fixed; R20 calendar 0.83 / exposure 0.773 both re-derived, not typed; stamp names the live store `6b9d00a7`; **generated UI-bundle byte-equality OK** | first run this era. Note this step re-extracts and `cmp`s both bundles — so item 2's `elig` addition is proved lane-generated, not hand-edited |
| 18 | disposable R15 regeneration preserves the future ladder + F5 | **HALT** — Guard 5 forward-valuation provenance | **INHERITED. Outside the exception. Second finding — see below.** |
| 19 | R14–R19 sequential season-state advance | **HALT** — same Guard 5 halt, same cause | **INHERITED. Outside the exception. Same finding.** |
| 20 | Track B fast unit + acceptance matrix | **PASS** — weekly_updater all pass · catchup preflight all pass · acceptance matrix **OVERALL: PASS**, `hard_fail=none`, deferred `['11_forward_vector_invariants']` | first run this era. Writes evidence JSONs under `session_2026-07-21/`; reverted, tree left clean |

## Live Scoring Updater — green end to end

CI at `28b3146`: **success**, so its shadowed steps ran. Re-measured locally for the map:

| step | what it runs | result |
|---|---|---|
| 11 | movers view logic tests | **PASS 65/65** |
| 12 | movers provenance transition | **PASS 39/39** |
| 13 | movers acceptance proof (committed R15–R19 reports) | **ALL PASS** |
| 14 | generic release-metadata contract proof | **ALL PASS** |

## The one failure, and why it is NOT re-pinnable

**FI step 12 — `session_2026-07-21/final_integration/tools/asset_view_ui_check.mjs`, 38/40.** Both
failures are the same assertion at 390px and 1440px: *"residual reconciliation panel present +
reconciles"*, which requires the rendered panel to read `= sealed F5 entrant layer 83,538 ✓`.

Measured, four ways:

| where | entrant layer | draft | mech |
|---|---|---|---|
| `data/release_contract.json` → `.f5_entrant_reconciliation.entrant_layer_pvc` (committed) | **83,538** | — | — |
| pre-adoption bundle at `a86c725` (board `8a38cca4`) | **83,538** | 69,266 | 14,272 |
| pre-adoption `release_contract.json` at `a86c725` | **83,538** | — | — |
| **adopted** bundle at `f2df6e0a` | **77,611** | 68,556 | 9,055 |

So before adoption the bundle and the contract **agreed**, and the reconciliation held. Adoption moved the
layer by **−5,927** (draft −710, mech −5,217; the two deltas sum exactly) and the contract's
`f5_entrant_reconciliation` block was **not re-stamped**. The panel's own arithmetic is internally
consistent (65,925 visible + 2,631 deep-tail + 9,055 non-ND = 77,611 ✓) — it is the *seal* it no longer
matches.

**The check is working, not stale.** It caught a real divergence between a committed release identity and
the board being served. Under the owner's bound, the replacement value must be *the adopted identity as
carried by committed `data/expected_boot.json` or `data/release_contract.json`* — and that value is
**83,538, i.e. unchanged**. Re-pinning the check to 77,611 would be precisely the forbidden move: a value
re-derived from the tree because it makes the step pass. So this falls under bound (3): **stopped, handed
to the seam.**

It is also outside the fence twice over — the harness script is not in `ui/`, and the plausible *correct*
fix (re-stamping `data/release_contract.json`, or re-deriving the F5 layer) is a `data/` write, explicitly
barred for this wave.

Confirmed inherited: the identical two failures reproduce at main tip `f1557b2` in a clean worktree with
none of this wave's changes present.

## The second finding — the R14 rewind cannot import today's forward_valuation

**FI steps 18 and 19** both halt before doing any work, on the same Guard 5 refusal:

```
============ FORWARD-VALUATION PROVENANCE (Guard 5) FAILED — BUILD HALTED ============
  - fv CHECKOUT DRIFT: checked-out forward_valuation identity
        d10aa93e977a16a7…  !=  pinned 6a9a520fa2f8b405… (data/expected_boot.json 'fv')
  - fv LOADED-PATH DRIFT: the engine will IMPORT forward-valuation from RL_FV=…
        identity d10aa93e977a16a7…  !=  pinned 6a9a520fa2f8b405…
```

Both proofs build a throwaway scratch repo and then call `materialize_r14()` — "reconstruct the accepted
R14 baseline… stamps engine identities". So the scratch's manifest is deliberately rewound to the R14-era
pins, including the R14-era `fv` **6a9a520f**. But the scratch copies the repo's *current*
`engine/forward_valuation`, whose identity is **d10aa93e**. Guard 5 exists precisely to refuse booting on a
forward_valuation that is not the pinned one, so it refuses — correctly.

The R14 rewind rests on an assumption that no longer holds: that the fv source has not moved since R14. It
has. The live tree is *self*-consistent (`data/expected_boot.json` `fv` = d10aa93e = the checked-out
source, and FI step 15's Guard 5 asserts that match and PASSES) — the conflict exists only inside the R14
rewind.

**Why this is not re-pinnable under the exception.** The stale-looking `6a9a520f` is not a hardcoded
literal in the harness; it is derived from the frozen R14 record, where it is *correct history* and must
stay. The adopted identity carried by `data/expected_boot.json` is `d10aa93e`, but stamping that into the
R14 materialisation would make the reconstructed "accepted R14 baseline" declare an identity R14 never had
— manufacturing a false record to make a step pass. The real options are to vendor the R14-era fv source
alongside the frozen record, or to rule that the R14 rewind is retired now that fv has moved. Both are
rulings about how a historical baseline is reconstructed, not literal swaps. **Bound (3): stopped.**

**Confirmed inherited, by diff scope rather than a 15-minute rebuild:** the halt depends on exactly two
things — the fv identity `materialize_r14` stamps, and the identity of `engine/forward_valuation`. Neither
`engine/forward_valuation`, nor `data/expected_boot.json`, nor any harness file appears anywhere in this
branch's diff against `f1557b2`, so the halt is provably independent of this wave.

## What the seam has to decide

**On the F5 reconciliation (step 12):** which side is right — did adoption legitimately move the F5 entrant
layer, in which case `release_contract.json`'s reconciliation block needs re-stamping and the check
re-pinned to the new sealed value; or is the adopted board's F5 layer wrong, in which case it is a
valuation-side defect. Either answer is a ruling about a released identity, not a stale number.

**On the R14 rewind (steps 18/19):** vendor the R14-era forward_valuation source so the rewind can boot
under its own pin, or retire the R14 rewind now that fv has moved. Either way the frozen R14 record keeps
its true identity; what changes is how a proof reconstructs it.

Neither is a UI display item, and neither is reachable from inside this wave's fence.

## Bottom line

Of the twelve previously-unmeasured steps, **nine pass on first measurement** and **three fail — all three
inherited, all three outside the granted exception**. Final Integration halts at step 12, so in CI steps
13–20 remain shadowed behind the F5 failure even though they are measured green (or classified) here. The
all-four-green bar therefore cannot be reached from inside `ui/`: it needs the two rulings above.

## Literals re-pinned under the exception

**None.** No failure in this map fell inside the exception's class, so the exception was not used and no
before→after literal table is required. Nothing outside `ui/` and the two granted engine files was edited.
