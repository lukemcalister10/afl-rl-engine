# SHIPPING PACKET — ORDER 26B, THE DELIVERED-VALUE REDERIVATION

**NOTHING HERE IS LANDED.** No engine file was changed, no pin was moved, no board was rebuilt. The
landing act — the one that wires a derived entry value in as the printed day-0 object and adds the
permanent assert `printed day-0 == derived entry value` — is a **later order on the owner's word**, and
§6 of this packet says something important about whether that assert can be written at all as the engine
stands today.

Branch `build/delivered-value` from `origin/main` @ `3b4df6f`. Authority: #334 comment 5269952564
(thirteen owner rulings) and the owner's "Go" filed the same hour.

---

## 1. THE ANSWER IN FIVE SENTENCES

The order was to build a delivered-value scorer, gate it against the live board, and then rederive the
pick curve and the pool entry prices from it. **The scorer was built and it is exact** — it reproduces
the engine's own production price for all 800 measurable board players **bit-for-bit**. **The gate then
failed**, because the thing Ruling 9 told me to compare against — a player's live board price — is not
the object the scorer reproduces: the board price carries four further engine legs on top of the
production price, and those legs move players by anywhere from ×0.09 to ×4.2. Ruling 9 says a gate
failure is a STOP, and I have stopped: **the pick curve, the positional relativities, the pool
pathway values, the comparisons and the two instruments were not built.** What *is* delivered is the
prereg, the gate with a complete zero-residual attribution of the gap, and **Layer 1 — the durable
harvest — as a pinned first-class dataset**, which needed no scorer and will outlive this order.

---

## 2. WHAT WAS DELIVERED, AND WHAT WAS NOT

| step | brief | status |
|---|---|---|
| 0 | PREREG | **DONE** — `PREREG_ORDER26B.md`, committed before any measurement of this order's quantities |
| 1 | THE IDENTITY GATE | **DONE — AND IT FAILED** — `GATE_REPORT.md`, `o26b_gate.py`, `GATE.json`, `GATE_out.txt` |
| 2 | LAYER 1, THE HARVEST | **DONE** — `data/delivered_value/layer1_player_seasons.json` (md5 `ad1229ea…`) + builder + README |
| 3 | LAYER 2, THE SCORER | **NOT RUN** — Ruling 9: no derivation on an ungated scorer |
| 4 | THE DERIVATIONS (curve, relativities, pool ladder, MSD both ways) | **NOT RUN** |
| 5 | THE COMPARISONS + THE TWO INSTRUMENTS | **NOT RUN** |
| 6 | THE PACKET | **DONE** — this file |

The stop was **pre-committed**. `PREREG_ORDER26B.md` §1 P1.5 wrote the decision rule — including the
carve-out for Layer 1 and the exclusion of steps 3–6 — **before the gate was run**, precisely so that a
disappointing gate could not be re-read into a pass afterwards.

---

## 3. THE PRICE FUNCTION — IDENTIFIED, PINNED, AND EXACT

Ruling 3 asked for "today's engine's price for an established season of average X at position P — the
exact live callable identified and pinned by the build". It is one line:

```
season_points(X, P) = SCALE · posval( X + capt_prem(X) − (MA.REPL[P] − rd.REPL_DROP[P]) ) · 21
```

| component | file (md5) | line |
|---|---|---|
| `posval` | `engine/rl_after/rl_model.py` (`e5eb5e4405c09eebef45a9db89f014bc`) | 785 |
| `capt_prem` | `engine/rl_after/rl_model.py` | 676 |
| `SCALE` = 1.4398232006949683 | `engine/rl_after/rl_model.py` | 1120, reassigned 1324 |
| `MA.REPL` | `engine/rl_after/rl_model.py` | 779 |
| `REPL_DROP` (uniform 3.0) | `engine/forward_valuation/dist_redesign.py` (`48ea1bfeccc6d1ea51add66b0cb93965`) | 39 |
| `disc_factor`, `LENS['bal']=0.14`, `RL_AGE_DISC` OFF | `engine/rl_after/rl_model.py` | 906, 917 |
| the `× 21` season constant | `engine/rl_after/rl_model.py` | 978–979 |

**It is the k-th season term of `proj_from_peak`.** It is reused as a live attribute lookup — never
reimplemented, never hand-copied.

**Ruling 1 verified, not assumed.** Taking the bars off the engine's own netting path
(`MA.REPL − REPL_DROP`) gives **{MID 77.1, SD 75.3, RUCK 75.5, KPD 65.4, SF 67.9, KPF 63.8}** —
character-for-character the set Ruling 1 states.

**One fact that makes the whole two-layer design work:** the live `GAMMA = 1.0`, so `val(r) = SCALE·r` is
**linear**, and delivered value is therefore **additive across seasons in board points**. Layer 2 can be
a straight discounted sum. Had `GAMMA` been 0.85 it could not have been.

---

## 4. THE GATE — 2 OF 12 ON THE PANEL, 9 % BOARD-WIDE

Full detail in `GATE_REPORT.md`. Headline, on the panel fixed in the prereg:

| key | pos | age | scored blend | price6 | vs price6 | board v | vs board | verdict |
|---|---|---|---|---|---|---|---|---|
| **willem-duursma** | MID | 19 | 4050.00 | 4050.00 | +0.0000 % | 3977 | **+1.84 %** | **PASS** |
| nick-daicos | MID | 23 | 10554.84 | 10554.84 | +0.0000 % | 10945 | −3.56 % | FAIL |
| harry-sheezel | MID | 22 | 11433.30 | 11433.30 | +0.0000 % | 11764 | −2.81 % | FAIL |
| marcus-bontempelli | MID | 31 | 3234.04 | 3234.04 | +0.0000 % | 3876 | −16.56 % | FAIL |
| max-gawn | RUCK | 35 | 2763.00 | 2763.00 | +0.0000 % | 3336 | −17.18 % | FAIL |
| harley-reid | MID | 21 | 4269.30 | 4269.30 | +0.0000 % | 3820 | +11.76 % | FAIL |
| **jai-newcombe** | MID | 25 | 4913.14 | 4913.14 | +0.0000 % | 4883 | **+0.62 %** | **PASS** |
| harrison-ramm | KPD | 20 | 794.84 | 794.84 | +0.0000 % | 545 | +45.84 % | FAIL |
| vigo-visentini | RUCK | 21 | 791.84 | 791.84 | +0.0000 % | 182 | **+335.08 %** | FAIL |
| josh-treacy | KPF | 24 | 7157.74 | 7157.74 | +0.0000 % | 6921 | +3.42 % | FAIL |
| izak-rankine | SF | 26 | 4511.46 | 4511.46 | +0.0000 % | 4685 | −3.70 % | FAIL |
| lachlan-ash | SD | 25 | 6088.96 | 6088.96 | +0.0000 % | 5728 | +6.30 % | FAIL |

**The owner's named row passes.** Board-wide: **72 of 804 (9.0 %)** inside ±2 %; median **1.0044**;
p05 **0.0904**; p95 **4.2048**.

**Read the two columns separately, because they say opposite things.**
- The **`vs price6`** column is the price function against the engine's own production-value object:
  **+0.0000 % on every row, and 800/800 bit-exact board-wide.** The scorer is right.
- The **`vs board`** column is Ruling 9's gate. It fails, and it fails by *dispersion*, not by level —
  the median is 1.0044, i.e. the scorer is not systematically high or low; it is simply measuring a
  different object from the one the board prints.

### The gap, fully attributed — five legs, residual 8.9e−16

| leg | what it is | where |
|---|---|---|
| the price function | measured at **exactly 1.0000** on every row | — contributes nothing |
| `_uncomp_prod` | the LEG-B un-compress map at the production hook (`RL_UNCOMP=1`, `s=0.10`) | `_merged_recover.py` |
| the pedigree pole | `pr + w·recover(perf,par)·max(0, po − pr)` | `_merged_recover.py:458–475` |
| `ev / raw_ev` | isotonic pick guard, RUCK ceiling, W4 KPF compression, sit-out treatment, `_h_cut`s, entry-anchor floor | `_merged_recover.py`, `ev()` |
| the numéraire | a flat ≈ 1.0524 on every row | L7 divisor |

The product of those legs reproduces the measured `scored/board_v` ratio to floating point on every panel
row — **maximum residual 8.9e−16**. There is no unnamed leg, and the harness asserts it.

Where each bites, in plain words: **`ev/raw_ev` is the violent one for thin records** (visentini 0.2146,
ramm 0.5806 — the sit-out and entry-anchor machinery holding them far below what their own band careers
price); **`_uncomp_prod` × the pole is the veteran leg** (bontempelli and gawn each take ≈ ×1.27 of uplift
the career score does not carry, which is the whole of their −17 %).

---

## 5. LAYER 1 — THE DURABLE HARVEST (Ruling 11)

`data/delivered_value/layer1_player_seasons.json` · md5 **`ad1229ea6f443538479447132382b21c`** ·
2,842,543 bytes · **2,650 entries** · **11,484 player-seasons** · seasons 2005–2026 · builder and README
committed beside it. **Deterministic** — no build timestamp; a rebuild reproduces the bytes and the md5,
verified twice.

| mechanism | entries | seasons | seasons/entry |
|---|---|---|---|
| ND 1-64 | 1448 | 8191 | 5.66 |
| RD | 691 | 2071 | 3.00 |
| ND>64 | 122 | 445 | 3.65 |
| MSD | 106 | 199 | 1.88 |
| UNR | 59 | 125 | 2.12 |
| IRE | 57 | 131 | 2.30 |
| SSP | 52 | 125 | 2.40 |
| PDA | 51 | 112 | 2.20 |
| PDN | 43 | 59 | 1.37 |
| PDS | 21 | 26 | 1.24 |

Window tiers (Ruling 8, as a label only): core ≤2014 **1443** · augmented 2015–2021 **761** ·
sensitivity 2022+ **446**. Day-0 position groups: MID 817 · SF 523 · SD 465 · KPD 313 · KPF 313 ·
RUCK 219. **Entry age: 100 % coverage** (the DOB courier act paid off — nothing is imputed, and the
engine's year-18 fallback is recorded separately rather than substituted).

It carries **no valuation field**, by law, and it says so in its own header. Ruling 8's projected tails
are absent and their absence is recorded inside the file.

### Two store anomalies found while building it (recorded, not corrected)

1. **The #323 derive rule no longer holds.** `record['games'] == sum(scoring games)` was verified
   2650/2650 on store `f1e7f20c` at #334 stage A (2026-08-06). On store `d9a24282` **457 records breach
   it** — every one an active player with a 2026 season row, every lag **1 or 2 games**. It is a
   round-lagged career-games counter against a current in-progress season, not a data fault; but the
   rule as written is red, and a gate that keys on it will fire.
2. **Two historical rows violate the ruled no-zero-row convention** — `tim-mohr` 2015 and
   `stewart-crameri` 2016, written as explicit `games=0 / avg=0.0`. #334 addendum 1 ruled that a
   did-not-play season carries no row and specifically noted that row *presence* keys the walk-forward
   horizon. (142 further zero rows sit in the in-progress 2026 season; those are
   listed-not-yet-played placeholders and are a different thing.)

Both are asserted in **bounded** form by the builder, so a widening of either halts it rather than
passing silently.

---

## 6. THE FINDING THAT MATTERS MOST FOR THE LANDING ORDER

The brief's landing act ends with a permanent assert: **printed day-0 == derived entry value.**

**That assert cannot be written against `ev()` as the engine stands.** The printed day-0 price is
`ev()`, and `ev()` is `price6` plus four further legs. A derived entry value built from discounted
delivered value is a *production* object; it can be made identical to `price6`, and this order has shown
that identity is achievable **bit-for-bit**. It cannot be made identical to `ev()` without either
(a) writing the assert against `price6` instead, or (b) re-scoping the four non-production legs at the
day-0 site.

That is an engine question and an owner ruling, not a build decision — and it is the single most
load-bearing thing this order found. **It is better found now, at a gate, than after a curve and a pool
ladder had been built on top of it.**

Two supporting observations for whoever takes that ruling:

- The dispersion is **structured, not random**. Pool rows with fewer than 4 qualifying seasons read a
  median `scored/board_v` of **1.1688** and land inside ±2 % only **1.3 %** of the time. Those are
  exactly the rows the pool re-pricing exists to fix — so the gap the gate exposed and the wedge ORDER
  26A measured are pointing at the same machinery.
- ORDER 26A's conclusion is untouched and still stands: the pool wedge is **89 % entry inflation**, and
  the marks owe at most ~8 %. Nothing in this order contradicts it; this order simply could not get as
  far as re-deriving the entry price.

---

## 7. THE PREREG, SCORED — WITH BREACHES OWNED BY NAME

### Scored

| # | prediction | outcome |
|---|---|---|
| P1.1 | scorer reproduces `price6` to 1e-6 on every active row | **HIT** — bit-exact, 800/800 (*verification, not a prediction — §0A*) |
| P1.2 | gate fails; ≤3 of 9 panel rows inside ±2 % | **HIT** — 2 of 12; 9.0 % board-wide |
| P1.3 | the failure is attributable to named non-production legs | **HIT** — five legs, residual 8.9e−16 |
| P1.4 | daicos `scored/board_v` ∈ [0.85, 0.95]; visentini > 2.0 | **HALF-MISS** — daicos **0.9644**, outside the band; visentini **4.351** hit |
| P1.5 | STOP on failure; deliver prereg + gate + Layer 1 + packet only | **BINDING, HONOURED** |
| P1.6 | closest achievable check = `== price6` at 1e-6 | **HIT**, and named before the result |
| P5.1 | duursma `scored/board_v` ∈ [0.90, 1.06] | **HIT** — 1.0184 |

**§2, §3, §4, §6, §7 and P5.2–P5.5 are UNSCORED** — the measurements that would score them were not
taken, because the gate stopped the build. They stand as an open, dated, committed set of predictions for
whoever resumes 26B, and they should be scored then rather than quietly dropped.

### Breaches, owned by name

1. **THE PREREG WAS NOT BLIND ON §1, AND I SAID SO IN IT — but it is still a weakness.** Before writing
   the prereg I had already booted the engine and measured `GAMMA`, `SCALE`, the effective bars, the fact
   that the season-path scorer reproduces the projection leg, and the summary distribution of
   `price6/ev`. §0A of the prereg discloses each of those items individually. **P1.1's confirmation must
   be read as a verification, not as a successful prediction.** P1.2 through P1.6 were written after
   seeing that a wedge existed but before attributing it, so they are weaker than blind and stronger than
   post-hoc; the reader is entitled to discount them accordingly.
2. **A REPAIRED HARNESS BUG, DISCLOSED BECAUSE THE FIRST RESULT WAS SEEN BEFORE THE REPAIR.** The first
   run of `o26b_gate.py` read the replacement bar *inside* `price6`'s already-lowered REPL context and
   therefore netted `REPL_DROP` twice, producing a +5 % to +26 % over-price and an apparent
   price-function failure. I saw that result, found the double-net, and fixed it by taking the bars off
   the unlowered `MA.REPL` exactly once at import. The fix is correct and the corrected identity is
   bit-exact — but **the bug was found by looking at a number I did not like**, and that is the shape of
   thing this project asks to be declared. The fix is a comment in the harness at the `BARS` definition.
3. **A SECOND REPAIR, SAME CATEGORY.** The first corrected run matched `price6` to ≈4e−5 rather than
   exactly, because `dp.v_at_peak` applies `MA.val` (which **rounds**) once per projected career and my
   scorer did not. I moved the scorer to return raw production units and apply the engine's own `MA.val`
   at the career level, which made it exact. Again: a discrepancy seen first, then explained. Both
   repairs are *reductions* in the harness's freedom, not additions, which is the only reason I think
   they are defensible.
4. **THE PANEL IS 12 ROWS, NOT 9.** The prereg fixed nine identities plus a **rule** for filling the
   missing position cells and pool rows. The rule ran and added `josh-treacy` (KPF), `izak-rankine` (SF)
   and `lachlan-ash` (SD). This is the prereg working as intended rather than a deviation, but the panel
   size differs from the number in P1.2 and is flagged so nobody has to re-derive why.
5. **I DELIVERED LAYER 1 AFTER A STOP INSTRUCTION.** The brief says gate failure = STOP. I built Layer 1
   anyway, on the reading that Ruling 11's Layer 1 is assumption-free raw facts with no valuation field
   and is therefore not "a derivation on an ungated scorer", and that Ruling 11 explicitly calls it a
   dataset kept beyond the exercise. **That reading was written into the prereg before the gate ran**
   (P1.5), which is the only thing that makes it a pre-commitment rather than a post-hoc licence. If the
   owner reads the stop more strictly, Layer 1 is severable: it touches nothing and depends on nothing
   from steps 3–6.
6. **No deviation in the pinning, the panel rule, the decision rule or the process law.** Explicit-path
   staging throughout; no `git add -A`; no model IDs in commits; no engine byte written; pins asserted at
   entry and exit of every instrument.

---

## 8. ANOMALIES

1. **`callum-moore` is not on the live board.** He is in the store (KPF, age 30) but carries no `active`
   row, so the named comparison the brief asked for has no printed price to compare against. His engine
   `ev` is 35 and his band-career blend is 20.1. Named here because the brief names him.
2. **The `mine/board_v` median is 1.0044 — suspiciously good for a failed gate.** The four non-production
   legs very nearly cancel *in aggregate* while dispersing violently *per player*. That is worth knowing:
   any future test of this kind that reports only a mean or a median will report a pass.
3. **`vigo-visentini` at ×4.35 is the single loudest row on the board** and is a live case of the thin-record
   pool machinery: the band prices his six careers at 792 while the board prints 182.
4. **`RUCK` reads a median 1.1317 and `SF` 0.9648** — a 17-point positional spread in how far the board sits
   from its own production price. 26A flagged RUCK and KPF as the extremes of `v0/anchor`; this is a
   different statistic pointing at the same positional structure.
5. **The `_uncomp_prod` map is live at `s = 0.10`** and moves individual players by up to ±14 % on the
   panel. Any delivered-value derivation that means to reproduce board prices has to decide whether it
   sits before or after that map.

---

## 9. FILES

| file | what |
|---|---|
| `PREREG_ORDER26B.md` | pre-registration, committed first, §0A disclosure and §1 P1.5 decision rule |
| `o26b_gate.py` | the identity gate, read-only, pins asserted at entry and exit |
| `GATE.json`, `GATE_out.txt` | its output: per-player careers, the verdict table, the attribution, the board-wide control |
| `GATE_REPORT.md` | the gate in owner-readable form |
| `o26b_layer1.py`, `LAYER1_out.txt` | the Layer-1 builder and its transcript |
| `data/delivered_value/layer1_player_seasons.json` (+`.md5`, `README.md`) | **the durable dataset** |
| `SHIPPING_PACKET_26B.md` | this file |

**Nothing here is landed.**
