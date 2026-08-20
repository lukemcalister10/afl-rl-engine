# PREREG — ORDER D8, THE CEILING-ONLY LEG. Free B-3 from the dead ladder, price it, produce the movers list.

**Seat:** D8 build seat (the ceiling-only leg), register **v794** (probation **v772**, sequencing **v793**)
**Date:** 2026-08-20 · **Base:** `origin/main` @ `6bfda2c`
**Measured base identities:** store `cc02567f80bef39228f25854d121a766` · board `a05fe951f78482c70520480e184c80ec` ·
engine_head (`_merged_recover.py`) `5ac6780f3c4931edcaa527576bbdfb88` · `rl_model.py` `6fe7c4155866d80e8045bed2d3bf2802` ·
`rl_export.py` `e69637ff0e9ef98b704411b989f495be` · config `eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1` ·
q97m `cfdc73216c099e5e8f1fda3968f31c00` · `as_of_round=22` · balanced sibling `72fe3a176953fce36239d7b81c3cd492`.

**This document is written and committed BEFORE the engine edit. Nothing below was measured after the fact.**
The one measurement that PRECEDES it — that the dev-shell build recipe named in §3 reproduces the live board
`a05fe951` byte-exact on the unedited tree — is stated as such, and it involved no edit.

**PRICED, NOT ADOPTED.** The live board must not move. The owner's look at the movers list, and his word, come
between this delivery and any adoption. This seat moves no board pin, no store, no config, no register.

---

## 1. What is on probation, and why it cannot currently be run alone

The owner kept ORDER B's **B-3 ceiling fix** on probation — *"happy to look at still boosting the younger
players pending a look at the movers list"* (register v772) — and v793 re-sequenced it to land **before** the R23
ingestion so the round movers are lever-constant. Delivering that look requires pricing B-3 **by itself**.

`RL_O33` (ORDER B) has two live legs and one stage dial:

| leg | site | gate today |
|---|---|---|
| **B-1** tall post-peak ladder | `rl_model.py:frac()` (`O33_TALL_LADDER`) | `_O33 and _O33S>=1 and j>0 and g in ('KPD','KPF')` |
| **B-1** anchor-preserving renorm `s*` | `_merged_recover.py:1448` | `MA._O33 and MA._O33S>=1 and g in ('KPF','KPD')` |
| **B-3** taper retirement | `_merged_recover.py:1120` (the `b6` wrapper) | `MA._O33 and MA._O33S>=2` |

`_O33S` is `int(RL_O33_STAGE)` **only when `_O33` is true**, otherwise `0`. Both B-1 sites fire at `>=1`; B-3
fires at `>=2`; and `2 >= 1`. **There is therefore no stage value that runs B-3 without also running B-1.**
B-1 is OWNER-KILLED (v772 — the tall ladder must not fire). So the ceiling fix is currently unrunnable, and
that is the entanglement this seat exists to cut.

## 2. THE WIRING — stated exactly, in advance

**Scope: `engine/rl_after/_merged_recover.py` ONLY. ONE contiguous hunk, at the `b6` wrapper (currently
`:1117-1124`). No expression, constant, threshold or law is touched. NO NEW PARAMETER IS INTRODUCED.**

The declared kill-switch `RL_O33_TAPEROFF`, default OFF, defined at its point of use and consumed in the same
hunk (the house pattern: `RL_O41_UNWIND` is likewise read in this file; `RL_CAPT`/`RL_ISOFADE`/`RL_EVW`/
`RL_UNCOMP`/`RL_ONEMACH` are the declared-kill-switch family):

```python
_b6_pre_v7=b6
_O33_TAPEROFF=os.environ.get('RL_O33_TAPEROFF','0')!='0'     # ORDER D8 (declared kill-switch, default OFF)
def b6(p,Y=2026):
    bb=_b6_pre_v7(p,Y)
    if (MA._O33 and MA._O33S>=2) or _O33_TAPEROFF: return bb  # B-3 TAPER RETIREMENT
    if _isreal(p):
        try: return _v7(bb,p,Y)
        except Exception: return bb
    return bb
```

**Why this isolates B-3, provably.** Both B-1 expressions are guarded by `MA._O33`, which is read from
`RL_O33` **and from nothing else** (`rl_model.py:857`). `RL_O33_TAPEROFF` is a distinct environment name that
this seat never causes `RL_O33` to be set. With `RL_O33` unset: `MA._O33 is False`, `MA._O33S == 0`, and the
ladder's two `and`-chains short-circuit on their first term at every call — the ladder table `O33_TALL_LADDER`
and the pin `O33_SSTAR` are read by no reachable expression. The ladder stays dead **by construction, not by
convention**, and F2 tests it rather than asserting it.

**No constant is fitted.** `asc == 1` is not a value this seat chose: it is ORDER B's own quantile re-fit
answer — the boundary solution `asc*=1` in **every** band the taper bites (`RESULTS_B_TAPER.json`,
`PACKET_B_DERIVATION.md` §4). The dial is a boolean. There is nothing here to target-fit.

**Adoption is NOT this act.** `RL_O33_TAPEROFF` is deliberately **not** a manifest dial: it is absent from
`data/model_config.json`, so `config_manifest.enforce()` **rejects it as an unknown model override in
bake/gate/canonical mode** and no certifying build can carry it. Adoption — flipping the default and stamping
the manifest — is a later act through the same lane the bake used, on the owner's word.

### 2.1 The disclosed, unavoidable consequence: the engine_head identity restamp

Editing `_merged_recover.py` moves the **computed** `engine_head` identity. `release_manifest_check.py`
computes truth from the file and asserts four **live** carriers against it, and Guard 5
(`boot_guard.assert_boot`) asserts it too. Leaving them stale would red two acceptance checks that are GREEN
on the base tree, so this seat restamps exactly these four fields and nothing else:

* `data/expected_boot.json` → `engine_head`
* `data/release_contract.json` → `identities.engine_head` (+ its recomputed `contract_sha256` self-seal)
* `ui/data/board_view_working.js` → `stamp.engine` (8 hex) and `stamp.release.engine_head`

**No other pin moves. `board` stays `a05fe951`, `store` stays `cc02567f`, `config` stays `eed19a75`,
`rl_model` stays `6fe7c415`, `register` and `as_of_round` unchanged.** `data/book_stable_seal.json`'s
`head_md5` is a **freeze-stamp** (kind `sealed` in the gate) and will read as SEALED-LAG — reported, never
gating, and NOT re-sealed here: a book re-seal is a separate act and this seat does not smuggle one in. If a
genuine ambiguity arises about whether `reseal_book` is required, **HALT and report** (the H3 seat's rule).

### 2.2 What this prereg explicitly does NOT do

* It does **not** touch `frac()`, `O33_TALL_LADDER`, `O33_SSTAR`, `_o33_ladder`, or the `s*` renorm site.
  If the wiring cannot isolate B-3 without touching a ladder expression, this seat **HALTS** and reports the
  entanglement precisely.
* It does **not** change `RL_O33` / `RL_O33_STAGE` semantics. A build that sets `RL_O33=1 RL_O33_STAGE=2`
  behaves exactly as it does today.
* It does **not** refit `q97m` (frozen; its censoring-aware refit is bake-time per R-W6) and does not touch
  `_v7`, `_b6_core`, `V7_FORM_W` or the W4 form-conditioned tail retention.
* It does **not** flip any default, adopt anything, move the board, or re-seal the book.

## 3. THE BUILD RECIPE, pinned before use

The accepted disposable FV builder — `session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build`
— exactly as the H3 repair seat used it, `balanced=False`, `PYTHONHASHSEED=0`, all five BLAS thread counts
pinned to 1, staging into a throwaway dir and **writing nothing under the repo**; staging deleted after each
run; strictly sequential; under `tools/build_lock.sh`.

* **dev-shell posture** (`config_mode=None`) is the pricing comparator, because `RL_O33_TAPEROFF` is not a
  manifest var and canonical mode rejects it (§2). **Measured on the unedited tree, before any edit:
  dev-shell `balanced=False` builds `a05fe951f78482c70520480e184c80ec` — byte-exact to the live board.**
  The dev-shell base and the board of record are therefore the same object and the priced delta is
  attributable to the dial alone.
* **canonical posture** (`config_mode='canonical'`) is run with the dial unset only, to re-tie the edited tree
  to the board of record through the fenced path.

**Disclosed tooling interaction, measured on the base tree:** a canonical-mode build launched from inside
`tools/build_lock.sh` HALTS, because the lock exports `RL_BUILD_LOCK_HELD` and `config_manifest.enforce()`
rejects it as an unknown `RL_`-prefixed model override. The driver therefore drops `RL_BUILD_LOCK_HELD` from
the **child build's** environment (the lock itself is still held by the parent shell's fd). This is reported
as a finding, not worked around silently.

## 4. FALSIFIERS — declared before the edit. Any one firing HALTS and is reported as fired.

| id | falsifier | pass condition |
|---|---|---|
| **F1** | **Dial unset ⇒ the live board is BYTE-IDENTICAL.** The wire must be a pure no-op when off. | dev-shell `balanced=False`, `RL_O33_TAPEROFF` unset ⇒ board md5 **`a05fe951f78482c70520480e184c80ec`**, byte-exact; and the same under `config_mode='canonical'`. Any other md5 ⇒ HALT. |
| **F2** | **The ladder must NOT fire.** Both B-1 legs dead on the priced board. | (a) in the priced posture `MA._O33 is False` and `MA._O33S == 0`; (b) for **every** KPD/KPF row past peak (`j>0`), `MA.frac(a,pa,g) == MA.DELTAS[j]` exactly — the shared DELTAS path, 0 divergences; (c) on the priced board **no tall (KPD/KPF) veteran moves DOWN**. Any divergence ⇒ HALT. |
| **F3** | **Determinism.** | two independent builds in each of the two postures (dial off, dial on) ⇒ identical board md5 within each posture. |
| **F4** | **Ceiling v-inversions.** The claim under test is ORDER B's *"kills every ceiling v-inversion by construction"*. A **v-inversion** is a row whose ceiling band sits below the band beneath it: `b6(p)[5] < b6(p)[4]` (`PREREG_W6.md` §C2 — `_b6_core` returns `band[5] = max(pred, b[4])`, so a **pre**-taper inversion is impossible and every inversion is the v7 taper's). Counted over the active board population in both postures. | priced count **≤** live count. The construction claim is **tested**, not assumed: if the priced count is not **0**, that is reported as the claim failing, not smoothed over. |
| **F5** | **The day-0 boot-class assert.** | `rl_export.py`'s PRINTED-DAY-0 ASSERT reads **89 of 89** at tolerance 0 on the priced build's own stdout. Fewer, or a HALT ⇒ report as fired. |
| **F6** | **The acceptance runner GREEN with the dial unset.** | `python3 -m acceptance.runner` ⇒ `VERDICT GREEN`, 0 FAIL, on the edited tree with the dial unset (after the §2.1 restamp). |

## 5. THE DELIVERABLE — the owner's movers list

Every mover between the base board (`a05fe951`) and the priced board: **name · age · position · before ·
after · delta · %**, sorted by delta, with:

* a summary — count, total, direction split (up / down / unmoved), cohort shape;
* **per-band attribution** — which age × position bands carry the movement, on the derivation's own age bands
  (`≤19 · 20-21 · 22-23 · 24-26 · 27+`) crossed with the six positions;
* the full list, not a top-N.

**The expected shape, declared in advance:** young talls and rucks UP, nothing down. **If anything moves down,
that is a finding to explain, not to smooth over.** The mechanism to check first is named here, in advance, so
that the explanation cannot be invented afterwards: retiring the taper raises `band[5]` for the rows it bit,
which raises their captain-free production `pr0`; `RL_UNCOMP`'s load-time **per-position conservation renorm**
`C[pos] = Σpr0 / Σv0p` (`_merged_recover.py:5828`) and the reference medians `V_ref_b[pos]` / `RHO_DEN[pos]`
are therefore re-derived at a different level, and they rescale **every** row in that position — including rows
whose own ceiling never moved. `C[pos]`, `V_ref_b[pos]` and `RHO_DEN[pos]` are printed by the build itself and
will be recorded for both postures.

**Documents:** the `ui/templates/` skeletons are tried first (`movers.html`, first live use) and the outcome —
fit or misfit, named slot by slot — is reported. Where they do not fit, the v757/house movers format is used.
Raw `*_out.txt` for everything.

## 6. Sanctioned-edit discipline

**ONE engine-file edit** for this whole order: the §2 hunk in `engine/rl_after/_merged_recover.py`. The four
identity fields of §2.1 are bookkeeping, not engine edits, and are enumerated above. The owner's input bytes
are never modified. Prereg lands first, in its own commit, before the edit exists.
