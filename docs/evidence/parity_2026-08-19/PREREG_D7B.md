# PREREG — ORDER D7b, **THE THIRD WIRING SITE OF THE PARITY LAW (`o31_D`)**

**Branch `land/order-29`, from `origin/land/order-29` at `db1d11c`. Engine at prereg time:
`29376d5a73a3e8274fcebe5cd90ada0b` — UNTOUCHED.**

**THIS FILE IS PUSHED BEFORE THE ENGINE IS EDITED (F6).** Nothing below is written after the fact.
Every measurement quoted here as *already known* comes from evidence committed at or before `db1d11c`
and is cited to its file.

> ## THE BOARD IS **PRICED, NOT ADOPTED.**
> Nothing here is adopted, merged, tagged or promoted. Those are owner-only acts. Nothing goes to
> `main`. No tag, no PR, no promote.

---

## 1 · AUTHORITY

**Register v771** — the owner's parity ruling, verbatim:

> "Being marked as injured shouldn't all of a sudden enrol you to a mechanism that doesn't affect
> your peers. In other words, a first year sitter who is injured is punished harder for it. No
> thanks."

**Register v775** — this order. D7b is instructed to wrap the third wiring site (`o31_D`) under the
existing dial and then finish the completion pass's items that fail-closed on it.

**U0 = 7 return games: OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19).**

**The law is unchanged by this order.** It is the same per-row `max` at `Y=2026`, on the same ruling,
under the **same dial `RL_O43`**. **NO NEW DIAL. NO NEW PARAMETER. NOTHING IS FITTED.**

---

## 2 · THE SITE, AND WHY IT IS THE THIRD ONE

`ORDER D7` wired the parity `max` at **two** sites:

| site | symbol | engine | what it governs |
|---|---|---|---|
| 1 | `ev` | `_merged_recover.py:6036` | the row's price |
| 2 | `_entry30b_price` | `_merged_recover.py:6068` | the engine's day-0 predicate |

**It did not wire `o31_D` itself.** `docs/evidence/final_candidate_2026-08-19/HALT_EMIT_CP.md` and
`O31D_PROBE_out.txt` diagnose this fully: the ORDER 31-F emitter reads `o31_D` **out of the engine
namespace** (`emit_matrix_31f.py:83`, `o31_D = G['o31_D']`) and forms the year-0 column as
`int(round(_landed_v0_board(q) * o31_D(q, BASE_REF)))` (`:143`). Because `o31_D` is unguarded, the
emitter forms the **live-depth (injury) fade** while the board carries the **healthy** one, and the
emit fail-closed at **82 of 89**, on exactly the seven rows where the healthy fade wins.

**The emitter is faithful to its design and is not modified. `DAY0_CP.json` is correct and is not
touched.** The gap is in the engine: the law moved to a wrapper one level *above* the symbol the
emitter was told to read.

### 2.1 · THE STRUCTURAL FINDING THAT SHAPES THIS EDIT — DISCLOSED IN ADVANCE

Read off the engine at `db1d11c`, before any edit:

```
_merged_recover.py:5109   def _entry30b_price(p,Y=2026,__d=_entry29b_derived):
:5110       _d0=__d(p,Y)
:5111       if _d0 is None: return None
:5112       return _d0*o31_D(p,Y)
```

**`_entry30b_price` IS `_d0 * o31_D`.** It resolves `o31_D` as a **module global at call time**
(`o31_D` is defined at `:4224` inside a module-level `if _O30B_PREVIEW:` block, which creates no new
scope). The D7 **second site** corrects that predicate by multiplying its result by `_dh/_dl`
(`:6075`).

**Therefore the third site SUBSUMES the second.** The moment `o31_D` returns the healthy fade, the
un-wrapped `_entry30b_price` already returns `_d0*_dh` — which is **exactly** the board's printed
day-0 price. If the D7 second-site ratio *also* fired, the predicate would return `_d0*_dh²/_dl` and
the law would be applied **twice**. Worked on `harley-barker` from `O31D_PROBE_out.txt`:

| | value |
|---|---|
| `derived_v0` | `843.128494491119` |
| `_dl` (live/injury fade) | `0.571012` |
| `_dh` (healthy fade) — implied by `_e30b_price/derived_v0` | `0.597193` |
| `_d0*_dl` — what the EMITTER forms today | `481.4362` → `481` |
| `_d0*_dh` — the board's printed day-0 | `503.5089` → **`504`** ✓ |
| `_d0*_dh²/_dl` — **if both sites fired** | `526.60` → `527` ✗ |

**So this edit is not "add a third wrapper on top of the second".** It is: **put the one correction
at the one symbol every consumer reads, so the predicate, the price and the emitter cannot disagree.**
The second site's *ruling*, its *dial* and its *arithmetic* are unchanged — only the **level** at
which it is applied moves down one, from the predicate to the fade the predicate is built from. That
is **ONE site**. The engine change is confined to the `RL_O43` block; **no other engine file and no
other engine behaviour is touched.**

### 2.2 · WHAT THE WRAPPER WILL BE

Installed inside `if _O43:`, **after** the healthy-counterpart measurement loop (so `_dl` and `_dh`
are both measured on the **unwrapped** fade — a wrapper installed earlier would measure itself), and
in place of the second-site wrapper:

- keyed on `_D7_DFADE`, which D7 already populates **only** where the healthy value wins;
- **`Y=2026` only** — the parity ruling is a 2026 ruling. Years 1..7 of the walk-forward matrix go
  through `ev(p,Y)` at `Y>2026` and **must not move**;
- a **`max`**: the fade is raised to the healthy fade and can only rise. `_D7_DFADE` is populated
  under `_v_hth > _v_inj`, and the wrapper additionally requires `_dh > _dl`, so a riser
  (`ollie-murphy`) is returned **untouched**. The shield is not a charge.
- **dial off ⇒ the wrapper is never installed**, exactly as the other two sites.

### 2.3 · THE KNOWN RISK, NAMED BEFORE IT IS RUN

`o31_D` has **three** live consumers in the engine (`grep` at `db1d11c`): `o31_pi` (`:4877`, the
price path), `_entry30b_price` (`:5112`, the predicate) and a structural assert (`:5120`, which runs
**before** the `RL_O43` block and so sees the unwrapped fade).

The consumer that carries risk is **`o31_pi` at `:4877`** — the price path. Of the **23 lifted rows**
(`PARITY_D7.json`), **17 have `g2026 == 0`** and **6 have `g2026 > 0`** (Armstrong 3, Fiorini 2,
Rozee 2, Edwards 2, Hinge 1, Lord 1).

- For a **gameless** row the one law collapses to `v = v0 * D(c_u)` exactly, so lifting the fade is
  identically the `max` the `ev` wrapper already performs — **it cannot move the board.**
- For a row **with games**, `o31_pi` blends `D*(1-r) + phi*beta*r`, so lifting `D` raises the price
  by a quantity that is **not** identically the floor. The `ev` wrapper's `max` should still return
  the floor `_v_hth` — the fade is only one of the seven injury channels, so the lifted-fade price
  should stay **at or below** the all-channels-off healthy value — **but this is an expectation, not
  a proof, and it is therefore a falsifier and not an assumption.**

**If the board moves, this seat HALTS and reports. It does not renormalise, does not re-fit, does not
adjust the floor, and does not regenerate a reference to absorb the move.**

---

## 3 · THE FALSIFIERS

Every one is a **byte-exact** identity or an exact count. **Any failure is reported as a failure.**

| # | falsifier | pass condition |
|---|---|---|
| **D7B-F1** | **the board must not move.** Dial ON, the candidate dial line, board md5 | **`a05fe951f78482c70520480e184c80ec` byte-exact.** `o31_D` must NOT feed the board price a second time. **If it moves: HALT AND REPORT, do not renormalise.** |
| **D7B-F2** | **dial off is a no-op.** `RL_O43` UNSET, same line | **`daa16812e50fb71241e627d89180412c` byte-exact** |
| **D7B-F3** | **the emit reads 89 of 89** against `DAY0_CP.json`, **zero reference edits**, emitter byte-carried at `d5f4880662b7de3f2716e1c84112d11d` | **`89 of 89` at tolerance 0** |
| **D7B-F4** | **determinism ×2**, board and matrix | board repeat identical; matrix md5 identical |
| **D7B-F5** | the printed-day-0 internal assert | **89 of 89 at tolerance 0** |
| **D7B-F6** | the dial-off identity chain, all upstream | `O42-off ff936186` · `all-O41+-off 374d4e44` · `K f3101883` · `R20A 7f88f509` |
| **D7B-F7** | **years 1..7 must not move.** The wrapper is `Y==2026`-only | no `Y>2026` price changes; the matrix's year>0 columns are formed from `ev(p,Y)` |
| **D7B-F8** | **the riser is untouched.** `ollie-murphy` | `o31_D` unchanged for him; his emitted year-0 stays `200` |

**A failure of F1 is a HALT, not a finding to be worked around.**

---

## 4 · WHAT IS **NOT** TOUCHED

- `docs/evidence/candidate_31f/emit_matrix_31f.py` — **byte-carried by design.** `d5f48806…`
- `docs/evidence/final_candidate_2026-08-19/DAY0_CP.json` — **the reference is CORRECT.** `210510fe…`
- `docs/evidence/order_k_2026-08-18/DAY0_K.json` — the frozen ORDER K reference.
- Any engine file other than `engine/rl_after/_merged_recover.py`.
- Any dial, any parameter, any threshold, any fitted quantity. **There is none in this order.**

---

## 5 · PINS

| | md5 |
|---|---|
| engine (pre-edit) | `29376d5a73a3e8274fcebe5cd90ada0b` |
| store | `cb38ef1171dcf20aae66ebf12682be0d` |
| v0surf | `5dd34ca82735f5c8f021b1c7320df8f8` |
| sitter sheet | `b26798c35adcd9bda5cef50ff2c884da` |
| day-0 reference `DAY0_CP.json` | `210510fe5d09bbbd16909bb63f4a118d` |
| ORDER 31-F emitter | `d5f4880662b7de3f2716e1c84112d11d` |

**THE DIAL LINE** — read verbatim from `build_D7.sh`:

```
RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20
RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08
RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1 RL_O43=1
```

`RL_V0SURF_PKL` is bound explicitly to this branch tree's own `data/v0surf.pkl` on every run.

**GUARD 5 IS RED on this branch (C3 pin staleness, PRE-EXISTING). It is recorded, NEVER claimed
green, and NOT re-pinned by this order.**

---

## 6 · THE REST OF THE ORDER

After the identities pass, this seat completes the three items the completion pass fail-closed on:
the **emit** on `a05fe951` (via `run_emit_CP.sh`, **never** `run_emit_ASM.sh`), the **class mark**
on the candidate matrix (self-validating against ORDER K `1.0513`/`1.0324`, base `ff936186` =
`1.0671174504`), and the **full no-arb page** for `a05fe951`. Whatever they read is reported, in
either direction. The R3-probe FAIL on `PACKET_COMPLETION.md` is a **named instrument follow-up** and
is **NOT** in this order's scope; it stays failed.

**Priced, not adopted.**
