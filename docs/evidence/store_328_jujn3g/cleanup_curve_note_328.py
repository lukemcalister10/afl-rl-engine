#!/usr/bin/env python3
"""#328 STEP 7 — the shipped curve artifact's SCAR-era self-description, corrected.

#323 Addendum 2 item 5 (owner-ratified, "we've found something that needs fixing") names three
behaviour-neutral SCAR-era text fossils. This instrument does the one of the three that can be done
without moving a value or an identity this act does not already own: the shipped curve artifact's
"SCAR-denominated BY CONSTRUCTION" self-description.

WHY IT NEEDS AN INSTRUMENT AND NOT AN EDIT. `pvc_curve_v2.json` is identity-pinned three deep:

    md5(pvc_curve_v2.json)  ->  ui/release_pick_curve.json  pick_curve_file_md5
                            ->  one_source_selftest.py      _contract_md5 (md5 of the ui file)
                            ->  data/release_contract.json  contract_sha256

  So a one-character change to a comment field breaks four FROZEN-RULER checks unless the whole chain
  moves with it, in one act. That is what this does — the same chain, in the same order, with the same
  interlocks as the re-closure install.

WHY IT IS STILL TEXT-ONLY IN THE SENSE STEP 7 MEANS. The engine reads exactly two fields out of this
artifact — `curve` and `pool_value` (`_merged_recover.py:1840-1842`). `note` is inert to valuation.
The proof is not the reading, though: the board is REBUILT after this runs and asserted BYTE-IDENTICAL.

  python3 cleanup_curve_note_328.py <REPO> [--dry-run]
"""
import hashlib, importlib.util, json, os, re, sys

REPO = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else os.getcwd()
DRY = '--dry-run' in sys.argv
P = lambda *a: os.path.join(REPO, *a)

NEW_NOTE = (
    'ITEM 271 stage B, as amended by the #328 re-closure. pool_value is the RULED pool level, from '
    'realised outcomes with never-established entrants at 0.0 — never from a pedigree/V0 mean. The pool '
    'sits BELOW the last national band by the lawful same-instrument comparison. '
    'DENOMINATION (corrected 2026-08-05 per #323 Addendum 2 item 5, owner-ratified): this artifact was '
    'previously self-described as "SCAR-denominated BY CONSTRUCTION", from build_pvc_v34\'s step 5 '
    'anchoring the pooled top band to the legacy realised value. That is ERA PROVENANCE, not a live '
    'property: the engine executes gamma = 1.0 VOR everywhere (rl_model.py:504 defaults RL_GAMMA to '
    '1.0), and the note itself always recorded that this artifact is identical in the SCAR and the '
    'gamma=1.0 VOR columns. It is a fixed input file; a natively-VOR curve remains a referee-era '
    'question. ERA FIGURES, kept as the evidence they were measured as and NOT re-measured here: the '
    'stage-B comparison read ND 55-64 realised 361.2 vs pool 299.3, on that era\'s store, curve and '
    'pool level. Today\'s pool_value is carried in this artifact\'s own field.')


def md5f(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    CURVE_F, UI_F = P('engine/rl_after/pvc_curve_v2.json'), P('ui/release_pick_curve.json')
    RC_F, ST_F = P('data/release_contract.json'), P('engine/rl_after/one_source_selftest.py')

    c = json.load(open(CURVE_F))
    old_note = c['note']
    assert 'SCAR-denominated BY CONSTRUCTION' in old_note, 'the fossil this act targets is not present'
    before = {'curve': dict(c['curve']), 'pool_value': c['pool_value'], 'curve_md5': c['curve_md5'],
              'numeraire': dict(c['numeraire'])}

    c['note'] = NEW_NOTE                                       # BY PATH — the only field touched
    curve_bytes = json.dumps(c, indent=1, sort_keys=True) + '\n'
    c2 = json.loads(curve_bytes)
    after = {'curve': dict(c2['curve']), 'pool_value': c2['pool_value'], 'curve_md5': c2['curve_md5'],
             'numeraire': dict(c2['numeraire'])}
    assert before == after, 'a VALUE-BEARING field moved — this act is text-only and HALTs'
    print('the two fields the engine actually reads are UNCHANGED:')
    print('  curve      64 entries, payload %s (unmoved)' % c2['curve_md5'])
    print('  pool_value %s (unmoved)' % c2['pool_value'])

    NEW_CURVE_MD5 = hashlib.md5(curve_bytes.encode()).hexdigest()
    print('\n  md5(pvc_curve_v2.json)  %s -> %s' % (md5f(CURVE_F), NEW_CURVE_MD5))

    u = json.load(open(UI_F))
    assert u['pick_curve_file_md5'] == md5f(CURVE_F), 'the ui pin must be current before this act'
    u['pick_curve_file_md5'] = NEW_CURVE_MD5
    ui_bytes = json.dumps(u, indent=1, sort_keys=True) + '\n'
    NEW_UI_MD5 = hashlib.md5(ui_bytes.encode()).hexdigest()
    print('  md5(ui/release_pick_curve.json)  %s -> %s' % (md5f(UI_F), NEW_UI_MD5))

    st = open(ST_F).read()
    m = re.search(r"_contract_md5='([0-9a-f]{32})'", st)
    assert m and m.group(1) == md5f(UI_F), 'the selftest pin must be current before this act'
    st_new = st.replace(m.group(1), NEW_UI_MD5)
    assert st_new.count(NEW_UI_MD5) == st.count(m.group(1)), 'replacement count mismatch'
    assert len(st_new.splitlines()) == len(st.splitlines()), 'line count must not change'
    print('  selftest _contract_md5  %s -> %s (FULL 32)' % (m.group(1)[:8], NEW_UI_MD5[:8]))

    RCT = _load('release_contract_328c', P('release_contract.py'))
    rc = json.load(open(RC_F))
    old_seal = rc['contract_sha256']
    assert old_seal == RCT.contract_hash(rc), 'the seal must be self-consistent before this act'
    # nothing in the contract names the curve FILE md5; the seal is re-verified, not moved.
    print('  contract_sha256 %s… — self-consistent, and this act moves no contract field' % old_seal[:8])

    if DRY:
        print('\n--dry-run: nothing written.')
        return
    open(CURVE_F, 'w').write(curve_bytes)
    open(UI_F, 'w').write(ui_bytes)
    open(ST_F, 'w').write(st_new)
    assert md5f(CURVE_F) == NEW_CURVE_MD5 and md5f(UI_F) == NEW_UI_MD5
    assert json.load(open(UI_F))['pick_curve_file_md5'] == md5f(CURVE_F)
    assert ("_contract_md5='%s'" % NEW_UI_MD5) in open(ST_F).read()
    rc2 = json.load(open(RC_F))
    assert rc2['contract_sha256'] == RCT.contract_hash(rc2), 'contract seal must still verify'
    print('\nWRITTEN and re-asserted — the fossil is gone and the identity chain is consistent.')
    print('The board MUST now rebuild byte-identically; that is the proof this was text-only.')


if __name__ == '__main__':
    main()
