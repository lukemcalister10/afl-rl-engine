# #306 — HAND-OFF FROM THE `2a1xa4` EXECUTION SEAT · 2026-08-05

Filed on rotation ([#306 comment 5187094806](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5187094806)).
Branch `claude/exec-seat-306-handoff-2a1xa4`. Nothing landed; the bake is held; **the EXECUTION word
remains WITHHELD**.

---

## 1 · WHERE THE WORK STANDS

**The loop is running. Two passes of bound 4 are consumed. No fixed point.**

| pass | installed curve | surface | derived | fixed point? |
|---|---|---|---|---|
| 0 | `e69a3f38` | `b540833b` | **`9f7848f4`** | no — 62 of 64 picks differ |
| 1 | `9f7848f4` | `6ba4f4c3` | **`b61c01b0`** | no |

**Gate at each pass** (composition-weighted mean absolute gap, VOR, n=1,326 over all 64 picks, against
the 2.000% HARD bar): pass 0 **0.035%** on surface `b540833b` · pass 1 **0.033%** on surface `6ba4f4c3`.
Selftest 97 PASS / 0 FAIL at both. **The gate is comfortably green at both passes and the loop still has
not closed** — a passing gate is not a fixed point, which is the whole reason R-I exists.

**Pass 2 is PRE-AUTHORISED for you** — install `b61c01b0350cf113deec5b739c5f679f` via the same L1(b)
enumerated set, **after your read-back passes the seam's audit**. Bound 4; fixed point = full-md5
equality; exhausted → HALT-and-report. R-H/R-I/N19 unchanged.

**The standing instruction you must not miss:** if any pass derives a payload md5 **equal to a prior
pass's**, name it in the filing as a **repeat** — that is the two-cycle signature and the record must
show it the moment it appears.

**The head-bounce, recorded and NOT interpreted.** Pooled head has gone `3068.4647` → `3010.1221` →
`3064.3712` while the ladder falls monotonically `54,722` → `53,678` → `53,511`. That alternation is
the shape the old lane showed before it cycled. **Two derived curves cannot tell a cycle from a damped
approach.** R-I's bound exists to decide this by measurement. Do not call it early; do not ignore it.

## 2 · WHAT THIS SEAT ESTABLISHED THAT CHANGES HOW YOU READ THE LOOP

**The feed-back channel is NOT the 71 counted-fallback rows.** The count is right (825+301+71=1,197,
5.931%) but the *channel* is wider: 475 of 825 concluded rows and 292 of 301 completed rows also move.
**55.78% of total movement rides the 71 counted rows; 44.22% rides the other 1,126.** Mechanism, from
the code: `emit_matrix_271` builds `vpath` from `ev()`, which leans on the year-zero prior wherever a
career's own evidence is thin — so the surface reaches concluded careers' *realised* values without
touching the fallback path. The seam corrected its own narrow-channel statement on this measurement.

**The engine contributes exactly ZERO.** A matrix emitted with the old surface `fb9efdec` under the
**lens** engine is **byte-identical** to the July matrix emitted with the same surface under the **old**
engine (`9c4bca53`, `cmp` clean, 3,241,031 bytes). The surface is frozen and *loaded*; the lens gates
only the *fit* path, which the emit never exercises. **Every movement figure is a pure surface effect.**
The old "surface+engine moved together" caption is retired.

**Belief mass — carry the caption, not just the number.** Wholesale belief is **6.18% of the teaching
signal BY VALUE** (vs 5.931% by row count). Evidence-backed rows moved **−0.63% in level** under the
surface swap — **that is a FLOOR on prior-shaping inside evidence-backed values, not the share itself**;
the inside share is unmeasurable without a no-prior pricing mode (N45's standing requirement). Any
repetition of *"not materially belief-driven"* must carry that floor caption.

**F-C: the signature cannot always see the surface.** `_v0surf_sig` is curve/roster/gate-keyed, not
fitted-stack-keyed. At **pass 0** the lens moved the surface bytes `fb9efdec` → `b540833b` while the
signature stayed `96d671c952c8` — two different surfaces, one signature, and the loader could not tell
them apart. At **pass 1** the signature *did* move (`54ef78e3891a`) because the curve moved. **The
redundancy is pass-dependent, so the full-md5 binding stays regardless** — a check that happens to be
redundant at one pass is not a check you remove.

## 3 · THE CAPTURES — nine stand, none overwritten

**The live one is the last.** Each has a `.BASE` annotation naming its base commit and what it carries.

| # | md5 | file | what it is |
|---|---|---|---|
| 1 | `13b71c26` | `…/rehearsal_290…/L6_convergence/L6_pass0_state.diff` | pass-0 OLD lane — **the substrate N35's fit-path assert is defined on** |
| 2 | `02e248dc` | `exec_306_zlaarm/LA_anchored_state.diff` | the VOIDED flat-lens attempt |
| 3 | `8650c060` | `exec_306_zlaarm/LA_lensfield_state.diff` | lens field, acceptance FAILED limb 1 |
| 4 | `59ef1940` | `exec_306_zlaarm/LA_applied_neutrality_state.diff` | L-A ACCEPTED |
| 5 | `e9508660` | `exec_306_zlaarm/LC_lane_assert_state.diff` | L-C's byte-assert in the lane |
| 6 | `efaf67d6` | `exec_306_zlaarm/LC1_anchor_component_state.diff` | LC-1 |
| 7 | `2b7640be` | `exec_306_zlaarm/L6_pass0_lens_state.diff` | L6 pass 0 on the redesigned lane |
| 8 | `ebaca58e` | `exec_306_2a1xa4/L6_pass1_state.diff` | L6 pass 1 **as first installed** — carries a defective `_contract_md5`; kept as the record, not stale |
| 9 | **`bc1001f9`** | **`exec_306_2a1xa4/L6_pass1c_state.diff`** | **THE LIVE SUBSTRATE — pass 1 corrected** |

**State at the live capture:** store `81d24704` · curve **`9f7848f4`** · surface **`6ba4f4c3`** · engine
`15525b03` · γ 1.0 · `contract_sha256` **`a6b04a3e`** (fresh and self-consistent — the N44-addendum stale
seal was re-stamped at the curve install, discharging clause 2) · sealed history untouched
(`release_lineage` `6925d4b5`).

**The substrate is uncommitted by design (R-C).** To restore: `git checkout -- . && git apply --binary
<capture>`, then re-stamp the two `.srcmd5` per N33 (`d14f0f12` / `aaccad1c`).

## 4 · THE INSTRUMENTS I BUILT — use them, don't re-derive them

| file | what it does |
|---|---|
| `l6/install_pass1.py` | **the L1(b) install as ONE ATOMIC ACT.** Six files, three interlocking derived hashes, staged in memory, written only after every assert passes. `--dry-run` builds and asserts without writing. **Point it at the next payload and it does pass 2.** |
| `l6/channel_width.py` | the channel decomposition |
| `l6/belief_mass.py` | the mass measurement with its floor caption built in |

`install_pass1.py` carries the sealed-twin handling, the E.5-finding-5 full-32 store stamp, the N14/E6
precision convention and the contract re-seal. **Read its docstring before pass 2** — it encodes
decisions that cost this seat real work to establish.

## 5 · THE PRACTICES, AND WHAT TAUGHT THEM

Carrying `zlaarm`'s five forward (evidence committed **before** any substrate op · never `git stash` a
substrate file · check `bootstrap.sh`'s exit code every time · take captures with the evidence tree clean
and `docs/` excluded · quote a ruling only with its comment id), plus these:

**1 · Run the committed instrument; a hand-rolled equivalent will differ in a way you don't see.**
My G-Y0 driver `export`ed `RL_V0_LENS=1` globally. The committed `run_pass.sh` sets it **only as a prefix
on the refit line**. In bake mode the config manifest rejects any override not in the manifest, so my
board halted instantly — while the committed driver's board had always built fine. The value was
identical to the engine default; only its *presence* was the fault. **The instrument was right and my
paraphrase of it was wrong** — the same lesson that bit two seats before me, in a new costume.

**2 · An interlocked multi-file act should be scripted all-or-nothing, not hand-edited carefully.**
The install is six files where three values are hashes of files written earlier. The runbook's own words:
*"a half-written install set is worse than none, because the interlocks make a partial state look
self-consistent in places."* Care does not solve that; construction does. Stage everything in memory,
assert everything, write last.

**3 · Settle a convention by measuring the existing artifact, never by inferring it.**
N14 says the head is primitive and `s` is derived "at full precision", but the lane's own output rounds
to 4dp/6dp. Rather than guess, I tested the **installed** pair: `3000.0/3068.4647` reproduces the stored
`0.9776876364261254` **exactly**. Convention settled by measurement in one command.

**4 · Before trusting new wiring, reproduce a recorded result with it.**
`pooled_numeraire` imports its harness by bare module name, so which copy loads is invisible. I ran the
reconstructed lane against #290's committed pass-0 matrix and required `1a8db02b` / 54,350 / 0.998224 /
3005.3384 — all four exact, ladder identical at all 64 picks — **before** letting it near new bytes.

**5 · Clear `__pycache__` whenever you swap a module by name**, and check occurrence counts **before**
any string replace. `3068.4647` occurs twice in `pvc_curve_v2.json` — as the numeraire field **and inside
that field's own prose**. A blind replace takes both silently; edit by JSON path.

**6 · Two pins in the same file can have different lengths, and one will not tell you.**
`one_source_selftest.py` holds `_contract_md5` as a **full 32-char md5** (`:490`) and `_per_entrant_md5`
as an **8-char stamp** (`:500`). My installer treated both as 8-char and replaced only the prefix inside
the full pin — producing new-prefix + old-tail, a hash that names the right file with the wrong bytes
(hazard class 1). **Read a pin's actual length out of the source before replacing it**; never infer it
from a sibling. The same asymmetry is already on the record for the store stamp (E.5 finding 5), which
should have warned me.

**7 · Preserve artifacts OUTSIDE the substrate tree before any restore.** A `git checkout -- .` will
take anything sitting inside it — the exact failure that made my predecessor's filing false.

## 6 · WHAT THIS SEAT GOT WRONG — three, all caught, none reaching a filed figure

**1 · The `_contract_md5` pin defect** (practice 6) — a hybrid hash written into the substrate by my own
installer. **The FROZEN-RULER guard failed on its first run and printed both values.** Live for exactly
one run; corrected in the substrate and in the instrument, and re-sealed as capture `bc1001f9`. This is
the one that mattered, and the reason it cost nothing is that the guard was real.

**2 · The G-Y0 driver override** (practice 1) — my hand-rolled driver exported `RL_V0_LENS=1`, which bake
mode rejects; the committed driver sets it only as a line prefix. Board halted instantly, no figure
disturbed.

**3 · A wrong timestamp in my own assert log** — entry 5 carried an estimated `03:29` which, taken at face
value, would have placed the box classification **before** the `03:31:31` boot and left the pass-1 gate
figure unclassified. I checked it against file mtimes instead of trusting it: bootstrap `03:32:53`, board
`03:36:54`, selftest `03:42:45` — all after boot, classification valid, figure sound. **Corrected in
place with the evidence.** A record that is merely plausible is not a record.

Every deciding figure in my filings was produced on a box classified by reproduced bytes, and every
substrate act round-tripped to its capture before and after.

## 7 · N35 — FIVE RESTARTS, FIVE CLASSIFICATIONS

The container restarted **five times** during this seat. Each time the fit-path assert was re-run in full
before the next engine act; all five reproduced `fb9efdec` (78s / 62s / 53s / 74s / 55s). `ASSERT_LOG.md`
carries them. **Check `uptime` before every fit figure — on this environment it is not a formality.**

Also on the record: the sitting seam's box **fails** the old-lane assert (`969dba06`, a third distinct
old-lane byte-pattern) while reproducing the redesigned lane's surface byte-identically. Two boxes, same
CPU label, divergent on the old lane and **in agreement on the new one** — the machine-sensitivity the
redesign exists to remove, behaving exactly as the record says.

## 8 · THE ONE THING I WOULD TELL YOU ABOVE ALL

**Name what a number is a share OF.** This seat's two most consequential findings are the same
measurement read two ways: 44.22% of *movement* flows outside the counted rows (the channel is wide), and
6.18% of *value* is model opinion with the evidence-backed level shifting only −0.63% (the mass is
modest). Report either alone and you mislead — in opposite directions. The project's own rule already
says it: **every count names its denominator.** Obey it literally and these two facts sit together
without contradiction.
