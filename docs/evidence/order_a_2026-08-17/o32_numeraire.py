#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — A12: THE NUMERAIRE. Report whether s moves.

Candidate 32 touches NO artifact: every mechanism is engine-side (clocks, gates, the discount
surface's constants) behind RL_O32. The all-in ladder, the positional v0 surface (nd_v0.posv, the
31-F head-fixed cells) and the numeraire block are byte-identical to Candidate 31's — asserted
here by md5 on the ONE file that carries all three, plus the block itself re-quoted. rl_model's
_load_numeraire re-asserts s == published_pin / H at every build (it ran on every board in this
order). The emit control already proved the v0 column identical record-for-record to the O31FFINAL
matrix. CONSEQUENCE: s is UNMOVED and no re-pin is triggered; the composed-ledger discipline for a
re-pin is therefore NOT invoked. The candidate remains PRE-NUMERAIRE exactly as Candidate 31 was.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ART = os.path.join(ROOT, 'engine', 'rl_after', 'pvc_curve_v2.json')
md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

m = md5f(ART)
J = json.load(open(ART))
NUM = J['numeraire']
H = float(NUM['pooled_head_pre_scale']); pin = float(NUM['published_pin']); s = float(NUM['s'])
P('ORDER A / CANDIDATE 32 — NUMERAIRE (A12)')
P('  artifact pvc_curve_v2.json md5 ......... %s' % m)
P('  Candidate 31 artifact md5 .............. 78ad9842525ae4f09875b95afc2e2b39')
P('  BYTE-IDENTICAL ......................... %s' % ('YES' if m == '78ad9842525ae4f09875b95afc2e2b39' else 'NO — HALT'))
assert m == '78ad9842525ae4f09875b95afc2e2b39', 'the artifact moved — a re-pin question exists'
P('  numeraire block: H=%.9f  pin=%.1f  s=%.12f' % (H, pin, s))
P('  s == pin/H to 1e-9 ..................... %s (|diff| %.2e)' % ('YES' if abs(s - pin / H) < 1e-9 else 'NO', abs(s - pin / H)))
P('')
P('  VERDICT: s DOES NOT MOVE. Candidate 32 writes no artifact and re-derives no ladder; the v0')
P('  column of its walk-forward matrix is record-for-record identical to Candidate 31\'s (the S4')
P('  rescore control). No re-pin is triggered; the composed-ledger discipline is not invoked; the')
P('  candidate is PRE-NUMERAIRE exactly as Candidate 31 was.')
json.dump(dict(artifact_md5=m, identical_to_c31=True, H=H, pin=pin, s=s,
               s_repin_triggered=False, verdict='s unmoved; pre-numeraire, as Candidate 31'),
          open(os.path.join(HERE, 'NUMERAIRE_32.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'NUMERAIRE_32_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: NUMERAIRE_32.json')
