# -*- coding: utf-8 -*-
"""THE INPUTS A POSITION MAP ACTUALLY DEPENDS ON — one definition, computable on both sides.

`ui/app/positions_data.js` is a VALUES-FREE map: board player key -> canonical position codes, from
the owner's locations CSV. Until 2026-08-31 its stamp named a BOARD:

    "stamp": {"board": "f2df6e0a2902f48e1df36f35493ba8c1", "expectedBoard": "f2df6e0a", ...}

That is the wrong dependency, and the mismatch it produced was not a defect. The map's content does
not depend on the board — a price move, a round advance, a re-bake all move the board md5 and leave
every position code exactly where it was. Measured when the flag was investigated: the stamp named
board f2df6e0a while the live bundle was c8c2f2b6, and coverage was 804/804 with no stragglers. The
file was correct and its stamp said otherwise.

WHY A WRONG STAMP IS WORTH FIXING EVEN THOUGH NOTHING READS IT. Two reasons, both about the next
reader rather than about today:

  1. IT INVITES A FIX THAT IS NOT NEEDED. Anyone comparing the stamp to the live board sees a
     mismatch and reaches for a repair. That is exactly what happened — it was filed as an open flag
     in the same class as the v0 sidecar defect, which it was not.
  2. THE OBVIOUS REPAIR WOULD BREAK IT. Adding a board pin check to the reader would fail the map
     closed on every landing, taking the pocket panel dark for a reason that has nothing to do with
     the data. A stamp that names the wrong dependency is a trap laid for whoever tidies it up.

WHAT IT REALLY DEPENDS ON, and therefore what this module defines:

  · THE ROSTER — the set of board player keys the map is keyed by. A player joining or leaving the
    league is the one board-side event that genuinely stales this file.
  · THE CSV — docs/inputs/AFFL_Player_Locations.csv, the owner's own input. Re-courier it and the
    position codes can change with no board movement at all.

BOTH ARE COMPUTED FROM RAW BYTES, with no engine and no join re-implementation, so the writer here
and the reader in ui/tests/counting_rule.test.js can compute the SAME figures in two languages
without a mirrored pair that drifts. The signature is deliberately NOT over the CSV's parsed rows:
that would mean re-implementing `nkey` in JavaScript, and a normalisation implemented twice is a
normalisation that disagrees eventually. The file's md5 is coarser and cannot drift.
"""
import hashlib

SIG_VERSION = 'positions-inputs-1'


def roster_sig(board_keys):
    """A stable digest over the board's player-key SET.

    Sorted, so it is a function of membership and not of board order — a re-sorted board that holds
    the same players must not look like a different roster.
    """
    h = hashlib.sha256()
    h.update((SIG_VERSION + '\x1e').encode('utf-8'))
    for key in sorted(set(board_keys)):
        h.update(key.encode('utf-8'))
        h.update(b'\x1e')
    return h.hexdigest()


def csv_md5(path):
    """The owner's locations CSV, by content. Coarse on purpose — see the module note."""
    with open(path, 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()
