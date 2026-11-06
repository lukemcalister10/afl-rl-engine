# P4-5 — The stale-docs sweep (LOW; last)

**Goal.** Every document under docs/ (14 top-level .md files, docs/runbooks, START_HERE.md, REQUIRED_INPUTS.md,
ui/MAINTAINER.md, the README) says what the tree does AFTER Phases 2–5: no sibling, no LTI register, no round
lane, no selftest/claims/day0, no hand flip, no "NOT ADOPTED"; the weekly command, the player tool, the rollover
and the as-at boards documented in one place each. docs/register/LATEST.md gets one closing entry naming the
plan's landing commits.

**Why.** Every retired mechanism still has a page; an agent reading the docs first is led to the wrong tool.

**Rules.** `python3 tools/rulebook_lint.py` and `acceptance doc_lint` green; do not rewrite history files
(docs/OPEN_ITEMS_REGISTER.md is byte-sealed; docs/CHANGELOG.md append-only); the RULEBOOK changes only with the
owner's word (none expected: its retired paragraphs already say so).

**Proof.** The two lints; a fresh-eyes read by an agent given only START_HERE.md and asked to run a finals week
on a copy (`tools/ingest --check`) and to describe how an engine act lands — both must come back right.

**Lands via.** Plain commit.
