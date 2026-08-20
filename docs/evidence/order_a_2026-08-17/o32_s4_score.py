#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — A6: THE S4 MID-CAREER SHOOTOUT, RE-SCORED (prereg rules unchanged).

`s4_shootout.py` is exec'd WHOLE (the w1_cf_score.py discipline) with two declared substitutions:
CAND_P -> the Candidate 32 matrix; the RESULTS output -> this directory. The OLD matrix, the seed,
the bootstrap, the verdict rule and every ruler constant are the committed instrument's own.
REPORT-ONLY per R-W1: no pass/fail target — the years-4-6 recovery is the number the owner reads.

Controls first: the v0 column must be IDENTICAL record-for-record to the O31FFINAL matrix (the
entry law is untouched by every Candidate 32 mechanism) and yrs/seasons structurally identical.
"""
import os, json, hashlib, io, contextlib, collections

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

C32_P = SP + '/per_entrant_O32RFINAL.json'
BASE_P = SP + '/per_entrant_O31FFINAL.json'
C32 = json.load(open(C32_P)); BASE = json.load(open(BASE_P))
P('ORDER A / CANDIDATE 32 — S4 rescore controls')
P('  C32 matrix   md5 %s' % md5f(C32_P)[:8])
P('  base matrix  md5 %s (d97f1aee = the committed S4 candidate input)' % md5f(BASE_P)[:8])
c32r = {r['key']: r for r in C32['recs']}; bar = {r['key']: r for r in BASE['recs']}
assert set(c32r) == set(bar) and len(C32['recs']) == 2648
n_v0 = sum(1 for k in c32r if c32r[k]['v0'] != bar[k]['v0'])
n_struct = sum(1 for k in c32r if c32r[k]['yrs'] != bar[k]['yrs'] or c32r[k]['seasons'] != bar[k]['seasons'])
P('  CONTROL v0 column identical on all 2648 ......... %s' % ('PASS' if n_v0 == 0 else 'FAIL on %d' % n_v0))
P('  CONTROL yrs/seasons identical on all 2648 ....... %s' % ('PASS' if n_struct == 0 else 'FAIL on %d' % n_struct))
if n_v0 or n_struct:
    raise SystemExit('ORDER A HALT: matrix control failed')

S4_SRC = os.path.join(S4DIR, 's4_shootout.py')
_txt = open(S4_SRC).read()
S4_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ("CAND_P = SP + '/per_entrant_O31FFINAL.json'", "CAND_P = SP + '/per_entrant_O32RFINAL.json'"),
    ("with open(os.path.join(HERE, 'RESULTS_S4.json'), 'w') as f:",
     "with open(%r, 'w') as f:" % os.path.join(HERE, 'RESULTS_S4_32.json')),
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
open(os.path.join(HERE, 'S4_32_console.txt'), 'w').write(buf.getvalue())
P('  scorer ran clean; console S4_32_console.txt (%d lines)' % buf.getvalue().count('\n'))

NEW = json.load(open(os.path.join(HERE, 'RESULTS_S4_32.json')))
OLD = json.load(open(os.path.join(S4DIR, 'RESULTS_S4.json')))
def key_of(c):
    return (c['pop'], c['N'], c['horizon'])
newc = {key_of(c): c for c in NEW['cells']}
oldc = {key_of(c): c for c in OLD['cells']}
assert set(newc) == set(oldc)
bad_old = [k for k in newc if newc[k].get('M1') and oldc[k].get('M1')
           and newc[k]['M1']['rho_old'] != oldc[k]['M1']['rho_old']]
P('')
P('  CONTROL rho_old unchanged in every scored cell ... %s' % ('PASS' if not bad_old else 'FAIL %s' % bad_old[:4]))

P('')
P('=== PRIMARY ND CELLS: Candidate 32 vs Candidate 31 vs the old law (M1 Spearman) ===')
P('  %-3s %-6s %5s %8s %8s %8s %10s %10s %9s' %
  ('N', 'hz', 'n', 'rho_old', 'rho_c31', 'rho_c32', 'S4 verd', 'C32 verd', 'recovery'))
REC = []
for N in range(1, 7):
    for hz in ('dv1', 'dvrest'):
        k = ('ND', N, hz)
        o, n = oldc[k], newc[k]
        m0, m1 = o['M1'], n['M1']
        gap = m0['rho_old'] - m0['rho_cand']
        rec = (m1['rho_cand'] - m0['rho_cand']) / gap if abs(gap) > 1e-12 else float('nan')
        REC.append(dict(N=N, hz=hz, n=o['n'], rho_old=m0['rho_old'], rho_c31=m0['rho_cand'],
                        rho_c32=m1['rho_cand'], s4_verdict=m0['verdict'], c32_verdict=m1['verdict'],
                        c32_delta=m1['delta'], c32_ci=m1['delta_ci'], recovery=rec,
                        m2_s4=o.get('M2', {}).get('verdict'), m2_c32=n.get('M2', {}).get('verdict')))
        P('  %-3d %-6s %5d %8.3f %8.3f %8.3f %10s %10s %8s' %
          (N, hz, o['n'], m0['rho_old'], m0['rho_cand'], m1['rho_cand'], m0['verdict'], m1['verdict'],
           ('%+.0f%%' % (100 * rec)) if rec == rec else 'n/a'))

old_won = [r for r in REC if r['s4_verdict'] == 'oldlaw']
early_won = [r for r in REC if r['N'] <= 3 and r['s4_verdict'] == 'candidate']
recs_ = sorted(r['recovery'] for r in old_won)
med_rec = recs_[len(recs_) // 2] if len(recs_) % 2 else 0.5 * (recs_[len(recs_) // 2 - 1] + recs_[len(recs_) // 2])
lost_early = [r for r in early_won if r['c32_verdict'] != 'candidate']
flipped = [r for r in old_won if r['c32_verdict'] != 'oldlaw']
P('')
P('  A6 READING: %d S4 old-law-won primary M1 cells (years 4-6); MEDIAN RECOVERY %+.0f%%; per-cell %s'
  % (len(old_won), 100 * med_rec, ['N%d %s %+.0f%%' % (r['N'], r['hz'], 100 * r['recovery']) for r in old_won]))
P('  years 1-3 candidate wins retained: %d of %d %s' %
  (len(early_won) - len(lost_early), len(early_won),
   ('-- LOST: %s' % [(r['N'], r['hz']) for r in lost_early]) if lost_early else '(all)'))
P('  old-law cells no longer old-law wins: %d of %d -> %s'
  % (len(flipped), len(old_won), [(r['N'], r['hz'], r['c32_verdict']) for r in flipped]))

json.dump(dict(order='ORDER A / Candidate 32 — S4 mid-career rescore (A6, report-only)',
               instrument='order32_s4_2026-08-17/s4_shootout.py', instrument_md5=S4_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               c32_matrix_md5=md5f(C32_P), primary_cells=REC,
               median_recovery_oldlaw_cells=med_rec,
               early_wins_retained=[len(early_won) - len(lost_early), len(early_won)],
               oldlaw_cells_flipped=[(r['N'], r['hz'], r['c32_verdict']) for r in flipped]),
          open(os.path.join(HERE, 'S4_32_RECOVERY.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'S4_32_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: RESULTS_S4_32.json / S4_32_RECOVERY.json / S4_32_out.txt')
