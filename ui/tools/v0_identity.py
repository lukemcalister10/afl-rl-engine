# -*- coding: utf-8 -*-
"""THE INPUTS AN ENTRY PRICE ACTUALLY DEPENDS ON — one definition, two callers.

`gen_v0_sidecar.py` writes `ui/data_aux/v0.js`; `extract_board_view.py` reads it and decides whether
it may be joined to the board it is publishing. Until 2026-08-31 that decision compared the sidecar's
stamped BOARD and STORE md5 against the bundle's. Both move on every round advance — and v0 does not.
The generator's own docstring says so:

    "v0 is a draft-time constant off a FROZEN surface: _ageR(p) is age as of the draft year and the
     slot key depends only on (future position, draft age, pick), so v0 does not move on a round
     advance. It moves only when the store changes a player's dob / pick / type / future position,
     when the v0 surface or a ruled curve is re-cut, or when the roster changes."

So the gate contradicted the file's own stated invariant, and the contradiction had teeth: FW1 moved
the store, the stamp named the old one, the join refused, and every player card lost its entry price
for a day. MEASURED at that landing: 804 of 804 entry prices were byte-identical across the move. The
refusal protected nothing and cost everything.

REGENERATING ON EVERY LANDING IS NOT THE FIX EITHER. The generator loads the engine — 580 seconds,
measured — so making it a landing step would add ~10 minutes to every act to reproduce a file that
did not change. What is needed is a gate that tracks the inputs rather than the calendar.

THIS SIGNATURE IS THAT GATE. It covers exactly the store fields the slot key derives from, read as
RAW JSON so both callers compute it without an engine — the one property that lets a single function
serve the writer and the reader instead of a mirrored pair that drifts. A score applied to a season
row touches none of these; a corrected date of birth, a re-keyed pick, a changed future position, a
player entering or leaving the roster all do, and each of those genuinely moves an entry price.
"""
import hashlib
import json

#: The store fields an entry price derives from. Extending this list is a DELIBERATE act: a field
#: added here invalidates every existing sidecar (by design — the signature is meant to change when
#: the inputs do), and a field wrongly omitted lets a stale entry price publish as current.
ENTRY_INPUT_FIELDS = ('pick', '_by', 'future_position', 'type', '_pool', 'draft_stream',
                      'stream_pick', 'stream_year')

SIG_VERSION = 'v0-entry-inputs-1'


def entry_inputs_sig(store_rows):
    """A stable digest over every player's v0-determining inputs.

    `store_rows` is the parsed rl_model_data.json list. Rows without a key are skipped — they cannot
    carry an entry price and cannot be joined to a board row. Sorted by key so the digest is a
    function of CONTENT and not of file order.
    """
    parts = []
    for row in store_rows:
        key = row.get('key')
        if not key:
            continue
        parts.append('|'.join([str(key)] + [repr(row.get(f)) for f in ENTRY_INPUT_FIELDS]))
    parts.sort()
    h = hashlib.sha256()
    h.update((SIG_VERSION + '\n').encode('utf-8'))
    h.update('\n'.join(parts).encode('utf-8'))
    return h.hexdigest()


def entry_inputs_sig_of_store(store_path):
    """The same digest, read straight off a store file."""
    with open(store_path, encoding='utf-8') as fh:
        return entry_inputs_sig(json.load(fh))
