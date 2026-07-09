#!/usr/bin/env python3
"""Re-stamp the CANDIDATE engine-head pins in data/expected_boot.json (engine_head + rl_model) from the
current repo files, and set the candidate tag. The store/register/band/config pins are LEFT UNCHANGED (the
store is untouched a2fbc9a0; the register/config are pinned in their own commits). Run after each engine
edit during the Chapter-3 injury candidate. This is NOT a bake — it only tracks the candidate head so Guard 5
(workspace==checkout==pin) passes; the baked reference is the tag/START_HERE, not this candidate pin."""
import json, hashlib, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def md5(p):
    h=hashlib.md5(); h.update(open(p,'rb').read()); return h.hexdigest()
bp=os.path.join(ROOT,'data','expected_boot.json'); d=json.load(open(bp))
d['engine_head']=md5(os.path.join(ROOT,'engine','rl_after','_merged_recover.py'))
d['rl_model']=md5(os.path.join(ROOT,'engine','rl_after','rl_model.py'))
d['tag']=("CANDIDATE chapter-3 injury/availability build 2026-07-09 (RL_AVAIL/RL_LTI_RETURN/RL_LTI_CLOCK; "
          "_b2hc retired). Store a2fbc9a0 UNCHANGED (no re-seal); register 652d83e8 pinned. Baked reference "
          "stays v2.6 head 4b08796c (START_HERE/tag). engine_head/rl_model track the candidate head so Guard 5 "
          "(workspace==checkout==pin) passes; owner bakes at his word.")
json.dump(d,open(bp,'w'),indent=1); print("re-stamped engine_head=%s rl_model=%s"%(d['engine_head'][:8],d['rl_model'][:8]))
