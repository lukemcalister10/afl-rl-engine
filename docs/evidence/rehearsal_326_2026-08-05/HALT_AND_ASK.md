# #326 rehearsal — HALT-and-ask items

Two findings where the directive as amended and the code on live bytes do not agree. Neither was worked
around; both are recorded with the measurement that establishes them.

---

## HALT 1 — the site the directive names is not on the board's price path

**The directive (addendum 1 item 2, seam-verified "on live bytes"):** the per-player pool price resolves
through `rl_model.py`'s ladder object read by the two per-player consumers (`unpl_eq` and `pedestal`,
via `min(ep,70)`); the other copies are scaffold.

**On live bytes:** `rl_model.value()` — which is where `unpl_eq` and `pedestal` live — does not set any
exported player price. `rl_export.py` **overwrites** `_v`, `_vP1`, `_vP2`, `_vM1`, `_vM2` and `_cvx` from
the engine's gated `ev()` before `player_rec` reads them:

```
rl_export.py:191   _r = _ev(_p, 2026); _raw2026[_p['key']] = _r; _p['_v'] = _nb(_r)
rl_export.py:198   _p['_vP1'], _p['_vP2'] = _nb(_ev(_p, 2027)), _nb(_ev(_p, 2028))
rl_export.py:220   _p['_v'] = _p['_vM2'] = _p['_vM1'] = _p['_vP1'] = _p['_vP2'] = _nb(_ev(_p, 2026))
rl_export.py:221   _p['_cvx'] = 1.0
```

`ev()` (`_merged_recover.py:1783`) is a separate valuation chain (`b6`/`price6`/`par_pole`/`recover`,
times `iso_eff`, floored on `v0_start`). It never calls `MA.value()`. `MA.value` has no caller anywhere in
`_merged_recover.py` or `rl_export.py`.

**Measurement.** With the #326 lookup installed, moving a signed level by +50% and re-pricing:

| level | active entrants | board prices that move | `value()` results that move |
|---|---|---|---|
| MSD | 63 | **0** | 45 |
| SSP | 28 | **0** | 19 |
| ND65+ | 28 | **0** | 7 |
| PDN | 16 | **0** | 11 |
| PDA | 15 | **0** | 9 |
| IRE | 14 | **0** | 8 |
| UNR | 13 | **0** | 9 |
| RD:SD | 16 | **0** | 1 |
| RD:SF | 15 | **0** | 4 |
| RD:MID | 12 | **0** | 8 |
| RD:RUCK | 9 | **0** | 3 |
| RD:KPD | 8 | **0** | 2 |
| RD:KPF | 6 | **0** | 1 |
| PDS | 0 (store tier) | n/a | **0 of 21 store rows** |

Whole-board confirmation: the rehearsed board `5d1e0709` differs from the pre-change board `2b7c1a00` in
**zero** player values — 0 movers, 0 added, 0 dropped, no field on any row differs. The only difference is
the ORDER of the `active` array (339 of 804 positions), because `rl_model` sorts `players` by the
pre-overwrite `value()` figure.

**Consequence.** The reach-the-price acceptance (addendum 2 item 1, two-tiered by addendum 3 item 1)
cannot pass as directed: all 14 signed levels are installed, read verbatim, correctly resolved — and
reach no board price. This is exactly the vacuity class the acceptance exists to catch, and the catch
worked. The selftest is left RED on all 14 rather than weakened.

**PDS additionally fails its own off-board tier for a second, independent reason:** all 21 rows are
2007-2011 and `decay = max(0, 1-(seasons-1)/4.5)` is 0 for them, so `pedestal` is 0 and the level cannot
bind even inside `value()`. The store-population tier as written is unsatisfiable for PDS today.

**What is being asked.** Whether the lookup should move to where the board price actually resolves —
`_merged_recover.py`'s `ev()` chain. That file is `engine_head`, pinned at `15525b03` in
`data/expected_boot.json` and `data/release_contract.json`, asserted by Guard 5 and N44, and held constant
by both committed attribution instruments. Moving it is a materially larger act than this directive
scopes, with its own re-pinning and its own audit. Not taken unilaterally.

---

## HALT 2 — `pool_value` still sets 12 board prices, all through the site the audit classified as scaffold

**The directive (addendum 1 item 3, as corrected by addendum 2 item 3):** after this change no player
price may read `pool_value`.

**On live bytes:** `_merged_recover.py:1806` `draftval(p) = float(_PVC0[min(effpk(p), KMAX)])` returns the
pool slot for every pool entrant, and feeds the ruck prior cap at `:1180`, `:1184` and `:1703`
(`RUC_PRIOR_CAP*draftval(p)*_ruc_head_v0(p)`). The pre-fire audit called `_PVC0` "a local copy … the cap
and scaffold basis", i.e. not a price. It is a price for rucks.

**Measurement** (two full builds, identical except `pool_value` 237.2 → 400.0, surface refit on both sides
so the surface is not a confound; `RL_LEGF=0` because the entrant layer's sealed total halts on any pool
move):

```
pool_value 237.2 -> 400.0 : 12 board prices move, ALL RUCK
  flynn-riley  MSD 295->471 · caleb-may MSD 263->444 · alex-van-wyk MSD 263->444 · max-mapley MSD 263->444
  iliro-smit   MSD 187->316 · vigo-visentini RD 187->316 · aiden-riddle RD 201->340 · joe-pike RD 201->340
  liam-reidy   RD  315->483 · logan-smith ND 201->340 · patrick-carr UNR 263->444
  jaime-uhr-henry UNR 201->340
```

Two of the twelve move under runtime perturbation alone (Flynn Riley, Liam Reidy); the other ten move only
across a rebuild, because the rest of the path runs through the frozen year-zero surface, whose signature
is curve-sensitive.

The selftest carries this as a live check — `#326 no board price follows the ladder's pool slot` — which
is RED on 2 rows today and would be RED on all 12 under a rebuild-scoped probe.

**What is being asked.** Whether the ruck prior cap is in scope: it is the same site as HALT 1, so both
questions are answered by the same decision about `_merged_recover.py`.

---

## Not a halt, recorded for the filing

* **Counts.** The engine's own view of the corrected store `f1e8c9fe` gives RD **691** rows
  (KPD 72 · MID 176 · RUCK 71 · SD 158 · SF 149 · KPF 65) and ND65+ **122**, against the signed
  measurement n of 693 / 120-121. Addendum 1 already rules the signed n is the measurement population and
  never a row-count assert, so nothing asserts on it. The discriminator counts reproduce the record
  exactly: **171** present-differing and **181** drafted-differing rookie rows, **7** of the drafted case
  active on the board, **0** of the present case.
* **PSD.** Zero rows in the live store; the nine `type` values present are exactly the signed eight plus
  ND. The halt clause for an engine-pool row outside the signed set is installed and exercised by the
  same code path as the ND halt.
* **The stale seal assert in `ui/tests/extract_seam.test.py`** is known and was not touched.
