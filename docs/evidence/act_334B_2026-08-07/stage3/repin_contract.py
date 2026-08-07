"""Stage 3 PIN COHERENCE — re-derive ui/release_pick_curve.json and the curve artifact's stamp.

Both moves are DERIVED, never typed: every identity written here is measured from the artifact that
carries it, at the moment it is written.
"""
import os, json, hashlib

REPO = '/home/claude/seamcheck_landing'
HERE = os.path.dirname(os.path.abspath(__file__))
CURVE = os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')
CONTRACT = os.path.join(REPO, 'ui/release_pick_curve.json')
MATRIX = os.path.join(HERE, 'per_entrant_338_stage3.json')

STORE32 = json.load(open(os.path.join(REPO, 'data/expected_boot.json')))['store']
PER_ENTRANT32 = hashlib.md5(open(MATRIX, 'rb').read()).hexdigest()

# ---------- 1. the curve artifact's own stamp -------------------------------------------------
v2 = json.load(open(CURVE))
st = v2['stamp']
prev = dict(st)
st['item'] = '334B-stage3'
st['store_md5'] = STORE32[:8]
st['per_entrant_md5'] = PER_ENTRANT32[:8]
st['per_entrant_path'] = ('docs/evidence/act_334B_2026-08-07/stage3/per_entrant_338_stage3.json')
st['prev_curve_md5'] = 'df766dff'
st['v0surf_sig_at_fit'] = json.load(open(MATRIX))['meta']['v0surf_sig']
st['ladder_total'] = int(sum(int(v2['curve'][str(k)]) for k in range(1, 65)))
st['nd_curve_rows'] = 1197
st['statistic'] = 'VOR'
st['_superseded_stamp'] = {k: prev[k] for k in sorted(prev)}
st['_note'] = (
 'RE-STAMPED at #334 stage B stage 3. The superseded item-271 stage-B stamp is carried verbatim in '
 '_superseded_stamp rather than deleted. ladder_total is the 1-64 national curve sum on THIS ladder '
 '(the item-271 figure 65925 was the pre-split 1-99 sum and is not comparable). nd_curve_rows is the '
 "harness loader's ND teaching population (EXPECT_N=1197), which is the population this ladder was "
 'taught on; the item-271 figure 1325 counted its own derivation\'s rows. pool_rows / '
 'pool_never_established / prev_pool_value / windows are derive_271-specific quantities that this '
 "stage's machinery does not re-measure, so they are left in _superseded_stamp and NOT re-asserted here.")
for k in ('pool_rows', 'pool_never_established', 'prev_pool_value', 'windows'):
    st.pop(k, None)
with open(CURVE, 'w') as fh:
    json.dump(v2, fh, indent=1, sort_keys=True); fh.write('\n')

CURVE_FILE_MD5 = hashlib.md5(open(CURVE, 'rb').read()).hexdigest()
CURVE_PAYLOAD8 = v2['curve_md5']
print('curve file md5   %s' % CURVE_FILE_MD5)
print('curve payload    %s' % CURVE_PAYLOAD8)
print('per_entrant md5  %s' % PER_ENTRANT32)

# ---------- 2. the UI provenance contract ------------------------------------------------------
c = json.load(open(CONTRACT))
old = {k: c[k] for k in ('curve_source_store_md5', 'per_entrant_md5', 'pick_curve_curve_md5',
                         'pick_curve_file_md5', 'pick_curve_path')}
old['pathway'] = c['adopted_pathway']
old['note'] = ('Superseded by the #334 stage B stage-3 re-anchor: the base curve was re-taught era-free on '
               'the era-free #338 matrix and the stage-2 per-pick re-anchor f(p) applied, then the whole '
               'result re-based to the numeraire anchor by g = f(1) = 1.121405224905. This entry is the '
               '#328 re-closure ladder df766dff on store f1e8c9fe. Prior chain retained in git history and '
               "in this entry's own supersedes chain below.")
old['supersedes'] = c['supersedes']

c['supersedes'] = old
c['curve_source_store_md5'] = STORE32
c['per_entrant_md5'] = PER_ENTRANT32[:8]
c['pick_curve_curve_md5'] = CURVE_PAYLOAD8
c['pick_curve_file_md5'] = CURVE_FILE_MD5
c['pool_levels'] = v2['pool_levels']          # mirrored verbatim, as the file's own note requires
c['pool_value'] = v2['pool_value']
c['numeraire_pin1'] = int(v2['pin'])
c['_doc'] = (
 '#334 stage B STAGE 3 working substrate: pick curve payload %s (ladder sum %d, pick1 %d, pick64 %d), file '
 'md5 %s, pool_value %s (UNCHANGED — owner data), per_entrant %s. curve_source_store_md5 MOVES to %s and '
 'stays the FULL 32 chars by the asymmetric stamp convention (E.5 finding 5) — this ladder is derived on the '
 'current gate store, so the field would be false at the old value. The ladder is base_erafree(p) * f(p) / g '
 'with g = f(1) = 1.121405224905; the SAME g re-bases the artifact\'s numeraire block (pooled head x g, '
 's / g), which is the E6 two-sided law. numeraire_pin1 is UNMOVED at 3000. Adoption remains the owner\'s '
 'separate click, and the #328 reversal condition (any pass moving any pick by more than one board point) is '
 'tripped by construction, so it re-opens.'
 % (CURVE_PAYLOAD8, sum(int(v2['curve'][str(k)]) for k in range(1, 65)), int(v2['curve']['1']),
    int(v2['curve']['64']), CURVE_FILE_MD5, v2['pool_value'], PER_ENTRANT32[:8], STORE32[:8]))
with open(CONTRACT, 'w') as fh:
    json.dump(c, fh, indent=1, sort_keys=True); fh.write('\n')
CONTRACT_MD5 = hashlib.md5(open(CONTRACT, 'rb').read()).hexdigest()
print('contract md5     %s' % CONTRACT_MD5)
print()
print('SELFTEST PINS TO RE-POINT:')
print("  _contract_md5        -> '%s'" % CONTRACT_MD5)
print("  _curve_source_store  -> '%s'" % STORE32)
print("  _per_entrant_md5     -> '%s'" % PER_ENTRANT32[:8])
json.dump({'contract_md5': CONTRACT_MD5, 'curve_file_md5': CURVE_FILE_MD5,
           'curve_payload8': CURVE_PAYLOAD8, 'store32': STORE32,
           'per_entrant32': PER_ENTRANT32, 'old_contract': old},
          open(os.path.join(HERE, 'pins.json'), 'w'), indent=1, sort_keys=True)
