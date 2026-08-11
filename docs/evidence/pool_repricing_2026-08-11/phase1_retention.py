"""TASK 5 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY.

RULED (D8, owner comment 5253173347), verbatim:
  "the pool sitter on top penalty should go, and the pool index should be rederived in the same way
   the ND one is where possible not for pick 65, but for the pool."
  "I imagine the ND sitter was derived from historical data, just like the pool sitter could be."

WHAT RETIRES:  H_POOLSIT = 0.804  and  H_UNION = 0.280   (_merged_recover.py:2018-2019)
WHAT REPLACES IT: one measured retention per pool class x depth, derived on POOL history, STANDING IN
PLACE OF the current read -- not multiplying on top of it.

THE METHOD IS THE NATIONAL ONE, carried across deliberately (d13_norm_harvest.py + d13_derive.py):
    norm(d)   = E[ winsor(O/V0, 2.0) | still-listed, depth d ]      the developer-inclusive same-depth
                                                                    benchmark that strips survivor selection
    r_sit(d)  = E[ winsor(O/V0, 2.0) | SIT-OUT subset, depth d ]
    R(d)      = clip( r_sit(d) / norm(d), 0.05, 1.0 )
    then ISOTONIC NON-INCREASING IN DEPTH  (the owner's signed law: a sitter never gains value by sitting)

ONE DELIBERATE DEPARTURE, DECLARED RATHER THAN SLIPPED IN. d13 used v0_start(p) as the denominator for
every row. v0_start is the NATIONAL v0 curve, and a pool entrant is NOT priced off it -- he is priced
off entry_anchor(p) = pool_level(p) * _PL_F * _b_factor(p) (_merged_recover.py:1856). Using v0_start
for a pool row would measure retention against a price that row never had. BOTH denominators are
computed and BOTH are reported, so the choice is visible and challengeable rather than assumed.

THERE IS NO PICK AXIS. d13's surface is pick-conditioned; effpk returns the constant POOL_PICK=65 for
every pool entrant, so a pick-conditioned pool surface would be a fabricated dimension. The pool object
is keyed on CLASS x DEPTH, and on PATHWAY x DEPTH where samples permit.

THE MEAN-PRESERVING LAW (owner amendment, D8) is CHECKED here rather than asserted: once a pathway's
entry price is calibrated to that pathway's own realized returns -- sitters included -- any
within-pathway sitter differential must be a REDISTRIBUTION, never a net charge. The uplift the
non-sitters must carry is computed and printed per pathway.

Loads the engine READ-ONLY from a staged copy so the repo is untouched. No emits. Deterministic.
"""
import os, sys, io, json, contextlib, math, collections

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng_stage/rl_after'
HERE = os.path.dirname(os.path.abspath(__file__))

os.environ.update(PYTHONHASHSEED='0')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)

MA, cp = G['MA'], G['cp']
price6 = G['price6']
v0_start, entry_anchor, _sitout_cls = G['v0_start'], G['entry_anchor'], G['_sitout_cls']
H_POOLSIT, H_UNION = G['H_POOLSIT'], G['H_UNION']
_R_surf, _b_age = G['_R_surf'], G['_b_age']

P = print
P("=" * 118)
P("TASK 5 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY")
P("=" * 118)
P("  engine loaded read-only from a staged copy; repo untouched.  MA.data n=%d" % len(MA.data))
P("  retiring: H_POOLSIT=%.3f  H_UNION=%.3f   (composed today: %.4f, and %.4f inside the union cell)"
  % (H_POOLSIT, H_UNION, H_POOLSIT, H_POOLSIT * H_UNION))
P()


def draftyr(p): return cp.debutyr(p) - 1


def min_window(p):
    t, pk = p.get('type'), p.get('pick')
    if t == 'ND' and pk and pk <= 20: return 4
    if t == 'ND' and pk and pk <= 40: return 3
    return 2


def listed_through(p):
    if p.get('_last_listed') is not None: return int(p['_last_listed'])
    if not p.get('_retired'): return 2026
    lg = max((x['year'] for x in p['scoring']), default=0)
    dy = p.get('year') or lg
    return max(dy + min_window(p) - 1, lg)


def outcomeO(p, Y):
    """d13's forward outcome, WITH ONE FORCED DEPARTURE THE SEAT DID NOT CHOOSE.

    d13 read  L = max(avg * REF / era[year]).  ERA NORMALIZATION NO LONGER EXISTS: it was removed by
    owner ruling in the #334 stage B salvage (ballot word 1, comment 5242713366) -- "SuperCoach scores
    are era-comparable BY CONSTRUCTION... NO era normalization may be applied to scoring anywhere...
    Do not reintroduce." (_merged_recover.py:51-57).

    So the national method CANNOT be replayed verbatim: one of its terms is now forbidden. Season
    averages are read RAW, which is the current engine's own convention. This is recorded as a limit
    on the phrase "the same way the ND one is" rather than silently absorbed.
    """
    fwd = [x for x in p['scoring'] if x['games'] >= 6 and Y < x['year'] <= Y + 4]
    if not fwd: return 0.0
    L = max(x['avg'] for x in fwd)
    with contextlib.redirect_stdout(io.StringIO()):
        return price6(p, [L] * 6, Y)


def wins(x, cap=2.0): return min(max(x, 0.0), cap)


def stream(p):
    t = p.get('type')
    if t == 'ND':
        pk = p.get('pick') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


# ------------------------------------------------------------------ harvest
cells = []
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue
        dy = draftyr(p)
        if dy < 2003 or dy > 2024: continue
        lt = listed_through(p)
        rows = sorted(p['scoring'], key=lambda x: x['year'])
        pos = MA.gfut(p)
        cls = _sitout_cls(pos)
        va = float(v0_start(p))
        try:
            ea = float(entry_anchor(p))
        except Exception:
            ea = float('nan')
        for Y in range(dy + 1, min(lt, 2025) + 1):
            quals = [x for x in rows if x['games'] >= 6 and x['year'] <= Y]
            cells.append(dict(pool=bool(p.get('_pool')), stream=stream(p), cls=cls, pos=pos,
                              d=Y - dy, sitout=bool(not quals), O=outcomeO(p, Y),
                              V0start=va, Vanchor=ea, wc=bool(Y <= 2021),
                              age=_b_age(p), typ=p.get('type')))

POOL = [c for c in cells if c['pool'] and c['wc']]
NDC = [c for c in cells if not c['pool'] and c['wc']]
P("  harvested cells (complete-window, Y<=2021):  pool %d   national %d" % (len(POOL), len(NDC)))
P("  pool sit-out cells: %d of %d (%.1f%%)"
  % (sum(1 for c in POOL if c['sitout']), len(POOL),
     100.0 * sum(1 for c in POOL if c['sitout']) / len(POOL)))
P()

DEPTHS = list(range(1, 7))


def ratio(c, den):
    v = c['Vanchor'] if den == 'anchor' else c['V0start']
    if not v or v != v or v <= 0: return None
    return wins(c['O'] / v)


def isotonic_noninc(vals):
    out = list(vals)
    for i in range(1, len(out)):
        if out[i] is not None and out[i - 1] is not None and out[i] > out[i - 1]:
            out[i] = out[i - 1]
    return out


def derive(sub, den):
    """The d13 construction: r_sit/norm at each depth, clipped, then isotonic non-increasing."""
    raw, ns, nn = [], [], []
    for d in DEPTHS:
        at = [c for c in sub if c['d'] == d]
        nv = [ratio(c, den) for c in at]
        nv = [x for x in nv if x is not None]
        sv = [ratio(c, den) for c in at if c['sitout']]
        sv = [x for x in sv if x is not None]
        ns.append(len(sv)); nn.append(len(nv))
        if not nv or not sv:
            raw.append(None); continue
        norm = sum(nv) / len(nv)
        rs = sum(sv) / len(sv)
        raw.append(min(max(rs / norm, 0.05), 1.0) if norm > 0 else None)
    return isotonic_noninc(raw), ns, nn


# ------------------------------------------------------------------ the surface today
P("=" * 118)
P("WHAT THE POOL READS TODAY -- the national surface at the pool index, then the multiplier on top")
P("=" * 118)
P("  %-8s | %s" % ('class', "".join("%9s" % ("d%d" % d) for d in DEPTHS)))
P("  " + "-" * 114)
TODAY = {}
for cls in ('nonKPP', 'KPP', 'RUCK'):
    v = [_R_surf(cls, 65, float(d)) for d in DEPTHS]
    TODAY[cls] = v
    P("  %-8s | %s" % (cls, "".join("%9.4f" % x for x in v)))
P()
P("  composed with H_POOLSIT (%.3f), a pool non-KPP sitter at depth 1 takes %.4f x %.3f = %.4f;"
  % (H_POOLSIT, TODAY['nonKPP'][0], H_POOLSIT, TODAY['nonKPP'][0] * H_POOLSIT))
P("  inside the union cell a further x%.3f -> %.4f."
  % (H_UNION, TODAY['nonKPP'][0] * H_POOLSIT * H_UNION))
P()

# ------------------------------------------------------------------ derived, per class
P("=" * 118)
P("THE DERIVED POOL RETENTION -- by class x depth, on POOL history alone")
P("=" * 118)
DER = {}
for den, label in (('anchor', 'DENOMINATOR = entry_anchor  (what a pool row is ACTUALLY priced off)'),
                   ('v0start', "DENOMINATOR = v0_start      (what d13 used for every row)")):
    P()
    P("  %s" % label)
    P("  %-8s | %s | %s" % ('class', "".join("%9s" % ("d%d" % d) for d in DEPTHS),
                            "".join("%7s" % ("n%d" % d) for d in DEPTHS)))
    P("  " + "-" * 114)
    DER[den] = {}
    for cls in ('nonKPP', 'KPP', 'RUCK'):
        sub = [c for c in POOL if c['cls'] == cls]
        v, ns, nn = derive(sub, den)
        DER[den][cls] = v
        P("  %-8s | %s | %s" % (cls,
                                "".join("%9s" % ("%.4f" % x if x is not None else '-') for x in v),
                                "".join("%7d" % x for x in ns)))
    sub = POOL
    v, ns, nn = derive(sub, den)
    DER[den]['ALL'] = v
    P("  %-8s | %s | %s" % ('ALL POOL',
                            "".join("%9s" % ("%.4f" % x if x is not None else '-') for x in v),
                            "".join("%7d" % x for x in ns)))
P()

P("=" * 118)
P("THE COMPARISON THAT MATTERS -- derived pool retention vs what the pool takes today")
P("=" * 118)
P("  %-8s | %9s %9s %9s %9s | %9s" %
  ('class', 'today R', 'x H_POOL', 'x H_UNION', 'DERIVED', 'derived/composed'))
P("  " + "-" * 114)
for cls in ('nonKPP', 'KPP', 'RUCK'):
    t = TODAY[cls][0]
    d = DER['anchor'][cls][0]
    comp = t * H_POOLSIT
    P("  %-8s | %9.4f %9.4f %9.4f | %9s | %9s" %
      (cls, t, comp, comp * H_UNION,
       "%.4f" % d if d is not None else '-',
       "%.3fx" % (d / comp) if (d is not None and comp) else '-'))
P()
P("  (depth 1 shown; full depth profiles above)")
P()

# ------------------------------------------------------------------ per pathway
P("=" * 118)
P("PER PATHWAY x DEPTH, where the samples permit (n_sit >= 20 at that depth, else blank with count)")
P("=" * 118)
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
PATH = {}
P("  %-8s | %s | %s" % ('pathway', "".join("%9s" % ("d%d" % d) for d in DEPTHS),
                        "".join("%7s" % ("n%d" % d) for d in DEPTHS)))
P("  " + "-" * 114)
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    v, ns, nn = derive(sub, 'anchor')
    vv = [x if (x is not None and ns[i] >= 20) else None for i, x in enumerate(v)]
    PATH[s] = vv
    P("  %-8s | %s | %s" % (s,
                            "".join("%9s" % ("%.4f" % x if x is not None else '-') for x in vv),
                            "".join("%7d" % x for x in ns)))
P()
P("  Only the rookie draft carries enough sit-out cells to support its own per-depth curve at any")
P("  depth. Every other pathway is thin and takes the pool class curve, which is the same")
P("  borrowing discipline layer 2 uses -- disclosed, never forced.")
P()

# ------------------------------------------------------------------ the mean-preserving law
P("=" * 118)
P("THE MEAN-PRESERVING CHECK -- the owner's law, CHECKED rather than asserted")
P("=" * 118)
P()
P("  The law (D8 amendment): once a pathway's entry price is calibrated to that pathway's own")
P("  realized returns -- SITTERS INCLUDED -- any within-pathway sitter differential must be a")
P("  REDISTRIBUTION and never a net charge. So if sitters carry retention R < 1, the non-sitters of")
P("  that same pathway must carry an uplift U > 1 with the entry-weighted mean landing on 1.0000:")
P()
P("      U  =  ( SUM_all e  -  SUM_sitters e*R )  /  SUM_non-sitters e")
P()
P("  %-8s %8s %8s | %9s %9s | %9s %12s" %
  ('pathway', 'cells', 'sitters', 'sit share', 'mean R', 'UPLIFT U', 'net charge'))
P("  " + "-" * 114)
MP = {}
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    if not sub: continue
    tot = 0.0; sitw = 0.0; nonw = 0.0; num = 0.0; nsit = 0
    for c in sub:
        e = c['Vanchor']
        if not e or e != e or e <= 0: continue
        cls = c['cls']
        d = min(max(c['d'], 1), 6)
        Rv = DER['anchor'][cls][d - 1]
        if Rv is None: Rv = DER['anchor']['ALL'][d - 1]
        if Rv is None: continue
        tot += e
        if c['sitout']:
            sitw += e; num += e * Rv; nsit += 1
        else:
            nonw += e
    if tot <= 0 or nonw <= 0: continue
    U = (tot - num) / nonw
    meanR = num / sitw if sitw else float('nan')
    post = (num + nonw * U) / tot
    MP[s] = dict(U=U, meanR=meanR, sit_share=sitw / tot, post=post, n=len(sub), nsit=nsit)
    P("  %-8s %8d %8d | %9.4f %9.4f | %9.4f %12.10f" %
      (s, len(sub), nsit, sitw / tot, meanR, U, post))
P("  " + "-" * 114)
P("  The right-hand column is the entry-weighted mean AFTER the redistribution. It is 1.0000000000")
P("  by construction of U -- which is the point: the differential moves value BETWEEN sitters and")
P("  non-sitters of the same pathway and takes none out of the pathway.")
P()
P("  CONTRAST WITH WHAT SHIPS TODAY. H_POOLSIT/H_UNION multiply the sitter's finished price and give")
P("  nothing back to anyone: the pathway's entry-weighted mean falls BELOW 1.0, which is a NET CHARGE")
P("  and is exactly what the owner's amendment forbids once the pathway is calibrated. Measured:")
P()
P("  %-8s %9s %9s %12s" % ('pathway', 'today mean', 'net charge', 'vs law'))
P("  " + "-" * 114)
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    if not sub or s not in MP: continue
    tot = 0.0; num = 0.0
    for c in sub:
        e = c['Vanchor']
        if not e or e != e or e <= 0: continue
        tot += e
        if c['sitout']:
            f = H_POOLSIT
            if (c['age'] is not None and c['age'] >= 23.0) or c['typ'] in ('IRE', 'MSD'):
                f *= H_UNION
            num += e * f
        else:
            num += e
    P("  %-8s %9.4f %9.4f %12s" % (s, num / tot, num / tot - 1.0, 'BREACH' if num / tot < 0.9999 else 'ok'))
P()

out = dict(
    retiring=dict(H_POOLSIT=H_POOLSIT, H_UNION=H_UNION, composed_union=H_POOLSIT * H_UNION),
    today_surface_at_pool_index={k: v for k, v in TODAY.items()},
    derived_anchor=DER['anchor'], derived_v0start=DER['v0start'],
    per_pathway=PATH, mean_preserving={k: MP[k] for k in MP},
    n_pool_cells=len(POOL), n_pool_sitout=sum(1 for c in POOL if c['sitout']),
)
json.dump(out, open(os.path.join(HERE, 'PHASE1_RETENTION.json'), 'w'), indent=1, default=float)
P("wrote PHASE1_RETENTION.json")
