#!/usr/bin/env python3
"""ORDER C — the S4 mid-career shootout, re-scored on the ORDER C matrix (prereg §6.6; the repair's
o32_s4_score.py carried; the ONE change: the candidate matrix is per_entrant_O34FINAL.json and the
comparison column beside the old law is the REPAIRED C32 result, so movement either way is visible).
REPORT-ONLY per R-W1: no pass/fail target — the years-4-6 recovery is the number the owner reads.
"""
import os, json, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
S4DIR = os.path.join(EV, 'order32_s4_2026-08-17')

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s, flush=True)

def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

C34_P = SP + '/per_entrant_O34FINAL.json'
BASE_P = SP + '/per_entrant_O31FFINAL.json'
C34 = json.load(open(C34_P)); BASE = json.load(open(BASE_P))
P('ORDER C — S4 rescore controls')
P('  Order C matrix md5 %s' % md5f(C34_P)[:8])
P('  base matrix    md5 %s (d97f1aee = the committed S4 candidate input)' % md5f(BASE_P)[:8])
c34r = {r['key']: r for r in C34['recs']}; bar = {r['key']: r for r in BASE['recs']}
assert set(c34r) == set(bar) and len(C34['recs']) == 2648
n_v0 = sum(1 for k in c34r if c34r[k]['v0'] != bar[k]['v0'])
n_struct = sum(1 for k in c34r if c34r[k]['yrs'] != bar[k]['yrs'] or c34r[k]['seasons'] != bar[k]['seasons'])
P('  CONTROL v0 column identical on all 2648 ......... %s' % ('PASS' if n_v0 == 0 else 'FAIL on %d' % n_v0))
P('  CONTROL yrs/seasons identical on all 2648 ....... %s' % ('PASS' if n_struct == 0 else 'FAIL on %d' % n_struct))
if n_v0 or n_struct:
    raise SystemExit('ORDER C HALT: matrix control failed')

S4_SRC = os.path.join(S4DIR, 's4_shootout.py')
_txt = open(S4_SRC).read()
S4_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ("CAND_P = SP + '/per_entrant_O31FFINAL.json'", "CAND_P = SP + '/per_entrant_O34FINAL.json'"),
    ("with open(os.path.join(HERE, 'RESULTS_S4.json'), 'w') as f:",
     "with open(%r, 'w') as f:" % os.path.join(HERE, 'RESULTS_S4_34.json')),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:60]
    _run = _run.replace(a, b)
P('')
P('S4 SCORER RUN WHOLE — committed md5 %s, as-run md5 %s' % (S4_MD5, hashlib.md5(_run.encode()).hexdigest()))
for a, b in SUBS:
    P('  SUB  %-60s -> %s' % (a[:60], b[:80]))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(_run, S4_SRC, 'exec'), {'__name__': '__main__', '__file__': S4_SRC})
open(os.path.join(HERE, 'S4_34_console.txt'), 'w').write(buf.getvalue())
P('  scorer ran clean; console S4_34_console.txt (%d lines)' % buf.getvalue().count('\n'))

NEW = json.load(open(os.path.join(HERE, 'RESULTS_S4_34.json')))
OLD = json.load(open(os.path.join(S4DIR, 'RESULTS_S4.json')))
R32 = json.load(open(os.path.join(EV, 'order_a_2026-08-17', 'RESULTS_S4_32.json')))
def key_of(c):
    return (c['pop'], c['N'], c['horizon'])
newc = {key_of(c): c for c in NEW['cells']}
oldc = {key_of(c): c for c in OLD['cells']}
c32c = {key_of(c): c for c in R32['cells']}
assert set(newc) == set(oldc)
bad_old = [k for k in newc if newc[k].get('M1') and oldc[k].get('M1')
           and newc[k]['M1']['rho_old'] != oldc[k]['M1']['rho_old']]
P('')
P('  CONTROL rho_old unchanged in every scored cell ... %s' % ('PASS' if not bad_old else 'FAIL %s' % bad_old[:4]))

P('')
P('=== PRIMARY ND CELLS: Order C vs repaired C32 vs Candidate 31 vs the old law (M1 Spearman) ===')
P('  %-3s %-6s %5s %8s %8s %8s %8s %10s %9s %9s' %
  ('N', 'hz', 'n', 'rho_old', 'rho_c31', 'rho_c32', 'rho_C', 'C verd', 'rec_C32', 'rec_C'))
REC = []
for N in range(1, 7):
    for hz in ('dv1', 'dvrest'):
        k = ('ND', N, hz)
        o, n, m32 = oldc[k], newc[k], c32c[k]
        m0, m1, m2 = o['M1'], n['M1'], m32['M1']
        gap = m0['rho_old'] - m0['rho_cand']
        rec = (m1['rho_cand'] - m0['rho_cand']) / gap if abs(gap) > 1e-12 else float('nan')
        rec32 = (m2['rho_cand'] - m0['rho_cand']) / gap if abs(gap) > 1e-12 else float('nan')
        REC.append(dict(N=N, hz=hz, n=o['n'], rho_old=m0['rho_old'], rho_c31=m0['rho_cand'],
                        rho_c32=m2['rho_cand'], rho_c=m1['rho_cand'],
                        s4_verdict=m0['verdict'], c_verdict=m1['verdict'],
                        recovery_c32=rec32, recovery=rec))
        P('  %-3d %-6s %5d %8.3f %8.3f %8.3f %8.3f %10s %8s %8s' %
          (N, hz, o['n'], m0['rho_old'], m0['rho_cand'], m2['rho_cand'], m1['rho_cand'], m1['verdict'],
           ('%+.0f%%' % (100 * rec32)) if rec32 == rec32 else 'n/a',
           ('%+.0f%%' % (100 * rec)) if rec == rec else 'n/a'))

old_won = [r for r in REC if r['s4_verdict'] == 'oldlaw']
early_won = [r for r in REC if r['N'] <= 3 and r['s4_verdict'] == 'candidate']
recs_ = sorted(r['recovery'] for r in old_won)
med_rec = recs_[len(recs_) // 2] if len(recs_) % 2 else 0.5 * (recs_[len(recs_) // 2 - 1] + recs_[len(recs_) // 2])
recs32_ = sorted(r['recovery_c32'] for r in old_won)
med_rec32 = recs32_[len(recs32_) // 2] if len(recs32_) % 2 else 0.5 * (recs32_[len(recs32_) // 2 - 1] + recs32_[len(recs32_) // 2])
lost_early = [r for r in early_won if r['c_verdict'] != 'candidate']
P('')
P('  READING: %d S4 old-law-won primary M1 cells (years 4-6); MEDIAN RECOVERY %+.0f%% under ORDER C '
  '(repaired C32 was %+.0f%%); per-cell %s'
  % (len(old_won), 100 * med_rec, 100 * med_rec32,
     ['N%d %s %+.0f%%' % (r['N'], r['hz'], 100 * r['recovery']) for r in old_won]))
P('  years 1-3 candidate wins retained: %d of %d %s' %
  (len(early_won) - len(lost_early), len(early_won),
   ('-- LOST: %s' % [(r['N'], r['hz']) for r in lost_early]) if lost_early else '(all)'))

json.dump(dict(order='ORDER C — S4 mid-career rescore (report-only)',
               instrument='order32_s4_2026-08-17/s4_shootout.py', instrument_md5=S4_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               c34_matrix_md5=md5f(C34_P), primary_cells=REC,
               median_recovery_oldlaw_cells=med_rec,
               median_recovery_oldlaw_cells_c32r=med_rec32,
               early_wins_retained=[len(early_won) - len(lost_early), len(early_won)]),
          open(os.path.join(HERE, 'S4_34_RECOVERY.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'S4_34_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: RESULTS_S4_34.json / S4_34_RECOVERY.json / S4_34_out.txt')
