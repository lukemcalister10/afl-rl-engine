# PREREG — THE F2 FIX: R3 MUST NOT CHARGE A ROW WHOSE ONLY ABSENCE IS THE IN-PROGRESS SEASON

**Seat:** ASSEMBLY BUILD. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Raised by:** the independent audit, `docs/evidence/audit_2026-08-19/AUDIT_PACKET.md` (`f76dbb0`),
finding **F2 (HIGH)**.

**THIS FILE IS PUSHED BEFORE THE ENGINE EDIT IT DESCRIBES.** That is the discipline the audit's **F6**
found broken on three of four previous passes, and it restarts here. **Nothing below is a result.**

---

## 1 · THE DEFECT, AS THE AUDIT FOUND IT AND AS I RE-VERIFIED IT

**The declared behaviour.** `PREREG_ASSEMBLY.md` §4.4 and `PACKET_ASSEMBLY.md`:
*"Zero below depth 2 by construction … day-0 and one-season-out rows are untouched."*

**The built behaviour.** Rows whose **only** unplayed season is the in-progress one are charged.

**THE MECHANISM, RE-VERIFIED ON A LOADED ENGINE RATHER THAN TAKEN ON REPORT:**

- `o41_absence_depth` returns `1.0 + _n` with `_n` starting at the in-progress season's fraction.
- `_fEy` (`:130`) returns `SEASON_FE` normally, but **`1.0`** for a row `_fe_p_one` marks out — a row
  on **`LTI_REGISTER.md`**, the engine's own long-term-injury register.
- `o41_r3_take` exempts only `if _cx < 2.0`.

So an ordinary row absent only in 2026 sits at depth `1 + SEASON_FE` and is **uncharged**; a row on
the LTI register sits at **exactly 2.0000** and is **charged** at F3's depth-2 cost.

**My own measurement, on the candidate's dial line:** of **116** rows whose only unplayed season is
2026, **4** reach depth ≥ 2 — **Mani Liddy, Noah Long, Jackson Archer, Jack Payne** — and **all four
have `fEy = 1.000` and `LTI_out = True`**. **Not one non-LTI row reaches the threshold.** The audit's
finding reproduces exactly.

**ONE CORRECTION TO THE AUDIT'S PROSE, AND IT DOES NOT CHANGE THE FINDING.** The audit states
`SEASON_FE = 0.58`; the live value read from `data/season_state.json::calendar_progress` is **0.92**,
so an ordinary row sits at **1.92**, not 1.58. The finding is unaffected — 1.92 is still below the
guard and 2.00 is still above it — and the correction is recorded rather than passed over.

---

## 2 · THE FIX — STRUCTURAL, NOT NUMERIC

**THE RULE:** a row is reachable by R3 only if its current absence run contains **at least one
COMPLETED unplayed season**. A row whose only unplayed season is the in-progress one is **never**
charged, **at any value of `fE`**.

**No new constant. No threshold moved. No dial.** The `_cx < 2.0` guard stays exactly as it is; a
second, structural condition is added beside it.

**Why structural rather than numeric.** Nudging the threshold (say to 2.01) would fix these four rows
by arithmetic accident and would silently re-break the moment `SEASON_FE`, the register, or the
season state changed. The property the packet actually promises is *"one-season-out rows are
untouched"*, and that is a statement about **completed seasons**, so the code should say that.

**THE EDIT:** a helper `o41_completed_absent(p, Y)` returns the count of **completed** (i.e.
`year < Y`) unplayed seasons inside the same current consecutive run `o41_absence_depth` walks. It
reuses that walk's own rules — a season with games > 0 breaks the run, the draft year floors it — so
the two objects cannot drift apart. `o41_r3_take` then gates on:

```
if _cx < 2.0 or o41_completed_absent(p, Y) < 1: return 0.0
```

**Nothing else in the R3 sizing law changes.**

---

## 3 · PREDICTIONS — THESE CAN BE WRONG

**P-F2-1.** Exactly the **4** rows named above stop being charged. **No other row's price moves.**
*(The audit says 3 of the 12 charged rows are affected; I measure 4 at depth ≥ 2, one of which may
already take 0. If the built count of moved rows is not 3 or 4, I have misunderstood the mechanism
and will say so.)*

**P-F2-2.** The board **rises** by the removed take — predicted **between +50 and +70 board points**
(the audit measured the three charged rows at −7, −15, −36 = 58).

**P-F2-3.** The R3 charged-row count falls from **12** to **8 or 9**.

**P-F2-4.** **Day-0 stays 89/89 bit-identical.** A gameless row has no completed *played* season, but
it has completed *unplayed* ones, so the new condition is satisfied for him and his depth logic is
untouched. **This is the prediction most worth being wrong about, and it is checked, not assumed.**

**P-F2-5.** No acceptance law moves: dial-off `374d4e44`, R `7f88f509`, burn 0, birthday 0,
continuity clean on every axis, class mark stays **1.0671** (the class window is 2005-2015 and these
rows are recent).

**P-F2-6.** The fractional-break variant moves by a similar small amount and its comparison stands.

---

## 4 · FALSIFIERS — EACH HALTS AND IS REPORTED

| id | fires if | consequence |
|---|---|---|
| **F2-A1** | dial-off does not reproduce `374d4e44` byte-exact | **VOID** |
| **F2-A2** | day-0 is not 89/89 bit-identical against the frozen reference | **HALT** |
| **F2-A3** | determinism ×2 differs | **HALT** |
| **F2-A4** | any row whose only unplayed season is in-progress is still charged | **the fix failed** |
| **F2-A5** | a row with ≥1 completed unplayed season stops being charged | **over-reach — HALT** |
| **F2-A6** | the class mark leaves [1.03, 1.14) | **HALT** |
| **F2-A7** | burn ≠ 0 or birthday ≠ 0 | **HALT** |

---

## 5 · WHAT THIS FIX DELIBERATELY DOES **NOT** DO

- **It does not exempt the LTI register.** Finding **F3** — that the engine's own `LTI_REGISTER.md`
  (43 rows, 21 of them not `injured=Y` in the owner's annotation) is never consulted by the two-channel
  exemption — is **disclosed, not wired.** Whether long-term-injured rows join the exemption is **an
  open owner question** and this seat will not answer it by editing code. After this fix I will
  **re-measure** how many LTI-listed rows R3 still charges and put that number in the packet.
- **It does not touch `_fEy` or the LTI register.** Both are consumed by many other objects; changing
  either to fix R3 would be a far larger blast radius than the defect.
- **It does not re-open the binary-vs-fractional break question** (v754). That is the owner's.
