# DIRECTIVE — Derive the ND 1–64 curve and the pool's level FROM SCRATCH

**Status:** FIRED — owner word 2026-07-28.
**Seat:** one execution supervisor, cold, directing hands. **Not the #217 seat** — it implemented the
structure and must not also decide the values.
**Sequencing:** follows #217 **including its Addendum 1**. You cannot fit a national-only curve until
the pool rows are out of the curve builders, because until then the fit still sees them.
**Nature:** DERIVATION. This job produces candidate values. **It does not adopt them** — adoption is the
owner's, and it is a separate release with its own word.

---

## Why this job exists, stated plainly

The owner has specified this repeatedly and it has never been built. Every previous attempt implemented
the *structure* — where a player sits — and left the *values* inherited from a curve fitted under the
old model. **Nobody was ever commissioned to derive the new numbers.** That is this job.

**The specification, owner's own words, 2026-07-28 — this is the requirement, not a paraphrase:**

> It is essential to me that this new number we are deriving is ENTIRELY from scratch. Based on the
> players value over any NEW positions they've been assigned, so busts for KPDs might go up if more
> midfielders that busted have been assigned to KPD. If rookies that did well now no longer tack on to
> the ND, they CANNOT bleed value. ND pick 64 can only be valued based on outcomes of players that were
> DRAFTED IN THE ND, and the outcomes are based on the NEW information we have.

Read that again before you write anything. Every requirement below is downstream of it.

## What "from scratch" means, concretely

1. **National-draft rows only.** The ND curve is fitted on players drafted in the national draft, at
   national picks 1–64. **No rookie-draft row, no pre-season-draft row, no pickless-mechanism row
   contributes any weight at any pick 1–64.** Not through chaining, not through a kernel, not through a
   ±4 window, not through a fallback. This is the requirement the whole split exists to satisfy.
2. **The new position assignments.** Positions are as they now stand in the store, not as they stood
   when the old curve was fitted. The owner's own example is the acceptance case: **a bust reassigned
   from midfield to key defence must move the key-defence prior, not the one he left.** 538 players
   changed drafted position at the restructure, 338 of them inside the priors' own training window.
3. **The current store.** Not `c120cfd5`. Take the store as it stands when you start and name its md5 in
   every figure you report. #207's stage-1 numbers were measured on `c120cfd5` and the store has moved
   since — they are context, not inputs.
4. **Not adjusted from the inherited curve.** Do not start from `pvc_curve_v2.json` and modify it. Fit.
   If your output happens to resemble the old curve, that is a finding to report, not a target to hit.

## The pool's level — derive it, and not from a pedigree mean

#217 carried over 528 (the pre-split artifact's value at index 65) as an acknowledged placeholder. It is
yours to replace with a derived value.

**It established one thing you must not repeat.** The pool's composition-weighted mean `v0_start` is
575.89 over 763 rows, and it cannot be the level, because within that population the players who
**never played a senior game** average 612.41 (n=297) while those who **played at least one** average
550.29 (n=429). The failures score higher. `v0_start` is a zero-evidence pedigree projection, so a mean
of it is anti-correlated with actually making it. **Any level set from a pedigree mean is set from the
busts.**

So: the level must come from **realised outcomes**, on the same footing as the bust priors — target is
the realised production of pool entrants, with **never-established players entered as 0.0**. That zero
is the survivorship fix and it is not optional; dropping those players is what produces a level set by
survivors.

Also: that 763-row population admitted only ND 65+ and RD, dropping 331 of the 1,094 ruled pool rows in
window. **Your population is the ruled pool** — ND 65+, all rookie draft, all post-draft selection, with
SSP and MSD valued at the pool but tracked separately so they can become their own pools later.

**One value per position.** Order of selection carries no value inside the pool. There is no ordering to
fit, so there is no isotonic step in the pool — one number per position, and the position layer
(`iso_corr`) applies it.

## Two known defects in the priors recipe — address them or carry them explicitly

Both were found at v509 and neither was flagged when the priors were first derived:

- **The `× 0.6` blend ceiling has no stated basis.** `w = min(n_pos/200, 1) × 0.6` means every prior is
  at least 40% pooled, and the cap binds for **five of six positions** — MID with 579 samples receives
  exactly what KEY_FWD receives with 208. Above n=200 sample size stops mattering. Measured effect:
  spread at pick 1 is 18.9 as shipped against 35.5 uncompressed, a **1.88× compression**. Report the
  fit with and without the ceiling and say which you recommend and why.
- **`IsotonicRegression(increasing=False)` on raw pick gives plateau widths set by noise.** Report
  whether your construction inherits that and what you did about it.

## The check that decides whether this job succeeded

**Prove that no pool row contributes weight at any pick 1–64**, at every fit site, and **show the check
failing** when the exclusion is lifted. A check that cannot fail proves nothing — that is a named hazard
here and it has been caught repeatedly.

Then report, each naming its population and the store it was measured on:

- `curve[1]`, and picks 55–64 individually, **before and after** the exclusion. If the last four picks
  do not move, the exclusion did not take — say so and stop.
- The count of rows in the ND fit, and the count excluded, with the reason each was excluded.
- The pool's derived level per position, with the realised-outcome basis named and the never-established
  count stated.
- The board effect on a **scratch board only**. Nothing is adopted, baked, re-pinned or released here.

## The fence — narrower than #217's, because this job does derive

You **are** commissioned to derive values, which #217 was not. You are **not** commissioned to decide:
which construction ships, whether to adopt, the replacement bar, era handling, or how eligibility keys
anything. Those are ITEM 412 and the owner's. **Produce the numbers with their basis and recommend;
do not adopt.**

If deriving the curve requires a rulebook change, stop and return it — Law-10, owner's exact words only.
G-MONO as amended (v2.1) scopes strict descent to picks 1–64, and the pool is exempt because it is one
value per position rather than an ordering. That should be sufficient; if it isn't, that is a finding.

## Rules

- `bash bootstrap_env.sh && bash bootstrap.sh` first, never bypass the pin — an unpinned numpy silently
  reorders the board. Known fault: the script invokes bare `python3` while the lock pins the cp312 wheel.
- **The `v0surf` pickle is stale and the engine silently falls through to a refit path.** #217 found the
  config signature moved with the split (`a610237e → d702e463`). Establish which surface you are
  measuring on and say so beside every figure. Do not report a number without naming it.
- Screen by re-running, never by reading. Every count names its denominator. Every duration names its
  basis.
- Shallow clone by default — `git fetch --unshallow` before any ancestry claim.
- Take current `main` in first; do not build on a stale base.

## Hand back

On the issue. Lead with whether the requirement at the top of this directive is met — no pool row
teaching the national curve, positions as newly assigned, current store, fitted not adjusted — and the
evidence for each. Then the numbers. Then anything you found yourself choosing rather than deriving.

---

# ADDENDUM 1 — 2026-07-28, owner-directed. Amends by addition; nothing above is edited.

## A · APPLES FOR APPLES. Replicate the method exactly. Change only the data and the separation.

**Owner's words, 2026-07-28:**

> We should be looking to replicate the old system for now, so however it handled 'low sample'
> positions like ruck — should be replicated. It is an apples for apples replication, except it is
> based off the new data entirely. So the new store. The new separation. But within that information,
> the way it's calculated is the same.

**This overrides part of the body above, and the part it overrides was my error.** The body asks you to
"report the fit with and without the ceiling and say which you recommend." That invites a **method
change**, and no method change is wanted. Do not make one and do not recommend one.

**Keep, unchanged:**

- **The `× 0.6` blend ceiling and the `min(n_pos/200, 1)` pooling weight.** This *is* the old system's
  low-sample handling — it is how RUC at 208 samples gets pulled toward the pooled average rather than
  trusting a thin cell. Replacing it would be a different model, not a replication.
- **The isotonic step on the ND curve**, as constructed today.
- Every other construction choice: target definition, cohort window, weighting, era handling.

**Change, and only these:**

- **The data** — the current store, not `c120cfd5`.
- **The separation** — two populations, per §B below.
- **The position assignments** — as they now stand, which is a consequence of the new data, not a method
  change.

**The two known defects are still to be REPORTED, not acted on.** State the measured effect of the
`× 0.6` ceiling (spread at pick 1 with and without, and which positions bind) and whether your
construction inherits the noise-set plateau widths from `increasing=False` on raw pick. Those are
observations for a later owner decision. **Do not fix them in this job.** An acceptance criterion for
this job is that a reader can attribute every difference from the old numbers to the data or the
separation — never to a method you changed.

## B · TWO FITS, TWO POPULATIONS, NOTHING CROSSING

The body says "national-draft rows only", which is correct for the curve and silent on the pool. Stated
in full, because this is the whole point of the split:

| | trained on | never sees |
|---|---|---|
| **ND curve, picks 1–64** | national draftees at picks 1–64 | any rookie, pre-season or pickless row |
| **The pool level, per position** | pool entrants — ND 65+, rookie draft, pre-season draft, pickless mechanisms | any national row at picks 1–64 |

**This is not one fit with the rookies deleted. It is two fits.** A rookie's outcome shapes the pool's
price and never touches a national pick. A national draftee's outcome shapes the curve and never touches
the pool. The exclusion runs **both ways**, and the check must prove both directions.

SSP and MSD are valued at the pool but tracked separately, so they can become their own pools later.

## C · V0 IS NOT THE INSTRUMENT FOR THE POOL'S LEVEL. OUTCOMES ARE.

This is the trap #217 mapped, stated so it cannot be walked into again.

`v0_start` is **a function of position, age band and pick only** — the engine's own
`_v0_curve_assert` (i) asserts exactly that. **It carries no information about whether a player ever
played.** It is the value of the slot a player came from, not a judgement about the player.

That is why the pool's mean `v0_start` is higher for players who never played a senior game (612.41,
n=297) than for those who played at least one (550.29, n=429): the never-played group skews **younger**
— drafted at 18, delisted at 20 — and V0 reads youth as runway. The pool players who did play skew
mature-age, taken at 22–24 because they were ready, so their slot value is lower. **The inversion is an
age-composition artifact, not a signal about quality.**

So: **a mean of V0 over a population is a statement about that population's entry slots and ages. It is
never a statement about what those players turned out to be worth.** Do not set the pool's level from
one, do not sanity-check against one, and do not report a V0 mean beside an outcome-derived level
without saying which is which.

**The pool's level comes from realised outcomes on the same footing as the bust priors**, with
never-established players entered as **0.0**. A pool player who never played is a bust and counts as
one. That zero is the survivorship fix and it is the reason the outcome measure does not suffer the
inversion above.
