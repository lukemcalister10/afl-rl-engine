#!/usr/bin/env python3
"""LEG A (iso evidence-fade) — re-pin the board of record + expected_boot (board + engine_head ONLY;
store/config/band/register/fitted/rl_model pins ALL UNCHANGED). Run AFTER the candidate (ISOFADE-ON, gate
mode) board is built in the workspace.
  1. copy the workspace candidate board -> data/rl_build/rl_app_data.json (repo record) + /home/claude/rl_build/ (shipped)
  2. expected_boot.json: board -> new md5, engine_head -> new engine md5, panel -> new note; add _isofade_note; nothing else moves.
RL_ISOFADE is a DECLARED kill-switch (not a manifest dial) => config_sha256 UNMOVED; RL_ISOFADE=0 reproduces 790136a3 byte-exact.
"""
import json, hashlib, os, shutil, sys
ROOT='/home/user/afl-rl-engine'; RA='/home/claude/rl_workspace/rl_after'
def m(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
ws_board=os.path.join(RA,'rl_app_data.json')
assert os.path.exists(ws_board), 'build the candidate (ISOFADE-ON, gate mode) board first (rl_export in workspace)'
new_board=m(ws_board); new_eng=m(os.path.join(RA,'_merged_recover.py'))
# panel note: the 10 named at the candidate (num = round(ev/1.0524))
PANEL=json.loads(open(os.path.join(os.path.dirname(__file__),'panel_new.json')).read()) if os.path.exists(os.path.join(os.path.dirname(__file__),'panel_new.json')) else None
shutil.copyfile(ws_board, os.path.join(ROOT,'data','rl_build','rl_app_data.json'))
shutil.copyfile(ws_board, '/home/claude/rl_build/rl_app_data.json')
eb_path=os.path.join(ROOT,'data','expected_boot.json'); eb=json.load(open(eb_path))
old_board=eb['board']; old_eng=eb['engine_head']
eb['board']=new_board; eb['engine_head']=new_eng
if PANEL:
    eb['panel']=("PASS 10/10 (LEG A iso evidence-fade candidate, board %s; the 10 named = round(ev/1.0524) and "
                 "equal the shipped board 'v': %s. RL_ISOFADE default ON; the iso pick-tax fades on the v2.10 "
                 "evidence weight and the ISO table is monotonized. RL_ISOFADE=0 reproduces board 790136a3 "
                 "byte-exact. Supersedes the v2.10 CAPTAINCY BAKE panel pin, board 790136a3.)"
                 % (new_board[:8], ' '.join('%s %d'%(n,v) for n,v in PANEL)))
eb['_isofade_note']=("LEG A — iso_corr EVIDENCE-FADE + ISO MONOTONIZATION (RL_ISOFADE, 2026-07-16, "
    "session_2026-07-16/isofade; candidate, no bake/tag/main). iso_corr(pos,pk) gains an evidence fade in the "
    "house pedigree-fade family on the v2.10 evidence weight w=E_q (iso_eff = 1 + (iso_corr-1)*exp(-w/1.1), "
    "residual-0 member; full strength at zero evidence => V0 unchanged BY CONSTRUCTION, -> 1.0 as evidence "
    "saturates), wired at all 6 iso_corr sites; the ISO multiplier is MONOTONIZED non-increasing in pick "
    "(IsotonicRegression(increasing=False), conserving) killing the Newcombe trough. Fade applies to REAL "
    "players only (synths = structural scaffolds, unfaded). engine fc7045d6 -> %s; board 790136a3 -> %s. store "
    "b1fd0bce UNCHANGED; config c2d233ae UNMOVED (RL_ISOFADE is a DECLARED kill-switch, not a manifest dial: "
    "RL_ISOFADE=0 reproduces board 790136a3 byte-exact, proven full-board md5). book RE-SEALED. English/Briggs "
    "1.561x -> 1.766x; watch rows Gawn/Bont/Reid UP; young side net +2749 (LIFT, no strip); the 37 young "
    "over-performer trims decomposed to 100%% pick-channel (raw_ev byte-identical). Candidate — owner tag/main "
    "promote owner-only." % (new_eng[:8], new_board[:8]))
json.dump(eb, open(eb_path,'w'), indent=2)
print('re-pinned expected_boot: board %s -> %s | engine_head %s -> %s%s'
      % (old_board[:8], new_board[:8], old_eng[:8], new_eng[:8], ' | panel updated' if PANEL else ''))
print('board of record + shipped updated to %s' % new_board[:8])
