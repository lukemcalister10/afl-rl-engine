# LEG B SEGMENT-5 — BLOCKER: the map-ON path cannot load (seg-4 wiring load-order defect)

**Status:** HALT-AND-ASK (mid-build, fence). Steps 0 (checkpoint) + 1 (A/B) PASS. Step 2 (the grid) is
blocked: no ON board can build, so β(s) cannot be measured at any grid point.

## What passed
- **A/B (step 1):** `RL_UNCOMP=0` board builds `8d90c9ac` **BYTE-EXACT** (verified). Default board too.
- **β_c (map OFF):** frozen fit_beta = **0.6219**, CI [0.4836, 0.7899], n=116 (matches memo §1 ~0.622).

## The defect
With the map **ON** (`RL_UNCOMP_S=s`, or once `UNCOMP_S_DEFAULT` is set), the engine fails at MODULE LOAD:

```
_merged_recover.py:358  ISO-table build:  raw = [raw_ev(synth(pk, ...)) for pk in PICKS]
_merged_recover.py:334  raw_ev -> _uncomp_prod(pr, p, Y, bb)
_merged_recover.py:311  _uncomp_prod guard:  ... or not _isreal(p): return pr
NameError: name '_isreal' is not defined
```

`_isreal` is defined at **line 491** (`_REAL = set(...); def _isreal(p): ...`), but the Leg-A ISO-table
build at **line 358** calls `raw_ev(synth(...))` 133 lines earlier. `_uncomp_prod`'s guard reads
`not _isreal(p)`:

- **map OFF** (`UNCOMP_S is None`): the guard **short-circuits** on `MA.UNCOMP_S is None` before ever
  reaching `_isreal` → no error → OFF board is byte-exact. This is why every OFF/inert build works.
- **map ON** (`UNCOMP_S=0.55`): the short-circuit no longer fires, so `_isreal(p)` is evaluated at
  load-time when it does not yet exist → hard `NameError` → the module never finishes importing → the
  board, the grid, the ledger, and every gate are blocked.

Confirmed on BOTH paths (not a harness artifact): `beta_measure.py` (truncated exec) AND `rl_export.py`
(the shipped board build) fail identically. The `print("=== AFTER"` split marker is at line 1447, well
after both 358 and 491, so the load order is identical to a normal import.

## Why seg-4 never caught it
Seg-4 HALTED at the λ pre-gate (item 245: "nothing selected; board/store/config unchanged"). Its
kernel-family diagnostic measured λ by calling `rho_out(p,pos)` **directly**, never through the map /
`raw_ev`. So the ON integration path (`_uncomp_prod` reached via the ISO build) was never exercised. The
map is BUILT but has never run ON.

## The map is genuinely inert during the ISO build regardless
The ISO table must be map-independent (a structural scaffold on synths). Two independent guards enforce
that: (1) `not _isreal(p)` — synths are non-real; (2) at line 358 the load-time reference dicts
(`_UC_VREFB`/`_UC_RHODEN`, built at line ~1342, AFTER the ISO build) are still empty, so line 313
(`if not Vb or not Rden: return pr`) returns identity anyway. So the ONLY problem is the premature
`_isreal` NAME lookup — there is no behavioural question, only load order.

## Minimal, behaviour-preserving fix options (need a supervisor ruling — OUT-of-fence)
- **Option A (recommended):** relocate the 2-line `_REAL`/`_isreal` definition (lines 490–491) to
  BEFORE the ISO-table build (before line 356). `_REAL` depends only on `MA.data` (available far
  earlier), so this is a pure move — `_uncomp_prod` and the ISO build are byte-unchanged; OFF board
  stays `8d90c9ac`.
- **Option B:** in `_uncomp_prod` (line 311), evaluate the reference-existence check (line 313, empty
  during the ISO build) BEFORE `not _isreal(p)`. One-line guard reorder; behaviour-identical (refs are
  built at runtime, so real players are unaffected).

Both leave the wired law's runtime behaviour identical and keep `RL_UNCOMP=0 == 8d90c9ac`. Option A does
not touch `_uncomp_prod` at all (cleanest w.r.t. "you do not redesign the wired law").

## Ask
Authorize a fix (Option A recommended) so the map can run ON, then I resume: the grid → s-selection →
the full return + all-804 ledger. This touches the wired-law MODULE, so per the fence it is a HALT.
