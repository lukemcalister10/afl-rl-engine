# PACKET — ORDER D8, THE CEILING-ONLY LEG. The wiring, the six falsifiers, the movers list.

**Seat:** D8 build seat, register **v794** (probation **v772**, sequencing **v793**) · **Date:** 2026-08-20
**Base:** `origin/main` @ `6bfda2c` · **Prereg:** `PREREG_D8.md`, committed and pushed **before** the engine
edit (commit `8eca222`).

> ## PRICED, NOT ADOPTED.
> The live board **has not moved** and is not proposed to move by this act. `RL_O33_TAPEROFF` ships
> **default OFF**; with it unset the board of record `a05fe951f78482c70520480e184c80ec` reproduces
> **byte-exact**, three times, in both postures. The owner's look at the movers list, and his word, come
> between this delivery and any adoption.

---

## 1. The entanglement, and the cut

ORDER B's **B-3 ceiling fix** was on owner probation (v772: *"happy to look at still boosting the younger
players pending a look at the movers list"*), and v793 sequenced it ahead of the R23 ingestion. Delivering
that look meant pricing B-3 **alone** — and no configuration could do it:

| leg | gate before D8 |
|---|---|
| **B-1** tall post-peak ladder (`rl_model.frac`) | `_O33 and _O33S>=1 and j>0 and g in ('KPD','KPF')` |
| **B-1** anchor-preserving renorm `s*` (`_merged_recover`) | `MA._O33 and MA._O33S>=1 and g in ('KPF','KPD')` |
| **B-3** taper retirement (the `b6` wrapper) | `MA._O33 and MA._O33S>=2` |

`_O33S` is `0` unless `_O33`; B-1 fires at `>=1`, B-3 at `>=2`, and `2 >= 1`. Every stage that reached the
probated ceiling fix also raised the **owner-killed** ladder. That is the entanglement. It is cut, and the
ladder is **not** touched.

## 2. THE WIRING — one engine edit, one file, one contiguous hunk

**`engine/rl_after/_merged_recover.py:1117-1152`** — the `b6` wrapper. The dial is defined at its point of
use and consumed two lines later (the house pattern: `RL_O41_UNWIND` is read in this file too):

```python
_O33_TAPEROFF=os.environ.get('RL_O33_TAPEROFF','0')!='0'     # :1145  ORDER D8, default OFF
def b6(p,Y=2026):                                            # :1146
    bb=_b6_pre_v7(p,Y)                                       # :1147
    if (MA._O33 and MA._O33S>=2) or _O33_TAPEROFF: return bb  # :1148  <- THE ONLY CHANGED EXPRESSION
```

`engine_head` `5ac6780f3c4931edcaa527576bbdfb88` → `338a790b773cfbbff0e1283794c72efe`; the rest of the diff is
the comment block stating what the dial gates, what it provably cannot reach, and that adoption is a later act.
**No other engine file is touched.** `rl_model.py` is byte-unmoved at `6fe7c415`.

**Why the ladder is unreachable, by construction.** Both B-1 expressions are guarded by `MA._O33`, read from
`RL_O33` and nothing else. `RL_O33_TAPEROFF` is a distinct name and never sets it, so with `RL_O33` unset both
`and`-chains short-circuit on their first term at every call and neither `O33_TALL_LADDER` nor `O33_SSTAR` is
read by any reachable expression. **F2 tests this rather than asserting it.**

**No constant was fitted and no parameter added.** `asc == 1` is ORDER B's own quantile re-fit answer — the
boundary solution `asc*=1` in every band the taper bites (`RESULTS_B_TAPER.json`). The dial is a boolean.

**Not a manifest dial, on purpose.** It is absent from `data/model_config.json`, so
`config_manifest.enforce()` **rejects it as an unknown model override in bake/gate/canonical mode**: no
certifying build can carry it. That is the safety property, not an oversight — adoption means flipping the
default and stamping the manifest, through the lane the bake used, on the owner's word.

### 2.1 The identity restamp (declared in PREREG_D8 §2.1, before the edit)

Editing `_merged_recover.py` moves the **computed** `engine_head` identity, so four **live** carrier fields
were restamped by `d8_restamp.py` — through their writers of record, never by hand:

| carrier | before → after |
|---|---|
| `data/expected_boot.json` `engine_head` | `5ac6780f…` → `338a790b…` |
| `data/release_contract.json` `identities.engine_head` (+ `contract_sha256`) | `5ac6780f…` → `338a790b…` (seal `8da998ce…` → `88d29826…`) |
| `ui/data/board_view_working.js` `stamp.engine` + `stamp.release.engine_head` | regenerated via `ui/tools/extract_board_view.py` + `round_movers.inject_release_contract` |

Verified before use: with `expected_boot` unchanged, running both UI writers in sequence reproduces the
committed bundle **byte-identical** (`fa20f2fc4c7e65c6c050868a11c9139f`), so the bundle is regenerated, not
patched. The whole restamp is **2 + 4 + 2 changed lines**. `d8_restamp.py` **refuses to run** unless
`board` / `store` / `rl_model` / `register` all equal their pins, and it writes none of them.

**No board, store, config, rl_model, register or as-of-round pin moved.** `data/book_stable_seal.json`'s
`head_md5` is a freeze-stamp and now reads **SEALED-LAG** — reported, never gating, and deliberately **not**
re-sealed: a book re-seal is a separate act and this seat did not smuggle one in.

## 3. THE FALSIFIERS — all six, measured

Method: the accepted disposable FV builder (`test_fv_provenance._run_build`, `balanced=False`,
`PYTHONHASHSEED=0`, five BLAS thread counts pinned to 1), staging into a throwaway dir, **writing nothing
under the repo**, staging deleted after each run, strictly sequential, under `tools/build_lock.sh`.

| id | falsifier | measured | verdict |
|---|---|---|---|
| **F1** | dial unset ⇒ the live board byte-identical | dev-shell ×2 **and** canonical ×1 ⇒ `a05fe951f78482c70520480e184c80ec`, byte-exact, `rc=0` | **PASS — did not fire** |
| **F2 (a)** | the ladder's own switches are off in the priced posture | `MA._O33 is False`, `MA._O33S == 0`, `RL_O33` unset, `RL_O33_TAPEROFF` = `'1'` | **PASS** |
| **F2 (b)** | `frac()` == the shared `DELTAS` path | **161 of 161** domain cells (`j = -8…14` × `KPD/KPF/MID/SD/SF/RUCK/two-arg`) identical; **2,220 of 2,220** per-row post-peak KPD/KPF checks identical. **0 divergences, both postures.** | **PASS** |
| **F2 (c)** | no tall veteran moves DOWN on the priced board | **FIRED, at −1 point.** One tall veteran falls: **Taylor Walker, KPF 37, 129 → 128 (−1, −0.78 %)**. Explained in §5 and shown *not* to be the ladder. | **FIRED — reported, not smoothed** |
| **F3** | determinism ×2 | dial off `a05fe951…` ×2 · dial on `5ea978f7b6a073abb2012f10cccbc3e3` ×2 | **PASS** |
| **F4** | ceiling v-inversions, priced ≤ live; the "kills by construction" claim **tested** | live board **407 of 804** · priced board **0 of 804**. | **PASS — and the claim is CONFIRMED at exactly 0** |
| **F5** | day-0 89/89 internal assert | `PRINTED-DAY-0 ASSERT: 89 of 89 … tolerance 0` on **all five** builds, the priced ones included | **PASS** |
| **F6** | acceptance runner GREEN, dial unset | `7 checks · PASS 7 · FAIL 0 · BLOCKED 0 · RULED-RED 0 · VERDICT GREEN` | **PASS** |

### F4 in full — the inversions the fix exists to kill

A **v-inversion** is `band[5] < band[4]`: the ceiling below the band beneath it. `_b6_core` returns
`band[5] = max(pred, b[4]) ≥ b[4]`, so a *pre*-taper inversion is impossible and every inversion is the v7
taper's (`PREREG_W6.md` §C2). On today's board there were **407**, not the derivation-era 341:

| by position | MID 92 · SD 90 · SF 82 · KPD 58 · KPF 58 · RUCK 27 |
|---|---|
| **by age band** | **27+ 230 · 24-26 137 · 22-23 40 · 20-21 0 · ≤19 0** |
| worst | Samson Ryan (RUCK 26) −15.14 · Oliver Hayes-Brown (RUCK 26) −15.10 · Jack Watkins (MID 26) −14.96 |

**Priced: 0.** Every one dies. Independently: **no row's ceiling moved DOWN — 0 of 804** — so the dial is
strictly a ceiling *lift*, as ORDER B claimed.

## 4. THE MOVERS LIST — the owner's probation look

Full list, per-band attribution and back rows: **`MOVERS_D8.md`** (every mover, name · age · position ·
before · after · delta · % · Δ ceiling), raw in `MOVERS_D8_out.txt`, machine-readable in `MOVERS_D8.json`.

| | |
|---|---|
| base board (= the board of record) | `a05fe951f78482c70520480e184c80ec` — total **664,949** |
| **PRICED** | **`5ea978f7b6a073abb2012f10cccbc3e3`** — total **693,753** (**+28,804**, **+4.3318 %**) |
| movers | **559 of 804** — **551 up**, **8 down**, 245 unmoved |
| total up / total down | **+28,826** / **−22** |
| ceiling v-inversions | **407 → 0** |
| back rows (board-history-only) | **19 movers, every one UP**, +1…+3 |

### By age band

| age band | n | movers | up | down | Δ | % of band |
|---|---:|---:|---:|---:|---:|---:|
| ≤19 | 71 | **0** | 0 | 0 | **+0** | +0.00 % |
| 20-21 | 162 | 51 | 48 | 3 | +1,660 | +1.40 % |
| 22-23 | 142 | 121 | 121 | 0 | +7,899 | **+5.65 %** |
| 24-26 | 164 | 158 | 158 | 0 | +9,463 | +5.18 % |
| 27+ | 265 | 229 | 224 | 5 | +9,782 | +5.54 % |

### By position

| position | n | movers | up | down | Δ | % of position |
|---|---:|---:|---:|---:|---:|---:|
| MID | 197 | 137 | 136 | 1 | +9,386 | +3.12 % |
| SD | 173 | 126 | 124 | 2 | +6,127 | +5.24 % |
| SF | 185 | 119 | 116 | 3 | +3,953 | +5.16 % |
| KPD | 92 | 69 | 68 | 1 | +3,004 | **+6.67 %** |
| KPF | 103 | 75 | 74 | 1 | +3,433 | +5.15 % |
| RUCK | 54 | 33 | 33 | **0** | +2,901 | +4.91 % |

### Per-band attribution — age band × position (n / movers / Δ)

| age band | MID | SD | SF | KPD | KPF | RUCK |
|---|---:|---:|---:|---:|---:|---:|
| ≤19 | 22/0/+0 | 15/0/+0 | 22/0/+0 | 3/0/+0 | 9/0/+0 | 0/0/+0 |
| 20-21 | 41/15/+657 | 28/9/+234 | 40/12/+284 | 16/3/+47 | 23/11/+359 | 14/1/+79 |
| 22-23 | 34/33/**+2,974** | 33/28/+1,716 | 33/28/+1,146 | 15/13/+674 | 18/16/+1,057 | 9/3/+332 |
| 24-26 | 51/49/**+3,656** | 33/33/+1,931 | 36/36/+1,327 | 17/14/+818 | 18/18/+872 | 9/8/+859 |
| 27+ | 49/40/+2,099 | 64/56/+2,246 | 54/43/+1,196 | 41/39/+1,465 | 35/30/+1,145 | 22/21/**+1,631** |

### Top 20 by movement

| # | name | age | pos | before | after | Δ | % | Δ ceiling |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Tom De Koning | 27 | RUCK | 1,677 | 1,874 | **+197** | +11.75 % | +14.8 |
| 2 | Nick Bryan | 25 | RUCK | 583 | 751 | **+168** | +28.82 % | +16.0 |
| 3 | Dante Visentini | 23 | RUCK | 807 | 971 | **+164** | +20.32 % | +12.8 |
| 4 | Samson Ryan | 26 | RUCK | 212 | 376 | **+164** | +77.36 % | +23.3 |
| 5 | Lachlan Ash | 25 | SD | 5,303 | 5,456 | **+153** | +2.89 % | +4.9 |
| 6 | Sean Darcy | 28 | RUCK | 689 | 841 | **+152** | +22.06 % | +14.9 |
| 7 | Jake Soligo | 23 | MID | 1,874 | 2,019 | **+145** | +7.74 % | +8.3 |
| 8 | Will Day | 25 | MID | 2,139 | 2,284 | **+145** | +6.78 % | +8.8 |
| 9 | Ned Reeves | 28 | RUCK | 202 | 343 | **+141** | +69.80 % | +16.5 |
| 10 | Wil Powell | 27 | SD | 746 | 885 | **+139** | +18.63 % | +12.1 |
| 11 | Massimo D'Ambrosio | 23 | MID | 1,566 | 1,704 | **+138** | +8.81 % | +8.3 |
| 12 | Will Setterfield | 28 | MID | 593 | 730 | **+137** | +23.10 % | +19.8 |
| 13 | Marcus Windhager | 23 | MID | 1,683 | 1,819 | **+136** | +8.08 % | +7.6 |
| 14 | Jack Graham | 28 | MID | 604 | 738 | **+134** | +22.19 % | +14.8 |
| 15 | Sam Berry | 24 | MID | 3,527 | 3,661 | **+134** | +3.80 % | +5.4 |
| 16 | Peter Ladhams | 28 | RUCK | 438 | 570 | **+132** | +30.14 % | +20.2 |
| 17 | James Worpel | 27 | MID | 388 | 518 | **+130** | +33.51 % | +13.7 |
| 18 | Adam Cerra | 27 | MID | 1,005 | 1,133 | **+128** | +12.74 % | +12.6 |
| 19 | Matt Johnson | 23 | MID | 985 | 1,113 | **+128** | +12.99 % | +8.7 |
| 20 | Andrew McGrath | 28 | SD | 1,003 | 1,130 | **+127** | +12.66 % | +12.6 |

Names illustrate; they never gate. **The cohort shape, stated plainly:**

* **The `≤19` band does not move at all — 0 of 71.** That is not a defect and it is the answer to half the
  owner's probation question. The v7 taper is `asc = interp(age, [20,22,24,27] → [1.0,0.76,0.58,0.40])`,
  so at age ≤ 20 `asc` is already **1.0** and the taper was **already inert**. **Retiring the taper cannot
  boost the youngest players, because it was never taxing them.** The lever that compresses the ≤19 cohort,
  if one is wanted, is a different lever. The band's own arithmetic makes the point sharper than any
  argument: `asc` reads 1.00 at age 20 and 0.88 at age 21, and in the `20-21` band **47 of the 75
  twenty-one-year-olds move while only 4 of the 87 twenty-year-olds do — and three of those four are
  down-movers with a zero ceiling change** (§5). The lever switches on, exactly, at 21.
* The lift lands on **22-26** in proportional terms (+5.65 % / +5.18 % of band) and on **27+** in absolute
  terms (+9,782, the largest single band) — 27+ is where the taper bit hardest (`asc` flat at 0.40) and it
  is also where 230 of the 407 inversions were.
* **RUCK is the sharpest position** — 33 of 54 move, every one up, +4.91 % of the position, and it owns the
  top four movements on the board. That matches ORDER B's own preview (T. De Koning, Bryan, S. Ryan named
  there too, at the same rank order) on a different store and a different board — an independent agreement
  worth having.
* **KPD carries the largest positional share (+6.67 %)** and no position falls in aggregate.
* The largest *proportional* moves are cheap rows coming off a floor (Daniel Butler 1→3, Jordon Butts
  12→35, Wil Parker 13→35): a ceiling lift on a near-replacement row is a large percentage of very little.

## 5. THE EIGHT ROWS THAT MOVE DOWN — the finding, explained, not smoothed

Eight of 804 fall, for **−22 points in total** against **+28,826** up. Every one is ≤ 1 % :

| name | age | pos | before | after | Δ | % | its own Δ ceiling |
|---|---:|---|---:|---:|---:|---:|---:|
| Noah Mraz | 20 | KPD | 1,057 | 1,050 | −7 | −0.66 % | **0.000** |
| Jagga Smith | 20 | MID | 4,348 | 4,344 | −4 | −0.09 % | **0.000** |
| Tom Papley | 30 | SF | 403 | 399 | −4 | −0.99 % | +7.33 |
| Jesse Dattoli | 20 | SF | 349 | 347 | −2 | −0.57 % | **0.000** |
| Zachary Williams | 32 | SF | 357 | 355 | −2 | −0.56 % | +10.76 |
| Ed Langdon | 30 | SD | 744 | 743 | −1 | −0.13 % | +6.94 |
| Jeremy Howe | 36 | SD | 219 | 218 | −1 | −0.46 % | +14.07 |
| **Taylor Walker** | **37** | **KPF** | **129** | **128** | **−1** | **−0.78 %** | **+13.98** |

**The cause was named in the prereg, before the numbers existed, and the numbers confirm it.** `RL_UNCOMP`'s
load-time **per-position conservation renorm** `C[pos] = Σpr0 / Σv0p` rescales *every* row in a position.
Lifting ceilings raises `pr0` across the position, so `C[pos]` is re-derived slightly lower — and a row whose
own ceiling gained little (or nothing) takes the renorm without the offsetting lift:

| pos | `C[pos]` base | `C[pos]` priced | `V_ref_b` base → priced |
|---|---:|---:|---|
| KPD | 1.11646 | **1.10759** | 189.7 → 239.0 |
| KPF | 1.08684 | **1.08086** | 504.5 → 544.0 |
| MID | 1.09358 | **1.08679** | 1,388.6 → 1,507.3 |
| SD | 1.11110 | **1.10189** | 462.3 → 523.6 |
| SF | 1.23523 | **1.21176** | 128.0 → 163.6 |
| RUCK | 1.03492 | **1.03625** | 1,686.8 → 1,701.9 |

Five positions' `C` falls; **RUCK's rises**, and RUCK is the one position with **zero** down-movers. The
three rows with a **zero** ceiling move (Mraz, Smith, Dattoli — all aged 20, where the taper was already
inert) are the pure renorm effect with nothing to offset it; the other five gained ceiling but less than
their position's renorm cost them. `RHO_DEN` is unchanged in every position, as expected — it is a rho-axis
object the ceiling does not touch. (Second-order corroboration: the proven-population count in the
calibration pass reads **354 → 358**, four more rows clearing `pr0 > 0` once their ceiling lifts.)

### Why this is not the ladder — F2 (c), fired, adjudicated

F2 (c) was written as a **proxy** for "the ladder fired". It fired on **Taylor Walker (KPF 37) at −1 point**.
The proxy is wrong here, and the direct tests say so:

1. **`frac()` never diverged from `DELTAS`** — 161/161 domain cells and 2,220/2,220 per-row post-peak KPD/KPF
   checks, exactly equal, in **both** postures. The ladder branch was not taken once.
2. **`MA._O33 is False` and `MA._O33S == 0`** in the priced posture; `RL_O33` was never set.
3. **Walker's ceiling went UP +13.98**, not down. The ladder cuts a projection; it cannot raise a ceiling.
4. **Scale.** At Walker's `j = 10` the ladder would multiply the post-peak stream by
   `O33_TALL_LADDER[10]/DELTAS[10] = 0.4030/0.660 = 0.611` — a ~39 % cut, in the −1,493 / −399 class ORDER B's
   own preview measured on Wilkie and Andrews. The observed move is **−1 on 129**.

**The ladder is dead. One tall veteran nonetheless fell by one point, through the conservation renorm, and it
is reported rather than rounded away.**

## 6. The template — `ui/templates/movers.html`, first live use, and how it went

Attempted for real (`d8_template_try.py`, output `TEMPLATE_TRY_out.txt`), filling every slot the D8
comparison can fill **honestly** and passing `slots.ABSENT` only where the manifest declares nullability.
**Verdict: it does not fit this deliverable.** Three findings, in the order they bite:

1. **There is no `age` slot.** The row block is `name / pos / club / played / score / prev_value /
   cur_value / value_change / value_change_pct` + the six rank columns. The owner's probation question *is*
   about age; the order names age as a required column; and the layout law forbids a seat adding one.
2. **`played` is mandatory and has no honest value here.** `slots.validate()` returned exactly one distinct
   problem, 559 times: `row N of 'players' is missing column 'played'`. In the weekly report it means "did he
   play this round". In a **lever** comparison both sides are the same round on the same store and whether a
   player played is not a fact of the comparison. Filling it would be the dash-that-says-nothing the template
   exists to forbid, in a different costume. It was left unsupplied and the validator was allowed to say so.
3. **`previous_round` assumes a round boundary.** Both boards are round 22. `from_label`/`to_label` are free
   text and filled honestly; `previous_round == as_of_round == 22` renders a comparison that did not happen.

**What did fit, and is worth keeping:** `score` is correctly declared nullable and `ABSENT` was accepted;
the identity stamp carries **both ends** of the comparison, which is exactly right for a lever diff; and all
six rank columns are computable and meaningful across a lever (rank on the base board vs rank on the priced
board) — they were computed and are in `MOVERS_D8.json`. On 29 of its 30 slots the template took the payload.

**Delivered in** the v757 / house movers format (`MOVERS_D8.md`), which carries age and the per-band
attribution. **Recommendation, not this seat's to land:** the schema wants a **sibling** — a *lever-movers*
template with `age`, no `played`, no `previous_round`, and the both-ends stamp kept verbatim. That is a
template **addition**, not an edit, and it belongs to whoever owns `ui/templates`.

## 7. Findings this seat did not go looking for

1. **A canonical-mode build cannot run inside `tools/build_lock.sh`.** The lock exports
   `RL_BUILD_LOCK_HELD`; `config_manifest.enforce()` scans every `RL_`-prefixed variable and rejects unknown
   ones; so the build HALTS on line one with
   `UNKNOWN model override RL_BUILD_LOCK_HELD='…' is not in the manifest`. Measured on the **unedited** tree
   (`BASE_PREEDIT_out.txt`) and disclosed in the prereg before the edit. The two house tools — the interlock
   the estate built for exactly this seat, and the config gate every certifying build runs — are mutually
   exclusive today. The D8 driver drops the variable from the **child build's** environment only (the lock is
   still held by the parent shell's fd); the durable fix is one entry in `config_manifest.INFRA_ALLOW`, which
   is a change to a gate and therefore **not** this seat's to make. **Referred, not smuggled.**
2. **`ui/tools/extract_board_view.py` is not the sole writer of the bundle it says to regenerate with.** The
   file's own header says *"Do not hand-edit; regenerate via ui/tools/extract_board_view.py"*, but running it
   alone **deletes `stamp.release`** — eight carrier fields the release-manifest gate reads. The second writer
   is `round_movers.inject_release_contract`, and nothing in the bundle says so. Anyone following the header
   literally silently drops eight identity fields. Both writers were run here, in that order, and the round
   trip was verified byte-exact before use.
3. **The board carries 407 ceiling inversions today, not the 341 the ORDER B derivation measured.** Same
   defect, larger on the current store/board. Recorded for whoever re-reads the derivation.

## 8. What this seat did NOT do

* No adoption, no default flipped, no manifest amended, no board/store/config/register pin moved, no tag,
  no promote. The live board is `a05fe951` and stays there until the owner's word.
* `q97m` **not** refitted (frozen; R-W6 is bake-time). `_v7`, `_b6_core`, `V7_FORM_W` untouched.
* `frac()`, `O33_TALL_LADDER`, `O33_SSTAR`, `_o33_ladder` and the `s*` renorm site — **not touched**.
  `RL_O33` / `RL_O33_STAGE` semantics unchanged: `RL_O33=1 RL_O33_STAGE=2` still behaves exactly as before.
* `data/book_stable_seal.json` **not** re-sealed. Its `head_md5` reads SEALED-LAG, reported, non-gating.
* The two referred findings in §7 (the lock/manifest collision; the bundle's second writer) are **reported,
  not fixed** — both are changes to gates or to the UI generator contract.

## 9. Files

| file | what |
|---|---|
| `PREREG_D8.md` | the prereg, committed before the edit (`8eca222`) |
| `MOVERS_D8.md` | **the owner's movers list** — all 559, name·age·pos·before·after·Δ·%·Δceiling, + attribution |
| `MOVERS_D8.json` / `MOVERS_D8_out.txt` | machine-readable / raw |
| `BUILD_D8_out.txt` | the five builds, raw |
| `BANDS_D8_out.txt`, `BANDS_OFF.json`, `BANDS_ON.json`, `BANDS_*_rows.csv` | F2 + F4, per-row bands |
| `DAY0_D8_out.txt` | F5, off every build's own stdout |
| `ACCEPTANCE_D8_out.txt` | F6 |
| `RESTAMP_out.txt` | the four-field engine_head restamp |
| `TEMPLATE_TRY_out.txt` | the `ui/templates/movers.html` first-live-use attempt |
| `BASE_PREEDIT_out.txt` | the pre-edit base measurement + the build-lock finding |
| `d8_*.py`, `run_*.sh` | every driver, exactly as run |
