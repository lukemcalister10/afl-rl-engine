# P5-5 — Exit risk counted once, at the source (HIGH; owner word + blind review)

**Depends on.** P5-4 (the RL_LSYM_TAB env override becomes a module constant; the re-derivation needs it).
P4-3. Serial rule: engine + rl_export.py.

**Done when.** Exit risk on the +1/+2 lenses has ONE carrier: the fitted survival S_k(age, games) applied to every
projected row, with r_pop (the L-SYMMETRY damper's sealed rate) re-derived WITHOUT its exit component and re-sealed;
the export-layer within-cohort rule (the 2026-10-14 survival act) retired in the same act; the owner has seen the
three measured variants with movers by age and evidence, a blind review is filed, and the act lands on his word.

**Facts (checked at ffb2663b).**
- LEG F4 / L-SYMMETRY damper: _merged_recover.py:267-403. The sealed literal `_LSYM_SEAL` (:294-296):
  r_pop = 1.0016 (18), 1.0007 (20), 0.9777 (22), 0.9073 (24), 0.7886 (26 through 36), 0.6591 (38), seal
  `r_pop_sha256_8` c62b5ee8; s(age) = 0 (18-22), 0.048 (24), 0.5988 / 0.6053 / 0.5988 / 0.426 (26-32), 1.0 from 34
  (s = 1 means UNDAMPED: the damper is inert from 34, so a 36-year-old's +2 carries none of r_pop's exit component), seal
  `s_sha256_8` efe97ee3. r_pop is "measured on the committed -2/-1/now boards INCLUDING exiters' realized residual
  paths" (:270-273, :288-291) — that is where exit risk is embedded. RULEBOOK law 5 (L-SYMMETRY) governs it.
- The re-derivation hook today: `os.environ.get('RL_LSYM_TAB')` (:299; P5-4 turns it into a module constant).
  The original derivation chain: session_2026-07-18/legf4, legf5 (MEMO_LEGF v1.3 §2.ix is cited at :285-286).
- The within-cohort capped rule lives at the export layer: rl_export.py:274-300 (survival_hazard.apply over the
  charged rows, `CAP_LIFT` the measurement switch), calibration data/survival_hazard.json, fit by
  engine/rl_after/ingestion/fit_survival_hazard.py. Its disclosed double count: 1.27% of the 26-32 vP1 total and
  2.76% of vP2 (docs/evidence/engine_survival_hazard_2026-10-14/MEASURED_TABLES_F1.txt; rl_export.py:292-295).

**Change.** Measure first, on scratch copies, three variants: (a) S_k applied absolutely to every projected row
(H1) with r_pop re-derived on the same boards EXCLUDING exiters (and s re-bisected so the damped median vP1/v per
age reproduces the new r_pop, as the seal's own method says, :290-291); (b) as (a) with never-played rows kept at
pick price; (c) as (a) plus the owner's reconciliation check (players + entrant layer within 2-3% of present).
Then implement the chosen variant: new `_LSYM_SEAL` literals with recomputed sha256_8 seals and the derivation
script committed; survival applied at one site; the rl_export within-cohort block deleted.

**Must not change.** Present v; vM1/vM2; the picks ladder; the frozen v0-surface signature; config (unless the
variant needs a dial — then it is a declared config move via P4-3).

**Prove it.** One measurement build per variant (lens totals, movers by age band and by games band, the named
veterans: Zorko, Gawn, Pendlebury at +2); the reconciliation numbers; blind independent review (law 11); the
landing gate set; acceptance `--profile full`; the as-at harness control (present untouched ⇒ 0 diffs).

**Lands via.** Lever act on the owner's word, movers shown first (RULEBOOK P1), `moves: [engine_head, board]`.
