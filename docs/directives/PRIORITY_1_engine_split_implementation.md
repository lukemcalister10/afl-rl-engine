# DIRECTIVE — Implement the ruled pricing split in the engine

**Status:** FIRED — owner word 2026-07-28. **This one writes the store and the board.**
**Seat:** one fresh execution supervisor, cold, directing hands. Not #207 and not #208.
**Sequencing:** read in and prepare now; **do not move the board** until #208's three closing tasks
have landed — the schema-version bump, the Bailey Williams override retirement, and the removal of the
four-surface panel re-pin. The panel one matters to you directly: until it is gone, every board move
costs a hand-typed re-pin across four surfaces, and this job moves the board.

---

## Why this comes before more measurement

The owner has ruled the pricing structure seven or eight times, and seats keep returning questions that
assume picks past 64 are priced. The cause is not comprehension. The old structure is implemented in the
code, in every artifact shaped 1–99, in the tests, and across the register; the new structure exists in
owner rulings and one page of `docs/CURRENT_STATE.md`. A seat doing work reads code and artifacts, so it
rebuilds the old model from the material in front of it. The ruling loses to the code.

This job makes the ruling true in the place seats actually read. Everything measured before it is
measured against a structure that does not exist.

## The structure, and it is already ruled — you are not designing it

**The national curve stops at pick 64.** Everything past 64 enters a **pool**: ND 65+, all rookie draft,
all post-draft selections. Valued **by position**. **Order of selection is irrelevant inside the pool.**
SSP and MSD are valued at the pool but tracked separately.

**There is no price for pick 70.** A player taken there is priced from the pool by position, not from a
curve. If your work produces a value indexed to a pick number above 64, you have reverted to the old
model — stop and re-read this section.

## The work

**1 · Remove the chaining.** `rl_model.py:209` and `:215` give RD and PSD entrants an effective pick of
`last_national_pick + their_pick`, putting them on the same ladder as national draftees. Both go.

**2 · End the curve at 64.** The pick curve covers picks 1–64. Nothing past it.

**3 · Give the pool one index.** Every pool player sits at a single index. Do not build a positional
valuation path — **one already exists**: `iso_corr(pos, pk)` takes position and pick, and
`_v0_curve_assert` asserts V0* is a function of `(pos, ageR, pick)`. A key forward at pick 1 is already
priced differently from a midfielder at pick 1. One index plus the existing position layer gives you one
value per position, which is exactly the ruling. What is position-blind is only `_PVC0`/`draftval`, the
raw pick ladder underneath — that is not the layer that prices players.

**4 · Do not re-derive `national_draft_last_pick.json`.** Lines 209 and 215 are its only consumers and
both are being removed.

## G-MONO — read this before you touch the curve

`docs/RULEBOOK.md` §4: *"THE CURVE DESCENDS (G-MONO). The pick curve is strictly decreasing; pick 1 =
3000 exactly."* That is law. The engine's own assert (`rl_export.py:137`) is weaker — `>=`, non-increasing
— so the code will not stop you breaking the rule. The rulebook will.

Under the ruled structure the pick curve is 1–64 and descends, and the pool is a value per position not
indexed by pick, so **G-MONO is satisfied as written and no amendment is needed.** That reading is with
the owner for confirmation.

If your implementation finds itself needing the rule changed, **stop and return it.** Rulebook wording is
a Law-10 act: exact wording pre-filed, owner's explicit word, never a seat decision.

## The fence — this is the part that has failed repeatedly

**Implement exactly what is ruled and decide nothing else.** Anything you find yourself *choosing* —
curve family, era handling, how the boundary is measured, how the replacement bar is keyed — belongs to
ITEM 412 and goes back to the owner. It is not yours to settle because you happened to reach it.

## Sequencing — why you cannot start yet

This job re-prices every player and **moves the board**. That is the same out-of-round board move that
broke the Movers chain and left round 20 unfinalised. #208 is currently finalising R20 and building a
history column against the current board; landing this underneath them invalidates their column
mid-flight and recreates the failure.

**Wait for #208 to land.** Its from/to work is the prerequisite that makes the board safe to move at all.

When you do move the board, the standing rule applies: **write a history column at that point**, so the
Movers tab can compare across it. The column's label is owner-set — ask for it, do not invent one.

## Rules that still apply

- Run `bash bootstrap_env.sh && bash bootstrap.sh` first and never bypass the pin — an unpinned numpy
  silently reorders the board. If it fails, say so and stop rather than working around it. Note the known
  fault: the script invokes bare `python3` while the lock pins the cp312 wheel.
- Screen by re-running, never by reading. Every figure names what it was measured on and how many rows.
- The container shallow-clones by default — `git fetch --unshallow` before any ancestry claim.
- Take current `main` in before you start.

## Hand back

On the issue. State: that lines 209 and 215 are gone and what replaced them; the curve's last pick; the
pool index and the per-position values it produces; the board before and after; the history column you
wrote and its label; and any point at which you had to choose something rather than implement it.

---

# ADDENDUM 1 — 2026-07-28. URGENT. Owner-directed. Amends by addition; nothing above is edited.

## THE DEFECT — this directive was insufficient, and the gap is mine

The body above says "remove the chaining at `rl_model.py:209` and `:215`". That removes where a pool
entrant **sits**. It does not remove whether his outcome **teaches the national curve**. Those are two
different things and the directive named only the first.

**Owner's specification, given 2026-07-28 and now binding on this job:**

> ND pick 64 can only be valued from the outcomes of players who were **drafted in the national
> draft**. Rookies cannot bleed value into the national curve — not by chaining, and not by
> contributing observations to the fit. Positions are the newly assigned ones. The values are derived
> from scratch on current information, not adjusted from an inherited curve.

He has stated this repeatedly and it has been acknowledged repeatedly and not implemented. It is the
whole point of the split. **A curve that still learns from rookie outcomes makes this job pointless.**

## WHY THE ONE-INDEX POOL MADE THIS WORSE, NOT BETTER

The fit cohort at `rl_model.py:245` is unchanged: `_grp in ('ND','RD')`. The curve builders draw
observations within **±4 effective picks** of each pick (`build_pvc`, `build_pvc_v34`, and the third
site — the `abs(_epk(p)-k)<=4` filters).

Every pool entrant now sits at exactly `POOL_PICK = 65`. So **every rookie-draft row is within ±4 of
picks 61, 62, 63 and 64** — all four on the curve. Previously they were spread from roughly 62 to 99
and their weight at pick 64 was diluted across many picks. Collapsing them to one index adjacent to the
boundary concentrates all of them at the last four picks.

**The evidence that this is live: `curve[64]` is still 530 — identical to the pre-split curve.** Picks
1–60 are clean, because no pool row is within ±4 of them. Picks 61–64 are not.

## WHAT TO CHANGE

**Exclude every pool row from every pick-curve builder.** The mechanism already exists and you already
wrote the helper: the builders' filter becomes `_in_pvc(p) and not is_pool(p)`. `_pvc_exclude` was
built for exactly this — it drops a player from the curve builders **only**, leaving him in the cohort
for `BASEPK_REG`, establishment and forward valuation. So a rookie is still valued as a player and
still appears on the board; he simply no longer teaches the national curve.

Apply it at every site that fits or samples the curve — the three `abs(_epk(p)-k)<=4` windows and any
kernel-weighted path (`fit_year0` and anything it feeds). Do not fix one and leave the others; that is
the duplicated-assertion class.

**`_grp` may stay `'RD'`.** You were right that it governs cohort membership rather than price. Do not
re-scope `hist`. Gate the **curve builders**, not the cohort.

## THE CHECK — and it must be able to fail

Prove that **no pool row carries any weight at any pick 1–64**, at every fit site, and show the check
failing when the exclusion is removed. A check that cannot fail is the vacuity class this project has
caught repeatedly. State the count of rows excluded and the count remaining, each naming its
population.

Then report `curve[61]` through `curve[64]` before and after the exclusion. If they do not move, say so
and stop — because that would mean the exclusion did not take.

## THE BOARD MOVE IS WITHDRAWN UNTIL THIS LANDS

The board you have rebuilt (`8a38cca4 → 3664689a`, 534 of 804 moved) is built on a curve whose last
four picks still learn from rookie outcomes. **Do not move it further and do not seek the history
column label yet.** Re-derive with the exclusion in, then come back.

## TWO THINGS FROM YOUR HAND-BACK, CARRIED FORWARD

**The 528 question is settled and you settled it.** The perturbation test was the right instrument —
levels 400/528/700 giving ratios 1.4056/1.0907/0.8354 shows the 9.07% is not an identity, and your
population finding is the decisive part: 318 of 763 rows never played a senior game and are carried at
full weight, and among matured entrants the never-played mean (612.41, n=297) sits **above** the played
mean (550.29, n=429). A quantity where failures outscore contributors cannot be an entry level. **Do
not rule from it, and the level stays at the carried 528 as an acknowledged placeholder.** Recording
the caveat beside the number in the selftest was the right call.

Also noted: the leg admits only ND 65+ and RD, dropping 331 of the 1,094 ruled pool rows in that
window — so it does not measure the ruled pool either. Another reason it cannot set the level.

**The `v0surf` finding blocks shipping and must not be lost.** The frozen pickle's config signature
includes the pick curve, so the split moved it (`a610237e → d702e463`) and the engine has silently
fallen through to the refit path — a path the design reserves for kill-switches. Every board figure you
have reported is built on a refit surface, not the frozen one. Regenerate via `refit_v0surf.py` at a
bake before any of this ships, and say plainly in the hand-back which of your figures were measured on
the refit surface.

## WHAT IS STILL NOT YOURS

The pool's level, the curve family, how the boundary is measured, and the from-scratch re-derivation —
that last one is now its own job and follows this one. Your fence was right and it held. The failure
was that nobody had commissioned the derivation behind it.
