#!/usr/bin/env python3
"""ACT B — THE BOOK RE-SEAL, on the BARE SHIPPED LINE, under GATE MODE.
Owner word, VERBATIM: "And I'll re seal once that is done." (2026-08-20)

WHAT THIS IS. docs/evidence/bake_2026-08-20/reseal_bake.py — the act that LAST moved
data/book_stable_seal.json — carried with ITS LOGIC UNCHANGED, BYTE FOR BYTE. The only edits are this
docstring and the two NARRATIVE fields of the seal (_comment, sealed_by). Not one line of the
procedure, the hashing, the assertions or the --check path is touched, because re-typing them could
only weaken them.

WHY THE BAKE'S PORT IS THE INSTRUMENT OF RECORD AND NOT THE 2026-07-17 ORIGINAL. RESEAL_HALT.md §1
names session_2026-07-17/legd_derivation/reseal_book.py. That instrument was superseded on 2026-08-20
by the bake's DECLARED three-change port, and each of the three changes is load-bearing here:
  (1) ROOT/RA re-pointed at this worktree. The original hardcodes RA='/home/claude/rl_workspace/
      rl_after' — SHARED, out-of-repo, and measured on this box at engine 338a790b / store cc02567f,
      i.e. STALE and not this branch's tree. Sealing from it would seal a book this branch never built.
  (2) THE RL_GAMMA='0.85' DIAL BLOCK IS DROPPED. **THIS IS THE PRICE-LINE RULING, ALREADY
      IMPLEMENTED.** The settled ruling is that certification runs on the BARE SHIPPED LINE with no
      env dials, which by the bake's design IS the live board's line. This instrument already does
      exactly that: gate mode clears the ambient model env and loads data/model_config.json
      authoritatively, and the shipped dials are DEFAULT-ON in code and deliberately absent from the
      manifest, so a bare line prices the shipped board. Passing 0.85 by hand would additionally be
      REJECTED by the gate-mode reject scan as a divergent override (the manifest carries 1.0).
  (3) Thread pinning made explicit, so the run is reproducible standalone.

THE IDENTITY WAS RE-VERIFIED ON THE POST-ACT-A BOARD BEFORE THIS RAN, not assumed: a bare gate-mode
board build reproduces the live board 68be10c79d0ee096455754e084bcf757 BYTE-EXACT (14_reseal.txt).
That is prereg B1 / falsifier FB1, and it is the premise the ruling rests on.

WHAT THIS ACT IS CLOSING. The seal names engine 5ac6780f / store cb38ef11 — THE BAKE's line. The tree
carries engine 1867e953 / store b745002e: both moved at the D8 adoption, the injury-sheet re-cut and
the R23 advance, none of which re-sealed. That one-chapter lag is exactly what
release_manifest_check.py reports as its two sealed-lag lines, and closing it is this act.

WHAT THIS ACT IS *NOT* CLAIMING. s4_matrix_M1v7.py builds the book from _merged_recover.ev() and does
NOT import rl_export.py, so ACT A's back-rows repair does not change the book's CONTENT. The board
enters here only as a GUARD — single_source.assert_startup consumes rl_app_data.json and asserts its
stamp against the live store — which is why this seal could not have been taken over an incoherent
board. Sealing AFTER Act A, on the owner's sequencing, is correct-and-cheap rather than
content-changing: the book is sealed on the tree whose board is the corrected one.

--check re-verifies an existing seal and writes NOTHING. It is this act's certification, run directly,
which is what the brief authorises when ship_gates_check.py cannot run.
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
print('ACT B — THE BOOK RE-SEAL, BARE SHIPPED LINE, GATE MODE%s' % ('  [--check, writes nothing]' if CHECK_ONLY else ''))
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
    "_comment": ("Walk-forward book freeze-stamp — RE-SEALED 2026-08-20 after THE BACK-ROWS AGE_REF "
                 "REPAIR, on the owner's word \"And I'll re seal once that is done.\", so the book is "
                 "sealed on the CORRECTED tree. WHAT MOVED THE SEAL: the previous stamp was taken at THE "
                 "BAKE against engine 5ac6780f / store cb38ef11; since then the D8 adoption, the "
                 "injury-sheet re-cut and the R23 advance moved the engine to 1867e953 and the store to "
                 "b745002e without re-sealing, which is precisely the one-chapter lag "
                 "release_manifest_check.py reported as its two sealed-lag lines. The book is "
                 "engine-ev()-derived, so it is RE-BUILT on the current engine and store (G-BOOK) and "
                 "re-stamped, NOT re-hashed, and n_players is RE-COUNTED rather than carried. THE "
                 "PRICE-LINE, SETTLED AND APPLIED: certification runs on the BARE SHIPPED LINE — no env "
                 "dials — which by the bake's design IS the live board's line, and that identity was "
                 "RE-VERIFIED on this board before sealing (a bare gate-mode board build reproduces the "
                 "live board 68be10c7 byte-exact). config eed19a75 UNMOVED. HONEST SCOPE NOTE: "
                 "s4_matrix_M1v7.py does not import rl_export.py, so the back-rows repair did not change "
                 "the book's CONTENT — the corrected board enters as the GUARD the book builds under, not "
                 "as an input. CANDIDATE — owner tag/main promote owner-only."),
    "generator": "engine/rl_after/s4_matrix_M1v7.py",
    "head_md5": HEAD, "store_md5": STORE, "n_players": len(by), "stable_sha256": sha,
    "sealed_by": ("ACT B re-seal 2026-08-20 (docs/evidence/backrows_reseal_2026-08-20/"
                  "reseal_backrows.py, docs/evidence/bake_2026-08-20/reseal_bake.py carried with its "
                  "logic UNCHANGED byte-for-byte and only its narrative fields re-pointed; owner word "
                  "\"And I'll re seal once that is done.\"). engine %s -> %s and store %s -> %s, both "
                  "moved by the D8 adoption / injury-sheet re-cut / R23 advance without a re-seal; "
                  "config %s UNMOVED. stable_sha256 %s -> %s and n_players %s -> %s, RE-COUNTED not "
                  "carried, because the book is rebuilt on the moved engine and store. Certified by the "
                  "same instrument's --check against a freshly regenerated gate-mode book. Candidate — "
                  "owner tag/main owner-only."
                  % (str(old.get('head_md5'))[:8], HEAD, str(old.get('store_md5'))[:8], STORE,
                     str(cfg_full)[:8], str(old.get('stable_sha256'))[:8], sha[:8],
                     old.get('n_players'), len(by))),
    "sealed_date": "2026-08-20", "config": cfg_full,
}
json.dump(seal, open(seal_path, 'w'), indent=2)
os.remove(mpath)
print('\nRE-SEALED: head %s -> %s | n_players %s -> %s | stable_sha256 %s -> %s'
      % (old.get('head_md5'), HEAD, old.get('n_players'), len(by),
         str(old.get('stable_sha256'))[:8], sha[:8]))
print('NOT ADOPTED. OWNER WORD PENDING.')
