"""ORDER 20B TASK 2 — THE v0-CHAIN LAWS ON THE FIXED ENGINE.

Reports `_v0_curve_assert` (the D14 gates), `_v0_surface_assert` (D14d) and `_ruc_prior_cap` binding,
HEAD vs FIX, from engine_probe.py dumps.

IT REPORTS EACH GATE TWICE, AND THE SECOND READING IS THE ONE THAT MATTERS:

  FROZEN   the shipped state. `v0_start` on the board path returns `_V0CURVE[...]`, the D14 surface,
           and that surface is FROZEN (`_v0surf_frozen == True`). A frozen artifact is a function of
           (pos, draft-age, pick) only, so D14a/D14b CANNOT move when the par surface moves. Their
           green here is TRUE BUT VACUOUS for the national arm, and must not be quoted as evidence
           that the fix leaves the v0 chain sound.
  REFIT    the same gates with RL_V0SURF_REFIT=1, which re-fits the D14 surface from the live roster's
           `_v0_raw` (_merged_recover.py:1735). This is the state an ADOPTION plus a re-bake would put
           the engine in, and it is where the gates are actually tested against the fix.

Run: python3 gates_report.py <probe_HEAD> <probe_FIX> [<probe_HEAD_refit> <probe_FIX_refit>] <out_prefix>
"""
import json, sys

args = sys.argv[1:]
PRE = args[-1]; files = args[:-1]
H = json.load(open(files[0])); X = json.load(open(files[1]))
HR = json.load(open(files[2])) if len(files) > 2 else None
XR = json.load(open(files[3])) if len(files) > 3 else None
P = print
OUT = {}

GATE_MEANING = {
    'cross_draft_maxdisp': ('D14a', 'same (pos,ageR,pick) -> identical V0* across draft years; law says 0.0', 0.0),
    'within_cell_inversions': ('D14b', 'within (pos,ageR,year): V0* non-increasing in pick; law says 0', 0),
    'kpp_depth_monotone': ('D14c', 'KPP-floored retention surface depth-monotone; law says True', True),
}

P("=" * 118)
P("ORDER 20B TASK 2 — THE v0-CHAIN LAWS ON THE FIXED ENGINE")
P("=" * 118)


def block(tag, h, x, note):
    P()
    P("  ---- %s ----" % tag)
    P("    %s" % note)
    a = h['gates']['v0_curve_assert']; b = x['gates']['v0_curve_assert']
    P("    %-8s %-30s %20s %20s   %s" % ('gate', 'quantity', 'HEAD', 'FIX', 'verdict'))
    res = {}
    for k, (gid, desc, law) in GATE_MEANING.items():
        va, vb = a.get(k), b.get(k)
        ok = (vb == law)
        flipped = (va == law) and (vb != law)
        verdict = 'GREEN' if ok else ('*** RED — BLOCKER ***' if flipped else 'RED (red on HEAD too)')
        res[gid] = {'quantity': k, 'head': va, 'fix': vb, 'law': law, 'green_on_fix': ok, 'flipped_red': flipped}
        P("    %-8s %-30s %20s %20s   %s" % (gid, k, va, vb, verdict))
    sa = h['gates'].get('v0_surface_assert', {}); sb = x['gates'].get('v0_surface_assert', {})
    for k in ('rising_steps_1_64', 'rising_steps_full_grid'):
        va, vb = sa.get(k), sb.get(k)
        ok = (vb == 0); flipped = (va == 0) and (vb != 0)
        res['D14d/' + k] = {'head': va, 'fix': vb, 'law': 0, 'green_on_fix': ok, 'flipped_red': flipped}
        P("    %-8s %-30s %20s %20s   %s" % ('D14d', k, va, vb,
          'GREEN' if ok else ('*** RED — BLOCKER ***' if flipped else 'RED (red on HEAD too)')))
    P("    %-8s %-30s %20s %20s   %s" % ('(info)', 'population (surface rows)', a.get('population'), b.get('population'), ''))
    P("    %-8s %-30s %20s %20s   %s" % ('(info)', 'pool_rows_excluded', a.get('pool_rows_excluded'), b.get('pool_rows_excluded'), ''))
    P("    REPORT-ONLY (whole-ND incl. pool rows; declared unsatisfiable by the 2026-08-10 population correction —")
    P("    they compare pool division-level prices against national surface prices, two different price objects):")
    for k in ('report_only_all_nd_maxdisp', 'report_only_all_nd_inversions'):
        P("    %-8s %-30s %20s %20s   %s" % ('', k, a.get(k), b.get(k), '' if a.get(k) == b.get(k) else 'MOVED'))
    return res


OUT['frozen'] = block('READING 1 — THE SHIPPED (FROZEN) STATE',
                      H, X,
                      "v0surf frozen: HEAD=%s FIX=%s. With the surface frozen, D14a/D14b are functions of "
                      "(pos,ageR,pick) alone" % (True, True))
if HR and XR:
    OUT['refit'] = block('READING 2 — WITH THE D14 V0 SURFACE RE-FIT (RL_V0SURF_REFIT=1)',
                         HR, XR,
                         "the state an ADOPTION + re-bake would produce. THIS is where the gates are "
                         "actually tested against the fix.")

# ---------------------------------------------------------------- ruc prior cap
P()
P("  ---- _ruc_prior_cap BINDING (V0 PRIOR SCAFFOLD cap, _merged_recover.py:1219) ----")
P("    population: every REAL RUCK row the board carries. `binds` = the ceiling cut, i.e. min() was active.")
P("    the ceiling itself is RUC_PRIOR_CAP * _cap_basis(p) * _ruc_head_v0(p) — par-independent.")


def rucblock(tag, h, x):
    hh = {(r.get('set'), r.get('key')): r for r in h['ruc_prior_cap'] if 'binds' in r}
    xx = {(r.get('set'), r.get('key')): r for r in x['ruc_prior_cap'] if 'binds' in r}
    K = [k for k in hh if k in xx]
    P()
    P("    %s" % tag)
    res = {}
    for a in ('NATIONAL', 'POOL'):
        sub = [k for k in K if (('POOL' if hh[k]['pool'] else 'NATIONAL') == a)]
        bh = sum(1 for k in sub if hh[k]['binds']); bx = sum(1 for k in sub if xx[k]['binds'])
        ch = sum(hh[k]['cut'] for k in sub); cx = sum(xx[k]['cut'] for k in sub)
        newb = [k for k in sub if xx[k]['binds'] and not hh[k]['binds']]
        rel = [k for k in sub if hh[k]['binds'] and not xx[k]['binds']]
        res[a] = {'n': len(sub), 'binds_head': bh, 'binds_fix': bx, 'cut_head': ch, 'cut_fix': cx,
                  'newly_binding': [hh[k]['name'] for k in newb], 'released': [hh[k]['name'] for k in rel]}
        P("      %-9s n=%-4d binds %d -> %d   total cut %9.1f -> %9.1f   newly-binding %d  released %d"
          % (a, len(sub), bh, bx, ch, cx, len(newb), len(rel)))
        for k in newb:
            P("          NEWLY BINDING  %-24s ep%-4s  v0_uncapped %8.1f -> %8.1f   ceiling %8.1f (unmoved)"
              % (hh[k]['name'], hh[k]['ep'], hh[k]['v0_uncapped'], xx[k]['v0_uncapped'], hh[k]['ceiling']))
        for k in rel:
            P("          RELEASED       %-24s ep%-4s  v0_uncapped %8.1f -> %8.1f   ceiling %8.1f (unmoved)"
              % (hh[k]['name'], hh[k]['ep'], hh[k]['v0_uncapped'], xx[k]['v0_uncapped'], hh[k]['ceiling']))
    moved = sum(1 for k in K if abs(hh[k]['ceiling'] - xx[k]['ceiling']) > 1e-9)
    P("      ceilings that moved: %d of %d  (the cap's HEIGHT is par-independent; what moves is what it is applied to)"
      % (moved, len(K)))
    res['ceilings_moved'] = moved
    return res


OUT['ruc_frozen'] = rucblock('shipped (frozen) state:', H, X)
if HR and XR: OUT['ruc_refit'] = rucblock('with the V0 surface re-fit:', HR, XR)

json.dump(OUT, open(PRE + '.json', 'w'), indent=1, default=str)
P()
P("  json -> %s.json" % PRE)
