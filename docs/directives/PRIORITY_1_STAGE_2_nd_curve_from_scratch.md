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

---

# ADDENDUM 2 — 2026-07-28, seam pre-fire audit after #217 landed. Amends by addition; nothing above is edited.

#217 merged to `main` at `6634221`. The sequencing precondition in the header is **satisfied** — the split
and Addendum 1's exclusion are on `main` and this job is clear to start. Five things in the body are now
stale, and the first would send you backwards.

## 1 · THE `v0surf` HALT IS THE DESIGN. IT IS NOT A FAULT, AND YOU WILL HIT IT.

The Rules section says the pickle is stale and *"the engine silently falls through to a refit path."*
**That is no longer true and must not be acted on.** #217 regenerated and re-pinned the pickle and
**deleted the silent fallback**. An unknown config signature now **HALTs**, naming its own signature and
the regeneration command.

**You will trigger this halt**, because changing the fit population changes the signature. That is
correct behaviour reporting itself, not a defect to route around. **Do not restore a fallback, do not
widen the accepted-signature set, and do not treat the halt as a blocker to be removed.** Regenerate
deliberately:

    RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 session_2026-07-18/legf6/scripts/refit_v0surf.py --bake

The bake freezes **every** surface a build fits, not just the shipped one — `_build_v0_curve` runs three
times per build, and the old pickle froze only the last, so the first two always live-fitted.

The signature attribution in the body is also wrong and was corrected by #217: pristine `main` computed
`90a937e7`, which was *also* absent from the pickle — **`main` was already on the refit path before the
split existed.** The real chain is `90a937e7 → d702e463 → 76498b5a`. The split did not cause the
fallthrough; it revealed it.

## 2 · THE EXCLUSION CHECK ALREADY EXISTS. ONE DIRECTION OF IT.

The body tells you to prove no pool row contributes at picks 1–64 and to show the check failing. **Do not
build that — it is on `main` and it is the instrument you inherit.** Five fit sites register the actual
row list they sample (`build_pvc`, `build_pvc_v34`, `_natcv`, `_natcv34`, `v0_kernel`) and the selftest
inspects those recorded populations rather than recomputing them, so a correct helper cannot mask a
broken call site. Seam-verified: breaking any one site alone fails the suite naming that site, and
deleting a registration fails too.

Note when reading a failure: `_natcv` windows on the **raw pick** while the others window on the slid
`_pvc_eff`, so they produce genuinely different contamination profiles.

**What does NOT exist is the other direction.** §B requires the exclusion to run both ways and the check
to prove both. Only *"no pool row teaches the national curve"* is built. **"No national 1–64 row
contributes to the pool level" is yours**, to the same standard: it must fail, by name, when lifted.

## 3 · THE POOL POPULATION FIGURES IN THE BODY ARE WITHDRAWN NUMBERS.

`575.89 / 612.41 / 550.29` were measured on the refit surface and #217 restated them on the frozen
surface: **580.04 / 618.31 / 553.12** (n unchanged at 763 / 297 / 429). Quote the frozen-surface figures.
**The conclusion is unaffected and still binds** — the inversion holds, never-played still sits above
played, so no pedigree mean may set the level.

## 4 · THE ENVIRONMENT, CONCRETELY — THIS HAS COST THREE SEATS.

The known fault is real and measured live: bare `python3` resolves to **3.11** while
`requirements-lock.txt` pins the **cp312** wheel, and system pip is PEP 668-blocked. Do not weaken the
pin. What works, verified by the seam in this container:

    python3.12 -m venv <venv> && <venv>/bin/python -m pip install --require-hashes \
        --only-binary=:all: -r requirements-lock.txt
    RL_VENV=<venv> bash bootstrap.sh          # bootstrap.sh honours RL_VENV; do not patch it

`bootstrap.sh` already prefers `$RL_VENV/bin` on PATH, so the pinned env is used without editing
anything. #231 is repairing the script itself; until it lands, use the above.

## 5 · REGENERATING `v0surf` VS THE "NOTHING RE-PINNED" FENCE — RULED.

The body says *"Nothing is adopted, baked, re-pinned or released here."* Regenerating `v0surf` re-pins it
in `data/expected_boot.json`, so read literally the fence and the halt trap you between them.

**Seam ruling, reversible by one owner sentence:** regenerate and re-pin **in your own working tree and
on your own branch** — that is a working necessity and is not adoption. **Do not land it on `main`, do
not move the board of record, do not touch the shipped UI bundles.** The fence's intent is that nothing
this job produces becomes the shipped baseline without the owner's separate word, and that intent is
untouched by a local re-pin.

Also, from #217's close-out: `refit_v0surf.py`'s clean-instance precondition tests *balanced board ==
`06d8af60`*, which is **pre-split and unreachable**. You cannot satisfy it as written. State what
cleanliness evidence you do have — intra-box determinism across repeated refits, and board reproduction
against a known reference — and say plainly that the literal precondition could not be evaluated. Do not
manufacture a substitute and call it satisfied.

## 6 · COORDINATION

#231 is in flight and also touches `data/expected_boot.json` and `bootstrap_env.sh`. Neither of you lands
to `main` without the seam sequencing it. Flag it rather than resolving a conflict yourself.

**Everything in the body and Addendum 1 that is not corrected above still stands** — in particular the
owner's specification at the top, apples-for-apples with the method held constant, and the fence on what
you may decide.
