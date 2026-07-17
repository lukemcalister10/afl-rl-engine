#!/usr/bin/env python3
"""LEG C RELAY — flex re-ingest (validate-or-halt). Stable-ID resolution ONLY over the 804-scope
(name-matching over the 2,652-row store is FORBIDDEN as an identity instrument — item 269 standing rule).
Sources (fetched from main, NEVER merged): the corrected AFFL_Future_Positioning.csv (Driscoll 100% MID)
+ AFFL_Player_Locations.csv (Position/s = current-season eligibilities).

Dry-run (default): compute + validate the 11 primary-future + 4-write rider + 90 blend, HALT on any count
mismatch, write nothing. --write : apply to the store (JOB 3, post-PROCEED only).
"""
import json, csv, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.environ.get('RL_STORE', os.path.join(HERE, '../../engine/rl_after/rl_model_data.json'))
FUT   = os.path.join(HERE, 'inputs/AFFL_Future_Positioning.csv')
LOC   = os.path.join(HERE, 'inputs/AFFL_Player_Locations.csv')

# store position codes are compact (GDEF/GFWD/KDEF/KFWD/MID/RUC). CSV is hyphenated + RUCK.
def norm(tok):
    if tok is None: return None
    t = tok.strip().upper().replace('-', '')
    if t in ('RUCK', 'RUC'): return 'RUC'          # RUCK ≡ RUC (item-269 / v1.1 normalization)
    return t or None

VOCAB = {'GDEF', 'GFWD', 'KDEF', 'KFWD', 'MID', 'RUC'}

ELEVEN = {'Jack Carroll','Zeke Uwland','Archie Roberts','Xavier Lindsay','Harvey Thomas','Tom Powell',
          'Will Graham','Bailey Humphrey','Max Hall','Luke Lloyd','Louis Emmett'}   # item-269 verified list

def load_store():
    return json.load(open(STORE))

def read_future():
    rows = []
    with open(FUT, newline='') as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row or not row[0].strip(): continue
            sid, name, team, pri, alt, pd = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip()
            rows.append(dict(sid=sid, name=name, team=team, pri=pri, alt=alt, pd=pd))
    return rows

def read_locations():
    rows = []
    with open(LOC, newline='') as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row or not row[0].strip(): continue
            rows.append(dict(name=row[0].strip(), team=row[1].strip(), pos=row[2].strip(), club=row[3].strip() if len(row) > 3 else ''))
    return rows

def main(do_write=False):
    store = load_store()
    by_sid = {p.get('stable_player_id'): p for p in store if p.get('stable_player_id')}
    fut = read_future()
    loc = read_locations()

    # name->ID map from the POSITIONING file (the authoritative 804-scope). Collisions (e.g. two Max Kings)
    # are disambiguated by AFFL team; unresolved collision => HALT.
    name_ids = {}
    for r in fut:
        name_ids.setdefault(r['name'], []).append(r)
    def resolve(name, team):
        cand = name_ids.get(name, [])
        if len(cand) == 1: return cand[0]['sid']
        if not cand: return None
        m = [c for c in cand if c['team'] == team]
        if len(m) == 1: return m[0]['sid']
        raise SystemExit('HALT: ambiguous name->ID for %r team=%r (%d candidates) — item-269 collision rule' % (name, team, len(cand)))

    halts, prim, blend, elig_writes, present_writes = [], [], [], [], []

    # 804-scope check + vocab
    if len(fut) != 804:
        halts.append('future CSV rows = %d (expect 804)' % len(fut))
    for r in fut:
        if r['sid'] not in by_sid:
            halts.append('future sid %s (%s) not in store 804-scope' % (r['sid'], r['name']))
        for tok in (r['pri'], r['alt']):
            if tok and norm(tok) not in VOCAB:
                halts.append('vocab: %s token %r not in vocab' % (r['name'], tok))

    # (1) primary-future writes: CSV primary vs base store future_position (== present in the base)
    for r in fut:
        p = by_sid.get(r['sid'])
        if not p: continue
        npri = norm(r['pri'])
        if npri and p.get('future_position') != npri:
            prim.append((r['name'], p.get('future_position'), npri))

    # (2) blend writes: CSV alternate + p_dual (item-180 trap: alternate present <=> p_dual present, else HALT)
    for r in fut:
        p = by_sid.get(r['sid'])
        if not p: continue
        alt, pd = norm(r['alt']), (r['pd'].replace('%', '').strip() if r['pd'] else '')
        if bool(alt) != bool(pd):
            halts.append('blend trap: %s alternate=%r p_dual=%r (must both be set or both blank)' % (r['name'], r['alt'], r['pd']))
            continue
        if alt and pd:
            q = float(pd)
            if not (0.0 < q <= 100.0): halts.append('blend: %s p_dual %s out of (0,100]' % (r['name'], pd))
            if alt == norm(r['pri']): halts.append('blend: %s alternate == primary (%s)' % (r['name'], alt))
            blend.append((r['name'], norm(r['pri']), alt, q))

    # (3) eligibilities rider: §1b requires AT MOST TWO. The base store carries eligibilities for all 804;
    # exactly the OVER-POPULATED entries (>2 positions) are corrected to the corrected Locations 2-position
    # value (name->ID). The K+matching-G "diffs" elsewhere collapse to single under R105.1, so they are NOT
    # §1b-relevant and are left as the store carries them (out of this build's scope — item-270 4-write rider).
    loc_by_sid = {}
    for lr in loc:
        sid = resolve(lr['name'], lr['team'])
        if sid: loc_by_sid[sid] = lr['pos']
    for sid, p in by_sid.items():
        cur = p.get('eligibilities')
        if cur and len([x for x in cur.split(',') if x.strip()]) > 2:
            newv = loc_by_sid.get(sid)
            if newv is None:
                halts.append('over-populated eligibilities %r (%s) has no Locations correction' % (cur, p.get('player')))
            elif len([x for x in newv.split(',') if x.strip()]) > 2:
                halts.append('Locations value %r for %s still >2 positions' % (newv, p.get('player')))
            else:
                elig_writes.append((p.get('player'), cur, newv))

    # (4) present rider: the enumerated owner/register correction (item 270): Sam Flanders present MID->GDEF
    for r in fut:
        if r['name'] == 'Sam Flanders':
            p = by_sid.get(r['sid'])
            if p and p.get('present_position') != 'GDEF':
                present_writes.append((r['name'], p.get('present_position'), 'GDEF'))

    # ---- validate-or-halt ----
    print('=== RE-INGEST DRY-RUN (validate-or-halt) ===')
    print('primary-future writes: %d (expect 11)' % len(prim))
    for nm, a, b in sorted(prim): print('   %-18s %s -> %s' % (nm, a, b))
    if set(nm for nm, _, _ in prim) != ELEVEN:
        halts.append('primary-future set != the item-269 ELEVEN (got %s)' % sorted(nm for nm, _, _ in prim))
    print('blend rows: %d (expect 90)' % len(blend))
    print('eligibilities rider: %d (expect 3)' % len(elig_writes))
    for nm, a, b in elig_writes: print('   %-18s %r -> %r' % (nm, a, b))
    print('present rider: %d (expect 1)' % len(present_writes))
    for nm, a, b in present_writes: print('   %-18s %s -> %s' % (nm, a, b))
    print('rider total: %d (expect 4)' % (len(elig_writes) + len(present_writes)))

    if len(prim) != 11: halts.append('primary-future count %d != 11' % len(prim))
    if len(blend) != 90: halts.append('blend count %d != 90' % len(blend))
    if len(elig_writes) + len(present_writes) != 4: halts.append('rider count %d != 4' % (len(elig_writes) + len(present_writes)))

    if halts:
        print('\n*** HALT — %d finding(s):' % len(halts))
        for h in halts: print('   -', h)
        sys.exit(1)
    print('\nVALIDATED: 11 primary-future + 90 blend + 4-write rider. Driscoll = 100% MID (blend dropped 91->90).')

    if do_write:
        for r in fut:
            p = by_sid.get(r['sid']);  npri = norm(r['pri'])
            if p and npri: p['future_position'] = npri
            alt, pd = norm(r['alt']), (r['pd'].replace('%', '').strip() if r['pd'] else '')
            if p:
                p['alternate_position'] = alt if (alt and pd) else None
                p['p_dual_stream'] = float(pd) if (alt and pd) else None
        for nm, _, nb in elig_writes:
            sid = next(sid for sid, p in by_sid.items() if p.get('player') == nm and p.get('eligibilities') and len(p['eligibilities'].split(',')) > 2)
            by_sid[sid]['eligibilities'] = nb
        for nm, _, nb in present_writes:
            r = next(x for x in fut if x['name'] == nm); by_sid[r['sid']]['present_position'] = nb
        json.dump(store, open(STORE, 'w'), sort_keys=True, indent=0)
        print('WROTE store %s' % STORE)

if __name__ == '__main__':
    main(do_write=('--write' in sys.argv))
