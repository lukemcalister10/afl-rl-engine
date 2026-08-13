#!/usr/bin/env python3
"""ORDER 29 (T4) -- THE OWNER-FACING NO-ARB TABLES, IN THE ORDER 25 `NOARB_REVIEW` LAYOUT.

Composes NOARB_MARGINS_29.md and NOARB_MARGINS_29.json from instrument output ONLY. It computes no
price and re-derives nothing: every number below is lifted from a file some instrument wrote.

  live cohort readings   allarm_O29LIVE.json / table_O29LIVE.json  (the two canonical instruments on
                         per_entrant_O25R4.json, the matrix behind the LIVE board 88ce647f)
  landed cohort readings  ** HALTED ** -- both instruments refuse the landed matrix on their store /
                         surface / population pins. NOARB_LANDED_HALT.txt, NOARB_BASIS_out.txt.
  landed pathway readings INSTRUMENTS29.json (mark-path + reverse no-arb, which carry no store pin
                         and DID run on the landed board)
  landed identity gate    GATE29.json

The landed column is left EMPTY AND LABELLED rather than filled from a near-enough instrument. A
number carried across from a different construction, or from the live basis, would read as a landed
result and it is not one.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
N = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o22/noarb/'
CHARGE = 0.14

AL = json.load(open(N + 'allarm_O29LIVE.json'))
TB = json.load(open(N + 'table_O29LIVE.json'))
INS = json.load(open(os.path.join(HERE, 'INSTRUMENTS29.json')))
GAT = json.load(open(os.path.join(HERE, 'GATE29.json')))
RAW = json.load(open(os.path.join(HERE, 'NOARB_MARGINS_29.json'))) \
    if os.path.exists(os.path.join(HERE, 'NOARB_MARGINS_29.json')) else {}

HALT = dict(
    status='HALTED -- both cohort instruments refuse the landed matrix on their identity pins',
    matrix='per_entrant_O29FINAL.json 814df6917961db122af2571a0f65bbb9',
    matrix_basis=dict(store='cb38ef11', engine_head='e5109864', v0surf='4405cba2b42fb96f50496ec791cb806c',
                      n_records=2648, nd_teaching=1200),
    blocking_pins=[
        dict(file='harness_pvc_REPINNED_pass3.py', line=327, via='noarb_table_338.py',
             name='EXPECT_STORE', holds='d9a24282', landed='cb38ef11'),
        dict(file='harness_pvc_REPINNED_pass3.py', line=255, via='noarb_table_338.py',
             name='EXPECT_V0SURF', holds='6ef67f07db98', landed='4405cba2b42f'),
        dict(file='harness_pvc_REPINNED_pass3.py', line=257, via='noarb_table_338.py',
             name='EXPECT_N', holds=1197, landed=1200),
        dict(file='noarb_table_allarm.py', line=50, via='itself',
             name='store_md5 inline', holds='d9a24282', landed='cb38ef11'),
        dict(file='noarb_table_allarm.py', line=51, via='itself',
             name='v0surf_sig inline', holds='6ef67f07db98', landed='4405cba2b42f'),
    ],
    noarb_table_338_itself='UNMODIFIED and carries NO pin: md5 0f8220351c64c56ccfa90c60edcdfa5f',
    arbitrages_opened_on_landed_basis=None,
    note='No reading was taken on the landed basis, so no arbitrage was opened and none is claimed.')

rows = lambda g: {int(r['N']): r['ratio_meanN_over_mean0'] for r in g['rows']}
L = []
W = L.append


def f(x, w=6):
    return ('%.4f' % x) if isinstance(x, float) and x == x else ('n/a\\*' if w else 'n/a')


W("# NO-ARBITRAGE TABLES — THE **FINAL LANDED BOARD** (ORDER 29, PR #510, board `86c8d5d9`)")
W("")
W("Companion to `docs/evidence/pool_landing_v2_2026-08-12` / the ORDER 25 `NOARB_REVIEW`, in the same")
W("layout so the owner can read landed against live side by side.")
W("A NEGATIVE margin against the 14% annual charge is an arbitrage.")
W("")
W("> ## READ THIS FIRST — THE DECIDING LANDED READING DID NOT RUN")
W("> The as-of matrix **was** regenerated under the landed engine — that is the expensive half and it")
W("> is done (`per_entrant_O29FINAL.json`, 2648 records, 3m14s). **Both cohort instruments then")
W("> refused to read it**, on their own store / surface / population pins. Nothing was tuned to get a")
W("> number: the halt is transcribed verbatim in `NOARB_LANDED_HALT.txt` and the five blocking")
W("> literals are measured in `NOARB_BASIS_out.txt`.")
W("> ")
W("> **So sections 1–3 below carry the LIVE board's numbers with the landed column marked HALTED.**")
W("> Section 4 carries the landed readings that *did* run — the pathway-grain instruments and the")
W("> identity gate, neither of which pins the store.")
W("")
W("---")
W("")
W("## 0. WHAT BLOCKS THE LANDED READING, AND WHAT IT WOULD TAKE")
W("")
W("| file | name | holds | landed matrix carries |")
W("|---|---|---|---|")
for p in HALT['blocking_pins']:
    W("| `%s` | `%s` | `%s` | `%s` |" % (p['file'], p['name'], p['holds'], p['landed']))
W("")
W("`noarb_table_338.py` **itself carries no pin and needs no edit** — md5 `0f8220351c64c56ccfa90c60edcdfa5f`,")
W("verified unmoved at run. It delegates to the harness; `noarb_table_allarm.py` asserts *its* md5.")
W("")
W("`EXPECT_N` moves **1197 → 1200**, and the +3 are named: **`adam-treloar`, `dylan-shiel`,")
W("`jeremy-cameron`** — the ORDER 29 unflag-three (lever 1), which stop being `_pvc_exclude` and")
W("therefore start teaching the curve. Nothing else entered the teaching population and nothing left.")
W("")
W("**The control that makes this diagnostic:** the same invocation, same instrument copies, on the")
W("live matrix reproduced `NOARB_MARGINS_V2` **to the last digit**. The pipeline is sound; the pin is")
W("the blocker. The harness is named `harness_pvc_REPINNED_pass3.py` and its header is a log of")
W("prior declared re-points — so the fix is precedented and small, but it re-points the instrument")
W("that *defines the basis of the no-arb reading*, and this seat was authorised exactly one re-point")
W("(the identity gate's). It is the owner's call, and it is now a two-minute call.")
W("")
W("---")
W("")
W("## 1. OVERALL — the all-arm deciding instrument (ND + every pool pathway, one cohort)")
W("")
W("| window | n | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |")
W("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
J1 = []
for wname, g in AL['groups'].items():
    if 'rows' not in g or wname.startswith('self_check'):
        continue
    y = rows(g)
    a = y[1] / y[0] - 1.0
    m = CHARGE - a
    lbl = wname.replace('cohorts ', '').replace('  ', ' ').strip()
    W("| %s **(LIVE `88ce647f`)** | %d | %s | %s | %s | %s | %s | %s | %s | %s | %+.2f%% | **%+.2f%%** | %s |"
      % (lbl, g['n'], f(y.get(0)), f(y.get(1)), f(y.get(2)), f(y.get(3)), f(y.get(4)),
         f(y.get(5)), f(y.get(6)), f(y.get(7)), 100 * a, 100 * m, 'no arb' if m >= 0 else '**ARB**'))
    J1.append(dict(window=lbl, basis='LIVE 88ce647f', n=g['n'],
                   yr={str(k): y[k] for k in sorted(y)}, apprec=a, margin=m, arb=bool(m < 0)))
    W("| %s **(LANDED `86c8d5d9`)** | — | — | — | — | — | — | — | — | — | — | **HALTED** | pin |"
      % lbl)
W("")
W("## 2. ND ONLY (picks 1–64) — the legacy retained instrument, `noarb_table_338.py` UNMODIFIED")
W("")
W("| group | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |")
W("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
J2 = []
for gname, G in TB['groups'].items():
    if not isinstance(G, dict) or 'rows' not in G:
        continue
    y = rows(G)
    if 0 not in y or 1 not in y:
        continue
    a = y[1] / y[0] - 1.0
    m = CHARGE - a
    W("| %s **(LIVE)** | %s | %s | %s | %s | %s | %s | %s | %s | %+.2f%% | **%+.2f%%** | %s |"
      % (gname, f(y.get(0)), f(y.get(1)), f(y.get(2)), f(y.get(3)), f(y.get(4)), f(y.get(5)),
         f(y.get(6)), f(y.get(7)), 100 * a, 100 * m, 'no arb' if m >= 0 else '**ARB**'))
    J2.append(dict(group=gname, basis='LIVE 88ce647f', yr={str(k): y[k] for k in sorted(y)},
                   apprec=a, margin=m, arb=bool(m < 0)))
    W("| %s **(LANDED)** | — | — | — | — | — | — | — | — | — | **HALTED** | pin |" % gname)
W("")
W("## 3. BY ARM — ND vs each pool pathway (all-arm construction, pooled ratio within the arm)")
W("")
J3 = {}
for wname, g in AL['groups'].items():
    if 'by_arm' not in g or wname.startswith('self_check'):
        continue
    lbl = wname.replace('cohorts ', '').replace('  ', ' ').strip()
    W("**%s — LIVE `88ce647f`.  LANDED: HALTED on the same pins.**" % lbl)
    W("")
    W("| arm | n | yr1 | yr4 |")
    W("|---|---:|---:|---:|")
    J3[lbl] = {}
    for arm, d in sorted(g['by_arm'].items(), key=lambda kv: -kv[1]['n']):
        y1 = d.get('yr1'); y4 = d.get('yr4')
        W("| %s | %d | %s | %s |" % (arm, d['n'],
                                     f(y1) if (isinstance(y1, float) and y1 == y1) else 'n/a\\*',
                                     f(y4) if (isinstance(y4, float) and y4 == y4) else 'n/a\\*'))
        J3[lbl][arm] = dict(n=d['n'], yr1=y1 if (isinstance(y1, float) and y1 == y1) else None,
                            yr4=y4 if (isinstance(y4, float) and y4 == y4) else None)
    W("")
W("\\* the disclosed MSD debut-year gap: the mid-season draft begins 2019 and its cohort year 1")
W("precedes the emitted window for part of the population; those rows are EXCLUDED from that year,")
W("never scored zero.")
W("")
W("---")
W("")
W("## 4. WHAT **DID** RUN ON THE LANDED BOARD")
W("")
W("These instruments carry no store pin, so the landing did not lock them out. Both are committed")
W("pre-statements, re-read on the landed basis with no predicate touched.")
W("")
W("### 4.1 By arm, on the landed board — the mark-path construction (`INSTRUMENTS29`)")
W("")
W("**This is NOT section 3's number and must not be read as a landed version of it.** Section 3's")
W("`yr1`/`yr4` are *as-of price in cohort year N ÷ mean year-0 price* over the arm. The table below is")
W("`m_allin(d)` = *sum of marks at depth d ÷ sum of derived day-0*, the pre-stated mark-path")
W("progression. Different denominator, different question — but it is a genuine **landed** pathway")
W("reading, and it is the only by-arm number in this document that is one.")
W("")
W("| arm | n | d0 | d1 | d4 | peak | at d | verdict | reverse no-arb |")
W("|---|---:|---:|---:|---:|---:|---:|---|---|")
PROG = INS['progression']; NO = INS['noarb']
J4 = {}
for arm in PROG:
    ma = {int(k): v for k, v in PROG[arm]['m_allin'].items()}
    nn = {int(k): v for k, v in PROG[arm]['n'].items()}
    nb = NO.get(arm, {})
    W("| %s | %d | %s | %s | %s | %.4f | d%s | %s | %s |"
      % (arm, nb.get('n', 0), f(ma.get(0)), f(ma.get(1)), f(ma.get(4)),
         PROG[arm]['peak'], PROG[arm]['peak_d'],
         'PASS' if PROG[arm]['ok'] else '**FAIL**',
         '**FAIL**' if nb.get('fail') else 'PASS'))
    J4[arm] = dict(n=nb.get('n'), m_allin={str(k): ma[k] for k in sorted(ma)},
                   peak=PROG[arm]['peak'], peak_d=PROG[arm]['peak_d'], progression_ok=PROG[arm]['ok'],
                   reverse_noarb_fail=nb.get('fail'), max_m=nb.get('max_m'),
                   boot_upper=nb.get('boot_upper'))
W("")
W("**Mark-path progression: %d of %d arms PASS. Reverse no-arb: %d of %d arms PASS, %d pathways fail.**"
  % (sum(1 for a in PROG if PROG[a]['ok']), len(PROG),
     sum(1 for a in NO if not NO[a]['fail']), len(NO), len(INS['noarb_any_fail'])))
_mn = min(NO, key=lambda a: NO[a]['max_m'])
W("Smallest `max m(d≥1)` across arms is **%.4f** (%s) — %.0f%% above the failure line."
  % (NO[_mn]['max_m'], _mn, 100 * (NO[_mn]['max_m'] - 1)))
W("")
W("### 4.2 The identity gate (P16), on the landed board")
W("")
bw = GAT['board_wide']
ip = [abs(r['mine'] / r['price6'] - 1) for r in bw if r['price6']]
W("| reading | result |")
W("|---|---|")
W("| price-function identity, panel | **%d of %d PASS**, max &#124;mine/price6 − 1&#124; = **0.000e+00** |"
  % (GAT['identity_pass'], GAT['gate_n']))
W("| price-function identity, board-wide | **%d of %d within 1e−6 (100.0%%)**, max **%.3e**, over %d active rows |"
  % (sum(1 for x in ip if x <= 1e-6), len(ip), max(ip), len(bw)))
W("| pins re-asserted at exit | store `cb38ef11` · board `86c8d5d9` — **unmoved** |")
W("")
W("---")
W("")
W("## 5. THE DELTA — WHAT MOVED vs THE LIVE BOARD'S TABLES")
W("")
W("The pool day-0 re-derivation was the point of this landing, so the question the owner will ask is")
W("**did the pool yr0→yr1 cliffs close** — the live RD 0.4379, UNR 0.2052, PDN 0.1522, PDS 0.1329,")
W("IRE 0.2276 of section 3.")
W("")
W("**That question cannot be answered from this document, and the reason is section 0, not the board.**")
W("The instrument that measures those cliffs is the one that refused the landed matrix. Section 4.1's")
W("landed by-arm numbers are a *different construction* and do not answer it — quoting them as though")
W("they did would be the exact substitution this packet has refused everywhere else.")
W("")
W("What **is** measured, landed against live, on identical constructions:")
W("")
W("| reading | live | landed | source |")
W("|---|---|---|---|")
W("| mark-path progression | 10 of 10 PASS (ORDER 28 *candidate* basis, off-dial marks) | **10 of 10 PASS** (landed board, landed marks) | `INSTRUMENTS29` vs `INSTRUMENTS28` |")
W("| reverse no-arb | 10 of 10 PASS (same caveat) | **10 of 10 PASS**, 0 pathways fail | `INSTRUMENTS29` |")
W("| price-function identity, board-wide | 800 of 800, 0.000e+00 | **800 of 800, 0.000e+00** | `GATE29` vs `GATE28` |")
dd = INS['dial_delta']
sh = [dd[a][d] for a in dd for d in ('0', '1') if dd[a][d] is not None and dd[a][d] == dd[a][d]]
dp = [dd[a][d] for a in dd for d in ('2', '3', '4', '5', '6')
      if dd[a][d] is not None and dd[a][d] == dd[a][d]]
W("| marks, landed − live (same denominator) | — | shallow **%+.4f**, deep **%+.4f** | `INSTRUMENTS29` §3 |"
  % (sum(sh) / len(sh), sum(dp) / len(dp)))
W("")
W("**One delta is a correction to a delivered packet.** ORDER 28 could not measure the dial's effect")
W("on the marks, so it predicted the direction — *higher at shallow depths, unchanged deeper* — and")
W("used it to argue its own progressions were **conservative**. Re-emitted under the landed engine,")
W("the marks are **lower at essentially every arm and every depth, and they fall further deep than")
W("shallow** (%+.4f vs %+.4f) — the opposite shape, consistent with a board that fell 6.17%% under the"
  % (sum(sh) / len(sh), sum(dp) / len(dp)))
W("numéraire re-pin. ORDER 28's read was **optimistic, not conservative**. Neither verdict in section")
W("4.1 depends on that assumption — both instruments are run on the landed marks directly — but")
W("ORDER 28's reported margin was defended by a claim that has now been measured and did not hold.")
W("")
W("---")
W("")
W("### Provenance")
W("")
W("| file | what |")
W("|---|---|")
W("| `emit_variant_o29.sh` | the as-of matrix, re-emitted on the landed tree (the expensive half, done) |")
W("| `run_noarb_o29.sh` · `NOARB_MARGINS_29_out.txt` | both cohort instruments, live basis + the landed attempt |")
W("| `NOARB_LANDED_HALT.txt` | the two refusals, verbatim, with instrument md5s computed at run |")
W("| `o29_noarb_basis.py` · `NOARB_BASIS_out.txt` | the five blocking literals, measured |")
W("| `o29_instruments.py` · `INSTRUMENTS29.{json,txt}` | mark-path + reverse no-arb, ON the landed board |")
W("| `o29_gate.py` · `GATE29.{json,txt}` · `GATE29_REPOINT.diff` | the identity gate, re-pointed and run |")

open(os.path.join(HERE, 'NOARB_MARGINS_29.md'), 'w').write("\n".join(L) + "\n")
json.dump(dict(
    charge=CHARGE,
    board=dict(landed='86c8d5d9ba5b95e2cba05c78fbc31f78', live='88ce647f531030d8d2e094188b258191'),
    instrument_md5=dict(noarb_table_338='0f8220351c64c56ccfa90c60edcdfa5f',
                        noarb_table_allarm=AL['canonical_instrument_md5']),
    section1_overall_live=J1, section2_nd_live=J2, section3_by_arm_live=J3,
    section4_landed_markpath=J4,
    section4_landed_gate=dict(panel_pass=GAT['identity_pass'], panel_n=GAT['gate_n'],
                              board_wide_within_1e6=sum(1 for x in ip if x <= 1e-6),
                              board_wide_n=len(ip), board_wide_max=max(ip), rows=len(bw)),
    landed_cohort_reading=HALT,
    dial_delta=dict(shallow_mean=sum(sh) / len(sh), deep_mean=sum(dp) / len(dp), by_arm=dd),
    margins_instrument_output=RAW),
    open(os.path.join(HERE, 'NOARB_MARGINS_29.json'), 'w'), indent=1, sort_keys=True, default=float)
print("wrote NOARB_MARGINS_29.md / NOARB_MARGINS_29.json")
