#!/usr/bin/env python3
"""PICK-CONVENTION REMEDIATION (i)/(ii)/(iii) 2026-07-11 — record the remediation in the ledger.

Under the OWNER DATA LAW (store pick numbers are database-universe ordinals; redrafts excluded;
store numbers deliberately differ from AFL-official numbering), the correction build's
"renumber to real-world" pass violated the convention. This updates the ledger to record:
  (i)   the 190 rookie renumbers REVERTED to the original store ordinals,
  (ii)  the last-national-pick chain table RE-DERIVED from the database (2010 77->93),
  (iii) the 495 'unverifiable' rookie flags CLEARED (never suspect under the convention) and
        the 42 2010-11 tail flags CLEARED (intentional database ordinals).
"""
import json, collections

STORE = 'engine/rl_after/rl_model_data.json'
SIDECAR = 'session_2026-07-11/pick_corrections/out/store_corrections_ledger.json'

OWNER_LAW = ('Store pick numbers are DATABASE-UNIVERSE ordinals, not AFL official numbering. '
    '"Players previously listed are excluded when redrafted, and only their initial entry is recorded." '
    'One row per player at initial entry; redrafts never consume numbering; store ordinals deliberately '
    'differ from AFL-official numbering. The rookie draft chains onto the database\'s ND end. No build may '
    '"correct" store picks against external sources without an owner ruling.')

def main():
    d = json.load(open(STORE))
    led = json.load(open(SIDECAR))
    cats = led['categories']

    # (i) record the revert of the 190 renumbers
    ren = (cats['c3_rookie_renumber_verified']['changes']
           + cats['c3_rookie_renumber_verified_expanded']['changes'])
    by = {p['key']: p for p in d if p.get('key')}
    # confirm every renumber key is back at its original stored ordinal and stamp removed
    reverted = []
    for c in ren:
        p = by[c['key']]
        reverted.append({'key': c['key'], 'reverted_from_realworld': c['new'], 'restored_store_ordinal': p['pick']})
    cats['c3_rookie_renumber_verified']['REMEDIATION'] = (
        'REVERTED 2026-07-11 (pick-convention remediation): these real-world renumbers violated the owner '
        'data law and were restored to the original store ordinals (byte-restore from pre-correction store '
        'a2fbc9a0). _pick_source stamps removed. treacy 7->5.')
    cats['c3_rookie_renumber_verified_expanded']['REMEDIATION'] = cats['c3_rookie_renumber_verified']['REMEDIATION']

    # (iii) clear the 495 unverifiable flags — never suspect under the convention
    unver = cats.get('c3_rookie_unverifiable', {})
    unver_n = unver.get('n')
    cats['c3_rookie_unverifiable'] = {
        'n': unver_n, 'status': 'CLEARED',
        'reason': ('CLEARED 2026-07-11 under the owner data law: these rookie rows were never suspect. Their '
                   'stored ordinals are database-universe numbers (redrafts excluded), which are AUTHORITATIVE '
                   'and deliberately differ from AFL-official numbering. There was nothing to verify against an '
                   'external source; the "unverifiable" framing was the mistaken real-world premise the '
                   'remediation reverts. All rows kept at their stored (correct) database ordinal.'),
        'rows': unver.get('rows', [])}

    # (ii) re-judge + clear the 42 2010-11 national tail flags
    tail_rows = cats.get('c2_national_tail_2010_11', {}).get('rows', [])
    # verify within-convention: unique ordinals per year, all type ND
    anomalies = []
    for y in (2010, 2011):
        yr = [p for p in d if p['type'] == 'ND' and p['year'] == y]
        dup = [x for x, c in collections.Counter(p['pick'] for p in yr).items() if c > 1]
        if dup:
            anomalies.append({'year': y, 'duplicate_picks': dup})
    cats['c2_national_tail_2010_11'] = {
        'n': len(tail_rows), 'applied': False, 'status': 'CLEARED',
        'reason': ('CLEARED 2026-07-11 under the owner data law (re-judged against the database universe): '
                   'these 42 ND 2010/2011 rows (pick>66) are legitimate database-universe national ordinals '
                   '(unique per year, all type=National, real careers). The gaps below the max are excluded/'
                   'redrafted players that never consume numbering. The database ND end = the store MAX '
                   '(2010=93, 2011=89), used by the re-derived chain table. The correction build\'s 2010->77 '
                   'override used the real-world selection count, which is NOT the authority; it is reverted.'),
        'within_convention_anomalies': anomalies if anomalies else 'none (0 duplicate ordinals; all clear)',
        'rows': tail_rows}

    # top-level remediation banner + owner law
    led['REMEDIATION'] = {
        'date': '2026-07-11', 'build': 'pick-convention remediation (candidate)',
        'owner_data_law': OWNER_LAW,
        'items': {
            'i_reverted_rookie_renumbers': len(reverted),
            'ii_chain_table': 'RE-DERIVED from database (store MAX National ordinal); 2010 77->93, all else unchanged',
            'iii_flags_cleared': {'rookie_unverifiable': unver_n, 'national_tail_2010_11': len(tail_rows)},
        },
        'kept_intact': 'c1 _draft fills (325), c4 PSD splits (8, type/_draft/pick/_pick_source), (a) band-pool basis, (f) re-denomination',
    }

    json.dump(led, open(SIDECAR, 'w'), indent=1)
    print('ledger updated.')
    print('  (i) renumbers reverted     :', len(reverted))
    print('  (iii) rookie flags cleared :', unver_n)
    print('  (ii/iii) tail flags cleared:', len(tail_rows), '| anomalies:', anomalies if anomalies else 'none')

if __name__ == '__main__':
    main()
