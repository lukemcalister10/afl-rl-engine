#!/usr/bin/env python3
"""L5 DOCKET HEADLINE, MEASURED — manifest value vs code default, for every RL_* the manifest pins.

THE RULING THIS SERVES (Addendum I.2):

  > For every `RL_*` the manifest pins, the landing asserts `manifest value == code default` — or
  > removes the default so the read fails loud.

WHY IT EXISTS. `rl_model.py:504` read `os.environ.get('RL_GAMMA','0.85')` while the manifest had
moved to 1.0. The board builds under bake mode (manifest); the selftest runs plainly (code default).
At baseline both said 0.85 and the gate passed. Under L1 the manifest moved and the default did not,
so the gate recomputed the entire board at SCAR against a VOR board — 666 of 804 mismatches. That
site was in NONE of the three enumerations that had been made.

This script is the census the ruling asks for. It reports, it does not fix: writing the assertion (or
removing the defaults) is a LANDING act.

Run from the repo root:  python3 docs/evidence/.../L5_census/manifest_vs_default.py
"""
import json, os, re, sys, collections

REPO = os.getcwd()
MANIFEST = os.path.join(REPO, 'data', 'model_config.json')

# Every place a default can be introduced for an RL_* name.
PATTERNS = [
    (re.compile(r"""os\.environ\.get\(\s*['"](RL_[A-Z0-9_]+)['"]\s*,\s*['"]([^'"]*)['"]"""), 'environ.get'),
    (re.compile(r"""os\.environ\.setdefault\(\s*['"](RL_[A-Z0-9_]+)['"]\s*,\s*['"]([^'"]*)['"]"""), 'setdefault'),
    (re.compile(r"""getenv\(\s*['"](RL_[A-Z0-9_]+)['"]\s*,\s*['"]([^'"]*)['"]"""), 'getenv'),
    (re.compile(r"""^\s*export\s+(RL_[A-Z0-9_]+)=['"]?([^\s'"]*)"""), 'shell export'),
]

SCAN_EXT = ('.py', '.sh')
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'backups', 'docs'}


def scan():
    found = collections.defaultdict(list)   # name -> [(path, line, kind, default)]
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in files:
            if not fn.endswith(SCAN_EXT):
                continue
            p = os.path.join(root, fn)
            try:
                lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for rx, kind in PATTERNS:
                    for m in rx.finditer(line):
                        found[m.group(1)].append(
                            (os.path.relpath(p, REPO), i, kind, m.group(2)))
    return found


def main():
    man = json.load(open(MANIFEST))
    pinned = {k: str(v) for k, v in (man.get('vars') or {}).items() if k.startswith('RL_')}
    found = scan()

    agree, disagree, no_default, not_pinned = [], [], [], []
    for name, want in sorted(pinned.items()):
        sites = found.get(name, [])
        if not sites:
            no_default.append((name, want))
            continue
        for path, line, kind, got in sites:
            rec = (name, want, got, path, line, kind)
            (agree if str(got) == str(want) else disagree).append(rec)
    for name in sorted(found):
        if name not in pinned:
            not_pinned.append((name, found[name]))

    n_pin = len(pinned)
    print('MANIFEST-vs-CODE-DEFAULT CENSUS  (I.2)')
    print('  manifest: %s' % os.path.relpath(MANIFEST, REPO))
    print('  RL_* pinned by the manifest — THE DENOMINATOR : %d' % n_pin)
    print('  of those, with at least one code default      : %d' % (n_pin - len(no_default)))
    print('  of those, with NO code default (read fails loud or is always supplied): %d'
          % len(no_default))
    print()
    print('  DEFAULT SITES for pinned names : %d' % (len(agree) + len(disagree)))
    print('     AGREE with the manifest     : %d' % len(agree))
    print('     DISAGREE                    : %d   <- each one is a latent basis fork' % len(disagree))
    if disagree:
        print()
        print('  THE DISAGREEMENTS, by name:')
        for name, want, got, path, line, kind in sorted(disagree):
            print('     %-22s manifest %-10s code default %-10s  %s:%d (%s)'
                  % (name, want, got, path, line, kind))
    print()
    print('  RL_* with a code default but NOT pinned by the manifest : %d' % len(not_pinned))
    for name, sites in not_pinned[:40]:
        p, l, k, g = sites[0]
        print('     %-24s default %-12s %s:%d%s'
              % (name, g, p, l, ('  (+%d more)' % (len(sites) - 1)) if len(sites) > 1 else ''))
    print()
    print('  READING IT: a DISAGREEMENT is the rl_model.py:504 shape exactly — bake mode takes the')
    print('  manifest, a plain run takes the default, and nothing asserts they agree. A name with no')
    print('  default is the STRONGER remedy I.2 allows (the read fails loud). A name with a default')
    print('  but no manifest pin is outside I.2 but worth seeing: nothing pins it at all.')
    print()
    print('  REPORTED, NOT FIXED. Writing the assertion or removing the defaults is a LANDING act.')

    json.dump({'denominator_pinned_RL_vars': n_pin,
               'agree': [list(x) for x in agree],
               'disagree': [list(x) for x in disagree],
               'pinned_without_code_default': [list(x) for x in no_default],
               'code_default_without_manifest_pin': {k: [list(s) for s in v] for k, v in not_pinned}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'manifest_vs_default.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
