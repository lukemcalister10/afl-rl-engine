#!/usr/bin/env python3
"""
CHANGE LEDGER  --  a plain "what moved" report between two board states.

Descriptive ONLY. This tool does not score, gate, abort, judge "better/worse",
or block anything. It takes a BEFORE board and an AFTER board and tells the
league manager, in names and dollars, exactly what shifted: which players moved,
by how much, where the movement clusters, who the biggest movers are, and which
columns the schema gained or lost. Nothing here decides whether a change should
ship -- that is a gate's job, and this is not a gate.

Usage:
    python tools/change_ledger.py <before.json> <after.json> [--top N]

Each board artifact is either the full app-data JSON (an object with an
"active" list) or a bare list of player rows. A player row carries a stable
"key", a "name", a position ("grp"), a draft cohort ("yr"), a "pick" ("pk"),
and the five SCAR value fields v / vM1 / vM2 / vP1 / vP2:

    vM2 vM1  v  vP1 vP2  =  ev(player) as of 2024 2025 2026 2027 2028.

`v` (the present-season price, in dollars) is the headline field; the report
covers all five.
"""
import sys, json, argparse
from collections import defaultdict

SCAR_FIELDS = ['v', 'vM1', 'vM2', 'vP1', 'vP2']
# Magnitude buckets, by a player's largest |%Δ| across the five SCAR fields.
# "0" is exact no-move; the rest are open-low/closed-high bands.
BUCKETS = ['0', '<2%', '2-5%', '5-10%', '>10%']


def load_board(path):
    """Return {key: row} from a board artifact (full app-data or bare list)."""
    with open(path) as fh:
        d = json.load(fh)
    rows = d['active'] if isinstance(d, dict) else d
    board = {}
    for r in rows:
        board[r['key']] = r
    return board, rows


def money(x):
    """League-manager dollars: $7,002 (or a dash for missing)."""
    if x is None:
        return '     --'
    return '${:,}'.format(int(round(x)))


def signed_money(x):
    if x is None:
        return '   --'
    return ('+' if x >= 0 else '-') + '${:,}'.format(int(round(abs(x))))


def pct_str(p):
    if p is None:
        return '  n/a'
    return '{:+.1f}%'.format(p)


def bucket_of(max_abs_pct, any_move):
    """Bucket a player by its largest |%Δ| across fields."""
    if not any_move:
        return '0'
    if max_abs_pct is None:          # moved but base was 0/None -> can't take a %
        return '>10%'
    if max_abs_pct < 2:
        return '<2%'
    if max_abs_pct < 5:
        return '2-5%'
    if max_abs_pct < 10:
        return '5-10%'
    return '>10%'


def field_delta(before, after):
    """(delta, pct) for one field; pct is None when the base is 0 or missing."""
    if before is None or after is None:
        if before == after:
            return 0.0, 0.0
        return None, None            # appeared/disappeared value -> undefined %
    d = after - before
    p = (d / before * 100.0) if before else None
    return d, p


def analyse(before, after):
    """Build the per-player movement record for the shared roster."""
    keys_b, keys_a = set(before), set(after)
    common = keys_b & keys_a
    dropped_players = sorted(keys_b - keys_a)   # in before, gone in after
    added_players = sorted(keys_a - keys_b)     # new in after

    movers = []
    for k in common:
        rb, ra = before[k], after[k]
        moved_fields = []            # (field, before, after, delta, pct)
        max_abs_pct = None
        max_abs_dollar = 0.0
        for f in SCAR_FIELDS:
            vb, va = rb.get(f), ra.get(f)
            if vb == va:
                continue
            d, p = field_delta(vb, va)
            moved_fields.append((f, vb, va, d, p))
            if p is not None:
                max_abs_pct = abs(p) if max_abs_pct is None else max(max_abs_pct, abs(p))
            if d is not None:
                max_abs_dollar = max(max_abs_dollar, abs(d))
        if not moved_fields:
            continue
        # headline per-player numbers key off `v` (present-season price)
        dv, pv = field_delta(rb.get('v'), ra.get('v'))
        movers.append({
            'key': k,
            'name': ra.get('name', rb.get('name', k)),
            'pos': ra.get('grp', rb.get('grp')),
            'cohort': ra.get('yr', rb.get('yr')),
            'pick': ra.get('pk', rb.get('pk')),
            'v_before': rb.get('v'), 'v_after': ra.get('v'),
            'v_delta': dv, 'v_pct': pv,
            'moved_fields': moved_fields,
            'max_abs_pct': max_abs_pct,
            'max_abs_dollar': max_abs_dollar,
            'bucket': bucket_of(max_abs_pct, True),
        })
    return {
        'M': len(common),
        'movers': movers,
        'added_players': added_players,
        'dropped_players': dropped_players,
    }


def column_diff(rows_b, rows_a):
    """Schema delta: which row columns the AFTER board added / dropped."""
    cb = set().union(*[set(r) for r in rows_b]) if rows_b else set()
    ca = set().union(*[set(r) for r in rows_a]) if rows_a else set()
    return sorted(ca - cb), sorted(cb - ca)   # added, dropped


# ---------------------------------------------------------------- reporting ---
def hr(ch='-', n=72):
    return ch * n


def report(before_path, after_path, res, added_cols, dropped_cols, top_n, out=sys.stdout):
    movers = res['movers']
    M = res['M']
    N = len(movers)
    p = lambda *a: print(*a, file=out)

    p(hr('='))
    p('CHANGE LEDGER   (descriptive -- what moved; not a score, not a gate)')
    p('  before : {}'.format(before_path))
    p('  after  : {}'.format(after_path))
    p(hr('='))

    col_note = ''
    if added_cols or dropped_cols:
        bits = []
        if added_cols:
            bits.append('{} added ({})'.format(len(added_cols), ', '.join(added_cols)))
        if dropped_cols:
            bits.append('{} dropped ({})'.format(len(dropped_cols), ', '.join(dropped_cols)))
        col_note = '; ' + '; '.join(bits) + '.'
    else:
        col_note = '; 0 columns added/dropped.'

    # ---- NO-OP: clean, zero-noise ----
    if N == 0 and not res['added_players'] and not res['dropped_players']:
        p('')
        p('HEADLINE: 0 of {} players moved -- nothing changed in v/vM1/vM2/vP1/vP2{}'.format(M, col_note))
        p('')
        p('No player value moved. This is a clean no-op on the board values.')
        if added_cols or dropped_cols:
            p('(Schema only: {}{})'.format(
                'columns added ' + ', '.join(added_cols) + ' ' if added_cols else '',
                'columns dropped ' + ', '.join(dropped_cols) if dropped_cols else '').strip())
        p(hr('='))
        return

    # ---- headline for a real change ----
    big = max(movers, key=lambda m: m['max_abs_dollar'])
    # which position group concentrates the movement (by mover count)
    by_pos_count = defaultdict(int)
    for m in movers:
        by_pos_count[m['pos']] += 1
    conc_pos, conc_n = max(by_pos_count.items(), key=lambda kv: kv[1])

    max_dollar = big['max_abs_dollar']
    # the % that goes with that biggest dollar move
    max_pct = None
    for f, vb, va, d, pc in big['moved_fields']:
        if d is not None and abs(d) == max_dollar:
            max_pct = pc
            break

    p('')
    p('HEADLINE: {} of {} players moved; max Δ = {} ({}) on {}; '
      'concentrated in {} ({} of {} movers){}'.format(
          N, M, money(max_dollar), pct_str(max_pct), big['name'],
          conc_pos, conc_n, N, col_note))

    roster = []
    if res['added_players']:
        roster.append('{} new player row(s)'.format(len(res['added_players'])))
    if res['dropped_players']:
        roster.append('{} player row(s) removed'.format(len(res['dropped_players'])))
    if roster:
        p('ROSTER: ' + '; '.join(roster) + '.')

    # ---- roll-up: by magnitude bucket ----
    p('')
    p(hr())
    p('ROLL-UP BY MAGNITUDE  (a player is bucketed by its largest |%Δ| across the 5 fields)')
    p(hr())
    p('  {:<8} {:>7}   {}'.format('bucket', 'players', 'net $ move on v (sum)'))
    bkt_players = defaultdict(int)
    bkt_dollar = defaultdict(float)
    non_movers = M - N
    bkt_players['0'] = non_movers
    for m in movers:
        bkt_players[m['bucket']] += 1
        if m['v_delta'] is not None:
            bkt_dollar[m['bucket']] += m['v_delta']
    for b in BUCKETS:
        p('  {:<8} {:>7}   {}'.format(b, bkt_players[b], signed_money(bkt_dollar[b]) if b != '0' else signed_money(0)))

    # ---- roll-up: by position ----
    p('')
    p(hr())
    p('ROLL-UP BY POSITION')
    p(hr())
    p('  {:<10} {:>7} {:>14} {:>14}'.format('position', 'movers', 'net $ (on v)', 'largest |Δ|'))
    pos_agg = defaultdict(lambda: {'n': 0, 'net': 0.0, 'max': 0.0})
    for m in movers:
        a = pos_agg[m['pos']]
        a['n'] += 1
        if m['v_delta'] is not None:
            a['net'] += m['v_delta']
        a['max'] = max(a['max'], m['max_abs_dollar'])
    for pos in sorted(pos_agg, key=lambda k: -pos_agg[k]['n']):
        a = pos_agg[pos]
        p('  {:<10} {:>7} {:>14} {:>14}'.format(
            str(pos), a['n'], signed_money(a['net']), money(a['max'])))

    # ---- roll-up: by draft cohort ----
    p('')
    p(hr())
    p('ROLL-UP BY DRAFT COHORT')
    p(hr())
    p('  {:<10} {:>7} {:>14} {:>14}'.format('cohort', 'movers', 'net $ (on v)', 'largest |Δ|'))
    coh_agg = defaultdict(lambda: {'n': 0, 'net': 0.0, 'max': 0.0})
    for m in movers:
        a = coh_agg[m['cohort']]
        a['n'] += 1
        if m['v_delta'] is not None:
            a['net'] += m['v_delta']
        a['max'] = max(a['max'], m['max_abs_dollar'])
    for coh in sorted(coh_agg, key=lambda k: (k is None, k)):
        a = coh_agg[coh]
        p('  {:<10} {:>7} {:>14} {:>14}'.format(
            str(coh), a['n'], signed_money(a['net']), money(a['max'])))

    # ---- top movers, both directions (headline field: v) ----
    def top_line(m):
        return '  {:<22} {:<9} {:>9} -> {:>9}   {}  ({})'.format(
            m['name'][:22], str(m['pos']),
            money(m['v_before']), money(m['v_after']),
            signed_money(m['v_delta']), pct_str(m['v_pct']))

    with_v = [m for m in movers if m['v_delta'] is not None and m['v_delta'] != 0]
    risers = sorted(with_v, key=lambda m: -m['v_delta'])[:top_n]
    fallers = sorted(with_v, key=lambda m: m['v_delta'])[:top_n]

    p('')
    p(hr())
    p('TOP {} RISERS  (present-season price v, before -> after)'.format(top_n))
    p(hr())
    if risers:
        for m in risers:
            p(top_line(m))
    else:
        p('  (none moved up on v)')

    p('')
    p(hr())
    p('TOP {} FALLERS  (present-season price v, before -> after)'.format(top_n))
    p(hr())
    if fallers:
        for m in fallers:
            p(top_line(m))
    else:
        p('  (none moved down on v)')

    # movers whose v held but a projection year (vM*/vP*) moved -- surfaced so
    # they are not silently invisible in a v-keyed top-movers view.
    proj_only = [m for m in movers if (m['v_delta'] in (0, None)) ]
    if proj_only:
        p('')
        p('NOTE: {} player(s) held on present-season v but moved on a projection '
          'year (vM2/vM1/vP1/vP2).'.format(len(proj_only)))

    p(hr('='))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Descriptive change ledger between two board states.')
    ap.add_argument('before', help='BEFORE board artifact (app-data JSON or bare list)')
    ap.add_argument('after', help='AFTER board artifact (app-data JSON or bare list)')
    ap.add_argument('--top', type=int, default=10, help='how many top movers to name each way (default 10)')
    args = ap.parse_args(argv)

    before, rows_b = load_board(args.before)
    after, rows_a = load_board(args.after)
    res = analyse(before, after)
    added_cols, dropped_cols = column_diff(rows_b, rows_a)
    report(args.before, args.after, res, added_cols, dropped_cols, args.top)


if __name__ == '__main__':
    main()
