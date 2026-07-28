# ITEM 207 · Priority 1 Stage 1 — what the restructure moved

Measurement only. Nothing adopted, baked, re-pinned or released. No product byte written.

**Pinned to:** base `85e39ee`, store `c120cfd5` (1,808,700 B, 2,651 players), board `fa172ac1`
(1,255,256 B). All three verified by md5 and byte size after checkout, and re-verified on this branch.
The repo was shallow on arrival; `git fetch --unshallow` was run before any ancestry claim. This
branch sits three docs-only commits above the pin; the product tree is byte-identical to `85e39ee`.

**Owner rulings applied, 2026-07-28.** D1's densification stands and the boundary table is the stale
side. Matt Maguire's removal was intended. The table is **not** to be repaired. Both rulings were
already specified in `ITEM_411_store_restructure_charter.md` before D1 ran — see §1 and §2.

---

## 1. The boundary table is stale, and the mechanism it feeds is being deleted

`engine/rl_after/national_draft_last_pick.json` disagrees with store `c120cfd5` for four years.

| year | table says | store says | gap |
|---|---|---|---|
| 2009 | 68 | 67 | −1 |
| 2010 | 93 | 77 | −16 |
| 2011 | 89 | 80 | −9 |
| 2019 | 65 | 64 | −1 |

The table matches the store exactly across all 23 years at every earlier point — `04f38dad`
(11 Jul, where it was derived), `968de0c7` (17 Jul), and `f37d9716` (immediately pre-D1). It
disagrees only at `c120cfd5`. Zero mismatches before D1, four after.

**This was specified, not accidental.** Charter Amendment 2 (2026-07-24, owner rulings on issue #146)
line 102: `stream_pick` is "the compressed entrant order, exactly the integer sequence 1..N per
populated group — not the raw AFL selection number. **Gap-compression edits are lawful under this
convention.**" D1 densified 2010 from a gapped 1..93 to a dense 1..77, 2011 to 1..80, 2019 to 1..64 —
173 ND rows renumbered in total (74 · 69 · 30). That is the convention being applied. 2009 moved for
a different reason, covered in §2.

**Owner ruling:** the new numbers are correct and the table is stale, but it is **not repaired**.
Its only consumers are `rl_model.py:209` and `:215` — verified: `_NDC` appears nowhere else in the
engine, and no other file in `engine/`, `ui/`, `tools/` or `verify/` reads the sidecar. Both lines do
the same thing, convert a rookie pick into a national-draft-equivalent number, and that conversion is
being removed under R-STREAMS (§4). Repairing it would maintain a mechanism scheduled for deletion.

**The cost while it survives**, for the record. `_eff = min(99, last_national_pick[year] + pick)`.
Filtering on `type` first: 160 rows are `RD` in the four affected years, and after the `min(99)` cap
absorbs part of the error, **84 carry a wrong effective pick** — 1 to 16 slots, mean 4.6, always
deeper than the store now supports. By year: 2009 · 31, 2010 · 21, 2011 · 18, 2019 · 14. The board of
record `fa172ac1` was built through this.

*Note on the `type == 'PSD'` branch at `:211`:* it matches nothing, because charter Amendment 2
line 105 consolidated PSD into RD with no PSD rows remaining. Dead by design, and deleted with the
rest.

## 2. Matt Maguire — closed

Charter Amendment 2 line 106: "Matt Maguire is REMOVED ('should never have been in the store')."
Owner-authored, 2026-07-24. He was 2009 ND pick 68, 71 games, retired; his removal is the whole of
the 2,652 → 2,651 row change and the whole of the 2009 boundary move. Intended. Thread closed.

## 3. The unknown root — confirmed, and it is the finding

`bust_prior_table.json` and `params.json` have **no producer anywhere in the repository.** Searched
every `.py`, `.sh`, `.ipynb`, `.yml` and `.json` in the tree, including all 24 session directories,
for direct writes, variable-indirected writes, and every mention of either filename. Every hit is a
read, a pin registration, or a corruption-proof test. Neither carries any provenance stamp.

`build_peak_model_v4.py` takes `bust_prior_table.json` as a model input, so the chain
`priors → peak model + snapshot → pick curve` has a root nobody can re-derive. `params.json` holds
`AGE_CURVE`, `PEAK`, `PEAK_AGE`, read at `rl_model.py:29`. The project already says as much in its
own code — `single_source.py:36` calls the boundary sidecar "a classified static input, like
params.json".

These are hand-set numbers. They cannot be recalculated against the new store because nothing that
calculates them exists.

## 4. R-STREAMS — the blend the charter was written to remove

Charter line 8: "The rookie draft and national draft are separate mechanisms and must be valued as
separate streams; the historical blend let rookie picks needlessly prop up the ND tail." Line 57: the
pricing rebuild "prices the two streams as separate entrant distributions."

The engine has not implemented it. The cohort at `rl_model.py:220` is
`_grp in ('ND','RD')`, 2003–2021, `pos in GRP` — one blended pool. Measured against `c120cfd5`:

| | players |
|---|---|
| fitting pool | **1,975** |
| national draft | 1,318 |
| **rookie-drafted** | **657 — 33.3%** |

(After the three `_pvc_exclude` rows drop: 1,972 / 1,315 / 657, unchanged at 33.3%.)

A third of the population the pick curve is fitted over enters at a chained effective pick derived
from the boundary table in §1. That is the contamination R-STREAMS names, and it has never been
quantified. The two-way fit — as it stands, and with rookie-drafted players out of the pool — is the
centrepiece of the remaining work.

## 5. The stream fields are inert by design — a fact, not a defect

D1 added `draft_stream`, `stream_pick`, `stream_year` and nothing reads them. Charter Amendment 1
line 65 says new stream fields "move nothing in the current world; feed the panel, harness, and
pricing rebuild." That is the specification working as written.

Measured across all 2,651 rows, the fields are exactly redundant with what the engine already reads:
`stream_pick` == `pick` (0 differences), `stream_year` == `year` (0 differences), and `draft_stream`
== a coarsening of `type` (0 differences — ND 1569, RD 693, MSD 106, SSP 52, OTHER 231 = UNR 59 +
IRE 57 + PDA 51 + PDN 43 + PDS 21). Recorded so the next seat does not re-derive it.

*Correction to CURRENT_STATE:* it gives the populations as "2,651 / 2,651 / 2,368" for
draft_stream/stream_pick/stream_year. Measured: 2,651 / 2,368 / 2,651 — the last two are transposed.

## 6. The nine artifacts — and a tenth

| # | artifact | fitted on | producer | pinned |
|---|---|---|---|---|
| 1 | `data/q97m.pkl` | no record | `refit_q97m.py` | ✔ q97m |
| 2 | `data/v0surf.pkl` | no record | `session_2026-07-18/legf6/scripts/refit_v0surf.py` | ✔ v0surf |
| 3 | `engine/rl_after/peak_model_v4.pkl` | no record | `build_peak_model_v4.py:71` | ✔ peak_model |
| 4 | `engine/rl_after/pvc_snapshot.json` | no record | same script `:84` — co-emitted | ✔ pvc_snapshot |
| 5 | `engine/rl_after/bust_prior_table.json` | no record | **none found** | ✔ bust_prior |
| 6 | `data/cm_400.pkl` | no record | none found | ✔ band |
| 7 | `engine/rl_after/pvc_curve_v2.json` | **declares `968de0c7`** | `derive_pvc2.py:231` | ✗ |
| 8 | `engine/rl_after/params.json` | no record | **none found** | ✗ |
| 9 | `engine/rl_after/national_draft_last_pick.json` | 11 Jul, store `04f38dad` | `job4a_national_last_pick.py` | ✗ |
| **10** | `engine/rl_after/pvc_curve_L1b.json` | no record | none found | ✗ |

The pick curve's stale source is read from the artifact: `stamp.store_md5` = `968de0c7`,
`derived_from` = `"out/per_entrant.json (base 968de0c7)"`. The store has moved twice since.

`pvc_curve_v2.json` carries an internal note reading "Candidate ONLY" — stale text. Its gate
`RL_PVC2` defaults to `'1'` (`_merged_recover.py:1561`), so it is live. **`pvc_curve_L1b.json` is a
genuine tenth artifact** that was not on the list of nine: it is the adopted pick-side artifact
(`rl_export.py:122`) and the fallback whenever `RL_PVC2=0`. Unpinned, unstamped, unmeasured.

## 7. Environment

`bootstrap_env.sh` **fails on this container as invoked**, deterministically, and it is not the
OpenBLAS.

`requirements-lock.txt` pins numpy 2.4.4 by hash `81f4a14b…`, which is the **cp312** wheel. This
container's `python3` is 3.11.15, so pip resolves the cp311 wheel, `df377529…`, and
`--require-hashes` halts. The download is sound: `df377529…` is exactly what PyPI declares for that
file, and two independent fetches gave the same digest. Every wheel in the lock is cp312, so any
container whose default `python3` is not 3.12 can never pass.

**The fix already exists elsewhere in the repo.** `.github/workflows/live-scoring.yml:64–76` pins
Python 3.12.3 and then runs a step named "Ensure python3.12 on PATH" that symlinks it if absent. The
local bootstrap path never got the same treatment — `bootstrap_env.sh` runs bare `python3`.
`/usr/bin/python3.12` is present here; under it the pinned install completes hash-verified with the
lock file untouched, and both scripts pass — `[env-pin] OK: numpy 2.4.4 + bundled OpenBLAS
05c9f9eb… (byte-exact to the pin)`, then `bootstrap OK` with Guard 5 confirming store `c120cfd5`.
No hash edited, no gate bypassed.

**A separate hole in the guard.** The bundled OpenBLAS in the cp311 wheel hashes to
`05c9f9eb89ee68a4b9d673184fa91c99587e736392c0c2d49180a8aa5303d080` — *identical* to `PIN_BLAS_SHA`.
So `verify()`, which hashes only that library, cannot tell the two wheels apart and reports
"byte-exact to the pin" on either. The script's own comments say the amplifier is the compiled
`np.interp` inside the numpy binary, not the BLAS — and that binary is the one thing `verify()` never
hashes. Only the pip hash gate discriminates. This is the guard whose whole purpose is preventing a
wrong board.

## 8. Still open

The `re-derived` and `board effect` columns, and the join test, are not yet done — in progress, with
the two-way curve fit of §4 as the centrepiece. Scratch boards only.

---
*Execution supervisor, ITEM 207 stage 1. Measurement only; adoption is the owner's and belongs to
stage 2.*
