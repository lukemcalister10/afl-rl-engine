"""TASK 1 -- THE POPULATION QUESTION (directive D8 iii). It gates task 5.

THE QUESTION: were pool rows inside the retention surface R's OWN derivation population?

THE DIRECTIVE'S POSITION, quoted exactly (D8 iii):
  "Whether pool rows were IN that derivation population cannot be determined from the derivation
   script -- session_2026-07-03/d13/scripts/d13_derive.py reads `pick` clamped to [1,90], and rookie
   picks carried numbers on the old 1-99 ladder."

THAT IS TRUE OF d13_derive.py, AND d13_derive.py IS THE CONSUMER, NOT THE PRODUCER.
  d13_derive.py:15        ->  json.load(open('session_2026-07-03/d13/d13_normcells.json'))
  d13_norm_harvest.py:62  ->  writes that same file.

The population is defined by the HARVEST, and the harvest survives in the repo. Its gate is explicit
(d13_norm_harvest.py:43-52):

    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue    # (1) pos group
        if not (p.get('pick') or p.get('_ft')):                     continue   # (2) pick-or-ft
        dy = draftyr(p)                                                        # = cp.debutyr(p) - 1
        if dy < 2003 or dy > 2024:                                  continue   # (3) draft-year window

THERE IS NO _pool GATE. Pool rows were not categorically excluded. Entry is decided by gate (2), and
gate (2) is NOT uniform across pool pathways, because `_ft` is assigned per pathway in rl_model.py
:262-281 and the STORE PICK is present for some pool pathways and absent for others:

    ND (any pick, incl >64)      _ft=True   + stored pick   -> IN
    RD / PSD                     _ft=True   + stored pick   -> IN
    MSD                          _ft=False  + stored pick   -> IN  (enters on the pick alone)
    SSP IRE UNR PDA PDN PDS      _ft=False  + NO stored pick-> OUT

TWO FIELD CORRECTIONS THIS SCRIPT MAKES AGAINST A FIRST DRAFT OF ITSELF, both found by checking
rather than by assuming, and both recorded because each reversed a conclusion:

  (A) THE PICK FIELD. The matrix's `pick` is the ENGINE'S EFFECTIVE pick and reads the constant 65 for
      every pool row. The harvest reads MA.data's `pick`, which is the STORE pick -- carried on the
      matrix as `pick_stored` / `raw_pick` (identical to each other on all 2645 rows). Reading `pick`
      would wrongly report every pool pathway as carrying a pick and therefore as IN.

  (B) THE YEAR FIELD. draftyr = cp.debutyr(p) - 1, and conditional_prior.py:51 defines
      debutyr(p) = p['year'] if type=='MSD' else p['year']+1 -- a pure function of the STORED DRAFT
      YEAR, never of the first game played. So draftyr = p['year'] (non-MSD) / p['year']-1 (MSD).
      The matrix's `debut` field is the ACTUAL first-game year and is null for the 708 never-played
      rows. Using `debut` would exclude every never-played row -- which is precisely the SIT-OUT
      SUBSET the surface is derived on, i.e. it would have inverted the answer.

READ-ONLY. No emits. Deterministic.
"""
import json, collections, os

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/afl-rl-engine'
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']

P = print
P("=" * 110)
P("TASK 1 -- THE POPULATION QUESTION (D8 iii): were pool rows inside retention surface R's derivation population?")
P("=" * 110)
P()
P("SOURCE OF THE POPULATION DEFINITION")
P("  producer : session_2026-07-03/d13/scripts/d13_norm_harvest.py   (BUILDS d13_normcells.json)")
P("  consumer : session_2026-07-03/d13/scripts/d13_derive.py         (reads it; the directive cites this one)")
P("  artefact : session_2026-07-03/d13/d13_normcells.json            -> %s" % (
    "PRESENT" if os.path.exists(f'{ROOT}/session_2026-07-03/d13/d13_normcells.json')
    else "ABSENT -- population RECONSTRUCTED by gate replay"))
P("  matrix   : per_entrant_SHIP.json  n=%d rows" % len(R))
P()


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick_stored') and 1 <= r['pick_stored'] <= 64: return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


GRP6 = {'MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK'}


def gate_pos(r):
    return r.get('pos') in GRP6


def ft_of(r):
    # rl_model.py:266,267 (ND all picks), :273,:277 (RD/PSD) -> True ; :281 (pickless mechanisms) -> False
    return r.get('type') in ('ND', 'RD', 'PSD')


def store_pick(r):
    return r.get('pick_stored')


def gate_pickft(r):
    return bool(store_pick(r)) or ft_of(r)


def draftyr(r):
    # cp.debutyr(p) - 1, with debutyr(p) = year if MSD else year+1   (conditional_prior.py:51)
    y = r.get('year')
    if y is None: return None
    return (y - 1) if r.get('type') == 'MSD' else y


def gate_year(r):
    dy = draftyr(r)
    return dy is not None and 2003 <= dy <= 2024


def in_population(r):
    return gate_pos(r) and gate_pickft(r) and gate_year(r)


ORDER = ['ND 1-64', 'ND>64', 'RD', 'MSD', 'SSP', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR']

P("=" * 110)
P("THE GATE, REPLAYED PER PATHWAY")
P("=" * 110)
P("  %-9s %6s | %7s %8s %8s | %7s %8s  %s" %
  ('pathway', 'n', 'g1 pos', 'g2 pk/ft', 'g3 year', 'IN', 'share', 'gate-2 basis'))
P("  " + "-" * 106)
rows_out = {}
for s in ORDER:
    sub = [r for r in R if stream(r) == s]
    if not sub: continue
    g1 = sum(1 for r in sub if gate_pos(r))
    g2 = sum(1 for r in sub if gate_pickft(r))
    g3 = sum(1 for r in sub if gate_year(r))
    inn = [r for r in sub if in_population(r)]
    rows_out[s] = (len(sub), len(inn))
    npk = sum(1 for r in sub if store_pick(r))
    basis = ("_ft=True + store pick %d/%d" % (npk, len(sub))) if ft_of(sub[0]) else \
            ("_ft=False; store pick %d/%d %s" % (npk, len(sub), "-> IN on pick" if npk else "-> OUT"))
    P("  %-9s %6d | %7d %8d %8d | %7d %7.1f%%  %s" %
      (s, len(sub), g1, g2, g3, len(inn), 100.0 * len(inn) / len(sub), basis))
P("  " + "-" * 106)
pool = [s for s in ORDER if s != 'ND 1-64']
pn = sum(rows_out[s][0] for s in pool if s in rows_out)
pi = sum(rows_out[s][1] for s in pool if s in rows_out)
P("  %-9s %6d | %7s %8s %8s | %7d %7.1f%%" % ('ALL POOL', pn, '', '', '', pi, 100.0 * pi / pn))
P()

P("=" * 110)
P("WHICH GATE EXCLUDES -- so every exclusion is attributable")
P("=" * 110)
P("  %-9s %6s | %9s %10s %9s %9s" % ('pathway', 'n', 'out:pos', 'out:pk/ft', 'out:year', 'out:any'))
P("  " + "-" * 106)
for s in ORDER:
    sub = [r for r in R if stream(r) == s]
    if not sub: continue
    P("  %-9s %6d | %9d %10d %9d %9d" % (
        s, len(sub),
        sum(1 for r in sub if not gate_pos(r)),
        sum(1 for r in sub if not gate_pickft(r)),
        sum(1 for r in sub if not gate_year(r)),
        sum(1 for r in sub if not in_population(r))))
P()

P("=" * 110)
P("THE DIRECTIVE'S OWN SUB-QUESTION: the [1,90] clamp and 'the old 1-99 rookie ladder'")
P("=" * 110)
P("  d13_derive.py clamps pick to [1,90] at :41 and :47. The clamp bites only on stored picks > 90.")
P("  Measured on the CURRENT store (%s):" % 'd9a24282')
P()
P("  %-9s %8s %9s %9s %9s %11s" % ('pathway', 'in-pop', 'min pick', 'max pick', '>64', '>90 CLAMPED'))
P("  " + "-" * 106)
clamped_total = 0
for s in ORDER:
    sub = [r for r in R if stream(r) == s and in_population(r)]
    v = [store_pick(r) for r in sub if store_pick(r)]
    if not v:
        P("  %-9s %8d %9s %9s %9s %11s" % (s, len(sub), '-', '-', '-', '-'))
        continue
    c = sum(1 for x in v if x > 90)
    clamped_total += c
    P("  %-9s %8d %9d %9d %9d %11d" % (s, len(sub), min(v), max(v), sum(1 for x in v if x > 64), c))
P()
P("  ROWS ACTUALLY CLAMPED BY [1,90], WHOLE STORE: %d" % clamped_total)
P("  The rookie ladder in THIS store tops out at %d, so the clamp the directive worried about is INERT."
  % max(store_pick(r) for r in R if r.get('type') == 'RD' and store_pick(r)))
P("  It is therefore not the reason the question was hard; gate (2) is.")
P()

# ---- depth-cell context (declared approximate) ----
P("=" * 110)
P("CELL-LEVEL CONTEXT (DECLARED APPROXIMATE)")
P("=" * 110)
P("  The harvest emits one cell per (player, Y) over Y in [dy+1, min(listed_through, 2025)], and")
P("  d13_derive keeps complete-window cells (Y <= 2021). `listed_through` depends on `_last_listed`")
P("  and `_retired`, which the matrix does not carry, so CELL COUNTS ARE NOT EXACTLY RECONSTRUCTIBLE.")
P("  Player-level membership above IS exact and is what the question asks. No cell count is asserted.")
P()

P("=" * 110)
P("VERDICT")
P("=" * 110)
P()
P("  THE QUESTION IS DETERMINABLE, and it is settled by the PRODUCER script, which survives in the")
P("  repo. The directive's statement is correct about d13_derive.py and is not correct as a claim")
P("  about the record as a whole. The seat reports this as a correction to the directive, not as a")
P("  disagreement with its ruling.")
P()
P("  THE ANSWER IS SPLIT BY PATHWAY. Neither of the directive's two stated possibilities is the whole")
P("  answer -- BOTH ARE TRUE AT ONCE, OF DIFFERENT PATHWAYS:")
P()
IN_S = [s for s in pool if s in rows_out and rows_out[s][1] > 0]
OUT_S = [s for s in pool if s in rows_out and rows_out[s][1] == 0]
nin = sum(rows_out[s][1] for s in IN_S)
nout = sum(rows_out[s][0] for s in OUT_S)
for s in IN_S:
    P("    IN   %-7s %3d of %3d rows" % (s, rows_out[s][1], rows_out[s][0]))
for s in OUT_S:
    P("    OUT  %-7s   0 of %3d rows  (pickless mechanism, _ft=False)" % (s, rows_out[s][0]))
P()
P("    -> pool rows IN  R's derivation population: %d  (%s)" % (nin, ', '.join(IN_S)))
P("    -> pool rows OUT of it:                     %d  (%s)" % (nout, ', '.join(OUT_S)))
P()
P("  CONSEQUENCE FOR H, in the directive's own framing:")
P("    - For RD, ND>64 and MSD (%d rows): pool rows WERE in R. `_h_cut` therefore charged the same" % nin)
P("      sit-out effect A SECOND TIME on rows R had already accounted for -- a DOUBLE CHARGE.")
P("    - For SSP/IRE/PDA/PDN/PDS/UNR (%d rows): they were NOT in R. `_h_cut` was a BOLT-ON to a" % nout)
P("      surface read outside its evaluated range (effpk=65 vs knots ending at 50).")
P()
P("  WHAT THIS DECIDES FOR TASK 5 (the directive: 'the answer decides whether the pool retention is a")
P("  genuinely new object or a correction to a mis-scoped one'):")
P("    IT IS BOTH, AND THE SPLIT IS THE REASON A SINGLE POOL-WIDE RETENTION CANNOT INHERIT FROM R.")
P("    A replacement derived on pool history is a CORRECTION for the %d rows R already saw and a NEW" % nin)
P("    OBJECT for the %d it never saw. Deriving one object per pathway on pool history alone is the" % nout)
P("    only construction that is right for both halves -- which is what D8 ruled, and the split is a")
P("    positive reason for that ruling rather than merely a consistent one.")
P()
P("  WHAT IS NOT DETERMINABLE, stated rather than papered over:")
P("    (i)   d13_normcells.json is ABSENT, so this is a GATE REPLAY, not a read-back. It reproduces")
P("          the gate exactly; it cannot prove the 2026-07-03 run met an identical roster.")
P("    (ii)  The harvest ran on engine af1fc6aa against a store that has since moved to d9a24282.")
P("          Row-level membership AT THAT ENGINE is not recoverable from here. The pathway-level")
P("          verdict is robust to this because it turns on `_ft` and on pick PRESENCE, both")
P("          structural, but individual row counts would differ.")
P("    (iii) `_double_count` is not carried on the matrix and is not reconstructible, so rows excluded")
P("          by that flag ALONE are invisible to this replay.")
P("    (iv)  Cell counts by depth are not reconstructible (listed_through unavailable) -- see above.")
P()

out = dict(
    determinable=True,
    verdict='SPLIT: RD/ND>64/MSD were IN (double charge); SSP/IRE/PDA/PDN/PDS/UNR were OUT (bolt-on)',
    producer='session_2026-07-03/d13/scripts/d13_norm_harvest.py',
    consumer='session_2026-07-03/d13/scripts/d13_derive.py',
    normcells_present=os.path.exists(f'{ROOT}/session_2026-07-03/d13/d13_normcells.json'),
    clamp_1_90_rows_affected=clamped_total,
    rd_max_store_pick=max(store_pick(r) for r in R if r.get('type') == 'RD' and store_pick(r)),
    per_pathway={s: dict(n=rows_out[s][0], in_pop=rows_out[s][1]) for s in rows_out},
    pool_in=nin, pool_out=nout,
    not_determinable=['normcells artefact absent (gate replay, not read-back)',
                      'row-level membership at engine af1fc6aa',
                      '_double_count flag not reconstructible',
                      'depth-cell counts (listed_through unavailable)'],
)
json.dump(out, open(os.path.join(HERE, 'PHASE1_POPULATION.json'), 'w'), indent=1)
P("wrote PHASE1_POPULATION.json")
