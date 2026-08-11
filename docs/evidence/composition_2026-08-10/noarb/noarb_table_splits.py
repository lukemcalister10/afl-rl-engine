"""noarb_table_splits.py — THE SPLIT COHORT TABLES (owner spec, #334 ORDER 8).

  "Can we issue the no arb table using the following splits: ND picks 1-64 . Pool, split into Rookie,
   and non rookie . Separated. Year 0, 1, 2, 3, 4, 5, 6 total cohort values (across all time, not just
   the current board) . Then combined. And then ... reissue that data but of the sample of cohorts
   2012 and onwards ONLY."                                                            -- the owner

A SIBLING of noarb_table_allarm.py, which is itself a sibling of noarb_table_338.py. THE CANONICAL
INSTRUMENT IS NOT MODIFIED: its md5 is asserted at every run. No new emit — the stored matrices already
carry every row and every year, so this is a re-read of the SAME engine runs.

SPLITS (the engine's own _pool/type fields, never a re-invented rule):
  (a) ND 1-64        type ND, 1 <= pick <= 64, not is_pool
  (b) Pool-Rookie    type RD
  (c) Pool-non-rookie  every other is_pool row: SSP MSD PDA PDN PDS IRE UNR, AND ND picks > 64.
      ND>64 sits here because under the ruled July-28 pricing split it collapses to the single pool
      index and is priced off its signed division level, not off the pick curve. Its count is PRINTED.

BOTH totals and ratios are given for every cell, with n. A total moves when either prices or the
population move; a ratio divides one by the other. Reading only one of them is how a pool column whose
numerator AND denominator both fell can look unmoved.
"""
import os, sys, json, hashlib, statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CANON_MD5 = '0f8220351c64c56ccfa90c60edcdfa5f'
_m = hashlib.md5(open(os.path.join(HERE, 'noarb_table_338.py'), 'rb').read()).hexdigest()
assert _m == CANON_MD5, "canonical instrument md5 moved: %s" % _m

YEARS = list(range(0, 7))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
BASES = [('main', SP + '/per_entrant_main.json'), ('FULL', SP + '/per_entrant_FULL.json')]
WINDOWS = [('ALL-TIME cohorts', None), ('COHORTS 2012+', 2012)]


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def split_of(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'):
        return 'ND 1-64'
    if t == 'RD':
        return 'Pool-Rookie'
    return 'Pool-non-rookie'


def value_at(r, N, WEND):
    if N == 0:
        return float(r['v0']), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0, 'ended'
    if Y < yrs[0]: return None, 'pre'
    if Y > yrs[-1]: return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


L = []
def P(s=''):
    print(s); L.append(s)

OUT = {}
P("=" * 118)
P("THE SPLIT COHORT TABLES — ND 1-64 vs POOL-ROOKIE vs POOL-NON-ROOKIE, separated then combined")
P("=" * 118)
P("  OWNER SPEC (#334 ORDER 8). Cohort = every player drafted through mechanisms eligible to debut in")
P("  the same year: draft year + 1, except MSD = draft year (the engine's own debutyr convention).")
P("  instrument : noarb_table_splits.py, sibling of noarb_table_allarm.py. noarb_table_338.py NOT")
P("               modified, md5 %s asserted at run." % CANON_MD5)
P("  year 0     : each entrant's OWN v0 under that base. TOTALS are Sigma price over the included set.")
P("  disclosure : MSD rows have no cohort year 1 in the matrix (an MSD debuts in his DRAFT year but the")
P("               emitter builds yrs from draft year + 1). They are EXCLUDED from year 1, never scored")
P("               zero, and the excluded count is the n_pre column.")
P()

for bname, path in BASES:
    D = json.load(open(path)); R = D['recs']; meta = D['meta']
    WEND = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    nd64plus = [r for r in elig if r.get('type') == 'ND' and r.get('pick') and r['pick'] > 64]
    ndpool = [r for r in elig if r.get('type') == 'ND' and r.get('is_pool')]
    for wname, lo in WINDOWS:
        pop = [r for r in elig if lo is None or cohort(r) >= lo]
        groups = [('ND 1-64', [r for r in pop if split_of(r) == 'ND 1-64']),
                  ('Pool-Rookie', [r for r in pop if split_of(r) == 'Pool-Rookie']),
                  ('Pool-non-rookie', [r for r in pop if split_of(r) == 'Pool-non-rookie']),
                  ('COMBINED', pop)]
        P("=" * 118)
        P("### BASE %s   |   %s   |   n = %d   |   store %s   window end %d"
          % (bname, wname, len(pop), meta['store_md5'][:8], WEND))
        P("=" * 118)
        arms = Counter(r['type'] for r in pop)
        P("  arms in window: " + "  ".join("%s %d" % (t, n) for t, n in sorted(arms.items(), key=lambda x: -x[1])))
        P("  ND picks > 64 in window (placed in Pool-non-rookie): %d   |  ND rows the engine types as pool: %d"
          % (len([r for r in nd64plus if r in pop]), len([r for r in ndpool if r in pop])))
        P()
        for gname, sub in groups:
            if not sub:
                P("  --- %s: EMPTY IN THIS WINDOW ---" % gname); P(); continue
            P("  --- %s   n = %d ---" % (gname, len(sub)))
            P("      %-4s %7s %7s %8s %16s %16s %9s" %
              ("yrN", "n", "n_zero", "n_pre", "TOTAL yr N", "TOTAL yr 0", "ratio"))
            rows = []
            for N in YEARS:
                reached = sub if N == 0 else [r for r in sub if cohort(r) + N - 1 <= WEND]
                vals, v0s, npre = [], [], 0
                for r in reached:
                    v, k = value_at(r, N, WEND)
                    if k == 'pre':
                        npre += 1; continue
                    vals.append(v); v0s.append(float(r['v0']))
                sN, s0 = sum(vals), sum(v0s)
                ratio = (sN / s0) if s0 else float('nan')
                nz = sum(1 for v in vals if v == 0.0)
                P("      %-4d %7d %7d %8d %16s %16s %9.4f"
                  % (N, len(vals), nz, npre, format(round(sN), ','), format(round(s0), ','), ratio))
                rows.append(dict(N=N, n=len(vals), n_zero=nz, n_pre=npre,
                                 total_yearN=round(sN, 1), total_year0=round(s0, 1),
                                 ratio_sum_over_sum=round(ratio, 4)))
            P()
            OUT.setdefault(bname, {}).setdefault(wname, {})[gname] = dict(n=len(sub), rows=rows)

# H8.5 — the P7.3 effect, per split: does the year-0 denominator itself move main -> FULL?
P("=" * 118)
P("### H8.5 — DOES THE YEAR-0 DENOMINATOR ITSELF MOVE?  (Sigma v0 per split, main vs FULL)")
P("=" * 118)
P("  This is why totals are printed beside ratios. A pool ratio that looks unmoved can be a numerator")
P("  AND a denominator that both fell.")
Dm = {r['key']: r for r in json.load(open(BASES[0][1]))['recs']}
Df = {r['key']: r for r in json.load(open(BASES[1][1]))['recs']}
for wname, lo in WINDOWS:
    P("  --- %s ---" % wname)
    P("      %-18s %6s %16s %16s %10s" % ("split", "n", "Sigma v0 main", "Sigma v0 FULL", "move"))
    for g in ('ND 1-64', 'Pool-Rookie', 'Pool-non-rookie', 'COMBINED'):
        keys = [k for k, r in Df.items()
                if cohort(r) is not None and (r.get('v0') or 0) > 0
                and (lo is None or cohort(r) >= lo)
                and (g == 'COMBINED' or split_of(r) == g) and k in Dm]
        a = sum(Dm[k]['v0'] for k in keys); b = sum(Df[k]['v0'] for k in keys)
        P("      %-18s %6d %16s %16s %9.2f%%"
          % (g, len(keys), format(round(a), ','), format(round(b), ','), 100 * (b / a - 1) if a else 0))
    P()

json.dump(OUT, open(os.path.join(HERE, 'SPLIT_TABLES.json'), 'w'), indent=1)
open(os.path.join(HERE, 'SPLIT_TABLES.txt'), 'w').write('\n'.join(L) + '\n')
