# DESIGN_S7 — THE PLAYER-LEVEL VARIANCE OBJECT AND THE λ CONVEXITY DIAL

ORDER 32 seat S7, objective B. **For owner ruling, not wiring.** Nothing in this document is
implemented; nothing touches the engine, the board or the sealed law. Companion measurement:
`CELLFANS_S7.md` / `CELLFANS_S7.json` (the pedigree-leg cell fans, prereg'd in `PREREG_S7.md`).

The law everything mirrors:

    price(p, Y) = rho(g)·P̂  +  [ D(c_u)·(1−rho(g)) + Φ(g,s)·β(g)·rho(g) ]·v0

Two legs, one ρ-blend. The production leg already has a distribution — S6 is emitting the
six-scenario production fan (`b6`: five `cond_prior_band` levels + the q97 head, priced level by
level; the mean board price is that fan through WQ6 = [.18 ×5, .10]). The pedigree leg had none
until now. `CELLFANS_S7` supplies the missing half: an empirical six-level fan for every v0 cell
(pick band × position; pool arm), on the fit's own rows, at the production fan's own levels.

---

## 1. The object: one six-level fan per player, mirroring the law level-by-level

Let k index the six levels (q10, q30, q50, q70, q90, q97). Define per player:

- `F_prod[k]` — the production leg's level-k price (S6's emit: the level-k scenario priced
  through the same `v_at_peak` pricing the mean uses). By construction
  Σ_k WQ6_k·F_prod[k] = P̂-leg contribution.
- `F_cell[k]` — the player's pedigree cell fan from `CELLFANS_S7.json` (his pick band × position
  cell on the ND route; his pool arm on a pool route).
- `F_ped[k] = F_cell[k] · ( v0 / m_cell )`, where `m_cell = Σ_k WQ6_k·F_cell[k]` — the cell fan
  **calibrated so its WQ6-mean is exactly the player's own v0**. The measured fan supplies the
  SHAPE; the sealed v0 supplies the LEVEL. This one scalar is what makes the λ=0 identity of §5
  exact, and it is honest: the raw cell mean already tracks the fitted v0 to ≤ 9% on every ND
  band (mean/v0 column in CELLFANS_S7.md), so the scalar is a small, disclosed correction —
  except on the thin pool arms (PDS 0.27, PDN 0.59, IRE 0.73), where it is large because the v0
  cell itself borrows level via K-shrink. The scalar must be printed per player, per §5-C7.

**The player fan is the law's own blend, applied at every level:**

    F_player[k] = rho(g)·F_prod[k]
                + D(c_u)·(1−rho(g))·F_ped_faded[k]          (the fade term — §2 for F_ped_faded)
                + Φ(g,s)·β(g)·rho(g)·v0                     (the persistence term — a constant add)

Three structural choices, each argued:

1. **Comonotone addition, not convolution.** The two legs are added level-by-level (best
   production case travels with best pedigree case). The alternative — convolving two independent
   distributions — requires a dependence model nobody has measured, and the law itself gives no
   licence for one: it adds the legs deterministically at the mean. Comonotone addition is the
   unique choice that (a) needs no new fitted object, (b) preserves the λ=0 identity exactly,
   (c) preserves monotonicity across levels for free. It errs on the side of WIDE total fans
   (perfect positive dependence); that bias is stated, and it is the conservative direction for a
   variance display.
2. **The persistence term Φβρ·v0 enters as a location shift, the same at all six levels.** It is
   a mean object measured by a panel regression (a persistence premium), with no distributional
   content of its own. Adding it uniformly keeps it exactly what the law says it is, moves no
   spread, and preserves the λ=0 identity. (Letting it scale with the pedigree fan would
   manufacture variance the measurement never produced.)
3. **ρ(g) is the same ρ the law prices with.** The fan converges to the production fan exactly as
   fast as the price converges to the production price. A 2-game kid (ρ small) is priced off
   pedigree, and now his fan says so too — which is the whole point: today the display would show
   him with a tiny production-leg fan and misleadingly low variance, when he is in fact holding a
   ticket in the widest distribution measured on this project (CELLFANS: band 41-64 median 1.9 vs
   q97 2301; RD arm median 0 vs q97 2086).

## 2. What a fade means for a distribution — argued from the sitter measurements

D(c_u) multiplies the (1−ρ) pedigree share of the MEAN. For the fan, "multiply every level by D"
is one option — but it is the wrong shape, and the sitter evidence says so directly.
`docs/evidence/sitter_fade_2026-08-14` (RECUT30A2, T1): the depth-2 sitter cell has mean 0.5846
of baseline but **median 0.0028, p25 = 0.0000, 121 zeros of 462, p75 0.3042** — a spike at zero
plus a long right tail, at every depth. The fade's mean reduction is produced almost entirely by
probability mass collapsing into the zero spike, **not** by the ceiling coming down: the packet's
own words are that the spike-plus-tail shape holds everywhere, and the T4 games transition shows
the zero spike thinning the moment a player has any games. Sitting, as measured, is close to a
Bernoulli gate on the whole distribution: with growing probability you get ~nothing; conditional
on escape, the surviving distribution keeps most of its reach.

So a fade should primarily TRUNCATE FROM THE BOTTOM, not scale:

- **Proposal F-A (recommended): zero-collapse to the fade.** Choose the smallest set of lower
  levels whose WQ6 weight absorbs the fade, i.e. push q10 (then q30, then q50 …) to 0 until the
  remaining WQ6-mean of the fan equals D·(cell mean), scaling only the one boundary level for the
  remainder. Upper levels move last and least. This reproduces the measured shape (spike grows,
  tail survives) and is exactly what the owner's "lottery ticket" instinct says a sitter is.
- **Proposal F-B (the naive alternative, stated for the ruling): scale all six levels by D.**
  Simple, monotone, but contradicts the measurement — it shows a deep sitter as a narrow cheap
  fan (ceiling 2301 → 240 at D≈0.10), when the measured deep-sitter cells still carry real
  right-tail mass. F-B systematically UNDERSTATES exactly the players the dial exists for.
- Either way the faded fan is re-anchored so Σ WQ6·F_ped_faded = D·v0: the mean board is
  untouched by the choice; only the displayed shape differs. Where a measured depth-N conditional
  fan resolves (the sitter cells n ≥ the prereg floors), a later order could REPLACE the
  synthetic faded fan with the measured one — flagged as measured-vs-constructed. Thin depths
  stay constructed; nothing is silently smoothed.

## 3. The λ dial — how a convexity slider consumes the unified fan

One scalar λ per view (not per player). Display price:

    price_λ = Σ_k  w_k(λ) · F_player[k],      w_k(λ) = WQ6_k · e^{λ·(k − k̄)} / Z(λ)

with k the level index (1..6), k̄ the WQ6-mean index, Z(λ) the normaliser. Properties, all
mechanical:

- **λ = 0 ⇒ w = WQ6 exactly ⇒ price_0 = the board price, to the digit** (given §5-C1). The mean
  board is a POINT ON THE DIAL, not a separate mode.
- λ > 0 tilts weight toward q90/q97 — the lottery view; λ < 0 tilts toward q10/q30 — the floor
  view. price_λ is monotone non-decreasing in λ (exponential tilting of a monotone fan), and
  bounded by F_player[q10] and F_player[q97] at the extremes.
- The dial consumes the UNIFIED fan, so it automatically expresses the owner's intuition: for a
  veteran (ρ≈1, tight production fan) λ barely moves the price; for a late-pick sitter the same λ
  moves it a lot. Convexity preference prices exactly where variance lives.
- Tilting the six weights is preferred over tilting the underlying scenario levels because the
  levels are measured objects; the weights are display policy. The dial never manufactures an
  outcome that was not in the fan.

## 4. What stays OUT of the sealed law — said plainly

- **The board's ruler stays the mean.** price_λ is a display/decision layer. The sealed law, the
  numeraire s, the no-arb instruments, the movers ledger, every gate — all continue to read the
  λ=0 mean board and only that.
- **The instruments police the mean board only.** If a user trades on a tilted view (λ ≠ 0), the
  no-arb margins, parity checks and the ledger will value both sides at the MEAN. A λ-tilted
  view can therefore recommend trades the mean board scores as value-losing, and no instrument
  will flag the tilt — that is not a leak, it is the definition of a convexity preference, and it
  must be displayed as such (the UI should show price_λ NEXT TO the board price, never instead of
  it). Conversely, no new arbitrage is created against the house: nothing settles at price_λ.
- **No fan number enters any fitted object.** ρ, D, Φ, β, v0 and the production leg are upstream
  of the fan; the fan is strictly downstream of all of them.

## 5. Coherence checks the eventual implementation must pass

- **C1 — the λ=0 identity:** for EVERY player, Σ_k WQ6_k·F_player[k] equals the board price to
  1e-9, exactly (asserted over the full board, the same style as the assert wall).
- **C2 — monotone fans:** F_player[q10] ≤ … ≤ F_player[q97] for every player. (Holds by
  construction if F_prod and F_cell are monotone and the calibration scalars are positive —
  assert anyway.)
- **C3 — dial monotonicity:** price_λ non-decreasing in λ for every player; price_0 = board.
- **C4 — refresh lineage:** the fan artifact stamps the md5s of the v0 surface
  (`HEADFIX_31F`-lineage), the pool cells (`POOL31F`-lineage) and `CELLFANS_S7.json`. Any v0
  refit ⇒ the cell fans MUST be re-measured and re-calibrated; a fan emitted against a stale v0
  md5 halts, it does not display.
- **C5 — bounds stay bounds:** a level flagged `BOUND(max)` in CELLFANS (every `*`, and every
  n<8 cell) must surface flagged in any display (as "≥", or suppressed by ruling — see Q4),
  never as a point estimate.
- **C6 — fade conservation:** under either fade proposal, Σ WQ6·F_ped_faded = D·v0 exactly, so
  C1 survives sitting at every depth, continuous clock included.
- **C7 — calibration disclosure:** the per-player scalar v0/m_cell is printed; a scalar outside
  a declared band (say [0.5, 2]) flags the cell for owner review rather than silently rescaling
  (today that flag would fire exactly where it should: PDS/PDN/IRE).
- **C8 — no engine reads:** a grep-provable property that no engine/board/instrument code path
  imports the fan or λ (the 31-F "provably inside the dial" control style, applied to this
  layer).

## 6. Open questions for the owner

- **Q1.** Should the dial also tilt the D fade on sitters — i.e. should λ > 0 read a sitter
  through proposal F-A's surviving tail (the measured spike-plus-tail), rather than through the
  scaled fan of F-B? The sitters are the purest lottery tickets on the board; F-A vs F-B is the
  single choice that most changes what the dial shows on them.
- **Q2.** For a low-games non-sitter (the 2-game kid), should the pedigree fan re-condition on
  the games transition (the T4 `D(k games by depth)` cells show the zero spike thinning with any
  games), or stay the entry cell fan until ρ takes over? Re-conditioning is more truthful and
  more machinery.
- **Q3.** Cell resolution for display: the player's fan currently keys on pick band × position;
  where that cell is thin (RUCK 1-10 n=7) do you prefer the position-pooled band fan (wider
  support, declared borrowing) or the bounded thin cell (no borrowing, bounds shown)?
- **Q4.** Should `BOUND(max)` levels display as "≥ x", or should q97 be suppressed on cells that
  cannot resolve it (n < 34)?
- **Q5.** Is λ per user, per view, or one board-wide dial? (Design assumes per view; nothing
  settles at price_λ either way.)
- **Q6.** Comonotone addition of the two legs (§1) deliberately shows the WIDE reading of total
  variance. Acceptable as the displayed convention, or do you want an owner-ruled note on every
  fan that the legs are coupled best-with-best?
- **Q7.** Should the thin pool arms (PDS/PDN/IRE), whose v0 leans on K-shrink borrowing and
  whose raw means sit at 0.27–0.73 of their signed cells, display the pooled pool-arm fan
  instead of their own bounded arm fans until their cells resolve?

## 7. Non-goals, restated

No wiring. No engine, board, law, store or instrument edit. The ruler is the mean and stays the
mean. This document plus `CELLFANS_S7` is the complete input the owner needs to rule the variance
layer; implementation is a later order's work, gated on that ruling.
