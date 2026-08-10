#!/usr/bin/env python3
"""OUT-OF-ROUND HISTORY COLUMN for the never-rises restore.

The standing owner rule (out_of_round_column.py, owner word 2026-07-28): "whenever the board moves
OUTSIDE a round, write a column at that point." This act moves the board without a round being
applied — the never-rises law is restored on the v0 lens path, the frozen surface is re-cut through
the declared refit lane, and the board goes a672ed3a -> 4b448a82 at round 22 — so the column is
written here.

No valuation. This reads the finished board and writes JSON. It computes no value, tunes no
parameter, and touches neither the store nor the engine.

Usage:  python3 register_column.py <repo_root> [--dry-run]
"""
import json
import os
import sys

COLUMN_ID = "g1-never-rises-10-8"
LABEL = "10/8 never-rises restore (R12)"
AFTER_ROUND = 22
BOARD_MD5 = "4b448a821f54180182637983f7a26a9d"


def main():
    root = os.path.abspath(sys.argv[1])
    dry = "--dry-run" in sys.argv
    sys.path.insert(0, os.path.join(root, "engine", "rl_after", "ingestion"))
    import out_of_round_column as OOC

    board_path = os.path.join(root, "data", "rl_build", "rl_app_data.json")
    import hashlib
    raw = open(board_path, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    if got != BOARD_MD5:
        raise SystemExit("HALT: board md5 %s != expected %s" % (got, BOARD_MD5))

    board = json.loads(raw)
    ev = OOC.add_column(root, column_id=COLUMN_ID, label=LABEL, after_round=AFTER_ROUND,
                        board=board, board_md5=BOARD_MD5, dry_run=dry)
    print(json.dumps(ev, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
