#!/usr/bin/env python3
"""ORDER 26B-L / 26B-L2 -- THE PLAYER LEDGER, re-issued on the GRACE-A basis.

Owner request: one row per store player, for his own reading. NO DERIVATION CHANGES -- this file only
reads Layer 1 and Layer 2 and lays them out. Nothing here feeds a curve, a cell or an instrument.

    writes  data/delivered_value/PLAYER_LEDGER.csv   (all 2,650 players, one row each)
            data/delivered_value/PLAYER_LEDGER.md    (top 60 by grace-A value + definitions)

RE-ISSUE (26B-L2): the first issue was built pre-grace, on a reading that the owner's "before the
year 1 grace thing" was an instruction to exclude grace. It was not -- he was naming the KIND of
rating he meant. The ledger now leads with GRACE-A, the current ruled basis, and keeps the pre-grace
number beside it as the baseline.

THE THREE VALUE COLUMNS, all OBSERVED ONLY -- no projected tail anywhere in this file:
  * GRACE-A (CURRENT BASIS)  = LAYER2.json::grace_a[key].obs -- entry age <=19: seasons 1 and 2
    undiscounted, the 14%/yr fade starts at season 3; entry age 20+: unchanged.
  * BASELINE PRE-GRACE       = LAYER2.json::base[key].obs -- the flat-14 score's observed leg, fade
    from season 1 for everybody.
  * RAW UNDISCOUNTED         = LAYER2_NODISC.json::obs[key].obs -- the SAME season valuation (bars
    via the engine's netting path, identical games weighting) with the discount OFF. UNCHANGED by
    grace: with no discount there is no exponent to shift.

The grace-A leg was already computed and cached by the 26B-V variants run, so this re-issue is pure
arithmetic on LAYER2.json -- no engine re-boot.

DETERMINISTIC: no timestamp is written, so re-running against the same inputs reproduces the same
bytes and the same md5. READ-ONLY on the engine; the store pin is asserted at entry and at exit.

  usage:  python3 o26b_ledger.py
"""
import os, sys, csv, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUTDIR = os.path.join(ROOT, 'data', 'delivered_value')
CSVP = os.path.join(OUTDIR, 'PLAYER_LEDGER.csv')
MDP = os.path.join(OUTDIR, 'PLAYER_LEDGER.md')
STORE_REL = 'engine/rl_after/rl_model_data.json'
STORE_MD5 = 'd9a24282357cf3083b1640466e3ecd83'
L1_MD5 = 'ad1229ea6f443538479447132382b21c'


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = []
    if _md5(os.path.join(ROOT, STORE_REL)) != STORE_MD5:
        bad.append('store %s' % _md5(os.path.join(ROOT, STORE_REL)))
    if _md5(os.path.join(OUTDIR, 'layer1_player_seasons.json')) != L1_MD5:
        bad.append('layer1 %s' % _md5(os.path.join(OUTDIR, 'layer1_player_seasons.json')))
    if bad:
        raise SystemExit('PIN ASSERTION FAILED (%s): %s' % (when, '; '.join(bad)))


assert_pins('entry')

L1 = json.load(open(os.path.join(OUTDIR, 'layer1_player_seasons.json')))
L2 = json.load(open(os.path.join(HERE, 'LAYER2.json')))
# The RAW UNDISCOUNTED column lives in its own side file, written by `o26b_layer2.py --ledger`, so
# that adding a read-only reporting column does not move LAYER2.json's md5 and invalidate the three
# committed artifacts that quote it (DERIVE / COMPARE / VARIANTS).
ND = json.load(open(os.path.join(HERE, 'LAYER2_NODISC.json')))
assert ND['layer1_md5'] == L1_MD5, 'LAYER2_NODISC.json was built against a different Layer 1'
E = {e['key']: e for e in L1['entries']}
BASE = L2['base']; NODISC = ND['obs']; GRACEA = L2['grace_a']; ATTR = L2['attribution']
# The grace-A observed leg is ALREADY in LAYER2.json (written by the 26B-V variants run) -- this
# re-issue is pure arithmetic on a cached field, with no engine re-boot. Reading O, the primary
# reading: exponent max(0, k - 2) for entry age <=19, unchanged for 20+.
assert 'grace-A: G_O = 2 if entry_age <= 19 else 0' in L2['grace_cfg']['reading_O'], \
    'the grace-A rule in LAYER2.json is not the one this ledger claims to print'
assert set(NODISC) == set(BASE), 'the undiscounted run and the flat-14 run cover different players'
FM = L2['force_majeure']; FMK = set(FM['excluded_keys'])
FITND = set(L2['fit_nd_keys']); FITPOOL = set(L2['fit_pool_keys'])

# THE _pvc_exclude FLAG, read straight off the store. It is NOT in Layer 1 (Layer 1 carries raw
# facts; this is an engine-side teaching flag), and this order's derivation therefore did NOT honour
# it -- see PLAYER_LEDGER.md "NUANCES". Reported here as a flag so the fact is visible per row.
store = json.load(open(os.path.join(ROOT, STORE_REL)))
PVCX = set(r.get('key') for r in store if r.get('_pvc_exclude'))

TIER = {'core<=2014': 'FIT-TIER-core', 'augmented2015-2021': 'FIT-TIER-augmented',
        'sensitivity2022+': 'FIT-TIER-sensitivity'}

rows = []
for k in sorted(E):
    e = E[k]; a = ATTR.get(k, {})
    is_nd = (e['type'] == 'ND')
    flags = []
    if k in FMK: flags.append('FORCE-MAJEURE-EXCLUDED')
    if not e['retired']: flags.append('ACTIVE')
    if e['window_tier'] in TIER: flags.append(TIER[e['window_tier']])
    if e['entry_year'] is not None and e['entry_year'] < 2004: flags.append('PRE-2004-OUT-OF-WINDOW')
    if k in PVCX: flags.append('STORE-PVC-EXCLUDE')
    if e['pickless']: flags.append('PICKLESS')
    if a.get('slid'): flags.append('SLID-2013-14')
    if k in FITND: flags.append('IN-ND-CURVE-FIT')
    elif k in FITPOOL: flags.append('IN-POOL-CELL-FIT')
    rows.append(dict(
        key=k,
        stream=(a.get('mechanism') or e['mechanism'] or ''),
        entry_year=(e['entry_year'] if e['entry_year'] is not None else ''),
        natural_pick=(e['pick'] if e['pick'] else ''),
        attributed_pick=(a.get('pick') if (is_nd and a.get('pick')) else ''),
        day0_position=(e['position_group'] or ''),
        n_seasons=e['n_season_rows'],
        career_games=e['career_games_from_seasons'],
        observed_discounted_grace_a=round(GRACEA[k]['obs'], 2),
        observed_discounted_flat14_baseline=round(BASE[k]['obs'], 2),
        raw_undiscounted_value=round(NODISC[k]['obs'], 2),
        grace_a_over_baseline=(round(GRACEA[k]['obs'] / BASE[k]['obs'], 4)
                               if BASE[k]['obs'] > 0 else ''),
        flags='|'.join(flags),
        player=e['player'] or ''))

COLS = ['key', 'stream', 'entry_year', 'natural_pick', 'attributed_pick', 'day0_position',
        'n_seasons', 'career_games',
        'observed_discounted_grace_a',            # <- THE CURRENT-BASIS RATING
        'observed_discounted_flat14_baseline',    # <- the pre-grace baseline
        'raw_undiscounted_value', 'grace_a_over_baseline', 'flags', 'player']
os.makedirs(OUTDIR, exist_ok=True)
with open(CSVP, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
    w.writeheader()
    for r in rows: w.writerow(r)

top = sorted(rows, key=lambda r: -r['observed_discounted_grace_a'])[:60]

# ---- RANK MOVERS between the two observed columns ------------------------------------------------
# grace-A multiplies a <=19 entrant by ~1.30 and leaves a 20+ entrant at exactly 1.0000, so the two
# rankings differ purely by entry age. Ranked over players with a non-zero BASELINE, so a rank is a
# meaningful thing to hold.
# MATERIAL careers only. A rank move inside the block of players tied at 0.00 is an artefact of tie
# ordering, not a fact about anybody -- the first cut of this table was 12 of 15 zero-valued rows.
# Threshold stated on the face of the table.
RANK_FLOOR = 100.0
_rk = [r for r in rows if r['observed_discounted_flat14_baseline'] >= RANK_FLOOR]
_by_base = sorted(_rk, key=lambda r: -r['observed_discounted_flat14_baseline'])
_by_gr = sorted(_rk, key=lambda r: -r['observed_discounted_grace_a'])
RANK_BASE = {r['key']: i + 1 for i, r in enumerate(_by_base)}
RANK_GR = {r['key']: i + 1 for i, r in enumerate(_by_gr)}
for r in _rk:
    r['_rank_base'] = RANK_BASE[r['key']]
    r['_rank_grace'] = RANK_GR[r['key']]
    r['_rank_move'] = RANK_BASE[r['key']] - RANK_GR[r['key']]   # +ve = moved UP under grace-A
DOWN = sorted(_rk, key=lambda r: r['_rank_move'])[:15]           # biggest slides
UP = sorted(_rk, key=lambda r: -r['_rank_move'])[:15]            # biggest rises
_ages = {}
for r in _rk:
    ea = E[r['key']]['entry_age'] or E[r['key']]['entry_age_fallback_if_null']
    _ages[r['key']] = ea


def rline(r):
    ea = _ages[r['key']]
    return ("| `%s` | %s | %s | %s | %s | %s | %s | %s | %+d |"
            % (r['key'], r['player'], r['stream'], r['entry_year'], ea,
               '{:,.1f}'.format(r['observed_discounted_grace_a']),
               '{:,.1f}'.format(r['observed_discounted_flat14_baseline']),
               '%d → %d' % (r['_rank_base'], r['_rank_grace']), r['_rank_move']))


RHDR = ("| key | player | stream | entry | entry age | grace-A | baseline | rank base → grace-A | "
        "move |\n|---|---|---|---|---|---|---|---|---|")
NAMED = ['joshua-kelly', 'christian-petracca', 'jason-horne-francis', 'willem-duursma',
         'callum-moore', 'thomas-boyd', 'paddy-mccartin', 'harrison-ramm', 'vigo-visentini',
         'jai-newcombe']
BYK = {r['key']: r for r in rows}


def line(r):
    return ("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s | %s |"
            % (r['key'], r['player'], r['stream'], r['entry_year'],
               r['natural_pick'] if r['natural_pick'] != '' else '—',
               r['attributed_pick'] if r['attributed_pick'] != '' else '—',
               r['day0_position'], r['n_seasons'], r['career_games'],
               '{:,.1f}'.format(r['observed_discounted_grace_a']),
               '{:,.1f}'.format(r['observed_discounted_flat14_baseline']),
               '{:,.1f}'.format(r['raw_undiscounted_value']),
               r['flags'].replace('|', ' · ') or '—'))


HDR = ("| key | player | stream | entry | nat. pick | attr. pick | d0 pos | seasons | games | "
       "**GRACE-A (current basis)** | baseline pre-grace | raw undiscounted | flags |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|")

s26 = [s for s in L1['player_seasons'] if s['year'] == 2026]
n26p = sum(1 for s in s26 if 0 < s['games'] < 10)
n26f = sum(1 for s in s26 if s['games'] >= 10)
n26z = sum(1 for s in s26 if s['games'] <= 0)

# TOKEN substitution, not %-formatting: this template is full of literal percent signs and a
# %-format would eat them.
MD = """# PLAYER LEDGER — ORDER 26B (re-issued 26B-L2, GRACE-A BASIS)

**One row per store player, 2,650 rows. Built for the owner's own reading. NO derivation changes.**

> ### THE RATING TO READ IS `observed_discounted_grace_a`
> **RE-ISSUED on the owner's clarification.** The first issue of this ledger was built pre-grace,
> on a reading that his *"before the year 1 grace thing"* was an instruction to exclude grace. It was
> not: he was citing the pre-grace number as **the KIND of rating he meant**, not asking for that
> basis. **The current ruled basis is grace-A**, and the ledger now leads with it.
>
> The pre-grace column is **kept as the baseline**, and the raw undiscounted column is **unchanged by
> grace** (no discount, nothing to shift).
>
> **Provenance, stated exactly:** relayed to this seat as ORDER 26B-L2, an owner clarification
> **still to be filed** on #334. `SHIPPING_PACKET_26B.md` §18 still carries grace-A as NOT-RULED
> because it was written before this clarification; the two will agree once the clarification is
> filed. **Nothing in this ledger feeds a derivation**, so no curve, cell or instrument moves either
> way.

| | |
|---|---|
| dataset | `PLAYER_LEDGER.csv` (md5 below) |
| builder | `docs/evidence/delivered_value_2026-08-12/o26b_ledger.py` |
| source store | `@STORE_REL@` md5 `@STORE_MD5@` |
| source Layer 1 | `layer1_player_seasons.json` md5 `@L1_MD5@` |
| source Layer 2 | `docs/evidence/delivered_value_2026-08-12/LAYER2.json` |
| rows | **@NROWS@** |

**Deterministic**: no timestamp is written, so re-running the builder against the same inputs
reproduces the same bytes and the same md5. Read-only: the store pin is asserted at entry and exit.

---

## COLUMN DEFINITIONS

| # | column | definition |
|---|---|---|
| 1 | `key` | the store's own player key |
| 2 | `stream` | the pathway the career was ATTRIBUTED to: `ND 1-64`, `ND>64`, `RD`, `SSP`, `MSD`, `IRE`, `PDA`, `PDN`, `PDS`, `UNR` |
| 3 | `entry_year` | draft / intake year (the store's `year`) |
| 4 | `natural_pick` | the pick as the store records it. **Blank for pickless pool entrants.** |
| 5 | `attributed_pick` | **the attribution the curve actually used.** ND rows only; blank for pool rows, which are attributed to pathway × day-0-position cells and never to a pick. |
| 6 | `day0_position` | the ACQUISITION-slot position group (Ruling 5) — the position on his card the day he arrived, not the position he ended up playing |
| 7 | `n_seasons` | played-season rows in the store |
| 8 | `career_games` | games summed from those season rows |
| 9 | **`observed_discounted_grace_a`** | **THE CURRENT-BASIS RATING.** Every played season valued at the position played that season against its replacement bar (via the engine's own netting path), games-weighted, summed — discounted back to acquisition under **grace-A**: for an entrant aged **≤19**, seasons 1 and 2 are **undiscounted** and the 14 %/yr fade starts at season 3; for an entrant aged **20+**, unchanged from the baseline. **Board points.** |
| 10 | `observed_discounted_flat14_baseline` | **the BASELINE, PRE-GRACE.** Identical in every respect except that the 14 %/yr fade starts at season 1 for everybody. This was column 9 of the first issue. |
| 11 | `raw_undiscounted_value` | **the same season valuation with the discount OFF** — identical bars, identical games weighting, every season counting equally. **Unchanged by grace**: with no discount there is no exponent to shift. The gap between 10 and 11 is purely the time-weighting. |
| 12 | `grace_a_over_baseline` | column 9 ÷ column 10. **Exactly 1.0000 for every 20+ entrant** and ~1.30 for a ≤19 entrant whose value sits past season 2. Blank where the baseline is 0. |
| 13 | `flags` | `·`-separated (see below) |
| 14 | `player` | display name — a convenience column |

### Flags

| flag | meaning |
|---|---|
| `FORCE-MAJEURE-EXCLUDED` | `thomas-boyd` / `paddy-mccartin` — the owner's standing force-majeure ruling. **Their values ARE in this ledger**; they were excluded from the *curve*, not from the record. |
| `ACTIVE` | not retired in the store |
| `FIT-TIER-core` / `-augmented` / `-sensitivity` | Ruling 8's window on the entry year: ≤2014 / 2015–2021 / 2022+ |
| `IN-ND-CURVE-FIT` / `IN-POOL-CELL-FIT` | which fit population the career actually fed |
| `SLID-2013-14` | slid up one pick by the force-majeure whole-draft slide |
| `STORE-PVC-EXCLUDE` | the store carries `_pvc_exclude=True` on this row — **see NUANCES 3** |
| `PICKLESS` | the store records no pick |
| `PRE-2004-OUT-OF-WINDOW` | entry before 2004, outside every fit population |

---

## WHAT COLUMN 9 IS AND IS NOT — read this before comparing rows

1. **NO PROJECTED TAILS ANYWHERE IN THIS FILE.** Column 9 is the measured record only. That is the
   owner's explicit instruction, and it is why `jason-horne-francis` appears here on his four played
   seasons alone rather than on the observed-plus-projection total the curve saw.
2. **For a CORE-TIER (≤2014) ND player, column 9 IS his curve contribution — for a concluded career,
   exactly; for the handful still playing, to within a tail of 0.6 % value-weighted.** Core-tier
   careers are almost all finished, so observed = total for them. **The exception is worth naming
   rather than rounding away**: `joshua-kelly` contributed 3,592.8 to the curve and shows 3,590.9
   here (tail 1.9); `christian-petracca` contributed 3,621.7 and shows 3,513.0 (tail 108.7). Both
   are still playing. So "exactly" holds for retired core-tier players and to ~0.6 % for the rest.
3. **For an AUGMENTED-TIER (2015–2021) player, column 9 is LESS than what he contributed.** Those
   careers fed the fit as observed **+ a gated projected tail**, and the tail is 37.0 % of the
   augmented tier's value. Column 9 deliberately omits it.
4. **For a SENSITIVITY-TIER (2022+) player, he contributed NOTHING to any fit.** Those entries are
   walk-forward sensitivity only and never shape a curve.
5. **Pool players fed pathway × position CELLS, not the pick curve.** Their column-5 attribution is
   blank for that reason.
6. **GRACE-A IS APPLIED — this supersedes the first issue's note.** The first issue said *"grace-A /
   grace-B are NOT applied. These are pre-grace numbers, as asked."* **That note is withdrawn.**
   Column 9 is the grace-A basis and is the rating to read; column 10 preserves the pre-grace number
   it replaced. **grace-B is still not applied** and remains a NOT-RULED variant
   (`SHIPPING_PACKET_26B.md` §18); it would lift a ≤19 entrant by ~1.46 rather than ~1.30.
7. **The two observed columns rank players differently, and the difference is entirely entry age.**
   grace-A multiplies a ≤19 entrant by ~1.30 and a 20+ entrant by exactly 1.0000, so **mature-age
   entrants slide down the rankings and teenagers rise** — with no change whatever to the seasons
   underneath. The biggest movers in both directions are listed at the end of this file. A rank
   difference here is a statement about the discount rule, **not** about the careers.
8. **A zero is a real zero.** A career whose every season sat at or below its replacement bar scores
   0 and stays in every denominator. @NZERO@ of the @NROWS@ rows score 0.00 in column 9.

## THE 2026 IN-PROGRESS SEASON — carried as it stands

**Confirmed against the harvest**: Layer 1 carries **@N26@** season rows for the in-progress 2026
season, of which **@N26F@** are full seasons (≥10 games), **@N26P@** are PARTIAL (1–9 games) and
**@N26Z@** are listed-not-yet-played placeholders at 0 games. All of them are included in columns 9
and 10 exactly as they stand.

**The games weighting handles the partials by construction**: `w = min(1, sqrt(games/10))`, so a
season of ≥10 games counts as a full season at its average and anything below is down-weighted on the
square root — a 4-game cameo carries `sqrt(0.4) = 0.632` of a season, not a full one. A 0-game
placeholder contributes exactly 0. **No 2026 row is extrapolated to a full season.**

## NUANCES HIT WHILE BUILDING THIS — reported, not resolved

1. **The 2011 ND rows stand as they are, pre-insertion-fix.** Column 5 shows the attribution this
   order's curve actually used, which for 2011 is the store's own picks with no correction applied.
2. **The 2013 and 2014 drafts are slid** (flag `SLID-2013-14`): every ND draftee in those years is
   attributed one pick better than his natural pick, `thomas-boyd` and `paddy-mccartin` are dropped
   from the curve, and the natural pick-2s — **`joshua-kelly` and `christian-petracca` — carry
   attributed pick 1**. Their natural picks (2) are in column 4 beside it.
3. **THREE store rows carry `_pvc_exclude=True` and this order's derivation did not honour it.**
   They are `dylan-shiel` (ND 2011 pick 4), **`jeremy-cameron` (ND 2011 pick 12)** and
   `adam-treloar` (ND 2011 pick 14). The engine's own curve excludes these three from teaching; this
   order's fit population was built from Layer 1, which carries raw facts and not engine teaching
   flags, so **all three sat in the ND curve fit at picks 4, 12 and 14**. Flagged per row as
   `STORE-PVC-EXCLUDE`. Two things follow and neither is adjudicated here:
   - it is a **real divergence** between this derivation's teaching population and the engine's, and
     it is not covered by any assert in the packet;
   - the sweep's flag F1 records that the ruling's Cameron *"sits as RD 2013 pick 6, unflagged"* —
     that row is **`charlie-cameron`**, a different player. **`jeremy-cameron` IS in the store as ND
     2011 pick 12 with the exclude flag set.** Whether F1 means one Cameron or the other is an owner
     question, not a build decision.
4. **Career games are summed from the season rows**, not read off the store's career counter. The
   two disagree on 457 active records by 1–2 games — the counter is a round-lagged snapshot of the
   in-progress season (recorded in Layer 1's own `measured_anomaly_323`). Column 8 matches what was
   actually valued.

---

## TOP 60 BY GRACE-A OBSERVED VALUE (the current basis)

@TOPTABLE@

---

## THE ROWS THE OWNER ASKED FOR BY NAME

@NAMEDTABLE@

---

## RANK MOVERS BETWEEN THE TWO OBSERVED COLUMNS

Ranked over the **@NRANK@ players whose baseline is at least @RFLOOR@ board points** — a material
career. Rank moves inside the block of players tied at 0.00 are an artefact of tie ordering and are
excluded for that reason. `move` is positive when a player rises under grace-A.

**The whole effect is the entry-age clause.** A 20+ entrant is multiplied by exactly 1.0000 — his
grace-A and baseline figures are the same number — and he is simply overtaken by teenagers lifted
~1.30. Nothing about any career changed.

### Biggest SLIDES (mature-age entrants, passed by teenagers)

@DOWNTABLE@

### Biggest RISES (≤19 entrants)

@UPTABLE@
"""

for _tok, _val in [
        ('@STORE_REL@', STORE_REL), ('@STORE_MD5@', STORE_MD5), ('@L1_MD5@', L1_MD5),
        ('@NROWS@', str(len(rows))),
        ('@NZERO@', str(sum(1 for r in rows if r['observed_discounted_grace_a'] <= 0))),
        ('@N26@', str(len(s26))), ('@N26F@', str(n26f)), ('@N26P@', str(n26p)),
        ('@N26Z@', str(n26z)),
        ('@NRANK@', str(len(_rk))), ('@RFLOOR@', '%.0f' % RANK_FLOOR),
        ('@TOPTABLE@', HDR + "\n" + "\n".join(line(r) for r in top)),
        ('@NAMEDTABLE@', HDR + "\n" + "\n".join(line(BYK[k]) for k in NAMED if k in BYK)),
        ('@DOWNTABLE@', RHDR + "\n" + "\n".join(rline(r) for r in DOWN)),
        ('@UPTABLE@', RHDR + "\n" + "\n".join(rline(r) for r in UP))]:
    MD = MD.replace(_tok, _val)
assert '@' not in MD.split('## TOP 60')[0], "an unsubstituted token remains in PLAYER_LEDGER.md"

open(MDP, 'w').write(MD)
csv_md5 = _md5(CSVP)
open(CSVP + '.md5', 'w').write('%s  PLAYER_LEDGER.csv\n' % csv_md5)
MD = MD.replace('`PLAYER_LEDGER.csv` (md5 below)', '`PLAYER_LEDGER.csv` md5 `%s`' % csv_md5)
open(MDP, 'w').write(MD)

print('ORDER 26B-L -- THE PLAYER LEDGER')
print('  rows          %d' % len(rows))
print('  csv           %s  md5 %s' % (os.path.relpath(CSVP, ROOT), csv_md5))
print('  md            %s' % os.path.relpath(MDP, ROOT))
print('  zero rows     %d' % sum(1 for r in rows if r['observed_discounted_grace_a'] <= 0))
print('  2026 rows     %d total (%d full, %d partial, %d placeholder)' % (len(s26), n26f, n26p, n26z))
print('  store-pvc-exclude rows: %s' % sorted(PVCX))
print()
print('  TOP 15 BY OBSERVED DISCOUNTED VALUE')
print('  %-26s %-8s %6s %5s %5s %10s %12s' %
      ('key', 'stream', 'entry', 'nat', 'attr', 'observed', 'undiscounted'))
for r in top[:15]:
    print('  %-26s %-8s %6s %5s %5s %10.1f %12.1f' %
          (r['key'], r['stream'], r['entry_year'], r['natural_pick'] or '-',
           r['attributed_pick'] or '-', r['observed_discounted_grace_a'],
           r['raw_undiscounted_value']))
print()
print('  NAMED ROWS')
for k in NAMED:
    if k not in BYK: continue
    r = BYK[k]
    print('  %-26s %-8s %6s nat %-4s attr %-4s %10.1f %12.1f  %s' %
          (r['key'], r['stream'], r['entry_year'], r['natural_pick'] or '-',
           r['attributed_pick'] or '-', r['observed_discounted_grace_a'],
           r['raw_undiscounted_value'], r['flags']))
assert_pins('exit')
print('\n  store and Layer 1 pins re-verified at exit -- nothing under engine/ was written.')
