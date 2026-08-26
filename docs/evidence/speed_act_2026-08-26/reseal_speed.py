#!/usr/bin/env python3
"""THE SPEED ACT — THE BOOK RE-SEAL ON THE LANDED ORDER 45 TREE, GATE MODE, BARE SHIPPED LINE.

Owner words this act rides on, VERBATIM: "We can do B3 in the next set" (2026-08-25 — B3 carried out
of the ORDER 45 landing, falsifier 6 standing NOT DISCHARGED per prereg R-FIX5) and the standing
efficiency directive ("Parallelise. Load things once"), whose speed act this file belongs to.

WHAT THIS IS. docs/evidence/backrows_reseal_2026-08-20/reseal_backrows.py — the instrument that LAST
moved data/book_stable_seal.json — carried forward with ITS LOGIC UNCHANGED except ONE DECLARED
MECHANICAL CHANGE: the regeneration timeout rises 1800 -> 5400 seconds. That is not a style edit; it
is the reason this act exists. The arm-2 rebake (exact monotone band, feature dim 11 -> 12) made the
gate-mode matrix regeneration cost ~35 minutes where it used to cost ~3, which is why B1/B3 timed out
at the ORDER 45 ship-gates control run and why falsifier 6 could not be discharged that night. The
SAME raise is applied to ship_gates_check.py:382 in this act, so the sealer and the gate share one
ceiling. Every other line of the procedure, the hashing, the assertions and the --check path is
byte-identical to the instrument of record, because re-typing them could only weaken them.

WHAT THIS ACT IS CLOSING. The committed seal names engine 1867e953 / store b745002e / config
eed19a75 — the 2026-08-20 back-rows line, one full chapter back. Since then the ID-primary store
migration, the arm-2 rebake and the ORDER 45 net lever moved the tree to engine d84031cf / store
fb640ca0 / config 29fdfd1e (the LANDED board 3167cba6, owner's "Go", register v858) with no re-seal.
The pre-measured uncapped matrix (/home/user/arm2_norec/s4_cand_uncapped.json, ~35 min) already binds
exactly these three identities, so the ~35-minute regeneration below is expected to reproduce its
stable-key stamp; a divergence is a finding, not a formality.

WHAT THIS ACT IS *NOT* CLAIMING: s4_matrix_M1v7.py does not import rl_export.py — the board enters
only as the guard the book builds under (single_source.assert_startup), never as an input; and the
seal is a CANDIDATE stamp — tag/main promotion stays owner-only, as every seal in this lineage says.

--check re-verifies an existing seal and writes NOTHING; it is the certification path ship_gates B3
consumes at its next full run, which this act then executes for the falsifier-6 discharge.
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
print('SPEED ACT — THE BOOK RE-SEAL ON THE LANDED ORDER 45 TREE, BARE SHIPPED LINE, GATE MODE%s' % ('  [--check, writes nothing]' if CHECK_ONLY else ''))
print('=' * 100)
print('  worktree      : %s' % ROOT)
print('  engine head   : %s   store: %s' % (HEAD, STORE))
print('  RL_V0SURF_PKL : <NOT SET — the in-repo pinned surface is now the default load path>')

_fd, mpath = tempfile.mkstemp(prefix='s4_reseal_backrows_', suffix='.json'); os.close(_fd)
env = {k: v for k, v in os.environ.items() if not k.startswith('SGC_')}
env.pop('RL_V0SURF_PKL', None)                      # prove the precedence fix through the re-seal too
env.update(S4_MATRIX=mpath, RL_CONFIG_MODE='gate', RL_REPO=ROOT, PYTHONHASHSEED='0',
           PYTHONPATH=RA + os.pathsep + ROOT + os.pathsep + os.path.join(ROOT, 'vendor'),
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')

print('\nregenerating the book matrix (gate mode, BARE LINE — no env dials; the shipped defaults price it) ...')
r = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=env,
                   capture_output=True, text=True, timeout=5400)   # THE DECLARED CHANGE: arm-2 regen is ~35 min (see docstring)
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
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-08-26 in THE SPEED ACT, on the LANDED "
                 "ORDER 45 tree (board 3167cba6, owner word \"Go\", register v858; B3 carried on his word "
                 "\"We can do B3 in the next set\"). WHAT MOVED THE SEAL: the previous stamp (2026-08-20 "
                 "back-rows act) named engine 1867e953 / store b745002e / config eed19a75; the ID-primary "
                 "store migration, the arm-2 rebake and the ORDER 45 net lever moved the tree to engine "
                 "d84031cf / store fb640ca0 / config 29fdfd1e without a re-seal — the one-chapter lag "
                 "release_manifest_check.py reports as sealed-lag. The book is engine-ev()-derived, so it is "
                 "RE-BUILT on the landed engine and store and re-stamped, NOT re-hashed; n_players "
                 "RE-COUNTED, never carried. Certification on the BARE SHIPPED LINE, gate mode, no env "
                 "dials. THE ONE MECHANICAL CHANGE in this lineage copy: regeneration ceiling 1800 -> 5400s "
                 "(the arm-2 exact-monotone band made the regen ~35 min — the measured cause of the ORDER 45 "
                 "B1/B3 timeouts), applied identically to ship_gates_check.py. HONEST SCOPE NOTE unchanged: "
                 "s4_matrix_M1v7.py does not import rl_export.py; the board enters as the guard, not an "
                 "input. CANDIDATE — owner tag/main promote owner-only."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD, "store_md5": STORE, "n_players": len(by), "stable_sha256": sha,
    "sealed_by": ("SPEED ACT re-seal 2026-08-26 (docs/evidence/speed_act_2026-08-26/reseal_speed.py; "
                  "docs/evidence/backrows_reseal_2026-08-20/reseal_backrows.py carried with its logic "
                  "UNCHANGED except the DECLARED 1800->5400s regeneration ceiling; owner words \"We can do "
                  "B3 in the next set\" + the standing efficiency directive). engine %s -> %s and store "
                  "%s -> %s and config -> %s, all moved by the store migration / arm-2 rebake / ORDER 45 "
                  "net lever without a re-seal. stable_sha256 %s -> %s and n_players %s -> %s, RE-COUNTED "
                  "not carried. Certified by the same instrument's --check against a freshly regenerated "
                  "gate-mode book, then by ship_gates B3 at its next full run. Candidate — owner tag/main "
                  "owner-only."
                  % (str(old.get('head_md5'))[:8], HEAD, str(old.get('store_md5'))[:8], STORE,
                     str(cfg_full)[:8], str(old.get('stable_sha256'))[:8], sha[:8],
                     old.get('n_players'), len(by))),
    "sealed_date": "2026-08-26", "config": cfg_full,
}
json.dump(seal, open(seal_path, 'w'), indent=2)
os.remove(mpath)
print('\nRE-SEALED: head %s -> %s | n_players %s -> %s | stable_sha256 %s -> %s'
      % (old.get('head_md5'), HEAD, old.get('n_players'), len(by),
         str(old.get('stable_sha256'))[:8], sha[:8]))
print('NOT ADOPTED. OWNER WORD PENDING.')
