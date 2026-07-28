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
