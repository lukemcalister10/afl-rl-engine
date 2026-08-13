# ORDER 27 — FLAGS FOR THE OWNER

The register-wide standing-rulings sweep you commissioned on 2026-08-13. I read the whole register,
pulled out every owner ruling I could find, sorted them, and checked the standing ones against the
actual code and data.

**190 rulings found. 12 things need your attention.** Everything else is either working, already
done, parked on your own word, or superseded by a later ruling of yours.

Nothing was changed. No code was touched. I picked no winners between colliding rulings.

The short version: **the three cases you already caught this week are a class, and the class has more
members.** The pattern is always the same — a ruling lands as data or as a one-off act, and nothing in
the machinery stops the next act from forgetting it.

---

## SEVERITY 1 — the machinery does the opposite of the ruling

### FLAG 1 — Cameron, Shiel and Treloar are still excluded from the pick curve, though you ruled them IN

**Your ruling (register v533, 2026-07-29):** *"INCLUDE Jeremy Cameron, Dylan Shiel, Adam Treloar in
the PVC going forward — GWS-concession entries."* You then closed the open detail at v534 by
assigning them notional draft picks in your own sheet — *"where they would have gone if
draft-eligible; transcribe as given."*

**Where it should bite:** the pick-curve teaching population — every place a career teaches what a
pick is worth.

**What the machinery actually does:** the data half of your ruling landed — the store now carries the
notional picks you assigned (Shiel ND 2011 pick 4, Cameron pick 12, Treloar pick 14). The machinery
half did not. All three still carry `_pvc_exclude: true` in the landed store, and `_pvc_exclude` is
exactly the flag that drops a row from the pick-curve builders:

- `engine/rl_after/rl_model.py:284-296` — *"players flagged `_pvc_exclude` are dropped from the
  PICK-CURVE builders (build_pvc / build_pvc_v34 / _natcv34)"*, with the same slide-up mechanism
  applied to fill their vacated slots.
- `session_2026-07-29/item271/emit_matrix_271.py:89` and
  `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:119` — both derivation instruments filter
  `not p.get('_pvc_exclude')` out of the teaching population.

So you assigned them picks so they could teach the curve, and they are still the only three players in
the store mechanically prevented from teaching it. The flag is a leftover from the era when they were
concession entries with no pick.

**The open question:** was the INCLUDE ruling meant to clear `_pvc_exclude`, or did you intend the
notional picks for some other purpose while keeping them out of the fit? If the former, three store
rows and one re-derivation close it.

---

### FLAG 2 — the position-field gate you asked for was never built, and 341 rows would fail it

**Your ruling (register v502, 2026-07-27):** you rejected a one-off patch as *"a bandaid [that]
doesn't correct the issue if it arises again"* and asked for a durable rule. The ruled form:
**future_position == present_position for every player UNLESS he carries a declared blend or appears
on a declared-exception list** — an asserted invariant that *"FAILS LOUDLY the moment an edit pass
moves one field without its partner."* Direction sealed at v503: *"future can follow present"* — a
corrected fact carries the forecast; a forecast never rewrites the fact.

**Where it should bite:** every store edit pass, as a build-time check.

**What the machinery actually does:** the gate does not exist. I searched the whole tree for any check
comparing the two fields; `one_source_selftest.py:223-246` checks that `future_position` is in the
vocabulary and that there is at most one alternate — nothing more.

Measured on the landed store today (`tools/probe_v502.py`): **341 rows carry present ≠ future, and
none of them carries a declared blend.** 340 are retired, 13 are on the back board, 1 is on the active
board (`oskar-baker`, MID → SF).

The live-board exposure is genuinely small — which is probably why nobody noticed. But the register
recorded at v505 that the D1 re-stage was withdrawn and *"WHAT SURVIVES is the GATE (v502)"*. The gate
is the only thing that was supposed to survive, and it is the thing that did not.

**The open question:** do you still want the invariant asserted? If yes it is a small check plus a
declared-exception list; the 341 rows would need dispositioning (most are retired and inert).

---

### FLAG 3 — the #326 ruling is still not what the board prints (you know this one; here is the code half)

**Your ruling (register v574, 2026-08-05, "Keep as ruled. Land it."):** *"the N43 signed levels price
pool entrants AT ENTRY the way the pick curve prices national draftees."*

**Where it should bite:** the printed day-0 price of every fresh pool entrant.

**What the record shows:** ORDER 26A measured printed pool day-0 at **2.6498×** the signed anchors
(positional: RUCK 1.315 → KPF 5.114). You have this figure.

**What I add, from the code:** `one_source_selftest.py:627-700` runs **ten** #326 checks — the signed
levels are carried verbatim, the currency factor is right, the anchors reach `entry_anchor`, the
ND65+ amendment is honoured, there is no silent surface refit. **Not one of them asserts the ruled
sentence.** That is the mechanism of the failure, in one line: every instrument checked the *parts*
and none checked the *claim*.

**The open question:** none for you to decide — 26B's landing assert (printed day-0 == derived v0 ×
the display numéraire) is the fix and it is already specified. I flag it only because it is still true
today and it is the clearest worked example of the class this sweep found.

---

## SEVERITY 2 — honoured today, nothing stops it regressing

### FLAG 4 — the force-majeure exclusion lives in three hand-copied dicts, not in the engine or the store

**Your ruling (register v533, amended at #271 Addendum 2):** *"those players were pick 1 KPF busts, so
heavily bias the pool against them, however one retired early with depression, and another with
concussion issues. It's a force majeure situation, so I am ruling that it shouldn't reflect on the KPF
values."* — with your own amendment: whole-draft slide, a natural pick 65 slides to 64 and enters the
ND fit, slid picks computed before the ND/pool split, the store never edited.

**What the machinery actually does:** the derivation instruments honour it — but each by carrying its
own hard-coded copy of the two names:

- `session_2026-07-29/item271/emit_matrix_271.py:53` `FORCE_MAJEURE = {'thomas-boyd': 2013, 'paddy-mccartin': 2014}`
- `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:83` — the same dict again
- ORDER 26B-C1 — the same dict a third time, after the ruling was missed entirely

The **live engine** has a general exclude-and-slide facility for exactly this purpose
(`rl_model.py:284-296`), and McCartin and Boyd are **not in it**: neither store row carries
`_pvc_exclude` (`tools/probe_named_rows.py`). The ruling is honoured by whichever script remembers to
copy the names in.

This is precisely why 26B missed it. It will be missed again by the next instrument written by someone
who does not read v533.

**The open question:** should the exclusion become store data (a flag on the two rows, the way every
other population rule is expressed) or named engine config, so an instrument cannot silently omit it?
Note the interaction with FLAG 1: the `_pvc_exclude` flag currently holds the wrong three players.

---

### FLAG 5 — "no era normalisation" is protected by a comment

**Your ruling (register v598, #334 Addendum 3):** era normalisation *"is REMOVED everywhere, a product
law binding engine, teaching measures and instruments."*

**What the machinery actually does:** the engine is clean — `_merged_recover.py:53-57` records that
every `a*REF/era.get(y,REF)` site is gone and season averages are read raw. The only thing preventing
its return is the sentence *"Do not reintroduce"* in that comment. There is no gate, no selftest, no
lint.

Worth remembering: this law was **in breach on main for four days after you ruled it binding** (the
register names it at v637 — five live sites — and the composition build removed them at v638/v658). It
has already been broken once by being prose.

**The open question:** is a one-line scanner (the same shape as the R105.4 forbidden-token scan that
already exists at `one_source_selftest.py:333`) worth having here?

---

### FLAG 6 — the thread pin is on some paths, and the dispatch pin is on none

**Your ruling (register items 349 and 396, 2026-07-18/19):** *"every bit-exact proof, gate, audit
shard, and the bake itself runs with `OPENBLAS_NUM_THREADS=1`"*, and then, on the dispatch pin, *"A
please. We need to move on"* — filed as **permanent infrastructure**: the pin plus runtime-verified
asserts land in bootstrap for **every** future compute.

**What the machinery actually does:** `OPENBLAS_NUM_THREADS=1` is set in `live-scoring.yml`,
`live-scoring-proofs.yml` (six jobs), `tools/round_entry/weekly_update.sh:37` and both ingestion apply
paths — but **not** in `ci-guards.yml` or `final-integration.yml`, the two workflows that run the
guards. The dispatch pin (`NPY_DISABLE_CPU_FEATURES` / `OPENBLAS_CORETYPE`) appears **nowhere** in the
tree.

I have classified this QUEUED rather than a breach, because the register shows a deliberate, owner-
facing re-sequencing at item ~400 (move the dispatch pin to pre-go-live, post-bake) rather than a
silent drop. The env pin that *did* land (`bootstrap.sh:18-31`) is fail-closed and genuinely good.

**The open question:** the re-sequencing was recorded as *"OWNER AUTHORIZATION PENDING"*. Did that
word ever come? And should the two guard workflows get the thread pin in the meantime, since they are
the ones asserting byte-identity?

---

### FLAG 7 — the Mraz tolerance has two numbers in the record

**Your rulings:** at v631, *"The mraz tolerance (up to around 2k) was not set when he had zero games.
It was set when he had four. A four game player should not be quadrupling or more in value off such a
small sample."* The seat's delta-only re-basing was reversed and the level check re-anchored at the
ruled ~3.5× ladder. But the register also records, at v604-era (comment 5214443366), *"Mraz tolerance
widened 3.0x -> 3.5-3.8x acceptable fallout."*

**Where it should bite:** every act's side-by-side, as the named check on his row.

**What the record shows:** the tolerance is carried as prose in act briefs, with at least two live
numbers (≈2,000 board points; 3.5–3.8× his pick). Different acts have cited different ones. There is
no committed check.

**The open question:** which is the standing tolerance — an absolute cap or a multiple of his pick?
Both readings are in the register and this seat is not choosing between them.

---

## SEVERITY 3 — the record is unclear, or a ruling sits half-applied by design

### FLAG 8 — your O1 ruling was applied to the pool and queued for the national side, and the queue has no act

**Your ruling (register v682, 2026-08-12):** *"My July override no longer stands. I trust that the
data is correct so therefore my judgement is based on feelings, not fact… I should accept that, I
think."*

**What happened:** the pool object was already built O1-OFF, so the ruling cost nothing there. The
register then records that whether the same ruling reaches the **national surface's wired KPP floor**
*"MOVES ND PRICES so it cannot ride this act (separation law) and is queued."*

**The open question:** a ruling of general form ("my July override no longer stands") is currently
half-applied, and the other half is queued to no named act. Does it extend to the national KPP floor?

---

### FLAG 9 — "no hard bands" is satisfied on one path and breached on another, and nobody was commissioned to close it

**Your law (LAW-NO-HARD-BANDS, from the v561/v562 correction where you caught the audit):** the
year-zero surface is a true position × age × pick surface; a position dial constant across picks is
barred.

**What the record itself says (v613-era audit):** the year-0 **fit** is band-free — but *"the
production path still pools the seed-era hard band grid (`rl_model.py` bandof/MIX/BUST_BAND/basepk —
long-standing, now NAMED)."*

So the law holds where it was measured and is breached one layer over, the breach is named in the
register, and no act was ever commissioned to close it.

**The open question:** does the law reach the production path's band grid, or was it only ever about
the year-zero fit?

---

### FLAG 10 — the pool levels that are live are the ones you were told would move substantially

**Your grievance and ruling (v689/v693):** you withdrew the landing word over the origin goal, then
restored it with reasons — *"we work on this, and it never ends up live, but I think because it's done
it is"* and *"I'd like to have a better board while we wait."*

**What is live:** board `88ce647f…` with the signed levels MSD 337 / SSP 309 / RD KPD 369 etc.
(verified present in `engine/rl_after/pvc_curve_v2.json` and asserted by `one_source_selftest.py`).

**What the register says about them, in its own words:** *"STANDING CAVEAT ON THE RECORD: these LEVELS
ARE PROVISIONAL — iterated on the condemned realised_full meter, expected to move SUBSTANTIALLY DOWN
at the ORDER 26B delivered-value rederivation; the durable cargo is the MACHINERY."*

This is not a breach — it is exactly what you ruled, with your reasons. I flag it only because it is
the one place where the live board knowingly carries numbers the record expects to be wrong, and the
26B packet (which would replace them) is sitting unmerged on PR #489.

**The open question:** none, unless the 26B landing slips further than you expect.

---

## SEVERITY 4 — housekeeping that the sweep exists to catch

### FLAG 11 — your own law book lives in a folder called `archive`

`LUKE_RULINGS_LEDGER.md` — the source of R12 (the never-rises V0 law that broke on the board for 19
days) and the whole R-numbered ruling series — is at
`docs/archive/pre-mvp-2026-07/process/LUKE_RULINGS_LEDGER.md`.

It was flagged once already (v623) and you parked the restore on your own word — *"I am happy to park
the rulings ledger for now."* So this is not a breach. But R12 was still being cited as binding law at
v613, from a file in an archive directory, and this sweep's whole subject is rulings that go missing.

**The open question:** worth un-parking now, or still not?

### FLAG 12 — `docs/OPEN_DECISIONS.md` does not exist

Proposed at v696 as the second of the two mechanisms (the first being rulings-become-asserts), with
the V5 age-discount ladder named as its first entry. It is one of the two **"standing yes/nos still
open"** the register keeps listing as awaiting your word.

Right now every parked decision of yours — the V5 ladder, the D9 fade-speed act, the valuation-basis
workshop, the exchange-rate question, the incremental-currency re-founding, the referee, ITEM 412, the
mockup pick — lives only in this 8,400-line register. That is the exact condition that produced the V5
grievance.

**The open question:** yes or no on both mechanisms. They are the two things that would stop this
sweep from being needed again.

---

## Coverage and confidence

I segmented the register into 2,911 units covering 100% of its 1,765,759 bytes, screened every unit
against ~70 ruling-vocabulary patterns, and **read verbatim, in register order, every window around
every marker occurrence** — 842,699 characters across 1,258 windows, none skipped. The residue
(1,727 units, 373,863 characters) contains no ruling vocabulary at all; it was screened mechanically,
not read by eye, and the screen is committed so you can re-run it. I also read `owner_overrides.json`
in full, enumerated `docs/directives/`, and read the #334 comments of 12–13 August. Verification was
targeted rather than a full code audit: I opened `rl_model.py`, `_merged_recover.py`, `par_build.py`,
`one_source_selftest.py`, `ship_gates_check.py`, `owner_overrides.py`, `rl_export.py`, `bootstrap.sh`,
the five workflows, the model config, the curve artifact, the store and the shipped board. I am
confident in every ENFORCED verdict (each names a site I read) and in the three NOT-REFLECTED verdicts
(each rests on a named search plus a direct read of the landed data). I am least confident about
completeness: a ruling written without any ruling vocabulary would not have been surfaced, and the
process laws marked UNVERIFIABLE-BY-CODE were checked only against the register's own recent practice.
One instrument I built (`probe_326_day0.py`) has a defective filter; I have left it committed with the
defect stated and have relied on your own ORDER 26A measurement instead of anything it produced.

## The full inventory, by classification

| classification | n | meaning |
|---|---|---|
| **LIVE-STANDING** | 91 | should bind the machinery today → verified |
| **PROCESS-LAW** | 44 | binds how the seats work, not the code → verified against practice where checkable |
| **QUEUED** | 34 | ruled but not yet due (parked on your word, or awaiting a named later act) |
| **ONE-TIME-COMPLETED** | 15 | discharged by a single act, no ongoing bite |
| **SUPERSEDED** | 6 | a later ruling of yours changes it — both cited, no winner picked |
| **TOTAL** | **190** | |

Of the 135 that proceeded to verification:

| verification | n |
|---|---|
| ENFORCED (a named check or config site holds it) | 73 |
| DELIVERED-UNGUARDED (true today, nothing prevents regression) | 18 |
| NOT-REFLECTED (the machinery does not do it) | 3 |
| AMBIGUOUS-OR-CONFLICTING | 3 |
| UNVERIFIABLE-BY-CODE (process laws) | 38 |

**73 of your rulings have real teeth.** The three best examples are worth copying: the D14 never-rises
scan wired into the gated build path, the R105.4 forbidden-token AST scanner, and the owner-override
presence assertion. Each turns a ruling — a shape, a prohibition, a promise — into something that
fails the build. They are the existence proof for the rulings-become-asserts law you have not yet
ratified.

Full record: `INVENTORY.md` (all 190 with quotes and citations), `VERIFICATION.md` (the searches,
including the ones that came back empty), `RULINGS_INVENTORY.json` (machine-readable),
`METHOD.md` (how it was done, committed before any findings).
