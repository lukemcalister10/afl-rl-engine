# CONSTRAINTS — the single-source registry of guards and acceptance anchors — v1.10 · 2026-07-13 · supersedes v1.9
### CHANGELOG v1.10 (2026-07-13): **THE A-PAIRS BANDS ARE OWNER-RULED** (owner: "Bands okay").
### They were PENDING-OWNER for one turn; they are now BINDING as bands, and auditors SCORE against
### them: pair 2 |Δ| ≤ 10% (currently +3.2% — PASS) · pair 3 bont ABOVE sanders by 0–10% (currently
### sanders +13.7% the WRONG WAY — FAIL, the standing failed read). Everything else in v1.9 carries
### VERBATIM, including the guards, the v1.9 A-PAIRS filing, and the pair-3 diagnosis (item 44: the
### gap is BASE-CURVE, not flattery; it belongs to the PVC re-derivation; NO HAND EDIT).
### STATUS: OFFICIAL. v1.8's content carries VERBATIM except PART 2 / A-PAIRS below.
### CHANGELOG v1.9 (2026-07-13, supervisor pen at the owner's word):
### **A-PAIRS — THE YOUNG GUN, NAMED AT LAST.** The owner named BOTH sides of the runway-weighting
### test (his words: "Let's do Reid and Sanders. Both different players that offer a different kind
### of comparison to Bont" · "I feel like Harley and Bont can be similar, but interestingly I'd
### think Bont should be slightly above Sanders" · "Harley Reid, confirmed"). `young_gun_tbd` is
### RETIRED — the placeholder that has stood since the anchor was written is now two live reads:
###   PAIR 2  harley-reid  vs marcus-bontempelli — read: **SIMILAR / PARITY**
###   PAIR 3  ryley-sanders vs marcus-bontempelli — read: **BONT SLIGHTLY ABOVE SANDERS**
### KEY-VERIFIED against the source store before filing (the store carries TEN 'Reid' rows; the
### toby-briggs drift began exactly this way): `harley-reid` = Harley Reid, MID, pick 1, West Coast,
### b.2005 (NOT `murphy-reid`, GEN_FWD, pick 17) · `ryley-sanders` = Ryley Sanders, MID, pick 6,
### Western Bulldogs, b.2005.
### ⚠ **PAIR 3 FAILS ON THE CURRENT BOARD — and that is the anchor doing its job.** Measured on the
### TAGGED board (v2.9 = 9f8ae76, board 81e48293): bont **3,482** · harley-reid **3,594 (+3.2%)** ·
### ryley-sanders **3,960 (+13.7%)**. Pair 2 sits where the owner reads it. Pair 3 sits the WRONG
### WAY ROUND by ~14%: the model prices a pick-6 mid with 47 games materially ABOVE the best proven
### player in the competition, and the owner reads Bont ahead of him.
### **WHERE THE GAP IS NOT: flattery.** Decomposition (flattery census @ d6c481f, quoted in the
### numéraire): sanders = base **3,903** + iso 58 + par credit **0** (flat −21 ≈ nil) · bont = base
### **3,070** + par credit **+439** + iso −28 (flat −29 ≈ nil). Neither player carries par-relative
### flattery, so THE FLATTERY FIX WILL NOT CLOSE THIS. The gap is made by the BASE CURVE — the
### pick-band price × growth on the young side — which places it in the **PVC re-derivation /
### pricing-curve formalisation** chapter (and adjacent to G-CONVEX's young premium), NOT in the
### flattery chapter. Supervisor recommendation: carry pair 3 as a STANDING FAILED READ and make it
### an acceptance anchor OF that chapter. NO HAND EDIT: cutting Sanders to satisfy the read would be
### a predicate-based nerf wearing a rule's clothes (owner's own remediation doctrine, G-COHORT).
### BANDS: **OWNER-RULED at v1.10** (see the v1.10 changelog above).
### All other guards, anchors, flags, laws, and the change discipline carry VERBATIM from v1.8,
### including: the numéraire fold (pick-1 == 3000) · B1 conformance (July-8 construction IS the
### gate; indexed reading demoted) · A-DARCY −664 · G-CONVEX floors + seam verification · G-Y0
### PENDING-OWNER · the LENS PROJECTION and CYCLE laws · the stray-file obituary.
### Machine twin: acceptance_v1.9.json — regenerated from this file at filing.

## PART 1 — GUARDS
Carried VERBATIM from v1.8 (G-COHORT · G-MONO · G-FLOOR · G-PEAK · G-CONVEX · G-DATA · G-ATTR ·
G-Y0), including v1.8's measurements and provenance. NOTHING in Part 1 changed at v1.9.

## PART 2 — ACCEPTANCE ANCHORS — v1.9 amendment (A-PAIRS ONLY; all other anchors verbatim from v1.8)

### A-PAIRS — the runway-weighting test — OWNER_ON_SIGHT
| pair | left | right | owner's read (VERBATIM direction) | measured, tagged board 81e48293 | status |
|---|---|---|---|---|---|
| 1 | max-gawn | kieren-briggs | clearly above | (carries from v1.8) | PASS |
| 2 | **harley-reid** | marcus-bontempelli | **"Harley and Bont can be similar"** → PARITY | reid 3,594 vs bont 3,482 = **+3.2%** | **PASS (consistent with the read)** |
| 3 | **ryley-sanders** | marcus-bontempelli | **"Bont should be slightly above Sanders"** → bont > sanders | sanders 3,960 vs bont 3,482 = **+13.7% the WRONG WAY** | **FAILS — standing failed read** |

**WHAT THE TWO PAIRS TEST** (they are deliberately different questions — the owner's framing):
- **Pair 2 is the knife-edge.** Pick 1, 52 games: real production AND real runway, and the model has
  it at a coin-flip. It asks whether runway beats proven AT PARITY.
- **Pair 3 is the premium test.** It asks whether the model's young-side premium is over-cooked. It
  is the bolder claim and it is the one that broke.

**THE BANDS — OWNER-RULED 2026-07-13 ("Bands okay") — BINDING AS BANDS:**
- Pair 2 (PARITY): |v(harley-reid) / v(marcus-bontempelli) − 1| ≤ **10%**. Currently +3.2% — PASS.
- Pair 3 (BONT ABOVE, "slightly"): v(marcus-bontempelli) > v(ryley-sanders), with the gap in
  **0–10%**. Currently sanders is +13.7% ABOVE — a breach of ~14–24 points. Closing it means Sanders
  landing in roughly **3,165–3,482** (a fall of ~478–795 SCAR) OR Bont rising to meet him — and
  WHICH of those two is the correct mechanism is precisely what the PVC re-derivation must answer.
  **It is not the supervisor's to choose and it is not a build's to tune.**

**AUDITOR INSTRUCTION — CHANGED.** The standing "SKIP PAIR 2 AND REPORT THE SKIP" is RETIRED. Both
pairs are now live: score them, report direction and magnitude, and expect pair 3 to FAIL until the
pricing curve is re-derived. A pair-3 failure is EXPECTED until the pricing curve is re-derived; report it and SCORE it against the band — it is not a bake blocker on its own (A-PAIRS is OWNER_ON_SIGHT), but it must never again be reported as a skip.

## PART 3 (flags) + PART 4 — carry VERBATIM from v1.8.

## CHANGE DISCIPLINE — verbatim from v1.8. On filing: regenerate acceptance_v1.9.json, bump both,
## archive v1.8, update the manifest pointer.
