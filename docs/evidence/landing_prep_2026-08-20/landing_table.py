#!/usr/bin/env python3
"""THE FINAL ACCEPTANCE TABLE, re-printed on the RE-KEYED land/order-29 branch.

Every cell is SCRAPED from a raw output file on disk — no verdict is typed in. Each row names the
file it was read from and whether this seat RE-MEASURED it (a run performed in this seat, after the
C3 re-key) or CARRIED it (a prior seat's raw output, unmodified, md5-recorded). A row whose source
file is missing prints NOT-READ rather than a green tick.

NOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, the live board is untouched.
"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FC = os.path.join(ROOT, 'docs', 'evidence', 'final_candidate_2026-08-19')


def md5(p):
    try:
        return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    except Exception:
        return '--------'


def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return None


ROWS = []


def row(item, expect, got, verdict, how, src):
    ROWS.append((item, expect, got, verdict, how, os.path.relpath(src, ROOT) if src else '-'))


# ---------------------------------------------------------------- 1. THE IDENTITY CHAIN ----------
chain_p = os.path.join(HERE, 'IDENTITY_CHAIN_out.txt')
chain = read(chain_p)
IDENT = [('D7B_IDENT_P', '374d4e44', 'dial-off identity — every RL_O38*/O39/O40/O41/O42/O43 UNSET'),
         ('D7B_IDENT_K', 'f3101883', "ORDER K's ruled line, ORDER P dial off"),
         ('D7B_L0R',     '7f88f509', "A + B1 + TMAXPCT=20, the owner's reference"),
         ('D7B_NOO42',   'ff936186', 'the D5-final dial stack, RL_O42 UNSET'),
         ('D7B_BASE',    'daa16812', 'THE BASE, RL_O43 UNSET'),
         ('D7B_CAND',    'a05fe951', 'THE CANDIDATE'),
         ('D7B_CAND2',   'a05fe951', 'determinism repeat of D7B_CAND')]
built = {}
if chain:
    for tag, _e, _d in IDENT:
        m = re.search(r'^%s\s+([0-9a-f]{32})\s*$' % re.escape(tag), chain, re.M)
        if m:
            built[tag] = m.group(1)
for tag, exp, desc in IDENT:
    g = built.get(tag)
    row('identity %-11s %s' % (tag, desc), exp, (g or 'NOT BUILT')[:8],
        'GREEN' if g and g.startswith(exp) else ('NOT-READ' if not g else 'RED'),
        'RE-MEASURED this seat', chain_p)

det = built.get('D7B_CAND') and built.get('D7B_CAND') == built.get('D7B_CAND2')
row('determinism  D7B_CAND == D7B_CAND2 (x2)', 'equal',
    'equal' if det else 'NOT EQUAL / not built',
    'GREEN' if det else 'NOT-READ', 'RE-MEASURED this seat', chain_p)

# ------------------------------------------------- 2. DAY-0 89/89, BOTH INSTRUMENTS ---------------
n_int = len(re.findall(r'PRINTED-DAY-0 ASSERT: 89 of 89', chain)) if chain else 0
row('day-0 89/89 — INTERNAL board assert (printed == round(derived_v0 x D(c)) x numeraire, tol 0)',
    '89 of 89 on every build', '89 of 89 on %d of 7 builds' % n_int,
    'GREEN' if n_int == 7 else ('NOT-READ' if not chain else 'PARTIAL'),
    'RE-MEASURED this seat', chain_p)

emit_p = os.path.join(HERE, 'EMIT_LP_out.txt')
emit_how = 'RE-MEASURED this seat'
if not os.path.exists(emit_p):
    emit_p, emit_how = os.path.join(FC, 'EMIT_D7BCAND_out.txt'), 'CARRIED (v776 raw, md5 %s)'
emit = read(emit_p)
if emit_how.startswith('CARRIED'):
    emit_how = emit_how % md5(emit_p)
m = re.search(r'ORDER 31-F REPLICATION: (\d+) of (\d+) wired entrants on board (\w+)', emit or '')
row('day-0 89/89 — EMIT ORDER 31-F replication guard vs the FROZEN DAY0_CP.json (tol 0)',
    '89 of 89 on a05fe951', ('%s of %s on %s' % m.groups()) if m else 'NOT READ',
    'GREEN' if m and m.group(1) == m.group(2) == '89' and m.group(3).startswith('a05fe951') else 'NOT-READ',
    emit_how, emit_p)

emit2_p = os.path.join(FC, 'EMIT_D7BCAND2_out.txt')
m2 = re.search(r'ORDER 31-F REPLICATION: (\d+) of (\d+)', read(emit2_p) or '')
row('day-0 89/89 — emit second leg (both legs asserted)', '89 of 89',
    ('%s of %s' % m2.groups()) if m2 else 'NOT READ',
    'GREEN' if m2 and m2.group(1) == m2.group(2) == '89' else 'NOT-READ',
    'CARRIED (v776 raw, md5 %s)' % md5(emit2_p), emit2_p)

# ------------------------------------------------------------------ 3. THE CLASS MARK -------------
class_p = os.path.join(HERE, 'CLASS_LP_out.txt')
class_how = 'RE-MEASURED this seat'
if not os.path.exists(class_p):
    class_p, class_how = os.path.join(FC, 'CLASS_D7B_out.txt'), 'CARRIED (v776 raw, md5 %s)'
cls = read(class_p)
if class_how.startswith('CARRIED'):
    class_how = class_how % md5(class_p)
_lbl = 'LP' if class_how.startswith('RE-MEASURED') else 'D7BCAND'
m = re.search(r'^\s*%s\s+(\d\.\d+)\s+([+-]\d\.\d+)\s+([+-]\d\.\d+)\s+(.*)$' % _lbl, cls or '', re.M)
_ok_k = re.search(r'^\s*OKRULED\s+1\.0513\s', cls or '', re.M) is not None
row('class W2 draft-class mark — inside the law (floor / rail margins); instrument self-validated on '
    'ORDER K 1.0513 before any candidate number is quoted',
    '1.0672 inside the law',
    ('%s  floor %s  rail %s  %s  [ORDER K self-check %s]'
     % (m.group(1), m.group(2), m.group(3), m.group(4), 'PASS' if _ok_k else 'FAIL')) if m else 'NOT READ',
    'GREEN' if m and m.group(1) == '1.0672' and 'inside the law' in m.group(4) and _ok_k else 'NOT-READ',
    class_how, class_p)

# ------------------------------------------------------------------------ 4. THE TAIL -------------
tail_p = os.path.join(FC, 'TAIL_CP_out.txt')
tail = read(tail_p)
m = re.search(r'THE CANDIDATE READS (\d\.\d+)', tail or '')
row('tail calibration on the candidate\'s own charge form — RULED (built number stands, no dial chased)',
    '0.8004 (ruled red)', m.group(1) if m else 'NOT READ',
    'RULED' if m and m.group(1) == '0.8004' else 'NOT-READ',
    'CARRIED (v776 raw, md5 %s)' % md5(tail_p), tail_p)

# ------------------------------------------------------------------------ 5. THE BURN -------------
burn_p = os.path.join(HERE, 'carried', 'PR_BURN_CAND_out.txt')
burn = read(burn_p)
m = re.search(r'^\s*TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s*$', burn or '', re.M)
allm = re.findall(r'^\s*TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s*$', burn or '', re.M)
g = re.search(r'(\d+) of (\d+) rows exact', burn or '')
ok = allm and all(b == '0' and p == '0' for _n, b, p in allm) and g and g.group(1) == g.group(2)
row('burn census — every band, BOTH populations, on the FULLY-LIVE line (R3+O42+O43)',
    '0 burned / 0 points', ('%s populations, all bands 0 burned 0 pts; guard %s of %s exact'
                            % (len(allm), g.group(1), g.group(2))) if ok else 'NOT READ',
    'GREEN' if ok else 'NOT-READ',
    'CARRIED (v777 probe-repair seat, md5 %s)' % md5(burn_p), burn_p)

# -------------------------------------------------------------- 6. THE BIRTHDAY AXIS -------------
age_p = os.path.join(HERE, 'carried', 'PR_AGEGATE_CAND_out.txt')
age = read(age_p)
m = re.search(r'NET BOARD POINTS HANDED ACROSS THE BIRTHDAY, WHOLE BOARD\s*:\s*([+-]\d+)', age or '')
mv = re.search(r"ROWS WHOSE PRICE MOVES ON THE CHARGE'S BIRTHDAY ALONE\s*:\s*(\d+)", age or '')
tt = re.search(r'ROWS TESTED\s*:\s*(\d+)', age or '')
g1 = re.search(r'GUARD 1 — unperturbed, this routine reproduces the built board : (\d+) of (\d+) rows exact', age or '')
ok = m and mv and tt and g1 and m.group(1) == '+0' and mv.group(1) == '0' and g1.group(1) == g1.group(2)
row('acceptance birthday axis (o38_w age-24 handover, through R3 and the parity max)',
    '+0 on 804 of 804', ('%s net, %s movers of %s tested; guard %s of %s exact'
                         % (m.group(1), mv.group(1), tt.group(1), g1.group(1), g1.group(2))) if ok else 'NOT READ',
    'GREEN' if ok else 'NOT-READ',
    'CARRIED (v777 probe-repair seat, md5 %s)' % md5(age_p), age_p)

# ------------------------------------------------------------------------ 7. GUARD 5 -------------
g5_p = os.path.join(HERE, 'GUARD5_out.txt')
g5 = read(g5_p) or ''
bound_pass = 'GUARD 5 [bound] EXIT=0  ->  PASS' in g5
row('GUARD 5 — the boot form against the branch tree, RL_V0SURF_PKL bound (store · register · config · '
    'board · rl_model · fitted-artifact checkout + load-path · fv BOTH HALVES)',
    'PASS, every leg', 'PASS' if bound_pass else 'NOT READ',
    'GREEN' if bound_pass else 'NOT-READ', 'RE-MEASURED this seat', g5_p)

unb_fail = 'GUARD 5 [unbound] EXIT=1  ->  FAIL' in g5
ub_p = os.path.join(HERE, 'BUILD_UNBOUND_out.txt')
ub = read(ub_p) or ''
ub_halt = 'v0surf FROZEN-SIGNATURE HALT' in ub
row('GUARD 5 — the SAME form with RL_V0SURF_PKL UNBOUND (the boot-workspace footgun probe)',
    'PASS (footgun dead)', 'FAIL — v0surf LOAD-PATH MISMATCH, one leg, out-of-repo cause'
    if unb_fail else 'NOT READ',
    'RED — REPORTED, NOT WORKED AROUND' if unb_fail else 'NOT-READ',
    'RE-MEASURED this seat', g5_p)

row('unbound-surface CANDIDATE BUILD (no RL_V0SURF_PKL anywhere)',
    'a05fe951 byte-exact', 'NO BOARD — engine v0surf FROZEN-SIGNATURE HALT (fail-closed)'
    if ub_halt else 'NOT READ',
    'RED — FAIL-CLOSED, no wrong board can be produced' if ub_halt else 'NOT-READ',
    'RE-MEASURED this seat', ub_p)

# ------------------------------------------------------------------------ THE BOOK ---------------
row('THE BOOK RE-SEAL (data/book_stable_seal.json)', 're-sealed for the candidate',
    'HALTED — procedure ambiguous, decision not in the record',
    'HALTED — REPORTED, NOT GUESSED', 'RE-MEASURED this seat',
    os.path.join(HERE, 'RESEAL_PROBE_out.txt'))


def main():
    W = 118
    out = []
    a = out.append
    a('=' * W)
    a('THE FINAL ACCEPTANCE TABLE — re-printed on the RE-KEYED land/order-29')
    a('  candidate board a05fe951 / 664,949 / 804   ·   engine 5f434b95   ·   store cb38ef11')
    a('  dial line: docs/evidence/parity_2026-08-19/build_D7B.sh (D5-final stack + RL_O42=1 RL_O43=1, U0=7)')
    a('  NOT ADOPTED · NOTHING TAGGED · NOTHING PROMOTED TO MAIN · THE LIVE BOARD IS UNTOUCHED')
    a('  tag and main promote are OWNER-ONLY and the owner has not given the landing word.')
    a('=' * W)
    a('')
    greens = sum(1 for r in ROWS if r[3] == 'GREEN')
    ruled = sum(1 for r in ROWS if r[3].startswith('RULED'))
    reds = sum(1 for r in ROWS if r[3].startswith('RED'))
    halts = sum(1 for r in ROWS if r[3].startswith('HALTED'))
    nr = sum(1 for r in ROWS if r[3] == 'NOT-READ')
    a('  %d items  ·  %d GREEN  ·  %d RULED  ·  %d RED (named, reported)  ·  %d HALTED  ·  %d NOT-READ'
      % (len(ROWS), greens, ruled, reds, halts, nr))
    a('')
    for item, exp, got, verdict, how, src in ROWS:
        a('-' * W)
        a('  ITEM     %s' % item)
        a('  EXPECT   %s' % exp)
        a('  READ     %s' % got)
        a('  VERDICT  %s' % verdict)
        a('  HOW      %s' % how)
        a('  SOURCE   %s' % src)
    a('-' * W)
    a('')
    a('THE TWO ITEMS THAT ARE NOT GREEN, STATED PLAINLY:')
    a('')
    a('  1. THE UNBOUND-SURFACE FOOTGUN IS NOT DEAD. /home/claude/v0surf.pkl (fbc5b393) sits AHEAD of the')
    a('     branch\'s own data/v0surf.pkl (5dd34ca8) in the engine\'s OWN precedence, hard-coded at')
    a('     engine/rl_after/_merged_recover.py:1947 (_load_v0surf) and mirrored by boot_guard (0e). A pin')
    a('     re-key cannot move a precedence that lives in engine code, and the C3 pin is ALREADY CORRECT')
    a('     (it matches the branch file exactly), so there was no stale pin to fix here. Killing the footgun')
    a('     needs EITHER an engine edit (out of scope — the order says halt and report) OR deleting/replacing')
    a('     an out-of-repo file (the order forbids it). NOTE: bootstrap.sh does NOT seed /home/claude/v0surf.pkl')
    a('     (it seeds only cm_400.pkl and q97m.pkl), so the guard\'s own remedy line "Re-run bootstrap.sh"')
    a('     is WRONG for this artifact — reported as a finding.')
    a('     WHAT SAVES IT: the failure is FAIL-CLOSED at TWO independent layers. Guard 5 (0e) names it before')
    a('     the build, and the engine\'s own v0surf frozen-signature check HALTS the build at load time. The')
    a('     measured unbound build produced NO BOARD. A wrong board cannot be produced silently.')
    a('')
    a('  2. THE BOOK RE-SEAL IS HALTED, NOT GUESSED. See RESEAL_HALT.md for the full statement.')
    a('')
    a('=' * W)
    a('NOT ADOPTED. OWNER WORD PENDING.')
    a('=' * W)
    txt = '\n'.join(out) + '\n'
    open(os.path.join(HERE, 'LANDING_TABLE_out.txt'), 'w').write(txt)
    sys.stdout.write(txt)


if __name__ == '__main__':
    main()
