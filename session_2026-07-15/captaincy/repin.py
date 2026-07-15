#!/usr/bin/env python3
"""L-CAPTAIN WIRE — re-pin the board of record + expected_boot (board + rl_model ONLY; engine_head/store/config/
band/register/fitted pins all UNCHANGED). The curve lives in rl_model.py, so the rl_model pin moves and the
board moves; engine_head (_merged_recover.py) is fc7045d6, untouched. Run AFTER the candidate (RL_CAPT default
ON) board is built in the workspace.
  1. copy the workspace board -> data/rl_build/rl_app_data.json (repo record) + /home/claude/rl_build/ (shipped)
  2. expected_boot.json: board -> new md5, rl_model -> new rl_model.py md5; add _captaincy_note; nothing else moves.
"""
import json, hashlib, os, shutil
ROOT='/home/user/afl-rl-engine'; RA='/home/claude/rl_workspace/rl_after'
def m(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
ws_board=os.path.join(RA,'rl_app_data.json')
assert os.path.exists(ws_board), 'build the candidate board first (rl_export in workspace, gate mode default ON)'
new_board=m(ws_board); new_rlmodel=m(os.path.join(RA,'rl_model.py'))
shutil.copyfile(ws_board, os.path.join(ROOT,'data','rl_build','rl_app_data.json'))
shutil.copyfile(ws_board, '/home/claude/rl_build/rl_app_data.json')
eb_path=os.path.join(ROOT,'data','expected_boot.json'); eb=json.load(open(eb_path))
old_board=eb['board']; old_rlmodel=eb['rl_model']
eb['board']=new_board; eb['rl_model']=new_rlmodel
eb['_captaincy_note']=("L-CAPTAIN WIRE (the ruled captain curve, 2026-07-15, session_2026-07-15/captaincy; "
    "candidate, no bake/tag/main). credit(L)=G*integral[BAR->L]P(a)da (P logistic, BAR 105.0 M 109.5 W 1.85 "
    "G 1.00; the marginal IS P(L) so the slope-1 ceiling is structural) replaces the RETIRED saturating "
    "capt_prem (CAPT_GAIN/EXP/CAP, bar 107.4, hard 18-pt cap — never owner-ratified). Lives in rl_model.py "
    "952ddb3d -> %s; engine_head _merged_recover.py fc7045d6 UNCHANGED; board 800d0399 -> %s. store b1fd0bce "
    "UNCHANGED; config c2d233ae UNMOVED (RL_CAPT is a DECLARED kill-switch, not a manifest dial: RL_CAPT=0 "
    "reproduces board 800d0399 byte-exact). book RE-SEALED. Candidate — owner tag/main promote owner-only."
    % (new_rlmodel[:8], new_board[:8]))
json.dump(eb, open(eb_path,'w'), indent=2)
print('re-pinned expected_boot: board %s -> %s | rl_model %s -> %s (engine_head UNCHANGED)'
      % (old_board[:8], new_board[:8], old_rlmodel[:8], new_rlmodel[:8]))
print('board of record + shipped updated to %s' % new_board[:8])
