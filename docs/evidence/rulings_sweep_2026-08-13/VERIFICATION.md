# ORDER 27 — PHASE 3: VERIFICATION AGAINST THE MACHINERY

Every LIVE-STANDING ruling was checked against the actual tree at `evid/rulings-sweep` (cut from
`origin/main`). PROCESS-LAWS were checked against recent practice where checkable, else marked
UNVERIFIABLE-BY-CODE. Per-ruling verdicts and their citations live in `INVENTORY.md` beside each
record; this file carries **the searches that were run** — including the negative ones — so the owner
can re-run any of them and disagree.

**Nothing was changed.** The only writes in this branch are under
`docs/evidence/rulings_sweep_2026-08-13/`.

---

## 1. Counts

| verification class | n |
|---|---|
| ENFORCED | 73 |
| DELIVERED-UNGUARDED | 18 |
| NOT-REFLECTED | 3 |
| AMBIGUOUS-OR-CONFLICTING | 3 |
| UNVERIFIABLE-BY-CODE (process laws) | 38 |
| **verified total** | **135** |

The remaining 55 records are ONE-TIME-COMPLETED (15), QUEUED (34) or SUPERSEDED (6) and do not
proceed to verification per the brief.

## 2. What each verdict means here

- **ENFORCED** — a machine check, config value or code site implements the ruling such that a
  regression fails or is impossible. The site is named at `file:line`.
- **DELIVERED-UNGUARDED** — the current state honours it, and this seat could find nothing that would
  stop a future act from regressing it. The honouring site is named; so is the search that came back
  empty.
- **NOT-REFLECTED** — the machinery does not do what the ruling says, verified in code or data.
- **AMBIGUOUS-OR-CONFLICTING** — the record is unclear, or two rulings collide. Both readings stated.

## 3. The probes committed with this sweep

| probe | what it establishes |
|---|---|
| `tools/probe_named_rows.py` | 23 owner-ruled NAMED ROWS read back out of the landed store `engine/rl_after/rl_model_data.json`, each printed beside the ruling that governs it. |
| `tools/probe_v502.py` | The population the v502/v503 position-field invariant would judge, on the landed store and the shipped board. |
| `tools/probe_326_day0.py` | The #326 signed levels, the currency factor and the board's pool rows. **Its ratio column is NOT relied on** — see §6. |
| `tools/segment_register.py`, `tools/extract_windows.py` | The coverage spine (§7). |

## 4. Positive verifications worth naming

These are the rulings where the machinery genuinely holds the line, recorded so the owner can see the
guards that are working:

- **Pick 1 = 3000 (R001/R005).** `one_source_selftest.py:431` asserts `_PVC0(1)==3000`; `:551` asserts
  the curve artifact self-declares `numeraire_pin1_3000` and `r104_9_strict_descent`;
  `data/model_config.json` pins `RL_PICK1=3000`. The shipped board's first pick reads 3000 exactly.
- **The never-rises / R12 law (R018/R164).** `one_source_selftest.py:920-950` runs
  `_v0_curve_assert()` (D14a/b/c) **on the standing gated build path**, and D14d scans the surface
  itself (`rising_steps_1_64` and the full grid must both be 0). `.github/workflows/ci-guards.yml:93-97`
  runs the selftest. The file's own comment at `:925` records why: *"the 2026-08-05 break went 19 days
  unseen"*. This is the one place in the tree where a broken owner law was converted into a permanent
  check — it is the model the proposed rulings-become-asserts law (R099) generalises.
- **R105.4 / L-RECENCY (R023).** `one_source_selftest.py:276-340` — a monotonicity assert on the
  per-game recency weight **and** an AST scan of `rho_out`'s executable code for the forbidden tokens
  `('qualif','floor','exclud','exclus','phase','classif','interrupt','delist')`. A ruling expressed as
  a *prohibition* was turned into a scanner. Also a model worth generalising.
- **The H cells retired (R014).** `_merged_recover.py:2190-2208` — `H_UNION`, `H_POOLSIT`,
  `H_MATNONRD` all default `1.0`, with the superseded values preserved in comments as history;
  `data/model_config.json` declares all three at 1.0 so gate/bake mode rejects drift.
- **The ND65+ cap amendment (R009).** `one_source_selftest.py:660` asserts ND65+ prices at its
  DERIVED level *and* that the min-against-`curve[64]` cap is REMOVED — the amendment carries its own
  check, in both directions.
- **The owner override machinery (R086/R087).** `owner_overrides.py:41-62` HALTs when the file is
  absent in a non-dev mode; `rl_export.py:640` is the post-export presence assertion. Verified live:
  `will-brodie` carries `ov {factor 0.5, dispv 386, mark "OWNER OVERRIDE ×0.50"}` against `v=773` on
  `data/rl_build/rl_app_data.json`, and the overrides file still carries exactly one row — consistent
  with the override doctrine (extra-statistical information only).
- **The env pin (R082).** `bootstrap.sh:18-31` — an offline, fail-closed check that HALTs if the
  running numpy is not the pinned build (2.4.4 + the pinned `libscipy_openblas*.so` hash).
- **The captaincy law (R021).** `rl_model.py:658-678` — the ruled softplus integral-of-P curve with
  `LCAPT_BAR/M/W/G` **pinned in-code** ("no os.environ on a board-changing dial"); the rejected
  saturating curve survives only behind `RL_CAPT=0` as the byte-exact base proof.
- **The separation law (R015).** `_merged_recover.py:2209-2221` — every `_h_cut` cell is gated on
  `p['_pool']`, so no national row can see a pool multiplier by construction.
- **The pool isolation law (R163).** `_merged_recover.py:2014` — `entry_anchor(p)` returns
  `pool_level(p)*_PL_F*_b_factor(p)` for pool rows and `v0_start(p)` for everyone else; the
  `_v0_curve_assert` docstring states a pool row "teaches no fit site, and IT NEVER READS THIS SURFACE
  AT ALL".

## 5. Negative evidence — searches that came back empty

Each of these is why a DELIVERED-UNGUARDED or NOT-REFLECTED verdict was written rather than assumed.

| ruling | search run | result |
|---|---|---|
| R063 position-field invariant | `present_position.*future_position\|future_position.*present_position` across the tree excluding `session_*/`; then a full read of the position section of `one_source_selftest.py:223-246` | No equality assert anywhere. The selftest checks vocabulary membership and at-most-one-alternate only. |
| R011 #326 day-0 sentence | `day-0`, `day0`, `entry_anchor` equality asserts across `one_source_selftest.py`, `ship_gates_check.py`, `_merged_recover.py`; full read of selftest §(10) `:627-700` | Ten #326 checks exist (levels carried, currency, anchor reach, ND65+ amendment, no-silent-refit) — none asserts the ruled sentence itself. |
| R017 era removal | `era\.get\|ERA_REF\|_era\|era_factor` across `rl_model.py`, `_merged_recover.py`, `par_build.py` | Only the two comment lines at `_merged_recover.py:53-57` recording the removal. The value path is clean **and unguarded** — a comment is not a check. |
| R007 force majeure | `force_majeure\|mccartin\|boyd\|slide` across `engine/**/*.py` | The live engine has an exclude-and-slide facility (`rl_model.py:284-296`) but nothing names McCartin or Boyd. The names live only in offline instrument dicts. |
| R083 dispatch pin | `OPENBLAS_NUM_THREADS\|NPY_DISABLE_CPU_FEATURES\|OPENBLAS_CORETYPE` across `*.sh`, `*.py`, `*.yml` excluding `session_*/`, `docs/` | `OPENBLAS_NUM_THREADS=1` present in `live-scoring.yml:60`, `live-scoring-proofs.yml` (×6), `tools/round_entry/weekly_update.sh:37`, and the two ingestion apply paths — **absent** from `ci-guards.yml` and `final-integration.yml`; the dispatch pin appears nowhere. |
| R100 open-decisions ledger | `find . -iname "OPEN_DECISIONS*"` | No such file. |
| R130 rulings ledger | `find . -iname "*LUKE_RULINGS*"` | Only `docs/archive/pre-mvp-2026-07/process/LUKE_RULINGS_LEDGER.md`. |
| R098 ruled-but-not-live ledger | `grep -n -i "RULED-BUT-NOT-LIVE" docs/CURRENT_STATE.md` | Present at `docs/CURRENT_STATE.md:156` — the mechanism exists and is maintained. |
| R107 CI never commits | read of the five workflows in `.github/workflows/` | None commits to the repo. |

## 6. One instrument this seat built and then declined to rely on

`tools/probe_326_day0.py` computes a printed-day-0 ÷ signed-anchor ratio over the board's pool rows.
Its "fresh entrant" filter is **wrong** — it reads a season-rows field that the landed store does not
carry under that name, so it classified established careers (Treacy, Newcombe, Sinclair) as
zero-game entrants and produced a meaningless ratio column.

The tool is committed **with this defect stated** rather than silently deleted, and the FLAGS report
for R011 relies on the register's own ORDER 26A measurement (printed pool day-0 = **2.6498×** the
signed anchors; positional RUCK 1.315 → KPF 5.114) rather than on any number this seat derived. What
this seat *did* verify independently is the checkable half: that no committed check asserts the ruled
sentence. Stated plainly so the owner knows exactly which half of that flag is this seat's work and
which half is the record's.

## 7. Coverage statement

**Source 1 — `docs/OPEN_ITEMS_REGISTER.md` (1,765,759 bytes).** Segmented into **2,911 units**
covering 100% of the file's bytes (2,507 line-1 `' · '` segments + 404 blank-line-delimited
tail blocks). Of these:

| set | units | bytes | treatment |
|---|---|---|---|
| carrying a CORE ruling marker | 809 | — | **every marker occurrence read verbatim** in a ±500-char window (901 windows, 673,582 chars) |
| BROAD-only markers, no CORE marker | 357 windows | 169,117 chars | **read verbatim** at ±320 chars |
| no ruling vocabulary of any kind | 1,727 units | 373,863 chars | mechanically screened, **not read by eye** |

So **842,699 characters were read verbatim in register order, start to finish, with no window
skipped**. The residue is the non-window remainder of hit units plus the units whose text contains
none of ~70 ruling-vocabulary patterns (owner-rul*, RULED, RULING, owner word(s), verbatim, filed
`<comment-id>`, ratified, override, EXCLUDE, STANDING, LAW, MUST, NEVER, ALWAYS, convention, binding,
mandate, PARKED, DEFERRED, FROZEN, …). That screen is committed (`tools/segment_register.py`) and
re-runnable. **This is the one place coverage is less than "every byte read by eye", and it is stated
rather than implied away.**

**Source 2 — `data/owner_overrides.json`.** Read in full (one override row). Verified applied on the
shipped board.

**Source 3 — `docs/directives/`.** Directory enumerated (26 documents); the two current directives on
main (`POOL_REPRICING_DIRECTIVE_2026-08-11.md`, `COMPOSITION_DIRECTIVE_2026-08-10.md`) checked for the
verbatim-owner-words / property-shaped-acceptance discipline (R109). The older ITEM 408–412 directives
were treated as secondary and read only where a register entry pointed at them.

**Source 4 — `#334`.** The commissioning brief (5274888553) and the surrounding 16 comments of
2026-08-12/13 were read in full via the GitHub API. Earlier comments were not paged through; the
register's own quotes were used, which is why several inventory records carry a tight citation rather
than a full verbatim quote.

**Source 5 — the machinery.** Targeted verification, not a full code audit: `rl_model.py`,
`_merged_recover.py`, `par_build.py`, `one_source_selftest.py`, `ship_gates_check.py`,
`owner_overrides.py`, `rl_export.py`, `bootstrap.sh`, the five workflows, `data/model_config.json`,
`data/owner_overrides.json`, `engine/rl_after/pvc_curve_v2.json`, `engine/rl_after/rl_model_data.json`
and `data/rl_build/rl_app_data.json`.

## 8. Confidence, honestly

- **High** on the extraction of rulings whose text carries a ruling marker: the screen is broad and
  every hit was read.
- **High** on the ENFORCED verdicts: each names a site this seat opened and read.
- **Medium-high** on NOT-REFLECTED: each rests on a named search plus, for R008 and R063, a direct
  read of the landed data.
- **Medium** on completeness of the LIVE-STANDING set: a ruling stated in the register without any
  ruling vocabulary would not have been surfaced by the screen. The 1,727 no-marker units are the
  exposure, and they are counted above.
- **Low** on the PROCESS-LAW verdicts marked UNVERIFIABLE-BY-CODE: they are recorded as extracted;
  practice conformity was spot-checked against the register's own recent entries only.
