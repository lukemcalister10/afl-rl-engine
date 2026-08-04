## EXECUTION SEAT READ-BACK — #306 · fresh cold seat `zlaarm` · 2026-08-04 · **HOLDING for the seam's go**

Opened bare on the owner's paste under §10 + Addendum 1 §C/§D + C3′. Opening acts (1)–(4) are complete in
order. Designated branch `claude/exec-seat-306-afl-rl-zlaarm`. **Nothing has landed, no ref has moved, no
engine act has run.** Every figure below was produced by my own commands in this session; none is quoted
from prose.

---

## 1 · THE DECIDING FIGURES, RE-RUN — byte-identical, worktree clean

Detached worktree at the carrier tip `7e9d7f9`, both committed scripts run, outputs md5'd before and after:

```
BEFORE            4a1280278433a63d00e33d6f8f30e431  hysteresis_magnitude.json
                  a142b180017462dae1fcf7fe695f9be6  tail_gap_by_band.json
AFTER  (re-run)   4a1280278433a63d00e33d6f8f30e431  hysteresis_magnitude.json
                  a142b180017462dae1fcf7fe695f9be6  tail_gap_by_band.json
git status --porcelain → empty
```

**Both regenerate byte-identical.** The reported tables reproduce exactly:

| | measured here |
|---|---|
| hysteresis, same-curve pair (`ca662051`, pass 2 vs 4) | **60 of 2,646 moved (2.27%)** · max abs **0.1** · max rel **1.845e-04** · mean signed −0.0023 |
| different-curve control (pass 1 vs 3) | 130 of 2,646 (4.91%) · max rel 4.490e-04 |
| tail gap, pass 2 / 4 (`ca662051`) | overall **+8.399%** · 1–10 **−5.01%** · 11–20 −0.31% · 21–30 +3.30% · 31–45 +19.17% · **46–64 +64.25%** |
| tail gap, pass 3 (`b0bda532`) | overall +10.577% · 46–64 **+67.35%** |
| cycle amplitude (pass 3 − pass 2, pp) | 1–10 +1.98 · 11–20 +2.05 · 21–30 +2.09 · 31–45 +2.24 · **46–64 +3.09** |
| repeat control (pass 4 − pass 2, pp) | −0.0002 · −0.0014 · −0.0002 · +0.0000 · −0.0003 |

**§2's conclusion holds on my own run:** the path memory is ~three orders of magnitude below the cycle's
~2 pp swing. Determinism is necessary, not sufficient; the tail is the limb that moves the number. I carry
the population caveat: these are **FIT-population** figures (`teaches_curve`, picks 1–64, 1,444 rows), **not
the G-Y0 gate's ~1,326-row set**, and I will not quote them as a gated G-Y0.

**N32 re-proved live, not read.** From the halt substrate's `engine/rl_after/pvc_curve_v2.json`
(file md5 `d57032b0…`), 64 entries, keys stored as **strings**:

```
STRING-keyed payload md5 → ca662051   (matches the release stamp)
INT-keyed    payload md5 → b6a7ec87   (a plausible, wrong identity)
```

The key-type fact reproduces. **The named helper is still owed and prose has not discharged it.**

## 2 · LIVE STATE — verified by my own commands

| | measured |
|---|---|
| main | `b554d0e` — the v558 pen |
| **live carrier** `claude/exec-seat-290-handoff-d7bnaa` | **`7e9d7f9`** — the Addendum 1 tip, unmoved |
| frozen ancestors | `8e8c15b` j0kwl0 · `abf8f4c` fubolo · `3cccb9d` fp78jm — **intact** |
| HOLD branches | `9914c4d` 4ql38z · `592c7a2` g4edkc — **intact** |
| open issues | 306 292 290 283 279 276 275 270 269 146 139 = **11**, as expected |
| open PRs | **none** |
| gating workflows @ `b554d0e` | Live Scoring Updater **success** · Final Integration **success** · FV Provenance **success** · **CI Guards IN FLIGHT** (started 04:26:57Z, ~12 min in against a recorded ~17 min) — stated as in-flight, not predicted |
| halt capture | `L6_HALT_state.diff` md5 **`137c6d2c95c094b6f81961a991613e71`**, base `3ffbc1f`, **19 sections** |
| capture applies at the tip? | **`git apply --check --3way` at `7e9d7f9` → all 19 clean.** Re-verified, not assumed |

## 3 · A CATCH THE SEAM SHOULD PEN — `CURRENT_STATE` v50's reconstruction triple names the wrong surface

The queue line reads: *"reconstruct (apply `137c6d2c`, verify **`fb9efdec`**/`f305fe53`/`ade79790` …)"*.

I applied the capture in a throwaway worktree and hashed the artifacts:

```
after applying 137c6d2c:
  data/v0surf.pkl                    31e7f00b876081b46ed1f3b4169e667b     <-- NOT fb9efdec
  engine/rl_after/peak_model_v4.pkl  f305fe5330222f4fa14d3654a0e91ef7     OK
  engine/rl_after/pvc_snapshot.json  ade79790efc8ad4585c2c6800a935eaa     OK
  ui/release_pick_curve.json         → pick_curve_curve_md5 = ca662051
```

**`fb9efdec` is the PASS-0 surface. The halt capture does not install it and cannot.** The capture's own
BASE annotation (*"v0surf 31e7f00b"*) and the halt filing's pass-4 row both say `31e7f00b`; the register
governs and `CURRENT_STATE` is the derived view, so the derived view is wrong here. **Correct triple:
`31e7f00b` / `f305fe53` / `ade79790`.**

This is hazard class 1 in the shape the record names it — a true hash of the wrong artifact — and it is
load-bearing: a seat following the line literally hits a verify that **cannot** pass, and the tempting next
move is to "fix" the substrate to match a number that was never its. I am not editing anything; the pen is
the seam's. **I will reconstruct against `31e7f00b` and say so in the commit.** (The worktree was restored
clean; nothing was written.)

## 4 · C3′ — THE RE-ENTRY STATEMENT

### The installed curve I re-enter from: **`e69a3f38`**

Named as a choice, with the reason, per C3′. Three grounds:

1. **`ca662051` and `b0bda532` are the two limbs of the period-2 cycle** — outputs of the composition
   that failed, not independent measurements of what picks delivered. Re-entering on a limb imports the
   old lane's path into the new lane's **anchor**, which is precisely the input N29 makes load-bearing.
   The halt filing refused to pick a limb because picking one is a ruling; re-entering on one is the same
   act wearing a bookkeeping costume.
2. **`e69a3f38` is the curve of record** — the #279 ruled control fit, installed at both the pass-0 state
   and the L3–L5 record, and the only candidate in Addendum 1 §D's table that is not a product of L6's
   iteration.
3. Under N29 the curve is the skeleton the surface cannot leave. A skeleton taken from the cycle would
   make the anchor an artefact of the defect the job exists to remove.

**The cost, stated rather than hidden.** The substrate is held at the halt (`137c6d2c`, curve `ca662051`),
so re-entering at `e69a3f38` is **a deliberate curve install**, not a free choice — `ui/release_pick_curve.json`
and `pvc_curve_v2.json` edited **by JSON path** under the §4 sealed-twin discipline (`3068.4647` occurs twice
in the latter, as a field and inside that field's own prose), payload re-derived by N32's **string-keyed**
recipe, pre-assert HALTing on mismatch.

**The alternative, so the seam is choosing and not ratifying:** re-enter on **`ca662051`**, the substrate
exactly as held, zero install act, one hazard surface fewer. **I recommend `e69a3f38`** — the install cost is
one bounded, asserted act; a cycle-limb anchor is a defect baked into the design's first input. **This is the
seam's to confirm and I hold it.**

### The starting surfaces for the first fit: **`84fb0cde`** and **`31e7f00b`** — byte-agreement REQUIRED

Both verified retrievable as held committed bytes on the carrier:

| | md5 | held at | why it qualifies as materially different |
|---|---|---|---|
| **S1** | `84fb0cde29f36c1a91d440e63b753c3c` | `…/v0surf_frozen_2026-07-31/v0surf.pkl` | the L3–L5 record surface, pre-catch-up — **G-Y0 13.919%** |
| **S2** | `31e7f00b876081b46ed1f3b4169e667b` | `…/L6_convergence/pass4_surface/v0surf.pkl` | the halt substrate's own surface — **G-Y0 8.842%** |

These are the furthest-apart surfaces the record supplies — 5.1 points of G-Y0 between them — which is
L-B's own *"a curve as far from it as the record supplies"* limb. **Outputs compared on FULL md5, never the
signature key (N22). Disagreement = L-B has failed and the lane is not ready → HALT, never proceed.**

**Offered if the seam wants L-B's full three at the first fit** (one extra fit, ~62–72s on the old lane's
cost, UNMEASURED on the new one): **S3 = `fb9efdec`** (`…/pass0_surface/v0surf.pkl`) — the surface fitted
*at* `e69a3f38`, i.e. L-B's *"the state after fitting curve A"*; and L-B's *"fresh checkout, no surface
present"* state, which is also available. All five per-pass surfaces are held as bytes and none was
overwritten.

## 5 · THIS BOX'S COMPUTE-PATH POSTURE — **the assert is the gate, the CPU string is not**

Observed, and offered as observation only: Intel Xeon @ 2.10GHz · 4 cores · x86_64 · Linux 6.18.5 ·
python3 3.11.15 base (numpy absent from the base interpreter; engine acts run behind the 5-pin venv).

**None of that discharges anything, and I will not report it as if it did.** The gate is the **pre-L4 control
rebuild reproducing board `92e397bd` byte-exact** — an assert on **output bytes**, which is the whole of
L-C's holding: *the pin was never the guard.* The OpenBLAS `DYNAMIC_ARCH` precedent is exactly a case where
the byte-pin passed on both hosts while the dispatch tier differed, so a matching CPU string would prove
nothing about this box. Measured cost on the record: **139s** at L6 pass 0, **116s** at the halt filing.

**It has not run, because it is an engine act and I am holding.** It runs at reconstruction — after the
merge-forward and the capture apply, before any fit. **FAIL → HALT to the seam. No fit runs on an
uncorroborated box.** The double-fit byte-compare (R-H.1b) is the second pre-loop gate and is likewise
unrun; a mismatch there is a HALT filing, not a retry.

## 6 · THE MERGE-FORWARD, MEASURED BEFORE THE ACT (Addendum 1 §C)

Probed with `git merge-tree` — **no working tree touched, no ref moved**:

```
merge-base            98fe397   (register v555 / CURRENT_STATE v47)
commits to merge      44
file span             177
CONFLICTS             0        (merge-tree exit 0, tree 3d3db2a)
```

Noted for the record: the carrier diverged at v555, so main's v556/v557/v558 pens are **not** ancestors of
it. The merge is a **TRUE MERGE** on the `bf6596b` pattern — never a rebase — and these four figures go in
the commit message. The two `.srcmd5` regenerate per **N33** via `single_source.stamp_tier2_frozen`, a pure
function of the artifact bytes, expecting `d14f0f12` / `aaccad1c` — **no peak rebuild**, because rebuilding
a model on a travelling substrate is a modelling act. (The pass-0 capture's BASE annotation still carries
the superseded *"regenerate from the peak build (31s)"* phrasing; I am following N33, not it.)

## 7 · WHAT I HOLD AND WHAT I AM NOT DOING

I read the governing set in full and take it as binding: the body · the pre-fire audit (5174229825) · the
ANCHOR STEER (5174404784) · Addendum 1 (5174450071) · the seam confirmation with **Acceptance 7** and
**C3′** (5174497326) · the FIRE word (5174594459). L-A anchors and **redistributes, never inflates** — the
measured +8.4% aggregate and +64% tail are what Acceptance 7 is born failing against, and no post-hoc clamp
is a construction. Acceptance 4 binds: **I will state no expected G-Y0** — the number is re-measured or it
is not stated. §7's NOT-list stands; L1–L5 are closed; no gate is re-spec'd, including the definition of
converged. A second non-convergence is a HALT-and-report under R-I, not a licence to pick a limb.

**Nothing lands.** The carrier is never rewritten, the frozen ancestors and HOLD branches stay untouched,
main is untouched, and **the EXECUTION word remains WITHHELD** — it is not this job's to earn.

**HOLDING for the seam's go via the owner's paste.** Two things travel with this read-back for the seam's
word: the **C3′ curve choice** (`e69a3f38`, with `ca662051` as the tabled alternative), and the
**`CURRENT_STATE` verify-triple correction** (`31e7f00b`, not `fb9efdec`).

---
_Generated by [Claude Code](https://claude.ai/code)_
