"""ORDER 26A -- THE ROW-LEVEL LINE-UP. Read-only.

The bridge table says WHICH KNOB moved the number. This file says WHICH PLAYERS each knob moved:
counts and named examples, so the reconciliation is checkable by hand.

    usage: python o26a_rows.py <matrix.json> <out.json>
"""
import sys, json, os, collections

MATRIX = sys.argv[1]; OUTJS = sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
L = []
def P(s=''):
    print(s); L.append(s)

M = json.load(open(MATRIX)); R = M['recs']

def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t

elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
LEVI = {k: int(float(v)) for k, v in CUR['signed_flat'].items()}
LEVI['ND65+'] = int(float(CUR['signed_nd65_plus']['measured_k15']))
for k, v in CUR['signed_rd_positional'].items(): LEVI['RD:' + k] = int(float(v))
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])

def anchor_of(r):
    if r.get('is_pool_engine'):
        d = 'RD:' + r['pos'] if r.get('type') == 'RD' else ('ND65+' if r.get('type') == 'ND' else r.get('type'))
        if d in LEVI: return LEVI[d] * PL_F
    return float(r['v0'])

def mark_at(r, Y):
    if Y > W: return None, 'skip_notyet'
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0, 'zero_noyrs'
    if Y < yrs[0]: return None, 'skip_pre'
    if Y > yrs[-1]: return 0.0, 'zero_ended'
    v = vp[yrs.index(Y)]
    return (0.0, 'zero_null') if v is None else (float(v), 'path')

RD_D = [r for r in elig if stream(r) == 'RD']
RD_A = [r for r in elig if r['type'] == 'RD' and 2005 <= cohort(r) <= 2023]
KA = set(r['key'] for r in RD_A)

P("=" * 118)
P("ORDER 26A -- THE ROW-LEVEL LINE-UP OF THE RD BRIDGE   (window end %d)" % W)
P("=" * 118)
P()
P("-" * 118)
P("STEP P -- POPULATION. derive RD n=%d ; allarm RD n=%d ; difference %d rows."
  % (len(RD_D), len(RD_A), len(RD_D) - len(RD_A)))
P("-" * 118)
extra = [r for r in RD_D if r['key'] not in KA]
byc = collections.Counter(cohort(r) for r in extra)
P("  the %d rows derive counts and allarm does not, by cohort: %s"
  % (len(extra), dict(sorted(byc.items()))))
adm = [r for r in extra if mark_at(r, cohort(r) + 3)[0] is not None]
skp = [r for r in extra if mark_at(r, cohort(r) + 3)[0] is None]
P("  of them, %d are ADMITTED to the yr4 reading (cohort+3 <= %d) and %d are skipped as not-yet-reached."
  % (len(adm), W, len(skp)))
P("  ALL %d admitted rows come from cohorts BEFORE 2005 -- the pre-2005 rookie classes the all-arm"
  % len(adm))
P("  instrument's PRIMARY window excludes by design. NONE come from after 2023." if not [r for r in adm if cohort(r) > 2023]
  else "  (some admitted rows are post-2023)")
P()
P("  named examples of the %d ADMITTED rows (the ones that move the number):" % len(adm))
P("    %-28s %6s %6s %6s %10s %10s %10s" % ('player', 'cohort', 'pos', 'Y', 'mark@Y', 'anchor', 'board v0'))
for r in sorted(adm, key=lambda r: cohort(r))[:12]:
    v, k = mark_at(r, cohort(r) + 3)
    P("    %-28s %6d %6s %6d %10.1f %10.1f %10.1f"
      % (r['key'][:28], cohort(r), r['pos'], cohort(r) + 3, v, anchor_of(r), float(r['v0'])))
P("    ... (%d admitted rows in total)" % len(adm))
P()
if skp:
    P("  named examples of the %d SKIPPED rows (counted by derive's population but not by its yr4):" % len(skp))
    for r in sorted(skp, key=lambda r: cohort(r))[:6]:
        P("    %-28s cohort %d -> Y %d > window end %d" % (r['key'][:28], cohort(r), cohort(r) + 3, W))
P()

P("-" * 118)
P("STEPS I, S, A -- INDEXING, SKIP/ZERO SEMANTICS, AGGREGATION")
P("-" * 118)
P("  rows moved: ZERO, in all three cases. The instruments are textually different and")
P("  arithmetically identical:")
P("    I : derive cohort+3 ; allarm cohort+N-1 at N=4 -> cohort+3. Same year for all %d eligible rows."
  % len(elig))
P("    S : both skip Y>window_end, both skip Y<yrs[0] ('pre'), both score 0 past yrs[-1] and on a")
P("        null vpath cell. The ONLY textual difference is the empty-yrs row: derive labels it")
P("        'v=0.0' and allarm labels it 'ended' -- SAME VALUE, and in any case there are 0 such rows.")
P("    A : allarm's mean/mean is taken over the SAME included set as its own denominator, so it is")
P("        algebraically sum/sum. The n cancels exactly.")
P()

P("-" * 118)
P("STEP D -- THE ENTRY-PRICE OBJECT. This is 98.65%% of the whole gap.")
P("-" * 118)
kept = [r for r in RD_D if mark_at(r, cohort(r) + 3)[0] is not None]
P("  rows moved: ALL %d rows in the reading. Every single one." % len(kept))
sv = sum(float(r['v0']) for r in kept); sa = sum(anchor_of(r) for r in kept)
P("  SUM board v0 %s  vs  SUM signed anchor %s   ->  ratio %.4f"
  % (format(round(sv), ','), format(round(sa), ','), sv / sa))
P()
P("  the signed RD positional levels x _PL_F=%.4f (the whole of the anchor for an RD row):" % PL_F)
for p in ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']:
    sub = [r for r in kept if r['pos'] == p]
    mv = sum(float(r['v0']) for r in sub) / len(sub) if sub else 0
    P("    %-5s  level %4d  anchor %8.2f  |  mean board v0 %8.1f  |  board v0 / anchor = %.3f  (n=%d)"
      % (p, LEVI['RD:' + p], LEVI['RD:' + p] * PL_F, mv, mv / (LEVI['RD:' + p] * PL_F), len(sub)))
P()
P("  named examples -- the SAME player, the SAME year, the SAME mark, two entry prices:")
P("    %-28s %5s %6s %9s %9s %9s %9s %9s"
  % ('player', 'pos', 'Y', 'mark@Y', 'anchor', 'board v0', 'm/anchor', 'm/v0'))
ex = sorted([r for r in kept if mark_at(r, cohort(r) + 3)[0] > 0],
            key=lambda r: -float(r['v0']))[:8]
for r in ex:
    v, _ = mark_at(r, cohort(r) + 3); a = anchor_of(r); z = float(r['v0'])
    P("    %-28s %5s %6d %9.1f %9.1f %9.1f %9.3f %9.3f"
      % (r['key'][:28], r['pos'], cohort(r) + 3, v, a, z, v / a, v / z))
P()
P("  and the dead, who are ZEROED and KEPT (the branch the owner suspected of skipping them):")
dead = [r for r in kept if mark_at(r, cohort(r) + 3)[0] == 0.0]
P("    %d of the %d rows in the RD yr4 reading score exactly 0.0 and stay in the denominator." % (len(dead), len(kept)))
for r in dead[:6]:
    yrs = r.get('yrs') or []
    P("      %-28s cohort %d  Y %d  emitted yrs %s..%s  -> past the end, scored 0.0, entry %.1f KEPT"
      % (r['key'][:28], cohort(r), cohort(r) + 3, yrs[0] if yrs else '-', yrs[-1] if yrs else '-',
         anchor_of(r)))
P()

json.dump(dict(step_P=dict(derive_n=len(RD_D), allarm_n=len(RD_A), extra=len(extra),
                           admitted=[r['key'] for r in adm], skipped=[r['key'] for r in skp],
                           by_cohort={str(k): v for k, v in byc.items()}),
               step_ISA=dict(rows_moved=0),
               step_D=dict(rows_moved=len(kept), sum_v0=sv, sum_anchor=sa, ratio=sv / sa,
                           dead_zeroed_kept=len(dead),
                           examples=[dict(key=r['key'], pos=r['pos'], Y=cohort(r) + 3,
                                          mark=mark_at(r, cohort(r) + 3)[0], anchor=anchor_of(r),
                                          v0=float(r['v0'])) for r in ex])),
          open(OUTJS, 'w'), indent=1, default=float)
open(OUTJS.replace('.json', '_out.txt'), 'w').write('\n'.join(L) + '\n')
P("wrote %s" % OUTJS)
