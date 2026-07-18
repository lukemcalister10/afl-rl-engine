# MEMO — LEG F: PHANTOM INTAKE (+1/+2) + RETROSPECTIVE BOARDS (−1/−2) · v1.0 · 2026-07-18
### Owner-ruled at item 346 ("Option B, and also make the -1/2 lens work. Makes sense to do it
### all at the same time"). The construction of record for builds F1 (writer) + F2 (read-only).
### Strawman parameters carry [OWNER] slots, sealed before render, ratified at the viewing (the
### §6 Leg-E workflow). The balanced board `06d8af60` is untouchable throughout.

## 1 — THE CONSERVATION LAW (why phantom intake exists)
At +k, exiting players shed value that in the real league returns as list spots + draft capital.
Without the intake side, +1/+2 totals mechanically bleed and every club's decay is overstated
(owner-identified, items 342/345). The lens therefore carries a PHANTOM INTAKE LAYER at +k —
report/view only, never on the balanced board, never gating, never baked.

## 2 — THE PHANTOM LAYER (build F1; all parameters sealed as strawmen, [OWNER] at the viewing)
(i) **DRAFT CAPITAL:** each club's season-Y+k picks priced at the v2 curve GROSS (current
    ownership records where the store carries them; natural-order slots otherwise [strawman]).
    Rows flagged `phantom=true`.
(ii) **FREE INTAKE:** per club per season, the expected mechanism intake priced at
    **R_realized=207** [OWNER slot; alternatives on the artifact: R_owner 220 · R_curve 471 —
    the item-343 three-candidate frame].
(iii) **EXITS (list-size conservation):** at +k a club's projected list is trimmed to list size;
    players whose projected value falls below **X = R_realized** [OWNER slot] exit; their residual
    leaves the club total; the phantom intake fills the SLOT, not the player.
(iv) **k=0:** ZERO phantom content. Balanced `06d8af60` byte-exact — the assertable invariant.
(v) **TOTALS REPORT:** per-lens totals WITH and WITHOUT the phantom layer, so its size is always
    visible and the owner rules on a seen quantity.

## 3 — RETROSPECTIVE BOARDS (build F2, read-only)
−1/−2 are HISTORY, not projection: the board re-rendered at the recorded evidence state of the
2025 / 2024 lists (vpath + list membership as recorded). NO phantom layer backward — the past's
intake actually happened. Delivered as stamped DERIVED artifacts the UI reads; never gates, never
re-litigates (no gate consumes them). If the store lacks any required history, F2 HALTS and
returns what is missing — nothing reconstructed by guess.

## 4 — GATING + UI
All F1 machinery behind **RL_LEGF (default ON)**: =0 ⇒ the Leg-E boards byte-exact (`d85901af`
lens, `06d8af60` balanced). UI: the +1/+2 view gains the phantom layer (visibly flagged); the
lens control gains −1/−2 tabs reading F2's artifacts by stamped path.

## 5 — WHAT THIS DOES NOT DO
No change to any shipped value at k=0 · no exit model enters pricing law · phantoms never
gate/bake/seal (R104.4 extended) · the incremental-currency design (326/327) remains post-v2.11 —
this layer is a VIEW using its raw material, not the currency ruling.
