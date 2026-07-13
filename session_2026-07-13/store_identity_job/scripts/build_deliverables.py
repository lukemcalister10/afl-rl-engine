"""Build the two owner-facing deliverables from the before/after boards + the store transform:
   1. AFFECTED_ROWS.md — the COMPLETE affected-row list (v movers + club-display corrections)
   2. ELIGIBILITY_TABLE.md — the full K/G before/after tag table (191 normalize + 3 owner corrections)
"""
import json, sys, csv
SC = sys.argv[1].rstrip('/') + '/'
OUT = '/home/user/afl-rl-engine/session_2026-07-13/store_identity_job/out/'

b0 = json.load(open(SC + 'board_before_81e48293.json'))
b1 = json.load(open(SC + 'board_after_3dc19fbb.json'))
a0 = {r['key']: r for r in b0['active']}; a1 = {r['key']: r for r in b1['active']}
bk0 = {r['key']: r for r in b0['back']}; bk1 = {r['key']: r for r in b1['back']}

vmov = sorted([(k, a0[k]['v'], a1[k]['v']) for k in a0 if a0[k]['v'] != a1[k]['v']],
              key=lambda x: -abs(x[2] - x[1]))
cmov = [(k, a0[k].get('club'), a1[k].get('club')) for k in a0
        if a0[k].get('club') != a1[k].get('club')]
changed_club = sorted([(k, c0, c1) for k, c0, c1 in cmov if c0], key=lambda x: x[0])
filled_club = sorted([(k, c1) for k, c0, c1 in cmov if not c0], key=lambda x: x[0])
back_cmov = [k for k in bk0 if bk0[k].get('club') != bk1[k].get('club')]
back_vmov = [k for k in bk0 if bk0[k]['v'] != bk1[k].get('v')]

with open(OUT + 'AFFECTED_ROWS.md', 'w') as f:
    w = f.write
    w("# ITEM 20 — THE COMPLETE AFFECTED-ROW LIST (board 81e48293 → 3dc19fbb)\n\n")
    w("Store b0c39d78 → 340a7a32. Engine ev()/config/band UNCHANGED. Two kinds of change:\n")
    w("a VALUE move (bramble's games feed ev) and DISPLAY corrections (club field repointed to the\n")
    w("current AFL club). Eligibility changes are store-only (not shipped on the board) — see\n")
    w("ELIGIBILITY_TABLE.md.\n\n")
    w("## A. VALUE MOVERS (`v`) — the COMPLETE list\n\n")
    w("| key | before | after | Δ |\n|---|---:|---:|---:|\n")
    for k, o, n in vmov:
        w("| %s | %d | %d | %+d |\n" % (k, o, n, n - o))
    w("\n**%d value mover(s) total.** Sum v %d → %d (%+d). " % (
        len(vmov), sum(r['v'] for r in b0['active']), sum(r['v'] for r in b1['active']),
        sum(r['v'] for r in b1['active']) - sum(r['v'] for r in b0['active'])))
    w("The feared collateral ripple did NOT materialise — bramble's 2024 peak season is unchanged, so\n")
    w("the load-time calibration/cohort statistics did not move any other row. Bramble's own +1 is his\n")
    w("current-season (2026) level read shifting on 15→14 games @ 62.4→62.3.\n\n")
    w("## B. CLUB-DISPLAY CORRECTIONS (display-only; `club` repointed draft → current AFL club)\n\n")
    w("These are NOT value moves — the board now shows each player's CURRENT AFL club (afl_club) instead\n")
    w("of his DRAFT club (_draft_club). %d rows change club, %d formerly-blank rows fill.\n\n" % (
        len(changed_club), len(filled_club)))
    w("### B1. The ten formerly-blank rows filled (register item 33 red-path test)\n\n")
    w("| key | now displays |\n|---|---|\n")
    for k, c in filled_club:
        w("| %s | %s |\n" % (k, c))
    w("\n### B2. Draft-club → current-club corrections (%d rows)\n\n" % len(changed_club))
    w("| key | was (draft club) | now (current AFL club) |\n|---|---|---|\n")
    for k, c0, c1 in changed_club:
        w("| %s | %s | %s |\n" % (k, c0, c1))
    w("\n## C. UNCHANGED (verified)\n\n")
    w("- Back-catalogue rows: **%d club movers, %d v movers** (fall back to draft club; retired, no current club).\n" % (len(back_cmov), len(back_vmov)))
    w("- CAT_BY_CLUB: byte-identical (rename only). CAT_BY_RANGE: byte-identical.\n")
    w("- Panel 10/10 names: unmoved (no panel name is a v mover).\n")
    w("- lensConservation diagnostic: +1 (reflects bramble's lens values).\n")

# eligibility before/after table: old store (git HEAD, b0c39d78) vs new store (working tree, 340a7a32)
import subprocess
old_raw = subprocess.check_output(['git', 'show', 'HEAD:engine/rl_after/rl_model_data.json'],
                                  cwd='/home/user/afl-rl-engine')
old = {r['key']: r for r in json.loads(old_raw)}
new = {r['key']: r for r in json.load(open('/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'))}
CORR = {'darcy-gardiner', 'matt-whitlock', 'lukas-cooke'}
rows = []
for k in new:
    if k in old and old[k].get('eligibilities') != new[k].get('eligibilities'):
        cause = 'OWNER-CORRECTION' if k in CORR else 'K/G-normalize'
        rows.append((k, old[k].get('eligibilities'), new[k].get('eligibilities'), cause))
rows.sort(key=lambda r: (r[3] != 'OWNER-CORRECTION', r[0]))
with open(OUT + 'ELIGIBILITY_TABLE.md', 'w') as f:
    w = f.write
    w("# ITEM 20(e) / 20a — ELIGIBILITY BEFORE/AFTER TABLE (K/G companion-tag law + owner corrections)\n\n")
    w("Rule: drop the SAME-END G tag when the SAME-END K tag is present (cross-end survives; swingmen\n")
    w("keep both K). Then owner corrections. Store carries the normalized truth; raw strings preserved\n")
    w("in the archived CSV. Board impact: 0 (eligibilities are not shipped on the board).\n\n")
    w("**%d rows changed** (%d K/G-normalize + %d owner-correction).\n\n" % (
        len(rows), sum(1 for r in rows if r[3] == 'K/G-normalize'), sum(1 for r in rows if r[3] == 'OWNER-CORRECTION')))
    w("## Owner corrections (register 20a — restore agreement with each player's engine class)\n\n")
    w("| key | before | after | note |\n|---|---|---|---|\n")
    for k, b, a, c in rows:
        if c == 'OWNER-CORRECTION':
            w("| %s | %s | %s | owner-ruled |\n" % (k, b, a))
    w("\n## K/G-normalize (%d rows)\n\n" % sum(1 for r in rows if r[3] == 'K/G-normalize'))
    w("| key | before | after |\n|---|---|---|\n")
    for k, b, a, c in rows:
        if c == 'K/G-normalize':
            w("| %s | %s | %s |\n" % (k, b, a))
print("wrote AFFECTED_ROWS.md + ELIGIBILITY_TABLE.md (elig changed rows: %d)" % len(rows))
