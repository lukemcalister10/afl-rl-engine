#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE R3 RUN-BREAK: BINARY vs FRACTIONAL, PRICED SIDE BY SIDE. NOTHING ADOPTED.

THE DEFECT THIS PRICES. Under the wired BINARY rule any season with games > 0 breaks the current
absence run outright. Measured on the built board that is worth up to +560 board points of shielding
on ONE game, and 63 rows have their run broken by a season of two games or fewer.

THE VARIANT. RL_O41_BREAK=fractional: a season contributes (1 - credit(games)) of its own
season-weight to the run, and only a season that FULLY credits (11+ games) stops the walk. The credit
is o41_credit — THE SAME F1 GUARDED CURVE I1 already carries. One measured object, two consumers,
NO NEW CONSTANT.

THIS FILE REPORTS THE TWO BOARDS ON THE NAMED ROWS AND ON THE SHIELD POPULATION. IT DOES NOT CHOOSE.

NO ENGINE RUN — pure reads over boards already built.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
Y = 2026
GUARD = [0.0, 0.1286875208353465, 0.23834489196711883, 0.23834489196711883, 0.23834489196711883,
         0.2455042373957035, 0.38568558243890977, 0.38568558243890977, 0.45188866847720316,
         0.8878514765964253, 0.8878514765964253, 1.0]
L = []


def P(s=''):
    print(s); L.append(str(s))


def credit(g):
    g = float(g)
    if g <= 0:
        return 0.0
    if g >= 11:
        return 1.0
    n = int(g); f = g - n
    return GUARD[n] if f <= 0 else (1 - f) * GUARD[n] + f * GUARD[min(n + 1, 11)]


def board(tag):
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (ASM, tag)
    if not os.path.exists(p):
        return None, None
    return ({r['key']: r for r in json.load(open(p))['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


PRE, mPRE = board('V750_L5C')       # the board before R3
BIN, mBIN = board('V751_CAND')      # R3, BINARY break — THE CANDIDATE
FRA, mFRA = board('V751_FRAC')      # R3, FRACTIONAL break
FR2, mFR2 = board('V751_FRAC2')
IDP, mIDP = board('IDENT_P')
CHK, mCHK = board('V751_CANDC')     # dial-off re-check
STORE = {x['key']: x for x in json.load(open(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')))}


def seasons(k):
    return {int(x['year']): float(x.get('games') or 0.0)
            for x in (STORE.get(k, {}).get('scoring') or []) if int(x['year']) <= Y}


def gnow(k):
    return seasons(k).get(Y, 0.0)


P('=' * 122)
P('THE R3 RUN-BREAK — BINARY (wired) vs FRACTIONAL (the variant). PRICED, NOT ADOPTED.')
P('=' * 122)
P()
P('  before R3 at all             %s  %s' % (mPRE, '{:>9,}'.format(sum(r['v'] for r in PRE.values()))))
P('  R3, BINARY break  (CANDIDATE) %s  %s' % (mBIN, '{:>9,}'.format(sum(r['v'] for r in BIN.values()))))
P('  R3, FRACTIONAL break         %s  %s' % (mFRA, '{:>9,}'.format(sum(r['v'] for r in FRA.values()))))
tB = sum(r['v'] for r in BIN.values()); tF = sum(r['v'] for r in FRA.values())
tP = sum(r['v'] for r in PRE.values())
P()
P('  R3 marginal, BINARY    : {:+,} on {} rows'.format(
    tB - tP, sum(1 for k in PRE if PRE[k]['v'] != BIN[k]['v'])))
P('  R3 marginal, FRACTIONAL: {:+,} on {} rows'.format(
    tF - tP, sum(1 for k in PRE if PRE[k]['v'] != FRA[k]['v'])))
P('  *** FRACTIONAL vs BINARY: {:+,} board points, {} rows differ ***'.format(
    tF - tB, sum(1 for k in BIN if BIN[k]['v'] != FRA[k]['v'])))
P()
P('  IDENTITIES:')
P('    every ORDER 41 dial OFF          -> %s  %s'
  % (mIDP, 'reproduces ORDER P 374d4e44' if mIDP == '374d4e44' else '*** NOT 374d4e44 ***'))
P('    the break dial UNSET (binary)     -> %s  %s'
  % (mCHK, 'byte-identical to the candidate %s' % mBIN if mCHK == mBIN else '*** DIFFERS from %s ***' % mBIN))
P('    determinism, fractional x2        -> %s'
  % ('IDENTICAL — %s' % mFRA if mFRA == mFR2 else '*** FIRED *** %s vs %s' % (mFRA, mFR2)))
P()

# ---- day-0 ------------------------------------------------------------------------------------------
gl = [k for k in BIN if not any(g > 0 for g in seasons(k).values())]
mv0 = [k for k in gl if BIN[k]['v'] != FRA[k]['v']]
P('  DAY-0: %d truly gameless board rows, %d moved by the break rule   <-- must be 0 for 89/89'
  % (len(gl), len(mv0)))
P()

# ---- the named rows -----------------------------------------------------------------------------------
P('=' * 122)
P('THE NAMED ROWS — CONSEQUENCES, NEVER TARGETS')
P('=' * 122)
NAMED = [('Will Brodie', 'the shield case — 1 game'),
         ('Toby Conway', 'genuinely absent'),
         ('Harry Barnett', 'genuinely absent'),
         ('Mitchell Edwards', 'returned, 16 games'),
         ('Noah Mraz', 'returned, 4 games'),
         ('Jedd Busslinger', 'returned, 8 games'),
         ('Nick Madden', 'INTERMEDIATE — 7 games, credit ~0.39'),
         ('Taylor Goad', 'token games, small production leg'),
         ('Dante Visentini', 'token-ish, 13 games')]
KEY = {}
for k in BIN:
    KEY[BIN[k].get('name')] = k
P('  %-20s %6s %8s %9s %9s %9s %9s  %s'
  % ('player', 'g2026', 'credit', 'pre-R3', 'BINARY', 'FRACTNL', 'frac-bin', 'note'))
NAMEDJ = []
for nm, note in NAMED:
    k = KEY.get(nm)
    if not k:
        P('  %-20s NOT ON THE BOARD' % nm); continue
    g = gnow(k)
    row = dict(name=nm, g=g, credit=credit(g), pre=PRE[k]['v'], binary=BIN[k]['v'],
               frac=FRA[k]['v'], delta=FRA[k]['v'] - BIN[k]['v'],
               stripped_bin=(BIN[k]['v'] < PRE[k]['v']), stripped_frac=(FRA[k]['v'] < PRE[k]['v']),
               note=note)
    NAMEDJ.append(row)
    P('  %-20s %6.0f %8.4f %9d %9d %9d %+9d  %s'
      % (nm, g, credit(g), PRE[k]['v'], BIN[k]['v'], FRA[k]['v'], FRA[k]['v'] - BIN[k]['v'], note))
P()
P('  STRIPPED / RESTORED, read off the two boards (stripped = priced BELOW the pre-R3 board):')
P('  %-20s %14s %14s   %s' % ('player', 'BINARY', 'FRACTIONAL', 'changes?'))
for r in NAMEDJ:
    a = 'STRIPPED' if r['stripped_bin'] else 'restored'
    b = 'STRIPPED' if r['stripped_frac'] else 'restored'
    P('  %-20s %14s %14s   %s' % (r['name'], a, b, '***' if a != b else ''))
P()

# ---- the exploit-safety logic, verified on the takes ----------------------------------------------------
P('=' * 122)
P('THE EXPLOIT-SAFETY LOGIC, VERIFIED ON THE ACTUAL TAKES')
P('=' * 122)
P('The claim is that a token-games row cannot shield much BECAUSE its production leg (rho x e) is')
P('small — R3\'s take is capped at the production leg, so a thin career has little to strip. The takes')
P('below are the actual board points R3 removes from each row under each rule.')
P()
P('  %-20s %6s %10s %10s   %s' % ('player', 'g2026', 'take BIN', 'take FRAC', 'reading'))
for nm in ('Taylor Goad', 'Dante Visentini', 'Will Brodie', 'Nick Madden'):
    k = KEY.get(nm)
    if not k:
        continue
    tb = PRE[k]['v'] - BIN[k]['v']
    tf = PRE[k]['v'] - FRA[k]['v']
    P('  %-20s %6.0f %10d %10d   %s'
      % (nm, gnow(k), tb, tf,
         'take stays small — thin production leg' if tf < 300 else 'LARGE take'))
P()

# ---- the 63 shield rows, aggregate ------------------------------------------------------------------------
P('=' * 122)
P('THE SHIELD POPULATION — rows whose run is broken by a season of <= 2 games')
P('=' * 122)


def run_break_games(k):
    ss = seasons(k)
    if ss.get(Y, 0) > 0:
        return ss[Y]
    yy = Y - 1
    fl = STORE.get(k, {}).get('year')
    while fl is None or yy > int(fl):
        if ss.get(yy, 0) > 0:
            return ss[yy]
        yy -= 1
        if Y - yy > 40:
            break
    return None


shield = []
for k in BIN:
    g = run_break_games(k)
    if g is not None and g <= 2.0:
        shield.append(k)
sb = sum(PRE[k]['v'] - BIN[k]['v'] for k in shield)
sf = sum(PRE[k]['v'] - FRA[k]['v'] for k in shield)
P('  rows in the shield population: %d' % len(shield))
P('  R3 take on them, BINARY    : {:,} board points'.format(sb))
P('  R3 take on them, FRACTIONAL: {:,} board points'.format(sf))
P('  *** THE FRACTIONAL RULE RECOVERS {:,} BOARD POINTS OF SHIELDED TAKE ON THIS POPULATION ***'.format(sf - sb))
P()
top = sorted(((BIN[k]['v'] - FRA[k]['v'], k) for k in shield), reverse=True)[:12]
P('  the largest individual recoveries:')
P('  %-22s %6s %9s %9s %9s   %s' % ('player', 'g2026', 'pre-R3', 'BINARY', 'FRACTNL', 'recovered'))
for d, k in top:
    P('  %-22s %6.0f %9d %9d %9d   %+9d'
      % (str(BIN[k].get('name'))[:22], gnow(k), PRE[k]['v'], BIN[k]['v'], FRA[k]['v'], -d))
P()

# ---- whole-board movement ---------------------------------------------------------------------------------
mv = [k for k in BIN if BIN[k]['v'] != FRA[k]['v']]
dn = sum(1 for k in mv if FRA[k]['v'] < BIN[k]['v'])
P('WHOLE-BOARD: %d rows differ, %d down and %d up under the fractional rule.' % (len(mv), dn, len(mv) - dn))
P('Every mover is DOWN by construction unless a row\'s run shortens — the fractional rule can only')
P('lengthen a run relative to a binary break, never shorten it.')

json.dump(dict(md5=dict(pre=mPRE, binary=mBIN, frac=mFRA, frac2=mFR2, identp=mIDP, chk=mCHK),
               totals=dict(pre=tP, binary=tB, frac=tF),
               frac_minus_bin=tF - tB, n_diff=len(mv),
               day0_gameless=len(gl), day0_moved=len(mv0),
               named=NAMEDJ, shield_n=len(shield), shield_take_bin=sb, shield_take_frac=sf),
          open(os.path.join(HERE, 'BREAK_RULE.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'BREAK_RULE_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: BREAK_RULE.json · BREAK_RULE_out.txt')
