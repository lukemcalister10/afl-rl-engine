#!/usr/bin/env python3
"""ARM 1 — BUILD A CANDIDATE ROOT (scratch only; the committed checkout is never modified).

WHY A CANDIDATE ROOT AND NOT A SWITCH-PER-ARTIFACT
  Guard 5 is designed so a board CANNOT be built on an unpinned fitted artifact: block (0d) asserts
  every fitted artifact in the CHECKOUT against data/expected_boot.json, and block (0e) asserts the md5
  of the file the engine will actually LOAD against the same pin. That is exactly right and this arm does
  not weaken it. It also means a candidate board can only be built honestly against a COHERENT candidate
  world — candidate artifacts AND their pins together.

  So: copy the checkout to a scratch root, put the candidate artifacts at the pinned artifact paths
  THERE, re-pin THAT root's expected_boot.json from the artifacts (measured, never typed — P4), and
  point RL_REPO/RL_FV at it. The worktree's own data/expected_boot.json, live pickles, release contract
  and /home/claude/cm_400.pkl are byte-untouched throughout, and that is verified separately.

  data/rl_build/rl_app_data.json and the 'board' pin are left ALONE: block (0c) asserts the checked-out
  board file against its pin, and the live board is the correct baseline for a candidate run to be
  measured against.

Usage:
  python3 make_candidate_root.py --root <checkout> --out <scratch root> \
      [--cm PKL] [--q97m PKL] [--peak PKL] [--pvc JSON]
  Omitted artifacts stay at their live bytes (so a one-artifact attribution root is a one-flag change).
"""
import argparse, hashlib, json, os, shutil, sys


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
    a = ap.parse_args(argv[1:])
    root, out = os.path.abspath(a.root), os.path.abspath(a.out)
    if out.startswith(root + os.sep) or out == root:
        raise SystemExit('make_candidate_root HALT: --out must be OUTSIDE the checkout.')
    if os.path.exists(out):
        shutil.rmtree(out)
    print('copying checkout -> %s' % out)
    shutil.copytree(root, out, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'),
                    symlinks=True)

    # make everything writable (the tier-1/2 stamps set files read-only)
    for dp, _, fs in os.walk(out):
        for f in fs:
            p = os.path.join(dp, f)
            try:
                os.chmod(p, 0o644)
            except OSError:
                pass

    swaps = [('band', a.cm, os.path.join('data', 'cm_400.pkl'), None),
             ('q97m', a.q97m, os.path.join('data', 'q97m.pkl'), None),
             ('peak_model', a.peak, os.path.join('engine', 'rl_after', 'peak_model_v4.pkl'),
              'peak_model_v4.pkl'),
             ('pvc_snapshot', a.pvc, os.path.join('engine', 'rl_after', 'pvc_snapshot.json'),
              'pvc_snapshot.json')]

    boot_path = os.path.join(out, 'data', 'expected_boot.json')
    boot = json.load(open(boot_path))
    moved = {}
    for field, src, rel, tier2 in swaps:
        if not src:
            continue
        dst = os.path.join(out, rel)
        old = boot.get(field)
        shutil.copyfile(os.path.abspath(src), dst)
        new = md5(dst)                                 # MEASURED from the artifact (P4)
        boot[field] = new
        moved[field] = (old, new, rel)
        if tier2:                                      # keep the tier-2 own_md5 stamp truthful
            sp = dst + '.srcmd5'
            if os.path.exists(sp):
                s = json.load(open(sp))
                s['own_md5'] = new
                s['note'] = (s.get('note', '') +
                             ' | ARM 1 CANDIDATE ROOT 2026-08-24: re-stamped from the candidate artifact '
                             'in a SCRATCH root; the committed stamp is untouched.')
                json.dump(s, open(sp, 'w'))
        print('  %-13s %s  %s -> %s' % (field, rel, str(old)[:8], new[:8]))

    # the forward-valuation source-set identity moves with any edit under engine/forward_valuation
    sys.path.insert(0, out)
    import fv_provenance as fp
    fvid = fp.fv_identity(fp.checkout_fv_dir(out))
    if fvid != boot.get('fv'):
        print('  %-13s engine/forward_valuation  %s -> %s' % ('fv', str(boot.get('fv'))[:8], fvid[:8]))
        moved['fv'] = (boot.get('fv'), fvid, 'engine/forward_valuation/*.py')
        boot['fv'] = fvid

    boot['_arm1_note'] = (
        'REBAKE ARM 1 CANDIDATE ROOT, 2026-08-24 — A SCRATCH ARTEFACT, NOT A PIN MOVE. The committed '
        'data/expected_boot.json is byte-untouched. These fields are re-pinned here, measured from the '
        'candidate artifacts, ONLY so Guard 5 can run honestly against a coherent candidate world '
        'instead of being bypassed. The live board moves once, at week\'s end, on the owner\'s word, '
        'through tools/land lever.')
    with open(boot_path, 'w') as f:
        json.dump(boot, f, indent=2, ensure_ascii=False)
        f.write('\n')
    with open(os.path.join(out, 'ARM1_CANDIDATE_ROOT.json'), 'w') as f:
        json.dump({'source_checkout': root, 'moved_pins': moved}, f, indent=1, sort_keys=True)
        f.write('\n')
    print('candidate root ready: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
