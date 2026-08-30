#!/usr/bin/env python3
"""Turn FW1_EDIT_PLAN.json (emitted on a loaded engine) into the act spec the lander flies.

Mechanical: no arithmetic of its own, no name resolution of its own. Everything numeric came from
the pass that ran against the ingestor's own `_mean` and the ingestor's own `ROUND_DECIMALS`.
"""
import json, os, sys

REPO = '/home/user/afl-rl-engine'
EV = os.path.join(REPO, 'docs', 'evidence', 'finals_fw1_2026-08-30')
PLAN = os.path.join(EV, 'FW1_EDIT_PLAN.json')
OUT = os.path.join(EV, 'ACT_SPEC_FW1_EDIT.json')

plan = json.load(open(PLAN))

# A NO-OP FIELD IS DROPPED, NOT DECLARED. The validator refuses `old == new` — rightly, since an
# edit that changes nothing cannot be told from an edit that failed to apply. `games` always moves
# (+1); `avg` can land on its own old value when the score equals the running average closely
# enough to survive two-decimal rounding, and that is a real no-op, not an error.
edits, dropped = [], []
for e in plan['edits']:
    if e['old'] == e['new']:
        dropped.append(e)
        continue
    edits.append(e)

by_key = {}
for e in edits:
    by_key.setdefault(e['key'], []).append(e)
zero = [k for k in {e['key'] for e in plan['edits']} if k not in by_key]
if zero:
    raise SystemExit('HALT: %d player(s) would carry no edit at all: %s' % (len(zero), zero[:5]))
missing_games = [k for k, v in by_key.items() if not any(x['field'].endswith('.games') for x in v)]
if missing_games:
    raise SystemExit('HALT: a played game must always increment games; %s did not' % missing_games[:5])

spec = {
    'schema_version': 1,
    'act_kind': 'store-edit',
    'act': ('FINALS WEEK 1 APPLIED AS A STORE EDIT — 92 players at four clubs gain one game and a '
            're-averaged 2026 season row. The calendar is not touched, because a finals week was '
            'never a calendar event: the store has always carried finals inside the season row '
            '(Bontempelli 2016 reads 26 games — 22 home-and-away plus four finals).'),
    'date': '2026-08-30',
    'owner_word': ('"Explicit word given" (2026-08-30), on the FW1 direct-movers preview. On the '
                   'lane: "We\'re literally just updating player averages and game counts. Before '
                   'round 14 we didn\'t add games one by one, we just priced based off averages and '
                   'total season game counts. It really shouldn\'t be that hard." And on scope: '
                   '"As long as it doesn\'t impact the movers list still being accurate as of each '
                   'round since round 14."'),
    'authority': 'owner word 2026-08-30 — the finals scores, and the lane they land through',
    'prereg': {
        'path': 'docs/evidence/finals_fw1_2026-08-30/PREREG.md',
        'board_before': 'f81dbcda220110ad0113ae0633b6c34e',
        'board_after': None,
        '_doc_board_after': ('null: a board priced from scores nobody has put through the real '
                            'builder cannot be predicted without running it, and copying it out of '
                            'a build already run is not a prediction. The falsifier for this act is '
                            '`expected_movers` below — every mover, by key and both values, '
                            'measured on a loaded engine whose control pass reproduced the live '
                            'board with 0 diffs.'),
        'reference_board': None,
        'kill_switch': None,
    },
    'edit': {
        'store': edits,
        'expected_movers': plan['expected_movers'],
        '_doc': ('%d edits over %d players: scoring[2026].games +1 and a re-averaged '
                 'scoring[2026].avg, and NOTHING else. The career `games` field is deliberately '
                 'untouched — round_apply._merge_into_store does not touch it either, and an edit '
                 'that also moved it would be a second writer inventing a rule the ingestor never '
                 'had. Averages are round((avg*games + score)/(games+1), 2) through the ingestor\'s '
                 'OWN `_mean` at the ingestor\'s OWN ROUND_DECIMALS=2, called rather than restated.'
                 % (len(edits), len(by_key))),
    },
    'identities': {
        'moves': ['store', 'board'],
        'unmoved': ['engine_head', 'rl_model', 'fv', 'config', 'register', 'as_of_round'],
    },
    'column': {
        'id': 'fw1-finals-week-1-30-8',
        'label': ('30/8 FINALS WEEK 1 — 4 clubs, 92 players, one game each added to the 2026 '
                  'season row. The calendar round is UNTOUCHED at 24, so this is a board move '
                  'outside a round.'),
        'after_round': 24,
    },
    'lineage': {
        'doc': 'docs/evidence/finals_fw1_2026-08-30/PREREG.md',
        'owner_ruling_id': ['FW1_2026-08-30_explicit_word_given',
                            'FINALS_LANE_2026-08-30_averages_and_game_counts_not_a_round'],
        'owner_ruling': ('Finals scores are applied to the season row, not to the calendar. '
                         'Owner, 2026-08-30.'),
        'authority': 'owner word 2026-08-30',
        'invariants': {},
    },
    'day0_rebase': {'state': 'off'},
    'evidence_dir': 'docs/evidence/finals_fw1_2026-08-30',
    'gates': None,
}

os.makedirs(EV, exist_ok=True)
json.dump(spec, open(OUT, 'w'), indent=1)
print('wrote %s' % OUT)
print('  %d edits over %d players (%d no-op field(s) dropped: %s)'
      % (len(edits), len(by_key), len(dropped),
         ', '.join('%s %s' % (d['key'], d['field']) for d in dropped[:4]) or 'none'))
print('  %d expected movers declared' % len(plan['expected_movers']))

sys.path.insert(0, os.path.join(REPO, 'tools'))
from landing.spec import validate
probs = validate(json.load(open(OUT)))
print('  spec validation: %s' % ('0 problems' if not probs else probs))
if probs:
    raise SystemExit(1)
