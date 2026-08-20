#!/usr/bin/env python3
"""ORDER D8 — the FIRST LIVE USE attempt of ui/templates/movers.html, reported honestly.

The order says: use the ui/templates skeletons IF the movers template fits; otherwise the v757
movers format. This script is the test of "fits". It fills every slot the D8 comparison can fill
HONESTLY, passes slots.ABSENT only where the manifest declares nullability, and records exactly
what slots.validate() says. Nothing is invented to make the validator pass — that is the whole
point of the template's own rule ("a missing value is a loud failure, it is never a dash").

  D8MOVERS  MOVERS_D8.json      D8EVID  evidence dir
"""
import os, sys, json, datetime

EVID = os.environ['D8EVID']
ROOT = os.path.abspath(os.environ['D8REPO'])
sys.path.insert(0, os.path.join(ROOT, 'ui', 'templates'))
import slots                                                                     # noqa: E402

mv = json.load(open(os.environ['D8MOVERS']))
L = []
P = lambda s='': (L.append(s), print(s))

P('=' * 110)
P('ORDER D8 — ui/templates/movers.html, FIRST LIVE USE. The fit test, and its verdict.')
P('=' * 110)
P()
man = json.load(open(os.path.join(ROOT, 'ui', 'templates', 'manifest.json')))['movers']
P('declared slots (%d): %s' % (len(man['slots']), ', '.join(man['slots'])))
P('declared nullable  : %s' % ', '.join(man['nullable']))
P()

# Every player slot the D8 comparison can fill honestly, and the ones it cannot.
players = []
for i, r in enumerate(mv['movers'], 1):
    players.append({
        'name': r['name'], 'pos': r['pos'], 'club': r['club'],
        'prev_value': r['before'], 'cur_value': r['after'],
        'value_change': '%+d' % r['delta'], 'value_change_pct': '%+.2f%%' % r['pct'],
        # rank fields ARE computable — rank on the base board vs rank on the priced board
        'prev_rank': r['_prev_rank'], 'cur_rank': r['_cur_rank'],
        'rank_change': '%+d' % (r['_prev_rank'] - r['_cur_rank']),
        'prev_pos_rank': r['_prev_pos_rank'], 'cur_pos_rank': r['_cur_pos_rank'],
        'pos_rank_change': '%+d' % (r['_prev_pos_rank'] - r['_cur_pos_rank']),
        'score': slots.ABSENT,          # declared nullable — there is no round score in a lever comparison
        # 'played' — deliberately NOT supplied. See the verdict below.
    })

data = {
    'page_title': 'THE MOVERS — ORDER D8, the ceiling-only leg',
    'subtitle': 'B-3 taper retirement priced alone; the B-1 tall ladder dead. PRICED, NOT ADOPTED.',
    'boundary_note': 'Both sides are round 22 on store cc02567f. The only difference is the dial.',
    'from_label': 'base a05fe951 (RL_O33_TAPEROFF unset)',
    'to_label': 'priced %s (RL_O33_TAPEROFF=1)' % mv['priced_board_md5'][:8],
    'board_md5_before': mv['base_board_md5'], 'board_md5': mv['priced_board_md5'],
    'store_md5_before': 'cc02567f80bef39228f25854d121a766',
    'store_md5': 'cc02567f80bef39228f25854d121a766',
    'engine_head': '338a790b773cfbbff0e1283794c72efe',
    'config': 'eed19a75f775', 'as_of_round': 22,
    'previous_round': 22,
    'generated_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'players': players,
}

probs = slots.validate('movers', data)
P('slots.validate("movers", <the honest D8 payload>) ->')
if not probs:
    P('   NO PROBLEMS — the template fits.')
else:
    seen = []
    for p in probs:
        s = str(p)
        key = s.split('row')[0] if 'row' in s else s
        if key not in seen:
            seen.append(key)
            P('   %s' % s)
    P('   (%d problems, %d distinct)' % (len(probs), len(seen)))
P()
P('THE VERDICT — three findings, in the order they bite:')
P()
P(' 1. THERE IS NO age SLOT. The template\'s row block is')
P('    name / pos / club / played / score / prev_value / cur_value / value_change /')
P('    value_change_pct / prev_rank / cur_rank / rank_change / prev_pos_rank / cur_pos_rank /')
P('    pos_rank_change. The owner\'s probation question is ABOUT AGE — "still boosting the younger')
P('    players" — and D8\'s order names age as a required column. A template that cannot carry the')
P('    deciding column does not fit, and the layout law forbids a seat adding one')
P('    ("a seat injects data; a seat never injects layout").')
P()
P(' 2. played IS MANDATORY AND HAS NO HONEST VALUE HERE. It is not in the nullable list, so it')
P('    must be filled. In the WEEKLY report it means "did he play this round". In a LEVER')
P('    comparison both sides are the same round on the same store, and whether a player played is')
P('    not a fact of the comparison at all. Filling it would be exactly the dash-that-says-nothing')
P('    the template exists to forbid, wearing a different costume. It is left unsupplied above and')
P('    the validator is allowed to say so.')
P()
P(' 3. previous_round / from_label / to_label ASSUME A ROUND BOUNDARY. Both D8 boards are round 22.')
P('    from_label/to_label are free text and were filled honestly; previous_round == as_of_round ==')
P('    22 renders as a round-to-round comparison that did not happen. Not fatal on its own, but it')
P('    is the same category error as (2): the schema is round-shaped, this comparison is dial-shaped.')
P()
P('WHAT DID FIT, and is worth recording for the migration: score IS correctly declared nullable and')
P('slots.ABSENT was accepted for it; the identity stamp carries BOTH ends of the comparison, which is')
P('exactly right for a lever diff and is the one part of this schema a dial-movers page should keep;')
P('and all six rank columns are computable and meaningful across a lever (rank on the base board vs')
P('rank on the priced board), so a future dial-movers template should keep them.')
P()
P('DELIVERED IN: the v757 / house movers format (MOVERS_D8.md), which carries age, carries the')
P('per-band attribution the order asks for, and does not have to pretend a round boundary exists.')
P()
P('RECOMMENDATION (not this seat\'s to land): the movers schema wants a sibling — a LEVER-MOVERS')
P('template whose row block is name / age / pos / club / before / after / delta / pct / the six rank')
P('columns, whose header is from_label -> to_label with no previous_round, and which keeps the')
P('both-ends stamp verbatim. That is a template addition, not a template edit, and it belongs to')
P('whoever owns ui/templates.')
open(os.path.join(EVID, 'TEMPLATE_TRY_out.txt'), 'w').write('\n'.join(L) + '\n')
