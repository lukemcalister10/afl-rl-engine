#!/usr/bin/env python3
"""tools/draft_companion/build_page.py — inject v0_tables.json into template.html -> draft_night.html.
Run after extract_v0_tables.py. The page is published as a claude.ai artifact (see README.md)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, 'v0_tables.json')))
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
blob = json.dumps(data, separators=(',', ':')).replace('</', '<\\/')
assert tpl.count('/*__DATA__*/') == 1
open(os.path.join(HERE, 'draft_night.html'), 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', blob))
print('wrote draft_night.html (%d bytes)' % os.path.getsize(os.path.join(HERE, 'draft_night.html')))
