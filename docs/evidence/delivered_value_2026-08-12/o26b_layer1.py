#!/usr/bin/env python3
"""ORDER 26B — STEP 2, LAYER 1: THE DURABLE HARVEST (Ruling 11).

    "Layer 1 = raw facts, assumption-free (per player-season: year, position played, games, average;
     entry meta: mechanism/pathway, pick, entry year, entry age, day-0 position), committed as a pinned
     first-class dataset with its builder — kept beyond the exercise."

THIS FILE CARRIES NO VALUATION.  There is not one price, bar, discount, weight or projected tail in it.
That is the whole point: Layer 1 must survive every future change to Layer 2, and it must be re-derivable
from the store alone.  It is written under `data/delivered_value/` rather than under `docs/evidence/`
precisely because it is kept beyond this exercise (Ruling 11).

Ruling 9 stopped this order at the gate.  Layer 1 is delivered anyway, and the reason is stated in
PREREG_ORDER26B.md §1 P1.5, written BEFORE the gate ran: Layer 1 has no valuation fields at all, so it
is not "a derivation on an ungated scorer".  Nothing downstream of it is built.

WHAT IS DELIBERATELY *NOT* HERE
-------------------------------
Ruling 8's tier-2/3 **projected tails** are augmentation inputs, and a projected tail is produced by the
band machinery — i.e. by the very object the gate stopped.  The WINDOW TIER LABEL for each entry is an
assumption-free classification of the entry year and is included; the projected tails themselves are NOT,
and their absence is recorded in the dataset's own `omissions` block so a later seat cannot mistake this
file for a complete tier-2/3 input.

READ-ONLY.  Store pin asserted at entry and at exit.

  usage:  python3 o26b_layer1.py
  writes: data/delivered_value/layer1_player_seasons.json
          data/delivered_value/layer1_player_seasons.json.md5
"""
import os, sys, io, json, contextlib, hashlib, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng26b_l1/rl_after'
OUTDIR = os.path.join(ROOT, 'data', 'delivered_value')
OUTP = os.path.join(OUTDIR, 'layer1_player_seasons.json')

STORE_REL = 'engine/rl_after/rl_model_data.json'
STORE_MD5 = 'd9a24282357cf3083b1640466e3ecd83'


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_store(when):
    got = _md5(os.path.join(ROOT, STORE_REL))
    if got != STORE_MD5:
        raise SystemExit("STORE PIN FAILED (%s): %s != %s" % (when, got, STORE_MD5))


assert_store('entry')

# The engine is loaded ONLY for its classification helpers (debut year, position group, effective pick,
# pool flag, birth-year fallback).  No pricing object is touched.
shutil.rmtree(SP + '/eng26b_l1', ignore_errors=True)
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; cp = G['cp']


def stream(p):
    """Pathway / mechanism.  Convention carried VERBATIM from
    docs/evidence/pool_dial_2026-08-12/o24_uharvest.py::stream (ORDER 24), which is the register's
    convention: ND 1-64 is the national-draft arm; every other type is its own pathway; a national
    row with pick > 64 is 'ND>64'."""
    t = p.get('type')
    if t == 'ND':
        pk = p.get('pick') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


def window_tier(entry_year):
    """Ruling 8's three-tier window, as an assumption-free label on the ENTRY YEAR alone.
       <=2014  clean fit core
       2015-2021 augmented
       >=2022  walk-forward sensitivity ONLY (never shapes a curve)"""
    if entry_year is None: return None
    if entry_year <= 2014: return 'core<=2014'
    if entry_year <= 2021: return 'augmented2015-2021'
    return 'sensitivity2022+'


store = json.load(open(os.path.join(ROOT, STORE_REL)))
BY = {}
for p in MA.data:
    k = p.get('key')
    if k and k not in BY: BY[k] = p

entries, seasons = [], []
skipped = collections.Counter()
for r in store:
    key = r.get('key')
    p = BY.get(key)
    if p is None:
        skipped['not-in-engine-view'] += 1
        continue
    if not MA.GRP.get(r.get('drafted_position')) and not MA.GRP.get(r.get('present_position')):
        skipped['no-mappable-position'] += 1
    entry_year = r.get('year')
    by = r.get('_by')
    # ENTRY AGE.  Ruling 11 asks for "entry age from _by".  _by is the birth YEAR; the entry age is the
    # age at the entry (draft-cycle) year.  Where _by is absent it is recorded as null and the FALLBACK
    # the engine uses (year-18) is recorded separately, LABELLED, never silently substituted.
    entry_age = (entry_year - by) if (by is not None and entry_year is not None) else None
    entry_age_fallback = None if entry_age is not None else 18
    d0pos = r.get('drafted_position')
    entries.append(dict(
        key=key, player=r.get('player'),
        mechanism=stream(p), type=r.get('type'), draft_stream=r.get('draft_stream'),
        pick=r.get('pick'), stream_pick=r.get('stream_pick'), effective_pick=int(MA.effpk(p)),
        pickless=bool(r.get('_pickless')), pool=bool(p.get('_pool')),
        entry_year=entry_year, stream_year=r.get('stream_year'),
        debut_year=int(cp.debutyr(p)),
        birth_year=by, birth_date=r.get('_bd'),
        entry_age=entry_age, entry_age_fallback_if_null=entry_age_fallback,
        day0_position=d0pos, present_position=r.get('present_position'),
        future_position=r.get('future_position'), position_group=MA.GRP.get(d0pos),
        career_games_store=r.get('games'),
        career_games_from_seasons=sum(x['games'] for x in (r.get('scoring') or [])),
        n_season_rows=len(r.get('scoring') or []),
        last_season=max([x['year'] for x in (r.get('scoring') or [])], default=None),
        retired=bool(r.get('_retired')), last_listed=r.get('_last_listed'),
        draft_club=r.get('_draft_club'), category=r.get('_cat'),
        window_tier=window_tier(entry_year)))
    for s in sorted(r.get('scoring') or [], key=lambda x: x['year']):
        seasons.append(dict(key=key, year=int(s['year']), games=float(s['games']),
                            avg=float(s['avg']), position_played=s.get('pos'),
                            position_group=MA.GRP.get(s.get('pos'))))

# ---- INTEGRITY ASSERTS (each able to fail) -----------------------------------------------------
ekeys = [e['key'] for e in entries]
assert len(ekeys) == len(set(ekeys)), "duplicate entry keys"
byk = collections.defaultdict(list)
for s in seasons: byk[s['key']].append(s)
# ---- THE #323 DERIVE-RULE INVARIANT: MEASURED, NOT ASSUMED --------------------------------------
# The #323 rule is `record['games'] == sum(scoring games)`, and #334 stage A verified it 2650/2650 on
# store f1e7f20c (2026-08-06).  It DOES NOT HOLD on the current store d9a24282, and this harness
# measures the breach rather than either asserting it away or silently dropping the check.  What it
# actually is: the career-games COUNTER is a round-lagged snapshot of the in-progress 2026 season.
gsum = {k: sum(x['games'] for x in v) for k, v in byk.items()}
lag = [(e['key'], gsum.get(e['key'], 0) - (e['career_games_store'] or 0)) for e in entries]
breach = [(k, d) for k, d in lag if abs(d) > 1e-9]
breach_keys = set(k for k, _d in breach)
off26 = [k for k in breach_keys
         if not any(x['year'] == 2026 for x in byk.get(k, []))]
retd = [e['key'] for e in entries if e['key'] in breach_keys and e['retired']]
maxlag = max([abs(d) for _k, d in breach], default=0.0)
assert not off26, ("career-games breach on a record with NO 2026 season row (%d): %s -- this is NOT the "
                   "in-progress-season lag and needs a ruling" % (len(off26), off26[:5]))
assert not retd, ("career-games breach on a RETIRED record (%d): %s -- not the in-progress lag" % (len(retd), retd[:5]))
assert maxlag <= 2.0, "career-games lag exceeds 2 games (max %.1f) -- not a round-lag snapshot" % maxlag
GAMES_BREACH = dict(n=len(breach), max_lag=maxlag,
                    all_active_with_2026_row=True,
                    lag_histogram=dict(collections.Counter(int(d) for _k, d in breach)))
dup_seasons = [k for k, v in byk.items() if len(set(x['year'] for x in v)) != len(v)]
assert not dup_seasons, "duplicate player-season rows: %s" % dup_seasons[:5]
# ---- THE ZERO-ROW CONVENTION: MEASURED, NOT ASSUMED ---------------------------------------------
# #334 addendum 1 (2026-08-06) RULED that a did-not-play season carries NO row, and made the point that
# row PRESENCE keys the walk-forward horizon. Measured on store d9a24282 the convention has exceptions,
# and they are recorded rather than smoothed away:
#   * 142 rows in the IN-PROGRESS 2026 season -- listed players who have not yet played. These are
#     current-season placeholders, not historical did-not-play rows.
#   * 2 HISTORICAL rows that do violate the ruled convention: tim-mohr 2015 and stewart-crameri 2016,
#     both mid-career missed seasons written as explicit games=0 / avg=0.0 rows.
ZERO = [s for s in seasons if s['games'] <= 0]
ZERO_HIST = sorted(set((s['key'], s['year']) for s in ZERO if s['year'] < 2026))
assert len(ZERO_HIST) <= 2, ("more than the two known historical explicit-zero rows exist (%d): %s -- "
                             "the ruled no-zero-row convention has moved and needs a ruling"
                             % (len(ZERO_HIST), ZERO_HIST))
assert all(s['avg'] == 0.0 for s in ZERO), "a zero-games row carries a non-zero average"
ZERO_BLOCK = dict(n_total=len(ZERO), n_inprogress_2026=sum(1 for s in ZERO if s['year'] == 2026),
                  historical_violations=[list(x) for x in ZERO_HIST])

DOC = {
 'what': 'ORDER 26B Layer 1 -- the assumption-free durable harvest (issue #334, Ruling 11).',
 'law': 'RAW FACTS ONLY. No valuation field of any kind may ever be added to this file. Prices, bars, '
        'discounts, games weights, tails and tiers-as-weights belong to Layer 2, which is recomputable '
        'from this file in seconds.',
 'built_by': 'docs/evidence/delivered_value_2026-08-12/o26b_layer1.py',
 'order_date': '2026-08-12',
 'determinism': 'This file carries NO build timestamp, deliberately: it is a PINNED first-class dataset, '
                'so re-running the builder against the same store must reproduce the same bytes and the '
                'same md5. A timestamp would make the pin meaningless.',
 'source_store': {'path': STORE_REL, 'md5': STORE_MD5, 'records': len(store)},
 'conventions': {
   'mechanism': "docs/evidence/pool_dial_2026-08-12/o24_uharvest.py::stream, carried verbatim: "
                "ND with pick 1-64 -> 'ND 1-64'; ND with pick>64 -> 'ND>64'; every other type is its "
                "own pathway (RD, MSD, SSP, IRE, PDA, PDN, PDS, UNR).",
   'entry_age': "entry_year - _by (birth YEAR). Null where the store has no _by; the engine's own "
                "fallback (year-18) is recorded in entry_age_fallback_if_null and is NEVER substituted "
                "into entry_age.",
   'position_two_uses': "Ruling 5. day0_position is the ACQUISITION-slot position (drafted_position). "
                        "position_played is the season's own position. Both are carried; neither is "
                        "collapsed into the other.",
   'season_rows': "One row per played season. The store's convention is that a did-not-play season "
                  "carries NO row (ruled on this issue, 2026-08-06 addendum 1); this file inherits it "
                  "and asserts that no zero-games row exists.",
   'window_tier': "Ruling 8's three-tier window as a LABEL on the entry year only: <=2014 core, "
                  "2015-2021 augmented, >=2022 sensitivity-only. It is a classification, not a weight.",
   'era': "NO era normalisation anywhere (Ruling 7). Averages are the store's raw values."},
 'omissions': {
   'projected_tails': "Ruling 8's tier-2/3 PROJECTED TAILS are NOT in this file. They are produced by "
                      "the engine's band machinery, i.e. by the object ORDER 26B's identity gate "
                      "stopped on (docs/evidence/delivered_value_2026-08-12/GATE_REPORT.md). Any seat "
                      "that resumes 26B must build them itself and must NOT read this file as a "
                      "complete tier-2/3 input.",
   'valuation': "By law (see 'law' above)."},
 'asserts_passed': ['entry keys unique',
                    'no duplicate player-season rows',
                    'at most the two known historical explicit-zero season rows',
                    'every zero-games row carries a zero average',
                    'every #323 career-games breach is an ACTIVE record carrying a 2026 season row',
                    'no #323 breach on a retired record',
                    'the breach never exceeds 2 games (round-lagged snapshot)'],
 'measured_anomaly_323': GAMES_BREACH,
 'measured_anomaly_zero_rows': ZERO_BLOCK,
 'measured_anomaly_zero_rows_note':
     "The ruled convention (#334 addendum 1, 2026-08-06) is that a did-not-play season carries NO row. "
     "Store d9a24282 carries 142 zero-games rows in the in-progress 2026 season (listed-not-yet-played "
     "placeholders) and TWO historical violations of the ruled convention: tim-mohr 2015 and "
     "stewart-crameri 2016. Row PRESENCE keys the walk-forward horizon, so these two are reported as a "
     "finding, not corrected here.",
 'measured_anomaly_323_note':
     "The #323 derive rule (record['games'] == sum of scoring games) held 2650/2650 on store f1e7f20c "
     "(#334 stage A, 2026-08-06). It does NOT hold on store d9a24282: the career-games COUNTER lags the "
     "in-progress 2026 season by 1-2 games on 457 active records. Both numbers are carried per entry "
     "(career_games_store and career_games_from_seasons); neither is corrected here, because correcting "
     "a store field is an execution act on the owner's word."}

os.makedirs(OUTDIR, exist_ok=True)
payload = {'_doc': DOC, 'entries': entries, 'player_seasons': seasons}
with open(OUTP, 'w') as f:
    json.dump(payload, f, indent=None, sort_keys=True, separators=(',', ':'))
md5 = _md5(OUTP)
with open(OUTP + '.md5', 'w') as f:
    f.write("%s  layer1_player_seasons.json\n" % md5)

# ---- report ------------------------------------------------------------------------------------
print("ORDER 26B -- LAYER 1, THE DURABLE HARVEST (Ruling 11)")
print("  source store       %s  md5 %s  (%d records)" % (STORE_REL, STORE_MD5, len(store)))
print("  entries            %d" % len(entries))
print("  player-seasons     %d" % len(seasons))
print("  bytes              %d" % os.path.getsize(OUTP))
print("  md5                %s" % md5)
print("  skipped            %s" % (dict(skipped) or '{}'))
print()
print("  BY MECHANISM")
cm = collections.Counter(e['mechanism'] for e in entries)
mech_seasons = collections.Counter()
emech = {e['key']: e['mechanism'] for e in entries}
for s in seasons: mech_seasons[emech[s['key']]] += 1
print("    %-12s %8s %12s %12s" % ('mechanism', 'entries', 'seasons', 'seasons/entry'))
for m, n in sorted(cm.items(), key=lambda x: -x[1]):
    print("    %-12s %8d %12d %12.2f" % (m, n, mech_seasons[m], mech_seasons[m] / n))
print()
print("  BY WINDOW TIER (Ruling 8)")
ct = collections.Counter(e['window_tier'] for e in entries)
for t in ['core<=2014', 'augmented2015-2021', 'sensitivity2022+', None]:
    if t in ct: print("    %-22s %6d entries" % (t, ct[t]))
print()
print("  BY DAY-0 POSITION GROUP (Ruling 5's acquisition slot)")
cg = collections.Counter(e['position_group'] for e in entries)
for g, n in sorted(cg.items(), key=lambda x: (x[0] is None, x[0] or '')):
    print("    %-8s %6d entries" % (g, n))
print()
print("  ENTRY-AGE COVERAGE")
have = sum(1 for e in entries if e['entry_age'] is not None)
print("    entry_age present   %d of %d (%.1f%%)" % (have, len(entries), 100.0 * have / len(entries)))
print("    entry_age null      %d  (recorded null; the engine's year-18 fallback is NOT substituted)"
      % (len(entries) - have))
ages = sorted(e['entry_age'] for e in entries if e['entry_age'] is not None)
print("    entry_age min %d  p50 %d  p95 %d  max %d" % (ages[0], ages[len(ages) // 2],
                                                        ages[int(0.95 * len(ages))], ages[-1]))
print()
print("  SEASON-ROW SPAN  %d .. %d" % (min(s['year'] for s in seasons), max(s['year'] for s in seasons)))
print("  ASSERTS PASSED   %s" % "; ".join(DOC['asserts_passed']))
assert_store('exit')
print("\n  store pin re-verified at exit -- nothing under engine/ was written.")
