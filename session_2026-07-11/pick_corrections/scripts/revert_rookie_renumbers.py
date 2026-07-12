#!/usr/bin/env python3
"""PICK-CONVENTION REMEDIATION (i) 2026-07-11 — REVERT the 190 rookie renumbers.

Owner data law (stated 2026-07-11): store pick numbers are DATABASE-UNIVERSE ordinals.
"Players previously listed are excluded when redrafted, and only their initial entry is
recorded." Redrafts never consume numbering; store ordinals deliberately differ from AFL
official numbering. The correction build's 190 rookie renumbers to real-world numbers
therefore VIOLATED the convention and must be reverted.

This byte-restores the `pick` field of the 190 renumbered RD rows to the pre-correction
store value (main / a2fbc9a0) — revert, NOT re-derive — and removes the `_pick_source`
stamp the renumber added. Treacy returns to 5.

KEPT INTACT (all other (c) work):
  - the 325 _draft fills (c1),
  - the 8 PSD splits (c4: type=PSD, _draft, pick, _pick_source),
  - every other store field.

The revert set is read from the ledger (c3_rookie_renumber_verified +
c3_rookie_renumber_verified_expanded) and every restore is asserted against the
pre-correction store, so a wrong-row edit halts.
"""
import json, subprocess, hashlib, os

STORE   = 'engine/rl_after/rl_model_data.json'
SIDECAR = 'session_2026-07-11/pick_corrections/out/store_corrections_ledger.json'
MAIN_REF = 'main'  # pre-correction store (a2fbc9a0)

def main():
    d = json.load(open(STORE))
    by = {p['key']: p for p in d if p.get('key')}

    # pre-correction store (byte source for the restore)
    main_raw = subprocess.check_output(['git', 'show', '%s:%s' % (MAIN_REF, STORE)])
    main_by = {p['key']: p for p in json.loads(main_raw) if p.get('key')}
    assert hashlib.md5(main_raw).hexdigest().startswith('a2fbc9a0'), \
        'main store is not the pinned pre-correction a2fbc9a0'

    led = json.load(open(SIDECAR))['categories']
    renumber = (led['c3_rookie_renumber_verified']['changes']
                + led['c3_rookie_renumber_verified_expanded']['changes'])
    assert len(renumber) == 190, 'expected 190 renumber rows, got %d' % len(renumber)

    reverted = []
    pick_restored = 0
    src_dropped = 0
    for c in renumber:
        k = c['key']
        p = by[k]
        m = main_by[k]
        # guardrails: this is a renumber row (current state = the correction), restore to pre-correction pick
        assert p['type'] == 'RD', '%s not RD (is %s) — refusing (PSD/other must not be touched)' % (k, p['type'])
        assert p.get('pick') == c['new'], '%s current pick %s != ledger new %s' % (k, p.get('pick'), c['new'])
        assert m.get('pick') == c['old'], '%s main pick %s != ledger old %s' % (k, m.get('pick'), c['old'])
        # (1) byte-restore pick from pre-correction store
        if p.get('pick') != m.get('pick'):
            p['pick'] = m['pick']
            pick_restored += 1
        # (2) drop the renumber's provenance stamp (main had none on these rows)
        assert m.get('_pick_source') is None, '%s unexpectedly had _pick_source in main' % k
        if '_pick_source' in p:
            del p['_pick_source']
            src_dropped += 1
        reverted.append({'key': k, 'from': c['new'], 'to': m['pick']})

    json.dump(d, open(STORE, 'w'))

    md5 = hashlib.md5(open(STORE, 'rb').read()).hexdigest()
    print('REVERT (i) done.')
    print('  rows reverted           :', len(reverted), '(expected 190)')
    print('  pick fields restored    :', pick_restored, '(189 changed + jack-sinclair 1->1 no-op)')
    print('  _pick_source stamps drop :', src_dropped)
    print('  treacy pick now          :', by['josh-treacy']['pick'])
    print('  new store md5            :', md5)
    # sanity: PSD rows still carry their split + stamp
    psd = (led['c4_psd_split_verified']['changes'] + led['c4_psd_split_verified_expanded']['changes'])
    for c in psd:
        pp = by[c['key']]
        assert pp['type'] == 'PSD' and pp.get('_pick_source') and pp['pick'] == c['psd_pick'], \
            'PSD row %s disturbed!' % c['key']
    print('  PSD splits intact        :', len(psd), '(all type=PSD, stamp + pick preserved)')

if __name__ == '__main__':
    main()
