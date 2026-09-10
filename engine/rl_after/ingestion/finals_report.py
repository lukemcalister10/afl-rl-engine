#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""THE FINALS WEEK'S WEEKLY REPORT — written BY THE LANDING, not by somebody remembering afterwards.

A finals week lands as a STORE EDIT, and that lane does not produce a weekly report. The report is
what everything downstream hangs off: the movers page reads a week's per-player played/score from
it, and the walk-forward retrospective decides which games to subtract by reading which rounds have
reports. FW1 landed without one and both broke — the week's scores appeared nowhere, and the finals
game was carried backwards into every earlier round until it was found days later and cost a full
re-price to repair.

The guard added after that (movers.test.js: "a finals week that moved the board must have a weekly
report") then made the problem visible in a new way: it derives its expectation from the landed
finals COLUMNS, so the moment a finals column lands the bundle owes a report for it — and during the
landing that creates the week, no such report can exist yet. The guard is right; the ordering was
wrong. A report that has to be written by hand after the act is a report that can be forgotten, and
was.

SO THE ACT WRITES IT. This module is called by the landing's UI step, between the bundle rebuild and
the gates, so the bundle the gates inspect already carries the week.

WHERE EVERY NUMBER COMES FROM — all of it sourced, none of it restated:

  * the SCORES come from the act's own edit list, not from re-parsing the CSV. `scoring[2026].games`
    and `scoring[2026].avg` carry old and new, so the score that reached the store is
    `new_games*new_avg - old_games*old_avg` exactly. Reading the CSV again would re-introduce the
    name-resolution problem the plan already solved, and would report what the file said rather than
    what the store received — which is the thing a reader needs.
  * the VALUES and RANKS come from the two board columns the bundle already carries.
  * the IDENTITY comes from `data/expected_boot.json` in the tree being landed, with `as_of_round`
    set to the FEED round: the calendar HOLDS at 24 through the finals, so the manifest's 24 and the
    report's 25/26 are both right and `core.lineage` asserts the relationship between them.
  * `balanced_board_md5` comes from the bundle's own baseline — the book's fixed denominator, which
    every report must share and which a report must never re-denominate.

EVERY SCORE IS RECONCILED before anything is written: games must move by exactly +1, and the implied
score must be a whole number within the ingestor's rounding slack. A report of scores the store
never saw would be worse than no report at all.
"""
import hashlib
import io
import json
import os

ROUND_SLACK = 0.6      # avg is stored to 2dp; a score rebuilt from two rounded averages carries ~0.5


def _load_bundle(path):
    src = io.open(path, encoding='utf-8').read()
    i = src.index('{', src.index('__MATCHDAY_MOVERS__'))
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return src[:i], json.loads(src[i:j + 1]), src[j + 1:]
    raise ValueError('unterminated bundle object in %s' % path)


def feed_round_of(column_id, round_movers):
    """The feed round a finals COLUMN belongs to, via round_movers' own two tables. None if the
    column is not a finals week — which is the normal case and not an error."""
    name = None
    for prefix, week in (round_movers.FINALS_COLUMN_PREFIXES or {}).items():
        if str(column_id).startswith(prefix):
            name = week
            break
    if name is None:
        return None
    for feed, week in (round_movers.FINALS_WEEK_NAMES or {}).items():
        if week == name:
            return int(feed)
    raise ValueError('column %r names finals week %r, which round_movers.FINALS_WEEK_NAMES does not '
                     'carry — the two tables disagree.' % (column_id, name))


def scores_from_edits(edits, season):
    """{key: score} rebuilt from the act's own edit list, with the arithmetic asserted rather than
    trusted. Raises on any player whose games did not move by exactly one or whose implied score is
    not a whole number — either means the edit list is not what it claims to be."""
    per = {}
    gk, ak = 'scoring[%d].games' % season, 'scoring[%d].avg' % season
    for e in edits or ():
        if e.get('field') in (gk, ak):
            per.setdefault(e['key'], {})[e['field']] = (e.get('old'), e.get('new'))
    out, bad = {}, []
    for key, f in per.items():
        if gk not in f or ak not in f:
            bad.append('%s: carries %s but not both games and avg' % (key, sorted(f)))
            continue
        (og, ng), (oa, na) = f[gk], f[ak]
        if ng != og + 1:
            bad.append('%s: games %s -> %s; a played game adds exactly one' % (key, og, ng))
            continue
        implied = ng * na - og * oa
        if abs(implied - round(implied)) > ROUND_SLACK:
            bad.append('%s: implied score %.3f is not a whole number' % (key, implied))
            continue
        out[key] = int(round(implied))
    if bad:
        raise ValueError('%d player(s) do not reconcile with the edit that applied them:\n  %s'
                         % (len(bad), '\n  '.join(bad[:12])))
    return out


def build(repo_root, bundle, column_id, feed_round, edits, season,
          store_before, store_after, generated_at):
    """The report object. Pure: reads the bundle and the tree, writes nothing."""
    points = bundle.get('points') or []
    ids = [p.get('id') for p in points]
    if column_id not in ids:
        raise ValueError('the finals column %r is not on the bundle — the UI step rebuilds points '
                         'from the value-history columns, so a missing column means the act did not '
                         'reach that writer.' % column_id)
    this_i = ids.index(column_id)
    if this_i == 0:
        raise ValueError('the finals column %r is the first point on the bundle; there is nothing '
                         'to compare it against.' % column_id)
    prev_id = ids[this_i - 1]
    this_pt, prev_pt = points[this_i], points[this_i - 1]

    scored = scores_from_edits(edits, season)
    values = bundle.get('values') or {}
    players, played_n = [], 0
    for key, rec in sorted(values.items()):
        bp = rec.get('byPoint') or {}
        a_, b_ = bp.get(prev_id), bp.get(column_id)
        if not a_ or not b_ or a_.get('v') is None or b_.get('v') is None:
            continue
        sc = scored.get(key)
        dv = b_['v'] - a_['v']
        if sc is not None:
            played_n += 1
        players.append({
            'key': key, 'name': rec.get('name'), 'club': rec.get('club'),
            'affl_team': rec.get('affl_team'), 'pos': rec.get('pos'), 'posCode': rec.get('posCode'),
            'previous_round': prev_id, 'current_round': feed_round,
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
        raise ValueError('%d players were edited but only %d carry both board columns — the report '
                         'would silently lose %d of them.'
                         % (len(scored), played_n, len(scored) - played_n))

    def top(field, rev):
        rows = [p for p in players if p.get(field) is not None]
        rows.sort(key=lambda p: p[field], reverse=rev)
        return [p['key'] for p in rows[:50]]

    boot = json.load(io.open(os.path.join(repo_root, 'data', 'expected_boot.json'), encoding='utf-8'))
    baseline_bal = ((bundle.get('baseline') or {}).get('release_identity') or {}).get('balanced_board_md5')
    if not baseline_bal:
        raise ValueError('the bundle baseline carries no balanced_board_md5 to denominate against.')
    ident = {k: boot[k] for k in ('board', 'store', 'engine_head', 'rl_model', 'config', 'fv',
                                  'register', 'release_version') if k in boot}
    ident['balanced_board_md5'] = baseline_bal
    ident['manifest_source'] = 'data/expected_boot.json (the landing tree) + the book baseline'
    # THE REPORT NAMES THE FEED ROUND IT APPLIED, not the calendar round. The manifest reads 24
    # because the CALENDAR holds through a finals week; core.lineage asserts
    # min(report.as_of_round, HOME_AND_AWAY_ROUNDS) == loaded.as_of_round, which is exactly why the
    # two are allowed to differ.
    ident['as_of_round'] = feed_round

    return {
        'kind': 'weekly_movers_report', 'schema_version': 1, 'season': season,
        'submitted_round': feed_round, 'previous_round': prev_id,
        # WITHOUT A txn_id THE SAME-ROUND OVERWRITE GUARD IS OFF: round_movers identifies a report by
        # (txn_id, board_after, store_after, round) and treats an incomplete identity as "not a
        # conflict", because a repair must be able to rebuild a corrupt report. FW1's report shipped
        # without one and a second copy of that week could have overwritten it in silence. A finals
        # week has no round transaction to borrow an id from, so it takes its own column id.
        'txn_id': 'txn_' + str(column_id).replace('-', '_'),
        'board_md5_before': prev_pt.get('board'),
        'board_md5_after': this_pt.get('board'),
        'source_store_md5_before': store_before,
        'source_store_md5_after': store_after,
        'release_identity': ident,
        'generated_at': generated_at, 'player_count': len(players),
        'finals_week': None,   # filled by emit(), which holds the round_movers tables
        'integrity': {'players_unique': len(set(p['key'] for p in players)) == len(players),
                      'coverage_full': len(players) == len(values),
                      'board_after_matches_committed': True},
        'views': {'value_risers': top('value_change', True),
                  'value_fallers': top('value_change', False),
                  'rank_risers': top('rank_change', True),
                  'rank_fallers': top('rank_change', False),
                  'played_count': played_n, 'dnp_count': len(players) - played_n},
        'players': players,
    }


def emit(repo_root, column_id, edits, season, store_before, generated_at, round_movers,
         bundle_path=None, dry_run=False):
    """Write the finals week's report into ui/data/movers.js. Returns a summary dict, or None when
    `column_id` is not a finals column (the ordinary case for a non-finals act)."""
    feed = feed_round_of(column_id, round_movers)
    if feed is None:
        return None
    path = bundle_path or os.path.join(repo_root, 'ui', 'data', 'movers.js')
    head, bundle, tail = _load_bundle(path)
    if str(feed) in (bundle.get('reports') or {}):
        return {'feed_round': feed, 'already_present': True}

    store_after = hashlib.md5(
        io.open(os.path.join(repo_root, 'engine', 'rl_after', 'rl_model_data.json'), 'rb').read()
    ).hexdigest()
    rep = build(repo_root, bundle, column_id, feed, edits, season,
                store_before, store_after, generated_at)
    rep['finals_week'] = round_movers.FINALS_WEEK_NAMES[feed]

    bundle.setdefault('reports', {})[str(feed)] = rep
    if isinstance(bundle.get('rounds'), list) and feed not in bundle['rounds']:
        bundle['rounds'] = sorted(set(bundle['rounds']) | {feed})
    if not dry_run:
        body = json.dumps(bundle, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        io.open(path, 'w', encoding='utf-8').write(head + body + tail)
    return {'feed_round': feed, 'week': rep['finals_week'], 'already_present': False,
            'player_count': rep['player_count'], 'played': rep['views']['played_count'],
            'dnp': rep['views']['dnp_count'], 'store_after': store_after}
