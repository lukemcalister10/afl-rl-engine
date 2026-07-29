# FINDING — the vocabulary rename cannot complete a board build: v0surf frozen-signature HALT

**Status: STOP-and-report. No workaround applied.** Per the seam pre-fire audit point 2 on issue
#262: *"If the board regeneration HALTs at the v0surf frozen-signature gate, that is a
STOP-and-report, not a workaround… Never bake a new signature, never restore a fallback. Corollary:
the value-invariance proof requires a completed build — if the build cannot complete, the landing does
not merge."*

Nothing was refitted, re-baked, or fallen back to. `RL_V0SURF_REFIT` was not set.

---

## What happened

Stage 1 of the migration — the vocabulary replacement ALONE, no owner edits, no per-season data —
was applied and re-pinned, and the build halts:

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature 8faa737b18f575d4cbf3dad750fa2188
is NOT in data/v0surf.pkl (frozen: 1cbaf33de27ad9a2ccadf7cc98f57314,
                                   76498b5a7a7a80db17f5bb9748ff1492).
```

## Why — the exact mechanism

`engine/rl_after/_merged_recover.py:1286-1292`:

```python
def _v0surf_sig(real):
    _curve=_PVC0 if '_PVC0' in globals() else MA.PVC
    _payload={'pvc':    sorted((int(k),int(v)) for k,v in _curve.items()),
              'roster': sorted([str(MA.gfut(p)), _ageR(p), int(p.get('pick'))] for p in real),
              'gates':  {g:os.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    return _hl.md5(_js.dumps(_payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
```

The `roster` term hashes **`str(MA.gfut(p))` — the position group LABEL STRING** for every player in
the national-curve sample. `gfut()` returned `GEN_DEF` / `KEY_FWD` / `RUC` before the rename and
returns `SD` / `KPF` / `RUCK` after it.

So the signature moves **by construction** under any vocabulary replacement. The three payload terms
behave as follows:

| term | moved by the rename? | why |
|---|---|---|
| `pvc` | **no** | integers only — pick → value |
| `gates` | **no** | env var *names* (`RL_RUC_PRIOR_CAP` …) contain `RUC` only inside a longer identifier, so the word-boundary rename never touched them — verified |
| `roster` | **YES** | carries the label string; `_ageR` and `pick` are unchanged |

The grouping itself is identical — the same players fall in the same buckets in the same order. Only
the spelling of the bucket changed. But the signature is an md5 over the spelling, so it moves.

## This is the gate working as designed

`docs/CURRENT_STATE.md` v26: *"`v0surf` HALTs on an unknown config signature. That is the design."*
It is doing exactly its job — it cannot tell a semantically inert relabel from a real config change,
and it is built to refuse rather than guess. The HALT is correct behaviour, not a defect.

## Why it blocks the whole landing

Acceptance criterion 3 requires the regenerated board to be byte-identical modulo the relabel, proven
by a relabel-aware diff. That proof needs a completed build. The build cannot complete while the
signature is unknown. Therefore:

- stage 1 (rename only, must show zero movers) — **cannot be proven**
- stage 2 (the owner's 43+12+1+2 edits, movers reported and attributed) — **cannot be reached**

The baseline instrument is sound and was verified before any edit: a clean build off unmodified `main`
reproduces the pinned board `750446d74e7c5d6edeb132168db53259` **byte-exact**. So the halt is
attributable to the rename and nothing else in the environment.

## What is NOT the answer

- **Re-baking v0surf** (`RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 … refit_v0surf.py --bake`) — the HALT
  message offers this for *"if the config CHANGED deliberately"*. It is owner-word territory and is
  explicitly outside this seat's directive.
- **Restoring the fallback** — removed by owner word 2026-07-28, for the reason the message states.
- **Widening the accepted signature set** — issue #262 hazards: *"never widen the accepted set."*

## Options for the owner — none taken

1. **Re-bake the v0surf freeze under the new vocabulary, on a clean instance.** The configuration is
   genuinely unchanged apart from spelling, so the refitted surface should be numerically identical;
   that is checkable by comparing the refitted surface to the frozen one cell by cell before anything
   is pinned. Needs an owner word and probably belongs in the same commit as the landing.
2. **Make the signature vocabulary-invariant** — canonicalise the label before hashing, so a pure
   relabel cannot move it. This is an engine behaviour change, and the directive forbids this seat
   changing engine behaviour, so it would need to be commissioned.
3. **Land the rename without a rebuilt board**, deferring the board to the re-derivation job. This
   contradicts acceptance criterion 3 as written and would leave the shipped board's labels
   inconsistent with the store's.

**Recommendation: option 1**, with the refitted-vs-frozen surface compared numerically before pinning
— it keeps the freeze meaningful, keeps the engine unchanged, and the comparison is itself the proof
that the rename was inert. It needs the owner's word, which is why this stops here.

## Offered next step, not taken without a word

The claim *"only the label moved"* is directly checkable: recompute `_v0surf_sig`'s payload with the
new store and map the new labels back to the old spelling. If that reproduces `1cbaf33d…` or
`76498b5a…` exactly, the rename is proven inert at this boundary. That is a read-only diagnostic and
produces no shippable artifact — but it means reaching into the signature function, so it is not being
done unasked.

---

## State of the branch at this finding

Stage 1 is applied and committed so the work is not lost. It is **not proven** and must not merge as
is.

| | |
|---|---|
| store `rl_model_data.json` | `e3aaba77` → `ce997903` · 6,365 position values remapped · **0 non-position fields moved, 0 scoring arrays touched, 0 key-set changes** (verified against `git show HEAD:`) |
| vocabulary in the store | exactly the six new codes, nothing else |
| engine sources | 11 files · `rl_model.py`, `pgrid.py`, `_merged_recover.py`, `rl_export.py`, 7 × `forward_valuation` |
| engine data tables | 5 files · `params`, `rl_passmark`, `bust_prior`, `lti_return`, `ycred` |
| re-pinned in `expected_boot.json` | `store`, `rl_model`, `engine_head`, `fv`, **`bust_prior`** |
| still to re-pin (blocked on a build) | `board`, and all of `release_contract.json` incl. `held_candidates` |
| diff shape | 124 insertions / 124 deletions — balanced, the signature of a pure rename |

`bust_prior` was not named in the directive or the seam audit as a moved identity; Guard 5 caught it.
It is a **sixth** pin beyond the five the audit enumerated, and any future vocabulary work should
expect it.
