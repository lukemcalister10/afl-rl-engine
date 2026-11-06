# P5-6 — A smooth fitted surface replaces the five-point level average (HIGH; owner word + blind review)

**Depends on.** P4-3 (the new artifact's identity), P5-5 (same lenses; one value act at a time). Serial: engine.

**Done when.** `_prod_path` reads one pinned, fitted smooth surface over (level, exposure, games) instead of
re-pricing each live-season row five times on the level axis and three times on the games axis; the surface is a
pinned build input with its fit script committed and a signature halt like v0surf; the owner has seen the diff and
the step-removal demonstration, a blind review is filed, and the act lands on his word.

**Facts (checked at ffb2663b).**
- _merged_recover.py:2912-2952 `_prod_path`: for a row with a live-season row, Y == BASE_REF and not first-evidence,
  it prices avg −1, −0.5, 0, +0.5, +1 and takes the mean (:2920-2935, "owner-approved 2026-10-13"; four extra
  raw_ev × iso_eff calls per row); the first-evidence family gets a ±1-game 3-point average (:2936-2952). Scope is
  Y == BASE_REF only: vM1/vM2 and harness as-of years are not smoothed (:2925-2926).
- The band it smooths is the GBR prior (data/q97m.pkl, data/cm_400.pkl; boot_guard.py:212-232 pins the fitted
  artifacts, :237-280 the loaded-path checks).
- Owner (2026-10-14): "Quality is important. Is there a better way to do the smoothness that doesn't take the
  machine time?" — the grid surface was the answer given.

**What a new pinned surface needs (none of it exists yet).** An expected_boot.json field and a TRACKED_IDENTITIES
entry (spec.py:43-45); then EITHER a NO_WRITER identity (spec.py:66 — the q97m pattern: moves only at a bake, never in
a landing transaction) OR a PIN_MEASURERS entry (steps.py:93-104 — the v0surf pattern; FLIP_SCOPED unless P4-3 made it
movable). The steps.py:120-124 import-time cross-asserts must still hold. Add it to proofstash BUILD_INPUT_FILES
(:59-62, bump KEY_SCHEMA), to boot_guard's _FITTED and loaded-path checks, and to carriers.py only if a landing writes it.
Choose and say which; "like q97m" means NO_WRITER — it cannot be written by the lever act that adopts it, so the
artifact and its pin arrive in the act's input commit.

**Change.** Fit (once, offline, script committed) a monotone smooth surface of the band's prediction over a fine
(level, exposure, games) lattice — e.g. a tensor-product P-spline, or an isotonic-in-level grid with bilinear reads;
pickle it with a deterministic signature; `_prod_path` reads it for every lens (not only Y == BASE_REF). Delete both
moving averages.

**Must not change.** Store; picks ladder; the v0 surface; config (unless a dial is needed — a declared move).

**Prove it.** Measure first: the surface board vs today's board on the present lens (median, p90, largest |Δ|) shown to
the owner; the single-game and single-score steps removed on BOTH axes (the Ash +3x case and the ~70 young players
named in the 2026-10-13 act's evidence); every lens, the as-at boards included, re-priced (`tools/harness
…/pass_asat_seasons.py` — they move too: show them); build time before/after; blind review; the landing gates.

**Lands via.** Lever act on the owner's word (RULEBOOK P1 movers first; law 11), `moves: [engine_head, board, …]`.
