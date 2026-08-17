#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — M7/A1-A5: W2's SCORER, RUN WHOLE ON THE CANDIDATE 32 MATRIX.

`w2_forward_calibration.py` is the committed instrument (REUSED, NOT REINVENTED). Disclosed-copy
convention: character-level substitutions only, each printed and counted-unique — (1) the matrix
path/md5/engine-head identity re-pointed at per_entrant_O32FINAL.json (the Candidate 32 emit,
7a4b49db, engine d145fa8a, store cb38ef11 unchanged), (2) the output file re-pointed into this
directory. Every estimator, every seed, every bootstrap and every band is the instrument's own.
"""
import os, sys, json, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
SRC = os.path.join(EV, 'order33_w2_2026-08-17', 'w2_forward_calibration.py')

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ("CAND_P = SP + '/per_entrant_O31FFINAL.json'", "CAND_P = SP + '/per_entrant_O32FINAL.json'"),
    ("assert md5f(CAND_P) == 'd97f1aee4161ebcf785cd635ed095038', 'matrix md5 mismatch'",
     "assert md5f(CAND_P) == '7a4b49dbdfef147b1c4fc63c7f46ccd4', 'matrix md5 mismatch'"),
    ("assert A['meta']['engine_head'] == '71d9949a', 'engine head mismatch'",
     "assert A['meta']['engine_head'] == 'd145fa8a', 'engine head mismatch'"),
    ("print('identity OK: matrix md5 d97f1aee store cb38ef11 head 71d9949a n=2648')",
     "print('identity OK: matrix md5 7a4b49db store cb38ef11 head d145fa8a n=2648')"),
    ("with open(os.path.join(HERE, 'RESULTS_W2.json'), 'w') as f:",
     "with open(os.path.join(%r, 'W2_32_RESULTS.json'), 'w') as f:" % HERE),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:70]
    _run = _run.replace(a, b)
print('W2 SCORER RUN WHOLE — committed md5 %s, as-run md5 %s'
      % (HARNESS_MD5, hashlib.md5(_run.encode()).hexdigest()))
for a, b in SUBS:
    print('  SUB  %-70s -> %s' % (a[:70], b[:90]))
NS = {'__name__': '__main__', '__file__': SRC}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(_run, SRC, 'exec'), NS)
open(os.path.join(HERE, 'W2_32_console.txt'), 'w').write(buf.getvalue())
print(buf.getvalue())

# ---- the acceptance bands, scored (PREREG_32 A1-A5) -----------------------------------------------
R = json.load(open(os.path.join(HERE, 'W2_32_RESULTS.json')))
import numpy as np
per = {r['cls']: r['R_cand'] for r in R['level']['per_class_all']}
mean_0515 = float(np.mean([per[y] for y in range(2005, 2016)]))
mx = max(per.values()); mn = min(per.values())
slope = R['spread']['S1']['b']
W = R['spread']['S2']['W_cand']
cells = R['spread']['S3']['buckets']
terc = R['spread']['S3']['terciles']
gap59p = terc['5-9/poor']['gap']; gap59r = terc['5-9/riser']['gap']
g0 = cells['0']['gap']
V = []
V.append(('A1 class mean 2005-15 in [1.100,1.117]', mean_0515, 1.100 <= mean_0515 <= 1.117))
V.append(('A1 every class in [1.07,1.13]', (mn, mx), (mn >= 1.07 and mx <= 1.13)))
V.append(('A1 HARD no class > 1.14', mx, mx <= 1.14))
V.append(('A2 slope in [0.885,1.115]', slope, 0.885 <= slope <= 1.115))
V.append(('A3 W in [0.09,0.16]', W, 0.09 <= W <= 0.16))
V.append(('A4 5-9 poor gap halved (|gap|<=0.3445)', gap59p, abs(gap59p) <= 0.3445))
V.append(('A4 5-9 riser gap halved (|gap|<=0.2355)', gap59r, abs(gap59r) <= 0.2355))
V.append(('A5 g=0 gap within +-0.10', g0, abs(g0) <= 0.10))
print('\n==== PREREG_32 W2 SCORECARD (the committed instrument\'s own numbers) ====')
for nm, v, ok in V:
    print('  %-45s %-22s %s' % (nm, v if not isinstance(v, float) else round(v, 4), 'PASS' if ok else 'FAIL'))
json.dump(dict(instrument=os.path.relpath(SRC, os.path.dirname(EV)), instrument_md5=HARNESS_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               scorecard=[dict(gate=nm, value=v, verdict=('PASS' if ok else 'FAIL')) for nm, v, ok in V],
               mean_0515=mean_0515, min_class=mn, max_class=mx, slope=slope, W=W,
               cells={b: cells[b] for b in cells}, terciles=terc),
          open(os.path.join(HERE, 'W2_32_SCORECARD.json'), 'w'), indent=1, sort_keys=True, default=str)
print('written: W2_32_RESULTS.json / W2_32_SCORECARD.json / W2_32_console.txt')
