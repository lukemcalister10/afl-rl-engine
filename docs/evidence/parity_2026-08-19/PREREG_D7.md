# PREREG — ORDER D7, **THE PARITY GUARD**

**Branch `land/order-29`, from `origin/land/order-29` at `d5c37da`. Engine at prereg time:
`53fff6de156efa870da11edc5cbaa75a` — UNTOUCHED.**

**THIS FILE IS PUSHED BEFORE THE ENGINE IS EDITED (F6).** Nothing below is written after the fact.

> ## THE BOARD WILL BE **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing goes to
> `main`. The owner reviews the parity table before any completion pass.

---

## 1 · AUTHORITY — THE RULING, VERBATIM

Register **v771** on `main`, the owner:

> "Being marked as injured shouldn't all of a sudden enrol you to a mechanism that doesn't affect
> your peers. In other words, a first year sitter who is injured is punished harder for it. No
> thanks."

**The principle this encodes:** an annotated-injured row must **NEVER price below its healthy
counterpart.** Injury status may **SHIELD** — the KPF fork-v exclusion, the credited absence, the R3
injured-exemption — but it may **never ADD net charge** beyond what the healthy machinery would take
from the same row.

### 1.1 · The superseded document at the tip

The tip commit `d5c37da` is a disclosure for a day-0 print-reference regeneration. That document is
**SUPERSEDED by this ruling and is not acted on by this seat.** The frozen reference
`docs/evidence/order_k_2026-08-18/DAY0_K.json` was never touched and is not touched here. A later
pass amends that document.

---

## 2 · THE BASE — REPRODUCED BEFORE ANYTHING ELSE

The first pricing act of this seat, performed **before** this prereg was written and before any
engine edit:

```
RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1
```

| | value | status |
|---|---|---|
| board md5 | `daa16812e50fb71241e627d89180412c` | **REPRODUCED BYTE-EXACT** |
| total | **660,578** | matches |
| rows | **804** | matches |

Pins, all verified on this worktree: engine `53fff6de`, store `cb38ef11`, v0surf `5dd34ca8`
(pin `5dd34ca8`), sheet `b26798c35adcd9bda5cef50ff2c884da` (prefix `b26798c3`, asserted).
`RL_V0SURF_PKL` is bound explicitly to **this branch tree's own** `data/v0surf.pkl` on every run
(register v767 footgun).

---

## 3 · THE HAZARDS, ENUMERATED BEFORE THE BUILD

### 3.1 · The `RL_AVAIL=0` control board is UNBUILDABLE — and is not used

`docs/evidence/consolidation_2026-08-19/` records the halt and it stands:

> v0surf FROZEN-SIGNATURE HALT: this build's config signature `3ebc60f0` is NOT in
> `data/v0surf.pkl` (frozen: `41af7326`, `4405cba2`). The engine will NOT silently re-fit the V0
> pick-curve surface.

`RL_AVAIL` is part of the frozen config signature and only `RL_AVAIL=1` signatures are frozen. A
layer-off control board cannot be built without a v0surf **refit** — a bake act, outside this seat,
and one that would make the control non-comparable to the board it controls. **Reported, not
improvised around. This seat does not build it and does not need it.**

### 3.2 · `_ev_off` IS NOT THE HEALTHY COUNTERPART — the D6 read is insufficient here

The D6 seat read the engine's own in-process attribution `_AVAIL_MOVERS`
(`_ev_off → _ev_p1 → _vfull`). That was right for D6's question and is wrong for this one.

`_ev_off` is **layer-off**: it empties `_AVAIL_STATE` and zeroes `_avail_hc`. It does **NOT** clear
`o41_injured(p)`, which is built from `_O41_INJSET` — a **separate** read of the same sheet under
`RL_O41_INJ`. So under `_ev_off` the row still carries:

- the **R3 injured-exemption** (`o41_r3_take` returns `0.0` for an injured row),
- the **sitter-clock pause** (`o31_cu`: the live season's absence accrues nothing),
- the **absence-depth exemption** (the in-progress season is not added to the run).

All three are **SHIELDS**. A counterpart carrying them **UNDERSTATES the healthy charge**, which
would make the guard lift rows it has no business lifting. `_ev_off` is therefore **NOT USED** as the
counterpart, and this is the single most important design point in this prereg.

### 3.3 · If the honest counterfactual could not be computed → HALT

Per the order, if the healthy counterfactual could not be computed in-process or by a per-row
counterfactual evaluation with the row's injured flags cleared, this seat **HALTS and reports the
obstacle precisely** rather than approximating silently.

**IT CAN BE COMPUTED.** A **read-only feasibility probe** (`no engine file edited`, run before this
prereg, recorded at `docs/evidence/parity_2026-08-19/FEAS_D7_out.txt`) loaded the engine in-process
on the base dial line, neutralised every injury site for a row, evaluated, and restored. It returned
finite values on the four alphabetically-first annotated rows and **restored the row's original
value exactly (`restore_ok=True`) in every case.** The probe measured **feasibility only**. No dial
constant is derived from it — **this dial has no constant to derive** (§5).

### 3.4 · Guard 5 is RED on this branch

Pre-existing C3 pin staleness. It is **RECORDED, NEVER CLAIMED GREEN, AND NOT RE-PINNED** by this
seat.

---

## 4 · THE HEALTHY COUNTERPART — THE EXACT WIRING

**Definition.** The same row as the engine would price it **if the player had simply never been
logged injured anywhere** — with its absences charged by the normal machinery (R3 production fade,
sitting charges) exactly as a healthy peer's would be.

Every live injury-consumption site in `engine/rl_after/_merged_recover.py` at `53fff6de`, enumerated
exhaustively. There are **two** keying objects and **seven** sites:

| # | keyed on | line | site | direction |
|---|---|---:|---|---|
| 1 | `_AVAIL_STATE[key]` | 127–132 | `_fe_p_one`/`_fEy` — the `fE=1.0` season-complete override | **CHARGE** |
| 2 | `_AVAIL_STATE[key]` | 1244 | the KPF fork-v 2026-exclusion / nuked season | SHIELD |
| 3 | `_AVAIL_STATE[key]` | 1451 | the L1c clock, `g += L*cp.SEASON` (`RL_LTI_CLOCK=advance`) | **CHARGE** |
| 4 | `p['_avail_hc']` | 1339, 1389 | the Part-1 present haircut `L_p` | **CHARGE** |
| 5 | `p['_lti_ret_hc']` | 1265 | the Part-2 return haircut (retired under `RL_O42`; ships 0) | CHARGE |
| 6 | `o41_injured(p)` | 4139 | `o31_cu` — the sitter clock PAUSES on a logged-injured live season | SHIELD |
| 7 | `o41_injured(p)` | 4912/4926/4945, 5007 | `o41_absence_depth` in-progress term + the **R3 exemption** | SHIELD |

**The counterpart evaluation, per annotated row `p`:**

1. `_AVAIL_STATE.pop(p['key'])` — kills sites 1, 2, 3.
2. `p['_avail_hc'] = 0.0` — kills site 4.
3. `p['_lti_ret_hc'] = 0.0` — kills site 5.
4. `o41_injured(p)` forced `False` for this row only — kills sites 6, 7.
5. `v_healthy = ev(p, 2026)`.
6. **Every mutation is restored** and the row's original value is **re-asserted equal** before the
   next row is measured. A restore failure is falsifier **D7-F6**.

Steps 1–3 alone are `_ev_off`. **Step 4 is the difference between `_ev_off` and an honest healthy
counterpart, and it is the whole point** (§3.2).

**Basis.** The counterpart is evaluated **after** `MA._O36_SCOPE['armed']=True` — i.e. on the *same*
S1-armed basis the board price is formed on. Measuring it on the unarmed attribution basis (where
`_ev_off`/`_ev_p1`/`_vfull` live) would compare two different currencies.

**Scope, DISCLOSED as a seat choice the owner may overturn.** The guard applies to the **live board
price, `Y = 2026`** — the price the owner reads and the one the parity table reports. It is not
applied to the `vM2/vM1/vP1/vP2` display columns: the annotation is a **2026 log**, the availability
charge is a **2026-only object**, and guarding past seasons would rewrite history the owner did not
rule on. **Stated here so it cannot be glossed later.**

---

## 5 · THE DIAL AND THE RULE

**One dial: `RL_O43`.** Next free number after `RL_O42` on the engine's own convention; verified free
— `RL_O43` appears nowhere in the tree at `d5c37da`. It goes on the dial line. **No other engine
change is made.**

**The rule, per annotated row:**

```
final price  =  max( v under the injury regime , v under the healthy-counterpart regime )
```

**THERE IS NO FREE PARAMETER IN THIS DIAL.** `max` has no constant to fit, no threshold, no curve,
no exponent. Target-fitting is **structurally impossible** here, and that is stated as a property of
the encoding, not as a promise about this seat's conduct.

**It can only RAISE a row, never lower one.** A single falling row is a **HALT** (D7-F1).

**Murphy-type risers stand.** A row whose injury regime already prices **ABOVE** its healthy
counterpart keeps the higher value — the shield is not a charge, and the guard does not claw it back.

**Dial unset ⇒ not one byte of the D7 block executes ⇒ `daa16812` reproduces byte-exact** (D7-F2).

**The guard lives inside `ev()`.** `rl_export.py:650–660` runs a hard export↔engine parity gate —
every board value must equal `round(engine ev(p,2026)/F)` at tolerance 0. A post-hoc adjustment to
the written board would fail that gate. The guard is therefore installed as a wrapper on `ev` in the
engine's **own** established `_ev_preXX = ev` convention (the same pattern used at lines 3212 and
3325), placed after the S1 arming and before the `print("=== AFTER` split that `rl_export` execs to.

---

## 6 · MEMBERSHIP

- **The annotated rows** — `docs/owner_annotations/SITTER_2026_v1.csv`, md5 prefix `b26798c35adcd9bd`
  (**asserted**, full `b26798c35adcd9bda5cef50ff2c884da`), 219 rows, **37 marked `injured=Y`**.
- The guard applies to **every row carrying injury treatment**. Under `RL_O42=1` that set is exactly
  the 37 annotated rows: `_AVAIL_STATE` is built solely from the sheet (`_o42_state`), and
  `_O41_INJSET` is built solely from the sheet. Both resolve to 37.
- **Register-only rows.** `LTI_REGISTER.md` carries **43** keys; **21** of them are not annotated.
  Under `RL_O42=1` the register has **no live consumption**, so those 21 carry **no injury treatment
  of any kind**. **EXPECTED: none of them needs the guard. This is ASSERTED IN THE BUILD, not
  assumed** — the parity table reports them too, and a register-only row found carrying treatment is
  falsifier **D7-F5**.
- **Cohort clock:** MSD = draft year; everyone else draft year + 1. Depths are quoted **as depths**.

---

## 7 · THE FALSIFIERS — NAMED, WITH FIRE CONDITIONS

Every one is checked in the build and reported **whatever it says**.

| id | claim | FIRES IF | if it fires |
|---|---|---|---|
| **D7-F1** | **NO ROW FALLS.** The guard is a `max`; it can only raise. | any row on the priced board prices **below** its value on `daa16812` | **HALT.** The board is not delivered as priced. The falling row, its key, both values and the mechanism are reported raw. |
| **D7-F2** | dial unset reproduces the base | `RL_O43` unset does not give `daa16812` byte-exact | **HALT.** The dial is not clean; nothing is priced. |
| **D7-F3** | **`allen` and `mcdonald` RESTORE to 450 and 40** — *if* their healthy counterparts charge zero. **STATED AS EXPECTED, VERIFIED NOT ASSUMED.** | either row's guarded day-0 print ≠ its frozen `DAY0_K.json` print (450 / 40) | **REPORTED, NOT A HALT.** These rows **ILLUSTRATE, THEY DO NOT GATE.** If the healthy counterpart charges something non-zero the restore is *incomplete by mechanism*, and the honest number is reported with the charge that explains it. **No constant is touched to make this land.** |
| **D7-F4** | **`murphy` KEEPS HIS RISER.** His injury regime prices above his healthy counterpart and the guard leaves him alone. | `murphy`'s guarded value ≠ his unguarded value on `daa16812` | **REPORTED.** A move on murphy means the guard is clawing back a shield, which contradicts the ruling — that would be a **HALT**. |
| **D7-F5** | no register-only row carries injury treatment | any of the 21 register-only keys appears in `_AVAIL_STATE` or `_O41_INJSET`, or its floor differs from its value | **REPORTED** with the row named. D6's consolidation claim would be incomplete. |
| **D7-F6** | the counterfactual is **non-destructive** | after a row's healthy evaluation, its restored `ev(p,2026)` ≠ its pre-probe value | **HALT.** The measurement is corrupting the board and nothing it produced can be trusted. |
| **D7-F7** | determinism | two identical `RL_O43=1` runs do not give the same board md5 | **HALT.** |
| **D7-F8** | **day-0: ONLY `ollie-murphy` moves** vs the frozen `DAY0_K.json` prints. **VERIFY, DO NOT ASSUME.** | any wired entrant other than `ollie-murphy` moves against the frozen reference | **REPORTED** with the full mover list, raw. The frozen reference is **NOT** regenerated by this seat. |
| **D7-F9** | scope | any mover on the priced board lies **outside** the 37 annotated rows | **REPORTED** and investigated; a leak outside the treated set means the guard is not row-local. |

**No named player gates anything.** Allen, McDonald, Murphy, Green, Martin, Hinge and Powell-Pepper
appear in the parity table and in the claims note **as illustrations of a rule that was fixed before
they were looked at.**

---

## 8 · ACCEPTANCE IDENTITIES TO BE RUN

| chain | expected board |
|---|---|
| `RL_O43` unset, base line | `daa16812` |
| `RL_O42` unset chain | `ff936186` |
| every `RL_O41*`+ dial off | `374d4e44` |
| ORDER K chain | `f3101883` |
| R20A / owner's reference | `7f88f509` |

Plus: determinism ×2 on the priced board, and the day-0 report against the frozen `DAY0_K.json`.

---

## 9 · DELIVERABLES

`docs/evidence/parity_2026-08-19/` — this prereg (own commit, pushed first), the engine edit (one
dial, nothing else), the priced board with identity/total/movers, **the parity table** (every
annotated row: games this season, v under the injury regime, v under the healthy counterpart, which
side won, the delta — plus the register-only rows), the acceptance identities, and the day-0 report.

**Priced, not adopted.** Guard 5 stays RED and is not claimed green.
