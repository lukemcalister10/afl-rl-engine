# ORDER D7 — THE PARITY GUARD — DELIVERY PACKET

**Branch `land/order-29`, from `origin/land/order-29` at `d5c37da`. `PREREG_D7.md` pushed at
`04ef467` BEFORE the engine was touched.**

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing is on
> `main`. **The owner reviews the parity table before any completion pass.**

---

## 1 · THE RULING AND THE ENCODING

Register **v771**, the owner, verbatim:

> "Being marked as injured shouldn't all of a sudden enrol you to a mechanism that doesn't affect
> your peers. In other words, a first year sitter who is injured is punished harder for it. No
> thanks."

**One dial, `RL_O43`.** Per row carrying injury treatment:

```
final price = max( v under the injury regime , v under the healthy-counterpart regime )
```

**NO FREE PARAMETER.** `max` has no constant, threshold, curve or exponent. Target-fitting is
structurally impossible in this lever — a property of the encoding, not a promise about conduct.
It can only **RAISE** a row. Murphy-type risers keep their higher value: **the shield is not a
charge.**

---

## 2 · THE BOARD

| | value |
|---|---|
| **THE PRICED BOARD** | **`a05fe951f78482c70520480e184c80ec`** |
| total | **664,949** (base 660,578, **+4,371**) |
| rows | **804** |
| movers vs `daa16812` | **23 — every one UPWARD** |
| engine | `29376d5a73a3e8274fcebe5cd90ada0b` (base was `53fff6de`) |
| store / v0surf / sheet | `cb38ef11` / `5dd34ca8` / `b26798c35adcd9bda5cef50ff2c884da` |

`RL_V0SURF_PKL` bound explicitly to this branch tree's own `data/v0surf.pkl` on every run (v767).

### Acceptance identities — ALL PASS

| chain | expected | got |
|---|---|---|
| `RL_O43` unset (**D7-F2**) | `daa16812` | **`daa16812`** PASS |
| `RL_O42` unset chain | `ff936186` | **`ff936186`** PASS |
| every `RL_O41*`+ dial off | `374d4e44` | **`374d4e44`** PASS |
| ORDER K chain | `f3101883` | **`f3101883`** PASS |
| R20A reference | `7f88f509` | **`7f88f509`** PASS |
| determinism ×2 (**D7-F7**) | equal | `a05fe951` / `a05fe951` PASS |

**PRINTED-DAY-0 ASSERT on the priced board: 89 of 89 at tolerance 0.**

---

## 3 · THE FALSIFIERS — WHAT FIRED AND WHAT DID NOT

| id | claim | result |
|---|---|---|
| **D7-F1** | **no row falls** | **DID NOT FIRE** — all 23 movers move UP |
| **D7-F2** | dial unset reproduces the base | **DID NOT FIRE** — `daa16812` byte-exact |
| **D7-F3** | allen → 450, mcdonald → 40 | **DID NOT FIRE — BOTH RESTORE EXACTLY** |
| **D7-F4** | murphy keeps his riser | **DID NOT FIRE** — 200 → 200, untouched |
| **D7-F5** | no register-only row carries treatment | **DID NOT FIRE** — 0 of 20 |
| **D7-F6** | counterfactual non-destructive | **DID NOT FIRE** — every row restored exactly |
| **D7-F7** | determinism | **DID NOT FIRE** |
| **D7-F8** | **day-0: only `ollie-murphy` moves** | ### ***FIRED*** — **6 entrants move, not 1** |
| **D7-F9** | movers inside the treated set | **DID NOT FIRE** — 23 of 23 inside |

### D7-F8, THE ONE THAT FIRED — reported, not smoothed

Against the **frozen** `docs/evidence/order_k_2026-08-18/DAY0_K.json` (board `f3101883`), **six**
wired entrants move, not one. **The frozen reference is NOT touched by this seat** — it is read,
never rewritten. The superseded regeneration document at `d5c37da` is **not acted on**.

| key | frozen | priced | delta | annotated `injured=Y` |
|---|---:|---:|---:|---|
| `harley-barker` | 481 | 504 | **+23** | Y |
| `blake-thredgold` | 372 | 381 | **+9** | Y |
| `max-king-syd` | 129 | 138 | **+9** | Y |
| `liam-hetherton` | 66 | 70 | **+4** | Y |
| `ollie-murphy` | 196 | 200 | **+4** | Y |
| `noah-chamberlain` | 37 | 40 | **+3** | Y |

**All six are annotated `injured=Y`.** Every move is **upward**. `sam-allen` and `kobe-mcdonald`,
which moved DOWN against the frozen prints on the base board (450→428, 40→37), **no longer move at
all** — the guard restores them exactly. So the guard **reduces** the day-0 divergence from three
rows to… a different six: it removes the two downward movers and adds five upward ones, all inside
the annotated set. The prediction of "only ollie-murphy" was **wrong, and is reported wrong.**

---

## 4 · TWO DEFECTS THIS SEAT INTRODUCED AND CAUGHT — BOTH DISCLOSED

### 4.1 · The sentinel collision — the dial was DEAD CODE on the first candidate

`rl_export.py:68` truncates the engine source with a **bare substring split** on the banner string
`print("=== AFTER`. The first draft of the D7 block **quoted that sentinel verbatim in a comment**,
which truncated the exec **above** the block. Result: `RL_O43=1` was set, no banner printed, and the
candidate board came back **byte-identical to the base**.

**It was caught only because a guard that must move rows moved none.** The evidence is kept at
`BUILD_D7_SENTINEL_DEADCODE_out.txt`. A standing warning is now in the engine at the block itself.
**This is a real fragility in the harness, not only in this seat's comment**, and it is flagged for
the supervisor: any future comment containing that string silently deletes everything below it.

### 4.2 · The membership join — a script artifact briefly reported as three falsifier fires

The first parity run joined the sheet to the board by **normalising sheet names**, which mis-maps
three rows the engine resolves correctly:

| sheet name | naive join | **engine key** |
|---|---|---|
| `Maxwell King` (Sydney) | `maxwell-king` | **`max-king-syd`** |
| `Max King` (St Kilda) | `max-king` | **`max-king-stk`** |
| `Elliott Himmelberg` | `elliott-himmelberg` | **`elliot-himmelberg`** (engine spells one `t`) |

That artifact briefly showed **D7-F5** and **D7-F9** firing. **They do not fire.** All three rows are
annotated `injured=Y` (sheet lines 78, 126, 187). Membership is now read off the **engine's own**
`_D7_TREATED`, and the ORDER 42 builder independently **asserts** 37 names → 37 distinct
single-record keys. Recorded here rather than quietly corrected.

---

## 5 · THE SECOND WIRING SITE OF THE ONE DIAL — DISCLOSED

The first correctly-executing candidate **HALTED**, and the halt was right:

```
PRINTED-DAY-0 HALT: 7 of 89 day-0/sitter rows do not print round(derived v0 x sitter fade D(c))
x numeraire — ['Sam Allen printed 450 != 428.105725', ...]. Refusing to write the board.
```

ORDER 29B/30B installs a **permanent boot-class identity**: a day-0 row's printed price must equal
`round(day0_v0(p) × o31_D(p,Y))`, with the right-hand side read out of the engine's own
`_entry30b_price` precisely so board and engine cannot drift. The guard lifted a day-0 row to his
**healthy** price while `_entry30b_price` still recomputed the fade at his **live (injury)** depth —
**the engine was contradicting itself about the same row, and the assert caught it.**

**The fix is the SAME dial, SAME `max`, SAME `_O43` gate, applied to the engine's own predicate.**
The assert is **not weakened, not bypassed, not re-pointed**; `DAY0_K.json` is **not touched**.

For a zero-games row the one law collapses to `v = v0 × D(c_u)` exactly (`rho(0)=0`,
`o32_age_credit(...,0)=0`), so a max on the **value** is identically a max on the **fade**. The
predicate therefore substitutes the fade ratio `D_healthy / D_live` — in the predicate's own units,
so **no numéraire conversion can be got wrong**. Result: **89 of 89 at tolerance 0.**

This is a **second SITE**, not a second dial and not a second rule. It is called out here because
the order said one dial and no other engine changes: **one file is touched
(`engine/rl_after/_merged_recover.py`), one dial exists, and `rl_export.py` is NOT modified.**

---

## 6 · THE PARITY TABLE

Full table: **`PARITY_TABLE_out.txt`** · machine-readable: **`PARITY_D7.json`**.

**37 rows carry injury treatment · 23 LIFTED · 14 kept the injury-regime value (riser or tie) ·
total lift +4,371 board points.** Board currency (`round(ev/F)`, F = 1.0524).

### The lifted rows — the owner's complaint, priced

| player | g26 | v_injury | v_healthy | won | delta |
|---|---:|---:|---:|---|---:|
| Tom Green | 0 | 4,339 | **5,551** | HEALTHY | **+1,212** |
| Nicholas Martin | 0 | 3,199 | **4,168** | HEALTHY | **+969** |
| Connor Rozee | 2 | 2,559 | **3,380** | HEALTHY | **+821** |
| Joshua Kelly | 0 | 427 | **769** | HEALTHY | **+342** |
| Jack Viney | 0 | 254 | **559** | HEALTHY | **+305** |
| Brayden Fiorini | 2 | 182 | **349** | HEALTHY | **+167** |
| Darcy Jones | 0 | 1,095 | **1,244** | HEALTHY | **+149** |
| Mitchell Hinge | 1 | 194 | **303** | HEALTHY | **+109** |
| Sam Powell-Pepper | 0 | 97 | **173** | HEALTHY | **+76** |
| Thomas Sims | 0 | 670 | **737** | HEALTHY | **+67** |
| Harry Armstrong | 3 | 475 | **518** | HEALTHY | **+43** |
| Harley Barker | 0 | 481 | **504** | HEALTHY | **+23** |
| **Sam Allen** | 0 | 428 | **450** | HEALTHY | **+22** |
| Harry Edwards | 2 | 89 | **107** | HEALTHY | **+18** |
| Riley Garcia | 0 | 40 | **50** | HEALTHY | **+10** |
| Blake Thredgold | 0 | 372 | **381** | HEALTHY | **+9** |
| Maxwell King (Syd) | 0 | 129 | **138** | HEALTHY | **+9** |
| Jesse Motlop | 0 | 54 | **59** | HEALTHY | **+5** |
| Liam Hetherton | 0 | 66 | **70** | HEALTHY | **+4** |
| Josh Sinn | 0 | 159 | **162** | HEALTHY | **+3** |
| **Kobe McDonald** | 0 | 37 | **40** | HEALTHY | **+3** |
| Noah Chamberlain | 0 | 37 | **40** | HEALTHY | **+3** |
| Ollie Lord | 1 | 74 | **76** | HEALTHY | **+2** |

### The rows the guard leaves alone — risers and ties

| player | g26 | v_injury | v_healthy | won |
|---|---:|---:|---:|---|
| Max King (StK) | 0 | **209** | 78 | injury |
| Harry O'Farrell | 0 | **537** | 460 | injury |
| Lewis Hayes | 0 | **338** | 311 | injury |
| **Ollie Murphy** | 0 | **200** | 196 | injury |
| Josh Gibcus | 1 | **176** | 131 | injury |
| Henry Smith | 0 | **85** | 43 | injury |
| Judson Clarke | 1 | **55** | 49 | injury |
| Reef McInnes | 0 | **50** | 36 | injury |
| Andy Moniz-Wakefield | 2 | **38** | 23 | injury |
| Elliott Himmelberg | 0 | **31** | 16 | injury |
| Sam Sturt | 0 | **30** | 30 | injury |
| Nathan Wardius | 0 | 37 | 37 | tie |
| Ricky Mentha | 0 | 23 | 23 | tie |
| Rob Monahan | 0 | 37 | 37 | tie |

**Every one of these keeps its injury-regime value. The guard never claws a shield back.**

### The register-only rows — D6's consolidation claim CONFIRMED

`LTI_REGISTER.md` carries **43** keys; **20** are not annotated. **Zero** of them carry injury
treatment of any kind — not in `_AVAIL_STATE`, not in `_O41_INJSET`, no floor, and none appears in
the movers. Under `RL_O42=1` the register has **no live consumption**. **Asserted on this board, not
assumed.**

---

## 7 · THE HEALTHY COUNTERPART — WHY IT IS NOT `_ev_off`

`_ev_off` (the D6 attribution baseline) is **layer-off**, not healthy: it empties `_AVAIL_STATE` and
zeroes `_avail_hc`, but leaves `o41_injured` TRUE — so the row keeps **three shields** (the R3
injured-exemption, the sitter-clock pause, the absence-depth in-progress exemption) and its healthy
charge is **understated**. This guard neutralises **all seven** live injury sites per row
(`PREREG_D7.md` §4), including `o41_injured`, and evaluates on the **S1-armed** basis the board price
is formed on. Every mutation is restored and the row's original value re-asserted equal before the
next row (**D7-F6**, build-failing; it did not fire on any row).

The `RL_AVAIL=0` control board remains **UNBUILDABLE** (v0surf frozen-signature halt) and was **not
used and not needed** — the counterfactual is computed **in-process, per row**.

---

## 8 · NOT GREEN, AND NAMED

- **Guard 5 is RED** — pre-existing C3 pin staleness on this branch. **Not claimed green. Not
  re-pinned.**
- **D7-F8 FIRED** (§3). Reported, not smoothed.
- **Scope choice, disclosed:** the guard applies at **`Y = 2026`**, the live board price. The
  `vM2/vM1/vP1/vP2` display columns are **not** guarded (`PREREG_D7.md` §4). The owner may overturn
  this.
- The two seat-introduced defects in §4 are disclosed rather than quietly corrected.

---

## 9 · FILES

```
docs/evidence/parity_2026-08-19/
  PREREG_D7.md                      the prereg, pushed FIRST at 04ef467
  PACKET_D7.md                      this file
  PARITY_TABLE_out.txt              THE PARITY TABLE — the centrepiece
  PARITY_D7.json                    machine-readable rows/floors/movers/md5s
  d7_parity.py                      the parity harness (one engine load)
  build_D7.sh  bbD7.sh              the board build (strictly sequential)
  BUILD_D7_out.txt                  the delivered build — all identities, no halts
  BUILD_D7_SENTINEL_DEADCODE_out.txt  defect 4.1, kept as evidence
  BUILD_D7_DAY0HALT_out.txt         the day-0 halt of §5, kept as evidence
  base_repro_D7.sh  BASE_REPRO_D7_out.txt   the first pricing act
  feas_d7.py  FEAS_D7_out.txt       the read-only feasibility probe
```

**Priced, not adopted.**
