"""ITEM C worked rows — the evidence weight w = G x Q, gated by z, and the released ceiling.

OBJECT CITATIONS (all verified by reading, then exercised live in this script):
  par surface     : par_at(F,pos,pick,T)  engine/forward_valuation/par_build.py:255
                    exposed as PR.par_at(pos,pick,T) engine/forward_valuation/par_redesign.py:68
                    live consumers: _par_prior  engine/rl_after/_merged_recover.py:306-308
                                    local name `par` engine/rl_after/_merged_recover.py:1925
                    draft-age -> tenure bridge: eff_ten  _merged_recover.py:309-311
                    draft age integer: _ageR  _merged_recover.py:1271
  entry anchor    : entry_anchor(p)  _merged_recover.py:1761-1765
                    -> v0_start(p)   _merged_recover.py:1737-1741 (the D14 V0*(pos,draft-age,pick) surface)
  current expect. : ev(p,Y)          _merged_recover.py:1895-1937 (wired ev; board = ev/1.0524)
  old cap         : entry_anchor (see DISCREPANCIES) ; alternates R_SURF _merged_recover.py:1104-1125,
                    RUC_PRIOR_CAP/_ruc_ceiling :1138/:1195-1201, staleness/mediocre :1929-1936
"""
import engine_load, math, json
g = engine_load.load()
MA = g['MA']; cp = g['cp']; PR = g['PR']; ev = g['ev']
entry_anchor = g['entry_anchor']; v0_start = g['v0_start']
eff_ten = g['eff_ten']; _ageR = g['_ageR']; PL_F = g['_PL_F']
RUC_PRIOR_CAP = g['RUC_PRIOR_CAP']; _cap_basis = g['_cap_basis']; _ruc_ceiling = g['_ruc_ceiling']
_R_surf = g['_R_surf']; _sitout_cls = g['_sitout_cls']
Y = 2026
G0 = 8.0
QMAX = 2.0
HS = [1.04, 1.0945, 1.13]

data = MA.data
def get(k): return next((p for p in data if p.get('key') == k), None)
def career_g(p): return sum(x['games'] for x in p['scoring'])
def sa_career(p):
    t = career_g(p)
    return None if t == 0 else sum(x['games'] * x['avg'] for x in p['scoring']) / t
def sa_latest(p):
    rows = [x for x in p['scoring'] if x['games'] > 0]
    return max(rows, key=lambda x: x['year'])['avg'] if rows else None

KMAX = int(cp.KMAX)

def par_set(p):
    pos = MA.gfut(p); pk = min(MA.effpk(p), KMAX)
    da = _ageR(p)                                   # engine's own DRAFT AGE integer
    T_age = int(min(max(da - 18 + 1, 1), 6))        # par(pos, DRAFT-AGE): the eff_ten bridge read at draft
    T_ten = int(min(max(PR.tenure(p, Y), 1), 6))    # engine's live tenure axis
    T_eff = int(min(max(eff_ten(p, Y, PR.tenure(p, Y)), 1), 6))
    return dict(pos=pos, pk=pk, draft_age=da,
                T_age=T_age, T_ten=T_ten, T_eff=T_eff,
                par_age=PR.par_at(pos, pk, T_age),
                par_T1=PR.par_at(pos, pk, 1),
                par_ten=PR.par_at(pos, pk, T_ten),
                par_eff=PR.par_at(pos, pk, T_eff))

def row(p, label, sa_override=None, g_override=None, note=''):
    ps = par_set(p)
    gg = career_g(p) if g_override is None else g_override
    sa = (sa_career(p) if sa_override is None else sa_override)
    anchor = entry_anchor(p)
    e = float(ev(p, Y))
    G = gg / (gg + G0)
    Q = min(max(sa / ps['par_age'], 0.0), QMAX)
    z = math.log(e / anchor)
    gate = min(max(math.exp(z), 0.0), 1.0)
    w = G * Q * gate
    old_cap = anchor
    out = dict(label=label, key=p['key'], player=p['player'], type=p.get('type'),
               pos=ps['pos'], pick_stored=p.get('pick'), effpk=MA.effpk(p),
               draft_year=p.get('year'), debut=cp.debutyr(p), draft_age=ps['draft_age'],
               age_2026=cp._age_asof(p, Y), g=gg, sa=sa, sa_latest=sa_latest(p),
               par_age=ps['par_age'], par_T1=ps['par_T1'], par_ten=ps['par_ten'],
               par_eff=ps['par_eff'], T_age=ps['T_age'], T_ten=ps['T_ten'], T_eff=ps['T_eff'],
               entry_anchor=anchor, entry_anchor_board=anchor / PL_F,
               e=e, e_board=e / PL_F, G=G, Q=Q, z=z, gate=gate, w=w,
               old_cap=old_cap, old_cap_board=old_cap / PL_F, note=note,
               scoring=p['scoring'])
    for H in HS:
        c = anchor * (1 + w * (H - 1))
        out['ceil_%s' % H] = c
        out['ceil_%s_board' % H] = c / PL_F
        out['binds_%s' % H] = c > old_cap + 1e-9
        out['margin_%s' % H] = c - old_cap
        out['ceil_vs_e_%s' % H] = c - e
    # alternate cap objects, for the record
    out['alt_cap_sitout_R'] = _R_surf(_sitout_cls(ps['pos']), MA.effpk(p),
                                      max(0.0, Y - cp.debutyr(p))) * anchor
    if ps['pos'] == 'RUCK':
        out['alt_cap_ruck_prior'] = RUC_PRIOR_CAP * _cap_basis(p)
        out['alt_cap_ruck_ceiling'] = _ruc_ceiling(p, Y)
    return out

ROWS = []
ROWS.append(row(get('noah-mraz'), '1 Mraz'))
ROWS.append(row(get('archie-ludowyke'), '2 Ludowyke (illustration)'))
ROWS.append(row(get('luke-beecken'), '3a 1-game-at-7 (exact sa=7.00)'))
ROWS.append(row(get('gerrick-weedon'), '3b 1-game-at-7, nearest ND in-curve row (sa=5.00)'))
ROWS.append(row(get('zeke-uwland'), '4 Uwland (top-pick faller)'))
ROWS.append(row(get('bodhi-uwland'), '4b Uwland (the other one — PDA, for the name-collision record)'))
ROWS.append(row(get('toby-conway'), '5 6-games-at-70 mid-pick'))
# THE SPIRIT TEST: hypothetical 1 game at 120, SAME position and draft age as row 5.
c = get('toby-conway')
ROWS.append(row(c, '5H hypothetical 1 game @120 (same player/pos/age as row 5)',
                sa_override=120.0, g_override=1,
                note='counterfactual: g and sa overridden; anchor/e/par are Conway\'s own'))

print(json.dumps(ROWS, indent=1, default=str))
