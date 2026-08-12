#!/usr/bin/env python3
"""ORDER 24B STEP 2 -- THE PAR TABLE. The playing par by pathway x career depth.

Derived from the SAME complete-window harvest population that produced R -- o24b_uharvest.py's `WC`
(pool careers only, ZERO national rows asserted at the harvest gate, complete window Y <= 2021,
priceable entry anchor) -- and from nothing else. No store re-read, no second population.

  par_own(pw,d)  = SUM(avg_y * games) / SUM(games)   over PLAYING cells (games>0) with that (pw,d)
  par_donor(pw)  = SUM(avg_y * games) / SUM(games)   over ALL playing cells of that pathway
  w(pw,d)        = n(pw,d) / (n(pw,d) + K),  K = 10, n = the RAW EXACT-DEPTH cell count
  par(pw,d)      = w * par_own + (1-w) * par_donor

THE K=10 SHRINK IS ORDER 22'S CLASS-AXIS FORM, CARRIED VERBATIM (owner ruling 5262213139,
docs/evidence/pool_final_2026-08-12/o22_make_relaxed_surface.py:109-127): the weight uses the raw
exact-depth n recomputed from the harvest, never transcribed, and EVERY cell is disclosed with its
own value, its donor, its weight and what was wired. It is applied at every cell with NO thinness
threshold -- a threshold would be a new cliff, and cliffs are barred.

THE DEPTH AXIS IS THE HARVEST'S OWN, and it is the axis R is indexed on: the harvest sets
draftyr = cp.debutyr(p) - 1 and d = Y - draftyr, and o24_uderive.py's R_of clips it to [1,6]. This
script clips identically, so par(pw,d) and R(pw,cls,d) read the same integer depth for the same cell.
Declared in PREREG_ORDER24B.md section (a)(2).

  usage: o24b_par.py <ucells.json> <out_par.json> [out_PAR_TABLE.md]
"""
import sys, json, os, collections

CELLS = json.load(open(sys.argv[1]))
OUTJ = sys.argv[2]
OUTMD = sys.argv[3] if len(sys.argv) > 3 else None
WC = CELLS['cells']
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']
DEPTHS = [1, 2, 3, 4, 5, 6]
K = 10.0
P = print

CAVEAT = ("levels frozen at #469 values; absolute prices +/-few points, MSD up to ~5%; "
          "re-trued at landing")

# The population gate, re-asserted here rather than trusted: zero national rows reached this file.
assert CELLS['nd_seen'] > 0, "harvest recorded no national exclusions -- the gate did not run"
assert all(c['stream'] in PATHS for c in WC), \
    "a non-pool stream reached the par population: %s" % sorted({c['stream'] for c in WC} - set(PATHS))


def dclip(c):
    return min(max(int(c['d']), 1), 6)


PLAY = [c for c in WC if c['gy'] > 0 and c['avg_y'] is not None]
NOAVG = [c for c in WC if c['gy'] > 0 and c['avg_y'] is None]

P("=" * 120)
P("ORDER 24B STEP 2 -- THE PAR TABLE")
P("=" * 120)
P("  population: the complete-window pool harvest that produced R.")
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


DONOR = {}
for pw in PATHS:
    DONOR[pw] = par_of([c for c in PLAY if c['stream'] == pw])
DONOR_ALL = par_of(PLAY)

P("  PATHWAY ALL-DEPTH PAR (the shrink donor), games-weighted:")
P("    %-8s %10s %10s %10s" % ('pathway', 'par', 'games', 'cells'))
for pw in PATHS:
    v, g, n = DONOR[pw]
    P("    %-8s %10.4f %10d %10d" % (pw, v, round(g), n))
P("    %-8s %10.4f %10d %10d" % ('ALL POOL', DONOR_ALL[0], round(DONOR_ALL[1]), DONOR_ALL[2]))
P()

ROWS = []
PAR = {}
for pw in PATHS + ['ALL POOL']:
    donor = DONOR_ALL[0] if pw == 'ALL POOL' else DONOR[pw][0]
    vals = []
    for d in DEPTHS:
        sub = [c for c in PLAY if dclip(c) == d and (pw == 'ALL POOL' or c['stream'] == pw)]
        own, g, n = par_of(sub)
        w = n / (n + K)
        wired = w * own + (1.0 - w) * donor if n > 0 else donor
        vals.append(float(wired))
        ROWS.append(dict(pathway=pw, d=d, n=n, games=round(g), own=(None if n == 0 else round(own, 4)),
                         donor=round(donor, 4), w=round(w, 4), wired=round(wired, 4),
                         shrink_pts=(None if n == 0 else round(wired - own, 4)),
                         shrink_pct=(None if n == 0 or own <= 0 else round(100.0 * (wired - own) / own, 3))))
    PAR[pw] = vals

P("  THE PAR TABLE -- EVERY CELL DISCLOSED (own value, donor, K=%g weight, what was wired)" % K)
P("  %-9s %2s %7s %8s %10s %10s %8s %10s %9s %8s" %
  ('pathway', 'd', 'cells', 'games', 'own par', 'donor', 'w', 'WIRED', 'shrink', 'shrink%'))
for r in ROWS:
    P("  %-9s %2d %7d %8d %10s %10.4f %8.4f %10.4f %9s %7s%s"
      % (r['pathway'], r['d'], r['n'], r['games'],
         ('%10.4f' % r['own']) if r['own'] is not None else '     EMPTY',
         r['donor'], r['w'], r['wired'],
         ('%+9.4f' % r['shrink_pts']) if r['shrink_pts'] is not None else '        -',
         ('%+7.2f' % r['shrink_pct']) if r['shrink_pct'] is not None else '      -',
         '   <-- THIN (n<10, donor carries the majority)' if r['n'] < 10 else
         ('   <-- shrink >= 2%' if r['shrink_pct'] is not None and abs(r['shrink_pct']) >= 2.0 else '')))
P()

# ---- monotonicity in depth, reported not enforced (no isotonic projection on par) ---------------
P("  MONOTONICITY IN DEPTH (reported, NEVER projected -- par is a measurement, not a shape):")
for pw in PATHS + ['ALL POOL']:
    v = PAR[pw]
    steps = ['%s' % ('up' if v[i + 1] > v[i] else 'DOWN') for i in range(len(v) - 1)]
    P("    %-9s %s   d1->d6: %s" % (pw, "  ".join("%.2f" % x for x in v), " ".join(steps)))
P()

# ---- reconciliation against the supervising seat's four reference points ------------------------
REF = {('MSD', 1): (58.9, 162), ('MSD', 2): (61.4, 174), ('RD', 3): (66.5, 2878), ('SSP', 1): (57.7, 166)}
P("  RECONCILIATION -- the supervising seat's reference points (store md5 d9a24282, complete-window")
P("  <= 2021, d = Y - draftyr). The seat's quick cut and this harvest gate need not agree; a gap")
P("  above 5%% is EXPLAINED, never forced away.")
P("  %-9s %2s %10s %10s %10s %9s %9s %9s" %
  ('pathway', 'd', 'seat par', 'own par', 'wired par', 'gap own', 'gap wired', "seat n"))
RECON = []
for (pw, d), (sp, sn) in REF.items():
    r = next(x for x in ROWS if x['pathway'] == pw and x['d'] == d)
    go = 100.0 * (r['own'] - sp) / sp
    gw = 100.0 * (r['wired'] - sp) / sp
    RECON.append(dict(pathway=pw, d=d, seat_par=sp, seat_n=sn, own=r['own'], wired=r['wired'],
                      gap_own_pct=round(go, 3), gap_wired_pct=round(gw, 3),
                      my_cells=r['n'], my_games=r['games']))
    P("  %-9s %2d %10.2f %10.4f %10.4f %8.2f%% %8.2f%% %9d   (mine: %d cells, %d games)"
      % (pw, d, sp, r['own'], r['wired'], go, gw, sn, r['n'], r['games']))
P()

json.dump(dict(K=K, par=PAR, rows=ROWS, donor={k: v[0] for k, v in DONOR.items()},
               donor_all=DONOR_ALL[0], recon=RECON, caveat=CAVEAT,
               n_play=len(PLAY), n_noavg=len(NOAVG), n_cells=len(WC), nd_seen=CELLS['nd_seen']),
          open(OUTJ, 'w'), indent=1, default=float)
P("  wrote %s" % OUTJ)

if OUTMD:
    L = []
    A = L.append
    A("# PAR_TABLE — ORDER 24B, THE PLAYING PAR BY PATHWAY × CAREER DEPTH\n")
    A("Issue #334, ORDER 24B. Branch `build/pool-quality`. Pre-registration: `PREREG_ORDER24B.md`,")
    A("committed **before** this table was computed.\n")
    A("> **%s**\n" % CAVEAT.replace('+/-', '±'))
    A("---\n")
    A("## 1. The population, and the gate\n")
    A("The par comes from the **same complete-window harvest population that produced `R`** and from")
    A("nothing else — `o24b_uharvest.py`'s `WC`: pool careers only, complete window `Y ≤ 2021`,")
    A("priceable entry anchor. **National rows: %d encountered at the harvest gate and excluded, and"
      % CELLS['nd_seen'])
    A("zero present in this file — asserted in `o24b_par.py` before a single par is formed.**\n")
    A("| quantity | n |")
    A("|---|---:|")
    A("| complete-window cells with a priceable anchor | %d |" % len(WC))
    A("| of which **playing** (`games > 0`) with a usable average — **the par population** | **%d** |" % len(PLAY))
    A("| playing cells with no usable average (read as `q = 0`, never as par) | %d |" % len(NOAVG))
    A("| non-playing cells (`φ = 0`, no `q` exists) | %d |\n" % (len(WC) - len(PLAY) - len(NOAVG)))
    A("## 2. The rule\n")
    A("```")
    A("par_own(pw,d)  = SUM(avg_y * games) / SUM(games)   over playing cells with that (pw,d)")
    A("par_donor(pw)  = SUM(avg_y * games) / SUM(games)   over ALL playing cells of that pathway")
    A("w(pw,d)        = n(pw,d) / (n(pw,d) + %g)          n = raw exact-depth CELL count" % K)
    A("par(pw,d)      = w * par_own + (1-w) * par_donor")
    A("```\n")
    A("`d` is the harvest's own depth, `d = Y − debutyr + 1`, clipped to `[1,6]` — **the same integer")
    A("`R` is indexed on**, so `par(pw,d)` and `R(pw,cls,d)` read the same cell. The K=%g shrink is" % K)
    A("ORDER 22's class-axis form carried verbatim (owner ruling 5262213139); it applies at **every**")
    A("cell with no thinness threshold, and every cell is disclosed below.\n")
    A("## 3. The shrink donor — each pathway's all-depth playing par\n")
    A("| pathway | all-depth par | games | cells |")
    A("|---|---:|---:|---:|")
    for pw in PATHS:
        v, g, n = DONOR[pw]
        A("| `%s` | %.2f | %s | %d |" % (pw, v, format(round(g), ','), n))
    A("| **ALL POOL** | **%.2f** | %s | %d |\n" % (DONOR_ALL[0], format(round(DONOR_ALL[1]), ','), DONOR_ALL[2]))
    A("## 4. THE PAR TABLE — every cell, with its n and its shrink disclosed\n")
    A("| pathway | d | cells `n` | games | own par | donor | w = n/(n+%g) | **WIRED** | shrink | thin? |" % K)
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in ROWS:
        A("| `%s` | %d | %d | %s | %s | %.2f | %.4f | **%.2f** | %s | %s |"
          % (r['pathway'], r['d'], r['n'], format(r['games'], ','),
             ('%.2f' % r['own']) if r['own'] is not None else '_empty_', r['donor'], r['w'], r['wired'],
             ('%+.2f (%+.2f%%)' % (r['shrink_pts'], r['shrink_pct'])) if r['shrink_pts'] is not None else '—',
             ('**THIN** — n<10, donor carries the majority' if r['n'] < 10 else
              ('shrink ≥ 2%' if r['shrink_pct'] is not None and abs(r['shrink_pct']) >= 2.0 else ''))))
    A("")
    A("**Every cell in this table is shrunk** — that is the rule, applied uniformly. The `shrink`")
    A("column is the size of the move in points and per cent, so a reader can see exactly where the")
    A("donor is doing the work. Cells flagged **THIN** carry `n < 10`, where the donor holds the")
    A("majority weight; cells flagged `shrink ≥ 2%` are the ones where the pooling materially moved")
    A("the number even though the cell was not thin.\n")
    A("## 5. Monotonicity in depth — reported, never projected\n")
    A("Par is a measurement, not a shape: **no isotonic projection is applied**, and a non-monotone")
    A("step is reported as measured.\n")
    A("| pathway | d1 | d2 | d3 | d4 | d5 | d6 | steps |")
    A("|---|---:|---:|---:|---:|---:|---:|---|")
    for pw in PATHS + ['ALL POOL']:
        v = PAR[pw]
        st = " ".join(('↑' if v[i + 1] > v[i] else '↓') for i in range(5))
        A("| `%s` | %s | %s |" % (pw, " | ".join("%.2f" % x for x in v), st))
    A("")
    A("## 6. Reconciliation with the supervising seat's reference points\n")
    A("The seat computed four cells from the store (md5 `d9a24282`, complete-window ≤2021,")
    A("`d = Y − draftyr`). The conventions are not identical — the seat's quick cut against this")
    A("order's harvest gate — so the order asks for reconciliation, not agreement.\n")
    A("| pathway | d | seat par | my own par | my **wired** par | gap (own) | gap (wired) | seat `n` | my cells | my games |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in RECON:
        A("| `%s` | %d | %.1f | %.2f | **%.2f** | %+.2f%% | %+.2f%% | %s | %d | %s |"
          % (r['pathway'], r['d'], r['seat_par'], r['own'], r['wired'], r['gap_own_pct'],
             r['gap_wired_pct'], format(r['seat_n'], ','), r['my_cells'], format(r['my_games'], ',')))
    A("")
    open(OUTMD, 'w').write("\n".join(L) + "\n")
    P("  wrote %s" % OUTMD)
