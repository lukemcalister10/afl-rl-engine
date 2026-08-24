#!/usr/bin/env python3
"""tools/inbox_manifest.py — the owner-inputs PROVENANCE MANIFEST (PLAN_v6 1d), generated.

    python3 tools/inbox_manifest.py write     regenerate docs/inputs/incoming/MANIFEST.md (+ .json)
    python3 tools/inbox_manifest.py check     exit 1 if the committed manifest is out of date

THE ONE CANONICAL SOURCE, DECLARED. Two locations in this tree hold the owner's inputs, and until
now nothing said which one anything reads:

    scores/ (and its runbook-named siblings)   THE INGEST LOCATION. CANONICAL. Every tool, runbook
                                               and workflow that reads an owner input reads it from
                                               here — `round_entry catchup --file 23=scores/R23.csv`,
                                               R23_RUNBOOK.md:55 "Save it as scores/R23.csv".
    docs/inputs/incoming/                      THE PROVENANCE ARCHIVE. EXPLICITLY SECONDARY. Nothing
                                               reads it. It records that a file arrived, when, why,
                                               and WHICH CANONICAL COPY IT BECAME.

The manifest NAMES THE CANONICAL COPY for every archived file, by content. That is the whole job:
before this, two byte-identical R23.csv files sat in the tree with nothing declaring which was the
input of record, and a reader had to guess. Now the archive points at the ingest location and says
so in its own generated header.

THE DUPLICATION IS NOT RETIRED, AND THAT IS A CHOICE, NOT AN OVERSIGHT (REVIEW_COLD_OPUS O2). Git
already versions `scores/`, so the archive retires nothing under G4 — it is a declared hierarchy
rather than an unowned second source. It is kept anyway for one reason worth stating: the archive
records the file AS DELIVERED, with its arrival date and purpose, and `scores/` records it as
INGESTED. When those two ever differ, the difference is the finding, and there is nowhere else in
the tree that difference would show up. A CANONICAL-COPY MISMATCH IS A HARD FAILURE of `check`.

GENERATED-ONLY. Hand-appending to this manifest is how it becomes CURRENT_STATE.md. The per-file
PURPOSE — the one thing no hash can derive — lives in `docs/inputs/incoming/purposes.json`, a small
declared sidecar; everything else on the page is computed on every regeneration.
"""

import argparse
import hashlib
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

INCOMING_REL = os.path.join('docs', 'inputs', 'incoming')
MANIFEST_MD = 'MANIFEST.md'
MANIFEST_JSON = 'manifest.json'
PURPOSES = 'purposes.json'

#: The CANONICAL ingest locations, in search order. A file archived in `incoming/` is expected to
#: have become a copy in one of these.
CANONICAL_DIRS = ('scores', os.path.join('docs', 'owner_annotations'))

_GENERATED = (MANIFEST_MD, MANIFEST_JSON, PURPOSES)


def _git_arrival_date(path):
    """The date the file FIRST ENTERED THE REPOSITORY (its earliest commit's author date,
    YYYY-MM-DD) — deterministic in every checkout. The previous source, filesystem mtime, was a
    P4-class defect inside an acceptance check: a fresh clone stamps every file with checkout time,
    so `check` went red on any new container while asserting nothing about the input itself
    (register v836-era finding; the repair was queued at v833). Falls back to the epoch sentinel
    '1970-01-01' only if git cannot answer, which `check` will then surface as a diff."""
    import subprocess
    try:
        out = subprocess.run(['git', '-C', _ROOT, 'log', '--follow', '--format=%as', '--', path],
                             capture_output=True, text=True, timeout=30)
        dates = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
        if dates:
            return dates[-1]
    except Exception:
        pass
    return '1970-01-01'


def _hashes(path):
    m, s = hashlib.md5(), hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            m.update(chunk)
            s.update(chunk)
    return m.hexdigest(), s.hexdigest()


def _canonical_index(root):
    """content md5 -> [relpath] over every canonical ingest location."""
    idx = {}
    for d in CANONICAL_DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            p = os.path.join(base, name)
            if os.path.isfile(p):
                idx.setdefault(_hashes(p)[0], []).append(os.path.join(d, name).replace(os.sep, '/'))
    return idx


def scan(root):
    """-> (rows, problems). One row per archived file."""
    inc = os.path.join(root, INCOMING_REL)
    purposes = {}
    ppath = os.path.join(inc, PURPOSES)
    if os.path.exists(ppath):
        purposes = json.load(open(ppath, encoding='utf-8'))
    idx = _canonical_index(root)
    rows, problems = [], []
    if not os.path.isdir(inc):
        return rows, ['%s does not exist' % INCOMING_REL]
    for name in sorted(os.listdir(inc)):
        if name in _GENERATED or name.startswith('.'):
            continue
        p = os.path.join(inc, name)
        if not os.path.isfile(p):
            continue
        md5, sha = _hashes(p)
        canon = idx.get(md5) or []
        row = {'file': name,
               'md5': md5,
               'sha256': sha,
               'bytes': os.path.getsize(p),
               'arrived': _git_arrival_date(p),
               'purpose': purposes.get(name, {}).get('purpose', ''),
               'delivered_by': purposes.get(name, {}).get('delivered_by', ''),
               'canonical_copy': canon[0] if canon else None,
               'canonical_copies_all': canon}
        if not canon:
            problems.append('%s: NO canonical copy — an archived input that never became an input '
                            'of record. The archive is secondary; a file that exists only here has '
                            'not been ingested.' % name)
        if not row['purpose']:
            problems.append('%s: no purpose declared in %s/%s — a hash cannot derive why a file '
                            'arrived, so it is the one field that must be written down.'
                            % (name, INCOMING_REL, PURPOSES))
        rows.append(row)
    return rows, problems


HEADER = """<!-- GENERATED-ONLY — DO NOT HAND-EDIT. Regenerate: python3 tools/inbox_manifest.py write
     CI/runner assert it is current: python3 tools/inbox_manifest.py check
     Hand-appending to this file is how it becomes docs/CURRENT_STATE.md, which carried an
     authority banner and sat 156 register versions stale. -->

# OWNER INPUTS — PROVENANCE ARCHIVE

**`scores/` (and its runbook-named siblings) IS THE CANONICAL INGEST LOCATION.** Every tool,
runbook and workflow that reads an owner input reads it from there
(`round_entry catchup --file 23=scores/R23.csv`; `docs/runbooks/R23_RUNBOOK.md:55` — *"Save it as
`scores/R23.csv`"*).

**`docs/inputs/incoming/` IS THE PROVENANCE ARCHIVE, AND IT IS EXPLICITLY SECONDARY.** Nothing
reads it. It records that a file arrived, when, why, and — the column that removes the ambiguity —
**which canonical copy it became**.

The duplication is a declared choice, not an oversight: git already versions `scores/`, so this
archive **retires nothing** under G4. It is kept because it records the file *as delivered* while
`scores/` records it *as ingested*, and the day those two differ, the difference is the finding and
there is nowhere else it would show. A canonical-copy mismatch fails `check`.
"""


def render_md(root, rows, problems):
    out = [HEADER, '', '## Files', '',
           '| file | md5 | sha256 (prefix) | bytes | arrived | canonical copy | purpose |',
           '|---|---|---|---|---|---|---|']
    for r in rows:
        out.append('| `%s` | `%s` | `%s…` | %d | %s | %s | %s |'
                   % (r['file'], r['md5'], r['sha256'][:16], r['bytes'], r['arrived'],
                      ('`%s`' % r['canonical_copy']) if r['canonical_copy'] else '**NONE**',
                      r['purpose'] or '**undeclared**'))
    if not rows:
        out.append('| *(the archive is empty)* | | | | | | |')
    out.append('')
    if problems:
        out.append('## Problems (this manifest reports them; `check` exits non-zero on them)')
        out.append('')
        for p in problems:
            out.append('- %s' % p)
        out.append('')
    out.append('---')
    out.append('')
    out.append('Regenerated by `tools/inbox_manifest.py`. Canonical locations searched, in order: %s.'
               % ', '.join('`%s/`' % d.replace(os.sep, '/') for d in CANONICAL_DIRS))
    return '\n'.join(out) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('mode', choices=('write', 'check'))
    ap.add_argument('--root', default=os.environ.get('RL_REPO') or _ROOT)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    rows, problems = scan(root)
    md = render_md(root, rows, problems)
    js = json.dumps({'canonical_ingest_dirs': [d.replace(os.sep, '/') for d in CANONICAL_DIRS],
                     'archive_dir': INCOMING_REL.replace(os.sep, '/'),
                     'archive_is_secondary': True,
                     'files': rows,
                     'problems': problems}, indent=2, sort_keys=True) + '\n'
    mdp = os.path.join(root, INCOMING_REL, MANIFEST_MD)
    jsp = os.path.join(root, INCOMING_REL, MANIFEST_JSON)

    if a.mode == 'write':
        open(mdp, 'w', encoding='utf-8').write(md)
        open(jsp, 'w', encoding='utf-8').write(js)
        print('wrote %s and %s (%d file(s), %d problem(s))'
              % (mdp, jsp, len(rows), len(problems)))
        for p in problems:
            print('  problem: %s' % p)
        return 0

    stale = []
    for path, want in ((mdp, md), (jsp, js)):
        got = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
        if got != want:
            stale.append(os.path.relpath(path, root))
    print('inbox_manifest: %d archived file(s), %d problem(s), %d stale generated file(s)'
          % (len(rows), len(problems), len(stale)))
    for p in problems:
        print('  PROBLEM %s' % p)
    for s in stale:
        print('  STALE   %s — regenerate with tools/inbox_manifest.py write' % s)
    return 1 if (problems or stale) else 0


if __name__ == '__main__':
    sys.exit(main())
