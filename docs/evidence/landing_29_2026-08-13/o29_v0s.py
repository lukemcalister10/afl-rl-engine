#!/usr/bin/env python3
"""ORDER 29 -- STEPS 4, 5 and 6: THE POSITIONAL ND v0s, THE POOL v0s, AND THE NUMERAIRE RE-PIN.

STEP 4 (P7)  six positional ND v0 curves at EVERY pick 1..64, continuous per pick (not band steps),
             reconciling against THE CURVE THAT SHIPS.
STEP 5 (P8/P9) pool v0s per pathway x position on the MSD Way A basis, K-shrunk toward the pathway;
             the two n=0 cells published UNSIGNED (null), never as their fully-shrunk numbers.
STEP 6 (P10/P11) the numeraire re-pinned to the ruled ladder's own pre-anchor head, through the block
             _load_numeraire reads.

  usage: python3 o29_v0s.py <in_artifact.json> <out_artifact.json>
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
D28 = ROOT + '/docs/evidence/grace_adoption_2026-08-13/DERIVE28.json'
INP = ROOT + '/docs/evidence/grace_adoption_2026-08-13/inputs'
IN, OUT = sys.argv[1], sys.argv[2]

LOG = []
def P(s=''):
    print(s); LOG.append(s)

art = json.loads(open(IN).read(), object_pairs_hook=collections.OrderedDict)
CAND = json.load(open(D28))['candidate']
POSN = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']

ship = {int(k): int(v) for k, v in art['curve'].items()}          # THE CURVE THAT SHIPS (tiebroken, int)
pre = {int(k): float(v) for k, v in CAND['allin'].items()}        # the pre-tiebreak float all-in
AF = float(CAND['anchor_factor'])

P("=" * 116)
P("ORDER 29  --  STEPS 4, 5, 6:  POSITIONAL ND v0s / POOL v0s / THE NUMERAIRE RE-PIN")
P("=" * 116)
P("  input artifact   curve_md5 %s   (the TIEBROKEN, shipped curve)" % art['curve_md5'])

# ==================================================================== STEP 4
P()
P("STEP 4 -- POSITIONAL ND v0s AT EVERY PICK 1..64  (PREREG P7)")
P("-" * 116)
P()
P("  THE DECLARATION P7 REQUIRES, MADE BEFORE THE NUMBERS: what are the positional v0s v0s OF?")
P()
P("    The ORDER-28 lane derived, per pick, a positional RELATIVITY relat_g(p) and a population")
P("    SHARE share_g(p), with  SUM_g share_g(p) = 1  and  SUM_g share_g(p)*relat_g(p) = 1, so that")
P("    posv_g(p) = relat_g(p) * allin(p) reconciles to the all-in curve BY CONSTRUCTION.")
P()
P("    The tiebreak moved the all-in curve. The relativities are a POSITIONAL structure and the")
P("    tiebreak is an ORDERING convention on the all-in LEVEL -- it carries no positional content,")
P("    so it does not touch relat_g. THIS BUILD THEREFORE RE-BASES THE POSITIONAL v0s ONTO THE")
P("    TIEBROKEN SHIPPED CURVE:")
P()
P("            posv_g(p) = relat_g(p) * curve_SHIPPED(p)          <-- and NOT * allin_pre_tiebreak(p)")
P()
P("    RECONCILIATION IS AGAINST WHAT SHIPS. Had the v0s been left on the pre-tiebreak curve they")
P("    would reconcile to a ladder no consumer can read, and the reconciliation assert would be")
P("    measuring an object that is not on disk. The cost is disclosed rather than hidden: inside the")
P("    two tiebroken blocks a positional v0 moves by the same +-3 points, scaled by its relativity.")
P()
relat = {g: {int(k): float(v) for k, v in CAND['relat'][g].items()} for g in POSN}
share = {g: {int(k): float(v) for k, v in CAND['share'][g].items()} for g in POSN}
posv = {g: {p: relat[g][p] * ship[p] for p in ship} for g in POSN}

# ---- the reconciliation assert, on the PUBLISHED numbers
worst = 0.0; worstp = None
for p in sorted(ship):
    tot = sum(share[g][p] * posv[g][p] for g in POSN)
    rel = abs(tot / ship[p] - 1.0)
    if rel > worst: worst, worstp = rel, p
P("  RECONCILIATION  SUM_g share_g(p)*posv_g(p) == curve_shipped(p)  for every pick 1..64")
P("     max |ratio - 1|   %.3e   at pick %d        P7 bound 1e-12   %s"
  % (worst, worstp, "HELD" if worst < 1e-12 else "BREACH"))
assert worst < 1e-12, 'P7 reconciliation breached: %.3e at pick %d' % (worst, worstp)
_shsum = max(abs(sum(share[g][p] for g in POSN) - 1.0) for p in ship)
P("     max |SUM_g share_g(p) - 1|   %.3e" % _shsum)
P("     continuity: published at EVERY pick 1..64, six positions, no band steps   %s"
  % all(len(posv[g]) == 64 for g in POSN))

# ---- per-position monotonicity is NOT enforced (owner lean); ascents DISCLOSED as data
P()
P("  PER-POSITION MONOTONICITY IS NOT ENFORCED (owner lean). Ascents are DISCLOSED as data:")
asc_all = {}
for g in POSN:
    a = [p for p in range(1, 64) if posv[g][p + 1] > posv[g][p]]
    asc_all[g] = a
    P("     %-5s ascents %2d  %s" % (g, len(a), (str(a[:14]) + (' ...' if len(a) > 14 else '')) if a else 'none'))
P()
P("  THE RUCK RELATIVITY FLOOR AT PICKS 63-64 (ORDER 28 SS9.4) -- RE-DECLARED, not rediscovered.")
P("  THE FLOOR VALUE IS ZERO, and that is stated plainly rather than left to be discovered in a table:")
P("  the per-position local-linear fit goes NEGATIVE in the thinnest part of the tail and is floored at")
P("  0 by the estimator's own `floored` flag -- never silently clipped. So the printed RUCK day-0 v0 at")
P("  picks 63 and 64 is 0.0 board points. It is a THIN-CELL ARTEFACT of the last two picks; it does not")
P("  touch the all-in curve, and reconciliation still holds (max |ratio-1| above).")
for p in (61, 62, 63, 64):
    P("     pick %d  RUCK relat %.4f  posv %8.1f   (all-in %d)" % (p, relat['RUCK'][p], posv['RUCK'][p], ship[p]))
_floor = abs(relat['RUCK'][63] - relat['RUCK'][64]) < 1e-9
_floor0 = abs(relat['RUCK'][63]) < 1e-12 and abs(relat['RUCK'][64]) < 1e-12
P("     relat_RUCK(63) == relat_RUCK(64)  %s   and both are ZERO  %s" % (_floor, _floor0))
P("     -- the artefact PERSISTS through the tiebreak, exactly as P7 said it would. The tiebreak")
P("        touches picks 6-12 and 15-21 only, so it cannot reach picks 63-64 and does not.")

P()
P("  POSITIONAL v0s AT SELECTED PICKS (board points)")
P("  %-6s %s" % ('pick', ''.join('%10s' % g for g in POSN)))
for p in (1, 2, 5, 6, 9, 12, 15, 18, 21, 30, 40, 50, 64):
    P("  %-6d %s" % (p, ''.join('%10.1f' % posv[g][p] for g in POSN)))

art['nd_v0'] = collections.OrderedDict([
    ('_doc', 'PREREG P7 / ORDER 29 STEP 4. Six POSITIONAL national-draft day-0 v0 curves, published at '
             'EVERY pick 1..64 -- continuous per pick, NEVER band steps. Construction: '
             'posv_g(p) = relat_g(p) * curve(p), where curve(p) is THE SHIPPED (tiebroken) all-in curve in '
             'this same artifact and relat_g is the ORDER-28 positional relativity. The reconciliation '
             'SUM_g share_g(p)*posv_g(p) == curve(p) therefore holds against WHAT SHIPS, not against the '
             'pre-tiebreak curve; measured max |ratio-1| is recorded below. The -1-point ordering tiebreak '
             'carries no positional content, so relat_g is untouched by it. PER-POSITION MONOTONICITY IS '
             'NOT ENFORCED (owner lean): ascents are published as data in `ascents`. This is a PRINTED '
             'day-0 object -- no pricing leg reads it in this act (the consumption rewire is deferred, '
             'owner-ruled).'),
    ('basis', 'ORDER-28 candidate lane (DERIVE28.json::candidate), re-based onto the shipped tiebroken curve'),
    ('positions', POSN),
    ('reconciliation', collections.OrderedDict([
        ('identity', 'sum_g share_g(p) * posv_g(p) == curve(p)  for every pick 1..64'),
        ('max_abs_ratio_minus_1', worst), ('at_pick', worstp), ('bound', 1e-12), ('verdict', 'HELD')])),
    ('ruck_floor_63_64', collections.OrderedDict([
        ('_doc', 'ORDER 28 §9.4, RE-DECLARED here rather than rediscovered. THE FLOOR VALUE IS ZERO: the '
                 'per-position local-linear fit goes NEGATIVE in the thinnest part of the tail and is floored '
                 'at 0 by the estimator\'s own `floored` flag, never silently clipped. The printed RUCK day-0 '
                 'v0 at picks 63 and 64 is therefore 0.0 board points -- a thin-cell artefact of the last two '
                 'picks. It does not touch the all-in curve and reconciliation still holds. The -1 ordering '
                 'tiebreak reaches picks 6-12 and 15-21 only, so it cannot and does not affect this.'),
        ('relat_63', relat['RUCK'][63]), ('relat_64', relat['RUCK'][64]), ('equal', bool(_floor)),
        ('both_zero', bool(_floor0)), ('posv_63', posv['RUCK'][63]), ('posv_64', posv['RUCK'][64])])),
    ('ascents', collections.OrderedDict((g, asc_all[g]) for g in POSN)),
    ('share', collections.OrderedDict((g, collections.OrderedDict((str(p), share[g][p]) for p in sorted(ship))) for g in POSN)),
    ('posv', collections.OrderedDict((g, collections.OrderedDict((str(p), posv[g][p]) for p in sorted(ship))) for g in POSN)),
])

# ==================================================================== STEP 5
P()
P("STEP 5 -- POOL v0s, MSD WAY A BASIS, K-SHRUNK TOWARD THE PATHWAY  (PREREG P8 / P9)")
P("-" * 116)
cells_raw = CAND['cells']
anch_path = CAND['anchored_path']

# ---- the n=0 cells, MEASURED from the fit population rather than taken on trust
L2 = json.load(open(INP + '/LAYER2.json'))
L1 = json.load(open(INP + '/layer1_player_seasons.json'))
by = {x['key']: x for x in L1['entries']}
ncell = collections.Counter()
for k in L2['fit_pool_keys']:
    e = by.get(k)
    if e: ncell[(e['mechanism'], e['position_group'])] += 1
P("  CELL FIT COUNTS n, MEASURED from LAYER2::fit_pool_keys x Layer-1 position_group (954 rows):")
P("  %-8s%s%8s" % ('path', ''.join('%8s' % g for g in POSN), 'total'))
for m in POOLM:
    P("  %-8s%s%8d" % (m, ''.join('%8d' % ncell[(m, g)] for g in POSN), sum(ncell[(m, g)] for g in POSN)))
UNSIGNED = sorted('%s|%s' % (m, g) for m in POOLM for g in POSN if ncell[(m, g)] == 0)
P()
P("  n=0 CELLS MEASURED: %s      P9 predicted exactly PDN|KPF and PDS|KPF   %s"
  % (UNSIGNED, "HELD" if UNSIGNED == ['PDN|KPF', 'PDS|KPF'] else "BREACH"))
assert UNSIGNED == ['PDN|KPF', 'PDS|KPF'], UNSIGNED

P()
P("  THE PATHWAY LEVELS (anchored board points), and P8's predictions:")
P8 = {'MSD': 334.6, 'ND>64': 263.9, 'RD': 230.6, 'SSP': 216.1, 'PDA': 187.9,
      'UNR': 124.7, 'PDN': 111.0, 'PDS': 101.0, 'IRE': 94.5}
P("  %-7s %5s %11s %11s %11s %9s %8s %8s" % ('path', 'n', 'raw', 'shrunk', 'ANCHORED', 'P8 pred', 'verdict', 'nd eq'))
p8bad = []
for m in sorted(POOLM, key=lambda x: -anch_path[x]):
    ok = abs(anch_path[m] - P8[m]) <= 0.05
    if not ok: p8bad.append(m)
    P("  %-7s %5d %11.1f %11.1f %11.3f %9.1f %8s %8s"
      % (m, CAND['pathways'][m]['n'], CAND['pathways'][m]['raw'], CAND['pathways'][m]['shrunk'],
         anch_path[m], P8[m], 'HELD' if ok else 'BREACH', CAND['nd_equiv'][m]))
P("  P8 pathway levels: %s" % ('ALL NINE HELD' if not p8bad else 'BREACH at %s' % p8bad))

P()
P("  THE CELLS (anchored board points = raw cell x anchor_factor %.12f)" % AF)
P("  %-8s%s" % ('path', ''.join('%10s' % g for g in POSN)))
cells_out = collections.OrderedDict()
declined = collections.OrderedDict()
for m in POOLM:
    row = []
    for g in POSN:
        key = '%s|%s' % (m, g)
        if key in UNSIGNED:
            cells_out[key] = None
            declined[key] = round(cells_raw[key] * AF, 1)
            row.append('UNSIGNED')
        else:
            cells_out[key] = cells_raw[key] * AF
            row.append('%.0f' % cells_out[key])
    P("  %-8s%s" % (m, ''.join('%10s' % v for v in row)))
P()
P("  P9 -- THE TWO EMPTY CELLS STAY UNSIGNED, published as null and NOT as their numbers.")
P("     The derivation DID produce a number for each, and it is recorded here so it is provable")
P("     that a number existed and was DECLINED rather than never computed:")
for k, v in declined.items():
    P("       %-10s fully-shrunk anchored value %6.1f   -> PUBLISHED AS null (UNSIGNED)" % (k, v))
P("     P9 predicted 92.4 and 84.0    MEASURED %s   %s"
  % (list(declined.values()),
     "HELD" if [round(v) for v in declined.values()] == [92, 84] else "BREACH"))

art['pool_v0'] = collections.OrderedDict([
    ('_doc', 'PREREG P8/P9 / ORDER 29 STEP 5. The printed POOL day-0 object: per pathway x day-0 position '
             'cells on the MSD Way A basis, K-shrunk toward the pathway level (K=15), anchored into board '
             'points by the ladder anchor factor. THE TWO n=0 CELLS ARE UNSIGNED (null) BY RULING -- a cell '
             'with no fit rows takes no number, and the fully-shrunk numbers the derivation would have given '
             'them are recorded in `declined_unsigned` so it is provable they were DECLINED rather than never '
             'computed. A loud boot assert (rl_model.py) HALTS if any entrant ever maps to an unsigned cell. '
             'This is a PRINTED day-0 object -- no pricing leg reads it in this act; the signed per-division '
             'entry anchors the engine actually consumes remain the #326 `pool_levels` block above, untouched.'),
    ('basis', 'MSD Way A, K=15 shrink toward the pathway level; ORDER-28 candidate lane'),
    ('k', 15),
    ('anchor_factor', AF),
    ('positions', POSN),
    ('pathways', POOLM),
    ('pathway_levels_anchored', collections.OrderedDict((m, anch_path[m]) for m in POOLM)),
    ('pathway_nd_equivalent', collections.OrderedDict((m, CAND['nd_equiv'][m]) for m in POOLM)),
    ('cell_fit_n', collections.OrderedDict(('%s|%s' % (m, g), ncell[(m, g)]) for m in POOLM for g in POSN)),
    ('unsigned_cells', UNSIGNED),
    ('declined_unsigned', declined),
    ('cells', cells_out),
])

# ==================================================================== STEP 6
P()
P("STEP 6 -- THE NUMERAIRE RE-PIN, THROUGH THE BLOCK _load_numeraire READS  (P10 / P11)")
P("-" * 116)
H = float(CAND['head'])
old = dict(art['numeraire'])
pin = float(old['published_pin'])
s_new = pin / H
P("  pooled_head_pre_scale  %.10f -> %.10f" % (old['pooled_head_pre_scale'], H))
P("  published_pin          %.1f -> %.1f   (unmoved: the standing law pins pick 1 = 3000)" % (old['published_pin'], pin))
P("  s = published_pin / H  %.16f -> %.16f" % (old['s'], s_new))
P("  P10 predicted new s    0.9400914291048137   MEASURED %.16f   %s"
  % (s_new, "HELD" if abs(s_new - 0.9400914291048137) < 1e-15 else "BREACH"))
_ratio = s_new / old['s']
P("  player re-denomination s_new/s_old = %.12f" % _ratio)
P("  P11 predicted x0.945715            MEASURED x%.12f   diff %+.3e (rel %+.2e)"
  % (_ratio, _ratio - 0.945715, (_ratio - 0.945715) / 0.945715))
P("  P11's QUOTED CONSTANT IS BREACHED IN ITS 6th DECIMAL, and the breach is P11's OWN ARITHMETIC:")
P("     P11's ratio is inconsistent with P10's s, which P10 predicted EXACTLY right. Carrying P11's")
P("     0.945715 through the same s_old would imply s_new = %.10f, not the %.10f that P10 named and"
  % (old['s'] * 0.945715, s_new))
P("     this build measured. So the prediction that failed is the DERIVED ratio, not the numeraire:")
P("     the substantive P11 claim -- both sides re-denominate together, by ~x0.9457, no one-sided")
P("     scaling -- HOLDS. Owned by number rather than rounded into agreement.")
P("  E6 coherence |pin/H - s| = %.3e   (_load_numeraire HALTs above 1e-9)" % abs(pin / H - s_new))
P("  the anchor identity: H * anchor_factor = %.6f  == the published pin %.1f   %s"
  % (H * AF, pin, "HELD" if abs(H * AF - pin) < 1e-6 else "BREACH"))
assert abs(pin / H - s_new) < 1e-12
art['numeraire'] = collections.OrderedDict([
    ('_doc', 'ORDER 29 STEP 6 (#279 ruled pooled numeraire, PREREG P10/P11). THE MEASURED HEAD IS PRIMITIVE: '
             'pooled_head_pre_scale is the ruled ladder\'s OWN lane-measured pre-anchor head '
             '3191.178971663107, and s is DERIVED from it at full precision as published_pin / head. E6 '
             'coherence (published_pin / pooled_head_pre_scale == s to 1e-9) holds BY CONSTRUCTION and is '
             're-asserted by _load_numeraire on every build. RE-MEASURED AT THE ORDER-29 LANDING, on the '
             'ORDER-28/26B-C2 lane; the prior value 3017.9232 was measured on the item-271/#328 lane. THE '
             'LANE CHANGE IS A REAL CHANGE OF MEASURING STICK and is disclosed as such, not hidden inside '
             'the ratio. NOTE the engine\'s export log line "L7 NUMERAIRE RE-BASE /1.0524" is the '
             'DISPLAY-SIDE re-base divisor, a DIFFERENT object from this s (settled at P10).'),
    ('basis', 'pooled'),
    ('pooled_head_pre_scale', H),
    ('published_pin', pin),
    ('s', s_new),
    ('supersedes', collections.OrderedDict([('pooled_head_pre_scale', old['pooled_head_pre_scale']),
                                            ('s', old['s']), ('lane', 'item-271 / #328 re-closure')])),
])

json.dump(art, open(OUT, 'w'), indent=1)
P()
P("  written: %s" % OUT)
open(HERE + '/V0S29_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'recon_max': worst, 'recon_at': worstp, 'ascents': asc_all, 'unsigned': UNSIGNED,
           'declined': declined, 'cell_fit_n': {'%s|%s' % (m, g): ncell[(m, g)] for m in POOLM for g in POSN},
           'pathway_levels': anch_path, 's_old': old['s'], 's_new': s_new,
           'head_old': old['pooled_head_pre_scale'], 'head_new': H,
           'redenomination': s_new / old['s']},
          open(HERE + '/V0S29.json', 'w'), indent=1)
