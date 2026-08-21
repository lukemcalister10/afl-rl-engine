#!/usr/bin/env python3
"""BUILD THE A-RAW NO-ARB INSTRUMENT SET — the second declared byte-carry of the pricing seat's five
sfx_noarb_*.py, this time for THE ADOPTED ARM: VARIANT A RAW (RL_O44_LVLMONO=ratchet).

WHY THIS EXISTS. The owner re-ruled on 2026-08-21 after the B-raw no-arb reading was put in front of
him: "I misunderstood the A and B difference. I think based on those explanations, A raw I prefer.
Lock that in, unconserved." A RAW therefore needs the no-arb + class reading that B RAW got, and the
same instrument produces it.

THIS RUN CARRIES ALL FIVE ARMS AT ONCE — SFXARAW (adopted), SFXBRAW, SFXACON, SFXBCON, SFXBASE (the
live board) — because by now every matrix exists and a page that shows the owner four alternatives
beside the board he has is worth more than one that shows him a single column. It costs nothing: the
matrices are already on disk.

EVERY CHANGE IS A LITERAL STRING REPLACEMENT, DECLARED BELOW, AND EACH IS ASSERTED TO HAVE FIRED
EXACTLY ONCE. A carry that silently no-ops because an upstream line moved is the failure this file
refuses: it halts and says which replacement did not match. That assert already earned its keep once,
on the B-raw carry, catching a replacement that matched twice in sfx_noarb_page.py.

THE CHANGES, three kinds, same as the B-raw carry:
  (1) SFXARAW AND SFXBRAW ADDED to the label / candidate lists. The substantive change.
  (2) THE OUTPUT BASENAMES ARE SUFFIXED _ARAW so this set cannot overwrite either the pricing seat's
      committed artifacts or the B-raw set committed at 36f1122.
  (3) SRC — the pricing seat's directory — for the inputs carried from it rather than regenerated
      (DAY0_SFXBASE.json and its EMIT_*_out.txt logs). Both raw emit logs live HERE, so the lookup
      tries HERE first and falls back to SRC.

NOTHING IS ADOPTED BY THIS FILE. IT WRITES NO BOARD, NO PIN AND NO ENGINE FILE.
"""
import os

SRC = '/home/user/afl-rl-engine/docs/evidence/staircase_fix_2026-08-20'
DST = '/home/user/afl-rl-engine/docs/evidence/staircase_adoption_2026-08-21'

HEADER = '''# ==================================================================================================
# A-RAW CARRY. This file is docs/evidence/staircase_fix_2026-08-20/%s, byte-carried by
# build_araw_instruments.py with three declared changes and nothing else: (1) SFXARAW
# (RL_O44_LVLMONO=ratchet = VARIANT A RAW, THE ADOPTED ARM) and SFXBRAW added to the
# label/candidate lists, so all five arms are read side by side; (2) the output basenames suffixed
# _ARAW so this set cannot overwrite the pricing seat's artifacts or the B-raw set at 36f1122;
# (3) SRC introduced for the inputs carried from the pricing seat rather than regenerated.
# The owner re-ruled to A RAW on 2026-08-21 after seeing the B-raw reading. This is A RAW's.
# ==================================================================================================
'''

SRC_CONST = "\nSRC = '%s'  # the pricing seat's directory: carried inputs only\n" % SRC

A_LBL = "'*** ORDER 44 VARIANT A RAW — RL_O44_LVLMONO=ratchet — THE ADOPTED ARM ***'"
B_LBL = "'ORDER 44 variant B raw — RL_O44_LVLMONO=smooth (measured, NOT adopted)'"


def carry(name, subs, insert_src_after=None):
    src_p, dst_p = os.path.join(SRC, name), os.path.join(DST, 'araw_' + name[4:])
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
print('A-RAW NO-ARB INSTRUMENT CARRY — all five arms')
print('=' * 98)

# ------------------------------------------------------------------------------------------ BANDS
carry('sfx_noarb_bands.py', [
    ("for _l in ('SFXACON', 'SFXBCON', 'SFXBASE', 'D8CAND', 'D8BASE'):",
     "for _l in ('SFXARAW', 'SFXBRAW', 'SFXACON', 'SFXBCON', 'SFXBASE', 'D8CAND', 'D8BASE'):"),
    ("assert _CANON['SFXACON'] != _CANON['SFXBASE'], 'VARIANT A DID NOTHING — the pass-through did not fire'",
     "assert _CANON['SFXARAW'] != _CANON['SFXBASE'], 'VARIANT A RAW DID NOTHING — the pass-through did not fire'\n"
     "assert _CANON['SFXARAW'] != _CANON['SFXACON'], \\\n"
     "    'A RAW EQUALS A CONSERVED — the renormaliser is not in the candidate and the arm is mislabelled'\n"
     "assert _CANON['SFXARAW'] != _CANON['SFXBRAW'], \\\n"
     "    'A RAW EQUALS B RAW — the two variants are the same object and there was no choice to re-rule on'\n"
     "assert _CANON['SFXACON'] != _CANON['SFXBASE'], 'VARIANT A DID NOTHING — the pass-through did not fire'"),
    ("LABELS = [('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "LABELS = [('SFXARAW', %s),\n          ('SFXBRAW', %s),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***')," % (A_LBL, B_LBL)),
    ("'BANDS_NOARB_SFX.json'", "'BANDS_NOARB_ARAW.json'"),
    ("'BANDS_NOARB_SFX_out.txt'", "'BANDS_NOARB_ARAW_out.txt'"),
])

# ----------------------------------------------------------------------------------------- TABLES
carry('sfx_noarb_tables.py', [
    ("LABELS = [('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "LABELS = [('SFXARAW', %s),\n          ('SFXBRAW', %s),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***')," % (A_LBL, B_LBL)),
    ("CANDS = ('SFXACON', 'SFXBCON')", "CANDS = ('SFXARAW', 'SFXBRAW', 'SFXACON', 'SFXBCON')"),
    ("'STANDING_TABLES_NOARB_SFX.json'", "'STANDING_TABLES_NOARB_ARAW.json'"),
    ("'STANDING_TABLES_NOARB_SFX_out.txt'", "'STANDING_TABLES_NOARB_ARAW_out.txt'"),
])

# ------------------------------------------------------------------------------------------ CLASS
carry('sfx_noarb_class.py', [
    ("          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),",
     "          ('SFXARAW', %s),\n          ('SFXBRAW', %s),\n"
     "          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***')," % (A_LBL, B_LBL)),
    ("if l in ('SFXACON', 'SFXBCON') or os.path.exists",
     "if l in ('SFXARAW', 'SFXBRAW', 'SFXACON', 'SFXBCON') or os.path.exists"),
    ("'CLASS_SFX.json'", "'CLASS_ARAW.json'"),
    ("'CLASS_SFX_out.txt'", "'CLASS_ARAW_out.txt'"),
])

# ------------------------------------------------------------------------------------------- PAGE
carry('sfx_noarb_page.py', [
    ("CAND = os.environ.get('SFX_CAND', 'SFXACON')", "CAND = os.environ.get('SFX_CAND', 'SFXARAW')"),
    ("CANDS = {'SFXACON': ('ORDER 44 VARIANT A, CONSERVED', 'RL_O44_LVLMONO=ratchet+conserve',",
     "CANDS = {'SFXARAW': ('ORDER 44 VARIANT A, RAW — THE ADOPTED ARM', 'RL_O44_LVLMONO=ratchet',\n"
     "                     'b3e8da99bc7f632e5d1eebc732f9cf01'),\n"
     "         'SFXBRAW': ('ORDER 44 variant B, raw (measured, NOT adopted)', 'RL_O44_LVLMONO=smooth',\n"
     "                     '219266fafeca5ed4fb0206a72bf37046'),\n"
     "         'SFXACON': ('ORDER 44 VARIANT A, CONSERVED', 'RL_O44_LVLMONO=ratchet+conserve',"),
    ("BANDS_NOARB_SFX.json')))['nd']", "BANDS_NOARB_ARAW.json')))['nd']"),
    ("BANDS_NOARB_SFX.json')))['meta']", "BANDS_NOARB_ARAW.json')))['meta']"),
    ("AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_SFX.json')))",
     "AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_ARAW.json')))"),
    ("CL = json.load(open(os.path.join(HERE, 'CLASS_SFX.json')))",
     "CL = json.load(open(os.path.join(HERE, 'CLASS_ARAW.json')))"),
    ("OUTNAME = 'NOARB_SFX_%s.html' % CAND", "OUTNAME = 'NOARB_ARAW_%s.html' % CAND"),
    ("                ('the walk-forward emit, variant A conserved', 'EMIT_SFXACON_out.txt', 'run_emit_SFX.sh'),",
     "                ('*** the walk-forward emit, VARIANT A RAW — THE ADOPTED ARM ***',\n"
     "                 'EMIT_SFXARAW_out.txt', 'run_emit_SFX.sh (SFX_LABEL=SFXARAW RL_O44_LVLMONO=ratchet)'),\n"
     "                ('the walk-forward emit, variant B raw (measured, not adopted)',\n"
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
     "                ('the ND bands, both windows, ALL FIVE arms', 'BANDS_NOARB_ARAW_out.txt',\n"
     "                 'araw_noarb_bands.py'),\n"
     "                ('the ND bands, machine-readable', 'BANDS_NOARB_ARAW.json', 'araw_noarb_bands.py'),\n"
     "                ('the pool arms, both windows, ALL FIVE arms', 'STANDING_TABLES_NOARB_ARAW_out.txt',\n"
     "                 'araw_noarb_tables.py'),\n"
     "                ('the pool arms, machine-readable', 'STANDING_TABLES_NOARB_ARAW.json',\n"
     "                 'araw_noarb_tables.py'),\n"
     "                ('the class cohort mark (F4), all five arms', 'CLASS_ARAW_out.txt', 'araw_noarb_class.py'),\n"
     "                ('the page\\'s own inputs checked rather than asserted', 'NOARB_ARAW_CHECKS_out.txt',\n"
     "                 'araw_noarb_checks.py'),\n"
     "                ('the ADOPTION prereg, committed before the flip', 'PREREG_ADOPTION_A_RAW.md', 'process law P9'),\n"
     "                ('the B-raw reading the owner re-ruled on', 'NOARB_BRAW_SFXBRAW.html', 'braw_noarb_page.py'),"),
])

# ----------------------------------------------------------------------------------------- CHECKS
carry('sfx_noarb_checks.py', [
    ("BASE, CANDS = 'SFXBASE', ('SFXACON', 'SFXBCON')",
     "BASE, CANDS = 'SFXBASE', ('SFXARAW', 'SFXBRAW', 'SFXACON', 'SFXBCON')"),
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
     "check('SFXARAW differs from SFXACON — the ADOPTED arm is not the conserved one',\n"
     "      CAN['SFXARAW'] != CAN['SFXACON'], '%s vs %s' % (CAN['SFXARAW'], CAN['SFXACON']))\n"
     "check('SFXARAW differs from SFXBRAW — A raw is not B raw',\n"
     "      CAN['SFXARAW'] != CAN['SFXBRAW'], '%s vs %s' % (CAN['SFXARAW'], CAN['SFXBRAW']))\n"
     "check('SFXARAW differs from SFXBASE — the adopted arm is not the live board',\n"
     "      CAN['SFXARAW'] != CAN['SFXBASE'], '%s vs %s' % (CAN['SFXARAW'], CAN['SFXBASE']))"),
    ("CL = json.load(open(os.path.join(HERE, 'CLASS_SFX.json')))",
     "CL = json.load(open(os.path.join(HERE, 'CLASS_ARAW.json')))"),
    ("BJ = json.load(open(os.path.join(HERE, 'BANDS_NOARB_SFX.json')))",
     "BJ = json.load(open(os.path.join(HERE, 'BANDS_NOARB_ARAW.json')))"),
    ("AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_SFX.json')))",
     "AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_ARAW.json')))"),
    ("'NOARB_SFX_CHECKS_out.txt'", "'NOARB_ARAW_CHECKS_out.txt'"),
], insert_src_after="SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'")

print('=' * 98)
print('ALL FIVE CARRIED. Every declared replacement matched exactly once.')
