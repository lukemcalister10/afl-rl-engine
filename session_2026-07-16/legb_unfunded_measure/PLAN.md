# PLAN — LEG-B UNFUNDED MEASUREMENT (dev-toggle, ships nothing) · 2026-07-16 · seat 10

**First committed artifact (MODE: auto).** This build MEASURES the DECIDED output-anchored family
(memo v1.3 §2) with the §3 per-position conservation renorm turned OFF (C≡1), against the frozen
instruments, at five measurement points. NO SELECTION IS MADE. NOTHING SHIPS. The bar/grid returns
to the owner with the numbers.

## AUTHORITY / FEED (documents, verified at directive)
- Engine/store base — STRICT: branch `claude/legb-segment5-law-grid-flq57f` @ **`91d08f2`** (verified
  by full-URL ls-remote; NEW branch `claude/legb-unfunded-measurement-1f7vym` cut from it).
- Boot identity at base (data/expected_boot.json): store `b1fd0bce` · rl_model `f79fc740` ·
  board **`8d90c9ac`** (the A/B target) · engine_head `a83c9f6d` · config `c2d233ae…`.
- MEMO `docs/MEMO_LEGB_functional_form_2026-07-16.md` md5 `cf6c0080…` ✓ (verified).
- Acceptance `docs/acceptance_v1_20.json` md5 `6b83e336…` ✓ (verified).
- Frozen β: `session_2026-07-16/uncompress/beta_measure.py` md5 `14c59139…` ✓ (asserted at run).
- Register items 254/255/256/257 (owner's ruling: conservation is NOT his law; unfunded value
  permitted; guards = G-COHORT + SINCERITY; owner word 257 = "Measure").

## THE MECHANISM (located, verbatim)
- The §3 per-position conservation renorm is **C[pos]** (`_UC_C`), built at load time
  (`_merged_recover.py:1368–1379`) and APPLIED at the single hook site
  (`_merged_recover.py:332`): `return _UC_C.get(pos,1.0)*v0p+delta`.
- The un-compress map (`_uncomp_prod`, `:308–332`) is INERT unless `RL_UNCOMP` on AND `RL_UNCOMP_S`
  set. `UNCOMP_S_DEFAULT=None` ⇒ default board is `8d90c9ac` byte-exact (the A/B identity).
- `MA` in `_merged_recover.py` binds `rl_model`; the kill-switch/dial block lives at
  `rl_model.py:329–335` (the `RL_ISOFADE`/`RL_UNCOMP_S` env pattern).

## §1 — THE TOGGLE (`RL_UNCONSERVE`) — one clean commit, then MINI-CHECKPOINT HALT
- New dev-override `RL_UNCONSERVE`, mirroring the `_UNCOMP` pattern, declared in `rl_model.py`
  next to the uncompress block: `_UNCONSERVE=os.environ.get('RL_UNCONSERVE','0')=='1'` (default OFF).
- `=1` ⇒ the applied C is identity (C≡1) on the un-compress map: at `_merged_recover.py:332` the
  renorm factor becomes `1.0` instead of `_UC_C.get(pos,1.0)`. Load-time C is still *computed*
  (its print/table is a measurement byproduct) but *not applied*.
- unset/`0` ⇒ shipped behaviour BYTE-EXACT — the change is a pure no-op when the flag is off.
- **Shipped constants UNTOUCHED (FENCE): `UNCOMP_S_DEFAULT` stays `None`; `UNCOMP_DECAY` stays 0.25.**
- One clean commit. Then a **mini-checkpoint HALT** (≤5 lines + diff SHA) for the supervisor's diff
  prescreen **before any measurement**.

## §2 — A/B (in the same toggle commit's verification, dev-shell)
- Toggle unset ⇒ default board `8d90c9ac` BYTE-EXACT (RL_UNCOMP=0 identity also re-proved).
- Sanity: `RL_UNCONSERVE=1` alone (no `RL_UNCOMP_S`) ⇒ map still inert ⇒ `8d90c9ac` (the flag only
  matters once the map is active).

## §3 — THE MEASUREMENT GRID (measurement points, NOT a selection grid)
C≡1 (`RL_UNCONSERVE=1`) at **s ∈ {0.65, 0.85, 1.00, 1.25, 1.50}**. Per point, ALL VERDICTS FROM
FROZEN INSTRUMENTS ONLY (S4). Env per point: `RL_UNCONSERVE=1 RL_UNCOMP_S=<s>` (+ the pinned gate
env from grid.sh: PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72
RL_PRIOR_TREES=400 PAR_RAMPS=22). Store `b1fd0bce` untouched throughout.

Per point deliverables:
1. **β (proven-27+)** via FROZEN `beta_measure.py` (md5-assert first): β point · CI · width-rail note
   (≤0.35) · n. Also β_c (map OFF) as the anchor row.
2. **G-COHORT y4/y5/y6** via the FROZEN repo gate suite — build the candidate walk-forward matrix
   with the toggle env set (`s4_matrix_M1v7.py`, `RL_CONFIG_MODE=gate`, `S4_MATRIX=<tmp>`; `_subenv`
   passes `RL_*` through), then call `ship_gates_check._b1_july8(matrix)` verbatim: `SUM[N]`,
   `den=min(SUM[1],SUM[2])`, `ratios y4/y5/y6 = SUM[N]/den`, hard ≤1.30. THE unmeasured question of
   record: does the decided family **unfunded** hold ≤1.30? (matrix `__meta__` hashes are asserted
   against the running engine by the suite — no weakening.)
3. **E/B** = ev(`timothy-english`)/ev(`kieren-briggs`) captain-in, vs the owner's hard **1.75**.
4. **census/unearned gauge** + **position-pool Δ totals** — which pools re-rate, by how much (Σ Δnum
   per position; unearned/pick-prior population gauge). From OFF vs ON-unconserved ledger dumps.
5. **THE SINCERITY LEDGER (item 256, all 804 rows)** — from OFF (`8d90c9ac`) vs ON-unconserved
   ledger dumps (`ledger_dump.py`, `num=round(ev/1.0524)`): ΔSCAR · Δ% · rank before/after · Δrank.
   Headlines per point: top-20 rank gainers/losers · the named row **Bontempelli**
   (`marcus-bontempelli` — owner's test: SCAR up AND rank up, else reported as a FAILURE) · every
   player whose SCAR rises while rank falls, counted and named.

## §4 — HALT CONDITIONS
- Any G-COHORT breach at a point: RECORD it and CONTINUE the sweep (breach points are findings; a
  measurement job measures).
- Any guard/instrument failure to PRODUCE a verdict: SILENCE IS A RED — HALT.

## FENCE
IN: the one env toggle · the measurement grid · artifacts under
`session_2026-07-16/legb_unfunded_measure/` · the mini-checkpoint.
OUT (touch = HALT): the STORE · docs/ · config · acceptance · gate/guard code · shipped constants
(`UNCOMP_S_DEFAULT`=None, `UNCOMP_DECAY`=0.25) · any selection/hard-coding/tuning · grid values
outside the five listed.

## TIME
2–3.5 h estimate confirmed (engine loads dominate; seg-5 measured ~35 min/ON-point all-in: matrix
build + gate + β + two ledger dumps). Five ON points + β_c + A/B. Will report actual + the APP
counter; flag if actual runs >2× or <½× the estimate. The mini-checkpoint HALT gates the compute:
the multi-hour sweep proceeds only after the supervisor prescreens the toggle diff.

## SEQUENCE
1. Commit this PLAN. (done at commit of record below)
2. Implement the toggle (rl_model.py + `_merged_recover.py:332`); prove A/B byte-exact. Commit.
3. Mini-checkpoint HALT (≤5 lines + diff SHA) → supervisor diff prescreen.
4. [after prescreen] Run the five-point grid; commit artifacts (GRID.out, per-point ledgers,
   SINCERITY_*.csv, MEASURE.md) under `session_2026-07-16/legb_unfunded_measure/`.
5. RETURN: ≤30 lines + plain-terms close; disposition returns to the owner.
