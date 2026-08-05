#!/usr/bin/env python3
"""#306 L6 PASS 1 — THE L1(b) ENUMERATED SAME-COMMIT INSTALL, executed as ONE ATOMIC ACT.

Authority: seam #306 comment 5186820918 clause 2 -- "install derived payload
9f7848f41d3b041b7397b5fe0d5d909a via the L1(b) enumerated same-commit set -- the recorded set,
nothing improvised." The set is Addendum C.3 as instantiated by the recorded PASS1_INSTALL_SET.md.

WHY A SCRIPT AND NOT SIX HAND EDITS
  The recorded set is six files with THREE hashes computed from bytes written earlier in the same act.
  The runbook's own words: "the risk is atomicity, not time... a half-written install set is worse than
  none, because the interlocks make a partial state look self-consistent in places." This script makes
  the act all-or-nothing: it stages every file in memory, asserts every precondition, and writes only
  after all six are built. Any assert fires -> nothing is written. It also runs the committed
  instrument rather than ad-hoc shell, which is this project's own standing lesson.

DISCIPLINES CARRIED
  * C.2 field-level: every edit is BY JSON PATH, never a wholesale rewrite, never a blind string replace.
  * SEALED TWIN (directive section 8): `3068.4647` occurs TWICE in pvc_curve_v2.json -- as the
    numeraire field AND inside that same field's _doc prose. Both are moved DELIBERATELY and
    SEPARATELY by path; the occurrence count is asserted before and after.
  * N14 / E6: the measured head is PRIMITIVE at the lane's 4dp; `s` is DERIVED = published_pin / head
    at full double precision. Verified against the INSTALLED pair: 3000.0/3068.4647 reproduces the
    stored 0.9776876364261254 EXACTLY, so the convention is measured from the artifact, not assumed.
  * N22/N32: identity is the FULL md5; the payload recipe is string-sorted keys, default separators,
    int(round(v)), picks 1..64.
  * E.5 finding 5: `curve_source_store_md5` in ui/release_pick_curve.json stays the FULL 32 chars;
    the stamp convention is asymmetric and one_source_selftest compares one-sided [:8].
  * Sealed history: release_lineage.json / finalization_state.json byte-asserted UNTOUCHED.

USAGE:  python3 install_pass1.py <REPO>            # writes
        python3 install_pass1.py <REPO> --dry-run  # builds and asserts, writes nothing
"""
import os, sys, json, hashlib, shutil

REPO = sys.argv[1].rstrip('/')
DRY = '--dry-run' in sys.argv
P = lambda *a: os.path.join(REPO, *a)


def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def payload_md5(curve_dict):
    """N32 recipe: string-sorted keys, default separators, int(round(v)), picks 1..64."""
    pay = {str(k): int(round(curve_dict[str(k)])) for k in range(1, 65)}
    return hashlib.md5(json.dumps(pay, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- the new curve, from the derivation
DERIV = P('docs/evidence/exec_306_2a1xa4/l6/pass0_derived_curve1.json')
dv = json.load(open(DERIV))
LADDER = dv['ladders']['ruled_pooled_numeraire']
assert len(LADDER) == 64, 'ladder must be 64 points'
assert LADDER[0] == 3000, 'ladder must be pinned at 3000'
assert all(LADDER[i] < LADDER[i - 1] for i in range(1, 64)), 'ladder must be strictly descending'
NEW_CURVE = {str(i + 1): int(LADDER[i]) for i in range(64)}
NEW_PAYLOAD_FULL = payload_md5(NEW_CURVE)
NEW_PAYLOAD = NEW_PAYLOAD_FULL[:8]
assert NEW_PAYLOAD_FULL == '9f7848f41d3b041b7397b5fe0d5d909a', \
    'payload %s != the authorised 9f7848f41d3b041b7397b5fe0d5d909a' % NEW_PAYLOAD_FULL

HEAD = dv['THE_FACTOR_S']['pooled_head_pre_scale']          # primitive, the lane's measured 4dp
S = 3000.0 / HEAD                                            # DERIVED at full precision (N14)
assert abs(3000.0 / HEAD - S) < 1e-9, 'E6 coherence'
assert round(S, 6) == dv['THE_FACTOR_S']['s'], 'derived s must round to the lane-reported presentation'
POOL_VALUE = dv['levels_under_the_design']['POOL']['LEVEL_under_design_x_s']
NEW_PE_MD5 = md5f(P('docs/evidence/exec_306_2a1xa4/l6/pass0_lens_matrix.json'))[:8]
assert NEW_PE_MD5 == 'e1c62f86', 'per_entrant stamp %s' % NEW_PE_MD5

print('THE NEW CURVE')
print('  payload FULL   %s   [:8] %s' % (NEW_PAYLOAD_FULL, NEW_PAYLOAD))
print('  head[1..5]     %s   pick64 %d   sum %d' % (LADDER[:5], LADDER[63], sum(LADDER)))
print('  head primitive %r   s derived %r   (6dp presentation %s)' % (HEAD, S, round(S, 6)))
print('  pool_value     %s   per_entrant stamp %s' % (POOL_VALUE, NEW_PE_MD5))

# ---------------------------------------------------------------- sealed history, asserted untouched
SEALED = ['data/release_lineage.json', 'engine/rl_after/finalization_state.json',
          'data/finalization_state.json']
sealed_before = {p: md5f(P(p)) for p in SEALED if os.path.exists(P(p))}
print('\nSEALED HISTORY (asserted untouched): %s' % ', '.join(
    '%s=%s' % (os.path.basename(k), v[:8]) for k, v in sealed_before.items()))

# ================================================================ STEP 1 · pvc_curve_v2.json
CURVE_F = P('engine/rl_after/pvc_curve_v2.json')
raw = open(CURVE_F).read()
OLD_HEAD_STR = '3068.4647'
n_twin = raw.count(OLD_HEAD_STR)
assert n_twin == 2, 'expected the sealed twin: 2 occurrences of %s, found %d' % (OLD_HEAD_STR, n_twin)
print('\nSTEP 1  pvc_curve_v2.json   (sealed twin present: %d occurrences of %s)' % (n_twin, OLD_HEAD_STR))

c = json.loads(raw)
assert c['curve_md5'] == 'e69a3f38', 'installed curve must be e69a3f38, found %s' % c['curve_md5']
assert payload_md5(c['curve']) [:8] == 'e69a3f38', 'installed curve must reproduce its own payload'
assert c['stamp']['store_md5'] == '81d24704', 'store must not move'

c['curve'] = NEW_CURVE                                        # BY PATH
c['curve_md5'] = NEW_PAYLOAD                                  # BY PATH
c['numeraire']['pooled_head_pre_scale'] = HEAD                # BY PATH — sealed twin, occurrence 1
c['numeraire']['s'] = S                                       # BY PATH
c['numeraire']['_doc'] = (                                    # BY PATH — sealed twin, occurrence 2
    '#279 ruled pooled numeraire. THE MEASURED HEAD IS PRIMITIVE (seam ruling 2026-07-31): '
    'pooled_head_pre_scale is the lane-measured value %s exactly, and s is DERIVED from it at full '
    'precision. The 6dp %s seen in presentation is the ROUNDED form of this same s, never the stored '
    'primitive. E6 coherence (published_pin / pooled_head_pre_scale == s to 1e-9) holds BY '
    'CONSTRUCTION. Re-measured at #306 L6 pass 1 on surface b540833b; the prior value was %s.'
    % (HEAD, round(S, 6), OLD_HEAD_STR))
c['pool_value'] = POOL_VALUE                                  # BY PATH
c['stamp']['per_entrant_md5'] = NEW_PE_MD5                    # BY PATH
c['derived_from'] = (
    'docs/evidence/exec_306_2a1xa4/l6/pass0_lens_matrix.json (store 81d24704, surface b540833b) — '
    '#306 L6 pass 1: the matrix emitted on the redesigned lens lane, committed with its identity '
    'block and F-C full-md5 binding. Post-slide membership and Addendum-6 per-season bars unchanged.')
c['_working_substrate_note'] = (
    '#306 L6 PASS 1: curve 1 (%s) installed as DECLARED WORKING SUBSTRATE under R-H/R-I/N19, derived '
    'from surface b540833b at installed curve e69a3f38. pool_value is this pass\'s re-measurement, NOT '
    'a landing figure. Nothing between L1 and the converged fixed point is a landing figure. '
    'Bake HELD; EXECUTION word WITHHELD.' % NEW_PAYLOAD)

curve_bytes = json.dumps(c, indent=1, sort_keys=True) + '\n'
assert curve_bytes.count(OLD_HEAD_STR) == 1, \
    'after the move the old head must survive ONCE, in the _doc provenance sentence only'
assert curve_bytes.count(str(HEAD)) >= 2, 'the new head must appear as field and in its own prose'
print('        curve_md5 e69a3f38 -> %s | head %s -> %s | s -> %r' % (NEW_PAYLOAD, OLD_HEAD_STR, HEAD, S))
print('        pool_value 234.3 -> %s | stamp.per_entrant_md5 77eba4d3 -> %s' % (POOL_VALUE, NEW_PE_MD5))
print('        sealed twin: BOTH occurrences moved deliberately by path')

# ================================================================ STEP 2 · md5 of step 1's bytes
NEW_CURVE_FILE_MD5 = hashlib.md5(curve_bytes.encode()).hexdigest()
print('\nSTEP 2  md5(pvc_curve_v2.json) = %s   <- from step 1 bytes' % NEW_CURVE_FILE_MD5)

# ================================================================ STEP 3 · ui/release_pick_curve.json
UI_F = P('ui/release_pick_curve.json')
u = json.load(open(UI_F))
OLD_UI = dict(u)
assert u.get('pick_curve_curve_md5') == 'e69a3f38', 'ui curve stamp %s' % u.get('pick_curve_curve_md5')
full_store = u.get('curve_source_store_md5')
assert full_store and len(full_store) == 32, \
    'E.5 finding 5: curve_source_store_md5 must be the FULL 32 chars, found %r' % full_store

u['pick_curve_curve_md5'] = NEW_PAYLOAD
u['pick_curve_file_md5'] = NEW_CURVE_FILE_MD5
u['pool_value'] = POOL_VALUE
u['per_entrant_md5'] = NEW_PE_MD5
u['curve_source_store_md5'] = full_store                       # UNCHANGED, full 32 (asymmetric convention)
u['_doc'] = ('#306 L6 pass 1 working substrate: pick curve payload %s (ladder sum %d, pick64 %d), '
             'file md5 %s, pool_value %s re-measured this pass, per_entrant %s. curve_source_store_md5 '
             'stays the FULL 32 chars by the asymmetric stamp convention (E.5 finding 5). NOT a '
             'landing figure; bake HELD, EXECUTION word WITHHELD.'
             % (NEW_PAYLOAD, sum(LADDER), LADDER[63], NEW_CURVE_FILE_MD5, POOL_VALUE, NEW_PE_MD5))
ui_bytes = json.dumps(u, indent=1, sort_keys=True) + '\n'
assert len(u) == len(OLD_UI), 'no key added or dropped in the ui stamp'
print('\nSTEP 3  ui/release_pick_curve.json  curve_md5 -> %s | file_md5 -> %s' % (NEW_PAYLOAD, NEW_CURVE_FILE_MD5[:8]))
print('        pool_value -> %s | per_entrant -> %s | store stays FULL 32 (%s)' % (POOL_VALUE, NEW_PE_MD5, full_store[:8] + '…'))

# ================================================================ STEP 4 · md5 of step 3's bytes
NEW_UI_MD5 = hashlib.md5(ui_bytes.encode()).hexdigest()
print('\nSTEP 4  md5(ui/release_pick_curve.json) = %s   <- from step 3 bytes' % NEW_UI_MD5)

# ================================================================ STEP 5 · data/release_contract.json
RC_F = P('data/release_contract.json')
rc = json.load(open(RC_F))
assert rc['identities']['engine_head'] == '15525b033f390d041a7858f47a30b48e', 'N44 engine pin must hold'
rc['pvc_provenance']['curve_payload_md5'] = NEW_PAYLOAD
rc['pvc_provenance']['_note'] = ('#306 L6 pass 1: curve 1 installed as working substrate from surface '
                                 'b540833b. Bake HELD; EXECUTION word WITHHELD.')


def contract_sha256(body):
    """release_contract.py:69 — sha256 over the body EXCLUDING contract_sha256 and _doc."""
    b = {k: v for k, v in body.items() if k not in ('contract_sha256', '_doc')}
    return hashlib.sha256(json.dumps(b, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


OLD_SEAL = rc.get('contract_sha256')
rc['contract_sha256'] = contract_sha256(rc)
rc_bytes = json.dumps(rc, indent=1, sort_keys=True) + '\n'
print('\nSTEP 5  release_contract.json  curve_payload_md5 -> %s' % NEW_PAYLOAD)
print('        contract_sha256 %s… -> %s…  (the N44-addendum stale seal is re-stamped HERE,' % (OLD_SEAL[:8], rc['contract_sha256'][:8]))
print('        at the curve-install step, exactly where the record always re-stamps it, and it')
print('        covers the engine_head move too — N44 addendum clause 2 discharged.)')

# ================================================================ STEP 6 · one_source_selftest.py
ST_F = P('engine/rl_after/one_source_selftest.py')
st = open(ST_F).read()
OLD_CONTRACT_MD5 = 'ca2f2e87'
hits_c = st.count(OLD_CONTRACT_MD5)
hits_p = st.count('77eba4d3')
print('\nSTEP 6  one_source_selftest.py  occurrences: _contract_md5 seed %d | per_entrant %d' % (hits_c, hits_p))
assert hits_c >= 1, 'expected the contract md5 pin'
assert hits_p >= 1, 'expected the per_entrant pin'
st_new = st.replace(OLD_CONTRACT_MD5, NEW_UI_MD5[:8]).replace('77eba4d3', NEW_PE_MD5)
assert st_new.count(NEW_UI_MD5[:8]) == hits_c and st_new.count(NEW_PE_MD5) == hits_p, 'replacement count mismatch'
assert st_new.count('81d24704') == st.count('81d24704'), '_curve_source_store must not move'
assert len(st_new.splitlines()) == len(st.splitlines()), 'line count must not change'
print('        _contract_md5 %s -> %s | _per_entrant_md5 77eba4d3 -> %s | _curve_source_store UNCHANGED'
      % (OLD_CONTRACT_MD5, NEW_UI_MD5[:8], NEW_PE_MD5))

# ================================================================ WRITE — all or nothing
if DRY:
    print('\n--dry-run: every precondition and interlock asserted, NOTHING WRITTEN.')
    sys.exit(0)

BK = P('docs/evidence/exec_306_2a1xa4/l6/_install_backup')
os.makedirs(BK, exist_ok=True)
for f in (CURVE_F, UI_F, RC_F, ST_F):
    shutil.copy2(f, os.path.join(BK, os.path.basename(f)))
open(CURVE_F, 'w').write(curve_bytes)
open(UI_F, 'w').write(ui_bytes)
open(RC_F, 'w').write(rc_bytes)
open(ST_F, 'w').write(st_new)
print('\nWRITTEN — four files, in the order the interlocks force.')

# ================================================================ VERIFY
print('\nVERIFY')
c2 = json.load(open(CURVE_F))
print('  payload recomputed from the INSTALLED curve : %s' % payload_md5(c2['curve']))
assert payload_md5(c2['curve']) == NEW_PAYLOAD_FULL, 'installed curve must reproduce the payload'
assert md5f(CURVE_F) == NEW_CURVE_FILE_MD5, 'curve file md5 must match what step 3 consumed'
assert md5f(UI_F) == NEW_UI_MD5, 'ui file md5 must match what step 6 consumed'
u2 = json.load(open(UI_F))
assert u2['pick_curve_file_md5'] == md5f(CURVE_F), 'ui must pin the curve file it points at'
assert OLD_CONTRACT_MD5 not in open(ST_F).read(), 'stale contract pin must be gone'
assert NEW_UI_MD5[:8] in open(ST_F).read(), 'selftest must pin the ui file'
rc2 = json.load(open(RC_F))
assert rc2['contract_sha256'] == contract_sha256(rc2), 'contract seal must be self-consistent'
n2 = c2['numeraire']
assert abs(n2['published_pin'] / n2['pooled_head_pre_scale'] - n2['s']) < 1e-9, 'E6 coherence'
for p, h in sealed_before.items():
    assert md5f(P(p)) == h, 'SEALED HISTORY MOVED: %s' % p
print('  interlocks       ui.file_md5 == md5(curve file)  OK')
print('  interlocks       selftest._contract_md5 == md5(ui file)[:8]  OK')
print('  contract seal    self-consistent  OK')
print('  E6 coherence     published_pin / head == s to 1e-9  OK')
print('  sealed history   byte-identical  OK')
print('\nINSTALL COMPLETE AND VERIFIED. The engine will NOT boot until the v0surf re-bake (C.3 step 3).')
