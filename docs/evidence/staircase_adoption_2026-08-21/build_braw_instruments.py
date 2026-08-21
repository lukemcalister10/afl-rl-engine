#!/usr/bin/env python3
"""BUILD THE B-RAW NO-ARB INSTRUMENT SET — a DECLARED BYTE-CARRY of the pricing seat's five
sfx_noarb_*.py files, with the changes named here and asserted to have fired.

WHY THIS EXISTS. The pricing seat emitted the no-arb bands, the standing tables, the class mark and
the rendered page for the TWO CONSERVED arms (SFXACON = ratchet+conserve, SFXBCON = smooth+conserve)
and for the base. THE OWNER ADOPTED B RAW (`smooth`), which therefore has NO no-arb reading and NO
class mark of its own. PACKET_STAIRCASE.md §0 names this itself and hands it forward as "one emit
plus four instrument passes ... the four sfx_noarb_*.py with the label added". This is that.

EVERY CHANGE IS A LITERAL STRING REPLACEMENT, DECLARED BELOW, AND EACH ONE IS ASSERTED TO HAVE FIRED.
A carry that silently no-ops because an upstream line moved is the failure this file refuses: it
halts instead, and says which replacement did not match.

THE CHANGES, and there are only three kinds:
  (1) SFXBRAW ADDED to the label / candidate lists. The substantive change, and the whole point.
  (2) THE OUTPUT BASENAMES ARE SUFFIXED _BRAW so this set can never be confused with, or overwrite,
      the pricing seat's committed artifacts of the same shape. The reads in the page and the checks
      are re-pointed to match.
  (3) SRC — the pricing seat's directory — is introduced for the two inputs CARRIED from it rather
      than regenerated here (DAY0_SFXBASE.json and the three EMIT_*_out.txt logs). The B-RAW emit
      log lives in this directory, so the lookup tries HERE first and falls back to SRC.

NOTHING IS ADOPTED BY THIS FILE. IT WRITES NO BOARD, NO PIN AND NO ENGINE FILE.
"""
import os
import shutil

SRC = '/home/user/afl-rl-engine/docs/evidence/staircase_fix_2026-08-20'
DST = '/home/user/afl-rl-engine/docs/evidence/staircase_adoption_2026-08-21'

HEADER = '''# ==================================================================================================
# B-RAW CARRY. This file is docs/evidence/staircase_fix_2026-08-20/%s, byte-carried by
# build_braw_instruments.py with three declared changes and nothing else: (1) SFXBRAW
# (RL_O44_LVLMONO=smooth = VARIANT B RAW, THE ADOPTED ARM) added to the label/candidate lists;
# (2) the output basenames suffixed _BRAW so this set cannot overwrite or be confused with the
# pricing seat's committed artifacts; (3) SRC introduced for the inputs carried from that seat
# (DAY0_SFXBASE.json and the EMIT_*_out.txt logs) rather than regenerated here.
# The pricing seat named this leg open in PACKET_STAIRCASE.md section 0. This closes it.
# ==================================================================================================
'''

SRC_CONST = "\nSRC = '%s'  # the pricing seat's directory: carried inputs only\n" % SRC


def carry(name, subs, insert_src_after=None):
    src_p, dst_p = os.path.join(SRC, name), os.path.join(DST, 'braw_' + name[4:])
    txt = open(src_p, encoding='utf-8').read()
    for i, (old, new) in enumerate(subs):
        n = txt.count(old)
        assert n == 1, 'REFUSING: replacement %d in %s matches %d times, not 1:\n%r' % (i, name, n, old)
        txt = txt.replace(old, new)
    if insert_src_after:
        assert txt.count(insert_src_after) == 1, 'SRC anchor not unique in %s' % name
        txt = txt.replace(insert_src_after, insert_src_after + SRC_CONST)
    txt = HEADER % name + txt
    open(dst_p, 'w', encoding='utf-8').write(txt)
    print('  carried %-24s -> %-28s (%d change(s))' % (name, os.path.basename(dst_p), len(subs)))


os.makedirs(DST, exist_ok=True)
print('B-RAW NO-ARB INSTRUMENT CARRY')
print('=' * 98)

# ------------------------------------------------------------------------------------------ BANDS
carry('sfx_noarb_bands.py', [
    ("for _l in ('SFXACON', 'SFXBCON', 'SFXBASE', 'D8CAND', 'D8BASE'):",
     "for _l in ('SFXBRAW', 'SFXACON', 'SFXBCON', 'SFXBASE', 'D8CAND', 'D8BASE'):"),
    ("assert _CANON['SFXACON'] != _CANON['SFXBASE'], 'VARIANT A DID NOTHING — the pass-through did not fire'",
     "assert _CANON['SFXBRAW'] != _CANON['SFXBASE'], 'VARIANT B RAW DID NOTHING — the pass-through did not fire'\n"
     "assert _CANON['SFXBRAW'] != _CANON['SFXBCON'], \\\n"
     "    'B RAW EQUALS B CONSERVED — the renormaliser is not in the candidate and the arm is mislabelled'\n"
     "assert _CANON['SFXACON'] != _CANON['SFXBASE'], 'VARIANT A DID NOTHING — the pass-through did not fire'"),
    ("LABELS = [('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "LABELS = [('SFXBRAW', '*** ORDER 44 VARIANT B RAW — RL_O44_LVLMONO=smooth — THE ADOPTED ARM ***'),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),"),
    ("'BANDS_NOARB_SFX.json'", "'BANDS_NOARB_BRAW.json'"),
    ("'BANDS_NOARB_SFX_out.txt'", "'BANDS_NOARB_BRAW_out.txt'"),
])

# ----------------------------------------------------------------------------------------- TABLES
carry('sfx_noarb_tables.py', [
    ("LABELS = [('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "LABELS = [('SFXBRAW', '*** ORDER 44 VARIANT B RAW — RL_O44_LVLMONO=smooth — THE ADOPTED ARM ***'),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),"),
    ("CANDS = ('SFXACON', 'SFXBCON')", "CANDS = ('SFXBRAW', 'SFXACON', 'SFXBCON')"),
    ("'STANDING_TABLES_NOARB_SFX.json'", "'STANDING_TABLES_NOARB_BRAW.json'"),
    ("'STANDING_TABLES_NOARB_SFX_out.txt'", "'STANDING_TABLES_NOARB_BRAW_out.txt'"),
])

# ------------------------------------------------------------------------------------------ CLASS
carry('sfx_noarb_class.py', [
    ("          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "          ('SFXBRAW', '*** ORDER 44 VARIANT B RAW — RL_O44_LVLMONO=smooth — THE ADOPTED ARM ***'),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),"),
    ("if l in ('SFXACON', 'SFXBCON') or os.path.exists",
     "if l in ('SFXBRAW', 'SFXACON', 'SFXBCON') or os.path.exists"),
    ("'CLASS_SFX.json'", "'CLASS_BRAW.json'"),
    ("'CLASS_SFX_out.txt'", "'CLASS_BRAW_out.txt'"),
])

# ------------------------------------------------------------------------------------------- PAGE
carry('sfx_noarb_page.py', [
    ("CAND = os.environ.get('SFX_CAND', 'SFXACON')", "CAND = os.environ.get('SFX_CAND', 'SFXBRAW')"),
    ("CANDS = {'SFXACON': ('ORDER 44 VARIANT A, CONSERVED', 'RL_O44_LVLMONO=ratchet+conserve',",
     "CANDS = {'SFXBRAW': ('ORDER 44 VARIANT B, RAW — THE ADOPTED ARM', 'RL_O44_LVLMONO=smooth',\n"
     "                     '219266fafeca5ed4fb0206a72bf37046'),\n"
     "         'SFXACON': ('ORDER 44 VARIANT A, CONSERVED', 'RL_O44_LVLMONO=ratchet+conserve',"),
    ("BANDS_NOARB_SFX.json')))['nd']", "BANDS_NOARB_BRAW.json')))['nd']"),
    ("BANDS_NOARB_SFX.json')))['meta']", "BANDS_NOARB_BRAW.json')))['meta']"),
    ("AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_SFX.json')))",
     "AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_BRAW.json')))"),
    ("CL = json.load(open(os.path.join(HERE, 'CLASS_SFX.json')))",
     "CL = json.load(open(os.path.join(HERE, 'CLASS_BRAW.json')))"),
    ("OUTNAME = 'NOARB_SFX_%s.html' % CAND", "OUTNAME = 'NOARB_BRAW_%s.html' % CAND"),
    # THE PROVENANCE TABLE THE PAGE RENDERS MUST NAME THE FILES THIS RUN ACTUALLY READ, not the
    # pricing seat's. A page that lists an input it did not open is the exact class of static prose
    # the pricing seat's own §D8 correction removed.
    ("                ('the walk-forward emit, variant A conserved', 'EMIT_SFXACON_out.txt', 'run_emit_SFX.sh'),",
     "                ('*** the walk-forward emit, VARIANT B RAW — THE ADOPTED ARM ***',\n"
     "                 'EMIT_SFXBRAW_out.txt', 'run_emit_SFX.sh (SFX_LABEL=SFXBRAW RL_O44_LVLMONO=smooth)'),\n"
     "                ('the walk-forward emit, variant A conserved', 'EMIT_SFXACON_out.txt', 'run_emit_SFX.sh'),"),
    ("                ('the ND bands, both windows, all three boards', 'BANDS_NOARB_SFX_out.txt', 'sfx_noarb_bands.py'),\n"
     "                ('the ND bands, machine-readable', 'BANDS_NOARB_SFX.json', 'sfx_noarb_bands.py'),\n"
     "                ('the pool arms, both windows, all three boards', 'STANDING_TABLES_NOARB_SFX_out.txt',\n"
     "                 'sfx_noarb_tables.py'),\n"
     "                ('the pool arms, machine-readable', 'STANDING_TABLES_NOARB_SFX.json', 'sfx_noarb_tables.py'),\n"
     "                ('the class cohort mark (F4)', 'CLASS_SFX_out.txt', 'sfx_noarb_class.py'),\n"
     "                ('the page\\'s own inputs checked rather than asserted', 'NOARB_SFX_CHECKS_out.txt',\n"
     "                 'sfx_noarb_checks.py'),",
     "                ('the ND bands, both windows, ALL FOUR boards incl. B RAW', 'BANDS_NOARB_BRAW_out.txt',\n"
     "                 'braw_noarb_bands.py'),\n"
     "                ('the ND bands, machine-readable', 'BANDS_NOARB_BRAW.json', 'braw_noarb_bands.py'),\n"
     "                ('the pool arms, both windows, ALL FOUR boards incl. B RAW',\n"
     "                 'STANDING_TABLES_NOARB_BRAW_out.txt', 'braw_noarb_tables.py'),\n"
     "                ('the pool arms, machine-readable', 'STANDING_TABLES_NOARB_BRAW.json',\n"
     "                 'braw_noarb_tables.py'),\n"
     "                ('the class cohort mark (F4), incl. B RAW', 'CLASS_BRAW_out.txt', 'braw_noarb_class.py'),\n"
     "                ('the page\\'s own inputs checked rather than asserted', 'NOARB_BRAW_CHECKS_out.txt',\n"
     "                 'braw_noarb_checks.py'),\n"
     "                ('the ADOPTION prereg, committed before the flip', 'PREREG_ADOPTION.md', 'process law P9'),"),
])

# ----------------------------------------------------------------------------------------- CHECKS
carry('sfx_noarb_checks.py', [
    ("BASE, CANDS = 'SFXBASE', ('SFXACON', 'SFXBCON')",
     "BASE, CANDS = 'SFXBASE', ('SFXBRAW', 'SFXACON', 'SFXBCON')"),
    ("D0 = json.load(open(os.path.join(HERE, 'DAY0_SFXBASE.json')))",
     "D0 = json.load(open(os.path.join(SRC, 'DAY0_SFXBASE.json')))"),
    ("    p = os.path.join(HERE, 'EMIT_%s_out.txt' % l)",
     "    p = os.path.join(HERE, 'EMIT_%s_out.txt' % l)\n"
     "    if not os.path.exists(p):\n"
     "        p = os.path.join(SRC, 'EMIT_%s_out.txt' % l)   # carried from the pricing seat"),
    ("check('SFXACON differs from SFXBCON', CAN['SFXACON'] != CAN['SFXBCON'],\n"
     "      '%s vs %s' % (CAN['SFXACON'], CAN['SFXBCON']))",
     "check('SFXACON differs from SFXBCON', CAN['SFXACON'] != CAN['SFXBCON'],\n"
     "      '%s vs %s' % (CAN['SFXACON'], CAN['SFXBCON']))\n"
     "check('SFXBRAW differs from SFXBCON — the RAW arm is not the conserved one',\n"
     "      CAN['SFXBRAW'] != CAN['SFXBCON'], '%s vs %s' % (CAN['SFXBRAW'], CAN['SFXBCON']))\n"
     "check('SFXBRAW differs from SFXBASE — the adopted arm is not the live board',\n"
     "      CAN['SFXBRAW'] != CAN['SFXBASE'], '%s vs %s' % (CAN['SFXBRAW'], CAN['SFXBASE']))"),
    ("CL = json.load(open(os.path.join(HERE, 'CLASS_SFX.json')))",
     "CL = json.load(open(os.path.join(HERE, 'CLASS_BRAW.json')))"),
    ("BJ = json.load(open(os.path.join(HERE, 'BANDS_NOARB_SFX.json')))",
     "BJ = json.load(open(os.path.join(HERE, 'BANDS_NOARB_BRAW.json')))"),
    ("AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_SFX.json')))",
     "AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_BRAW.json')))"),
    ("'NOARB_SFX_CHECKS_out.txt'", "'NOARB_BRAW_CHECKS_out.txt'"),
], insert_src_after="SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'")

print('=' * 98)
print('ALL FIVE CARRIED. Every declared replacement matched exactly once.')
