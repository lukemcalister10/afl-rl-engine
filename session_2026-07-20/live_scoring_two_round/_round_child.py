#!/usr/bin/env python3
"""Apply ONE round in a FRESH process — the genuine stop/restart boundary of the two-round proof.

The parent proof stops entirely after committing round 15 and spawns THIS child to apply round 16.
The child imports the engine from the SCRATCH repo, arms the gate IN THIS PROCESS ONLY (scratch), and
applies the snapshot through the staged transaction, then (post-commit) refreshes the UI bundles. It
reads NOTHING from the parent's memory — only the committed on-disk scratch state — so a green child
proves round 16 resumes purely from the committed round-15 files.

Usage:  _round_child.py <scratch_repo> <snapshot_json> <round> <generated_at> <result_json_out>
Exit 0 = applied; the result (store/board/history/ui evidence) is written to <result_json_out>.
"""
import json
import os
import sys

SCR = sys.argv[1]
SNAP = sys.argv[2]
RND = int(sys.argv[3])
GEN = sys.argv[4]
OUT = sys.argv[5]

RA = os.path.join(SCR, 'engine', 'rl_after')
sys.path.insert(0, os.path.join(RA, 'ingestion'))
sys.path.insert(0, RA)
import staged_apply as SA        # noqa: E402
import score_ingestor as SI      # noqa: E402

os.environ.setdefault('RL_VENDOR', '/home/claude/rl_vendor')
SI.APPLY_DEFAULT = True                              # arm the gate IN THIS PROCESS ONLY (scratch)
os.environ['INGEST_SCORE_APPLY'] = 'two-round-restart-token'

with open(SNAP) as f:
    snapshot = json.load(f)

ap = SA.StagedRoundApplier.for_repo(SCR)
res = ap.apply_snapshot(snapshot, generated_at=GEN)
ui = ap.refresh_ui()
out = {
    'round': res.round, 'players_applied': res.players_applied,
    'store_before': res.store_md5_before, 'store_after': res.store_md5_after,
    'board_before': res.board_md5_before, 'board_after': res.board_md5_after,
    'guard5_green': res.guard5_green, 'ledger_total': res.ledger_total,
    'history': res.history, 'ui': {k: ui[k] for k in ui if k != 'stderr_tail'},
    'txn_dir': os.path.basename(res.txn_dir),
}
with open(OUT, 'w') as f:
    json.dump(out, f)
print("child applied R%d in a fresh process: store %s->%s board %s->%s guard5=%s"
      % (res.round, res.store_md5_before[:8], res.store_md5_after[:8],
         (res.board_md5_before or '')[:8], res.board_md5_after[:8], res.guard5_green))
sys.exit(0)
