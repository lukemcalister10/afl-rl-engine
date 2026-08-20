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
  R4 ONE LAWS FILE   1b: "no second laws file, ever". The scan: any OTHER file under docs/ that
                     declares itself derived from the RULEBOOK (a `regenerated_from` naming it,
                     or a "twin" pointer). It feeds R5 + R6.
  R5 TWIN ABSENCE    `docs/acceptance_v2_0.json` — the retired twin — must NOT exist. The RULEBOOK
                     v3 amendment removed it; a file back at that path is the retirement being
                     quietly undone.
  R6 NO DERIVED VIEW no file may declare itself a derived laws view of the RULEBOOK, at that path
                     or any other. This is process law P10's teeth.

R5/R6 REVERSED THEIR POLARITY ON 2026-08-20, AND THAT IS THE POINT. Until v3 the tree carried
`docs/acceptance_v2_0.json`, a hand-maintained derived laws view, and R5/R6 asserted PARITY with it
(same law set) and a DO-NOT-HAND-EDIT banner on it — the sanctioned shape for a derived view that
exists. The owner's v3 word retired the twin instead of wiring it ("Okay agree to the laws updated.",
2026-08-20), so parity rules now have nothing to compare and, left as they were, would red forever on
a file that is supposed to be gone. Asserting the ABSENCE is the honest successor: the RULEBOOK is
the only laws file, and a SECOND ONE REAPPEARING is the new red. The two rules that policed the twin
now police its grave.

CALIBRATION, stated so it can be checked rather than believed: all six rules are GREEN on the
RULEBOOK and the tree as committed by the v3 amendment act (12 laws in PART 1, P1–P11 in PART 4, no
derived view anywhere under docs/). The negative controls are mechanical: restore any JSON at
`docs/acceptance_v2_0.json` and R5 reds; give any other docs/ file a `regenerated_from: RULEBOOK.md`
and R6 reds.

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

#: The twin retired by the v3 amendment (owner word 2026-08-20). R5 asserts it stays absent.
RETIRED_TWIN_REL = os.path.join('docs', 'acceptance_v2_0.json')

#: Files scanned for "am I a derived view of the RULEBOOK?". Everything under docs/, one level.
_DERIVED_SCAN_DIRS = ('docs',)

_LAW_LINE = re.compile(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*')
_PAREN_ID = re.compile(r'\(([A-Z0-9][^()]*)\)')
_COUNT_DECL = re.compile(r'\b(\d+)\s+(?:timeless\s+)?laws\b', re.I)


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

    # R4 the scan · R5 the retired twin stays absent · R6 no derived laws view, anywhere
    views = find_derived_views(root)
    if not views:
        notes.append('R4 ONE LAWS FILE: no derived laws view found in the tree — the RULEBOOK is '
                     'the only laws file, which is what PART 4 P10 requires.')
    else:
        for rel, _kind, _payload in views:
            notes.append('R4 ONE LAWS FILE: derived view found: %s' % rel)

    # R5 TWIN ABSENCE
    if os.path.exists(os.path.join(root, RETIRED_TWIN_REL)):
        fails.append('R5 TWIN ABSENCE: %s is BACK. The twin was RETIRED by the v3 amendment (owner '
                     'word 2026-08-20, "Okay agree to the laws updated."), its thresholds folded '
                     'into RULEBOOK PART 3. A file at that path is the retirement being undone — '
                     'the RULEBOOK is amended or the file goes, and neither is a lint\'s to do'
                     % RETIRED_TWIN_REL)
    else:
        notes.append('R5 TWIN ABSENCE: %s is absent, as the v3 amendment left it.'
                     % RETIRED_TWIN_REL)

    # R6 NO DERIVED VIEW — P10's teeth: a second laws file reappearing is the red.
    for rel, _kind, _payload in views:
        fails.append('R6 NO DERIVED VIEW: %s declares itself derived from the RULEBOOK. Since the '
                     'v3 amendment there is no sanctioned derived laws view: the laws live in %s '
                     'and nowhere else (PART 4 P10, "no second laws file, ever"). A derived view '
                     'that reappears is this rule\'s whole subject.' % (rel, RULEBOOK_REL))
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
