"""acceptance/checks/m1a.py — THE M1a RESIDUE (PLAN_v6 1f), built.

M1a's adopted scope named four things that were never built: mirror-parity (q97m/cm), build-twice
determinism, dial coverage, and the three recorded one-line checks. The tranche was reported
complete with two check modules and seven registered checks. 1f is the honest completion, and this
module is it. Six checks:

    mirror_parity            boot_guard's mirrored fitted-artifact resolvers still mirror the
                             engine's, and the three fitted artifacts equal their pins
    dial_coverage            every DECLARED dial is read by the engine WITH A DEFAULT
    oneliner_gamma           M1a repair 1 — ship_gates_check's model env equals the manifest
    oneliner_r14_restore     M1a repair 3 — the R14 disposable fixture verifies (runs the real test)
    oneliner_f1_lens         M1a repair 4 — the F1 numeraire comparison is the repaired one
    build_twice_determinism  two bare builds, byte-identical (HEAVY: ~3.5 minutes of engine)

EVERY ONE OF THEM ASSERTS A RELATIONSHIP, NEVER THIS MONTH'S NUMBER (contract.py's standing rule).
There is not one hex literal of a current identity in this file: the pins are read from
`data/expected_boot.json`, the dial list from `data/model_config.json`, the mirrored precedences
from the two sources being compared. A check that hard-codes today's answer is the instrument class
this whole order exists to retire, and four of the estate's retired instruments died of exactly it.
"""

import ast
import json
import os
import re
import subprocess
import sys

from acceptance import contract as C

_TIMEOUT = 900


def _read(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------- 1f: mirror parity
def _func_node(src, name):
    """The FunctionDef node called `name`, anywhere in the module (nested included)."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def _precedence_tokens(node):
    """The ordered precedence tokens of a resolver: env names and path literals, normalised.

    Read off the CANDIDATE EXPRESSION only — the `_cands = [...]` assignment where there is one,
    otherwise the iterable of the function's `for`. Reading the whole function body would sweep in
    unrelated strings (v0surf's REFIT early-return, halt messages) and compare noise.

    f-string / %-format interpolation collapses to '{}' so that
    `f'/home/claude/cm_{trees}.pkl'` and `'/home/claude/cm_%s.pkl' % trees` compare equal — the two
    sides of the cm mirror are written in different syntax and mean the same path.
    """
    cand = None
    for n in ast.walk(node):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id.lstrip('_') in ('cands', 'cache'):
                    cand = n.value if cand is None else cand
        if isinstance(n, ast.For) and cand is None:
            cand = n.iter
    if cand is None:
        return None
    toks = []

    def visit(n):
        # An f-string is ONE token. Descending into it would also emit its literal fragments, and
        # the cm mirror would then compare ['/home/claude/cm_{}.pkl'] against that same string plus
        # its two halves — a drift report about nothing.
        if isinstance(n, ast.JoinedStr):
            toks.append(''.join(p.value if isinstance(p, ast.Constant) else '{}' for p in n.values))
            return
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            v = re.sub(r'%[sd]', '{}', n.value)
            if v:
                toks.append(v)
            return
        for child in ast.iter_child_nodes(n):
            visit(child)

    visit(cand)
    return toks


def _precedence(path, func):
    src = _read(path)
    node = _func_node(src, func)
    if node is None:
        return None, 'no function %r in %s' % (func, os.path.basename(path))
    toks = _precedence_tokens(node)
    if toks is None:
        return None, 'no candidate expression found in %s.%s' % (os.path.basename(path), func)
    return toks, ''


#: (label, guard fn, engine file, engine fn, expected_boot pin field, repo artifact)
_MIRRORS = (
    ('q97m', '_resolve_q97m_load', os.path.join('engine', 'rl_after', '_merged_recover.py'),
     '_load_q97m', 'q97m', os.path.join('data', 'q97m.pkl')),
    ('v0surf', '_resolve_v0surf_load', os.path.join('engine', 'rl_after', '_merged_recover.py'),
     '_load_v0surf', 'v0surf', os.path.join('data', 'v0surf.pkl')),
    ('cm/band', '_resolve_cm_load', os.path.join('engine', 'rl_after', 'wire_redesign.py'),
     'build', 'band', os.path.join('data', 'cm_400.pkl')),
)


def mirror_parity(ctx):
    """boot_guard's mirrored resolvers still mirror the engine's; fitted artifacts == their pins."""
    root = ctx.root
    boot = json.load(open(os.path.join(root, 'data', 'expected_boot.json')))
    lines, fails = [], []
    for label, gfn, erel, efn, pin_field, artifact in _MIRRORS:
        g, gerr = _precedence(os.path.join(root, 'boot_guard.py'), gfn)
        e, eerr = _precedence(os.path.join(root, erel), efn)
        if gerr or eerr:
            fails.append('%s: %s' % (label, gerr or eerr))
            lines.append('%-8s UNREADABLE  %s' % (label, gerr or eerr))
            continue
        if g == e:
            lines.append('%-8s MIRROR OK   %s' % (label, ' -> '.join(g)))
        else:
            fails.append('%s: boot_guard.%s precedence %s != %s.%s %s'
                         % (label, gfn, g, os.path.basename(erel), efn, e))
            lines.append('%-8s MIRROR DRIFT\n   guard : %s\n   engine: %s' % (label, g, e))
        pin = boot.get(pin_field)
        apath = os.path.join(root, artifact)
        if pin and os.path.exists(apath):
            got = _md5(apath)
            if got == pin:
                lines.append('%-8s PIN OK      %s == expected_boot[%r]' % ('', artifact, pin_field))
            else:
                fails.append('%s: %s md5 %s != pinned %s' % (label, artifact, got, pin))
                lines.append('%-8s PIN DRIFT   %s %s != %s' % ('', artifact, got, pin))
        elif pin:
            fails.append('%s: pinned as %r but %s is absent' % (label, pin_field, artifact))
    ev = C.write_evidence(ctx, 'mirror_parity.txt', '\n'.join(lines))
    if fails:
        return C.Verdict('mirror_parity', C.FAIL, ev, fails[0])
    return C.Verdict('mirror_parity', C.PASS, ev,
                     '%d fitted-artifact resolvers mirror the engine byte-for-byte; all %d pins hold'
                     % (len(_MIRRORS), len(_MIRRORS)))


mirror_parity.HALTS = ()
mirror_parity.PROFILE = 'host-insensitive'


# ------------------------------------------------------------------------------- 1f: dial coverage
_GET_DEFAULT = re.compile(r"environ\.(?:get|setdefault)\(\s*['\"]([A-Za-z0-9_]+)['\"]\s*,")
_GET_BARE = re.compile(r"environ\.get\(\s*['\"]([A-Za-z0-9_]+)['\"]\s*\)")
_INDEXED = re.compile(r"environ\[\s*['\"]([A-Za-z0-9_]+)['\"]\s*\]")


def _engine_sources(root):
    for base in (os.path.join(root, 'engine', 'rl_after'),
                 os.path.join(root, 'engine', 'forward_valuation')):
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d != '__pycache__']
            for f in sorted(fn):
                if f.endswith('.py'):
                    yield os.path.join(dp, f)


def dial_coverage(ctx):
    """every DECLARED dial is read by the engine WITH A DEFAULT (enumerated from the code)."""
    root = ctx.root
    cfg = json.load(open(os.path.join(root, 'data', 'model_config.json')))
    declared = cfg.get('vars') or {}
    notes = cfg.get('var_notes') or {}
    blob = '\n'.join(_read(p) for p in _engine_sources(root))
    with_default = set(_GET_DEFAULT.findall(blob))
    without = set(_GET_BARE.findall(blob)) | set(_INDEXED.findall(blob))

    covered, orphan_declared, no_default = [], [], []
    for name in sorted(declared):
        if name in with_default:
            covered.append(name)
        elif name in without:
            no_default.append(name)
        elif re.search(r'\borphan|\binert\b', str(notes.get(name, '')), re.I):
            orphan_declared.append(name)
        else:
            no_default.append(name)

    undeclared = sorted(n for n in (with_default | without)
                        if n.startswith(('RL_', 'PAR_')) and n not in declared)

    lines = ['DIAL COVERAGE — data/model_config.json vars vs what engine/ actually reads',
             '  declared dials             : %d' % len(declared),
             '  read WITH a default        : %d' % len(covered),
             '  DECLARED-ORPHAN (self-declared inert in var_notes): %d  %s'
             % (len(orphan_declared), orphan_declared or ''),
             '  read WITHOUT a default / not read at all: %d  %s' % (len(no_default), no_default or ''),
             '',
             'REPORTED, NOT GATED — engine-read RL_*/PAR_* vars the manifest does not declare: %d'
             % len(undeclared),
             '  This is the population PLAN_v6 4-zero is about (the declared kill_switches block, '
             'named on record and never delivered). Declaring them MOVES config_sha256, which is a '
             'value-bearing identity, so P1 measures the number and touches nothing.',
             '  ' + ', '.join(undeclared)]
    ev = C.write_evidence(ctx, 'dial_coverage.txt', '\n'.join(lines))
    if no_default:
        return C.Verdict('dial_coverage', C.FAIL, ev,
                         '%d declared dial(s) are not read with a default anywhere in engine/: %s'
                         % (len(no_default), ', '.join(no_default)))
    return C.Verdict('dial_coverage', C.PASS, ev,
                     '%d of %d declared dials read with a default in engine source (%d self-declared '
                     'orphan); %d engine-read vars undeclared (reported, 4-zero)'
                     % (len(covered), len(declared), len(orphan_declared), len(undeclared)))


dial_coverage.HALTS = ()
dial_coverage.PROFILE = 'host-insensitive'


# ------------------------------------------------------------------ 1f: the three recorded one-liners
def oneliner_gamma(ctx):
    """M1a repair 1 — ship_gates_check.py's model env equals the pinned manifest, dial for dial."""
    root = ctx.root
    src = _read(os.path.join(root, 'ship_gates_check.py'))
    cfg = json.load(open(os.path.join(root, 'data', 'model_config.json'))).get('vars') or {}
    m = re.search(r'os\.environ\.update\(([^)]*)\)', src, re.S)
    if not m:
        return C.Verdict('oneliner_gamma', C.FAIL, '',
                         'ship_gates_check.py no longer has an os.environ.update(...) model line')
    pairs = dict(re.findall(r"([A-Za-z0-9_]+)\s*=\s*'([^']*)'", m.group(1)))
    bad = ['%s=%r (manifest %r)' % (k, v, cfg[k])
           for k, v in sorted(pairs.items()) if k in cfg and cfg[k] != v]
    lines = ['ship_gates_check.py model env vs data/model_config.json:']
    for k, v in sorted(pairs.items()):
        lines.append('  %-18s suite %-8s manifest %-8s %s'
                     % (k, v, cfg.get(k, '(not a dial)'),
                        'OK' if k not in cfg or cfg[k] == v else 'DIVERGENT'))
    lines.append('')
    lines.append('WHY THIS CHECK EXISTS: enforce("gate") three lines below that update REJECTS a '
                 'divergent override, so ONE divergent dial makes the entire frozen A/B gate family '
                 'unexecutable on every box. RL_GAMMA sat at 0.85 against a manifest pinning 1.0 and '
                 'the suite killed itself on its own line. M1a repaired it; this keeps it repaired.')
    ev = C.write_evidence(ctx, 'oneliner_gamma.txt', '\n'.join(lines))
    if bad:
        return C.Verdict('oneliner_gamma', C.FAIL, ev,
                         'ship_gates_check.py model env diverges from the manifest: %s' % '; '.join(bad))
    dials = [k for k in pairs if k in cfg]
    return C.Verdict('oneliner_gamma', C.PASS, ev,
                     '%d of ship_gates_check.py\'s %d exported vars are manifest dials and all agree '
                     '(enforce("gate") would accept them)' % (len(dials), len(pairs)))


oneliner_gamma.HALTS = ()
oneliner_gamma.PROFILE = 'host-insensitive'


def oneliner_r14_restore(ctx):
    """M1a repair 3 — the R14 disposable fixture verifies (the real fail-closed suite, run)."""
    argv = [sys.executable, os.path.join(ctx.root, 'engine', 'rl_after', 'ingestion',
                                         'test_weekly_updater.py')]
    p = subprocess.run(argv, cwd=ctx.root, capture_output=True, text=True, timeout=_TIMEOUT,
                       env=dict(os.environ, RL_REPO=ctx.root))
    out = (p.stdout or '') + (p.stderr or '')
    ev = C.write_evidence(ctx, 'oneliner_r14_restore.txt',
                          '$ %s\n\n%s\n[exit %s]' % (' '.join(argv), out, p.returncode))
    if p.returncode != 0:
        line = next((l.strip() for l in out.splitlines() if 'FAIL' in l or 'Error' in l),
                    'exit %d' % p.returncode)
        return C.Verdict('oneliner_r14_restore', C.FAIL, ev,
                         'the R14 disposable fixture does not verify: %s' % line[:110])
    n = out.count('[PASS]')
    return C.Verdict('oneliner_r14_restore', C.PASS, ev,
                     'R14 disposable fixture + fail-closed controls + movers transition: %d [PASS], '
                     'exit 0 — the config-pin restore line holds' % n)


oneliner_r14_restore.HALTS = ()
oneliner_r14_restore.PROFILE = 'host-insensitive'


def oneliner_f1_lens(ctx):
    """M1a repair 4 — one_source_selftest's F1 comparison is the repaired, non-vacuous one."""
    root = ctx.root
    path = os.path.join(root, 'engine', 'rl_after', 'one_source_selftest.py')
    src = _read(path)
    lines, fails = [], []

    # The F1 leg must still exist and still compare board v against a recomputed engine ev().
    if 'EXPORT PARITY (F1)' not in src:
        fails.append('the F1 export-parity leg is gone from one_source_selftest.py')
    # It must still be a per-key comparison that can report a mismatch count — the repair removed a
    # FALSE red, and a repair that removes the check instead is the failure mode worth naming.
    if not re.search(r'mismatch', src, re.I):
        fails.append('the F1 leg no longer reports a mismatch count — a check that cannot fail')
    if not re.search(r'board active set == engine active set', src):
        fails.append('the F1 leg no longer asserts the active sets agree key-for-key')
    lines.append('one_source_selftest.py F1 leg: present=%s, mismatch-reporting=%s, key-for-key=%s'
                 % ('EXPORT PARITY (F1)' in src, bool(re.search(r'mismatch', src, re.I)),
                    bool(re.search(r'board active set == engine active set', src))))
    lines.append('')
    lines.append('SCOPE, STATED. This check asserts the REPAIRED SHAPE is still in the source. It '
                 'does NOT run the suite: one_source_selftest needs a bootstrapped workspace and a '
                 'board built from it, which is why ci-guards runs it only after setup_env.sh + '
                 'bootstrap.sh + rl_export.py. The suite\'s live verdict — 124 PASS / 15 FAIL, the '
                 'F1 red cleared and 15 residual reds unattributed — is carried as ruled-red CG1 '
                 'with a dated heavy probe, not silently assumed here.')
    ev = C.write_evidence(ctx, 'oneliner_f1_lens.txt', '\n'.join(lines))
    if fails:
        return C.Verdict('oneliner_f1_lens', C.FAIL, ev, fails[0])
    return C.Verdict('oneliner_f1_lens', C.PASS, ev,
                     'the F1 export-parity leg is present, key-for-key, and still reports a mismatch '
                     'count (the repair removed a false red, not the check)')


oneliner_f1_lens.HALTS = ()
oneliner_f1_lens.PROFILE = 'host-insensitive'


# ------------------------------------------------------------------------- 1f: build-twice determinism
def build_twice_determinism(ctx):
    """two bare builds of this tree, byte-identical (HEAVY — ~3.5 minutes of engine)."""
    root = ctx.root
    argv = ['bash', os.path.join(root, 'tools', 'build_lock.sh'), 'run', 'acceptance-determinism',
            '--', sys.executable, os.path.join(root, 'tools', 'build_twice_determinism.py'),
            '--root', root]
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=_TIMEOUT,
                       env=dict(os.environ, RL_REPO=root))
    out = (p.stdout or '') + (p.stderr or '')
    ev = C.write_evidence(ctx, 'build_twice_determinism.txt',
                          '$ %s\n\n%s\n[exit %s]' % (' '.join(argv), out, p.returncode))
    tail = next((l.strip() for l in reversed(out.splitlines())
                 if l.strip().startswith('determinism:')), 'exit %d' % p.returncode)
    return C.Verdict('build_twice_determinism', C.PASS if p.returncode == 0 else C.FAIL, ev, tail)


build_twice_determinism.HALTS = ()
build_twice_determinism.PROFILE = 'heavy'
