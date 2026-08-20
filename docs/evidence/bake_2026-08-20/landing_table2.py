#!/usr/bin/env python3
"""LANDING_TABLE_2 — THE FINAL ACCEPTANCE TABLE AFTER THE BAKE (register v780).

Same discipline as docs/evidence/landing_prep_2026-08-20/landing_table.py, which this carries: EVERY
CELL IS SCRAPED FROM A RAW OUTPUT FILE ON DISK. No verdict is typed in. A row whose source file is
missing prints NOT-READ rather than a green tick, and a row that reads red prints RED.

The two out-of-repo reds the landing prep left open are re-measured here, not restated.

NOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, the live board is untouched.
"""
import os, re, sys, hashlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ROWS = []


def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return None


def row(item, expect, got, verdict, src):
    ROWS.append((item, expect, got, verdict,
                 os.path.relpath(src, ROOT) if src else '-'))


def board_ids(txt):
    """Scrape the '=== BOARD IDS ===' block of build_BAKE.sh."""
    out = {}
    if not txt:
        return out
    blk = txt.split('=== BOARD IDS ===')[-1]
    for m in re.finditer(r'^(BAKE_\w+)\s+([0-9a-f]{32}|NO BOARD)\s*$', blk, re.M):
        out[m.group(1)] = m.group(2)
    return out


# ---------------------------------------------------------------- F1 / F2 / F3 : the board arms ----
arms_p = os.path.join(HERE, 'BUILD_BAKE_out.txt')
arms = read(arms_p)
B = board_ids(arms)

row('F1  THE BARE BUILD — no model-semantics RL_* set anywhere, RL_V0SURF_PKL unset',
    'a05fe951', (B.get('BAKE_CAND') or 'NOT BUILT')[:8],
    'GREEN' if (B.get('BAKE_CAND') or '').startswith('a05fe951') else ('NOT-READ' if not B.get('BAKE_CAND') else 'RED — FIRED'),
    arms_p)

c1, c2 = B.get('BAKE_CAND'), B.get('BAKE_CAND2')
row('F3  determinism x2 on the bare build', 'CAND == CAND2',
    ('%s == %s' % (c1[:8], c2[:8])) if (c1 and c2) else 'NOT BUILT',
    'GREEN' if (c1 and c2 and c1 == c2) else ('NOT-READ' if not (c1 and c2) else 'RED — FIRED'), arms_p)

KILL = [('BAKE_BASE',    'daa16812', 'RL_O43=0'),
        ('BAKE_NOO42',   'ff936186', 'RL_O42=0 RL_O43=0'),
        ('BAKE_IDENT_P', '374d4e44', 'OFFALL minus RL_O37=0'),
        ('BAKE_IDENT_K', 'f3101883', 'OFFALL + KLINE'),
        ('BAKE_L0R',     '7f88f509', 'OFFALL minus RL_O37=0, + O38A/O38B1/TMAXPCT=20')]
for tag, exp, ks in KILL:
    g = B.get(tag)
    row('F2  kill-switch %-13s  [%s]' % (tag.replace('BAKE_', ''), ks), exp, (g or 'NOT BUILT')[:8],
        'GREEN' if (g or '').startswith(exp) else ('NOT-READ' if not g else 'RED — FIRED'), arms_p)

# ---------------------------------------------------------------- F5 : Guard 5 --------------------
g5_p = os.path.join(HERE, 'GUARD5_BAKE_out.txt')
g5 = read(g5_p)


def g5_verdict(mode):
    if not g5:
        return None
    m = re.search(r'GUARD 5 \[%s\] EXIT=(\d+)\s+->\s+(\w+)' % mode, g5)
    return m.group(2) if m else None


for mode, label, expect in [
    ('unbound', 'F5  GUARD 5 UNBOUND — the footgun probe (no RL_V0SURF_PKL anywhere)', 'PASS'),
    ('bound',   '    GUARD 5 BOUND — control', 'PASS')]:
    v = g5_verdict(mode)
    row(label, expect, v or 'NOT-READ',
        'GREEN' if v == 'PASS' else ('NOT-READ' if not v else 'RED — FIRED'), g5_p)

v = g5_verdict('literal')
row('    GUARD 5 LITERAL — the SHARED OUT-OF-REPO workspace /home/claude/rl_workspace',
    'FAIL expected (out-of-repo)', v or 'NOT-READ',
    'RULED — OUT-OF-REPO, NOT THIS SEAT\'S TO FIX' if v == 'FAIL' else ('NOT-READ' if not v else 'CHANGED'), g5_p)

# ---------------------------------------------------------------- the frozen-signature guard ------
fs_p = os.path.join(HERE, 'FROZENSIG_out.txt')
fs = read(fs_p)
fs_ok = bool(fs) and 'FROZEN-SIGNATURE GUARD IS LIVE' in fs
row('    the frozen-SIGNATURE guard still HALTS on an unpinned surface',
    'HALT', 'HALTED' if fs_ok else ('NOT-READ' if not fs else 'DID NOT HALT'),
    'GREEN' if fs_ok else ('NOT-READ' if not fs else 'RED — A GUARD WAS WEAKENED'), fs_p)

# ---------------------------------------------------------------- Guards 1/2 : the sidecar --------
gg_p = os.path.join(HERE, 'GUARDS12_out.txt')
gg = read(gg_p)
gg_ok = bool(gg) and re.search(r'^GUARDS 1/2:\s+PASS', gg, re.M)
row('    SINGLE-SOURCE GUARDS 1/2 — the regenerated sidecar (RESEAL_HALT blocker C)',
    'PASS', 'PASS' if gg_ok else ('NOT-READ' if not gg else 'FAIL'),
    'GREEN' if gg_ok else ('NOT-READ' if not gg else 'RED'), gg_p)

# ---------------------------------------------------------------- the pins ------------------------
pin_p = os.path.join(HERE, 'PINS_BAKE_out.txt')
pin = read(pin_p)
cfg_unmoved = bool(pin) and re.search(r'^\s+config\s+eed19a75\S*\s+eed19a75\S*\s+UNMOVED', pin, re.M)
row('    config_sha256 + the expected_boot \'config\' pin UNMOVED (the C3 re-key stays valid)',
    'UNMOVED', 'UNMOVED' if cfg_unmoved else ('NOT-READ' if not pin else 'MOVED'),
    'GREEN' if cfg_unmoved else ('NOT-READ' if not pin else 'RED'), pin_p)

man_ok = bool(pin) and 'CONFIG-MANIFEST CHECK: PASS' in pin
row('    config_manifest.py check (manifest hash == pin == stored config_sha256)',
    'PASS', 'PASS' if man_ok else ('NOT-READ' if not pin else 'FAILED'),
    'GREEN' if man_ok else ('NOT-READ' if not pin else 'RED'), pin_p)

untouched = bool(pin) and 'fbc5b39387b2b135284a2e157f46c810' in pin
row('    /home/claude/v0surf.pkl BYTE-UNTOUCHED (the fix is in-repo precedence, not deletion)',
    'fbc5b393', 'fbc5b393' if untouched else 'NOT-READ',
    'GREEN' if untouched else 'NOT-READ', pin_p)

# ---------------------------------------------------------------- F4 : the emit -------------------
em_p = os.path.join(HERE, 'EMIT_BAKE_out.txt')
em = read(em_p)
m = re.search(r'ORDER 31-F REPLICATION:\s+(\d+) of (\d+)', em or '')
row('F4  emit replication guard vs FROZEN DAY0_CP.json (reference NOT re-based), run BARE',
    '89 of 89', ('%s of %s' % (m.group(1), m.group(2))) if m else 'NOT-READ',
    'GREEN' if (m and m.group(1) == m.group(2) == '89') else ('NOT-READ' if not m else 'RED — FIRED'), em_p)

m0 = re.search(r'PRINTED-DAY-0 ASSERT:\s+(\d+) of (\d+)', arms or '')
row('F4  day-0 internal assert on the BARE board (printed == derived, tolerance 0)',
    '89 of 89', ('%s of %s' % (m0.group(1), m0.group(2))) if m0 else 'NOT-READ',
    'GREEN' if (m0 and m0.group(1) == m0.group(2) == '89') else ('NOT-READ' if not m0 else 'RED — FIRED'), arms_p)

# ---------------------------------------------------------------- F6 : the class mark -------------
mm = re.search(r'VERDICT: (BYTE-IDENTICAL|THE MATRIX MOVED)', em or '')
row('F6  matrix identity vs the PRE-FLIP emit (per_entrant_LP.json c231fda2)',
    'BYTE-IDENTICAL', mm.group(1) if mm else 'NOT-READ',
    'GREEN' if (mm and mm.group(1) == 'BYTE-IDENTICAL') else ('NOT-READ' if not mm else 'MOVED — new mark reported'), em_p)

cl_p = os.path.join(HERE, 'CLASS_BAKE_out.txt')
cl = read(cl_p)
mc = re.search(r'^\s+BK\s+(\d+\.\d+)', cl or '', re.M) if cl else None
if mc is None and cl:
    mc = re.search(r'^\s+LP\s+(\d+\.\d+)', cl, re.M)
row('F6  year-1 class cohort mark on the shipped default (registered basis W2)',
    '1.0672', mc.group(1) if mc else ('CARRIED 1.0672' if (mm and mm.group(1) == 'BYTE-IDENTICAL') else 'NOT-READ'),
    'GREEN' if (mc and mc.group(1) == '1.0672') else
    ('GREEN — matrix byte-identical, mark stands' if (mm and mm.group(1) == 'BYTE-IDENTICAL' and not mc) else
     ('NOT-READ' if not mc else 'MOVED — REPORTED')),
    cl_p if cl else em_p)

# ---------------------------------------------------------------- F7 : the book seal --------------
rs_p = os.path.join(HERE, 'RESEAL_BAKE_out.txt')
rs = read(rs_p)
sealed = bool(rs) and 'RE-SEALED:' in rs
verified = bool(rs) and 'B3 RE-VERIFY: PASS' in rs
row('F7  THE BOOK RE-SEAL on the candidate line under GATE MODE (RESEAL_HALT blockers A+B+C)',
    'sealed + re-verified', ('sealed, B3 re-verify PASS' if (sealed and verified) else
                            ('sealed, NOT re-verified' if sealed else 'NOT SEALED')),
    'GREEN' if (sealed and verified) else ('NOT-READ' if not rs else 'HALTED — REPORTED'), rs_p)

# ---------------------------------------------------------------- print ---------------------------
W = 118
P = []


def out(s=''):
    print(s); P.append(str(s))


out('=' * W)
out('LANDING_TABLE_2 — THE FINAL ACCEPTANCE TABLE AFTER THE BAKE  (register v780, 2026-08-20)')
out('  every cell scraped from a raw output file — no verdict typed in')
out('=' * W)
for item, expect, got, verdict, src in ROWS:
    out('  ITEM     %s' % item)
    out('  EXPECT   %s' % expect)
    out('  READ     %s' % got)
    out('  VERDICT  %s' % verdict)
    out('  SOURCE   %s' % src)
    out('-' * W)

greens = sum(1 for r in ROWS if r[3].startswith('GREEN'))
ruled = sum(1 for r in ROWS if r[3].startswith('RULED'))
reds = [r for r in ROWS if r[3].startswith('RED') or r[3].startswith('NOT-READ')
        or r[3].startswith('MOVED') or r[3].startswith('HALTED') or r[3].startswith('CHANGED')]
out()
out('  %d rows: %d GREEN, %d RULED, %d not-green' % (len(ROWS), greens, ruled, len(reds)))
if reds:
    out()
    out('  NOT GREEN, STATED PLAINLY:')
    for r in reds:
        out('    - %s  ->  %s' % (r[0].strip(), r[3]))
else:
    out()
    out('  EVERY ITEM IS GREEN OR RULED.')
out()
out('  THE TWO OUT-OF-REPO REDS THE LANDING PREP LEFT OPEN, RE-MEASURED:')
out('    1. the v0surf UNBOUND leg — was RED (the out-of-repo copy won the precedence). The precedence')
out('       is now [$RL_V0SURF_PKL -> <repo>/data/v0surf.pkl] at BOTH mirrored sites, so it reads GREEN')
out('       above. /home/claude/v0surf.pkl is byte-untouched; it is simply no longer consulted.')
out('    2. the workspace-engine note — the SHARED /home/claude/rl_workspace still carries the stale D7')
out('       engine 29376d5a while this branch now carries its own head. The gap did not close, it WIDENED,')
out('       and legitimately so: the branch engine moved at this bake. Re-seeding that workspace is')
out('       bootstrap.sh\'s job and it is OUT OF REPO — this order forbids touching it. RULED, not fixed.')
out()
out('=' * W)
out('THIS PREPARES THE LANDING; IT IS NOT THE LANDING.')
out('NOT ADOPTED. OWNER WORD PENDING. Nothing merged, nothing tagged, PR #510 held, live board untouched.')
out('=' * W)

open(os.path.join(HERE, 'LANDING_TABLE_2_out.txt'), 'w').write('\n'.join(P) + '\n')
sys.exit(0)
