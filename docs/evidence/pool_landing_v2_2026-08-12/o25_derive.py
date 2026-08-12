"""ORDER 25 -- THE DERIVATION, ON THE LANDED DELIVERY. Carried from ORDER 23's o23_derive.py.

ORDER 23's file is carried BYTE FOR BYTE below the pins. Its whole construction -- the arm-split
strata and their split=False control, the freshly measured target, the uniform K=15 layer 1, the
layer 2 keyed on pathway x position with the n>=20 sampling bar and the K=10 whole-pool borrow, the
RULE 2 residual group, the per-pathway renormalisation, the entry-anchor denominator and the 1e-9
reconciliation -- is ORDER 22's, which is phase 1's, and NONE of it changes here.

TWO THINGS CHANGE, AND ONLY TWO, both of them facts about the tree rather than about the method:

  1. THE PINS ARE THIS BRANCH'S. The board this branch carries is ORDER 23's landed board
     665311ca, not main's 1dbd1480; the store and the instrument are unmoved from main and are
     pinned at exactly the same values ORDER 23 pinned them at. The instrument pin
     0f8220351c64c56ccfa90c60edcdfa5f is the one the ORDER 25 brief names.

  2. THE LEVELS FILE MAY CARRY THE ND65+ LEVEL ALONE. Nothing else.

WHAT DOES **NOT** CHANGE, AND IS WORTH SAYING BECAUSE IT IS THE POINT OF THE ORDER. The delivery the
matrix was emitted under is different -- ORDER 23 measured a matrix built with the career-state
delivery and a flat pathway premium; ORDER 25 measures a matrix built with current-state delivery and
a quality-conditioned premium against amended pars. THE MEASURING INSTRUMENT IS UNCHANGED BETWEEN
THEM. That is deliberate: if the instrument moved with the engine, the two acts' numbers could not be
compared, and the whole re-truing would be unfalsifiable.

    usage: o25_derive.py <matrix.json> <levels.json|CHECKOUT> <out.json> [label] [--basis anchor|v0]
"""
import sys, json, os, collections, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, ROOT + '/docs/evidence/composition_2026-08-10/noarb')
sys.path.insert(0, ROOT + '/docs/evidence/par_adoption_2026-08-12/ndprofile')
import harness_pvc_REPINNED_pass3 as H          # the PINNED harness -- imported, never written
import harness_armsplit as A                    # ORDER 20's arm-split stratum key -- imported, never written

MATRIX = sys.argv[1]
LEVELS = sys.argv[2]
OUTJS = sys.argv[3]
ARGS = [a for a in sys.argv[4:] if not a.startswith('--')]
LABEL = ARGS[0] if ARGS else os.path.basename(MATRIX)
BASIS = sys.argv[sys.argv.index('--basis') + 1] if '--basis' in sys.argv else 'anchor'
assert BASIS in ('anchor', 'v0')

K_LAYER1 = 15.0     # OWNER-RULED, UNIFORM ACROSS EVERY PATHWAY (2026-08-12)
K_LAYER2 = 10.0     # ruled: K_336 / K_338, the constant for this exact operation
NMIN_CELL = 20      # a cell is "sampled" at n >= 20
TOL = 1e-9

POS6 = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
P = print


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


# ---- PINS, COMPUTED NEVER HARDCODED ------------------------------------------------------------
PINS = {'board': ROOT + '/data/rl_build/rl_app_data.json',
        'store': ROOT + '/engine/rl_after/rl_model_data.json',
        'instrument noarb_table_338.py': ROOT + '/docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
        'harness_pvc_REPINNED_pass3.py': ROOT + '/docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py',
        'harness_armsplit.py': ROOT + '/docs/evidence/par_adoption_2026-08-12/ndprofile/harness_armsplit.py'}
EXPECT = {'board': '665311ca72576df6ff0bbf6dfd007739',
          'store': 'd9a24282357cf3083b1640466e3ecd83',
          'instrument noarb_table_338.py': '0f8220351c64c56ccfa90c60edcdfa5f'}
PINMD5 = {k: md5(v) for k, v in PINS.items()}
for k, want in EXPECT.items():
    assert PINMD5[k] == want, "PIN MOVED: %s = %s, expected %s" % (k, PINMD5[k], want)


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


M = json.load(open(MATRIX))
R = M['recs']
elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]

# ---- THE LEVELS IN FORCE, and the entry-anchor denominator they define -------------------------
_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']; CURVE = _V2['curve']
# ORDER 25: ORDER 23 RETIRED the live key, deliberately, so nothing can silently re-cap. The
# retired pick is read from its dated historical name and is used for REPORTING ONLY -- the
# effective ND65+ level is the stored level verbatim, exactly as the engine reads it.
_ND65B = CUR['signed_nd65_plus']
assert 'cap_against_curve_pick' not in _ND65B, \
    'the ND65+ cap key is live again -- the ORDER 23 retirement has been undone'
CAPPK = int(_ND65B['cap_against_curve_pick_REMOVED_2026_08_12'])
CAP = float(CURVE[str(CAPPK)])
if LEVELS == 'CHECKOUT':
    IN_FLAT = dict(CUR['signed_flat']); IN_RD = dict(CUR['signed_rd_positional'])
    IN_ND65 = float(CUR['signed_nd65_plus']['measured_k15'])
else:
    Lv = json.load(open(LEVELS))
    IN_FLAT = dict(Lv['signed_flat']); IN_RD = dict(Lv['signed_rd_positional'])
    IN_ND65 = float(Lv['nd65_measured_k15'])
# ORDER 23 (owner ruling 5262928754, 2026-08-12): THE CAP IS REMOVED. The engine now reads the
# stored level verbatim, so the denominator this file divides ND>64 by is that level and not
# curve[64]. SUPERSEDED: ND65_EFF = min(IN_ND65, CAP).
ND65_EFF = IN_ND65
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])

# the engine's own lookup: rl_model.py:1423-1427 (int truncation) and the ND65+ cap law
LEVI = {k: int(float(v)) for k, v in IN_FLAT.items()}
LEVI['ND65+'] = int(ND65_EFF)
for k, v in IN_RD.items(): LEVI['RD:' + k] = int(float(v))


def division(r):
    """rl_model.py:1432-1446, reproduced. RD keys on future_position, which the engine asserts equals
    gfut(p) -- the matrix's `pos` field -- for every RD row at build time."""
    t = r.get('type')
    if t == 'RD': return 'RD:' + r['pos']
    if t == 'ND': return 'ND65+'
    return t


def anchor_of(r):
    """entry_anchor(p): the signed level x _PL_F for a pool row (_b_factor == 1.0 exactly),
       v0_start otherwise -- which IS entry_anchor for a national row."""
    if r.get('is_pool_engine'):
        d = division(r)
        if d in LEVI: return LEVI[d] * PL_F
    return float(r['v0'])

# ---- CONTROL: split=False reproduces the pinned harness value-for-value ------------------------
_pin_rows, _ = H.structural_values(elig)
_flat_rows, _ = A.structural_values(elig, split=False)
_bad = [(a['key'], a['value'], b['value']) for a, b in zip(_pin_rows, _flat_rows) if a['value'] != b['value']]
assert not _bad, "CONTROL FAILED -- armsplit split=False does not reproduce the pinned harness: %s" % _bad[:4]

allrows, prov = A.structural_values(elig, split=True)
SV = {r['key']: row for r, row in zip(elig, allrows)}
VAL = lambda r: SV[r['key']]['value']
V0START = lambda r: float(r['v0'])
V0 = anchor_of if BASIS == 'anchor' else V0START


def profile(sub, den=None):
    """The ruled D3 measure: SUM structural_value / SUM entry-price. Entry-weighted by construction."""
    if not sub: return float('nan')
    f = den or V0
    d = sum(f(r) for r in sub)
    return sum(VAL(r) for r in sub) / d if d else float('nan')


# ---- THE NATIONAL TARGET, on the ENGINE's own arm classification --------------------------------
ND = [r for r in elig if not r.get('is_pool_engine') and r.get('type') == 'ND'
      and r.get('raw_pick') and 1 <= r['raw_pick'] <= 64]
NDp = profile(ND)
POOL = [r for r in elig if stream(r) in ORDER]
POOLp = profile(POOL)

P("=" * 122)
P("ORDER 25 DERIVATION (landed delivery; ND65+ UNCAPPED)   label=%s   matrix=%s (%s)" % (LABEL, os.path.basename(MATRIX), md5(MATRIX)[:8]))
P("=" * 122)
P("  matrix meta: engine_head=%s  store_md5=%s  recs=%d  eligible=%d"
  % (M['meta'].get('engine_head', '?')[:8], str(M['meta'].get('store_md5'))[:8], len(R), len(elig)))
P("  pins (computed, not hardcoded): " + " · ".join("%s %s" % (k.split()[0], v[:8]) for k, v in PINMD5.items()))
P("  strata: ARM-SPLIT S[(arm,pos,tenure)] (ORDER 20). CONTROL PASS -- split=False reproduces the")
P("          pinned harness on all %d eligible rows, value for value." % len(elig))
P("  completion provenance %s  fallback %.3f%%" % (prov['counts'], prov['fallback_share_pct']))
P()
P("  DENOMINATOR (the entry price each arm actually pays): BASIS = %s" % BASIS.upper())
P("      pool rows     -> %s" % ('entry_anchor = signed level x _PL_F (%.4f)' % PL_F if BASIS == 'anchor'
                                 else 'v0_start (the directive/phase-1 literal instrument)'))
P("      national rows -> v0_start, which IS entry_anchor for them")
P()
P("  *** THE TARGET, MEASURED FRESH ON THIS ENGINE ***")
P("      national arm profile (engine arm, picks 1-64, n=%d) = %.10f" % (len(ND), NDp))
P("      ALL POOL profile                          (n=%d) = %.10f" % (len(POOL), POOLp))
P("      pool delivers %.6f of what the national arm delivers per unit of entry price." % (POOLp / NDp))
P()
_alt = 'v0' if BASIS == 'anchor' else 'anchor'
_altf = V0START if BASIS == 'anchor' else anchor_of
P("  THE OTHER BASIS, PRINTED SO THE DEPARTURE IS VISIBLE (basis=%s):" % _alt.upper())
P("      national target %.10f (IDENTICAL -- entry_anchor == v0_start for a national row)"
  % profile(ND, _altf))
P("      ALL POOL       %.10f   ->  pool/target = %.6f"
  % (profile(POOL, _altf), profile(POOL, _altf) / profile(ND, _altf)))
P("      SUM pool entry price:  this basis %s   other basis %s"
  % (format(round(sum(V0(r) for r in POOL)), ','), format(round(sum(_altf(r) for r in POOL)), ',')))
P()

# =====================================================================================
# LAYER 1 -- UNIFORM K=15 SHRINKAGE, EVERY PATHWAY
# =====================================================================================
P("=" * 122)
P("LAYER 1 -- THE ALL-IN VALUE PER PATHWAY.  UNIFORM K=%g SHRINKAGE TOWARD THE WHOLE-POOL VALUE." % K_LAYER1)
P("=" * 122)
P('  Owner verbatim (2026-08-12): "K=15 was across the board, not PDS."   w = n/(n+15).')
P("  shrunk profile = w * own profile + (1-w) * ALL-POOL profile;  lambda = shrunk / target.")
P()
P("  %-8s %5s %8s | %11s %10s | %11s %10s | %12s" %
  ('pathway', 'n', 'w', 'raw profile', 'raw lam', 'shrunk prof', 'shrunk lam', 'S entry now'))
P("  " + "-" * 118)
L1 = {}
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    pr = profile(sub); n = len(sub)
    w = n / (n + K_LAYER1)
    sh = w * pr + (1 - w) * POOLp
    L1[s] = dict(n=n, profile=pr, shrunk=sh, lam=sh / NDp, lam_raw=pr / NDp, w=w,
                 entry_now=sum(V0(r) for r in sub))
    P("  %-8s %5d %8.4f | %11.6f %10.6f | %11.6f %10.6f | %12s" %
      (s, n, w, pr, pr / NDp, sh, sh / NDp, format(round(L1[s]['entry_now']), ',')))
P("  " + "-" * 118)
P("  %-8s %5d %8s | %11.6f %10.6f | %11s %10s | %12s" %
  ('ALL POOL', len(POOL), '-', POOLp, POOLp / NDp, '(donor)', '', format(round(sum(V0(r) for r in POOL)), ',')))
P()

# =====================================================================================
# THE BORROW DONOR
# =====================================================================================
P("=" * 122)
P("THE BORROW DONOR -- WHOLE-POOL POSITIONAL SHAPE (ruled whole-pool-only; ND excluded ON MEASUREMENT)")
P("=" * 122)
SHAPE = {}
P("  %-6s %6s %12s %12s" % ('pos', 'n', 'profile', 'shape'))
for p in POS6:
    g = [r for r in POOL if r.get('pos') == p]
    pr = profile(g)
    SHAPE[p] = pr / POOLp
    P("  %-6s %6d %12.6f %12.6f" % (p, len(g), pr, SHAPE[p]))
P()

# =====================================================================================
# LAYER 2 -- CELLS
# =====================================================================================
P("=" * 122)
P("LAYER 2 -- CELL CENSUS AND OWN-OUTCOME PROFILES.  KEYS: PATHWAY x POSITION x AGE ONLY.")
P("=" * 122)
P("  No pick axis and none invented: effpk == POOL_PICK == 65 for every pool row (isolation law, §0A).")
P("  The AGE key is the multiplicative _b_shape/_b_factor leg, FLAT at 1.0 by ORDER 9 and not wired here (D7).")
P("  A cell is SAMPLED at n >= %d and derives from its own outcomes." % NMIN_CELL)
P()
CELLS = {}
P("  %-8s %5s |" % ('pathway', 'n') + "".join("%15s" % p for p in POS6) + " | sampled")
P("  " + "-" * 118)
NSAMP = 0
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    row = {}; line = ""; ns = 0
    for p in POS6:
        g = [r for r in sub if r.get('pos') == p]
        samp = len(g) >= NMIN_CELL
        row[p] = dict(n=len(g), rows=g, sampled=samp, own=profile(g) if g else float('nan'),
                      e=sum(V0(r) for r in g))
        if samp:
            ns += 1; line += "%10.4f/%-4d" % (row[p]['own'] / NDp, len(g))
        else:
            line += "%10s/%-4d" % ('-', len(g))
    CELLS[s] = row; NSAMP += ns
    P("  %-8s %5d |" % (s, len(sub)) + line + " | %d of 6" % ns)
P("  " + "-" * 118)
P("  SAMPLED CELLS ACROSS THE POOL: %d of 54.   (entries are lambda = own profile / target, n after the slash)" % NSAMP)
P()


def recon(pathway, cells):
    Ps = L1[pathway]['lam']
    lhs = sum(e * l for e, l in cells)
    rhs = sum(e for e, _ in cells) * Ps
    denom = abs(rhs) if abs(rhs) > 0 else 1.0
    return abs(lhs - rhs) / denom, lhs, rhs


P("=" * 122)
P("THE RECONCILIATION TEST, per pathway, tolerance %g RELATIVE, ENTRY-WEIGHTED IN BOTH LAYERS" % TOL)
P("=" * 122)
P("  RULE 1 (diagnostic): sampled cells own; unsampled remainder carries THE PATHWAY VALUE.")
P("  RULE 2 (ruled):      sampled cells own; unsampled remainder is ITS OWN RESIDUAL GROUP.")
P()
P("  %-8s %8s | %14s %9s | %14s %9s" % ('pathway', 'sampled', 'RULE 1 resid', 'verdict', 'RULE 2 resid', 'verdict'))
P("  " + "-" * 118)
RULE = {}
for s in ORDER:
    row = CELLS[s]
    samp = [p for p in POS6 if row[p]['sampled']]
    unsamp = [p for p in POS6 if not row[p]['sampled']]
    rem_rows = [r for p in unsamp for r in row[p]['rows']]
    rem_e = sum(V0(r) for r in rem_rows)
    c1 = [(row[p]['e'], row[p]['own'] / NDp) for p in samp]
    if rem_e > 0: c1 = c1 + [(rem_e, L1[s]['lam'])]
    r1, _, _ = recon(s, c1)
    c2 = [(row[p]['e'], row[p]['own'] / NDp) for p in samp]
    if rem_e > 0: c2 = c2 + [(rem_e, profile(rem_rows) / NDp)]
    r2, _, _ = recon(s, c2)
    RULE[s] = dict(sampled=len(samp), rule1=r1, rule2=r2, rem_n=len(rem_rows), rem_e=rem_e,
                   rem_profile=(profile(rem_rows) if rem_rows else float('nan')))
    P("  %-8s %8s | %14.2e %9s | %14.2e %9s" %
      (s, "%d of 6" % len(samp), r1, "PASS" if r1 <= TOL else "FAIL", r2, "PASS" if r2 <= TOL else "FAIL"))
P()
P("  %-8s %8s %12s %14s %14s" % ('pathway', 'rem n', 'rem entry', 'rem profile', 'pathway value'))
for s in ORDER:
    if RULE[s]['rem_n'] and RULE[s]['sampled']:
        P("  %-8s %8d %12s %14.6f %14.6f" %
          (s, RULE[s]['rem_n'], format(round(RULE[s]['rem_e']), ','), RULE[s]['rem_profile'], L1[s]['shrunk']))
P()

# =====================================================================================
# THE SHIPPED CONSTRUCTION
# =====================================================================================
P("=" * 122)
P("THE SHIPPED CONSTRUCTION -- rule 2 + whole-pool borrow at K=%g + PER-PATHWAY RENORMALISATION" % K_LAYER2)
P("=" * 122)
P("    borrowed    v_c = w_c*own_c + (1-w_c)*(S_allin * shape_c),   w_c = n_c/(n_c+K)")
P("    measure     M   = SUM(e_c*v_c)/SUM(e_c)")
P("    renormalise v'_c = v_c * (S_allin / M)   ->   SUM(e_c*v'_c)/SUM(e_c) == S_allin EXACTLY")
P()
SHIPPED = {}
for s in ORDER:
    row = CELLS[s]; S = L1[s]['shrunk']; v = {}
    for p in POS6:
        n = row[p]['n']; w = n / (n + K_LAYER2)
        v[p] = (S * SHAPE[p]) if n == 0 else (w * row[p]['own'] + (1 - w) * (S * SHAPE[p]))
    e = {p: row[p]['e'] for p in POS6}; tot_e = sum(e.values())
    Mm = sum(e[p] * v[p] for p in POS6) / tot_e if tot_e else float('nan')
    k = S / Mm if Mm else 1.0
    vp = {p: v[p] * k for p in POS6}
    Mafter = sum(e[p] * vp[p] for p in POS6) / tot_e if tot_e else float('nan')
    SHIPPED[s] = dict(v=v, vprime=vp, e=e, M=Mm, k=k, Mafter=Mafter, S=S)

P("  %-8s %10s %10s %10s | %s" % ('pathway', 'S_allin', 'M pre', 'renorm k', 'renormalised cell lambda (vs target)'))
P("  %-8s %10s %10s %10s | %s" % ('', '', '', '', "".join("%10s" % p for p in POS6)))
P("  " + "-" * 118)
for s in ORDER:
    d = SHIPPED[s]
    P("  %-8s %10.6f %10.6f %10.6f | %s" %
      (s, d['S'], d['M'], d['k'], "".join("%10.4f" % (d['vprime'][p] / NDp) for p in POS6)))
P()
P("  RECONCILIATION OF THE SHIPPED CONSTRUCTION:")
P("  %-8s %18s %18s %14s %8s" % ('pathway', 'entry-wtd mean', 'S_allin', 'rel resid', 'verdict'))
P("  " + "-" * 118)
worst = 0.0; RES = {}
for s in ORDER:
    d = SHIPPED[s]
    r, lhs, rhs = recon(s, [(d['e'][p], d['vprime'][p] / NDp) for p in POS6])
    RES[s] = r; worst = max(worst, r)
    P("  %-8s %18.12f %18.12f %14.2e %8s" % (s, d['Mafter'], d['S'], r, "PASS" if r <= TOL else "FAIL"))
P("  " + "-" * 118)
P("  WORST RESIDUAL: %.2e   tolerance %g   -> %s" % (worst, TOL, "PASS" if worst <= TOL else "FAIL"))
P()

# =====================================================================================
# THE DERIVED LEVELS
# =====================================================================================
P("=" * 122)
P("THE DERIVED LEVELS -- CALIBRATION TARGETS, ITERATED ONTO, NEVER PASTED")
P("=" * 122)
P()
P("  THE LEVELS THAT PRODUCED THIS MATRIX (what the engine actually read -- ND65+ UNCAPPED by the\n  2026-08-12 ruling; the retired cap was curve[%d]=%g):" % (CAPPK, CAP))
P("    flat   " + " · ".join("%s %.4f" % (k, IN_FLAT[k]) for k in sorted(IN_FLAT)))
P("    RD     " + " · ".join("%s %.4f" % (k, IN_RD[k]) for k in sorted(IN_RD)))
P("    ND65+  stored %.4f -> effective %.4f  (CAP REMOVED; it would have %s at curve[%d]=%g)"
  % (IN_ND65, ND65_EFF, 'BOUND' if IN_ND65 > CAP else 'not bound', CAPPK, CAP))
P()
P("  v0 is a MACHINERY OUTPUT, not a stored curve. The levels below are the CALIBRATION TARGETS the")
P("  machinery is iterated onto -- what the level must become for the pathway to return the target.")
P("  next_level = level_in_force * lambda_measured  (the phase-1 construction; lambda < 1 lowers the level)")
P()
P("  LAYER 1 -- pathway levels (positionless; the engine's `signed_flat`, plus the ND65+ law)")
P("  %-8s %14s %12s %14s %11s" % ('pathway', 'level in force', 'shrunk lam', 'NEXT LEVEL', 'change'))
P("  " + "-" * 118)
NEXT_FLAT = {}; NEXT_ND65 = None
for s in ORDER:
    if s == 'RD':
        continue
    if s == 'ND>64':
        cur = ND65_EFF
    else:
        cur = float(IN_FLAT[s])
    lam = L1[s]['lam']; dv = cur * lam
    if s == 'ND>64': NEXT_ND65 = dv
    else: NEXT_FLAT[s] = dv
    P("  %-8s %14.4f %12.6f %14.4f %10.2f%%" % (s, cur, lam, dv, 100.0 * (dv / cur - 1)))
P("  %-8s %14s %12.6f %14s %11s   [RD carries NO flat level in the engine -- it prices positionally]"
  % ('RD', '(positional)', L1['RD']['lam'], '(see below)', ''))
P()
P("  LAYER 2 -- pathway x position (the load-bearing deliverable)")
P("  ONLY RD IS WIRABLE. The signed table carries positional cells for the rookie draft alone; the other")
P("  eight pathways carry ONE flat level each. Their derived positional cells are DERIVED AND REPORTED")
P("  below but CANNOT BE WIRED without new structure in the signed table -- an owner decision, not a build one.")
P()
NEXT_RD = {}
DERIVED_L2 = {}
for s in ORDER:
    d = SHIPPED[s]
    DERIVED_L2[s] = {}
    if s == 'RD':
        P("  RD  [WIRED -- signed_rd_positional]")
        P("    %-6s %14s %12s %14s %11s %7s" % ('pos', 'level in force', 'cell lam', 'NEXT LEVEL', 'change', 'n'))
        for p in POS6:
            cur = float(IN_RD[p]); lam = d['vprime'][p] / NDp; dv = cur * lam
            NEXT_RD[p] = dv; DERIVED_L2[s][p] = dv
            P("    %-6s %14.4f %12.6f %14.4f %10.2f%% %7d" % (p, cur, lam, dv, 100.0 * (dv / cur - 1), CELLS[s][p]['n']))
    else:
        base = ND65_EFF if s == 'ND>64' else float(IN_FLAT[s])
        nxt = NEXT_ND65 if s == 'ND>64' else NEXT_FLAT[s]
        P("  %s  [NOT WIRABLE -- reported only; the pathway ships its one flat level %.4f -> %.4f]" % (s, base, nxt))
        P("    %-6s %14s %12s %14s %7s" % ('pos', 'flat in force', 'cell lam', 'implied cell', 'n'))
        for p in POS6:
            lam = d['vprime'][p] / NDp; dv = base * lam
            DERIVED_L2[s][p] = dv
            P("    %-6s %14.4f %12.6f %14.4f %7d" % (p, base, lam, dv, CELLS[s][p]['n']))
P()

# =====================================================================================
# BOTH HEADLINE METRICS
# =====================================================================================
def yr4(sub):
    W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    num = den = 0.0
    for r in sub:
        Y = cohort(r) + 3
        if Y > W: continue
        yrs = r.get('yrs') or []; vp = r.get('vpath') or []
        if not yrs: v = 0.0
        elif Y < yrs[0]: continue
        elif Y > yrs[-1]: v = 0.0
        else:
            i = yrs.index(Y); v = 0.0 if vp[i] is None else float(vp[i])
        num += v; den += V0(r)
    return num / den if den else float('nan')


P("=" * 122)
P("BOTH HEADLINE METRICS -- the owner's ruling. NEITHER IS A TARGET; BOTH ARE READ.")
P("=" * 122)
P("  %-8s %5s | %16s %12s | %16s %12s" %
  ('pathway', 'n', 'CAREER PROFILE', 'vs target', 'YR4 / YR0', 'vs target'))
P("  " + "-" * 118)
nd_y4 = yr4(ND)
P("  %-8s %5d | %16.6f %12.6f | %16.6f %12.6f" % ('NATIONAL', len(ND), NDp, 1.0, nd_y4, 1.0))
Y4 = {}
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    y = yr4(sub); Y4[s] = y
    P("  %-8s %5d | %16.6f %12.6f | %16.6f %12.6f" % (s, len(sub), L1[s]['profile'], L1[s]['lam_raw'], y, y / nd_y4))
py4 = yr4(POOL)
P("  " + "-" * 118)
P("  %-8s %5d | %16.6f %12.6f | %16.6f %12.6f" % ('ALL POOL', len(POOL), POOLp, POOLp / NDp, py4, py4 / nd_y4))
P()

out = dict(
    basis=BASIS, label=LABEL, matrix=os.path.basename(MATRIX), matrix_md5=md5(MATRIX),
    engine_head=M['meta'].get('engine_head'), store_md5=M['meta'].get('store_md5'),
    pins=PINMD5, target_nd_profile=NDp, nd_n=len(ND), pool_profile=POOLp, pool_n=len(POOL),
    nd_yr4=nd_y4, pool_yr4=py4, yr4=Y4,
    K_layer1=K_LAYER1, K_layer2=K_LAYER2, nmin_cell=NMIN_CELL, tol=TOL, sampled_cells=NSAMP,
    layer1={s: {k: v for k, v in L1[s].items() if k != 'rows'} for s in L1},
    shape=SHAPE,
    cells={s: {p: dict(n=CELLS[s][p]['n'], sampled=CELLS[s][p]['sampled'],
                       own=CELLS[s][p]['own'], e=CELLS[s][p]['e']) for p in POS6} for s in CELLS},
    rule_diagnostics=RULE,
    shipped={s: dict(S=SHIPPED[s]['S'], k=SHIPPED[s]['k'], M=SHIPPED[s]['M'], Mafter=SHIPPED[s]['Mafter'],
                     lam={p: SHIPPED[s]['vprime'][p] / NDp for p in POS6},
                     e={p: SHIPPED[s]['e'][p] for p in POS6}) for s in SHIPPED},
    reconciliation=RES, worst_residual=worst,
    levels_in_force=dict(signed_flat=IN_FLAT, signed_rd_positional=IN_RD,
                         nd65_measured_k15=IN_ND65, nd65_effective=ND65_EFF, nd65_cap=CAP),
    next_levels=dict(signed_flat=NEXT_FLAT, signed_rd_positional=NEXT_RD, nd65_measured_k15=NEXT_ND65),
    derived_levels_layer2_reported=DERIVED_L2,
    provenance=prov,
)
json.dump(out, open(OUTJS, 'w'), indent=1, default=float)
P("wrote %s" % OUTJS)
