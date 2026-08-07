# Stage ER — self-test re-point enumeration

## The enumeration is EMPTY. Zero expectations were re-pointed.

```
$ python3 one_source_selftest.py
...
SELF-TEST PASSED: single source; guards 1-3; board==engine (F1); book==board (F2);
  Kako+Bontempelli ground-truth; DPP blend stripped; Leg B L-RECENCY + rho forbidden-list
  (R105.5/R105.4); collision sentry (King pair) clean.

EXIT = 0
PASS assertions: 146
FAIL assertions: 0
```

Full transcript: `selftest_full_output.txt` (228 lines).

The brief allowed for re-pointing any expectation that legitimately moves with the era removal,
one line each. **No such expectation exists.** Not one assertion had to be touched, and nothing
was edited in `one_source_selftest.py` — the file is byte-identical to `4d435ea`:

```
$ git diff --stat engine/rl_after/one_source_selftest.py
(no output)
```

## Why nothing moved — checked, not assumed

* The self-test carries **no era-dependent hardcoded number**. Its `grep` surface for `era` is two
  hits and both are innocuous: line 606 is print text using "era" in the ordinary-English sense,
  and the `REFIT` matches at 690-707 are the `RL_V0SURF_REFIT` no-silent-refit guard.
* Its named ground-truth fixtures (Kako, Bontempelli, the King collision pair, the item-284 DPP
  fixtures, the fourteen #326 entry-level reach-the-price rows) are **not among the 28 movers** —
  every mover is a KPF and none of the fixtures is one.
* The structural assertions it makes are **relations, not levels**: board == engine `ev()` (F1),
  book == board (F2), single-source/lookalike guards, the L-RECENCY and rho forbidden-list
  invariants, the collision sentry. Removing a multiplier that is applied identically on both
  sides of each relation cannot break any of them.

## The other two gates, for the record

| gate | result |
|---|---|
| `rl_export.py` PARITY GATE | **PASS** — all 804 active board values == engine gated `ev()`, matched by key, `eps=0` |
| `rl_export.py` NUMERAIRE GUARD | **PASS** — shipped pick-1 = 3000 |
| `rl_export.py` FUT-LABEL assertion | **PASS** — 87 dual rows carry the true primary/alternate |
| `rl_export.py` ZERO-EMPTY-CLUB | **PASS** — 0 blank club across 1002 exported rows |
| `s4_matrix_M1v7.py` BOOK<->BOARD PARITY GATE | **PASS** — all 802 shared board players' present value == `round(book cur / 1.0524)`; 2 outside the cohort book (`_pvc_exclude`: adam-treloar, jeremy-cameron) |
| Guard 5 (boot) | **PASS** — store 37ced3ce, rl_model b35c5521, fv 0976195c, all == pinned |
| v0surf freeze | **loaded frozen, no refit** — see below |

## The frozen year-zero surface did NOT halt

The brief flagged a possible halt if an engine-code change participates in the v0surf config
signature. It does not, and this was verified by reading the signature rather than by hoping:

```python
def _v0surf_sig(real):
    _payload={'pvc':    sorted((int(k),int(v)) for k,v in _curve.items()),
              'roster': sorted([str(MA.gfut(p)),_ageR(p),int(p.get('pick'))] for p in real),
              'gates':  {g:os.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    return md5(...)
```

The signature is made of (1) the active pick curve, (2) the roster's position/draft-age/pick, and
(3) the `_V0SURF_GATES` environment keys. **No engine source hash participates.** The pick curve was
restored to its stage-1 content by step 1, the roster is store-driven (store unmoved at 37ced3ce),
and no gate env var changed. The surface loaded from the freeze as normal — `data/v0surf.pkl` is
untouched this stage and its pin `d594dc03` is unmoved.
