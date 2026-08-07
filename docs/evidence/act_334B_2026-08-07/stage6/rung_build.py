#!/usr/bin/env python3
"""#334 stage 6 — THE RUNG BUILD.  One rung of the ladder, through the FULL gated build.

RL_G6_W is a manifest dial, so in gate mode the ambient environment is CLEARED and the manifest value
is loaded authoritatively — an `RL_G6_W=0.5` on the command line proves nothing and builds nothing.
This script flips the manifest value to the rung, re-stamps `config_sha256` + `expected_boot.json
'config'` exactly as a bake would, runs the REAL gated build (config manifest, Guard 5,
LOADED-PROVENANCE, NUMERAIRE GUARD, PARITY GATE, FUT-LABEL, ZERO-EMPTY-CLUB), copies the board out to
`boards/board_rung<W>.json`, and then RESTORES every file it touched — verified by md5 on the way out.

Usage:  RL_REPO=<worktree> RL_WORKDIR=<workspace>/rl_after python3 rung_build.py <W> [<KPD>]
"""
import os, sys, json, hashlib, subprocess, collections, shutil

REPO = os.environ['RL_REPO']; WS = os.environ['RL_WORKDIR']
W = sys.argv[1]; KPD = sys.argv[2] if len(sys.argv) > 2 else '0'
OUT = os.environ.get('RL_OUT', REPO + '/docs/evidence/act_334B_2026-08-07/stage6')
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
print("#334 STAGE 6 RUNG BUILD — RL_G6_W=%s  RL_G6_KPD=%s  (full gate)" % (W, KPD))
rc = 1
try:
    nh = [None]
    def flip(d):
        d['vars']['RL_G6_W'] = W; d['vars']['RL_G6_KPD'] = KPD
        d['config_sha256'] = cm.canonical_hash(d['vars']); nh[0] = d['config_sha256']
    rw(MC, flip)
    rw(EB, lambda e: e.__setitem__('config', nh[0]))
    print("  config_sha256 -> %s" % nh[0][:12])
    env = dict(os.environ)
    env.update(RL_CONFIG_MODE='gate', RL_REPO=REPO, RL_FV=REPO + '/engine/forward_valuation',
               PYTHONPATH=WS + ':/home/claude/rl_vendor', OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    for k in ('RL_WORKDIR', 'RL_VENDOR', 'RL_G6_W', 'RL_G6_KPD', 'RL_OUT'): env.pop(k, None)
    board = WS + '/rl_app_data.json'
    if os.path.exists(board): os.remove(board)
    r = subprocess.run([sys.executable, 'rl_export.py'], cwd=WS, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    keep = [l for l in r.stdout.splitlines()
            if any(t in l for t in ('config manifest', 'CONFIG ACCEPTED', 'Guard 5', 'PARITY',
                                    'NUMÉRAIRE', 'FUT-LABEL', 'ZERO-EMPTY-CLUB', 'REJECT', 'HALT',
                                    'LOADED-PROVENANCE', 'exported active'))]
    print("  --- gated build (exit %d) ---" % r.returncode)
    for l in keep: print("   ", l)
    if r.returncode != 0:
        print(r.stdout[-4000:])
    got = md5(board)
    os.makedirs(OUT + '/boards', exist_ok=True)
    dest = OUT + '/boards/board_rung%s_kpd%s.json' % (W, KPD)
    shutil.copyfile(board, dest)
    print("  board md5 = %s -> %s" % (got, os.path.basename(dest)))
    rc = 0 if r.returncode == 0 else 1
finally:
    for p, b in ORIG.items(): open(p, 'wb').write(b)
    assert md5(MC) == hashlib.md5(ORIG[MC]).hexdigest()
    assert md5(EB) == hashlib.md5(ORIG[EB]).hexdigest()
    print("  restored: model_config %s  expected_boot %s" % (md5(MC)[:8], md5(EB)[:8]))
sys.exit(rc)
