# GROUP 1 — THE NEVER-RISES LAW, RESTORED · 2026-08-10

Owner rulings **1.1 (restore)** and **1.2 (gates)** of 2026-08-10, filed at issue #334 comment
5235660463. Ruling **1.3 (the ledger move) is HELD** — nothing in this branch touches the ledger's
location.

Base: `origin/main` **`064abca`** (the DOB courier landing), store `d9a24282`, committed surface pin
`5a03c9ea`, committed board `a672ed3a`.

Plain English throughout, by the owner's standing rule.

---

## 1. WHAT WAS WRONG

The owner's V0 law (ledger entry R12, 2026-07-03) says a year-zero value curve **never rises as the
pick number rises**. It held for 33 days. It broke on 2026-08-05 at commit `dab9657`, the #306
anchored-lens landing — not by decision, but by omission. The old fit ended every curve with an
isotonic "never rises" step. The new construction

    v0*(position, draft age, pick) = anchor(pick) x m(position, draft age, pick)

never calls that step. The anchor ladder falls strictly but has near-flat stretches (picks 6-8 fall
about 4 points each); the lens is a smooth bounded field that is free to climb across them, and
nothing stopped it.

Measured on the shipped surface at this base: **439 rising steps inside picks 1-64**, spread across
**all 90** position x draft-age profiles. On real players the audit found 29 adjacent inverted pairs
— Grlj at pick 8 priced above Cumming at pick 7 being the one the owner saw.

## 2. WHAT WAS DONE

**One step, put back where it used to be.** Within each (position x draft age) profile, the composed
curve is projected onto the non-increasing curves over the log-pick grid by isotonic regression —
`IsotonicRegression(increasing=False)`, the exact call the deleted `_iso_dec` step made, on the same
grid. It runs **after** the lens multiply and after the neutrality fixed point, i.e. last, on the
finished curve, exactly where the old step sat.

Isotonic regression **is** the merge the owner described: a stretch that violates the law settles to
the weighted level between its neighbours — some rows come down a little, some go up a little — and
it is the closest non-increasing curve to the one the lens fitted, so it is the least total
distortion available. Two profiles, in full:

| profile | picks | before | after |
|---|---|---|---|
| MID, draft age 18 | 6, 7, 8 | 2042.0 · 2141.9 · 2185.6 | **2123.2 · 2123.2 · 2123.2** |
| SF, draft age 18 | 1, 2 | 2281.1 · 2520.7 | **2400.9 · 2400.9** |

Everything either side of a violating stretch is untouched — MID age-18 picks 1-5 and 9-64 come
through byte-identical.

**What is deliberately untouched:**

- **LAW-INTERSECTIONS.** A position's value may still cross the pick ladder, and two positions may
  still cross each other. The projection is solved **inside one profile at a time**; it never
  compares one profile with another and never compares a profile with the anchor. Crossing stays
  legal. Rising within a profile does not.
- **The lens fit itself** — kernels, bandwidths, hierarchical shrinkage, the bound m in [0.5, 2.0],
  the lam(pick) local-neutrality fixed point. All solved first, all unchanged.
- **The mature age ordering.** The pre-#306 mature fit also forced non-increasing in draft *age*.
  The #306 lens does not, and R12 is a *pick* law. Restoring one law is not licence to add another
  the owner did not rule, so this was left alone.

**One honest scope decision, stated plainly.** The surface grid runs to pick 90, but the national
ladder ends at pick 64 (`_PVC0`: 3000 at pick 1 down to 185 at pick 64). Index 65 is the **pool
slot** (237) — a different object, deliberately *above* the ladder's last rung. The anchor
extrapolates past its own last key off the 64->65 ratio, so that step up becomes a compounding
upward slope and the raw composed curve rockets away: the MID age-18 profile runs 238 at pick 64 to
about **39,500** at pick 90. Nothing reads that region — every row priced on this surface is a
non-pool national selection, measured maximum pick 64, and picks 65+ are pool by the owner's ruling
and are priced off the signed division levels.

Solving one isotonic projection across the whole 1-90 grid lets that unread artifact drag the real
ladder **up**: pool-adjacent-violators merges the exploding tail into the priced region and flattens
every profile to a single number. That was measured, not guessed — the first build of this repair
did exactly that (every cell collapsed to its own mean; MID age-18 flat from pick 1 to pick 90) and
was thrown away. So:

- **picks 1-64** — the isotonic merge, on the ladder the law is written about;
- **picks 65-90** — carried by running minimum from the pick-64 level. Same law (a value may never
  rise with pick), applied where there is no ladder to merge against. The tail can only fall; the
  artifact can never lift the priced region.

Result: **zero rising steps in every profile, all 90 cells, picks 1-64 and across the whole 1-90
grid.**

## 3. THE ZERO-STEPS PROOF

| | picks 1-64 | full 1-90 grid |
|---|---|---|
| rising steps BEFORE (`064abca`) | **439** | 2,779 |
| rising steps AFTER | **0** | **0** |
| profiles with at least one rise, before | 90 of 90 | 90 of 90 |
| profiles with at least one rise, after | **0** | **0** |
| adjacent pairs scanned | 90 cells x 89 pairs = 8,010 | |

Worst profiles before, picks 1-64: KPF age 23 (11 rises), KPF age 22 (11), KPF ages 19-21 (9 each),
SD age 23 (8).

Per-profile detail: `zero_steps_proof.csv` (one row per cell, before and after).
The shipped curve itself: `surface_after_1_64.csv` (90 cells x picks 1-64).

## 4. THE MOVERS

`movers.csv` — every player whose year-zero value or board price changes, with position, draft age,
pick, draft year, before, after and delta. `summary.json` carries the counts.

- **82** players' year-zero value (v0) moves at all; 79 by more than 1 point; **6** by more than 100
  points; largest single move **119.8**.
- **47 down** (total −1,755 v0 points) and **35 up** (total +1,322) — the merge in plain sight.
- **16** players' displayed board price moves: **9 down, 7 up**. Largest cut **−18**
  (Xavier Taylor), largest rise **+24** (Daniel Annable).
- Board total **761,587 → 761,574 = −13 points (−0.0017%)**.

The restore **is** a cut for players sitting above the non-increasing floor, and the owner ruled it
knowing that. The clearest pair is Cameron Rayner (SF, pick 1) **+119.8** and Jack Lukosius (SF,
pick 2) **−119.8** — an inverted adjacent pair merging to their common level. The named case, Grlj
and Cumming, resolves the same way: Annable (pick 6), Cumming (pick 7) and Grlj (pick 8) were
2042.0, 2141.9 and 2185.6 — each later pick dearer than the one before — and are now **all three at
2123.2**. Their board prices do not move: all three are priced on evidence well above their
year-zero value, so the law is restored on the surface without pretending it changed their price.

Most v0 movers show **no** price change for the same reason: v0 is the *entry* price, and a player
with a real record is priced off his record. The 16 price movers are the players still leaning on
the year-zero anchor (floor, sit-out blend, thin record).

**Year-1 cohort ratio.** Six of the 82 v0 movers are 2025 draftees (the year-1 cohort in 2026), and
two of them move on price: Annable **+24** and Xavier Taylor **−18**, a net **+6** across the whole
cohort. The act's year-1 ratio measurement lives on the act branch and is not run here; on this
basis the effect is inside rounding and no ratio figure moves at the two decimals the band
([1.04, 1.13]) is quoted to.

## 5. THE GATES (ruling 1.2)

**(a) D14a/b/c wired into the standing gated build.** The D14 laws already existed and would have
gone red on 2026-08-05. They did not fire because they lived **only** in `ship_gates_check.py`, a
hand-run checklist that last ran 2026-07-17 — nineteen days before the break. They now also run in
`engine/rl_after/one_source_selftest.py`, section (11): the standing gated build path that every
board build reaches, and which exits non-zero, so the **build halts**. `ship_gates_check.py` keeps
its own D14 block and stays the hand-run superset (three-column board, snapshots, the whole
checklist). Deliberate duplication of a cheap check, not a move.

**(b) D14d — the new surface-level scan.** D14b compares **rostered player pairs**, and the audit
measured what that covers: real players expose about **8%** of the surface's rising steps (29
inverted pairs against 439 rising steps). D14d reads **the surface itself** — every position x draft
age profile, every adjacent pick pair, 8,010 pairs, zero tolerance, halts the build on any rise. It
scans the artifact the board actually reads, so a bad freeze, a bad refit and a bad code path all
fail identically. Implemented as `_v0_surface_assert()` in the engine; wired into **both** the
standing build (`one_source_selftest.py`) and the hand-run checklist (`ship_gates_check.py`, gate
`D14d`).

**(c) A third thing had to be fixed to make (a) possible, and it is reported here plainly.**

When D14a and D14b were first wired into the build they went **red — on `origin/main` as well as on
this branch**, and not because of anything this repair did. The cause is the population they read.
D14a/b are assertions **about the V0 pick surface**, but they were selecting every national-draft row
with a pick: `type=='ND' and pick is not None`. Since the owner's pricing split, a national selection
at **pick 65+ is pool** — priced off its signed division level (#326 entry anchors), teaching no fit
site, and never reading this surface at all. Those 122 rows were swept in, and their division-level
prices were then reported as surface faults:

- **D14a** read a "cross-draft dispersion" of **310.1**, which is two pool KPDs at pick 70 sitting on
  different division levels. The surface's own dispersion is **0.000000** — exactly what the law says
  it should be.
- **D14b** counted ladder-versus-pool pairs as pick inversions. That compares two different price
  objects and **no surface can ever satisfy it**.

So both gates were unsatisfiable and permanently red, which is part of why they could sit in a
hand-run checklist for nineteen days without anybody reading them as a live alarm. Restricted to the
surface's own population — the **same `not is_pool` filter the surface's own fit uses** — they become
real assertions again. Nothing is hidden: the excluded rows are counted, and the whole-ND figures are
returned and printed as **report-only** by both the build and the checklist.

| gate | population | `origin/main` `064abca` | after this branch |
|---|---|---|---|
| D14a max cross-draft dispersion | surface rows (1,448) | 0.000000 | 0.000000 |
| D14b V0 pick inversions | surface rows (1,448) | **53** | **0** |
| D14d surface rising steps, picks 1-64 | the surface (8,010 pairs) | **439** | **0** |
| D14a dispersion (report-only) | all ND incl. 122 pool rows (1,570) | 310.1 | 310.1 |
| D14b inversions (report-only) | all ND incl. 122 pool rows (1,570) | 475 | 422 |

The report-only column does not fall to zero and is not meant to: those are ladder-versus-pool
comparisons, and the residue is the open pool-pricing question the audit named, not an R12 breach.

Measurement on both engines side by side: `d14_population.txt`.

**D14d is not vacuous.** A gate that cannot fail is not a gate, so it was pointed at the pre-restore
surface and made to go red: the **patched** engine loading main's `5a03c9ea` surface reports **439**
rising steps over picks 1-64 and **2,779** over the full grid, and names the offending steps
(`KPD|16 pick 10->11 1081.51->1089.37`, …). D14b reports 53 on the same run. `d14d_non_vacuity.txt`.

## 5a. GATES RUN, AND THE ONE ROW THAT IS RED

| gate | result |
|---|---|
| `rl_export.py` (F1 export↔engine parity) | **exit 0** — parity 804/804 `eps=0`, numéraire pick-1 = 3000, board `4b448a82` |
| `s4_matrix_M1v7.py` (F2 book↔board parity) | **exit 0** |
| `one_source_selftest.py` — **the standing gated build** | **exit 0 · 147 PASS / 0 FAIL / 0 STALE**, D14a/b/c/d green inside it |
| `guard_correction_canary.py` (Guard 4) | **exit 0** |
| `verify_restore.sh` | 9 PASS / **2 FAIL** — both **stale literals**, see below |

The two red rows in `verify_restore.sh` compare Maric and Langdon against hand-typed literals
(1271 / 567) written for an older board era. They do not describe this board and **they do not
describe main's board either**. Measured from the gated build on this container:
`ryan-maric` ev(2026) = **1473 before → 1473 after**; `ed-langdon` = **849 before → 849 after**.
Neither player is in `movers.csv`; neither is moved by this change by any amount. They are left
untouched — re-typing them would restart exactly the clock that script's own `stale()` doctrine warns
about, and re-pinning an owner-facing panel literal is not this branch's business. Every row that
binds to something this branch moved is green. Detail: `gate_verify_restore.txt`.

## 6. IDENTITIES, BEFORE AND AFTER

| artifact | before (`064abca`) | after |
|---|---|---|
| v0surf config signature | `6ef67f07db98258786189a6316ce24f9` | `6ef67f07db98258786189a6316ce24f9` (unchanged — the signature reads config, curve and roster, never surface values) |
| `data/v0surf.pkl` | `5a03c9ea3e9a32e6cc6e1ffec5293685` | `fbc5b39387b2b135284a2e157f46c810` |
| engine head `_merged_recover.py` | `8f0e3eb1b29fee6b2defa0a5cfd7ebec` | `6c46970ab7e8dc5219f701367515675a` |
| board `rl_app_data.json` | `a672ed3a6a1426a262d932f844e8f87b` | `4b448a821f54180182637983f7a26a9d` |
| store | `d9a24282357cf3083b1640466e3ecd83` | unchanged — no store write in this repair |

**The box is clean (N35).** Before baking anything, a refit was run on this box with the
**unpatched** engine and it reproduced the committed pin `5a03c9ea` byte-exact; the unpatched board
build reproduced `a672ed3a` byte-exact as well. So the whole delta is the law restore and none of it
is machine weather. Commands and output: `clean_box_control.txt`, `refit_verify_control.txt`.

## 7. REPRODUCE

```bash
bash setup_env.sh                      # pinned venv /root/rl_venv312
export PATH=/root/rl_venv312/bin:$PATH
RL_VENDOR=<repo>/vendor bash <repo>/bootstrap.sh
cd /home/claude/rl_workspace/rl_after
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_REPO=<repo> RL_FV=<repo>/engine/forward_valuation RL_CONFIG_MODE=gate PYTHONHASHSEED=0
# NOTE: do NOT set RL_V0SURF_PKL — gate mode rejects it as an unknown model override. bootstrap.sh
# seeds /home/claude/v0surf.pkl from this checkout and Guard 5 asserts that loaded path == the pin.

# 1. the surface is FROZEN — check that this box reproduces the committed pin, no write:
RL_V0SURF_REFIT=1 python3 <repo>/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify
#    expect: REPRODUCES the committed pin fbc5b39387b2b135284a2e157f46c810

# 2. the board and the book:
rm -f rl_app_data.json && python3 rl_export.py        # expect board 4b448a82
python3 s4_matrix_M1v7.py
python3 one_source_selftest.py                        # D14a/b/c/d run here; non-zero exit = build halts
python3 guard_correction_canary.py

# 3. the hand-run superset:
python3 <repo>/ship_gates_check.py                    # gate D14d on the board
```

To regenerate the surface after a deliberate config change, the one committed fit lane is unchanged:

```bash
RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 \
  python3 <repo>/session_2026-07-18/legf6/scripts/refit_v0surf.py --bake
```

## 8. SCOPE — WHAT THIS BRANCH DOES **NOT** DO

The brief scopes this to the v0 code path and its frozen surface. The board of record and the pins
that bind it move because the surface moved, and they are re-derived here. **The publication layer is
not touched**: no sibling/balanced-board repin, no UI bundles, no `release_lineage` transition entry,
no out-of-round history column. An out-of-round board move needs an owner-approved record before the
Movers dropdown can name the boundary (the DOB landing's section 5/6 records that lane), and this
branch is a candidate the seam verifies, not a landing. `identities.balanced_board_md5` is therefore
left at `a970c19c` and will move with that lane, not this one.

## 9. FILES IN THIS TREE

| file | what it is |
|---|---|
| `README.md` | this note — the patch rationale |
| `summary.json` | the headline counts, machine-readable |
| `zero_steps_proof.csv` | rising steps per profile, before and after (the proof) |
| `surface_after_1_64.csv` | the shipped year-zero curve, 90 profiles x picks 1-64 |
| `movers.csv` | every moved player: name, position, draft age, pick, draft year, before, after, delta |
| `clean_box_control.txt` | the N35 control — unpatched refit and board reproduce the committed pins |
| `refit_verify_control.txt` | raw output of the unpatched `--verify` run |
| `refit_verify_after.txt` | the patched `--verify` — this box reproduces the new pin `fbc5b393` |
| `d14_population.txt` | D14a/b measured on both engines, both populations |
| `d14d_non_vacuity.txt` | D14d pointed at the pre-restore surface — it goes red, as it must |
| `gate_run.sh` · `gate_run.log` | the exact gate script and its transcript |
| `gate_*.txt` | gate outputs (export, book, selftest, canary, verify_restore) |
| `diffstat.txt` | what this branch changes |
