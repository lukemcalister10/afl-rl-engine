# PREREG — THE STAIRCASE FIX ADOPTION (ORDER 44), VARIANT B

> ## STATUS: **THE ACT DID NOT PROCEED. NOTHING WAS ADOPTED.**
>
> **The engine was never touched. No flip commit exists. `tools/land lever` was never run.** The dial
> `RL_O44_LVLMONO` still ships **`0` / OFF**, the live board is still
> `68be10c79d0ee096455754e084bcf757` / total **692,296** / **804** rows, and every pin, seal and
> carrier is exactly where the pricing seat left it at `5deda20`.
>
> **WHY: the gate this seat was told to pass BEFORE flipping — the B-RAW no-arb reading — FAILED.**
> The adopted arm puts **FOUR cells over the +14 % buy rail that were inside it on the live board**,
> and removes **none**. The rule was fixed before a single number was read (§4), and it says: *if ANY
> rail crosses → DO NOT LAND; commit the measurement evidence, report the crossing plainly, and END —
> the owner re-rules with the reading in front of him.* **That is what happened.** §4.2 is the reading.
>
> This file is kept as written, in the tense it was written in, because that is what a prereg is for:
> the predictions and the stop rule were committed **before** the measurement, and the measurement
> stopped the act. Everything below §4.2 describes an act that **was prepared and not performed**.

Written **BEFORE the engine is touched** (process law P9 / law F6).

**Seat:** adoption seat, THE STAIRCASE FIX · **Date:** 2026-08-21
**Pricing:** `docs/evidence/staircase_fix_2026-08-20/` — prereg `5f94a44`, correction `901e731`, edit
`1446dec`, engine_head repair `1590a37`, **pricing evidence `192fa71`** (packet + no-arb + movers, all in
history before this file).
**Register:** **v808 pending** — the register is the supervisor's pen and is **NOT touched by this seat**.

> **EVERYTHING BELOW IS A PREDICTION.** Where the tree disagrees with it, the tree wins, this file is
> corrected against the tree, and the error is named. Never the other way round.
>
> **NO PUSH.** This seat commits to the local branch only. The SOAK line and hand-verification stand;
> the supervisor verifies after this seat.

---

## 0 · THE WORD

The owner's adoption word, given **2026-08-21**, **verbatim**:

> **"Happy to lock in 1.22% and variant B"**

It follows his conservation ruling, verbatim:

> **"The conservation law I don't like, especially in this case. It's 0.6% to fix a bug, it's fine.
> Accept it."**

That first ruling was given on a **stale premise** — the "0.6 %" in it is the *conserved* reading's board
**burn** (−0.581 % variant A / −0.602 % variant B), not the mint. **The supervisor re-presented the true
measured figure — the RAW mint, 1.22 % — and the owner re-confirmed on the corrected number.** The
re-confirmation, not the 0.6 % sentence, is the ruling of record, and it is the lineage citation this
landing carries.

This seat did not create the approval and does not interpret it. It records one that exists and executes
the lane the word names.

### 0.1 LAW 9 — THE EXCEPTION IS ON THE OWNER'S WORD, STATED NOT NETTED

RULEBOOK v3 PART 3 sets `band_scar = 200` (±0.029 % of a 692,296 board). **Variant B raw mints
+8,385 SCAR = +1.2112 %, which is 41.9× the rail.** That is a **LAW 9 BREACH ON ITS FACE** and it is
**ACCEPTED BY OWNER WORD**, above. It is recorded as an accepted exception wherever conservation is
asserted in this act — never as a pass, never netted against anything.

One precision the pricing seat refused to round away and this seat carries: **"1.22 %" is the headline;
the ADOPTED arm's own measured mint is +8,385 SCAR = +1.2112 %** (variant A raw is the +1.2220 % arm).
The adopted board mints marginally **under** the figure the owner locked in, not over it.

---

## 1 · WHAT IS BEING DONE, AND THROUGH WHICH LANE

`RL_O44_LVLMONO` — ORDER 44's level-axis band monotoniser, priced 2026-08-20 and delivered **PRICED,
NOT ADOPTED** — moves from **default OFF** to **shipped default `smooth`** (VARIANT B, RAW), behind a
**DECLARED KILL-SWITCH**, through the **exact lane** the D8 adoption used (`register v798`) and the bake
before it (`f27482f`, `register v780`).

**`smooth` IS VARIANT B AND THE MAPPING IS READ OFF THE TREE, NOT ASSUMED.** The dial's five accepted
values are declared at `engine/rl_after/_merged_recover.py:408` (`_O44_MODES`); `MOVERS_B_RAW.json`
records `"dial": "smooth"` and the `sfx_build.py` driver passed it through `SFX_ENV`. `smooth+conserve`
is the **conserved** sibling and is **NOT** what is adopted — the conservation leg is rejected by the
owner's word.

**ONE ENGINE EXPRESSION CHANGES:**

```python
_O44_RAW=(os.environ.get('RL_O44_LVLMONO','0') or '0').strip().lower()
                                            ^^^  ->  'smooth'
```

plus the comment block above it, restamped to the bake idiom its declared family already uses
(`:619 :641 :675 :723 :741 :759 :778 :796 :855 :916 :1296`). **The block's technical content is kept
intact** — why it is not a manifest var, the exact-knot construction, the sortedness proof, the
scaffolding classification. Only the stale half is rewritten (`DEFAULT OFF` → the BAKE stamp).

**No other engine file is touched.** `conditional_prior.py` is not edited, no forest is refitted,
`cm_400.pkl` (`34faa865`) and `data/q97m.pkl` (`cfdc7321`) are read exactly as they are. `data/model_config.json`
is **NOT** touched — the dial is a declared kill-switch, not a manifest dial.

**COMMIT ORDER (P9):** this file → the **flip** (one engine commit) → the **landing** (`tools/land lever`).

---

## 2 · THE NUMERIC PREDICTIONS

Measured by the lander's own child builder (`tools/landing/_build_child.py`, the accepted disposable FV
builder `session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build`, `PYTHONHASHSEED=0`,
staging into a throwaway dir), strictly sequential, under the lander's flock.

### 2.1 The two builds

| # | build | prediction |
|---|---|---|
| **P1** | **BARE** — no model-semantics `RL_*` set at all, `RL_O44_LVLMONO` **unset** | board md5 **`219266fafeca5ed4fb0206a72bf37046`**, total **700,681**, **804** rows — **byte-exact** against the variant-B candidate board identity recorded in `MOVERS_B_RAW.json` (`cand_board_md5`) |
| **P2** | **KILL-SWITCH** — `RL_O44_LVLMONO=0` | board md5 **`68be10c79d0ee096455754e084bcf757`**, total **692,296**, **804** rows — **byte-exact** against the live board of record |

P1 is the whole meaning of "shipped default": the bare build must reproduce, byte for byte, the board the
owner looked at and approved — not a rebuild of it. P2 is the whole meaning of "declared kill-switch".
The lander additionally refuses a switch-OFF board **equal** to the switch-ON board (a dial that changes
nothing is dead or silently deleted); that positive control is part of the prediction.

### 2.2 The identities

Pre-edit values read from `data/expected_boot.json` and re-hashed from the tree.

| identity | before | prediction |
|---|---|---|
| `board` | `68be10c79d0ee096455754e084bcf757` | **MOVES** → `219266fafeca5ed4fb0206a72bf37046` |
| `engine_head` (md5 `_merged_recover.py`) | `3f4aa10b23102dc4f7362b73fc20ac7b` | **MOVES at the flip commit** — value unknown until the edit exists; **RECOMPUTED** from the edited source by the tree's own definition, never typed |
| `balanced_board_md5` | `556ad70d295923455982ae33e4b8bfd3` | **MOVES** — value unknown until built. The dial sits at `_b6_core`, which the balanced sibling posture (`RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`) also reaches. **BUILT** by `sibling_repin.py reconcile` (build-and-compare) and the derived value recorded — never typed. **If it comes back UNMOVED that is a finding, reported, not smoothed.** |
| `contract_sha256` | `8e6dcdbc89d63480f055b9e250729463c3c2ab67c8f1f90db3005ef2e832d0c7` | **MOVES** (it seals the moved identities) |
| `store` | `b745002eb0a0fbb1c34fa44f1ef708d6` | **DOES NOT MOVE** — a lever landing writes no store |
| `config` / `config_sha256` | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` | **DOES NOT MOVE.** The dial is absent from `data/model_config.json`; `config_manifest.enforce()` must keep **REJECTING** `RL_O44_LVLMONO` as an unknown model override in bake/gate/canonical mode. A canonical build can only ship its **baked-in default** and can never *carry* this name. **Asserted, not assumed.** |
| `rl_model` | `6fe7c4155866d80e8045bed2d3bf2802` | **DOES NOT MOVE** (file untouched) |
| `fv` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | **DOES NOT MOVE** (`engine/forward_valuation` untouched) |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | **DOES NOT MOVE** — FROZEN, Guard-5 pinned, no refit |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | **DOES NOT MOVE** — FROZEN (R-W6) |
| `v0surf` | `5dd34ca82735f5c8f021b1c7320df8f8` | **DOES NOT MOVE** |
| `register` (LTI) | `652d83e87780e415a01a2de6d8b3cc57` | **DOES NOT MOVE** |
| `as_of_round` | `23` | **HELD at 23** — no round is applied by a lever landing |
| **day-0** | — | **OFF.** No day-0 reference is regenerated or re-based by this landing. `DAY0_CP.json` is untouched and un-repointed. The M1b ruling stands: automation never re-bases itself green. |

### 2.3 THE FOUR NAMED PLAYERS — the rows this fix exists for

They must land at their **measured variant-B-raw** values, from `MOVERS_B_RAW.json`:

| player | before | **predicted after** | Δ |
|---|---|---|---|
| Max Kondogiannis (`max-kondogiannis`) | 359 | **409** | +50 (+13.93 %) |
| Josh Dolan (`josh-dolan`) | 247 | **311** | +64 (+25.91 %) |
| Charlie West (`charlie-west`) | 381 | **382** | +1 (+0.26 %) |
| Will Hayes (`will-hayes-b`) | 180 | **250** | +70 (+38.89 %) |

**Charlie West moves +1 under B raw.** Under BOTH *conserved* readings he goes **DOWN** (−2.36 %) — one of
the four rows the fix exists for ends up below where it started. That is a property of the conserved arms,
which are **not** adopted; it is recorded here so the record cannot later be read as if the conserved
number were this act's.

---

## 3 · WHAT THIS SEAT IS NOT DOING, DECLARED

* **NO PUSH.** Local commits only.
* **THE REGISTER IS NOT TOUCHED.** `LTI_REGISTER.md` and `docs/OPEN_ITEMS_REGISTER.md` are the
  supervisor's pen. v808 is *pending*, and the engine comment says "pending" rather than claiming it.
* **NO PARAMETER IS ADDED, FITTED OR TARGETED.** The midpoint-interpolation rule is parameter-free by
  construction (prereg §3); the flip moves one string literal.
* **NO ROUND IS APPLIED.** `as_of_round` is HELD at 23.

---

## 4 · THE GAP THAT MUST CLOSE BEFORE THE FLIP — AND THE DECISION RULE, SET IN ADVANCE

**THE NO-ARB TABLES AND THE RENDERED PAGE WERE EMITTED FOR THE CONSERVED PAIR, NOT FOR THE RAW PAIR.**
`NOARB_SFX_SFXACON.html` is `ratchet+conserve` and `NOARB_SFX_SFXBCON.html` is `smooth+conserve`. **The
adopted arm is `smooth` (B RAW) and its no-arb reading was NOT MEASURED by the pricing seat.** That seat
named the gap itself, in `PACKET_STAIRCASE.md` §0, and handed it forward.

**IT IS NOT COSMETIC, and the reason is measured:** on the conserved reading variant B put ND band
**PRIMARY picks 11-20 over the +14 % buy rail** — 12.71 % on the live board → **14.11 %** under
`smooth+conserve`, a **NEW no-arb breach** (variant A conserved read 13.83 % and did not cross). The raw
arms mint MORE than the conserved arms on every band the pricing act measured, so **B RAW may sit higher
still.** That is an **expectation, not a measurement.**

**THIS SEAT'S FIRST DRAFT PROPOSED TO CARRY THE GAP FORWARD AND LAND ANYWAY. THE COORDINATOR OVERRULED
THAT, AND WAS RIGHT TO** — the priced-delivery law puts the no-arb reading and the rendered page ahead of
the adoption, and a reading that exists for two arms the owner did not pick is not a reading of the arm he
did. **The measurement is therefore taken BEFORE the flip and before the landing**, and the decision rule
was fixed **before this seat read a single number**:

> **(1)** emit the no-arb bands + pool arms + class mark for B RAW exactly per the pricing seat's
> machinery; **(2)** render the page; **(3)** verdicts: **if NO rail crossing and class inside the law →
> proceed with the landing as briefed, folding the B-raw no-arb evidence into the act; if ANY rail crosses
> or the class mark breaches → DO NOT LAND**: commit the measurement evidence, report the crossing plainly,
> and **END** — the owner re-rules with the reading in front of him.

**THE RULE IS THE COORDINATOR'S, QUOTED, AND THIS SEAT DOES NOT SOFTEN IT.** "Any rail crosses" is read
against the **live board's own cell**, which is how the pricing seat read it: a cell that ALREADY breaches
on `68be10c7` and still breaches is an inherited red, not a new crossing; a cell that was inside the rail
and is outside it under B RAW **is** a crossing and stops this act. The class mark (F4) is the registered
W2 basis against floor 1.03 / buy rail 1.14.

### 4.1 · THE INSTRUMENT — a declared byte-carry, not a new tool

`build_braw_instruments.py` carries the pricing seat's five `sfx_noarb_*.py` files into
`braw_noarb_*.py` with **three declared changes and nothing else**, each asserted to have matched
**exactly once** or the carry halts: **(1)** `SFXBRAW` added to the label/candidate lists; **(2)** output
basenames suffixed `_BRAW` so this set can never overwrite or be confused with the pricing seat's
committed artifacts; **(3)** `SRC` introduced for the two inputs carried from that seat rather than
regenerated (`DAY0_SFXBASE.json` and the `EMIT_*_out.txt` logs). The emit itself is the pricing seat's own
`run_emit_SFX.sh`, unmodified, at `SFX_LABEL=SFXBRAW RL_O44_LVLMONO=smooth`, under the build lock, against
the same day-0 reference, with the same `RL_CONFIG_MODE`-unset disclosure.

### 4.2 · THE READING — **THE RULE FIRED. THE ACT STOPPED.**

Emit: `run_emit_SFX.sh` at `SFX_LABEL=SFXBRAW RL_O44_LVLMONO=smooth`, **exit 0, 11m27s**, matrix
`per_entrant_SFXBRAW.json` md5 `9379fcf3`, store `b745002e`, engine `3f4aa10b`. The emitter's own
fail-closed day-0 guard read **87 of 87 wired entrants at tolerance 0** — **the day-0 expectation HELD
for B RAW.** All six instrument checks PASS, and the class instrument reproduced ORDER K's published
1.0513 / 1.0324 at difference **0.0000** before it was believed.

**F4 — THE CLASS MARK: INSIDE THE LAW.** Registered W2 basis, floor 1.03, buy rail 1.14:

| | live `68be10c7` | **B RAW** | B conserved | A conserved |
|---|---|---|---|---|
| W2 class mark | 1.0738 | **1.0952** | 1.0838 | 1.0829 |
| margin to rail | −0.0662 | **−0.0448** | −0.0562 | −0.0571 |

**B RAW passes F4.** It is the closest of the four to the rail, and it passes.

**THE NO-ARB RAILS: FOUR NEW CROSSINGS, NONE REMOVED.** Every cell read beside the LIVE board's own
cell, which is how the pricing seat read it — an inherited red is not a new crossing.

| cell | live `68be10c7` | **B RAW** | B con | A con | verdict move |
|---|---|---|---|---|---|
| ND `PRIMARY` picks **1-20** | +12.98 % | **+15.18 %** | +13.93 % | +13.70 % | **fair → BUY-SIDE RED** |
| ND `PRIMARY` picks **1-10** | +13.12 % | **+15.08 %** | +13.84 % | +13.64 % | **fair → BUY-SIDE RED** |
| ND `PRIMARY` picks **11-20** | +12.71 % | **+15.38 %** | +14.11 % | +13.83 % | **fair → BUY-SIDE RED** |
| pool arm `PRIMARY` **IRE** | +11.71 % | **+14.18 %** | +12.94 % | +12.37 % | **fair → BUY-SIDE RED** |

**Breaches REMOVED by the candidate: NONE.** One sell-side cell improves — `PRIMARY EX0506`
picks 21-64, SELL-RED → fair — on the **sensitivity** basis (2005/06 cohorts removed), not the standing
one. The parked SSP breach (register v744 C6) is inherited and worsens, 63.12 % → 66.45 %; it was never
this act's to repair and is reported, not counted as a new crossing.

**THE NEW `IRE` ARM ALSO FAILS THE OWNER'S OWN PATH TEST**, which the three other new crossings are not
subject to (it applies to arm cells): `SFXBRAW PRIMARY IRE yr0→1 +14.18 % n=47 — **FAILS**, beats carry
in yr 2; still rising at yr 7`. On the live board and on **both** conserved arms, IRE does not breach at
all, so this failing cell exists only under the adopted arm.

**THE PRICING SEAT'S EXPECTATION WAS RIGHT, AND UNDERSTATED IT.** It predicted B RAW would sit *at or
above* B conserved on the picks 11-20 cell and warned the breach was "more likely, not less". Measured:
B RAW sits above B conserved on **every** cell in both tables, and where B conserved crossed **one** rail,
**B RAW crosses four**. A conserved crossed **none**.

**VERDICT: DO NOT LAND.** The measurement evidence is committed. Nothing is adopted. **The owner
re-rules with the reading in front of him** — and he now has, for the first time, the no-arb reading of
the arm he actually chose. `NOARB_BRAW_SFXBRAW.html` is that page.

---

## 5 · THE LANE — `tools/land lever`, ITS FIRST REAL LANDING

This landing runs through the P2a lever lander (`tools/land` + `tools/landing/`), delivered at
`efbe1b6` with a 10/10 byte-exact abort self-test and a no-op rehearsal that reproduced the live board.
**This is its first landing of a real act.** Ten steps, fail-closed, abort-restores-byte-exact:

`preflight` → `build_proofs` → `pins` → `lineage` → `contract` → `sibling` → `ui` → `gates` → `claims` → `commit`

The **prediction** (`prereg.board_after` = `219266fa…`) and the **owner citation** (verbatim, above) are
**INPUTS** to the command, supplied in the act spec before the build runs. A lander that learned the
expected board from the build it just ran would assert nothing at all.

**IF THE LANDER HALTS,** its abort report is captured and the carriers are restored byte-exact. The fault
is then diagnosed as **the act's** (fix the input, re-run) or **the lander's** — and a lander defect on its
first real landing is a **FINDING**, recorded as such. Falling back to the per-act scripts the lander
consolidated happens **only** if the defect is confirmed as the lander's, and is **disclosed prominently**.

---

## 6 · FALSIFIERS — what would make this act wrong, named in advance

| # | falsifier | verdict if it fires |
|---|---|---|
| **F1** | The bare build does **not** reproduce `219266fafeca5ed4fb0206a72bf37046` byte-exact | **HALT.** The adopted board is not the board the owner approved. The lander halts on this by construction. |
| **F2** | `RL_O44_LVLMONO=0` does **not** restore `68be10c79d0ee096455754e084bcf757` byte-exact | **HALT.** The kill-switch does not do what the act says it does. |
| **F3** | The switch-OFF board **equals** the switch-ON board | **HALT.** The dial is dead or silently deleted. |
| **F4** | `config_sha256`, `store`, `rl_model`, `fv`, `band`, `q97m`, `v0surf` or `register` moves | **HALT.** The act reached outside its declared lane. |
| **F5** | Any of the four named players lands away from 409 / 311 / 382 / 250 | **FINDING, reported.** The board identity would already have failed F1; a divergence here with F1 green would mean the movers file and the board disagree. |
| **F6** | The day-0 column moves on any record | **HALT.** Day-0 is OFF and re-basing is owner-explicit. |
| **F7** | `balanced_board_md5` comes back **UNMOVED** | **FINDING, reported honestly, not smoothed.** The dial is predicted to reach the sibling posture. |
| **F8** | Any landing gate reds | **HALT.** Verdicts are read off exit codes; none is taken on trust. |
