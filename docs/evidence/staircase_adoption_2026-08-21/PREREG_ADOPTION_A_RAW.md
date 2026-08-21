# PREREG — THE STAIRCASE FIX ADOPTION (ORDER 44), **VARIANT A RAW**

Written and committed **BEFORE the engine is touched** (process law P9 / law F6).

**Seat:** adoption seat, THE STAIRCASE FIX · **Date:** 2026-08-21
**Pricing:** `docs/evidence/staircase_fix_2026-08-20/` — prereg `5f94a44`, correction `901e731`, edit
`1446dec`, engine_head repair `1590a37`, pricing evidence `192fa71`, gates/claims/owner-choice `5deda20`.
**This seat's prior act:** `36f1122` — the B-raw no-arb reading, and the halt it caused.
**Register:** **v808 pending** — the register is the supervisor's pen and is **NOT touched by this seat**.

> **EVERYTHING BELOW IS A PREDICTION.** Where the tree disagrees, the tree wins, this file is corrected
> against the tree, and the error is named. Never the other way round.
>
> **NO PUSH.** Local commits only. Hand-verification stands; the supervisor verifies after this seat.

---

## 0 · THE WORD — AND IT IS A RE-RULING

The owner's adoption word, given **2026-08-21**, **verbatim**:

> **"I misunderstood the A and B difference. I think based on those explanations, A raw I prefer. Lock
> that in, unconserved."**

**THIS SUPERSEDES HIS EARLIER WORD IN THIS SAME SESSION** — *"Happy to lock in 1.22% and variant B"* — and
the supersession is the point of the record, not a footnote to it. That earlier word drove this seat's
first act, which **HALTED before the flip** (`36f1122`) when the no-arb reading of B raw was measured for
the first time and showed **four new buy-rail breaches**. The owner was shown that reading, the A/B
difference was re-explained, and **he changed his choice.** The process worked exactly as it is supposed
to: a measurement was taken before the board moved, and it changed a decision.

### 0.1 THE CONSERVATION PRINCIPLE — the owner's own reasoning, verbatim

> **"in principle I don't like 'enforcing conservation' as that's another mechanism that gets baked in...
> If we want to conserve, I'd prefer to find a lever to remove value that works on its own"**

**The conserved arms are rejected on principle, not on their numbers.** `ratchet+conserve` and
`smooth+conserve` are not adopted and this act does not ship them. **`unconserved` in the ruling word is
therefore load-bearing: the adopted dial value is `ratchet`, NOT `ratchet+conserve`.**

### 0.2 THE NO-ARB WAIVER — given in full knowledge, verbatim

> **"happy to waive the no arb reading for this"**

**THE WAIVER WAS GIVEN AFTER THE SUPERVISOR TOLD HIM EXPLICITLY** that A raw's arbitrage reading is
expected to breach similarly to B raw's. It is an informed waiver of the **band rails**, not a claim that
they will not breach and not a request to be spared the number.

**WHAT THE WAIVER DOES NOT COVER, AND THIS SEAT DOES NOT STRETCH IT:**

* It covers the **ND band rails and the pool-arm rails**. It does **NOT** cover the **class law (F4)** —
  floor 1.03, buy rail 1.14 on the registered W2 basis. **A class-law breach still HALTS this act.**
* It does **NOT** excuse this seat from **measuring and reporting**. The A-raw no-arb + class reading is
  emitted as part of this act's evidence and **every breach is recorded plainly beside the live board's
  own cell** (§5). A waiver of a *gate* is not a licence to leave a *number* unmeasured.

### 0.3 LAW 9 — THE EXCEPTION IS ON THE OWNER'S WORD, STATED NOT NETTED

RULEBOOK v3 PART 3 sets `band_scar = 200` (±0.029 % of a 692,296 board). **Variant A raw mints
+8,460 SCAR = +1.2220 %** — **42.3× the rail**. That is a **LAW 9 BREACH ON ITS FACE** and it is
**ACCEPTED BY OWNER WORD**: his standing ruling *"It's 0.6% to fix a bug, it's fine. Accept it."*, given
originally on a stale premise, was re-presented by the supervisor at the true measured **raw** mint of
1.22 % and re-confirmed. **A raw is the +1.2220 % arm — it is the arm the 1.22 % figure was actually
quoted from.** Recorded as an accepted exception wherever conservation is asserted; never netted, never
called a pass.

---

## 1 · WHAT IS BEING DONE, AND THROUGH WHICH LANE

`RL_O44_LVLMONO` moves from **default OFF** to **shipped default `ratchet`** (VARIANT A, RAW), behind a
**DECLARED KILL-SWITCH**, through the **exact lane** the D8 adoption (`register v798`) and the bake before
it (`f27482f`, `register v780`) used.

**`ratchet` IS VARIANT A AND THE MAPPING IS READ OFF THE TREE, NOT ASSUMED.** The five accepted values are
declared at `engine/rl_after/_merged_recover.py:408` (`_O44_MODES`); `MOVERS_A_RAW.json` records
`"dial": "ratchet"`. **Variant A is the RUNNING-MAX / RATCHET form** —
`A_i(lvl) = max{ v_i(g) : g a knot, g <= lvl }` — non-decreasing in level by construction over the exact
knot set of the fitted trees (`PREREG_STAIRCASE.md` §3 and PREREG CORRECTION 1, `901e731`).

**ONE ENGINE EXPRESSION CHANGES:**

```python
_O44_RAW=(os.environ.get('RL_O44_LVLMONO','0') or '0').strip().lower()
                                            ^^^  ->  'ratchet'
```

plus the comment block above it, restamped to the bake idiom its declared family already uses
(`:619 :641 :675 :723 :741 :759 :778 :796 :855 :916 :1296`). The block's technical content is **kept
intact**; only the stale half is rewritten (`DEFAULT OFF` → the BAKE stamp).

**`data/model_config.json` is NOT touched.** `conditional_prior.py` is not edited, no forest is refitted,
`cm_400.pkl` (`34faa865`) and `data/q97m.pkl` (`cfdc7321`) are read exactly as they are.

**THE RESTAMP RIDES THE FLIP COMMIT.** The engine edit moves `engine_head`, and the four carriers that
name it are restamped **in the same commit**, through the estate's established writer for exactly this
case (`docs/evidence/staircase_fix_2026-08-20/sfx_restamp.py`, byte-carried from `d8_restamp.py`). That is
the lesson of repair `1590a37`, and it is **also structurally required by the lander** — see §3.

**COMMIT ORDER (P9):** this file → the **flip** (one engine commit, restamp included) → the **landing**.

---

## 2 · THE NUMERIC PREDICTIONS

### 2.1 The two builds

| # | build | prediction |
|---|---|---|
| **P1** | **BARE** — no model-semantics `RL_*` set at all, `RL_O44_LVLMONO` **unset** | board md5 **`b3e8da99bc7f632e5d1eebc732f9cf01`**, total **700,756**, **804** rows — **byte-exact** against `MOVERS_A_RAW.json`'s `cand_board_md5` |
| **P2** | **KILL-SWITCH** — `RL_O44_LVLMONO=0` | board md5 **`68be10c79d0ee096455754e084bcf757`**, total **692,296**, **804** rows — **byte-exact** against the live board of record |

P1 is the whole meaning of "shipped default": the bare build must reproduce, byte for byte, the priced
candidate — not a rebuild of it. P2 is the whole meaning of "declared kill-switch". The lander also
refuses a switch-OFF board **equal** to the switch-ON board; that positive control is part of the
prediction.

### 2.2 The identities

| identity | before | prediction |
|---|---|---|
| `board` | `68be10c79d0ee096455754e084bcf757` | **MOVES** → `b3e8da99bc7f632e5d1eebc732f9cf01` |
| `engine_head` | `3f4aa10b23102dc4f7362b73fc20ac7b` | **MOVES AT THE FLIP COMMIT**, with its restamp riding that commit. **RECOMPUTED** from the edited source, never typed. Declared **unmoved** to the lander, which is the measured truth of the landing transaction — see §3. |
| `balanced_board_md5` | `556ad70d295923455982ae33e4b8bfd3` | **MOVES** — value unknown until built. **BUILT** by `sibling_repin.py reconcile` (build-and-compare). If it comes back UNMOVED that is a **finding**, reported, not smoothed. |
| `contract_sha256` | `8e6dcdbc89d6…` | **MOVES** (it seals the moved identities) |
| `store` | `b745002eb0a0fbb1c34fa44f1ef708d6` | **DOES NOT MOVE** — a lever landing writes no store |
| `config` / `config_sha256` | `eed19a75f775…` | **DOES NOT MOVE.** The dial is absent from `data/model_config.json`; `config_manifest.enforce()` must keep **REJECTING** `RL_O44_LVLMONO` as an unknown model override in bake/gate/canonical mode. **Asserted, not assumed.** |
| `rl_model` | `6fe7c4155866d80e8045bed2d3bf2802` | **DOES NOT MOVE** |
| `fv` | `6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346` | **DOES NOT MOVE** |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | **DOES NOT MOVE** — FROZEN, Guard-5 pinned |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | **DOES NOT MOVE** — FROZEN (R-W6) |
| `v0surf` | `5dd34ca82735f5c8f021b1c7320df8f8` | **DOES NOT MOVE** |
| `register` (LTI) | `652d83e87780e415a01a2de6d8b3cc57` | **DOES NOT MOVE** |
| `as_of_round` | `23` | **HELD at 23** |
| **day-0** | — | **OFF.** No reference regenerated or re-based. `DAY0_CP.json` untouched and un-repointed. M1b: automation never re-bases itself green. |

### 2.3 THE FOUR NAMED PLAYERS — the rows this fix exists for

From `MOVERS_A_RAW.json`:

| player | before | **predicted after** | Δ |
|---|---|---|---|
| Max Kondogiannis (`max-kondogiannis`) | 359 | **409** | +50 (+13.93 %) |
| Josh Dolan (`josh-dolan`) | 247 | **311** | +64 (+25.91 %) |
| Charlie West (`charlie-west`) | 381 | **383** | +2 (+0.52 %) |
| Will Hayes (`will-hayes-b`) | 180 | **250** | +70 (+38.89 %) |

**Charlie West is 383 under A raw**, not the 382 of B raw and not the 372 of the conserved arms — under
both conserved readings he goes **DOWN** (−2.36 %). **All four rows rise under the adopted arm.**

### 2.4 A's shape, and its honest defect, carried from the packet

A is the **running maximum**: it only ever raises, so **32 rows move down** against 114 under B raw, and
519 move up. Its stated defect is **flatness**: on the MID/pick-40 sweep 44→58 at 0.05, A shows **203 of
280 steps FLAT** (0 negative, 77 rising); at 0.002 over 46→50, **1,985 of 2,000 FLAT**. A player can score
more, raise his level, and be worth **exactly the same**. That is strictly better than the current world —
where he can score more and be worth **less** — but it answers only half of "effort must be rewarded".
**The owner has this reasoning and chose A anyway**, in the word at §0, after the A/B difference was
re-explained. **A was also the pricing seat's own standing recommendation** (`PACKET_STAIRCASE.md` §7).

---

## 3 · THE LANE — `tools/land lever`, ITS FIRST REAL LANDING

Ten steps, fail-closed, abort-restores-byte-exact:
`preflight` → `build_proofs` → `pins` → `lineage` → `contract` → `sibling` → `ui` → `gates` → `claims` → `commit`

The **prediction** (`prereg.board_after` = `b3e8da99…`) and the **owner citation** (verbatim, §0) are
**INPUTS** to the command, supplied in the act spec before the build runs.

**WHY `engine_head` IS DECLARED UNMOVED TO THE LANDER — this seat's own finding, carried forward.** P9
forces the engine edit into its own commit ahead of the landing, and the lander's `preflight` requires a
clean tree, so by the time `steps._measure_sides` reads its source side via
`git show <base>:engine/rl_after/_merged_recover.py`, the flip is already `HEAD`. Two consequences, both
established by reading the lander's code:

1. the flip commit **must** carry the `engine_head` restamp itself, or the landing **halts at `lineage`**
   with *"base-commit engine_head disagrees with that tree's expected_boot"*;
2. the landing must therefore declare `engine_head` **unmoved** — the **measured truth of the
   transaction**, not a claim that the adoption left it alone. The lineage entry's invariants say so in
   words, because `moved_by_transition` alone would understate the act.

**IF THE LANDER HALTS**, its abort report is captured and the carriers restore byte-exact. The fault is
diagnosed as **the act's** (fix the input, re-run) or **the lander's** — and a lander defect on its first
real landing is a **FINDING**, recorded as such, with any fallback to the consolidated per-act scripts
disclosed prominently and used only if the defect is confirmed as the lander's.

---

## 4 · FALSIFIERS — what would make this act wrong, named in advance

| # | falsifier | verdict if it fires |
|---|---|---|
| **F1** | The bare build does **not** reproduce `b3e8da99bc7f632e5d1eebc732f9cf01` byte-exact | **HALT** |
| **F2** | `RL_O44_LVLMONO=0` does **not** restore `68be10c79d0ee096455754e084bcf757` byte-exact | **HALT** |
| **F3** | The switch-OFF board **equals** the switch-ON board | **HALT** — the dial is dead or silently deleted |
| **F4** | **The class mark leaves 1.03–1.14** on the registered W2 basis | **HALT. THE WAIVER DOES NOT COVER THE CLASS LAW.** |
| **F5** | The day-0 column moves on any record | **HALT** |
| **F6** | `config_sha256`, `store`, `rl_model`, `fv`, `band`, `q97m`, `v0surf` or `register` moves | **HALT** — the act reached outside its lane |
| **F7** | Any of the four named players lands away from 409 / 311 / 383 / 250 | **FINDING, reported** |
| **F8** | `balanced_board_md5` comes back **UNMOVED** | **FINDING, reported honestly** |
| **F9** | Any landing gate reds | **HALT** |
| **F10** | **ND band or pool-arm rails breach** | **RECORDED, NOT HALTING — WAIVED BY THE OWNER** (§0.2), measured and printed beside the live board's own cells in §5 |

---

## 5 · THE A-RAW NO-ARB AND CLASS READING — **MEASURED BEFORE THE FLIP**

Emitted as part of this act, on the same machinery, **before the engine was touched**. The rails are
**waived**; the numbers are **not**. `NOARB_ARAW_SFXARAW.html` renders all five arms side by side.

Emit: `run_emit_SFX.sh` at `SFX_LABEL=SFXARAW RL_O44_LVLMONO=ratchet`, under the build lock, **exit 0,
5m22s**, matrix `per_entrant_SFXARAW.json` md5 `a756078e`, store `b745002e`, engine `3f4aa10b`. All
instrument checks **PASS**; the class instrument reproduced ORDER K's published 1.0513 / 1.0324 at
difference **0.0000** before its own numbers were believed.

### 5.1 · **F4 — THE CLASS LAW: PASS.** The one gate the waiver did not cover.

| | live `68be10c7` | **A RAW** | B raw | A con | B con |
|---|---|---|---|---|---|
| W2 class mark | 1.0738 | **1.0943** | 1.0952 | 1.0829 | 1.0838 |
| margin to rail 1.14 | −0.0662 | **−0.0457** | −0.0448 | −0.0571 | −0.0562 |

**INSIDE THE LAW.** Floor 1.03, buy rail 1.14, registered W2 basis. **F4 did not fire, so this act
proceeds.** Had it fired, the waiver would not have saved it.

### 5.2 · **F5 — DAY-0: HELD.** The emitter's own fail-closed ORDER 31-F guard read **87 of 87** wired
entrants on board `68be10c7` reproducing printed day-0 **EXACTLY at tolerance 0**, on the printed integer
and the unrounded `derived_v0`, under `RL_O44_LVLMONO=ratchet`. No reference re-based.

### 5.3 · THE BAND RAILS — **WAIVED BY OWNER WORD, AND MEASURED ANYWAY**

Every cell read **beside the live board's own cell**: a cell already breaching on `68be10c7` and still
breaching is an **inherited** red, not a new crossing.

**THREE NEW ND CROSSINGS, on the standing PRIMARY basis:**

| cell | live | **A RAW** | B raw | A con | B con | move |
|---|---|---|---|---|---|---|
| picks **1-20** | +12.98 % | **+14.94 %** | +15.18 % | +13.70 % | +13.93 % | **fair → BUY-SIDE RED** |
| picks **1-10** | +13.12 % | **+14.87 %** | +15.08 % | +13.64 % | +13.84 % | **fair → BUY-SIDE RED** |
| picks **11-20** | +12.71 % | **+15.08 %** | +15.38 % | +13.83 % | +14.11 % | **fair → BUY-SIDE RED** |

**POOL ARMS: ZERO NEW CROSSINGS.** This is where A raw separates from B raw. The `PRIMARY IRE` arm —
which **crossed** under B raw at +14.18 % and **failed the owner's own path test** there (beats carry in
yr 2, still rising at yr 7) — reads **+13.63 % under A raw and does not breach at all.** A raw's only
path-test failures are `PRIMARY SSP` and `MODERN SSP` at +66.08 %, and those are the **inherited parked
breach** (register v744 C6, already failing on the live board at +63.12 %), not new.

**Breaches REMOVED: NONE.** One sell-side cell improves — `PRIMARY EX0506` picks 21-64, SELL-RED → fair —
on the **sensitivity** basis (2005/06 cohorts removed), not the standing one.

### 5.4 · **A RAW IS STRICTLY THE MILDER ARM ON THE RAILS, AND THE RE-RULING IMPROVED THE OUTCOME**

| | new ND crossings | new pool-arm crossings | **total new breaches** | new path-test failures |
|---|---|---|---|---|
| **A RAW — adopted** | 3 | **0** | **3** | **0** |
| B raw — halted at `36f1122` | 3 | 1 (`IRE`) | **4** | 1 (`IRE`) |
| A conserved | 0 | 0 | 0 | 0 |
| B conserved | 1 | 0 | 1 | 0 |

**A raw reads lower than B raw on every single cell in both tables**, without exception. The owner's
re-ruling therefore did not merely swap one breaching arm for another: it **removed a breach and a
path-test failure** relative to the arm he first named. The three ND crossings that remain are the ones he
waived, knowingly and after being told they were expected.

**THIS SEAT DOES NOT DRESS THAT UP AS A PASS.** Three cells at the top of the draft — picks 1-10, 11-20
and their union — move from fair to buy-side red on the standing basis, and nothing is repaired on the
buy side. The owner waived the reading; he did not receive a clean one, and the record says so.
