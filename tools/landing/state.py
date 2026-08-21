"""tools/landing/state.py — THE STATE FILE'S ONLY WRITER (PLAN_v6 3c).

    python3 -m tools.landing.state              print what would be written (no write)
    python3 -m tools.landing.state write        write docs/STATE.md
    python3 -m tools.landing.state check        exit 0 iff docs/STATE.md == a regeneration

GENERATED-ONLY, AND THE PREDECESSOR IS THE ARGUMENT. Process law P6 says a derived surface that
cannot be generated does not exist, and it names its own incident: `docs/CURRENT_STATE.md` carried
an authority banner ("IF THIS FILE AND THE REGISTER DISAGREE, THE REGISTER IS RIGHT"), was written
by the one seat whose job it was, and still sat 156 register versions stale at review time. A banner
is not a writer. This module is the writer, the landing sequence is the trigger, and
`acceptance::state_file` is the falsifier that says so out loud when the two disagree.

EVERY VALUE IS COMPUTED, NONE IS TYPED. The identities are read out of the carriers that already
hold them — `data/expected_boot.json`, `data/release_contract.json`, the config manifest,
`data/release_lineage.json`, `docs/register/LATEST.md` — and, where the artifact is in the tree, the
file is HASHED and the pin is checked against the hash rather than reprinted. That is process law
P4 in the one place it is easiest to breach: a state file whose identities were transcribed would be
a hand-typed identity in a document that claims to be current, which is the exact instrument the
estate has retired four times.

WHY THE GENERATION STAMP NAMES A COMMIT AND CARRIES NO CLOCK. `generated_at_commit` is the tree
HEAD at the moment of generation. In a landing that is the commit BEFORE the landing commit — the
state file is written inside the transaction and committed by it, so the commit that CARRIES this
file is the stamped commit's child, and the stamp names the tree the values were read from, which is
the honest fact. There is deliberately NO timestamp: a wall clock in a generated file makes every
regeneration differ from every other, which would leave `check()` with nothing to compare and this
whole file back where CURRENT_STATE.md was. `check()` therefore regenerates HOLDING THE RECORDED
COMMIT and compares byte-for-byte, and separately asserts the recorded commit is a real ancestor of
HEAD — so the one field it cannot re-derive is still not free.

NO VARIABLE THIS MODULE SETS CARRIES AN `RL_` OR `PAR_` PREFIX. The rule is written down in
`carriers.py`'s header after the estate paid for it twice: `config_manifest.enforce()` rejects an
unknown RL_-prefixed variable as a divergent model override, and the prefix leaks into every child a
tool spawns. This module sets no environment at all, which is the cheapest way to obey it.
"""

import hashlib
import json
import os
import subprocess
import sys

STATE_REL = os.path.join('docs', 'STATE.md')

#: The tool of record, printed in the stamp. One name, so a reader can find the writer.
TOOL = 'tools/landing/state.py'

#: Written into the stamp so a reader knows which entry point produced this copy.
GENERATORS = ('land lever (step `state`)', 'land round (step `state`)',
              'python3 -m tools.landing.state write')


class StateError(RuntimeError):
    """The state file could not be GENERATED. P6: then it does not exist — never a partial file."""


# --------------------------------------------------------------------------------------- helpers
def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _read_json(root, rel):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise StateError('%s is not in the tree — the state file cannot be generated from it' % rel)
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except ValueError as e:
        raise StateError('%s is not readable JSON (%s)' % (rel, e))


def _git(root, *args):
    p = subprocess.run(('git',) + args, cwd=root, capture_output=True, text=True)
    return p.returncode, (p.stdout or '').strip(), (p.stderr or '').strip()


def head_commit(root):
    rc, out, err = _git(root, 'rev-parse', 'HEAD')
    if rc != 0 or not out:
        raise StateError('cannot read HEAD in %s (%s)' % (root, err or 'no output'))
    return out


def _measured(root, rel):
    """The md5 of a tree artifact, or None where this tree does not carry it."""
    path = os.path.join(root, rel)
    return _md5(path) if os.path.isfile(path) else None


def _agree(pin, measured):
    """The one-word verdict a row carries. Never a bare tick: the two values are printed beside it."""
    if measured is None:
        return 'not in tree'
    return 'agrees' if pin == measured else 'DRIFTED'


def _config_manifest_hash(root):
    """The manifest hash, computed by the tree's OWN config_manifest.py — never re-implemented.

    Imported by path under a root-unique module name for the same reason `steps._load` does it: the
    self-test drives sandboxes and the live tree from processes that may share an interpreter, and a
    cached module from the wrong root is a silent cross-tree read.
    """
    import importlib.util
    path = os.path.join(root, 'config_manifest.py')
    if not os.path.isfile(path):
        return None, 'config_manifest.py is not in this tree'
    key = 'state_config_manifest__%s' % hashlib.md5(root.encode()).hexdigest()[:8]
    mod = sys.modules.get(key)
    if mod is None:
        spec = importlib.util.spec_from_file_location(key, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[key] = mod
        spec.loader.exec_module(mod)
    return mod.manifest_hash(root), None


def _rulebook_lint(root):
    """-> (verdict, headline). The laws pointer carries the LINT'S OWN verdict, read off its exit code.

    P5: a gate's name is not coverage. Naming `docs/RULEBOOK.md` here without its lint verdict would
    be a pointer claiming a gate; the verdict is what makes it a reading.
    """
    lint = os.path.join(root, 'tools', 'rulebook_lint.py')
    if not os.path.isfile(lint):
        return 'ABSENT', 'tools/rulebook_lint.py is not in this tree'
    p = subprocess.run([sys.executable, lint, root], cwd=root, capture_output=True, text=True,
                       timeout=120)
    out = (p.stdout or '') + (p.stderr or '')
    head = ''
    for ln in out.splitlines():
        if ln.strip().startswith('rulebook_lint:'):
            head = ln.strip()
            break
    if not head:
        head = (out.strip().splitlines() or ['(no output)'])[-1].strip()
    # THE HEADLINE IS MADE HOST-INDEPENDENT, and that is not cosmetic: the lint prints the absolute
    # tree it ran against, and a generated file carrying an absolute path is a file that changes
    # when the checkout moves — a difference the freshness gate would report as staleness in a tree
    # nothing had happened to. The verdict is the fact; the path is this box's.
    cut = head.find('(tree ')
    if cut != -1:
        head = head[:cut].strip()
    return ('PASS' if p.returncode == 0 else 'FAIL'), head[:160]


def _first_line(root, rel):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise StateError('%s is not in the tree — the record pointer cannot be generated' % rel)
    with open(path, encoding='utf-8') as fh:
        for ln in fh:
            ln = ln.rstrip('\n')
            if ln.strip():
                return ln
    raise StateError('%s line 1 is empty — SILENCE IS A RED (RULEBOOK PART 1 law 2)' % rel)


def _clip(s, n):
    s = ' '.join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + '…'


# ----------------------------------------------------------------------------------------- facts
def facts(root):
    """Every fact the state file states, COMPUTED. -> dict. Raises StateError if one cannot be got."""
    root = os.path.abspath(root)
    boot = _read_json(root, os.path.join('data', 'expected_boot.json'))
    contract = _read_json(root, os.path.join('data', 'release_contract.json'))
    lineage = _read_json(root, os.path.join('data', 'release_lineage.json'))
    cid = contract.get('identities') or {}

    board_rel = os.path.join('data', 'rl_build', 'rl_app_data.json')
    store_rel = os.path.join('engine', 'rl_after', 'rl_model_data.json')
    head_rel = os.path.join('engine', 'rl_after', '_merged_recover.py')
    model_rel = os.path.join('engine', 'rl_after', 'rl_model.py')

    manifest_hash, manifest_note = _config_manifest_hash(root)
    lint_verdict, lint_head = _rulebook_lint(root)

    reg = lineage.get('release_transition_register') or []
    tip = reg[-1] if reg else {}
    tip_dest = tip.get('destination') or {}
    tip_src = tip.get('source') or {}
    applies = tip.get('applies_to') or {}
    boundary = applies.get('boundary') or []

    rb_rel = os.path.join('docs', 'RULEBOOK.md')
    latest_rel = os.path.join('docs', 'register', 'LATEST.md')
    entries_dir = os.path.join(root, 'docs', 'register', 'entries')
    n_entries = len([f for f in os.listdir(entries_dir) if f.endswith('.md')]) \
        if os.path.isdir(entries_dir) else 0

    return {
        'identities': [
            # (name, pinned value, the carrier it was read from, the artifact re-hashed, measured)
            ('board', boot.get('board'), 'data/expected_boot.json', board_rel,
             _measured(root, board_rel)),
            ('store', boot.get('store'), 'data/expected_boot.json', store_rel,
             _measured(root, store_rel)),
            ('engine_head', boot.get('engine_head'), 'data/expected_boot.json', head_rel,
             _measured(root, head_rel)),
            ('rl_model', boot.get('rl_model'), 'data/expected_boot.json', model_rel,
             _measured(root, model_rel)),
            ('balanced_board_md5', boot.get('balanced_board_md5'), 'data/expected_boot.json',
             None, None),
            ('config', boot.get('config'), 'data/expected_boot.json', 'config_manifest.manifest_hash',
             manifest_hash),
        ],
        'manifest_note': manifest_note,
        'contract': {
            'contract_sha256': contract.get('contract_sha256'),
            'config_sha256': contract.get('config_sha256'),
            'release_version': contract.get('release_version'),
            'as_of_round': contract.get('as_of_round'),
            'board': cid.get('board'),
            'store': cid.get('store'),
            'engine_head': cid.get('engine_head'),
            'balanced_board_md5': cid.get('balanced_board_md5'),
            'held_checks': len(contract.get('held_checks') or []),
        },
        'boot': {
            'as_of_round': boot.get('as_of_round'),
            'release_version': boot.get('release_version'),
        },
        'laws': {
            'path': rb_rel.replace(os.sep, '/'),
            'md5': _measured(root, rb_rel),
            'header': _first_line(root, rb_rel) if os.path.isfile(os.path.join(root, rb_rel)) else '',
            'lint_verdict': lint_verdict,
            'lint_headline': lint_head,
        },
        'record': {
            'path': latest_rel.replace(os.sep, '/'),
            'line1': _first_line(root, latest_rel),
            'entries': n_entries,
            'frozen': 'docs/OPEN_ITEMS_REGISTER.md',
            'frozen_md5': _measured(root, os.path.join('docs', 'OPEN_ITEMS_REGISTER.md')),
        },
        'lineage': {
            'entries': len(reg),
            'column': (boundary[1] if len(boundary) > 1 else None),
            'after_round': (boundary[0] if boundary else None),
            'source_board': tip_src.get('board'),
            'destination_board': tip_dest.get('board'),
            'owner_ruling_id': ', '.join(tip.get('owner_ruling_id') or []) or None,
            'moved': ', '.join(tip.get('moved_by_transition') or []) or None,
        },
    }


# --------------------------------------------------------------------------------------- render
def render(root, generating_commit):
    """The state file's bytes. A PURE function of (tree, commit) — no clock, no environment."""
    f = facts(root)
    L = []
    a = L.append

    a('# STATE — GENERATED-ONLY · DO-NOT-HAND-EDIT')
    a('')
    a('> **THIS FILE IS MACHINE-WRITTEN AND REGENERATED AT EVERY LANDING.** The landing library')
    a('> writes it as a late step of both sequences (`land lever` and `land round`, step `state`);')
    a('> `python3 -m tools.landing.state write` regenerates it on demand. Every value below is')
    a('> COMPUTED from the carrier named beside it — nothing here is typed, and nothing here is')
    a('> authored. **Do not hand-edit:** an edit is overwritten at the next landing, and')
    a('> `acceptance::state_file` reds the tree before then.')
    a('>')
    a('> **This file states no law and settles no dispute.** The laws are `docs/RULEBOOK.md`; the')
    a('> record is `docs/register/`; the identities of record are the carriers. Where this file and')
    a('> a carrier disagree, the carrier is right and this file is stale — which is a red, not a')
    a('> footnote (process law P6: a derived surface that cannot be generated does not exist).')
    a('')

    a('## CURRENT IDENTITIES')
    a('')
    a('Pinned value from the carrier, beside the artifact re-hashed in this tree. `agrees` is a')
    a('measurement made while this file was written, not a claim carried over from the last one.')
    a('')
    a('| identity | pinned value | carrier | re-hashed from | verdict |')
    a('|---|---|---|---|---|')
    for name, pin, carrier, artifact, meas in f['identities']:
        art = artifact.replace(os.sep, '/') if artifact else '(no in-tree artifact)'
        a('| %s | `%s` | %s | %s | %s |'
          % (name, pin or '(absent)', carrier, art, _agree(pin, meas)))
    if f['manifest_note']:
        a('')
        a('note: %s' % f['manifest_note'])
    a('')
    c = f['contract']
    a('| release fact | value | carrier |')
    a('|---|---|---|')
    a('| contract seal | `%s` | data/release_contract.json:contract_sha256 |' % c['contract_sha256'])
    a('| config seal | `%s` | data/release_contract.json:config_sha256 |' % c['config_sha256'])
    a('| release version | %s | data/release_contract.json:release_version |' % c['release_version'])
    a('| round (as_of_round) | %s | data/release_contract.json:as_of_round |' % c['as_of_round'])
    a('| round (as_of_round) | %s | data/expected_boot.json:as_of_round |' % f['boot']['as_of_round'])
    a('| declared held checks | %d | data/release_contract.json:held_checks |' % c['held_checks'])
    a('')
    a('BOOT vs CONTRACT, computed here rather than assumed: board %s · store %s · engine_head %s · '
      'balanced %s · round %s.'
      % (_pair(f['identities'][0][1], c['board']), _pair(f['identities'][1][1], c['store']),
         _pair(f['identities'][2][1], c['engine_head']),
         _pair(f['identities'][4][1], c['balanced_board_md5']),
         _pair(f['boot']['as_of_round'], c['as_of_round'])))
    a('')

    a('## THE LAWS')
    a('')
    a('The single governing document, and its own lint\'s verdict — a pointer without a verdict is a')
    a('gate claimed by name (process law P5).')
    a('')
    a('- **%s** — md5 `%s`' % (f['laws']['path'], f['laws']['md5'] or '(absent)'))
    a('- header: %s' % _clip(f['laws']['header'], 150))
    a('- `tools/rulebook_lint.py` verdict: **%s** — %s'
      % (f['laws']['lint_verdict'], _clip(f['laws']['lint_headline'], 150)))
    a('')

    a('## THE RECORD')
    a('')
    r = f['record']
    a('- **%s**, line 1, quoted:' % r['path'])
    a('')
    a('  > %s' % _clip(r['line1'], 400))
    a('')
    a('- new-form entries under `docs/register/entries/`: %d' % r['entries'])
    a('- frozen predecessor `%s` — md5 `%s` (byte-sealed; `tools/seat/pen.py verify` is its gate)'
      % (r['frozen'], r['frozen_md5'] or '(absent)'))
    a('')

    a('## LINEAGE TIP')
    a('')
    ln = f['lineage']
    a('`data/release_lineage.json` — the append-only out-of-round transition register, %d entries.'
      % ln['entries'])
    a('')
    a('| field | value |')
    a('|---|---|')
    a('| column | %s |' % (ln['column'] or '(none)'))
    a('| after round | %s |' % (ln['after_round'] or '(none)'))
    a('| board moved | `%s` → `%s` |' % (ln['source_board'] or '?', ln['destination_board'] or '?'))
    a('| identities moved | %s |' % (ln['moved'] or '(none)'))
    a('| owner ruling id | %s |' % _clip(ln['owner_ruling_id'] or '(none)', 200))
    a('')

    a('## GENERATION STAMP')
    a('')
    a('| field | value |')
    a('|---|---|')
    a('| generated at commit | `%s` |' % generating_commit)
    a('| tool | `%s` |' % TOOL)
    a('| written by | %s |' % ' · '.join(GENERATORS))
    a('| freshness gate | `acceptance::state_file` — regenerates this file on the current tree and '
      'compares byte-for-byte |')
    a('')
    a('The stamped commit is the tree HEAD the values above were READ FROM. In a landing that is the')
    a('commit before the landing commit: this file is written inside the transaction and committed')
    a('by it, so the commit carrying these bytes is the stamped commit\'s child. There is no')
    a('timestamp by design — a clock would make every regeneration differ from every other and')
    a('leave the freshness gate nothing to compare.')
    a('')
    return '\n'.join(L) + '\n'


def _pair(a, b):
    """'agree' / 'DIFFER (x vs y)' — printed, never asserted here; the manifest gate owns the halt."""
    if a == b:
        return 'agree'
    return 'DIFFER (%s vs %s)' % (a, b)


# ---------------------------------------------------------------------------------- write / check
def write(root, generating_commit=None):
    """Generate and install docs/STATE.md. -> (rel path, md5, changed)."""
    root = os.path.abspath(root)
    commit = generating_commit or head_commit(root)
    text = render(root, commit)
    path = os.path.join(root, STATE_REL)
    before = _measured(root, STATE_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    after = _md5(path)
    return STATE_REL.replace(os.sep, '/'), after, before != after


_STAMP_PREFIX = '| generated at commit | `'


def recorded_commit(root):
    """The commit stamped into the state file on disk, or None if there is no readable stamp."""
    path = os.path.join(root, STATE_REL)
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as fh:
        for ln in fh:
            if ln.startswith(_STAMP_PREFIX):
                return ln[len(_STAMP_PREFIX):].split('`')[0].strip()
    return None


def check(root):
    """-> [problems]. Empty means docs/STATE.md IS a regeneration of the current tree.

    THE ONE FIELD THAT CANNOT BE RE-DERIVED IS STILL NOT FREE. The regeneration holds the stamped
    commit (a fresh `rev-parse HEAD` would differ from it by construction the moment the landing
    commit lands), and the stamped commit is then asserted to be a real commit AND an ancestor of
    HEAD. A stamp naming a commit this history does not contain is a hand-edit, and says so.
    """
    root = os.path.abspath(root)
    path = os.path.join(root, STATE_REL)
    if not os.path.isfile(path):
        return ['%s is ABSENT. It is generated at every landing; regenerate it with '
                '`python3 -m tools.landing.state write`.' % STATE_REL.replace(os.sep, '/')]
    commit = recorded_commit(root)
    if not commit:
        return ['%s carries no generation stamp — it was not written by %s'
                % (STATE_REL.replace(os.sep, '/'), TOOL)]

    problems = []
    rc, _out, _err = _git(root, 'cat-file', '-e', commit + '^{commit}')
    if rc != 0:
        problems.append('the generation stamp names commit %s, which is not a commit in this '
                        'repository — the stamp was hand-edited' % commit)
    else:
        rc2, _o, _e = _git(root, 'merge-base', '--is-ancestor', commit, 'HEAD')
        if rc2 != 0:
            problems.append('the generation stamp names commit %s, which is not an ancestor of HEAD '
                            '— this state file was generated on a tree this one does not descend '
                            'from' % commit)

    try:
        expect = render(root, commit)
    except StateError as e:
        return problems + ['the state file CANNOT be regenerated from this tree (%s). Under process '
                           'law P6 it therefore does not exist, and the copy on disk is a fossil.' % e]
    with open(path, encoding='utf-8') as fh:
        actual = fh.read()
    if actual != expect:
        problems.append('%s does NOT match a regeneration of this tree — %s'
                        % (STATE_REL.replace(os.sep, '/'), _first_difference(actual, expect)))
    return problems


def _first_difference(actual, expect):
    """The first differing line, named. A diff verdict that does not say WHERE is not diagnosable."""
    a_lines, e_lines = actual.splitlines(), expect.splitlines()
    for i in range(max(len(a_lines), len(e_lines))):
        av = a_lines[i] if i < len(a_lines) else '(file ends)'
        ev = e_lines[i] if i < len(e_lines) else '(file ends)'
        if av != ev:
            return 'first difference at line %d: on disk %r, regenerated %r' \
                % (i + 1, _clip(av, 90), _clip(ev, 90))
    return 'the files differ only in trailing bytes'


# ------------------------------------------------------------------------------------------- cli
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    verb = 'print'
    root = os.environ.get('RL_REPO') or os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    rest = []
    for tok in argv:
        if tok in ('write', 'check', 'print'):
            verb = tok
        else:
            rest.append(tok)
    if rest and rest[0] == '--root' and len(rest) > 1:
        root = rest[1]
    elif rest:
        root = rest[0]

    if verb == 'print':
        sys.stdout.write(render(root, head_commit(root)))
        return 0
    if verb == 'write':
        rel, md5, changed = write(root)
        print('state: wrote %s  md5 %s  (%s)'
              % (rel, md5, 'CHANGED' if changed else 'byte-identical to what was there'))
        return 0
    problems = check(root)
    if not problems:
        print('state: PASS — %s is a regeneration of this tree (stamp %s)'
              % (STATE_REL.replace(os.sep, '/'), (recorded_commit(root) or '?')[:12]))
        return 0
    print('state: %d FAIL' % len(problems))
    for p in problems:
        print('  FAIL %s' % p)
    return 1


if __name__ == '__main__':
    sys.exit(main())
