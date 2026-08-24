#!/usr/bin/env python3
"""ARM 2 — THE CANDIDATE ROOT, extending ARM 1's pattern by exactly one pin. SCRATCH ONLY.

WHY AN EXTENSION AND NOT A REWRITE
  ARM 1's make_candidate_root.py is FILED EVIDENCE and is not edited here. It copies the checkout to a
  scratch root, puts the candidate ARTIFACTS at the pinned artifact paths, re-pins expected_boot.json
  from them (measured, never typed) and re-pins fv. That is exactly right for an arm whose only moving
  parts are artifacts.

  ARM 2 moves one more thing: THE ENGINE HEAD. The design arm edits _merged_recover.py (the ratchet
  retirement, the two artifact-contract halts, the age-hill inference path), and data/expected_boot.json
  pins that file's md5 as 'engine_head'. Guard 5's stale-boot block asserts it on entry — and it FIRED,
  correctly, the first time this seat ran ship_gates_check against the ARM 1-shaped root:
      md5 53ce2fb7 != expected 3af8c1f7 (pinned; repo checkout)
  That is the guard doing its job. The answer is not to bypass it but to give the candidate world a
  COHERENT engine pin, exactly as ARM 1 gave it coherent artifact pins, so the whole Guard 5 chain runs
  HONESTLY against the candidate instead of being skipped.

  The re-pin is MEASURED from the root's own engine file, never typed. rl_model.py is re-pinned the same
  way but is expected to be unmoved — it is included so that a future arm that does touch it cannot
  discover this gap the way this one did.

  The worktree's committed data/expected_boot.json stays byte-untouched throughout; that is verified
  separately by byte_unmoved.py.

Usage: make_candidate_root_arm2.py --root <checkout> --out <scratch root> [--cm ...] [--q97m ...]
                                   [--peak ...] [--pvc ...] [--arm1-script <path>]
"""
import argparse, hashlib, json, os, subprocess, sys


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--cm'); ap.add_argument('--q97m')
    ap.add_argument('--peak'); ap.add_argument('--pvc')
    ap.add_argument('--arm1-script', default=None)
    a = ap.parse_args(argv[1:])

    arm1 = a.arm1_script or os.path.join(
        a.root, 'docs', 'evidence', 'rebake_arm1_store_alone_2026-08-24', 'scripts',
        'make_candidate_root.py')
    cmd = [sys.executable, arm1, '--root', a.root, '--out', a.out]
    for flag, val in (('--cm', a.cm), ('--q97m', a.q97m), ('--peak', a.peak), ('--pvc', a.pvc)):
        if val:
            cmd += [flag, val]
    print('--- ARM 1 candidate-root pattern (unchanged, reused) ---')
    r = subprocess.run(cmd, text=True)
    if r.returncode != 0:
        raise SystemExit('make_candidate_root_arm2 HALT: the ARM 1 root builder exited %d' % r.returncode)

    print('--- ARM 2 extension: the ENGINE HEAD pin ---')
    out = os.path.abspath(a.out)
    boot_path = os.path.join(out, 'data', 'expected_boot.json')
    boot = json.load(open(boot_path))
    moved = {}
    for field, rel in (('engine_head', os.path.join('engine', 'rl_after', '_merged_recover.py')),
                       ('rl_model', os.path.join('engine', 'rl_after', 'rl_model.py'))):
        p = os.path.join(out, rel)
        new = md5(p)                                    # MEASURED from the file in THIS root (P4)
        old = boot.get(field)
        if new != old:
            boot[field] = new
            moved[field] = (old, new, rel)
            print('  %-12s %s  %s -> %s' % (field, rel, str(old)[:8], new[:8]))
        else:
            print('  %-12s %s  UNMOVED (%s)' % (field, rel, str(old)[:8]))
    boot['_arm2_note'] = (
        'REBAKE ARM 2 CANDIDATE ROOT, 2026-08-24 — A SCRATCH ARTEFACT, NOT A PIN MOVE. In addition to '
        "ARM 1's artifact re-pins, engine_head is re-pinned here because the design arm edits "
        '_merged_recover.py (the ORDER 44 retirement and the two artifact-contract halts). Guard 5\'s '
        'stale-boot block asserts that pin on entry and FIRED against an un-extended root — this makes '
        'the candidate world coherent so the guard runs honestly rather than being bypassed. The '
        "committed data/expected_boot.json is byte-untouched; the real re-pins are owed at the LANDING "
        'act, on the owner\'s word, through tools/land lever.')
    with open(boot_path, 'w') as f:
        json.dump(boot, f, indent=2, ensure_ascii=False)
        f.write('\n')
    with open(os.path.join(out, 'ARM2_CANDIDATE_ROOT.json'), 'w') as f:
        json.dump({'source_checkout': os.path.abspath(a.root), 'engine_pins_moved': moved},
                  f, indent=1, sort_keys=True)
        f.write('\n')
    print('ARM 2 candidate root ready: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
