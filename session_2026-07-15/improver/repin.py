#!/usr/bin/env python3
"""IMPROVER BUILD — re-pin the board of record + expected_boot (board + engine_head ONLY; store/config/band/
register/fitted pins all UNCHANGED). Run AFTER the candidate (all-on) board is built in the workspace.
  1. copy the workspace all-on board -> data/rl_build/rl_app_data.json (repo record) + /home/claude/rl_build/ (shipped)
  2. expected_boot.json: board -> new md5, engine_head -> new engine md5; add _improver_note; nothing else moves.
"""
import json, hashlib, os, shutil, sys
ROOT='/home/user/afl-rl-engine'; RA='/home/claude/rl_workspace/rl_after'
def m(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
ws_board=os.path.join(RA,'rl_app_data.json')
assert os.path.exists(ws_board), 'build the all-on board first (rl_export in workspace)'
new_board=m(ws_board); new_eng=m(os.path.join(RA,'_merged_recover.py'))
shutil.copyfile(ws_board, os.path.join(ROOT,'data','rl_build','rl_app_data.json'))
shutil.copyfile(ws_board, '/home/claude/rl_build/rl_app_data.json')
eb_path=os.path.join(ROOT,'data','expected_boot.json'); eb=json.load(open(eb_path))
old_board=eb['board']; old_eng=eb['engine_head']
eb['board']=new_board; eb['engine_head']=new_eng
eb['_improver_note']=("IMPROVER BUILD (three legs, 2026-07-15, session_2026-07-15/improver; candidate, no bake/"
    "tag/main). RL_EO2 (kill the _eo min() => two-directional anti-flattery), RL_LSYM (L-SYMMETRY: equal bar "
    "DOWN_TOL + no _radq + smooth onset ramp on the riser side), RL_SAGE29 (the S_AGE 29-tail: age-29 slope "
    "0.0269->0.3793, fade still zero AT 30). engine edc47017 -> %s; board 9a9889f8 -> %s. store 340a7a32 "
    "UNCHANGED; config c2d233ae UNMOVED (three DECLARED kill-switches, not manifest dials; all-off reproduces "
    "9a9889f8 byte-exact). book RE-SEALED. Candidate — owner tag/main promote remain owner-only."
    % (new_eng[:8], new_board[:8]))
json.dump(eb, open(eb_path,'w'), indent=2)
print('re-pinned expected_boot: board %s -> %s | engine_head %s -> %s' % (old_board[:8], new_board[:8], old_eng[:8], new_eng[:8]))
print('board of record + shipped updated to %s' % new_board[:8])
