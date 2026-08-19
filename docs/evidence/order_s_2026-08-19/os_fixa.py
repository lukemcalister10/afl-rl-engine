#!/usr/bin/env python3
"""ORDER S — FALSIFIER S-F4. IS FIX A STILL EXACT UNDER THE COMPRESSION AND THE MATURE PREMIUM?

READ-ONLY, no engine load — the grids are read out of the engine SOURCE and the arithmetic is done
here, so this is an independent check of the engine rather than the engine checking itself.

FIX A finds the running maximum of  psi(x) = x - LAMBDA*A(g)*T(s(x))  over x = ln(v0) by evaluating
psi only at a finite candidate set: the PG grid nodes below the row's own price, plus the clip
crossings. THAT IS ONLY CORRECT IF psi ATTAINS ITS MAXIMUM ON EACH SEGMENT AT AN ENDPOINT.

Under ORDER P/Q/R's HARD CLIP that is trivial: psi is piecewise-AFFINE, so the maximum on a segment
is at an endpoint by inspection. UNDER THE COMPRESSION IT IS NOT PIECEWISE-AFFINE ANY MORE, so it
has to be checked, and this file checks it.

THE ARGUMENT, and then the measurement:
  s(x) is non-increasing in x (PG is isotone), so on a segment  T_raw = alpha + beta*x  with beta >= 0.
  Where T_raw > 0:   psi = x - LAMBDA*A*C + LAMBDA*A*C*exp(-(alpha+beta*x)/C)
                     = linear + a POSITIVE multiple of exp(affine)  =>  CONVEX  =>  max at an endpoint.
  Where T_raw == 0:  psi = x, linear, slope 1.
  AT THE ZERO CROSSING psi' DROPS from 1 to 1 - LAMBDA*A*beta. THAT KINK IS CONCAVE, so the crossing
  MUST be in the candidate set or the node maximum can miss the true maximum.

THE ENGINE ALREADY ADDS IT (o38_mono's `_extra` loop, `_tv = 0.0`). **THIS SEAT'S OWN FIRST VERSION
OF THIS CHECK OMITTED IT AND THE FALSIFIER FIRED, AT 1.062e-02. THE CHECK WAS WRONG, NOT THE ENGINE.**
Both runs are printed below so the correction is auditable rather than silently made.

  usage: python3 os_fixa.py
"""
import re, math, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py')).read()
LL = []


def P(s=''):
    print(s); LL.append(str(s))


def grab(name):
    m = re.search(r'%s=\{(.*?)\n    \}' % name, SRC, re.S)
    assert m, name
    ns = {}
    exec('import math as _math\n' + m.group(0).replace(name, 'G'), ns)
    return ns['G']


GY = grab('O37_PG_GRID')
GM = grab('O40_PGM_GRID')
LAM = 0.1743833036575403
BSAT = 0.11464630061141393
S0 = -2.4527332249999999
THR = BSAT / LAM
S_PQ = {5: -33.06133449874688, 15: -22.148794633345666, 20: -19.024574086528315}


def at(gr, x, cls):
    lo, hi, y = gr[cls]
    if x <= lo:
        return y[0]
    if x >= hi:
        return y[-1]
    t = (x - lo) / (hi - lo) * (len(y) - 1)
    i = int(t)
    if i >= len(y) - 1:
        return y[-1]
    return y[i] + (t - i) * (y[i + 1] - y[i])


def nodes_of(gr, cls):
    lo, hi, y = gr[cls]
    return [lo + (hi - lo) * i / (len(y) - 1.0) for i in range(len(y))]


def C_of(pct):
    return 1.0 - THR * (S_PQ[pct] - S0)


def T(s, pct, form):
    raw = max(1.0 - THR * (s - S0), 0.0)
    C = C_of(pct)
    return C * (1.0 - math.exp(-raw / C)) if form == 'smooth' else min(raw, C)


P('=' * 118)
P('ORDER S — FALSIFIER S-F4. IS FIX A\'s NODE MAXIMUM STILL EXACT UNDER THE ORDER S FORMS?')
P('=' * 118)
P('  independent of the engine: the grids are read out of the engine SOURCE and the arithmetic is')
P('  done here. 60 interior probes per segment.')
P()

WEIGHTS = [('TALL only', 1.0, 0.0, 0.0, 0.0), ('SMALL only', 0.0, 1.0, 0.0, 0.0),
           ('half and half', 0.5, 0.5, 0.0, 0.0),
           ('SMALL, half MATURE', 0.0, 0.5, 0.0, 0.5),
           ('MIX with MATURE', 0.3, 0.4, 0.1, 0.2)]
OUTS = (-40.0, -25.0, -12.0, -4.0, 0.0, 8.0)
GS = (1.0, 5.0, 20.0, 60.0, 200.0)
RES = {}


def run(with_crossing, pgmat, form, pct):
    worst = 0.0; cases = 0; wc = None
    for wname, wT, wS, wTm, wSm in WEIGHTS:
        if not pgmat and (wTm or wSm):
            continue
        if pgmat and not (wTm or wSm):
            continue
        base = []
        if wT > 0 or wTm > 0:
            base += nodes_of(GY, 'TALL')
            if pgmat:
                base += nodes_of(GM, 'TALL')
        if wS > 0 or wSm > 0:
            base += nodes_of(GY, 'SMALL')
            if pgmat:
                base += nodes_of(GM, 'SMALL')
        base = sorted(set(base))
        for OUTv in OUTS:
            def sx(x):
                return OUTv - ((wT - wTm) * at(GY, x, 'TALL') + wTm * at(GM, x, 'TALL')
                               + (wS - wSm) * at(GY, x, 'SMALL') + wSm * at(GM, x, 'SMALL'))
            nodes = list(base)
            if with_crossing:
                tvs = (0.0,) if form == 'smooth' else (0.0, C_of(pct))
                extra = []
                for a, b in zip(base[:-1], base[1:]):
                    sa, sb = sx(a), sx(b)
                    if sa == sb:
                        continue
                    for tv in tvs:
                        st = S0 + (1.0 - tv) / THR
                        if (sa - st) * (sb - st) < 0.0:
                            extra.append(a + (b - a) * (st - sa) / (sb - sa))
                nodes = sorted(set(base + extra))
            for g in GS:
                A = 1.0 - math.exp(-g / 9.89)

                def psi(x):
                    return x - LAM * A * T(sx(x), pct, form)
                for a, b in zip(nodes[:-1], nodes[1:]):
                    if b - a < 1e-12:
                        continue
                    ends = max(psi(a), psi(b))
                    interior = max(psi(a + (b - a) * k / 60.0) for k in range(1, 60))
                    cases += 1
                    if interior - ends > worst:
                        worst = interior - ends
                        wc = (wname, OUTv, g, a, b)
    return worst, cases, wc


P('  %-12s %-8s %-6s %-14s %10s %14s   %s'
  % ('form', 'anchor', 'PGMAT', 'zero crossing', 'segments', 'worst miss', 'verdict'))
for form, pct in (('clip', 5), ('smooth', 15), ('smooth', 20)):
    for pgmat in (False, True):
        for wc_on in ((False, True) if form == 'smooth' and not pgmat else (True,)):
            w, n, worstc = run(wc_on, pgmat, form, pct)
            tag = '%s|p%d|%s|%s' % (form, pct, 'PGMAT' if pgmat else 'young',
                                    'node' if wc_on else 'OMITTED')
            RES[tag] = dict(worst=w, segments=n, form=form, pct=pct, pgmat=pgmat,
                            crossing=wc_on, case=worstc)
            P('  %-12s %-8s %-6s %-14s %10d %14.3e   %s'
              % (form, 'p%d' % pct, 'yes' if pgmat else 'no',
                 'IN the set' if wc_on else '**OMITTED**', n, w,
                 'exact' if w <= 1e-12 else '**S-F4 FIRES**'))
P()
P('  THE ROW LABELLED "OMITTED" IS THIS SEAT\'S OWN FIRST, WRONG CHECK, KEPT ON THE PAGE.')
P('  It leaves the zero crossing out of the candidate set. The miss is real and it is 1.06e-02 of')
P('  psi — so the crossing is NOT decorative, it is load-bearing, and the engine already carries it.')
P()
bad = [k for k, v in RES.items() if v['crossing'] and v['worst'] > 1e-12]
P('  S-F4 VERDICT: %s'
  % ('*** FIRES on %s ***' % ', '.join(bad) if bad else
     'DOES NOT FIRE. With the zero crossing in the candidate set — which is what the engine does — '
     'psi is convex on every segment and FIX A\'s node maximum is EXACT under the compression and '
     'under the mature premium alike.'))
P()
P('  WHAT THIS DOES NOT PROVE, said plainly: it proves the SEARCH is exact given the decomposition.')
P('  That the decomposition itself still reconstructs the engine\'s own surplus under the ORDER S')
P('  dials is a SEPARATE falsifier, S-F3, measured on every real row in IDENTITY_S_out.txt.')

json.dump(RES, open(os.path.join(HERE, 'FIXA_S.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'FIXA_S_out.txt'), 'w').write('\n'.join(LL) + '\n')
print('\nwrote FIXA_S_out.txt / FIXA_S.json')
