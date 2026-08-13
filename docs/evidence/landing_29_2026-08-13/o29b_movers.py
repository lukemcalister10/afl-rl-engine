#!/usr/bin/env python3
"""ORDER 29B -- THE FULL MOVERS LEDGER: THE ENTRY-WIRING LEVER, AND THE COMPOSED FIVE-LEVER VIEW.

TWO LEDGERS OVER THE SAME 804 ROWS, and both must reconcile to the unit:

  (1) THE ENTRY-WIRING LEVER      86c8d5d9 -> 36d5dfc7, this act alone.
  (2) THE COMPOSED FIVE-LEVER VIEW  live 88ce647f -> 36d5dfc7, decomposed as
          lever 1 unflag-three | lever 2 grace dial | lever 3 curve + v0 | lever 4 numeraire
          | lever 5 ENTRY WIRING
      Levers 1-4 are read VERBATIM from ORDER 29's committed ledger (they are not re-derived here,
      because re-deriving a delivered decomposition is how two ledgers start disagreeing). Lever 5 is
      measured here. The reconciliation asserted per row is
          live + L1 + L2 + L3 + L4 + L5 == final        residual 0 on every row, or this halts.

Every row is carried, mover or not. The mover CLASS is measured, not assumed: each moved row is
classified as an ND in-curve entrant, a pool entrant, or -- if any appears -- an UNEXPLAINED mover,
which is reported by name rather than absorbed.

  usage: python3 o29b_movers.py <entry_board.json> <final_board.json>
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENTRY = sys.argv[1] if len(sys.argv) > 1 else None
FINAL = sys.argv[2] if len(sys.argv) > 2 else ROOT + '/engine/rl_after/rl_app_data.json'
L29 = json.load(open(ROOT + '/docs/ledgers/LANDING_29_MOVERS_2026-08-13.json'))
ART = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
POSV = ART['nd_v0']['posv']; CELLS = ART['pool_v0']['cells']
SIGN = ART['pool_v0'].get('cell_signature') or {}

LOG = []
def P(s=''):
    print(s); LOG.append(s)

def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

fin = {r['key']: r for r in json.load(open(FINAL))['active']}
ent = {r['key']: r for r in json.load(open(ENTRY))['active']} if ENTRY else None
L29ROW = {r['key']: r for r in L29['rows']}

# The ORDER 29 ledger's `final` column IS the ORDER 29 board (86c8d5d9). Use it as the entry basis so
# the two ledgers cannot disagree about what the entry board was; cross-check against the real file.
if ent is not None:
    _bad = [k for k in L29ROW if L29ROW[k]['final'] != ent[k]['v']]
    assert not _bad, ('ORDER 29B HALT: ORDER 29 ledger `final` disagrees with the entry board on %d row(s) '
                      '(%s) — the two ledgers would not compose.' % (len(_bad), _bad[:6]))

def cell_of(r):
    ty = r.get('ty')
    path = 'RD' if ty == 'RD' else ('ND>64' if ty == 'ND' else ty)
    return '%s|%s' % (path, r['gf'])

def klass(r):
    """The mover class, MEASURED from the row rather than assumed."""
    if (r.get('cg') or 0) != 0: return 'UNEXPLAINED (has career games)'
    if r.get('ty') == 'ND' and r.get('pk') and 1 <= int(r['pk']) <= 64: return 'ND in-curve entrant'
    return 'pool entrant'

P("=" * 122)
P("ORDER 29B  --  THE MOVERS LEDGER: THE ENTRY-WIRING LEVER AND THE COMPOSED FIVE-LEVER VIEW")
P("=" * 122)
P()
P("  entry board (ORDER 29 FINAL)  %s" % (md5f(ENTRY) if ENTRY else '(from ledger)'))
P("  final board (ORDER 29B)       %s" % md5f(FINAL))
P("  live  board (ORDER 29 ledger) %s" % L29['stages']['LIVE'])

rows = []
for k, r in fin.items():
    l = L29ROW[k]
    entry_v = l['final']
    l5 = r['v'] - entry_v
    rows.append(dict(key=k, name=r.get('name'), pos=r.get('gf'), ty=r.get('ty'), pick=r.get('pk'),
                     cg=(r.get('cg') or 0),
                     cell=(cell_of(r) if (r.get('cg') or 0) == 0 and not (
                         r.get('ty') == 'ND' and r.get('pk') and 1 <= int(r['pk']) <= 64) else None),
                     live=l['live'], entry=entry_v, final=r['v'],
                     lever1_unflag=l['lever1_unflag'], lever2_grace=l['lever2_grace'],
                     lever3_curve_v0=l['lever3_curve_v0'], lever4_numeraire=l['lever4_numeraire'],
                     lever5_entry_wiring=l5,
                     entry_lever_delta=l5, composed_total=r['v'] - l['live'],
                     mover_class=(klass(r) if l5 else None),
                     residual=(l['live'] + l['lever1_unflag'] + l['lever2_grace'] + l['lever3_curve_v0']
                               + l['lever4_numeraire'] + l5) - r['v']))
rows.sort(key=lambda x: (-abs(x['lever5_entry_wiring']), x['key']))

mv = [r for r in rows if r['lever5_entry_wiring']]
unexp = [r for r in mv if r['mover_class'].startswith('UNEXPLAINED')]
byclass = collections.Counter(r['mover_class'] for r in mv)
maxres = max(abs(r['residual']) for r in rows)
nfail = sum(1 for r in rows if r['residual'])

P()
P("  LEVER 5 -- THE ENTRY WIRING, vs %s" % L29['stages']['FINAL'][:8])
P("     rows            %d" % len(rows))
P("     movers          %d" % len(mv))
for c, n in sorted(byclass.items()):
    P("        %-34s %d" % (c, n))
P("     sum delta       %+d   (entry %d -> final %d)"
  % (sum(r['lever5_entry_wiring'] for r in rows),
     sum(r['entry'] for r in rows), sum(r['final'] for r in rows)))
P("     UNEXPLAINED     %s" % ([r['key'] for r in unexp] or 'NONE'))
assert not unexp, ('ORDER 29B HALT: %d mover(s) carry career games and are not day-0 entrants — %s. '
                   'STOP AND REPORT, do not absorb.' % (len(unexp), [r['key'] for r in unexp][:6]))

P()
P("  THE COMPOSED FIVE-LEVER VIEW, live %s -> final %s" % (L29['stages']['LIVE'][:8], md5f(FINAL)[:8]))
LEV = [('lever1_unflag', 'lever 1 — THE UNFLAG-THREE'),
       ('lever2_grace', 'lever 2 — THE GRACE DIAL'),
       ('lever3_curve_v0', 'lever 3 — THE CURVE + v0 REPRINT'),
       ('lever4_numeraire', 'lever 4 — THE NUMERAIRE SCALAR'),
       ('lever5_entry_wiring', 'lever 5 — THE ENTRY WIRING')]
P("     %-38s %8s %12s" % ('lever', 'movers', 'sum delta'))
tot = 0
for f, nm in LEV:
    n = sum(1 for r in rows if r[f]); s = sum(r[f] for r in rows); tot += s
    P("     %-38s %8d %+12d" % (nm, n, s))
P("     %-38s %8d %+12d" % ('TOTAL (composed)', sum(1 for r in rows if r['composed_total']), tot))
P("     %-38s %8s %+12d" % ('MEASURED live -> final', '', sum(r['final'] for r in rows) - sum(r['live'] for r in rows)))
assert tot == sum(r['final'] for r in rows) - sum(r['live'] for r in rows), 'lever sums do not add to the total'

P()
P("  RECONCILIATION, EVERY ROW: live + L1 + L2 + L3 + L4 + L5 == final")
P("     rows failing    %d" % nfail)
P("     max |residual|  %d" % maxres)
assert nfail == 0 and maxres == 0, 'ORDER 29B HALT: the five-lever decomposition does not reconcile'

P()
P("  BOARD TOTALS")
P("     LIVE   %s  %d" % (L29['stages']['LIVE'][:8], sum(r['live'] for r in rows)))
P("     ENTRY  %s  %d" % (L29['stages']['FINAL'][:8], sum(r['entry'] for r in rows)))
P("     FINAL  %s  %d   (%+d vs entry, %+.4f%% ; %+d vs live, %+.4f%%)"
  % (md5f(FINAL)[:8], sum(r['final'] for r in rows),
     sum(r['final'] for r in rows) - sum(r['entry'] for r in rows),
     100.0 * (sum(r['final'] for r in rows) - sum(r['entry'] for r in rows)) / sum(r['entry'] for r in rows),
     sum(r['final'] for r in rows) - sum(r['live'] for r in rows),
     100.0 * (sum(r['final'] for r in rows) - sum(r['live'] for r in rows)) / sum(r['live'] for r in rows)))

P()
P("  THE TEN ORDER-29 NAMED ROWS + kalani-white, on the entry-wiring lever (P29B-9)")
NAMED = ['harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'dante-visentini',
         'vigo-visentini', 'nicholas-martin', 'marcus-herbert', 'jai-newcombe', 'willem-duursma',
         'harry-sheezel', 'kalani-white']
byk = {r['key']: r for r in rows}
P("     %-20s %8s %8s %8s %10s" % ('row', 'live', 'entry', 'final', 'L5'))
for k in NAMED:
    r = byk[k]
    P("     %-20s %8d %8d %8d %+10d" % (k, r['live'], r['entry'], r['final'], r['lever5_entry_wiring']))

P()
P("  THE LARGEST TWENTY MOVES ON THE ENTRY-WIRING LEVER")
P("     %-28s %-6s %-5s %6s %8s %8s %8s" % ('row', 'ty', 'pos', 'pick', 'entry', 'final', 'L5'))
for r in mv[:20]:
    P("     %-28s %-6s %-5s %6s %8d %8d %+8d"
      % (r['key'], r['ty'], r['pos'], (r['pick'] if r['pick'] else '-'), r['entry'], r['final'],
         r['lever5_entry_wiring']))

open(HERE + '/MOVERS29B_out.txt', 'w').write("\n".join(LOG) + "\n")

# ---------------------------------------------------------------- the committed ledger
led = collections.OrderedDict([
    ('_doc', 'ORDER 29B — every one of the 804 active rows, twice over: the ENTRY-WIRING lever vs the '
             'ORDER 29 board 86c8d5d9, and the composed FIVE-LEVER view vs live 88ce647f. Levers 1-4 are '
             'read verbatim from LANDING_29_MOVERS_2026-08-13.json; lever 5 is measured here. Both sums '
             'reconcile exactly (0 rows failing, max |residual| 0).'),
    ('stages', collections.OrderedDict([('LIVE', L29['stages']['LIVE']),
                                        ('B_U', L29['stages']['B_U']), ('B_G', L29['stages']['B_G']),
                                        ('L3', L29['stages']['L3']),
                                        ('ENTRY_ORDER29_FINAL', L29['stages']['FINAL']),
                                        ('FINAL_ORDER29B', md5f(FINAL))])),
    ('levers', [collections.OrderedDict([
        ('name', nm), ('field', f),
        ('movers', sum(1 for r in rows if r[f])),
        ('sum_delta', sum(r[f] for r in rows))]) for f, nm in LEV]),
    ('lever5_doc', 'the printed day-0 price of an entrant becomes his derived v0 x numeraire: '
                   'nd_v0.posv[position][pick] for a national in-curve entrant, '
                   'pool_v0.cells[pathway|position] for a pool entrant (PDN|KPF and PDS|KPF signed as '
                   'BORROWED under owner OPTION A). Rows with any career games are untouched.'),
    ('totals', collections.OrderedDict([('LIVE', sum(r['live'] for r in rows)),
                                        ('ENTRY', sum(r['entry'] for r in rows)),
                                        ('FINAL', sum(r['final'] for r in rows))])),
    ('movers_entry_lever', len(mv)),
    ('movers_by_class', dict(byclass)),
    ('rows_total', len(rows)),
    ('reconciliation', {'rows_failing': nfail, 'max_abs_residual': maxres}),
    ('rows', rows),
])
json.dump(led, open(ROOT + '/docs/ledgers/LANDING_29B_MOVERS_2026-08-13.json', 'w'), indent=1)

M = []
M.append('# LANDING 29B — THE MOVERS LEDGER')
M.append('')
M.append('**Every one of the %d active rows, twice over.** The **entry-wiring lever** against ORDER 29\'s '
         'board `%s`, and the **composed five-lever view** against live `%s`. Levers 1–4 are read '
         'verbatim from ORDER 29\'s committed ledger — a delivered decomposition is not re-derived here — '
         'and lever 5 is measured. Both reconcile exactly.'
         % (len(rows), L29['stages']['FINAL'][:8], L29['stages']['LIVE'][:8]))
M.append('')
M.append('| stage | board md5 | total |')
M.append('|---|---|---:|')
M.append('| LIVE | `%s` | %s |' % (L29['stages']['LIVE'], format(sum(r['live'] for r in rows), ',')))
M.append('| ENTRY (ORDER 29 final) | `%s` | %s |' % (L29['stages']['FINAL'], format(sum(r['entry'] for r in rows), ',')))
M.append('| **FINAL (ORDER 29B)** | **`%s`** | **%s** |' % (md5f(FINAL), format(sum(r['final'] for r in rows), ',')))
M.append('')
M.append('| lever | movers | Σ delta |')
M.append('|---|---:|---:|')
for f, nm in LEV:
    M.append('| %s | %d | %+d |' % (nm, sum(1 for r in rows if r[f]), sum(r[f] for r in rows)))
M.append('| **total** | **%d** | **%+d** — the five sums add to the live→final total **exactly** |'
         % (sum(1 for r in rows if r['composed_total']), tot))
M.append('')
M.append('**Reconciliation, every row:** `live + L1 + L2 + L3 + L4 + L5 == final` — **%d rows failing, '
         'max |residual| %d**.' % (nfail, maxres))
M.append('')
M.append('## The entry-wiring lever, by mover class (measured, not assumed)')
M.append('')
M.append('| class | movers |')
M.append('|---|---:|')
for c, n in sorted(byclass.items()):
    M.append('| %s | %d |' % (c, n))
M.append('| **rows with career games** | **0 — asserted, not hoped** |')
M.append('')
M.append('## The ten ORDER-29 named rows, plus `kalani-white`')
M.append('')
M.append('| row | live | entry | final | entry-wiring lever |')
M.append('|---|---:|---:|---:|---:|')
for k in NAMED:
    r = byk[k]
    M.append('| `%s` | %d | %d | %d | %+d |' % (k, r['live'], r['entry'], r['final'], r['lever5_entry_wiring']))
M.append('')
M.append('## Every mover on the entry-wiring lever (%d rows)' % len(mv))
M.append('')
M.append('| row | type | pos | pick | cell | entry | final | Δ | class |')
M.append('|---|---|---|---:|---|---:|---:|---:|---|')
for r in mv:
    M.append('| `%s` | %s | %s | %s | %s | %d | %d | %+d | %s |'
             % (r['key'], r['ty'], r['pos'], (r['pick'] if r['pick'] else '—'),
                ('`%s`' % r['cell'].replace('|', '&#124;') +
                 (' **(BORROWED)**' if SIGN.get(r['cell']) == 'borrowed' else '')) if r['cell'] else '—',
                r['entry'], r['final'], r['lever5_entry_wiring'], r['mover_class']))
M.append('')
M.append('## Every row, composed (live → final)')
M.append('')
M.append('| row | pos | live | L1 unflag | L2 grace | L3 curve+v0 | L4 numéraire | L5 entry-wiring | final | Δ vs live |')
M.append('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in sorted(rows, key=lambda x: x['key']):
    M.append('| `%s` | %s | %d | %+d | %+d | %+d | %+d | %+d | %d | %+d |'
             % (r['key'], r['pos'], r['live'], r['lever1_unflag'], r['lever2_grace'],
                r['lever3_curve_v0'], r['lever4_numeraire'], r['lever5_entry_wiring'],
                r['final'], r['composed_total']))
M.append('')
open(ROOT + '/docs/ledgers/LANDING_29B_MOVERS_2026-08-13.md', 'w').write("\n".join(M) + "\n")
P()
P("  wrote docs/ledgers/LANDING_29B_MOVERS_2026-08-13.{md,json}")
open(HERE + '/MOVERS29B_out.txt', 'w').write("\n".join(LOG) + "\n")
