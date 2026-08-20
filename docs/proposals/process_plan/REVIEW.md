# ADVERSARIAL REVIEW of PLAN_v2 (independent, read-only, 2026-08-20)

Scope: PLAN_v2.md checked against PLAN_v1.md + SELF_REVIEW.md and against the repo ground truth:
docs/proposals/MODERNISATION_PROGRAMME.md (the review-folded rulings), the register (targeted slices,
v770–v798 pen entries + items 288–294, 400–408), acceptance/, release_manifest_check.py,
tools/build_lock.sh, ui/templates/, .github/workflows/ (all five read), and
engine/rl_after/_merged_recover.py (targeted greps only). No writes to the repo; no builds; the
build lock was not taken.

Context claims verified TRUE before findings: live board 5ea978f7/693,753 (register v798); runner
GREEN 7/7 with contract + self-test 45/45 (v791; acceptance/runner.py); build lock is real flock
(tools/build_lock.sh:3); manifest check is 40 fields / 8 identities / 7 files
(release_manifest_check.py:42,84,344); ui/templates skeletons exist (slots.py, selftest.py,
manifest.json, 5 pages); five workflows exist; the _SHEET_*/O41_INJ_* pins exist in
engine/rl_after/_merged_recover.py (lines 4207–4232 and 5907–5947). The plan is not built on
invented ground. The findings below are where it is wrong anyway.

---

## FINDINGS

**F1 — BLOCKER [4b/4c].** S2's fix, imported into the collapse gate, degrades the one leg that
detects a wrongly-deleted dial. 4c's second proof leg reads "historical board reproducible from
tag"; under 4b's S2 framing (PRIMARY = restore tagged BYTES; rebuild parity = secondary,
best-effort), that leg can be discharged by a byte-restore — which proves nothing about whether the
deleted branch still worked. The M3 ruling is explicit that the must-not-move gate alone "is
provably blind to deletion (the record's own case: a silently deleted dial, byte-identical board,
caught only by must-move)" (MODERNISATION_PROGRAMME.md, M3), and the paired gate's leg (b) is "the
retired branch still reproduces its historical identity byte-exact BEFORE retirement" — a rebuild
with the switch set, on the pinned local host (where cross-host float is not in play; v798 itself
ran exactly this proof: kill-switch build == a05fe951 byte-diffed). S2 is correct for ROLLBACK
years later; it must not leak into the pre-retirement eligibility proof.
FIX: 4c leg (b) restated: "pre-deletion, the switch-set REBUILD on the pinned environment
reproduces the historical identity byte-exact; the artifact tag (bytes) is the rollback vehicle,
never the eligibility proof." Add M1b's standing must-move positive control to the suite before the
first collapse.

**F2 — MATERIAL [P4, missing prerequisite].** No package delivers the declared `kill_switches`
block, yet P4 cannot run its proofs without it. The register records the measured mutual exclusion:
"the 18 baked switches are absent from the 84 manifest vars — setting any one under gate mode
halts; identity proofs necessarily ran ungated — resolved by a declared kill_switches block"
(register, v787-adjacent; also M1b's bullet and v787 root cause R3: "THE BAKE'S 18 DIALS ARE
OUTSIDE THE MANIFEST AND UNCLASSIFIED"). 4a classifies dials and 4c collapses them, but the
mechanism that lets a gated build set a switch at all is unscheduled. FIX: add the kill_switches
block (named switches, excluded from the value hash, admitted by the reject scan on explicit
identity-chain runs) as its own preregged act inside P4 (or late P3), gating 4b/4c on it.

**F3 — MATERIAL [1a/S8].** The loud-red halt mechanism self-defeats on the estate as it stands. At
the v787 audit three of five workflows were red on push (ci-guards RED, live-scoring RED stale-R14
fixture, final-integration RED-real x6 + one structurally impossible step); several one-liners have
since landed (v791) but final-integration's bundle-cmp step cannot pass as wired (the committed
bundle carries stamp.release injected by a second phase CI never runs — v787). Arm "red on main =
owner notified + standing landing halt" against that baseline and the owner is notified on every
push from day one — the exact furniture failure S8 cites, rebuilt by the fix meant to prevent it.
FIX: the notify+halt binds ONLY to the newly wired host-insensitive gates (a separate required
workflow), and pre-existing attributed reds route through the ruled-red/known-red self-expiring
ledger pattern the estate already built (v791: "the known-red ledger EXPIRED ITSELF") until
repaired or formally de-scoped.

**F4 — MATERIAL [1b].** LAWS.md creates a second hand-maintained home for the laws beside the
owner-signed RULEBOOK, which declares itself "the single governing document" (docs/RULEBOOK.md:5,
owner-signed 2026-07-22/28) — and beside the register's own owner rule that "nothing is 'on a
list' unless it is in THIS file" (register line 2, owner-driven 2026-07-11). A second manually
synchronized law surface is the exact class items 292–294 retired ("structures that must be
manually synchronized eventually aren't") and the shape CURRENT_STATE.md warns about in its own
header (the club_valuation.js fault of 2026-07-27). 1b's G4 line names what it retires in seat
briefs but not which DOCUMENT dies. FIX: either the incident citations go into RULEBOOK by
owner-signed amendment (no new file), or LAWS.md is GENERATED from register/rulebook markers;
either way 1b names the superseded surface, and the change to the register's line-2 rule is an
owner ruling, not a delegated act (it is not in G3's list).

**F5 — MATERIAL [ordering, 2b vs 3a].** P3a invalidates part of P2's soaked work. Today a round
advance includes an ENGINE edit (the sheet re-cut moves _SHEET_MD5/_SHEET_Y in-engine — v790:
"pins moved", with prereg + ADVANCE-REPIN). `land round` (2b) scripts that transaction and soaks
it (2e, stand-down per act type on the owner's word). 3a then removes the engine-edit/repin step
from the very transaction just soaked — the program changes after its verification stood down.
FIX: either land 3a BEFORE 2b (the pin move is small, and it simplifies what 2b must script), or
state in the plan that 3a amends the landing program and restarts `land round`'s soak clock.

**F6 — MATERIAL [2a/2b, day-0].** The landing program will inherit day-0 re-basing (the D7
completion pass regenerated DAY0_CP.json as part of a lever landing — register v775) but the plan
nowhere carries the folded M1b ruling: "Day-0 re-basing becomes an explicit, owner-visible,
off-by-default input with a mandatory printed diff of every moved row... a suite inheriting the
capability without the judgement re-bases itself green on the first halt"
(MODERNISATION_PROGRAMME.md, M1b). A scripted lander that can re-base to make itself green is the
recorded failure class, now automated. FIX: name day-0 in 2a as an off-by-default flag whose
activation prints the mover diff and appears in the claims file (1c).

**F7 — MATERIAL [3a].** The move deletes the ceremony that currently forces review of sheet
changes and names no replacement coverage. Today a sheet re-cut is an engine edit → prereg + F6 +
repin; after 3a it is a bare data-file commit, and a stale pin-file + matching stale sheet passes
the loader silently (the guard only compares them to each other) — a new stale-value-trusted
channel. Also, the pin is duplicated INSIDE the engine today: _merged_recover.py pins the same md5
21361291... at line 4207 (O41_INJ_MD5) and line 5907 (_SHEET_MD5) — two sites, one truth; a move
that migrates them 1:1 preserves an internal mirrored pair (S7's own lesson). FIX: 3a names the
replacement gate — the sheet md5 becomes a manifest-checked field whose sole writer of record is
the landing program — and collapses the double pin to ONE read site as part of the move, with the
new data file's coverage listed in G1's enumerated churn.

**F8 — MATERIAL [3b].** "Frozen byte-exact forever" forbids adding a pointer to the frozen file —
so its own header will forever read "the single durable list · v798" while being neither current
nor the list, for every human or seat that opens it (the stale-value-trusted class; S3 enumerated
only PARSERS). tools/seat/pen.py:30 hard-defaults to docs/OPEN_ITEMS_REGISTER.md and will
byte-surgery the frozen file unless repointed in the same act. FIX: the LAST pen entry before the
freeze IS the tombstone (freeze point includes it: "frozen at v79x; continues at <dir>"); pen
DEFAULT_REGISTER repointed in the same act; the owner amends the line-2 "THIS file" rule (see F4).

**F9 — MINOR [1a].** "Repair or formally retire the rotted one" misdescribes the estate and
brushes a standing owner ruling. Per v787 the rotted thing is a STEP inside final-integration (the
bundle cmp, structurally impossible as committed); the workflow a reader would take for "the
rotted one" — live-scoring-proofs — is not rotted but owner-de-scoped to manual (#251 part B,
2026-07-29: "kept... not deleted, and not otherwise changed"), and v787 found its stated de-scope
cause "now FALSE". Retiring it contradicts the ruling; repairing it (making it pass) is what its
own header declares out of scope while the v0surf freeze stands. FIX: 1a says: repair the
final-integration bundle-cmp STEP (accounting for the two-phase stamp.release injection), and
RE-ADJUDICATE live-scoring-proofs with the owner given the now-false cause — neither unilateral
repair nor retirement.

**F10 — MINOR [G3].** "Owner rules on exactly four things" is contradicted by the plan's own text:
1b makes law retirement an owner ruling; 4e's staged-publish word is an owner act; and the standing
owner gates (landing words, lever adoption, M5's "owner-only gates unchanged" and the
independent-read ruling) are outside the four. As written, G3 could be read as delegating things
the record reserves. FIX: restate G3 as "this plan CREATES exactly four new standing rulings; every
existing owner gate — including the independent read on mechanism changes — is unchanged." (P2's
landing program is itself a Lane-B mechanism and should get that independent read.)

**F11 — MINOR [3c/1e, G4 application].** 3c names the class it retires ("hand-maintained state
files") but not the file: docs/CURRENT_STATE.md — hand-maintained, last pen v642/2026-08-11 vs
register v798, i.e. currently 156 versions stale, proving 3c's own premise. 1e's incident index is
likewise a hand-extracted derived view with no authority banner. FIX: 3c names CURRENT_STATE.md
(at least its Part B) as retired-by-generation; 1e is generated, or carries the CURRENT_STATE-style
"where the two disagree, the register wins" banner.

**F12 — MINOR [P2, missing M2 ruling].** The programme's honest-pricing correction — "First act:
time one full acceptance run end-to-end and QUOTE THAT NUMBER as the target" and "'Live' includes
the landing transaction, priced honestly once measured" (M2) — appears nowhere in P2, though P2 is
the M2 analogue and the owner's original 15-minute framing is the incident behind the ruling.
FIX: `land lever`'s first soaked run is also the timing act; the measured number is what the owner
is quoted.

**F13 — OBSERVATION [S1].** S1's demanded "own measured act" for CI rebuilds is largely already on
record: final-integration asserts clean-room rebuild-equality (byte-identical board) on
ubuntu-24.04, and CI_MIGRATION_DIAGNOSIS.md calls the fresh-build record-md5 pin "also the A2
cross-machine proof". S1 is right to demand the re-proof on the current board, but it is a cheap
re-run, not a far-future research item — the plan should not let "REBUILDS only after proven" quietly
mean "never".

**F14 — OBSERVATION [2a/2b].** The landing program must state that it runs under the build lock
and commits with EXPLICIT paths only — the v786 incident (the v785 pen commit 6ff0d69 ran bare
`git commit` in the shared checkout and swept the seat's staged owner-input files; standing
correction: `git commit -- <explicit paths>`) is exactly the class a scripted lander in a shared
tree will hit.

**F15 — OBSERVATION [P1].** Whatever P1 does to the workflows, the fv-provenance suite must never
be executed on the shared box: v787 found it "NOT side-effect-free — it would overwrite
/home/claude/v0surf.pkl and plant a crashing rl_model; the seat REFUSED to run it". CI-hosted only.

---

## ON THE SELF-REVIEW (brief item 6)

Right and well-evidenced: S3, S4, S5, S6, S7, S9. Partially wrong or insufficient: S2 (correct for
rollback, leaks into the collapse gate — F1); S8 (the mechanism as designed self-defeats on the
red-as-attributed estate — F3; and its "one permanent-red workflow" example is actually the
owner-de-scoped manual battery, not silent furniture — the silent furniture is the three
push-red workflows); S1 (over-states the unknown — F13). Missed entirely: the kill-switch/config-gate
mutual exclusion as a P4 prerequisite (F2 — the register lesson closest to the retirement package),
the LAWS.md/RULEBOOK duplication (F4), the P3a-invalidates-P2b ordering (F5), day-0 inheritance
(F6), the 3a coverage gap and in-engine double pin (F7), and the frozen-header trap (F8).

## PROPORTIONALITY (brief item 5)

The plan mostly passes its own G4: 1c, 2a/2b, 3b, 3c, 4d all name retirements. Two items fail it
as written: 1b and 1e create new hand-maintained surfaces whose named retirement ("seat briefs stop
restating") does not offset the new drift channel (F4, F11). The per-package change-process
(prereg only where the engine file is touched, gates, one register entry per package) is
proportionate for tooling changes — do not add more ceremony than G2 already imposes; the packages'
register entries can be single pen entries, not new document types.

---

## VERDICT: LOCK-IN WITH AMENDMENTS

The four-package structure and P1→P2→P3→P4 order are sound and the plan's factual ground checks
out. Lock in only with these amendments (F1–F8 are the substance; F9–F12 are one-line edits):

1. (F1) 4c leg (b) = pre-deletion switch-set REBUILD on the pinned host, byte-exact to the
   historical identity; byte-restore stays rollback-only; must-move control enters the suite
   before the first collapse.
2. (F2) The kill_switches block scheduled as a named preregged act before any 4b/4c proof.
3. (F3) The loud-red halt binds to the new gates only; existing reds ride the self-expiring
   ruled-red ledger.
4. (F4) LAWS.md merged into RULEBOOK (owner-signed) or generated; the register's line-2 rule
   amended by the owner, not by delegation.
5. (F5) 3a lands before 2b, or 3a explicitly restarts `land round`'s soak.
6. (F6) Day-0 re-basing in the lander: off-by-default, owner-visible, printed row diff, recorded
   in the claims file.
7. (F7) Sheet md5 becomes a manifest-checked field with the lander as sole writer; the in-engine
   double pin collapses to one site in the move.
8. (F8) Tombstone-then-freeze; pen.py repointed in the same act.
9. (F9–F12, F14–F15) The one-line wording fixes above.

---

# VERIFICATION PASS — PLAN_v3 AMENDMENTS vs FINDINGS F1–F15 (same reviewer, read-only, 2026-08-20)

Method: PLAN_v3.md read in full; package text confirmed byte-identical to v2 (amendments appended,
declared binding + overriding). Each A-Fn checked against the finding's stated fix and the record.

## 1. FAITHFULNESS, per finding

- **F1 — PARTIAL.** The separation itself is airtight as written: A-F1 names two proofs, assigns
  byte-restore to rollback only, and makes 4c's paired proof "the REBUILD leg, always," switch-set,
  on the pinned host — that kills the blocker's conflation channel, and 4b's "secondary failure is a
  reproducibility finding" clause now reads coherently as rollback-context-only. **Dropped: the
  second half of the F1 fix — M1b's standing must-move positive control entering the suite before
  the first collapse.** The per-collapse rebuild leg proves the dial being retired; the standing
  must-move control is what catches the NEXT silent deletion between collapses (the register's
  incident was caught by must-move running as a control, not by a retirement ceremony). One
  sentence restores it. Nit: say "reproducing the historical IDENTITY byte-exact," not "the
  historical board."
- **F2 — FAITHFUL.** kill_switches block as P4-zero, cited to v787 R3. "Before any classification"
  is stricter than needed (only 4b/4c require it) — harmless.
- **F3 — FAITHFUL.** Binds loud-red to new gates + self-expiring ruled-red ledger. "Repaired or
  formally re-adjudicated FIRST" is acceptable only on the reading that re-adjudication (a ruled-red
  entry) is the cheap path; if "FIRST" is read as repair-the-estate-before-P1, P1 balloons. State the
  intended reading: each legacy red gets a ruled-red entry or a repair BEFORE arming — never a
  repair mandate.
- **F4 — PARTIAL.** "No new LAWS.md beside RULEBOOK; laws land INTO the RULEBOOK" is the right
  primary. **The parenthetical "(or are generated from it)" half-reopens the trap:** generation is
  safe only with a regeneration trigger and an authority banner — a generated-once file is a
  hand-extracted file in disguise. Bind any generated laws view to the house discipline: regenerated
  by the lander at every landing (3c pattern) or CI-linted equal to the RULEBOOK (1a's laws lint is
  sitting right there), plus DO-NOT-HAND-EDIT + "RULEBOOK wins" banner. Also unstated: incident
  citations added to the owner-signed RULEBOOK are an owner-signed amendment, not a delegated edit.
- **F5 — FAITHFUL, one NEW gap.** The revised order P1 → P2a → P3a → P2b → rest-of-P3 → P4 resolves
  the invalidation (2b is built against the final pin location), and the coordinator's worry does
  not bite: the shared transaction library is built with P2a, which precedes P3a. **The new gap is
  the 3a→2b transition window:** after 3a, a round advance still runs MANUALLY off the R23-runbook,
  whose sheet-pin step (in-engine pins + that leg of ADVANCE-REPIN) is now wrong — and the runbook
  fix lives in 3d, which the new order puts AFTER 2b. Fix: 3a amends the round runbook in the SAME
  act; any advance in the window follows the amended runbook.
- **F6 — FAITHFUL.** "M1b ruling, inherited verbatim" carries owner-visibility. Nit: day-0
  activation should also appear in the 1c claims file (it is a per-landing claim).
- **F7 — PARTIAL.** Prereg-lite (predicted md5 + counts + disclosed movers committed with the data
  change) restores the review-forcing ceremony, and the pin-block unification (4207/5907 → one
  declaration) is exactly right. **Dropped: the coverage half** — the sheet md5 (and the pin file)
  entering the manifest as a checked carrier field with the round lander its sole writer of record.
  Without it the sheet truth lives outside the 40-field/8-identity coherence net that exists
  precisely to catch unfinished/stale carriers (v785: the manifest is "the generalisation of the
  six-way coherence gate"). Also: the new data file's churn must be listed in G1's enumerated set.
- **F8 — PARTIAL.** Tombstone-then-freeze + pen repoint in the same act: implemented. **Unassigned:
  the owner word.** The single-list rule is owner-driven ("nothing is on a list unless it is in
  THIS file," register line 2); 3b changes what "THIS file" means, and A-F4 declaring the rule
  "stands" does not substitute for the owner amending it to the new form. One owner sentence inside
  the 3b act closes this.
- **F9 — PARTIAL.** Owner re-adjudication: right. Two gaps: (i) "the de-scoped live-scoring
  workflow" is the WRONG NAME — the de-scoped one is live-scoring-proofs.yml (#251); live-scoring.yml
  is the every-push workflow with the stale-R14 red. As written a seat could re-adjudicate the wrong
  file. (ii) The actual rotted item — final-integration's bundle-cmp STEP (structurally impossible:
  stamp.release injected by a second phase CI never runs, v787) — is still assigned nowhere, while
  un-amended 1a text still says "repair or formally retire the rotted ONE [workflow]."
- **F10 — FAITHFUL.** Nit: "per 1b" should read "per 1b as amended by A-F4" (the ruling diff is now
  a RULEBOOK diff).
- **F11 — FAITHFUL.** Nit: the incident index remains hand-appended; give it the CURRENT_STATE-style
  "the register wins" banner.
- **F12 — FAITHFUL.** Machine-timed landings, measured cost before promised target.
- **F13 — FAITHFUL.** Cheap re-proof retained; claim matches the record (A2 cross-machine proof /
  final-integration clean-room rebuild-equality, R19 era).
- **F14 — FAITHFUL,** strengthened (asserted in self-tests).
- **F15 — FAITHFUL.** Wording muddle only ("CI exclude it there" — CI never runs on the shared box;
  intent clear: shared box never, isolated workspaces/GitHub runners only).

## 2. COHERENCE of the override structure

The amendments-override-text device is legally sound but leaves SIX places where reading only the
package text reproduces a found defect — in a project whose named root-cause class is "a stale
value trusted": 1b still orders LAWS.md built (vs A-F4); 4c still says "reproducible from tag" (vs
A-F1 — a BLOCKER-class line surviving verbatim in the operative text); 1a still says "repair or
formally retire the rotted one" and keeps the unscoped loud-red sentence (vs A-F3/A-F9); G3 still
says "exactly four things... everything else delegated" (vs A-F10); line 85 still says "P1 → P2 →
P3 → P4 strictly" and G2 still says "one package at a time" (vs A-F5's interleave). REQUIRED at
lock-in: either fold the amendments into the package text, or annotate every overridden line inline
("[superseded — A-Fn]"). For 4c specifically, folding is mandatory, not optional — a blocker fix
should not depend on the reader reaching line 92.

## 3. NEW defects introduced by the amendments

- The F5 transition window (runbook amendment must ride 3a) — see F5 above.
- A-F3's "FIRST" ambiguity — see F3 above.
- No others found: A-F2's over-strictness and A-F15's wording are harmless.

## VERDICT: AMENDMENTS NEED FIXES

Nine of fifteen are faithful as written (F2, F3, F5, F6, F10–F15, with the noted one-line nits).
Five are partial and need one-to-two-line additions before lock-in; plus one structural edit:

1. **A-F1:** add M1b's standing must-move positive control to the suite before the first collapse;
   "historical identity byte-exact."
2. **A-F4:** bind the generated-laws parenthetical to a regeneration trigger (lander-generated per
   3c, or CI-linted equal to RULEBOOK) + authority banner; RULEBOOK additions are owner-signed.
3. **A-F7:** sheet md5 + pin file become manifest-checked carrier fields, round lander sole writer;
   new file listed in G1's enumerated churn.
4. **A-F8:** the owner's word amending the single-list rule rides the 3b act.
5. **A-F9:** name live-scoring-proofs.yml precisely; assign the final-integration bundle-cmp step
   repair (two-phase stamp.release) explicitly.
6. **A-F5 (new gap):** 3a amends the round runbook in the same act (the 3a→2b window).
7. **Structural:** fold or inline-annotate the six superseded package-text lines; folding 4c is
   mandatory.

---

# FINAL PASS — PLAN_v4 (same reviewer, read-only, 2026-08-20)

Method: v4 read in full; checked (1) the seven verification fixes are integrated inline, (2) no
superseded text survives, (3) nothing from EITHER pass (15 findings + the 9 self-review fixes S1–S9
+ the flagged nits) was lost in the rewrite, (4) fresh defects.

## 1. The seven fixes — ALL SEVEN FAITHFULLY INTEGRATED

- A-F1: 4c is now the RETIREMENT GATE "distinct from 4b BY DESIGN" — switch-set REBUILD on the
  pinned host, historical identity BYTE-EXACT, "never a byte-restore," AND the standing must-move
  positive control enters the suite before the first collapse, with the correct rationale stated
  (per-collapse rebuild proves only the retired dial; the standing control catches the NEXT silent
  deletion). The blocker is closed in the operative text.
- A-F4: 1b — laws INTO the RULEBOOK, "no second laws file, ever"; any derived view GENERATED with a
  defined trigger (3c lander or 1a CI-lint), banner, G1 churn listing; owner-signed amendments;
  owner diff-ruling on retirement. Closed.
- A-F5: sequence header P1→P2a→P3a(+runbook amendment)→P2b→P3b-d→P4; 3a amends the round runbook
  IN THE SAME ACT, with the 3a→2b-window rationale stated. Closed.
- A-F7: sheet md5 + pin file as MANIFEST-CHECKED CARRIER FIELDS, round lander sole writer, pin file
  in G1's enumerated churn (G1 itself now names it), prereg-lite kept, double pin unified. Closed.
- A-F8: tombstone-then-freeze, pen repoint same act, and the owner's word amending the single-list
  rule RIDES THE ACT ("owner-authored and only his word amends it"). Closed.
- A-F9: all three legacy items correctly named and assigned — live-scoring.yml stale-R14
  (ruled-red-or-repair), final-integration's bundle-cmp STEP (two-phase stamp.release, repaired or
  ruled-red in P1), live-scoring-proofs.yml owner-re-adjudicated. Closed.
- A-F3: loud-red binds only to new gates + self-expiring ruled-red ledger; triage scoped as
  "ruled-red-entries-or-repairs (never a repair-the-estate mandate gating P1)". Closed.

## 2. Superseded text — NONE SURVIVES

All six flagged lines are gone and restated correctly in place: 1b (no LAWS.md), 4c (no
"reproducible from tag"), 1a (no "rotted one"; loud-red scoped), G3 ("four NEW standing rulings...
delegates nothing that is already an owner gate", independent read named), the sequence header
(revised order), G2 ("one package at a time IN THE SEQUENCE BELOW" — coherent with the interleave).
S1–S9 all survive the rewrite (S1 in 1a as relaxed by F13; S2 in 4b; S3 in 3b PRE-ACT; S4 in
"Effort, honestly"; S5 in 4d; S6 in 1c; S7 in 2a's ONE shared library; S8 in 1a; S9 in G1), as do
F2 (4-zero), F6, F10–F15. Nothing from either pass was dropped in substance.

## 3. What the rewrite itself introduced or left

- **R1 (required before lock-in, record not plan-text): the header's provenance claim "Fable seat,
  owner-worded scoped exception to the Opus-only law" is UNVERIFIABLE from the record as of v798.**
  The Opus-only law is real, standing, and incident-born — the register records the breach, the
  owner's verdict in his own words, and "Opus-only launches, NO resumes to Fable seats ever";
  v767 shows the correct form (seats "launched with the explicit Opus override" ON THE RECORD). A
  lock-in document asserting an exception to THAT law must cite a penned owner word, verbatim, not
  assert it. Pen the exception (or strike the clause) at or before lock-in. This reviewer takes no
  position on whether the word was given — only that the record must show it before the claim rides
  a locked document.
- **R2 (minor, fix in the lock-in edit): item-numbering collision.** Inside PACKAGE 2a the items
  are relabeled 2a–2d, so "2b" now names BOTH the decision-packet item and the round-lander
  package; line 83's "the 3a->2b window" and the soak rule's act-type references become ambiguous
  to an implementer. Renumber the P2a items (2a.1–2a.4 or similar).
- **R3 (observation): the sole-writer transition.** 3a declares the round lander sole writer of the
  new carrier fields, but the lander lands one package later; in the 3a→2b window the amended
  runbook's manual procedure is the de-facto writer. The same-act runbook amendment covers this —
  it should explicitly include the carrier-field write so the manifest check stays green across
  the window.
- **R4 (residual nits carried from pass 2, still absent, both one-liners, non-blocking):** day-0
  activation recorded in the 1c claims file; the incident index (1e) carries a "the register wins"
  authority banner (it remains hand-appended).

## VERDICT: LOCK-IN READY

— conditional on R1 (the Opus-exception owner word penned to the register, or the clause struck)
and the R2 renumber; R3/R4 are one-line polish that can ride the lock-in edit. Every mechanism-level
finding from both passes is faithfully integrated; no superseded text survives; the rewrite lost
nothing of substance.

---

# CONFIRMATION — PLAN_v4 (edited in place), R1-R4 (same reviewer, read-only, 2026-08-20)

R2 CONFIRMED: P2a items are 2a.1-2a.4; every "2b" in the document now unambiguously names the
round-lander package, including 2a.1's library sentence and 3a's "3a->2b window". R3 CONFIRMED: the
interim writer is stated twice in 3a — at the carrier-fields sentence ("sole writer once 2b lands;
interim writer: the amended runbook's manual path") and at the runbook-amendment sentence ("EXPLICITLY
the interim writer... stated in the runbook, until the round lander (2b) takes over") — the
manifest check stays covered across the window. R4 CONFIRMED: day-0 activation state is in the 1c
claims schema ("off unless explicitly activated") and 1e carries the "register wins" banner ("a
lookup surface, never a source"). R1 RESOLVED AS PRESCRIBED, with one precision: the header no
longer asserts a recorded exception — it states the exception was proposed in-session and commits
the owner's word to a VERBATIM register pen AT lock-in, so by the document's own terms lock-in
cannot complete with the record silent. That discharges R1 structurally, but the discharge happens
at the PEN, not at this sentence: whoever executes lock-in must treat the register entry as part of
the lock-in act itself, and if the verbatim word cannot be produced, the clause is struck per the
original R1 disjunction (with an Opus re-verification then the record-clean path). The edits
introduced nothing new — all other text is byte-identical in substance to the v4 already verified;
both earlier verdicts' content (all 15 findings, S1-S9, the seven integrations) remains intact.

## VERDICT: CONFIRMED LOCK-IN READY — no remaining plan-text items; the sole outstanding act is the
R1 register pen, which the document itself now makes a constituent of lock-in.
