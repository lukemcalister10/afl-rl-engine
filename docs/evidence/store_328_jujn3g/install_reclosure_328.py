#!/usr/bin/env python3
"""#328 RE-CLOSURE — INSTALL THE RULED LADDER `df766dff`, as ONE ATOMIC ACT.

Authority: the owner's re-closure ruling of 2026-08-05, OPTION A, filed at
#328 comment 5192164003 — "the ruled curve becomes the corrected-store derived ladder: payload FULL
df766dff94657940e2a892e91da5a6e2. The prior adopted 01f27f02 is superseded by this word; the closure's
reversal condition RE-ANCHORS to the new ladder unchanged in terms."

WHAT THIS IS: `install_closure.py` by the `u8ir65` seat, RE-POINTED. Its structure, its asserts, its
all-or-nothing construction and every discipline it carries are unchanged. Only the pass-specific
constants move, and each is listed here so the diff against the closure install is readable:

    derived curve source   exec_306_u8ir65/l6/pass3_derived_curve4.json
                           ->  store_328_jujn3g/reversal_derived_pooled_numeraire.json
    authorised payload     01f27f0231929b285de83aaa6713048d  ->  df766dff94657940e2a892e91da5a6e2
    installed curve (pre)  3f5875b5                          ->  01f27f02
    sealed-twin token      3014.1435                         ->  3060.621    (the CURRENT head, twinned)
    per_entrant stamp      b6bacff2                          ->  557a53db    (what this act replaces)
    source surface named   b683e2ec                          ->  e4215093

THE ONE DISCIPLINE THAT CHANGES DIRECTION HERE, AND WHY
  Every prior pass held `curve_source_store_md5` (and the selftest's `_curve_source_store`, and
  `stamp.store_md5`) at `81d24704`, on the stated ground that the field records the store the ruled
  curve was DERIVED ON — which remained true while the curve was derived on the rehearsal store.
  **That ground is gone.** This ladder is derived on the corrected store `f1e8c9fe`, so holding the
  field at `81d24704` would make it false. It MOVES here, and the three places that carry it move
  together in this one act, because the selftest binds them to each other:

      ui/release_pick_curve.json  curve_source_store_md5   FULL 32   -> f1e8c9fed354…
      engine/rl_after/pvc_curve_v2.json  stamp.store_md5   8-char    -> f1e8c9fe
      engine/rl_after/one_source_selftest.py  _curve_source_store  FULL 32  -> f1e8c9fed354…

  The FROZEN-RULER check asserts stamp.store_md5 == curve_source_store_md5[:8], so any one of the
  three moving alone is a red.

DISCIPLINES CARRIED, UNCHANGED
  * C.2 field-level: every edit BY JSON PATH, never a wholesale rewrite, never a blind string replace.
  * SEALED TWIN: the live head occurs TWICE in pvc_curve_v2.json — as the numeraire field AND inside
    that same field's own prose. Both move DELIBERATELY and SEPARATELY by path; the occurrence count
    is asserted before and after.
  * N14 / E6: the measured head is PRIMITIVE at the lane's 4dp; `s` is DERIVED = published_pin / head
    at full double precision, and must round to the lane's own 6dp report.
  * N22/N32: identity is the FULL md5; the payload recipe is string-sorted keys, default separators,
    int(round(v)), picks 1..64.
  * THE PIN-LENGTH TRAP (hazard class 1): `_contract_md5` and `_curve_source_store` are FULL 32-char
    pins while `_per_entrant_md5` is an 8-char stamp. Every full pin is read out of the source by
    regex and replaced WHOLE, and the verify demands the literal full form — never a substring.
  * Sealed history byte-asserted UNTOUCHED.
  * The contract seal is recomputed by the contract's OWN writer (release_contract.contract_hash),
    not by a local reimplementation.

USAGE:  python3 install_reclosure_328.py <REPO> [--dry-run]
"""
import hashlib, importlib.util, json, os, re, shutil, sys

REPO = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else os.getcwd()
DRY = '--dry-run' in sys.argv
P = lambda *a: os.path.join(REPO, *a)

AUTHORISED = 'df766dff94657940e2a892e91da5a6e2'   # THE RE-CLOSURE RULING, owner word 2026-08-05
PRE_CURVE = '01f27f02'                            # what must be installed before this act
OLD_HEAD_STR = '3060.621'                         # the CURRENT head — the sealed twin token
OLD_PE = '557a53db'                               # the per_entrant stamp this act replaces
SRC_SURFACE = 'e4215093'                          # the surface this ladder was derived from
NEW_STORE_FULL = 'f1e8c9fed35462536d00add604f69a3f'
OLD_STORE_FULL = '81d2470440a80f72afea4405e94338c5'
NEW_V0SURF_SIG = 'aca37f9f0e24cb266e7236f49d152d5a'
DERIV_REL = 'docs/evidence/store_328_jujn3g/reversal_derived_pooled_numeraire.json'
MATRIX_REL = 'docs/evidence/store_328_jujn3g/per_entrant_328_corrected_store.json'


def md5f(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def payload_md5(curve_dict):
    """N32 recipe: string-sorted keys, default separators, int(round(v)), picks 1..64."""
    pay = {str(k): int(round(curve_dict[str(k)])) for k in range(1, 65)}
    return hashlib.md5(json.dumps(pay, sort_keys=True).encode()).hexdigest()


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- the new curve, from the derivation
dv = json.load(open(P(DERIV_REL)))
LADDER = dv['ladders']['ruled_pooled_numeraire']
assert len(LADDER) == 64, 'ladder must be 64 points'
assert LADDER[0] == 3000, 'ladder must be pinned at 3000'
assert all(LADDER[i] < LADDER[i - 1] for i in range(1, 64)), 'ladder must be strictly descending'
NEW_CURVE = {str(i + 1): int(LADDER[i]) for i in range(64)}
NEW_PAYLOAD_FULL = payload_md5(NEW_CURVE)
NEW_PAYLOAD = NEW_PAYLOAD_FULL[:8]
assert NEW_PAYLOAD_FULL == AUTHORISED, \
    'payload %s != the authorised %s' % (NEW_PAYLOAD_FULL, AUTHORISED)

HEAD = dv['THE_FACTOR_S']['pooled_head_pre_scale']          # primitive, the lane's measured 4dp
S = 3000.0 / HEAD                                            # DERIVED at full precision (N14)
assert round(S, 6) == dv['THE_FACTOR_S']['s'], 'derived s must round to the lane-reported presentation'
POOL_VALUE = dv['levels_under_the_design']['POOL']['LEVEL_under_design_x_s']
NEW_PE_MD5 = md5f(P(MATRIX_REL))[:8]

print('THE NEW CURVE — the owner-ruled corrected-store ladder')
print('  payload FULL   %s   [:8] %s' % (NEW_PAYLOAD_FULL, NEW_PAYLOAD))
print('  head[1..5]     %s   pick64 %d   sum %d' % (LADDER[:5], LADDER[63], sum(LADDER)))
print('  head primitive %r   s derived %r   (6dp presentation %s)' % (HEAD, S, round(S, 6)))
print('  pool_value     %s   per_entrant stamp %s' % (POOL_VALUE, NEW_PE_MD5))
print('  ND-65+ cap law re-evaluates against curve[64] = %d (the ruling records it UNCHANGED at 185)'
      % LADDER[63])

# ---------------------------------------------------------------- sealed history, asserted untouched
SEALED = ['data/release_lineage.json', 'engine/rl_after/finalization_state.json',
          'data/finalization_state.json']
sealed_before = {p: md5f(P(p)) for p in SEALED if os.path.exists(P(p))}
print('\nSEALED HISTORY (asserted untouched): %s' % ', '.join(
    '%s=%s' % (os.path.basename(k), v[:8]) for k, v in sealed_before.items()))

# ================================================================ STEP 1 · pvc_curve_v2.json
CURVE_F = P('engine/rl_after/pvc_curve_v2.json')
raw = open(CURVE_F).read()
n_twin = raw.count(OLD_HEAD_STR)
assert n_twin == 2, 'expected the sealed twin: 2 occurrences of %s, found %d' % (OLD_HEAD_STR, n_twin)
print('\nSTEP 1  pvc_curve_v2.json   (sealed twin present: %d occurrences of %s)' % (n_twin, OLD_HEAD_STR))

c = json.loads(raw)
OLD_POOL_VALUE = c['pool_value']
assert c['curve_md5'] == PRE_CURVE, 'installed curve must be %s, found %s' % (PRE_CURVE, c['curve_md5'])
assert payload_md5(c['curve'])[:8] == PRE_CURVE, 'installed curve must reproduce its own payload'
assert c['stamp']['store_md5'] == OLD_STORE_FULL[:8], 'stamp store %s' % c['stamp']['store_md5']
assert c['stamp']['per_entrant_md5'] == OLD_PE, 'per_entrant stamp %s' % c['stamp']['per_entrant_md5']

c['curve'] = NEW_CURVE                                        # BY PATH
c['curve_md5'] = NEW_PAYLOAD                                  # BY PATH
c['numeraire']['pooled_head_pre_scale'] = HEAD                # BY PATH — sealed twin, occurrence 1
c['numeraire']['s'] = S                                       # BY PATH
c['numeraire']['_doc'] = (                                    # BY PATH — sealed twin, occurrence 2
    '#279 ruled pooled numeraire. THE MEASURED HEAD IS PRIMITIVE (seam ruling 2026-07-31): '
    'pooled_head_pre_scale is the lane-measured value %s exactly, and s is DERIVED from it at full '
    'precision. The 6dp %s seen in presentation is the ROUNDED form of this same s, never the stored '
    'primitive. E6 coherence (published_pin / pooled_head_pre_scale == s to 1e-9) holds BY '
    'CONSTRUCTION. Re-measured at the #328 re-closure on surface %s; the prior value was %s.'
    % (HEAD, round(S, 6), SRC_SURFACE, OLD_HEAD_STR))
c['pool_value'] = POOL_VALUE                                  # BY PATH
c['stamp']['per_entrant_md5'] = NEW_PE_MD5                    # BY PATH
c['stamp']['store_md5'] = NEW_STORE_FULL[:8]                  # BY PATH — the derivation's own store
c['stamp']['per_entrant_path'] = MATRIX_REL                   # BY PATH
c['stamp']['v0surf_sig_at_fit'] = NEW_V0SURF_SIG              # BY PATH
c['derived_from'] = (
    '%s (store %s, surface %s) — #328 re-closure: the matrix emitted on the #323 corrected store and '
    'the surface re-fit on it, committed with its identity block and F-C full-md5 binding. Post-slide '
    'membership and Addendum-6 per-season bars unchanged.'
    % (MATRIX_REL, NEW_STORE_FULL[:8], SRC_SURFACE))
c['_working_substrate_note'] = (
    '#328 RE-CLOSURE (owner word 2026-08-05, OPTION A, seam 5192164003): the corrected-store derived '
    'ladder %s is installed as THE ADOPTED RULED CURVE, superseding %s. The reversal condition '
    'RE-ANCHORS to this ladder, unchanged in terms: any future pass moving any pick by more than 1 '
    'board point re-opens it. Derived from surface %s on store %s at installed curve %s. pool_value '
    'is this derivation\'s own pool-wide level. Adoption remains the owner\'s separate click.'
    % (NEW_PAYLOAD, PRE_CURVE, SRC_SURFACE, NEW_STORE_FULL[:8], PRE_CURVE))

curve_bytes = json.dumps(c, indent=1, sort_keys=True) + '\n'
assert curve_bytes.count(OLD_HEAD_STR) == 1, \
    'after the move the old head must survive ONCE, in the _doc provenance sentence only'
assert curve_bytes.count(str(HEAD)) >= 2, 'the new head must appear as field and in its own prose'
print('        curve_md5 %s -> %s | head %s -> %s | s -> %r' % (PRE_CURVE, NEW_PAYLOAD, OLD_HEAD_STR, HEAD, S))
print('        pool_value %s -> %s | stamp.per_entrant_md5 %s -> %s' % (OLD_POOL_VALUE, POOL_VALUE, OLD_PE, NEW_PE_MD5))
print('        stamp.store_md5 %s -> %s   (MOVES: this ladder is derived on the corrected store)'
      % (OLD_STORE_FULL[:8], NEW_STORE_FULL[:8]))
print('        sealed twin: BOTH occurrences moved deliberately by path')

# ================================================================ STEP 2 · md5 of step 1's bytes
NEW_CURVE_FILE_MD5 = hashlib.md5(curve_bytes.encode()).hexdigest()
print('\nSTEP 2  md5(pvc_curve_v2.json) = %s   <- from step 1 bytes' % NEW_CURVE_FILE_MD5)

# ================================================================ STEP 3 · ui/release_pick_curve.json
UI_F = P('ui/release_pick_curve.json')
u = json.load(open(UI_F))
OLD_UI_KEYS = set(u)
assert u.get('pick_curve_curve_md5') == PRE_CURVE, 'ui curve stamp %s' % u.get('pick_curve_curve_md5')
old_full_store = u.get('curve_source_store_md5')
assert old_full_store == OLD_STORE_FULL, 'ui source store %r' % old_full_store
assert len(NEW_STORE_FULL) == 32, 'E.5 finding 5: curve_source_store_md5 must be the FULL 32 chars'

u['pick_curve_curve_md5'] = NEW_PAYLOAD
u['pick_curve_file_md5'] = NEW_CURVE_FILE_MD5
u['pool_value'] = POOL_VALUE
u['per_entrant_md5'] = NEW_PE_MD5
u['curve_source_store_md5'] = NEW_STORE_FULL                   # MOVES, still FULL 32 (asymmetric convention)
u['_doc'] = ('#328 re-closure working substrate: pick curve payload %s (ladder sum %d, pick64 %d), '
             'file md5 %s, pool_value %s from this derivation, per_entrant %s. curve_source_store_md5 '
             'MOVES to %s and stays the FULL 32 chars by the asymmetric stamp convention (E.5 finding '
             '5) — this ladder is derived on the #323 corrected store, so the field would be false at '
             'the old value. Adoption remains the owner\'s separate click.'
             % (NEW_PAYLOAD, sum(LADDER), LADDER[63], NEW_CURVE_FILE_MD5, POOL_VALUE, NEW_PE_MD5,
                NEW_STORE_FULL[:8]))
ui_bytes = json.dumps(u, indent=1, sort_keys=True) + '\n'
assert set(u) == OLD_UI_KEYS, 'no key added or dropped in the ui stamp'
print('\nSTEP 3  ui/release_pick_curve.json  curve_md5 -> %s | file_md5 -> %s' % (NEW_PAYLOAD, NEW_CURVE_FILE_MD5[:8]))
print('        pool_value -> %s | per_entrant -> %s | curve_source_store %s -> %s (FULL 32)'
      % (POOL_VALUE, NEW_PE_MD5, old_full_store[:8], NEW_STORE_FULL[:8]))

# ================================================================ STEP 4 · md5 of step 3's bytes
NEW_UI_MD5 = hashlib.md5(ui_bytes.encode()).hexdigest()
print('\nSTEP 4  md5(ui/release_pick_curve.json) = %s   <- from step 3 bytes' % NEW_UI_MD5)

# ================================================================ STEP 5 · data/release_contract.json
RCT = _load_module('release_contract_328i', P('release_contract.py'))
RC_F = P('data/release_contract.json')
rc = json.load(open(RC_F))
assert rc['identities']['engine_head'] == '15525b033f390d041a7858f47a30b48e', 'N44 engine pin must hold'
assert rc['identities']['store'] == NEW_STORE_FULL, 'the contract must already name the corrected store'
OLD_SEAL = rc.get('contract_sha256')
assert OLD_SEAL == RCT.contract_hash(rc), 'the seal must be SELF-CONSISTENT before this act'
rc['pvc_provenance']['curve_payload_md5'] = NEW_PAYLOAD
rc['pvc_provenance']['_note'] = ('#328 re-closure (owner word 2026-08-05, OPTION A): the corrected-store '
                                 'derived ladder installed as the adopted ruled curve from surface %s '
                                 'on store %s. Adoption remains the owner\'s separate click.'
                                 % (SRC_SURFACE, NEW_STORE_FULL[:8]))
rc['contract_sha256'] = RCT.contract_hash(rc)
rc_bytes = json.dumps(rc, indent=1, sort_keys=True) + '\n'
print('\nSTEP 5  release_contract.json  curve_payload_md5 %s -> %s' % (PRE_CURVE, NEW_PAYLOAD))
print('        contract_sha256 %s… -> %s…   (recomputed by the contract\'s OWN writer)'
      % (OLD_SEAL[:8], rc['contract_sha256'][:8]))

# ================================================================ STEP 6 · one_source_selftest.py
ST_F = P('engine/rl_after/one_source_selftest.py')
st = open(ST_F).read()
m = re.search(r"_contract_md5='([0-9a-f]{32})'", st)
assert m, 'could not read the full 32-char _contract_md5 pin'
OLD_CONTRACT_MD5 = m.group(1)
assert OLD_CONTRACT_MD5 == md5f(UI_F), 'the incoming full pin must already equal md5(ui file)'
ms = re.search(r"_curve_source_store='([0-9a-f]{32})'", st)
assert ms and ms.group(1) == OLD_STORE_FULL, 'could not read the full 32-char _curve_source_store pin'
hits_c, hits_p, hits_s = st.count(OLD_CONTRACT_MD5), st.count(OLD_PE), st.count(OLD_STORE_FULL)
print('\nSTEP 6  one_source_selftest.py  occurrences: _contract_md5 %d | per_entrant %d | source_store %d'
      % (hits_c, hits_p, hits_s))
assert hits_c >= 1 and hits_p >= 1 and hits_s >= 1, 'expected all three pins'
st_new = (st.replace(OLD_CONTRACT_MD5, NEW_UI_MD5)          # FULL md5, not the prefix
            .replace(OLD_STORE_FULL, NEW_STORE_FULL)        # FULL md5, not the prefix
            .replace(OLD_PE, NEW_PE_MD5))                   # the 8-char stamp
assert st_new.count(NEW_UI_MD5) == hits_c, 'contract replacement count mismatch'
assert st_new.count(NEW_STORE_FULL) == hits_s, 'source-store replacement count mismatch'
assert st_new.count(NEW_PE_MD5) == hits_p, 'per_entrant replacement count mismatch'
assert re.search(r"_contract_md5='%s'" % NEW_UI_MD5, st_new), 'the contract pin must carry the FULL new md5'
assert re.search(r"_curve_source_store='%s'" % NEW_STORE_FULL, st_new), 'the source-store pin must carry the FULL new md5'
assert re.search(r"_per_entrant_md5='%s'" % NEW_PE_MD5, st_new), 'the per_entrant pin must carry the 8-char stamp'
assert OLD_STORE_FULL not in st_new and OLD_CONTRACT_MD5 not in st_new, 'a stale full pin survived'
assert len(st_new.splitlines()) == len(st.splitlines()), 'line count must not change'
print('        _contract_md5 %s… -> %s (FULL)' % (OLD_CONTRACT_MD5[:8], NEW_UI_MD5))
print('        _curve_source_store %s… -> %s… (FULL, MOVES with the derivation basis)'
      % (OLD_STORE_FULL[:8], NEW_STORE_FULL[:8]))
print('        _per_entrant_md5 %s -> %s (8-char)' % (OLD_PE, NEW_PE_MD5))

# ================================================================ WRITE — all or nothing
if DRY:
    print('\n--dry-run: every precondition and interlock asserted, NOTHING WRITTEN.')
    sys.exit(0)

BK = P('docs/evidence/store_328_jujn3g/_install_backup_reclosure')
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
assert c2['stamp']['store_md5'] == u2['curve_source_store_md5'][:8], \
    'FROZEN-RULER binding: curve stamp store must equal the contract source store prefix'
st2 = open(ST_F).read()
assert ("_contract_md5='%s'" % NEW_UI_MD5) in st2, 'selftest must pin the ui file by FULL md5'
assert ("_curve_source_store='%s'" % NEW_STORE_FULL) in st2, 'selftest must pin the new source store'
rc2 = json.load(open(RC_F))
assert rc2['contract_sha256'] == RCT.contract_hash(rc2), 'contract seal must be self-consistent'
n2 = c2['numeraire']
assert abs(n2['published_pin'] / n2['pooled_head_pre_scale'] - n2['s']) < 1e-9, 'E6 coherence'
for p, h in sealed_before.items():
    assert md5f(P(p)) == h, 'SEALED HISTORY MOVED: %s' % p
print('  interlocks       ui.file_md5 == md5(curve file)  OK')
print('  interlocks       selftest._contract_md5 == md5(ui file), FULL 32  OK')
print('  interlocks       curve stamp store == ui curve_source_store[:8]  OK')
print('  contract seal    self-consistent (own writer)  OK')
print('  E6 coherence     published_pin / head == s to 1e-9  OK')
print('  sealed history   byte-identical  OK')
print('\nINSTALL COMPLETE AND VERIFIED. The engine will NOT boot until the v0surf re-bake.')
