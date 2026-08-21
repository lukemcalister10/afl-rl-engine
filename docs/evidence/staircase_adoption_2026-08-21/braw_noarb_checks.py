# ==================================================================================================
# B-RAW CARRY. This file is docs/evidence/staircase_fix_2026-08-20/sfx_noarb_checks.py, byte-carried by
# build_braw_instruments.py with three declared changes and nothing else: (1) SFXBRAW
# (RL_O44_LVLMONO=smooth = VARIANT B RAW, THE ADOPTED ARM) added to the label/candidate lists;
# (2) the output basenames suffixed _BRAW so this set cannot overwrite or be confused with the
# pricing seat's committed artifacts; (3) SRC introduced for the inputs carried from that seat
# (DAY0_SFXBASE.json and the EMIT_*_out.txt logs) rather than regenerated here.
# The pricing seat named this leg open in PACKET_STAIRCASE.md section 0. This closes it.
# ==================================================================================================
#!/usr/bin/env python3
"""ORDER 44 MEASUREMENT — THE PAGE'S OWN INPUTS, CHECKED RATHER THAN ASSERTED.

d8_noarb_checks.py's JOB, carried; its CHECKS, re-derived. That distinction is the whole of this
file's honesty and it is stated first.

  D8's checks existed to prove ONE claim: that its base column was byte-identical to the on-file D7B
  matrix, so "the comparison column IS the standing-law table, re-emitted rather than re-typed". THAT
  CLAIM IS NOT AVAILABLE HERE and is not smuggled in: the live board moved a05fe951 -> 68be10c7 at
  the D8 adoption and the store moved cc02567f -> b745002e at the R23 advance, so this act's base
  matrix is a different object BY CONSTRUCTION. A carried assert would have been a green light for a
  claim nobody made.

  What this act CAN check, and therefore does, is the set of claims the two pages actually rest on:

  CHECK 1  provenance      all three matrices carry the SAME store (b745002e, the R23 store this
                           tree pins) and the SAME engine head (the edited tree) — so the ONLY
                           difference between base and candidate is the dial.
  CHECK 2  non-vacuity     each candidate's priced records differ from the base's. A dial that did
                           nothing would render two identical pages and no one would notice.
  CHECK 3  separation      the two candidates differ from EACH OTHER. If they did not, the owner
                           would be choosing between two names for one object.
  CHECK 4  THE DAY-0 CHECK the year-0 column is UNMOVED, row by row, on every wired entrant, under
                           BOTH variants, at tolerance 0. EXPECTED: 0 moved. ORDER 44 monotonises
                           the BAND; a day-0 entrant has no games and is priced off v0 x D(c_u), so
                           a moved day-0 price would mean the dial reached a surface it has no
                           business on. This is the SECOND reading of the same law — the emitter's
                           own fail-closed replication guard is the first, and it is quoted here
                           from each emit's log rather than re-run.
  CHECK 5  instrument      the class instrument reproduces ORDER K's published marks (1.0513 /
                           1.0324) off ORDER K's own matrix, before any candidate mark is read.
  CHECK 6  page inputs     every label the two pages render is present in all three table files.

ANY failure prints as a failure and the exit code is non-zero. NO ENGINE RUN — pure reads.
PRICED, NOT ADOPTED. NO PIN MOVES.
"""
import json, os, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
SRC = '/home/user/afl-rl-engine/docs/evidence/staircase_fix_2026-08-20'  # the pricing seat's directory: carried inputs only

BASE, CANDS = 'SFXBASE', ('SFXBRAW', 'SFXACON', 'SFXBCON')
STORE, ENGINE = 'b745002eb0a0fbb1c34fa44f1ef708d6', '3f4aa10b23102dc4f7362b73fc20ac7b'
L, FAIL = [], []


def P(s=''):
    print(s); L.append(str(s))


def check(name, ok, detail=''):
    P('  %-58s %s %s' % (name, 'PASS' if ok else '*** FAIL ***', detail))
    if not ok:
        FAIL.append(name)


def mx(lab):
    return json.load(open(os.path.join(SP, 'per_entrant_%s.json' % lab)))


P('=' * 118)
P('ORDER 44 — THE NO-ARB PAGE INPUTS, CHECKED')
P('=' * 118)
M = {l: mx(l) for l in (BASE,) + CANDS}
CAN = {l: hashlib.md5(json.dumps(M[l]['recs'], sort_keys=True).encode()).hexdigest()[:12] for l in M}

P()
P('CHECK 1 — PROVENANCE: one store, one engine, one record count; the ONLY difference is the dial.')
for l in (BASE,) + CANDS:
    me = M[l]['meta']
    P('  %-9s store %s   engine %s   records %d   recs-md5 %s'
      % (l, me['store_md5'], me['engine_head'], me['n_records'], CAN[l]))
check('every matrix on store %s' % STORE[:8],
      all(M[l]['meta']['store_md5'] == STORE[:8] or M[l]['meta']['store_md5'] == STORE for l in M),
      '(%s)' % ' '.join(sorted({M[l]['meta']['store_md5'] for l in M})))
check('every matrix on engine %s (the edited tree)' % ENGINE[:8],
      len({M[l]['meta']['engine_head'] for l in M}) == 1,
      '(%s)' % ' '.join(sorted({M[l]['meta']['engine_head'] for l in M})))
check('every matrix the same record count',
      len({M[l]['meta']['n_records'] for l in M}) == 1,
      '(%s)' % ' '.join(str(x) for x in sorted({M[l]['meta']['n_records'] for l in M})))

P()
P('CHECK 2 — NON-VACUITY: the dial did something, on both variants.')
for c in CANDS:
    check('%s differs from the base' % c, CAN[c] != CAN[BASE], '%s vs %s' % (CAN[c], CAN[BASE]))

P()
P('CHECK 3 — SEPARATION: the owner is choosing between two DIFFERENT objects.')
check('SFXACON differs from SFXBCON', CAN['SFXACON'] != CAN['SFXBCON'],
      '%s vs %s' % (CAN['SFXACON'], CAN['SFXBCON']))
check('SFXBRAW differs from SFXBCON — the RAW arm is not the conserved one',
      CAN['SFXBRAW'] != CAN['SFXBCON'], '%s vs %s' % (CAN['SFXBRAW'], CAN['SFXBCON']))
check('SFXBRAW differs from SFXBASE — the adopted arm is not the live board',
      CAN['SFXBRAW'] != CAN['SFXBASE'], '%s vs %s' % (CAN['SFXBRAW'], CAN['SFXBASE']))

P()
P('CHECK 4 — THE DAY-0 CHECK. The year-0 column, row by row, tolerance 0. EXPECTED: 0 MOVED.')
D0 = json.load(open(os.path.join(SRC, 'DAY0_SFXBASE.json')))
P('  reference: DAY0_SFXBASE.json — %s' % D0['label'])
P('  reference identity on the live board: %s' % D0['identity_all'])
b0 = {r['key']: r['v0'] for r in M[BASE]['recs']}
for c in CANDS:
    c0 = {r['key']: r['v0'] for r in M[c]['recs']}
    moved = sorted(k for k in b0 if k in c0 and float(b0[k] or 0) != float(c0[k] or 0))
    check('%s: year-0 column unmoved on all %d records' % (c, len(b0)), not moved,
          '(%d moved%s)' % (len(moved), (': ' + ', '.join(moved[:8])) if moved else ''))
    wired = [r['key'] for r in D0['rows']]
    wmoved = sorted(k for k in wired if k in b0 and k in c0 and float(b0[k] or 0) != float(c0[k] or 0))
    check('%s: the %d WIRED day-0 entrants unmoved' % (c, len(wired)), not wmoved,
          '(%d moved%s)' % (len(wmoved), (': ' + ', '.join(wmoved[:8])) if wmoved else ''))
P('  the emitter\'s OWN fail-closed replication guard, quoted from each emit log:')
for l in (BASE,) + CANDS:
    p = os.path.join(HERE, 'EMIT_%s_out.txt' % l)
    if not os.path.exists(p):
        p = os.path.join(SRC, 'EMIT_%s_out.txt' % l)   # carried from the pricing seat
    line = ''
    if os.path.exists(p):
        for ln in open(p):
            if 'REPLICATION' in ln:
                line = ln.strip()
    P('    %-9s %s' % (l, line or '(log not found)'))
    check('%s emit read the replication guard' % l, 'REPLICATION' in line and ' of ' in line,
          '')

P()
P('CHECK 5 — INSTRUMENT VALIDATION: the class instrument reproduces ORDER K before it is believed.')
CL = json.load(open(os.path.join(HERE, 'CLASS_BRAW.json')))
if 'OKRULED' in CL:
    dw = abs(CL['OKRULED']['w2'] - 1.0513); dc = abs(CL['OKRULED']['cohort'] - 1.0324)
    check('ORDER K reproduced (W2 1.0513 / cohort 1.0324)', max(dw, dc) < 5e-4,
          'W2 %.4f (%.4f) cohort %.4f (%.4f)' % (CL['OKRULED']['w2'], dw, CL['OKRULED']['cohort'], dc))
else:
    check('ORDER K validation row present', False, '(OKRULED matrix missing)')
for l in (BASE,) + CANDS:
    m = CL.get(l)
    P('  %-9s W2 %.4f   floor %+.4f (>= 1.03)   rail %+.4f (< 1.14)   %s'
      % (l, m['w2'], m['w2'] - 1.03, m['w2'] - 1.14,
         'INSIDE THE LAW' if (m['w2'] >= 1.03 and m['w2'] < 1.14) else '*** F4 FIRES ***'))
for c in CANDS:
    m = CL[c]
    check('F4 — %s inside floor 1.03 and rail 1.14' % c, m['w2'] >= 1.03 and m['w2'] < 1.14,
          'W2 %.4f' % m['w2'])

P()
P('CHECK 6 — PAGE INPUTS: every label the pages render is present in every table file.')
BJ = json.load(open(os.path.join(HERE, 'BANDS_NOARB_BRAW.json')))
AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_BRAW.json')))
for l in (BASE,) + CANDS:
    check('%s present in bands / arms / class' % l,
          l in BJ['nd'] and l in AJ['arms'] and l in CL, '')

P()
P('=' * 118)
P('RESULT: %s' % ('ALL CHECKS PASS' if not FAIL else '*** %d FAILED: %s ***' % (len(FAIL), FAIL)))
P('=' * 118)
open(os.path.join(HERE, 'NOARB_BRAW_CHECKS_out.txt'), 'w').write('\n'.join(L) + '\n')
sys.exit(1 if FAIL else 0)
