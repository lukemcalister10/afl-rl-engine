# SHIPPING PACKET — ORDER 29, THE LANDING BUILD

**2026-08-13 · branch `land/order-29` · build seat**

> # THE LANDING DID NOT COMPLETE.
> It **stopped at Step 3**, on a measured engine halt: the curve the owner ruled cannot be loaded by
> the engine, because **Ruling C and G-MONO are in direct collision**. Steps 0–2 landed and are proven.
> Steps 3–7 did not run. The board is still `88ce647f`, no pin has been re-stamped, and the candidate
> curve is **not installed**.
>
> **One decision is owed before this can finish, and it is the owner's: `STOP_STEP3_GMONO.md` §5.**

---

## 1. THE ONE THING TO READ FIRST

The ORDER-28 candidate curve is **monotone** because Ruling C ruled it monotone, and it is monotone
**by weighted PAVA**, which removes an ascent by replacing a violating block with its weighted mean.
A pooled block is therefore a **plateau**, by construction. The curve carries 12 of them:
picks 6–11 all read **1319**, picks 15–20 all read **812**.

The engine requires the shipped national curve to be **strictly** decreasing — no plateaus — and
enforces it at four independent sites. So the build halted:

```
rl_model.py:1449  _PVC2M=_split_ladder(_V2RAW,'RL_PVC2 v2 curve')
AssertionError: RL_PVC2 v2 curve G-MONO: national curve 1..64 is not STRICTLY decreasing
              — 12 plateau(s) at picks [6, 7, 8, 9, 10, 11, 15, 16]
```

**PREREG P5 predicted those plateaus by name** — it lists pick 7 = 1319 *and* pick 10 = 1319, pick 15
= 812 *and* pick 20 = 812. All twelve of its spot values matched exactly. The prediction was right and
the artifact is still unloadable. That is the finding.

Both sides are owner law. Ruling C is 2026-08-12. G-MONO is RULEBOOK v2.1 law 4, and the register's
v444 hold on it is **explicitly scoped away from this build**: *"the CURRENT frozen curve (blended
world) still satisfies G-MONO as written and remains gated by it until the restructured pricing
exists — the hold governs the new world, not the old ruler."* The restructured pricing does not exist.
The register separately records *"NOT ADOPTED: … plateau permissiveness (strict descent is owner
law)."*

A build seat cannot choose between two owner rulings. Nothing was improvised: no assert was relaxed,
no ruled number was nudged, and the breaking artifact was never installed in the checkout. The three
possible resolutions, with the cost of each, are set out in `STOP_STEP3_GMONO.md` §5.

---

## 2. THE PREREGISTRATION, SCORED — ALL TWENTY, BY NUMBER

`PREREG.md` was committed and pushed **before** this seat measured anything (`a19525d`, and this seat
started from it). Git history is the proof, not this paragraph.

| # | prediction | outcome |
|---|---|---|
| **P1** | byte-identity at entry, dial OFF, reproduces `88ce647f` | **HELD** — exact, on the untouched tree |
| **P2** | the unflag-three, structural (4 clauses) | **HELD** — all four |
| **P3** | the three indirect movers, both channels, head Δ < 3% | **HELD** — every clause, +1.2510% |
| **P4** | grace-A ON as code default; `RL_GRACE=0` still byte-reproduces dial-off | **HELD** — byte-identical |
| **P5** | the monotone hybrid curve, **wired** | **PARTIAL — the numbers HELD, the wiring did not.** All 12 spot values, seam 56, tail 57–64, pick 64 = 179, non-increasing: all confirmed. **The curve was NOT wired** — it halts the engine. And P5's own re-check clause fired: the artifact's `r104_9_strict_descent` self-declaration would have been **false** under this curve |
| **P6** | the conservation ledger | **HELD** — weighted `0.000e+00`, plain `+0.0000%`, int drift `−0.0029%` printed not absorbed |
| **P7** | positional ND v0s at every pick, reconciliation < 1e−12 | **NOT REACHED** — blocked by the Step 3 stop |
| **P8** | pool v0s, Way A, K-shrunk, the predicted pathway levels | **NOT REACHED** |
| **P9** | the two n=0 cells stay unsigned + the loud boot assert | **NOT REACHED** |
| **P10** | the numéraire re-pin, `s → 0.9400914291048137` | **NOT REACHED.** But its input is now confirmed: the candidate's own pre-anchor head is `3191.1789716631` and `3000/3191.1789716631 = 0.9400914291048137` exactly, so P10's arithmetic stands ready. Its declared brief-discrepancy is also **settled in P10's favour** — see §5 |
| **P11** | E6 coherence, both sides together, ×0.945715 | **NOT REACHED** |
| **P12** | the printed-day-0 assert | **NOT REACHED** |
| **P13** | the final board's mover classes; 800–804 movers; total 705,000–725,000; sign DOWN | **NOT REACHED as written** (no final board). On the two levers that did land: **543 movers of 804**, total **752,429 → 748,405**, **sign DOWN**. The two dominant predicted classes — the numéraire scalar and the curve re-print — never ran, and they are the ones that reach *every* row |
| **P14** | the ten named rows, per-lever; duursma the only riser | **PARTIAL — and its substantive claim HELD on what landed.** All ten reported in the ledger. `willem-duursma` is **the only named row that rises** (+488, +12.27%); every other named row falls or is flat |
| **P15** | no-arb, both instruments, on the FINAL board | **NOT REACHED** — there is no final board to read them on |
| **P16** | the identity gate on the landed board | **NOT REACHED** |
| **P17** | determinism across two full builds | **HELD, on the last buildable configuration.** Two independent builds from fresh scratch workspaces both produced `0017657e0469addda9260964938bad78`. Not the *final* configuration P17 names, because there is none |
| **P18** | the moved-set of pins | **BREACHED — and the breach predates this build.** See §4 |
| **P19** | boot guard PASSES; book re-sealed as an isolated commit | **NOT MET, deliberately.** Guard 5 **FAILS** on the branch, and re-stamping the pins to make it pass would bake a half-landing. See §4 |
| **P20** | nothing merges; the PR is opened and HELD | **HELD** |

**Six held outright · one held on the landed configuration · three partial · nine not reached · one
breached.** Nothing here is scored favourably by reading a prediction loosely; where a prediction
cannot be scored as written, it says so.

---

## 3. WHAT LANDED, WITH ITS NUMBERS

### 3.1 Step 0 — the control at entry (P1)

The first seat edited the store **before** running this control and died; that edit went with its
worktree. This seat started from a clean tree and ran the control **first**, because a control that
shares the change it is controlling for is not a control.

| artifact | md5 at entry | expected |
|---|---|---|
| store | `d9a24282357cf3083b1640466e3ecd83` | matches prereg §0 |
| board | `88ce647f531030d8d2e094188b258191` | matches prereg §0 |
| `rl_model.py` | `5d1e7b7a8172c58cb2c8c49a0aaad77a` | ORDER 28 post |
| `_merged_recover.py` | `e51098648c1ccb6951b30d57d9aac3fe` | ORDER 28 post |

`git status` empty. Full staged rebuild, dial OFF → **`88ce647f531030d8d2e094188b258191`**, exact.
**1m57s** wall under full five-var thread pinning — against ORDER 28's *1h53m without finishing*
unpinned. Every divergence measured after this point is caused by a change this build made.

### 3.2 Step 1 — the unflag-three (P2, P3)

Store **`d9a24282357cf3083b1640466e3ecd83` → `cb38ef1171dcf20aae66ebf12682be0d`**, −66 bytes = 3 × the
needle `"_pvc_exclude": true, ` exactly. Byte surgery on the single-line store, then re-parsed and
compared row by row against the live store:

| P2 clause | result |
|---|---|
| store carries zero `_pvc_exclude` rows | **3 → 0, PASS** |
| ND-2011 is 81 rows, zero duplicate picks | **81 rows, picks 1..81 contiguous, PASS** |
| all three curve-contributing at picks 4 / 12 / 14 | **PASS** |
| the diff is exactly three deleted keys | **3 deleted, 0 added, 0 values changed, key order preserved — PASS** |

**P3 — both predicted channels fired**, enumerated in `P3_INDIRECT_out.txt`:

| quantity | pre | post | move |
|---|---|---|---|
| v3.4 pre-anchor head `PVC[1]` | 3917 | 3966 | **+49 (+1.2510%)** — P3's <3% bound **HELD** |
| `BOARD_FACTOR = (_P1/PVC[1])·s` | 0.761343692730 | 0.751937277969 | **−1.2355%**, reaching every priced row |
| kernel picks 1–64 that moved | — | — | **61 of 64** (max +53 at pick 19) |
| ND-2011 rows whose attribution slid | — | — | **75**, max **+3** picks (P3 said "up to 3") |

The three re-enter the fit at picks **1–8 / 8–16 / 10–18**; previously at none. The head rises because
pick 1's ±4 window reaches pick 4, where `dylan-shiel` sits — and a higher head *divides into*
`BOARD_FACTOR`, so the player side falls.

**A hazard the probe found and closed.** `rl_model.py:1371` reassigns `SCALE`, so calling
`build_pvc_v34()` after import returns the curve already multiplied by `BOARD_FACTOR` — measured head
**2983** against the true **3917**. The probe restores `SCALE` and then checks its result against the
engine's own identity `H = _P1·s/BOARD_FACTOR`, halting rather than publishing a contaminated curve.
A first version of this packet would have carried the wrong head.

### 3.3 Step 2 — the grace dial on as code default (P4)

`rl_model.py` `5d1e7b7a` → **`cb78e0efe129fdcd9c02be5364db4aab`**: one operative character, the dial's
default `'0'` → `'1'`. The grace-A law is untouched — `grace_years`, `GRACE_G = 1`,
`GRACE_MAX_ENTRY_AGE = 19`, `disc_factor`'s branch and all seven call sites are verbatim ORDER 28.

`data/model_config.json`: `RL_GRACE: "1"` added to `vars`, `config_sha256` `bf012105…` →
**`eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1`**. Not optional — ORDER 28 §9.8
named it in advance: `config_manifest.enforce()` rejects unknown `RL_*` overrides in bake/gate mode,
so a canonical build would have refused the dial.

The naive control was unavailable (the store had already moved), so the dial-off reference was
**built**:

| build | `rl_model.py` | default | env | board md5 |
|---|---|---|---|---|
| **B_U** | `5d1e7b7a` | OFF | unset | **`71cbb13b3414d031135771dd7e564b3c`** |
| **B_G0** | `cb78e0ef` | ON | `RL_GRACE=0` | **`71cbb13b3414d031135771dd7e564b3c`** |
| **B_G** | `cb78e0ef` | ON | unset | `0017657e0469addda9260964938bad78` |

**B_U == B_G0 byte for byte — P4 HELD**, and B_G differing is what makes it non-vacuous.

Recorded because it shaped the method: an attempt to run this control by staging a *foreign*
`rl_model.py` was **refused by the engine's own active-provenance guard**. The guard is working; the
control was redone the honest way, by reverting the checkout and restoring it.

### 3.4 The board, live → landed-so-far

| stage | board | total | Δ vs LIVE |
|---|---|---|---|
| **LIVE** | `88ce647f531030d8d2e094188b258191` | 752,429 | — |
| **B_U** — + unflag-three | `71cbb13b3414d031135771dd7e564b3c` | 743,734 | −8,695 (−1.1556%) |
| **B_G** — + grace dial | `0017657e0469addda9260964938bad78` | 748,405 | **−4,024 (−0.5348%)** |

| population | n | LIVE | B_G | Δ |
|---|---|---|---|---|
| national (ND 1–64) | 561 | 620,877 | 618,074 | −2,803 (−0.4515%) |
| pool (past 64) | 243 | 131,552 | 130,331 | −1,221 (−0.9282%) |

**543 of 804 rows move.** The levers reconcile **exactly**: 0 rows fail, max |residual| **0**.

**The control group holds:** the 30 rows debuting 2026 at entry age ≥ 20 move by **exactly zero**
under the grace dial's own leg — the ruled discrimination visible in the data rather than asserted.

### 3.5 The named rows (P14)

| row | pos | pick | grace | LIVE | lever 1 unflag | lever 2 grace | landed-so-far | Δ |
|---|---|---|---|---|---|---|---|---|
| harrison-ramm | KPD | 3 | 0 | 545 | −4 | 0 | 541 | −4 (−0.73%) |
| luker-kentfield | KPF | 11 | 0 | 419 | −2 | 0 | 417 | −2 (−0.48%) |
| mani-liddy | MID | 15 | 0 | 152 | 0 | 0 | 152 | 0 |
| robert-hansen | SF | 2 | 0 | 132 | 0 | 0 | 132 | 0 |
| dante-visentini | RUCK | 56 | 0 | 1274 | −16 | 0 | 1258 | −16 (−1.26%) |
| vigo-visentini | RUCK | 5 | 0 | 182 | 0 | 0 | 182 | 0 |
| nicholas-martin | MID | pool | 0 | 3513 | −44 | 0 | 3469 | −44 (−1.25%) |
| marcus-herbert | SD | 13 | 0 | 906 | −12 | 0 | 894 | −12 (−1.32%) |
| jai-newcombe | MID | 2 | 0 | 4883 | −61 | 0 | 4822 | −61 (−1.25%) |
| **willem-duursma** | MID | 1 | **1** | 3977 | −50 | **+538** | **4465** | **+488 (+12.27%)** |
| harry-sheezel | MID | 3 | 0 | 11764 | −146 | 0 | 11618 | −146 (−1.24%) |

**P14's substantive claim held on what landed**: duursma is the only named row that rises, and he
rises because grace reaches him and outweighs the other lever — exactly the mechanism P14 named.

---

## 4. THE PINS — P18 BREACHED, AND P19 DELIBERATELY NOT MET

**P18 is breached, and the breach predates this build.** `data/expected_boot.json` was **already
stale at entry**, before this seat changed anything:

| pin | pinned | actual at entry | moved by |
|---|---|---|---|
| `rl_model` | `e5eb5e44…` | `5d1e7b7a…` | **ORDER 28** (P18 lists it — fine) |
| `engine_head` | `3f1468e5…` | `e5109864…` | **ORDER 28** (P18 lists it — fine) |
| **`fv`** | `2621b56a…` | `6e9a370e…` | **ORDER 28**, which edited `distribution_pricing.py::v_at_peak` |

P18 names `fv` among the identities whose movement is a **STOP-AND-REPORT**. It moved — but not
because of ORDER 29. ORDER 28 moved it and, having landed nothing, correctly left the pin alone. This
build does not touch `engine/forward_valuation` at all, and the Step-0 control passed *with* that
source in place, which proves it is inert dial-off. So P18's letter is breached; its purpose — catch
an **unexplained** cross-environment mover — is not.

**No pin has been re-stamped, and that is a decision, not an omission.** The landing did not produce
a final board, and re-stamping `store` / `board` / `config` / `rl_model` / `fv` to a half-landed state
would pin a board that is not the landed board — the precise failure the ORDER 28 packet's
finding-11 lesson warns against.

**So Guard 5 FAILS on this branch, on five counts, all expected:**

```
  checkout store  cb38ef11 != pinned d9a24282
  model config    eed19a75 != pinned bf012105
  checkout rl_model cb78e0ef != pinned e5eb5e44
  fv CHECKOUT DRIFT     6e9a370e != pinned 2621b56a
  fv LOADED-PATH DRIFT  6e9a370e != pinned 2621b56a
```

**P19 is therefore not met, deliberately.** The guard is telling the truth: this tree is mid-landing.
It goes green in the same commit that lands the final board, and not before. The book was **not**
re-sealed, for the same reason.

---

## 5. THE NUMÉRAIRE — P10's DECLARED DISCREPANCY, SETTLED

P10 declared, before measuring, that the brief's *"today s = 3000/2850.6 = 1.0524"* did not match the
artifact, and predicted the artifact would prove to be the authority. **It is**, and the evidence
arrived from an unexpected direction: the engine's own export log prints

```
L7 NUMÉRAIRE RE-BASE ÷1.0524: order preserved (no strict inversion; 11 rounding ties)
```

So **1.0524 is real, and it is a different object** — the L7 display-side re-base divisor, a
presentation step (ORDER 28's identity gate reads the same number as its *attribution* numéraire leg).
The artifact's `numeraire` block is the one `_load_numeraire` reads and the one `BOARD_FACTOR`
multiplies by, and it reads `pooled_head_pre_scale 3017.9232`, `s 0.9940610814748366`,
`published_pin 3000.0` — E6-coherent as committed, and confirmed live in both probes.

**P10's arithmetic stands ready and unexecuted.** The candidate's own pre-anchor head is
`3191.1789716631`, and `3000 / 3191.1789716631 = 0.9400914291048137` — the ×0.94 class the register
ruled. The re-pin was **not performed**, because `s` re-pins to the head of a curve that cannot be
installed; publishing a new `s` against an uninstallable ladder is exactly the one-sided scaling
`_load_numeraire` exists to prevent.

---

## 6. THE CONTROLS — WHAT RAN, WHAT COULD NOT

| control | status |
|---|---|
| byte-identity at entry, dial OFF | **PASS** — `88ce647f`, exact |
| the dial-off reference vs `RL_GRACE=0` | **PASS** — byte-identical, `71cbb13b` |
| the dial is reachable | **PASS** — `0017657e` differs |
| **deterministic double-build** | **PASS** — two independent fresh-workspace builds, both `0017657e0469addda9260964938bad78` |
| the grace control group (entry age ≥ 20) | **PASS** — 30 rows, 0 moved by the dial |
| lever reconciliation, every row | **PASS** — 0 failures, max residual 0 |
| the engine's active-provenance guard | **FIRED IN ANGER** — refused a foreign `rl_model.py` |
| Guard 5 boot guard | **FAILS** — expected mid-landing; see §4 |
| identity gate on the final board | **NOT RUN** — no final board |
| both no-arb instruments, mark-path, reverse no-arb | **NOT RUN** — specified on the final board |
| book re-seal | **NOT DONE** — would seal a half-landing |

The instruments and the identity gate are not skipped for convenience. They are specified *on the
FINAL board*, and running them on an intermediate board would produce numbers that read like results
and are not.

---

## 7. WHAT IS OWED, AND BY WHOM

**The owner owes one ruling** — `STOP_STEP3_GMONO.md` §5, the Ruling-C / G-MONO collision:

* **(A)** relax the ship-side enforcement to non-increasing — keeps every ruled number, amends
  RULEBOOK law 4 for the current world (which the v444 hold pointedly did **not** do);
* **(B)** de-plateau the pooled blocks — cheapest in code, but re-introduces the exact ordering PAVA
  was ruled in to remove, and breaks P5 and the P6 plain-sum;
* **(C)** the −1 ordering tiebreak — smallest numeric distortion and a named house convention, but
  still edits ruled output and still breaches P5's published spot values.

*This seat's recommendation, and nothing more:* **(A)** is the only one that does not edit a ruled
number. But it amends a law, and that is his word.

**On his word, the build resumes at Step 3** and runs to the end: the curve wired, the positional ND
v0s (P7), the pool v0s with the two cells unsigned and the loud boot assert (P8/P9), the numéraire
re-pin through `_load_numeraire` (P10/P11), the printed-day-0 assert (P12), then the full control
suite on the final board — identity gate, both instruments, mark-path, reverse no-arb, the
deterministic double-build, Guard 5, the book re-seal, and the pin re-stamp with the moved-set
asserted. Steps 0–2 do not need redoing; they are committed, pushed and proven.

---

## 8. STATE

| | |
|---|---|
| branch | `land/order-29` |
| store | `cb38ef1171dcf20aae66ebf12682be0d` — **moved** |
| board | `88ce647f531030d8d2e094188b258191` — **unmoved** |
| `pvc_curve_v2.json` | `f6f3027fc56615fc77cd455638a5fa79` — **unmoved**; the candidate is not installed |
| `rl_model.py` | `cb78e0efe129fdcd9c02be5364db4aab` |
| `config_sha256` | `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` |
| last buildable board | `0017657e0469addda9260964938bad78` (dial ON) — a **variant**, not landed |
| PR | opened from `land/order-29` to `main`, **HELD** |

**NOTHING MERGES WITHOUT THE OWNER'S WORD.**

---

### Evidence index

| file | what |
|---|---|
| `PREREG.md` | the twenty predictions, filed before any measurement |
| `CONTROL_ENTRY.md` | Step 0 — the byte-identity control on the untouched tree |
| `o29_unflag.py` · `UNFLAG29_out.txt` · `UNFLAG29.json` | Step 1 — the unflag-three and its P2 asserts |
| `o29_probe34.py` · `o29_p3.py` · `P3_INDIRECT_out.txt` · `P3_INDIRECT.json` | Step 1b — the P3 indirect movers, enumerated |
| `GRACE_DEFAULT.md` | Step 2 — the default flip and its three-build control |
| `o29_curve.py` · `CURVE29_out.txt` · `pvc_curve_v2_CANDIDATE.json` | Step 3 — the candidate curve, P5/P6 scored |
| **`STOP_STEP3_GMONO.md`** · `GMONO_HALT_transcript.txt` | **the stop, the halt transcript, and the three resolutions** |
| `o29_movers.py` · `docs/ledgers/LANDING_29_MOVERS_2026-08-13.{md,json}` | the composed movers ledger, every player |
| `bb.sh` | the staged-workspace board builder |
