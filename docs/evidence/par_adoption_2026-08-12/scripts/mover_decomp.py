"""ORDER 20B TASK 4/5 — PER-MOVER CHANNEL DECOMPOSITION.

Reads the channel_harness.py sweep (ALL_HEAD, ALL_FIX, one-channel-FIX, and leave-one-out) and reports,
for each named mover, how much of his price delta each par consumer carries.

TWO ATTRIBUTIONS ARE REPORTED, DELIBERATELY, AND THEY DO NOT AGREE:

  ONE-AT-A-TIME (from HEAD)   delta_c = v(only c on FIX) - v(ALL_HEAD)
  LEAVE-ONE-OUT (from FIX)    delta_c = v(ALL_FIX)      - v(all but c on FIX)

If the channels were additive and independent these would be equal and each would sum to the total.
They are not: the par surface enters `ev()` through terms that multiply and clamp each other. The gap
between the two attributions IS the interaction, and it is reported as a residual rather than hidden by
picking whichever decomposition looks tidier.

Run: python3 mover_decomp.py <scratchpad_dir> <out_prefix>
"""
import json, os, sys, collections

SP = sys.argv[1].rstrip('/') + '/'
PRE = sys.argv[2]
CH = ['ISO', 'POLE', 'BLEND', 'BAR', 'BASE', 'LVLPAR']

NAMED = ['Harry Dean', 'Angus Clarke', 'Harvey Johnston', 'James Leake', 'Willem Duursma',
         'Will Hayes', 'Luke Cleary']     # the order's five + the two remaining >15% national movers


def load(tag):
    f = SP + 'chan_%s.json' % tag
    if not os.path.exists(f): return None
    d = json.load(open(f))
    return {'meta': d['meta'], 'by': {r['name']: r for r in d['rows']}, 'rows': d['rows']}


BASE = load('ALL_HEAD'); FULL = load('ALL_FIX')
ONLY = {c: load('only_%s' % c) for c in CH}
WO = {c: load('wo_%s' % c) for c in CH}
P = print
OUT = {}

P("=" * 122)
P("ORDER 20B TASK 4 — PER-MOVER PAR-CHANNEL DECOMPOSITION")
P("  population for the control totals: the 1002 rows the board carries (active+back)")
P("=" * 122)

# ---------------------------------------------------------------- CONTROL 3: the two ends reproduce
missing = [t for t, d in [('ALL_HEAD', BASE), ('ALL_FIX', FULL)] + [('only_%s' % c, ONLY[c]) for c in CH]
           + [('wo_%s' % c, WO[c]) for c in CH] if d is None]
if missing: P("  MISSING CONFIGS: %s" % missing)


def natl(r): return r['ty'] == 'ND' and (r['ep'] or 99) <= 64


def totals(d):
    n = [r for r in d['rows'] if natl(r) and r.get('v') is not None]
    p = [r for r in d['rows'] if not natl(r) and r.get('v') is not None]
    return sum(r['v'] for r in n), sum(r['v'] for r in p), n, p


P()
P("  ---- CONTROL 3: does each config reproduce its expected board totals? ----")
tn0, tp0, _, _ = totals(BASE); tn1, tp1, _, _ = totals(FULL)
P("    ALL_HEAD  national %d  pool %d      (ORDER 20 BOARD_DELTA before: 624418 / 123939)" % (tn0, tp0))
P("    ALL_FIX   national %d  pool %d      (ORDER 20 BOARD_DELTA after:  622650 / 126244)" % (tn1, tp1))
OUT['control3'] = {'ALL_HEAD': [tn0, tp0], 'ALL_FIX': [tn1, tp1]}

P()
P("  ---- WHOLE-BOARD national delta carried by each channel ----")
P("    %-8s %14s %14s %14s %14s" % ('channel', 'one-at-a-time', 'share of total', 'leave-one-out', 'share of total'))
tot = tn1 - tn0
OUT['board_by_channel'] = {}
for c in CH:
    o = (totals(ONLY[c])[0] - tn0) if ONLY[c] else None
    w = (tn1 - totals(WO[c])[0]) if WO[c] else None
    OUT['board_by_channel'][c] = {'one_at_a_time': o, 'leave_one_out': w}
    P("    %-8s %14s %14s %14s %14s" % (
        c, ('%+d' % o) if o is not None else '--', ('%+.1f%%' % (100.0 * o / tot)) if o is not None and tot else '--',
        ('%+d' % w) if w is not None else '--', ('%+.1f%%' % (100.0 * w / tot)) if w is not None and tot else '--'))
so = sum(v['one_at_a_time'] or 0 for v in OUT['board_by_channel'].values())
sw = sum(v['leave_one_out'] or 0 for v in OUT['board_by_channel'].values())
P("    %-8s %14d %14s %14d" % ('SUM', so, '', sw))
P("    %-8s %14d   <- TOTAL national delta (ALL_FIX - ALL_HEAD)" % ('ACTUAL', tot))
P("    one-at-a-time residual %+d   leave-one-out residual %+d   (interaction; channels are NOT additive)"
  % (tot - so, tot - sw))
OUT['board_total'] = tot; OUT['residual_oaat'] = tot - so; OUT['residual_loo'] = tot - sw

# ---------------------------------------------------------------- per mover
P()
P("=" * 122)
P("PER-MOVER DECOMPOSITION")
P("=" * 122)
OUT['movers'] = {}
for nm in NAMED:
    if nm not in BASE['by']:
        P("  %s — NOT ON THE BOARD" % nm); continue
    b = BASE['by'][nm]; f = FULL['by'][nm]
    tot_m = f['v'] - b['v']
    P()
    P("  %s   %s  pick %s (eff %s)   %d -> %d   (%+d, %+.2f%%)"
      % (nm, b['pos'], b['pk'], b['ep'], b['v'], f['v'], tot_m, 100.0 * tot_m / max(1, b['v'])))
    P("    %-8s %16s %16s %16s %16s" % ('channel', 'one-at-a-time', 'share', 'leave-one-out', 'share'))
    rec = {'pos': b['pos'], 'pick': b['pk'], 'ep': b['ep'], 'before': b['v'], 'after': f['v'],
           'delta': tot_m, 'pct': 100.0 * tot_m / max(1, b['v']), 'channels': {}}
    for c in CH:
        o = (ONLY[c]['by'][nm]['v'] - b['v']) if ONLY[c] and nm in ONLY[c]['by'] else None
        w = (f['v'] - WO[c]['by'][nm]['v']) if WO[c] and nm in WO[c]['by'] else None
        rec['channels'][c] = {'one_at_a_time': o, 'leave_one_out': w}
        P("    %-8s %16s %16s %16s %16s" % (
            c, ('%+d' % o) if o is not None else '--',
            ('%+.1f%%' % (100.0 * o / tot_m)) if (o is not None and tot_m) else '--',
            ('%+d' % w) if w is not None else '--',
            ('%+.1f%%' % (100.0 * w / tot_m)) if (w is not None and tot_m) else '--'))
    so = sum((rec['channels'][c]['one_at_a_time'] or 0) for c in CH)
    sw = sum((rec['channels'][c]['leave_one_out'] or 0) for c in CH)
    rec['sum_oaat'] = so; rec['sum_loo'] = sw
    rec['residual_oaat'] = tot_m - so; rec['residual_loo'] = tot_m - sw
    P("    %-8s %16d %16s %16d" % ('SUM', so, '', sw))
    P("    %-8s %16d  <- his actual delta;  residual oaat %+d (%.0f%% of delta), loo %+d"
      % ('ACTUAL', tot_m, tot_m - so, (100.0 * abs(tot_m - so) / abs(tot_m)) if tot_m else 0, tot_m - sw))
    OUT['movers'][nm] = rec

json.dump(OUT, open(PRE + '.json', 'w'), indent=1)
P()
P("  json -> %s.json" % PRE)
