#!/usr/bin/env python3
"""tools/incident_index.py — THE INCIDENT INDEX, GENERATED (PLAN_v6 1e).

    python3 tools/incident_index.py write     regenerate docs/incidents/INDEX.md (+ index.json)
    python3 tools/incident_index.py check     exit 1 if the committed index is out of date
    python3 tools/incident_index.py rules     print the extraction rules and nothing else

GENERATED-ONLY, LIKE EVERY DERIVED SURFACE IN THIS PLAN. If it cannot be generated it does not
exist, and it is NEVER hand-appended. The repo's own evidence kills the alternative:
`docs/CURRENT_STATE.md` carries exactly the authority banner a hand-maintained index would carry,
and still went 156 register versions stale.

THE INPUT CONTRACT, named because 3b freezes history. The generator parses the register's EXISTING
structure — the ` · vNNN (date):` entry markers — and nothing else. NO TAGGING CONVENTION EXISTS
AND NONE IS RETRO-APPLIED to the append-only record, ever. `docs/OPEN_ITEMS_REGISTER.md` is not
written to by this tool under any mode. Post-3b entries MAY carry an explicit `incident:` field,
and the generator PREFERS it where present (see `_explicit_incident`), so the pattern rules below
become a fallback rather than the mechanism, without any change to the frozen history.

WHAT THE MARKER COVERS, MEASURED RATHER THAN ASSUMED: 178 entries, v622-v803 (the marker
form ` · vNNN (date):` — four further `· vNNN (` occurrences carry no date and are not entry
markers). The register's older
record predates the marker form and is one continuous body of prose with no entry boundaries a
parser can find. The index says so on its own front page. Inventing boundaries for that region
would be archaeology dressed as extraction, which is the thing 1e retires.

THE EXTRACTION RULES ARE CONSERVATIVE, AND THAT IS THE DESIGN. An entry is an INCIDENT only by its
own words — a correction, an incident, a halt that happened, a defect, a revert, a breach, a false
red. Design vocabulary that merely contains those letters is excluded by name: "halt-not-warn" and
"fail-closed" describe how a gate is built, not something that went wrong, and the estate's prose
is full of both. WHEN UNSURE, EXCLUDE. An index that over-reports incidents is an index nobody
believes, and the register stays the durable record either way: this is a lookup, never a
replacement.

RETIRES (G4, named): register-prose archaeology as the incident lookup — grepping 8,400 lines of
append-only record to answer "when did that go wrong before?".
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

REGISTER_REL = os.path.join('docs', 'OPEN_ITEMS_REGISTER.md')
OUT_DIR_REL = os.path.join('docs', 'incidents')
OUT_MD = 'INDEX.md'
OUT_JSON = 'index.json'

ENTRY = re.compile(r' · v(\d+) \((\d{4}-\d{2}-\d{2})\):')

#: An entry is an incident only if one of these fires on its own words. Each carries the label the
#: index reports, so a reader can see WHICH word made the call.
RULES = (
    ('CORRECTION', re.compile(r'\b(CORRECTION|CORRECTED|ERRATUM|ERRATA)\b')),
    ('INCIDENT',   re.compile(r'\bINCIDENT\b', re.I)),
    ('HALT',       re.compile(r'\bHALT(?:ED|S)?\b')),
    ('DEFECT',     re.compile(r'\b(DEFECT|BUG)\b', re.I)),
    ('REVERT',     re.compile(r'\b(REVERT|REVERTED|ROLLED BACK|ROLLBACK)\b', re.I)),
    ('BREACH',     re.compile(r'\bBREACH(?:ED|ES)?\b', re.I)),
    ('FALSE-RED',  re.compile(r'\bFALSE (?:RED|POSITIVE)\b', re.I)),
)

#: Design vocabulary that CONTAINS an incident word without being one. Removed from the text before
#: the rules run. Every entry here is a phrase the estate uses to describe how a gate is BUILT.
DESIGN_PHRASES = (
    re.compile(r'halt[-\s]?not[-\s]?warn', re.I),
    re.compile(r'halts?[,\s]+never warns?', re.I),
    re.compile(r'fail[-\s]?closed', re.I),
    re.compile(r'\bhalt behaviour\b', re.I),
    re.compile(r'must (?:always )?halt\b', re.I),
    re.compile(r'\bwould halt\b', re.I),
    re.compile(r'\bcan halt\b', re.I),
    re.compile(r'\bhalt on drift\b', re.I),
)

#: The post-3b escape hatch: an explicit field wins over the pattern rules.
_EXPLICIT = re.compile(r'\bincident:\s*(yes|no)\b', re.I)


def _explicit_incident(body):
    m = _EXPLICIT.search(body)
    if not m:
        return None
    return m.group(1).lower() == 'yes'


def _strip_design(body):
    out = body
    for p in DESIGN_PHRASES:
        out = p.sub(' ', out)
    return out


def _first_sentence(body, n=220):
    s = ' '.join(body.split())
    cut = s[:n]
    return cut + ('…' if len(s) > n else '')


def entries(root):
    """-> [(version:int, date:str, body:str)] for every marker-delimited entry, in file order."""
    text = open(os.path.join(root, REGISTER_REL), encoding='utf-8').read()
    marks = list(ENTRY.finditer(text))
    out = []
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((int(m.group(1)), m.group(2), text[start:end]))
    return out


def _snippets(scrubbed, pat, limit=3, width=95):
    """The SENTENCES that fired, not the entry's opening line.

    Register entries are DAY-SIZED narratives — 7-8 KB each, covering a whole session. A label on
    such an entry means "somewhere in this day's words there is a halt", which is nearly useless as
    a lookup and reads as an over-report. Carrying the matched context makes the index answer the
    question it exists for: not "did something go wrong on the 20th" but "WHAT went wrong, in the
    record's own words, and where do I read the rest of it".
    """
    out, seen = [], set()
    for m in pat.finditer(scrubbed):
        lo = max(0, m.start() - width)
        hi = min(len(scrubbed), m.end() + width)
        snip = ' '.join(scrubbed[lo:hi].split())
        key = snip[:40].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(('…' if lo else '') + snip + ('…' if hi < len(scrubbed) else ''))
        if len(out) >= limit:
            break
    return out


def classify(body):
    """-> (is_incident, [(label, [snippet])], how) where how is 'explicit' or 'pattern'."""
    ex = _explicit_incident(body)
    if ex is not None:
        return ex, ([('DECLARED', [_first_sentence(body)])] if ex else []), 'explicit'
    scrubbed = _strip_design(body)
    hits = [(name, _snippets(scrubbed, pat)) for name, pat in RULES if pat.search(scrubbed)]
    return bool(hits), hits, 'pattern'


def build(root):
    rows = []
    all_entries = entries(root)
    for version, date, body in all_entries:
        is_inc, hits, how = classify(body)
        if not is_inc:
            continue
        rows.append({'version': version, 'date': date,
                     'labels': [n for n, _s in hits],
                     'hits': {n: s for n, s in hits},
                     'by': how,
                     'headline': _first_sentence(body, 150)})
    return rows, all_entries


BANNER = """<!-- GENERATED-ONLY — DO NOT HAND-EDIT, DO NOT HAND-APPEND.
     Regenerate: python3 tools/incident_index.py write
     Assert current: python3 tools/incident_index.py check
     docs/OPEN_ITEMS_REGISTER.md is the durable record and is NEVER written to by the generator.
     A hand-maintained index with an authority banner is what docs/CURRENT_STATE.md was, and it
     sat 156 register versions stale. -->
"""


def render_md(rows, all_entries):
    vers = [v for v, _d, _b in all_entries]
    lo, hi = (min(vers), max(vers)) if vers else (0, 0)
    out = [BANNER, '# INCIDENT INDEX — generated from the open-items register', '',
           '**Coverage: %d register entries, v%d–v%d.** The generator parses the register\'s existing '
           '` · vNNN (date):` entry markers and nothing else. The record before v%d predates that '
           'form and is one continuous body of prose with no entry boundaries a parser can find; it '
           'is NOT indexed, and inventing boundaries for it would be archaeology dressed as '
           'extraction. No tagging convention is retro-applied to the append-only record, ever.'
           % (len(all_entries), lo, hi, lo),
           '',
           '**The extraction rules are CONSERVATIVE. When unsure, an entry is EXCLUDED.** An entry '
           'is an incident only by its own words: %s. Design vocabulary that contains those letters '
           'without being an incident — "halt-not-warn", "fail-closed", "would halt" — is stripped '
           'before the rules run. This is a LOOKUP, not a replacement: the register remains the '
           'durable record, and an entry missing here is an index limitation, not an absolution.'
           % ', '.join(name for name, _p in RULES),
           '',
           '**%d of %d indexed entries carry incident words (%.0f%%).**'
           % (len(rows), len(all_entries), 100.0 * len(rows) / max(1, len(all_entries))),
           '']
    for r in sorted(rows, key=lambda r: -r['version']):
        out.append('### v%d · %s · %s' % (r['version'], r['date'], ' · '.join(r['labels'])))
        out.append('')
        out.append('%s' % r['headline'])
        out.append('')
        for label in r['labels']:
            for snip in r['hits'][label]:
                out.append('- **%s** — %s' % (label, snip))
        out.append('')
    out.append('')
    out.append('---')
    out.append('')
    out.append('Generated by `tools/incident_index.py`. Post-3b entries may carry an explicit '
               '`incident: yes|no` field, which the generator PREFERS over the pattern rules; '
               'today %d of %d classifications are explicit.'
               % (sum(1 for r in rows if r['by'] == 'explicit'), len(rows)))
    return '\n'.join(out) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('mode', choices=('write', 'check', 'rules'))
    ap.add_argument('--root', default=os.environ.get('RL_REPO') or _ROOT)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)

    if a.mode == 'rules':
        print('AN ENTRY IS AN INCIDENT ONLY BY ITS OWN WORDS. Rules, in order:')
        for name, pat in RULES:
            print('  %-11s %s' % (name, pat.pattern))
        print('STRIPPED FIRST (design vocabulary, not incidents):')
        for p in DESIGN_PHRASES:
            print('  %s' % p.pattern)
        print('EXPLICIT OVERRIDE (post-3b): %s' % _EXPLICIT.pattern)
        print('WHEN UNSURE, EXCLUDE.')
        return 0

    rows, all_entries = build(root)
    md = render_md(rows, all_entries)
    js = json.dumps({'coverage_entries': len(all_entries),
                     'incidents': len(rows),
                     'rules': [name for name, _p in RULES],
                     'register': REGISTER_REL.replace(os.sep, '/'),
                     'entries': sorted(rows, key=lambda r: -r['version'])},
                    indent=2, sort_keys=True) + '\n'
    outdir = os.path.join(root, OUT_DIR_REL)
    mdp, jsp = os.path.join(outdir, OUT_MD), os.path.join(outdir, OUT_JSON)

    if a.mode == 'write':
        os.makedirs(outdir, exist_ok=True)
        open(mdp, 'w', encoding='utf-8').write(md)
        open(jsp, 'w', encoding='utf-8').write(js)
        print('wrote %s and %s — %d incidents from %d indexed register entries'
              % (mdp, jsp, len(rows), len(all_entries)))
        return 0

    stale = [os.path.relpath(p, root) for p, want in ((mdp, md), (jsp, js))
             if (open(p, encoding='utf-8').read() if os.path.exists(p) else '') != want]
    print('incident_index: %d incidents / %d indexed entries; %d stale generated file(s)'
          % (len(rows), len(all_entries), len(stale)))
    for s in stale:
        print('  STALE %s — regenerate with tools/incident_index.py write' % s)
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
