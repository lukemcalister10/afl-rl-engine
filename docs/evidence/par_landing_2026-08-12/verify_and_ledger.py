"""ORDER 20C — verify my rebuilt delta against ORDER 20's committed record, then emit the movers ledger.

  python3 verify_and_ledger.py <CONTROL.json> <FIX.json> <O20_BOARD_DELTA.json> <CHANNEL_DECOMP.json> <outdir>

Arm predicate and row keying are ORDER 20's board_delta.py, verbatim, so the two are comparable.
"""
import json, sys, collections, os

CTRL, FIX, O20, CHAN, OUT = sys.argv[1:6]
A = json.load(open(CTRL)); B = json.load(open(FIX))
REF = json.load(open(O20)); CH = json.load(open(CHAN))


def is_national(r):
    return r.get('ty') == 'ND' and (r.get('ep') or 99) <= 64


def rows(bd):
    o = {}
    for s in ('active', 'back'):
        for r in bd.get(s) or []:
            o[(s, r.get('key') or r.get('name'))] = r
    return o


RA, RB = rows(A), rows(B)
report = []
P = report.append

P("=" * 108)
P("ORDER 20C — MOVERS LEDGER BUILD + VERIFICATION AGAINST ORDER 20's COMMITTED BOARD_DELTA")
P("=" * 108)

ARMS = {}
for armname, pred in (('NATIONAL', is_national), ('POOL', lambda r: not is_national(r))):
    sub = [k for k in RA if k in RB and pred(RA[k]) and RA[k].get('v') is not None]
    mv = [(k, RA[k]['v'], RB[k]['v']) for k in sub if RA[k]['v'] != RB[k]['v']]
    tot_a = sum(RA[k]['v'] for k in sub); tot_b = sum(RB[k]['v'] for k in sub)
    ARMS[armname] = dict(sub=sub, mv=mv, tot_a=tot_a, tot_b=tot_b)

    r = REF[armname]
    checks = [('n', len(sub), r['n']), ('movers', len(mv), r['movers']),
              ('total_before', tot_a, r['total_before']), ('total_after', tot_b, r['total_after']),
              ('delta', tot_b - tot_a, r['delta'])]
    P("")
    P("  %s" % armname)
    for label, got, exp in checks:
        P("    %-14s mine=%-10s ORDER20=%-10s  %s" % (label, got, exp, "MATCH" if got == exp else "*** MISMATCH ***"))

    # every one of ORDER 20's 40 named top movers must reproduce to the unit
    mine = {}
    for k, x, y in mv:
        mine.setdefault(RA[k].get('name') or k[1], []).append((x, y))
    bad = []
    for t in r['top']:
        got = mine.get(t['name'])
        if not got:
            bad.append((t['name'], 'ABSENT from my mover set', t))
        elif not any(x == t['before'] and y == t['after'] for x, y in got):
            bad.append((t['name'], 'value mismatch %s' % got, t))
    P("    top-40 named movers reproduce to the unit: %s" % ("ALL 40 MATCH" if not bad else "*** %d MISMATCH ***" % len(bad)))
    for n, why, t in bad:
        P("      *** %-28s %s   (ORDER20 %s -> %s)" % (n, why, t['before'], t['after']))

# ---------------------------------------------------------------- the ledger
CHANNELS = ('ISO', 'POLE', 'BLEND', 'BAR', 'BASE', 'LVLPAR')
led = {'lever': 'par separation fix (arm split) — PR #457, build/nd-pool-separation 78d5c38',
       'order': 'ORDER 20C — the adoption landing (owner ruling, issue #334 comment 5261191193)',
       'board_before': '94f1fec59f99c59d5890d5975c79fa9b',
       'board_after': '1dbd1480a34c7823f330273211cbb76a',
       'arm_predicate': "NATIONAL = (ty=='ND' and ep<=64); POOL = everything else (ORDER 20 board_delta.py)",
       'channel_decomposition_source': 'ORDER 20B docs/evidence/par_adoption_2026-08-12/movers/CHANNEL_DECOMP.json',
       'arms': {}}

for armname in ('NATIONAL', 'POOL'):
    a = ARMS[armname]
    ent = []
    for k, x, y in sorted(a['mv'], key=lambda t: -abs(t[2] - t[1])):
        r = RA[k]
        name = r.get('name') or k[1]
        e = {'key': k[1], 'section': k[0], 'name': name, 'ty': r.get('ty'), 'pk': r.get('pk'),
             'ep': r.get('ep'), 'club': r.get('club'), 'pos': r.get('pos'),
             'before': x, 'after': y, 'delta': y - x,
             'pct': round(100.0 * (y - x) / max(1, x), 4)}
        if name in CH['movers']:
            c = CH['movers'][name]
            e['channels'] = {ch: c['channels'][ch] for ch in CHANNELS if ch in c['channels']}
            e['channel_residual'] = {'one_at_a_time': c['residual_oaat'], 'leave_one_out': c['residual_loo']}
        ent.append(e)
    led['arms'][armname] = {'n': len(a['sub']), 'movers': len(a['mv']),
                            'total_before': a['tot_a'], 'total_after': a['tot_b'],
                            'delta': a['tot_b'] - a['tot_a'],
                            'pct': round(100.0 * (a['tot_b'] - a['tot_a']) / max(1, a['tot_a']), 6),
                            'rows': ent}

led['board_by_channel'] = CH['board_by_channel']
led['board_channel_residual'] = {'one_at_a_time': CH['residual_oaat'], 'leave_one_out': CH['residual_loo']}
led['ledger_rows'] = sum(len(led['arms'][x]['rows']) for x in led['arms'])

# BASE must be exactly zero for every decomposed mover (20B's P14)
base_nonzero = [n for n, c in CH['movers'].items()
                if c['channels']['BASE']['one_at_a_time'] != 0 or c['channels']['BASE']['leave_one_out'] != 0]
P("")
P("  LEDGER: %d rows (%d national + %d pool)" % (led['ledger_rows'], len(led['arms']['NATIONAL']['rows']),
                                                 len(led['arms']['POOL']['rows'])))
P("  decomposed movers carried into the ledger: %d — %s"
  % (len(CH['movers']), ", ".join(sorted(CH['movers']))))
P("  BASE channel exactly 0.0 for every decomposed mover: %s"
  % ("TRUE (all 7)" if not base_nonzero else "*** FALSE: %s ***" % base_nonzero))
P("")

json.dump(led, open(os.path.join(OUT, 'PAR_FIX_MOVERS_2026-08-12.json'), 'w'), indent=1)
open(os.path.join(OUT, 'VERIFY.txt'), 'w').write("\n".join(report) + "\n")
print("\n".join(report))
