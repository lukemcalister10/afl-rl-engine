# #306 L6 — **HALT BEFORE THE DERIVATION: THE FEED-BACK CHANNEL IS WIDER THAN THE 71 ROWS**

**Seat `2a1xa4`, 2026-08-05.** Filed under the rotation order's own stop condition
([#306 comment 5185851272](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5185851272)):
*"Confirm this against the recorded provenance before anything runs; **if the channel is other than these
rows, stop and file.**"*

**The derivation did not run.** Fire-order steps 1–4 completed and passed; step 5 halted on this finding.
Substrate restored and proven. Bake held; EXECUTION word withheld; nothing landed.

---

## 1 · THE COUNT CONFIRMS. THE CHANNEL DOES NOT.

The order's arithmetic is exactly right, and it re-measured exactly right on a matrix emitted on the lens
substrate: **825 concluded + 301 completed + 71 counted-fallback = 1,197**, share **5.931%**. Identical to
`structural_basis_279.json`'s recorded provenance. That much is confirmed.

But the count describes the **composition**, not the **channel**. The channel is the path by which a moved
surface reaches the next curve, and it is measurably wider:

| how the row is valued | rows | moved | moved % | mean \|d\| | max \|d\| |
|---|---|---|---|---|---|
| `concluded_realised` | 825 | **475** | 57.6% | 22.53 | 238.79 |
| `completed` | 301 | **292** | 97.0% | 11.96 | 152.62 |
| `prior_fallback_thin` | 71 | 70 | 98.6% | 255.77 | 607.40 |

**Share of total absolute movement (32,095.8 over 1,197 rows):**
the 71 counted-fallback rows carry **55.78%** — the largest single concentration by far, and the order is
right that they are the loudest door. **The other 1,126 rows carry 44.22%.**

## 2 · THE MECHANISM, FROM THE CODE — NOT INFERRED

`emit_matrix_271.py` builds each row's value path from the engine's own valuation:

```
ASOF[(id(p), Y)] = ev(p, Y)                      # walk-forward, per as-of year
Vpath           = [ASOF[(id(p), y)] for y in yrs]
```

`harness_pvc.realised_full` / `realised_at` then average that `vpath` under the evidence weights to produce
the structural career value **for every concluded row**. `ev()` leans on the year-zero prior wherever a
career's own evidence is thin — so **a moved surface reaches a concluded row's realised value without ever
touching the counted-fallback path.**

Measured directly: **`vpath` differs in 1,128 of 2,646 records** between the two emits. Worked example —
`scott-gumbleton` (`concluded_realised` on both sides, `pw` identical, never a fallback row):

```
vpath old  [1077, 383, 351, 1005, 283, 384, 416]
vpath new  [1217, 945, 866, 1005, 457, 384, 416]
structural value  566.0054  ->  804.7992
```

The rows with **0 games and 1–5 games do not move at all** (141 + 90 rows): they are `never_established`
and sit at 0.0 by construction. The movement is carried by players **with** careers — 380 of the 420 rows
at 101+ games moved, mean \|d\| 51.15.

## 3 · THE LIMIT OF THIS COMPARISON, STATED RATHER THAN BURIED

The two matrices differ in **both** the surface (`fb9efdec` → `b540833b`) **and** the engine
(`3c7b0c3c` → `15525b03`, the lens). So this measures the redesign's **total** effect on the teaching
values; **it does not by itself split that between the two causes.** The mechanism above is
surface-sensitive by construction, which is why the narrow-channel premise cannot stand as stated — but
the clean attribution needs one more measurement, named rather than assumed:

> **The control:** emit on the **lens engine** carrying the **old surface** `fb9efdec`
> (re-pinning `expected_boot.v0surf` so Guard 5 passes), and compare to this emit. The delta is then the
> surface alone. ~147s of emit plus the substrate swap and its restore.

I did not run it: the order's stop condition had already fired, and swapping the installed surface is a
substrate act on a held bake that the seam should authorise rather than a seat assume.

## 4 · WHY THIS IS WORTH A HALT AND NOT A FOOTNOTE

The mechanical fixed-point test — `derived payload md5 == e69a3f38` — does not depend on the channel's
width. **The interpretation of the result does.** If the channel were the 71 rows at 5.931%, a fixed point
would mean the loop had closed through one narrow, counted, printed door. It does not: it closes through
the realised values of the majority of the teaching population, most of which never appear in any fallback
count. A convergence verdict reported on the narrow-channel premise would be a **correct audit of the wrong
question** — hazard class 16, the one the owner himself had to extract at v562.

The redesign's own §2 correction says the same thing in a different register: *the cycle is a property of
the ruled composition itself.* A wide channel is what a composed map looks like from the inside.

## 5 · WHAT PASSED BEFORE THE HALT

| step | result |
|---|---|
| 1 · lane-wiring proof | **PASS** — payload `1a8db02b`, ladder total 54,350, s 0.998224, pooled head 3005.3384, ladder identical at all 64 picks |
| 2 · the re-pin | **DONE** — `EXPECT_V0SURF 8291668eff41 → 96d671c952c8`; store and N unchanged and re-measured; non-vacuity proven in both directions before **and** after |
| 3 · matrix emit | **DONE** — 147s; md5 `e1c62f8677e5714df1be4e91c960ec7c`; store `81d24704`, sig `96d671c952c8` — **the matrix met the pin set before the emit**; F-C full-md5 binding holds; `EXPECT_N` re-measured 1197; key set vs #290 pass 0: **0 added, 0 dropped** |
| 4 · channel check | **HALT — the condition fired** |
| 5 · derivation | **NOT RUN** |
| 6 · restore | **PROVEN** — `2f8b4bd4` → `2f8b4bd4`; round trip to `2b7640be` intact apart from the one authorised re-pin |

## 6 · REPRODUCING THIS

```
# under the pinned venv, from a dir holding the re-pinned harness as harness_pvc.py
python3 channel_width.py  l6/pass0_lens_matrix.json  <#290>/L6_convergence/pass0_matrix.json
```

`l6/channel_width.py` is the instrument; `l6/channel_width.txt` is its recorded output; `l6/pass0_lens_matrix.json`
(`e1c62f86`) is the emitted matrix with `l6/pass0_matrix_identity.json` beside it. Committed as evidence so the
finding is re-runnable rather than asserted — and committed **before** the substrate operations that follow it.
