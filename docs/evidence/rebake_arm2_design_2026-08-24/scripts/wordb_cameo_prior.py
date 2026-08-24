#!/usr/bin/env python3
"""WORD B — THE EVIDENCE-CONDITIONED BUST PRIOR (seam-lever CAND-B), as a measurable object.

OWNER WORD B, verbatim: "Fit both and show me on word B, please." This module is the CONDITIONED
feature; the harness that fits both peak models and compares them is wordb_fit_both.py. NEITHER
VERSION IS ADOPTED BY THIS TASK — it is a measurement for the owner's packet ruling.

THE CONSTRUCTION IS THE SEAM LEVER'S, READ FROM ITS OWN CONSTRUCTION.md, NOT FROM A SUMMARY:

    mu(pos, k, t, g, c) = (1 - A(t,g)) * B(pos,k)  +  A(t,g) * T(c,t)

      k  MA.effpk capped 70
      t  tenure = Y - debut + 1
      g  career games through Y
      c  RAW games-weighted cameo average through Y
             c = sum_s(games_s * avg_s) / sum_s(games_s)  over seasons with games_s > 0
         — the axis the level vocabulary cannot see: the seam study measured 81.1% of in-scope
         states carrying level_through == 0 while their c spans 4.0 to 86.0.

      B(pos,k)   the DRAFT-DAY bust prior — here the v838 MODERNIZED table (owner word A), which is
                 exactly the A=0 limit of this surface. The candidate NESTS its own baseline.
      T(c,t) = M(t) / (1 + exp(-(c - c50(t)) / w_c))
               M(t)   = M1 * exp(-(t-1)/tauM)
               c50(t) = c0 + beta*(t-1)          beta = 0 in CAND-B (it settled on its bound and
                                                 wanted to go negative; dropped, one fewer parameter)
      A(t,g) = (1 - r) * W / (W + kappa(t))
               kappa(t) = kappa0 * exp(-(t-1)/tauK)
               W = sum_s w(g_s),  w(g) = g^2 / (g + 5.8)   <- THE ENGINE'S OWN FIX-1 DAMPING,
                                                  _DAMP_K at _merged_recover.py:191, reused verbatim
               r = _EVW_R = 0.11 (_merged_recover.py:208) — CAND-B inherits the estate's own
                   "pedigree fades to a residual, NEVER vanishes" constant (R98.5) rather than
                   inventing one. It is why A cannot reach 1 and the pick can never be erased.

CONSTANTS: the REPRICING refit on the full primary window (CONSTRUCTION.md section 2), which is what
the coordinator's brief names and what a repricing measurement must use. They carry NO out-of-sample
claim and this module does not make one.

THE ONE CHOICE THIS SEAT HAD TO MAKE, AND IT IS DECLARED RATHER THAN BURIED
  The surface was FITTED on tenure 1-4 only (TRAIN = debut 2006-2014, 580 states). The peak model
  trains on every scored year of a career, so it asks for a bust_prior at t = 5, 9, 14...
  Extrapolating there is not neutral: M(t) decays with tauM 2.1, so at t=10 M is ~2.1 while A rises
  toward (1-r)=0.89 — mu would collapse to ~0.11*B for every veteran, annihilating the feature far
  outside the evidence that fitted it.
  DECISION: OUTSIDE THE FITTED SCOPE (t > TMAX) THE FEATURE IS THE STATIC B — A is held at 0.
  It keeps the nesting exact, it keeps day-0 exact, and it confines the lever to the population the
  seam study actually measured (early-career states whose only evidence is cameo minutes). The row
  counts in each regime are reported by the harness so the scope is visible, not assumed.
"""

import json
import math

# CAND-B, refit on the FULL primary window for repricing (CONSTRUCTION.md section 2). Declared as a
# repricing fit with NO out-of-sample claim.
M1 = 149.7064
TAU_M = 2.1061
C0 = 45.8848
W_C = 13.6587
KAPPA0 = 4.6810
TAU_K = 0.4333
BETA = 0.0          # CAND-B fixes beta at 0 (see the module docstring)
R_RESID = 0.11      # _EVW_R, the engine's own residual-pedigree constant
DAMP_K = 5.8        # _DAMP_K, the engine's own FIX-1 damping
TMAX = 4            # the fitted tenure scope; beyond it the feature is the static B (declared)


def w_games(g):
    """The engine's own FIX-1 damping w(g) = g^2/(g + _DAMP_K). Reused, not reinvented."""
    g = float(g)
    return (g * g) / (g + DAMP_K) if g > 0 else 0.0


def W_of(season_games):
    """W = sum_s w(g_s) over the player's seasons through Y. Zero evidence => 0 => A = 0."""
    return sum(w_games(g) for g in season_games if g and g > 0)


def kappa(t):
    return KAPPA0 * math.exp(-(t - 1) / TAU_K)


def A_of(t, season_games):
    """A(t,g) in [0, 1-r). Cannot reach 1: the residual r keeps the pick alive at every t."""
    W = W_of(season_games)
    if W <= 0.0:
        return 0.0
    return (1.0 - R_RESID) * W / (W + kappa(t))


def M_of(t):
    return M1 * math.exp(-(t - 1) / TAU_M)


def c50_of(t):
    return C0 + BETA * (t - 1)


def T_of(c, t):
    """The cameo-strength logistic. Monotone non-decreasing in c by construction."""
    z = (float(c) - c50_of(t)) / W_C
    # guard the exponential the same way any logistic must be guarded; no behavioural effect in range
    if z < -700:
        return 0.0
    return M_of(t) / (1.0 + math.exp(-z))


def cameo_avg(seasons):
    """c = RAW games-weighted average over seasons with games > 0. None when there is no evidence."""
    num = den = 0.0
    for g, a in seasons:
        if g and g > 0:
            num += float(g) * float(a)
            den += float(g)
    return (num / den) if den > 0 else None


def mu(B_pos_k, t, seasons):
    """The conditioned prior. `seasons` is [(games, avg), ...] through Y; B_pos_k is the static table
    value for this (position, pick). Returns (value, A, T, c) so a caller can census the components.

    ZERO EVIDENCE => A = 0 => mu == B_pos_k EXACTLY. That is what makes the draft row byte-exact, and
    the harness asserts it rather than trusting this sentence."""
    if t > TMAX:                                   # declared scope clamp — see the module docstring
        return float(B_pos_k), 0.0, None, None
    gs = [g for g, _ in seasons]
    A = A_of(t, gs)
    if A <= 0.0:
        return float(B_pos_k), 0.0, None, None
    c = cameo_avg(seasons)
    if c is None:
        return float(B_pos_k), 0.0, None, None
    T = T_of(c, t)
    return (1.0 - A) * float(B_pos_k) + A * T, A, T, c


def load_table(path, key='modern'):
    """The v838 MODERNIZED table (owner word A). Returned as the plain {pos: {pick_str: value}} dict
    the estate's own bust_prior_table.json format uses, so it can be written straight to a root."""
    d = json.load(open(path))
    if key in d:
        return d[key]
    return d


def spec():
    return {'construction': 'seam-lever CAND-B, evidence-conditioned bust prior',
            'constants': {'M1': M1, 'tauM': TAU_M, 'c0': C0, 'w_c': W_C, 'kappa0': KAPPA0,
                          'tauK': TAU_K, 'beta': BETA, 'r': R_RESID, 'damp_k': DAMP_K},
            'constants_provenance': 'the REPRICING refit on the full primary window '
                                    '(CONSTRUCTION.md section 2); no out-of-sample claim',
            'tenure_scope': TMAX,
            'outside_scope_rule': 'A held at 0 => the feature is the static B (declared, not fitted)',
            'B_table': 'v838 MODERNIZED (owner word A) — the A=0 limit of this surface'}
