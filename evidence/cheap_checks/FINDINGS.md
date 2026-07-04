# CHEAP CHECKS — establishment-P + PVC start-year

Read-only, report-only. No value-scale changes. 2026-07-04.

## STEP 0 — FETCH + ASSERT
- `git fetch --all --prune` — OK
- main = **389ac39** ✓ (`389ac397712e623f927259de930ce266bec51afd`)
- engine md5 = **c47cb43d** ✓ (`engine/rl_after/_merged_recover.py`)
- No mismatch → proceed.

---

## CHECK 1 — establishment-P: PRESENT but GATING INERT (feeds nothing on the board)

**Verdict: the machinery is PRESENT in code, but its gating is DEACTIVATED — it feeds no live value.**
The owner's belief ("removed") is effectively correct for the value scale; the code was
wired off, not deleted.

### The kill switch
- `engine/rl_after/rl_model.py:782` — `P_HOOK=None` with comment:
  `# cont.20: establishment-P gating DEACTIVATED (xP_establish deleted); v4 projection replaces it. (was: P_HOOK=P_estab)`
  This is the **last** assignment of `P_HOOK` (after the machinery block at line 729+), so it wins.
- `engine/rl_after/rl_model.py:730` — self-documenting:
  `# The consuming machinery (PROD_GATE + the min(decay,Pz) line in value()) was already here but inert with P_HOOK=None.`
- `engine/rl_after/rl_model.py:628` — `PROD_GATE='off'` (`cont.20: rigid establishment blend REMOVED`).

### Why it feeds nothing — traced through `value()`
- `rl_model.py:650-651` (0-game, in-window branch): `Pz = 1.0 if P_HOOK is None ...` → `unpl_eq * 1.0` → **no effect**.
- `rl_model.py:653`: `Pz = None if P_HOOK is None else P_HOOK(p)` → `Pz=None`.
- `rl_model.py:660`: `decay_eff = decay if Pz is None else min(decay, Pz)` → `Pz is None` → pedigree pedestal uses plain `decay`, **untouched**.
- `rl_model.py:664`: production-gating branch guarded by `if Pz is not None and PROD_GATE!='off'` → both false → **skipped**.

### The machinery that still exists (dead / diagnostic only)
- `pgrid.py` — the smoothed establishment surface; `rl_model.py:733` still runs `pgrid.build(...)`.
- `rl_model.py:770` — `def P_estab(p)` still defined (uses `pgrid.Praw × mat_mult`).
- `P_estab` is consumed **only** as a reported diagnostic column, NOT in pricing:
  - `engine/rl_after/compute.py:18` — emits `'P': round(P_estab(p),3) if not est(p) else 1.0` into an analysis panel.
  - `compute.py` is imported **only** by `engine/rl_after/verify_anchors.py:15` (a diagnostic), NOT by the board/panel path (`_merged_recover.py` → `ev`).
  - `engine/rl_after/rl_export.py:50` — the JS-parity bake hardcodes `'P':1.0` (FROZEN), so even the export carries no live establishment-P.

**Bottom line for CHECK 1:** establishment-P does NOT feed pricing, pedigree pedestal, or the
production floor on the live board. It is a present-but-inert relic (surface + function retained,
gating switched off at `rl_model.py:782`), surviving only as a printed `P` column in a diagnostic
panel.

---

## CHECK 2 — PVC spec: stated reason the primary window starts at 2006

Source: `docs/PVC_DERIVATION_SPEC_v1.md` (Fable-authored, branch `origin/claude/pvc-derivation-spec-17l4ly`).

### Exact window the spec defines (three-window design, §2b.3 survivorship table, line 150)
- **Primary fit = decided cohorts 2006–2018**
- **Extension = 2019–2022** — enter ONLY via censoring-adjusted projection (completion factors from decided cohorts).
- **2023+ = validation-only** (out-of-sample targets for Yr1/Yr2 predictions).

### Stated reason for the 2006 start (verbatim / tight quote)
From the survivorship-design row (line 150):
> "primary fit = **decided cohorts 2006–2018** (scoring rows begin 2005 [store]; **2003–2005 drafts are left-censored** — see era row; realised values stabilise at ≤2017/2018 [cont.27])"

From the era-effects row (line 151), reason (i) and its handling:
> "(i) 2003–2005: **scoring history starts 2005 → left-censored early careers** … (i) **exclude 2003–2005 from the primary window** (matches the book's **REFONLY-2003 precedent**)"

**Paraphrase:** The spec starts the primary window at 2006 because the store's per-season scoring
rows begin only in 2005, so the 2003–2005 draft cohorts have **left-censored early careers**
(their first one-to-three seasons are unobserved) and are excluded from the primary fit; this also
matches the existing "REFONLY-2003" book precedent.

### Context for the report (NOT acted on)
Owner's data starts 2005, so 2004 is the first fully-observable year-one cohort (2003 airtight).
The spec's stated basis for excluding 2004/2005 is the left-censoring of those cohorts' early
careers relative to a 2005 scoring floor — the reason to move the window to 2004 post-bake turns on
whether that left-censoring is material given the owner's read. **No change made to the spec.**
