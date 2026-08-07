"""STAGE 5 TEACHING MEASUREMENT — the forward-ratio surface for the sit-out-path population.

READ-ONLY.  Teaching source: the FROZEN baseline walk-forward matrix
docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json (md5 b564b12e),
at the ruled baseline board b56bbdde.  NEVER re-emitted for teaching (Addendum 2).

Method (round-2 M2, extended to the tau=2/3 knots the directive requires MEASURED before the fit):
  For every (player, evaluation year Y) that the ENGINE routes through sitout_ev (ns==0 at Y),
  reconstructed under the emitter's own walk-forward as-of convention, record the mechanism state
  (tau, cumulative career games through Y, effective pick, retention class, R, lam, e_full,
  entry_anchor) and the REALIZED DISCOUNTED FUTURE read off the frozen matrix vpath:

      F = mean_k [ v(Y+k) / 1.0939**k ] ,  k = 1..KMAX, busts/out-of-window = 0.

  The honest anchor multiplier the cell implies, solving the engine's own blend for the anchor leg:

      G_row_num = F - lam*e_full           G_row_den = (1-lam)*R*A
      G(cell)   = sum(num) / sum(den)      (value-weighted; the frozen-lam read, no fixed point)

Emits the raw per-row table for the teach + the knot diagnostics.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s5_measure'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; ev = G['ev']; delisted = G['delisted']; cp = G['cp']
nseas_pro = G['nseas_pro']; v0_start = G['v0_start']; entry_anchor = G['entry_anchor']
_R_surf = G['_R_surf']; _sitout_cls = G['_sitout_cls']; _fEy = G['_fEy']
_prod_path = G['_prod_path']; _ped_prior = G['_ped_prior']; _surprise = G['_surprise']
LAM_SIT = G['LAM_SIT']; PED_BAR = G['PED_BAR']

MATRIX = os.environ.get('RL_MATRIX',
    REPO + '/docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json')
MMD5 = hashlib.md5(open(MATRIX, 'rb').read()).hexdigest()
assert MMD5 == 'b564b12e533119f49c2c6bb0c92a5d91', 'teaching matrix md5 mismatch: ' + MMD5
MX = json.load(open(MATRIX))
RECS = {(r['key'], r['type'], r['year']): r for r in MX['recs']}

DISC = 1.0939
KMAX = int(os.environ.get('RL_KMAX', '4'))
YR_LO, YR_HI = 2004, 2022          # round-2 measurement classes
FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}

def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]

def _min_tenure(p):
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2
def _debut_year(p):
    C = p.get('year')
    if C is None: return None
    return C if p.get('type') == 'MSD' else C + 1
def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)

# ---------------- walk-forward as-of scan: capture the sit-out-path state ----------------
ROWS = []
for Y in range(2004, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for p in players:
        C = p.get('year')
        if C is None or C > Y or not (YR_LO <= C <= YR_HI): continue
        try:
            if delisted(p): continue
            if nseas_pro(p, Y) != 0: continue          # not on the sit-out path
            fe = _fEy(Y, p)
            tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
            cls = _sitout_cls(MA.gfut(p)); pk = MA.effpk(p)
            R = _R_surf(cls, pk, tau)
            gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
            gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
            gp = min(gy / fe, 6.0)
            lam0 = float(np.interp(gp, [0, 1, 2, 3, 4, 5, 6], LAM_SIT))
            with contextlib.redirect_stdout(io.StringIO()):
                e_full = _prod_path(p, Y)
            A = entry_anchor(p)
            q = _ped_prior(p, Y, fe, tau, cls, pk)
            sur = _surprise(e_full, R * A, gp)
            lam = lam0 ** (1.0 + PED_BAR * (1.0 - q) + sur)
            price = (1.0 - lam) * R * A + lam * e_full
        except Exception as ex:
            continue
        ROWS.append(dict(key=p.get('key'), typ=p.get('type'), C=C, Y=Y, N=Y - C,
                         tau=float(tau), cls=cls, pk=int(pk), gy=float(gy), gcum=float(gcum),
                         gp=float(gp), R=float(R), A=float(A), lam=float(lam),
                         e_full=float(e_full), price=float(price), v0=float(v0_start(p))))
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

# ---------------- attach the realized discounted future off the FROZEN matrix ----------------
def rec_for(key, C):
    for t in ('ND', 'MSD', 'RD', 'PDA', 'PDN', 'PDS', 'SSP', 'UNR', 'IRE'):
        if (key, t, C) in RECS: return RECS[(key, t, C)]
    return None

kept = []
for r in ROWS:
    rec = rec_for(r['key'], r['C'])
    if rec is None: continue
    yrs = rec['yrs']; vp = rec['vpath']
    vmap = {y: (float(v) if v is not None else 0.0) for y, v in zip(yrs, vp)}
    ks = [k for k in range(1, KMAX + 1) if r['Y'] + k <= 2026]
    if not ks: continue
    F = float(np.mean([vmap.get(r['Y'] + k, 0.0) / (DISC ** k) for k in ks]))
    r2 = dict(r, F=F, nk=len(ks), realized={k: vmap.get(r['Y'] + k, 0.0) for k in ks})
    kept.append(r2)

print("sit-out-path rows scanned = %d ; with realized-future window = %d" % (len(ROWS), len(kept)))
json.dump(kept, open(os.environ.get('RL_OUT', '.') + '/s5_rows.json', 'w'))

# ---------------- diagnostics ----------------
def agg(rows):
    if not rows: return None
    num = sum(x['F'] - x['lam'] * x['e_full'] for x in rows)
    den = sum((1.0 - x['lam']) * x['R'] * x['A'] for x in rows)
    return dict(n=len(rows),
                G=(num / den if den > 0 else float('nan')),
                Fr=sum(x['F'] for x in rows) / sum(x['A'] for x in rows),
                pr=sum(x['price'] for x in rows) / sum(x['A'] for x in rows),
                Rb=sum(x['R'] * x['A'] for x in rows) / sum(x['A'] for x in rows),
                tau=float(np.mean([x['tau'] for x in rows])),
                lam=float(np.mean([x['lam'] for x in rows])))

print("\n%-28s %6s %8s %8s %8s %8s %8s" % ("cell", "n", "meanTau", "price/A", "F/A", "Rbar", "G"))
print("-" * 84)
def show(name, rows):
    a = agg(rows)
    if a: print("%-28s %6d %8.3f %8.4f %8.4f %8.4f %8.4f"
                % (name, a['n'], a['tau'], a['pr'], a['Fr'], a['Rb'], a['G']))

show("ALL", kept)
for lo, hi, nm in [(0.5, 1.5, "tau~1"), (1.5, 2.5, "tau~2"), (2.5, 3.5, "tau~3"),
                   (3.5, 4.5, "tau~4"), (4.5, 9.9, "tau5+")]:
    show(nm, [x for x in kept if lo <= x['tau'] < hi])
print()
for lo, hi, nm in [(0.5, 1.5, "tau~1"), (1.5, 2.5, "tau~2"), (2.5, 3.5, "tau~3")]:
    sub = [x for x in kept if lo <= x['tau'] < hi]
    show(nm + "  gcum==0", [x for x in sub if x['gcum'] == 0])
    show(nm + "  gcum 1-5", [x for x in sub if 1 <= x['gcum'] <= 5])
    show(nm + "  gcum 6-15", [x for x in sub if 6 <= x['gcum'] <= 15])
    show(nm + "  gcum 16+", [x for x in sub if x['gcum'] >= 16])
print()
for lo, hi, nm in [(1, 20, "pick 1-20"), (21, 40, "pick 21-40"), (41, 64, "pick 41-64"), (65, 999, "pool")]:
    show(nm, [x for x in kept if lo <= x['pk'] <= hi])
print()
for c in ('nonKPP', 'KPP', 'RUCK'):
    show("cls " + c, [x for x in kept if x['cls'] == c])
