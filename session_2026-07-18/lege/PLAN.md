# LEG E — PROJECTION LAW + POSTURES — PLAN (first committed artifact)

- **Base:** `a90052add8570c014626196cc2e3e13eece02548` (five-migration BUILD B EXIT), branch
  `claude/lege-projection-law-postures-63u283`. Governance docs live on MAIN (a separate lineage that
  does NOT carry the engine); the engine candidate is this base. Both true at once, never joined.
- **Entry proof:** `ENTRY_PROOF.txt` — balanced board **`06d8af60`** (RL_PVC2=1) and kill-switch
  **`9829d01a`** (RL_PVC2=0) both reproduced BYTE-EXACT this session; store `968de0c7` / curve
  `56dd7a7b`(payload `89c14729`) / engine `fdc54e24` all as pinned. No HALT condition.
- **Feed:** MEMO_LEGE v1.0 (construction of record; wins over the directive paraphrase) · SPEC v1.4
  §3+§6.2 · acceptance_v1_21.json (`laws[LENS-PROJECTION]`, `leg_d_placeholders.posture_2027_discounts`)
  · R103.3 · R104.4/.5 · R105.4.

---

## 0 — MEASUREMENT DISCIPLINE: THE D5 DIAL FAMILY, EXACT SEMANTICS (read from `a90052a` code, stated BEFORE any profile renders — memo §3)

Source line, verbatim (`engine/rl_after/rl_model.py:414`):

    LENS={'now':0.34,'bal':(0.14 if os.environ.get('RL_DIAL14','1')!='0' else 0.15),'fut':0.05}

**What the dial IS.** Each `LENS[key]` is a **per-annum discount rate `d`**, consumed at two sites only:
`proj_from_peak` (`:442`, `d=LENS[lens]`) and `prod_floor` (`:473`, `d=LENS[lens]`). Both weight a
future-year production stream geometrically: **year-k contribution ×`1/(1+d)**k`**. There is no
horizon-shift in the dial itself — it re-weights the SAME projected stream.

**Which horizon each key weights** (larger `d` ⇒ future discounted MORE ⇒ present/near-term weighted more):
- `now` = 0.34 — steep discount; near-season production dominates. (present-weighted)
- `bal` = 0.14 — the canonical owner-ruled dial ("14 for now"; gate `RL_DIAL14` default ON, `=0`⇒0.15⇒the
  pre-v2.9 base). **This is the ONLY dial the shipped balanced board exercises.**
- `fut` = 0.05 — shallow discount; far-future years weighted almost fully. (future-weighted)

**Critical fact about the interim lens (why balanced is byte-exact under this build).** In `value()`
(`:819`) the production terms are **hard-anchored at balanced**: `player_raw(p,'bal')` (`:829`) and
`prod_floor(p,'bal')` (`:841`). The only place the display `lens` argument acts is the FINAL multiplier
`lens_tilt(p,lens)` (`:849`) — a bounded ±30 % phase tilt (`LTILT=0.30`, `:415-419`) that returns **1.0
for `lens=='bal'`**. So the `now`/`fut` discount rates (0.34 / 0.05) are DORMANT in the value path;
the only cross-age view the base ships is `lens_tilt`, which credits **no projected production** — it is
the **interim no-improvement-floor lens** (`laws[LENS-PROJECTION]`: *"interim lens = no-improvement
floor, cross-age trades NOT read off it"*).

**Consequence for the build.** Two invariance levers fall out and are proven, not assumed:
1. Setting a posture's production discount to `bal`(=0.14) reproduces the balanced production term exactly.
2. Deleting `lens_tilt` cannot move the balanced board — it already returns 1.0 there.

## 0b — THE FORWARD-PROJECTION MACHINERY ALREADY EXISTS (the +1/+2 lens is the forward twin of the back-boards)

`rl_model.py` carries an `AGE_REF`/`BASE_REF` offset seam (`:124-125`): `AGE_REF` advances the age clock,
`BASE_REF` anchors demonstrated form + scoring truncation; `offset = AGE_REF-BASE_REF` drives Phase-2
development projection through **`_dev_advance`** (`:360`, rolls demonstrated form along the dev curve).
The backward boards `_vM1/_vM2` are already built by **`_backval`** (`:1057`) — set `BASE_REF=AGE_REF=Y`,
`proj_value(_trunc_p(p,Y),0)`. **`AGE_REF=BASE_REF=2026` reproduces shipped values byte-for-byte.**
The +1/+2 lens is the FORWARD analog: `AGE_REF=2026+k`, `BASE_REF=2026` (demonstrated form — incl. LTI
truncation — fixed at true-now), `proj_value(p,k)`. **k=0 ⇒ AGE_REF=BASE_REF=2026 ⇒ byte-exact.**

---

## 1 — SEALED POSTURE PRESETS (memo §6.2 — SEAL FIRST, recorded here BEFORE any non-balanced render)

Preset vectors: **`session_2026-07-18/lege/posture_presets_v1.json`**, **md5 `c2e17c49`** (full
`c2e17c4959ee7eeb2de0d04c9de7d077`), seal date **2026-07-18**.

| posture   | prod discount `d` | 2027-pick discount | ruled?  | note                                             |
|-----------|-------------------|--------------------|---------|--------------------------------------------------|
| balanced  | 0.14              | 0.10               | OWNER   | canonical = `LENS['bal']`; board `06d8af60`; never tuned |
| contender | 0.18 (strawman)   | 0.15               | proposed| sketch 0.14→0.18–0.20 (future discount UP)        |
| rebuilder | 0.10 (strawman)   | 0.05               | proposed| sketch 0.14→~0.10 (future discount DOWN)          |

The **2027-pick discounts {0.10 · 0.15 · 0.05} are BINDING** (acceptance
`leg_d_placeholders.posture_2027_discounts`, R104.5 + audit #6) — NOT owner-tunable. The `prod_discount_d`
strawmen ARE tunable; the owner ratifies them at the movers report. Nothing here rules.

## 2 — THE PROJECTION LAW (memo §2 · R103.3)

`+k` lens = the SAME un-compressed valuation map (`value()`) evaluated at the projected evidence state:
age+k, expected development projected through `_dev_advance` (the map's own cohort/growth curve — the
Reid constraint: **no separate young multiplier, no lens-only growth term**), demonstrated form + games
(incl. **LTI truncation — Rozee's 2026 stays his real 2 games**) held at true-now via `BASE_REF=2026`.
L-SMOOTH (continuous in age/evidence), L-SYMMETRY (same bar up and down), weight-don't-gate (R105.4) bind
inside the lens exactly as outside — the offset seam changes weights, never gates. **Invariant: k=0 ⇒
`06d8af60` byte-exact.**

## 3 — POSTURES (memo §3) — new VALUES over the existing dial, not new code paths

A posture re-parameterizes the production discount `d` (balanced 0.14 unchanged; contender 0.18;
rebuilder 0.10). Implemented by threading the posture's `d` into `player_raw`/`prod_floor` in place of
the hard-anchored `'bal'`, so balanced is byte-exact and contender/rebuilder re-price the SAME streams.
Balanced is the ONLY board that gates/bakes/seals (R104.4); postures are un-baked display.

## 4 — COMPOSITION LAW (memo §4) — one discount per axis

A 2027 pick under a posture = (live Leg-D curve over its band, lens-weighted like every future stream) ×
(1 − posture 2027-discount) applied **ONCE** as the final step. The lens `fut` dial must not touch a pick
asset twice. **Committed unit test** (`tests/test_composition_single_discount.py`) proves exactly one
application per posture on a synthetic pick.

## 5 — INJURY × POSTURE (memo §5) — default construction only

Graded amplification for free: the existing B2/RL_AVAIL current-season haircut composes with a
contender's higher near-term weight automatically — no new term. **Rozee** (out 2026, out_until_2027,
A3 standing-fail scored-never-skipped) is the mandatory named LTI row in the movers report; magnitude is
an [OWNER] ruling there, not a lens weight.

## 6 — RETIREMENT

Delete `lens_tilt` (the interim no-improvement-floor lens) — **deleted, not disabled** — with an OBITUARY.
Re-enable the UI lens toggle on this landing (SPEC §3).

## 7 — EXIT PROOFS

k=0 lens ⇒ balanced board `06d8af60` byte-exact · balanced board unchanged by every posture render ·
L-SMOOTH horizon sweep (no cliffs) committed · store `968de0c7` untouched · single-discount unit test ·
frozen suite (S4, `one_source_selftest.py`) · SSI guards · gates snapshot invariant under v-parity ·
movers report (top-20 risers/fallers per lens vs balanced + Rozee) · candidate PR.

## FENCE (derived — the 322 law)

**IN:** the lens/dial/posture sites in `engine/rl_after/rl_model.py`; the export forward/posture columns
in `engine/rl_after/rl_export.py`; the UI lens toggle site; the session dir `session_2026-07-18/lege/`.
**HARD-OUT:** the store `rl_model_data.json` · the curve `pvc_curve_v2.json` · the balanced-board pricing
path (any diff that moves `06d8af60` at k=0 is a build defect, full stop) · `docs/` · SEASON_PROG. HALT
on any job requiring a HARD-OUT file.
