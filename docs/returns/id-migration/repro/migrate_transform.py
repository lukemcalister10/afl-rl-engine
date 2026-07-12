"""ID-primary migration — the canonical store transform.
Applied to engine/rl_after/rl_model_data.json (the ONE source). Pure data.
Returns (new_store_list, changelog) — changelog rows describe every field write.
Import scope (owner-ruled, register v8 item 10 / directive v1a):
  - stable_player_id on every csv-matched row (identity; not read by ev)
  - affl_team, eligibilities as NEW identity fields (current-season DPP; NOT positional judgment)
  - _by / _bd from csv where authoritative
  - named-row entry switches (re-entry trio), nankervis no-import, taylor-adams retire
Historical/unmatched store rows: UNCHANGED (no synthetic ids).
"""
import json, csv

# RE-ENTRY TRIO — §45 later-entry exception. DEFERRED to the v2.9 lever build (owner-ruled 2026-07-12;
# register v11 item 11a, alongside the now-ruled MSD calibration-pool exclusion). Reason: applying it here
# reprices 657 non-named players via the load-time calibration refit (mcandrew alone = 653), for ~zero
# intended movement (perez 14->14). The ruling STANDS; its execution rides v2.9 where a board-wide move is
# in scope. This build applies APPLY_REENTRY=False -> the trio keep their current (initial) entry; they DO
# receive the identity + DOB import like every other matched row.
APPLY_REENTRY = False
RE_ENTRY = {
    'flynn-perez':     {'year': 2025, 'type': 'SSP', '_draft': 'SSP', '_pickless': True, 'pick': None},
    'lachlan-mcandrew':{'year': 2024, 'type': 'SSP', '_draft': 'SSP', '_pickless': True, 'pick': None},
    'mark-keane':      {'year': 2022, 'type': 'SSP', '_draft': 'SSP', '_pickless': True, 'pick': None},
}
NO_IMPORT_ENTRY = {'luke-nankervis'}     # store PSD pick 2 STANDS; csv RD-1 does not import
RETIRE = {'taylor-adams'}                # owner: retired mid-season; not in csv, no id

def load_csv(path):
    rows = {}
    for r in csv.DictReader(open(path)):
        r['_ev'] = json.loads(r['identity_evidence_json'])
        rows[r['legacy_key']] = r
    return rows

def migrate(store, csv_rows):
    changelog = []   # (key, field, old, new, cause)
    by_key = {}
    for r in store:
        by_key.setdefault(r['key'], []).append(r)

    def setf(r, field, val, cause):
        old = r.get(field, '<absent>')
        if old != val:
            changelog.append((r['key'], field, old, val, cause))
            r[field] = val

    for key, c in csv_rows.items():
        rs = by_key.get(key)
        if not rs:
            continue  # 100% coverage expected; skip if not
        r = rs[0]
        ev = c['_ev']
        # 1. identity — stable_player_id (not read by valuation)
        setf(r, 'stable_player_id', c['stable_player_id'], 'id-attach')
        # 2. new identity fields — current club + current-season DPP eligibilities (valuation ignores)
        setf(r, 'affl_team', c['affl_team'], 'identity-field')
        setf(r, 'eligibilities', c['eligibilities'], 'identity-field')
        # 3. DOB import where authoritative (age keys off _by only; _bd is display)
        cby = ev.get('birth_year')
        if cby is not None:
            setf(r, '_by', cby, 'dob-age')
        cbd = ev.get('birth_date')
        if cbd:  # skip empty-string csv dates (perez/keane have none)
            setf(r, '_bd', cbd, 'dob-day')
        # 4. entry basis — re-entry trio DEFERRED to v2.9 (APPLY_REENTRY=False); nankervis NO-import by design
        if APPLY_REENTRY and key in RE_ENTRY:
            for f, v in RE_ENTRY[key].items():
                setf(r, f, v, 'entry-switch')

    # 5. taylor-adams retire (not in csv)
    for key in RETIRE:
        for r in by_key.get(key, []):
            setf(r, '_retired', True, 'retirement')

    return store, changelog

if __name__ == '__main__':
    import sys
    store = json.load(open(sys.argv[1]))
    csv_rows = load_csv(sys.argv[2])
    store, cl = migrate(store, csv_rows)
    # SAME serialization as the source store (single-line default json.dump) so untouched rows stay byte-exact
    json.dump(store, open(sys.argv[3], 'w'))
    # summary
    from collections import Counter
    print("changelog rows:", len(cl))
    print("by cause:", dict(Counter(c[4] for c in cl)))
    print("keys touched:", len(set(c[0] for c in cl)))
