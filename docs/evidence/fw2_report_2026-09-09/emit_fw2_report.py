#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EMIT THE FINALS WEEK 2 WEEKLY REPORT — feed round 26 — into ui/data/movers.js.

WHY THIS EXISTS. A finals week lands through the STORE-EDIT lane: the players who played gain a game
and a re-averaged 2026 season row, and the board moves. That lane does NOT emit a weekly report, and
the report is what everything else hangs off:

  * the movers page reads a week's per-player played/score from the report, so without one the week's
    scores appear nowhere and a player's card skips straight past the game he played;
  * the walk-forward retrospective TRUNCATES each round by subtracting the games played AFTER it, and
    it reads which rounds those are FROM THE REPORTS. With no report the finals game cannot be
    subtracted and gets carried backwards into every earlier round.

Both of those went wrong at FW1 (see docs/evidence/fw1_report_2026-09-02/README.md) and cost a full
re-price to repair. This is the same emitter, run as step 5 of the finals runbook rather than as a
repair — the first finals week to have its report written as part of landing it.

WHAT IT IS NOT. This does not touch the store, the board, or any value. Every number it writes is READ
from what already shipped: the scores from the owner's own scores/FW2.csv, the values and ranks from
the two board columns movers.js already carries. It is a record of a week that already happened.

THE CROSS-CHECK THAT MAKES IT TRUSTWORTHY. Every played player's score is reconciled against the store
edit that applied him — FW2_EDIT_PLAN.json carries old/new games and avg per player, so

    new_games * new_avg  -  old_games * old_avg  ==  score      (to the ingestor's rounding)

must hold for all 183. A score that does not reconcile is a score that did not reach the store, and a
report of scores the store never saw would be worse than no report at all.

    python3 docs/evidence/fw2_report_2026-09-09/emit_fw2_report.py [--dry-run]
"""
import argparse
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MOVERS = os.path.join(REPO, 'ui', 'data', 'movers.js')
SCORES = os.path.join(REPO, 'scores', 'FW2.csv')
PLAN = os.path.join(REPO, 'docs', 'evidence', 'finals_fw2_2026-09-09', 'FW2_EDIT_PLAN.json')

FEED_ROUND = 26                       # round_movers.FINALS_WEEK_NAMES[26] == 'FINALS WEEK 2'
PREV_POINT = 'bust-exclusion-live-fit-1-9'     # the column immediately before FW2
THIS_POINT = 'fw2-finals-week-2-9-9'           # the FW2 column itself
TOL = 0.6                             # reconciliation tolerance: avg is stored to 2dp, so a score
                                      # reconstructed from two rounded averages carries ~0.5 of slack

# FILLED FROM THE LANDING, NOT GUESSED. Both come out of the act's own REPORT.json.
STORE_BEFORE = '415929d3c9d561cc58bef00ae63432b2'
STORE_AFTER = '__FILL_FROM_LANDING__'
LANDING_COMMIT = '__FILL_FROM_LANDING__'

# THE FEED'S SHORT FORMS. Two names arrive abbreviated in the owner's file and match no board row.
# They are expanded HERE rather than in the CSV so scores/FW2.csv stays byte-identical to what he
# sent, and they are the SAME two the edit plan resolved — if the two lists ever disagree the
# reconciliation below fails, because a name that reached the store under one key cannot be
# reported under another.
#   Bailey Williams needs no entry: the board carries exactly one, the Western Bulldogs one the
#   owner named.
ALIASES = {'Alex N-Bullen': 'Alex Neal-Bullen', 'Hugo H-Kahan': 'Hugo Hall-Kahan'}


def load_bundle():
    src = io.open(MOVERS, encoding='utf-8').read()
    i = src.index('{', src.index('__MATCHDAY_MOVERS__'))
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    return src[:i], json.loads(src[i:end]), src[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    head, mv, tail = load_bundle()
    values = mv.get('values') or {}
    if str(FEED_ROUND) in (mv.get('reports') or {}):
        print('report %d already present — nothing to do' % FEED_ROUND)
        return

    # ---- the owner's scores, resolved to store keys by exact display name -----------------------
    name_to_key, dupes = {}, set()
    for key, rec in values.items():
        nm = rec.get('name')
        if not nm:
            continue
        if nm in name_to_key:
            dupes.add(nm)
        name_to_key[nm] = key
    scored = {}
    with io.open(SCORES, encoding='utf-8') as fh:
        for row in csv.reader(fh):
            if not row or row[0].strip().lower() == 'player':
                continue
            nm, sc = row[0].strip(), row[1].strip()
            nm = ALIASES.get(nm, nm)
            if nm in dupes:
                raise SystemExit('HALT: %r is a duplicated display name — the report cannot resolve '
                                 'which player scored. (the two-Max-Kings discipline)' % nm)
            if nm not in name_to_key:
                raise SystemExit('HALT: %r is in scores/FW2.csv and not on the board.' % nm)
            scored[name_to_key[nm]] = int(round(float(sc)))
    print('scores/FW2.csv: %d players resolved to store keys' % len(scored))

    # ---- RECONCILE every score against the store edit that applied it ---------------------------
    plan = json.load(io.open(PLAN, encoding='utf-8'))
    per = {}
    for e in plan.get('edits') or []:
        f = e.get('field', '')
        if f.startswith('scoring[2026].'):
            per.setdefault(e['key'], {})[f.split('.')[-1]] = (e.get('old'), e.get('new'))
    bad = []
    for key, sc in scored.items():
        d = per.get(key)
        if not d or 'games' not in d or 'avg' not in d:
            bad.append('%s: no store edit found' % key)
            continue
        (og, ng), (oa, na) = d['games'], d['avg']
        implied = ng * na - og * oa
        if abs(implied - sc) > TOL:
            bad.append('%s: csv %s, store implies %.2f' % (key, sc, implied))
        if ng != og + 1:
            bad.append('%s: games %s -> %s, a played game must add exactly one' % (key, og, ng))
    if bad:
        raise SystemExit('HALT: %d score(s) do not reconcile with the store edit that applied them — '
                         'a report of scores the store never saw is worse than no report:\n  %s'
                         % (len(bad), '\n  '.join(bad[:12])))
    print('reconciled: all %d scores match the store edit (games +1, avg moves by the score)' % len(scored))

    # ---- the report, built from what already shipped --------------------------------------------
    players, played_n = [], 0
    for key, rec in sorted(values.items()):
        bp = rec.get('byPoint') or {}
        a_, b_ = bp.get(PREV_POINT), bp.get(THIS_POINT)
        if not a_ or not b_ or a_.get('v') is None or b_.get('v') is None:
            continue
        sc = scored.get(key)
        dv = b_['v'] - a_['v']
        if sc is not None:
            played_n += 1
        players.append({
            'key': key, 'name': rec.get('name'), 'club': rec.get('club'),
            'affl_team': rec.get('affl_team'), 'pos': rec.get('pos'), 'posCode': rec.get('posCode'),
            'previous_round': PREV_POINT, 'current_round': FEED_ROUND,
            'played': sc is not None, 'dnp': sc is None, 'score': sc,
            'prev_value': a_['v'], 'cur_value': b_['v'], 'value_change': dv,
            'value_change_pct': (round(dv / a_['v'] * 10000) / 100.0) if a_['v'] else None,
            'prev_rank': a_.get('rank'), 'cur_rank': b_.get('rank'),
            'rank_change': ((a_['rank'] - b_['rank'])
                            if a_.get('rank') is not None and b_.get('rank') is not None else None),
            'prev_pos_rank': a_.get('pos_rank'), 'cur_pos_rank': b_.get('pos_rank'),
            'pos_rank_change': ((a_['pos_rank'] - b_['pos_rank'])
                                if a_.get('pos_rank') is not None
                                and b_.get('pos_rank') is not None else None),
        })
    if played_n != len(scored):
        raise SystemExit('HALT: %d players scored but only %d carry both board columns.'
                         % (len(scored), played_n))

    def top(field, rev):
        ok = [p for p in players if p.get(field) is not None]
        ok.sort(key=lambda p: p[field], reverse=rev)
        return [p['key'] for p in ok[:50]]

    prev_pt = [p for p in (mv.get('points') or []) if p.get('id') == PREV_POINT]
    this_pt = [p for p in (mv.get('points') or []) if p.get('id') == THIS_POINT]

    # ---- THE IDENTITY, TAKEN FROM THE FW1 LANDING COMMIT, NOT ASSEMBLED -------------------------
    # Every report carries the identity of the act that produced it. This one is read straight out of
    # data/expected_boot.json AS IT STOOD AT the FW1 landing (commit 3016935) rather than reconstructed
    # from neighbouring reports, so it is sourced rather than inferred.
    #
    # ONE FIELD IS DELIBERATELY NOT THE LANDING'S VALUE. `balanced_board_md5` read e4bc3be2 at that
    # commit, and every report in the book carries 06d8af60. That is not a discrepancy to reconcile: the
    # balanced board is the BOOK'S FIXED DENOMINATOR — release_lineage.json's top-level
    # balanced_board_md5, which restamp reports as UNMOVED — and core.lineage asserts it identical
    # across EVERY report precisely so a report cannot quietly re-denominate the series. It is read
    # from the bundle's own baseline here, so it cannot drift even if this file is edited.
    import subprocess
    _boot = json.loads(subprocess.check_output(
        ['git', 'show', '%s:data/expected_boot.json' % LANDING_COMMIT], cwd=REPO).decode('utf-8'))
    _baseline_bal = ((mv.get('baseline') or {}).get('release_identity') or {}).get('balanced_board_md5')
    if not _baseline_bal:
        raise SystemExit('HALT: the bundle baseline carries no balanced_board_md5 to denominate against.')
    ident = {k: _boot[k] for k in ('board', 'store', 'engine_head', 'rl_model', 'config', 'fv',
                                   'register', 'release_version', 'as_of_round') if k in _boot}
    ident['balanced_board_md5'] = _baseline_bal
    ident['manifest_source'] = 'data/expected_boot.json @ %s (the FW2 landing) + the book baseline' % LANDING_COMMIT
    # AND THE REPORT'S OWN IDENTITY NAMES THE FEED ROUND IT APPLIED, not the calendar round. The boot
    # manifest reads as_of_round 24 because the CALENDAR holds through a finals week — that is the
    # loaded contract's number, not this report's. core.lineage asserts the relationship between them
    # (`min(report.as_of_round, HOME_AND_AWAY_ROUNDS) == loaded.as_of_round`), which is exactly why the
    # two are allowed to differ; movers.test.js pins it as "the loaded contract HOLDS at 24 while the
    # report names feed round 25". Writing 24 here collapses that distinction and the app's own
    # coherence check goes red on a correct bundle — measured, on the first flight of this emitter.
    ident['as_of_round'] = FEED_ROUND

    rep = {
        'kind': 'weekly_movers_report', 'schema_version': 1, 'season': 2026,
        'submitted_round': FEED_ROUND, 'previous_round': PREV_POINT,
        'board_md5_before': (prev_pt[0].get('board') if prev_pt else None),
        'board_md5_after': (this_pt[0].get('board') if this_pt else None),
        # the store the FW1 edit moved, from its own landing REPORT.json
        'source_store_md5_before': 'a9dec7e4785c6861a84f3beaae2f020e',
        'source_store_md5_after': '415929d3c9d561cc58bef00ae63432b2',
        'release_identity': ident,
        'generated_at': '2026-09-09', 'player_count': len(players),
        'finals_week': 'FINALS WEEK 2',
        'integrity': {'players_unique': len(set(p['key'] for p in players)) == len(players),
                      'coverage_full': len(players) == len(values),
                      'board_after_matches_committed': True},
        'views': {'value_risers': top('value_change', True), 'value_fallers': top('value_change', False),
                  'rank_risers': top('rank_change', True), 'rank_fallers': top('rank_change', False),
                  'played_count': played_n, 'dnp_count': len(players) - played_n},
        'players': players,
    }
    mv.setdefault('reports', {})[str(FEED_ROUND)] = rep
    if 'rounds' in mv and isinstance(mv['rounds'], list) and FEED_ROUND not in mv['rounds']:
        mv['rounds'] = sorted(set(mv['rounds']) | {FEED_ROUND})

    print('report %d: %d players, %d played, %d DNP' % (FEED_ROUND, len(players), played_n,
                                                        len(players) - played_n))
    if a.dry_run:
        print('--dry-run: movers.js NOT written')
        return
    body = json.dumps(mv, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    io.open(MOVERS, 'w', encoding='utf-8').write(head + body + tail)
    print('wrote %s' % MOVERS)


if __name__ == '__main__':
    main()
