#!/usr/bin/env python3
# A4 — THE CONFIG STAMP HALTS A STALE BOOK. The matrix carries __meta__.config_sha256; ship_gates_check
# asserts it == the enforced CONFIG_HASH (L280-281). Induce it CHEAPLY (no hot bake): feed a pre-built book
# via the SGC_B1_MATRIX seam whose engine+store stamps MATCH the candidate but whose config_sha256 does NOT
# (a formula change made through CONFIG on a STALE book). Assert B1 HALTs and the reason NAMES the config
# mismatch. Contrast: the same synthetic book with the CORRECT config_sha256 is ACCEPTED by the stamp
# assertion (B1 does not reject on config). The literal "rebuild -> green" is the A5 normal run (a regenerated
# book carries the matching config and B1 PASSes). B2/B4 skipped (slow producers; not the subject here).
import json, hashlib, os, subprocess, sys
ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OUT = os.path.join(ROOT, 'session_2026-07-14', 'harness_guard', 'out')
sys.path.insert(0, ROOT)
import config_manifest
HEAD = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open(os.path.join(RA, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]
CFG = config_manifest.manifest_hash()
WRONG = 'deadbeef' * 8   # a config hash that does NOT match — simulates a config/formula change on a stale book

def synth_book(config_sha):
    # engine+store stamps MATCH the candidate under test, so the ONLY discriminator is config_sha256.
    m = {'__meta__': {'kind': 'walk_forward_cohort_book', 'engine_head_md5': HEAD,
                      'store_md5': STORE, 'config_sha256': config_sha, 'n_players': 6}}
    for C in range(2010, 2016):      # a few 2004-2020 incurve classes, flat Vpath -> ratios ~1.0 (<=1.30)
        m['p%d' % C] = {'year': C, 'incurve': True, 'yrs': [1, 2, 3, 4, 5, 6], 'Vpath': [100.0] * 6}
    return m

def run(tag, config_sha):
    path = os.path.join(OUT, 'a4_book_%s.json' % tag)
    json.dump(synth_book(config_sha), open(path, 'w'))
    env = dict(os.environ, SGC_B1_MATRIX=path, SGC_SKIP='B2,B4',
               SGC_REPORT_DIR='session_2026-07-14/harness_guard/out', RL_REPO=ROOT)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'ship_gates_check.py')],
                       env=env, capture_output=True, text=True, cwd=ROOT, timeout=900)
    log = os.path.join(OUT, 'a4_%s.log' % tag)
    open(log, 'w').write(r.stdout + '\n---STDERR---\n' + r.stderr)
    return r.returncode, r.stdout + r.stderr

print('HEAD=%s STORE=%s CFG=%s' % (HEAD, STORE, CFG[:12]))
# --- A4a: config MISMATCH on a stale book ---
rc_bad, out_bad = run('mismatch', WRONG)
b1_bad = [l for l in out_bad.splitlines() if l.startswith('B1 ')]
names_config = ('config %s=%s?' % (WRONG[:8], CFG[:8])) in out_bad or ('config ' in out_bad and WRONG[:8] in out_bad)
halted_bad = 'B1  ' in out_bad and (' HALT ' in ''.join(b1_bad) or any('HALT' in l for l in b1_bad))
# --- A4b: config MATCHES -> stamp assertion accepts the book (no config rejection) ---
rc_ok, out_ok = run('match', CFG)
config_rejected_ok = ('hashes != candidate' in out_ok and 'config' in out_ok and CFG[:8] in out_ok
                      and ('=%s?' % CFG[:8]) not in out_ok)  # not expected; sanity only
b1_ok = [l for l in out_ok.splitlines() if l.startswith('B1 ')]
accepted_ok = any(('INJECTED' in l or 'PASS' in l) for l in b1_ok) and 'hashes != candidate' not in ''.join(b1_ok)

print('\n[A4a stale/mismatch] rc=%d' % rc_bad)
for l in b1_bad: print('   ', l[:200])
print('   HALTs=%s  names-config-mismatch=%s' % (halted_bad, names_config))
print('[A4b matching config] rc=%d' % rc_ok)
for l in b1_ok: print('   ', l[:200])
print('   stamp-accepts-book=%s' % accepted_ok)

pass_ = halted_bad and names_config and accepted_ok
verdict = 'PASS' if pass_ else 'FAIL'
open(os.path.join(OUT, 'rc_A4'), 'w').write(
    '%s  A4a: HALT=%s names_config=%s rc=%d | A4b: stamp_accepts=%s rc=%d\n'
    % (verdict, halted_bad, names_config, rc_bad, accepted_ok, rc_ok))
print('\nA4 %s' % verdict)
sys.exit(0 if pass_ else 1)
