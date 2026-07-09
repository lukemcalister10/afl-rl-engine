#!/usr/bin/env python3
"""DERIVE the LTI RETURN-FROM-INJURY haircut surface (Chapter-3 Part 2, 2026-07-09) — walk-forward,
leak-free, NET OF AGING. Emits lti_return_table.json (the engine consumes THAT; this is the derivation).

CASE (spec §4.1, walk-forward): >=5 games in season Y, ZERO games in Y+1, >=1 game in Y+2, Y+2 <= LEAKCUT.
MEASURE (spec §4.2): the return haircut is the return-season output shortfall NET of the aging the fade/M2
levers already own. E_aged is estimated from the store's OWN same-age NON-GAP cohort (played Y, Y+1, Y+2) —
its Y->Y+2 output drift IS the age-expected change. h = 1 - gap_ratio / nongap_ratio.

THE BINDING DOCTRINE (study-v2 + A-DARCY "absence is a finding", DECISIONS §33 R-v/directive):
 * YOUNG / SPECULATIVE (return-age < YOUNG_CUT, or nqual<4 at consumption): h = 0, SHIPPED ZERO. The raw
   young return ratio is >=1.0 (they come back at their prior level — no ceiling dent). The apparent gap vs
   the non-gap cohort is DEVELOPMENT SELECTION (the non-gap young are the ones who kept developing), and
   charging it here would double-charge the forfeited GROWTH-YEAR cost Part 1 already prices — exactly the
   double-count study-v2 forbids. So the young return arm is ZERO by construction; their cost is the lost
   season (Part 1) and the preserved L1c runway (fork i-a), never a return dent.
 * ESTABLISHED OLDER (age >= YOUNG_CUT): aging dominates and gap-vs-aging is identifiable — ship the measured
   net residual, adaptive-kernel smoothed over age, POOLED across position classes (the class cells are
   n=0..8 — cannot support finest-resolution; class rides as a reported covariate, not a split; spec §4.3),
   CAPPED (RET_CAP) against the thin 30+ tail, applied to the RETURN SEASON ONLY and decaying to 0 the next.

Run:  python3 derive_lti_return.py   (reads rl_model_data.json in cwd; writes lti_return_table.json)
"""
import json, os, math
from statistics import median

LEAKCUT   = 2024      # Y+2 <= 2024 : every consumed row is <= the eval cut (walk-forward, leak-free)
YOUNG_CUT = 27        # return-age below this ships ZERO (development/injury unidentifiable; Part 1 owns it)
RET_CAP   = 0.15      # hard cap on the shipped haircut (thin 30+ tail; conservative)
AGE_KNOTS = list(range(22, 35))   # reported/interp knots
BW0, BWMAX, EFFN_MIN = 1.5, 6.0, 35.0


def _cls(p):
    pos = p.get('future_position') or p.get('present_position') or p.get('drafted_position') or ''
    return 'RUC' if pos == 'RUC' else ('KPP' if pos in ('KEY_FWD', 'KEY_DEF') else 'nonKPP')


def _rows(p):
    return {r['year']: r for r in p['scoring']}


def collect(players):
    gap, nongap = [], []      # (age_at_return, cls, ratio)
    never = 0
    for p in players:
        rm = _rows(p); by = p.get('_by')
        for Y in sorted(rm):
            rY = rm[Y]
            if rY['games'] < 5 or not rY['avg']:
                continue
            y1, y2 = rm.get(Y + 1), rm.get(Y + 2)
            g1 = y1['games'] if y1 else 0
            g2 = y2['games'] if y2 else 0
            aret = (Y + 2 - by) if by else None
            if g1 == 0 and g2 >= 1 and (Y + 2) <= LEAKCUT and aret:
                gap.append((aret, _cls(p), y2['avg'] / rY['avg']))
            elif g1 == 0 and g2 == 0 and (Y + 1) <= LEAKCUT:
                never += 1
            if g1 >= 1 and g2 >= 1 and (Y + 2) <= LEAKCUT and aret:
                nongap.append((aret, _cls(p), y2['avg'] / rY['avg']))
    return gap, nongap, never


def _kernel_ratio(pts, age):
    """adaptive-bandwidth NW median-ish: weighted mean of ratios, bw grown until eff-n>=EFFN_MIN."""
    xs = [a for a, _, _ in pts]; vs = [r for _, _, r in pts]
    bw = BW0
    while True:
        w = [math.exp(-0.5 * ((x - age) / bw) ** 2) for x in xs]
        sw = sum(w); effn = (sw * sw) / sum(wi * wi for wi in w) if sw > 0 else 0.0
        if effn >= EFFN_MIN or bw >= BWMAX:
            break
        bw *= 1.15
    val = sum(wi * vi for wi, vi in zip(w, vs)) / sw if sw > 0 else float('nan')
    return val, effn, bw


def derive(players):
    gap, nongap, never = collect(players)
    surface = {}; meta_effn = {}
    for age in AGE_KNOTS:
        if age < YOUNG_CUT:
            surface[age] = 0.0; meta_effn[age] = None      # SHIP ZERO (doctrine)
            continue
        gr, ge, gbw = _kernel_ratio(gap, age)
        nr, ne, nbw = _kernel_ratio(nongap, age)
        h = 1.0 - gr / nr if (nr and not math.isnan(gr)) else 0.0
        h = max(0.0, min(RET_CAP, h))                      # clip [0, RET_CAP]
        surface[age] = round(h, 4); meta_effn[age] = round(min(ge, ne), 1)
    # monotone non-decreasing in age (aging is monotone; kills kernel wiggle), still capped
    run = 0.0
    for age in AGE_KNOTS:
        if age >= YOUNG_CUT:
            run = max(run, surface[age]); surface[age] = round(min(RET_CAP, run), 4)
    from collections import Counter
    return {
        'version': '1', 'date': '2026-07-09',
        'method': 'net-of-aging (E_aged = store non-gap same-age cohort Y->Y+2 drift); adaptive-bw NW over '
                  'return-age, eff-n>=%g; classes POOLED (reported covariate, not split); young<%d shipped ZERO '
                  '(A-DARCY doctrine — development/injury unidentifiable, Part 1 owns the growth-year cost); '
                  'monotone-in-age; capped at %.2f.' % (EFFN_MIN, YOUNG_CUT, RET_CAP),
        'store_note': 'derived on store a2fbc9a0 (post King/Murphy fix). Historical windows carry no injury '
                      'labels — the measured quantity prices ABSENCE, the treatment the register applies (§4.1).',
        'young_cut': YOUNG_CUT, 'cap': RET_CAP, 'leakcut': LEAKCUT,
        'n_gap_cases': len(gap), 'n_nongap': len(nongap), 'n_never_returned': never,
        'class_counts_gap': dict(Counter(c for _, c, _ in gap)),
        'age_surface': {str(a): surface[a] for a in AGE_KNOTS},
        'age_eff_n': {str(a): meta_effn[a] for a in AGE_KNOTS},
    }


if __name__ == '__main__':
    HERE = os.path.dirname(os.path.abspath(__file__))
    players = json.load(open(os.path.join(HERE, 'rl_model_data.json')))
    tab = derive(players)
    out = os.path.join(HERE, 'lti_return_table.json')
    json.dump(tab, open(out, 'w'), indent=1)
    print("wrote %s" % out)
    print("gap=%d nongap=%d never=%d  class_gap=%s" % (tab['n_gap_cases'], tab['n_nongap'],
                                                       tab['n_never_returned'], tab['class_counts_gap']))
    print("age_surface:", tab['age_surface'])
    print("age_eff_n  :", tab['age_eff_n'])
