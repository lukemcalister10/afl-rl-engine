#!/usr/bin/env python3
"""OUT-OF-ROUND HISTORY COLUMN for THE F5 ROUNDING ACT (2026-08-20).

The standing owner rule (out_of_round_column.py, owner word 2026-07-28): "whenever the board moves
OUTSIDE a round, write a column at that point." This act moved the live board 7a3f4fe2 -> c97a4d9f at
round 23 with no round applied, so a column is owed.

IT IS ALSO WHAT KEEPS THE MOVERS LINEAGE HONEST. `ui/app/movers.js`'s lineage check requires the
NEWEST STORED POINT to be the board the app is serving. Without this column the newest point is round
23, whose report terminates on 7a3f4fe2 — the board this act retired — and the lineage falls to
`mismatch`. With it, the newest point carries the live board and the state reads `bridged`: the
bundle's history was made under an earlier board and is displayed under the current one, which is
exactly true. That is the same reading the D8 adoption and the DOB courier landings took, and for the
same reason.

WHAT THIS COLUMN RECORDS, HONESTLY. Every prior out-of-round column marked a moment that moved player
values. THIS ONE DOES NOT: all 804 players' v/vM2/vM1/vP1/vP2 and all 198 back rows are byte-identical
across the move (measured, 06_f5_builds.txt — the complete board diff is ten fields, none of them a
player). The column is written because the BOARD ID moved and the histories must be able to name that
board as a point, not because anybody's price changed. The label says so, so a reader of the Movers
dropdown is not misled into looking for movement that does not exist.

FIRST COLUMN WRITTEN UNDER THE REPAIRED SORT (Act B, commit 4c3dedd). Its position is recorded by an
explicit `seq` stamped at registration rather than won by an alphabetical race, and `registered_at` is
supplied as provenance. The assert-after-write below is KEPT anyway, exactly as the R23 runbook's
erratum says it should be: it checks the outcome rather than the mechanism, and it costs nothing.

WRITER OF RECORD: engine/rl_after/ingestion/out_of_round_column.add_column — the same call
register_recut_column.py, register_d8_column.py and register_landing_column.py make. No valuation:
this reads a finished board and writes JSON. It computes no value, tunes no parameter, and touches
neither the store nor the engine. add_column is append-only and idempotent: re-registering the same id
with DIFFERENT values raises.
"""
import hashlib, json, os, sys

COLUMN_ID = "the-f5-rounding-20-8"
LABEL = "20/8 F5 ROUNDING FIX — declared entrant layer 56772->56773 (no player value moved)"
AFTER_ROUND = 23
BOARD_MD5 = "c97a4d9f9fa42597f85517c7850d3943"
PREV_BOARD = "7a3f4fe23207a29095e6d37408a4b727"
REGISTERED_AT = "2026-08-20"


def main():
    root = os.path.abspath(sys.argv[1]); dry = "--dry-run" in sys.argv
    sys.path.insert(0, os.path.join(root, "engine", "rl_after", "ingestion"))
    import out_of_round_column as OOC

    bp = os.path.join(root, "data", "rl_build", "rl_app_data.json")
    raw = open(bp, "rb").read(); got = hashlib.md5(raw).hexdigest()
    if got != BOARD_MD5:
        raise SystemExit("HALT: board md5 %s != expected %s" % (got, BOARD_MD5))
    board = json.loads(raw)

    ev = OOC.add_column(root, column_id=COLUMN_ID, label=LABEL, after_round=AFTER_ROUND,
                        board=board, board_md5=BOARD_MD5, dry_run=dry,
                        registered_at=REGISTERED_AT)
    print(json.dumps(ev, indent=2, sort_keys=True))

    vh = json.load(open(os.path.join(root, "engine", "rl_after", "ingestion", "value_history.json")))
    pts = OOC.selectable_points(vh)
    print("\nselectable points, in display order:")
    for p in pts:
        print("   %-24s %-12s after_round=%s board=%s"
              % (p['id'], p['kind'], p['after_round'], (p.get('board') or '')[:8]))
    last = pts[-1]
    print("\nNEWEST STORED POINT: %s  board=%s" % (last['id'], last['board']))

    if not dry:
        # THE ASSERT-AFTER-WRITE, kept on its own merits (R23 runbook erratum E6).
        if last['id'] != COLUMN_ID:
            raise SystemExit("HALT: the newest stored point is %r, not this column. The movers lineage "
                             "would not name the board the app is serving." % last['id'])
        if last['board'] != BOARD_MD5:
            raise SystemExit("HALT: the newest stored point names board %s, not the live board" % last['board'])
        col = [c for c in (vh.get('columns') or []) if c['id'] == COLUMN_ID][0]
        print("\nASSERTED: the newest stored point is this column, naming the live board %s." % BOARD_MD5)
        print("REGISTERED WITH AN EXPLICIT SEQUENCE (Act B's repair): %s" % json.dumps(col, sort_keys=True))
        # and the value it records IS the retired board's value, unchanged — the point of the label
        vals = (vh.get('players') or {})
        n_same = sum(1 for k, e in vals.items()
                     if (e.get('by_round') or {}).get(COLUMN_ID) == (e.get('by_round') or {}).get('23'))
        n_tot = sum(1 for k, e in vals.items() if COLUMN_ID in (e.get('by_round') or {}))
        print("MEASURED: %d of %d players carry the SAME value at this column as at round 23 — this act "
              "moved no player value, and the history says so." % (n_same, n_tot))


if __name__ == "__main__":
    main()
