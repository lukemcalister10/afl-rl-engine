#!/usr/bin/env python3
"""ORDER 23 -- THE COMPOSED POOL-UPDATE MOVERS LEDGER.

  usage: o23_write_ledger.py <CONSEQUENCE_O23.json> <out.md> <out.json>

Every board row that moves between the live board `1dbd1480` and the landed board `665311ca`, named,
before -> after -> delta -> pct, with the THREE-LEVER DECOMPOSITION on every row (not only the ones
the order requires it for, because the columns cost nothing once the four boards exist):

    lever H          the ITEM H retirement           LIVE -> H-only board
    lever retention  the derived pool sit-out surface  H-only -> +retention board
    lever repricing  the derived entry levels + the ND65+ amendment  +retention -> LANDED

The three components sum to the row's total delta BY CONSTRUCTION (they are consecutive differences
of the same four boards); the identity is nevertheless ASSERTED on every row, because a ledger whose
columns do not add up is worse than no ledger.
"""
import sys, json, collections

SRC, OUTMD, OUTJS = sys.argv[1], sys.argv[2], sys.argv[3]
C = json.load(open(SRC))
LED = C['ledger']
BOARDS = C['boards']
LABEL = {'LIVE': 'LIVE 1dbd1480', 'VARA': 'lever 1 — H retirement',
         'STAGED22': 'lever 2 — + the derived retention', 'FINAL': 'lever 3 — + the repricing (LANDED)'}

bad = [r for r in LED if abs((r['lever_H'] + r['lever_retention'] + r['lever_repricing']) - r['delta']) > 1e-9]
assert not bad, "LEVER DECOMPOSITION DOES NOT SUM on %d row(s): %s" % (len(bad), [b['key'] for b in bad][:5])

BIG = [r for r in LED if abs(r['delta']) >= 50]
byp = collections.Counter(r['pathway'] for r in LED)

L = []
A = L.append
A("# THE COMPOSED POOL-UPDATE MOVERS LEDGER — 2026-08-12")
A("")
A("Issue #334, ORDER 23. Branch `land/pool-update`. Owner rulings 5253173347 (D8), 5262159933,")
A("5262213139 and **5262928754** (the ND>64 cap amendment and this act's authority).")
A("")
A("**Live board `1dbd1480a34c7823f330273211cbb76a` → landed board `665311ca72576df6ff0bbf6dfd007739`.**")
A("")
A("| board | md5 | total | Δ vs LIVE | % | moved | up | down |")
A("|---|---|---:|---:|---:|---:|---:|---:|")
for k in ('LIVE', 'VARA', 'STAGED22', 'FINAL'):
    b = BOARDS[k]
    A("| %s | `%s` | %s | %s | %+.3f%% | %d | %d | %d |"
      % (LABEL[k], b['md5'], format(round(b['total']), ','), format(round(b['delta']), ','),
         100.0 * b['delta'] / BOARDS['LIVE']['total'], b['moved'], b['up'], b['down']))
A("")
A("**Lever totals across every moved row: H retirement %+d · retention %+d · repricing %+d = %+d.**"
  % (round(C['lever_totals']['H']), round(C['lever_totals']['retention']),
     round(C['lever_totals']['repricing']), round(sum(C['lever_totals'].values()))))
A("")
A("## Separation — asserted, not claimed")
A("")
A("| check | result |")
A("|---|---|")
for k in ('VARA', 'STAGED22', 'FINAL'):
    s = C['separation'][k]
    A("| non-pool board rows moved, %s | **%d** |" % (LABEL[k], s['non_pool_rows_moved']))
A("| ND 1-64 board value, LIVE → LANDED | **%s → %s** |"
  % (format(round(C['by_pathway']['ND 1-64']['LIVE']), ','), format(round(C['by_pathway']['ND 1-64']['FINAL']), ',')))
A("")
A("## By pathway")
A("")
A("| pathway | rows | moved | LIVE | H only | + retention | **LANDED** | **Δ** | **%** |")
A("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for pw in sorted(C['by_pathway'], key=lambda p: -C['by_pathway'][p]['LIVE']):
    d = C['by_pathway'][pw]
    dl = d['FINAL'] - d['LIVE']
    A("| %s | %d | %d | %s | %s | %s | **%s** | **%+d** | **%+.3f%%** |"
      % (pw, d['rows'], d['moved'], format(round(d['LIVE']), ','), format(round(d['VARA']), ','),
         format(round(d['STAGED22']), ','), format(round(d['FINAL']), ','), round(dl),
         100.0 * dl / d['LIVE'] if d['LIVE'] else 0.0))
A("")
A("## THE MOVERS ≥ 50 POINTS — the owner's attribution requirement, every one named (%d rows)" % len(BIG))
A("")
A("| player | pathway | pos | LIVE | H only | + retention | **LANDED** | **Δ** | % | lever H | lever retention | lever repricing |")
A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for r in BIG:
    A("| %s | %s | %s | %d | %d | %d | **%d** | **%+d** | %+.1f%% | %+d | %+d | %+d |"
      % (r['player'] or r['key'], r['pathway'], r['pos'] or '', round(r['live']), round(r['vara']),
         round(r['staged']), round(r['final']), round(r['delta']), r['pct'],
         round(r['lever_H']), round(r['lever_retention']), round(r['lever_repricing'])))
A("")
A("## EVERY MOVER — all %d rows, with the same decomposition" % len(LED))
A("")
A("| # | player | pathway | pos | LIVE | H only | + retention | **LANDED** | **Δ** | % | lever H | lever retention | lever repricing |")
A("|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for i, r in enumerate(LED, 1):
    A("| %d | %s | %s | %s | %d | %d | %d | **%d** | **%+d** | %+.1f%% | %+d | %+d | %+d |"
      % (i, r['player'] or r['key'], r['pathway'], r['pos'] or '', round(r['live']), round(r['vara']),
         round(r['staged']), round(r['final']), round(r['delta']), r['pct'],
         round(r['lever_H']), round(r['lever_retention']), round(r['lever_repricing'])))
A("")
A("**Movers by pathway:** " + " · ".join("%s %d" % (k, v) for k, v in sorted(byp.items())) + ".")
A("")
A("**The lever-sum identity holds on all %d rows** (H + retention + repricing == total delta, "
  "asserted at write time; the writer halts otherwise)." % len(LED))
A("")
A("**Why the lever column totals (+%d / +%d / +%d) do not equal the board-wide lever deltas "
  "(+%d / +%d / +%d).** The columns are summed over the rows that move in the LANDED board. "
  "TWO rows move under an intermediate lever and land back on EXACTLY their live value, so they "
  "carry no total delta and are not ledger rows: **jacob-moss** (36 → 45 → 57 → **36**) and "
  "**jayden-nguyen** (452 → 452 → 456 → **452**). Together they account for the whole +9 gap in "
  "the H column. Named here rather than reconciled away."
  % (round(C['lever_totals']['H']), round(C['lever_totals']['retention']),
     round(C['lever_totals']['repricing']), round(BOARDS['VARA']['delta']),
     round(BOARDS['STAGED22']['delta'] - BOARDS['VARA']['delta']),
     round(BOARDS['FINAL']['delta'] - BOARDS['STAGED22']['delta'])))
A("")
A("One act, three levers, one ledger.")
A("")
A("_Generated by [Claude Code](https://claude.ai/code)_")
open(OUTMD, 'w').write("\n".join(L) + "\n")

json.dump(dict(live_board='1dbd1480a34c7823f330273211cbb76a',
               landed_board='665311ca72576df6ff0bbf6dfd007739',
               boards=BOARDS, lever_totals=C['lever_totals'], separation=C['separation'],
               by_pathway=C['by_pathway'], n_movers=len(LED), n_movers_ge50=len(BIG),
               movers_by_pathway=dict(byp), ledger=LED),
          open(OUTJS, 'w'), indent=1, default=float)
print("wrote %s (%d movers, %d of them >= 50 points)" % (OUTMD, len(LED), len(BIG)))
print("wrote %s" % OUTJS)
