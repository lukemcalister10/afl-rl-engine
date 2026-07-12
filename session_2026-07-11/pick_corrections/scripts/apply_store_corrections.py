#!/usr/bin/env python3
"""(c) STORE SOURCE CORRECTIONS — PICK-CORRECTIONS build 2026-07-11.
Edits the ONE source of truth engine/rl_after/rl_model_data.json in place (per SSI: change the source).
Deterministic + web-verified corrections only; unverifiable rows are FLAGGED in a sidecar, never guessed.

Categories:
  (c.1) fill _draft on the 325 None rows from the verified latent `type` (Q3: 186 ND / 136 RD / 3 IRE).
  (c.3) rookie pick ordinals -> official rookie slots, WHERE web-verified (Q5 committed evidence). Rows not
        verified keep their stored ordinal and are recorded 'unverifiable' in the sidecar (egress policy
        blocked per-row web verification this build).
  (c.4) split the web-verified Pre-Season Draft rows out of 'Rookie' -> type='PSD', _draft='Pre-Season Draft'
        (chained after national, before rookie — engine arm added separately in rl_model.py).
  (c.2) 2010-11 national tail renumber: NOT applied — requires authoritative pick-by-pick data that egress
        policy blocks this build. The rows are recorded in the sidecar for a web-enabled follow-up. The (b)
        last-national-pick table already carries the load-bearing 2010 offset fix (77).
"""
import json, os, sys, collections

STORE = 'engine/rl_after/rl_model_data.json'
SIDECAR = 'session_2026-07-11/pick_corrections/out/store_corrections_ledger.json'

# ---- Q5 web-verified set (prior web-enabled session, cited in session_2026-07-11/pick_integrity_audit/Q5) ----
# rookie rows that STAY rookie, corrected to official rookie-draft pick:
ROOKIE_FIX = {   # key -> (old_pick, new_pick)
 'josh-treacy':(5,7),'jack-ginnivan':(9,13),'callum-wilkie':(2,3),'rowan-marshall':(9,10),
 'tom-papley':(11,14),'jack-sinclair':(1,1),'charlie-cameron':(6,7),'jake-lloyd':(18,16),
 'rory-laird':(11,5),'luke-breust':(41,47),'shane-mumford':(50,57),'matt-priddis':(27,31),
 'kieren-jack':(42,58),
}
# rows that were actually PRE-SEASON DRAFT selections folded in as 'Rookie' -> split out to type='PSD':
PSD_FIX = {   # key -> (old_pick, psd_pick)
 'eddie-betts':(1,3),'michael-johnson':(12,8),'dylan-grimes':(1,2),
}

def main():
    d = json.load(open(STORE))
    by_key = {}
    for p in d:
        by_key.setdefault(p.get('key'), []).append(p)

    ledger = {'build':'pick-corrections 2026-07-11','categories':{}}

    # (c.1) fill _draft on the 325 None rows from latent type
    TYPE2DRAFT = {'ND':'National','RD':'Rookie','IRE':'Post-Draft - Ireland'}
    filled = collections.Counter()
    none_rows = [p for p in d if p.get('_draft') is None]
    for p in none_rows:
        t = p['type']
        assert t in TYPE2DRAFT, "unexpected None-row type %s (%s)" % (t, p['player'])
        p['_draft'] = TYPE2DRAFT[t]
        filled[t] += 1
    ledger['categories']['c1_draft_fill'] = {'total':sum(filled.values()),
        'National':filled['ND'],'Rookie':filled['RD'],'Post-Draft - Ireland':filled['IRE']}

    def one(key):
        rows = by_key.get(key, [])
        assert len(rows) == 1, "key %s -> %d rows (expected 1)" % (key, len(rows))
        return rows[0]

    # (c.3) rookie renumber (verified)
    r_changes = []
    for key,(old,new) in ROOKIE_FIX.items():
        p = one(key)
        assert p['type']=='RD', "%s not RD" % key
        assert p.get('pick')==old, "%s stored pick %s != expected %s" % (key,p.get('pick'),old)
        p['pick'] = new
        p['_pick_source'] = 'rookie-draft-official (web-verified Q5)'
        r_changes.append({'key':key,'old':old,'new':new})
    ledger['categories']['c3_rookie_renumber_verified'] = {'n':len(r_changes),'changes':r_changes}

    # (c.4) PSD split (verified)
    psd_changes = []
    for key,(old,psd) in PSD_FIX.items():
        p = one(key)
        assert p['type']=='RD', "%s not RD" % key
        assert p.get('pick')==old, "%s stored pick %s != expected %s" % (key,p.get('pick'),old)
        p['type'] = 'PSD'
        p['_draft'] = 'Pre-Season Draft'
        p['pick'] = psd
        p['_pick_source'] = 'pre-season-draft-official (web-verified Q5)'
        psd_changes.append({'key':key,'old_pick':old,'psd_pick':psd})
    ledger['categories']['c4_psd_split_verified'] = {'n':len(psd_changes),'changes':psd_changes,
        'engine':'chained after national before rookie (rl_model.py PSD arm: _eff = last_national_pick + psd_slot)',
        'note':'rookie-offset-by-per-year-PSD-count refinement DEFERRED: authoritative per-year PSD sizes '
               'are not web-verifiable this build (egress policy blocked). Only web-verified PSD rows moved.'}

    # (c.3 flag) all remaining rookie rows are UNVERIFIABLE this build -> recorded (not mutated), not guessed
    verified_keys = set(ROOKIE_FIX) | set(PSD_FIX)
    rookie_all = [p for p in d if p['type']=='RD']
    unver = [{'key':p.get('key'),'player':p['player'],'year':p['year'],'pick':p.get('pick')}
             for p in rookie_all if p.get('key') not in verified_keys]
    ledger['categories']['c3_rookie_unverifiable'] = {'n':len(unver),
        'reason':'per-row official rookie pick not web-verifiable this build (org egress policy blocks '
                 'wikipedia/draftguru/footywire — 403 CONNECT). Rows keep their stored ordinal; a web-enabled '
                 'session should complete these (near-$0 board impact: chained rookie picks cap at KMAX=70).',
        'rows':unver}

    # (c.2) 2010-11 national tail renumber: BLOCKED -> record the candidate rows for a follow-up
    tail = [{'key':p.get('key'),'player':p['player'],'year':p['year'],'pick':p.get('pick')}
            for p in d if p['type']=='ND' and p['year'] in (2010,2011) and (p.get('pick') or 0) > 66]
    ledger['categories']['c2_national_tail_2010_11'] = {'n':len(tail),'applied':False,
        'reason':'renumber requires authoritative official pick-by-pick data (which rows are real national '
                 'picks 1..N vs folded-in concession/mini-draft entrants). Egress policy blocked that '
                 'verification this build; NOT guessed. The (b) last-national-pick table already fixes the '
                 'load-bearing 2010 chaining offset (93->77). 2011 evidence (pick 89 real) conflicts with the '
                 'Q5 inflation hypothesis and is left for web-enabled reconciliation.',
        'rows':tail}

    json.dump(d, open(STORE,'w'))
    os.makedirs(os.path.dirname(SIDECAR), exist_ok=True)
    json.dump(ledger, open(SIDECAR,'w'), indent=1)

    import hashlib
    md5 = hashlib.md5(open(STORE,'rb').read()).hexdigest()
    print('STORE written. new md5:', md5)
    print('c1 _draft fill:', ledger['categories']['c1_draft_fill'])
    print('c3 rookie renumber (verified):', len(r_changes))
    print('c4 PSD split (verified):', len(psd_changes))
    print('c3 rookie unverifiable (flagged, kept):', len(unver))
    print('c2 2010-11 tail rows (flagged, NOT renumbered):', len(tail))
    print('ledger ->', SIDECAR)

if __name__ == '__main__':
    main()
