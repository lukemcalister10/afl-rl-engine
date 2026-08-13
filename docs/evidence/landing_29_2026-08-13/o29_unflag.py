#!/usr/bin/env python3
"""ORDER 29 -- STEP 1, THE UNFLAG-THREE.

Deletes the `_pvc_exclude` KEY (prereg P2: the whole key, not a false value) from exactly three store
rows -- dylan-shiel (ND 2011 pick 4), jeremy-cameron (pick 12), adam-treloar (pick 14) -- and proves
by measurement that nothing else moved.

The edit is done as a BYTE SURGERY on the single-line store, not by re-serialising it: a json.dump
round-trip would rewrite all 1.98 MB and make "the diff is exactly three deleted keys" unprovable by
inspection.  The structural asserts below then re-parse both sides and compare row by row, key by key,
so the byte surgery is checked against the object model rather than trusted.

  usage:  python3 o29_unflag.py --check   (assert only, no write)
          python3 o29_unflag.py --apply   (assert, write, re-assert)
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STORE = ROOT + '/engine/rl_after/rl_model_data.json'

THREE = {'dylan-shiel': 4, 'jeremy-cameron': 12, 'adam-treloar': 14}
NEEDLE = '"_pvc_exclude": true, '
LIVE_STORE_MD5 = 'd9a24282357cf3083b1640466e3ecd83'

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def md5s(b):
    return hashlib.md5(b if isinstance(b, bytes) else b.encode()).hexdigest()


mode = sys.argv[1] if len(sys.argv) > 1 else '--check'
raw = open(STORE, 'r', encoding='utf-8').read()

P("=" * 110)
P("ORDER 29  --  STEP 1, THE UNFLAG-THREE   (%s)" % mode)
P("=" * 110)
P("  store            %s" % STORE)
P("  md5 at entry     %s   %s" % (md5s(raw), 'MATCHES LIVE d9a24282' if md5s(raw) == LIVE_STORE_MD5 else '*** UNEXPECTED ***'))
P("  bytes at entry   %d" % len(raw))
assert md5s(raw) == LIVE_STORE_MD5, "store is not the live store -- halt"

OLD = json.loads(raw)

# ------------------------------------------------------------------ pre-state, measured not assumed
pre_flagged = [p for p in OLD if '_pvc_exclude' in p]
P()
P("  PRE-STATE")
P("    rows in store                 %d" % len(OLD))
P("    rows carrying _pvc_exclude    %d" % len(pre_flagged))
for p in pre_flagged:
    P("      %-16s %s %d  pick %-3s  _pvc_exclude=%r" %
      (p.get('key'), p.get('type'), p.get('year'), p.get('pick'), p['_pvc_exclude']))
assert len(pre_flagged) == 3, "expected exactly three flagged rows"
assert {p['key'] for p in pre_flagged} == set(THREE), "the flagged three are not the ruled three"
for p in pre_flagged:
    assert p['pick'] == THREE[p['key']], "%s is at pick %s, expected %d" % (p['key'], p['pick'], THREE[p['key']])
    assert p['type'] == 'ND' and p['year'] == 2011, "%s is not an ND-2011 row" % p['key']

occ = raw.count(NEEDLE)
P("    byte occurrences of %r: %d" % (NEEDLE, occ))
assert occ == 3, "the needle does not occur exactly three times -- byte surgery is unsafe, halt"

# ------------------------------------------------------------------ the surgery
new = raw.replace(NEEDLE, '')
P()
P("  THE EDIT")
P("    bytes removed    %d   (= 3 x %d, the needle exactly)" % (len(raw) - len(new), len(NEEDLE)))
assert len(raw) - len(new) == 3 * len(NEEDLE), "byte delta is not three needles"
NEW = json.loads(new)

# ------------------------------------------------------------------ P2 asserts, each able to fail
P()
P("  PREREG P2 ASSERTS")

# P2.a -- zero _pvc_exclude rows
post_flagged = [p for p in NEW if '_pvc_exclude' in p]
P("    P2.a  store carries ZERO _pvc_exclude rows            3 -> %d    %s"
  % (len(post_flagged), 'PASS' if not post_flagged else 'FAIL'))
assert not post_flagged

# P2.b -- ND-2011 is 81 rows, zero duplicate picks
nd11 = [p for p in NEW if p.get('type') == 'ND' and p.get('year') == 2011]
picks = [p.get('pick') for p in nd11]
dups = {k: v for k, v in collections.Counter(picks).items() if v > 1}
P("    P2.b  ND-2011 cohort rows                              %d       %s"
  % (len(nd11), 'PASS' if len(nd11) == 81 else 'FAIL'))
P("          ND-2011 duplicate picks                          %s        %s"
  % (dups or '{}', 'PASS' if not dups else 'FAIL'))
P("          ND-2011 pick set == 1..81 contiguous             %s      %s"
  % (sorted(picks) == list(range(1, 82)), 'PASS' if sorted(picks) == list(range(1, 82)) else 'FAIL'))
assert len(nd11) == 81 and not dups and sorted(picks) == list(range(1, 82))

# P2.c -- the three are curve-contributing at their stored picks
#         _in_pvc(p) is rl_model.py:328  ->  not p.get('_pvc_exclude')
def _in_pvc(p): return not p.get('_pvc_exclude')
NEWK = {p['key']: p for p in NEW if p.get('key')}
P("    P2.c  the three are curve-contributing (_in_pvc true) at their stored picks:")
for k, pk in sorted(THREE.items(), key=lambda kv: kv[1]):
    r = NEWK[k]
    ok = _in_pvc(r) and r['pick'] == pk and r['type'] == 'ND' and r['year'] == 2011
    P("            %-16s pick %-3d  _in_pvc=%-5s  %s" % (k, r['pick'], _in_pvc(r), 'PASS' if ok else 'FAIL'))
    assert ok

# P2.d -- the diff is EXACTLY three deleted keys and nothing else
P("    P2.d  the diff against the live store, computed row by row:")
assert len(OLD) == len(NEW), "row count changed"
deleted, changed, added = [], [], []
for i, (a, b) in enumerate(zip(OLD, NEW)):
    ka, kb = set(a), set(b)
    for kk in ka - kb: deleted.append((i, a.get('key'), kk))
    for kk in kb - ka: added.append((i, a.get('key'), kk))
    for kk in ka & kb:
        if a[kk] != b[kk]: changed.append((i, a.get('key'), kk, a[kk], b[kk]))
P("            rows                                           %d -> %d" % (len(OLD), len(NEW)))
P("            KEYS DELETED                                   %d" % len(deleted))
for i, k, kk in deleted: P("               row %-5d %-16s  -%s" % (i, k, kk))
P("            KEYS ADDED                                     %d" % len(added))
P("            VALUES CHANGED                                 %d" % len(changed))
for c in changed: P("               *** %r" % (c,))
ok = (len(deleted) == 3 and not added and not changed
      and {(k, kk) for _, k, kk in deleted} == {(k, '_pvc_exclude') for k in THREE})
P("            VERDICT: exactly three deleted keys, no value / pick / position / birth-year /")
P("                     games field moved on any row          %s" % ('PASS' if ok else 'FAIL'))
assert ok

# key ORDER within each row is preserved too (the needle removal cannot reorder, but prove it)
order_ok = all(list(a) == list(b) + [] if False else
               [x for x in a if x != '_pvc_exclude'] == list(b) for a, b in zip(OLD, NEW))
P("            key ORDER within every row preserved            %s" % ('PASS' if order_ok else 'FAIL'))
assert order_ok

P()
P("  RESULT md5 %s   bytes %d" % (md5s(new), len(new)))

if mode == '--apply':
    with open(STORE, 'w', encoding='utf-8') as f: f.write(new)
    back = open(STORE, 'r', encoding='utf-8').read()
    assert back == new, "write-back mismatch"
    P("  WRITTEN.  store md5 %s -> %s" % (LIVE_STORE_MD5, md5s(back)))
else:
    P("  CHECK ONLY -- nothing written.")

open(HERE + '/UNFLAG29_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'mode': mode, 'store_md5_pre': LIVE_STORE_MD5, 'store_md5_post': md5s(new),
           'bytes_pre': len(raw), 'bytes_post': len(new),
           'deleted_keys': [{'row': i, 'key': k, 'field': kk} for i, k, kk in deleted],
           'nd2011_rows': len(nd11), 'nd2011_dup_picks': dups,
           'three': {k: {'pick': NEWK[k]['pick'], 'in_pvc': _in_pvc(NEWK[k])} for k in THREE}},
          open(HERE + '/UNFLAG29.json', 'w'), indent=1)
