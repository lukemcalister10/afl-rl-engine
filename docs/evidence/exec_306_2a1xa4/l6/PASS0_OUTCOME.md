# #306 L6 PASS 0 ON THE REDESIGNED LENS LANE — **THE DERIVATION RAN. IT IS NOT THE FIXED POINT.**

**Seat `2a1xa4`, 2026-08-05.** Fire-order steps 5–7 under the channel ruling
([#306 comment 5186208519](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5186208519)).
Bake held; EXECUTION word withheld; nothing landed; no curve installed.

---

## 1 · THE VERDICT — R-I's fixed point, compared on FULL md5 per N22

```
derived   payload  FULL 9f7848f41d3b041b7397b5fe0d5d909a   [:8] 9f7848f4
installed payload  FULL e69a3f3816785f1be9bfc23688332d44   [:8] e69a3f38
EQUAL? False
```

**PASS 0 IS NOT THE FIXED POINT.** The curve derived from surface `b540833b` does not reproduce the
installed ruled curve `e69a3f38`. **62 of 64 picks differ.** Bound 4; this is pass 0 of 4; the loop is
not exhausted. **Nothing is declared.**

Input matrix `e1c62f8677e5714df1be4e91c960ec7c` (the committed `pass0_lens_matrix.json`), surface
`b540833b2e251631bf76aeec0040cc05`, store `81d24704`, basis STRUCTURAL / class cut 2022 / γ 1.0 VOR.

## 2 · WHERE THE DISAGREEMENT SITS — and it is the tail

| band | installed | derived | mean Δ | mean % |
|---|---|---|---|---|
| 1–10 | 20,998 | 20,785 | −21.3 | **−1.22%** |
| 11–20 | 11,550 | 11,478 | −7.2 | −0.61% |
| 21–30 | 7,868 | 7,753 | −11.5 | −1.51% |
| 31–45 | 8,231 | 8,013 | −14.5 | −2.74% |
| **46–64** | 6,075 | 5,649 | −22.4 | **−7.50%** |

Ladder total **54,722 → 53,678, −1,044 (−1.908%)**. Pick 1 unchanged at 3,000 (the pooled-numeraire
unit). **Pick 64: 221 → 189.**

**The gap is monotone in pick and concentrated in the tail** — the region L-A was built to constrain.
Read carefully and without over-claiming: this says the structural career values now want a *cheaper*
tail than the installed ruled ladder prices, having previously wanted the surface's tail ~64% *dearer*
than the curve. It is one pass, and a pass is not a trend.

## 3 · TRAJECTORY, FOR SHAPE ONLY

| state | payload | ladder | `s` | pooled head |
|---|---|---|---|---|
| installed ruled curve | `e69a3f38` | 54,722 | 0.977688 | 3068.4647 |
| #290 old-lane pass-0 derived | `1a8db02b` | 54,350 | 0.998224 | 3005.3384 |
| **#306 lens-lane pass-0 derived** | **`9f7848f4`** | **53,678** | **0.996637** | **3010.1221** |

`s` sits near 1.0 on both post-redesign lanes (0.9982 / 0.9966) against 0.9777 at the installed curve —
the pooled head is close to a true unit. That is a property of the numeraire policy, **not** evidence of
convergence, and must not be read as such.

## 4 · THE CHANNEL DECOMPOSITION — filed beside the verdict, as ruled

Per ruling 1, the wide-channel fact is part of what any "converged" would mean here. On this pass's
matrix, against the #290 pre-lens matrix (same store, same 1,197-row population, 0 keys added/dropped):

- Counted composition, re-measured: **825 concluded + 301 completed + 71 fallback = 1,197, share 5.931%.**
- Movement: `concluded_realised` **475/825 moved**, `completed` **292/301**, `prior_fallback_thin` **70/71**.
- **Total |Δ| 32,095.8 — the 71 counted rows carry 55.78%, the other 1,126 rows carry 44.22%.**
- Rows at 0 games and 1–5 games moved **exactly 0.00** (231 rows, hard-zeroed by `never_established`).

**Required caption, per ruling 4:** the two matrices differ in **both** surface (`fb9efdec` → `b540833b`)
**and** engine (`3c7b0c3c` → `15525b03`). These are the redesign's **total** effect and do **not**
attribute between the two. The separating measurement is ordered post-verdict.

## 5 · THE PASS-0 GATE FIGURE AND THE LANE EXPECTATION

- **G-Y0 = 0.035% ≤ 2.000% HARD**, n=1,326 over all 64 picks, on surface **`b540833b`** at installed
  curve `e69a3f38` — composition-weighted mean absolute gap, VOR-denominated. Measured by the `zlaarm`
  seat and reproduced **byte-identically** by the seam (comment 5185781133). **I did not re-measure it**:
  the substrate is unchanged, and the figure already carries two independent reproductions. Stated so the
  provenance is visible rather than implied.
- **Lane expectation — APPLICABLE and matched at this pass.** Key `basis md5(12) | anchor payload(8) |
  roster digest(12)` = `25a72f85a96b|e69a3f38|bce3c13d27ff`, recorded lens digest `b760b17ea3ab…`.
  The anchor payload at pass 0 is the installed `e69a3f38`, so the recorded key applies.
- **Lens-lane determinism re-proven on a third box:** `refit_v0surf.py --verify` on the lens substrate
  reproduced the baked pin **`b540833b2e251631bf76aeec0040cc05`** (98s) — L-B's passing direction,
  independently on this seat's box.
- **Note for pass 1:** installing `9f7848f4` moves the anchor payload, so the lane-expectation key becomes
  `…|9f7848f4|…` — **no recorded run exists for it and the assert will report INAPPLICABLE.** That is the
  instrument working as designed (*"inapplicable is not green"*), not a regression, and the new key's
  expectation is recorded at that pass rather than assumed.

## 6 · N35 — THREE CLASSIFICATIONS, THREE RESTARTS

The container restarted **three times** across this seat. Every classification was re-run before the next
engine act; all three reproduced `fb9efdec` on the pure pass-0 substrate (78s / 62s / 53s). Entry 3
immediately preceded this derivation. `ASSERT_LOG.md` carries them.

## 7 · SUBSTRATE — RESTORED AND PROVEN

- `per_entrant_271.json` **`2f8b4bd4` → `2f8b4bd4`**, restore proven by md5.
- Round trip: substrate minus the one authorised re-pin re-hashes to **`2b7640be`** exactly, after every act.
- `data/v0surf.pkl` unmoved at `b540833b`. Diff sections 20 (19 capture + the re-pin). **Nothing committed
  to the substrate; no curve installed.**

## 8 · WHERE I STOP, AND WHY

**Pass 1 requires INSTALLING curve `9f7848f4`.** The fire order is explicit: *"No install without returning
for the L1(b) enumerated same-commit set."* A curve install is not a file copy — it is the enumerated
identity set (curve artifact + numeraire block, `pool_value`, `stamp.statistic`, `stamp.store_md5`,
`stamp.per_entrant_md5`, the six FROZEN-RULER pins across `one_source_selftest.py` /
`ui/release_pick_curve.json` / `release_contract.pvc_provenance` + `contract_sha256`, then the refit, then
the `expected_boot.v0surf` re-pin inside Addendum C.1).

So I stop here and return for it, at exactly the boundary my two predecessors stopped at, for the reason
the order names.

**One downstream consequence the seam and the owner should see now rather than at the landing:** N43 binds
the ND-65+ pool cap to `curve[64]` explicitly live-and-breathe — *"if the curve moves, the cap moves"*.
Installed `curve[64]` is **221**; this pass derives **189**. The mechanism is already ruled and needs no
change; the **number** moves, and the signed level table would carry a different ND-65+ figure at a curve
that closes near here. Flagged, not acted on: N43's levels ship at the landing and are the owner's.
