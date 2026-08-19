# PREREG — D6-CONSOLIDATION (register v760): THE INJURY CONSOLIDATION

**Pushed BEFORE the first engine edit (F6 discipline).** Branch `land/order-29`, base `55f4dd3`.
Evidence dir `docs/evidence/consolidation_2026-08-19/`.

**Titling.** A previous seat's prereg titled the break-speed adjudication "D6". That collision is
resolved by REGISTER numbering: this order is **D6-CONSOLIDATION** and everything here carries that
name. Nothing in this document adjudicates break speed.

**NOTHING IN THIS ORDER IS ADOPTED, MERGED, TAGGED OR PROMOTED.** Boards are PRICED, not adopted.
Those acts are owner-only. Nothing goes on `main`.

---

## 0 · THE BASE, AND THE FIRST PRICING ACT (already discharged)

The base is the owner-ruled D5-final dial stack (**OWNER-RULED, DATA-SUPPORTED**, 2026-08-19), with
the break mode at `RL_O41_BREAK=unwind`, `RL_O41_UNWIND=7`.

Reproduced byte-exact from the dial stack before this prereg was written, through the assembly seat's
own `bbASM.sh` unchanged:

```
board  ff936186   total 659,222   rows 804
engine e886222f855b41d6bc65188f8fe6ec80
store  cb38ef1171dcf20aae66ebf12682be0d   (pin cb38ef11)
v0surf 5dd34ca82735f5c8f021b1c7320df8f8   (pin 5dd34ca8)
PRINTED-DAY-0 ASSERT: 89 of 89
```

Raw: `BASE_REPRO_out.txt`. **The base reproduces. The order proceeds.**

The dial line, read off `build_v755ASM.sh` and the engine source (not guessed):

```
RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105
RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 RL_O40_RECW=0.47 RL_O40_PGMAT=1
RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1
RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7
```

**U0 = 7 is OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19).** That label is carried into the
source comments of this order's edit as a standing obligation, so no later pass can re-gloss it.

---

## 1 · ANTICIPATED DISCLOSURE FIRST — GUARD 5 IS RED ON THIS BRANCH, AND IT IS NOT MINE

The brief requires Guard 5 PASS before any pricing run. **It does not pass on `land/order-29`, and it
did not pass before this seat existed.** This is stated before any result so that nobody reads a green
build suite as a green Guard 5. ORDER P disclosed the same thing at `bc63d5d`.

`bash run_panel.sh` exits 1. Its own named remedy (`bash bootstrap.sh`) was run and **also** exits 1.
The complaints that SURVIVE the remedy:

| # | complaint | mine? |
|---|---|---|
| 1 | checkout `rl_model.py` 98f16794 != pinned 14000af2 | no — pin staleness, predates this order |
| 2 | `v0surf` load-path resolves to `/home/claude/v0surf.pkl` fbc5b393 != pinned 5dd34ca8 | no — a shadow file outside the repo |
| 3 | workspace engine `_merged_recover.py` != pinned `engine_head` a353a9d3 | no — the pin matches no engine on this branch |
| 4 | `fv` CHECKOUT DRIFT — `engine/forward_valuation` identity != pinned | no — predates this order |
| 5 | `fv` LOADED-PATH DRIFT — same identity, same cause | no — predates this order |

**Per the brief's own instruction I HALT THAT PATH rather than improvise around it: I will NOT claim
Guard 5 PASS on any run in this order.** The acceptance suite will carry Guard 5 as **RED,
PRE-EXISTING** with these five lines attached, and never as green.

What is true instead, and is the reason a board can still be believed: **every board in this order is
built through `bbASM.sh`, which pins the engine, the forward-valuation tree, the store, the five
thread variables and `RL_V0SURF_PKL` EXPLICITLY and prints their md5s on every run.** Complaint 2 in
particular does not touch a build: `bbASM.sh` sets `RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"`, and
`data/v0surf.pkl` on this branch **is** the pinned 5dd34ca8 (verified). The base board reproduced
byte-exact under exactly that harness, which is the strongest available evidence that the tree is the
tree.

**If the supervisor's charter requires a green Guard 5 for this order to count, this order cannot
satisfy it and the re-pin is a landing act outside this seat.** Reported, not worked around.

---

## 2 · THE FOUR LIVE CONSUMPTION SITES — VERIFIED LINE REFS, AND WHAT HAPPENS TO EACH

Line refs re-verified against the engine at `55f4dd3` (`engine/rl_after/_merged_recover.py`). The
brief's refs are correct to within the block; the exact lines are recorded here.

Every one of the four sites reads **one** object: `_AVAIL_STATE`, which today is populated at
`:5721` from `lti_register.build_state()` over `LTI_REGISTER.md`. That single fact is what makes a
one-dial consolidation possible: **re-key the state source and all four sites follow.**

| # | site | verified lines | reads | disposition under `RL_O42=1` |
|---|---|---|---|---|
| 1 | `_fe_p_one` / `_fEy` — the `fE=1.0` LTI override (behind audit F2's one-season-out leak) | 127-132 | `_AVAIL_STATE[key]['out']` | **RE-KEYED.** `out` now comes from the sheet. Register-only names stop overriding `fE`. |
| 2 | KPF fork-v — the 2026-exclusion / nuked season | 1207-1208 | `_AVAIL_STATE[key]['out']` | **RE-KEYED.** Only annotated-injured KPFs nuke 2026 and extend the window. |
| 3 | L1c clock advance `g += L*cp.SEASON` | 1414-1415 | `_AVAIL_STATE[key]['out']`, `['L']` | **RE-KEYED.** Membership from the sheet; `L` is the re-based `L₁₈` (§3). `cp.SEASON` at this site is **UNTOUCHED** — it is the clock's own season length, not the availability base. |
| 4 | `_AVAIL_STATE` population + `lti_return_table` (Part-2 return arm) | 5688-5752 (`assert` at 5698; `_RET_TAB` 5705-5715; `_AVAIL_STATE.update` at 5721) | `LTIREG.build_state()` | **STATE RE-KEYED to the sheet; the Part-2 RETURN ARM IS RETIRED** — see §5. |

`LTI_REGISTER.md` remains a file in the tree and remains seeded by `bootstrap.sh`. **What this order
retires is its LIVE CONSUMPTION**, not the artifact.

---

## 3 · THE 18-REBASE — THE FORM, AND EXACTLY WHAT HAPPENS TO THE `:5698` ASSERT

Today, `lti_register.py:115`:

```
L = 1 − min(g26 / G_FULL, 1)        G_FULL = 22
```

Under `RL_O42=1` the availability haircut is **re-based to the owner's 18-game season**:

```
L₁₈ = 1 − min(g / 18, 1)
```

**`g` STAYS THE STORE'S 2026 GAMES.** The register's own header states the governing rule — *"Game
counts are NEVER carried here — the store stays the single source of production (spec §3.3)"* — and
this order does not overturn it. **Pre-verified, and it makes the choice moot: the sheet's
`games_2026` column and the store's 2026 games agree on 37 of 37 annotated rows, zero
disagreements.** That agreement is itself re-asserted at build time (falsifier D6-F7).

### THE ASSERT — THE ANTICIPATED DISCLOSURE, HANDLED DELIBERATELY

`_merged_recover.py:5698`:

```
assert LTIREG.G_FULL==cp.SEASON, "LTI G_FULL %s != engine season-games cp.SEASON %s (one constant, spec §3.1)"
```

`G_FULL = 22`, `cp.SEASON = 22` (`engine/forward_valuation/conditional_prior.py:49`). Re-basing to 18
**by changing `G_FULL`** would break this assert by construction, and changing `cp.SEASON` is
forbidden.

**WHAT I WILL DO, STATED IN ADVANCE:**

- **`cp.SEASON` is NOT touched.** It stays 22.
- **`lti_register.G_FULL` is NOT touched.** It stays 22.
- **The assert at `:5698` is NOT touched, NOT weakened, and NOT made conditional. It stays exactly as
  written and it still PASSES on every board in this order, dial on and dial off.**
- The 18 enters as a **NEW, SEPARATELY NAMED constant**, `_O42_AVAIL_BASE = 18`, used only to form
  `L₁₈`. **Nothing is asserted equal to 18.** The 18 is the AVAILABILITY BASE — the owner's statement
  about how much of a season a player is expected to be available for — and it is deliberately NOT the
  season-length constant. The engine keeps exactly one season constant and it is still 22.
- A **new** dial-on assert records the separation so a later pass cannot silently collapse the two:
  `_O42_AVAIL_BASE == 18 and _O42_AVAIL_BASE != cp.SEASON`.

**If instead I find at build time that the re-base cannot be expressed without touching `G_FULL` or
`cp.SEASON`, I will HALT and report that, and will not ship a weakened assert.**

---

## 4 · MEMBERSHIP — THE RULE, AND THE MEASURED SETS

**Membership = the annotated-injured rows ONLY: the 37 `injured=Y` rows of
`docs/owner_annotations/SITTER_2026_v1.csv`.** Nothing else is injured. The register's 43 names have
no standing of their own.

**The sheet is asserted before it is consumed** (md5 `b26798c35adcd9bda5cef50ff2c884da` — pinned
prefix `b26798c35adcd9bd` **VERIFIED**; 219 rows; 37 `Y`). These are the pins ORDER 41's injury stream
already enforces at `:4017-4042`; this order repeats them at its own site rather than depending on
another dial's state.

The name→row resolution is the engine's OWN existing normaliser (`:4046`,
`re.sub(r'[^a-z0-9]+','-', name.lower())` matched against store `key` **or** `player`). It is not a
new mechanism. **Pre-verified: all 37 annotated rows resolve to exactly one store row each; zero
misses, zero ambiguities.** The `max-king` collision resolves correctly and the two are distinct
annotated rows — `Max King` → `max-king-stk`, `Maxwell King` → `max-king-syd`.

### THE MEASURED CROSS — AND A CORRECTION TO THE BRIEF

The register carries **43 unique keys** (45 rows; `reef-mcinnes` has two windows). All 43 currently
have `out=True`, i.e. all 43 receive treatment today.

| set | count |
|---|---:|
| annotated `injured=Y` rows | **37** |
| register keys | **43** |
| register **AND** annotated-Y — treatment continues, re-based | **23** |
| **register-only — LOSING treatment** | **20** |
| annotated-Y **not** in the register — **GAINING** treatment | **14** |

**THE BRIEF SAYS 21 REGISTER-ONLY ROWS. I MEASURE 20.** 43 = 23 + 20, and all 43 are `out=True`, so
there is no "not currently treated" residue that could make up the difference. **I preregister the
number as MEASURED, not as briefed, and the R1 table will be 37 + 20 with the discrepancy stated in
these words.** The 20:

`archie-may · brody-mihocek · deven-robertson · esava-ratugolea · ewan-mackinlay · jack-payne ·
jackson-archer · jacob-newton · jai-culley · jamie-elliott · joel-amartey · jonty-faull · mani-liddy ·
matt-carroll · noah-long · oscar-steene · sam-darcy · sam-flanders · toby-conway · toby-pink`

The **14 gaining** treatment are a real consequence of the ruling and are not suppressed: the sheet is
the only injury truth, so an annotated row that the old register never listed becomes injured.

---

## 5 · SITE 4's SECOND HALF — THE PART-2 RETURN ARM IS RETIRED, AND WHY

The return-season haircut (`lti_return_table.json`, `_ret_hc_for`, applied at `:1303`) is gated on
`section == 'A'`. **`section` is register-only information. The sheet has no section column and no
analogue of one.**

The order's own words are *"retired **or** re-keyed to the sheet"*. There is no honest re-keying here:
defaulting all 37 to Section A would **invent** section membership for 14 rows that were never on the
register at all. **This seat will not invent an owner input.**

**DISPOSITION: under `RL_O42=1` the Part-2 return arm is RETIRED** — `return_arm=False`, `ret_year`
carried at 2027, `_lti_ret_hc = 0.0` for every row. `RL_LTI_RETURN` and `lti_return_table.json` are
untouched and still govern the dial-off path exactly as today.

**This deletes a priced component and I will price it as its own number**, not fold it into the total:
today five rows carry a non-zero return haircut on the base board (Joshua Kelly 0.0872, Jack Viney
0.0909, Brayden Fiorini 0.0771, Jack Payne 0.0427, Esava Ratugolea 0.0586, Jamie Elliott 0.0909). The
packet reports the Part-2 delta separately so the owner can rule on the retirement on its own merits.

---

## 6 · THE DIAL

**`RL_O42` — one dial for the whole consolidation.** `RL_O42=1` switches all four sites from the
register to the sheet. Next free number: the engine's highest existing family is `RL_O41`. On the dial
line, never a default flip. Halts are named `ORDER 42 HALT:` per the engine's convention.

`RL_O42` unset ⇒ **not one byte of behaviour changes**: `LTIREG.build_state()` runs exactly as today,
the `:5698` assert runs exactly as today, `G_FULL` is 22, and the board is ff936186.

---

## 7 · THE R1 COMBINED-TAKE GUARD

The packet will print **PER ROW**, for the 37 annotated and the 20 register-only:

`row · key · membership (annotated / register-only) · g₂₀₂₆ · L₂₂ · L₁₈ · avail_hc · Part-1 take
(avail_nerf) · Part-2 take (lti_ret_delta) · COMBINED TAKE · price base → cand · Δ`

Both takes are read from the engine's own separable attribution (`_avail_nerf` / `_lti_ret_delta`,
computed at `:5738-5746`); they are not re-derived by this seat.

### CONWAY — THE OWNER'S STANDING WORD

**Toby Conway is NOT injured (sheet `injured=N`) and is EXPECTED TO KEEP HIS SITTING CHARGES.** He is
register-only, so he **loses LTI treatment** — that is the ruling working as intended. His sitting
charges come from a different mechanism (the depth/fade machinery: sheet depth 4.08, fade 0.346) and
**must survive untouched**.

Pre-measured on the base board: Conway `avail_hc=1.0000` but **`avail_nerf = 0`** — the LTI layer
already takes nothing from him, because his k=0 present leg is empty (0 games in 2026, last played
2024). So the prediction is that removing his LTI treatment costs him **0**, and his sitting charge is
untouched. **If the build removes or reduces Conway's sitting charges, that is a DEFECT: falsifier
D6-F4 fires, I HALT and report.**

Conway is a CHECK, not a target. No parameter in this order is chosen to produce any Conway outcome.

---

## 8 · NAMED FALSIFIERS, FIRE CONDITIONS, AND WHAT I REPORT IF THEY FIRE

| id | fires when | if it fires |
|---|---|---|
| **D6-F1** | `RL_O42` unset does not reproduce **ff936186** byte-exact | **HALT.** Report the two md5s. The dial is not clean; nothing else in the packet is believable. |
| **D6-F2** | every ORDER 41 dial unset does not reproduce **374d4e44** byte-exact | **HALT.** The standing identity is broken by my edit. Report both md5s and the chain state to f3101883 / 7f88f509. |
| **D6-F3** | two identical `RL_O42=1` runs differ | **HALT.** Report both md5s. |
| **D6-F4** | Toby Conway's sitting charge is removed or reduced under `RL_O42=1` | **HALT and report as a DEFECT**, in the owner's own words: the sheet wins, Conway is not injured, and he keeps his sitting charges. Report his base and candidate price, his fade and depth, and the mechanism that moved him. |
| **D6-F5** | the annotated membership resolved at build time is not exactly **37**, or any annotated row resolves to zero or >1 store rows | **HALT.** Report the count and the offending names. |
| **D6-F6** | any register-only key still appears in `_AVAIL_STATE` under `RL_O42=1`, i.e. a live register consumption survives | **HALT.** The consolidation is incomplete. Report the surviving keys. |
| **D6-F7** | the sheet's `games_2026` and the store's 2026 games disagree on any annotated row at build time | **HALT.** Report every disagreeing row. (Pre-verified 0 of 37; a fire means an input moved.) |
| **D6-F8** | `L₁₈ < L₂₂` for any row, or `L₁₈ ≠ 0` for a row with g ≥ 18 | **HALT.** The re-base is not the stated form. Report the row and both values. |
| **D6-F9** | any row OUTSIDE the 57-key union (37 annotated ∪ 20 register-only) moves between base and candidate | **REPORT PROMINENTLY** as a scope leak, with the count and the largest movers, and diagnose before claiming the board. |
| **D6-F10** | `cp.SEASON ≠ 22`, or `LTIREG.G_FULL ≠ cp.SEASON`, or the `:5698` assert is weakened/skipped on any board | **HALT.** The disclosure in §3 has been violated. |
| **D6-F11** | any acceptance row fails: day-0 89/89 · burn 0 · class 1.0671 (registered W2 basis) · tail 0.8004 · birthday probe +0 on the R3-aware probe · the 79/79 suite | **REPORT the failure in these preregistered words**, with the measured value against the expected one, and do not re-tune anything to recover it. |

**Guard 5 is NOT a falsifier in this order — it is a disclosed pre-existing RED (§1).** Scoring it as
a falsifier I could pass would be dishonest.

---

## 9 · DISCIPLINE THIS SEAT IS BOUND BY

- **No target-fitting.** Conway, Brodie, Madden, Goad, Mraz and Busslinger illustrate outcomes. **None
  of them gates a parameter.** The only free choices in this order are the two the owner already made
  (the sheet is the truth; the base is 18) plus the Part-2 retirement, which is declared in §5 and
  priced separately rather than absorbed.
- **Depths are quoted as depths.** "depth 4.08", "depth ≥ 3" — never re-glossed as "Nth year" prose.
- **Cohort clock:** MSD cohort = draft year; everyone else draft year + 1.
- **Adjudications and falsifier fires are reported HONESTLY, in the words above, even when they go
  against the ruling.** §1 (Guard 5) and §4 (20 not 21) are already exercises of that rule.
- **The board is PRICED, NOT ADOPTED.** No adoption, merge, tag or promotion language anywhere.

---

## 10 · DELIVERABLES

1. **This prereg**, pushed to `land/order-29` in its own commit **before** the engine edit.
2. The engine edit — **one dial, `RL_O42`** — carrying the **U0=7 OWNER-RULED, DATA-SUPPORTED** label
   in source comments.
3. `PACKET_D6.md`: board identity + total · per-site disposition of the four sites · the 18-rebase
   disclosure and what happened to the `:5698` assert · the R1 per-row table (37 + 20) · movers vs
   ff936186 with named-row commentary · acceptance suite · falsifier scoring.
4. Raw `*_out.txt` for every claim in the packet.

---

## 11 · AMENDMENT — **D6-F8 FIRED ON THE FIRST CANDIDATE BUILD, AND THE FALSIFIER WAS WRONG**

**Added AFTER the fire, on the same day, rather than editing §8 silently. The original wording of
D6-F8 above is left exactly as it was pushed at `bd365f9` so the record shows what was claimed
before the build and what the build did to it.**

**WHAT FIRED.** The first `RL_O42=1` build HALTED on its own guard:

```
ORDER 42 HALT: andy-moniz-wakefield — the re-base is not the stated form
(g=2 L22=0.909091 L18=0.888889). It may only ever RAISE the haircut, and
must clear to exactly zero at the availability base.
```

**THE DIAGNOSIS, AND IT GOES AGAINST ME: the falsifier was mis-stated, not the re-base.** §8 asserted
that the re-base "may only ever RAISE the haircut". **That is arithmetically backwards.** Against a
SHORTER season the same games are a LARGER fraction of it, so `g/18 > g/22` and therefore
`L₁₈ ≤ L₂₂`. Andy Moniz-Wakefield with 2 games reads `1 − 2/22 = 0.909091` on the old base and
`1 − 2/18 = 0.888889` on the new one — a **smaller** haircut, exactly as the arithmetic requires.

**THE RE-BASE ITSELF IS UNCHANGED AND IS EXACTLY WHAT WAS BRIEFED AND PREREGISTERED**: `L₁₈ = 1 −
min(g/18, 1)`, the form stated in §3 and in the order. **Not one constant moved to make the guard
pass.** What changed is the guard's claim about the direction of the form it guards.

**THE SUBSTANTIVE CONSEQUENCE, STATED PLAINLY BECAUSE IT IS A REAL RESULT AND NOT A BOOKKEEPING
NOTE: re-basing to the owner's 18-game availability season makes an injured row who PLAYED SOME
GAMES in 2026 LESS penalised, not more.** A row with zero 2026 games is unaffected (`L = 1` on both
bases). Only rows with `0 < g < 18` move, and they move DOWNWARD in haircut. The packet reports how
many rows that is and what it is worth.

**THE CORRECTED D6-F8**, now in the engine, guards the invariant the form actually has:

| | condition |
|---|---|
| range | `0 ≤ L₁₈ ≤ 1` |
| direction | `L₁₈ ≤ L₂₂` — against the shorter base the haircut may only FALL or hold |
| clears at the base | `g ≥ 18 ⇒ L₁₈ = 0` exactly |
| no games | `g = 0 ⇒ L₁₈ = 1` exactly |

**It fires and HALTS on any violation, exactly as before.** The guard was not removed, weakened into
a warning, or made conditional — it was pointed at the right invariant.

**This amendment is itself reportable and is reported: a falsifier fired, and the honest reading is
that this seat's preregistered arithmetic was wrong.** It is recorded here and in `PACKET_D6.md`
rather than being quietly corrected between builds.
