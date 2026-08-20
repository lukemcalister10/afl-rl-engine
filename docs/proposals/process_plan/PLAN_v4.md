# THE PROCESS PLAN v4 — LOCK-IN READY (fully integrated; final-pass fixes R2/R3/R4 applied; R1 rides
# the lock-in register pen)

Chain: v1 (drafted) -> SELF_REVIEW (9 findings) -> v2 -> independent adversarial review, Fable seat
(scoped exception to the Opus-only seats law: proposed by the owner in-session, penned VERBATIM to the
register at lock-in per the reviewer's R1 — the record must show the word) (15 findings: 1 BLOCKER/7 MATERIAL/4 MINOR/3 OBS,
verdict LOCK-IN WITH AMENDMENTS) -> v3 (amendments appended) -> reviewer VERIFICATION pass (9/15
faithful, 5 partial, 1 new gap, 1 structural: fold superseded text) -> THIS v4, all fixes integrated
INLINE. Review record: REVIEW.md beside this file (append-only, both passes).

Context: afl-rl-engine, post-D8-adoption; the opening modernisation tranche is landed (acceptance
runner, build lock, manifest check, template skeletons, M0 rule). This plan completes that tranche.

## Governing rules
- G1. No process change moves the board or any value-bearing artifact: byte-exact before/after is the
  standing falsifier for ALL packages. Identity/administrative churn (contract sha, manifest fields,
  and — once 3a lands — the data-pin carrier file) is allowed but ENUMERATED per change; anything
  outside the enumerated set = halt.
- G2. One package at a time in the sequence below; each lands under the EXISTING discipline (prereg
  where the engine file is touched, gates, register entry). New tools earn trust under old rules
  before old rules retire.
- G3. The owner makes four NEW standing rulings: (i) N green rounds for dial-collapse eligibility,
  (ii) dial classification policy-vs-scaffolding, (iii) pruning cadence in ROUNDS, (iv) each
  stand-down of hand-verification per act type. This delegates nothing that is already an owner gate
  (adoption/landing/publish words, the independent read, law retirement per 1b, the A-F9
  re-adjudication) — those all remain owner-worded.
- G4. Net-negative-process test: every mechanism names what it retires. Anything that can't, stays out.

## SEQUENCE (revised at review): P1 -> P2a -> P3a(+runbook amendment) -> P2b -> P3b-d -> P4

## PACKAGE 1 — THE SAFETY NET
1a. CI wiring, host-scoped: on every push, the HOST-INSENSITIVE gates run — committed-artifact hashes,
    manifest coherence, contract check, rulebook/laws lint, runner in identity mode — by extending the
    existing five workflows. Board REBUILDS in CI: cross-machine byte-exact rebuild is ALREADY PROVEN
    on record (a candidate board rebuilt byte-identical on a GitHub runner), so the rebuild gate needs
    only a cheap re-proof on the current runner class before arming. Legacy-estate triage BEFORE any
    loud-red arms, scoped as ruled-red-entries-or-repairs (never a repair-the-estate mandate gating
    P1): live-scoring.yml's every-push stale-R14 red gets a ruled-red entry or repair;
    final-integration's bundle-cmp STEP (the two-phase stamp.release rot) is repaired or ruled-red
    IN P1; live-scoring-proofs.yml is OWNER-RE-ADJUDICATED (its recorded de-scope cause is now false)
    — an owner question, not a silent repair or retirement. Loud-red then binds ONLY to the new
    host-insensitive gates + the self-expiring ruled-red ledger: red on main notifies the owner and
    stands as a halt on landings until attributed. The owner is never notified into furniture-red.
1b. THE LAWS land INTO docs/RULEBOOK.md — the owner-signed single governing document; no second laws
    file, ever. If any derived laws view exists it is GENERATED with a defined regeneration trigger
    (lander-generated per 3c, or CI-linted equal to the RULEBOOK via 1a), carries a DO-NOT-HAND-EDIT /
    "the RULEBOOK wins" banner, and is listed as generated in G1's churn. New laws enter as
    owner-signed RULEBOOK amendments; retiring a law is an owner diff-ruling.
1c. Proof-carrying deliverables: every seat's final act includes a claims file (FIXED schema per act
    type: identities, counts, gate verdicts — including day-0 activation state on every landing, off
    unless explicitly activated); one standard checker verifies claims against artifacts;
    the checker carries its own negative control — a deliberately false claim must fail it, asserted
    in self-test. Retires: supervisor re-derivation of gate-covered facts (judgment review stays).
1d. Free habits (no ruling needed): no codenames in owner-facing text; owner-inputs inbox
    (docs/inputs/incoming/ + provenance manifest: md5, date, purpose); rendered board/movers page
    delivered to the owner at every round.
1e. Incident index: one line per historical incident (what, root-cause class, covering gate),
    extracted ONCE from the register prose it retires as a lookup surface; new incidents one line each.
    The index carries a 'the register wins' authority banner — a lookup surface, never a source.

## PACKAGE 2a — THE LEVER LANDER
2a.1 `land lever`: one command running the full lever-landing transaction (build+proofs, pins, lineage
    append, contract restamp+repin, sibling repin, BOTH UI writers, manifest check, acceptance runner),
    built as ONE shared landing-transaction library (2b becomes a second thin entry point — mirrored
    script pairs drift; the repo's loader/emitter history proves it). The lander: takes the build lock
    and uses explicit-path commits, asserted in self-test; treats day-0 re-basing as EXPLICIT,
    OFF-BY-DEFAULT, with a mandatory printed row diff (the M1b ruling — automation never re-bases
    itself green); TIMES every landing step machine-recorded, and the measured landing cost is quoted
    before any turnaround target is promised (the M2 ruling); never runs the fv-provenance suite on
    the shared box (it overwrites a shared pickle) — isolated workspaces only, and CI excludes it on
    shared runners.
2a.2 Decision-packet template: fixed slots — what changes; who moves AND who doesn't (by name); cost;
    standing-table impacts; what-would-make-it-silly; recommendation; falsifiers. A question earns a
    permanent slot only when the owner has asked it twice.
2a.3 Self-test: the program deliberately breaks each step in a sandbox and asserts the failure is caught.
2a.4 Soak rule: supervisor hand-verification runs ALONGSIDE the lander for its first landings; stands
    down per act type only on the owner's word (G3.iv).
    Retires (after soak): checklist landings, landing-tail ordeals, duplicated verification.

## PACKAGE 3a — DATA PINS OUT OF THE ENGINE (lands BEFORE the round lander)
3a. The pure-data pins (_SHEET_*/O41_INJ_* family) move to ONE data file — the two duplicate in-engine
    pin blocks UNIFY into one declaration (never a mirrored pair in the new location) — with THE GUARD
    MOVING INTACT (a drifted sheet still halts the build). The sheet md5 + the pin file become
    MANIFEST-CHECKED CARRIER FIELDS with the round lander as sole writer once 2b lands (interim
    writer: the amended runbook's manual path, defined at the end of this item), and the pin file
    joins G1's enumerated churn. Data changes keep a review-forcing step: prereg-lite (predicted sheet md5 +
    row/Y counts + disclosed movers, committed WITH the data change). IN THE SAME ACT, the round
    runbook's sheet-pin/ADVANCE-REPIN steps are amended — a manual advance in the 3a->2b window must
    follow a correct runbook, not the one 3a just made wrong — and in that window the amended runbook's
    manual path is EXPLICITLY the interim writer of the new carrier fields, stated in the runbook,
    until the round lander (2b) takes over as sole writer.
    Effect: sheet updates stop being engine edits; engine_head moves ⇔ code changed.

## PACKAGE 2b — THE ROUND LANDER (after 3a)
`land round`: the second thin entry point over the P2a library — sheet/data commits (per 3a's form),
scores staging, preflight, armed catchup, ADVANCE-REPIN, movers page, gates. All P2a lander rules
(lock, explicit paths, day-0, timing, fv-provenance exclusion) apply identically.

## PACKAGE 3b-d — THE REST OF THE TIDY-UP
3b. Register evolution: PRE-ACT — enumerate every reader of the current file; the new form keeps every
    found reader working or migrates it in the same act. Then TOMBSTONE-THEN-FREEZE: the file's final
    in-file entry states where the record continues, tools/seat/pen.py (and any tool defaulting to the
    old file) is repointed IN THE SAME ACT, and the owner's word amending the register's own
    single-list rule ("nothing is on a list unless it is in THIS file") RIDES THE ACT — that rule is
    owner-authored and only his word amends it. History frozen byte-exact forever; new entries as
    append-only files; index generated. Retires: pen byte-surgery.
3c. STATE file: machine-generated by the lander at every landing (current identities, queue, laws
    pointer). GENERATED-ONLY — if it cannot be generated it does not exist. Retires (G4, named):
    docs/CURRENT_STATE.md, the hand-maintained predecessor that sat 156 register-versions stale at
    review time — the standing proof hand-maintained state drifts.
3d. Remaining runbook errata absorbed; reusable scratch scripts promoted to tools/ with names.

## PACKAGE 4 — THE RETIREMENT ERA (only after 1-3 soak)
4-zero. PREREQUISITE, first: the declared kill_switches block in the config manifest (the named fix on
    record, never delivered) — without it, collapse proofs cannot run under gate mode.
4a. Dial classification (owner rules, G3.ii): scaffolding vs policy. Policy dials keep switches forever.
4b. The one ROLLBACK fire drill before the first collapse: restore the tagged artifact BYTES + boot
    guards accept them (tags are bytes, not recipes). Rebuild-from-source parity is secondary,
    best-effort; its failure is a reproducibility finding, not a rollback failure.
4c. THE RETIREMENT GATE, distinct from 4b BY DESIGN: collapsing a dial requires a SWITCH-SET REBUILD
    on the pinned host reproducing the historical board's identity BYTE-EXACT — never a byte-restore,
    which is precisely the leg the record proved blind to silent deletion. BEFORE the first collapse,
    the STANDING must-move positive control enters the suite (the per-collapse rebuild proves only the
    dial being retired; the standing control is what catches the NEXT silent deletion). Then: one dial
    at a time; eligibility = N green rounds (G3.i); paired proof (live board unmoved AND the
    switch-set rebuild); each collapse its own preregged act.
4d. Pruning review at owner cadence in ROUNDS (G3.iii): each law/ceremony names the mechanical gate
    covering it or it stays; dormant-is-not-dead — only prune what a gate demonstrably covers.
4e. Round-advance automation milestones: seat+verify -> lander+verified claims -> lander to STAGED +
    the owner's one word publishes -> full-auto only on a sustained flawless record (may be never).
    The publish word is and remains an owner gate.

## Effort, honestly
Estimates are ±2x guesses (the record says things take longer): P1 ~1 session, P2a ~2 sessions,
3a ~half, 2b ~half-to-1, 3b-d ~1, P4 spread over rounds; soak is ROUND-clocked, not session-clocked.
Interleaved with normal operations; nothing pauses. No elapsed-weeks promise is made.
