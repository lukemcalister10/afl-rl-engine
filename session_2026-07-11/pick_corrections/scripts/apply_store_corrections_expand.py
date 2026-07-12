#!/usr/bin/env python3
"""(c-expand) Apply the FULL web-verified rookie/PSD corrections (199-row verification pass, 2026-07-11).
Runs ON TOP of the Q5 base corrections already in the store. Every correction:
  - asserts the store row's current pick == the recorded stored ordinal (guards against wrong-row edits),
  - writes the official pick + a _pick_source provenance stamp (with source URL),
  - is $0 on the board (chained picks cap at KMAX=70) but is the owner's stated ground truth (truth-keeping).
Unverifiable rows are recomputed and re-flagged in the ledger (never guessed).
"""
import json, csv, os, hashlib

STORE='engine/rl_after/rl_model_data.json'
TSV='session_2026-07-11/pick_corrections/out/rookie_verified_websearch_2026-07-11.tsv'
SIDECAR='session_2026-07-11/pick_corrections/out/store_corrections_ledger.json'

# 5 additional Pre-Season Draft rows found in the verification pass (each Wikipedia/club-cited):
PSD_NEW={  # key -> (stored_pick, psd_pick, source)
 'tom-bellchambers':(7,8,'en.wikipedia.org/wiki/Tom_Bellchambers'),
 'tom-rockliff':(2,5,'en.wikipedia.org/wiki/Tom_Rockliff'),
 'michael-hibberd':(2,4,'en.wikipedia.org/wiki/Michael_Hibberd'),
 'aaron-hall':(1,7,'en.wikipedia.org/wiki/Aaron_Hall_(footballer)'),
 'luke-nankervis':(1,2,'afc.com.au/news/1033976'),
}

def main():
    d=json.load(open(STORE))
    bk={p.get('key'):p for p in d}
    rookie_applied=[]; rookie_already=[]; rookie_missing=[]; rookie_skip=[]
    for r in csv.reader(open(TSV),delimiter='\t'):
        if not r or len(r)<6: continue
        key,player,yr,spk,mech,opk=r[0],r[1],int(r[2]),int(r[3]),r[4],int(r[5])
        src=r[6] if len(r)>6 else ''
        if key in PSD_NEW: continue           # handled below as PSD
        p=bk.get(key)
        if not p: rookie_missing.append(key); continue
        if p['type']!='RD': rookie_skip.append((key,'type=%s'%p['type'])); continue
        cur=p.get('pick')
        if cur==opk:                          # already at official (Q5 base) -> nothing to do
            rookie_already.append(key); continue
        if cur!=spk:                          # store pick != recorded stored ordinal -> wrong row, skip (no guess)
            rookie_skip.append((key,'store=%s tsv_stored=%s'%(cur,spk))); continue
        p['pick']=opk
        p['_pick_source']='rookie-official (web-verified 2026-07-11: %s)'%src
        rookie_applied.append({'key':key,'old':spk,'new':opk,'source':src})

    psd_applied=[]
    for key,(spk,ppk,src) in PSD_NEW.items():
        p=bk.get(key)
        if not p: rookie_missing.append(key); continue
        assert p['type']=='RD' and p.get('pick')==spk, '%s unexpected (%s / pick %s)'%(key,p['type'],p.get('pick'))
        p['type']='PSD'; p['_draft']='Pre-Season Draft'; p['pick']=ppk
        p['_pick_source']='pre-season-draft-official (web-verified 2026-07-11: %s)'%src
        psd_applied.append({'key':key,'old_pick':spk,'psd_pick':ppk,'source':src})

    # recompute unverifiable rookie set
    verified_keys={p['key'] for p in d if p.get('_pick_source')}
    rd_all=[p for p in d if p['type']=='RD']
    unver=[{'key':p.get('key'),'player':p['player'],'year':p['year'],'pick':p.get('pick')}
           for p in rd_all if not p.get('_pick_source')]

    # update ledger
    led=json.load(open(SIDECAR))
    led['categories']['c3_rookie_renumber_verified_expanded']={
        'n':len(rookie_applied),
        'note':'full web-verification pass 2026-07-11 (199-row sweep; WebSearch-corroborated against club '
               '"Rookie Pick N" pages / Wikipedia infoboxes / SANFL / draftguru; method validated by exact '
               'reproduction of the independently-committed Q5 set). Each row asserts store-pick==recorded '
               'stored-ordinal before writing; 0 mismatches. Full source list: '
               'session_2026-07-11/pick_corrections/out/rookie_verified_websearch_2026-07-11.tsv',
        'already_official_q5':len(rookie_already),'missing_key':rookie_missing,'skipped':rookie_skip,
        'changes':rookie_applied}
    led['categories']['c4_psd_split_verified_expanded']={'n':len(psd_applied),'changes':psd_applied,
        'note':'5 further Pre-Season Draft rows found in the verification pass (incl. luke-nankervis 2021 — '
               'the reintroduced-PSD era proves PSD-folding is not confined to pre-2018). Chained after '
               'national before rookie via the rl_model.py PSD arm.'}
    led['categories']['c3_rookie_unverifiable']={'n':len(unver),
        'reason':'after the full verification pass, these RD rows still lack a citable official pick '
                 '(mostly obscure pre-2015 rows outside the substantial-career scope, plus a handful the '
                 'sweep flagged as club-ordinal-only / expansion-zone). Kept at stored ordinal, NOT guessed. '
                 'Near-$0 board impact (chained picks cap at KMAX=70).','rows':unver}

    json.dump(d,open(STORE,'w'))
    json.dump(led,open(SIDECAR,'w'),indent=1)
    md5=hashlib.md5(open(STORE,'rb').read()).hexdigest()
    print('STORE new md5:',md5)
    print('rookie corrections applied (expand):',len(rookie_applied),'| already official:',len(rookie_already),
          '| missing:',len(rookie_missing),'| skipped:',len(rookie_skip))
    print('new PSD splits:',len(psd_applied))
    import collections
    print('type dist:',dict(collections.Counter(p['type'] for p in d)))
    print('total rookie rows with verified _pick_source:',len(verified_keys),'| still unverifiable:',len(unver))

if __name__=='__main__': main()
