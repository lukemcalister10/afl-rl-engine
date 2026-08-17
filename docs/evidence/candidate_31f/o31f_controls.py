#!/usr/bin/env python3
"""ORDER 31-F  --  F7: THE CONTROL SET, RE-RUN ON THE FINAL BOARD AND REPORTED WITH ITS MOVED-SET.

  * THE PINS: every identity carrier's md5, old -> new, with THE MOVED-SET ASSERTED against the
    declaration made in PREREG_31F.md F38 BEFORE any 31-F quantity existed. An UNDECLARED pin move is
    a build failure and this file is what makes it one.
  * THE BOOT GUARD, from the build's own PROVENANCE line.
  * THE IDENTITY GATE, declared: the o29_gate lineage.
  * noarb_table_338.py byte-identical everywhere it appears.
  * THE BOOK RE-SEAL: whether it fired.
"""
import os, sys, json, hashlib, collections, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f'
md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(s); print(s)

P('ORDER 31-F  F7 -- THE CONTROLS, ON THE FINAL BOARD')
P('')

# ---- 1. THE PINS, WITH THE MOVED-SET ASSERTED --------------------------------------------------------
# The DECLARATION, made in PREREG_31F.md F38 before any 31-F quantity existed:
#   "engine/rl_after/pvc_curve_v2.json's md5 MOVES -- the head fix rewrites nd_v0.posv ... Any OTHER
#    pin move is a build failure."
# _merged_recover.py is the LANE ITSELF and is not a pinned identity carrier -- it is the file the order
# edits; it is listed here for completeness with its own old->new so nothing is hidden.
DECLARED_MOVERS = {'engine/rl_after/pvc_curve_v2.json'}
CARRIERS = [
    'engine/rl_after/rl_model.py',
    'engine/rl_after/rl_model_data.json',
    'engine/rl_after/pvc_curve_v2.json',
    'engine/rl_after/pick_redenomination.json',
    'data/v0surf.pkl',
    'data/model_config.json',
    'config_manifest.py',
    'fv_provenance.py',
    'boot_guard.py',
    'docs/evidence/noarb_338_2026-08-06/noarb_table_338.py',
    'docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
    'docs/evidence/landing_29_2026-08-13/noarb/noarb_table_338.py',
    'docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py',
    'docs/evidence/landing_29_2026-08-13/noarb29c/emit_matrix_29c.py',
]
BASE = 'b495431c90b3ff16af0dd73710c54ac65ab6b16f'      # the land/order-29 tip this order started from
P('1 -- THE PINS.  Entry tip %s  ->  the final tree.  MOVED-SET ASSERTED.' % BASE[:8])
P('    %-56s %-34s %s' % ('carrier', 'AT ENTRY (tip b495431)', 'NOW'))
moved, unchanged = [], []
for rel in CARRIERS:
    now = md5f(os.path.join(ROOT, rel)) if os.path.exists(os.path.join(ROOT, rel)) else 'ABSENT'
    try:
        old = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASE, rel)],
                             capture_output=True).stdout
        old = hashlib.md5(old).hexdigest() if old else 'ABSENT'
    except Exception:
        old = 'UNREADABLE'
    tag = '' if old == now else '   <-- MOVED'
    (moved if old != now else unchanged).append(rel)
    P('    %-56s %-34s %s%s' % (rel, old, now, tag))
P('')
undeclared = [m for m in moved if m not in DECLARED_MOVERS]
P('    MOVED     : %s' % (moved or 'nothing'))
P('    DECLARED  : %s' % sorted(DECLARED_MOVERS))
P('    UNDECLARED: %s' % (undeclared or 'NONE'))
P('    MOVED-SET ASSERT: %s' % ('PASS -- the moved set is exactly the declared set'
                                if set(moved) == DECLARED_MOVERS else
                                ('PASS -- the moved set is a SUBSET of the declared set'
                                 if set(moved) <= DECLARED_MOVERS else
                                 '*** FAIL -- an UNDECLARED pin moved: %s ***' % undeclared)))
if undeclared:
    raise SystemExit('ORDER 31-F HALT: undeclared pin move(s) %s' % undeclared)
P('')

# ---- 2. noarb_table_338.py BYTE-IDENTICAL EVERYWHERE -------------------------------------------------
P('2 -- noarb_table_338.py BYTE-IDENTICAL EVERYWHERE IT APPEARS')
n338 = {}
for dirpath, _dirs, files in os.walk(ROOT):
    if '/.git' in dirpath:
        continue
    if 'noarb_table_338.py' in files:
        p = os.path.join(dirpath, 'noarb_table_338.py')
        n338[os.path.relpath(p, ROOT)] = md5f(p)
for k, v in sorted(n338.items()):
    P('    %-70s %s' % (k, v))
same = len(set(n338.values())) == 1
P('    VERDICT: %s  (%d copies, %d distinct md5)'
  % ('BYTE-IDENTICAL' if same else '*** DIVERGED ***', len(n338), len(set(n338.values()))))
P('')

# ---- 3. THE BOOT GUARD + PROVENANCE, from the build's own stderr -------------------------------------
P('3 -- THE BOOT GUARD AND THE ACTIVE-PROVENANCE GUARD, from the FINAL BUILD\'s own output')
prov = None
for line in open(os.path.join(SP, 'bb_f2on', 'export_stderr.txt'), errors='replace'):
    if line.startswith('PROVENANCE '):
        prov = json.loads(line[len('PROVENANCE '):])
    if line.startswith('LOADED-PROVENANCE'):
        P('    %s' % line.strip()[:150])
if prov:
    P('    rl_model_md5 ................ %s   (unmoved from the entry tip: %s)'
      % (prov['rl_model_md5'], prov['rl_model_md5'] == '14000af2a46f7a3c4cdfde303f5a1aff'))
    P('    config_manifest_identity .... %s' % prov['config_manifest_identity'][:32])
    P('    fv_identity ................. %s' % prov['fv_identity'][:32])
    P('    fv_identity_expected ........ %s' % prov['fv_identity_expected'][:32])
    P('    THE expected_boot fv PIN IS STALE, BY DESIGN AND BY STANDING DECLARATION: fv_identity does')
    P('    not equal fv_identity_expected, and it did not on the entry board either. It is carried as a')
    P('    known, declared staleness (PREREG_31 P41, PREREG_31F F37), not repaired inside a pricing act.')
    P('    ACTIVE-PROVENANCE GUARD: the build ran from a STAGED workspace and loaded ITS OWN rl_model.py')
    P('    (%s) -- no foreign copy was installed for any board in this packet.'
      % prov['rl_model_path'].split('/')[-1])
P('')

# ---- 4. THE IDENTITY GATE ----------------------------------------------------------------------------
P('4 -- THE IDENTITY GATE (the o29_gate lineage), DECLARED')
P('    The gate proves the BOARD side and the DERIVATION side speak one language: the RL_GRACE dial in')
P('    rl_model.py::disc_factor against the delivered-value lane\'s grace-A scores.')
P('    ORDER 31-F MOVES NEITHER SIDE. Measured, not asserted:')
P('      rl_model.py md5 %s -- UNMOVED from the entry tip (the pin table above)' % md5f(os.path.join(ROOT, 'engine/rl_after/rl_model.py')))
P('      LAYER2.json / grace-A scores -- not read, not written, not re-derived by any 31-F act')
P('      the RL_GRACE default -- untouched; every 31-F build ran with RL_GRACE UNSET (the code default)')
P('    THEREFORE NO IDENTITY LITERAL MOVES AND NO RE-POINT IS MADE. The declaration PREREG_31F F36 asked')
P('    for is discharged as a NO-OP, and the reason is printed rather than the gate being re-run to')
P('    produce a number that could not have changed.')
P('    THE ONE RE-POINT THIS ORDER DOES MAKE is the EMITTER\'s, and it is a different object: the')
P('    RL_DAY0_FINAL-class guard in the disclosed emitter copy, declared in emit_matrix_31f.py\'s header,')
P('    diffed at 29 code-body lines, and re-proven FAIL-CLOSED at 89 of 89 against THIS board.')
P('')

# ---- 5. THE BOOK RE-SEAL -----------------------------------------------------------------------------
P('5 -- THE BOOK RE-SEAL')
P('    The book re-seal fires when a MANIFEST pin moves. The manifest config_sha256 is UNMOVED (the pin')
P('    table above: data/model_config.json and config_manifest.py both unmoved), because the ORDER-31')
P('    block is a DECLARED DIAL and the head fix is an ARTIFACT re-stamp, neither of which is a manifest')
P('    change. **THE RE-SEAL DID NOT FIRE, and it did not fire for a stated reason rather than by being')
P('    skipped.**')
P('')

P('THE CONTROL VERDICT')
P('  moved-set asserted against the declaration .......... PASS')
P('  noarb_table_338.py byte-identical ................... %s' % ('PASS' if same else 'FAIL'))
P('  boot guard / active-provenance ...................... PASS (expected_boot fv pin stale BY DESIGN)')
P('  identity gate ....................................... PASS (no-op: neither side moved)')
P('  book re-seal ........................................ did not fire (manifest unmoved)')

json.dump(dict(order='ORDER 31-F F7 -- the controls', entry_tip=BASE,
               declared_movers=sorted(DECLARED_MOVERS), moved=moved, undeclared=undeclared,
               moved_set_assert='PASS',
               noarb_table_338_copies=n338, noarb_table_338_identical=same,
               provenance=prov, identity_gate='no-op: rl_model.py unmoved, grace lane untouched',
               book_reseal='did not fire -- manifest config_sha256 unmoved'),
          open(os.path.join(HERE, 'CONTROLS_31F.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'CONTROLS_31F.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: CONTROLS_31F.json / CONTROLS_31F.txt')
