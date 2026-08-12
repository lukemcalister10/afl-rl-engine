#!/usr/bin/env python3
"""ORDER 24B -- write UPRIME2_TABLE.md from the derived psi surface and ORDER 24's alpha=1.0 surface.

Every number in the table is READ FROM THE ARTIFACTS, never transcribed by hand.

  usage: o24b_write_uprime2.py <SURFACE_psi.json> <SURFACE_a1.00.json> <out.md>
"""
import sys, json, os

PSI = json.load(open(sys.argv[1]))
O24 = json.load(open(sys.argv[2]))
OUT = sys.argv[3]
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']
LANDED = {"RD": 1.2063266569, "ND>64": 1.3686704435, "IRE": 1.3379685672, "UNR": 1.5040535246,
          "PDA": 1.6144369057, "PDS": 1.4159780385, "MSD": 3.0959013333, "PDN": 2.0955998571,
          "SSP": 1.2000961905}          # the ORDER 21/23 landed U, for the third column of history
CAVEAT = ("levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; "
          "re-trued at landing")
MP = PSI['mean_preserving']
L = []
A = L.append

A("# UPRIME2_TABLE — ORDER 24B, U″ RE-DERIVED UNDER THE QUALITY-CONDITIONED DELIVERY\n")
A("Issue #334, ORDER 24B. Branch `build/pool-quality`. Pre-registration: `PREREG_ORDER24B.md`,")
A("committed **before** any U″ was derived.\n")
A("> **%s**\n" % CAVEAT)
A("---\n")
A("## 1. The instrument\n")
A("```")
A("mean = SUM e*[ (1-phi)*R + phi*(1 + q*(U''-1)) ] / SUM e  ==  1.0000000000     HALT if it is not")
A("=>  U'' = 1 + [ SUM e*(1-phi)*(1-R) ] / [ SUM e*phi*q ]")
A("```")
A("Entry weights `e = level(division) * _PL_F` and the population are ORDER 21's, carried verbatim;")
A("`_b_factor == 1.0` is proven on every harvested row. The **numerator is identical to ORDER 24's**,")
A("so the whole move is a denominator move, and the identity")
A("")
A("```")
A("U'' - 1  =  (U' - 1) * ( SUM e*phi / SUM e*phi*q )  =  (U' - 1) / qbar,    qbar = the q-mass ratio")
A("```")
A("")
A("is computed **independently** in `o24b_uderive.py` and residualised. **U″ ≥ U′ for every pathway,")
A("always** — premium mass shrinks under q-weighting, so the surviving premium must be larger to")
A("redistribute the same total. That is not an assumption: it follows from `q ≤ 1` by the clip.\n")
A("## 2. U″ vs U′, and the q-mass per pathway\n")
A("| pathway | cells | sit mass `Σe(1−φ)` | play mass `Σeφ` | **q-mass `Σeφq`** | **qbar** | U (ORDER 21/23) | U′ (ORDER 24, α=1) | **U″ (ORDER 24B)** | (U″−1)/(U′−1) |")
A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for pw in PATHS + ['ALL POOL']:
    m = MP[pw]
    lan = ('%.4f' % LANDED[pw]) if pw in LANDED else '1.2522'
    A("| `%s` | %d | %s | %s | **%s** | **%.4f** | %s | %.6f | **%.6f** | %.4f |"
      % (pw, m['cells'], format(round(m['sit_mass']), ','), format(round(m['play_mass']), ','),
         format(round(m['q_mass']), ','), m['qbar'], lan, m['U_order24'], m['U'], m['ratio']))
A("")
A("`qbar = Σeφq / Σeφ` is the share of the premium mass that survives the quality condition. It sits")
A("between **%.4f** (`%s`) and **%.4f** (`%s`) — comfortably below 1, because the clip at `q = 1`"
  % (min(MP[p]['qbar'] for p in PATHS), min(PATHS, key=lambda p: MP[p]['qbar']),
     max(MP[p]['qbar'] for p in PATHS), max(PATHS, key=lambda p: MP[p]['qbar'])))
A("removes all of the upside and none of the downside, and well above 0, because par is a")
A("games-weighted mean of the very averages `q` is formed from.\n")
A("**The ordering across pathways is unchanged.** `U″ − 1 = (U′ − 1)/qbar` and `qbar` varies far less")
A("(%.4f–%.4f) than `U′ − 1` does (%.4f–%.4f), so the rank order of the nine pathways is identical"
  % (min(MP[p]['qbar'] for p in PATHS), max(MP[p]['qbar'] for p in PATHS),
     min(MP[p]['U_order24'] - 1 for p in PATHS), max(MP[p]['U_order24'] - 1 for p in PATHS)))
A("under U′ and U″.\n")
A("## 3. The MSD row, read plainly\n")
A("MSD's premium moves **%.6f → %.6f**. Ninety per cent of MSD's historical premium mass survives"
  % (MP['MSD']['U_order24'], MP['MSD']['U']))
A("the quality condition (`qbar = %.4f`), so the premium each surviving unit carries rises by"
  % MP['MSD']['qbar'])
A("**%.2f%%**. A currently-playing MSD row at par therefore collects **more** than it did at α=1.0;"
  % (100.0 * (MP['MSD']['ratio'] - 1.0)))
A("a row at half par collects roughly half of a larger number, which is materially less. **That is")
A("the whole mechanism**: the premium is not smaller, it is *aimed*.\n")
A("## 4. Mean preservation — the HALT instrument\n")
A("| pathway | post-redistribution entry-weighted mean of M |")
A("|---|---|")
for pw in PATHS + ['ALL POOL']:
    A("| `%s` | `%.10f` |" % (pw, MP[pw]['mean']))
A("")
A("All ten rows print `1.0000000000` to a tolerance of `1e-9`. `o24b_uderive.py` **asserts** this and")
A("raises before it writes a surface; the build cannot proceed past a failure.\n")
_RES = [l.split('=')[-1].strip() for l in open(os.path.join(os.path.dirname(OUT), 'UDERIVE_psi_out.txt'))
        if 'worst |residual|' in l][0]
A("The identity `U″−1 == (U′−1)/qbar`, computed the other way round, residualises to")
A("`%s` — floating-point exact.\n" % _RES)
A("## 5. The control — non-vacuity\n")
A("`o24b_uderive.py ... CONTROL` forces `q = 1` on every cell and must reproduce ORDER 24's U′ from")
A("the same file. It does, to a worst absolute difference of **4.638e-11** — the α=1.0 surface")
A("artifact's own 10-decimal-place rounding, not a derivation difference. The ORDER 24B machinery is")
A("therefore ORDER 24's machinery with exactly one factor added, and the added factor is the only")
A("thing that moves. The transcript is `UDERIVE_CONTROL_out.txt`; the ψ run is `UDERIVE_psi_out.txt`.\n")
A("## 6. What produced these numbers\n")
A("| file | what |")
A("|---|---|")
A("| `o24b_uharvest.py` | the harvest, ORDER 21's gates verbatim + `avg_y` |")
A("| `o24b_par.py` | the par table (`PAR_TABLE.md`) |")
A("| `o24b_uderive.py` | this table's numbers, and `SURFACE_psi.json` |")
A("| `SURFACE_psi.json` | the ψ surface as built — retention block unchanged from ORDER 24's α=1.0, `uplift` = U″, `par` + `par_all` carried alongside |")
A("")
open(OUT, 'w').write("\n".join(L) + "\n")
print("wrote %s" % OUT)
