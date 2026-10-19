"""TASKS 2, 3 and 4 -- LAYER 1, LAYER 2, and THE RECONCILIATION TEST.

THE BASIS IS RULED (D3): the FULL CAREER PROFILE, measured by the pick curve's OWN function.
This file CALLS the harness rather than re-implementing it, so it cannot drift from the pick curve:

    harness_pvc_REPINNED_pass3.realised_full   (:313)   -- the per-player realised value
    harness_pvc_REPINNED_pass3.structural_values(:339)  -- the curve's own completion of live careers

The headline measure is PROFILE (B) in the directive's [PROFILE] table: the curve's own completion,
strata built on the WHOLE eligible cohort so a thin stream cannot fall back to its own entry price and
score 1.00 by construction.

    profile_X = SUM_X structural_value / SUM_X v0
    lambda_X  = profile_X / profile_ND1-64          ("vs ND": 1.0000 == returns what an ND pick returns
                                                     for the same money. The target is ND's OWN profile,
                                                     1.0252, NOT 1.00.)

LAYER 1 (task 2) -- one positionless value per pathway, every pathway including thin ones.
    PDS ALONE is shrunk toward the pool aggregate at K=15 (owner ruling: "Shrink PDS towards the
    pool"), w = n/(n+15). No other pathway is shrunk: every other pathway holds n >= 43.
    K=15 is the constant the signed pool level table was ITSELF built at (pvc_curve_v2.json
    pool_levels _doc: "VOR, K=15 toward the measured pool aggregate 235.8").

LAYER 2 (task 3) -- the player v0, keyed on PATHWAY x POSITION x AGE ONLY.
    THERE IS NO PICK AXIS AND NONE IS INVENTED: effpk returns the constant POOL_PICK=65 for every
    pool entrant, so a pick axis would be a fabricated dimension. The AGE key is the third key and is
    multiplicative (_b_shape / _b_factor, currently FLAT at 1.0 by ORDER 9); D7 is measured separately
    in phase1_age.py and this file's level table is the pathway x position object it multiplies.
    Cells at n >= 20 derive from their own outcomes. Thin cells borrow the WHOLE-POOL shape at K=10
    (donor ruled whole-pool-only by the D4 shared-signal pre-check, which FAILED for the national
    draft), then the pathway is RENORMALISED so it still averages its own all-in value.

THREE CONSTRUCTIONS ARE BUILT AND ALL THREE ARE REPORTED, because the directive's [RECON] finding is
that the choice between them is measurable rather than a matter of taste:
    RULE 1  sampled cells own; unsampled remainder carries THE PATHWAY VALUE      -> expected to FAIL
    RULE 2  sampled cells own; unsampled remainder is ITS OWN RESIDUAL GROUP      -> expected to PASS
    SHIPPED rule 2 + K=10 borrow + per-pathway renormalisation, all six cells     -> the deliverable

RECONCILIATION (task 4), the owner's law as a checkable identity, ENTRY-WEIGHTED IN BOTH LAYERS:
    PASS if  SUM_c (v0_c * lambda_c)  ==  (SUM_c v0_c) * P_s   within 1e-9 RELATIVE.
    It is an IDENTITY, not an approximation. Anything above float noise means the construction is
    broken, not that the data disagreed.

READ-ONLY. No emits. Does not touch the shipped configuration. Deterministic.
"""
import sys, json, os, collections, math

ROOT = '/home/user/afl-rl-engine'
sys.path.insert(0, ROOT + '/docs/evidence/composition_2026-08-10/noarb')
import harness_pvc_REPINNED_pass3 as H

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else 'SHIP'
M = json.load(open(f"{SP}/per_entrant_{BASE}.json"))
R = M['recs']

K_LAYER1 = 15.0     # ruled: the constant the pool level table was itself built at
K_LAYER2 = 10.0     # ruled: K_336 / K_338, the constant for this exact operation
NMIN_CELL = 20      # a cell is "sampled" at n >= 20
TOL = 1e-9

POS6 = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
allrows, prov = H.structural_values(elig)
SV = {r['key']: row for r, row in zip(elig, allrows)}

VAL = lambda r: SV[r['key']]['value']
V0 = lambda r: float(r['v0'])


def profile(sub):
    """The ruled measure: SUM structural_value / SUM v0.  Entry-weighted by construction."""
    if not sub: return float('nan')
    d = sum(V0(r) for r in sub)
    return sum(VAL(r) for r in sub) / d if d else float('nan')


P = print
P("=" * 118)
P("PHASE 1 -- LAYER 1, LAYER 2, RECONCILIATION.   base=%s   matrix n=%d   eligible n=%d" % (BASE, len(R), len(elig)))
P("=" * 118)
P("  measure : harness_pvc_REPINNED_pass3.realised_full (:313) via structural_values (:339)")
P("  basis   : the FULL CAREER PROFILE (D3 ruling). Year four is one consulted data point, not the basis.")
P("  strata  : built on the WHOLE eligible cohort -- completion provenance %s, fallback %.3f%%"
  % (prov['counts'], prov['fallback_share_pct']))
P()

ND = [r for r in elig if stream(r) == 'ND 1-64']
NDp = profile(ND)
POOL = [r for r in elig if stream(r) in ORDER]
POOLp = profile(POOL)
P("  ND 1-64 profile (THE CALIBRATION TARGET) = %.4f   n=%d" % (NDp, len(ND)))
P("  ALL POOL profile                          = %.4f   n=%d" % (POOLp, len(POOL)))
P("  pool delivers %.4f of what ND delivers per unit of entry price." % (POOLp / NDp))
P()

# =====================================================================================
# LAYER 1 -- the positionless all-in value per pathway
# =====================================================================================
P("=" * 118)
P("LAYER 1 -- THE POSITIONLESS ALL-IN VALUE PER PATHWAY   (task 2)")
P("=" * 118)
P("  PDS alone shrunk toward the pool aggregate at K=%g (owner ruling). w = n/(n+K)." % K_LAYER1)
P()
P("  %-8s %5s | %9s %9s | %9s %9s %8s | %9s" %
  ('pathway', 'n', 'profile', 'vs ND', 'shrunk', 'vs ND', 'w', 'S entry now'))
P("  " + "-" * 114)
L1 = {}
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    pr = profile(sub)
    n = len(sub)
    if s == 'PDS':
        w = n / (n + K_LAYER1)
        sh = w * pr + (1 - w) * POOLp
    else:
        w = 1.0
        sh = pr
    L1[s] = dict(n=n, profile=pr, shrunk=sh, lam=sh / NDp, lam_raw=pr / NDp, w=w,
                 entry_now=sum(V0(r) for r in sub))
    P("  %-8s %5d | %9.4f %9.4f | %9.4f %9.4f %8.4f | %9s" %
      (s, n, pr, pr / NDp, sh, sh / NDp, w, format(round(L1[s]['entry_now']), ',')))
P("  " + "-" * 114)
P("  %-8s %5d | %9.4f %9.4f | %9s %9s %8s | %9s" %
  ('ALL POOL', len(POOL), POOLp, POOLp / NDp, '', '', '', format(round(sum(V0(r) for r in POOL)), ',')))
P()
P("  PDS: profile %.4f -> %.4f shrunk (w=%.4f at n=%d). It is the ONLY pathway thin enough for"
  % (L1['PDS']['profile'], L1['PDS']['shrunk'], L1['PDS']['w'], L1['PDS']['n']))
P("  stream-level shrinkage to bite; every other pathway holds 43 players or more.")
P("  PDS ran 2007-2011 and takes no new entrants, so this moves historical prices only.")
P()

# =====================================================================================
# the whole-pool positional SHAPE -- the ruled donor
# =====================================================================================
P("=" * 118)
P("THE BORROW DONOR -- WHOLE-POOL POSITIONAL SHAPE (ruled whole-pool-only; ND excluded on measurement)")
P("=" * 118)
SHAPE = {}
P("  %-6s %6s %10s %10s" % ('pos', 'n', 'profile', 'shape'))
for p in POS6:
    g = [r for r in POOL if r.get('pos') == p]
    pr = profile(g)
    SHAPE[p] = pr / POOLp
    P("  %-6s %6d %10.4f %10.4f" % (p, len(g), pr, SHAPE[p]))
P()
P("  shape_c = pool_profile_c / pool_profile_all. The D4 pre-check FAILED for the national draft")
P("  (correlation -0.2350, 4 concordant pairs of 15), so ND is not a donor. The whole-pool shape is")
P("  dominated by RD (%d of %d pool players), which is a declared limit of the borrow, not a defect"
  % (L1['RD']['n'], len(POOL)))
P("  in it: a thin MSD ruck borrowing 'the pool ruck prior' is in practice borrowing the RD ruck prior.")
P()

# =====================================================================================
# LAYER 2 -- cells
# =====================================================================================
P("=" * 118)
P("LAYER 2 -- CELL CENSUS AND OWN-OUTCOME PROFILES   (task 3)")
P("=" * 118)
P("  keyed on PATHWAY x POSITION x AGE only. No pick axis: effpk == POOL_PICK == 65 for every pool row.")
P("  a cell is SAMPLED at n >= %d and derives from its own outcomes." % NMIN_CELL)
P()
CELLS = {}
P("  %-8s %5s |" % ('pathway', 'n') + "".join("%14s" % p for p in POS6) + " | sampled")
P("  " + "-" * 114)
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    row = {}
    line = ""
    ns = 0
    for p in POS6:
        g = [r for r in sub if r.get('pos') == p]
        samp = len(g) >= NMIN_CELL
        row[p] = dict(n=len(g), rows=g, sampled=samp,
                      own=profile(g) if g else float('nan'),
                      e=sum(V0(r) for r in g))
        if samp:
            ns += 1
            line += "%9.4f/%-4d" % (row[p]['own'] / NDp, len(g))
        else:
            line += "%9s/%-4d" % ('-', len(g))
    CELLS[s] = row
    P("  %-8s %5d |" % (s, len(sub)) + line + " | %d of 6" % ns)
P()
P("  (cell entries are lambda = own profile / ND, with n after the slash; '-' = below the n>=20 bar)")
P()

# =====================================================================================
# THE THREE CONSTRUCTIONS
# =====================================================================================


def recon(pathway, cells):
    """The owner's law as an identity. cells = list of (e_c, lam_c). Entry-weighted.
       PASS if SUM(e_c*lam_c) == (SUM e_c) * P_s  within TOL relative."""
    Ps = L1[pathway]['lam']
    lhs = sum(e * l for e, l in cells)
    rhs = sum(e for e, _ in cells) * Ps
    denom = abs(rhs) if abs(rhs) > 0 else 1.0
    return abs(lhs - rhs) / denom, lhs, rhs


P("=" * 118)
P("TASK 4 -- THE RECONCILIATION TEST, per pathway, tolerance %g relative, ENTRY-WEIGHTED IN BOTH LAYERS" % TOL)
P("=" * 118)
P()
P("  RULE 1 (diagnostic): sampled cells own; the unsampled remainder carries THE PATHWAY VALUE.")
P("  RULE 2 (ruled):      sampled cells own; the unsampled remainder is ITS OWN RESIDUAL GROUP.")
P()
P("  %-8s %8s | %14s %10s | %14s %10s" % ('pathway', 'sampled', 'RULE 1 resid', 'verdict', 'RULE 2 resid', 'verdict'))
P("  " + "-" * 114)
RULE = {}
for s in ORDER:
    row = CELLS[s]
    samp = [p for p in POS6 if row[p]['sampled']]
    unsamp = [p for p in POS6 if not row[p]['sampled']]
    rem_rows = [r for p in unsamp for r in row[p]['rows']]
    rem_e = sum(V0(r) for r in rem_rows)

    c1 = [(row[p]['e'], row[p]['own'] / NDp) for p in samp]
    if rem_e > 0: c1 = c1 + [(rem_e, L1[s]['lam'])]              # rule 1: remainder at pathway value
    r1, _, _ = recon(s, c1)

    c2 = [(row[p]['e'], row[p]['own'] / NDp) for p in samp]
    if rem_e > 0: c2 = c2 + [(rem_e, profile(rem_rows) / NDp)]   # rule 2: remainder as own group
    r2, _, _ = recon(s, c2)

    RULE[s] = dict(sampled=len(samp), rule1=r1, rule2=r2,
                   rem_n=len(rem_rows), rem_e=rem_e,
                   rem_profile=(profile(rem_rows) if rem_rows else float('nan')))
    P("  %-8s %8s | %14.2e %10s | %14.2e %10s" %
      (s, "%d of 6" % len(samp), r1, "PASS" if r1 <= TOL else "FAIL",
       r2, "PASS" if r2 <= TOL else "FAIL"))
P()
P("  WHY RULE 1 FAILS where it fails: the unsampled remainder's own outcome profile is NOT the")
P("  pathway average, so giving it the pathway value leaves the sampled cells' deviation unoffset.")
P()
P("  %-8s %8s %12s %14s %14s" % ('pathway', 'rem n', 'rem entry', 'rem profile', 'pathway value'))
for s in ORDER:
    if RULE[s]['rem_n'] and RULE[s]['sampled']:
        P("  %-8s %8d %12s %14.4f %14.4f" %
          (s, RULE[s]['rem_n'], format(round(RULE[s]['rem_e']), ','),
           RULE[s]['rem_profile'], L1[s]['shrunk']))
P()

# =====================================================================================
# THE SHIPPED CONSTRUCTION: rule 2 + K=10 borrow + renormalisation
# =====================================================================================
P("=" * 118)
P("THE SHIPPED CONSTRUCTION -- rule 2 + whole-pool borrow at K=%g + PER-PATHWAY RENORMALISATION" % K_LAYER2)
P("=" * 118)
P()
P("    borrowed   v_c = w_c*own_c + (1-w_c)*(S_allin * shape_c),   w_c = n_c/(n_c+K)")
P("    measure    M   = SUM(e_c*v_c)/SUM(e_c)")
P("    renormalise v'_c = v_c * (S_allin / M)      ->  SUM(e_c*v'_c)/SUM(e_c) == S_allin EXACTLY")
P()
P("  The renormalisation is MANDATORY and is not cosmetic: a pathway's position mix does not match the")
P("  pool's (UNR is 30 rucks of 59; IRE is 35 small defenders of 57), so an unrenormalised borrow drags")
P("  the pathway off its own measured level and silently breaks the reconciliation law.")
P()
SHIPPED = {}
for s in ORDER:
    row = CELLS[s]
    S = L1[s]['shrunk']
    v = {}
    for p in POS6:
        n = row[p]['n']
        w = n / (n + K_LAYER2)
        own = row[p]['own'] if n > 0 else 0.0
        if n == 0:
            v[p] = S * SHAPE[p]
        else:
            v[p] = w * own + (1 - w) * (S * SHAPE[p])
    # entry weights: cells with no players carry no entry weight and cannot affect the mean
    e = {p: row[p]['e'] for p in POS6}
    tot_e = sum(e.values())
    Mm = sum(e[p] * v[p] for p in POS6) / tot_e if tot_e else float('nan')
    k = S / Mm if Mm else 1.0
    vp = {p: v[p] * k for p in POS6}
    Mafter = sum(e[p] * vp[p] for p in POS6) / tot_e if tot_e else float('nan')
    SHIPPED[s] = dict(v=v, vprime=vp, e=e, M=Mm, k=k, Mafter=Mafter, S=S)

P("  %-8s %9s %9s %9s | %s" % ('pathway', 'S_allin', 'M pre', 'renorm k', 'renormalised cell lambda (vs ND)'))
P("  " + "-" * 114)
P("  %-8s %9s %9s %9s | %s" % ('', '', '', '', "".join("%9s" % p for p in POS6)))
for s in ORDER:
    d = SHIPPED[s]
    P("  %-8s %9.4f %9.4f %9.4f | %s" %
      (s, d['S'], d['M'], d['k'], "".join("%9.4f" % (d['vprime'][p] / NDp) for p in POS6)))
P()

P("  RECONCILIATION OF THE SHIPPED CONSTRUCTION (the one that would ship):")
P("  %-8s %16s %16s %14s %8s" % ('pathway', 'entry-wtd mean', 'S_allin', 'rel resid', 'verdict'))
P("  " + "-" * 114)
worst = 0.0
RES = {}
for s in ORDER:
    d = SHIPPED[s]
    cells = [(d['e'][p], d['vprime'][p] / NDp) for p in POS6]
    r, lhs, rhs = recon(s, cells)
    RES[s] = r
    worst = max(worst, r)
    P("  %-8s %16.10f %16.10f %14.2e %8s" %
      (s, d['Mafter'], d['S'], r, "PASS" if r <= TOL else "FAIL"))
P("  " + "-" * 114)
P("  WORST RESIDUAL ACROSS ALL PATHWAYS: %.2e   tolerance %g   -> %s"
  % (worst, TOL, "PASS" if worst <= TOL else "FAIL"))
P()

# =====================================================================================
# DERIVED LEVELS -- the calibration targets
# =====================================================================================
P("=" * 118)
P("THE DERIVED LEVELS -- CALIBRATION TARGETS, NOT VALUES TO PASTE")
P("=" * 118)
CUR = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
FLAT = dict(CUR['signed_flat'])
FLAT['RD'] = CUR['rd_division_level']
FLAT['ND>64'] = CUR['signed_nd65_plus']['measured_k15']
RDPOS = CUR['signed_rd_positional']
P()
P("  v0 is a MACHINERY OUTPUT (_v0_uncapped = raw_ev(p, debutyr-1) * iso_eff(...)), not a stored")
P("  curve. What this act changes is the machinery's INPUT: the per-pathway, per-position entry")
P("  levels in pvc_curve_v2.json pool_levels. The levels below are the TARGETS the machinery must be")
P("  iterated onto at adoption; they are not the machinery's outputs and are not pasted as such.")
P()
P("  LAYER 1 -- pathway levels (positionless)")
P("  %-8s %12s %10s %12s %12s" % ('pathway', 'level now', 'lambda', 'DERIVED', 'change'))
P("  " + "-" * 114)
DERIVED_L1 = {}
for s in ORDER:
    cur = FLAT.get(s)
    if cur is None: continue
    lam = L1[s]['lam']
    dv = cur * lam
    DERIVED_L1[s] = dv
    P("  %-8s %12.1f %10.4f %12.1f %11.1f%%" % (s, cur, lam, dv, 100.0 * (dv / cur - 1)))
P()
P("  LAYER 2 -- pathway x position levels (the load-bearing deliverable)")
P("  Today ONLY the rookie draft is positional; every other pathway carries one flat level. This act")
P("  derives all six cells for every pathway. It does NOT introduce the positional lens -- v0 already")
P("  carries positional differentiation from the general machinery -- it corrects the LEVEL of an")
P("  already-positional object with pathway-specific outcome history.")
P()
DERIVED_L2 = {}
for s in ORDER:
    base = RDPOS if s == 'RD' else None
    cur_flat = FLAT.get(s)
    P("  %s" % s)
    P("    %-6s %12s %10s %12s %12s %8s" % ('pos', 'level now', 'lambda', 'DERIVED', 'change', 'n'))
    d = SHIPPED[s]
    DERIVED_L2[s] = {}
    for p in POS6:
        cur = base[p] if base else cur_flat
        lam = d['vprime'][p] / NDp
        dv = cur * lam
        DERIVED_L2[s][p] = dv
        tag = '' if base else '  (new cell; was flat)'
        P("    %-6s %12.1f %10.4f %12.1f %11.1f%% %8d%s" %
          (p, cur, lam, dv, 100.0 * (dv / cur - 1), CELLS[s][p]['n'], tag))
P()

P("=" * 118)
P("HEADLINE METRICS -- BOTH, per the owner's ruling. Neither is a target.")
P("=" * 118)
P()


def yr4(sub):
    W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    num = den = 0.0
    for r in sub:
        Y = cohort(r) + 3
        if Y > W: continue
        yrs = r.get('yrs') or []; vp = r.get('vpath') or []
        if not yrs:
            v = 0.0
        elif Y < yrs[0]:
            continue
        elif Y > yrs[-1]:
            v = 0.0
        else:
            i = yrs.index(Y); v = 0.0 if vp[i] is None else float(vp[i])
        num += v; den += V0(r)
    return num / den if den else float('nan')


P("  %-8s %5s | %14s %14s | %14s %14s" %
  ('pathway', 'n', 'CAREER PROFILE', 'vs ND', 'YR4 / YR0', 'vs ND'))
P("  " + "-" * 114)
nd_y4 = yr4(ND)
P("  %-8s %5d | %14.4f %14.4f | %14.4f %14.4f" % ('ND 1-64', len(ND), NDp, 1.0, nd_y4, 1.0))
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    y = yr4(sub)
    P("  %-8s %5d | %14.4f %14.4f | %14.4f %14.4f" %
      (s, len(sub), L1[s]['profile'], L1[s]['lam_raw'], y, y / nd_y4))
py4 = yr4(POOL)
P("  " + "-" * 114)
P("  %-8s %5d | %14.4f %14.4f | %14.4f %14.4f" % ('ALL POOL', len(POOL), POOLp, POOLp / NDp, py4, py4 / nd_y4))
P()
P("  The two answer different questions -- did the whole career justify the price, and did it justify")
P("  the price at the peak -- and the gap between them IS the 'year four flatters the pool' finding.")
P()

out = dict(
    base=BASE, nd_profile=NDp, pool_profile=POOLp, nd_yr4=nd_y4, pool_yr4=py4,
    K_layer1=K_LAYER1, K_layer2=K_LAYER2, nmin_cell=NMIN_CELL, tol=TOL,
    layer1={s: {k: v for k, v in L1[s].items()} for s in L1},
    shape=SHAPE,
    cells={s: {p: dict(n=CELLS[s][p]['n'], sampled=CELLS[s][p]['sampled'],
                       own=CELLS[s][p]['own'], e=CELLS[s][p]['e']) for p in POS6} for s in CELLS},
    rule_diagnostics={s: RULE[s] for s in RULE},
    shipped={s: dict(S=SHIPPED[s]['S'], k=SHIPPED[s]['k'], M=SHIPPED[s]['M'],
                     lam={p: SHIPPED[s]['vprime'][p] / NDp for p in POS6}) for s in SHIPPED},
    reconciliation={s: RES[s] for s in RES}, worst_residual=worst,
    derived_levels_layer1=DERIVED_L1, derived_levels_layer2=DERIVED_L2,
    current_levels=dict(flat=FLAT, rd_positional=RDPOS),
)
for s in out['layer1']:
    out['layer1'][s].pop('rows', None)
json.dump(out, open(os.path.join(HERE, 'PHASE1_DERIVE.json'), 'w'), indent=1, default=float)
P("wrote PHASE1_DERIVE.json")
