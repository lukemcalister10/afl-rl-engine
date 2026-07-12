# A-DARCY — TRIPLE-LOCUS ATTRIBUTION (closes audit CA-9) · BAKE v2.8 · 2026-07-12

**Player:** `sam-darcy` — Sam Darcy, Western Bulldogs, KEY_FWD (Father-Son), age 23, pick 2 (ND 2021).
**Board:** candidate chapter-lever L1 board `9ecbe0fa` (== full == L1-only; L2 shipped nothing).
**Anchor requirement (acceptance v1.6, A-DARCY):** *lifts*; triple-locus (young-convexity ceiling ·
KPF-speculative · availability) — attribute WHICH layer held him down; **none may clip his ceiling.**

## VERDICT — PASS
Sam Darcy **lifts to v = 4013 SCAR** (band 0, top of board; the 9th KEY_FWD by value, above every KPF
except the four established/older ones). **Exactly one** of the three loci is an active suppressor — the
**availability layer** — and it is a legitimate, bounded, present-year (2026) proration for a real
absence, **not** a ceiling clip. The young-convexity ceiling and the KPF-speculative locus are both
**inactive/absent** for him. His forward and peak values are intact.

## THE THREE LOCI (from the committed board record + the injury machinery)

### 1. Young-convexity ceiling — ABSENT (no clip)
`cvx = 1.0`. The convexity multiplier is neutral (1.0) for Sam Darcy — and, verified, for all 805 active
records in this board (G-CONVEX is ADVISORY; the metric prices synthetic reference players, not the real
board, per CONSTRAINTS v1.6). **No convexity ceiling is applied to him; nothing caps his young-KPF option
value.** Absence is the finding here, not a failure.

### 2. KPF-speculative — ABSENT (priced as a full KEY_FWD, no speculative haircut)
`mech = None`; `grp = gf = KEY_FWD`; `fut = [['KEY_FWD', 1.0]]`. The engine's mechanism tags that could
discount a speculative/thin key forward (observed on the board: `SSP`, `MSD`, `PDN`, `PDA`, `IRE`, `UNR`)
are **not** attached to Darcy — he carries no speculative-KPF flag. He is priced on his demonstrated
KEY_FWD production (track: s1 51.8 → s3 79.0 → s4 95.7 → s5 81.8), not marked down as unproven. **No
KPF-speculative layer holds him down.**

### 3. Availability layer — ACTIVE, and the SOLE suppressor (−677 SCAR, present-year proration only)
`avail_hc = 0.7273` · `avail_nerf = −677` · `lti_return_hc = 0.0` ·
`lti_reg = {L: 0.7273, designations: ['2026'], out: True, ret_year: 2027, return_arm: True, section: 'A'}`.

This is the Chapter-3 RL_AVAIL machinery (owner-authored LTI register, pinned input R-REG=R2). Darcy sits
in **register Section A, designated out for 2026, returning 2027** (his real ACL). The engine's separable
two-part treatment (G-ATTR, engine `_merged_recover.py` lines ~500 / ~1038–1066):

- **Part 1 — present-season lost-production haircut.** For the present year only (k==0, BASE_REF 2026),
  the production lever is scaled by `(1 − avail_hc) = (1 − 0.7273) = 0.2727` — i.e. ~72.7% of the 2026
  season is priced out. Effect, measured as the layer-on minus layer-off delta: **avail_nerf = −677 SCAR.**
- **Part 2 — return haircut.** `lti_return_hc = 0.0` → **no** return-year haircut. This matches the
  acceptance note exactly: no LTI *return*-haircut machinery bites him; the availability effect is purely
  the present-season proration (the `_b2hc`/season-proration family), never a haircut on his return form.

**Quantified:** fully-available (layer-off) Sam Darcy prices at **≈ 4690 SCAR**; the real 2026 absence
prorates him **−677** to the shipped **4013**. The suppression is entirely the current-season proration
and it **unwinds on return** (`return_arm: True`, `ret_year: 2027`, return-haircut 0.0).

## DOES ANY LAYER CLIP HIS CEILING? — NO
His forward/retrospective lens components are undiminished: `vP1 = 3720`, `vP2 = 2924` (projected years),
`vM1 = 6010`, `vM2 = 3285` (prior years). The only reduction is the bounded −677 present-year availability
proration, which is a real-world 2026 discount, not a cap on his underlying talent or option value.
Convexity (locus 1) and KPF-speculative (locus 2) apply **zero** clip. **No layer clips his ceiling.**

## SEPARABILITY (G-ATTR)
The three loci are individually attributable from the board's own separable columns
(`cvx` · `mech` · `avail_nerf`/`lti_return_hc`), each independently zero or quantified. L1 (young-GDEF
transition credit) is **GEN_DEF-only** and does not touch Sam Darcy (KEY_FWD) — his 4013 is entirely
base-engine + the pick redenomination, with L1 contribution = 0. (Base v2.7 comparator 3825 → candidate
4013 is the +5.24% redenomination, not a lever on him.)

## CA-9 STATUS: CLOSED
The audit's CA-9 gap (Darcy attribution not emitted) is closed: **availability layer is the single active
suppressor (−677, present-season proration, return-haircut 0.0); convexity ceiling and KPF-speculative are
absent; no layer clips his ceiling; he lifts to 4013.** Direction "up" satisfied; A-DARCY is OWNER_ON_SIGHT
+ attribution-mandatory — the attribution is hereby supplied for the owner's on-sight read.
