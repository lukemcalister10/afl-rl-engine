# Pre-registration — the second candidate round, written BEFORE the emits

Four emits: an identity proof, A-as-floor, A-evidence-faded-drag, and discount V4.

---

## 0. IDENT — the identity proof, and it runs first

Three new dials were added to the engine (`RL_A_FLOOR`, `RL_A_DRAGFADE`, and V4's `mode 4` branch).
With all of them **off**, the emit must reproduce `per_entrant_FULL.json` **exactly**.

- **PASS**: matrix md5 `== c698b5b2`
- **FAIL**: any other md5 → the additions are not inert when off → **HALT**, and none of the three
  candidate readings below may be reported, because they would be measured against a moved baseline.

This is the first thing run and the gate on everything after it.

---

## 1. A-AS-FLOOR (`RL_A_FLOOR=1`)

One-way borrowing: `price = max(production-led value, blended value)` at the A site. Since
`blend = e_full + s·(anch − e_full)`, the blend exceeds `e_full` **iff** `anch > e_full`, so this is
exactly "apply the blend only where it raises the row", continuous at `anch == e_full`.

**Expected**: yr1 book rises **above main's 1.1239** (cold rows lifted, hot rows no longer dragged);
yr4 moves little; a **net book lift** that the conservation re-teach must absorb — **its size is
printed, not asserted to be small.**

**Surprise-law interaction — the composition order implemented, and why.** SUR acts inside
`sitout_ev` on the sit-out path; the floor acts at the A site in `ev()`; **neither is applied to the
other's output.** The floor **cannot undo SUR on a hot row**: SUR's job on a hot thin record is to
shrink it toward the anchor, and the floor is **inert whenever `anch < e_full`** — it only ever
raises. Hot rows stay shrinkable **by construction, not by tuning**.

Where they *do* compose, flagged as an interaction to watch: SUR's statistic
`s = |log(e_full/anchor)|` is **symmetric in sign**, so it also fires on a **cold** thin record and
pushes it *toward* the anchor — i.e. **up**. On cold thin rows SUR and the floor push the **same
way**. That is the one place a double-lift can appear, and the measurement prints its size.

---

## 2. A-EVIDENCE-FADED DRAG (`RL_A_DRAGFADE=1`)

In the **drag case only** (`anch < e_full`), the anchor's weight `s` is scaled by `(1 − w)`, with `w`
the ITEM C evidence weight. The **support case keeps the existing games-fade untouched**.

**Expected**: yr1 recovers **most** of the −11.3%, and this variant **sits between FULL and A-floor
in every rung**. That ordering is the sharpest test — if it does not sit between them, the design is
not doing what it claims.

**One-sa-reader discipline — asserted, not assumed.** `w` is computed **exactly once** per call and
serves **both** the C ceiling release (on the anchor *level*) and the drag fade (on the anchor
*weight*). `sa` is read once per row, one par lookup, exactly as before.

**How the two roles interact.** They act in **opposite directions** on a drag-case row, so they
cannot compound into a runaway: a high-evidence player gets a **larger** C release
(`anch × (1 + w(H−1))`) but a **smaller** drag weight (`s × (1−w)`). The more proof he has, the more
his own production leads and the less the raised ceiling can pull him back.

**Clamp, disclosed because it is a real edge.** `w = G·Q·gate` is **not bounded by 1** — `Q` is
clipped at `_C_QMAX = 2.0`, so `w` can approach 2. An unclamped `(1−w)` would go **negative** and
flip the anchor from a drag into a *push*, which is not the design. The scale is clipped to `[0,1]`;
at `w ≥ 1` the drag is fully faded and the row prices on production alone — the intended limit.

---

## 3. DISCOUNT V4 (`RL_AGE_DISC=1 RL_AGE_DISC_MODE=4`)

Current-age keyed: 11% ≤19 · 12% at 20 · 13% at 21 · 14% at 22 · smooth glide 14→15 across 23-25 ·
15% at 26-27 · 16% ≥28.

### The "yr4 exactly unchanged" expectation needs one correction, and I am filing it in advance

The order pre-registers *"yr4 book EXACTLY unchanged vs FULL (age-22 rate = baseline 14% under
current-age keying — if yr4 moves at all beyond noise, that is a keying surprise, halt and report)"*.

**That holds only for players who are exactly 22 at year 4, and 14.2% of the population is not.**
Measured on the canonical population (n=1197), draft-age dispersion is real:

| draft age | share | age at yr4 | V4 rate | effect vs flat 14% |
|---|---|---|---|---|
| 17 | 8.4% | 21 | 13.0% | less discount → **value up** |
| 18 | 81.7% | 22 | 14.0% | unchanged |
| 19 | 4.1% | 23 | 14.0% | unchanged |
| 20-26 | 5.8% | 24-30 | 14.5-16.0% | more discount → **value down** |

**85.8% unchanged · 8.4% valued up · 5.8% valued down.**

So a **small** yr4 move is *structurally guaranteed* by draft-age dispersion and is **NOT a keying
surprise**. Filing this before the measurement so that a small move is neither mis-reported as a
surprise **nor explained away after the fact**.

- **NOT a surprise**: a small yr4 move consistent with ~14% of the book seeing a non-baseline rate.
- **IS a surprise, and halts**: a *large* yr4 move, or one whose direction/size cannot be accounted
  for by the table above — that would mean the keying is not current-age as specified.

**Expected otherwise**: yr1-3 lifted (11/12/13%); yr5+ trimmed (23+ sits above baseline), which
should help the peak/yr0 envelope. The **free-money margin at yr0→yr1 is printed against the 11%
line** (the 19-year-old rate), which binds if any combination lifts yr1 above ~1.11.

---

**Nothing is tuned toward any of this.** The envelope and the no-arb frame are frames for judging,
not targets. Sizing remains the owner's word. Nothing ships.
