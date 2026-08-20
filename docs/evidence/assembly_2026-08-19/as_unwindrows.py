#!/usr/bin/env python3
"""ASSEMBLY BUILD — D5: THE THREE RUN-BREAK RULES, SIDE BY SIDE ON THE NAMED ROWS.

BINARY (wired) · FRACTIONAL (priced v754) · UNWIND (the owner's shape, priced v755).

All three boards are built on ONE engine with the D4 ramp folded in, so the only thing that differs
between them is the break rule. The named rows are the ones the instruction asked about; they are
ILLUSTRATIONS OF A RULE, never targets of one — no row is fitted and no constant is chosen to make a
row come out a particular way.

NO ENGINE RUN. Pure reads over boards already built.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ASM = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm'
Y = 2026
U0 = 5.0
L = []


def P(s=''):
    print(s); L.append(str(s))


def board(tag):
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (ASM, tag)
    if not os.path.exists(p):
        return None, None
    return ({r['key']: r for r in json.load(open(p))['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


PRE, mPRE = board('V755_L5C')      # before R3 AND before the ramp — the v754 lever-stack board
# THE BASELINE THE R3 MARGINAL IS MEASURED AGAINST MUST CARRY THE RAMP, OR THE TWO EFFECTS ARE
# CONFLATED. `V755_L5C` has the ramp OFF, so PRE->CAND would count the ramp's 8 rows as R3's. The
# first draft of this file did exactly that and printed "17 rows" for a collector that charges 9.
# `V755_L5CR` is the same board WITH the ramp on and R3 still off, and it is the correct denominator.
RPRE, mRPRE = board('V755_L5CR')   # ramp ON, R3 OFF — the true R3 baseline
BIN0, mBIN0 = board('V755_BIN0')   # binary, NO ramp — the previous candidate
BIN, mBIN = board('V755_CAND')     # binary + ramp folded in — THE NEW CANDIDATE
FRA, mFRA = board('V755_FRAC')     # fractional + ramp
UNW, mUNW = board('V755_UNW')      # unwind U0=5 + ramp
IDP, mIDP = board('IDENT_P')
STORE = {x['key']: x for x in json.load(open(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')))}


def gnow(k):
    return sum(float(x.get('games') or 0.0)
               for x in (STORE.get(k, {}).get('scoring') or []) if int(x['year']) == Y)


def tot(B):
    return sum(r['v'] for r in B.values())


P('=' * 122)
P('D4 + D5 — THE RAMP FOLDED IN, AND THE THREE RUN-BREAK RULES SIDE BY SIDE')
P('=' * 122)
P()
P('  %-46s %10s %11s %13s %7s' % ('board', 'md5', 'total', 'R3 marginal', 'rows'))
for lab, B, m in (('before R3 at all', PRE, mPRE),
                  ('binary, NO ramp — the PREVIOUS candidate', BIN0, mBIN0),
                  ('*** binary + RAMP FOLDED IN = THE CANDIDATE ***', BIN, mBIN),
                  ('fractional + ramp (priced v754)', FRA, mFRA),
                  ('unwind U0=5 + ramp (priced v755, THE OWNER\'S SHAPE)', UNW, mUNW)):
    if B is None:
        P('  %-46s %10s  NOT BUILT' % (lab, '—')); continue
    n = sum(1 for k in PRE if PRE[k]['v'] != B[k]['v'])
    P('  %-46s %10s %11s %13s %7d'
      % (lab, m, '{:,}'.format(tot(B)), '{:+,}'.format(tot(B) - tot(PRE)) if B is not PRE else '—', n))
P()
P('  IDENTITIES:')
P('    every ORDER 41 dial OFF            -> %s  %s'
  % (mIDP, 'reproduces ORDER P 374d4e44 (D-A1 did not fire)' if mIDP == '374d4e44' else '*** NOT 374d4e44 ***'))
P('    the last pre-R3 lever board        -> %s  %s'
  % (mPRE, 'byte-identical to 1270991c — the edit cannot reach it (D-A7 did not fire)'
     if mPRE == '1270991c' else '*** MOVED — D-A7 FIRED ***'))
P()

# ---- WHAT FOLDING THE RAMP IN ACTUALLY COST --------------------------------------------------
P('=' * 122)
P('D4 — WHAT FOLDING THE RAMP IN COST, MEASURED RATHER THAN ASSUMED')
P('=' * 122)
d = [(BIN[k]['v'] - BIN0[k]['v'], k) for k in BIN0 if BIN[k]['v'] != BIN0[k]['v']]
d.sort(key=lambda x: -abs(x[0]))
P('  the ramp moves %d rows, %+d board points in total.' % (len(d), sum(x[0] for x in d)))
P('  %-30s %8s %10s %10s' % ('row', 'delta', 'before', 'after'))
for dv, k in d:
    P('  %-30s %+8d %10d %10d' % ((BIN0[k].get('name') or k)[:30], dv, BIN0[k]['v'], BIN[k]['v']))
P()
P('  The ramp is a DEPTH convention: it prorates the in-progress season\'s contribution to an absence')
P('  clock concavely (f**1.5) instead of linearly, so early-season absence counts for less and')
P('  late-season absence for more. It is the engine\'s OWN already-ruled shape, used at two existing')
P('  sites for exactly this question. It is deliberately NOT applied to the I1 credit, which is a')
P('  participation weight — the engine\'s own comment at the D12 site gives that reason and it stands.')
P()

# ---- THE NAMED ROWS ----------------------------------------------------------------------------
NAMES = ['Will Brodie', 'Toby Conway', 'Harry Barnett', 'Charlie Edwards', 'Nick Madden',
         'Noah Mraz', 'Jedd Busslinger', 'Taylor Goad', 'Dante Visentini', 'Vigo Visentini']
KEYS = {}
for k, r in PRE.items():
    nm = r.get('name')
    if nm in NAMES:
        KEYS.setdefault(nm, k)

P('=' * 122)
P('THE NAMED ROWS — BINARY (the candidate) vs UNWIND (the owner\'s shape). ILLUSTRATIONS, NOT TARGETS.')
P('=' * 122)
P('  u(g) = min(1, g/%g). A row with %g+ games this season is FULLY unwound and pays nothing.' % (U0, U0))
P()
P('  %-20s %6s %7s %9s %9s %9s   %s'
  % ('row', 'g 2026', 'u(g)', 'pre-R3', 'BINARY', 'UNWIND', 'what the unwind does'))
ROWS = []
for nm in NAMES:
    k = KEYS.get(nm)
    if not k:
        P('  %-20s  NOT ON THE BOARD' % nm[:20]); continue
    g = gnow(k)
    u = 0.0 if g <= 0 else min(1.0, g / U0)
    pv, bv, uv = PRE[k]['v'], BIN[k]['v'], (UNW[k]['v'] if UNW else None)
    if uv is None:
        continue
    if uv == pv and bv == pv:
        say = 'untouched by either rule'
    elif uv == pv and bv < pv:
        say = 'RESTORED — binary charged him, unwind does not'
    elif uv < pv and bv == pv:
        say = '*** STRIPPED — binary shielded him, unwind charges %d ***' % (pv - uv)
    elif uv < bv:
        say = 'charged HARDER than binary by %d' % (bv - uv)
    elif uv > bv:
        say = 'charged LESS than binary by %d' % (uv - bv)
    else:
        say = 'identical under both'
    ROWS.append((nm, g, u, pv, bv, uv, say))
    P('  %-20s %6.0f %7.3f %9d %9d %9d   %s' % (nm[:20], g, u, pv, bv, uv, say))
P()

# ---- THE WHOLE-BOARD READ ------------------------------------------------------------------------
P('=' * 122)
P('THE WHOLE-BOARD READ — the three rules against each other')
P('=' * 122)
for a, an, b, bn in (('BINARY', BIN, 'UNWIND', UNW), ('UNWIND', UNW, 'FRACTIONAL', FRA),
                     ('BINARY', BIN, 'FRACTIONAL', FRA)):
    if an is None or bn is None:
        continue
    mv = [k for k in an if an[k]['v'] != bn[k]['v']]
    dn = sum(1 for k in mv if bn[k]['v'] < an[k]['v'])
    P('  %-11s -> %-11s %+9d board points on %4d rows  (%d down, %d up)'
      % (a, b, tot(bn) - tot(an), len(mv), dn, len(mv) - dn))
P()
P('  MEASURED AGAINST THE RAMP-ON, R3-OFF BASELINE %s (%s) — so these are R3 ALONE, with the'
  % (mRPRE, '{:,}'.format(tot(RPRE))))
P('  ramp\'s own 8 rows held out of the count rather than silently attributed to the collector.')
for nm, B in (('binary', BIN), ('unwind', UNW), ('fractional', FRA)):
    if B is None:
        continue
    ks = [k for k in RPRE if B[k]['v'] != RPRE[k]['v']]
    P('  rows R3 charges under %-11s: %4d   total %+d'
      % (nm, len(ks), sum(B[k]['v'] - RPRE[k]['v'] for k in ks)))
P()
P('  THE ORDERING, AS PREREGGED (P-D-3): unwind saturates at %g games where the F1 credit curve' % U0)
P('  saturates at 11, so MORE rows break their run under unwind and it should collect LESS than')
P('  fractional and MORE than binary. Built ordering above.')

# ---- the shield population ------------------------------------------------------------------------
SH = [k for k in PRE if 0 < gnow(k) <= 2]
if UNW:
    P()
    P('  THE SHIELD POPULATION — rows whose run is broken by a season of <= 2 games: %d' % len(SH))
    P('    R3 take on them, BINARY : %+d' % sum(BIN[k]['v'] - RPRE[k]['v'] for k in SH))
    P('    R3 take on them, UNWIND : %+d' % sum(UNW[k]['v'] - RPRE[k]['v'] for k in SH))
    P('    R3 take on them, FRACTNL: %+d' % (sum(FRA[k]['v'] - RPRE[k]['v'] for k in SH) if FRA else 0))

json.dump(dict(boards=dict(pre=mPRE, binary_noramp=mBIN0, binary=mBIN, fractional=mFRA, unwind=mUNW,
                           ident_p=mIDP),
               totals=dict(pre=tot(PRE), binary_noramp=tot(BIN0), binary=tot(BIN),
                           fractional=(tot(FRA) if FRA else None), unwind=(tot(UNW) if UNW else None)),
               U0=U0, ramp_rows=[dict(key=k, delta=dv) for dv, k in d],
               named=[dict(name=n, g=g, u=u, pre=p_, binary=b_, unwind=u_, note=s)
                      for n, g, u, p_, b_, u_, s in ROWS]),
          open(os.path.join(HERE, 'UNWIND_ROWS.json'), 'w'), indent=1)
open(os.path.join(HERE, 'UNWIND_ROWS_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: UNWIND_ROWS.json · UNWIND_ROWS_out.txt')
