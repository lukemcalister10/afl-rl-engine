import os, sys, io, json, contextlib, statistics
STAGE = os.environ['STAGE']; ROOT = os.environ['RL_REPO']
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; day0_v0 = G['day0_v0']; _PL_F = G['_PL_F']
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

# 1. the 89 wired entrants the emitter's proof checks
D0 = json.load(open(ROOT + '/docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json'))
BYK = {p['key']: p for p in MA.data if p.get('key')}
mis = []
for r in D0['rows']:
    p = BYK.get(r['key'])
    cur = None if p is None else day0_v0(p)
    if cur is None: continue
    mis.append((r['key'], r['derived_v0'], cur, cur / r['derived_v0'] - 1.0))
bad = [m for m in mis if abs(m[1] - m[2]) > 1e-9]
print('THE 89 WIRED ENTRANTS (the emitter proof population)')
print('  reproduce exactly : %d of %d' % (len(mis) - len(bad), len(mis)))
if bad:
    rs = sorted(m[3] for m in bad)
    print('  moved             : %d   ratio min %+.3f%%  median %+.3f%%  max %+.3f%%'
          % (len(bad), 100 * rs[0], 100 * statistics.median(rs), 100 * rs[-1]))
    print('  mean |move|       : %.3f%%' % (100 * statistics.mean(abs(x) for x in rs)))

# 2. THE POPULATION THAT ACTUALLY SETS THE DENOMINATOR: the emitted matrix's v0 column, 2648 records
MX = json.load(open(SP + '/per_entrant_O29CFINAL.json'))
recs = MX['recs']
if isinstance(recs, dict): recs = list(recs.values())
print('\nTHE EMIT POPULATION (per_entrant_O29CFINAL.json, the 29C landed-law basis)')
print('  records: %d' % len(recs))
old, new = [], []
nmiss = 0
for rec in recs:
    k = rec.get('key')
    p = BYK.get(k)
    if p is None: nmiss += 1; continue
    try: cur = day0_v0(p)
    except Exception: cur = None
    if cur is None or not rec.get('v0'): continue
    old.append(float(rec['v0'])); new.append(cur * _PL_F)
print('  comparable rows   : %d   (unmapped %d)' % (len(old), nmiss))
if old:
    so, sn = sum(old), sum(new)
    print('  mean v0 OLD (29C basis)      : %.2f' % (so / len(old)))
    print('  mean v0 NEW (Step-1 re-fit)  : %.2f' % (sn / len(new)))
    print('  DENOMINATOR MOVE             : %+.3f%%' % (100 * (sn / so - 1)))
    moved = sum(1 for a, b in zip(old, new) if abs(a - b) > 0.05)
    print('  rows whose v0 moved          : %d of %d (%.1f%%)' % (moved, len(old), 100.0 * moved / len(old)))
    rr = sorted(b / a - 1.0 for a, b in zip(old, new) if a)
    print('  per-row move  p05 %+.2f%%  median %+.2f%%  p95 %+.2f%%'
          % (100 * rr[int(.05 * len(rr))], 100 * rr[len(rr) // 2], 100 * rr[int(.95 * len(rr))]))
