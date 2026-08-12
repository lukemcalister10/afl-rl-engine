#!/usr/bin/env python3
"""ORDER 25 -- THE N43 LEVEL TABLE, WRITTEN OUT AS A STAGEABLE FILE FOR THE LEDGER'S LEVER 2.

The composed ledger decomposes LIVE -> LANDED into three consecutive boards, and the middle one --
"the psi retention/delivery machinery, WITHOUT the repricing" -- has to be built at the levels the
LIVE board actually priced at. Those are the 2026 N43 signed levels (#306 comment 5179992080), which
this branch superseded twice (ORDER 23, then ORDER 25). They are written here from the SUPERSEDED
history preserved inside pvc_curve_v2.json's own ruling blocks, never re-typed from memory.

THE ND65+ VALUE IS THE **EFFECTIVE** ONE, 185, AND THAT IS DELIBERATE. On the live board the signed
ND65+ level was 266.1 read through the cap `min(measured_k15, curve[64]=185)`, so 185 is the price
that pathway actually paid. ORDER 23 removed the cap and attributed the whole 185 -> 298 move to
lever 3 (verified against docs/ledgers/POOL_UPDATE_MOVERS_2026-08-12.json: aidan-johnson's
lever_repricing carries it). This file keeps that attribution intact by staging 185, so the cap
removal stays in the repricing lever where ORDER 23 put it, instead of leaking into lever 2 because
the landed engine no longer has a cap to apply.

  usage: o25_levels_n43.py <out_levels.json>
"""
import sys, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
OUT = sys.argv[1]

PL = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
CURVE = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['curve']
CAPPK = int(PL['signed_nd65_plus']['cap_against_curve_pick_REMOVED_2026_08_12'])
CAP = float(CURVE[str(CAPPK)])


def harvest(txt, keys):
    """pull `KEY 123.4` pairs out of a preserved-history sentence."""
    out = {}
    for k in keys:
        m = re.search(r'\b%s\s+([0-9]+(?:\.[0-9]+)?)' % re.escape(k), txt)
        assert m, "the superseded %s value is not in the preserved history" % k
        out[k] = float(m.group(1))
    return out


flat_txt = PL['_signed_flat_ruling_2026_08_12']
rd_txt = PL['_signed_rd_positional_ruling_2026_08_12']
tail_f = flat_txt[flat_txt.index('the 2026 N43 signature'):]
tail_r = rd_txt[rd_txt.index('SUPERSEDED BEFORE THAT -- N43'):]

FLAT = harvest(tail_f, ['MSD', 'SSP', 'PDA', 'PDS', 'IRE', 'PDN', 'UNR'])
RD = harvest(tail_r, ['KPD', 'MID', 'RUCK', 'SD', 'SF', 'KPF'])
ND65_SIGNED = 266.1
ND65_EFFECTIVE = min(ND65_SIGNED, CAP)

print("  THE N43 LEVELS, recovered from the preserved history in pvc_curve_v2.json:")
print("    flat  " + " · ".join("%s %.1f" % (k, FLAT[k]) for k in sorted(FLAT)))
print("    RD    " + " · ".join("%s %.1f" % (k, RD[k]) for k in sorted(RD)))
print("    ND65+ signed %.1f -> EFFECTIVE %.1f under the cap against curve[%d]=%g that was in force"
      % (ND65_SIGNED, ND65_EFFECTIVE, CAPPK, CAP))
print("          (staged as the effective value so the cap removal stays in the REPRICING lever,")
print("           exactly where ORDER 23's ledger put it)")

json.dump(dict(signed_flat=FLAT, signed_rd_positional=RD, nd65_measured_k15=ND65_EFFECTIVE,
               _what="the 2026 N43 signed levels, the ones the LIVE board 1dbd1480 priced at",
               _nd65_signed=ND65_SIGNED, _nd65_cap_pick=CAPPK, _nd65_cap_value=CAP),
          open(OUT, 'w'), indent=1)
print("  wrote %s" % OUT)
