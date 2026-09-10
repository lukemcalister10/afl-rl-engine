#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""finals_report.py — its tests, against the FW1 report that actually shipped.

THE STRONGEST AVAILABLE TEST IS A REBUILD OF HISTORY. FW1's weekly report was written by hand in
2026-09-02 and has been on the board ever since; its column, its edit list and its scores are all
still in the tree. So this rebuilds that report from FW1's edit list through the LANDING'S writer and
asserts it comes back identical — same points, same 92 scores, same 804 players, same per-player
values and deltas, same txn_id. A writer that reproduces a report a human made, on real data, is a
writer that can be trusted to make the next one.

It also asserts the two things the writer must never do: invent a score the store did not receive
(every score is rebuilt from `new_games*new_avg - old_games*old_avg` and cross-checked against the
owner's own CSV), and fire on an act that is not a finals week.

Run:  python3 engine/rl_after/ingestion/test_finals_report.py     (exit 0 = all pass)
"""
import collections
import csv
import importlib.util
import io
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

_fails = [0]


def _ck(cond, label, extra=''):
    print('  [%s] %s%s' % ('PASS' if cond else 'FAIL', label, ('  ' + str(extra)) if extra else ''))
    if not cond:
        _fails[0] += 1


def _load(name, rel):
    p = os.path.join(REPO, rel)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _norm(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())


def run_all():
    RM = _load('_rm_fr', 'engine/rl_after/ingestion/round_movers.py')
    FR = _load('_fr', 'engine/rl_after/ingestion/finals_report.py')
    print('FINALS-REPORT WRITER TESTS\n  ' + '-' * 66)

    # ---- the column -> feed-round table, both directions and the negative case ------------------
    _ck(FR.feed_round_of('fw1-finals-week-1-30-8', RM) == 25, 'an fw1- column is feed round 25')
    _ck(FR.feed_round_of('fw2-finals-week-2-9-9', RM) == 26, 'an fw2- column is feed round 26')
    _ck(FR.feed_round_of('bust-exclusion-live-fit-1-9', RM) is None,
        'a NON-finals column is not a finals week — the writer must not fire on an ordinary act')

    # ---- scores are rebuilt from the edit list, never re-parsed from the file -------------------
    plan_p = os.path.join(REPO, 'docs', 'evidence', 'finals_fw1_2026-08-30', 'FW1_EDIT_PLAN.json')
    fw1_plan = json.load(io.open(plan_p, encoding='utf-8'))
    scored = FR.scores_from_edits(fw1_plan['edits'], 2026)
    _ck(len(scored) == 92, 'FW1: 92 scores rebuilt from the edit list', len(scored))

    # non-vacuity: a games field that does not move by one is refused
    bad = [dict(e) for e in fw1_plan['edits']]
    for e in bad:
        if e['field'] == 'scoring[2026].games':
            e['new'] = e['old'] + 2
            break
    try:
        FR.scores_from_edits(bad, 2026)
        _ck(False, 'a games field moving by TWO is refused')
    except ValueError as exc:
        _ck('exactly one' in str(exc), 'a games field moving by TWO is refused', str(exc)[:60])

    # ---- the scores agree with the owner's own file, resolved the way the plan resolved it ------
    store = json.load(io.open(os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json'),
                              encoding='utf-8'))
    by = collections.defaultdict(list)
    for p in store:
        by[_norm(p.get('player'))].append(p)
    csv_p = os.path.join(REPO, 'scores', 'FW1.csv')
    OVERRIDE = {'will hayes': 'will-hayes-b'}
    mismatched, listed = [], 0
    with io.open(csv_p, encoding='utf-8') as fh:
        for row in csv.reader(fh):
            if not row or not row[0].strip() or row[0].strip().lower() == 'player':
                continue
            listed += 1
            nm = row[0].strip()
            key = OVERRIDE.get(nm.lower())
            if not key:
                cands = [x for x in by[_norm(nm)] if not x.get('_retired')]
                key = cands[0]['key'] if len(cands) == 1 else None
            if key is None or scored.get(key) != int(float(row[1])):
                mismatched.append(nm)
    _ck(listed == 92 and not mismatched,
        'every score in scores/FW1.csv equals the score the STORE received', mismatched[:4])

    # ---- THE REBUILD: the writer reproduces the report a human wrote ----------------------------
    _head, bundle, _tail = FR._load_bundle(os.path.join(REPO, 'ui', 'data', 'movers.js'))
    shipped = (bundle.get('reports') or {}).get('25')
    if not shipped:
        _ck(False, 'the shipped bundle carries the FW1 report to rebuild against')
        return _fails[0]
    built = FR.build(REPO, bundle, 'fw1-finals-week-1-30-8', 25, fw1_plan['edits'], 2026,
                     shipped['source_store_md5_before'], shipped['source_store_md5_after'],
                     shipped['generated_at'])
    for k in ('submitted_round', 'previous_round', 'board_md5_before', 'board_md5_after',
              'player_count', 'txn_id', 'source_store_md5_before', 'source_store_md5_after'):
        _ck(built[k] == shipped[k], 'rebuilt %s == shipped' % k, built[k])
    _ck(built['views']['played_count'] == shipped['views']['played_count'] == 92
        and built['views']['dnp_count'] == shipped['views']['dnp_count'] == 712,
        'rebuilt played/DNP == shipped (92 / 712)')
    bs = {p['key']: p['score'] for p in built['players'] if p['played']}
    ss = {p['key']: p['score'] for p in shipped['players'] if p['played']}
    _ck(bs == ss, 'every one of the 92 rebuilt scores == the shipped score', len(bs))
    bv = {p['key']: (p['cur_value'], p['prev_value'], p['value_change']) for p in built['players']}
    sv = {p['key']: (p['cur_value'], p['prev_value'], p['value_change']) for p in shipped['players']}
    _ck(bv == sv, 'every player row carries the shipped values and delta', len(bv))

    # ---- the report names the FEED round while the calendar holds -------------------------------
    _ck(built['release_identity']['as_of_round'] == 25,
        'the report names the FEED round (25), not the calendar round')
    boot = json.load(io.open(os.path.join(REPO, 'data', 'expected_boot.json'), encoding='utf-8'))
    _ck(min(built['release_identity']['as_of_round'], RM.HOME_AND_AWAY_ROUNDS) == boot['as_of_round'],
        'and min(feed, 24) == the manifest\'s calendar round — the relation core.lineage asserts')

    print('  ' + '-' * 66)
    if _fails[0]:
        print('FINALS-REPORT TESTS: %d FAIL' % _fails[0])
    else:
        print('FINALS-REPORT TESTS: ALL PASS')
    return _fails[0]


if __name__ == '__main__':
    sys.exit(1 if run_all() else 0)
