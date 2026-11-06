# P4-5 — The stale-docs sweep (LOW; last)

**Depends on.** Every other brief that has landed (it documents the end state). Run it once, after the last one.

**Done when.** Every live document says what the tree does after the items that actually landed: the weekly command
for finals AND rounds (if P2-1 landed), `tools/player`, `tools/rollover`, the as-at columns, the in-transaction flip
(P4-3), no `land round` (if P4-4 landed), no claims step, day-0 optional. Each topic is documented in ONE place and
the others link to it. One closing register entry naming the plan's landing commits, written ONLY with
`python3 tools/seat/pen.py append --entry-file F` (it writes entries/vNNN.md, rewrites docs/register/LATEST.md and
runs `verify`, pen.py:13-21) — never hand-edit LATEST.md or the index.

**Facts (checked at ffb2663b).**
- Live docs: the 14 top-level docs/*.md, docs/runbooks/ (F5_OFFBYONE_DIAGNOSIS.md, R23_RUNBOOK.md,
  STANDING_PROCEDURES.md, WEEKLY_SCORES.md), the root README.md, START_HERE.md, REQUIRED_INPUTS.md, ui/MAINTAINER.md.
- Records that are never rewritten: docs/OPEN_ITEMS_REGISTER.md (frozen; tools/incident_index.py:15, :203 "NEVER
  written to"), docs/CHANGELOG.md (the lineage record, exempt by design, doc_lint.py:17), docs/register/entries/,
  data/release_lineage.json, every docs/evidence/ directory.
- The RULEBOOK changes only on the owner's word (law 10a, RULEBOOK.md:40-42). Its retired paragraphs (P7, P9, P11,
  P12, :145-158) and law 11's claims sentence (:46-48) already say what is retired; P13 is P4-4's (owner word).
- Things that are NOT retired and must not be documented as retired: the lander's pre-transaction self-test
  (tools/landing/selftest.py, run by `tools/land` at cli.py:231/293/335 — NOT by tools/ingest, ingest.py:450-463, P14), acceptance/selftest.py (CI), the manifest-pinned engine
  dials in data/model_config.json (config identity, see the plan README).
- Lints: `python3 tools/rulebook_lint.py` (0 FAIL today) and the acceptance `doc_lint` check
  (acceptance/checks/standing.py:104).

**Change.** For each live doc: grep for the retired names that apply (`claims.py`, `land round`, `restamp.py apply`,
`day0_rebase` as required, `values_r24`-style bare ids, "NOT ADOPTED", "env flag"), rewrite the passage to the current
behaviour or delete it, and link to the one place the topic lives (WEEKLY_SCORES.md for weeks, a ROLLOVER.md from
P3-2, the lander README/runbook for acts). Do not touch the records listed above.

**Must not change.** Any record file; the RULEBOOK (unless the owner gives the word); code.

**Prove it.** `python3 tools/rulebook_lint.py` 0 FAIL; `python3 -m acceptance.runner --profile full` with doc_lint
green; a fresh-eyes check: an agent given only START_HERE.md, asked (a) to run a finals or round week on a scratch
copy with `tools/ingest --check` and (b) to describe how an engine act lands — both answers right, recorded in the
commit message.

**Lands via.** Plain commit.
