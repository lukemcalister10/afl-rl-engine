"""Re-inject stamp.release into the working board bundle.

sibling_repin regenerates ui/data/board_view_working.js via extract_board_view, which does not emit
the `release` block; in a weekly round it is round_finalize that calls
round_movers.inject_release_contract right after the refresh. This act moves the board outside a
round, so the same injection is done here explicitly. Idempotent.
"""
import json
import os
import sys

REPO = '/home/claude/dobwrite'
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
import round_movers as MV

working = os.path.join(REPO, 'ui', 'data', 'board_view_working.js')
rel = MV.inject_release_contract(working, REPO, 22)
print(json.dumps(rel, indent=1, sort_keys=True))
