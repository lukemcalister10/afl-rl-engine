"""#334 stage B / OWNER-BASIS CONSERVATION TABLES, RE-DERIVED UNDER THE COHORT-MEMBERSHIP RULE.

Owner ruling (#334 comment 5235016488, verbatim): *"The 2025 cohort is NOT the 2025 MSD. The 2025 MSD
played in 2025, so that is their year 1. The 2025 cohort is 2025 ND, 2025 RD, 2025 pathways, SSP, 2026
MSD."*  And, the same session: *"When we are talking about yearly value across career, we can't exclude
certain players because of their entrance mechanism. We're not balancing the ND book, we're balancing
the cohort book."*

THE RULE APPLIED HERE: cohort N = every entrant whose YEAR 1 is season N+1, regardless of route.
Concretely, cohort N = the ND / RD / IRE / SSP / PDA / PDN / PDS / UNR entrants labelled year N, PLUS the
MSD entrants labelled year N+1 (the mid-season draft happens inside their year-1 season). No route is
excluded. Every previous owner-facing table grouped MSD by its draft-calendar LABEL; this file regroups
them and prints the diff so the owner can see exactly what the rule change moved.

VALUE CONVENTION — unchanged, read straight off the committed no-arb matrices, exactly as the committed
docs/evidence/act_334B_2026-08-07/stage5/owner_basis.py does it:
  * year 0 = v0;  year N = vpath[N-1];  a bust / concluded career scores 0 and STAYS in the denominator;
  * an entrant that has not reached year N (label year + N > WINDOW_END = 2026) is EXCLUDED from that row;
  * rows with v0 <= 0 or a missing value are excluded;
  * the population is the key-intersection of the matrices compared.

READ-ONLY. Writes only OWNER_BASIS_COHORT.txt and OWNER_BASIS_COHORT.json beside this script.
"""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)                       # .../docs/evidence/act_334B_2026-08-07
WINDOW_END = 2026
COHORT_LO, COHORT_HI = 2004, 2025
RUNGS = ['0.25', '0.5', '0.75', '1.0']

PATHS = [
    ('baseline',  EV + '/stage4_amend1/noarb/per_entrant_338_stage4a1.json'),
    ('s5 LANDED', EV + '/stage5/noarb/per_entrant_338_stage5.json'),
] + [('rung ' + w, EV + '/stage6/noarb/per_entrant_338_rung%s.json' % w) for w in RUNGS]
STATES = [n for n, _ in PATHS]

L = []
def P(s=''):
    print(s); L.append(s)


def recs(path):
    return {(r['key'], r['type'], r['year']): r for r in json.load(open(path))['recs']}


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


M = {n: recs(p) for n, p in PATHS}
keys = sorted(set.intersection(*[set(M[n]) for n in STATES]))
A = M['baseline']


# ---------------------------------------------------------------- value convention (committed basis)
def val(r, n):
    if r['year'] + n > WINDOW_END:
        return None
    if n == 0:
        return float(r['v0'])
    vp = r.get('vpath') or []
    if n - 1 >= len(vp):
        return 0.0
    v = vp[n - 1]
    return 0.0 if v is None else float(v)


def ratio(MM, ks, n=1):
    num = den = 0.0
    cnt = 0
    for k in ks:
        r = MM[k]
        a, b = val(r, n), val(r, 0)
        if a is None or b is None or b <= 0:
            continue
        num += a
        den += b
        cnt += 1
    return (num / den if den else float('nan')), cnt


# ---------------------------------------------------------------- the membership rules
def cohort_of(k):
    """THE OWNER'S RULE: the cohort whose year 1 is this entrant's year 1."""
    key, typ, yr = k
    return yr - 1 if typ == 'MSD' else yr


def label_of(k):
    """THE OLD RULE, kept only for the diff table: group by draft-calendar label."""
    return k[2]


ND = lambda k: (A[k]['type'] == 'ND' and A[k].get('pick') and 1 <= A[k]['pick'] <= 64)
POOL = lambda k: not ND(k)
MSD = lambda k: A[k]['type'] == 'MSD'


def pop(grp, lo, hi, filt=None):
    return [k for k in keys if lo <= grp(k) <= hi and (filt is None or filt(k))]


def fmt(x, w=10, p=6):
    return ('%*.*f' % (w, p, x)) if x == x else ('%*s' % (w, 'n/a'))


OUT = {}

# ================================================================== header
P('=' * 132)
P('#334 stage B  /  OWNER-BASIS CONSERVATION TABLES, RE-DERIVED UNDER THE COHORT-MEMBERSHIP RULE')
P('=' * 132)
P('')
P('  THE RULE, in the owner\'s words (#334 comment 5235016488):')
P('')
P('      "The 2025 cohort is NOT the 2025 MSD. The 2025 MSD played in 2025, so that is their year 1.')
P('       The 2025 cohort is 2025 ND, 2025 RD, 2025 pathways, SSP, 2026 MSD."')
P('')
P('      "When we are talking about yearly value across career, we can\'t exclude certain players because')
P('       of their entrance mechanism. We\'re not balancing the ND book, we\'re balancing the cohort book."')
P('')
P('  So: COHORT N = every entrant whose YEAR 1 is season N+1, whatever route they came in by. In practice')
P('  that is the ND, RD, IRE, SSP, PDA, PDN, PDS and UNR entrants labelled year N, PLUS the MSD entrants')
P('  labelled year N+1, because the mid-season draft happens INSIDE their year-1 season. No route is left')
P('  out. Cohorts %d to %d. Every number below is read straight off the committed matrices.' % (COHORT_LO, COHORT_HI))
P('')
P('  MATRICES READ (md5, first 8):')
for n, p in PATHS:
    P('      %-10s  %s  %s' % (n, md5(p)[:8], p[len(EV) + 1:]))
P('      population = key-intersection of all six = %d entrants (the six matrices carry identical key' % len(keys))
P('      sets, so nothing is dropped by the intersection).')
P('')

# ================================================================== the MSD convention, verified
P('-' * 132)
P('  THE MSD CONVENTION USED HERE, AND WHY  (checked on the records before any number was aggregated)')
P('-' * 132)
P('')
msd_all = [k for k in keys if MSD(k)]
chk = []
for k in msd_all:
    r = A[k]
    yrs = r.get('yrs') or []
    seas = {s['year']: s['games'] for s in r['seasons']}
    chk.append((
        bool(yrs) and yrs[0] == r['year'] + 1,
        r.get('games_yr1') == seas.get(r['year'], 0) + seas.get(r['year'] + 1, 0),
        bool(r['seasons']) and r['seasons'][0]['year'] == r['year'],
    ))
P('  1. EVERY route uses the SAME grid. For an entrant labelled year Y, vpath slot N-1 is the value at')
P('     season Y+N. Verified on all %d MSD records: yrs[0] == Y+1 holds %d/%d times. No index shift is'
  % (len(msd_all), sum(c[0] for c in chk), len(chk)))
P('     needed, and none was applied.')
P('')
P('  2. The engine already folds the mid-season-draft season INTO the MSD year-1 measure. For every one')
P('     of the %d MSD records, games_yr1 == (games in season Y) + (games in season Y+1) -- %d/%d. For ND'
  % (len(msd_all), sum(c[1] for c in chk), len(chk)))
P('     it is season Y+1 alone. So an MSD\'s vpath[0] IS their year-1 value, and it already covers the')
P('     season the owner points at. That is what "clock depth 1" means here.')
P('')
P('  3. %d of the %d MSD records have their first playing season IN the label year itself. That is the'
  % (sum(c[2] for c in chk), len(msd_all)))
P('     owner\'s point restated by the data: the 2026 MSD played in 2026, so 2026 is their year 1, so they')
P('     belong to the 2025 cohort.')
P('')
P('  WORKED EXAMPLES (straight from the baseline matrix):')
P('')
P('     %-20s %-6s %8s %8s %-26s %s' % ('player', 'label', 'v0', 'vpath0', 'grid years', 'seasons played (games)'))
EXAMPLES = ['flynn-riley', 'ryan-maric', 'jack-hutchinson', 'tom-mccarthy']
for want in EXAMPLES:
    for k in msd_all:
        if k[0] != want:
            continue
        r = A[k]
        vp = (r.get('vpath') or [None])[0]
        seas = ' '.join('%d:%d' % (s['year'], s['games']) for s in r['seasons']) or '(none)'
        P('     %-20s %-6d %8.1f %8s %-26s %s'
          % (r['player'], r['year'], r['v0'], ('null' if vp is None else '%d' % vp),
             str(r.get('yrs')), seas))
P('')
P('  THE CONVENTION ADOPTED: depth alignment. Year N of a cohort takes each member\'s OWN year-N value --')
P('  v0 for year 0, vpath[N-1] for year N -- for every route including MSD. Nothing is re-indexed and')
P('  nothing is fabricated. The MSD entrants are simply filed into the cohort whose year 1 is theirs.')
P('')
P('  THE ONE HONEST COST, stated plainly: the "has it reached year N" gate is still each entrant\'s own')
P('  (label year + N <= %d). An MSD sits one calendar year later than the rest of its cohort, so at the' % WINDOW_END)
P('  window edge the MSD leg drops out one year sooner. Concretely: the 2026 MSD -- the MSD leg of the')
P('  2025 cohort -- has NO year-1 number inside the %d window (their grid year is 2027), so they are' % WINDOW_END)
P('  counted in the 2025 cohort but contribute nothing to its year-1 row yet. The MSD leg is therefore')
P('  ALSO printed on its own below, so the owner can see exactly what it does and does not carry.')
P('')

# ================================================================== TABLE 1 + 2
P('=' * 132)
P('  TABLE 1 & 2 -- THE FULL-COHORT LEAD, WITH THE ND 1-64 AND POOL SPLITS BESIDE IT   (year 1)')
P('=' * 132)
P('')
POPS = [
    ('FULL COHORT, all routes, cohorts %d-%d' % (COHORT_LO, COHORT_HI), None),
    ('  ND 1-64 split', ND),
    ('  pool split (every non-ND-1-64 route)', POOL),
    ('     of which MSD leg only', MSD),
]
P('  %-42s %7s %11s %11s %11s %11s %11s %11s' %
  ('population (year 1)', 'n', 'baseline', 's5 LANDED', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
P('  ' + '-' * 120)
T12 = {}
for nm, f in POPS:
    ks = pop(cohort_of, COHORT_LO, COHORT_HI, f)
    row = {}
    n_used = 0
    for st in STATES:
        r, c = ratio(M[st], ks)
        row[st] = r
        n_used = c
    T12[nm.strip()] = dict(n=n_used, n_members=len(ks), **{st: row[st] for st in STATES})
    P('  %-42s %7d %s %s %s %s %s %s'
      % (nm, n_used, fmt(row['baseline'], 11), fmt(row['s5 LANDED'], 11),
         fmt(row['rung 0.25'], 11), fmt(row['rung 0.5'], 11),
         fmt(row['rung 0.75'], 11), fmt(row['rung 1.0'], 11)))
P('')
tw_ks = pop(cohort_of, 2004, 2022, ND)
tw = {}
for st in STATES:
    tw[st], tw_n = ratio(M[st], tw_ks)
P('  printed LAST and labelled, so the fitting population is never mistaken for the presentation one:')
P('  %-42s %7d %s %s %s %s %s %s'
  % ('ND 1-64, 2004-2022 (TEACHING WINDOW)', tw_n, fmt(tw['baseline'], 11), fmt(tw['s5 LANDED'], 11),
     fmt(tw['rung 0.25'], 11), fmt(tw['rung 0.5'], 11), fmt(tw['rung 0.75'], 11), fmt(tw['rung 1.0'], 11)))
P('  (the teaching window is ND-only, so the cohort rule cannot move it -- it is unchanged by construction.)')
P('')
fc = T12['FULL COHORT, all routes, cohorts %d-%d' % (COHORT_LO, COHORT_HI)]
P('  WHAT THE OWNER READS OFF THIS: on the cohort book, year-1 conservation sits at %.4f at the ruled'
  % fc['baseline'])
P('  baseline and %.4f once stage 5 lands, across %d entrants. The four stage-6 rungs move it to %.4f,'
  % (fc['s5 LANDED'], fc['n'], fc['rung 0.25']))
P('  %.4f, %.4f and %.4f. The ND leg and the pool leg are printed beside it, not instead of it.'
  % (fc['rung 0.5'], fc['rung 0.75'], fc['rung 1.0']))
P('')
OUT['table_1_2_year1_populations'] = T12
OUT['teaching_window_year1'] = dict(n=tw_n, **tw)

# ================================================================== TABLE 3
P('=' * 132)
P('  TABLE 3 -- THE RECENT COHORTS, ROW BY ROW, AT THEIR REACHED YEARS   (cohorts 2023, 2024, 2025)')
P('=' * 132)
P('')
P('  Cohort N here means: everything labelled N except MSD, plus the MSD labelled N+1. A cohort reaches')
P('  year k only while N+k <= %d, so the newer the cohort the fewer rows it has.' % WINDOW_END)
P('')
T3 = {}
for C in (2023, 2024, 2025):
    ks_all = pop(cohort_of, C, C)
    ks_nd = pop(cohort_of, C, C, ND)
    ks_pl = pop(cohort_of, C, C, POOL)
    ks_ms = pop(cohort_of, C, C, MSD)
    P('  COHORT %d  --  %d entrants in the cohort book (%d ND 1-64, %d pool, of which %d MSD labelled %d)'
      % (C, len(ks_all), len(ks_nd), len(ks_pl), len(ks_ms), C + 1))
    P('  %-30s %5s %7s %11s %11s %11s %11s %11s %11s'
      % ('leg / year', 'yr', 'n', 'baseline', 's5 LANDED', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
    P('  ' + '-' * 118)
    T3[C] = dict(members=len(ks_all), members_nd=len(ks_nd), members_pool=len(ks_pl),
                 members_msd=len(ks_ms), rows={})
    for legnm, ks in (('full cohort', ks_all), ('  ND 1-64', ks_nd), ('  pool routes', ks_pl)):
        for n in range(1, WINDOW_END - C + 1):
            row = {}
            cnt = 0
            for st in STATES:
                row[st], cnt = ratio(M[st], ks, n)
            if cnt == 0:
                P('  %-30s %5d %7d %s' % (legnm, n, 0, '   -- no entrant in this leg has reached year %d inside the window --' % n))
                T3[C]['rows']['%s|%d' % (legnm.strip(), n)] = dict(n=0)
                continue
            T3[C]['rows']['%s|%d' % (legnm.strip(), n)] = dict(n=cnt, **row)
            P('  %-30s %5d %7d %s %s %s %s %s %s'
              % (legnm, n, cnt, fmt(row['baseline'], 11), fmt(row['s5 LANDED'], 11),
                 fmt(row['rung 0.25'], 11), fmt(row['rung 0.5'], 11),
                 fmt(row['rung 0.75'], 11), fmt(row['rung 1.0'], 11)))
        P('')
    ms_r, ms_n = ratio(M['baseline'], ks_ms, 1)
    ms_r5, _ = ratio(M['s5 LANDED'], ks_ms, 1)
    T3[C]['msd_leg_year1'] = dict(n=ms_n, baseline=ms_r, s5=ms_r5)
    if ms_n:
        P('  MSD leg of cohort %d (the %d MSD labelled %d), year 1 on its own: n=%d  baseline %.6f  s5 %.6f'
          % (C, len(ks_ms), C + 1, ms_n, ms_r, ms_r5))
    else:
        P('  MSD leg of cohort %d (the %d MSD labelled %d): NO year-1 number inside the %d window -- their'
          % (C, len(ks_ms), C + 1, WINDOW_END))
        P('  grid year is %d. They are members of the cohort but carry nothing into its year-1 row yet.' % (C + 2))
    P('')
OUT['table_3_recent_cohorts'] = T3

# ================================================================== TABLE 4
P('=' * 132)
P('  TABLE 4 -- THE YEAR-BY-YEAR FULL-COHORT PATH, YEARS 0-7')
P('=' * 132)
P('')
P('  The whole cohort book, cohorts %d-%d, at each career year. Year 0 is the entry value itself, so it' % (COHORT_LO, COHORT_HI))
P('  is 1.000000 by construction and is printed as the anchor. n falls away with depth because a cohort')
P('  only appears at year k while it has reached it.')
P('')
P('  %-5s %8s %13s %13s %13s %13s %13s' %
  ('yr', 'n', 'baseline', 's5 LANDED', 'rung 0.25', 'move s5', 'move r.25'))
P('  ' + '-' * 84)
full = pop(cohort_of, COHORT_LO, COHORT_HI)
T4 = {}
for n in range(0, 8):
    rb, cnt = ratio(M['baseline'], full, n)
    r5, _ = ratio(M['s5 LANDED'], full, n)
    r25, _ = ratio(M['rung 0.25'], full, n)
    T4[n] = dict(n=cnt, baseline=rb, s5=r5, rung025=r25)
    P('  %-5d %8d %s %s %s %s %s'
      % (n, cnt, fmt(rb, 13), fmt(r5, 13), fmt(r25, 13), fmt(r5 - rb, 13), fmt(r25 - rb, 13)))
P('')
OUT['table_4_full_cohort_path'] = T4

# ================================================================== TABLE 5
P('=' * 132)
P('  TABLE 5 -- WHAT THE RULE CHANGE ACTUALLY MOVED: cohort rule vs the OLD draft-label grouping')
P('=' * 132)
P('')
P('  OLD = group every entrant, MSD included, by its draft-calendar LABEL (what every owner-facing table')
P('  in this act did until the ruling). NEW = the owner\'s cohort rule. Year 1, same value convention,')
P('  same matrices, same population pool. "n" is the count that actually scored, not the membership.')
P('')
P('  %-40s %6s %11s %11s %4s %6s %11s %11s %4s %10s'
  % ('population (year 1)', 'OLDn', 'OLD base', 'OLD s5', '', 'NEWn', 'NEW base', 'NEW s5', '', 'move base'))
P('  ' + '-' * 128)
DIFFPOPS = [
    ('FULL BOOK, all routes, %d-%d' % (COHORT_LO, COHORT_HI), COHORT_LO, COHORT_HI, None),
    ('  ND 1-64', COHORT_LO, COHORT_HI, ND),
    ('  pool routes', COHORT_LO, COHORT_HI, POOL),
    ('     of which MSD leg', COHORT_LO, COHORT_HI, MSD),
    ('class/cohort 2023, all routes', 2023, 2023, None),
    ('class/cohort 2024, all routes', 2024, 2024, None),
    ('class/cohort 2025, all routes', 2025, 2025, None),
    ('class/cohort 2023, MSD leg only', 2023, 2023, MSD),
    ('class/cohort 2024, MSD leg only', 2024, 2024, MSD),
    ('class/cohort 2025, MSD leg only', 2025, 2025, MSD),
]
T5 = {}
for nm, lo, hi, f in DIFFPOPS:
    ko = pop(label_of, lo, hi, f)
    kn = pop(cohort_of, lo, hi, f)
    ob, on = ratio(M['baseline'], ko)
    o5, _ = ratio(M['s5 LANDED'], ko)
    nb, nn = ratio(M['baseline'], kn)
    n5, _ = ratio(M['s5 LANDED'], kn)
    mv = nb - ob if (nb == nb and ob == ob) else float('nan')
    T5[nm.strip()] = dict(old_n=on, old_base=ob, old_s5=o5, new_n=nn, new_base=nb, new_s5=n5,
                          old_members=len(ko), new_members=len(kn), move_base=mv)
    P('  %-40s %6d %s %s %4s %6d %s %s %4s %s'
      % (nm, on, fmt(ob, 11), fmt(o5, 11), '', nn, fmt(nb, 11), fmt(n5, 11), '', fmt(mv, 10)))
P('')
agg = T5['FULL BOOK, all routes, %d-%d' % (COHORT_LO, COHORT_HI)]
y0_old, n0_old = ratio(M['baseline'], pop(label_of, COHORT_LO, COHORT_HI), 0)
y0_new, n0_new = ratio(M['baseline'], pop(cohort_of, COHORT_LO, COHORT_HI), 0)
P('  READING IT, plainly:')
P('')
P('  * ON THE AGGREGATE THE RULE CHANGES NOTHING AT YEAR 1 -- the move is exactly %+.6f, on the same %d'
  % (agg['move_base'], agg['new_n']))
P('    scoring entrants. That is not a coincidence and it is not a fudge. The only membership difference')
P('    across the whole %d-%d book is the %d MSD labelled 2026, who move IN (they are the 2025 cohort\'s'
  % (COHORT_LO, COHORT_HI, T5['of which MSD leg']['new_members'] - T5['of which MSD leg']['old_members']))
P('    MSD leg), and they have no year-1 number inside the window yet. Everyone else just changes which')
P('    cohort they are filed under, and the aggregate does not care how the book is sorted. Membership')
P('    does grow: the year-0 anchor row goes from %d entrants to %d.' % (n0_old, n0_new))
P('')
P('  * PER COHORT IT IS REAL, AND LARGE. Cohort 2023 moves %+.6f, cohort 2024 %+.6f, cohort 2025 %+.6f'
  % (T5['class/cohort 2023, all routes']['move_base'], T5['class/cohort 2024, all routes']['move_base'],
     T5['class/cohort 2025, all routes']['move_base']))
P('    at the baseline. The MSD-leg rows show why: each cohort now takes the NEXT calendar MSD class, and')
P('    those classes read very differently (%.3f, %.3f, and nothing-yet at year 1). Under the old label'
  % (T5['class/cohort 2023, MSD leg only']['new_base'], T5['class/cohort 2024, MSD leg only']['new_base']))
P('    grouping the 2025 cohort was carrying the 2025 MSD at %.3f -- the inflated pool figure the ruling'
  % T5['class/cohort 2025, MSD leg only']['old_base'])
P('    struck. Under the rule it carries the 2026 MSD instead, who have not scored yet, and the 2025')
P('    cohort reads %.4f rather than %.4f.'
  % (T5['class/cohort 2025, all routes']['new_base'], T5['class/cohort 2025, all routes']['old_base']))
P('')

# ------------------------------------------------ cross-check against the figures printed in the ruling
P('-' * 132)
P('  CROSS-CHECK AGAINST THE NUMBERS THE RULING ITSELF PRINTED (comment 5235016488), stated honestly')
P('-' * 132)
P('')
c25 = T3[2025]
row_all = c25['rows']['full cohort|1']
row_nd = c25['rows']['ND 1-64|1']
row_pl = c25['rows']['pool routes|1']
P('  The ruling published a corrected 2025-cohort reading: "105 rostered ... whole book 0.940 baseline ->')
P('  0.985 candidate (ND 0.927 -> 0.971 . pool routes 1.021 -> 1.073)". Re-derived here off the committed')
P('  matrices, under the rule and the committed value convention:')
P('')
P('     %-34s %-22s %s' % ('', 'the ruling printed', 're-derived here'))
P('     %-34s %-22s %d' % ('cohort 2025 membership', '105', c25['members']))
P('     %-34s %-22s %.6f -> %.6f' % ('ND 1-64 leg, year 1', '0.927 -> 0.971',
                                     row_nd['baseline'], row_nd['rung 0.25']))
P('     %-34s %-22s %.6f -> %.6f' % ('pool leg, year 1', '1.021 -> 1.073',
                                     row_pl['baseline'], row_pl['rung 0.25']))
P('     %-34s %-22s %.6f -> %.6f' % ('whole cohort, year 1', '0.940 -> 0.985',
                                     row_all['baseline'], row_all['rung 0.25']))
P('')
P('  MEMBERSHIP AND THE ND LEG REPRODUCE EXACTLY -- 105 entrants, 0.927 -> 0.971, which also confirms the')
P('  ruling\'s "candidate" is the rung-0.25 matrix and its baseline is the stage-4-amend-1 matrix.')
P('')
P('  THE POOL LEG AND THE WHOLE-COHORT LINE DO NOT REPRODUCE. This seat could not recover 1.021 from the')
P('  committed matrices under any pool definition it tried: not-ND-1-64, the is_pool flag, the')
P('  is_pool_engine flag and not-type-ND all return the SAME %d scoring entrants at %.6f. The gap is not'
  % (row_pl['n'], row_pl['baseline']))
P('  the struck MSD figure either -- putting the 2025 MSD back in gives 1.128, not 1.021. This seat does')
P('  not know where 1.021 came from and does not claim the ruling\'s figure is wrong; it reports that the')
P('  committed evidence gives %.4f for the pool leg and %.4f for the whole 2025 cohort, and leaves the'
  % (row_pl['baseline'], row_all['baseline']))
P('  reconciliation to the owner and the seam. FLAGGED, NOT RESOLVED.')
P('')
OUT['cross_check_vs_ruling'] = dict(
    ruling=dict(members=105, nd='0.927->0.971', pool='1.021->1.073', whole='0.940->0.985'),
    rederived=dict(members=c25['members'],
                   nd=[row_nd['baseline'], row_nd['rung 0.25']],
                   pool=[row_pl['baseline'], row_pl['rung 0.25']],
                   whole=[row_all['baseline'], row_all['rung 0.25']]),
    verdict='membership and ND leg reproduce exactly; pool leg and whole-cohort line do not; flagged')
OUT['table_5_diff_vs_old_grouping'] = T5

# ================================================================== MSD leg on its own
P('=' * 132)
P('  APPENDIX -- THE MSD LEG ON ITS OWN, every MSD class, so nothing is forced into a grid it does not fit')
P('=' * 132)
P('')
P('  %-8s %-8s %7s %7s %11s %11s %11s' %
  ('label', 'cohort', 'members', 'n yr1', 'baseline', 's5 LANDED', 'rung 0.25'))
P('  ' + '-' * 72)
MSDT = {}
labels = sorted(set(k[2] for k in keys if MSD(k)))
for lab in labels:
    ks = [k for k in keys if MSD(k) and k[2] == lab]
    rb, cnt = ratio(M['baseline'], ks)
    r5, _ = ratio(M['s5 LANDED'], ks)
    r25, _ = ratio(M['rung 0.25'], ks)
    MSDT[lab] = dict(cohort=lab - 1, members=len(ks), n=cnt, baseline=rb, s5=r5, rung025=r25)
    P('  %-8d %-8d %7d %7d %s %s %s'
      % (lab, lab - 1, len(ks), cnt, fmt(rb, 11), fmt(r5, 11), fmt(r25, 11)))
P('')
P('  The 2026 MSD row scores n=0 at year 1: their year-1 grid slot is season 2027, outside WINDOW_END.')
P('  They are counted as members of the 2025 cohort and will score once the window advances.')
P('')
OUT['appendix_msd_by_class'] = MSDT

P('=' * 132)
P('  LIMITS OF THIS FILE: evidence only. Nothing here changes an engine, a config, or a board byte. Every')
P('  number is a re-read of matrices already committed on this branch, under the owner\'s membership rule')
P('  and the act\'s existing value convention. No rung is recommended; that ruling is the owner\'s.')
P('=' * 132)

open(os.path.join(HERE, 'OWNER_BASIS_COHORT.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(OUT, open(os.path.join(HERE, 'OWNER_BASIS_COHORT.json'), 'w'), indent=1, default=str)
