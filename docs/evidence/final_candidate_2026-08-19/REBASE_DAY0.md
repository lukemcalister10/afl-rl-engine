# DISCLOSURE — THE DAY-0 PRINT REFERENCE IS REGENERATED FOR THE FINAL CANDIDATE `daa16812`

**Branch `land/order-29`, from `origin/land/order-29` at `65ae9ab`. Engine `53fff6de` — UNCHANGED, and
no engine edit is made or needed. This is a REFERENCE/DATA change and nothing else.**

**This file is pushed BEFORE the reference is touched.** Nothing below is measured after the fact.

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing is on `main`.

---

## 1 · AUTHORITY

- **Register v763**, bake item: *"sitter print reference regeneration if day-0 moved — disclose as
  Orders D/K did."* The item was already ruled; it was queued for the bake.
- **Register v769**, the supervisor ruling on the final-candidate assembly, **pulls that item
  forward** and orders it executed now, with full disclosure, so the class mark and the no-arb page
  can be produced for `daa16812`.

This seat is not deciding that a regeneration is lawful. It was ruled lawful before this seat
existed. What this seat owes is the disclosure, the assertions, and the honest count.

---

## 2 · WHAT IS BEING REGENERATED, AND WHAT IS NOT

| | file | status |
|---|---|---|
| **the OLD reference** | `docs/evidence/order_k_2026-08-18/DAY0_K.json` (board `f3101883`) | **NOT TOUCHED.** Filed history. It stays. |
| **the NEW reference** | `docs/evidence/final_candidate_2026-08-19/DAY0_FC.json` (board `daa16812`) | written by `fcrb_day0.py` |
| the emitter | `docs/evidence/candidate_31f/emit_matrix_31f.py` | **NOT TOUCHED.** Byte-carried, as always. |
| the engine | `engine/rl_after/_merged_recover.py` `53fff6de` | **NOT TOUCHED.** |
| the guard | the ORDER 31-F replication proof inside the emitter | **NOT WEAKENED.** Same two legs, same tolerance 0. |

The re-point is `RL_DAY0_FINAL`, which the emitter already reads as an environment variable and which
`run_emit_FC.sh` already sets. **No code changes to make the guard pass. The guard is pointed at the
reference for the law it is guarding, which is what it was built to do** — the emitter's own header
calls this "a declared re-point in the disclosed-copy convention, at each candidate's reading"
(supervisor's filed basis resolution, #334 comment 5310447449).

---

## 3 · THE THREE ROWS, WITH THE OLD AND NEW PRINTED DAY-0

Straight off the guard's own halt output (`EMIT_FCCAND_out.txt`, committed at `65ae9ab`, unedited):

```
ORDER 31-F HALT (replication): 86 of 89 wired entrants reproduce the board's printed day-0 at
tolerance 0. Mismatches: [('sam-allen', 450, 428, 791.8152857422534),
('ollie-murphy', 196, 200, 398.35828513161437), ('kobe-mcdonald', 40, 37, 87.02989219418069)].
```

The tuple is `(key, the reference's printed, the printed integer THIS law forms, the raw entry
object)`. Written out:

| row | pathway | depth on the sheet | **printed day-0 OLD** (`DAY0_K.json`) | **printed day-0 NEW** (`daa16812`) | move | `derived_v0` old → new |
|---|---|---:|---:|---:|---:|---|
| `sam-allen` | ND pick 29, MID | 1.58 | **450** | **428** | **−22** | 791.8152857422534 → **791.8152857422534** — *unchanged* |
| `ollie-murphy` | ND pick 41, KPD | 3.58 | **196** | **200** | **+4** | 398.35828513161437 → **398.35828513161437** — *unchanged* |
| `kobe-mcdonald` | IRE pool, `IRE\|SD` | 1.58 | **40** | **37** | **−3** | 87.02989219418069 → **87.02989219418069** — *unchanged* |

**All three are annotated `injured=Y`** on `docs/owner_annotations/SITTER_2026_v1.csv`
(md5 `b26798c35adcd9bda5cef50ff2c884da`, the value the engine itself pins and asserts):

```
Sam Allen,West Coast,MID,19,ND,2025,0,0,never,1.58,0.707,never,618,Y,
Ollie Murphy,Fremantle,KPD,21,ND,2023,0,0,never,3.58,0.308,never,168,Y,
Kobe McDonald,St Kilda,SD,19,IRE,2025,0,0,never,1.58,0.707,never,85,Y,
```

**Two of the three move DOWN and one moves UP.** The regeneration is not a one-way haircut and is not
presented as one.

---

## 4 · THE MECHANISM — SHEET-AS-INJURY-TRUTH MOVES THE **FADE**, NOT THE ENTRY VALUE

**A day-0 price for a man who has never played is `round(day0_v0(p) × D(c_u))` — an entry value
multiplied by the sitting fade.** Two objects, and only one of them moves.

**`RL_O42=1` re-keys the availability layer onto the owner's annotation sheet** (engine
`_merged_recover.py` §"ORDER 42 — THE INJURY CONSOLIDATION", register v760, owner-ruled *"The old LTI
register can be redundant. A - run it."*). It retires the live consumption of `LTI_REGISTER.md` and
builds `_AVAIL_STATE` from the sheet instead, re-basing the availability haircut from `1 − g/22` to
`1 − g/18` — the owner's **availability** base, deliberately not the season constant.

`_AVAIL_STATE` feeds `_fe_p_one` / `_fEy`, and **`_fEy` is an input to the UNPLAYED CLOCK `c_u`**
(`o31_cu`), which is the single argument of the sitter fade `o31_D`. So for a wired entrant who
appears on the sheet, `c_u` moves, `D(c_u)` moves, and the printed integer moves with it.

**The entry object does not move, and the guard itself proves it.** The ORDER 31-F guard has TWO legs
at tolerance 0:

- **(a)** `int(round(_landed_v0_board(q) × o31_D(q, BASE_REF)))` against `::printed` — **this is the
  leg that failed on the three rows.**
- **(b)** `abs(_landed_v0_board(q) − ::derived_v0) == 0.0` — **this leg PASSED on 89 of 89.** The
  halt tuple's fourth element is `_landed_v0_board(q)` itself, and for every one of the three it is
  bit-identical to the value `DAY0_K.json` already carries as `derived_v0`.

`fc_v0.py`'s own self-check at `65ae9ab` reads the same three numbers off the candidate's engine state
and agrees at tolerance 0.

**CONSEQUENCE, AND IT IS THE ONE THAT MATTERS: the walk-forward matrix's year-0 column does not move
at all.** The regeneration touches the *printed* day-0 column of the reference and nothing else.

### 4a · A CORRECTION TO `PACKET_FINAL.md` §4a, MADE AGAINST THIS SEAT'S OWN CONVENIENCE

`PACKET_FINAL.md` §4a at `65ae9ab` prints a table headed *"the availability layer reaches the
entry-price objects"*, reading `sam-allen 833.3 → 791.8`, `ollie-murphy 419.2 → 398.4`,
`kobe-mcdonald 91.6 → 87.0`, and concludes *"the candidate's year-0 law genuinely is not ORDER K's
published one."*

**Those three "base" numbers are not measured anywhere in that evidence set.** They appear only in the
docstring of `fc_v0.py`; `fc_v0.py` loads the engine **once**, on the candidate line only, and never
evaluates the base line. Its printed output (`V0_FC_out.txt`) contains one column, the candidate's.

**And the guard's leg (b) contradicts them.** If `_landed_v0_board(sam-allen)` were 833.3 on the base
and 791.8 on the candidate, then the base emit — which reads **89 of 89** against this same
`DAY0_K.json` whose `derived_v0` is 791.8152857422534 — could not have passed. It did pass, at
tolerance 0, and its matrix was written.

**The corrected statement:** `derived_v0` is bit-identical across ORDER K's board, `FC_BASE`
`ff936186` and `FC_CAND` `daa16812`. **What `RL_O42` moves is the sitter fade `D(c_u)`, through the
availability clock.** The conclusion that a regeneration is required is **unchanged** — the printed
day-0 really does move on three rows — but the reason stated for it was wrong, and the corrected
reason is a *narrower* claim, not a wider one. It is recorded here rather than quietly fixed.

`derived_v0` is bit-identical on **89 of 89** and that is asserted, not asserted-away — see §6, A2.

---

## 5 · THE PRECEDENT — ORDERS D AND K DID THIS, IN THIS FORMAT

| order | what moved the fade | printed day-0 rows that moved | `derived_v0` | disclosed where |
|---|---|---:|---|---|
| **ORDER D** | the pick-curve fade `D^κ(pick)` landed | the sitter print reference regenerated | unmoved | `PACKET_D_WIRED.md` |
| **ORDER J** | the floor-fix / tall lane | regenerated | unmoved | `PACKET_J.md`, `DAY0_J_TALL.json` |
| **ORDER K** | the owner-ruled tall/small factor | **87 of 89** (30 up, 57 down) | **bit-identical 89/89** | `PACKET_K.md` §8, scorecard line **G6b** |
| **THIS PASS** | `RL_O42=1`, sheet-as-injury-truth → `c_u` | **3 of 89** (1 up, 2 down) | **bit-identical 89/89** | this file, and `PACKET_FINAL.md` §4 |

ORDER K's own generator states the rule this seat is following:

> *"A day-0 price for a man who has never played IS his entry value multiplied by the sitting
> discount... So the printed day-0 of every wired sitter moves BY CONSTRUCTION the moment the ruled
> factor is live, and the landing candidate's own day-0 file cannot match. What does NOT move is
> `derived_v0`... This is the same regeneration ORDER D's own pick-curve fade required when it landed,
> and the same one ORDER I disclosed. It is DISCLOSED on the packet, not buried here."*

**Three of 89 is the smallest regeneration in the sequence, by a wide margin.** ORDER K moved 87.

---

## 6 · THE ASSERTION PLAN — WHAT `fcrb_day0.py` WILL REFUSE TO WRITE THROUGH

`fcrb_day0.py` is `ok_day0.py` carried, with four declared changes: the board path, the dial line, the
output name, and **a new assertion block**. Every assertion is HARD — it raises and writes no
reference — and every one of them is PRINTED into `REBASE_DAY0_out.txt` whether it passes or fails.

| | assertion | HALTS ON |
|---|---|---|
| **A1** | same 89-key set as `DAY0_K.json` | the wired-entrant population changing |
| **A2** | `derived_v0` **bit-identical on 89 of 89** | **any** movement in the matrix year-0 column |
| **A3** | **exactly three** rows move on `printed`, and they are exactly `sam-allen`, `ollie-murphy`, `kobe-mcdonald` | **a fourth mover, OR a named row that fails to move** |
| **A4** | each mover's new printed integer equals the guard's own diagnosed value (**428 / 200 / 37**), and each mover's `derived_v0` equals the guard's own `_mb` | any disagreement with the halt output |
| **A5** | **every moved row is `injured=Y`** on the pinned sheet `b26798c3…` | **a mover that is not sheet-annotated** |
| **A6** | the 86 non-movers are byte-identical on **every field** — `ty pos pick cell printed derived_v0 fade_D day0_price` — not merely on `printed` | a non-mover moving on any field |
| **A7** | ORDER K's own check: the printed-day-0 identity holds **89 of 89 at tolerance 0 on the WRITTEN board** `daa16812` | the identity failing on the board itself |

Only **10 of the 89** wired entrants are annotated on the sheet at all, so A5 has real teeth: it is a
subset test against a set of 10, not against the whole board.

**After the reference is written, the emit is re-run against it and must read 89 of 89.** If it reads
anything else, that is reported as a failure and no matrix is used.

---

## 7 · WHAT THIS DISCLOSURE DOES NOT CLAIM

- **It does not claim the candidate is adopted.** Priced, not adopted.
- **It does not claim Guard 5 is green.** Guard 5 is RED on this branch, pre-existing (register v767
  item C3, the stale rl_model pin). It is not re-pinned here and it is not scored as a pass anywhere.
- **It does not claim the class mark or the no-arb numbers before they are measured.** They are
  produced after this, on the regenerated reference, and reported at whatever they read.
- **It does not claim the regeneration is small because small is better.** Three of 89 is what the
  guard measured. If a fourth row had moved, this file would say four.
- **U0 = 7 return games is carried as OWNER-RULED, DATA-SUPPORTED**, both halves, wherever quoted.

---

## 8 · FILES

| file | what |
|---|---|
| `REBASE_DAY0.md` | this disclosure — **pushed before the reference is touched** |
| `fcrb_day0.py` | the regenerator: `ok_day0.py` carried, plus the assertion block |
| `REBASE_DAY0_out.txt` | the raw run, assertions printed pass or fail |
| `DAY0_FC.json` | the regenerated reference, board `daa16812` |
| `docs/evidence/order_k_2026-08-18/DAY0_K.json` | the OLD reference — untouched, filed history |
