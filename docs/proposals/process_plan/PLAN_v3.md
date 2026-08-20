# THE PROCESS PLAN v3 — four packages (self-reviewed + independently reviewed [15 findings, verdict LOCK-IN WITH AMENDMENTS]; amendments below are BINDING and override the package text where they conflict)

Context: afl-rl-engine, post-D8-adoption (live board 5ea978f7/693,753), R23 advance in flight.
The opening modernisation tranche is landed: acceptance runner (verdict contract, GREEN 7/7),
build lock (flock), release_manifest_check (40 fields/8 identities/7 files), ui/templates skeletons,
M0 data/lever rule. This plan COMPLETES that tranche and adds the items surfaced in the
2026-08-20 "from the inside" discussion. Register refs: v783/v785 (programme), v798 (adoption).

## Governing rules (apply to every package)
- G1 (S9). No process change ever moves the board or any value-bearing artifact: byte-exact
  before/after is the standing falsifier for ALL packages. Identity/administrative churn (contract sha,
  manifest fields) is allowed but ENUMERATED per change; anything outside the enumerated set = halt.
- G2. One package at a time; each lands under the EXISTING discipline (prereg where the engine file
  is touched, gates, register entry). New tools earn trust under old rules before old rules retire.
- G3. Owner rules on exactly four things: (i) N green rounds for dial-collapse eligibility,
  (ii) dial classification policy-vs-scaffolding, (iii) pruning review cadence, (iv) each stand-down
  of hand-verification per act type. Everything else delegated.
- G4. Net-negative-process test: every mechanism must name what it retires. Anything that can't, stays out.

## PACKAGE 1 — THE SAFETY NET
1a. CI wiring, HOST-SCOPED (S1): on every push, the HOST-INSENSITIVE gates run — committed-artifact
    hashes, manifest coherence, contract check, laws/register lint, runner in identity mode — by
    extending the existing 5 workflows (repair or formally retire the rotted one). Full board REBUILDS
    in CI only after reproducibility on that runner class is PROVEN as its own measured act. Red CI on
    main is LOUD (S8): owner notified; any active session treats it as a standing halt on landings
    until attributed.
1b. LAWS.md: the standing laws, one line each, with the incident that created each. Seat briefs
    reference it instead of restating. Retiring a law = a visible diff the owner rules on.
1c. Proof-carrying deliverables: every seat's final act includes a claims file (fixed schema per act
    type: identities, counts, gate verdicts); one standard checker verifies claims against artifacts,
    and the checker carries its own negative control (S6): a deliberately false claim must fail it,
    asserted in self-test.
    Retires: supervisor re-derivation of gate-covered facts (judgment review stays).
1d. Free habits (no ruling needed): no codenames in owner-facing text; owner-inputs inbox
    (docs/inputs/incoming/ + provenance manifest: md5, date, purpose); rendered board/movers page
    delivered to the owner at every round.
1e. Incident index: one line per historical incident (what, root cause class, covering gate),
    extracted once from the register; new incidents get a line each.

## PACKAGE 2 — THE LANDING PROGRAM
2a. `land lever`: one command running the full lever-landing transaction (build+proofs, pins via C3
    pattern, lineage append, contract restamp+repin, sibling repin, BOTH UI writers, manifest check,
    acceptance runner) — the scripted form of the D8 adoption's act sequence. Fails closed at each step.
2b. `land round`: the same for the round advance — 2a and 2b are thin entry points over ONE shared
    landing-transaction library (S7: mirrored script pairs drift; the repo's own loader/emitter history
    proves it). Covers sheet/data commits, scores staging, preflight, armed catchup, ADVANCE-REPIN,
    movers page, gates — the scripted form of the R23 runbook.
2c. Self-test: the program deliberately breaks each step in a sandbox and asserts the failure is
    caught (verdict-contract pattern).
2d. Decision-packet template: fixed slots — what changes; who moves AND who doesn't (by name);
    cost; standing-table impacts; what-would-make-it-silly; recommendation; falsifiers. Slot list
    capped: a question earns a slot only when the owner has asked it twice.
2e. Soak rule: supervisor hand-verification runs ALONGSIDE the program for its first landings;
    stands down per act type only on the owner's word (G3.iv).
    Retires (after soak): checklist landings, landing-tail ordeals, duplicated verification.

## PACKAGE 3 — THE TIDY-UP
3a. Data pins out of engine source: _SHEET_*/O41_INJ_* (and any other pure-data pins) move to a
    data file; THE GUARD MOVES WITH THEM (loader asserts identically; a drifted sheet still halts
    the build). Effect: sheet updates stop being engine edits; engine_head moves ⇔ code changed.
3b. Register evolution: PRE-ACT (S3) — enumerate every reader of the current file (pens grep marker
    strings; find any other parser first); the new form keeps every found reader working or migrates it
    in the same act. Then: the existing file FROZEN byte-exact forever (history never rewritten); new
    entries as append-only files in a directory; index generated. Pen byte-surgery retired.
3c. STATE file: machine-generated by the landing program at every landing (current identities,
    queue, laws pointer). GENERATED-ONLY — if it cannot be generated it does not exist (hand-
    maintained state files drift and mislead successors).
3d. Runbook errata absorbed; reusable scratch scripts promoted to tools/ with names.

## PACKAGE 4 — THE RETIREMENT ERA (only after 1-3 soak)
4a. Dial classification (owner rules G3.ii): scaffolding vs policy. Policy dials keep switches forever.
4b. The one rollback fire drill BEFORE the first collapse (S2): PRIMARY = restore the tagged artifact
    BYTES and prove the boot guards accept them (tags are bytes, not recipes — the v783 ruling).
    SECONDARY, best-effort = rebuild-from-source parity on the pinned environment; a secondary failure
    is a reproducibility finding, not a rollback failure.
4c. Collapse process: one dial at a time; eligibility = N green rounds (G3.i); paired proof (live
    board unmoved AND historical board reproducible from tag); each collapse its own preregged act.
4d. Pruning review at owner cadence DENOMINATED IN ROUNDS (S5, G3.iii): each law/ceremony names the
    mechanical gate covering it or it stays; dormant-is-not-dead — only prune what a gate demonstrably
    covers.
4e. Round-advance automation milestones: seat+verify (now) → program+verify claims → program to
    STAGED + owner's one word publishes → full-auto only on sustained flawless record (may be never).

## Sequencing & effort
P1 → P2 → P3 → P4 strictly. Estimates are ±2x guesses (S4 — the honest record says things take
longer): P1 ~1 session, P2 ~2 sessions + soak over following ROUNDS (calendar time is round-clocked,
not session-clocked), P3 ~1 session, P4 spread over rounds. Interleaved with normal operations;
nothing pauses. No elapsed-weeks promise is made.


## AMENDMENTS (from the independent review, supervisor-verified against the record; binding)
A-F1 [BLOCKER, 4b/4c]. Two different proofs, never conflated: the ROLLBACK drill = restore the tagged
  artifact BYTES + boot guards accept (S2 stands for rollback). The RETIREMENT gate for a dial collapse
  = a switch-set REBUILD on the pinned host reproducing the historical board — because a byte-restore
  is exactly the leg the record proved blind to silent deletion (the must-move lesson, v783). 4c's
  paired proof uses the REBUILD leg, always.
A-F2 [4a prerequisite]. The declared kill_switches block in the config manifest (named fix on record at
  v787 R3, never delivered) is a P4 PREREQUISITE: without it the collapse proofs cannot run under gate
  mode. Scheduled as P4-zero, before any classification.
A-F3 [1a]. Loud-red binds ONLY to the NEW host-insensitive gates + the self-expiring ruled-red ledger.
  The legacy estate (red on push today, 3 of 5) is repaired or formally re-adjudicated FIRST — the
  owner is never notified into furniture-red from day one.
A-F4 [1b]. No new LAWS.md beside docs/RULEBOOK.md (the owner-signed "single governing document") — the
  laws land INTO the RULEBOOK (or are generated from it); the register's own single-list rule stands.
A-F5 [ordering]. P3a (data pins out of engine) lands BEFORE P2b (`land round`) so the scripted round
  transaction is built against the final pin location — a later package must not invalidate a soaked
  earlier one. Revised order: P1 -> P2a (lever lander) -> P3a -> P2b (round lander) -> rest of P3 -> P4.
A-F6 [2a/2b]. Day-0 re-basing in the landers is EXPLICIT, OFF-BY-DEFAULT, with a mandatory printed
  row diff (the M1b ruling, inherited verbatim) — automation never re-bases itself green.
A-F7 [3a]. The pin move keeps a review-forcing step for DATA changes (prereg-lite: predicted sheet md5
  + row/Y counts + disclosed movers, committed with the data change) — moving pins must not delete the
  ceremony that catches a wrong sheet; and the move UNIFIES the two duplicate in-engine pin blocks
  (4207/5907 today) into ONE declaration — never a mirrored pair in the new location.
A-F8 [3b]. Tombstone-then-freeze: the register's final in-file entry states where the record continues;
  tools/seat/pen.py (and any tool defaulting to the old file) is repointed in the SAME act.
A-F9 [1a]. The de-scoped live-scoring workflow gets RE-ADJUDICATED by the owner (its recorded de-scope
  cause is now false), not silently repaired or retired.
A-F10 [G3]. G3 reads: four NEW standing rulings; it does not delegate existing owner gates (adoption
  words, publish words, the independent read, law retirement remains an owner diff-ruling per 1b).
A-F11 [3c/1e]. Named retirements added (G4): the STATE file retires docs/CURRENT_STATE.md (156
  register-versions stale at review time — the proof hand-maintained state drifts); the incident index
  names the register-prose extraction it replaces.
A-F12 [2a/2b]. The landers TIME every landing (start/end per step, machine-recorded): the measured
  landing cost is quoted before any turnaround target is promised (the M2 ruling, inherited).
A-F13 [1a]. S1 relaxed: cross-machine byte-exact board rebuild is ALREADY PROVEN on record (CI rebuilt
  a candidate board byte-identical on a GitHub runner) — the CI rebuild gate needs only a cheap
  re-proof on the current runner class, not a research project.
A-F14 [2a/2b]. The landers take the build lock and use explicit-path commits (v786), asserted in
  their self-tests.
A-F15 [operational]. The fv-provenance suite never runs on the shared box (v787: it overwrites a
  shared pickle) — the landers and CI exclude it there; it runs only in isolated workspaces.
