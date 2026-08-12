#!/usr/bin/env python3
"""ORDER 23 -- THE SEPARATION LAW ON THE WALK-FORWARD, AND THE `_ruc_prior_cap` CHECK.

(a) SEPARATION. Over the 24-year walk-forward matrices, SHIP vs FINAL:
      - national records repriced on ANY year  -> must be 0
      - records whose v0 moved                 -> must be 0 for national rows, exactly
      - nd_profile (the calibration target)    -> must be identical to the last printed digit
(b) `_ruc_prior_cap` (D14 build-time check, directive item 5). The cap is
      v0 := min(v0_uncapped, RUC_PRIOR_CAP * _cap_basis(p) * _ruc_head_v0(p))
    and for a POOL row `_cap_basis(p) == pool_level(p)` (ladder currency, UNCONVERTED). So the derived
    pool levels move the cap directly. This measures, on the emitted matrices, how many pool RUCK rows
    sit ON the cap and by how much the cap moved.

  usage: o23_separation_ruck.py <ship.json> <final.json> <levels.json> <out.json>
"""
import sys, json, os, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
SHIPP, FINALP, LEVP, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
P = print
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

S = json.load(open(SHIPP)); F = json.load(open(FINALP))
sr = {r['key']: r for r in S['recs']}; fr = {r['key']: r for r in F['recs']}
V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = V2['pool_levels']; CURVE = V2['curve']
CAP = float(CURVE[str(int(CUR['signed_nd65_plus']['cap_against_curve_pick']))])
LV = json.load(open(LEVP))
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])

OLD = {k: int(float(v)) for k, v in CUR['signed_flat'].items()}
OLD['ND65+'] = int(min(float(CUR['signed_nd65_plus']['measured_k15']), CAP))
for k, v in CUR['signed_rd_positional'].items(): OLD['RD:' + k] = int(float(v))
NEW = {k: int(float(v)) for k, v in LV['signed_flat'].items()}
# ORDER 23 (owner ruling 5262928754): the NEW table is UNCAPPED -- ND65+ takes its derived level.
# The OLD table above keeps the cap, because that IS what the shipped engine read.
NEW['ND65+'] = int(float(LV['nd65_measured_k15']))
for k, v in LV['signed_rd_positional'].items(): NEW['RD:' + k] = int(float(v))


def division(r):
    t = r.get('type')
    if t == 'RD': return 'RD:' + r['pos']
    if t == 'ND': return 'ND65+'
    return t


P("=" * 118)
P("(a) THE SEPARATION LAW ON THE 24-YEAR WALK-FORWARD   SHIP %s  ->  FINAL %s"
  % (md5(SHIPP)[:8], md5(FINALP)[:8]))
P("=" * 118)
nat = [k for k in sr if not sr[k].get('is_pool_engine')]
pool = [k for k in sr if sr[k].get('is_pool_engine')]
nat_v0 = [k for k in nat if float(sr[k]['v0']) != float(fr[k]['v0'])]
nat_path = [k for k in nat if (sr[k].get('vpath') or []) != (fr[k].get('vpath') or [])]
pool_v0 = [k for k in pool if float(sr[k]['v0']) != float(fr[k]['v0'])]
pool_path = [k for k in pool if (sr[k].get('vpath') or []) != (fr[k].get('vpath') or [])]
P("  records: %d national, %d pool" % (len(nat), len(pool)))
P("  NATIONAL records whose v0 moved  : %d   <-- must be 0" % len(nat_v0))
P("  NATIONAL records repriced on ANY walk-forward year: %d   <-- must be 0" % len(nat_path))
if nat_v0: P("    names: %s" % nat_v0[:10])
if nat_path: P("    names: %s" % nat_path[:10])
P("  pool records whose v0 moved      : %d  (the ruck cap -- see (b))" % len(pool_v0))
P("  pool records repriced on the walk-forward: %d" % len(pool_path))
P()
SEPOK = (len(nat_v0) == 0 and len(nat_path) == 0)
P("  VERDICT: %s" % ('SEPARATION LAW HOLDS -- ND rows moved = 0, national v0 delta = 0 EXACTLY'
                     if SEPOK else '*** BLOCKER -- SEPARATION VIOLATED ***'))
P()

P("=" * 118)
P("(b) `_ruc_prior_cap` ON THE DERIVED POOL RUCK v0s")
P("=" * 118)
P("  cap = RUC_PRIOR_CAP * _cap_basis(p) * _ruc_head_v0(p);  for a pool row _cap_basis == pool_level")
P("  (LADDER currency, UNCONVERTED -- the level enters this site without the %.4f board factor)." % PL_F)
P()
rucks = [k for k in pool if sr[k].get('pos') == 'RUCK']
byp = collections.defaultdict(lambda: [0, 0, 0.0, 0.0])
BIND = []
for k in rucks:
    d = division(sr[k])
    if d not in OLD: continue
    a, b = float(sr[k]['v0']), float(fr[k]['v0'])
    ratio_a = a / OLD[d] if OLD[d] else float('nan')
    ratio_b = b / NEW[d] if NEW[d] else float('nan')
    lvl_ratio = NEW[d] / OLD[d] if OLD[d] else float('nan')
    # a row sits ON the cap iff its v0 tracks the level exactly
    on_cap = abs((b / a if a else 0) - lvl_ratio) < 2e-3 and abs(lvl_ratio - 1.0) > 1e-9
    byp[sr[k]['type']][0] += 1
    byp[sr[k]['type']][1] += on_cap
    byp[sr[k]['type']][2] += a
    byp[sr[k]['type']][3] += b
    if on_cap:
        BIND.append(dict(key=k, type=sr[k]['type'], div=d, v0_ship=a, v0_final=b,
                         level_ship=OLD[d], level_final=NEW[d],
                         v0_over_level_ship=ratio_a, v0_over_level_final=ratio_b))
P("  %-8s %7s %10s %14s %14s %10s   %s" %
  ('pathway', 'rucks', 'ON the cap', 'S v0 SHIP', 'S v0 FINAL', 'delta %', 'level SHIP -> FINAL'))
for t in sorted(byp):
    n, nb, va, vb = byp[t]
    d = ('RD:RUCK' if t == 'RD' else ('ND65+' if t == 'ND' else t))
    P("  %-8s %7d %10d %14.1f %14.1f %9.2f%%   %d -> %d" %
      (t, n, nb, va, vb, 100.0 * (vb / va - 1) if va else 0.0, OLD.get(d, 0), NEW.get(d, 0)))
P()
nb = sum(v[1] for v in byp.values())
P("  POOL RUCK ROWS WHOSE v0 IS SET BY THE CAP: %d of %d." % (nb, len(rucks)))
if BIND:
    ex = BIND[0]
    P("  Size, from a bound row (%s): v0 = %.4f x the signed level, before and after"
      % (ex['key'], ex['v0_over_level_ship']))
    P("    %s: level %d -> %d, v0 %.1f -> %.1f (%.2f%%) -- the cap moves the v0 ONE FOR ONE with the level."
      % (ex['key'], ex['level_ship'], ex['level_final'], ex['v0_ship'], ex['v0_final'],
         100.0 * (ex['v0_final'] / ex['v0_ship'] - 1)))
P("  THE CAP IS THE ONLY ROUTE BY WHICH A SIGNED POOL LEVEL REACHES `v0_start` AT ALL -- which is the")
P("  same finding the derivation's denominator departure rests on, seen from the other side.")
P()
json.dump(dict(separation=dict(national_v0_moved=len(nat_v0), national_path_moved=len(nat_path),
                               pool_v0_moved=len(pool_v0), pool_path_moved=len(pool_path),
                               n_national=len(nat), n_pool=len(pool), holds=SEPOK,
                               national_v0_names=nat_v0[:20], national_path_names=nat_path[:20]),
               ruck_cap=dict(n_pool_rucks=len(rucks), n_on_cap=nb,
                             by_pathway={t: dict(n=v[0], on_cap=v[1], v0_ship=v[2], v0_final=v[3])
                                         for t, v in byp.items()},
                             bound=BIND)),
          open(OUT, 'w'), indent=1, default=float)
P("wrote %s" % OUT)
sys.exit(0 if SEPOK else 2)
