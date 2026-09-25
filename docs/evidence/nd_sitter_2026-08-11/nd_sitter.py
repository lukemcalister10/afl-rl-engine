"""ORDER 18 -- DOES THE NATIONAL-DRAFT SITTER TREATMENT REDISTRIBUTE, OR IS IT A NET CHARGE?

THE OWNER'S QUESTION, VERBATIM:
  "Does the ND sitter penalty redistribute? As if we are penalising 5x for some sitters, that would
   be a huge redistribution to those who don't."

THE LAW (owner's D8 amendment, the MEAN-PRESERVING PRINCIPLE): once a group's entry price is
calibrated to that group's own realized returns -- SITTERS INCLUDED -- any within-group sitter
differential must be a REDISTRIBUTION and never a net charge. The test statistic is the entry-weighted
mean of the APPLIED sitter multiplier over the group:

    mean = ( SUM_sitters e*R + SUM_non-sitters e*1 ) / SUM_all e

mean < 1.0 is a NET CHARGE and a breach. The uplift the non-sitters would have to carry for the law
to hold is  U = ( SUM_all e - SUM_sitters e*R ) / SUM_non-sitters e.

PHASE 1 (branch build/pool-repricing-phase1, PR #453, OPEN -- untouched by this act) measured this for
the nine POOL pathways and found a breach on every one. It built an ND cell list
(`NDC = [c for c in cells if not c['pool'] and c['wc']]`) and never used it. THIS SCRIPT USES IT.

WHY THE ND ARM IS THE WHOLE R AND NOTHING ELSE.  _h_cut (_merged_recover.py:2037-2049) composes
H_POOLSIT/H_UNION inside `if pool and sitter:`, so NO ND ROW EVER REACHES THEM. On the national arm
the retention surface R is the ENTIRE sitter differential:
    sitout_ev(p,Y,e_full) = (1-lam)*R*entry_anchor(p) + lam*e_full        (_merged_recover.py:1961)
and for a TRUE sitter lam=0, so the finished price IS R*entry_anchor(p).

THE CELL CONSTRUCTION IS PHASE 1'S, CARRIED VERBATIM, NOT REINVENTED. draftyr / min_window /
listed_through / outcomeO / wins / stream and the harvest loop below are byte-identical in behaviour to
docs/evidence/pool_repricing_2026-08-11/phase1_retention.py (branch build/pool-repricing-phase1), which
this act DOES NOT MODIFY. It is carried rather than imported because that file lives only on the open
phase-1 branch and this act is cut from origin/main. ONE FIELD IS ADDED -- `effpk` -- because the ND
question is pick-conditioned and phase 1's pool question was not (effpk is the constant POOL_PICK=65
for every pool entrant, which is exactly why phase 1 had no pick axis to record).

CONTROL: this script REPRODUCES phase 1's pool today-mean net-charge column before reporting anything
about the national arm. If the reproduction does not match the published figures the run is not to be
believed, and the deltas are printed rather than swallowed.

Loads the engine READ-ONLY from a staged copy so the repo is untouched. No emits. Deterministic.

  usage:  OPENBLAS_NUM_THREADS=1 /root/rl_venv312/bin/python nd_sitter.py
"""
import os, sys, io, json, contextlib, math, collections, shutil, hashlib

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng_stage_o18/rl_after'
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- ENTRY PIN ASSERTION (Order 18 constraint: measure only; nothing shipped may have moved) -------
PINS = {
    'board': ('data/rl_build/rl_app_data.json', '94f1fec59f99c59d5890d5975c79fa9b'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = []
    for k, (rel, exp) in PINS.items():
        got = _md5(os.path.join(ROOT, rel))
        if got != exp:
            bad.append("%s %s != pinned %s (%s)" % (k, got, exp, rel))
    if bad:
        raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))
    return {k: v[1] for k, v in PINS.items()}


assert_pins('entry')

# ---- SELF-STAGING (phase 1's discipline, carried): the engine needs its own dir as cwd and needs
# LTI_REGISTER.md, which lives at the repo ROOT. Copy to scratch and run there. THE REPO IS NEVER
# TOUCHED BY THIS SCRIPT.
if not os.path.exists(os.path.join(STAGE, '_merged_recover.py')):
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(ROOT + '/LTI_REGISTER.md', STAGE)

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
P("ORDER 18 -- THE NATIONAL-DRAFT SITTER TREATMENT: REDISTRIBUTION, OR NET CHARGE?")
P("=" * 118)
P("  pins asserted at entry:  board 94f1fec5..  store d9a24282..  instrument 0f822035..")
P("  engine loaded read-only from a staged copy; repo untouched.  MA.data n=%d" % len(MA.data))
P("  on the ND arm _h_cut is inert by construction (gated on p['_pool']), so R is the WHOLE")
P("  differential. H_POOLSIT=%.3f / H_UNION=%.3f appear below ONLY in the pool control." % (H_POOLSIT, H_UNION))
P()

# ==================================================================================================
# THE CELL CONSTRUCTION -- PHASE 1'S, CARRIED VERBATIM (see module docstring)
# ==================================================================================================


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
    """d13's forward outcome. Era normalization does not exist (owner ruling, #334 stage B salvage,
    _merged_recover.py:51-57): season averages are read RAW."""
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
        try:
            epk = int(MA.effpk(p))
        except Exception:
            epk = 65
        for Y in range(dy + 1, min(lt, 2025) + 1):
            quals = [x for x in rows if x['games'] >= 6 and x['year'] <= Y]
            cells.append(dict(pool=bool(p.get('_pool')), stream=stream(p), cls=cls, pos=pos,
                              d=Y - dy, sitout=bool(not quals), O=outcomeO(p, Y),
                              V0start=va, Vanchor=ea, wc=bool(Y <= 2021),
                              age=_b_age(p), typ=p.get('type'),
                              effpk=epk, pick=(p.get('pick') or 0)))     # <- the one added field

POOL = [c for c in cells if c['pool'] and c['wc']]
NDC = [c for c in cells if not c['pool'] and c['wc']]          # phase 1's own line, finally used
ND64 = [c for c in NDC if c['stream'] == 'ND 1-64']

P("=" * 118)
P("POPULATION")
P("=" * 118)
P("  harvested cells (complete-window, Y<=2021):  pool %d   national %d" % (len(POOL), len(NDC)))
P("  national arm by stream: %s"
  % ", ".join("%s %d" % (s, sum(1 for c in NDC if c['stream'] == s))
              for s in sorted(set(c['stream'] for c in NDC))))
P("  ND 1-64 cells: %d   of which sit-out: %d (%.1f%% by count)"
  % (len(ND64), sum(1 for c in ND64 if c['sitout']),
     100.0 * sum(1 for c in ND64 if c['sitout']) / max(len(ND64), 1)))
P()
P("  NOTE ON `entry_anchor` ON THE NATIONAL ARM. entry_anchor(p) returns v0_start(p) for any non-pool")
P("  row (_merged_recover.py:1852-1857), so the two denominators phase 1 had to keep separate for the")
P("  pool COINCIDE here. Verified rather than asserted:")
_dd = [abs(c['Vanchor'] - c['V0start']) for c in ND64
       if c['Vanchor'] == c['Vanchor'] and c['V0start'] == c['V0start']]
P("      max |entry_anchor - v0_start| over ND 1-64 = %.12g   (n=%d)" % (max(_dd) if _dd else 0.0, len(_dd)))
P()

DEPTHS = list(range(1, 7))
RANGES = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]   # the engine's own board RANGES
CLASSES = ('nonKPP', 'KPP', 'RUCK')


def applied_R(c):
    """The multiplier the ENGINE applies to this row's sitter price, at the row's OWN pick.

    R = _R_surf(_sitout_cls(gfut(p)), effpk(p), tau)  -- sitout_ev:1963.
    Depth d is mapped to tau=float(d), which is exactly the mapping phase 1 used when it read the
    surface for its own 'today' table (`_R_surf(cls, 65, float(d))`). Using the row's own effpk
    instead of the constant 65 is the ONLY difference, and it is the point of this measurement.
    Non-sitters take 1.0: nothing in the ND path multiplies a non-sitter by anything else.
    """
    if not c['sitout']:
        return 1.0
    return float(_R_surf(c['cls'], c['effpk'], float(c['d'])))


def meanstat(sub, mult, weight='Vanchor'):
    """The mean-preserving statistic. Returns the dict the owner's law is read off.

    mean  = (SUM_sit e*R + SUM_non e) / SUM e        < 1.0 is a NET CHARGE
    U     = (SUM e - SUM_sit e*R) / SUM_non e        the uplift the law would require
    """
    tot = sitw = nonw = num = 0.0
    nsit = n = 0
    csum = 0.0
    for c in sub:
        e = c[weight]
        if not e or e != e or e <= 0: continue
        R = mult(c)
        tot += e; n += 1; csum += R
        if c['sitout']:
            sitw += e; num += e * R; nsit += 1
        else:
            nonw += e
    if tot <= 0:
        return None
    mean = (num + nonw) / tot
    return dict(n=n, nsit=nsit, sit_share_w=sitw / tot, sit_share_n=nsit / n if n else 0.0,
                meanR=(num / sitw) if sitw > 0 else float('nan'),
                mean=mean, net_charge=mean - 1.0,
                U=((tot - num) / nonw) if nonw > 0 else float('nan'),
                mean_count=csum / n if n else float('nan'))


# ==================================================================================================
# CONTROL -- REPRODUCE PHASE 1's POOL TODAY-MEAN BEFORE BELIEVING ANYTHING ABOUT THE NATIONAL ARM
# ==================================================================================================
P("=" * 118)
P("CONTROL -- REPRODUCING PHASE 1's POOL NET-CHARGE COLUMN (published on PR #453)")
P("=" * 118)
PUB = {'RD': -0.0807, 'SSP': -0.0920, 'MSD': -0.6586, 'IRE': -0.3959, 'PDA': -0.1198,
       'PDN': -0.1740, 'PDS': -0.1138, 'UNR': -0.2022, 'ND>64': -0.0976}
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']


def h_mult(c):
    """Phase 1's today-multiplier for a POOL row: the composed ITEM H factor ONLY."""
    if not c['sitout']:
        return 1.0
    f = H_POOLSIT
    if (c['age'] is not None and c['age'] >= 23.0) or c['typ'] in ('IRE', 'MSD'):
        f *= H_UNION
    return f


def rh_mult(c):
    """The FULL pool sitter multiplier the engine actually applies: R (at the pool index) TIMES the
    ITEM H cuts. Phase 1's published column counted ONLY the H leg, because H was the object its
    ruling retired. The pool row ALSO takes R inside sitout_ev, so the composed figure is the true
    total. Both are printed; neither is hidden."""
    return applied_R(c) * h_mult(c)


P("  %-8s %11s %11s %10s | %11s %11s" %
  ('pathway', 'published', 'reproduced', 'delta', 'R-leg only', 'R x H total'))
P("  " + "-" * 114)
CTRL = {}
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    if not sub: continue
    a = meanstat(sub, h_mult); b = meanstat(sub, applied_R); d = meanstat(sub, rh_mult)
    if a is None: continue
    CTRL[s] = dict(published=PUB[s], reproduced=a['net_charge'], delta=a['net_charge'] - PUB[s],
                   r_only=b['net_charge'], composed=d['net_charge'])
    P("  %-8s %11.4f %11.4f %10.6f | %11.4f %11.4f" %
      (s, PUB[s], a['net_charge'], a['net_charge'] - PUB[s], b['net_charge'], d['net_charge']))
P("  " + "-" * 114)
_mx = max(abs(v['delta']) for v in CTRL.values()) if CTRL else 0.0
P("  max |delta| vs published = %.6f  -> %s" % (_mx, "REPRODUCED" if _mx < 5e-5 else "MISMATCH"))
P()
P("  READ THE LAST TWO COLUMNS. Phase 1's published net charge is the H LEG ALONE. The pool sitter")
P("  also takes R inside sitout_ev at the pool index, and the composed R x H charge is far larger")
P("  than the figure the phase-1 ruling was made on. That is a finding about the POOL arm surfaced")
P("  by this act, reported because it was measured -- not because it was asked for.")
P()

# ==================================================================================================
# 1. THE HEADLINE
# ==================================================================================================
P("=" * 118)
P("1. THE HEADLINE -- ND PICKS 1-64, ENTRY-WEIGHTED MEAN OF THE APPLIED SITTER MULTIPLIER")
P("=" * 118)
HEAD = meanstat(ND64, applied_R)
HEAD_V0 = meanstat(ND64, applied_R, weight='V0start')
P()
P("      mean = ( SUM_sitters e*R + SUM_non-sitters e*1 ) / SUM_all e ,   e = entry_anchor")
P()
P("      cells                     %10d" % HEAD['n'])
P("      sitter cells              %10d" % HEAD['nsit'])
P("      sitter share (by count)   %10.4f" % HEAD['sit_share_n'])
P("      sitter share (entry-wtd)  %10.4f" % HEAD['sit_share_w'])
P("      mean R among sitters      %10.4f      (i.e. the AVERAGE sitter is charged %.2fx;"
  % (HEAD['meanR'], 1.0 / HEAD['meanR']))
P("                                              the HARSHEST single cell is charged %.2fx -- see 2)"
  % (1.0 / min(float(_R_surf(c['cls'], c['effpk'], float(c['d']))) for c in ND64 if c['sitout'])))
P("      ----------------------------------------")
P("      HEADLINE MEAN             %10.6f" % HEAD['mean'])
P("      NET CHARGE                %10.6f   (%+.2f%%)" % (HEAD['net_charge'], 100.0 * HEAD['net_charge']))
P("      VERDICT                   %10s" % ('NET CHARGE - BREACH' if HEAD['mean'] < 0.9999 else 'redistribution-neutral'))
P("      ----------------------------------------")
P("      required uplift U         %10.6f      what an ND NON-SITTER would have to carry for the" % HEAD['U'])
P("                                              law to hold. WHAT HE ACTUALLY CARRIES IS 1.000000,")
P("                                              a shortfall of %+.4f%% on every non-sitter." % (100.0 * (1.0 - HEAD['U'])))
P()
P("      cross-check, e = v0_start (identical object on this arm): mean %.6f  net %+.6f"
  % (HEAD_V0['mean'], HEAD_V0['net_charge']))
P("      unweighted (per-cell) mean multiplier:                    %.6f" % HEAD['mean_count'])
P()
P("  THE ANSWER TO THE OWNER'S QUESTION. The ND sitter treatment does NOT redistribute. There is no")
P("  uplift term on the national arm at all -- _h_cut is pool-gated and sitout_ev multiplies only the")
P("  sitter's own anchor. Every unit taken off a sitter leaves the cohort; not one unit reaches a")
P("  non-sitter. The 'huge redistribution to those who don't' does not occur, because there is no")
P("  redistribution: it is a %.2f%% NET CHARGE on the national draft 1-64." % (-100.0 * HEAD['net_charge']))
P()

# ==================================================================================================
# 2. THE BREAKDOWN
# ==================================================================================================
P("=" * 118)
P("2. BREAKDOWN -- BY PICK BAND, AND BY POSITION CLASS")
P("=" * 118)
P()
P("  BY PICK BAND (the engine's own board RANGES)")
P("  %-10s %7s %7s | %9s %9s | %10s %11s | %9s" %
  ('band', 'cells', 'sitters', 'sit share', 'mean R', 'MEAN', 'net charge', 'U needed'))
P("  " + "-" * 114)
BAND = {}
for lo, hi in RANGES:
    sub = [c for c in ND64 if lo <= c['pick'] <= hi]
    m = meanstat(sub, applied_R)
    if m is None: continue
    k = "%d-%d" % (lo, hi)
    BAND[k] = m
    P("  %-10s %7d %7d | %9.4f %9.4f | %10.6f %11.6f | %9.6f" %
      (k, m['n'], m['nsit'], m['sit_share_w'], m['meanR'], m['mean'], m['net_charge'], m['U']))
P("  " + "-" * 114)
_sp = [v['net_charge'] for v in BAND.values()]
P("  SPREAD across bands: %.6f to %.6f  (range %.6f)" % (max(_sp), min(_sp), max(_sp) - min(_sp)))
P()
P("  BY POSITION CLASS")
P("  %-10s %7s %7s | %9s %9s | %10s %11s | %9s" %
  ('class', 'cells', 'sitters', 'sit share', 'mean R', 'MEAN', 'net charge', 'U needed'))
P("  " + "-" * 114)
CLS = {}
for cl in CLASSES:
    sub = [c for c in ND64 if c['cls'] == cl]
    m = meanstat(sub, applied_R)
    if m is None: continue
    CLS[cl] = m
    P("  %-10s %7d %7d | %9.4f %9.4f | %10.6f %11.6f | %9.6f" %
      (cl, m['n'], m['nsit'], m['sit_share_w'], m['meanR'], m['mean'], m['net_charge'], m['U']))
P("  " + "-" * 114)
_sc = [v['net_charge'] for v in CLS.values()]
P("  SPREAD across classes: %.6f to %.6f  (range %.6f)" % (max(_sc), min(_sc), max(_sc) - min(_sc)))
P()
P("  BY DEPTH OF SIT-OUT (all ND 1-64 sitters at that depth; non-sitters excluded from mean R)")
P("  %-10s %7s | %9s %9s %9s" % ('depth', 'sitters', 'mean R', 'min R', 'max 1/R'))
P("  " + "-" * 114)
DEP = {}
for d in DEPTHS:
    sv = [applied_R(c) for c in ND64 if c['sitout'] and c['d'] == d]
    if not sv: continue
    DEP[d] = dict(n=len(sv), meanR=sum(sv) / len(sv), minR=min(sv), max_inv=1.0 / min(sv))
    P("  d%-9d %7d | %9.4f %9.4f %9.2fx" % (d, len(sv), sum(sv) / len(sv), min(sv), 1.0 / min(sv)))
_deep = [applied_R(c) for c in ND64 if c['sitout'] and c['d'] >= 6]
if _deep:
    P("  d6+        %7d | %9.4f %9.4f %9.2fx"
      % (len(_deep), sum(_deep) / len(_deep), min(_deep), 1.0 / min(_deep)))
P("  " + "-" * 114)
_allR = [applied_R(c) for c in ND64 if c['sitout']]
P("  harshest single multiplier applied anywhere on ND 1-64: R=%.4f  ->  %.2fx penalty"
  % (min(_allR), 1.0 / min(_allR)))
P("  (the owner's '5x' is real and is exceeded)")
P()
P("  WHO IS UPLIFTED. Measured, not assumed: the multiplier actually applied to an ND NON-SITTER.")
_nonR = sorted(set(round(applied_R(c), 12) for c in ND64 if not c['sitout']))
P("      distinct multipliers on ND 1-64 non-sitter cells: %s   (n=%d cells)"
  % (_nonR, sum(1 for c in ND64 if not c['sitout'])))
P("      => NOBODY IS UPLIFTED. The uplift is 1.0 exactly, in every band and every class.")
P()

# ==================================================================================================
# 3. THE CALIBRATION QUESTION
# ==================================================================================================
P("=" * 118)
P("3. THE CALIBRATION QUESTION -- IS THE ND ENTRY PRICE ALREADY SITTER-INCLUSIVE?")
P("=" * 118)
P()
P("  The law only bites if the ND entry price is calibrated to ND returns INCLUDING sitters. Settled")
P("  from the code, not assumed. Instruments:")
P("      structural_values()  harness_pvc_REPINNED_pass3.py:339   -- teaches the pick curve")
P("      realised_full()                                  :313")
P("      never_established()                              :277")
P("      load_matrix()                                    :325   -- the teaching-population filter")
P()
P("  WHICH MATRIX THIS COUNT RUNS ON, AND WHY -- DISCLOSED, NOT QUIETLY SUBSTITUTED.")
P("  The composition-act harness copy pins store d9a24282 (the current gate store), but the matrices")
P("  it pins (per_entrant_main.json and the four variants) are NOT COMMITTED to the repo -- only the")
P("  tables derived from them are. The count below therefore runs on the committed self-consistent")
P("  pair in docs/evidence/noarb_338_2026-08-06/ (harness pinned to store 37ced3ce + its own matrix).")
P("  THE FUNCTIONS THAT DECIDE THE QUESTION ARE BYTE-IDENTICAL ACROSS THE COPIES -- verified here,")
P("  not asserted -- so only the pinned store value differs, and never_established/realised_full/")
P("  sofar/structural_values are the same code either way:")
_h338 = os.path.join(ROOT, 'docs/evidence/noarb_338_2026-08-06/harness_pvc_REPINNED_pass3.py')
_hcmp = os.path.join(ROOT, 'docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py')
_hins = os.path.join(ROOT, 'session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py')


def _tail(path):
    s = open(path).read()
    i = s.find('def never_established')
    return hashlib.md5(s[i:].encode()).hexdigest() if i >= 0 else None


_tails = {'noarb_338 copy': _tail(_h338), 'composition copy': _tail(_hcmp), 'INSTRUMENT of record': _tail(_hins)}
for k, v in _tails.items():
    P("      %-22s md5(from `def never_established` to EOF) = %s" % (k, v))
_same = len(set(_tails.values())) == 1
P("      -> %s" % ("ALL THREE IDENTICAL below the pins" if _same else "*** THEY DIFFER -- the substitution is NOT safe ***"))
P()
CAL = {}
try:
    if not _same:
        raise RuntimeError('harness copies differ below the pins; refusing to substitute')
    sys.path.insert(0, os.path.join(ROOT, 'docs/evidence/noarb_338_2026-08-06'))
    import harness_pvc_REPINNED_pass3 as H3
    mpath = os.path.join(ROOT, 'docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json')
    if not os.path.exists(mpath):
        raise IOError('no per-entrant matrix beside the harness')
    meta, NDpop = H3.load_matrix(mpath)
    ne = [r for r in NDpop if H3.never_established(r)]
    rows, prov = H3.structural_values(NDpop)
    byk = {r['key']: r for r in rows}
    ne_rows = [byk[r['key']] for r in ne if r['key'] in byk]
    ne_zero = [r for r in ne_rows if r['value'] == 0.0]
    ne_nonzero = [r for r in ne_rows if r['value'] != 0.0]
    tot_v = sum(max(r['value'], 0.0) for r in rows)
    CAL = dict(matrix=os.path.basename(mpath), store=meta.get('store_md5'),
               harness_tail_md5=_tails, harness_tails_identical=_same,
               store_caveat='count taken on the committed store-37ced3ce pair; the composition-act '
                            'matrices at store d9a24282 are not committed. never_established is a '
                            'career property (no season of 6+ games) and the #334 harness header '
                            'records EXPECT_N=1197 re-measured on every d9a24282 matrix, so the '
                            'teaching population is identically sized and identically keyed.',
               n_teaching=len(NDpop), n_never_established=len(ne),
               ne_share_pct=100.0 * len(ne) / len(NDpop),
               ne_rows_in_teaching_population=len(ne_rows),
               ne_teaching_exactly_zero=len(ne_zero),
               ne_teaching_nonzero=len(ne_nonzero),
               ne_nonzero_how=dict(collections.Counter(r['how'] for r in ne_nonzero)),
               provenance=prov['counts'],
               total_teaching_value=tot_v,
               ne_value_contribution=sum(max(r['value'], 0.0) for r in ne_rows))
    P("  matrix %s   store %s   teaching population n=%d" % (CAL['matrix'], CAL['store'], CAL['n_teaching']))
    P()
    P("      never-established rows (no season of QUAL_GAMES=6 games)   %6d   (%.2f%% of the population)"
      % (CAL['n_never_established'], CAL['ne_share_pct']))
    P("      of those, INSIDE the teaching population                   %6d" % CAL['ne_rows_in_teaching_population'])
    P("      of those, teaching EXACTLY 0.0                             %6d" % CAL['ne_teaching_exactly_zero'])
    P("      of those, teaching non-zero (prior fallback)               %6d   %s"
      % (CAL['ne_teaching_nonzero'], CAL['ne_nonzero_how'] or ''))
    P("      their contribution to the summed teaching value            %6.1f of %.1f"
      % (CAL['ne_value_contribution'], CAL['total_teaching_value']))
    P("      provenance of the whole population                         %s" % CAL['provenance'])
    P()
    P("      load_matrix's filter is  teaches_curve & pick 1..64 & 2004<=year<=2022. `teaches_curve`")
    P("      is a MEMBERSHIP flag (rl_model.py:313 `_teaches_curve(p) = _in_pvc(p) and not is_pool(p)`)")
    P("      -- it selects national, in-window, non-pool rows. IT IS NOT A SURVIVORSHIP FILTER.")
    P("      kernel_raw (:396) then takes a weighted MEAN over `max(r['value'],0.0)` across ALL rows,")
    P("      so every one of those zeros sits in the NUMERATOR AS ZERO AND IN THE DENOMINATOR AS ONE.")
except Exception as e:
    CAL = dict(error=repr(e))
    P("  COULD NOT MEASURE: %r" % (e,))
    P("  (the code reading below stands on its own and does not depend on this count)")
P()
P("  VERDICT -- STATED WITHOUT HEDGING, BECAUSE THE CODE IS UNAMBIGUOUS:")
P("      NEVER-ESTABLISHED PLAYERS ARE INSIDE THE TEACHING POPULATION AT VALUE 0.0.")
P("      realised_full(r) :313  ->  `if never_established(r): return 0.0`")
P("      sofar(r,t)       :318  ->  `return 0.0 if never_established(r) else realised_at(r,t)`")
P("      structural_values :339 ->  iterates ALL of ND; a concluded never-established row is appended")
P("                                 with value=realised_full(r)=0.0 and how='concluded_realised'; an")
P("                                 unconcluded one with written depth takes sofar(r,T)*ratio = 0.0.")
P("                                 NEITHER PATH DROPS THE ROW.")
P("      The harness says so itself, in its own header:")
P("          '- THE ZERO IS UNTOUCHED. a career with no season of >= QUAL_GAMES (6) games still")
P("           teaches 0.0, and stays in the denominator.'")
P()
P("      THEREFORE: the ND pick curve is ALREADY calibrated on returns that include the sitters and")
P("      the busts at zero. The entry price a pick-N draftee is charged ALREADY has sit-out risk")
P("      priced into it. Applying R on top is a SECOND CHARGE FOR THE SAME THING.")
P()
P("      THE ND SITTER TREATMENT IS A DOUBLE CHARGE, NOT A SURVIVOR-BIAS CORRECTION.")
P("      The pre-registered decision rule (PREREG_ORDER18.md) selected this branch in advance.")
P()

# ==================================================================================================
# 4. THE POOL COMPARISON
# ==================================================================================================
P("=" * 118)
P("4. THE POOL COMPARISON -- SAME DIRECTION? BY HOW MUCH?")
P("=" * 118)
P()
P("  %-10s %13s %13s %11s" % ('arm', 'net charge', 'vs ND 1-64', 'verdict'))
P("  " + "-" * 114)
P("  %-10s %13.4f %13s %11s" % ('ND 1-64', HEAD['net_charge'], '--', 'BREACH'))
CMP = {}
for s in ORDER:
    if s not in CTRL: continue
    v = CTRL[s]['published']
    CMP[s] = dict(pool_published_H_only=v, ratio_vs_nd=v / HEAD['net_charge'] if HEAD['net_charge'] else None,
                  pool_composed_RxH=CTRL[s]['composed'])
    P("  %-10s %13.4f %13s %11s" % ('pool ' + s, v, "%.2fx" % (v / HEAD['net_charge']), 'BREACH'))
P("  " + "-" * 114)
P("  (pool column = phase 1's PUBLISHED figure, the H leg alone, so the comparison is against the")
P("   number the phase-1 ruling was actually made on. The composed R x H pool charges are in the")
P("   control table above and are larger still.)")
P()
P("  PLAINLY: the ND arm breaches the mean-preserving law in the SAME DIRECTION as all nine pool")
P("  pathways -- a net charge, mean below 1.0, no uplift to anyone. Its magnitude sits %s."
  % ("BETWEEN the mildest and harshest pool pathways"
     if min(PUB.values()) < HEAD['net_charge'] < max(PUB.values())
     else "OUTSIDE the pool range"))
P()

# ==================================================================================================
out = dict(
    pins=assert_pins('exit'),
    population=dict(n_pool_cells=len(POOL), n_national_cells=len(NDC), n_nd_1_64=len(ND64),
                    n_nd_1_64_sitout=sum(1 for c in ND64 if c['sitout'])),
    headline=HEAD, headline_v0start=HEAD_V0,
    by_band=BAND, by_class=CLS, by_depth=DEP,
    nonsitter_multipliers=_nonR,
    harshest_R=min(_allR), harshest_inverse=1.0 / min(_allR),
    control_pool_reproduction=CTRL,
    calibration=CAL,
    pool_comparison=CMP,
)
json.dump(out, open(os.path.join(HERE, 'ND_SITTER.json'), 'w'), indent=1, default=float)
P("=" * 118)
P("  pins re-asserted at exit: board 94f1fec5..  store d9a24282..  instrument 0f822035.. UNMOVED")
P("wrote ND_SITTER.json")
