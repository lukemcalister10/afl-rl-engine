# STOP AT STEP 3 — THE RULED CURVE CANNOT BE LOADED BY THE ENGINE

**ORDER 29 · branch `land/order-29` · 2026-08-13 · build seat.**

> ## THE BUILD IS STOPPED AT STEP 3, BEFORE THE CURVE WAS INSTALLED.
> The ORDER-28 candidate curve — the one Ruling C produced and the one PREREG P5 predicts, spot value
> for spot value — **halts the engine on load**. Two owner rulings are in direct collision and only
> the owner can say which governs. Nothing was improvised around it: the curve is **not** installed in
> the checkout, no standing assert was relaxed, and no number was nudged to fit.

---

## 1. THE MEASUREMENT, NOT THE INFERENCE

The candidate artifact was composed (`o29_curve.py`), installed into a **scratch** workspace, and the
board build was run. It did not produce a board:

```
  File ".../rl_after/rl_model.py", line 1449, in <module>
    _PVC2M=_split_ladder(_V2RAW,'RL_PVC2 v2 curve')
  File ".../rl_after/rl_model.py", line 1436, in _split_ladder
    assert not _bad, "%s G-MONO: national curve 1..%d is not STRICTLY decreasing ..."
AssertionError: RL_PVC2 v2 curve G-MONO: national curve 1..64 is not STRICTLY decreasing
              — 12 plateau(s) at picks [6, 7, 8, 9, 10, 11, 15, 16]
```

This is a **halt, not a warning**. The build stops before any board exists, which is the same benign
failure class as the ORDER-28 thread starvation: it cannot produce a *wrong* board, only no board.

## 2. WHY THE CURVE HAS PLATEAUS — IT IS NOT A DEFECT IN THE DERIVATION

**Ruling C** (#334 comment 5276216984) ruled the priced curve **monotone**, implemented as weighted
PAVA. PAVA removes an ascent by replacing each violating block with its **weighted mean** — so a
pooled block **is a plateau by construction**. ORDER 28 §5.2 published exactly this: picks 6–12 pool
to 1319.1 and picks 15–21 pool to 812.2.

The plateaus are therefore the *intended output* of the ruling, and they are what PREREG P5 itself
predicts — P5 names **pick 7 = 1319 and pick 10 = 1319**, and **pick 15 = 812 and pick 20 = 812**.
The prereg predicted a curve the engine refuses to load. All twelve P5 spot values matched; the
prediction was accurate and the artifact is still unloadable.

## 3. WHY THE ENGINE REFUSES — G-MONO IS ALSO OWNER LAW

`_split_ladder(raw, what, strict=True)` (`rl_model.py:1409-1444`) asserts `nd[k] > nd[k+1]` across
1..64 — **strictly** decreasing, no plateaus. Its own docstring states the scope deliberately:

> *"G-MONO (strict descent) is asserted with strict=True, which is every ladder that SHIPS. It is
> relaxed only for a TRANSIENT intermediate basis that is overwritten before anything is written …
> That is a scope judgement about where the law bites, not a weakening of it."*

It is enforced at **four** independent sites, so this cannot be got round by patching one:

| # | site | what it asserts |
|---|---|---|
| 1 | `rl_model.py:1449` | `_split_ladder(_V2RAW,'RL_PVC2 v2 curve')` — **the halt above** |
| 2 | `_merged_recover.py:2568` | `_split_ladder(_V2CURVE,'RL_PVC2 v2 curve')` |
| 3 | `rl_export.py:144` | `_split_ladder(_ADOPTED,'L7 adopted curve')` — the shipped curve, unconditionally |
| 4 | `one_source_selftest.py:430` | `G-MONO strict descent on _PVC0 (p=1..64, no plateaus)` |

and a fifth, softer one: `one_source_selftest.py:551` asserts the artifact **self-declares**
`r104_9_strict_descent is True`. The live artifact declares `true` today and it is true today; under
the candidate curve that declaration would become a false statement about its own contents.

## 4. THE COLLISION, STATED PLAINLY

| | |
|---|---|
| **Ruling C** (2026-08-12, #334 5276216984) | the priced curve is **monotone**, via PAVA ⇒ plateaus |
| **G-MONO** (RULEBOOK v2.1 law 4) | the shipped national curve is **strictly decreasing** ⇒ no plateaus |

Both are owner law. The register's own words on each:

* v444 (2026-07-24): *"I'm happy to put a hold on G-MONO"* — **but the hold is scoped**, and the
  register says so explicitly: the lawful shape of record is *"STRICTLY DECREASING from pick 1 to the
  measured pool-merge point, FLAT AT POOL VALUE thereafter"*, and — decisively for this build —
  *"the CURRENT frozen curve (blended world) still satisfies G-MONO as written and **remains gated by
  it until the restructured pricing exists** — the hold governs the new world, not the old ruler."*
  The restructured pricing does not exist yet. **This landing is on the old ruler.**
* the register also records, in the competitor-method review: *"NOT ADOPTED: … **plateau
  permissiveness** (strict descent is owner law; the −1 step is an ordering tiebreak below data
  resolution, conceded as such, not measured precision)."*

So the record refuses plateau permissiveness in one place and mandates PAVA in another. **A build seat
cannot choose between two owner rulings.** That is the whole reason this file exists instead of a
landed board.

## 5. THE THREE RESOLUTIONS — FOR THE OWNER, NOT TAKEN BY THIS SEAT

Each is a real option with a real cost. None has been applied.

**(A) RELAX THE ENFORCEMENT to non-increasing for the shipped curve.** Change `strict=True` →
`strict=False` at the three `_split_ladder` ship sites, amend `one_source_selftest.py:430`, and flip
`r104_9_strict_descent` to `false` with its scope re-worded. *Cost:* amends RULEBOOK law 4 for the
current world, which the v444 hold explicitly did **not** do. Keeps the ruled numbers exactly — P5 and
P6 stay as measured. This is the option that honours Ruling C untouched.

**(B) DE-PLATEAU THE POOLED BLOCKS.** The engine already carries `_deplateau` (`rl_model.py:1376`),
which ramps an interior flat run linearly through its real endpoints. *Cost:* it **re-introduces the
exact ordering PAVA was ruled in to remove** — inside a pooled block the data says there is no
ordering, and this invents one. It also breaks P5 (picks 7 and 10 would no longer both read 1319) and
perturbs the P6 plain-sum conservation. Cheapest in code, most expensive in meaning.

**(C) THE −1 ORDERING TIEBREAK.** Separate each plateau step by one point, the convention the register
names as *"an ordering tiebreak below data resolution, conceded as such, not measured precision."*
*Cost:* smallest numeric distortion (≤ 5 points on any pick, ≤ 0.03% on the plain sum) and it is a
named house convention rather than an invention — but it still edits ruled output, and it still
breaches P5's published spot values.

**This seat's read, offered as a recommendation and nothing more:** (A) is the only one that does not
edit a ruled number, and the v444 hold shows the owner was already moving G-MONO's scope. But (A)
amends a rulebook law, and that is exactly the class of change the standing discipline says is his
word and not a build seat's.

## 6. WHAT IS ALREADY LANDED ON THE BRANCH, AND WHAT IS NOT

**Landed and proven (Steps 0–2):**

| | |
|---|---|
| P1 byte-identity control at entry | **HELD** — `88ce647f`, on the untouched tree |
| P2 the unflag-three | **HELD** — store `d9a24282` → `cb38ef11`, exactly three deleted keys |
| P3 the indirect movers | **HELD** — v3.4 head 3917 → 3966 (+1.2510%, under the 3% bound) |
| P4 grace-A on as code default | **HELD** — `RL_GRACE=0` still byte-reproduces dial-off |
| P5 the curve's own numbers | **HELD on every measurable clause** — all 12 spot values, seam 56, tail 57–64, pick 64 = 179, non-increasing |
| P6 the conservation ledger | **HELD** — weighted `0.000e+00`, plain `+0.0000%`, int drift `−0.0029%` printed |

**Not landed, and blocked by this stop:** Step 3 (the curve wired), Step 4 (positional ND v0s),
Step 5 (pool v0s), Step 6 (the numéraire re-pin), Step 7 (the printed-day-0 assert) — and every
control that has to run **on the final board**: the identity gate, both no-arb instruments, the
mark-path progression, reverse no-arb, the deterministic double-build, the boot guard, the book
re-seal, and the pin restamp.

**The numéraire re-pin is blocked by the same stop, and it matters that it is:** `s` re-pins to the
curve's own pre-anchor head, so publishing a new `s` while the curve it measures cannot be installed
would be exactly the one-sided scaling `_load_numeraire` exists to prevent.

## 7. STATE AT THE STOP

| | |
|---|---|
| store | `cb38ef1171dcf20aae66ebf12682be0d` (unflagged — **moved and committed**) |
| board | `88ce647f531030d8d2e094188b258191` — **unmoved; nothing re-pinned** |
| `pvc_curve_v2.json` | `f6f3027fc56615fc77cd455638a5fa79` — **unmoved; the candidate is NOT installed** |
| `rl_model.py` | `cb78e0efe129fdcd9c02be5364db4aab` (grace default ON) |
| `data/model_config.json` | `config_sha256 … → eed19a75…` (RL_GRACE pinned) |
| the candidate curve | composed, scored, and left in evidence only — `curve_md5 48046e2b` |

The branch is in a **buildable** state: the engine on it builds a board (`0017657e…`, dial ON) because
the breaking artifact was never installed. The stop cost no work — every step below it is measured,
committed and pushed.
