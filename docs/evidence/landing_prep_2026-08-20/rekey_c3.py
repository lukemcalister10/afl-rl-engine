#!/usr/bin/env python3
"""C3 — THE SIX-PIN RE-KEY of data/expected_boot.json on land/order-29.

THE LAW OF THIS SCRIPT: the re-key changes PINS TO MATCH REALITY, never reality to match pins.
Every new value is COMPUTED from the branch tree here, in this process, by the SAME routine the
guard uses (md5 for files; config_manifest.manifest_hash for config; fv_provenance.fv_identity for
the forward-valuation source set). Nothing is typed in from the order or the register.

SURGICAL: the file is edited as RAW TEXT by exact-value replacement, each value asserted to occur
EXACTLY ONCE in the whole file before it is touched. json.load/json.dump is NEVER used to rewrite
it, so every note field, every key order and every byte of whitespace survives untouched. The
script re-reads the result and asserts that the ONLY bytes that differ are the pin values it
declared.

The six pins of C3 (register v767/v769). Each is TRACED, not trusted: a pin whose computed value
already equals the pinned value is REPORTED AS ALREADY-CORRECT and left alone.

  engine_head  engine/rl_after/_merged_recover.py            md5
  rl_model     engine/rl_after/rl_model.py                   md5
  board        data/rl_build/rl_app_data.json                md5   (Guard 5 (0c) asserts THIS copy)
  config       data/model_config.json via config_manifest    manifest_hash
  v0surf       data/v0surf.pkl                               md5
  fv           engine/forward_valuation/*.py source set      fv_identity (sha256 tree hash)

NOT ADOPTED. OWNER WORD PENDING. No tag, no main, the live board untouched.
"""
import os, sys, json, hashlib, shutil, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, ROOT)
PIN = os.path.join(ROOT, 'data', 'expected_boot.json')


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def compute():
    """Compute the branch tree's ACTUAL value for each of the six pins."""
    import config_manifest as cm
    import fv_provenance as fv
    return [
        ('engine_head', 'engine/rl_after/_merged_recover.py',
         md5(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py'))),
        ('rl_model', 'engine/rl_after/rl_model.py',
         md5(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py'))),
        ('board', 'data/rl_build/rl_app_data.json',
         md5(os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json'))),
        ('config', 'data/model_config.json (manifest_hash)', cm.manifest_hash(ROOT)),
        ('v0surf', 'data/v0surf.pkl',
         md5(os.path.join(ROOT, 'data', 'v0surf.pkl'))),
        ('fv', 'engine/forward_valuation (source-set tree hash)',
         fv.fv_identity(fv.checkout_fv_dir(ROOT))),
    ]


def main():
    apply_it = '--apply' in sys.argv
    raw = open(PIN, encoding='utf-8').read()
    exp = json.loads(raw)
    rows = compute()

    print('=' * 108)
    print('C3 SIX-PIN RE-KEY — land/order-29 @ %s' % subprocess.check_output(
        ['git', '-C', ROOT, 'rev-parse', '--short=7', 'HEAD']).decode().strip())
    print('  values COMPUTED from the branch tree in this process; nothing typed in from the order')
    print('=' * 108)
    print('%-13s %-46s %s' % ('PIN', 'SOURCE OF TRUTH (branch tree)', 'OLD -> NEW'))
    print('-' * 108)

    edits, unchanged = [], []
    for field, src, actual in rows:
        old = exp.get(field)
        if old is None:
            raise SystemExit('HALT: pin %r absent from the manifest' % field)
        if old == actual:
            unchanged.append((field, src, old))
            print('%-13s %-46s %s' % (field, src, old))
            print('%-13s %-46s %s' % ('', '', 'ALREADY CORRECT — pin == tree. NOT re-stamped.'))
        else:
            edits.append((field, src, old, actual))
            print('%-13s %-46s %s' % (field, src, old))
            print('%-13s %-46s -> %s   RE-STAMPED' % ('', '', actual))
        print('-' * 108)

    print('re-stamped: %d   already-correct: %d   total: %d'
          % (len(edits), len(unchanged), len(rows)))
    if not apply_it:
        print('\nDRY RUN — re-run with --apply to write.')
        return 0
    if not edits:
        print('\nnothing to write.')
        return 0

    # ---- surgical raw-text replacement, one value at a time, uniqueness asserted -------------
    shutil.copyfile(PIN, PIN + '.prerekey')
    new = raw
    for field, _src, old, actual in edits:
        n = new.count(old)
        if n != 1:
            raise SystemExit('HALT: old value for %r occurs %d times (expected exactly 1) — '
                             'refusing a non-surgical edit' % (field, n))
        new = new.replace(old, actual)
    open(PIN, 'w', encoding='utf-8').write(new)

    # ---- verify: JSON still valid, ONLY the declared pins moved, notes byte-identical --------
    after_raw = open(PIN, encoding='utf-8').read()
    after = json.loads(after_raw)
    moved = {k for k in set(exp) | set(after) if exp.get(k) != after.get(k)}
    declared = {f for f, _s, _o, _a in edits}
    if moved != declared:
        raise SystemExit('HALT: moved keys %r != declared %r' % (sorted(moved), sorted(declared)))
    for f, _s, _o, a in edits:
        if after[f] != a:
            raise SystemExit('HALT: %r did not take the computed value' % f)
    # byte-level proof that nothing but the pin values changed
    rebuilt = raw
    for _f, _s, o, a in edits:
        rebuilt = rebuilt.replace(o, a)
    if rebuilt != after_raw:
        raise SystemExit('HALT: byte-level drift beyond the declared value replacements')
    notes_moved = [k for k in after if k.startswith('_') and exp.get(k) != after.get(k)]
    if notes_moved:
        raise SystemExit('HALT: note fields moved: %r' % notes_moved)

    print('\nWRITE VERIFIED')
    print('  JSON valid                                  : yes')
    print('  keys whose value moved                      : %s' % sorted(moved))
    print('  keys declared to move                       : %s' % sorted(declared))
    print('  note fields (_*) moved                      : NONE (byte-for-byte preserved)')
    print('  key count before / after                    : %d / %d' % (len(exp), len(after)))
    print('  bytes before / after                        : %d / %d' % (len(raw), len(after_raw)))
    print('  byte-diff == exactly the declared values    : yes')
    print('\nNOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, live board untouched.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
