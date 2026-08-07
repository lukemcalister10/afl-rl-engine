#!/usr/bin/env python3
"""#334 stage 5 — THE DIAL-0 STRUCTURAL SHORT-CIRCUIT PROOF, THROUGH THE FULL GATE.

RL_G5_W is a manifest dial, so in gate mode the ambient environment is CLEARED and the manifest value
is loaded authoritatively — an `RL_G5_W=0` on the command line proves nothing. This script therefore
flips the manifest value to "0", re-stamps `config_sha256` + `expected_boot.json 'config'` exactly as a
bake would, runs the REAL gated build (`rl_export.py` under RL_CONFIG_MODE=gate: config manifest, Guard 5,
LOADED-PROVENANCE, NUMERAIRE GUARD, PARITY GATE, FUT-LABEL, ZERO-EMPTY-CLUB), asserts the produced board
is byte-identical to the ruled baseline `b56bbdde`, and then restores every file it touched — verified by
md5 on the way out. Nothing is left flipped.

Usage:  RL_REPO=<worktree> RL_WORKDIR=<workspace>/rl_after python3 killswitch_check.py
"""
import os, sys, json, hashlib, subprocess, collections, shutil

REPO = os.environ['RL_REPO']; WS = os.environ['RL_WORKDIR']
BASELINE = 'b56bbddea15fd48e35b5794b1b5e9e23'
MC = REPO + '/data/model_config.json'; EB = REPO + '/data/expected_boot.json'
sys.path.insert(0, REPO)
import config_manifest as cm


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def rw(path, mut):
    raw = open(path, 'rb').read()
    d = json.loads(raw.decode(), object_pairs_hook=collections.OrderedDict)
    mut(d)
    out = json.dumps(d, indent=1, ensure_ascii=True)
    if raw.endswith(b'\n'): out += '\n'
    open(path, 'w', encoding='ascii').write(out)


ORIG = {p: open(p, 'rb').read() for p in (MC, EB)}
print("#334 STAGE 5 — DIAL-0 STRUCTURAL SHORT-CIRCUIT PROOF (full gate)")
print("  before: model_config %s  expected_boot %s" % (md5(MC)[:8], md5(EB)[:8]))
print("          shipped RL_G5_W = %r" % json.load(open(MC))['vars']['RL_G5_W'])
rc = 1
try:
    newhash = [None]
    def flip(d):
        d['vars']['RL_G5_W'] = '0'
        d['config_sha256'] = cm.canonical_hash(d['vars']); newhash[0] = d['config_sha256']
    rw(MC, flip)
    rw(EB, lambda e: e.__setitem__('config', newhash[0]))
    print("  flipped RL_G5_W -> '0' ; config_sha256 -> %s (expected_boot re-stamped in step)" % newhash[0][:12])

    env = dict(os.environ)
    env.update(RL_CONFIG_MODE='gate', RL_REPO=REPO,
               RL_FV=REPO + '/engine/forward_valuation',
               PYTHONPATH=WS + ':/home/claude/rl_vendor',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    for k in ('RL_WORKDIR', 'RL_VENDOR', 'RL_G5_W'): env.pop(k, None)
    board = WS + '/rl_app_data.json'
    if os.path.exists(board): os.remove(board)
    r = subprocess.run([sys.executable, 'rl_export.py'], cwd=WS, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    keep = [l for l in r.stdout.splitlines()
            if any(t in l for t in ('config manifest', 'CONFIG ACCEPTED', 'Guard 5', 'guard', 'PARITY',
                                    'NUMÉRAIRE', 'FUT-LABEL', 'ZERO-EMPTY-CLUB', 'REJECT', 'HALT',
                                    'LOADED-PROVENANCE', 'exported active'))]
    print("  --- gated build under RL_G5_W=0 (exit %d) ---" % r.returncode)
    for l in keep: print("   ", l)
    got = md5(board)
    print("  board md5 = %s   baseline = %s" % (got, BASELINE))
    ok = (r.returncode == 0 and got == BASELINE)
    print("  DIAL-0 STRUCTURAL SHORT-CIRCUIT: %s" % ("PASS — byte-exact b56bbdde through the full gate"
                                                     if ok else "FAIL"))
    rc = 0 if ok else 1
finally:
    for p, b in ORIG.items(): open(p, 'wb').write(b)
    print("  restored: model_config %s  expected_boot %s  (both == pre-run)" % (md5(MC)[:8], md5(EB)[:8]))
    assert md5(MC) == hashlib.md5(ORIG[MC]).hexdigest()
    assert md5(EB) == hashlib.md5(ORIG[EB]).hexdigest()
    print("          shipped RL_G5_W restored = %r" % json.load(open(MC))['vars']['RL_G5_W'])
sys.exit(rc)
