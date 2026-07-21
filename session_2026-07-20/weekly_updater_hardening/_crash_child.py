#!/usr/bin/env python3
"""Crash-simulation child (failure-injection proof, JOB 5 recovery case).

Runs a staged apply against a SCRATCH repo and HARD-EXITS (os._exit, skipping every except/finally
handler) immediately AFTER the FIRST live replacement — simulating a power-loss / kill mid-commit.
This leaves the transaction in a non-terminal state (COMMITTING) with the store already swapped but
the board/manifest/ledger not yet — the exact inconsistency the parent proof then RECOVERS.

Usage:  _crash_child.py <scratch_repo> <snapshot_json> [<generated_at>]
Exit 70 = crashed as intended (after the first replacement). Any other exit is a proof failure.
"""
import os, sys, json

REPO_ARG = sys.argv[1]
SNAP = sys.argv[2]
GEN = sys.argv[3] if len(sys.argv) > 3 else "2026-07-20T00:00:00Z"

# resolve the real engine package from the scratch repo (identical code to the live repo)
RA = os.path.join(REPO_ARG, 'engine', 'rl_after')
sys.path.insert(0, os.path.join(RA, 'ingestion'))
sys.path.insert(0, RA)
import staged_apply as SA          # noqa: E402
import score_ingestor as SI        # noqa: E402

os.environ.setdefault('RL_VENDOR', '/home/claude/rl_vendor')
SI.APPLY_DEFAULT = True                       # arm the gate IN THIS PROCESS ONLY (scratch)
os.environ['INGEST_SCORE_APPLY'] = 'crash-proof-token'

with open(SNAP) as f:
    snapshot = json.load(f)


def crash_fault(phase):
    if phase == 'after_first_replacement':
        # the store has been swapped live; the board/manifest/ledger have NOT. Die HARD now,
        # skipping the applier's rollback — the parent must detect + recover this on next run.
        os._exit(70)


ap = SA.StagedRoundApplier.for_repo(REPO_ARG, fault=crash_fault)
ap.apply_snapshot(snapshot, generated_at=GEN)
# if we reach here the fault never fired — that is itself a failure of the proof setup.
os._exit(1)
