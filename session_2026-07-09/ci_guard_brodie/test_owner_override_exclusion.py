#!/usr/bin/env python3
"""PART B EXCLUSION TEST — the Brodie owner override is DISPLAY-ONLY and excluded from everything a guard
or aggregate measures (2026-07-09).

Proves the acceptance property: the exported board is byte-identical with the override ON vs OFF EXCEPT
for the added `ov` (display) block on the overridden player's row. i.e.
  - every player's engine value `v` is identical on vs off,
  - every aggregate / analytics / curve / pick block is identical on vs off,
  - the ONLY difference is the overridden player's DISPLAYED row gaining its `ov` block,
  - and that displayed value == round(v * factor) with a visible marker.

HOW
  Builds the real board twice via rl_export.py (a subprocess each, honoring the one-engine-load rule):
    OFF: RL_NO_OWNER_OVERRIDES=1   ON: default.
  Then byte-compares the two boards. Run from the bootstrapped workspace under the panel env, e.g.:
    cd /home/claude/rl_workspace/rl_after && \
    RL_REPO=<repo> python3 <repo>/session_2026-07-09/ci_guard_brodie/test_owner_override_exclusion.py
  (RL_REPO must point at the checkout so the display input data/owner_overrides.json is found.)
Exits non-zero on any violation.
"""
import os, sys, json, copy, subprocess, tempfile

RA = os.environ.get('RL_WS', '/home/claude/rl_workspace/rl_after')
BOARD = os.path.join(RA, 'rl_app_data.json')

FAIL = []
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond: FAIL.append(msg)

def build(overrides_on):
    env = dict(os.environ)
    if overrides_on:
        env.pop('RL_NO_OWNER_OVERRIDES', None)
    else:
        env['RL_NO_OWNER_OVERRIDES'] = '1'
    env.setdefault('PYTHONHASHSEED', '0')
    r = subprocess.run([sys.executable, 'rl_export.py'], cwd=RA, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        print(r.stdout)
        raise SystemExit("rl_export.py failed (overrides_on=%s), exit=%d" % (overrides_on, r.returncode))
    with open(BOARD) as f:
        return json.load(f)

print("=== PART B: owner override is display-only + excluded from all guards/aggregates ===")
print("    building board OFF (RL_NO_OWNER_OVERRIDES=1) ...")
off = build(False)
print("    building board ON  (default) ...")
on = build(True)

# --- the ON board, with every `ov` block stripped, must be byte-identical to the OFF board ---------------
on_stripped = copy.deepcopy(on)
overridden = []
for row in on_stripped['active']:
    if 'ov' in row:
        overridden.append(row['key'])
        del row['ov']
check(json.dumps(on_stripped, sort_keys=True) == json.dumps(off, sort_keys=True),
      "ON board minus every `ov` block == OFF board, byte-for-byte (aggregates/curves/values untouched)")

# --- exactly the intended player(s) carry an override, and NOTHING else differs -------------------------
off_keys = {r['key'] for r in off['active']}
on_keys = {r['key'] for r in on['active']}
check(off_keys == on_keys, "same player set on vs off (no row added/removed)")
check(overridden == ['will-brodie'],
      "exactly Brodie's row carries the override (got %s)" % overridden)

# --- every player's engine value v is identical on vs off (this is what every guard/aggregate reads) -----
off_v = {r['key']: r['v'] for r in off['active']}
on_v = {r['key']: r['v'] for r in on['active']}
vdiff = [k for k in off_v if off_v[k] != on_v.get(k)]
check(not vdiff, "every engine value v identical on vs off; differing keys=%s" % vdiff[:8])

# --- the only per-row difference is Brodie gaining a well-formed, marked `ov` display block --------------
brod_off = [r for r in off['active'] if r['key'] == 'will-brodie'][0]
brod_on = [r for r in on['active'] if r['key'] == 'will-brodie'][0]
check('ov' not in brod_off, "OFF board: Brodie has NO ov block")
check('ov' in brod_on, "ON board: Brodie HAS an ov block")
if 'ov' in brod_on:
    ov = brod_on['ov']
    check(brod_on['v'] == brod_off['v'], "Brodie engine v unchanged by the override (%s == %s)" % (brod_on['v'], brod_off['v']))
    check(ov.get('factor') == 0.5, "override factor == 0.50 (got %s)" % ov.get('factor'))
    check(ov.get('dispv') == int(round(brod_on['v'] * ov['factor'])),
          "displayed value == round(v * factor) = %d (got %s)" % (int(round(brod_on['v'] * 0.5)), ov.get('dispv')))
    check(isinstance(ov.get('mark'), str) and 'OVERRIDE' in ov['mark'].upper(),
          "displayed row carries a visible override MARKER (got %r)" % ov.get('mark'))
    # the difference between the two Brodie rows is EXACTLY the added ov key, nothing else
    diff_keys = set(brod_on) ^ set(brod_off)
    check(diff_keys == {'ov'}, "Brodie row differs from OFF by exactly {'ov'} (got %s)" % diff_keys)
    same = all(brod_on[k] == brod_off[k] for k in brod_off)
    check(same, "every other Brodie field is identical on vs off")

print("\n" + ("PART B EXCLUSION TEST FAILED: %d check(s)\n  - " % len(FAIL) + "\n  - ".join(FAIL) if FAIL else
      "PART B EXCLUSION TEST PASSED: guards/aggregates/values byte-identical on vs off; only Brodie's DISPLAYED row differs (+ov ×0.50 marked)."))
sys.exit(1 if FAIL else 0)
