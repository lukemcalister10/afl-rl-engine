#!/usr/bin/env python3
"""#326 second rehearsal — add the signed pool_levels block to the curve artifact.

Carried over from the first rehearsal (the block itself is sound); the _doc text is rewritten for the
addendum-5 entry-anchor ruling and the addendum-6 currency law.

The ladder ('curve') and 'pool_value' are NOT touched: the payload identity (the N32 recipe over the
64-pick curve dict) is asserted equal before and after. The artifact FILE md5 moves, and every pin on
it is re-stamped in the same change.
"""
import hashlib, json, sys

PATH = sys.argv[1]
raw = open(PATH, 'rb').read()
doc = json.loads(raw)


def payload_id(d):
    return hashlib.md5(json.dumps({str(k): int(round(v)) for k, v in d['curve'].items()},
                                  sort_keys=True).encode()).hexdigest()


before = payload_id(doc)
assert before.startswith('df766dff'), before

assert 'pool_levels' not in doc
doc['pool_levels'] = {
    "_doc": (
        "N43 SIGNED PER-DIVISION POOL LEVELS (owner words, filed #306 comment 5179992080; installed by "
        "directive #326 as amended by its addenda 1-6). VOR, K=15 toward the measured pool aggregate 235.8. "
        "These are owner-signed data: copied verbatim, never recomputed by the engine. The division key is "
        "the store's own 'type' field; ND65+ is type ND at pick >= 65. The rookie draft prices positionally "
        "on future_position (the field the N42b measurement was keyed on). Any row the engine classifies as "
        "pool whose type is outside this set halts and asks. WHAT THE LEVEL DOES (addendum 5, the owner's "
        "consumption-site ruling): it is the ENTRY ANCHOR for a pool entrant -- it stands where the pick "
        "curve's year-zero start value stands for a national draftee, in the year-zero floor and in the "
        "thin-record blend, and it is the ruck prior cap's basis for a pool ruck. Careers still dominate: "
        "the anchor supports thin records only and fades as games arrive. CURRENCY (addendum 6 item 5): "
        "these numbers are ladder/board currency. They enter the engine-value sites (blend, floor) "
        "multiplied by the board factor 1.0524, and the ladder-currency site (the ruck cap's draftval "
        "basis) unconverted. pool_value above keeps its own job -- the pool-wide level on the current "
        "basis, the ladder's pool slot for the pick side, the entrant layer and the display bands -- and "
        "after #326 no player price reads it."),
    "k": 15,
    "measured_pool_aggregate": 235.8,
    "msd_completion_optimism_caveat": "+4.7-8.4% (travels with the MSD level, printed beside it wherever it is shown)",
    "rd_division_level": 261.6,
    "rd_position_field": "future_position",
    "rd_positional_shrink_target": 262.2,
    "signed_flat": {
        "IRE": 133.4,
        "MSD": 286.8,
        "PDA": 194.3,
        "PDN": 123.0,
        "PDS": 145.0,
        "SSP": 252.8,
        "UNR": 103.7,
    },
    "signed_nd65_plus": {
        "_rule": ("THE CAP IS A LAW, NOT A NUMBER: the price is min(measured_k15, the ruled curve's pick "
                  "cap_against_curve_pick) resolved against the ladder in force AT BUILD TIME. A curve "
                  "re-derivation moves it with no edit here."),
        "cap_against_curve_pick": 64,
        "measured_k15": 266.1,
    },
    "signed_rd_positional": {
        "KPD": 300.3,
        "KPF": 216.0,
        "MID": 294.8,
        "RUCK": 282.5,
        "SD": 246.9,
        "SF": 231.5,
    },
}

after = payload_id(doc)
assert after == before, 'payload identity moved: %s -> %s' % (before, after)

out = (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()
open(PATH, 'wb').write(out)
print('payload identity UNCHANGED %s' % before)
print('file md5 %s -> %s' % (hashlib.md5(raw).hexdigest(), hashlib.md5(out).hexdigest()))
