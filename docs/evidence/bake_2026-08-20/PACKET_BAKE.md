# PACKET — THE BAKE (register v780, 2026-08-20)

**THIS PREPARES THE LANDING; IT IS NOT THE LANDING.** Nothing merged to main. Nothing tagged or
promoted. PR #510 held. The live board `88ce647f` untouched. **NOT ADOPTED. OWNER WORD PENDING.**
The owner's word is the gate.

Preregistered at **`907b2da`**, pushed *before* the first engine byte moved (`PREREG_BAKE.md`).
Worktree from `origin/land/order-29` at `0ec4286`. The stale LOCAL `land/order-29` ref was not touched.

---

## 1. WHAT MOVED

| | before | after |
|---|---|---|
| `_merged_recover.py` | `5f434b95` | **`5ac6780f`** |
| `rl_model.py` | `98f16794` | **`6fe7c415`** |
| board (bare build) | — | **`a05fe951`** (unchanged pin) |
| store | `cb38ef11` | `cb38ef11` (unmoved) |
| `config_sha256` | `eed19a75` | **`eed19a75` (UNMOVED)** |
| `v0surf` pin | `5dd34ca8` | `5dd34ca8` (unmoved) |
| `engine/rl_after/rl_app_data.json` | `36d5dfc7` | **`a05fe951`** |
| sidecar `own_md5` | `88ce647f` (stale) | **`a05fe951`** |
| sidecar `source_md5` | `d9a24282` (stale) | **`cb38ef11`** |

Four files carry the engine/config change: `engine/rl_after/rl_model.py`,
`engine/rl_after/_merged_recover.py`, `boot_guard.py`, `config_manifest.py`.

---

## 2. THE DIAL LIST — THE BRIEF SAID 18, THE SCRIPT SAID 29, AND THE ENGINE SETTLED IT

`build_D7B.sh` builds the candidate as `env $CLEAR $KLINE $S RL_O42=1 RL_O43=1` — **29 assignments**,
because ORDER K's 11-dial `KLINE` is applied to *every* arm. The order said trust the script, so the
gap was real and had to be resolved by reading the engine rather than picking a number:

```
rl_model.py:1089   _O37 = RL_O37 or RL_O38A or RL_O38B1 or RL_O38B2
rl_model.py:1092   _O36 = RL_O36 or _O37
_merged_recover:758 _O35 = _O35 or _O36
_merged_recover:759 _O32 = RL_O32 or _O34 or _O35
_merged_recover:761 _O31 = RL_O31 or _O32
```

`RL_O37` implies the whole stack, and the four KLINE *values* are already `_O37`-conditional defaults
(`O36_LAM_S1 = '0.40' if _O37 else '0.25'`, and the same shape for `KAPPA`/`GAMMA`/`ETA`), while
`GAMMA_D`/`LAMBDA`/`TALL`/`FLOORFIX` are already the unconditional defaults.

**So the prereg predicted, in writing and before the edit, that flipping 18 dials would be enough —
and bound this seat to report F1 as FIRED rather than add KLINE dials until the number matched.**
The bare build produced `a05fe951` byte-exact. **The prediction held. No dial was added after the fact.**

---

## 3. THE FLIP TABLE — old default → new default → kill-switch

| # | dial | old | **new** | **kill-switch** |
|---|---|---|---|---|
| 1 | `RL_O37` | `0` | `1` | `RL_O37=0` **+ `RL_O38A=0 RL_O38B1=0`** |
| 2 | `RL_O38A` | `0` | `1` | `RL_O38A=0` |
| 3 | `RL_O38B1` | `0` | `1` | `RL_O38B1=0` |
| 4 | `RL_O39_BETASAT` | `''` | `0.105` | `RL_O39_BETASAT=` |
| 5 | `RL_O40_CAPFORM` | `''` | `smooth` | `RL_O40_CAPFORM=` **+ `RL_O40_CAPPCT=`** |
| 6 | `RL_O40_CAPPCT` | `''` | `15` | `RL_O40_CAPPCT=` |
| 7 | `RL_O40_RECW` | `''` | `0.47` | `RL_O40_RECW=` |
| 8 | `RL_O40_PGMAT` | `0` | `1` | `RL_O40_PGMAT=0` |
| 9 | `RL_O41_SDOFF` | `''` | `2.98` | `RL_O41_SDOFF=` |
| 10 | `RL_O41_CREDIT` | `0` | `1` | `RL_O41_CREDIT=0` |
| 11 | `RL_O41_RESET` | `0` | `1` | `RL_O41_RESET=0` |
| 12 | `RL_O41_INJ` | `0` | `1` | `RL_O41_INJ=0` |
| 13 | `RL_O41_R3` | `0` | `1` | `RL_O41_R3=0` **+ `RL_O41_BREAK=binary`** |
| 14 | `RL_O41_RAMP` | `0` | `1` | `RL_O41_RAMP=0` |
| 15 | `RL_O41_BREAK` | `binary` | `unwind` | `RL_O41_BREAK=binary` |
| 16 | `RL_O41_UNWIND` (**U0**) | `5` | **`7`** | `RL_O41_UNWIND=5` |
| 17 | `RL_O42` | `0` | `1` | `RL_O42=0` |
| 18 | `RL_O43` | `0` | `1` | `RL_O43=0` |

Not flipped, because the candidate does not carry them: `RL_O35`, `RL_O38B2`, `RL_O39_TMAXPCT`,
`RL_O40_LAMBDA`, `RL_O41_CREDITFORM`. The 11 KLINE names got **no edit at all**.

**Three kill-switches are COMBINATIONS, and that is deliberate.** The engine's coherence halts
(`_O38 and not _O37`, `_O40_CAPFORM=='smooth'` without an anchor, a break rule shaping a dead
collector) are **not weakened**. Killing an upstream dial requires killing its dependents — the same
coherence those guards always enforced, fail-closed rather than silent.

**U0 = 7 keeps its label at the site where the value now lives: OWNER-RULED, DATA-SUPPORTED.** The
engine's own rule is restated in the same comment block and is obeyed everywhere in this packet:
**U0 IS RULED, NOT MEASURED.** The D6 break-speed sweep supports the owner's word; it does not derive it.

---

## 4. WHY `data/model_config.json` WAS NOT TOUCHED — AND WHY THE RE-SEAL FORK DISSOLVED

`RESEAL_HALT.md` halted the re-seal because the manifest line and the candidate line were **different
boards**. Its own §2 records why every earlier re-seal was legitimate: those chapters' levers were
*"DECLARED KILL-SWITCHES wired default-ON into the engine with the manifest deliberately unmoved"*, so
under gate mode the engine priced the candidate **by default** and the two lines were one board.

The defaults flip **restores that condition**. Gate mode clears the ambient model env and loads the
manifest; the 18 dials are not in the manifest; so they fall through to their now-candidate code
defaults. **The fork was not chosen — it was dissolved**, and with it blocker (A).

The alternative (putting the dials into the manifest) would have moved `config_sha256`, moved the
`config` pin in `expected_boot.json`, and **invalidated the C3 six-pin re-key at `9c9d9f3` that this
work rides on**. Measured instead: `config_sha256` **`eed19a75` unmoved**, `config_manifest.py check`
**PASS**, and **0** candidate dials present in `vars`.

---

## 5. THE LOADER FOOTGUN, KILLED AT THE ROOT

It lived at **two mirrored sites** — `_merged_recover._load_v0surf` and
`boot_guard._resolve_v0surf_load`, the latter documented as mirroring the former *byte-for-byte*.
Both now read `[$RL_V0SURF_PKL, <repo>/data/v0surf.pkl]`. `/home/claude/v0surf.pkl` is **removed from
the precedence, not demoted** — demotion would leave it reachable whenever the repo file is missing.

**`/home/claude/v0surf.pkl` IS BYTE-UNTOUCHED**: `fbc5b393` before, `fbc5b393` after, re-measured
after every probe. The fix is in-repo precedence, never out-of-repo deletion.

`RL_V0SURF_PKL` joins `INFRA_ALLOW` (blocker B). That makes the var *settable*, so the claim that it is
still not allowed to be *wrong* was **priced, not asserted**: pointing it at the out-of-repo surface
still **HALTS with no board** (`FROZENSIG_out.txt`). The probe also shows exactly why the fix works —
the bare build's signature `4405cba2` is present in the in-repo pickle and **absent** from the
out-of-repo one, which is precisely why the unbound build used to die.

Two corrections carried into the code: the halt message's remedy line (*"re-run bootstrap.sh"*) is
**wrong for this artifact** — bootstrap.sh seeds only `cm_400.pkl` and `q97m.pkl` — and is replaced by
the real regeneration entry point.

---

## 6. THE SIDECAR — REGENERATED THROUGH THE WRITER OF RECORD

Blocker (C). The writer exists: `rl_export.py:898` → `single_source.stamp_derived(..., tier=1)`, which
stamps `own_md5` (the derived file's own content md5) and `source_md5` (the store), then sets both
read-only. **The board and sidecar were lifted together out of the bare build's staging directory** —
produced by the generator in one act — so Guards 1/2 pass *by construction* rather than by a
hand-written stamp. **GUARDS 1/2: PASS.**

`88ce647f` in the old stamp was a **stale stamp naming a board that was not there**: no file in this
worktree carries that md5; it appears only as a referenced id in `docs/ledgers/*`. Restamping it
cannot touch the live board, and the live board was not touched.

**A SECOND STALE SIDECAR WAS FOUND AND IS DISCLOSED:** `data/rl_build/rl_app_data.json.srcmd5` read
`own_md5 4b448a82` beside content `a05fe951` — the same class of defect, left by the prior seat's
board sync, and **not** the one the order named. It was repaired with the same generator-written
stamp, the two board files being byte-identical. Reported rather than done quietly.

---

## 7. FALSIFIERS — EVERY ONE MEASURED

| id | result |
|---|---|
| **F1** bare build (no model-semantics `RL_*`, `RL_V0SURF_PKL` unset) | **`a05fe951` BYTE-EXACT — PASS** |
| **F2** kill-switch identities | **all five byte-exact — PASS** |
| **F3** determinism ×2 | `a05fe951` == `a05fe951` — **PASS** |
| **F4** day-0 89/89 internal **and** emit 89/89 vs frozen `DAY0_CP.json` | **89 of 89 and 89 of 89 — PASS** |
| **F5** Guard 5 GREEN **unbound** | **PASS, every leg** |
| **F6** class mark | matrix md5 **moved**; reported as moved; mark **re-measured 1.0672** |
| **F7** book seal under gate mode | see §9 |

**F2, in full:**

| arm | kill-switch | expected | built |
|---|---|---|---|
| `BAKE_BASE` | `RL_O43=0` | `daa16812` | **`daa16812`** |
| `BAKE_NOO42` | `RL_O42=0 RL_O43=0` | `ff936186` | **`ff936186`** |
| `BAKE_IDENT_P` | `OFFALL` − `RL_O37=0` | `374d4e44` | **`374d4e44`** |
| `BAKE_IDENT_K` | `OFFALL` + `KLINE` | `f3101883` | **`f3101883`** |
| `BAKE_L0R` | `OFFALL` − `RL_O37=0`, + `O38A/O38B1/TMAXPCT=20` | `7f88f509` | **`7f88f509`** |

### F6 — reported in its preregistered words

The prereg bound this seat to re-emit only if the matrix identity would change, and **if it moved, to
report the new mark rather than restate 1.0672**. It moved: `c231fda2` → `592e9040`. So the class
instrument was **re-run, not reasoned about**.

`MATRIX_DIFF_out.txt` gives the precise account: the two matrices differ in **exactly one top-level
block (`meta`)** and **exactly two fields** — `engine_head 5f434b95 → 5ac6780f` (which *must* move,
the engine source moved) and `emitter.workdir` (the worktree path, not a priced value). The priced
payload `recs` is **byte-identical**, 2648 records, canonical md5 `491560370c9f`.

**Measured mark: `BK 1.0672`** (+0.0372 vs the 1.03 floor, −0.0728 vs the 1.14 rail, inside the law),
equal to `LP 1.0672` and `D7BCAND 1.0672`. The instrument self-validates against ORDER K's published
marks first (W2 `1.0513` / cohort `1.0324`, delta `0.0000` → VALIDATED).

---

## 8. THE HARNESS DEFECT THAT WOULD HAVE FAKED F2

`bbD7.sh` passes a dial through only `if [ -n "${!V:-}" ]` — **non-empty only**. Post-flip, the five
empty-string kill-switches (`RL_O39_BETASAT=`, `RL_O40_CAPFORM=`, `RL_O40_CAPPCT=`, `RL_O40_RECW=`,
`RL_O41_SDOFF=`) would have been **silently dropped**, and each historical arm would have quietly
rebuilt the *candidate* while wearing a historical label — exactly the silent mismatch that
pass-through list exists to prevent. It was declared in the prereg *before* the fix and corrected in
`bbBAKE.sh` (`${!V+x}`: export if SET, empty included). `bbBAKE.sh` carries **three** declared changes
from `bbD7.sh` and nothing else; the diff is in the record.

---

## 9. THE RE-SEAL — DONE, ON THE CANDIDATE LINE, UNDER GATE MODE

`data/book_stable_seal.json` had not moved since **2026-07-17**. It has now been re-sealed, and the
three `RESEAL_HALT.md` blockers were cleared by the work itself rather than worked around:

* **(A) the fork** — dissolved by the defaults flip (§4). Gate mode **accepted the shipped
  configuration**: the run did not halt on line one, and the matrix's own `__meta__` came back
  `config=eed19a75` — the unmoved hash.
* **(B) `RL_V0SURF_PKL` unusable under gate** — the re-seal ran with the var **not set at all**,
  because the in-repo pinned surface is now the default load path.
* **(C) the stale sidecar halting `s4_matrix`** — regenerated through the writer of record (§6).

```
matrix meta   : engine=5ac6780f store=cb38ef11 config=eed19a75f775
  sealed (before): head 40f43772 store 968de0c7 n 2649 stable 745e3462007aec2f
  candidate      : head 5ac6780f store cb38ef11 n 2650 stable 86a82e6ebce66844
RE-SEALED: head 40f43772 -> 5ac6780f | n_players 2649 -> 2650 | stable_sha256 745e3462 -> 86a82e6e
```

`n_players` was **re-counted, not carried** (2649 → 2650), as the procedure of record requires.

**F7 is closed by an independent re-verify, not by the write.** `reseal_bake.py --check` regenerated
the book a second time from scratch under gate mode and compared every field of the committed seal:

```
  B3 RE-VERIFY: PASS — the committed seal matches a freshly regenerated gate-mode candidate book, every field
```

That also prices the book path's determinism: two independent gate-mode regenerations produced the
same `stable_sha256` `86a82e6e` and the same `n_players` 2650.

**Declared port changes** (`reseal_bake.py`, 3, and nothing else): `ROOT`/`RA` re-pointed from the
hardcoded `/home/user/afl-rl-engine` + `/home/claude/rl_workspace/rl_after` to **this worktree** (that
shared workspace is out-of-repo and carries the stale D7 engine `29376d5a`); the `RL_GAMMA='0.85'…`
block **dropped**, because the manifest now says `RL_GAMMA=1.0` and gate mode would reject `0.85` as
DIVERGENT — gate mode loads those values itself; thread pinning made explicit.

**Standing finding, not fixed here:** `ship_gates_check.py:49` carries the same hardcoded
`RA = '/home/claude/rl_workspace/rl_after'`. It is reported, not edited — no order covers it.

---

## 10. THE FINAL ACCEPTANCE TABLE

`LANDING_TABLE_2_out.txt` — **20 rows: 18 GREEN, 1 RULED, 1 not-green.** Every cell scraped from a raw
output file; no verdict typed in.

* **RULED (1):** Guard 5 `literal` against the shared out-of-repo `/home/claude/rl_workspace`. That
  workspace still carries the stale D7 engine `29376d5a`. **The gap did not close — it WIDENED**, and
  legitimately: this branch's engine moved at this bake. Re-seeding that workspace is `bootstrap.sh`'s
  job and it is **out of repo**, which this order forbids touching. Reported, not fixed.
* **NOT-GREEN (1):** the F6 *matrix identity* row. It moved, and the row says so. §7 has the account:
  provenance metadata only, priced payload byte-identical, mark re-measured at 1.0672.

The landing prep's **two out-of-repo reds** are both re-measured: the v0surf unbound leg is now
**GREEN**, and the workspace-engine note is **RULED** as above.

### FINDINGS RAISED, NOT ACTED ON (no order covers them)

1. `ship_gates_check.py:49` hardcodes the out-of-repo workspace as its engine dir (§9).
2. `_V0SURF_GATES` (`_merged_recover.py`) carries `'RL_GAMMA':'0.85'` as its signature fallback while
   the engine's own default is `'1.0'` (`rl_model.py:872`) — a violation of that block's own stated
   invariant that *"value-gate defaults [are] byte-for-byte the code defaults, so a build that SETS a
   gate to its default signs identically to a build that leaves it UNSET."* It is **harmless today**
   only because `data/v0surf.pkl` happens to carry both signatures (`4405cba2`, `41af7326`). It was
   left alone deliberately: changing it would move the signature and is not this order's business.
3. The `v0surf FROZEN-SIGNATURE HALT` message names `data/v0surf.pkl` even when the surface it
   actually loaded came from `RL_V0SURF_PKL` (visible in `FROZENSIG_out.txt`). Cosmetic, but a guard
   message naming the wrong file is worth a line.

---

## 11. WHAT WAS NOT TOUCHED

`main` · any tag · PR #510 · the live board `88ce647f` · `/home/claude/v0surf.pkl` ·
`/home/claude/rl_workspace` · the local stale `land/order-29` ref · `data/model_config.json` `vars` ·
the `config` pin.

**NOT ADOPTED. OWNER WORD PENDING.**
