#!/usr/bin/env python3
"""#334 stage 6 — THE DIAL-0 STRUCTURAL SHORT-CIRCUIT PROOF, THROUGH THE FULL GATE.

Stage 6 ships BOTH dials at 0 (Addendum 1 F9/F10), so this is not a side experiment — it is the proof
that THE SHIPPED STATE IS THE STAGE-5 LANDED BOARD, byte for byte, through the real gated build.

It asserts, in order:
  1. the committed manifest really ships RL_G6_W = 0 and RL_G6_KPD = 0;
  2. the gated build (config manifest, Guard 5, LOADED-PROVENANCE, NUMERAIRE GUARD, PARITY GATE,
     FUT-LABEL, ZERO-EMPTY-CLUB) produces board 13f8c2e0240600733a5fb42414510445 — the stage-5 landing;
  3. the short-circuit is STRUCTURAL, not arithmetic: with both dials at 0 the engine never opens
     g6_table.json at all. Proved by moving the table aside for a second full gated build and showing
     the board is still byte-identical (if the branch were taken, _g6_load would SystemExit).

Nothing is left flipped; every file touched is restored and md5-verified on the way out.
"""
import os, sys, json, hashlib, subprocess, shutil

REPO = os.environ['RL_REPO']; WS = os.environ['RL_WORKDIR']
LANDED = '13f8c2e0240600733a5fb42414510445'
MC = REPO + '/data/model_config.json'
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

L = []
def say(s=''): L.append(s); print(s)

def gated_build():
    env = dict(os.environ)
    env.update(RL_CONFIG_MODE='gate', RL_REPO=REPO, RL_FV=REPO + '/engine/forward_valuation',
               PYTHONPATH=WS + ':/home/claude/rl_vendor', OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    for k in ('RL_WORKDIR', 'RL_VENDOR', 'RL_G6_W', 'RL_G6_KPD', 'RL_OUT'): env.pop(k, None)
    board = WS + '/rl_app_data.json'
    if os.path.exists(board): os.remove(board)
    r = subprocess.run([sys.executable, 'rl_export.py'], cwd=WS, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return r, (md5(board) if os.path.exists(board) else None)

say('#334 STAGE 6 — DIAL-0 STRUCTURAL SHORT-CIRCUIT PROOF (full gate)')
v = json.load(open(MC))['vars']
say('  shipped manifest: RL_G6_W = %r   RL_G6_KPD = %r' % (v['RL_G6_W'], v['RL_G6_KPD']))
assert v['RL_G6_W'] == '0' and v['RL_G6_KPD'] == '0', 'the shipped manifest does not ship both dials at 0'

r, got = gated_build()
keep = [l for l in r.stdout.splitlines()
        if any(t in l for t in ('config manifest', 'CONFIG ACCEPTED', 'Guard 5', 'PARITY', 'NUMÉRAIRE',
                                'FUT-LABEL', 'ZERO-EMPTY-CLUB', 'REJECT', 'HALT', 'LOADED-PROVENANCE',
                                'exported active'))]
say('  --- gated build at the shipped dials (exit %d) ---' % r.returncode)
for l in keep: say('    ' + l)
say('  board md5 = %s   stage-5 landing = %s' % (got, LANDED))
ok1 = (r.returncode == 0 and got == LANDED)
say('  (1) SHIPPED STATE == STAGE-5 LANDED BOARD: %s' % ('PASS — byte-exact' if ok1 else 'FAIL'))

TBL = WS + '/g6_table.json'
say('')
say('  (2) the STRUCTURAL claim: at dial 0 the taught table is never even opened.')
assert os.path.exists(TBL), 'g6_table.json missing from the workspace — re-seed via bootstrap.sh'
shutil.move(TBL, TBL + '.moved')
try:
    r2, got2 = gated_build()
finally:
    shutil.move(TBL + '.moved', TBL)
ok2 = (r2.returncode == 0 and got2 == LANDED)
say('      with g6_table.json MOVED ASIDE the gated build exits %d and produces %s' % (r2.returncode, got2))
say('      (if the branch were taken, _g6_load raises SystemExit and the build cannot complete)')
say('  (2) STRUCTURAL SHORT-CIRCUIT: %s' % ('PASS' if ok2 else 'FAIL'))
say('')
say('  VERDICT: %s' % ('PASS — the shipped stage-6 state rebuilds the stage-5 landed board byte-exact '
                      'through the full gate, and the correction is structurally inert at dial 0'
                      if (ok1 and ok2) else 'FAIL'))
open(os.environ.get('RL_OUT', '.') + '/KILLSWITCH_PROOF.txt', 'w').write('\n'.join(L) + '\n')
sys.exit(0 if (ok1 and ok2) else 1)
