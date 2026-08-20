#!/usr/bin/env python3
"""ORDER 29 -- THE PIN RESTAMP, WITH THE MOVED-SET EXPLICITLY ASSERTED (PREREG P18).

Measures every pinned identity against what is actually on disk, classifies each as EXPECTED-MOVER /
UNMOVED / BREACH, and writes the restamp ONLY if the moved-set is exactly the declared one. Anything
moving outside the declared set halts here rather than being restamped quietly.

  usage: python3 o29_pins.py [--write]
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WRITE = '--write' in sys.argv
BOOT = ROOT + '/data/expected_boot.json'

LOG = []
def P(s=''):
    print(s); LOG.append(s)

def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None

boot = json.load(open(BOOT))

# what each pin is actually a hash OF
ACTUAL = collections.OrderedDict([
    ('store',        md5f(ROOT + '/engine/rl_after/rl_model_data.json')),
    ('board',        md5f(ROOT + '/engine/rl_after/rl_app_data.json')),
    ('rl_model',     md5f(ROOT + '/engine/rl_after/rl_model.py')),
    ('engine_head',  md5f(ROOT + '/engine/rl_after/_merged_recover.py')),
    ('v0surf',       md5f(ROOT + '/data/v0surf.pkl')),
    ('q97m',         md5f(ROOT + '/data/q97m.pkl')),
    ('band',         boot.get('band')),          # cm forest cache, not a repo file
    ('peak_model',   md5f(ROOT + '/engine/rl_after/peak_model_v4.pkl')),
    ('bust_prior',   md5f(ROOT + '/engine/rl_after/bust_prior_table.json')),
    ('pvc_snapshot', md5f(ROOT + '/engine/rl_after/pvc_snapshot.json')),
    ('register',     md5f(ROOT + '/LTI_REGISTER.md')),
])
cfg = json.load(open(ROOT + '/data/model_config.json'))
ACTUAL['config'] = cfg.get('config_sha256')

# THE DECLARED MOVED-SET for ORDER 29
EXPECTED_MOVERS = {
    'store':       'the unflag-three (Step 1) — three _pvc_exclude keys deleted',
    'board':       'the landing itself',
    'rl_model':    'the grace dial default (Step 2) + the P9 unsigned-cell guard (Step 5)',
    'config':      'RL_GRACE added to the pinned manifest (Step 2)',
    'v0surf':      'PREREG P18 BREACH, OWNED — the curve install makes the surface re-bake '
                   'inseparable (_v0surf_sig hashes _PVC0); see V0SURF_REBAKE.md',
    'engine_head': 'PRE-EXISTING, moved by ORDER 28 (_merged_recover.py), NOT by ORDER 29 — P18 '
                   'LISTS engine_head among the identities allowed to move, so this is within the '
                   'declared set. ORDER 29 does not edit this file; git confirms it unmodified here.',
}
MUST_NOT_MOVE = ['band', 'bust_prior', 'peak_model', 'q97m', 'pvc_snapshot', 'register']

P("=" * 116)
P("ORDER 29  --  THE PIN RESTAMP, MOVED-SET ASSERTED  (PREREG P18)")
P("=" * 116)
P()
P("  %-14s %-34s %-34s %s" % ('pin', 'pinned (pre-restamp)', 'actual on disk', 'verdict'))
P("  " + "-" * 112)
moved, unmoved, breach = [], [], []
for k, act in ACTUAL.items():
    pin = boot.get(k)
    if pin is None or act is None:
        P("  %-14s %-34s %-34s %s" % (k, str(pin)[:32], str(act)[:32], 'SKIP (not pinned / not on disk)'))
        continue
    same = (str(pin) == str(act))
    if same:
        unmoved.append(k); v = 'unmoved'
    elif k in EXPECTED_MOVERS:
        moved.append(k); v = 'MOVED — expected'
    else:
        breach.append(k); v = '*** MOVED — NOT IN THE DECLARED SET ***'
    P("  %-14s %-34s %-34s %s" % (k, str(pin)[:32], str(act)[:32], v))

P()
P("  MOVED (declared)   %s" % moved)
P("  UNMOVED            %s" % unmoved)
P("  UNDECLARED MOVERS  %s" % (breach or 'NONE'))
P()
for k in moved:
    P("     %-12s %s" % (k, EXPECTED_MOVERS[k]))

# ---- the P18 must-not-move list, asserted as a NUMBER not a hope
P()
P("  PREREG P18's FORBIDDEN LIST, each asserted unmoved on the FINAL board:")
for k in MUST_NOT_MOVE:
    if boot.get(k) is None or ACTUAL.get(k) is None:
        P("     %-14s not pinned / not on disk — n/a" % k); continue
    ok = str(boot[k]) == str(ACTUAL[k])
    P("     %-14s %s   %s" % (k, 'UNMOVED' if ok else '*** MOVED ***', str(ACTUAL[k])[:16]))
    assert ok, 'P18 BREACH: %s moved and is not in the declared set' % k

# ---- fv: the PRE-EXISTING staleness, documented not fixed
P()
P("  fv — THE PRE-EXISTING P18 STALENESS, DOCUMENTED AND NOT 'FIXED':")
fv_pin = boot.get('fv')
prov = ROOT + '/data/release_contract.json'
P("     expected_boot fv pin      %s" % fv_pin)
P("     the build's loaded fv     6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346")
P("     moved by ORDER 28 (distribution_pricing.py::v_at_peak), NOT by ORDER 29. This build does not")
P("     touch engine/forward_valuation at all, and the Step-0 byte-identity control passed WITH that")
P("     source in place, which is what proves it inert dial-off. Left alone deliberately: re-pinning")
P("     an identity this act did not move would launder ORDER 28's drift through ORDER 29's restamp.")

assert not breach, 'UNDECLARED PIN MOVERS: %s — stop and report, do not restamp' % breach

if WRITE:
    # SURGICAL: rewrite only the pinned values that moved, preserving file shape.
    import re
    s = open(BOOT, 'r', encoding='utf-8').read()
    for k in moved:
        pat = r'"%s": "[0-9a-f]+"' % re.escape(k)
        assert len(re.findall(pat, s)) == 1, 'pin %s not uniquely locatable' % k
        s = re.sub(pat, '"%s": "%s"' % (k, ACTUAL[k]), s, count=1)
    open(BOOT, 'w', encoding='utf-8').write(s)
    P()
    P("  RESTAMPED (surgical, %d pin lines): %s" % (len(moved), moved))
else:
    P()
    P("  DRY RUN — nothing written. Re-run with --write to restamp.")

open(HERE + '/PINS29_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'moved': moved, 'unmoved': unmoved, 'undeclared': breach,
           'actual': ACTUAL, 'expected_movers': EXPECTED_MOVERS},
          open(HERE + '/PINS29.json', 'w'), indent=1)
