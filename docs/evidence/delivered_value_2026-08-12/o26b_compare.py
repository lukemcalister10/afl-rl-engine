#!/usr/bin/env python3
"""ORDER 26B -- STEP 5, THE COMPARISONS AND THE TWO NEW MANDATORY INSTRUMENTS.

  1. DERIVED v0 vs PRINTED DAY-0 vs SIGNED ANCHOR   (pool; per pathway x position; named rows)
  2. THE DERIVED CURVE vs TODAY'S PICK CURVE        (ND)
  3. THE MARK-PATH PROGRESSION TEST                 (new mandatory instrument)
  4. THE REVERSE NO-ARB TEST                        (new mandatory instrument)

THE TEST FORMS WERE STATED FIRST. `INSTRUMENTS_PRESTATEMENT.md` was committed and pushed in its own
commit BEFORE this file existed (commit c913dfd, 2026-08-12) -- the depth axis, the population rules,
the day-0 construction, both PASS predicates and the whole bootstrap specification. Nothing in this
file may deviate from it; where a reading is ambiguous, BOTH are printed.

EVERY DISTRIBUTIONAL CLAIM REPORTS p05 / median / p95. Binding law, from this order's own gate leg:
a board-wide median of 1.0044 sat on a distribution spanning 0.0904 to 4.2048.

CONVENTIONS ARE BORROWED, NOT INVENTED. The cohort key, the row semantics and the entry-price objects
are carried verbatim from docs/evidence/reconciliation_2026-08-12/o26a_bridge.py, which in turn
carried them verbatim from o25_derive.py and noarb_table_allarm.py and CONTROL-CHECKED them against
both instruments' published outputs.

READ-ONLY. Nothing under engine/ is written; no board is built; no pin is moved.

  usage:  python3 o26b_compare.py
"""
import os, sys, json, math, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
# THE MATRIX IS COPIED INTO THIS EVIDENCE TREE so the record is durable independently of the shared
# scratchpad -- the same discipline ORDER 26A applied to its own instruments. The scratchpad copy is
# preferred when present (it is the original), and BOTH are md5-asserted against the same pin, so the
# copy cannot silently drift from the object 26A measured.
MATRIX_MD5 = '3c6ffcdeaac9786473f3f017dba1d61e'
MATRIX = os.path.join(SP, 'per_entrant_O25R4.json')
if not os.path.exists(MATRIX):
    MATRIX = os.path.join(HERE, 'per_entrant_O25R4.json')
_LOCAL = os.path.join(HERE, 'per_entrant_O25R4.json')
L1P = os.path.join(ROOT, 'data', 'delivered_value', 'layer1_player_seasons.json')


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


for lbl, path, exp in [('matrix', MATRIX, MATRIX_MD5),
                       ('layer1', L1P, 'ad1229ea6f443538479447132382b21c'),
                       ('store', os.path.join(ROOT, 'engine/rl_after/rl_model_data.json'),
                        'd9a24282357cf3083b1640466e3ecd83'),
                       ('board', os.path.join(ROOT, 'engine/rl_after/rl_app_data.json'),
                        '88ce647f531030d8d2e094188b258191')]:
    got = _md5(path)
    if got != exp:
        raise SystemExit("PIN FAILED %s: %s != %s (%s)" % (lbl, got, exp, path))
if os.path.exists(_LOCAL) and _md5(_LOCAL) != MATRIX_MD5:
    raise SystemExit("PIN FAILED matrix (evidence copy): %s != %s" % (_md5(_LOCAL), MATRIX_MD5))

M = json.load(open(MATRIX)); R = M['recs']; META = M['meta']
assert META['store_md5'] == 'd9a24282', "matrix store %s" % META['store_md5']
assert META['v0surf_sig'][:12] == '6ef67f07db98', "matrix v0surf %s" % META['v0surf_sig'][:12]

D = json.load(open(os.path.join(HERE, 'DERIVE.json')))
L2 = json.load(open(os.path.join(HERE, 'LAYER2.json')))
L1 = json.load(open(L1P))
E = {e['key']: e for e in L1['entries']}
BASE = L2['base']

AF = float(D['anchor_factor'])
NUM = float(json.load(open(os.path.join(ROOT, 'engine/rl_after/pick_redenomination.json')))['factor'])
ALLIN = {int(k): float(v) for k, v in D['curve']['anchored'].items()}
PVC = {int(k): float(v) for k, v in D['curve']['pvc_today'].items()}
CELLS = {tuple(k.split('|')): v for k, v in D['pool']['cells'].items()}
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']

# ---- the entry-price objects, verbatim from o26a_bridge.py -------------------------------------
_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
IN_FLAT = dict(CUR['signed_flat']); IN_RD = dict(CUR['signed_rd_positional'])
IN_ND65 = float(CUR['signed_nd65_plus']['measured_k15'])
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])
LEVI = {k: int(float(v)) for k, v in IN_FLAT.items()}
LEVI['ND65+'] = int(IN_ND65)
for k, v in IN_RD.items(): LEVI['RD:' + k] = int(float(v))
assert abs(PL_F - NUM) < 1e-12, "the numeraire and _PL_F must be the same object"


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


def division(r):
    t = r.get('type')
    if t == 'RD': return 'RD:' + r['pos']
    if t == 'ND': return 'ND65+'
    return t


def anchor_of(r):
    if r.get('is_pool_engine'):
        d = division(r)
        if d in LEVI: return LEVI[d] * PL_F
    return float(r['v0'])


W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def sem(r, Y):
    """o25_derive.py::yr4()'s branch structure, verbatim. 'skip' = the entry LEAVES the denominator."""
    if Y > W: return ('skip_notyet', None)
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return ('zero_noyrs', 0.0)
    if Y < yrs[0]: return ('skip_pre', None)
    if Y > yrs[-1]: return ('zero_ended', 0.0)
    i = yrs.index(Y); v = vp[i]
    return ('zero_null', 0.0) if v is None else ('path', float(v))


# ---- THE DERIVED DAY-0, as the pre-statement fixed it -------------------------------------------
def derived_v0(r):
    """cell_v0 x ANCHOR_FACTOR x NUMERAIRE. The position is the ACQUISITION SLOT (Ruling 5), read off
    Layer 1's day0_position group -- NOT the matrix's r['pos'], which is the modelling position."""
    k = r['key']; e = E.get(k)
    st = stream(r)
    if st == 'ND 1-64' and r.get('pick') and 1 <= r['pick'] <= 64:
        return ALLIN[r['pick']] * NUM, 'nd_curve'
    g = (e or {}).get('position_group')
    c = CELLS.get((st, g))
    if c is None: return None, 'no_cell'
    return float(c['v0']) * AF * NUM, 'pool_cell'


LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


def disp(xs):
    xs = [x for x in xs if x == x]
    return dict(n=len(xs), mean=(sum(xs) / len(xs) if xs else float('nan')),
                p05=q(xs, .05), median=q(xs, .50), p95=q(xs, .95))


P("=" * 122)
P("ORDER 26B  --  STEP 5, THE COMPARISONS AND THE TWO NEW MANDATORY INSTRUMENTS")
P("=" * 122)
P("  matrix   per_entrant_O25R4.json  md5 %s  store %s  v0surf %s  window_end %d"
  % (MATRIX_MD5[:12], META['store_md5'], META['v0surf_sig'][:12], W))
P("  derived  DERIVE.json md5 %s   ANCHOR_FACTOR %.4f   NUMERAIRE %.4f"
  % (_md5(os.path.join(HERE, 'DERIVE.json'))[:12], AF, NUM))
P("  forms    INSTRUMENTS_PRESTATEMENT.md, committed 2026-08-12 BEFORE this harness existed")
P("  DISPERSION IS BINDING: no mean is printed here without p05/median/p95 beside it.")
P()

# ==================================================================================================
# 1. DERIVED v0  vs  PRINTED DAY-0  vs  SIGNED ANCHOR
# ==================================================================================================
P("-" * 122)
P("1.  DERIVED v0  vs  PRINTED DAY-0  vs  SIGNED ANCHOR")
P("-" * 122)
P("  printed day-0 = the matrix's r['v0'] (the shipped year-zero surface value the board prices an")
P("                  entrant at on day one)")
P("  signed anchor = o26a_bridge.py::anchor_of(r) = the owner's signed level x %.4f" % PL_F)
P("  derived v0    = cell_v0 x %.4f x %.4f   (the pre-statement's three declared multiplications)" % (AF, NUM))
P()

POOLROWS = [r for r in R if r.get('is_pool_engine') and (r.get('v0') or 0) > 0
            and cohort(r) is not None]
NDROWS_M = [r for r in R if stream(r) == 'ND 1-64' and (r.get('v0') or 0) > 0]
CMP = []
for r in POOLROWS:
    d, how = derived_v0(r)
    if d is None: continue
    CMP.append(dict(key=r['key'], mech=stream(r), pos=E.get(r['key'], {}).get('position_group'),
                    derived=d, printed=float(r['v0']), anchor=anchor_of(r), entry=r['year']))

dp_ = disp([c['derived'] / c['printed'] for c in CMP])
da_ = disp([c['derived'] / c['anchor'] for c in CMP if c['anchor'] > 0])
pa_ = disp([c['printed'] / c['anchor'] for c in CMP if c['anchor'] > 0])
P("  WHOLE POOL (n=%d entrants with a printed day-0 and a derived cell)" % len(CMP))
P("    %-28s %8s %10s %10s %10s %10s" % ('ratio', 'n', 'mean', 'p05', 'median', 'p95'))
for lbl, d in [('derived / printed day-0', dp_), ('derived / signed anchor', da_),
               ('printed day-0 / signed anchor  [26A read 2.6498 on its own population]', pa_)]:
    P("    %-28s %8d %10.4f %10.4f %10.4f %10.4f"
      % (lbl[:28], d['n'], d['mean'], d['p05'], d['median'], d['p95']))
P("    (the third row is 26A's headline restated on THIS population; 26A measured 2.6498 whole-pool)")
P("    AGGREGATE (sum/sum, the all-in form): derived/printed %.4f   derived/anchor %.4f"
  % (sum(c['derived'] for c in CMP) / sum(c['printed'] for c in CMP),
     sum(c['derived'] for c in CMP) / sum(c['anchor'] for c in CMP)))

P()
P("  BY DAY-0 POSITION (pooled across pathways)")
P("  %-6s %6s %11s %11s %11s   %10s %10s %10s   %10s" %
  ('pos', 'n', 'derived', 'printed', 'anchor', 'der/prn', 'der/anch', 'prn/anch', 'd/p p05-p95'))
BYPOS = {}
for g in POSN:
    sub = [c for c in CMP if c['pos'] == g]
    if not sub: continue
    dd = disp([c['derived'] / c['printed'] for c in sub])
    BYPOS[g] = dict(n=len(sub),
                    derived=sum(c['derived'] for c in sub) / len(sub),
                    printed=sum(c['printed'] for c in sub) / len(sub),
                    anchor=sum(c['anchor'] for c in sub) / len(sub),
                    der_prn=disp([c['derived'] / c['printed'] for c in sub]),
                    der_anch=disp([c['derived'] / c['anchor'] for c in sub if c['anchor'] > 0]),
                    prn_anch=disp([c['printed'] / c['anchor'] for c in sub if c['anchor'] > 0]))
    b = BYPOS[g]
    P("  %-6s %6d %11.1f %11.1f %11.1f   %10.4f %10.4f %10.4f   %5.3f-%5.3f"
      % (g, b['n'], b['derived'], b['printed'], b['anchor'],
         b['der_prn']['median'], b['der_anch']['median'], b['prn_anch']['median'],
         dd['p05'], dd['p95']))

P()
P("  BY PATHWAY x DAY-0 POSITION  (the named rows the packet carries are marked below the table)")
P("  %-7s %-5s %5s %11s %11s %11s %9s %9s %9s" %
  ('path', 'pos', 'n', 'derived', 'printed', 'anchor', 'der/prn', 'der/anch', 'prn/anch'))
CELLCMP = {}
for m in POOLM:
    for g in POSN:
        sub = [c for c in CMP if c['mech'] == m and c['pos'] == g]
        if not sub: continue
        dv = sum(c['derived'] for c in sub) / len(sub)
        pv = sum(c['printed'] for c in sub) / len(sub)
        av = sum(c['anchor'] for c in sub) / len(sub)
        CELLCMP['%s|%s' % (m, g)] = dict(
            n=len(sub), derived=dv, printed=pv, anchor=av,
            der_prn=disp([c['derived'] / c['printed'] for c in sub]),
            der_anch=disp([c['derived'] / c['anchor'] for c in sub if c['anchor'] > 0]))
        P("  %-7s %-5s %5d %11.1f %11.1f %11.1f %9.4f %9.4f %9.4f"
          % (m, g, len(sub), dv, pv, av, dv / pv, dv / av if av else float('nan'),
             pv / av if av else float('nan')))

P()
P("  BY PATHWAY (pooled positions)")
P("  %-7s %6s %11s %11s %11s %9s %9s %9s   %s" %
  ('path', 'n', 'derived', 'printed', 'anchor', 'der/prn', 'der/anch', 'prn/anch', 'der/prn p05-p95'))
BYPATH = {}
for m in POOLM:
    sub = [c for c in CMP if c['mech'] == m]
    if not sub: continue
    dv = sum(c['derived'] for c in sub) / len(sub)
    pv = sum(c['printed'] for c in sub) / len(sub)
    av = sum(c['anchor'] for c in sub) / len(sub)
    dd = disp([c['derived'] / c['printed'] for c in sub])
    BYPATH[m] = dict(n=len(sub), derived=dv, printed=pv, anchor=av, der_prn=dd,
                     der_anch=disp([c['derived'] / c['anchor'] for c in sub if c['anchor'] > 0]))
    P("  %-7s %6d %11.1f %11.1f %11.1f %9.4f %9.4f %9.4f   %5.3f-%5.3f"
      % (m, len(sub), dv, pv, av, dv / pv, dv / av if av else float('nan'),
         pv / av if av else float('nan'), dd['p05'], dd['p95']))

# ==================================================================================================
# 2. THE DERIVED CURVE vs TODAY'S CURVE (ND)
# ==================================================================================================
P()
P("-" * 122)
P("2.  THE DERIVED ALL-IN CURVE vs TODAY'S PICK CURVE (ND)")
P("-" * 122)
HEAD = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]
P("  %-16s %s" % ('pick', "".join("%8d" % p for p in HEAD)))
P("  %-16s %s" % ('DERIVED (ladder)', "".join("%8.0f" % ALLIN[p] for p in HEAD)))
P("  %-16s %s" % ('today PVC', "".join("%8.0f" % PVC[p] for p in HEAD)))
P("  %-16s %s" % ('derived/PVC', "".join("%8.3f" % (ALLIN[p] / PVC[p]) for p in HEAD)))
P("  %-16s %s" % ('DERIVED x num.', "".join("%8.0f" % (ALLIN[p] * NUM) for p in HEAD)))
ndpr = []
for r in NDROWS_M:
    if not (1 <= (r.get('pick') or 0) <= 64): continue
    ndpr.append(ALLIN[r['pick']] * NUM / float(r['v0']))
dnd = disp(ndpr)
P("  ND derived day-0 / printed day-0 (per entrant, n=%d): mean %.4f  p05 %.4f  med %.4f  p95 %.4f"
  % (dnd['n'], dnd['mean'], dnd['p05'], dnd['median'], dnd['p95']))
P("  (the ND spread around 1.0 is the year-zero SURFACE -- position/age redistribution around the")
P("   curve at a given pick. The curve-level comparison is the derived/PVC row above.)")

# ==================================================================================================
# 3. THE MARK-PATH PROGRESSION TEST
# ==================================================================================================
P()
P("-" * 122)
P("3.  THE MARK-PATH PROGRESSION TEST  (new mandatory instrument; form fixed in PREREG §6 and")
P("    detailed in INSTRUMENTS_PRESTATEMENT.md §3, both committed before this ran)")
P("-" * 122)
DEPTHS = list(range(0, 7))


def paths_for(rows):
    """Returns (m_allin[d], m_mean[d], n[d]) under the pre-stated semantics."""
    ma, mm, nn = {}, {}, {}
    for d in DEPTHS:
        num = den = 0.0; rat = []
        for r, v0 in rows:
            Y = cohort(r) + d
            kind, v = sem(r, Y)
            if v is None: continue
            num += v; den += v0; rat.append(v / v0)
        ma[d] = (num / den) if den else float('nan')
        mm[d] = (sum(rat) / len(rat)) if rat else float('nan')
        nn[d] = len(rat)
    return ma, mm, nn


ARMS = collections.OrderedDict()
ARMS['ND 1-64'] = [(r, derived_v0(r)[0]) for r in NDROWS_M
                   if cohort(r) is not None and derived_v0(r)[0]]
for m in POOLM:
    rows = [(r, derived_v0(r)[0]) for r in POOLROWS if stream(r) == m and derived_v0(r)[0]]
    if rows: ARMS[m] = rows

P("  PRIMARY reading m_allin(d) = sum(marks at depth d) / sum(derived day-0), dead ZEROED and KEPT.")
P("  %-8s %6s %s   %8s %6s %s" %
  ('arm', 'n@d4', "".join("%8s" % ('d%d' % d) for d in DEPTHS), 'peak', 'at d', 'verdict'))
PROG = {}
for arm, rows in ARMS.items():
    ma, mm, nn = paths_for(rows)
    best_d = max((d for d in DEPTHS if ma[d] == ma[d]), key=lambda d: ma[d])
    peak = ma[best_d]
    rise = [d for d in DEPTHS if d >= 2 and ma[d] == ma[d] and ma[d] > ma[0]]
    thin = nn.get(4, 0) < 40
    ok = bool(rise) and best_d >= 2
    # THE MSD DEBUT-YEAR GAP, a KNOWN and PREVIOUSLY DISCLOSED instrument defect (ORDER 26A
    # SUMMARY.md anomaly 5): the emitter builds `yrs` from draft year + 1 on every route, but
    # cohort() for MSD is the draft year itself, so an MSD entrant's d=0 always resolves BEFORE his
    # first emitted year and every row leaves the denominator. m(0) is then undefined and the
    # literal predicate cannot be evaluated -- it reads as a FAIL for a reason that has nothing to
    # do with MSD's marks. The REPAIRED reading below re-bases the entry reference on the first
    # depth with a non-empty denominator. It is printed BESIDE the literal reading, never instead
    # of it, and the deviation is named in the packet.
    d0 = next((d for d in DEPTHS if nn[d] > 0), None)
    rep_ok = None; rep_base = None
    if d0 is not None and d0 != 0:
        rep_base = d0
        rep_ok = bool([d for d in DEPTHS if d >= d0 + 2 and ma[d] == ma[d] and ma[d] > ma[d0]]) \
            and best_d >= d0 + 2
    PROG[arm] = dict(m_allin=ma, m_mean=mm, n=nn, peak=peak, peak_d=best_d,
                     passes=ok, thin=thin, n_at_d4=nn.get(4, 0),
                     entry_depth=d0, repaired_passes=rep_ok, repaired_base_depth=rep_base)
    P("  %-8s %6d %s   %8.3f %6d %s"
      % (arm, nn.get(4, 0), "".join(("%8.3f" % ma[d]) if ma[d] == ma[d] else "%8s" % 'n/a'
                                    for d in DEPTHS), peak, best_d,
         ('PASS' if ok else 'FAIL') + ('  [THIN n<40]' if thin else '')
         + ('' if rep_ok is None else
            '  [m(0) UNDEFINED -- the MSD debut-year gap; REPAIRED from d%d: %s]'
            % (rep_base, 'PASS' if rep_ok else 'FAIL'))))
P()
P("  SECONDARY reading m_mean(d) = mean of per-entrant ratios (PREREG §6's literal 'mean_i' wording)")
P("  %-8s %s   %8s %6s %s" % ('arm', "".join("%8s" % ('d%d' % d) for d in DEPTHS),
                              'peak', 'at d', 'verdict'))
DISAGREE = []
for arm in ARMS:
    mm = PROG[arm]['m_mean']
    bd = max((d for d in DEPTHS if mm[d] == mm[d]), key=lambda d: mm[d])
    base = PROG[arm]['entry_depth'] or 0
    ok2 = bd >= base + 2 and mm[bd] > mm[base]
    if ok2 != PROG[arm]['passes']: DISAGREE.append(arm)
    PROG[arm]['passes_mean'] = ok2; PROG[arm]['peak_d_mean'] = bd; PROG[arm]['peak_mean'] = mm[bd]
    P("  %-8s %s   %8.3f %6d %s"
      % (arm, "".join(("%8.3f" % mm[d]) if mm[d] == mm[d] else "%8s" % 'n/a' for d in DEPTHS),
         mm[bd], bd, 'PASS' if ok2 else 'FAIL'))
P()
P("  THE TWO READINGS DISAGREE ON: %s" % (", ".join(DISAGREE) if DISAGREE else "no arm"))
P("  n in the denominator by depth (the dead are IN it; only 'not yet' and 'pre-first-season' leave)")
P("  %-8s %s" % ('arm', "".join("%8s" % ('d%d' % d) for d in DEPTHS)))
for arm in ARMS:
    P("  %-8s %s" % (arm, "".join("%8d" % PROG[arm]['n'][d] for d in DEPTHS)))

# ==================================================================================================
# 4. THE REVERSE NO-ARB TEST
# ==================================================================================================
P()
P("-" * 122)
P("4.  THE REVERSE NO-ARB TEST  (new mandatory instrument)")
P("-" * 122)
P("  THE PREDICATE, as stated in INSTRUMENTS_PRESTATEMENT.md §4 BEFORE this computation:")
P("    A pathway FAILS (is a systematic guaranteed-loss hold) iff BOTH")
P("      (1) m_allin(d) < 1 for EVERY d = 1..6 at which it has any denominator, AND")
P("      (2) the upper end of a 95%% bootstrap interval on max_{d>=1} m_allin(d) is ALSO below 1.")
P("    PASS = no pathway fails. Bootstrap: B=2000, ENTRANT-level resampling, seed 20260812,")
P("    97.5th percentile. n < 8 entrants => printed but marked UNRELIABLE; no FAIL is issued there.")
P()
B = 2000
SEED = 20260812


def boot_max(rows):
    rs = np.random.RandomState(SEED)
    n = len(rows)
    pre = []
    for r, v0 in rows:
        row = []
        for d in DEPTHS:
            if d == 0: continue
            kind, v = sem(r, cohort(r) + d)
            row.append((v, v0) if v is not None else None)
        pre.append(row)
    stats = np.empty(B)
    idx = rs.randint(0, n, size=(B, n))
    for b in range(B):
        num = np.zeros(len(DEPTHS) - 1); den = np.zeros(len(DEPTHS) - 1)
        for i in idx[b]:
            for j, cell in enumerate(pre[i]):
                if cell is None: continue
                num[j] += cell[0]; den[j] += cell[1]
        with np.errstate(invalid='ignore', divide='ignore'):
            mm = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
        stats[b] = np.nanmax(mm) if np.any(den > 0) else np.nan
    return float(np.nanpercentile(stats, 2.5)), float(np.nanpercentile(stats, 97.5))


P("  %-8s %6s %s   %8s %10s %10s   %s" %
  ('arm', 'n', "".join("%8s" % ('d%d' % d) for d in DEPTHS[1:]), 'max d>=1',
   'boot lo', 'boot hi', 'verdict'))
NOARB = {}
for arm, rows in ARMS.items():
    ma = PROG[arm]['m_allin']
    ds = [d for d in DEPTHS[1:] if ma[d] == ma[d] and PROG[arm]['n'][d] > 0]
    mx = max(ma[d] for d in ds) if ds else float('nan')
    limb1 = bool(ds) and all(ma[d] < 1.0 for d in ds)
    lo, hi = boot_max(rows)
    limb2 = hi < 1.0
    unrel = len(rows) < 8
    fails = bool(limb1 and limb2 and not unrel)
    NOARB[arm] = dict(n=len(rows), max_m=mx, limb1=limb1, boot_lo=lo, boot_hi=hi,
                      limb2=limb2, unreliable=unrel, fails=fails,
                      m_allin={d: ma[d] for d in DEPTHS[1:]})
    P("  %-8s %6d %s   %8.3f %10.3f %10.3f   %s"
      % (arm, len(rows), "".join(("%8.3f" % ma[d]) if ma[d] == ma[d] else "%8s" % '--'
                                 for d in DEPTHS[1:]), mx, lo, hi,
         ('FAIL -- GUARANTEED-LOSS HOLD' if fails else 'PASS')
         + ('  [UNRELIABLE n<8]' if unrel else '')
         + ('' if not limb1 else '  [limb 1 red]')))
ANYFAIL = [a for a in NOARB if NOARB[a]['fails']]
P()
P("  VERDICT: %s" % ("PASS -- no pathway is a systematic guaranteed-loss hold at the derived entry "
                     "price." if not ANYFAIL else
                     "FAIL -- guaranteed-loss holds: %s" % ", ".join(ANYFAIL)))
P("  NON-VACUITY: the predicate is able to go red. Limb 1 (every m_allin(d) < 1) is red for %s;"
  % (", ".join(a for a in NOARB if NOARB[a]['limb1']) or 'no arm'))
P("  a FAIL needs limb 2 as well, and the bootstrap upper limits are printed above so the distance")
P("  to the failure line is legible rather than hidden behind a verdict word.")

# ==================================================================================================
# 5. THE NAMED ROWS
# ==================================================================================================
NAMED = ['willem-duursma', 'callum-moore', 'harrison-ramm', 'vigo-visentini', 'jai-newcombe']
BROW = {r['key']: r for r in json.load(open(ROOT + '/engine/rl_after/rl_app_data.json'))['active']}
MROW = {r['key']: r for r in R}
P()
P("-" * 122)
P("5.  THE NAMED ROWS")
P("-" * 122)
P("  'delivered TO DATE' is the OBSERVED leg alone; 'delivered TOTAL' adds Ruling 8's gated projected")
P("  tail. PREREG §5 wrote 'delivered value to date' for harrison-ramm, so both objects are printed and")
P("  both are scored in the packet -- the prediction is not quietly re-read onto whichever one it hits.")
P("  %-18s %-7s %-5s %6s %10s %10s %6s %11s %11s %11s %8s %9s" %
  ('key', 'path', 'pos', 'entry', 'to date', 'TOTAL', 'tail%', 'derived v0', 'printed d0', 'anchor',
   'der/prn', 'board v'))
NAMEDROWS = {}
for k in NAMED:
    e = E.get(k); r = MROW.get(k)
    if e is None:
        P("  %-18s NOT IN LAYER 1" % k); continue
    dv = (derived_v0(r)[0] if r is not None else None)
    if dv is None and e['mechanism'] == 'ND 1-64' and e['pick']:
        dv = ALLIN[e['pick']] * NUM
    if dv is None:
        c = CELLS.get((e['mechanism'], e['position_group']))
        dv = float(c['v0']) * AF * NUM if c else float('nan')
    pv = float(r['v0']) if r is not None and r.get('v0') else float('nan')
    an = anchor_of(r) if r is not None else float('nan')
    bv = BROW.get(k, {}).get('v')
    NAMEDROWS[k] = dict(mech=e['mechanism'], pos=e['position_group'], entry=e['entry_year'],
                        delivered=BASE[k]['total'], obs=BASE[k]['obs'], tail=BASE[k]['tail'],
                        tail_share=BASE[k]['tail_share'],
                        derived_v0=dv, printed_v0=pv, anchor=an, board_v=bv,
                        on_live_board=(k in BROW))
    P("  %-18s %-7s %-5s %6s %10.1f %10.1f %5.1f%% %11.1f %11.1f %11.1f %8.4f %9s"
      % (k, e['mechanism'], e['position_group'], e['entry_year'], BASE[k]['obs'], BASE[k]['total'],
         100 * BASE[k]['tail_share'], dv, pv, an,
         (dv / pv) if pv == pv and pv else float('nan'),
         (str(bv) if bv is not None else 'NOT ON BOARD')))
P("  callum-moore is NOT on the live board -- his delivered-value score is the object the packet uses.")

OUT = dict(matrix=dict(file='per_entrant_O25R4.json', md5=MATRIX_MD5, store=META['store_md5'],
                       v0surf=META['v0surf_sig'], window_end=W),
           anchor_factor=AF, numeraire=NUM,
           pooled=dict(n=len(CMP), der_prn=dp_, der_anch=da_, prn_anch=pa_,
                       agg_der_prn=sum(c['derived'] for c in CMP) / sum(c['printed'] for c in CMP),
                       agg_der_anch=sum(c['derived'] for c in CMP) / sum(c['anchor'] for c in CMP)),
           by_pos=BYPOS, by_path=BYPATH, by_cell=CELLCMP,
           nd_curve=dict(derived={p: ALLIN[p] for p in HEAD}, pvc={p: PVC[p] for p in HEAD},
                         per_entrant_der_over_printed=dnd),
           progression=PROG, progression_disagreements=DISAGREE,
           noarb=NOARB, noarb_any_fail=ANYFAIL, bootstrap=dict(B=B, seed=SEED, pct=97.5,
                                                               resample='entrant-level'),
           named=NAMEDROWS)
json.dump(OUT, open(os.path.join(HERE, 'COMPARE.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'COMPARE_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote COMPARE.json / COMPARE_out.txt")
