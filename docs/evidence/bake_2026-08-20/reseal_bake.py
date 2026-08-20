#!/usr/bin/env python3
"""THE BAKE — B3 WALK-FORWARD BOOK RE-SEAL, on the CANDIDATE LINE, under GATE MODE (register v780).

WHAT THIS IS. session_2026-07-17/legd_derivation/reseal_book.py — the act that LAST moved
data/book_stable_seal.json (commit 2e49963) — carried with THREE DECLARED CHANGES and nothing else:

  (1) ROOT / RA RE-POINTED AT THIS WORKTREE. The original hardcodes ROOT='/home/user/afl-rl-engine'
      and RA='/home/claude/rl_workspace/rl_after'. That workspace is SHARED, OUT-OF-REPO, not owned by
      this branch, and measured to carry the STALE D7 engine (29376d5a) against this branch's own head
      — sealing from it would seal a book this branch did not build. Register v770 already ruled on
      exactly this re-pointing for the Guard 5 recipe. ship_gates_check.py:49 carries the same
      hardcoded RA; that is reported as a standing finding, not edited here.
  (2) THE RL_GAMMA='0.85' / RL_PICK1 / RL_RUCK_TAX / RL_RECENCY_DECAY / RL_PRIOR_TREES / PAR_RAMPS
      BLOCK IS DROPPED. data/model_config.json now carries RL_GAMMA=1.0, so passing 0.85 would be
      rejected by the gate-mode reject scan as a DIVERGENT model override and the re-seal would halt
      on line one. Gate mode loads those values itself, authoritatively, from the manifest — which is
      the whole point of gate mode. Passing them by hand is what the manifest replaced.
  (3) THREAD PINNING MADE EXPLICIT (OPENBLAS/OMP/MKL/NUMEXPR/VECLIB = 1, PYTHONHASHSEED=0). The
      original inherited these from its calling shell; naming them makes the run reproducible
      standalone instead of depending on an ambient the record does not carry.

WHY THE RESEAL_HALT FORK IS GONE. docs/evidence/landing_prep_2026-08-20/RESEAL_HALT.md halted this act
because the manifest line and the candidate line were DIFFERENT BOARDS (the 18 dials were default-OFF
and absent from the manifest), so either fork would have sealed a book for a board nobody meant. Its
own §2 records why every prior re-seal was legitimate: the levers of those chapters were DECLARED
KILL-SWITCHES WIRED DEFAULT-ON WITH THE MANIFEST DELIBERATELY UNMOVED, so gate mode priced the
candidate BY DEFAULT and the two lines were the same board. The defaults flip restores exactly that
condition. The fork is not chosen here — it is DISSOLVED, and the proof is mechanical: gate mode
clears the ambient model env and loads the manifest; the 18 dials are not in the manifest; so they
fall through to their (now candidate) code defaults. config_sha256 is UNMOVED (eed19a75) and so is the
'config' pin the C3 re-key certified.

The steps are the instrument's own, unchanged: regenerate the matrix EXACTLY as ship_gates B3 does
(RL_CONFIG_MODE=gate), assert the embedded __meta__ engine/store stamps == the candidate, recompute
stable_sha256 over the STABLE-KEYED content and re-count n_players, rewrite data/book_stable_seal.json.

--check re-verifies an existing seal and writes NOTHING. Run it after the seal to close F7.

NOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, the live board is untouched.
"""
import json, sys, hashlib, os, subprocess, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
RA = os.path.join(ROOT, 'engine', 'rl_after')
CHECK_ONLY = '--check' in sys.argv

HEAD = hashlib.md5(open(os.path.join(RA, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open(os.path.join(RA, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]


def stable(path):
    """The B3 stable-key seal, byte-for-byte the gate's own _b3_stable_sha (ship_gates_check.py:505)."""
    d = json.load(open(path)); by = {}
    for _idk, rec in d.items():
        if _idk.startswith('__'):
            continue
        by[(rec.get('player'), rec.get('type'), rec.get('year'), rec.get('pick'))] = rec
    h = hashlib.sha256()
    for k in sorted(by.keys(), key=lambda t: json.dumps(t, sort_keys=True)):
        h.update(json.dumps(k, sort_keys=True).encode())
        h.update(json.dumps(by[k], sort_keys=True, separators=(',', ':')).encode())
    return h.hexdigest(), by


print('=' * 100)
print('THE BAKE — BOOK RE-SEAL on the CANDIDATE LINE, GATE MODE%s' % ('  [--check, writes nothing]' if CHECK_ONLY else ''))
print('=' * 100)
print('  worktree      : %s' % ROOT)
print('  engine head   : %s   store: %s' % (HEAD, STORE))
print('  RL_V0SURF_PKL : <NOT SET — the in-repo pinned surface is now the default load path>')

_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_bake_', suffix='.json'); os.close(_fd)
env = {k: v for k, v in os.environ.items() if not k.startswith('SGC_')}
env.pop('RL_V0SURF_PKL', None)                      # prove the precedence fix through the re-seal too
env.update(S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           PYTHONPATH=RA + os.pathsep + ROOT + os.pathsep + os.path.join(ROOT, 'vendor'),
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')

print('\nregenerating the candidate matrix (gate mode, the 18 dials at their SHIPPED DEFAULTS) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env,
                   capture_output=True, text=True, timeout=1800)
meta = json.load(open(mpath)).get('__meta__', {}) if os.path.exists(mpath) else {}
if not meta:
    print('FAILED: no __meta__ (exit=%s)' % r.returncode)
    print('--- stdout tail ---\n%s' % r.stdout[-2500:])
    print('--- stderr tail ---\n%s' % r.stderr[-2500:])
    sys.exit(1)

eng, sto = meta.get('engine_head_md5', '')[:8], meta.get('store_md5', '')[:8]
cfg_meta = meta.get('config_sha256')
print('matrix meta   : engine=%s store=%s config=%s' % (eng, sto, str(cfg_meta)[:12]))
assert eng == HEAD, 'engine mismatch %s != %s' % (eng, HEAD)
assert sto == STORE, 'store mismatch %s != %s' % (sto, STORE)

seal_path = os.path.join(ROOT, 'data', 'book_stable_seal.json')
old = json.load(open(seal_path))
sha, by = stable(mpath)
cfg_full = json.load(open(os.path.join(ROOT, 'data', 'model_config.json'))).get('config_sha256')
if cfg_meta is not None and cfg_meta != cfg_full:
    print('HALT: matrix config %s != manifest config_sha256 %s' % (cfg_meta, cfg_full)); sys.exit(1)

print('\n  sealed (before): head %s store %s n %s stable %s'
      % (old.get('head_md5'), old.get('store_md5'), old.get('n_players'), str(old.get('stable_sha256'))[:16]))
print('  candidate      : head %s store %s n %s stable %s' % (HEAD, STORE, len(by), sha[:16]))

if CHECK_ONLY:
    ok = (old.get('stable_sha256') == sha and old.get('head_md5') == HEAD
          and old.get('store_md5') == STORE and old.get('n_players') == len(by)
          and old.get('config') == cfg_full)
    print('\n  B3 RE-VERIFY: %s' % ('PASS — the committed seal matches a freshly regenerated gate-mode '
                                    'candidate book, every field' if ok else 'FAIL — see the two lines above'))
    os.remove(mpath); sys.exit(0 if ok else 1)

seal = {
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-08-20 at THE BAKE (register v780, "
                 "docs/evidence/bake_2026-08-20; PREREG_BAKE.md pushed at 907b2da before the engine was "
                 "touched). The candidate's 18-dial stack is now the SHIPPED DEFAULT, wired DEFAULT-ON "
                 "behind DECLARED KILL-SWITCHES with data/model_config.json 'vars' DELIBERATELY UNMOVED "
                 "(the v2.9 RL_EVW/RL_CAPT/RL_ISOFADE/RL_PVC2 pattern), so under GATE MODE the manifest "
                 "line and the candidate line are THE SAME BOARD again and this seal is taken on the "
                 "candidate. That identity is what docs/evidence/landing_prep_2026-08-20/RESEAL_HALT.md "
                 "found missing when it halted this act; the defaults flip restores it. The book is "
                 "engine-ev()-derived and the O37..O43 stack moves ev(), so it is RE-BUILT on the "
                 "candidate engine (G-BOOK) and re-stamped, NOT re-hashed. store cb38ef11 and config "
                 "eed19a75 UNCHANGED. Each named kill-switch reproduces its historical board byte-exact. "
                 "CANDIDATE — owner tag/main promote owner-only. NOT ADOPTED, OWNER WORD PENDING."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD, "store_md5": STORE, "n_players": len(by), "stable_sha256": sha,
    "sealed_by": ("THE BAKE re-seal 2026-08-20 (docs/evidence/bake_2026-08-20/reseal_bake.py, a declared "
                  "3-change port of session_2026-07-17/legd_derivation/reseal_book.py; engine %s -> %s, "
                  "the defaults flip; store %s UNCHANGED; config %s UNMOVED). stable_sha256 %s -> %s "
                  "because the shipped default now prices the O37..O43 stack, which moves ev() and thus "
                  "the book's present and walk-forward columns. n_players re-counted, not carried. "
                  "Candidate — owner tag/main owner-only."
                  % (str(old.get('head_md5'))[:8], HEAD, STORE, str(cfg_full)[:8],
                     str(old.get('stable_sha256'))[:8], sha[:8])),
    "sealed_date": "2026-08-20", "config": cfg_full,
}
json.dump(seal, open(seal_path, 'w'), indent=2)
os.remove(mpath)
print('\nRE-SEALED: head %s -> %s | n_players %s -> %s | stable_sha256 %s -> %s'
      % (old.get('head_md5'), HEAD, old.get('n_players'), len(by),
         str(old.get('stable_sha256'))[:8], sha[:8]))
print('NOT ADOPTED. OWNER WORD PENDING.')
