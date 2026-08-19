#!/usr/bin/env python3
"""ORDER D7b — THE READ-ONLY VERIFICATION PROBE FOR THE THIRD WIRING SITE.

Proves, in ONE engine load on the candidate's own dial line, the four properties the prereg's
falsifiers name that a board md5 alone cannot show:

  D7B-F7  Y==2026 ONLY. For every guarded row the wrapper returns the INNER fade VERBATIM at every
          Y != 2026, so the walk-forward matrix's years 1..7 cannot move.
  D7B-F8  THE RISER IS UNTOUCHED. ollie-murphy carries no fade pair, so the max cannot reach him.
  SINGLE  THE LAW IS APPLIED EXACTLY ONCE. `_entry30b_price` is the UNWRAPPED predicate built on
          o31_D (:5109-5112); it inherits the lift through the fade and is NOT ratio-wrapped on top
          of it. Had both sites fired, harley-barker's predicate would read 526.60 -> 527 and the
          board's own printed-day-0 assert would have refused the board.
  EMIT    THE EMITTER'S ARITHMETIC NOW AGREES WITH THE BOARD. int(round(derived_v0 * o31_D)) --
          emit_matrix_31f.py:143, with o31_D read from the engine namespace at :83 -- reproduces the
          board's printed day-0 on the seven rows that previously diverged.

READ-ONLY. No board is built, nothing is written, no engine or emitter file is modified.
"""
import io, os, json, contextlib

os.chdir(os.path.join(os.environ['RL_REPO'], 'engine', 'rl_after'))
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_d7b_probe'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']
o31_D = G['o31_D']
derived = G['_entry29b_derived']
e30 = G.get('_entry30b_price')
DFADE = G.get('_D7_DFADE') or {}
FLOOR = G.get('_D7_FLOOR') or {}

W = 120
print('=' * W)
print('ORDER D7b — VERIFICATION OF THE THIRD WIRING SITE (read-only probe)')
print('=' * W)
print('  RL_O43 live in the engine namespace : _O43 = %s' % G.get('_O43'))
print('  _D7_DFADE entries (fade pairs)      : %d' % len(DFADE))
print('  _D7_FLOOR entries (lifted rows)     : %d' % len(FLOOR))

# ---- the wrapper is installed, and the predicate is NOT double-wrapped -------------------------
inner = (o31_D.__defaults__ or (None,))[0]
print()
print('  o31_D is the D7b wrapper            : %s   (inner fade recovered: %s)'
      % (o31_D.__name__ == 'o31_D' and inner is not None, inner is not None))
print('  o31_D docstring is D7b              : %s' % ('D7b' in (o31_D.__doc__ or '')))
print('  _entry30b_price is NOT ratio-wrapped: %s   (its code reads o31_D directly: %s)'
      % ('D7b' not in (e30.__doc__ or '') and 'ORDER D7:' not in (e30.__doc__ or ''),
         'o31_D' in e30.__code__.co_names))
assert inner is not None, 'D7b HALT: the o31_D wrapper is not installed'
assert 'o31_D' in e30.__code__.co_names, 'D7b HALT: the predicate is not built on o31_D'

BY = {p.get('key'): p for p in MA.data}

# ---- D7B-F7 : Y != 2026 IS RETURNED VERBATIM ---------------------------------------------------
print()
print('-' * W)
print('D7B-F7 — Y==2026 ONLY. For every guarded row, wrapper(Y) must EQUAL inner(Y) at every Y != 2026.')
print('-' * W)
YEARS = [2024, 2025, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
bad7 = []
for k in sorted(DFADE):
    p = BY.get(k)
    if p is None:
        bad7.append((k, 'row missing')); continue
    for Y in YEARS:
        with contextlib.redirect_stdout(io.StringIO()):
            a = float(o31_D(p, Y)); b = float(inner(p, Y))
        if a != b:
            bad7.append((k, Y, a, b))
print('  guarded rows checked : %d   years per row : %d   TOTAL COMPARISONS : %d'
      % (len(DFADE), len(YEARS), len(DFADE) * len(YEARS)))
print('  MISMATCHES AT Y != 2026 : %d   %s' % (len(bad7), 'PASS' if not bad7 else 'FAIL %s' % bad7[:6]))

# ---- the lift at Y == 2026 is exactly the healthy fade, and only ever raises --------------------
print()
print('-' * W)
print('THE LIFT AT Y=2026 — a max, so it can only RAISE. (_dl = live/injury fade, _dh = healthy fade)')
print('-' * W)
print('  %-22s %10s %10s %12s %12s %8s' % ('key', '_dl', '_dh', 'inner(2026)', 'o31_D(2026)', 'raises?'))
badmax = []
for k in sorted(DFADE):
    p = BY.get(k)
    if p is None: continue
    _dl, _dh = DFADE[k]
    with contextlib.redirect_stdout(io.StringIO()):
        a = float(o31_D(p, 2026)); b = float(inner(p, 2026))
    if a < b: badmax.append((k, a, b))
    print('  %-22s %10.6f %10.6f %12.6f %12.6f %8s' % (k, _dl, _dh, b, a, 'yes' if a > b else 'no'))
print('  ROWS WHERE THE WRAPPER LOWERED THE FADE : %d   %s'
      % (len(badmax), 'PASS (a max can only raise)' if not badmax else 'FAIL %s' % badmax))

# ---- D7B-F8 : the riser is untouched ------------------------------------------------------------
print()
print('-' * W)
print('D7B-F8 — THE RISER IS UNTOUCHED. A row whose injury regime already prices at or above its')
print('healthy counterpart carries NO fade pair, so the max cannot reach him. The shield is not a charge.')
print('-' * W)
for k in ['ollie-murphy']:
    p = BY.get(k)
    with contextlib.redirect_stdout(io.StringIO()):
        a = float(o31_D(p, 2026)); b = float(inner(p, 2026))
        d0 = derived(p, 2026)
    print('  %-18s in _D7_DFADE = %-5s   in _D7_FLOOR = %-5s   o31_D=%0.6f  inner=%0.6f  IDENTICAL=%s'
          % (k, k in DFADE, k in FLOOR, a, b, a == b))
    print('  %-18s emitted year-0 = int(round(derived_v0 * o31_D)) = %d'
          % (k, int(round(float(d0) * a))))

# ---- SINGLE APPLICATION + the emitter's arithmetic against the board's own reference ------------
REF = os.path.join(os.environ['RL_REPO'],
                   'docs/evidence/final_candidate_2026-08-19/DAY0_CP.json')
D0 = json.load(open(REF))
byref = {r['key']: r for r in D0['rows']}
print()
print('-' * W)
print('THE SEVEN ROWS THAT PREVIOUSLY DIVERGED — the emitter arithmetic against DAY0_CP.json (UNTOUCHED).')
print('  EMITTER = int(round(derived_v0 * o31_D))  [emit_matrix_31f.py:143]')
print('  PREDICT = _entry30b_price  [the engine\'s day-0 predicate, :5109-5112, built on the SAME o31_D]')
print('  DOUBLE  = what BOTH D7 sites firing would have produced: _d0*_dh^2/_dl  -- REFUSED BY DESIGN')
print('-' * W)
KEYS = ['harley-barker', 'blake-thredgold', 'sam-allen', 'max-king-syd',
        'noah-chamberlain', 'liam-hetherton', 'kobe-mcdonald', 'ollie-murphy']
print('  %-20s %12s %10s %10s %10s %8s %8s %8s' %
      ('key', 'derived_v0', 'o31_D', 'PREDICT', 'DOUBLE', 'EMITTER', 'REF', 'ok'))
nbad = 0
for k in KEYS:
    p = BY.get(k)
    if p is None: continue
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = derived(p, 2026); dd = float(o31_D(p, 2026)); pr = e30(p, 2026)
    emit = int(round(float(d0) * dd))
    ref = byref.get(k, {}).get('printed')
    dbl = ''
    if k in DFADE:
        _dl, _dh = DFADE[k]
        dbl = '%.2f' % (float(d0) * _dh * (_dh / _dl))
    ok = (emit == ref)
    nbad += (0 if ok else 1)
    print('  %-20s %12.4f %10.6f %10.4f %10s %8d %8s %8s'
          % (k, float(d0), dd, float(pr), dbl or '-', emit, ref, 'OK' if ok else 'MISMATCH'))
print()
print('  EMITTER vs REFERENCE mismatches on these rows : %d   %s' % (nbad, 'PASS' if not nbad else 'FAIL'))

# ---- the full 89 ---------------------------------------------------------------------------------
n_ok = 0; mis = []
for r in D0['rows']:
    p = BY.get(r['key'])
    if p is None: mis.append((r['key'], 'missing')); continue
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = derived(p, 2026); dd = float(o31_D(p, 2026))
    if int(round(float(d0) * dd)) == r['printed']: n_ok += 1
    else: mis.append((r['key'], r['printed'], int(round(float(d0) * dd))))
print()
print('=' * W)
print('  THE EMITTER ARITHMETIC OVER ALL WIRED ENTRANTS : %d of %d reproduce DAY0_CP.json EXACTLY  %s'
      % (n_ok, len(D0['rows']), 'PASS' if n_ok == len(D0['rows']) else 'FAIL %s' % mis[:6]))
print('=' * W)
print('  THE REFERENCE IS NOT TOUCHED. THE EMITTER IS NOT TOUCHED. PRICED, NOT ADOPTED.')
