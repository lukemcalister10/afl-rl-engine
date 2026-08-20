#!/usr/bin/env python3
"""COMPLETION PASS — THE READ-ONLY PROBE THAT LOCATES THE EMIT HALT.

WHY THIS FILE EXISTS. The walk-forward emit on a05fe951 HALTED on the ORDER 31-F replication guard at
82 of 89. This probe establishes WHERE the two laws diverge, by reading BOTH the engine's guarded
day-0 predicate and the raw fade the emitter multiplies by, in ONE engine load, on the candidate's own
dial line. It proves the divergence is in the INSTRUMENT WIRING, not in the board.

  the emitter (emit_matrix_31f.py:143) forms   int(round(_landed_v0_board(q) * o31_D(q, BASE_REF)))
  the engine  (_merged_recover.py, D7 site 2)  forms   _entry30b_price(q, BASE_REF)

Under RL_O43 the parity guard is wired into `_entry30b_price` and into `ev`, but NOT into `o31_D`.
The board is written from the guarded path; the emitter reads the UNGUARDED fade. Both are internally
consistent; they are simply not the same law any more.

READ-ONLY. No board is built, nothing is written, no engine or emitter file is modified.
"""
import io, os, contextlib

os.chdir(os.path.join(os.environ['RL_REPO'], 'engine', 'rl_after'))
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_cp_probe'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; o31_D = G['o31_D']
derived = G['_entry29b_derived']; e30 = G.get('_entry30b_price')

print('=' * 118)
print('COMPLETION PASS — WHERE THE EMIT HALT COMES FROM (read-only probe)')
print('=' * 118)
print('  RL_O43 live in the engine namespace : _O43 = %s' % G.get('_O43'))
print('  _D7_DFADE entries (fade pairs)      : %d' % len(G.get('_D7_DFADE') or {}))
print('  _D7_FLOOR entries (lifted rows)     : %d' % len(G.get('_D7_FLOOR') or {}))
print()
print('  THE EMITTER multiplies by o31_D  -- emit_matrix_31f.py:143, o31_D read from G at :83')
print('  THE ENGINE  forms _entry30b_price -- the D7 SECOND WIRING SITE, which wraps THIS and not o31_D')
print()
print('  %-18s %12s %11s %14s %14s %8s %8s' % ('key', 'derived_v0', 'o31_D', 'd0*o31_D', '_e30b_price',
                                               'EMITTER', 'BOARD'))
BY = {p.get('key'): p for p in MA.data}
KEYS = ['harley-barker', 'blake-thredgold', 'max-king-syd', 'liam-hetherton', 'ollie-murphy',
        'noah-chamberlain', 'sam-allen', 'kobe-mcdonald']
for k in KEYS:
    p = BY.get(k)
    if p is None:
        print('  %-18s ABSENT' % k); continue
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = float(derived(p, MA.BASE_REF)); D = float(o31_D(p, MA.BASE_REF))
        pr = float(e30(p, MA.BASE_REF)) if e30 else float('nan')
    flag = '' if round(d0 * D) == round(pr) else '   <-- DIVERGES'
    print('  %-18s %12.4f %11.6f %14.4f %14.4f %8d %8d%s'
          % (k, d0, D, d0 * D, pr, round(d0 * D), round(pr), flag))
print()
print('  READING: where the two columns differ, the BOARD carries the right-hand value (the guarded')
print('  price) and the EMITTER forms the left-hand one (the unguarded fade). The ORDER 31-F guard')
print('  compares the emitter\'s value against the reference, which describes the BOARD -- so it')
print('  fail-closes. THE GUARD IS BEHAVING CORRECTLY. Closing the gap needs o31_D wrapped under')
print('  _O43 (AN ENGINE CHANGE) or the guard re-pointed at _entry30b_price (A CHANGE TO THE')
print('  BYTE-CARRIED EMITTER). This seat is authorised to make NEITHER, so the item HALTS here.')
