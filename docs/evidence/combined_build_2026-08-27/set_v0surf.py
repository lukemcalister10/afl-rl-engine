#!/usr/bin/env python3
"""Swap the v0surf artifact between the two frozen worlds and restamp the pin coherently.
The refit (--bake) froze the SMOOTHED-curve signatures; the kill-switch/F1 world (dials off,
original pvc) needs the ORIGINAL pkl and pin. A leg that binds one without the other trips
either the frozen-signature halt or the boot pin — this helper makes the swap atomic.
  usage: set_v0surf.py <ROOT> pre|refit
"""
import hashlib, json, os, shutil, sys

ROOT = os.path.abspath(sys.argv[1]); which = sys.argv[2]
EV = os.path.join(ROOT, 'docs', 'evidence', 'combined_build_2026-08-27')
SRC = {'pre': os.path.join(EV, 'pre_bake', 'v0surf.pkl'),
       'refit': os.path.join(EV, 'v0surf_refit.pkl')}[which]
dst = os.path.join(ROOT, 'data', 'v0surf.pkl')
shutil.copy2(SRC, dst)
md5 = hashlib.md5(open(dst, 'rb').read()).hexdigest()
ebp = os.path.join(ROOT, 'data', 'expected_boot.json')
eb = json.load(open(ebp)); eb['v0surf'] = md5
json.dump(eb, open(ebp, 'w'), indent=1, sort_keys=True)
print('v0surf -> %s (%s) · pin restamped' % (which, md5[:8]))
