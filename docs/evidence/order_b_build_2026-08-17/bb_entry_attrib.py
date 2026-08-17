#!/usr/bin/env python3
"""ORDER B — entry-year-control breach ATTRIBUTION. The five yr1 cells outside +-1.5% are re-read on
the stage-2 matrix (ladder+fade, NO taper). If stage-2 sits inside the bound, the movement is the
B-3 taper-retirement leg — the RULED ceiling repair lifting mature-age year-1 rows through the 0.10
WQ6 weight — attributed, not a veteran-mechanism leak."""
import json

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'


def yr1_nd(matrix, lo, hi):
    D = json.load(open(matrix))
    R = [r for r in D['recs'] if r.get('teaches_curve') and r.get('pick') and lo <= r['pick'] <= hi
         and 2004 <= r['year'] <= 2022]
    vals = []
    for r in R:
        yrs = r.get('yrs') or []
        vp = r.get('vpath') or []
        Y = r['year'] + 1
        if not yrs:
            vals.append(0.0); continue
        if Y > yrs[-1]:
            vals.append(0.0); continue
        v = vp[yrs.index(Y)]
        vals.append(0.0 if v is None else float(v))
    return sum(vals) / len(vals)


def yr1_arm(matrix, arm):
    D = json.load(open(matrix))

    def cohort(r):
        y = r.get('year')
        return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

    R = [r for r in D['recs'] if r.get('is_pool') and cohort(r) is not None and (r.get('v0') or 0) > 0
         and (arm == 'ALLPOOL' or r['type'] == arm) and 2005 <= cohort(r) <= 2023]
    num = den = 0.0
    n = 0
    for r in R:
        Y = cohort(r)
        yrs = r.get('yrs') or []
        vp = r.get('vpath') or []
        if yrs and Y < yrs[0]:
            continue
        v = 0.0
        if yrs and Y <= yrs[-1]:
            x = vp[yrs.index(Y)]
            v = 0.0 if x is None else float(x)
        num += v; den += float(r['v0']); n += 1
    return (num / n) / (den / n)


CELLS = [('picks 41-64', ('nd', 41, 64)), ('arm RD', ('arm', 'RD')), ('arm UNR', ('arm', 'UNR')),
         ('arm SSP', ('arm', 'SSP')), ('arm ALLPOOL', ('arm', 'ALLPOOL'))]
print('%-14s %10s %10s %10s   %9s %9s  %s' % ('breached cell', 'control', 'stage2', 'full', 'no-taper', 'full', 'attribution'))
OUT = {}
for name, spec in CELLS:
    vals = {}
    for lab in ('O32RFINAL', 'O33L2', 'O33B'):
        m = SP + '/per_entrant_%s.json' % lab
        vals[lab] = yr1_nd(m, spec[1], spec[2]) if spec[0] == 'nd' else yr1_arm(m, spec[1])
    r2 = vals['O33L2'] / vals['O32RFINAL'] - 1
    rf = vals['O33B'] / vals['O32RFINAL'] - 1
    attrib = 'TAPER LEG (B-3 ruled ceiling repair)' if abs(r2) <= 0.015 else 'NOT taper alone — investigate'
    OUT[name] = dict(control=vals['O32RFINAL'], stage2=vals['O33L2'], full=vals['O33B'],
                     rel_stage2=round(r2, 5), rel_full=round(rf, 5), attribution=attrib)
    print('%-14s %10.3f %10.3f %10.3f   %+8.2f%% %+8.2f%%  %s' % (
        name, vals['O32RFINAL'], vals['O33L2'], vals['O33B'], 100 * r2, 100 * rf, attrib))
json.dump(OUT, open('ENTRY_ATTRIB.json', 'w'), indent=1)
print('wrote ENTRY_ATTRIB.json')
