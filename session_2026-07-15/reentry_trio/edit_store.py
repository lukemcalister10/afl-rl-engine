#!/usr/bin/env python3
"""RE-ENTRY TRIO STORE CORRECTION (item 108a / register item 10a, owner-ruled 2026-07-12).
Record the LATER (SSP re-entry) entry for Flynn Perez / Lachlan McAndrew / Mark Keane onto the ONE
authored store (SSI: change THE SOURCE). Fields per the ruled v30 record (register item 17 ii):
type=SSP + re-entry year + pick None; SSP is pickless by convention (_pickless True, _draft 'SSP').
Identity/original-entry facts (stable_player_id, _by, scoring, games, positions) are UNTOUCHED.
Byte-format preserved: default json.dumps (ensure_ascii, ', '/': ' separators), no trailing newline.
"""
import json, hashlib, sys

STORE = '/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'
# name -> (re-entry type, re-entry year)  — verbatim from the ruling (SSP 2025 / 2024 / 2022)
TRIO = {
    'flynn-perez':     ('SSP', 2025),
    'lachlan-mcandrew':('SSP', 2024),
    'mark-keane':      ('SSP', 2022),
}

raw = open(STORE).read()
obj = json.loads(raw)
assert json.dumps(obj, ensure_ascii=True) == raw, 'round-trip format mismatch — refusing to rewrite'
old_md5 = hashlib.md5(raw.encode()).hexdigest()

changed = []
for p in obj:
    k = p.get('key')
    if k in TRIO:
        t, yr = TRIO[k]
        before = {f: p.get(f) for f in ('type','year','pick','_pickless','_draft')}
        p['type'] = t
        p['year'] = yr
        p['pick'] = None
        p['_pickless'] = True
        p['_draft'] = 'SSP'
        after = {f: p.get(f) for f in ('type','year','pick','_pickless','_draft')}
        changed.append((k, before, after))

assert len(changed) == 3, 'expected exactly 3 trio rows, changed %d' % len(changed)

out = json.dumps(obj, ensure_ascii=True)
if '--write' in sys.argv:
    open(STORE, 'w').write(out)
new_md5 = hashlib.md5(out.encode()).hexdigest()
print('store md5 %s -> %s  (%s)' % (old_md5[:8], new_md5[:8], 'WRITTEN' if '--write' in sys.argv else 'DRY-RUN'))
for k, b, a in changed:
    print('  %-18s %s' % (k, b))
    print('  %-18s -> %s' % ('', a))
