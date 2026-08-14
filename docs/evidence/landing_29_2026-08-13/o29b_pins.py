#!/usr/bin/env python3
"""ORDER 29B -- THE PIN RESTAMP, WITH THE MOVED-SET EXPLICITLY ASSERTED (PREREG_29B P29B-22).

ORDER 29's o29_pins.py with ONE thing changed and nothing else: the DECLARED MOVED-SET, which is
29B's, not 29's. The measurement, the classification, the must-not-move assertions, the fv treatment
and the surgical rewrite are carried over verbatim. Anything moving outside the declared set HALTS
here rather than being restamped quietly.

29B additionally measures pvc_curve_v2.json, which expected_boot does NOT pin. It is reported as a
DECLARED FILE MOVER with its curve PAYLOAD md5 asserted UNMOVED -- the borrowed cells and their
disclosure live in pool_v0, and if the curve payload had moved, _v0surf_sig would have invalidated
the frozen surface and this act would have owed a re-bake. It does not.

  usage: python3 o29b_pins.py [--write]
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

# THE DECLARED MOVED-SET for ORDER 29B (PREREG_29B P29B-22, filed before the wiring was written)
EXPECTED_MOVERS = {
    'board':       'the entry wiring — 89 day-0 entrants now print derived v0 x numeraire',
    'rl_model':    'the P9 unsigned-cell halt replaced by the signed-cell COVERAGE assert (Step 2)',
    'engine_head': 'the day-0 branch in ev() (_merged_recover.py) — Step 3',
}
MUST_NOT_MOVE = ['store', 'v0surf', 'config', 'band', 'bust_prior', 'peak_model', 'q97m',
                 'pvc_snapshot', 'register']

P("=" * 116)
P("ORDER 29B  --  THE PIN RESTAMP, MOVED-SET ASSERTED  (PREREG_29B P29B-22)")
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
        moved.append(k); v = 'MOVED — declared'
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

P()
P("  P29B-22's MUST-NOT-MOVE LIST, each asserted against a real hash on the FINAL board:")
for k in MUST_NOT_MOVE:
    if boot.get(k) is None or ACTUAL.get(k) is None:
        P("     %-14s not pinned / not on disk — n/a" % k); continue
    ok = str(boot[k]) == str(ACTUAL[k])
    P("     %-14s %s   %s" % (k, 'UNMOVED' if ok else '*** MOVED ***', str(ACTUAL[k])[:16]))
    assert ok, 'P29B-22 BREACH: %s moved and is not in the declared set' % k

# ---- the artifact: a DECLARED file mover whose CURVE PAYLOAD must be unmoved -----------------------
ART = ROOT + '/engine/rl_after/pvc_curve_v2.json'
_a = json.load(open(ART))
P()
P("  pvc_curve_v2.json — NOT pinned in expected_boot, measured and declared here:")
P("     file md5              52aa11258e83a0c8a549940ab3b4388a  ->  %s" % md5f(ART))
P("     curve_md5 (PAYLOAD)   9729f0c5  ->  %s   %s"
  % (_a['curve_md5'], 'UNMOVED' if _a['curve_md5'] == '9729f0c5' else '*** MOVED ***'))
P("     unsigned_cells        ['PDN|KPF','PDS|KPF']  ->  %s" % _a['pool_v0']['unsigned_cells'])
P("     borrowed_cells        %s" % sorted(_a['pool_v0'].get('borrowed_cells') or {}))
assert _a['curve_md5'] == '9729f0c5', (
    'ORDER 29B HALT: the curve PAYLOAD md5 moved. _v0surf_sig hashes the active pick curve, so a moved '
    'payload would invalidate the frozen year-zero surface and this act would owe a re-bake it did not '
    'declare. The borrowed cells live in pool_v0 and must not touch the curve.')
assert not _a['pool_v0']['unsigned_cells'], 'ORDER 29B HALT: an unsigned cell survives the signing.'

# ---- fv: the PRE-EXISTING staleness, carried, documented, and NOT laundered ------------------------
P()
P("  fv — THE INHERITED ORDER-28 STALENESS, CARRIED FORWARD AND NOT 'FIXED':")
P("     expected_boot fv pin      %s" % boot.get('fv'))
P("     moved by ORDER 28 (distribution_pricing.py::v_at_peak), NOT by ORDER 29 and NOT by ORDER 29B.")
P("     This act does not touch engine/forward_valuation at all — the RL_ENTRY29B=0 kill-switch build")
P("     reproduces 86c8d5d9 BYTE-EXACT with that source in place, which is what proves it inert here.")
P("     Re-pinning an identity this act did not move would launder ORDER 28's drift through 29B's")
P("     restamp, so it is left red and reported.")

# ---- a pre-existing contract staleness, found while measuring; reported, not fixed -----------------
_rc = json.load(open(ROOT + '/data/release_contract.json'))
_rcp = (_rc.get('pvc_provenance') or {}).get('curve_payload_md5')
P()
P("  PRE-EXISTING, REPORTED NOT FIXED: data/release_contract.json::pvc_provenance.curve_payload_md5")
P("     carries %r while the shipped curve payload is %r. It was ALREADY stale at ORDER 29's landing"
  % (_rcp, _a['curve_md5']))
P("     (the ruling-C tiebreak moved df766dff -> 9729f0c5 and the contract was not restamped). ORDER 29B")
P("     does not move the curve payload, so this is not 29B's drift and 29B does not restamp it.")

assert not breach, 'UNDECLARED PIN MOVERS: %s — stop and report, do not restamp' % breach

if WRITE:
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

open(HERE + '/PINS29B_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'moved': moved, 'unmoved': unmoved, 'undeclared': breach,
           'actual': ACTUAL, 'expected_movers': EXPECTED_MOVERS,
           'pvc_curve_file_md5': md5f(ART), 'curve_payload_md5': _a['curve_md5'],
           'release_contract_curve_payload_md5_stale': _rcp},
          open(HERE + '/PINS29B.json', 'w'), indent=1)
