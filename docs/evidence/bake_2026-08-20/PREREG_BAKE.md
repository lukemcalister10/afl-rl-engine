# PREREG — THE BAKE (register v780)

**PUSHED BEFORE ANY ENGINE, CONFIG, OR SIDECAR EDIT.** This is falsifier F6 of the order and it is
the first commit of this seat. Everything below is written while the tree is still byte-identical to
`origin/land/order-29` at `0ec4286`.

> **THIS PREPARES THE LANDING; IT IS NOT THE LANDING.** Nothing merges to main. Nothing is tagged or
> promoted. PR #510 stays held. The live board `88ce647f` is untouched. **NOT ADOPTED. OWNER WORD
> PENDING.** The owner's word is the gate.

---

## 0. WHAT THIS SEAT WAS ORDERED TO DO

Make the candidate's dial stack the **shipped default** behind **declared kill-switches**, kill the
surface-loader footgun **at the root**, regenerate the **stale sidecar**, and **re-seal the book** on
the candidate line. Four edits, seven falsifiers, one acceptance table.

The tree, verified raw before a line was written:

| pin | value | source |
|---|---|---|
| board (candidate) | `a05fe951f78482c70520480e184c80ec` | `data/expected_boot.json` `board` |
| engine head | `5f434b9592ad8adb7dcd534da49df3c7` | `engine/rl_after/_merged_recover.py` |
| store | `cb38ef1171dcf20aae66ebf12682be0d` | `engine/rl_after/rl_model_data.json` |
| config | `eed19a75f775aeaf…` | `data/model_config.json` `config_sha256` |
| v0surf (in-repo, pinned) | `5dd34ca82735f5c8f021b1c7320df8f8` | `data/v0surf.pkl` |
| v0surf (out-of-repo shadow) | `fbc5b39387b2b135284a2e157f46c810` | `/home/claude/v0surf.pkl` — **NOT TOUCHED** |

**CONTROL, RUN BEFORE ANY EDIT** (`CONTROL_PREFLIP_out.txt`): `build_D7B.sh ONLY=cand` on this
worktree produced `a05fe951` byte-exact. The harness reproduces the candidate on the pre-flip tree.
Every post-flip number below is measured against that control, not against a remembered one.

---

## 1. THE DIAL LIST — READ FROM THE SCRIPT, NOT FROM THE BRIEF

The order says *trust the script*. `docs/evidence/parity_2026-08-19/build_D7B.sh` defines the
candidate arm as `env $CLEAR $KLINE $S RL_O42=1 RL_O43=1`, i.e. **three** groups, not one:

```
KLINE = RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1
        RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08
BASE  = RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
        RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
S     = BASE + RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7
CAND  = KLINE + S + RL_O42=1 RL_O43=1        ← 29 assignments, not 18
```

**The brief named 18. The script carries 29.** The discrepancy is real and it is resolved by reading
the engine, not by picking a number:

`rl_model.py:1089` `_O37 = RL_O37 or RL_O38A or RL_O38B1 or RL_O38B2`, then `:1092` `_O36 = RL_O36 or
_O37`, then `_merged_recover.py:758` `_O35 = _O35 or _O36`, `:759` `_O32 = RL_O32 or _O34 or _O35`,
`:761` `_O31 = RL_O31 or _O32`. **`RL_O37` implies the entire KLINE stack.** And the four KLINE
*values* are already written into the engine as `_O37`-conditional defaults —
`O36_LAM_S1 = '0.40' if _O37 else '0.25'` (`rl_model.py:1103`), `O36_KAPPA '0.20' if _O37 else '0.24'`,
`O36_GAMMA '8.0' if _O37 else '11.0'`, `O36_ETA '0.50' if _O37 else '0.41'` (`_merged_recover.py:3794-3796`)
— while `RL_O36_GAMMA_D=14.0`, `RL_O36_LAMBDA=1.08`, `RL_O36_TALL=1`, `RL_O36_FLOORFIX=1` are already
the unconditional code defaults.

**PREDICTION, PREREGISTERED AND FALSIFIABLE:** the 11 KLINE assignments are *redundant restatements*
of what `RL_O37=1` already implies, so flipping the **18** dials below — and only those 18 — makes a
BARE build reproduce `a05fe951`. **If the bare build is not byte-exact, this prediction is WRONG,
F1 has FIRED, and I report it in these words rather than adding KLINE dials until the number matches.**
Chasing the identity by adding dials post hoc would be fitting the flip to the answer.

### 1.1 THE FLIP TABLE — every dial, exact current default, new default, kill-switch

Kill-switch = **the exact string that restores the old behaviour**. `''` means *set the variable to
the empty string*, which the engine reads identically to unset (`os.environ.get(X,'')`).

| # | dial | site | current default | **new default** | **kill-switch (off-value)** |
|---|---|---|---|---|---|
| 1 | `RL_O37` | `rl_model.py:1089` | `'0'` | `'1'` | `RL_O37=0` (+ #2,#3 — see §1.2) |
| 2 | `RL_O38A` | `_merged_recover.py:473` | `'0'` | `'1'` | `RL_O38A=0` |
| 3 | `RL_O38B1` | `_merged_recover.py:474` | `'0'` | `'1'` | `RL_O38B1=0` |
| 4 | `RL_O39_BETASAT` | `_merged_recover.py:493` | `''` | `'0.105'` | `RL_O39_BETASAT=` |
| 5 | `RL_O40_CAPFORM` | `_merged_recover.py:523` | `''` | `'smooth'` | `RL_O40_CAPFORM=` (+ #6) |
| 6 | `RL_O40_CAPPCT` | `_merged_recover.py:524` | `''` | `'15'` | `RL_O40_CAPPCT=` |
| 7 | `RL_O40_RECW` | `_merged_recover.py:522` | `''` | `'0.47'` | `RL_O40_RECW=` |
| 8 | `RL_O40_PGMAT` | `_merged_recover.py:526` | `'0'` | `'1'` | `RL_O40_PGMAT=0` |
| 9 | `RL_O41_SDOFF` | `_merged_recover.py:564` | `''` | `'2.98'` | `RL_O41_SDOFF=` |
| 10 | `RL_O41_CREDIT` | `_merged_recover.py:565` | `'0'` | `'1'` | `RL_O41_CREDIT=0` |
| 11 | `RL_O41_RESET` | `_merged_recover.py:578` | `'0'` | `'1'` | `RL_O41_RESET=0` |
| 12 | `RL_O41_INJ` | `_merged_recover.py:579` | `'0'` | `'1'` | `RL_O41_INJ=0` |
| 13 | `RL_O41_R3` | `_merged_recover.py:580` | `'0'` | `'1'` | `RL_O41_R3=0` (+ #15) |
| 14 | `RL_O41_RAMP` | `_merged_recover.py:592` | `'0'` | `'1'` | `RL_O41_RAMP=0` |
| 15 | `RL_O41_BREAK` | `_merged_recover.py:608` | `'binary'` | `'unwind'` | `RL_O41_BREAK=binary` |
| 16 | `RL_O41_UNWIND` | `_merged_recover.py:623` | `'5'` | `'7'` | `RL_O41_UNWIND=5` |
| 17 | `RL_O42` | `_merged_recover.py:676` | `'0'` | `'1'` | `RL_O42=0` |
| 18 | `RL_O43` | `_merged_recover.py:735` | `'0'` | `'1'` | `RL_O43=0` |

**DIALS DELIBERATELY NOT FLIPPED** (the candidate leaves them unset; they stay at today's default):
`RL_O35`, `RL_O38B2` (`'0'`), `RL_O39_TMAXPCT` (`''`), `RL_O40_LAMBDA` (`''`),
`RL_O41_CREDITFORM` (`'guarded'`), `RL_O31_NOPHI`, `RL_O34`, `RL_O33*`. The 11 KLINE names get **no
edit at all** — per §1 they are implied. This is stated as a prediction, not an assumption.

**U0 = 7.** Dial #16 is `RL_O41_UNWIND`, the owner's `U0`. The engine's own comment block at
`_merged_recover.py:612-622` states in capitals that U0 is **RULED, NOT MEASURED**, and that *"NO
DOCUMENT MAY DESCRIBE U0 AS MEASURED."* The order requires the label **OWNER-RULED, DATA-SUPPORTED**
to be preserved where the value now lives. Both statements are kept verbatim at the new default site:
the value is the owner's word (`20% a game`), re-ruled to 7 at D5-final 2026-08-19 with the D6
break-speed sweep as *support*, not as derivation. **The label travels with the number into the
default.** No document this seat writes will call U0 measured.

### 1.2 THE IMPLICATION GUARDS STAY LIVE — so some kill-switches are COMBINATIONS

The engine carries hard `SystemExit` coherence guards: `if _O38 and not _O37`, `if _O39 and not _O38`,
`if _O40 and not _O38`, `if _O41_BREAK!='binary' and not _O41_R3`, `if _O40_CAPFORM=='smooth' and
_O40_CAPPCT_RAW==''`, `if _O40_CAPFORM=='' and _O40_CAPPCT_RAW!=''`, `if _O38B1 and _O38B2`.
**These are NOT weakened.** Consequence, stated plainly so nobody is surprised at the console:

* `RL_O37=0` **alone does nothing** — `_O37` is an OR over `RL_O37|RL_O38A|RL_O38B1|RL_O38B2`, and
  #2/#3 now default ON. Killing the ORDER P charge requires `RL_O37=0 RL_O38A=0 RL_O38B1=0`.
* `RL_O40_CAPFORM=` alone **halts** (anchor set with no form). It must be killed with `RL_O40_CAPPCT=`.
* `RL_O41_R3=0` alone **halts** (break rule shaping a dead collector). It must be killed with
  `RL_O41_BREAK=binary`.

Killing an upstream dial requires killing its dependents — the same coherence the guards always
enforced. Fail-closed, never silent.

### 1.3 THE NAMED KILL-SWITCH COMBINATIONS = THE HISTORICAL IDENTITY CHAIN (F2)

`OFFALL` below is the full 18-dial kill-switch line (every off-value from the table):

```
OFFALL = RL_O37=0 RL_O38A=0 RL_O38B1=0 RL_O39_BETASAT= RL_O40_CAPFORM= RL_O40_CAPPCT=
         RL_O40_RECW= RL_O40_PGMAT=0 RL_O41_SDOFF= RL_O41_CREDIT=0 RL_O41_RESET=0
         RL_O41_INJ=0 RL_O41_R3=0 RL_O41_RAMP=0 RL_O41_BREAK=binary RL_O41_UNWIND=5
         RL_O42=0 RL_O43=0
```

| arm | historical identity | kill-switch combination (post-flip) |
|---|---|---|
| `BAKE_CAND` | **`a05fe951`** | *(none — bare)* |
| `BAKE_BASE` | `daa16812` | `RL_O43=0` |
| `BAKE_NOO42` | `ff936186` | `RL_O42=0 RL_O43=0` |
| `BAKE_IDENT_P` | `374d4e44` | `OFFALL` **minus** `RL_O37=0` (P charge stays live) |
| `BAKE_IDENT_K` | `f3101883` | `OFFALL` + `KLINE` (with `_O37` off, the KLINE values are no longer implied and must be supplied — exactly as `build_D7B.sh` supplies them) |
| `BAKE_L0R` | `7f88f509` | `OFFALL` minus `RL_O37=0`, plus `RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20` |

**A HARNESS DEFECT I MUST FIX TO RUN F2 AT ALL, DECLARED HERE BEFORE I FIX IT.** `bbD7.sh`'s
pass-through is `if [ -n "${!V:-}" ]; then export $V; fi` — it exports a dial **only if non-empty**.
Post-flip, the five empty-string kill-switches (#4,#5,#6,#7,#9) would be silently dropped and the arm
would build the *candidate* while wearing a historical label. That is precisely the class of silent
mismatch the pass-through list exists to prevent. `bbBAKE.sh` is `bbD7.sh` with **two declared
changes and nothing else**: (1) `${!V:-}` → `${!V+x}` (export if SET, even if empty); (2)
`export RL_V0SURF_PKL=…` → `unset RL_V0SURF_PKL`, so every arm runs **unbound** and F5 is proved by
the build itself rather than beside it. The diff goes in the record.

---

## 2. THE LOADER PRECEDENCE — THE FOOTGUN, KILLED AT THE ROOT

Today, at **two mirrored sites**:

```
_merged_recover.py:1947  _cands=[RL_V0SURF_PKL, '/home/claude/v0surf.pkl', <repo>/data/v0surf.pkl]
boot_guard.py:263-265    (the same list, byte-for-byte, "mirror _merged_recover._load_v0surf precedence")
```

The out-of-repo shadow (`fbc5b393`) sits **ahead** of the branch's own pinned surface (`5dd34ca8`), so
with the env unset the engine loads a file this branch does not own. **Both sites become
`[RL_V0SURF_PKL, <repo>/data/v0surf.pkl]`** — `/home/claude/v0surf.pkl` is removed from the
precedence outright, not merely demoted. Demotion would leave it reachable whenever the repo file is
missing; the order says it *must no longer be consulted when the env is unset*, and removal is the
only edit that makes that true unconditionally.

**`/home/claude/v0surf.pkl` IS NOT TOUCHED.** It stays exactly as it is, byte-for-byte. The fix is
in-repo precedence. I will `md5sum` it before and after and print both.

Also corrected: the halt message's remedy line still says *"Re-run bootstrap.sh to seed the workspace
copy"*. The landing-prep seat measured that `bootstrap.sh` **does not seed this artifact** (it seeds
only `cm_400.pkl` and `q97m.pkl`). Carrying a remedy known to be wrong is a trap for the next seat;
the message is corrected to name the real regeneration entry point.

**`INFRA_ALLOW` gains `RL_V0SURF_PKL`** (`config_manifest.py:39`). It is a path/IO var by that file's
own definition and never part of the value hash. This clears RESEAL_HALT blocker (B). **What still
protects the surface, and I will prove both are live:** Guard 5's fitted-artifact **load-path** leg
compares the *loaded* file's md5 against the pin, and the engine's **frozen-signature** check halts on
a surface whose signature is not in the frozen set. Neither is weakened. **Falsifier: I will point
`RL_V0SURF_PKL` at the out-of-repo `fbc5b393` surface and show it still HALTS.** If it does not halt,
I have weakened a guard and I report that as a fired falsifier.

---

## 3. THE SIDECAR

`engine/rl_after/rl_app_data.json.srcmd5` carries `own_md5 88ce647f` (the LIVE board id) beside a file
whose content is `36d5dfc7`, with `source_md5 d9a24282` against a store of `cb38ef11`. Guards 1 and 2
both fail, and `s4_matrix` halts at startup — RESEAL_HALT blocker (C), pre-existing at `ba37032`.

**The writer of record exists and I will use it, not a hand-written JSON.** `rl_export.py:898` calls
`single_source.stamp_derived('rl_app_data.json', tier=1)`, which writes `own_md5` = the derived file's
own content md5 and `source_md5` = the store md5, then sets both read-only. The bare build runs that
exact line. So: **the board file and its sidecar are lifted together out of the bare build's staging
directory** into `engine/rl_after/`. Guards 1/2 then pass *by construction*, because the pair was
produced by the generator in one act.

`engine/rl_after/rl_app_data.json` therefore becomes `a05fe951` — the candidate. That is the correct
content for a tier-1 derived artifact on this branch: `single_source.py` defines tier-1 as
*"regenerated from the store EVERY build"*, the store is `cb38ef11`, and post-flip a build from that
store **is** the candidate.

**`88ce647f` IS A STALE STAMP HERE, NOT THE LIVE BOARD.** Verified raw: no file in this worktree has
that md5; it appears only as a referenced id in `docs/ledgers/*`. Restamping a sidecar that points at
a board which is not there cannot touch the live board. I will state this again with the measurement.

**A SECOND STALE SIDECAR, FOUND AND DISCLOSED:** `data/rl_build/rl_app_data.json.srcmd5` reads
`own_md5 4b448a82` beside content `a05fe951`. It is the same class of defect, it is **not** the one the
order names, and it was left by the prior seat's board sync. I will report it with its measurement and
will **not** silently repair an artifact outside the order's scope; if repairing it is required to make
a named guard pass, I will say so and halt that item with the question.

---

## 4. THE RE-SEAL — WHY THE HALT'S FORK DISSOLVES

RESEAL_HALT blocker (A) is that the manifest line and the candidate line are **different boards**, so
sealing either would be false. Its own §2 records *why* every prior re-seal was legitimate:

> the levers of those chapters were **DECLARED KILL-SWITCHES wired default-ON into the engine with the
> manifest deliberately unmoved** … Under gate mode those engines priced the candidate line **by
> default**, so "the manifest line" and "the candidate line" were the same board.

**The defaults flip restores exactly that condition.** Once the 18 dials default ON, gate mode — which
clears ambient `RL_*` and loads the manifest — produces the candidate, because the dials are not in the
manifest and fall through to their (now candidate) code defaults. The two lines are **the same board
again**. The fork is not chosen; it is dissolved.

**`data/model_config.json` `vars` IS NOT MOVED, AND THAT IS THE POINT.** Adding the dials is Fork 2,
which moves `config_sha256`, which moves the `config` pin in `data/expected_boot.json` — the pin the C3
re-key at `9c9d9f3` just certified and the pin `a05fe951` was built under. The v2.9 kill-switch pattern
(`RL_EVW`, `RL_CAPT`, `RL_ISOFADE`, `RL_PVC2` — *"config c2d233ae UNMOVED … a declared kill-switch, not
a manifest dial"*) is precedent for leaving it unmoved, and it is the only path that does not invalidate
the re-key. **Gate mode accepts the shipped configuration because nothing ambient is set, not because
the manifest was widened.** I will prove acceptance by running it, and I will print `config_sha256` and
the boot `config` pin before and after to show both are unmoved.

The re-seal instrument is `session_2026-07-17/legd_derivation/reseal_book.py`, ported with **declared
changes**: (1) `ROOT`/`RA` re-pointed from the hardcoded `/home/user/afl-rl-engine` +
`/home/claude/rl_workspace/rl_after` to **this worktree** (the shared workspace is out-of-repo, carries
the stale D7 engine `29376d5a`, and is not owned by this branch — register v770 already ruled on
re-pointing); (2) its `RL_GAMMA='0.85'` … block **dropped**, because the manifest now says `RL_GAMMA=1.0`
and gate mode would reject `0.85` as DIVERGENT — gate mode loads those values itself.

**If a genuine ambiguity survives the flip, I HALT that item with the precise question and write no
seal.** `data/book_stable_seal.json` stays byte-unchanged in that case.

---

## 5. FALSIFIERS — WHAT WOULD MAKE THIS SEAT WRONG

Every one is measured raw and its output committed. **A fired falsifier is reported in these words.**

| id | falsifier | pass condition | **if it FIRES** |
|---|---|---|---|
| **F1** | **BARE build — no `RL_*` env at all** | `a05fe951` **BYTE-EXACT** | **HALT the flip.** The default set does not equal the candidate line. Report the produced id and the diff of dials. **Do not add dials until the number matches** — that is fitting the flip to the answer. |
| **F2** | each named kill-switch combination | `daa16812` · `ff936186` · `374d4e44` · `f3101883` · `7f88f509` all **byte-exact** | **HALT.** A kill-switch that does not restore its history is not a kill-switch. Name which arm moved and to what. Do not re-label the arm. |
| **F3** | determinism ×2 on the bare build | run 1 == run 2, byte-exact | **HALT.** A non-deterministic default build cannot be shipped. Report both ids. |
| **F4** | day-0 **89/89** internal **AND** emit replication guard **89/89** vs frozen `DAY0_CP.json` | both 89 of 89 at tolerance 0 | **HALT.** The guard fails closed and no matrix is used. Report the count. **Do not re-base the reference** — this order does not change entry prices. |
| **F5** | **Guard 5 GREEN UNBOUND** (no `RL_V0SURF_PKL` exported anywhere) | PASS, every leg | **REPORT RED.** The footgun survived the precedence edit. State which leg and the resolved path. |
| **F6** | class mark **unchanged at 1.0672** | matrix identity unmoved ⇒ mark unmoved | Re-emit **only** if the matrix identity would change. **Prove it does not** by byte-comparing the post-flip emitted matrix against the pre-flip one; if it moved, **report the new mark**, do not restate 1.0672. |
| **F7** | book seal verifies under **gate mode** on the candidate line | seal written and re-verified green | **HALT the re-seal**, leave `book_stable_seal.json` byte-unchanged, state the precise question. |

**Two further self-checks I bind myself to:** the frozen-signature guard must still HALT on the
out-of-repo surface (§2), and `config_sha256` + the boot `config` pin must be **unmoved** (§4). If
either fails I report it as a fired falsifier of my own construction.

---

## 6. SEQUENCE, AND WHAT IS NEVER TOUCHED

1. **This file, committed and pushed first.** ← *you are here*
2. Defaults flip (18 dials, 2 engine files) + the U0 label.
3. Loader precedence (2 sites) + `INFRA_ALLOW`.
4. F1/F3 bare builds → sidecar regenerated from the bare build's own staging pair.
5. F2 kill-switch arms · F5 Guard 5 unbound · frozen-signature probe.
6. F4 day-0 + emit · F6 class · F7 re-seal under gate mode.
7. `LANDING_TABLE_2` — every item green or ruled — and the commit.

**NEVER TOUCHED, BY THE ORDER AND BY THIS SEAT'S OWN WORD:** anything outside the repo
(`/home/claude/v0surf.pkl` above all, and the shared `/home/claude/rl_workspace`); the local stale
`land/order-29` ref; `main`; any tag; PR #510; the live board `88ce647f`; `data/model_config.json`
`vars`; the `config` pin in `data/expected_boot.json`.

**Depths as depths. Named players illustrate, never gate. No adoption language.**

---

**NOT ADOPTED. OWNER WORD PENDING.** The owner's word is the gate.
