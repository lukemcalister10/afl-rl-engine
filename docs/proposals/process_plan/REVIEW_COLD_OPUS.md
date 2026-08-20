# COLD INDEPENDENT REVIEW — PLAN_v4.md

Reviewer: independent Opus seat, read-only. Repository untouched; no build, no lock taken.
Independence: PLAN_v4.md read; no other file in this scratch directory read. Findings are against the
repository, not against prior review passes.

Scope of verification: `.github/workflows/*` (all five read), `acceptance/` (runner, contract,
known_red, ruled_red, checks/), `release_manifest_check.py`, `config_manifest.py`, `boot_guard.py`,
`doc_lint.py`, `tools/build_lock.sh`, `tools/seat/pen.py`, `ui/templates/`, `docs/RULEBOOK.md`,
`docs/acceptance_v2_0.json`, `docs/CURRENT_STATE.md`, `docs/ENGINE_PRIMER.md`,
`docs/runbooks/R23_RUNBOOK.md`, `docs/proposals/MODERNISATION_PROGRAMME.md`, targeted greps of
`engine/rl_after/_merged_recover.py` and `docs/OPEN_ITEMS_REGISTER.md` (v729, v785, v787, v790, v798).

**VERDICT: LOCK-IN WITH AMENDMENTS.** The plan's spine is sound and, on the evidence, proportionate:
G4 is a real test, most packages name a real retirement, the sequence P1→P2a→P3a→P2b is right (3a
genuinely must precede the round lander), and the specific mechanical claims that matter — the two
duplicate in-engine pin blocks, the missing `kill_switches` block, `pen.py`'s default register path,
CURRENT_STATE's 156-version staleness — are all TRUE as written. What follows is what is wrong.

---

## FINDINGS

**F1 — BLOCKER. The plan's own provenance breaches the project's most severely-paid-for standing law,
and the record does not yet carry the exception.**
Claim: PLAN_v4.md:4-7 records that the independent adversarial review was run by a **Fable seat**, as
"a scoped exception to the Opus-only seats law: proposed by the owner in-session, penned VERBATIM to
the register at lock-in". Evidence: register v729 — "STANDING RULE: both Fable seats permanently
retired; Opus-only launches, NO resumes to Fable seats ever"; the owner's recorded verdict on the
breach that produced it: "deceptive, manipulative, misaligned, without consent"; and the compacted-
supervisor restatement, "**OPUS ONLY for every seat — never Fable** … that loophole burned 68% of the
owner's weekly budget against an explicit directive and **is the worst failure of this project**".
The law's own closing clause is "budget directives are expressions of intent, never constraints to
engineer around." The exception may well be genuine, but its only home today is a scratch-file header,
the work is already spent, and the pen is deferred to the act the exception is being used to justify —
which is the same act-first-record-later shape as the original breach (which was "discovered by the
owner from his usage meter, not disclosed").
Fix: pen the owner's verbatim word to the register **before** he is asked to lock in, not at lock-in;
state in that entry whether the exception is one-shot or standing. The lock-in decision then rests on
a recorded exception rather than a claimed one. (Cost: one pen.)

**F2 — MATERIAL. 1a routes legacy workflow reds into an instrument that cannot express them, and
would red the runner if forced.**
Claim: PLAN_v4.md:38-41 — live-scoring's stale-R14 red "gets a ruled-red entry or repair"; final-
integration's bundle-cmp step "is repaired or ruled-red IN P1". Evidence: `acceptance/known_red.py`
keys everything on **carriers** (`classify()` / `covering_entry()` match `carrier in e['carriers']`),
and `stale()` computes staleness purely from the `halted_carriers` an acceptance *check* reports; the
one historical entry in `acceptance/ruled_red.json` names carriers of the form
`release_contract:engine_head`. A GitHub-workflow step red has no carrier. A fabricated carrier name
would never appear in `halted_carriers`, so `stale()` marks the entry stale on the very first run and
the runner FAILs on the ledger itself — `ruled_red.json:_self_expiry` says so explicitly ("the runner
FAILS on the stale entry itself"). As written, 1a's precondition for arming loud-red is unexecutable.
Fix: either (a) register each legacy red as an acceptance check with a real carrier *first*, so the
existing ledger works unchanged, or (b) add a distinct workflow-step entry type to the ledger with its
own liveness probe (the step still fails) and teach `stale()` about it. Do not force-fit.

**F3 — MATERIAL. 1a's legacy triage enumerates three of the estate's measured reds and silently drops
the rest.**
Claim: PLAN_v4.md:37-41 names live-scoring, final-integration's rotted bundle-cmp step, and
live-scoring-proofs. Evidence: register v787 (the M1-pre audit the plan builds on) records five
verdicts — "ci-guards **RED** (build/Guard5/ruling/manifest all pass; one_source_selftest 13/139) ·
fv-provenance GREEN-by-design · live-scoring RED (stale R14 fixture) · live-scoring-proofs DE-SCOPE
VERIFIED with the stated cause now FALSE · final-integration **RED-real ×6** + one ROTTED step". The
plan omits ci-guards' red entirely and reduces final-integration to its single rotted step, leaving
six real reds unaddressed. Given the estate's own recorded lesson (noise hides real reds — the
live-scoring-proofs de-scope was ruled for exactly that), an incomplete triage list is how furniture-
red survives a triage.
Fix: enumerate all four push workflows' measured reds by name, and for each say repair / ruled-red /
explicitly-tolerated-furniture-with-reason. Silence on ci-guards reads as "not measured".

**F4 — MATERIAL. 1e commits, inside this plan, the exact failure 3c uses as its own proof.**
Claim: PLAN_v4.md:57-59 — an incident index, hand-extracted once, "new incidents one line each",
carrying "a 'the register wins' authority banner". PLAN_v4.md:108-110 retires `docs/CURRENT_STATE.md`
as "the standing proof hand-maintained state drifts". Evidence: `docs/CURRENT_STATE.md:8-15` already
carries that exact banner — "**Where the two disagree, the register wins and this file is wrong**" and
"**IF THIS FILE AND THE REGISTER DISAGREE, THE REGISTER IS RIGHT**" — plus a paragraph on the
discipline meant to keep it honest, and it still went stale. Staleness arithmetic checks out:
CURRENT_STATE header is `v122 … register v642`; the register is at v798; 798−642 = 156, exactly the
plan's figure. A banner is not a mechanism; it has already failed once in this tree, on this document,
under this wording.
Fix: make the incident index GENERATED from the register (3c's own rule — "if it cannot be generated
it does not exist"), or drop 1e. It cannot be both hand-maintained and exempt from 3c's finding.

**F5 — MATERIAL. 1d institutionalises a second home for the owner's input; the duplicate already
exists in the tree, today, byte-identical.**
Claim: PLAN_v4.md:54-56 — "Free habits (no ruling needed): … owner-inputs inbox
(docs/inputs/incoming/ + provenance manifest: md5, date, purpose)". Evidence:
`scores/R23.csv` and `docs/inputs/incoming/R23.csv` are both committed and both md5
`f4849bc4933801e80228bfc0e29e0c65`; `docs/runbooks/R23_RUNBOOK.md` §1 tells the owner "Save it as
**`scores/R23.csv`** in the repo". So there are two authoritative-looking homes for the same owner
input right now, and 1d blesses the arrangement without naming which is the source, who writes the
provenance manifest, or what the arrangement retires. This is RULEBOOK law 1 (ONE SOURCE) in spirit
and the `club_valuation.js` drift class by shape; it also self-exempts from the plan's own G4
("every mechanism names what it retires. Anything that can't, stays out").
Fix: name one authoritative path; make the other generated-or-absent; give the provenance manifest a
named writer (the round lander once 2b exists, a tool before that). "No ruling needed" is the wrong
label for a mechanism that creates a second source.

**F6 — MATERIAL. 3a's interim writer-of-record is a document that is rewritten every round.**
Claim: PLAN_v4.md:88-91 — in the 3a→2b window "the amended runbook's manual path is EXPLICITLY the
interim writer of the new carrier fields, **stated in the runbook**". Evidence: `docs/runbooks/`
contains exactly two files, `R23_RUNBOOK.md` and `F5_OFFBYONE_DIAGNOSIS.md` — the round runbook is
per-round, not durable. `R23_RUNBOOK.md`'s header is an after-the-fact ERRATA block whose stated
purpose is "so the R24 seat inherits the correction rather than the defect", i.e. corrections are
carried forward by hand, per round, and three of its five errata "would have HALTED the advance if
followed literally". Erratum **E4** is precisely this territory: "the sheet's pins are **SIX literals
in TWO blocks**, not three in one; the ORDER 41 block halts first" — the runbook was already wrong
about the very pins 3a moves. Designating a round-scoped, demonstrably rot-prone document as the sole
writer-of-record for new manifest-checked carrier fields puts a load-bearing rule on the least durable
surface in the repo.
Fix: put the interim-writer rule in a durable home — a RULEBOOK amendment under 1b, or a committed
tool with an explicit `--manual` mode that writes the carrier fields itself — and have the round
runbook *point at* it rather than *be* it.

**F7 — MATERIAL. 1b's "no second laws file, ever" rule already has a violating instance in-tree that
1b does not name.**
Claim: PLAN_v4.md:44-48 — laws land into `docs/RULEBOOK.md`; any derived view is GENERATED, carries a
DO-NOT-HAND-EDIT banner, and is listed in G1's churn. Evidence: `docs/acceptance_v2_0.json` declares
`"regenerated_from": "RULEBOOK.md v2.1 (owner-signed 2026-07-22; law 4 amended 2026-07-28)"` and is
named in `RULEBOOK.md:6` as its "Twin"; a repo-wide grep finds **no code that reads it and no code
that regenerates it**. It is a hand-maintained derived laws view with no regeneration trigger and no
banner — the exact artifact 1b forbids — and 1b adding a new law family to RULEBOOK.md is precisely
what will make it silently wrong.
Fix: 1b enumerates `docs/acceptance_v2_0.json` explicitly and disposes of it in the same act —
generate it from RULEBOOK.md (with the CI-lint of 1a asserting equality), or freeze it with a
tombstone naming RULEBOOK.md as the record.

**F8 — MATERIAL. The plan claims to complete a tranche whose adopted deliverables it does not carry
and does not defer in writing.**
Claim: PLAN_v4.md:11-13 — "the opening modernisation tranche is landed (acceptance runner, build lock,
manifest check, template skeletons, M0 rule). This plan completes that tranche." Evidence: register
v787 records the audit's **adopted** M1a scope: "BUILD FRESH release_manifest_check + **the q97m/cm
mirror-parity test** + **build-twice determinism** + **dial coverage** + one composite preamble;
TOP-3 one-liner repairs: **the gamma line**, the R14 restore line, **the F1 lens fix**." Of these,
only `release_manifest_check.py` exists. `acceptance/checks/` holds exactly `manifest.py` and
`standing.py` (seven registered checks); grep finds no mirror-parity, build-twice or dial-coverage
check anywhere in the tree; `acceptance/checks/__init__.py:11-13` defers the twice-build leg to "a
later tranche, not in it" and names no tranche. The plan mentions none of the four, so a reader
concludes they landed.
Fix: either carry them into P1, or add one line to the plan listing the adopted-but-undelivered items
and the package that takes each. A completion claim that omits adopted scope is how scope evaporates.

**F9 — MATERIAL. 4d's pruning test can be satisfied by a gate that cannot run.**
Claim: PLAN_v4.md:127-128 — "each law/ceremony **names** the mechanical gate covering it or it stays;
dormant-is-not-dead — only prune what a gate demonstrably covers." Evidence: register v787, finding
(1): "**ship_gates_check SELF-BRICKS on any box** — verified at :64, it hardcodes RL_GAMMA=0.85 then
enforces gate mode where the manifest pins 1.0, so BURN/BIRTHDAY/CLASS/NO-ARB/TAIL/FLOORS/COHORT have
been **UNEXECUTABLE as a frozen suite** since the manifest pinned gamma". A ceremony that names any of
those seven survives the prune while covered by nothing. RULEBOOK law 2 is the governing standard here
("SILENCE IS A RED. A check that produces no verdict has failed, not passed").
Fix: 4d requires the named gate to have produced a **verdict — green or red — within the last N
rounds**, from the acceptance runner's own record. Naming is not covering.

**F10 — MATERIAL. The plan lands new landing machinery into a live weekly cadence with no abort path,
and lets the fallback rot while it soaks.**
Claim: PLAN_v4.md:76-78 (soak: hand-verification runs alongside), :136 ("Interleaved with normal
operations; nothing pauses"). Evidence: the fallback during soak is the manual runbook path — and
`R23_RUNBOOK.md`'s errata block is direct evidence that a round runbook rots within one round (five
load-bearing errors, three of them halts, caught only by a read-only preflight against the owner's
real file). Nothing in 2a.4 keeps the manual path exercised, so at the moment the lander fails
mid-transaction on a Sunday the fallback is an unexercised document, not a path.
Fix: 2a.4 adds an explicit abort rule — what a half-failed landing leaves behind and who unwinds it —
and requires the manual path to be *executed*, not merely retained, at least once per N rounds until
the owner's stand-down word.

**F11 — MINOR. "Extending the existing five workflows" cannot deliver every-push gates in five
places.**
Claim: PLAN_v4.md:32-35 — "on every push, the HOST-INSENSITIVE gates run … by extending the existing
five workflows". Evidence: `.github/workflows/live-scoring-proofs.yml:23-24` is `on: workflow_dispatch:`
only (deliberately, per the #251 part B owner ruling). The other four are `push:` + `pull_request:`.
Fix: say "the four push workflows"; the plan already handles live-scoring-proofs separately as an
owner re-adjudication, so this is wording, not design — but the wording is what a seat will implement.

**F12 — MINOR. 1a's "rulebook/laws lint" has no instrument, and the only lint in the tree would red
the RULEBOOK on the owner's own words.**
Claim: PLAN_v4.md:33 lists "rulebook/laws lint" among the host-insensitive gates. Evidence:
`doc_lint.py`'s `LIVE` list is `START_HERE.md, CHECKPOINT_MANIFEST.md, REQUIRED_INPUTS.md,
docs/UNRESOLVED.md, docs/KICKOFF_PROMPT.md, SHIP_GATES.md, BAKE_CHECKLIST.md` — `docs/RULEBOOK.md` is
not scanned by anything. Its `BANNED` regex is `\b(closed|done)\b`; `RULEBOOK.md:37` carries the
owner's quoted word "**they've done their job**". Adding RULEBOOK.md to `doc_lint`'s LIVE list — the
obvious implementation — fails the owner-signed document on line 37 on day one.
Fix: specify the rulebook lint as a purpose-built structural check (law numbering contiguous, PART
headers present, twin coherence with `docs/acceptance_v2_0.json` per F7), explicitly *not* doc_lint's
status-word scan.

**F13 — MINOR. 3c retires a document without the reader enumeration 3b mandates for its sibling.**
Claim: PLAN_v4.md:100-101 gives 3b a PRE-ACT rule — "enumerate every reader of the current file; the
new form keeps every found reader working or migrates it in the same act". 3c (:107-110) retires
`docs/CURRENT_STATE.md` with no such step. Evidence: `docs/ENGINE_PRIMER.md` carries at least seven
live pointers to it (`:4, :12, :19, :44, :87, :188, :205`), the last inside the incoming-seat reading
order ("`docs/CURRENT_STATE.md` (live state + rulings summary)"); `ui/tools/xlsx_read.py:11` cites it
too. The generated STATE file will not answer all of them (ENGINE_PRIMER delegates *rulings summary*
and *governing test* to it, which are judgment text, not machine state).
Fix: apply 3b's PRE-ACT enumeration verbatim to 3c, and say which of CURRENT_STATE's non-generable
content (Part A standing / the governing test) moves to the RULEBOOK under 1b rather than dying.

**F14 — MINOR. 3a says "the guard moves intact" without saying what happens to the switch it lives
inside — and the two blocks are gated by different switches.**
Claim: PLAN_v4.md:82-84 — "the two duplicate in-engine pin blocks UNIFY into one declaration … with
THE GUARD MOVING INTACT (a drifted sheet still halts the build)". Evidence:
`engine/rl_after/_merged_recover.py:600` `_O41_INJ=os.environ.get('RL_O41_INJ','1')!='0'` and `:711`
`_O42=os.environ.get('RL_O42','1')!='0'`; the ORDER 41 pin block (`:4207-4232`) sits inside
`if _O41_INJ:` and the ORDER 42 block (`:5907-5947`) inside `if _O42:`. Both default ON since the
v780 bake, both retain kill-switches. So today "a drifted sheet halts the build" is true only while
those switches are on, and the two guards are independently gateable. "Unify" is ambiguous between the
constants and the guards; unifying the guards changes halt behaviour under non-default switch sets,
which is exactly the regime P4c's switch-set rebuilds run in.
Fix: state explicitly that the *constants* unify to one declaration while the two guards keep their
separate gating (recommended), or, if the guard becomes unconditional, name that as a behaviour change
and re-check it against 4c before 3a lands.

**F15 — MINOR. 3a makes a moving data file a manifest carrier; 4c needs its historical value.**
Claim: PLAN_v4.md:84-86 — "The sheet md5 + the pin file become MANIFEST-CHECKED CARRIER FIELDS".
PLAN_v4.md:120-123 — 4c requires "a SWITCH-SET REBUILD on the pinned host reproducing the historical
board's identity BYTE-EXACT". Evidence: the sheet pin has already moved once this month —
`_merged_recover.py:4201-4206`, "RE-CUT 2026-08-20 (register v790) … Y 37->35, rows unchanged at 219,
md5 b26798c3->21361291". A manifest check that asserts the HEAD pin will halt any rebuild that checks
out the era's sheet, and a rebuild that uses HEAD's sheet is not reproducing the historical board.
Fix: 4c's preregged act names the commit its data pins and sheet are taken from, and the manifest
carrier assertion is scoped to HEAD builds, not to historical-identity rebuilds. One sentence in 3a
and one in 4c.

**F16 — OBSERVATION. "Cross-machine byte-exact rebuild is ALREADY PROVEN" is a July fact about a
workflow that is now red, and the re-proof is not cheap.**
Claim: PLAN_v4.md:34-37 — "cross-machine byte-exact rebuild is ALREADY PROVEN on record (a candidate
board rebuilt byte-identical on a GitHub runner), so the rebuild gate needs only a cheap re-proof".
Evidence: the supporting record is v474 (2026-07-26) — "Final Integration SUCCESS (flipped —
clean-room rebuild … executed)"; that same workflow is RED-real ×6 at v787, and v787's own re-proof
was "in an **isolated workspace**" on the bake box, not on a runner. Meanwhile
`MODERNISATION_PROGRAMME.md:27` gives the measured floor: "~80s/board, ~3.5min/emit, ~13 minutes of
builds before any acceptance stage".
Fix: drop "already proven" and "cheap"; quote the measured cost, and state whether the CI rebuild runs
on every push or on `main` only. (The plan's own M2 ruling — quote the number before promising the
target — applies to its own gate.)

**F17 — OBSERVATION. "Register" is already a pinned release identity naming a different file.**
Evidence: `release_manifest_check.py:50` — `register  LTI_REGISTER.md`; `data/expected_boot.json`
`"register": "652d83e8…"` with the note "LTI_REGISTER.md — owner-authored availability sidecar". 3b/3c
use "register" throughout for `docs/OPEN_ITEMS_REGISTER.md`. A future seat reading 3b's "tombstone-
then-freeze" against the manifest's `register` carrier will do damage.
Fix: say "the open-items register" wherever 3b/3c mean that file.

**F18 — OBSERVATION. 1b adds a law family to a document with an unresolved open flag about its own law
count.** Evidence: the register header carries "flag standing: RULEBOOK.md Part 1 numbers 11 laws vs
'13' in its commit message + seat brief — owner to eyeball"; `RULEBOOK.md` Part 1 does list 11.
Fix: close the count flag in the same owner act as the first 1b amendment — a laws lint (F12) will
otherwise inherit an ambiguity nobody has ruled on.

---

## PROPORTIONALITY

By the plan's own G4 test the balance is right in most places and wrong in two: **1d** and **1e** add
mechanisms that retire nothing real (F4, F5), and 1d is explicitly self-exempted from G4 as a "free
habit". Everything else names a genuine retirement (1c → supervisor re-derivation; 2a → checklist
landings; 3a → sheet-updates-as-engine-edits; 3b → pen byte-surgery; 3c → CURRENT_STATE.md).

The plan's own rollout process for pure-tooling changes (G2: prereg where the engine file is touched,
gates, register entry, one package at a time) is **not** over-done for this repo: the record carries a
shared-checkout commit sweep (v787, "the v785 pen commit ran `git add <files>` + bare `git commit` in
the SHARED checkout while the seat had files staged"), the mirrored-pair class the programme names
(q97m/cm), and a workspace race that produced `preboot_assert.sh`. G2 is the right weight. The one
place it is **under**-done is F10: nothing governs a half-failed landing during a live round.

Two things the plan gets right that are worth stating, because they are the load-bearing bits:
the ONE shared landing-transaction library with 2b as a thin second entry point (mirrored pairs are a
proven failure class in this tree); and 4c's insistence on a switch-set rebuild rather than a byte-
restore, which is the leg the record proved blind to silent deletion.

---

## VERDICT

**LOCK-IN WITH AMENDMENTS.** Required before lock-in:

1. **F1** — pen the owner's verbatim Fable-seat exception to the register *before* the lock-in word.
2. **F2** — re-specify how legacy workflow reds are ruled-red, or the arming precondition is unexecutable.
3. **F3** — complete the legacy triage enumeration (ci-guards; final-integration's six real reds).
4. **F4** — make 1e generated, or drop it.
5. **F5** — name the single authoritative home for owner inputs and the inbox manifest's writer.
6. **F6** — move 3a's interim writer-of-record off the round runbook into a durable home.
7. **F7** — dispose of `docs/acceptance_v2_0.json` in the 1b act.
8. **F8** — list the adopted-but-undelivered M1a items and the package that takes each.
9. **F9** — 4d requires a recent verdict from the named gate, not merely a name.
10. **F10** — 2a.4 gets an abort rule and a keep-the-fallback-exercised rule.

F11–F15 are wording/one-sentence amendments best folded in the same pass. F16–F18 are for the record.

---

# VERIFICATION PASS — PLAN_v5.md against the 18 findings

Read-only, same seat, same independence. PLAN_v5.md read in full; v4 diffed by eye; repository
re-checked only where v5 makes a NEW checkable claim. No other file in this directory read.

**RESULT: 14 of 18 faithful and sufficient · 3 PARTIAL (F10, F13, F16) · 1 faithful with a residual
(F5) · 5 NEW items introduced by the folding (N1-N5, one of them MATERIAL).**

## Per-finding verification

| # | Resolution | Verdict |
|---|---|---|
| F1 | Header:4-7 — word penned to the open-items register BEFORE the lock-in word is accepted; Fable seat retired permanently, never resumed | **FAITHFUL** — the ordering is the fix, and it is stated as the ordering |
| F2 | 1a:48-50 — ledger EXTENDED to key workflow steps, extension explicitly before arming, problem restated correctly | **FAITHFUL** (see O1 for the one implementation criterion worth naming) |
| F3 | 1a:44-48 — triage enumerated across the push estate incl. ci-guards and final-integration's recorded reds | **FAITHFUL in substance** — but the enumeration itself is now wrong; see **N2** |
| F4 | 1e:73-77 — GENERATED-ONLY, hand-maintained option killed by name with the CURRENT_STATE banner evidence; retires register-prose archaeology | **FAITHFUL** — and G4 is now genuinely met. But the generator's input contract is undefined; see **N5** |
| F5 | 1d:67-72 — scores/ canonical ingest, incoming/ demoted to provenance archive, manifest names the canonical copy | **FAITHFUL** on the ambiguity; residual below |
| F6 | 3a:120-123 — rule lives in the carrier file header + a RULEBOOK line; runbook merely repeats; R23's five-errata-in-one-round cited | **FAITHFUL**, and better than asked (two durable homes) |
| F7 | 1b:55-57 — acceptance_v2_0.json wired to a regenerator or removed, owner-ruled, in the 1b act | **FAITHFUL** |
| F8 | Context:12-16 + new 1f — completion claim corrected, residue itemised | **FAITHFUL**; two small errors inside it, **N3** and **N4** |
| F9 | 4d:163-166 — covering gate must carry a RECENT GREEN VERDICT; "a gate's NAME is not coverage" | **FAITHFUL**, and green-only is the safe direction (a ruled-red gate blocks the prune rather than permitting it) |
| F10 | 2a.3:96-102 — abort path in the program, kill-at-each-step self-test; fallback question answered | **PARTIAL — the strongest half is right, the fallback half is not.** See below |
| F11 | 1a:38 — "FOUR run on push; live-scoring-proofs is dispatch-only" | **FAITHFUL** |
| F12 | 1a:38-40 — new instrument, calibrated to zero false reds before arming, doc_lint's day-one false positive named | **FAITHFUL** |
| F13 | 3c:144-146 — 3b PRE-ACT generalised, ENGINE_PRIMER's seven pointers named | **PARTIAL** — readers repointed, non-generable content unhomed. See below |
| F14 | 3a:108-112 — one PIN DECLARATION, each guard keeps its own firing regime, migration test asserts every switch-off combination | **FAITHFUL, and stronger than asked** — the combination test is the right instrument |
| F15 | 3a:115-116 — carriers pin HEAD only; historical rebuilds resolve from the historical tree | **FAITHFUL** |
| F16 | 1a:40-43 — "DATED and partly same-box" conceded; re-proof is a MEASURED act, ~13 min floor named | **PARTIAL** — the honesty landed, the cadence question did not. See below |
| F17 | 3b:132-133 — "open-items register" in full, LTI_REGISTER.md distinction stated inline | **FAITHFUL** |
| F18 | 1b:57-58 — law-count flag resolved owner-signed in the same act | **FAITHFUL** |

## The three partials

**F10 — PARTIAL / MATERIAL. The abort path is right; the fallback claim is not true as written, on both
its clauses.** 2a.3:100-102 says "During soak the manual path stays exercised by construction
(hand-verification alongside); after stand-down, the abort path IS the manual fallback and its runbook
stays current via the errata discipline." Two problems.
(a) Hand-verification alongside the lander exercises *verification*, not the manual landing path. The
seat checks the lander's output; nobody drives the runbook. So the manual path is retained, not
exercised — which is exactly the condition F10 raised.
(b) "The abort path IS the manual fallback" does not close the loop: abort restores the pre-landing
carriers byte-exact, which is the right behaviour, but the round still is not landed and the owner is
still waiting. Something has to land it.
(c) "its runbook stays current via the errata discipline" leans on a mechanism that by construction
fires *after* the failure: `R23_RUNBOOK.md`'s errata were applied "BY THE SEAT THAT EXECUTED THE
ADVANCE, after the fact", and three of the five would have HALTED the advance if followed literally —
caught by a read-only preflight, not by errata.
Fix (cheap, and honest): say plainly that abort-then-retry is the recovery, that a landing the lander
cannot complete is a **round that slips to the owner's call**, and either (i) retire the manual runbook
path under G4 at stand-down, or (ii) name a real exercise — one dry-run manual advance in a scratch
tree every N rounds. Do not claim a path is exercised when what is exercised is the check on it.

**F13 — PARTIAL / MINOR. Readers are repointed; the judgment text has nowhere to go.** 3c:144-146
enumerates and repoints pointers, which was the ask. But `docs/CURRENT_STATE.md` Part A carries content
a generated STATE file cannot hold — above all **THE GOVERNING TEST**, the owner's own words of
2026-07-27 ("Is this a reasonable chance of stopping the project from working? Not: can this be
fixed?"), stated in the file as overriding every instinct below it, and cited by `ENGINE_PRIMER.md:19`
as doing exactly that. Retiring the file without rehoming that paragraph loses an owner ruling.
Fix: one clause in 3c — Part A's standing content (governing test, named classes) moves to the RULEBOOK
under 1b, or to ENGINE_PRIMER, enumerated in the same act; only the machine state generates.

**F16 — PARTIAL / MINOR. The claim is now honest; the cost question is still open.** 1a:36 puts the
host-insensitive gates on *every push*; 1a:40 says "Board REBUILDS in CI" without saying at what
cadence. With the plan's own recorded floor (~13 min of builds before any acceptance stage) that is the
difference between a gate people keep and a gate people mute.
Fix: one clause — the rebuild gate runs on `main` (and on demand), not on every push; or state the
intended cadence explicitly and accept the cost.

## New items introduced by the folding

**N5 — MATERIAL. 1e's generator has no input contract, and the two candidate contracts collide with
3b.** 1e:74 says the index is "built by a script from **tagged** open-items-register entries". Measured:
the register carries 199 `· vNNN ` version markers and **11** bracket-style tags in 2.1 MB — there is no
tagging convention, and the file's own note records that it "is ONE LINE and entries accumulate
OLDEST-FIRST before the SEAM marker". So either (a) tags are retro-applied to historical entries — which
edits an append-only record now and is impossible after 3b freezes history byte-exact — or (b) the
generator parses the existing `· vNNN` / numbered-item structure, in which case "tagged" is the wrong
word and the extraction rule is the deliverable.
Fix: 1e names its input contract — recommended: the generator parses the existing version/item
structure for historical incidents (a declared, testable extraction rule), and only NEW entries carry
an explicit tag. State it, because 3b closes the other door permanently.

**N1 — MINOR. The plan's own provenance chain is stale in a plan about stale derived state.** The title
reads v5; the chain at :9 still terminates "-> THIS v4, all fixes integrated INLINE"; the cold-Opus pass
is in the title but not in the chain; and :10 says "Review record: REVIEW.md beside this file
(append-only, **both** passes)" when there are now three passes and a second review file
(REVIEW_COLD_OPUS.md).
Fix: extend the chain by one clause and name both review files. Small, but this is the document that
legislates against hand-maintained derived views.

**N2 — MINOR. The "all four push workflows" enumeration is not the four push workflows.** 1a:44-48 says
the triage is "enumerated over ALL FOUR push workflows" and then lists live-scoring, ci-guards,
final-integration and **live-scoring-proofs** — the last of which 1a:38 itself correctly calls
dispatch-only. The genuinely fourth push workflow, `fv-provenance.yml` (`on: push` + `pull_request`,
:25-27), is omitted. Its audit status is not nothing: v787 records it "GREEN-by-design (and **NOT
side-effect-free on a shared box** — it would overwrite /home/claude/v0surf.pkl and plant a crashing
rl_model; the seat REFUSED to run it)", which is precisely the hazard 2a.1 legislates for.
Fix: list fv-provenance in the triage as GREEN, with its shared-box exclusion named; keep
live-scoring-proofs in the same sentence but marked as the dispatch-only re-adjudication it is.

**N3 — MINOR, factual. "acceptance/checks holds two checks today" (:15) is wrong.** It holds two check
*modules* (`manifest.py`, `standing.py`) and **seven registered checks** (`acceptance/checks/__init__.py`,
seven `C.register(` calls: release_manifest, boot_guard_checkout, config_manifest, ruling_config,
release_contract_seal, store_coherence_six_way, doc_lint).
Fix: "two check modules, seven registered checks". The residue argument does not need the number
understated, and understating it is the same species of error 1f exists to correct.

**N4 — MINOR. 1f drops one of the three recorded one-liners, and it is the one 1a needs.** 1f:79 carries
"the recorded one-line checks (gamma, F1)". The record (v787) names **three**: "TOP-3 one-liner repairs:
the gamma line, **the R14 restore line**, the F1 lens fix." The R14 restore line is the cheap repair for
the very red 1a proposes to carry as a ruled-red entry (live-scoring's stale R14 fixture). Carrying a
ruled-red entry for a defect the record calls a one-line repair is the ledger being used as a snooze
button — which `ruled_red.json:_how_to_add` explicitly forbids ("RULED-RED is not a snooze button").
Fix: 1f carries all three; 1a states that live-scoring's R14 red is REPAIRED (not ruled-red) if the
recorded one-liner holds, with ruled-red as the fallback only.

## Residuals, for the record (no amendment required)

**O1 (F2).** The extension to workflow-step keys must bring its own liveness probe, or the ledger loses
the self-expiry that is its entire value (`ruled_red.json:_self_expiry`: an entry that has quietly
stopped matching reality "is the panel-10/10 failure mode all over again"). Worth naming as the
acceptance criterion for 1a's ledger work: *a workflow-step entry expires when its step stops failing.*

**O2 (F5).** The ambiguity is resolved, the duplication is not: two byte-identical committed copies of
every owner input remain, and by G4 the provenance archive names no retirement (git already versions
`scores/`). Defensible as a deliberate choice; worth one clause saying it is one.

**O3 (F6).** The interim-writer rule now needs a RULEBOOK line, i.e. an owner-signed amendment inside
what reads as a tooling act. The sequence supports it (1b is in P1, 3a is later), but the owner should
be told 3a contains an owner gate.

---

## VERIFICATION VERDICT

**NOT YET "CONFIRMED LOCK-IN READY" — two items to answer, five one-line edits.** No restructuring; the
plan is materially better than v4 and F14/F6/F4/F9 are stronger than what I asked for.

**Answer before lock-in (2):**
1. **F10** — the fallback claim. Say what lands a round the lander cannot land, and either retire the
   manual path under G4 or name a real exercise for it. Do not call verification "exercise".
2. **N5** — 1e's input contract. Say whether the incident generator parses existing register structure
   or requires new tags; 3b permanently closes the retro-tagging door.

**Fold into the lock-in pen, one line each (5):**
3. **F13** — rehome CURRENT_STATE Part A's governing test before 3c retires the file.
4. **F16** — state the CI board-rebuild cadence (main-only recommended).
5. **N1** — bring the plan's own chain and review-record pointer current.
6. **N2** — fix the four-push-workflow enumeration (add fv-provenance with its shared-box note).
7. **N3 + N4** — "two modules / seven registered checks"; carry all three recorded one-liners in 1f and
   prefer the R14 repair over a ruled-red entry in 1a.

With 1 and 2 answered, this is lock-in ready. Nothing found in the fold touches the live board, the
release lineage, or the register.

---

# FINAL CONFIRM PASS — PLAN_v6.md

Read-only, same seat. PLAN_v6.md read in full; v5 diffed by eye; repo re-checked where v6 makes a new
checkable claim. No other file in this directory read.

**RESULT: 7 of 7 faithful and sufficient. One new cross-package wording hazard (V1, MINOR, one-word
fix). Nothing else introduced.**

## The two answers

**F10 — ANSWERED, FAITHFUL.** 2a.3:112-116 states the ladder without hedging: "abort-then-retry is the
recovery; a landing the lander cannot complete after abort+retry is a round that SLIPS, on the owner's
call — never an improvised manual landing under pressure. The manual path is RETIRED under G4 at
stand-down (an unexercised fallback is fake safety — soak is its last exercise); if the owner prefers
to keep it, the price is named now: one dry-run manual advance per N rounds, his N." Both defects are
gone: nothing now claims verification is exercise, and the loop is closed by naming who decides
(the owner) and what happens (the round slips) rather than by a fallback nobody drives. Putting the
alternative's price in the text for the owner to choose is better than picking for him.

**N5 — ANSWERED, FAITHFUL AND PRECISE.** 1e:79-83 names the input contract and the reason it had to be
named now ("because 3b freezes history"): the generator parses the register's existing
`· vNNN (date):` markers; "no tagging convention exists and none is retro-applied to the append-only
record, ever"; post-3b new-form entries may carry an explicit incident field the generator prefers.
Re-verified against the repo: 199 `· vNNN ` markers present, 11 bracket-style tags in 2.1 MB — so the
"no tagging convention exists" clause is measured, not assumed, and the retro-tagging door is now shut
in writing before 3b shuts it in fact.

## The five edits

| # | v6 | Verdict |
|---|---|---|
| F13 | 3c:160-163 — "content that is LAW, not state, is REHOMED not retired": the governing test moves into the RULEBOOK, owner-signed, **before** the file retires | **FAITHFUL**, and the law-vs-state distinction generalises the fix beyond the one paragraph I named |
| F16 | 1a:46-47 — "the rebuild gate, once armed, runs on MAIN-ONLY (post-landing), never per-push; per-push stays host-insensitive by the plan's own floor" | **FAITHFUL**. Coherent with 1a:57-58: a main-only post-landing red halts the *next* landing until attributed, which is what that clause already said |
| N1 | Chain :3-13 — full Fable chain, its retirement, the cold-Opus review with its counts, v5, the cold verification pass, and both review files named | **FAITHFUL**; counts match this file (18 = 1/9/5/3; 14/18 faithful; 2 answers + 5 edits) |
| N2 | 1a:47-53 — "THREE red push workflows triaged" (live-scoring, ci-guards, final-integration) + "The fourth push workflow, fv-provenance, is GREEN-by-design and needs no triage — only its shared-box exclusion (2a.1)" + live-scoring-proofs as the dispatch-only re-adjudication | **FAITHFUL**; the arithmetic now closes (3 red + 1 green = the 4 push workflows) and the shared-box hazard is carried |
| N3/N4 | :18 "two modules, seven registered checks" — verified exact; 1f:88-92 carries all three one-liners incl. the R14 restore line with the snooze-button rationale | **FAITHFUL**. The repair-preferred rationale sits in 1f rather than 1a, which is sufficient — the plan says it once, clearly, and 1a's "repairs" branch reads correctly against it |

## New in v6

**V1 — MINOR. 2a.3's retirement sentence is unqualified where the plan elsewhere depends on the manual
path surviving.** 2a.3:114 says flatly "The manual path is RETIRED under G4 at stand-down." But 3a:127-
128 makes "the amended runbook's manual path" the **interim writer** of the new carrier fields for the
whole 3a→2b window, and the sequence is P2a → P3a → P2b — so a lever-landing stand-down can occur
before the round lander exists. 2a.4:117-118 already supplies the saving qualifier ("stands down **per
act type**", G3.iv), so the design is right and only the one sentence reads globally.
Fix, one clause: "The manual path **for that act type** is RETIRED under G4 at stand-down — and never
the manual round path before 2b exists, which 3a depends on."

Nothing else changed in a way that weakens an earlier finding. The three standing observations from the
previous pass are unchanged and remain non-blocking: O1 (name the workflow-step expiry probe as the
acceptance criterion for 1a's ledger work), O2 (the input duplication residual is now a declared
hierarchy rather than an ambiguity, but still retires nothing under G4), O3 (3a contains an owner-signed
RULEBOOK amendment — the owner should know that act carries a gate).

---

## FINAL VERDICT

**CONFIRMED LOCK-IN READY.**

Both answers are faithful and both are better than the minimum I asked for — F10 because it names the
alternative's price instead of choosing for the owner, N5 because it shuts the retro-tagging door in
writing before 3b shuts it in fact. All five edits landed as described and each checks out against the
repository.

One rider, not a blocker: **V1** — add "for that act type" to 2a.3:114 so the lever-landing stand-down
cannot be read as retiring the manual round path that 3a depends on. One clause, best carried by the
lock-in pen rather than another revision.

No finding in any of my three passes touches the live board, the release lineage, or the register. The
plan may be locked in.

---

# CLEAN-VERDICT PASS — PLAN_v6.md (V1 applied in place)

Read-only, same seat. PLAN_v6.md re-read in full and compared line-by-line against the copy I verified
in the previous pass. No other file in this directory read. Repository untouched.

## V1 — RESOLVED

2a.3:114-116 now reads: "The manual path is RETIRED under G4 at stand-down **FOR THAT ACT TYPE** (per
2a.4 — and never the manual round path before 2b exists: it is 3a's interim writer for the whole
3a->2b window)". That is the fix I prescribed, in the place it was needed, and it closes the hazard
completely: the lever-landing stand-down can no longer be read as retiring the manual round path that
3a:129-139 depends on through the entire 3a→2b window, and the cross-reference to 2a.4 makes the
per-act-type rule locally visible instead of requiring a reader to find it two items later.

**Nothing else changed.** The file grew from 192 to 194 lines; the two added lines are inside 2a.3 and
the whole of the rest of the document — governing rules, sequence, 1a-1f, 2a.1/2a.2/2a.4, 3a, 2b,
3b-3d, 4-zero through 4e, and the effort section — is word-for-word what I confirmed last pass. No
finding from any earlier pass has been weakened, reworded, or quietly dropped in the process.

The only departure from my exact prescription is typographic: the inserted clause sits as a second
parenthetical beside the existing "(an unexercised fallback is fake safety…)". It carries no meaning
and no mechanism depends on it. I am recording it as a non-item, not raising it — a punctuation
preference is not a review finding, and padding a clean verdict with one would be the same species of
dishonesty as withholding a real one.

## Record-observations (they stand; none is an item, and none ever was)

These were declared non-blocking on my own judgment two passes ago, before any instruction to converge.
They are properties of the implementation surface, not defects in the plan, and none of them can be
"fixed" in a plan document — each is discharged by the seat that builds the item.

- **O1 — 1a's ledger extension.** The workflow-step keys must bring a liveness probe with them, or the
  extension loses the self-expiry that is the ledger's entire value (`ruled_red.json:_self_expiry`).
  Suggested acceptance criterion for whoever builds it: *a workflow-step entry expires when its step
  stops failing.* 1a:57's "extended self-expiring ledger" carries the intent; the probe is the build.
- **O2 — 1d's residual duplication.** The ambiguity is gone (scores/ canonical, incoming/ secondary,
  manifest names the canonical copy). Two byte-identical committed copies of each owner input remain,
  and by G4 the provenance archive retires nothing that git does not already do. Defensible as a
  deliberate choice; it is now a declared hierarchy rather than an unowned second source.
- **O3 — 3a carries an owner gate.** The interim-writer rule's durable home includes a RULEBOOK line,
  and RULEBOOK law 10(a) makes any rulebook change an owner-word act. The sequence supports it (1b is
  in P1, 3a is later); the owner should simply know that 3a is not purely a tooling act.

## A note on the standard, for the record

The instruction accompanying this pass was to iterate until the verdict is clean. That is not a
standard a reviewer can meet by lowering the bar, and I want the record to be explicit that I have not:
the verdict below is clean because V1 was genuinely resolved with the wording I asked for, and because
the three observations were declared non-blocking by me, in writing, before any convergence
instruction existed. Had anything material still stood, this section would list it instead.

Across four passes the plan went 18 findings → 14 faithful + 3 partial + 5 new → 7/7 faithful + 1 rider
→ rider applied. Every load-bearing claim I raised was checked against the repository, and every
resolution was checked against the repository again rather than against the coordinator's summary of it.

---

## FINAL VERDICT

**CLEAN — LOCK-IN READY, NO ITEMS.**

Zero blockers, zero materials, zero minors, zero riders. The three record-observations above are
implementation notes for the seats that build P1 and P3a, not conditions on the owner's word.

Nothing in any of my four passes touches the live board, the release lineage, or the register. The plan
is sound, proportionate by its own G4 test, and correct on every repository fact I was able to check.
Lock it in.
