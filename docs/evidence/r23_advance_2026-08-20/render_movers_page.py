#!/usr/bin/env python3
"""ACT 4 — THE MOVERS PAGE for R22 -> R23, rendered through ui/templates (the layout law).

A SEAT INJECTS DATA. A SEAT NEVER INJECTS LAYOUT. Every value below comes out of the movers report
of record (engine/rl_after/ingestion/movers/movers_R23.json), written inside the advance transaction
by round_finalize/round_movers. Nothing is recomputed here and no markup is authored here:
slots.render('movers', data) fills the frozen skeleton ui/templates/movers.html and REFUSES an
absent slot, a None, an empty string or any dash sentinel.

THE FIRST GENUINELY FITTING LIVE USE OF THIS TEMPLATE. The D8 pricing seat tried it and reported
honestly that it did not fit a LEVER comparison (docs/evidence/d8_ceiling_2026-08-20/d8_template_try.py:
no age column, `played` has no honest value across a dial, previous_round == as_of_round). Every one
of those three objections is about a dial-shaped comparison wearing a round-shaped schema. THIS is a
round boundary: `played` and `score` are facts of it, and previous_round != as_of_round.

`score` is the ONE declared-nullable slot and is passed as slots.ABSENT for the 393 players who did
not play. That is the honest use of the sentinel — "he has no score because he did not play" — and it
is exactly the distinction the slot contract exists to force a caller to state.

THE BASELINE IS B0, NOT R22. `previous_round` in the report reads `the-sheet-recut-20-8`, the
out-of-round column at the post-re-cut R22 board 1d5c9f7a. round_finalize chose it through
round_movers.previous_point (the stored point IMMEDIATELY BEFORE round 23), which is rule M0 working:
the baseline shares as_of_round 22 with the candidate, so the D8 adoption and the injury-sheet re-cut
both sit on the R22 side of the boundary and this page shows ONLY what round 23's scores did.
"""
import datetime, hashlib, json, os, sys

ROOT = '/home/user/afl-rl-engine'
sys.path.insert(0, os.path.join(ROOT, 'ui', 'templates'))
import slots                                                                     # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'evidence', 'r23_advance_2026-08-20', 'MOVERS_R23.html')
rep = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'ingestion', 'movers', 'movers_R23.json')))
boot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
vh = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'ingestion', 'value_history.json')))
col = {c['id']: c for c in vh['columns']}

# --- fences: the page must describe the tree it was built from -----------------------------------
assert rep['submitted_round'] == 23, rep['submitted_round']
assert rep['board_md5_after'] == boot['board'], 'report board != manifest board'
assert rep['source_store_md5_after'] == boot['store'], 'report store != manifest store'
assert rep['previous_round'] == 'the-sheet-recut-20-8', \
    'the R23 baseline is not B0 — it is %r' % rep['previous_round']
assert col['the-sheet-recut-20-8']['board'] == rep['board_md5_before'], 'baseline column board mismatch'
assert col['the-sheet-recut-20-8']['after_round'] == 22, 'rule M0: the baseline must sit at round 22'
assert rep['integrity']['coverage_full'] and rep['integrity']['players_unique']
assert rep['player_count'] == len(rep['players']) == 804

order = sorted(rep['players'], key=lambda p: (-p['value_change'], p['name']))
players = []
for p in order:
    players.append({
        'name': p['name'], 'pos': p['pos'], 'club': p['club'],
        'played': 'yes' if p['played'] else 'no',
        'score': ('%g' % p['score']) if p['played'] else slots.ABSENT,
        'prev_value': p['prev_value'], 'cur_value': p['cur_value'],
        'value_change': '%+d' % p['value_change'],
        'value_change_pct': '%+.1f%%' % p['value_change_pct'],
        'prev_rank': p['prev_rank'], 'cur_rank': p['cur_rank'],
        'rank_change': '%+d' % p['rank_change'],
        'prev_pos_rank': p['prev_pos_rank'], 'cur_pos_rank': p['cur_pos_rank'],
        'pos_rank_change': '%+d' % p['pos_rank_change'],
    })

up = sum(1 for p in rep['players'] if p['value_change'] > 0)
dn = sum(1 for p in rep['players'] if p['value_change'] < 0)
tb = sum(p['prev_value'] for p in rep['players'])
ta = sum(p['cur_value'] for p in rep['players'])

data = {
    'page_title': 'THE MOVERS — round 23, 2026',
    'subtitle': ('%d players · %d played, %d did not · %d moved (%d up, %d down) · '
                 'board total %s -> %s (%+d)'
                 % (len(players), rep['views']['played_count'], rep['views']['dnp_count'],
                    up + dn, up, dn, format(tb, ','), format(ta, ','), ta - tb)),
    'boundary_note': (
        'BASELINE IS THE POST-RE-CUT ROUND-22 BOARD, NOT THE ROUND-22 REPORT. The point compared FROM '
        'is the out-of-round column `the-sheet-recut-20-8` (board 1d5c9f7a, as_of_round 22) — chosen by '
        'round_movers.previous_point, which takes the stored point IMMEDIATELY BEFORE round 23. Two '
        'board moves sit between the round-22 report and this round: THE D8 ADOPTION (a05fe951 -> '
        '5ea978f7, owner word "Yes. I\'m adopting.") and THE INJURY-SHEET RE-CUT (5ea978f7 -> 1d5c9f7a, '
        'owner word "All good on the injury sheet. Fine by me."). Both are on the ROUND-22 side of this '
        'boundary and neither appears in the numbers below, which is rule M0: a diff baseline must share '
        'as_of_round with the candidate. EVERY DELTA ON THIS PAGE IS WHAT ROUND 23\'S SCORES DID.'),
    'from_label': 'post-re-cut R22 board 1d5c9f7a (the-sheet-recut-20-8)',
    'to_label': 'R23 board %s' % rep['board_md5_after'][:8],
    'board_md5_before': rep['board_md5_before'], 'board_md5': rep['board_md5_after'],
    'store_md5_before': rep['source_store_md5_before'], 'store_md5': rep['source_store_md5_after'],
    'engine_head': rep['release_identity']['engine_head'],
    'config': rep['release_identity']['config'][:12],
    'as_of_round': rep['submitted_round'],
    'previous_round': rep['previous_round'],
    'generated_at': rep['generated_at'],
    'players': players,
}

probs = slots.validate('movers', data)
print('slots.validate("movers", <the R23 weekly payload>) -> %s'
      % ('NO PROBLEMS — the template fits.' if not probs else probs[:5]))
if probs:
    raise SystemExit('HALT: the movers payload does not satisfy the slot contract: %d problems' % len(probs))

html = slots.render('movers', data)
open(OUT, 'w', encoding='utf-8').write(html)
print('wrote %s  (%d bytes, %d rows)' % (OUT, len(html.encode()), len(players)))
print('  md5 %s' % hashlib.md5(open(OUT, 'rb').read()).hexdigest())
print('  from board %s store %s  (point %s, round %s)'
      % (data['board_md5_before'], data['store_md5_before'], data['previous_round'],
         col['the-sheet-recut-20-8']['after_round']))
print('  to   board %s store %s  (round %s)' % (data['board_md5'], data['store_md5'], data['as_of_round']))
