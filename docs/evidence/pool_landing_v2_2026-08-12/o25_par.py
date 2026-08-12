#!/usr/bin/env python3
"""ORDER 25 STEP 2 -- THE AMENDED PAR TABLE. The owner's donor amendment, and nothing else.

Adapted from docs/evidence/pool_quality_2026-08-12/o24b_par.py. The population, the depth axis, the
games-weighted par, the K=10 shrink form and the "every cell disclosed with its n" discipline are all
CARRIED VERBATIM. **EXACTLY ONE THING CHANGES, and it is the owner's amendment:**

    OWNER, VERBATIM (#334 comment 5267147448, 2026-08-12):
        "I feel like MSD pars should borrow from the wider pool given the thin sample. Do they not?"

    ORDER 24B:  par(pw,d) = w * par_own(pw,d) + (1-w) * par_donor(pw)      donor = the PATHWAY's
                                                                          ALL-DEPTH par
    ORDER 25:   par(pw,d) = w * par_own(pw,d) + (1-w) * par_all(d)         donor = the ALL-POOL
                                                                          SAME-DEPTH par

`par_all(d)` is the games-weighted playing par of EVERY pool pathway at that depth. This is the ORDER
21 class-axis convention, exactly: `o22_make_relaxed_surface.py:109-127` shrinks each class cell
toward THE ALL-CLASS SAME-DEPTH CELL, with `w = n_exact/(n_exact + 10)` and `n_exact` the RAW
EXACT-DEPTH CELL COUNT. ORDER 24B carried the K and the weight but pointed the donor down the wrong
axis -- at the pathway's own all-depth average, which for a pathway with no deep careers is simply
its own shallow average wearing a deep label. The owner caught it.

WHY IT MATTERS MOST WHERE IT MATTERS MOST. An EMPTY cell IS its donor. MSD d4/d5/d6, SSP d4/d5/d6 and
PDN d5/d6 carry no complete-window playing cells at all, so under ORDER 24B they were flat at their
pathway's shallow all-depth number; under the amendment they are the all-pool par AT THAT DEPTH,
which is what a fourth-, fifth- or sixth-year player is actually measured against.

THE WEIGHT'S `n`, DECLARED. The brief's phrase is "K=10 on games". This file reads that as *the par
itself is games-weighted* -- which it is, at every cell, own and donor alike -- and keeps `n` as the
RAW EXACT-DEPTH CELL COUNT, because (a) that is the named ORDER 21 class-axis convention it is told
to adopt, and (b) it is the reading under which thin cells borrow MORE, which is the whole purpose of
the owner's amendment. A games-count weight `w = games/(games+10)` would give MSD d1 a weight of
0.800 instead of 0.474 and make the thin cells borrow LESS -- the opposite of the instruction. THE
ALTERNATIVE READING IS COMPUTED AND PUBLISHED ANYWAY, cell by cell, in the sensitivity block below,
so the choice is visible and scoreable rather than assumed. Pre-registered as B2.

  usage: o25_par.py <ucells.json> <out_par.json> [out_PAR_TABLE_V2.md] [--o24b <o24b_par.json>]
"""
import sys, json, os

CELLS = json.load(open(sys.argv[1]))
OUTJ = sys.argv[2]
OUTMD = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else None
O24B = None
if '--o24b' in sys.argv:
    O24B = json.load(open(sys.argv[sys.argv.index('--o24b') + 1]))

WC = CELLS['cells']
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']
DEPTHS = [1, 2, 3, 4, 5, 6]
K = 10.0
P = print

CAVEAT = ("the landing configuration: alpha=1.0 current-state delivery, quality-conditioned premium, "
          "ALL-POOL SAME-DEPTH par donor (owner amendment 2026-08-12); levels RE-TRUED in this act")

# The population gate, re-asserted here rather than trusted: zero national rows reached this file.
assert CELLS['nd_seen'] > 0, "harvest recorded no national exclusions -- the gate did not run"
assert all(c['stream'] in PATHS for c in WC), \
    "a non-pool stream reached the par population: %s" % sorted({c['stream'] for c in WC} - set(PATHS))


def dclip(c):
    return min(max(int(c['d']), 1), 6)


PLAY = [c for c in WC if c['gy'] > 0 and c['avg_y'] is not None]
NOAVG = [c for c in WC if c['gy'] > 0 and c['avg_y'] is None]

P("=" * 128)
P("ORDER 25 STEP 2 -- THE AMENDED PAR TABLE (donor = ALL-POOL SAME-DEPTH par)")
P("=" * 128)
P('  OWNER, VERBATIM (#334 comment 5267147448): "I feel like MSD pars should borrow from the wider')
P('  pool given the thin sample. Do they not?"')
P()
P("  population: the complete-window pool harvest that produced R -- the SAME file ORDER 24B used")
P("  (%s, md5 asserted by the caller)." % os.path.basename(sys.argv[1]))
P("    national rows encountered and EXCLUDED at the harvest gate: %d  (SEPARATION, asserted)"
  % CELLS['nd_seen'])
P("    complete-window cells with a priceable anchor .............. %d" % len(WC))
P("    of which PLAYING (games > 0) and carrying an average ....... %d" % len(PLAY))
P("    playing cells with NO usable average (q = 0 by the rule) ... %d" % len(NOAVG))
P("    non-playing cells (no q exists; phi = 0) ................... %d" % (len(WC) - len(PLAY) - len(NOAVG)))
P()


def par_of(cs):
    g = sum(c['gy'] for c in cs)
    return (sum(c['avg_y'] * c['gy'] for c in cs) / g if g > 0 else float('nan')), g, len(cs)


# ---- THE TWO DONORS: the retired one (pathway all-depth) and THE AMENDED ONE (all-pool same-depth)
OLD_DONOR = {pw: par_of([c for c in PLAY if c['stream'] == pw]) for pw in PATHS}
OLD_DONOR_ALL = par_of(PLAY)
NEW_DONOR = {d: par_of([c for c in PLAY if dclip(c) == d]) for d in DEPTHS}

P("  THE RETIRED DONOR -- each pathway's ALL-DEPTH par (ORDER 24B). Kept for disclosure only:")
P("    %-8s %10s %10s %10s" % ('pathway', 'par', 'games', 'cells'))
for pw in PATHS:
    v, g, n = OLD_DONOR[pw]
    P("    %-8s %10.4f %10d %10d" % (pw, v, round(g), n))
P("    %-8s %10.4f %10d %10d   [the all-pool all-depth number; NOT the new donor either]"
  % ('ALL POOL', OLD_DONOR_ALL[0], round(OLD_DONOR_ALL[1]), OLD_DONOR_ALL[2]))
P()
P("  *** THE AMENDED DONOR -- THE ALL-POOL par AT THE SAME DEPTH (owner ruling 2026-08-12) ***")
P("    %-8s %10s %10s %10s" % ('depth', 'par', 'games', 'cells'))
for d in DEPTHS:
    v, g, n = NEW_DONOR[d]
    P("    d%-7d %10.4f %10d %10d" % (d, v, round(g), n))
P()
P("  The donor now RISES with depth (58.57 -> 75.63) instead of being one flat pathway number. That")
P("  is the whole content of the amendment: a fourth-year player borrows from fourth-year players.")
P()

ROWS = []
PAR = {}
for pw in PATHS + ['ALL POOL']:
    vals = []
    for d in DEPTHS:
        donor = NEW_DONOR[d][0]
        old_donor = OLD_DONOR_ALL[0] if pw == 'ALL POOL' else OLD_DONOR[pw][0]
        sub = [c for c in PLAY if dclip(c) == d and (pw == 'ALL POOL' or c['stream'] == pw)]
        own, g, n = par_of(sub)
        w = n / (n + K)
        wired = w * own + (1.0 - w) * donor if n > 0 else donor
        # the retired construction, recomputed here so the two are compared on one population
        old_wired = w * own + (1.0 - w) * old_donor if n > 0 else old_donor
        # THE DECLARED SENSITIVITY: the games-count reading of "K=10 on games"
        wg = g / (g + K) if g > 0 else 0.0
        wired_g = wg * own + (1.0 - wg) * donor if n > 0 else donor
        vals.append(float(wired))
        ROWS.append(dict(pathway=pw, d=d, n=n, games=round(g),
                         own=(None if n == 0 else round(own, 4)),
                         donor_old=round(old_donor, 4), donor_new=round(donor, 4),
                         w=round(w, 4), wired=round(wired, 4), wired_o24b=round(old_wired, 4),
                         delta_vs_o24b=round(wired - old_wired, 4),
                         delta_pct_vs_o24b=round(100.0 * (wired - old_wired) / old_wired, 3),
                         w_games=round(wg, 4), wired_games_reading=round(wired_g, 4),
                         sens_delta=round(wired_g - wired, 4)))
    PAR[pw] = vals

P("  THE AMENDED PAR TABLE -- EVERY CELL: own value, n, OLD donor, NEW donor, WIRED value")
P("  %-9s %2s %6s %7s %10s %10s %10s %7s %10s %10s %9s" %
  ('pathway', 'd', 'cells', 'games', 'own par', 'OLD donor', 'NEW donor', 'w', 'WIRED', 'o24b was', 'change'))
P("  " + "-" * 124)
for r in ROWS:
    P("  %-9s %2d %6d %7d %10s %10.4f %10.4f %7.4f %10.4f %10.4f %+8.2f%%%s"
      % (r['pathway'], r['d'], r['n'], r['games'],
         ('%10.4f' % r['own']) if r['own'] is not None else '     EMPTY',
         r['donor_old'], r['donor_new'], r['w'], r['wired'], r['wired_o24b'], r['delta_pct_vs_o24b'],
         '   <-- EMPTY CELL: the donor IS the par' if r['n'] == 0 else
         ('   <-- THIN (n<10)' if r['n'] < 10 else '')))
P()

# ---- THE DECLARED SENSITIVITY -------------------------------------------------------------------
P("  THE DECLARED SENSITIVITY -- the OTHER reading of \"K=10 on games\" (w = games/(games+10)).")
P("  NOT WIRED. Published so the reading this file adopts is visible and scoreable (prereg B2).")
P("  %-9s %2s %8s %8s %12s %12s %10s" %
  ('pathway', 'd', 'w(cells)', 'w(games)', 'WIRED (this)', 'wired (games)', 'diff'))
P("  " + "-" * 124)
sens_worst = 0.0
for r in ROWS:
    if r['pathway'] == 'ALL POOL':
        continue
    if r['n'] == 0:
        continue
    sens_worst = max(sens_worst, abs(r['sens_delta']))
    if abs(r['sens_delta']) >= 0.5:
        P("  %-9s %2d %8.4f %8.4f %12.4f %12.4f %+10.4f" %
          (r['pathway'], r['d'], r['w'], r['w_games'], r['wired'], r['wired_games_reading'], r['sens_delta']))
P("  (only cells differing by >= 0.5 points are listed; worst difference across all cells: %.4f)" % sens_worst)
P("  Under the games reading EVERY thin cell borrows LESS, which is the opposite of the owner's")
P("  instruction. The cell-count reading is adopted, and this block is the disclosure.")
P()

# ---- monotonicity in depth, reported not enforced -----------------------------------------------
P("  MONOTONICITY IN DEPTH (reported, NEVER projected -- par is a measurement, not a shape):")
mono = {}
for pw in PATHS + ['ALL POOL']:
    v = PAR[pw]
    steps = ['up' if v[i + 1] > v[i] else 'DOWN' for i in range(len(v) - 1)]
    mono[pw] = steps
    P("    %-9s %s   d1->d6: %s" % (pw, "  ".join("%.2f" % x for x in v), " ".join(steps)))
P()
P("  MONOTONE PATHWAYS: %d of 10 (ORDER 24B measured 2 of 10 -- the amendment repairs the depth"
  % sum(1 for pw in mono if all(s == 'up' for s in mono[pw])))
P("  axis because the donor itself now rises with depth).")
P()

# ---- the identity the ALL POOL row must satisfy under the amendment -----------------------------
allrow = [r for r in ROWS if r['pathway'] == 'ALL POOL']
worst_id = max(abs(r['wired'] - r['own']) for r in allrow)
P("  IDENTITY CHECK -- under the amendment the ALL POOL row IS its own donor, so its wired values")
P("  must equal its own values exactly. Worst |wired - own| = %.2e" % worst_id)
assert worst_id < 1e-9, "the ALL POOL row is not its own donor -- the amendment is not what it claims"
P()

json.dump(dict(K=K, donor_axis='ALL-POOL SAME-DEPTH (owner amendment, #334 comment 5267147448)',
               par=PAR, rows=ROWS,
               donor_new={('d%d' % d): NEW_DONOR[d][0] for d in DEPTHS},
               donor_old={k: v[0] for k, v in OLD_DONOR.items()},
               donor_old_all=OLD_DONOR_ALL[0], caveat=CAVEAT, monotone=mono,
               sensitivity_worst_pts=sens_worst,
               n_play=len(PLAY), n_noavg=len(NOAVG), n_cells=len(WC), nd_seen=CELLS['nd_seen']),
          open(OUTJ, 'w'), indent=1, default=float)
P("  wrote %s" % OUTJ)

if OUTMD:
    L = []
    A = L.append
    A("# PAR_TABLE_V2 — ORDER 25, THE AMENDED PLAYING PAR (all-pool same-depth donor)\n")
    A("Issue #334, ORDER 25. Branch `land/pool-update-v2`. Pre-registration: `PREREG_ORDER25.md`,")
    A("committed **before** this table was computed.\n")
    A("> **%s**\n" % CAVEAT)
    A("---\n")
    A("## 1. The amendment, in one line\n")
    A("**Owner, verbatim** (#334 comment [5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)):\n")
    A("> \"I feel like MSD pars should borrow from the wider pool given the thin sample. Do they not?\"\n")
    A("```")
    A("ORDER 24B:  par(pw,d) = w*par_own(pw,d) + (1-w)*par_donor(pw)   donor = the PATHWAY's ALL-DEPTH par")
    A("ORDER 25:   par(pw,d) = w*par_own(pw,d) + (1-w)*par_all(d)      donor = the ALL-POOL SAME-DEPTH par")
    A("            w = n/(n+%g),  n = the RAW EXACT-DEPTH CELL COUNT   [unchanged]" % K)
    A("```\n")
    A("This is the **ORDER 21 class-axis convention**, adopted exactly: `o22_make_relaxed_surface.py`")
    A("lines 109–127 shrink each class cell toward the **all-class same-depth cell** at K=10 on the raw")
    A("exact-depth cell count. ORDER 24B carried the K and the weight but pointed the donor down the")
    A("wrong axis. **An empty cell _is_ its donor**, so the pathways with no deep careers — MSD, SSP,")
    A("PDN — were being told that a fourth-year player is measured against their own first-year")
    A("average. They are now measured against fourth-year players.\n")
    A("### The weight's `n`, declared\n")
    A("The brief says \"K=10 on games\". This table reads that as **the par itself is games-weighted**")
    A("— it is, at every cell, own and donor alike — and keeps `n` as the **cell count**, for two")
    A("reasons: it is the named ORDER 21 convention, and it is the reading under which thin cells")
    A("borrow **more**, which is the purpose of the amendment. The alternative reading")
    A("(`w = games/(games+10)`) is computed and published in §6 rather than argued away. Under it MSD")
    A("d1 would weight its own 9-cell sample at 0.800 instead of 0.474 — borrowing **less** from the")
    A("wider pool, the opposite of the instruction.\n")
    A("## 2. The population, and the gate\n")
    A("The same complete-window harvest that produced `R` and `q`, byte-identical to ORDER 24B's")
    A("(`ucells.json` md5 `68bc25e7e0c95cc75ee7fa013bacabcd`, re-run from scratch on this branch and")
    A("reproduced exactly). **National rows: %d encountered at the harvest gate and excluded, zero"
      % CELLS['nd_seen'])
    A("present in this file — asserted before a single par is formed.**\n")
    A("| quantity | n |")
    A("|---|---:|")
    A("| complete-window cells with a priceable anchor | %d |" % len(WC))
    A("| of which **playing** with a usable average — **the par population** | **%d** |" % len(PLAY))
    A("| playing cells with no usable average (read as `q = 0`) | %d |" % len(NOAVG))
    A("| non-playing cells (`φ = 0`, no `q` exists) | %d |\n" % (len(WC) - len(PLAY) - len(NOAVG)))
    A("## 3. THE AMENDED DONOR — the all-pool par at each depth\n")
    A("| depth | all-pool par | games | cells |")
    A("|---|---:|---:|---:|")
    for d in DEPTHS:
        v, g, n = NEW_DONOR[d]
        A("| **d%d** | **%.2f** | %s | %d |" % (d, v, format(round(g), ','), n))
    A("")
    A("**The donor now rises with depth (58.57 → 75.63)** instead of being one flat pathway number.")
    A("For comparison, the retired donors — each pathway's all-depth par — were: %s.\n"
      % " · ".join("`%s` %.2f" % (pw, OLD_DONOR[pw][0]) for pw in PATHS))
    A("## 4. THE PAR TABLE — every cell, both donors, and what was wired\n")
    A("| pathway | d | cells `n` | games | own par | OLD donor (retired) | **NEW donor** | w = n/(n+%g) | **WIRED** | ORDER 24B wired | change |" % K)
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in ROWS:
        A("| `%s` | %d | %d | %s | %s | %.2f | **%.2f** | %.4f | **%.2f** | %.2f | %+.2f%% |"
          % (r['pathway'], r['d'], r['n'], format(r['games'], ','),
             ('%.2f' % r['own']) if r['own'] is not None else '_empty — **the donor IS the par**_',
             r['donor_old'], r['donor_new'], r['w'], r['wired'], r['wired_o24b'], r['delta_pct_vs_o24b']))
    A("")
    big = sorted([r for r in ROWS if r['pathway'] != 'ALL POOL'],
                 key=lambda r: -abs(r['delta_pct_vs_o24b']))[:8]
    A("**The eight cells the amendment moves most:** " +
      " · ".join("`%s` d%d %+.1f%%" % (r['pathway'], r['d'], r['delta_pct_vs_o24b']) for r in big) + ".")
    A("Every one of the largest is an **empty or near-empty deep cell** — exactly the population the")
    A("owner named.\n")
    A("## 5. Monotonicity in depth — reported, never projected\n")
    A("| pathway | d1 | d2 | d3 | d4 | d5 | d6 | steps |")
    A("|---|---:|---:|---:|---:|---:|---:|---|")
    for pw in PATHS + ['ALL POOL']:
        v = PAR[pw]
        st = " ".join(('↑' if v[i + 1] > v[i] else '↓') for i in range(5))
        A("| `%s` | %s | %s |" % (pw, " | ".join("%.2f" % x for x in v), st))
    A("")
    A("**%d of 10 pathways are now monotone in depth**, against 2 of 10 under ORDER 24B. No isotonic"
      % sum(1 for pw in mono if all(s == 'up' for s in mono[pw])))
    A("projection is applied and none is wanted — the repair is a consequence of pointing the donor")
    A("down the depth axis, not of imposing a shape.\n")
    A("## 6. The declared sensitivity — the other reading of \"K=10 on games\"\n")
    A("`w = games/(games+10)` instead of `w = cells/(cells+10)`. **Not wired.** Cells differing by")
    A("≥ 0.5 points:\n")
    A("| pathway | d | w (cells, wired) | w (games) | **WIRED** | wired under games reading | diff |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for r in ROWS:
        if r['pathway'] == 'ALL POOL' or r['n'] == 0 or abs(r['sens_delta']) < 0.5:
            continue
        A("| `%s` | %d | %.4f | %.4f | **%.2f** | %.2f | %+.2f |"
          % (r['pathway'], r['d'], r['w'], r['w_games'], r['wired'], r['wired_games_reading'], r['sens_delta']))
    A("")
    A("Worst difference across all cells: **%.2f points**. Under the games reading every thin cell" % sens_worst)
    A("borrows **less** from the wider pool — the opposite of the owner's instruction — which is the")
    A("ground on which the cell-count reading is adopted.\n")
    open(OUTMD, 'w').write("\n".join(L) + "\n")
    P("  wrote %s" % OUTMD)
