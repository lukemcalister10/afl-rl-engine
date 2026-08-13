#!/usr/bin/env python3
"""ORDER 27 sweep tool: ruling-bearing window extraction.

For every occurrence of a CORE ruling marker anywhere in the register, cut a
context window (default +-700 chars, snapped to sentence-ish boundaries) and
merge overlapping windows inside the same unit. Every window is then read
verbatim by the seat. Units with no CORE marker but a BROAD marker are emitted
to a second file for the second reading pass.
"""
import re
import json
import os

OUT = 'docs/evidence/rulings_sweep_2026-08-13/tools'
W = 500
WB = 320

CORE = [r'OWNER[- ]RUL\w*', r'owner[- ]rul\w*', r'\bRULED\b', r'\bRULING\b', r'owner words?', r'OWNER WORDS?',
        r'owner override', r'owner overrule\w*', r'owner-caught', r'OWNER-CAUGHT', r'verbatim', r'VERBATIM',
        r'filed \d{6,}', r'owner-directed', r'owner-ordered', r"owner'?s word", r'owner’s word',
        r'owner-worded', r'DEFERRED \(owner', r'ratified', r'RATIFIED', r'owner says', r'owner said',
        r'owner-ratified', r'THE [A-Z][A-Z ’—-]{3,40} LAW', r'\bSTANDING\b', r'EXCLUDE', r'EXCLUSION',
        r'owner-approved', r'owner-raised', r'owner-driven', r'OWNER INPUT', r'owner input',
        r'owner act', r'owner release', r'owner-released', r'FROZEN RULER', r'frozen ruler']
rx = re.compile('|'.join(CORE))


BROAD2 = [r'\bLAW\b', r'\blaw\b', r'\bMUST\b', r'\bNEVER\b', r'\bALWAYS\b', r'convention', r'CONVENTION',
          r'binding', r'BINDING', r'MANDAT\w*', r'mandat\w*', r'PARKED', r'parked', r'DEFERRED', r'deferred',
          r'FROZEN', r'frozen', r'OVERRIDE', r'override', r'his word', r'STANDING', r'standing']
rxb = re.compile('|'.join(BROAD2))


def windows(text, rex=None, w=None):
    rex = rex or rx
    w = w or W
    spans = []
    for m in rex.finditer(text):
        a, b = max(0, m.start() - w), min(len(text), m.end() + w)
        if spans and a <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(spans[-1][1], b))
        else:
            spans.append((a, b))
    return spans


def main():
    units = json.load(open(os.path.join(OUT, 'units.json'), encoding='utf-8'))
    out, nwin, nchars = [], 0, 0
    broad_only = []
    for u in units:
        sp = windows(u['text'])
        if sp:
            for a, b in sp:
                out.append({'uid': u['uid'], 'span': [a, b], 'text': u['text'][a:b]})
                nwin += 1
                nchars += b - a
        elif u['broad']:
            for a, b in windows(u['text'], rxb, WB):
                broad_only.append({'uid': u['uid'], 'span': [a, b], 'text': u['text'][a:b]})
    with open(os.path.join(OUT, 'windows.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    with open(os.path.join(OUT, 'broad_only.json'), 'w', encoding='utf-8') as f:
        json.dump(broad_only, f, ensure_ascii=False)
    print(json.dumps({'windows': nwin, 'window_chars': nchars,
                      'units_with_windows': len(set(w['uid'] for w in out)),
                      'broad_only_units': len(broad_only),
                      'broad_only_chars': sum(len(b['text']) for b in broad_only)}, indent=2))


if __name__ == '__main__':
    main()
