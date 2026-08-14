"""ORDER 29C — THE PREDICTION CALCULATOR. Run BEFORE the emit, BEFORE any instrument.

This file exists so `PREREG_29C.md` can table NUMBERS instead of adjectives, and so a wrong number
is a scoreable breach rather than a vague "roughly". It does NOT run either instrument. It takes two
COMMITTED, ALREADY-PUBLISHED inputs —

    per_entrant_O29B.json   ORDER 29B's as-of matrix (md5 ca24a49a), whose years 1..7 ORDER 29C does
                            not touch, and
    LANDED_V0_29C.json      the landed-entry-law year-0 column, produced by `o29c_lawprobe.py` from
                            pvc_curve_v2.json + the store, and PROVEN against the board's own 89
                            printed day-0 numbers at tolerance 0

— and re-derives, in this seat's OWN code, the aggregation the two instruments perform. If this
model of the instruments is wrong, the Step-3 readings will not match it and the prediction is
scored BREACHED. That is the point: the prediction is falsifiable by the instruments, and it is
filed before they run.

WHY THIS IS A PREDICTION AND NOT A RESULT. The instruments are the authority. This file is a
declaration of what this seat expects them to print, made from inputs that cannot see them. Nothing
in Step 3 is permitted to edit this file or PREREG_29C.md.
"""
import os, sys, json, statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = sys.argv[1]
LANDED = sys.argv[2]
OUTJ = sys.argv[3]

D = json.load(open(MATRIX))
meta, R = D['meta'], D['recs']
V0 = json.load(open(LANDED))
CHARGE = 0.14

miss = [r['key'] for r in R if '%s|%s|%s' % (r['key'], r['type'], r['year']) not in V0]
print("records %d   landed-v0 map misses: %d %s" % (len(R), len(miss), miss[:8]))

NEW = {}
for r in R:
    NEW[id(r)] = V0['%s|%s|%s' % (r['key'], r['type'], r['year'])]

WINDOW_END = max(y for r in R
                 for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
print("WINDOW_END %d  (unchanged: derived from vpath, which ORDER 29C does not touch)" % WINDOW_END)


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def allarm_value(r, N):
    if N == 0:
        return float(NEW[id(r)]), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0, 'ended'
    if Y < yrs[0]: return None, 'pre'
    if Y > yrs[-1]: return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


def t338_value(r, N):
    if N == 0:
        return float(NEW[id(r)]), 'v0'
    vp = r.get('vpath') or []
    i = N - 1
    if i >= len(vp): return 0.0, 'ended'
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


OUT = {}

# ---------- ALL-ARM ----------
elig = [r for r in R if cohort(r) is not None and (NEW[id(r)] or 0) > 0]
elig_old = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
print("all-arm eligible: OLD basis %d   LANDED-LAW basis %d   (delta %d — the v0<=0 exclusion)"
      % (len(elig_old), len(elig), len(elig) - len(elig_old)))
dropped = [(r['key'], r['type'], r['pos'], r['pick']) for r in elig_old if r not in elig]
print("  rows the landed law drops from the all-arm population: %s" % dropped)

for wname, lo, hi in [('PRIMARY  cohorts 2005-2023', 2005, 2023),
                      ('MODERN   cohorts 2019-2023', 2019, 2023)]:
    pop = [r for r in elig if lo <= cohort(r) <= hi]
    rows = {}
    for N in range(0, 8):
        reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WINDOW_END]
        vals, v0s = [], []
        for r in reached:
            v, k = allarm_value(r, N)
            if k == 'pre': continue
            vals.append(v); v0s.append(float(NEW[id(r)]))
        rows[N] = (statistics.mean(vals) / statistics.mean(v0s)) if vals else float('nan')
    a = rows[1] - 1.0; m = CHARGE - a
    print("%-28s n=%4d  yr1 %.4f  apprec %+.2f%%  margin %+.2f%%  %s"
          % (wname, len(pop), rows[1], 100 * a, 100 * m, 'ARB' if m < 0 else 'no arb'))
    per = {}
    arms = Counter(r['type'] for r in pop)
    for t in sorted(arms, key=lambda t: -arms[t]):
        sub = [r for r in pop if r['type'] == t]
        cells = {}
        for N in (1, 4):
            reached = [r for r in sub if cohort(r) + N - 1 <= WINDOW_END]
            vv, zz = [], []
            for r in reached:
                v, k = allarm_value(r, N)
                if k == 'pre': continue
                vv.append(v); zz.append(float(NEW[id(r)]))
            cells[N] = (statistics.mean(vv) / statistics.mean(zz)) if vv and statistics.mean(zz) else float('nan')
        per[t] = dict(n=len(sub), yr1=round(cells[1], 4), yr4=round(cells[4], 4),
                      yr1_crosses_1=bool(cells[1] >= 1.0), yr4_crosses_1=bool(cells[4] >= 1.0))
    OUT[wname] = dict(n=len(pop), yr={str(k): round(v, 4) for k, v in rows.items()},
                      apprec=a, margin=m, verdict='ARB' if m < 0 else 'no arb', by_arm=per)
    print("    by arm: " + "  ".join("%s yr1 %.4f yr4 %.4f" % (t, per[t]['yr1'], per[t]['yr4'])
                                     for t in sorted(per, key=lambda t: -per[t]['n'])))

# ---------- LEGACY ND (noarb_table_338.py population) ----------
# THE POPULATION IS NOT GUESSED. It is the committed harness's OWN `load_matrix`, imported from
# ORDER 29's disclosed copy — the same call `noarb_table_338.py` makes — so the EXPECT_N = 1200 pin
# and the year window (YR_LO..CLASS_CUT) come from the instrument rather than from this seat's
# reading of it. A first cut of this file filtered on `teaches_curve and 1<=pick<=64` alone and got
# 1447; that is the whole reason this import exists.
sys.path.insert(0, os.environ['RL_NOARB_DIR'])
import harness_pvc_REPINNED_pass3 as H
_meta_h, ND = H.load_matrix(MATRIX)
print("legacy ND population, via the harness's own load_matrix: %d (EXPECT_N pin %d, asserted)"
      % (len(ND), H.EXPECT_N))
# load_matrix re-reads the file, so its records are DIFFERENT objects; re-select from R by the
# emitter's own record key so `NEW[id(r)]` stays valid.
_ndkeys = {'%s|%s|%s' % (r['key'], r['type'], r['year']) for r in ND}
ND = [r for r in R if '%s|%s|%s' % (r['key'], r['type'], r['year']) in _ndkeys]
assert len(ND) == H.EXPECT_N, "re-selection lost rows: %d != %d" % (len(ND), H.EXPECT_N)
for gname, filt in [('ALL picks 1-64', lambda r: True),
                    ('picks 1-20', lambda r: 1 <= r['pick'] <= 20),
                    ('picks 21-64', lambda r: 21 <= r['pick'] <= 64)]:
    sub = [r for r in ND if filt(r)]
    yr = {}
    for N in range(0, 8):
        reached = [r for r in sub if r['year'] + N <= WINDOW_END]
        vals = [t338_value(r, N)[0] for r in reached]
        v0s = [float(NEW[id(r)]) for r in reached]
        yr[N] = (statistics.mean(vals) / statistics.mean(v0s)) if vals else float('nan')
    a = yr[1] - 1.0; m = CHARGE - a
    print("%-16s n=%4d  yr1 %.4f  apprec %+.2f%%  margin %+.2f%%  %s"
          % (gname, len(sub), yr[1], 100 * a, 100 * m, 'ARB' if m < 0 else 'no arb'))
    OUT[gname] = dict(n=len(sub), yr={str(k): round(v, 4) for k, v in yr.items()},
                      apprec=a, margin=m, verdict='ARB' if m < 0 else 'no arb')

narb = sum(1 for k, v in OUT.items() if v.get('verdict') == 'ARB')
print("PREDICTED ARBITRAGES: %d of %d primary readings" % (narb, len(OUT)))
json.dump(dict(basis='LANDED-LAW year-0 (ORDER 29C)', matrix=os.path.basename(MATRIX),
               window_end=WINDOW_END, charge=CHARGE, n_arb=narb, readings=OUT),
          open(OUTJ, 'w'), indent=1)
print("wrote %s" % OUTJ)
