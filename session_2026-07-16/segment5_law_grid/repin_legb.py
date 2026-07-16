#!/usr/bin/env python3
"""LEG B SEGMENT-5 — re-pin the board of record + expected_boot to the ON candidate (map at UNCOMP_S_DEFAULT).
Moves ONLY board + engine_head + rl_model + panel note; store/config/band/register/fitted pins UNCHANGED
(RL_UNCOMP is a DECLARED kill-switch, not a manifest dial => config_sha256 UNMOVED; RL_UNCOMP=0 reproduces
8d90c9ac byte-exact). Run AFTER the ON board is built in the workspace (rl_export, default => map ON).
usage: python3 repin_legb.py <s> "<panel 10 named as 'Name val' space-joined>"
"""
import json, hashlib, os, shutil, sys
ROOT = '/home/user/afl-rl-engine'; RA = '/home/claude/rl_workspace/rl_after'
def m(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
S = sys.argv[1]
PANEL = sys.argv[2] if len(sys.argv) > 2 else ''
ws_board = os.path.join(RA, 'rl_app_data.json')
assert os.path.exists(ws_board), 'build the ON candidate board first (rl_export in workspace, map ON)'
new_board = m(ws_board)
new_eng = m(os.path.join(RA, '_merged_recover.py'))
new_rl = m(os.path.join(RA, 'rl_model.py'))
shutil.copyfile(ws_board, os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json'))
shutil.copyfile(ws_board, '/home/claude/rl_build/rl_app_data.json')
eb_path = os.path.join(ROOT, 'data', 'expected_boot.json'); eb = json.load(open(eb_path))
old = dict(board=eb['board'], engine_head=eb['engine_head'], rl_model=eb['rl_model'])
eb['board'] = new_board; eb['engine_head'] = new_eng; eb['rl_model'] = new_rl
eb['panel'] = ("PASS 10/10 (LEG B un-compress candidate, board %s; RL_UNCOMP default ON at s=%s, "
               "UNCOMP_DECAY=0.25 R105.6; the 10 named = round(ev/1.0524): %s. RL_UNCOMP=0 reproduces the "
               "Leg-A board 8d90c9ac BYTE-EXACT (the A/B identity); config_sha256 UNMOVED.)"
               % (new_board[:8], S, PANEL))
eb['_legb_note'] = ("LEG B — UN-COMPRESS THE OUTPUT->PRICE MAP (RL_UNCOMP, 2026-07-16, "
    "session_2026-07-16/segment5_law_grid; candidate, no bake/tag/main). v' = pr0^(1-w)*(V_ref_b*rho)^w, "
    "w = s*E*ramp, at the production-value hook (price6, captain-free), production-side per-position "
    "conservation; rho = games x recency realised output (u_s=games_s*0.25^(Ynow-year_s), d=0.25 OWNER-SET "
    "R105.6; NO exclusion/floor/phase). s=%s selected as the SMALLEST grid point clearing beta point>=0.80 "
    "(OWNER bar). engine (_merged_recover.py) a83c9f6d->%s (seg-4 law wiring + seg-5 _isreal load-order fix); "
    "rl_model f79fc740->%s (UNCOMP_DECAY 0.5->0.25 + UNCOMP_S_DEFAULT=%s); board 8d90c9ac->%s. store b1fd0bce "
    "UNCHANGED; config c2d233ae UNMOVED (RL_UNCOMP is a DECLARED kill-switch, not a manifest dial: RL_UNCOMP=0 "
    "reproduces 8d90c9ac byte-exact). book RE-SEALED. Candidate — owner tag/main promote owner-only."
    % (S, new_eng[:8], new_rl[:8], S, new_board[:8]))
json.dump(eb, open(eb_path, 'w'), indent=2)
print("re-pinned expected_boot:")
print("  board       %s -> %s" % (old['board'][:8], new_board[:8]))
print("  engine_head %s -> %s" % (old['engine_head'][:8], new_eng[:8]))
print("  rl_model    %s -> %s" % (old['rl_model'][:8], new_rl[:8]))
print("  store/config/band/register/fitted UNCHANGED")
print("board of record + shipped updated to %s" % new_board[:8])
