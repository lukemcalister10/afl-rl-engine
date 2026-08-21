# THE 2026-08-21 UI ACT — CLAIMS, AND WHERE EACH ONE IS CHECKED

One UI seat, owner-ruled. **App logic only.** No engine act, no build, no build lock, no store read for
value, no carrier moved, no register entry, no push.

An engine landing ran concurrently and owns `engine/`, `data/`, `ui/data/*` and `tools/landing/`.
Nothing in this act touches any of them.

**IT MOVED THE BOARD UNDER THIS SEAT TWICE, AND THAT IS ITSELF A RESULT.** Mid-session it landed
`b3e8da99`, and then it **ABORTED and rolled back to `68be10c7`**
(`docs/evidence/staircase_adoption_2026-08-21/ABORT_gates.json`). Two consequences, both handled and
neither smoothed over:

- **The v0 sidecar went stale and refused itself** — which is the fail-closed pin doing exactly its
  job, on a real board move rather than a contrived one. It was regenerated on the restored board.
  v0 itself did not move (draft-time constant, store unchanged); only the live ratings beside it did.
- **Every figure in this directory was re-measured on the settled tree**, and every gate re-run. The
  first pass of `acceptance.runner` caught the tree mid-landing and read RED on `oneliner_r14_restore`;
  re-run on the settled tree that same check is PASS. **Do not read the mid-landing numbers into
  anything** — they are not in this directory.

| what | value |
|---|---|
| board of record at hand-back | `68be10c79d0ee096455754e084bcf757` |
| store | `b745002eb0a0fbb1c34fa44f1ef708d6` |
| files written | `ui/app/{board,card,config,movers,seam,trade,v0}.js` · `ui/index.html` · `ui/tools/gen_v0_sidecar.py` · `ui/data_aux/v0.js` · `ui/tests/ui_defects_2026-08-21.test.js` · `docs/proposals/ui_backlog/UI_PARKED_2026-08-21.md` · this directory |
| files deliberately NOT written | anything under `engine/`, `data/`, `ui/data/`, `tools/landing/`, `ui/styles/` |

---

## THE CLAIMS

Each claim is stated so it can be falsified, with the artifact that checks it. Where a check is a
measurement rather than an assertion, the measurement is in the file named.

### C1 — A from/to comparison never reports a player as DNP again
Participation is tri-state through ONE resolver (`core.participation`), read by the renderer, the
filter, the meta strip and the footer tally, so they cannot drift apart. The synthetic path emits
`played:null, dnp:null` — the ABSENT sentinel — where it emitted `dnp:false`, which was a claim.

**Checked:** `test_ui_defects_2026-08-21.txt` §(a), 17 assertions, incl. the negative — *"NOT ONE
synthetic row resolves to DNP"*. **Measured on the live R22→R23 view:** `fromto_scope.txt` — 804 of 804
rows read "not recorded"; every one of them rendered DNP before the fix.

### C2 — The trade translator never names a pick the curve cannot carry
Ceiling clamp with two rungs, both read off the shipped PVC, each stating the multiple of pick 1.

**Checked:** `test_ui_defects_2026-08-21.txt` §(b), exercised against the SHIPPED PVC (pick 1 = 3,000;
first round = 26,909). The blind reviewer's 11,376 now reads *"more than pick 1 (≈ 3.8× pick 1)"*.
An incomplete curve skips the round rung rather than guessing a total.

### C3 — No surface claims a `dRound` figure that does not exist, and no default column is dead
The name→key bridge is deleted; both false comments are retracted in place (quoted, then corrected, so
the belief cannot be rebuilt from them); `DELTA_BASE_DEFAULT` flips to the basis the board actually
carries; the unfed basis button disables itself **by measuring the loaded board**, so it re-lights
itself the day a writer lands rather than needing another edit.

**Checked:** `test_ui_defects_2026-08-21.txt` §(c). The final assertion is a measurement, not a pin:
*the DEFAULT Δ basis must be fed on the shipped board.* dRound 0/804 · vPrev 804/804.

### C4 — The attribution waterfall renders from the shipped data, and does not hide what it finds
Reads the shipped `{L1..L5}` dict. **The label map is sourced from two independent files, not invented**
— the certified chain generator that produced the sidecar, and the config inventory that names each
dial. Bars render in the chain's order, never sorted by size, because the register's own reading forbids
reading these as order-free.

**Checked:** `test_ui_defects_2026-08-21.txt` §(d) + `attribution_residual_finding.txt`.

> **C4 CARRIES A FINDING, AND IT IS THE MOST IMPORTANT LINE IN THIS DOCUMENT.**
> The certified lever split **no longer closes on the shipped board**: 802 of 804 rows carry a residual
> (median 151, p90 577, max 2,224). `export_attribution.json` is frozen at its certification era — its
> own `source` field names engine `2030e5df` / store `b0c39d78` — and the board has advanced several
> engine eras since, so every move after that certification lands in the residual by construction.
> DESIGN_DIRECTION §5 requires exactly what the panel now does: an explicit unattributed bar in alarm
> red, and words saying why. **Regenerating that sidecar on the current engine is an ENGINE-side item.
> It is now queued in the backlog. This seat did not attempt it** — it is outside a UI seat's domain and
> would move a file the concurrent landing owns.

### C5 — A ruled-wrong +1/+2 number cannot reach the screen
Not merely un-clickable: **unreachable.** `MD.config.LENS_DISABLED = [3,4]` declares it, `MD.lensClamp()`
enforces it, and the board applies the clamp at EVERY render — so a restored Back snapshot, a stale
value or any future caller is clamped to the default rather than trusted.

**Checked:** `test_ui_defects_2026-08-21.txt` §(2) — including the negative (−2/−1/Now are NOT disabled)
and the clamp round-trip. **Exercised live:** `smoke_render.txt` renders the board with `state.lens`
force-set to 3 and reports `lens after clamp = 2`.

**Not done, deliberately:** the rebuild. It is engine-side, rides the merged PVC+FLEX chapter, and stays
queued. Lifting the mitigation is emptying one list, on the owner's word, after the rebuild lands.

### C6 — The from/to page is narrowed, not amputated
Only the selector narrows. The comparator, the model-change labelling and every stored point remain, and
a bundle that cannot honour the scope falls back to the previous defaults rather than showing a wrong
pair.

**Checked:** `fromto_scope.txt` — 2 of 20 stored points offered; `core.compare` still answers
`(20,23)` and `(15,19)` with 804 rows each.

**One thing the owner should know, stated rather than left to be discovered:** R22 → R23 is **not a
single round**. Five out-of-round board moves sit between the two stored points, so the range is
labelled a model change and carries no played/DNP facts — value and rank movement across it are real and
complete. The participation-bearing view of R23 is the STORED report, whose baseline is the 20/8
injury-sheet re-cut rather than R22. Re-pointing the scope at that pair is changing one id in
`core.SCOPE`. **His call, not a seat's.**

**Recorded, not built:** the retrospective "every round since ingestion under today's model" view. It is
an ENGINE act, not a widened selector — this tab compares stored boards each priced by the model that
was live at the time, so widening it would label old models' answers as the live model's.

### C7 — Every player on the board has a v0, and it is the right one for him
Two populations, one engine function. `entry_anchor(p)` returns the frozen year-zero pick-surface value
for a numbered-pick entrant and the signed division entry level (#326) for a pool entrant, and the
generator records **which branch answered** so the surface labels the provenance instead of implying one
for both.

**Measured:** `v0_spotcheck.txt` — **804 rows = 561 pick-slot + 243 entry-anchor + 0 unrecoverable.**
**Nothing is dashed.** Pool entrants carry real anchors (Saad 258 → 439 = 1.70x; Caminiti 325 → 961 =
2.96x). This is the owner's correction, honoured: *"Pool entrants do have a v0 though? The moment they
are drafted, they have a value."*

### C8 — v0 is a slot belief, and the surface says so instead of ranking over it
**No ranking anywhere** — cut on the owner's corrected spec, not deferred pending a tie ruling.

**Measured:** `v0_spotcheck.txt` — the eight pick-5 mids (Cerra, Rozee, Parish, Stephens, Tsatas,
Ashcroft, Pendlebury, Setterfield) all carry **v0 2,218** to the dollar, while their live ratings run
from 341 to 3,686. Across the whole surface: 141 shared slots, **0 with more than one v0**. The card
states the sharing in words, once. A rank over that field would have manufactured order the model does
not have.

**The four figures, as the owner specified them** (*"v0 of 3200, live rating of 4000, would mean +800 /
1.25x"*): Daicos 2,640 → 9,892 = **+7,252 / 3.75x**; Reid 3,436 → 3,919 = **+483 / 1.14x**;
Pendlebury 2,218 → 341 = **−1,877 / 0.15x**.

### C9 — A stale v0 sidecar is refused, not honoured
`ownership.js`'s pin shape verbatim, against both identities, naming which one broke. A refused row
yields **no figure**: there is no second source for an entry price and none is invented.

**Checked:** `test_ui_defects_2026-08-21.txt` §(4) — the pin passes on the loaded board and is REFUSED
when the board is swapped. The board moving under this seat mid-session is exactly the failure this
guards, and it is why the bundle carries full md5s rather than an 8-char head.

**Route note:** the bundle is at **`ui/data_aux/`, not `ui/data/`**, which is a change from the backlog's
recommendation. `ui/data/` is landing-carrier territory (`tools/landing/carriers.py`); a bundle that is
not a landing carrier must not live inside the set a landing sweeps.

### C10 — The cohort clock is a fact read from the store, not a convention adopted from a sentence
The owner stated it; the store proves it. **MSD is the only entry type whose modal debut gap is 0**
(53 rows); every other type is +1.

**Measured:** `cohort_clock_derivation.txt` — the full per-type distribution over 2,650 store records,
then the rule applied to the shipped board: every MSD row inside the 2024 cohort carries draft year
2025, and no other. The derivation is carried verbatim in the control's own tooltip so nobody has to
find this file to read it.

### C11 — "Eligible to play KPF now" is answerable, and is a different question from "modelled as KPF"
Both controls are kept and labelled differently. **186 of 804 players are dual-eligible** and the
modelling axis cannot see dual eligibility at all — which is why one control cannot serve both.

**Checked:** `test_ui_defects_2026-08-21.txt` §(5), including that eligible-KPF is a superset of
modelled-KPF on the shipped board.

### C12 — The new filters and the column lens survive the universal Back
A filtered board that Back returns you to unfiltered is the same class of defect as a dead column that
does not say it is dead.

**Checked:** `test_ui_defects_2026-08-21.txt` §(5) — snapshot/restore round-trip.

---

## GATES

| gate | result |
|---|---|
| `ui/tests/ui_defects_2026-08-21.test.js` (new) | **116 / 116 PASS** |
| `ui/tests/counting_rule.test.js` | 24 / 24 |
| `ui/tests/club_totals_parity.test.js` | 17 / 17 |
| `ui/tests/release_seam.test.js` | 30 / 30 |
| `ui/tests/adoption_gate.test.js` | 3 / 3 |
| `ui/tests/movers.test.js` | **66 / 66 PASS** |
| `ui/tests/ownership_sidecar.test.js` | 22 / 35 — **PRE-EXISTING, NOT THIS ACT** (see below) |
| `ui/tests/ownership_single_source.test.js` | 15 / 17 — **PRE-EXISTING, NOT THIS ACT** (see below) |
| `acceptance.runner` (full profile, settled tree) | **GREEN — 16 PASS · 0 FAIL · 1 BLOCKED** (`lander_selftest`: no git worktree on this host — non-gating by contract, and not this act's to clear) |
| smoke render, every view, real app files | `smoke_render.txt` — all OK |
| `python3 doc_lint.py` on the backlog doc | 0 FAIL, 0 WARN |

**The two reds are proved not-mine, not asserted not-mine.** `baseline_preexisting_reds.txt` re-runs
all three suites with **every file this act touched reverted to HEAD**, then again with them restored:
identical counts both ways. `movers.test.js` is 66/66 either way on the settled tree — its 63/66 during
the session was the landing mid-flight, and it is recorded here only so nobody re-opens item 14 off a
stale reading.

**AND THE TWO THAT STAY RED CARRY A LIVE FINDING, NOT JUST A TEST ARTEFACT** —
`ownership_sidecar_stale_finding.txt`. `ui/data/ownership.js` is stamped board `a05fe951` / store
`cc02567f` / round 22, while the app is loaded on `68be10c7` / `b745002e` / round 23. The mirror pin
correctly REFUSES it, so every row falls back to the board's own store-derived `affl_team` — a degraded
display, never a wrong club, exactly as #283 designed. **But it means the live ownership lane is not
live right now:** any trade the owner authored into `docs/inputs/AFFL_Player_Locations.csv` after store
`cc02567f` is not being reflected. One command closes it (`ui/tools/ownership_store_apply.py`), and it
writes `ui/data/ownership.js` — a landing carrier, explicitly this seat's no-go zone. **Named, not
touched.**

**A second live finding, named and not touched:** `ui/data/ownership.js` — see
`ownership_sidecar_stale_finding.txt` and the paragraph above.

**Two suites could not be run at all:** `ui/tests/responsive_layout.test.mjs` and
`ui/tests/ui_222_items.test.mjs` both `require("playwright-core")`, which is not installed in this
environment. They were unrunnable before this act and are unrunnable after it; no screenshot or layout
assertion in this act rests on them, and the smoke render is the substitute — a real load of every
shipped file and a real render of every view, which catches the class of error those suites would.

---

## WHAT THIS ACT DID NOT DO, NAMED RATHER THAN COLLIDED WITH

1. **The +1/+2 LENS PROJECTION rebuild.** Engine-side, rides the merged PVC+FLEX chapter. Mitigated, not
   fixed. Queued.
2. **Regenerating `export_attribution.json`.** Engine-side, and it moves a file the landing owns.
   Surfaced by C4 and queued. The waterfall shows the consequence honestly meanwhile.
3. **The retrospective from/to view.** Owner-conditioned on model confidence, and it is an engine act.
   Recorded in code and in the backlog; deliberately not approximated.
4. **The public tier for v0.** The public bundle is leak-proof by construction and what rides it is a
   ruling. `MD.v0.status()` reports it as pending rather than deciding it.
5. **`ui/styles/matchday.css`.** Outside this seat's named domain. Where a disabled-control affordance
   needed a rule the stylesheet scopes to two segments, it is applied inline with a comment saying why,
   rather than widening a file this seat was not given.
6. **`ui/data/*`, `data/*`, `engine/*`, `tools/landing/*`.** Untouched, and the v0 sidecar was routed to
   a new path specifically to keep it that way.
7. **Any board field, any carrier, any pin, any register entry, any push.**
