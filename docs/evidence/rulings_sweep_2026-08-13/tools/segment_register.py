#!/usr/bin/env python3
"""ORDER 27 sweep tool: deterministic segmentation + lexicon screen of the register.

READ-ONLY on the register. Writes only into docs/evidence/rulings_sweep_2026-08-13/.
Segmentation:
  * line 1 (the appended prose stream, ~962 KB) is split on the register's own
    ' · ' entry separator (kept as SEG units, preserving order and offsets);
  * lines 2+ (the SEAM-era content) are split into blank-line-delimited BLOCK units.
Screening: a broad, high-recall ruling lexicon (see METHOD.md #3).
"""
import re
import json
import os
import sys

REG = 'docs/OPEN_ITEMS_REGISTER.md'
OUT = 'docs/evidence/rulings_sweep_2026-08-13/tools'

SEP = re.compile(r'(?<=[\.\)”\"a-zA-Z0-9]) · ')

BROAD = [r'OWNER[- ]RUL', r'owner[- ]rul', r'RULED', r'RULING', r'ruling', r'owner word', r'OWNER WORD',
         r'owner-worded', r'owner override', r'owner overrule', r'OVERRIDE', r'override', r'owner-caught',
         r'OWNER-CAUGHT', r'\bLAW\b', r'\blaw\b', r'STANDING', r'standing', r'EXCLUDE', r'exclude',
         r'EXCLUSION', r'DEFERRED', r'deferred', r'verbatim', r'VERBATIM', r'filed \d{6,}', r'ratified',
         r'RATIFIED', r'owner-directed', r'owner-ordered', r'owner’s word', r"owner's word", r'FROZEN',
         r'frozen', r'PARKED', r'parked', r'owner-approved', r'owner said', r'his word', r'BINDING',
         r'binding', r'MANDAT', r'mandat', r'convention', r'CONVENTION', r'NEVER', r'ALWAYS', r'MUST']

CORE = [r'OWNER[- ]RUL', r'owner[- ]rul', r'\bRULED\b', r'owner word', r'OWNER WORD', r'owner override',
        r'owner overrule', r'owner-caught', r'OWNER-CAUGHT', r'RULED \(STANDING\)', r'verbatim',
        r'filed \d{6,}', r'owner-directed', r'owner-ordered', r"owner's word", r'owner’s word',
        r'owner-worded', r'DEFERRED \(owner', r'ratified', r'owner says', r'owner said', r'owner-ratified',
        r'THE [A-Z][A-Z —-]{2,40} LAW']

rx_broad = re.compile('|'.join(BROAD))
rx_core = re.compile('|'.join(CORE))


def main():
    txt = open(REG, encoding='utf-8').read()
    lines = txt.split('\n')
    parts = SEP.split(lines[0])
    blocks, cur = [], []
    for ln in lines[1:]:
        if ln.strip() == '':
            if cur:
                blocks.append('\n'.join(cur))
                cur = []
        else:
            cur.append(ln)
    if cur:
        blocks.append('\n'.join(cur))

    units = []
    for i, p in enumerate(parts):
        units.append({'uid': 'SEG%04d' % i, 'kind': 'line1-seg', 'idx': i, 'chars': len(p),
                      'broad': bool(rx_broad.search(p)), 'core': bool(rx_core.search(p)), 'text': p})
    for i, b in enumerate(blocks):
        units.append({'uid': 'BLK%04d' % i, 'kind': 'tail-block', 'idx': i, 'chars': len(b),
                      'broad': bool(rx_broad.search(b)), 'core': bool(rx_core.search(b)), 'text': b})

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'units.json'), 'w', encoding='utf-8') as f:
        json.dump(units, f, ensure_ascii=False)

    tot = len(units)
    broad_n = sum(1 for u in units if u['broad'])
    core_n = sum(1 for u in units if u['core'])
    stats = {
        'register_bytes': len(txt),
        'line1_bytes': len(lines[0]),
        'tail_lines': len(lines) - 1,
        'units_total': tot,
        'line1_segments': len(parts),
        'tail_blocks': len(blocks),
        'broad_hits': broad_n,
        'broad_hit_chars': sum(u['chars'] for u in units if u['broad']),
        'core_hits': core_n,
        'core_hit_chars': sum(u['chars'] for u in units if u['core']),
        'no_hit_units': tot - broad_n,
        'no_hit_chars': sum(u['chars'] for u in units if not u['broad']),
    }
    with open(os.path.join(OUT, 'segment_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    json.dump(stats, sys.stdout, indent=2)
    print()


if __name__ == '__main__':
    main()
