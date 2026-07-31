#!/usr/bin/env python3
"""L2 — THE TWO WINDOW CANDIDATES, measured. #290, runbook L2 + Addendum A.1.

Run from /home/claude/rl_workspace/rl_after on the L1-exit substrate with E3 applied.

MEASURES BOTH, CHOOSES NEITHER. The owner words the window.

  candidate A  censor-aware-2003-inclusive : DRAFT_LO=2003
  candidate B  uniform 2004+               : DRAFT_LO=2004

For each: cell populations, gate classifications, surface deltas — every count with
its denominator. Nothing is fitted beyond the par surface itself, which IS L2's act;
no prior, no retrain (A.1).
"""
import os, sys, io, json, contextlib, collections

OUT = os.environ['L2_OUT']
os.makedirs(OUT, exist_ok=True)

# --- PORTABILITY AUDIT ------------------------------------------------------
# v0surf.pkl is the ONE input that differs between this container's reconstructed
# L1-exit tree and the record's (proven field-level). If the par measurement never
# reads it, these L2 numbers are independent of that difference. Audit every file
# this process opens rather than reasoning about the call graph.
_OPENED = set()
def _audit(event, args):
    if event == 'open':
        try: _OPENED.add(str(args[0]))
        except Exception: pass
sys.addaudithook(_audit)

# NON-VACUITY CONTROL (seam ruling 2026-07-31 item 4: prove the hook can FAIL before citing it).
# L2_AUDIT_CONTROL=1 makes this process deliberately open the pkl. The audit must then catch it
# and the verdict must flip to NOT PORTABLE. An audit that cannot fire is worth nothing.
if os.environ.get('L2_AUDIT_CONTROL') == '1':
    _ctl = os.path.join(os.environ['RL_REPO'], 'data', 'v0surf.pkl')
    with open(_ctl, 'rb') as _f:
        _f.read(16)
    print('[CONTROL] deliberately opened %s — the audit MUST catch this' % _ctl)

import numpy as np

FV = os.environ['RL_FV']
if FV not in sys.path:
    sys.path.insert(0, FV)

with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    import conditional_prior as CP
    import par_build as pb

R = {}

# ============================================================================
# 0 · SUBSTRATE + the runbook's stated context, re-measured rather than read
# ============================================================================
years = collections.Counter()
for p in MA.data:
    for x in p.get('scoring') or []:
        years[x['year']] += 1
span = (min(years), max(years))

draft_class = collections.Counter()
for p in MA.data:
    try:
        draft_class[pb.draftyr(p)] += 1
    except Exception:
        pass

# 2003 draft class: how many rows, how many carry ANY scoring row
def _dy(p):
    try: return pb.draftyr(p)
    except Exception: return None
c2003 = [p for p in MA.data if _dy(p) == 2003]
c2003_scoring = [p for p in c2003 if (p.get('scoring') or [])]
# and how many are in par_build's own eligible pool shape (GRP + pick/_ft)
c2003_pool = [p for p in c2003 if MA.GRP.get(p.get('pos')) and (p.get('pick') or p.get('_ft'))]
c2003_pool_scoring = [p for p in c2003_pool if (p.get('scoring') or [])]

R['substrate'] = {
    'store_rows_total': len(MA.data),
    'scoring_year_span': list(span),
    'scoring_rows_total': int(sum(years.values())),
    'rows_in_year_2004': int(years.get(2004, 0)),
    'rows_in_year_2005': int(years.get(2005, 0)),
    'draft_class_2003_rows': len(c2003),
    'draft_class_2003_with_any_scoring': len(c2003_scoring),
    'draft_class_2003_in_par_pool': len(c2003_pool),
    'draft_class_2003_in_par_pool_with_scoring': len(c2003_pool_scoring),
    'par_dials': {'MIN_GAMES': pb.MIN_GAMES, 'TEN_MAX': pb.TEN_MAX,
                  'DRAFT_HI': pb.DRAFT_HI, 'H_LOGPICK': pb.H_LOGPICK,
                  'PAR_DUAL_RULE': getattr(pb, 'PAR_DUAL_RULE', '<E3 NOT APPLIED>')},
    'groups': list(pb.GROUPS),
    'eval_picks': list(pb.EVAL_PICKS),
}

# CENSORING CHECK, both directions: does an absent season impute a zero, or drop out?
# gather() reads `g = r['games'] if r else 0` then `if g > 0`. Prove the 2003 class's
# tenure-1 (Y=2004) contributes NOTHING rather than a zero observation.
t1_2004_rows = sum(1 for p in c2003_pool
                   if any(x['year'] == 2004 for x in (p.get('scoring') or [])))
R['censoring_check'] = {
    'tenure_for_2003_class_at_Y2004': 1,
    'tenure_for_2003_class_at_Y2005': 2,
    'store_scoring_rows_at_Y2004_whole_store': int(years.get(2004, 0)),
    'par_pool_2003_class_rows_carrying_a_2004_season': int(t1_2004_rows),
    'note': ('gather() computes g=r["games"] if r else 0 and admits only g>0, so an absent '
             'season is SKIPPED, never taught as a zero. Measured, not reasoned.'),
}

# ============================================================================
# 1 · PER-CANDIDATE MEASUREMENT
# ============================================================================
def measure(lo):
    """Everything L2 owes for one window, from ONE gather() + ONE fit()."""
    pb.DRAFT_LO = lo
    pool = [p for p in MA.data if MA.GRP.get(p.get('pos'))
            and (p.get('pick') or p.get('_ft')) and lo <= pb.draftyr(p) <= pb.DRAFT_HI]
    obs, base, raw = pb.gather()

    # ---- cell populations -------------------------------------------------
    raw_cell = collections.Counter()      # (pos,T) -> raw rows (played, g>0)
    obs_cell = collections.Counter()      # (pos,T) -> gated ON-PARK observations
    raw_by_pos = collections.Counter()
    obs_by_pos = collections.Counter()
    raw_by_T = collections.Counter()
    obs_by_T = collections.Counter()
    for pos, pk, T, Y, g, p in raw:
        raw_cell[(pos, T)] += 1; raw_by_pos[pos] += 1; raw_by_T[T] += 1
    for pos, x, T, lv in obs:
        obs_cell[(pos, T)] += 1; obs_by_pos[pos] += 1; obs_by_T[T] += 1

    # ---- gate classifications --------------------------------------------
    # the live gate is flat MIN_GAMES; the docstring advertises a base-rate-relative
    # gate that the code does not implement. Classify under BOTH, and report the
    # disagreement — it is the "re-derive the structural gate" half of L2.
    gate_flat_on = collections.Counter(); gate_flat_off = collections.Counter()
    gate_rel_on = collections.Counter()
    disagree = 0
    for pos, pk, T, Y, g, p in raw:
        b = base.get((pos, T), float('nan'))
        on_flat = g >= pb.MIN_GAMES
        on_rel = (g >= b) if b == b else False
        (gate_flat_on if on_flat else gate_flat_off)[(pos, T)] += 1
        if on_rel: gate_rel_on[(pos, T)] += 1
        if on_flat != on_rel: disagree += 1

    # ---- the surface ------------------------------------------------------
    F = pb.fit()
    surface = {}
    for g in pb.GROUPS:
        for pk in pb.EVAL_PICKS:
            for T in range(1, pb.TEN_MAX + 1):
                v = pb.par_at(F, g, pk, T)
                surface['%s|%d|%d' % (g, pk, T)] = None if v != v else round(float(v), 6)

    return {
        'DRAFT_LO': lo, 'DRAFT_HI': pb.DRAFT_HI,
        'denominators': {
            'store_rows': len(MA.data),
            'eligible_pool_players': len(pool),
            'raw_played_season_rows': len(raw),
            'gated_on_park_observations': len(obs),
        },
        'cell_populations': {
            'raw_by_pos_tenure': {'%s|%d' % k: v for k, v in sorted(raw_cell.items())},
            'obs_by_pos_tenure': {'%s|%d' % k: v for k, v in sorted(obs_cell.items())},
            'raw_by_pos': dict(raw_by_pos), 'obs_by_pos': dict(obs_by_pos),
            'raw_by_tenure': {str(k): v for k, v in sorted(raw_by_T.items())},
            'obs_by_tenure': {str(k): v for k, v in sorted(obs_by_T.items())},
            'base_play_rate_by_pos_tenure': {'%s|%d' % k: v for k, v in sorted(base.items())},
            'n_by_pos_fitted': {k: int(v) for k, v in F['n_by_pos'].items()},
            'starved_groups': [g for g in pb.GROUPS if F['n_by_pos'][g] == 0],
            'thin_groups_lt4': [g for g in pb.GROUPS if 0 < F['n_by_pos'][g] < 4],
        },
        'gate_classifications': {
            'rule_live': 'flat games >= %g at that tenure' % pb.MIN_GAMES,
            'rule_docstring': 'games >= base_play_rate(pos,tenure)  [NOT IMPLEMENTED in the live code]',
            'flat_on_park_total': int(sum(gate_flat_on.values())),
            'flat_off_park_total': int(sum(gate_flat_off.values())),
            'flat_on_park_rate': (sum(gate_flat_on.values()) / len(raw)) if raw else None,
            'base_relative_on_park_total': int(sum(gate_rel_on.values())),
            'rows_where_the_two_rules_disagree': int(disagree),
            'flat_on_by_pos_tenure': {'%s|%d' % k: v for k, v in sorted(gate_flat_on.items())},
            'flat_off_by_pos_tenure': {'%s|%d' % k: v for k, v in sorted(gate_flat_off.items())},
        },
        'surface': surface,
        'ramp_shr': {g: [round(float(x), 6) for x in F['ramp_shr'][g]] for g in pb.GROUPS},
    }

A = measure(2003)
B = measure(2004)
R['candidate_A_censor_aware_2003'] = A
R['candidate_B_uniform_2004plus'] = B

# ============================================================================
# 2 · THE DELTAS — A minus B, with denominators
# ============================================================================
keys = sorted(set(A['surface']) | set(B['surface']))
deltas = {}
both = 0; nan_a = 0; nan_b = 0; moved = 0
absmax = (None, 0.0); rel_list = []
for k in keys:
    a, b = A['surface'].get(k), B['surface'].get(k)
    if a is None: nan_a += 1
    if b is None: nan_b += 1
    if a is None or b is None:
        deltas[k] = None; continue
    both += 1
    d = a - b
    deltas[k] = round(d, 6)
    if abs(d) > 1e-9: moved += 1
    if abs(d) > abs(absmax[1]): absmax = (k, d)
    if abs(b) > 1e-12: rel_list.append(abs(d) / abs(b))

rel_list.sort()
def _pct(v, q):
    if not v: return None
    i = int(round(q * (len(v) - 1)))
    return round(v[i], 6)

# rows the 2003 class actually contributes = A's raw minus B's raw
R['deltas'] = {
    'surface_cells_compared': both,
    'surface_cells_total': len(keys),
    'cells_nan_in_A': nan_a, 'cells_nan_in_B': nan_b,
    'cells_that_MOVED_gt_1e-9': moved,
    'cells_unchanged': both - moved,
    'max_abs_delta_cell': absmax[0],
    'max_abs_delta_value': round(absmax[1], 6),
    'rel_delta_median': _pct(rel_list, 0.50),
    'rel_delta_p90': _pct(rel_list, 0.90),
    'rel_delta_max': round(rel_list[-1], 6) if rel_list else None,
    'per_cell': deltas,
    'population_delta': {
        'eligible_pool_players': A['denominators']['eligible_pool_players'] - B['denominators']['eligible_pool_players'],
        'raw_played_season_rows': A['denominators']['raw_played_season_rows'] - B['denominators']['raw_played_season_rows'],
        'gated_on_park_observations': A['denominators']['gated_on_park_observations'] - B['denominators']['gated_on_park_observations'],
    },
}

# per-position surface movement summary
by_pos = {}
for g in pb.GROUPS:
    vals = [abs(deltas[k]) for k in keys if k.startswith(g + '|') and deltas.get(k) is not None]
    by_pos[g] = {'cells': len(vals),
                 'max_abs': round(max(vals), 6) if vals else None,
                 'mean_abs': round(sum(vals) / len(vals), 6) if vals else None}
R['deltas']['by_position'] = by_pos

# ============================================================================
# 3 · PORTABILITY — did this measurement read the one differing input?
# ============================================================================
v0 = sorted(p for p in _OPENED if 'v0surf' in p)
R['portability_audit'] = {
    'question': ('v0surf.pkl is the sole input differing between this container and the '
                 'record (proven field-level). Did the par measurement read it?'),
    'files_opened_matching_v0surf': v0,
    'v0surf_read_during_measurement': bool(v0),
    'verdict': ('PORTABLE — the L2 window comparison never touched v0surf.pkl, so it is '
                'independent of the G-Y0 divergence'
                if not v0 else
                'NOT PORTABLE — v0surf.pkl was read; these numbers inherit the divergence'),
    'total_files_opened': len(_OPENED),
}

with open(os.path.join(OUT, 'l2_window_candidates.json'), 'w') as f:
    json.dump(R, f, indent=2, sort_keys=False)

print('L2 WINDOW MEASUREMENT — both candidates, neither chosen')
print('  substrate store rows           :', R['substrate']['store_rows_total'])
print('  scoring span                   :', R['substrate']['scoring_year_span'],
      '| rows in 2004 =', R['substrate']['rows_in_year_2004'])
print('  2003 draft class in par pool   :', R['substrate']['draft_class_2003_in_par_pool'],
      '(with scoring:', R['substrate']['draft_class_2003_in_par_pool_with_scoring'], ')')
print('  PAR_DUAL_RULE                  :', R['substrate']['par_dials']['PAR_DUAL_RULE'])
for nm, C in (('A censor-aware-2003', A), ('B uniform 2004+', B)):
    d = C['denominators']
    print('  %-22s pool %4d | raw %5d | on-park %5d | starved %s'
          % (nm, d['eligible_pool_players'], d['raw_played_season_rows'],
             d['gated_on_park_observations'], C['cell_populations']['starved_groups'] or 'none'))
print('  surface cells moved            : %d of %d  (max |delta| %s at %s)'
      % (R['deltas']['cells_that_MOVED_gt_1e-9'], R['deltas']['surface_cells_compared'],
         R['deltas']['max_abs_delta_value'], R['deltas']['max_abs_delta_cell']))
print('  portability                    :', R['portability_audit']['verdict'])
print('  wrote', os.path.join(OUT, 'l2_window_candidates.json'))
