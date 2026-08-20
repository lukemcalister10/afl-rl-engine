#!/usr/bin/env python3
"""tools/rulebook_lint.py — THE RULEBOOK LINT. A NEW instrument (PLAN_v6 1a).

    python3 tools/rulebook_lint.py [TREE_ROOT]        exit 0 = clean, 1 = at least one FAIL

WHY THIS IS NOT doc_lint.py. `doc_lint.py` is a status-vocabulary gate: it bans the words
"closed"/"done" and flags superseded hashes claimed current, over a fixed LIVE/HISTORY file list.
Point it at `docs/RULEBOOK.md` and it reds on the RULEBOOK's own prose day one — Part 2 is titled
"ALL RETIRED", the owner's quoted word is "they've done their job", and Part 3 says a rule that
cannot be measured is "never silently waived". Every one of those is a false red. The RULEBOOK needs
a lint that knows what a rulebook IS, so this is that lint and doc_lint is left alone.

WHAT IT ASSERTS (each rule names the plan line it serves):

  R1 SIGNED          the RULEBOOK carries an owner-signature line. 1b: "the owner-signed single
                     governing document".
  R2 NUMBERING       Part 1's laws are numbered 1..N with no gap, no repeat, no restart. The
                     count flag (register v803 header: "Part 1 numbers 11 laws vs '13' in its
                     commit message + seat brief") is a counting question, so counting is
                     mechanised here rather than eyeballed again.
  R3 COUNT DECLARED  whatever the RULEBOOK says its own law count is, it must equal R2's count.
                     Silent today (the file states no count) — the rule exists so that the moment
                     1b's amendment writes one, it is checked rather than trusted.
  R4 ONE LAWS FILE   1b: "no second laws file, ever". Any OTHER file in the tree that declares
                     itself derived from the RULEBOOK (a `regenerated_from` naming it, or a
                     "twin" pointer) is a DERIVED VIEW and must satisfy R5 + R6.
  R5 TWIN PARITY     a derived view's law set must equal the RULEBOOK's law set — same ids, same
                     count. This is the plan's own sanctioned form for a derived view:
                     "CI-linted equal to the RULEBOOK via 1a".
  R6 TWIN BANNER     a derived view must carry a DO-NOT-HAND-EDIT / "the RULEBOOK wins" banner.

CALIBRATION, stated so it can be checked rather than believed: R1, R2, R3 and R4 are GREEN on the
RULEBOOK as committed at 0244935. R5 and R6 are RED on `docs/acceptance_v2_0.json`, and that red is
TRUE, not a false positive: the twin carries 13 laws where Part 1 numbers 11 (`G-Y0` and `G-COHORT`
appear in the twin and in no numbered law), and it carries no do-not-hand-edit banner. That is the
in-tree violator 1b exists to dispose of, and it is carried as a presented RULED-RED entry
(`acceptance/ruled_red.json`, id RB1) until the owner signs the 1b diff — the lint is armed, the
finding is measured, and nobody is asked to remember it.

LAW-ID EXTRACTION, honestly: a law's id is the **bolded token** in its numbered line
(`**ONE SOURCE.**`, `**THE CURVE DESCENDS (G-MONO).**`). Where the bold carries a parenthesised
short id, that short id wins — it is the name the twin and the gates use. Where it does not, the
bolded words are normalised (upper, spaces -> '-', trailing '.' dropped). The rule is conservative
by construction: a line whose bold cannot be parsed is reported as UNPARSED and reds R2, rather
than being silently skipped.
"""

import json
import os
import re
import sys

RULEBOOK_REL = os.path.join('docs', 'RULEBOOK.md')

#: Files scanned for "am I a derived view of the RULEBOOK?". Everything under docs/, one level.
_DERIVED_SCAN_DIRS = ('docs',)

_LAW_LINE = re.compile(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*')
_PAREN_ID = re.compile(r'\(([A-Z0-9][^()]*)\)')
_COUNT_DECL = re.compile(r'\b(\d+)\s+(?:timeless\s+)?laws\b', re.I)
_BANNER = re.compile(r'do[\s\-_]?not[\s\-_]?hand[\s\-_]?edit|the rulebook wins|generated[\s\-_]?only',
                     re.I)


def _norm_id(bold):
    """The law id for one bolded law heading. See the module docstring's extraction rule."""
    bold = bold.strip()
    m = _PAREN_ID.search(bold)
    if m:
        # 'L-SAGE-FADE / A-FADE, direction-only' -> the first named id
        return m.group(1).split('/')[0].split(',')[0].strip().upper()
    txt = bold.rstrip('.').strip().upper()
    txt = re.sub(r'[^A-Z0-9]+', '-', txt).strip('-')
    return txt or None


def _tokens(law_id):
    return [t for t in re.split(r'[^A-Z0-9]+', (law_id or '').upper()) if t]


def recoverable_from(view_id, rulebook_ids):
    """Is `view_id` recoverable from one of the RULEBOOK's own law headings?

    R5 must not turn into a hand-kept mapping table between two spellings of the same law — that is
    a second laws file by another route. The rule instead is mechanical: a derived view's id is
    legitimate when its tokens appear, IN ORDER, inside a RULEBOOK law's tokens (or the RULEBOOK
    law's inside the view's). `SILENCE-IS-RED` is recoverable from `SILENCE IS A RED`;
    `SEAM-PATTERN` from `THE SEAM PATTERN`; `G-Y0` and `G-COHORT` are recoverable from nothing,
    which is the finding.
    """
    def subseq(a, b):
        it = iter(b)
        return all(any(x == y for y in it) for x in a)
    vt = _tokens(view_id)
    for rid in rulebook_ids:
        rt = _tokens(rid)
        if vt and rt and (subseq(vt, rt) or subseq(rt, vt)):
            return rid
    return None


def parse_rulebook(text):
    """-> (laws, numbers, unparsed).  laws = [id]; numbers = [int]; unparsed = [line]."""
    laws, numbers, unparsed = [], [], []
    in_part1 = False
    for ln in text.splitlines():
        if ln.startswith('## PART 1'):
            in_part1 = True
            continue
        if in_part1 and ln.startswith('## '):
            break
        if not in_part1:
            continue
        m = _LAW_LINE.match(ln)
        if not m:
            # a numbered line whose bold we could not read is a finding, not a skip
            if re.match(r'^\s*\d+\.\s', ln):
                unparsed.append(ln.strip())
            continue
        lid = _norm_id(m.group(2))
        if not lid:
            unparsed.append(ln.strip())
            continue
        numbers.append(int(m.group(1)))
        laws.append(lid)
    return laws, numbers, unparsed


_PROC_LINE = re.compile(r'^\s*P(\d+)\.\s+\*\*(.+?)\*\*')


def parse_process_laws(text):
    """-> (ids, numbers) for a PROCESS LAWS section, or ([], []) if the RULEBOOK has none.

    The 1b amendment lands the process laws as their OWN part, numbered P1..Pn, deliberately: PART 1
    is about the model and its count is the subject of an owner-signed flag, so process laws must not
    renumber it. This parser exists now, before the amendment, so the section is checked from the
    moment it is signed rather than after somebody notices it is not.
    """
    ids, numbers = [], []
    inside = False
    for ln in text.splitlines():
        if ln.startswith('## ') and 'PROCESS LAW' in ln.upper():
            inside = True
            continue
        if inside and ln.startswith('## '):
            break
        if not inside:
            continue
        m = _PROC_LINE.match(ln)
        if m:
            numbers.append(int(m.group(1)))
            ids.append(_norm_id(m.group(2)))
    return ids, numbers


def declared_count(text):
    """The count the RULEBOOK states about itself, or None. Only header/signature prose is read."""
    for ln in text.splitlines():
        if ln.startswith('#') or ln.lower().startswith('part 1'):
            m = _COUNT_DECL.search(ln)
            if m:
                return int(m.group(1))
    return None


def find_derived_views(root):
    """Every file that declares itself derived from the RULEBOOK. -> [(relpath, kind, payload)]."""
    out = []
    rb_lower = 'rulebook'
    for d in _DERIVED_SCAN_DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            rel = os.path.join(d, name)
            path = os.path.join(base, name)
            if not os.path.isfile(path) or rel.replace(os.sep, '/') == RULEBOOK_REL.replace(os.sep, '/'):
                continue
            if not name.endswith(('.json', '.md')):
                continue
            try:
                text = open(path, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            if name.endswith('.json'):
                try:
                    doc = json.loads(text)
                except ValueError:
                    continue
                src = str(doc.get('regenerated_from') or doc.get('derived_from') or '')
                if rb_lower in src.lower():
                    out.append((rel, 'json', doc))
            else:
                if re.search(r'regenerated[_\s]from\s*:?.{0,40}rulebook', text, re.I):
                    out.append((rel, 'md', text))
    return out


def lint(root):
    """-> (fails, notes). `fails` reds the run; `notes` are measured facts worth printing."""
    fails, notes = [], []
    rb_path = os.path.join(root, RULEBOOK_REL)
    if not os.path.exists(rb_path):
        return ['%s: ABSENT — the single governing document is not in the tree' % RULEBOOK_REL], notes
    text = open(rb_path, encoding='utf-8').read()

    # R1 SIGNED
    if not re.search(r'owner[\s\-]?signed|^## SIGNED|owner word given', text, re.I | re.M):
        fails.append('R1 SIGNED: %s carries no owner-signature line' % RULEBOOK_REL)

    # R2 NUMBERING
    laws, numbers, unparsed = parse_rulebook(text)
    for ln in unparsed:
        fails.append('R2 NUMBERING: unparsed numbered line in PART 1 (a law the lint cannot read is '
                     'a law it cannot check): %s' % ln[:90])
    if not laws:
        fails.append('R2 NUMBERING: PART 1 declares no readable laws')
    else:
        if numbers != list(range(1, len(numbers) + 1)):
            fails.append('R2 NUMBERING: PART 1 law numbers are %s — expected 1..%d contiguous'
                         % (numbers, len(numbers)))
        dupes = sorted({i for i in laws if laws.count(i) > 1})
        if dupes:
            fails.append('R2 NUMBERING: duplicate law id(s) %s' % dupes)
    notes.append('PART 1 laws counted: %d  (%s)' % (len(laws), ', '.join(laws)))

    # R2b PROCESS-LAW NUMBERING — checked only when the section exists (it arrives with 1b).
    pids, pnums = parse_process_laws(text)
    if pids:
        if pnums != list(range(1, len(pnums) + 1)):
            fails.append('R2 NUMBERING: PROCESS LAW numbers are %s — expected P1..P%d contiguous'
                         % (pnums, len(pnums)))
        pdupes = sorted({i for i in pids if pids.count(i) > 1})
        if pdupes:
            fails.append('R2 NUMBERING: duplicate process-law id(s) %s' % pdupes)
        notes.append('PROCESS LAWS counted: %d  (%s)' % (len(pids), ', '.join(pids)))
    else:
        notes.append('PROCESS LAWS: no such section in the RULEBOOK yet (the 1b amendment adds it; '
                     'the rule is armed and simply has nothing to read).')

    # R3 COUNT DECLARED
    dc = declared_count(text)
    if dc is None:
        notes.append('R3 COUNT DECLARED: the RULEBOOK states no law count of its own — nothing to '
                     'contradict. The rule arms itself the moment one is written.')
    elif dc != len(laws):
        fails.append('R3 COUNT DECLARED: the RULEBOOK says %d laws; PART 1 numbers %d' % (dc, len(laws)))

    # R4/R5/R6 derived views
    views = find_derived_views(root)
    if not views:
        notes.append('R4 ONE LAWS FILE: no derived laws view found in the tree.')
    for rel, kind, payload in views:
        notes.append('R4 ONE LAWS FILE: derived view found: %s' % rel)
        if kind == 'json':
            ids = [str(l.get('id')) for l in (payload.get('laws') or [])]
            raw = json.dumps(payload)
        else:
            ids = []
            raw = payload
        if kind == 'json':
            matched = {}
            extra = []
            for i in ids:
                hit = recoverable_from(i, laws)
                (matched.setdefault(hit, i) if hit else extra.append(i))
            missing = [i for i in laws if i not in matched]
            if missing or extra:
                fails.append('R5 TWIN PARITY: %s law set != RULEBOOK PART 1 (%d vs %d). '
                             'in RULEBOOK only: %s | in view only: %s'
                             % (rel, len(laws), len(ids), missing or '-', extra or '-'))
        if not _BANNER.search(raw):
            fails.append('R6 TWIN BANNER: %s carries no DO-NOT-HAND-EDIT / "the RULEBOOK wins" '
                         'banner — a derived view without one is a second laws file in disguise' % rel)
    return fails, notes


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = argv[0] if argv else (os.environ.get('RL_REPO')
                                 or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fails, notes = lint(root)
    print('rulebook_lint: %d FAIL  (tree %s)' % (len(fails), root))
    for n in notes:
        print('  note', n)
    for f in fails:
        print('  FAIL', f)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
