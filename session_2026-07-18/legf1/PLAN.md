# LEG F1 — THE PHANTOM INTAKE LAYER — PLAN (job 1)
seat 13 · 2026-07-18 · branch `claude/legf-phantom-intake-build-dvbipz` (harness-assigned working branch;
maps to the directive's `claude/legf1-phantom-intake-<suffix>`) · base `cc58570` (Leg-E tip; docs stay on MAIN).

## 0 — ENTRY (see ENTRY_PROOF.md, discriminator.txt, REPRODUCIBILITY_ANNEX.md)
- GIT anchor `cc58570…5adc` STRICT **PASS**. Store **968de0c7** + curve file **56dd7a7b** byte-exact **PASS**.
- Board-hash entry assertions do **not** reproduce here (30d96f1f/83a4b21d/86444a70 vs filed
  06d8af60/d85901af/9829d01a). **Root cause proven environmental**: OpenBLAS DYNAMIC_ARCH last-ULP weather
  confined to 6-dp float display fields; store/curve/engine files byte-identical; kill-switch equivalence
  exact. **Supervisor item 347**: proceed CONTAINER-RELATIVE with (1) discriminator + (2) reproducibility
  annex — both committed. Discriminator: filed 10-value panel reproduces **10/10, max|Δv|=0, 0 rank moves**
  ⇒ the gap is weather, not a defect. BLAS finding carried as the headline for reconciliation.

## 1 — CONTAINER BASELINES (all container-relative proofs target these)
| config (dev-shell) | this container | filed |
|---|---|---|
| RL_LEGE=0 RL_PVC2=1 (balanced k=0) | `30d96f1f` | 06d8af60 |
| RL_LEGE=1 RL_PVC2=1 (default / Leg-E lens) | `83a4b21d` | d85901af |
| RL_LEGE=0 RL_PVC2=0 (RL_PVC2 kill) | `86444a70` | 9829d01a |

## 2 — SEALED STRAWMAN VECTOR (the §6 law — HASHED BEFORE ANY RENDER)
`sealed_strawman.json` sha256 = **1d180424dc86dd4f7bcbbd54b7b177fab0f08665720dd03162d73a0f1497ac3c**
(recorded in `sealed_strawman.sha256`). Free-intake **R=207**, exit bar **X=207** (alternatives 220/471
labelled only), draft capital = picks 1..30 v2-curve GROSS attributed natural-order round-robin over the 18
clubs (alphabetical strawman order), list-size conservation `refill==exit` (no exogenous L), `phantom=true`
on every intake row. **One structural strawman FLAGGED** (draft picks consume exit slots vs add-on-top) —
sealed to the memo-§1 reading, ratifiable at the viewing.

## 3 — DERIVED FENCE (the 322 law — derived HONESTLY from the jobs; NARROWER than "expected")
The whole phantom layer is a **pure export/view addition**: draft capital reads `PVC`, free intake/exit read
the already-computed `vP1/vP2` + the `club` field, totals aggregate the board. It needs **no engine change**.
Keeping the engine byte-identical makes the balanced board untouchable **by construction**, not just by proof.
- **IN (touched):** `engine/rl_after/rl_export.py` (phantom layer + totals + the RL_LEGF gate) ·
  `ui/app/board.js` (phantom-row flag + −1/−2 tabs) · `session_2026-07-18/legf1/` (proofs).
- **Deliberately NOT touched** (listed "expected" but derived out): `rl_model.py`, `distribution_pricing.py`
  — touching the engine would risk the balanced board; the layer is view-only, so they stay out. The
  RL_LEGF gate lives entirely in the export (a lens/display kill-switch like RL_LEGE's export half).
- **HARD-OUT (held):** the store · the curve · `_merged_recover.py:1121-1171` · pins/acceptance · `docs/` ·
  SEASON_PROG · F2's session dir (`session_2026-07-18/legf2/`).

## 4 — JOBS (rl_export.py additive block, all under `if RL_LEGF`)
2. **DRAFT CAPITAL** (§2.i): per-club natural-order picks 1..30 at PVC gross, `phantom=true`.
3. **FREE INTAKE** (§2.ii): per-club per-lens free-intake slots at R=207.
4. **EXITS** (§2.iii): per club per lens, vP_k<207 exit (residual leaves total); slots refill phantom
   (draft picks then free intake), list size conserved. Structural reading per the sealed flag.
5. **TOTALS** (§2.v): `phantomTotals` — per club + league, per lens, WITH/WITHOUT phantom; per-pick, no bins.
6. **UI** (board.js): phantom rows visibly flagged on +1/+2; lens control gains −1/−2 tabs reading F2's
   artifact path (stamp-asserted at load; empty-state safe if F2 not landed).
7. **GATE RL_LEGF** (default ON): =0 ⇒ the export emits none of §§2–5 ⇒ board byte-exact to the Leg-E
   baselines (83a4b21d default / 30d96f1f balanced).

## 5 — CHECKPOINT LAW (BINDING) + PROOFS
The balanced board cannot move. Because the engine is untouched and the phantom keys are additive
lens-scoped arrays, the k=0 `active[*].v` column is byte-identical RL_LEGF on vs off — proven by a keyed
0-mover diff. Per-commit intent honoured; the byte-exact + 0-mover proofs are captured SAME-CONTAINER at
EXIT (build cost ~90s each). Any k=0 `v` mover of any kind ⇒ HALT, commit nothing further, return the diff.

## 6 — EXIT
Frozen panel (10/10) · RL_LEGF=0 byte-exact (83a4b21d/30d96f1f) · RL_LEGF=1 0 k=0 v-movers · Guard-5 red =
the known pre-bake class (flag, never self-pin) · store 968de0c7 held · README(artifact→stamp) · PR · RETURN.
