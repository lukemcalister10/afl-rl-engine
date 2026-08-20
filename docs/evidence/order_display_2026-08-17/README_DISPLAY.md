# DISPLAY SEAT (issue #334) — LOTTERY_DIAL_V2.html: the two ceilings, kept apart

**Display-only seat, READ-ONLY on the engine and the board.** No engine file, law constant, no-arb
instrument, board or emit was touched — this seat only reads two committed artefacts and writes one
self-contained HTML page. `WQ6` stays sealed at `[0.18 ×5, 0.10]`; the λ dial is still a lens over the
S6 emit and never re-enters the pricing path. S6's original page is untouched
(`S6_LOTTERY_DIAL.html` md5 `6ce21187…`, unchanged at this commit).

## The defect

The sixth scenario column was headed **"S6 q97"**. It is not a career ceiling — it is
`sp[5] = anchor_pts + rho × six_phat[5]`, **today's board price re-weighted onto the top scenario**,
with `(1 − rho)` of it still sitting on the pedigree leg that the scenario never moves. On nick-madden
(rho 0.345) that printed **1,388**, and 1,388 was read against realized careers in the thousands. Per
`PACKET_W6.md` §3 and §7.4, that mislabel is a substantial part of the owner's catch.

## What the page does about it

| # | change | where |
|---|---|---|
| 1 | sixth scenario column relabelled **"Price if ceiling lands"** (tooltip: *a PRICE, not a career*); the ▼ markers on the 341 tapered-inversion rows are kept exactly as they were | table header + `.sc` cells |
| 2 | new **"His ceiling, career value"** column = `six_raw[5]`, the engine's own career value at that same top scenario — the like-for-like number, in career units | new column, sortable |
| 3 | new **"Measured ceiling · top 3% like him"** column = the realized **q97 career delivered value** of the row's own S7 cell (ND rows: pick band × position; pool rows: pathway arm), with the count of finished careers printed on every cell | new column, sortable |
| 4 | plain-language explainer box distinguishing the three numbers, with the madden row worked through | `.box.fix`, above the existing caveat box |
| 5 | λ = 0 ≡ board assertion badge, every pre-existing column, every sort, the dial and the filters: unchanged | — |

**Thin cells are never printed as a naked number.** Where the cell's q97 does not resolve
(`BOUND(max)` under S7's rule "level f resolved iff n(1−f) ≥ 1"), the cell prints `≥ value *` with its
`n` — **361 of 804 rows**. Where a row's own ND cell has n < 8 (S7 publishes no fan at all there:
RUCK 1-10 n=7, RUCK 21-30 n=5) the band's all-positions row is shown instead and the cell says so —
**5 rows**. **28 ND rows were picked beyond 64**, where the measured history stops; they use the 41-64
band and carry that note. No row prints NaN, `undefined` or `null` under any sort (asserted).

## Two honesties carried on the page

- The measured column is **unconditional** — it knows the route a player came in by, not how he is
  playing now. A player already getting games at a good level is not the median of his own entry cell.
- The two career columns share a **scale** (board points of delivered career) but not a **ruler**: one
  is the engine's scenario valuation, the other a measured grace-A career total (W6's "scale-cousin").
  The page says to read the gap as a bearing, not a decimal.

## Verification (headless, node + DOM shim — the route S6 took)

`node docs/evidence/order_display_2026-08-17/verify_dial_v2.js` → **62/62 checks pass**
(transcript: `V2_VERIFY_out.txt`). It asserts: the page's own λ=0 badge goes green and the identity
holds to 1.8e-12 (~2 ulp, the page's own 5e-4 bound); at λ=0 the board reads **666,913** with **0 of
804** rows moving rank; all **22** headers sort in **both** directions with all 804 rows retained; the
two new columns sort **numerically** (top value is the true maximum, not a string max); madden's row
shows the corrected pairing; no NaN/undefined/null in any cell under any sort; the ▼ markers sit on
exactly the 341 emit-flagged rows; λ=±1.2 reproduce the S6 README totals 947,934 / 458,634 and reset
returns the board exactly; the file is fully self-contained (no external src/href, no `url()`, no
fetch/XHR/import).

## Files

| path | what |
|---|---|
| `build_dial_v2.py` | the builder (no engine import; reads the two committed inputs only) |
| `LOTTERY_DIAL_V2.html` | **the owner page**, self-contained, md5 `0721d353…` |
| `verify_dial_v2.js` | the headless verifier |
| `V2_VERIFY_out.txt` | build + verification transcript |

Inputs: `docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json` (`c4338a9b…`) ·
`docs/evidence/order32_s7_2026-08-17/CELLFANS_S7.json` (`a95615c3…`) ·
recommendations from `docs/evidence/order33_w6_2026-08-17/PACKET_W6.md` §7.4.

Reproduce (deterministic, no engine, seconds):

```bash
python3 docs/evidence/order_display_2026-08-17/build_dial_v2.py
node       docs/evidence/order_display_2026-08-17/verify_dial_v2.js
```
