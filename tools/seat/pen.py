#!/usr/bin/env python3
"""pen.py — the register pen, NEW FORM (the 3b act, 2026-08-21).

The durable record lives in TWO homes since the freeze:
  · docs/OPEN_ITEMS_REGISTER.md      — FROZEN history, v622-v812 + the numbered legacy items.
                                       Byte-sealed; its identity is docs/register/frozen_identity.json
                                       and `verify` asserts it on every run. NEVER written again.
  · docs/register/entries/vNNN.md    — the live record, ONE FILE PER ENTRY, same version counter
                                       (no restart), each opening with the same ` · vNNN (date):`
                                       marker the frozen file used, so one grep idiom spans the seam.

Subcommands
  append --entry-file F [--incident yes|no] [--date YYYY-MM-DD] [--dry-run]
      F holds the entry BODY (no marker — the pen writes it). Computes the next version, writes
      entries/vNNN.md, rewrites LATEST.md (the one-line freshest-state pointer orient.sh reads),
      regenerates the address index, then runs verify. WRITES FILES ONLY — no git: the supervisor
      commits explicit-path per process law P8. An `incident: yes|no` trailer is written when
      --incident is given; tools/incident_index.py PREFERS it over its pattern rules.
  verify
      The standing falsifiers: frozen-file md5 == the sealed identity · entry files well-formed,
      filename == marker version, versions unique and CONTIGUOUS from v813 · LATEST.md names the
      newest version · the generated index matches regeneration. Non-zero exit on any failure.
  index
      Regenerate docs/register/INDEX.md + index.json in place.

The old pen (register item 148) targeted the `## FABLE'S QUEUE` splice model and was REPLACED, not
repointed, in the 3b act — pointed at the new form it would have been wrong in a new way (READERS_3B
R1). Reading law for humans and seats: docs/register/README.md.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
FROZEN = os.path.join(ROOT, 'docs', 'OPEN_ITEMS_REGISTER.md')
REGDIR = os.path.join(ROOT, 'docs', 'register')
ENTRIES = os.path.join(REGDIR, 'entries')
LATEST = os.path.join(REGDIR, 'LATEST.md')
IDENTITY = os.path.join(REGDIR, 'frozen_identity.json')
INDEX_MD = os.path.join(REGDIR, 'INDEX.md')
INDEX_JSON = os.path.join(REGDIR, 'index.json')

FIRST_NEW = 813          # frozen file ends at v812 (the tombstone); the counter continues, C6.
MARKER = re.compile(r'^· v(\d+) \((\d{4}-\d{2}-\d{2})[^)]{0,16}\): ')
FNAME = re.compile(r'^v(\d+)\.md$')
LEGACY_ITEM = re.compile(r'^(\d+)\. ', re.M)
NNUM = re.compile(r'\bN(\d{1,3})\b')


def die(msg):
    sys.stderr.write('pen: FAIL — %s\n' % msg)
    raise SystemExit(1)


def entry_files():
    if not os.path.isdir(ENTRIES):
        return []
    out = []
    for name in os.listdir(ENTRIES):
        m = FNAME.match(name)
        if not m:
            die('foreign file in entries/: %s (only vNNN.md belongs here)' % name)
        out.append((int(m.group(1)), os.path.join(ENTRIES, name)))
    return sorted(out)


def parse_entry(path):
    text = open(path, encoding='utf-8').read()
    m = MARKER.match(text)
    if not m:
        die('%s does not OPEN with the `· vNNN (YYYY-MM-DD): ` marker' % os.path.relpath(path, ROOT))
    return int(m.group(1)), m.group(2), text[m.end():]


def build_index():
    """-> (md_text, json_text), deterministic. The address map that keeps 1,260 citations cheap:
    vNNN -> file · legacy `item NNN` -> the frozen file · N-numbers -> every home they appear in."""
    frozen_rel = os.path.relpath(FROZEN, ROOT).replace(os.sep, '/')
    ftext = open(FROZEN, encoding='utf-8').read()
    ident = json.load(open(IDENTITY, encoding='utf-8'))
    lo, hi = (int(v[1:]) for v in ident['entry_span'])
    versions = {'v%d' % n: frozen_rel for n in range(lo, hi + 1)}
    rows = []
    for n, path in entry_files():
        v, date, body = parse_entry(path)
        if v != n:
            die('%s: filename says v%d, marker says v%d' % (path, n, v))
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        versions['v%d' % v] = rel
        rows.append((v, date, rel, ' '.join(body.split())[:140]))
    items = {m.group(1): frozen_rel for m in LEGACY_ITEM.finditer(ftext)}
    nnums = {}
    for src_rel, text in [(frozen_rel, ftext)] + [
            (r, open(os.path.join(ROOT, r), encoding='utf-8').read()) for _v, _d, r, _s in rows]:
        for m in NNUM.finditer(text):
            nnums.setdefault('N' + m.group(1), []).append(src_rel)
    nnums = {k: sorted(set(v)) for k, v in nnums.items()}
    newest = max(int(v[1:]) for v in versions)
    md = ['<!-- GENERATED-ONLY — regenerate: python3 tools/seat/pen.py index ; '
          'assert current: python3 tools/seat/pen.py verify -->',
          '# REGISTER ADDRESS INDEX — generated',
          '',
          'Newest entry: **v%d**. Frozen history v%d–v%d lives whole in `%s` (sealed, '
          'md5 `%s`); entries from v%d live one-per-file below. `item NNN` and N-number '
          'addresses resolve into the frozen file; the JSON twin carries the full maps.'
          % (newest, lo, hi, frozen_rel, ident['md5'][:8], FIRST_NEW),
          '']
    for v, date, rel, snip in sorted(rows, reverse=True):
        md.append('- **v%d** (%s) — `%s` — %s' % (v, date, rel, snip))
    md_text = '\n'.join(md) + '\n'
    json_text = json.dumps({'newest': 'v%d' % newest, 'frozen': ident,
                            'versions': versions, 'items': items, 'nnumbers': nnums},
                           indent=1, sort_keys=True) + '\n'
    return md_text, json_text


def write_index():
    md, js = build_index()
    open(INDEX_MD, 'w', encoding='utf-8').write(md)
    open(INDEX_JSON, 'w', encoding='utf-8').write(js)


def latest_line(version, date, body):
    summary = ' '.join(body.split())
    return '# OPEN ITEMS REGISTER · v%d %s · %s' % (version, date, summary)


def write_latest(version, date, body):
    top = latest_line(version, date, body)[:400]
    rest = ('\n\n(one line per pen; full entry: docs/register/entries/v%d.md · reading law: '
            'docs/register/README.md · frozen history: docs/OPEN_ITEMS_REGISTER.md)\n' % version)
    open(LATEST, 'w', encoding='utf-8').write(top + rest)


def cmd_verify(_a=None):
    fails = []
    ident = json.load(open(IDENTITY, encoding='utf-8'))
    md5 = hashlib.md5(open(FROZEN, 'rb').read()).hexdigest()
    if md5 != ident['md5']:
        fails.append('FROZEN FILE MOVED: md5 %s != sealed %s — the freeze falsifier fired' %
                     (md5, ident['md5']))
    seen, prev = set(), FIRST_NEW - 1
    newest = None
    for n, path in entry_files():
        v, date, body = parse_entry(path)
        if v != n:
            fails.append('%s: filename/marker version mismatch (%d vs %d)' % (path, n, v))
        if v in seen:
            fails.append('duplicate version v%d' % v)
        seen.add(v)
        if v != prev + 1:
            fails.append('version gap: v%d follows v%d (contiguity from v%d is the law)' %
                         (v, prev, FIRST_NEW))
        prev = v
        newest = (v, date, body)
    if newest:
        want = latest_line(*newest)[:200]
        got = open(LATEST, encoding='utf-8').read().split('\n', 1)[0][:200] if os.path.exists(LATEST) else ''
        if got != want:
            fails.append('LATEST.md line 1 does not match the newest entry v%d' % newest[0])
        md, js = build_index()
        if open(INDEX_MD, encoding='utf-8').read() != md if os.path.exists(INDEX_MD) else True:
            fails.append('INDEX.md stale — regenerate: pen.py index')
        if open(INDEX_JSON, encoding='utf-8').read() != js if os.path.exists(INDEX_JSON) else True:
            fails.append('index.json stale — regenerate: pen.py index')
    for f in fails:
        sys.stderr.write('pen verify: FAIL — %s\n' % f)
    print('pen verify: frozen %s sealed-ok=%s · %d new-form entries · newest v%s' %
          (md5[:8], md5 == ident['md5'], len(seen), (newest[0] if newest else '(none yet)')))
    return 1 if fails else 0


def cmd_append(a):
    body = open(a.entry_file, encoding='utf-8').read().strip()
    if not body:
        die('entry body is empty')
    if MARKER.match(body):
        die('the body already carries a marker — the pen writes the marker, not the author')
    vs = [n for n, _p in entry_files()]
    nxt = (max(vs) + 1) if vs else FIRST_NEW
    date = a.date or datetime.date.today().isoformat()
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        die('--date must be YYYY-MM-DD')
    text = '· v%d (%s): %s\n' % (nxt, date, body)
    if a.incident:
        text += '\nincident: %s\n' % a.incident
    path = os.path.join(ENTRIES, 'v%d.md' % nxt)
    if os.path.exists(path):
        die('%s already exists' % path)
    if a.dry_run:
        print('DRY RUN — would write v%d (%s), %d bytes, incident=%s' %
              (nxt, date, len(text.encode()), a.incident or '(unset)'))
        return 0
    os.makedirs(ENTRIES, exist_ok=True)
    open(path, 'w', encoding='utf-8').write(text)
    write_latest(nxt, date, body)
    write_index()
    rc = cmd_verify()
    if rc == 0 and a.file:
        rc = _file_pen(nxt, path, a.commit_message)
    else:
        print('penned v%d -> %s (%d bytes). Commit explicit-path: the entry, LATEST.md, INDEX.md, '
              'index.json.' % (nxt, os.path.relpath(path, ROOT), len(text.encode())))
    return rc


def _file_pen(nxt, entry_path, message):
    """--file: the whole filing chain in one command (shrink review S12, owner word 2026-08-28).

    Before this flag every pen was four commands and a push — entry, incident index, STATE, an
    explicit-path commit — a procedure that grew out of its own misses (v822). The chain here is
    the SAME four instruments invoked in the same order, not a fifth implementation; each one's
    own verify still gates the next, and the commit is explicit-path (P8), never `add -A`."""
    import subprocess

    def run(argv):
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        if p.returncode != 0:
            print((p.stdout or '') + (p.stderr or ''))
        return p.returncode

    if run([sys.executable, os.path.join(ROOT, 'tools', 'incident_index.py'), 'write']):
        die('incident_index write failed — the entry stands, the filing stopped')
    if run([sys.executable, '-m', 'tools.landing.state', 'write']):
        die('STATE write failed — the entry stands, the filing stopped')
    if run([sys.executable, '-m', 'tools.landing.state', 'check']):
        die('STATE check failed after write')
    paths = [os.path.relpath(entry_path, ROOT),
             'docs/register/LATEST.md', 'docs/register/INDEX.md', 'docs/register/index.json',
             'docs/incidents/INDEX.md', 'docs/incidents/index.json', 'docs/STATE.md']
    msg = message or ('register v%d' % nxt)
    if run(['git', 'add', '--'] + paths) or run(['git', 'commit', '-m', msg, '--'] + paths):
        die('the explicit-path commit failed')
    print('penned AND filed v%d — entry + indexes + incidents + STATE committed (explicit paths). '
          'Push when ready.' % nxt)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='the register pen — new form (3b)')
    sub = ap.add_subparsers(dest='cmd', required=True)
    a1 = sub.add_parser('append')
    a1.add_argument('--entry-file', required=True)
    a1.add_argument('--incident', choices=('yes', 'no'))
    a1.add_argument('--date')
    a1.add_argument('--dry-run', action='store_true')
    a1.add_argument('--file', action='store_true',
                    help='run the whole filing chain: incident index + STATE + explicit-path commit (S12)')
    a1.add_argument('--commit-message', help='commit message for --file (default: "register vN")')
    sub.add_parser('verify')
    a3 = sub.add_parser('index')
    a = ap.parse_args(argv)
    if a.cmd == 'append':
        return cmd_append(a)
    if a.cmd == 'index':
        write_index()
        print('index regenerated')
        return 0
    return cmd_verify()


if __name__ == '__main__':
    sys.exit(main())
