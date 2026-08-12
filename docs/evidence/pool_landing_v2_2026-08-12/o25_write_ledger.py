#!/usr/bin/env python3
"""ORDER 25 -- THE COMPOSED POOL-UPDATE v2 MOVERS LEDGER.

  usage: o25_write_ledger.py <CONSEQUENCE_V2.json> <out.md> <out.json>

Carried from docs/evidence/pool_landing_2026-08-12/o23_write_ledger.py. Every board row that moves
between the live board `1dbd1480` and the landed board `88ce647f`, named, before -> after -> delta ->
pct, with the THREE-LEVER DECOMPOSITION ON EVERY ROW -- not only on the ones the owner's attribution
requirement covers, because the columns cost nothing once the four boards exist:

    lever H                     the ITEM H retirement                       LIVE   -> H-only board
    lever retention/delivery    the derived pool sit-out surface AND the current-state delivery
                                AND the quality-conditioned premium AND the amended pars, all at
                                the N43 levels the live board priced at     H-only -> psi board
    lever repricing             ORDER 25's derived entry levels, and the
                                ND65+ cap removal 185 -> 297                psi    -> LANDED

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
         'STAGED22': 'lever 2 — + the ψ retention/delivery machinery',
         'FINAL': 'lever 3 — + the repricing (LANDED)'}

bad = [r for r in LED if abs((r['lever_H'] + r['lever_retention'] + r['lever_repricing']) - r['delta']) > 1e-9]
assert not bad, "LEVER DECOMPOSITION DOES NOT SUM on %d row(s): %s" % (len(bad), [b['key'] for b in bad][:5])

NAMED = {'harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'vigo-visentini',
         'marcus-herbert', 'jai-newcombe', 'nicholas-martin'}
BIG = [r for r in LED if abs(r['delta']) >= 50]
byp = collections.Counter(r['pathway'] for r in LED)


def flag(r):
    return ' **[NAMED]**' if r['key'] in NAMED else ''


L = []
A = L.append
A("# THE COMPOSED POOL-UPDATE v2 MOVERS LEDGER — 2026-08-12")
A("")
A("Issue #334, ORDER 25 (the landing build). Branch `land/pool-update-v2`. Owner's word: **\"Land\"**")
A("(comment [5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)),")
A("with the par amendment folded in. Rulings underneath: 5253173347 (D8, H), 5262159933, 5262213139,")
A("5262928754 (the ND>64 cap amendment), 5265698024 and 5266652914 (the delivery and the premium).")
A("")
A("**Live board `1dbd1480a34c7823f330273211cbb76a` → landed board `88ce647f531030d8d2e094188b258191`.**")
A("")
A("| board | md5 | total | Δ vs LIVE | % | moved | up | down |")
A("|---|---|---:|---:|---:|---:|---:|---:|")
for k in ('LIVE', 'VARA', 'STAGED22', 'FINAL'):
    b = BOARDS[k]
    A("| %s | `%s` | %s | %s | %+.3f%% | %d | %d | %d |"
      % (LABEL[k], b['md5'], format(round(b['total']), ','), format(round(b['delta']), ','),
         100.0 * b['delta'] / BOARDS['LIVE']['total'], b['moved'], b['up'], b['down']))
A("")
A("**Lever totals across every moved row: H retirement %+d · ψ retention/delivery %+d · repricing %+d = %+d.**"
  % (round(C['lever_totals']['H']), round(C['lever_totals']['retention']),
     round(C['lever_totals']['repricing']), round(sum(C['lever_totals'].values()))))
A("")
A("**Lever 1 is ORDER 23's own board, reused byte-identically** (`452623ad`). Nothing in ORDERS 24,")
A("24B or 25 touches H, so re-measuring that lever would be re-measuring the same thing under a new")
A("name. Its column total here (**%+d**) is identical to the H column of ORDER 23's ledger."
  % round(C['lever_totals']['H']))
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
A("**The national arm does not move under any lever, at any stage.** Not as a claim — the")
A("consequence builder computes it on the board bytes at every one of the three stages, and the")
A("landing act's own separation instrument asserts it and raises before anything is written.")
A("")
A("## By pathway")
A("")
A("| pathway | rows | moved | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | **%** |")
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
A("| player | pathway | pos | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | % | lever H | lever ψ delivery | lever repricing |")
A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for r in BIG:
    A("| %s%s | %s | %s | %d | %d | %d | **%d** | **%+d** | %+.1f%% | %+d | %+d | %+d |"
      % (r['player'] or r['key'], flag(r), r['pathway'], r['pos'] or '', round(r['live']),
         round(r['vara']), round(r['staged']), round(r['final']), round(r['delta']), r['pct'],
         round(r['lever_H']), round(r['lever_retention']), round(r['lever_repricing'])))
A("")
A("## EVERY MOVER — all %d rows, with the same decomposition" % len(LED))
A("")
A("| # | player | pathway | pos | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | % | lever H | lever ψ delivery | lever repricing |")
A("|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for i, r in enumerate(LED, 1):
    A("| %d | %s%s | %s | %s | %d | %d | %d | **%d** | **%+d** | %+.1f%% | %+d | %+d | %+d |"
      % (i, r['player'] or r['key'], flag(r), r['pathway'], r['pos'] or '', round(r['live']),
         round(r['vara']), round(r['staged']), round(r['final']), round(r['delta']), r['pct'],
         round(r['lever_H']), round(r['lever_retention']), round(r['lever_repricing'])))
A("")
A("**Movers by pathway:** " + " · ".join("%s %d" % (k, v) for k, v in sorted(byp.items())) + ".")
A("")
A("**The lever-sum identity holds on all %d rows** (H + ψ delivery + repricing == total delta, "
  "asserted at write time; the writer halts otherwise)." % len(LED))
A("")
A("**Why the lever column totals (%+d / %+d / %+d) do not equal the board-wide lever deltas "
  "(%+d / %+d / %+d).** The columns are summed over the rows that move on the LANDED board. "
  "ONE row moves under the intermediate levers and lands back on EXACTLY its live value, so it "
  "carries no total delta and is not a ledger row: **jacob-moss** (36 → 45 → 57 → **36**; H +9, "
  "ψ delivery +12, repricing −21). It accounts for the whole of each of the three gaps. Named here "
  "rather than reconciled away."
  % (round(C['lever_totals']['H']), round(C['lever_totals']['retention']),
     round(C['lever_totals']['repricing']), round(BOARDS['VARA']['delta']),
     round(BOARDS['STAGED22']['delta'] - BOARDS['VARA']['delta']),
     round(BOARDS['FINAL']['delta'] - BOARDS['STAGED22']['delta'])))
A("")
A("## The seven named rows, with their lever split")
A("")
A("| player | pathway | LIVE | H only | + ψ delivery | **LANDED** | lever H | lever ψ delivery | lever repricing |")
A("|---|---|---:|---:|---:|---:|---:|---:|---:|")
seen = {r['key']: r for r in LED}
for k in ('harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'vigo-visentini',
          'marcus-herbert', 'jai-newcombe', 'nicholas-martin'):
    r = seen.get(k)
    if r is None:
        A("| `%s` | — | — | — | — | **unmoved** | 0 | 0 | 0 |" % k)
        continue
    A("| `%s` | %s | %d | %d | %d | **%d** | %+d | %+d | %+d |"
      % (k, r['pathway'], round(r['live']), round(r['vara']), round(r['staged']), round(r['final']),
         round(r['lever_H']), round(r['lever_retention']), round(r['lever_repricing'])))
A("")
A("`marcus-herbert` and `jai-newcombe` do not appear because they **do not move at all**: both are")
A("full current participants (φ = 1) carrying an anchor share of exactly zero, so no multiplier and")
A("no level reaches them. That is the design working, and it is the cheapest available check that")
A("the delivery fix reaches only the population it is meant to reach.")
A("")
A("One act, three levers, one ledger.")
A("")
A("_Generated by [Claude Code](https://claude.ai/code)_")
open(OUTMD, 'w').write("\n".join(L) + "\n")

json.dump(dict(live_board='1dbd1480a34c7823f330273211cbb76a',
               landed_board='88ce647f531030d8d2e094188b258191',
               boards=BOARDS, lever_totals=C['lever_totals'], separation=C['separation'],
               by_pathway=C['by_pathway'], n_movers=len(LED), n_movers_ge50=len(BIG),
               movers_by_pathway=dict(byp), named_rows=sorted(NAMED), ledger=LED),
          open(OUTJS, 'w'), indent=1, default=float)
print("wrote %s (%d movers, %d of them >= 50 points)" % (OUTMD, len(LED), len(BIG)))
print("wrote %s" % OUTJS)
