#!/usr/bin/env python3
"""THE ONE COMPARISON — the round 21 board next to the round 22 board.

Owner's rule (issue #334, comment 5235125560): "the only comparison I want is to be able to see the
before/after of round 21 and round 22... just need an apples for apples round 21 to round 22 rankings
comparison to see who's changed."

Same system, same basis, one store step apart:
  BEFORE = the board of record after round 21 (rl_app_data.json at 113b36f8)
  AFTER  = the board of record after round 22 (rl_app_data.json rebuilt by the round-22 apply)

No historical re-computation. No re-derivation. No other analysis. Both sides are the same engine,
the same curve, the same surface, the same numeraire — the ONLY thing that moved between them is the
round-22 scores landing in the store.

Reads two board files, writes the mover table + the readable summary. Writes nothing else.

usage: compare_r21_r22.py <board_before.json> <board_after.json> <rank_history.json> <outdir>
"""
import csv
import json
import os
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def board_rows(b):
    rows = {}
    for p in b['active']:
        rows[p['key']] = {'name': p['name'], 'v': p['v'], 'afl_club': p.get('club'),   # the board's `club` IS the real AFL club (== store afl_club), not the AFFL ownership team
                          'pos': p.get('grp'), 'age': p.get('age')}
    return rows


def ranks_of_record(rank_history_path, round_n):
    """The board's OWN published overall rank for that round, straight out of the weekly rank
    history the apply writes. Not recomputed here — both sides come from the same producer, which
    is what makes the two columns apples for apples."""
    rh = json.load(open(rank_history_path))
    key = str(round_n)
    out = {k: int(v['by_round'][key]) for k, v in rh['players'].items() if key in v['by_round']}
    if len(out) != len(rh['players']):
        raise SystemExit('rank history is missing round %s for %d player(s)'
                         % (round_n, len(rh['players']) - len(out)))
    return out


def main(argv):
    if len(argv) != 5:
        sys.stderr.write(__doc__)
        return 2
    before_p, after_p, rankhist_p, outdir = argv[1], argv[2], argv[3], argv[4]
    B, A = load(before_p), load(after_p)
    rb, ra = board_rows(B), board_rows(A)

    only_before = sorted(set(rb) - set(ra))
    only_after = sorted(set(ra) - set(rb))
    shared = sorted(set(rb) & set(ra))

    kb, ka = ranks_of_record(rankhist_p, 21), ranks_of_record(rankhist_p, 22)

    table = []
    for k in shared:
        vb, va = rb[k]['v'], ra[k]['v']
        table.append({
            'key': k,
            'player': ra[k]['name'],
            'afl_club': ra[k]['afl_club'],
            'pos': ra[k]['pos'],
            'rank_r21': kb[k],
            'rank_r22': ka[k],
            'rank_change': kb[k] - ka[k],          # positive = climbed the board
            'value_r21': vb,
            'value_r22': va,
            'delta': va - vb,
            'pct': round(100.0 * (va - vb) / vb, 3) if vb else None,
        })

    # FULL BOARD, sorted by absolute move (largest value move first), name as the stable tiebreak.
    table.sort(key=lambda r: (-abs(r['delta']), r['player']))

    os.makedirs(outdir, exist_ok=True)
    cols = ['player', 'afl_club', 'pos', 'rank_r21', 'rank_r22', 'rank_change',
            'value_r21', 'value_r22', 'delta', 'pct', 'key']
    csv_path = os.path.join(outdir, 'board_R21_vs_R22.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in table:
            w.writerow({c: r[c] for c in cols})

    movers = [r for r in table if r['delta'] != 0]
    ups = [r for r in movers if r['delta'] > 0]
    downs = [r for r in movers if r['delta'] < 0]
    risers = sorted(movers, key=lambda r: -r['delta'])[:20]
    fallers = sorted(movers, key=lambda r: r['delta'])[:20]
    rank_up = sorted([r for r in table if r['rank_change'] > 0],
                     key=lambda r: (-r['rank_change'], -r['delta']))[:20]
    rank_dn = sorted([r for r in table if r['rank_change'] < 0],
                     key=lambda r: (r['rank_change'], r['delta']))[:20]

    summary = {
        'kind': 'r21_vs_r22_board_comparison',
        'basis': 'same engine, same curve, same surface, same numeraire (pick 1 = 3000); the only '
                 'change between the two sides is the round-22 scores landing in the store',
        'rank_source': 'engine/rl_after/ingestion/rank_history.json — the board\'s own published '
                       'overall rank for round 21 and for round 22, not recomputed here',
        'board_before': 'after round 21',
        'board_after': 'after round 22',
        'players_both_sides': len(shared),
        'only_on_r21_board': only_before,
        'only_on_r22_board': only_after,
        'movers': len(movers),
        'unmoved': len(table) - len(movers),
        'up': len(ups), 'down': len(downs),
        'board_total_r21': sum(r['value_r21'] for r in table),
        'board_total_r22': sum(r['value_r22'] for r in table),
        'net_delta': sum(r['delta'] for r in table),
        'gross_delta': sum(abs(r['delta']) for r in table),
        'largest_rise': risers[0] if risers else None,
        'largest_fall': fallers[0] if fallers else None,
        'top20_risers': risers,
        'top20_fallers': fallers,
        'top20_rank_climbers': rank_up,
        'top20_rank_sliders': rank_dn,
    }
    json.dump(summary, open(os.path.join(outdir, 'R21_vs_R22_summary.json'), 'w'),
              indent=1, sort_keys=True)

    def block(title, rows, key):
        out = ['### %s' % title, '',
               '| # | Player | AFL club | Rank R21 | Rank R22 | Rank move | Value R21 | Value R22 | Change |',
               '|---:|---|---|---:|---:|---:|---:|---:|---:|']
        for i, r in enumerate(rows, 1):
            out.append('| %d | %s | %s | %d | %d | %+d | %d | %d | %+d (%+.2f%%) |'
                       % (i, r['player'], r['afl_club'] or '', r['rank_r21'], r['rank_r22'],
                          r['rank_change'], r['value_r21'], r['value_r22'], r['delta'],
                          r['pct'] if r['pct'] is not None else 0.0))
        out.append('')
        return '\n'.join(out)

    md = []
    md.append('# Round 21 board vs round 22 board')
    md.append('')
    md.append('Same system, same basis. The two boards are one store step apart: the round-22 scores')
    md.append('landed, and nothing else changed. No earlier board was re-computed. This is the whole')
    md.append('comparison, and it is the only one here.')
    md.append('')
    md.append('- Players on both boards: **%d**' % len(shared))
    md.append('- Players whose value moved: **%d** (up %d, down %d, unchanged %d)'
              % (len(movers), len(ups), len(downs), len(table) - len(movers)))
    md.append('- Board total: **%s** after round 21, **%s** after round 22 (net **%+d**, %+.2f%%)'
              % ('{:,}'.format(summary['board_total_r21']), '{:,}'.format(summary['board_total_r22']),
                 summary['net_delta'],
                 100.0 * summary['net_delta'] / summary['board_total_r21']))
    md.append('- Gross movement (every change added up, ignoring direction): **%s**'
              % '{:,}'.format(summary['gross_delta']))
    if only_before or only_after:
        md.append('- On the round-21 board only: %s' % (', '.join(only_before) or 'none'))
        md.append('- On the round-22 board only: %s' % (', '.join(only_after) or 'none'))
    else:
        md.append('- Same 804 players on both sides. Nobody entered or left.')
    md.append('')
    md.append('The full board, every player, sorted by the size of the move, is in '
              '`board_R21_vs_R22.csv` alongside this file.')
    md.append('')
    md.append(block('Top 20 risers (by value)', risers, 'delta'))
    md.append(block('Top 20 fallers (by value)', fallers, 'delta'))
    md.append(block('Top 20 biggest climbs up the rankings', rank_up, 'rank_change'))
    md.append(block('Top 20 biggest slides down the rankings', rank_dn, 'rank_change'))
    open(os.path.join(outdir, 'R21_vs_R22.md'), 'w').write('\n'.join(md) + '\n')

    print('players both sides %d · movers %d (up %d, down %d) · net %+d · gross %d'
          % (len(shared), len(movers), len(ups), len(downs),
             summary['net_delta'], summary['gross_delta']))
    print('board total %d -> %d' % (summary['board_total_r21'], summary['board_total_r22']))
    if risers:
        print('largest rise : %-24s %d -> %d  (%+d)  rank %d -> %d'
              % (risers[0]['player'], risers[0]['value_r21'], risers[0]['value_r22'],
                 risers[0]['delta'], risers[0]['rank_r21'], risers[0]['rank_r22']))
    if fallers:
        print('largest fall : %-24s %d -> %d  (%+d)  rank %d -> %d'
              % (fallers[0]['player'], fallers[0]['value_r21'], fallers[0]['value_r22'],
                 fallers[0]['delta'], fallers[0]['rank_r21'], fallers[0]['rank_r22']))
    print('wrote %s' % csv_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
