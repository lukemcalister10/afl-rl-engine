# LTI / AVAILABILITY MECHANISM AUDIT — FINDINGS

**Scope:** characterize how the BAKED engine treats injury/availability — MECHANISM and
EXISTENCE, not price magnitudes. READ-ONLY; no engine change, no bake.
**State:** `[BAKED c47cb43d]` · main `389ac39` · register `LTI_REGISTER_2026-07-02.md` **is committed**.
**Name-collision guard:** every single-player line carries identity (cohort-year · pick · pos); never surname alone.
**Evidence:** `probe_availability.py`, `reconcile_register.py`, `grep_machinery.sh` (this dir).

Repo paths: engine = `engine/rl_after/_merged_recover.py`; support = `engine/rl_after/rl_model.py`;
pricing = `engine/forward_valuation/distribution_pricing.py`. (Workspace mirror: `/home/claude/rl_workspace/…`.)

---

## STEP 0 — asserts
- `origin/main` = **389ac39** ✓
- engine md5 (`_merged_recover.py`, repo + workspace) = **c47cb43d** ✓
- `LTI_REGISTER_2026-07-02.md` = **committed** ✓ (do not re-commit)

---

## (1) Does LTI / haircut machinery already exist?  — PARTIALLY. Verify-don't-assert result below.

**A present-unavailability haircut EXISTS and reaches the baked board. A return-season (LTI) haircut DOES NOT exist.**

- **EXISTS — `_b2hc`, "B2 present-unavailability haircut"** — `engine/rl_after/rl_model.py:800‑811` (set),
  `:804` (`_b2band`), applied at the current (k==0) production step `:316` and `:330`, plumbed via
  `proj_from_peak(..., pre_hc=p['_b2hc'])` at `rl_model.py:410` and consumed by the baked pricing path at
  `engine/forward_valuation/distribution_pricing.py:254` (`v_at_peak` → `price6` → `raw_ev` → baked `ev()`).
  - **Fires when:** established (≥3 pre-2026 seasons) AND recent-3-season peak avg ≥ 90 SC AND **zero 2026 games**
    AND season >1/3 elapsed. Age-banded cut: **<27 → 8.8%, 27–29 → 3.9%, 30+ → 0%** (age curve already prices 30+).
  - **What it is:** a small, single-season cut to the *present* production step only. Its own comment: *"Transient →
    next build's return data supersedes it."* It is **not** a forward/return-season discount.
  - **Verified live:** it fires on only **2 of 42** register players — Nic Martin (`_b2hc=0.088`, costs −229) and
    Tom Green (`0.088`, costs −291). Everyone else = `0.000` (peak <90, or age 30+, or partial games logged).

- **EXISTS but NOT injury — `_role_decay_hc` (O'Brien rule)** — `rl_model.py:178,184‑194`. Explicitly *"dropped on
  ability (role collapsed, output cratered), **not injury**"*; requires 1≤games<3 this season with output ≥30% below
  baseline. An availability question, mis-answered by this gate, would be a false positive — it is scoped away from us.

- **DOES NOT EXIST — return-season / LTI haircut.** Grep-by-concept across engine + `rl_model` + `wire_redesign` +
  `par_redesign` + `distribution_pricing` finds no return-season, layoff-length, or "out-until-YYYY" discount. The
  register's own timing designations (may-return-2026 vs out-till-2027) have **no consumer in the engine today.**
  → **This is the gate the owner parked: the LTI return-season haircut is greenfield.**

---

## (2) The zero-games / calendar mechanism — why an injured established player BUMPS, why Rozee FREEZES

The engine reads a player who logged zero (or few) 2026 games through the **M3 clock-pin** (`_merged_recover.py`
`M3 CLOCK-PIN PLUMBING` :203‑234; `_ev_m3` :525‑534; `_m3_s` :522‑524; wired into live `ev` via
`ev_prefloor=_ev_m3` :549).

**Mechanism.** Mid-season the age/tenure clocks advance a **full** year, but only `fE=0.58` of the season has
elapsed. M3 corrects this by blending the full-calendar evaluation (`click`) with a **clock-pinned** evaluation
(age −1, tenure −1, `_M3PIN`): `ev = w·click + (1−w)·pin`, `w = 1 − s·(1−fE)`, `s = clip(1 − g₂₀₂₆/11, 0, 1)`.
- **On-pace player** (g₂₀₂₆ ≥ 11) → `s=0` → untouched by construction (verified: Elliott, Flanders, Amartey).
- **Zero-games player** → `s=1` → **maximum pinning** → clock read a full year younger.

**(a) Injured established → BUMP.** For an established player the pinned (younger) clock is worth *more* (less age
decay, level held at last-good seasons since zero-game rows contribute nothing to the recency-weighted level). The
missing season is read as **freshness (not-yet-aged), never as unavailability.**
- **Nic Martin** [store `Nicholas Martin` · coh2021 · pickless(effpk94) · MID]: no 2026 row; last seasons 79/88/105/98.
  `click=2688`, `pin=3664`; baked `ev=3098`. **3098 / 2688 = +15.25 %** → *this is the observed "+15%".* The `_b2hc`
  8.8% cut (−229) is real but is dwarfed by the pin lift (+410 net after the 0.58 blend).
- Same bump on every zero-games established case: Tom Green (3908→ev 4436), Jack Viney (632→801), Darcy Jones
  (1361→1639), Deven Robertson (250→369), Josh Sinn (241→357).

**(b) Rozee → FREEZE at partial games.** **Connor Rozee** [coh2018 · pk5 · MID], g₂₀₂₆=2, `ns_pro=7` (established) →
**NORMAL** branch, not sit-out. His identity resolves cleanly by pick/cohort (no name collision), and his 2-game
partial season is taken **at pace** via M3 (`s=0.82`, `w=0.66`): `click=2610`, `pin=3435`, `ev=2894`. The "freeze"
is that the engine takes the 2-game snapshot as a functioning established mid and **does not flag him out-for-season
or discount the layoff** — identity is handled, availability is not.

**Feature or artifact?** M3's *design intent* (avoid over-aging a player whose calendar year hasn't finished) is a
legitimate feature for players who **will still play**. The **bump on injured players is an ARTIFACT**: M3 keys purely
on games-logged and cannot distinguish "hasn't played *yet*" from "won't play *at all*." Absence-of-games is read as
freshness; the injured established player therefore receives the **largest** anti-aging credit precisely because he is
injured. (Note the pin is not universally a bump — for thin-career *young* players tenure-loss can outweigh the age
gain and pin < click: e.g. Harry O'Farrell 833→693, Jonty Faull 1168→938. The bump is the *established*-player case.)

---

## (3) Register reconciliation by timing-class (MECHANISM, not $)  — 42 players; branch split NORMAL 33 / SIT-OUT 9 / DELIST 0

The engine has **no signal that separates the register's timing classes.** "2025", "2026", and "2026 pre-season"
zero-games players are all mechanically identical (zero 2026 row → NORMAL branch → M3 pin bump ± `_b2hc`). The only
real fork is **career depth** (established vs never-qualified), not injury timing.

| register timing-class | representative (identity) | 2026 prod registers? | engine branch | availability treatment today |
|---|---|---|---|---|
| **A · 2025** (may return 2026) | Nic Martin [`Nicholas Martin` coh2021 · pickless · MID] | no 2026 row → nil | NORMAL | valued off last-good seasons; **M3 pin +15%**; `_b2hc` −8.8% (peak≥90). Net **bumped**. "May return 2026" invisible to engine. |
| **A · 2026** (out till 2027) | Tom Green [coh2019 · pk10 · MID] | no row → nil | NORMAL | same as above (`_b2hc` fires, peak≥90). "Out till 2027" invisible. |
| **A · 2026 pre-season** (out till 2027) | Jack Viney [coh2012 · pk13 · MID] | no row → nil | NORMAL | M3 pin bump (632→801); no `_b2hc` (age 30+ band=0). Mechanically indistinguishable from the "2025" class. |
| **A · established, partial 2026** | Sam Darcy [coh2021 · pk2 · KEY_FWD], g=6 | 6 games @ pace | NORMAL | partial season taken at pace; M3 `s=0.45` → mild bump. No layoff discount. |
| **A/B · never-qualified sitter** (`ns_pro==0`) | Lewis Hayes [coh2022 · pk25 · KEY_DEF]; Toby Conway [coh2021 · pk24 · RUC] | no qualifying season | **SIT-OUT** | `sitout_ev` = V0-anchored retention `(1−λ)·R·V0 + λ·e_full` (`:460‑465`), clock-independent → **M3 does not move them**. Scoring-aware if any games logged (Jacob Newton 3g). |
| **B · out 2026, no haircut** | Connor Rozee [coh2018 · pk5 · MID], g=2 | 2 games @ pace | NORMAL | **freeze** case above; valued as functioning mid, no out-for-season recognition. |
| **true departure** (for contrast) | *(none in register)* — gate = `_retired` or `_last_listed<2026` | — | **DELIST-scrap** `0.02·V0` (`:490`) | **0 of 42 register players caught.** Confirms the delist gate is departure-only and never fires on injuries. |

- `nil-2026 production registers?` — **No.** Zero-game seasons contribute nothing to the recency-weighted level
  (rows filtered `games>0`), so production is simply held at the last-good seasons; there is no explicit nil-out.
- `is there any haircut?` — Only `_b2hc` (present-component, 2/42 players), and it is **out-weighed by the M3 bump**.
- `does the delist gate catch injuries?` — **No.** It keys on `_last_listed`/`_retired` (`rl_model.py:871‑877,887‑890`);
  injured-but-listed players (all 42) pass through untouched.

---

## (4) Interaction surfaces — where future LTI wiring must reconcile with existing machinery

| surface | file : line | why LTI must reconcile |
|---|---|---|
| **The calendar / M3 clock-pin fix** | `engine/rl_after/_merged_recover.py:203‑234, 522‑534` (`_ev_m3`, `_m3_s`, `_M3PIN`) | **The bump lives here.** LTI must make M3 (or a pre-M3 gate) read register-confirmed injury as *unavailable*, not *fresh*. This is the primary fix site — the +15% originates here. |
| **The cliff blend / sit-out retention** | `_merged_recover.py:460‑465` (`sitout_ev`), `303` (`LAM_SIT`), `281‑302` (`R_SURF`, `_R_surf`) | The `ns_pro==0` sitter path already blends V0-retention → production with a continuous (no-cliff) λ ramp. An LTI return-season haircut should compose with this λ/R surface, not duplicate it, for the 9 never-qualified sitters. |
| **`SITOUT_RETAIN` successor (V0-anchor + R surface)** | `_merged_recover.py:245‑303`; `v0_start` `430‑434` | The flat `SITOUT_RETAIN×draftval` anchor is purged; retention now = `R_SURF × v0_start`. LTI haircuts must be expressed on the **live V0 scale**, not old-PVC draftval. |
| **The present-unavailability haircut** | `rl_model.py:800‑811`; applied `:316,:330`; plumbed `:410` → `distribution_pricing.py:254` | `_b2hc` is the existing hook to extend/replace. LTI must decide: widen `_b2hc` (peak≥90 gate, age bands, present-only) into a register-driven forward haircut, or supersede it. |
| **The delist gate** | `_merged_recover.py:237,490`; `rl_model.py:871‑877,887‑890` | Departure-only by design. LTI is the *complement*: catch injuries the delist gate deliberately lets through. Keep them separate (a listed injured player is not delisted). |
| **The register itself** | `LTI_REGISTER_2026-07-02.md` (committed) | Ground-truth availability + timing-class. The engine has **no consumer for it today** — the LTI layer is the consumer to build. Consumers must key by ID/pick/cohort (Max King → Maxwell King; 8 known collisions). |

Guardrail carried from the register: *A3 is evaluated PRE-LTI-layer — any LTI overlay must not be the thing that passes A3.*

---

## IN PLAIN TERMS
The engine does **not** meaningfully handle injuries today. The one existing lever is a small present-season haircut
(`_b2hc`, ~9%, only for high-scoring under-27s), and it is out-weighed by a bigger, opposite effect: the mid-season
"clock-pin" (M3) reads a player's missing games as *not having aged yet* and **bumps** an injured established player —
Nic Martin lands **+15%** for being hurt. Injured players never trip the delist scrap (that's departure-only), and the
register's timing classes (may-return-2026 vs out-till-2027) are **invisible** to the engine — all zero-games cases
look identical. The LTI workstream will have to **build** the return-season haircut from scratch (there is no
existing one to tune), and **reconcile** it against three live surfaces it will collide with: the M3 clock-pin (fix
the freshness-misread), the sit-out V0/R retention blend (compose, don't duplicate), and the delist gate (stay
complementary). Magnitudes above are illustrative `[BAKED c47cb43d]` and will move when the overhaul re-prices; the
mechanism findings survive.
