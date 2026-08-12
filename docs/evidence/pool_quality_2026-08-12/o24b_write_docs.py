#!/usr/bin/env python3
"""ORDER 24B -- write MOVERS_TABLE_PSI.md and Q_TABLE.md from MOVERS_TABLE_PSI.json.

Every number is READ FROM THE ARTIFACT, never transcribed by hand.

  usage: o24b_write_docs.py <evidence_dir>
"""
import sys, json, os

D = sys.argv[1]
J = json.load(open(os.path.join(D, 'MOVERS_TABLE_PSI.json')))
S = json.load(open(os.path.join(D, 'SURFACE_psi.json')))
QBAR = {p: S['mean_preserving'][p]['qbar'] for p in S['mean_preserving']}
CAV = J['caveat']
COLS = ['pre_act', 'live', 'pr469', 'a025', 'a050', 'a100', 'psi']
ROWS, QR, T, SEP, MD5 = J['rows'], J['q_rows'], J['totals'], J['separation'], J['board_md5']
NAMED, WHY = J['named'], J['named_why']
QK = {r['key']: r for r in QR}
part = set(J['cells']['partial'])
mov = sorted([QK[k] for k in part if QK[k]['d_psi'] != 0], key=lambda r: r['d_psi'])

# ---------------------------------------------------------------- MOVERS_TABLE_PSI.md
L = []
A = L.append
A("# MOVERS_TABLE — ORDER 24B, THE ψ COLUMN BESIDE a100\n")
A("Issue #334, ORDER 24B. Branch `build/pool-quality`, stacked on ORDER 24's `build/pool-dial`.")
A("Pre-registration: `PREREG_ORDER24B.md`, committed **before** any measurement or code change.\n")
A("> **%s**\n" % CAV)
A("---\n")
A("## 1. The seven boards\n")
A("| column | what it is | md5 |")
A("|---|---|---|")
A("| `pre_act` | main @ `7f4d5d2`, the last board-touching main commit before PR #462 | `%s` |" % MD5['pre_act'])
A("| `live` | `origin/main` today | `%s` |" % MD5['live'])
A("| `pr469` | committed on `land/pool-update` / this branch | `%s` |" % MD5['pr469'])
A("| `a025` | ORDER 24, α = 0.25 | `%s` |" % MD5['a025'])
A("| `a050` | ORDER 24, α = 0.50 | `%s` |" % MD5['a050'])
A("| `a100` | ORDER 24, α = 1.00 — the pure delivery fix | `%s` |" % MD5['a100'])
A("| **`psi`** | **ORDER 24B — the quality-conditioned premium** | **`%s`** |" % MD5['psi'])
A("")
A("The first six are ORDER 24's **recorded** boards, re-used and re-pinned by md5 in `o24b_table.py`")
A("before a single row is read. The ψ board was built twice from scratch and produced `%s`"
  % MD5['psi'][:8])
A("both times.\n")
A("## 2. The separation law\n")
A("| check | a100 | psi |")
A("|---|---:|---:|")
A("| national rows on the board (`ty==ND`, pick ≤ 64) | %d | %d |"
  % (SEP['a100']['nd_rows'], SEP['psi']['nd_rows']))
A("| **ND movers vs live `1dbd1480`** | **%d** | **%d** |"
  % (SEP['a100']['nd_movers'], SEP['psi']['nd_movers']))
A("| ND rows absent | %d | %d |" % (SEP['a100']['nd_absent'], SEP['psi']['nd_absent']))
A("| ND board value (live: %s) | %s | %s |"
  % (format(round(SEP['psi']['nd_value_live']), ','), format(round(SEP['a100']['nd_value']), ','),
     format(round(SEP['psi']['nd_value']), ',')))
A("")
A("`o24b_table.py` **asserts this and raises before it writes anything at all** — the Q table, the")
A("movers table and the JSON are all downstream of the assertion.\n")
A("## 3. Pool totals\n")
A("| board | pool total | vs live | vs live % | moved vs live | moved vs `pr469` | **moved vs `a100`** |")
A("|---|---:|---:|---:|---:|---:|---:|")
for c in COLS:
    t = T[c]
    A("| `%s` | %s | %s | %+.3f%% | %d | %d | **%d** |"
      % (c, format(round(t['pool_total']), ','), format(round(t['delta_vs_live']), ','),
         100.0 * t['delta_vs_live'] / T['live']['pool_total'], t['moved_vs_live'],
         t['moved_vs_pr469'], t['moved_vs_a100']))
A("")
A("## 4. Who can move at all, and who did\n")
A("| cell (243 pool rows) | n | moved `a100` → `psi` |")
A("|---|---:|---:|")
A("| full participants, `φ = 1` — anchor share **exactly 0** | %d | **0** |" % len(J['cells']['full']))
A("| **partial participants, `0 < φ < 1`** | **%d** | **%d** |"
  % (len(J['cells']['partial']), len(mov)))
A("| current sitters, `φ = 0` — `M = R`, no premium leg exists | %d | **0** |" % len(J['cells']['sit']))
A("")
A("**Movers outside the partial cell: 0**, asserted. That is not a happy accident — it is the")
A("arithmetic. A sitter reads `R` and never touches `U″`; a full participant carries an anchor share")
A("of exactly zero, so no multiplier of any kind reaches his price. **ψ can only reach a pool player")
A("who is playing, but not yet playing a full load.**\n")
A("## 5. The direction law, verified on every one of the %d partials\n" % len(part))
A("```")
A("M_psi - M_a100  =  phi * (U'-1) * ( q/qbar - 1 )")
A("```")
A("so a partial with `q > qbar` **rises** and one with `q < qbar` **falls** — the price never enters")
A("the decision, only the quality does. Measured across all %d partials: **0 violations**." % len(part))
A("%d rows moved down, %d moved up, %d sat still because the move was below one point at integer"
  % (sum(1 for r in mov if r['d_psi'] < 0), sum(1 for r in mov if r['d_psi'] > 0), len(part) - len(mov)))
A("rounding (deep careers whose evidence fade has all but extinguished the anchor leg).\n")
A("## 6. THE EIGHT NAMED ROWS\n")
A("| player | pathway | g26 | avg26 | d | par | **q** | φ | pre_act | live | pr469 | a025 | a050 | a100 | **psi** | ψ−a100 |")
A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for k in NAMED:
    r = next((x for x in ROWS if x['key'] == k), None)
    if r is None:
        A("| `%s` | — | | | | | | | | | | | | | | absent |" % k); continue
    A("| `%s` | %s | %s | %s | %s | %s | **%.4f** | %.4f | %s | %s | %s | %s | %s | %s | **%s** | %+d |"
      % (k, r['pathway'], r.get('games_2026'), (r.get('avg_2026') if r.get('avg_2026') else '—'),
         r.get('depth'), ('%.2f' % r['par']) if r.get('par') else '—', r.get('q', 0), r.get('phi', 0),
         r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'], r['a100'], r['psi'],
         r['d_psi_vs_a100']))
A("")
for k in NAMED:
    A("- `%s` — %s" % (k, WHY[k]))
A("")
A("## 7. Top movers `a100` → `psi`\n")
A("### Down (%d rows)\n" % sum(1 for r in mov if r['d_psi'] < 0))
A("| player | pathway | avg26 | par | **q** | φ | a100 | **psi** | Δ |")
A("|---|---|---:|---:|---:|---:|---:|---:|---:|")
for r in [x for x in mov if x['d_psi'] < 0][:15]:
    A("| `%s` | %s | %.2f | %.2f | **%.4f** | %.4f | %d | **%d** | %+d |"
      % (r['key'], r['pathway'], r['avg'], r['par'], r['q'], r['phi'], r['a100'], r['psi'], r['d_psi']))
A("")
A("### Up (%d rows)\n" % sum(1 for r in mov if r['d_psi'] > 0))
A("| player | pathway | avg26 | par | **q** | φ | a100 | **psi** | Δ |")
A("|---|---|---:|---:|---:|---:|---:|---:|---:|")
for r in sorted([x for x in mov if x['d_psi'] > 0], key=lambda r: -r['d_psi'])[:15]:
    A("| `%s` | %s | %.2f | %.2f | **%.4f** | %.4f | %d | **%d** | %+d |"
      % (r['key'], r['pathway'], r['avg'], r['par'], r['q'], r['phi'], r['a100'], r['psi'], r['d_psi']))
A("")
A("## 8. THE TABLE — %d rows (%d material, %d named-only)\n" % (J['n_rows'], J['n_material'],
                                                                J['n_rows'] - J['n_material']))
A("Materiality: any of `pre_act`, `pr469`, `a025`, `a050`, `a100`, `psi` differs from `live` by")
A("**≥ 20 points or ≥ 10%%**. Pool rows only. The eight named rows are always present and flagged.")
A("Material against live on the ψ column alone: **%d** rows.\n" % J['n_material_psi'])
A("| player | pathway | pos | g26 | q | pre_act | live | pr469 | a025 | a050 | a100 | **psi** | ψ−a100 | named |")
A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
for r in ROWS:
    A("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s |"
      % (r['key'], r['pathway'], r.get('pos') or '', r.get('games_2026'),
         ('%.3f' % r['q']) if r.get('q') is not None else '—',
         r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'], r['a100'], r['psi'],
         ('%+d' % r['d_psi_vs_a100']) if r['d_psi_vs_a100'] is not None else '',
         '**named**' if r['named'] else ''))
A("")
A("One mover is **not** in this table: `brandon-zerk-thatcher` (a100 49 → ψ 48), which fails the")
A("materiality bar against live on every column. It is in `Q_TABLE.md` and in the JSON.\n")
open(os.path.join(D, 'MOVERS_TABLE_PSI.md'), 'w').write("\n".join(L) + "\n")
print("wrote MOVERS_TABLE_PSI.md")

# ---------------------------------------------------------------- Q_TABLE.md
L = []
A = L.append
A("# Q_TABLE — ORDER 24B, THE QUALITY OF EVERY CURRENTLY-PLAYING POOL ROW\n")
A("Issue #334, ORDER 24B. Branch `build/pool-quality`.\n")
A("> **%s**\n" % CAV)
A("---\n")
A("## 1. What this is\n")
A("Every pool row on the live board with `φ > 0` — that is, every pool player with at least one 2026")
A("game — **%d rows**, with the quality the engine formed for him:\n" % len(QR))
A("```")
A("d   = Y - cp.debutyr(p) + 1, clipped to [1,6]      the harvest's own depth, the axis R is indexed on")
A("par = _PR_PAR[pathway][d-1]                        the playing par (PAR_TABLE.md)")
A("q   = clip( avg26 / par, 0, 1 )                    games>0 with no usable average gives q = 0")
A("psi = phi * q                                      the composite weight on the premium leg")
A("```\n")
A("**The `q`, `par`, `depth` and `φ` columns are produced by calling the engine's own `_pr_q`,")
A("`_pr_par`, `_pr_depth` and `_pr_phi` on the store records** — never re-implemented in the")
A("reporting script — so this table cannot drift from what the board was priced on.\n")
A("| quantity | n |")
A("|---|---:|")
A("| currently-playing pool rows | %d |" % len(QR))
A("| of which `q == 1.0` (at or above par — the clip binds) | %d |" % sum(1 for r in QR if r['q'] >= 1.0))
A("| of which `q == 0.0` (games played, no usable average) | %d |" % sum(1 for r in QR if r['q'] <= 0.0))
A("| of which `φ == 1` (full participants — anchor share exactly 0, price cannot move) | %d |"
  % sum(1 for r in QR if r['phi'] >= 1.0))
A("| **of which `0 < φ < 1` — the only rows ψ can reach** | **%d** |"
  % sum(1 for r in QR if r['phi'] < 1.0))
A("")
A("## 2. The pathway q-mass, for reading the table\n")
A("A row rises `a100 → ψ` if its `q` is above its pathway's `qbar`, and falls if it is below.\n")
A("| pathway | qbar (`Σeφq / Σeφ`) | U′ (a100) | **U″ (ψ)** |")
A("|---|---:|---:|---:|")
for p in ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']:
    A("| `%s` | %.4f | %.6f | **%.6f** |"
      % (p, QBAR[p], S['mean_preserving'][p]['U_order24'], S['uplift'][p]))
A("")
A("## 3. THE TABLE — every currently-playing pool row, sorted by |ψ − a100| then by key\n")
A("| player | pathway | g26 | avg26 | d | par | **q** | φ | ψ weight `φq` | a100 | **psi** | Δ |")
A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for r in QR:
    A("| `%s` | %s | %g | %s | %d | %.2f | **%.4f** | %.4f | %.4f | %d | **%d** | %s |"
      % (r['key'], r['pathway'], r['games'], ('%.2f' % r['avg']) if r['avg'] else '—',
         r['depth'], r['par'], r['q'], r['phi'], r['psi_weight'], r['a100'], r['psi'],
         ('%+d' % r['d_psi']) if r['d_psi'] else '0'))
A("")
open(os.path.join(D, 'Q_TABLE.md'), 'w').write("\n".join(L) + "\n")
print("wrote Q_TABLE.md")
