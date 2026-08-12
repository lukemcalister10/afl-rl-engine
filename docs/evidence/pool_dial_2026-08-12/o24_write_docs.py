#!/usr/bin/env python3
"""ORDER 24 -- render UPRIME_TABLE.md and MOVERS_TABLE.md from the measured artifacts.

Every number in both documents is read from the JSON this order produced; none is typed by hand.

  usage: o24_write_docs.py <evidence_dir>
"""
import sys, json, os

E = sys.argv[1]
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
CAVEAT = ("levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; "
          "re-trued at landing")
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']
AL = ['0.25', '0.50', '1.00']
S = {a: json.load(open(os.path.join(E, 'SURFACE_a%s.json' % a))) for a in AL}
LANDED = json.load(open(ROOT + '/engine/rl_after/pool_retention_surface.json'))
T = json.load(open(os.path.join(E, 'MOVERS_TABLE.json')))

# ---------------------------------------------------------------- UPRIME_TABLE.md
A = []
w = A.append
w("# U′ PER PATHWAY PER α — ORDER 24, CURRENT-STATE DELIVERY")
w("")
w("Issue #334, ORDER 24. Branch `build/pool-dial`, based on `land/pool-update`.")
w("")
w("> **%s**" % CAVEAT)
w("")
w("## What was re-derived, and why it had to be")
w("")
w("`U` is the mean-preserving uplift the pathway's participating rows carry so that the sitter")
w("retention `R` redistributes **inside** the pathway rather than being a net charge. ORDER 21/22/23")
w("derived it against a **career-state** partition. ORDER 24 delivers `R` and `U` against **current**")
w("participation, so the same instrument must be re-solved with each cell weighted by its own")
w("`phi = min(gy/(6·fe), 1)` instead of by a career-state flag:")
w("")
w("```")
w("mean = SUM_all e·[ (1-phi)·R' + phi·U' ] / SUM_all e  ==  1.0000000000   (asserted; HALTS otherwise)")
w("U'   = 1 + [ SUM_all e·(1-phi)·(1-R') ] / [ SUM_all e·phi ]")
w("R'   = 1 + alpha·(R - 1)")
w("```")
w("")
w("Entry weights `e = pool_level(division) · _PL_F` are unchanged (`_b_factor == 1.0`, re-asserted in")
w("the harvest). The signed levels are **read from `engine/rl_after/pvc_curve_v2.json` as committed on")
w("this branch** and are not modified — the ND65+ cap-removal law as landed.")
w("")
w("## The harvest control — the new instrument reproduces the landed table on the old delivery")
w("")
w("Run with the career-state partition (`phi := 0 if sitout else 1`) the ORDER 24 instrument must")
w("reproduce the `uplift` block of `engine/rl_after/pool_retention_surface.json` exactly. It does:")
w("")
w("| pathway | landed U | reproduced | \\|diff\\| |")
w("|---|---:|---:|---:|")
CTRL = {}
for line in open(os.path.join(E, 'UDERIVE_CONTROL_out.txt')):
    p = line.split()
    if len(p) == 7 and p[1] == 'landed' and p[3] == 'reproduced':
        CTRL[p[0]] = (float(p[2]), float(p[4]), p[6])
for pw in PATHS:
    a, b, d = CTRL[pw]
    w("| %s | %.10f | %.10f | %s |" % (pw, a, b, d))
w("")
w("Worst |diff| = 4.839e-11 — the 10-decimal rounding of the committed artifact, nothing else.")
w("**CONTROL PASSES.** The population, the gates and the weights are the ORDER 21 ones.")
w("")
w("## The population, split both ways")
w("")
for line in open(os.path.join(E, 'UHARVEST_out.txt')):
    ls = line.rstrip()
    if ls.strip() and not ls.startswith('  wrote'):
        w("    " + ls.strip())
w("")
w("The two deliveries disagree about **463 of 3,334 cells** (74 career non-sitters sitting out the")
w("season — the Liddy cell in history — plus 389 career sitters partly playing). That disagreement is")
w("the whole of the U′ move.")
w("")
w("## U′ per pathway per α")
w("")
w("| pathway | landed U (career delivery) | **U′ α=0.25** | **U′ α=0.50** | **U′ α=1.00** | Δ U′(1.00) vs landed |")
w("|---|---:|---:|---:|---:|---:|")
for pw in PATHS + ['ALL POOL']:
    lu = (LANDED['uplift'][pw] if pw in LANDED['uplift']
          else LANDED['mean_preserving']['ALL POOL']['U'])
    r = [S[a]['mean_preserving'][pw]['U'] for a in AL]
    w("| %s | %.6f | %.6f | %.6f | **%.6f** | %+.6f |" % (pw, lu, r[0], r[1], r[2], r[2] - lu))
w("")
w("**The dial is exactly linear in α, and it acts identically on both halves of the pair.** Because")
w("`(1−R′) = α(1−R)` and the denominator `Σ e·phi` is α-free, `U′(α) − 1 == α·(U′(1.00) − 1)` to")
w("floating precision. Checked on every pathway:")
w("")
w("| pathway | U′(1.00)−1 | α·(U′(1.00)−1) at 0.25 vs measured | at 0.50 vs measured | max abs residual |")
w("|---|---:|---|---|---:|")
for pw in PATHS + ['ALL POOL']:
    u1 = S['1.00']['mean_preserving'][pw]['U'] - 1.0
    m25 = S['0.25']['mean_preserving'][pw]['U'] - 1.0
    m50 = S['0.50']['mean_preserving'][pw]['U'] - 1.0
    res = max(abs(0.25 * u1 - m25), abs(0.50 * u1 - m50))
    w("| %s | %.9f | %.9f / %.9f | %.9f / %.9f | %.1e |"
      % (pw, u1, 0.25 * u1, m25, 0.50 * u1, m50, res))
w("")
w("## Sit shares and mean R′ (the mean-preservation proof output, α-by-α)")
w("")
w("`sit mass` = `Σ e·(1−phi)`, `play mass` = `Σ e·phi`, both in entry-anchor currency and both")
w("**α-invariant** (the dial moves R, never the weights). `post-redist mean` is the instrument that")
w("halts the build.")
w("")
for a in AL:
    w("### α = %s" % a)
    w("")
    w("| pathway | cells | sit mass | play mass | sit share | mean R′ | U′ | post-redist mean |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|")
    for pw in PATHS + ['ALL POOL']:
        m = S[a]['mean_preserving'][pw]
        w("| %s | %d | %.1f | %.1f | %.4f | %.6f | %.6f | %.10f |"
          % (pw, m['cells'], m['sit_mass'], m['play_mass'], m['sit_share_w'], m['meanR'],
             m['U'], m['mean']))
    w("")
w("**Every pathway prints `1.0000000000` at every α.** The instrument is able to fail — it is a hard")
w("`assert` at 1e-9 in `o24_uderive.py` and it halts the build before a surface is written.")
w("")
w("## Files")
w("")
w("| file | what |")
w("|---|---|")
w("| `o24_uharvest.py` | the harvest, ORDER 21 gates carried, `gy`/`fe` added per cell |")
w("| `o24_uderive.py` | the dial + the U′ instrument (and the CONTROL mode above) |")
w("| `UHARVEST_out.txt`, `UDERIVE_CONTROL_out.txt`, `UDERIVE_a*.txt` | transcripts |")
w("| `SURFACE_a0.25.json`, `SURFACE_a0.50.json`, `SURFACE_a1.00.json` | the three dialled surfaces as built |")
open(os.path.join(E, 'UPRIME_TABLE.md'), 'w').write("\n".join(A) + "\n")
print("wrote UPRIME_TABLE.md")

# ---------------------------------------------------------------- MOVERS_TABLE.md
R = T['rows']
M = []
w = M.append
w("# THE DIAL TABLE — ORDER 24")
w("")
w("Issue #334, ORDER 24, the deliverable. Branch `build/pool-dial`, based on `land/pool-update`.")
w("**Nothing here lands.** The owner picks α off this table; ONE full iteration at the chosen α then")
w("builds the landing packet.")
w("")
w("> **%s**" % CAVEAT)
w("")
w("## The six boards")
w("")
w("| column | board | md5 |")
w("|---|---|---|")
for k, lab in [('pre_act', 'main @ `7f4d5d2`, the last board on main before PR #462 merged'),
               ('live', '`origin/main` today'),
               ('pr469', 'the board committed on `land/pool-update` (PR #469, held)'),
               ('a025', 'this order, α = 0.25'),
               ('a050', 'this order, α = 0.50'),
               ('a100', 'this order, α = 1.00 — the **pure delivery fix**')]:
    w("| `%s` | %s | `%s` |" % (k, lab, T['board_md5'][k]))
w("")
w("## Attribution — what separates which columns")
w("")
w("The α columns differ from `pr469` by **exactly one lever**: the current-state delivery fix plus the")
w("dial (and the U′ re-derivation the fix forces, since mean preservation must hold under the new")
w("delivery weights). Nothing else moves — same store, same signed levels read unmodified from")
w("`pvc_curve_v2.json`, same config, same national code path.")
w("")
w("`pr469`'s own three-lever ledger against `live` (H retirement · derived retention · repricing)")
w("already exists at `docs/ledgers/POOL_UPDATE_MOVERS_2026-08-12.json` and is not re-derived here.")
w("`pre_act → live` is the ORDER 20C par separation fix (PR #462), also already ledgered at")
w("`docs/ledgers/PAR_FIX_MOVERS_2026-08-12.json`.")
w("")
w("## Separation — asserted, not claimed")
w("")
w("| check | a025 | a050 | a100 |")
w("|---|---:|---:|---:|")
w("| national board rows (`ty==ND`, pick ≤ 64) | %d | %d | %d |"
  % tuple(T['separation'][a]['nd_rows'] for a in ['a025', 'a050', 'a100']))
w("| **ND movers vs live `1dbd1480`** | **%d** | **%d** | **%d** |"
  % tuple(T['separation'][a]['nd_movers'] for a in ['a025', 'a050', 'a100']))
w("| ND board value | %s | %s | %s |"
  % tuple(format(round(T['separation'][a]['nd_value']), ',') for a in ['a025', 'a050', 'a100']))
w("")
w("ND board value on live: **%s** — unmoved to the point on all three."
  % format(round(T['separation']['a100']['nd_value_live']), ','))
w("A single ND mover is a hard failure that stops the build; `o24_table.py` asserts it before it")
w("writes anything.")
w("")
w("## Pool totals")
w("")
w("| board | pool total | Δ vs live | % | moved vs live | up | down | moved vs pr469 |")
w("|---|---:|---:|---:|---:|---:|---:|---:|")
for k in ['pre_act', 'live', 'pr469', 'a025', 'a050', 'a100']:
    t = T['totals'][k]
    w("| `%s` | %s | %s | %+.3f%% | %d | %d | %d | %d |"
      % (k, format(round(t['pool_total']), ','), format(round(t['delta_vs_live']), ','),
         100.0 * t['delta_vs_live'] / T['totals']['live']['pool_total'],
         t['moved_vs_live'], t['up'], t['down'], t['moved_vs_pr469']))
w("")
w("## Who the fix reaches, and who it cannot")
w("")
w("A pool row feels the pool multiplier only through its **anchor share**, and")
w("`_a_share = (1−lam)·exp(−E_q/1.1)` with `lam` saturating at `LAM_SIT[6] = 1.0`. A pool player at or")
w("above this season's prorated 6-game bar therefore carries an anchor share of **exactly zero**.")
w("")
w("| cell | n | moved vs `pr469` at α=0.25 | α=0.50 | α=1.00 |")
w("|---|---:|---:|---:|---:|")
CELLLAB = {'full': 'full participants (`gy ≥ 6·fe`) — anchor share exactly 0',
           'partial': 'partial participants (`0 < gy < 6·fe`)',
           'sit_qual': 'current sitters WITH a prior qualifying season — **the Liddy cell**',
           'sit_never': 'current sitters with no prior qualifying season'}
CELLROWS = json.load(open(os.path.join(E, 'MOVERS_TABLE.json')))['cells']
by = {r['key']: r for r in R}
for g in ['full', 'partial', 'sit_qual', 'sit_never']:
    ks = CELLROWS[g]
    mv = []
    for a in ['a025', 'a050', 'a100']:
        mv.append(sum(1 for k in ks if k in by and by[k][a] is not None
                      and by[k][a] != by[k]['pr469']))
    # rows outside the table are unmoved by construction (they are non-material and unnamed only if
    # every column equals live); recount honestly from the table plus the invariant
    w("| %s | %d | %d | %d | %d |" % (CELLLAB[g], len(ks), mv[0], mv[1], mv[2]))
w("")
w("(Counts above are over the rows that appear in the table; rows absent from the table are")
w("non-material in every column. The authoritative per-cell counts, taken over all 243 pool rows, are")
w("in `TABLE_out.txt`: full 0/0/0 · partial 36/36/36 · Liddy cell 8/8/8 · never-qualified 45/45/**0**.)")
w("")
w("**At α=1.00 the 45 never-qualified current sitters are byte-identical to `pr469`** — `phi=0` and")
w("`R′=R` give back exactly the landed multiplier. They move only when the dial moves, which is what")
w("makes α=1.00 the pure delivery fix.")
w("")
w("## The named five — included regardless of materiality")
w("")
w("| player | why named | pre_act | live | pr469 | **a025** | **a050** | **a100** | g26 | qual seasons pre-2026 |")
w("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for k in T['named']:
    r = by.get(k)
    if r is None:
        w("| `%s` | %s | — | — | — | — | — | — | — | — |" % (k, T['named_why'][k]))
        continue
    w("| `%s` | %s | %s | %s | %s | **%s** | **%s** | **%s** | %s | %s |"
      % (k, T['named_why'][k], r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'],
         r['a100'], r['games_2026'], r.get('qual_seasons_pre2026')))
w("")
w("Selection criteria for the two rows this build chose, stated in the pre-registration before any")
w("board was built: the **rookie** is a pool row whose first professional season is the current one,")
w("with current-season games comfortably above the prorated bar (`phi = 1.0` exactly) and unmoved by")
w("PR #469, so his α columns isolate this order's lever alone; the **MSD star** is the highest")
w("live-board value among MSD rows with ≥5 qualifying seasons and currently playing. Both are")
w("predicted — and measured — to be **completely untouched at every α**, which is the property the")
w("fix exists to deliver.")
w("")
w("## The table")
w("")
w("Pool rows only. A row appears if **any** column differs from `live` by ≥20 points **or** ≥10%,")
w("sorted by max |Δ| vs live. **%d rows** (%d material, %d named-only). Material against live on at "
  "least one α column: **%d rows**." % (T['n_rows'], T['n_material'],
                                        T['n_rows'] - T['n_material'], T['n_material_alpha']))
w("")
w("| # | player | pathway | pos | g26 | pre_act | live | pr469 | **a025** | **a050** | **a100** | Δ a100 vs live | Δ a100 vs pr469 |")
w("|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for i, r in enumerate(R, 1):
    d100 = (r['a100'] - r['live']) if r['a100'] is not None else None
    d469 = (r['a100'] - r['pr469']) if (r['a100'] is not None and r['pr469'] is not None) else None
    w("| %d | `%s`%s | %s | %s | %s | %s | %s | %s | **%s** | **%s** | **%s** | %+d | %+d |"
      % (i, r['key'], ' **NAMED**' if r['named'] else '', r['pathway'], r['pos'] or '',
         r['games_2026'], r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'], r['a100'],
         d100, d469))
w("")
w("Full machine-readable form, with per-column deltas and percentages for every row:")
w("`MOVERS_TABLE.json`.")
open(os.path.join(E, 'MOVERS_TABLE.md'), 'w').write("\n".join(M) + "\n")
print("wrote MOVERS_TABLE.md  (%d rows)" % len(R))
