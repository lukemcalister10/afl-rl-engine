#!/usr/bin/env python3
"""Re-stamp the CANDIDATE identity pins in data/expected_boot.json for the R-i=advance flip candidate:
engine_head + rl_model (from the checkout source), config (from the manifest hash), and the R-i tag.
The store/register/band pins are LEFT UNCHANGED (store untouched a2fbc9a0; register/band pinned elsewhere).
The board pin is stamped separately by the proof runner from the freshly-built advance board. This is NOT a
bake — it only tracks the candidate head so Guard 5 (workspace==checkout==pin) passes; owner bakes at his word.

Distinct from session_2026-07-09/injury_build/restamp_head.py (which carries the pre-flip Jul-9 tag and does
not touch config); this one owns the R-i tag + the config pin so regeneration/proof re-runs stay consistent."""
import json, hashlib, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def md5(p):
    h = hashlib.md5(); h.update(open(p, 'rb').read()); return h.hexdigest()
import sys; sys.path.insert(0, ROOT)
import config_manifest as _CM
bp = os.path.join(ROOT, 'data', 'expected_boot.json'); d = json.load(open(bp))
d['engine_head'] = md5(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py'))
d['rl_model']    = md5(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py'))
d['config']      = _CM.manifest_hash(ROOT)
d['tag'] = ("CANDIDATE chapter-3 injury/availability build 2026-07-10 — R-i FLIPPED to ADVANCE (owner ruling, "
            "DECISIONS v90 §36): RL_LTI_CLOCK code default = advance, manifest-pinned + ruling-config asserted "
            "(a paused bake fails loudly). Store a2fbc9a0 UNCHANGED (no re-seal); register 652d83e8 pinned. Baked "
            "reference stays v2.6 head 4b08796c (START_HERE/tag). engine_head/rl_model/config track the candidate "
            "head so Guard 5 (workspace==checkout==pin) passes; owner bakes at his word.")
with open(bp, 'w') as f:
    json.dump(d, f, indent=1); f.write('\n')
print("re-stamped R-i candidate: engine_head=%s rl_model=%s config=%s"
      % (d['engine_head'][:8], d['rl_model'][:8], d['config'][:8]))
