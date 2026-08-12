"""ORDER 23 (carried from ORDER 20C) — does the F2 book<->board parity gate break on the landed board?

Replicates one_source_selftest.py section (3) exactly: book 'cur' vs board 'v' for shared keys,
compared as round(cur / F) where F is the numeraire divisor the selftest uses.
"""
import json, os

ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-aca7a2be63ef974c9'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o23'

book = {v['key']: v.get('cur') for v in json.load(open(os.path.join(ROOT, 'engine/rl_after/s4_matrix.json'))).values()
        if v.get('key')}

for label, path in (('CONTROL board 1dbd1480', os.path.join(SP, 'board_C1_control.json')),
                    ('LANDED  board 665311ca', os.path.join(ROOT, 'data/rl_build/rl_app_data.json'))):
    board = {r['key']: r['v'] for r in json.load(open(path))['active']}
    shared = [k for k in board if k in book]
    for F in (1.0, 1.0524):
        mis = [(k, book[k], board[k]) for k in shared
               if book[k] is not None and board[k] != int(round(book[k] / F))]
        print("%-24s F=%-7s shared=%-5d mismatches=%d" % (label, F, len(shared), len(mis)))
    print()
