"""ITEM 20 — THE STORE-IDENTITY JOB: the canonical store transform + importer (register items 20/20a/33).

Pure data transform on engine/rl_after/rl_model_data.json (the ONE source, SSI). Produces
(new_store, changelog, elig_table) and applies the ENTRY-BOUND ASSERTIONS (item 20(f), register
v43-era prevention commitment): any violation HALTS with the row named — the store never writes a
row that breaks the round ceiling, the DOB window, the club set, or the legal tag set.

Fence: the enumerated edits ONLY. Nothing here reads or writes any valuation lever, gate, or engine.

  (a) BRAMBLE: 2026 games 15->14, avg 62.4->62.3, career `games` 91->90.
  (b) afl_club: add to the 804 CSV-matched rows from CSV `legacy_afl_club` (current club). identity.
  (c) `_club` -> `_draft_club` rename (store-wide) + the TEN-ROW draft backfill (register v60):
      for the enumerated ten ONLY, _draft_club := afl_club (owner-declared one-club players).
      STRICT FENCE — no generalisation; every OTHER null-draft row is reported, never backfilled.
  (e) eligibilities: K/G companion-tag law (drop same-end G when same-end K present) + owner
      corrections gardiner->K-DEF, whitlock->K-DEF,K-FWD, cooke->K-DEF (register 20a spec of record).
  (f) entry-bound assertions (below) — HALT with the row named.

usage: python3 store_identity_transform.py <store_in> <csv> <store_out>   # writes new store + prints summary
"""
import json, csv, sys
from collections import Counter, OrderedDict

# ---- constants of record (register 20/20a/33) ----
ROUNDS_ELAPSED = 14                                   # 2026 season through round 14 (bramble: 872 pts / 14 g)
DOB_LO, DOB_HI = 1975, 2009                           # sane birth-year window (active store range is 1988-2007)
LEGAL_TAGS = {'G-DEF', 'G-FWD', 'K-DEF', 'K-FWD', 'MID', 'RUCK'}

# the ten club-less BOARD rows (register item 33) — draft-club backfill := afl_club (owner: one-club players).
# ENUMERATED; the equality is owner-declared FOR THESE TEN ONLY (no inference to any other null-draft row).
TEN_DRAFT_BACKFILL = ['dayne-zorko', 'scott-pendlebury', 'ben-murphy', 'kobe-mcdonald', 'patrick-carr',
                      'oscar-berry', 'indy-cotton', 'cillian-bourke', 'wil-parker', 'jamie-elliott']

# owner eligibility corrections (register 20a; applied AFTER normalization, as explicit overrides) —
# each restores agreement with the player's own engine class (present/drafted/future_position all K-*).
ELIG_CORRECTIONS = {'darcy-gardiner': 'K-DEF', 'matt-whitlock': 'K-DEF,K-FWD', 'lukas-cooke': 'K-DEF'}

BRAMBLE = 'lachlan-bramble'


def normalize_elig(tags_str):
    """K/G companion-tag law (register 20a): drop the SAME-END G when the SAME-END K is present.
    cross-end tags survive; key swingmen keep both K's; no row loses all tags. Order preserved."""
    tags = [t.strip() for t in (tags_str or '').split(',') if t.strip()]
    keep = set(tags)
    if 'K-DEF' in keep:
        keep.discard('G-DEF')
    if 'K-FWD' in keep:
        keep.discard('G-FWD')
    return ','.join(t for t in tags if t in keep)


def load_csv(path):
    rows = {}
    for r in csv.DictReader(open(path)):
        rows[r['legacy_key']] = r
    return rows


def _rename_and_insert(row, csv_row):
    """Rebuild a CSV-matched row's ordered dict: rename _club -> _draft_club IN PLACE and insert afl_club
    right after it. Non-club fields keep byte-identical order/values (only eligibilities is set separately)."""
    out = OrderedDict()
    for k, v in row.items():
        if k == '_club':
            out['_draft_club'] = v
            out['afl_club'] = csv_row['legacy_afl_club']
        else:
            out[k] = v
    if '_draft_club' not in out:                       # row had no _club key at all -> add both explicitly
        out['_draft_club'] = None
        out['afl_club'] = csv_row['legacy_afl_club']
    return out


def migrate(store, csv_rows):
    changelog = []            # (key, field, old, new, cause)
    elig_table = []           # (key, before, after, cause)  — the full before/after tag table
    by_key = {}
    for i, r in enumerate(store):
        by_key.setdefault(r['key'], []).append((i, r))

    def setf(r, field, val, cause):
        old = r.get(field, '<absent>')
        if old != val:
            changelog.append((r['key'], field, old, val, cause))
            r[field] = val

    new_store = list(store)   # will replace matched rows in place by index

    # ---- (b)+(c) rename + afl_club on the 804 CSV-matched rows ----
    for key, c in csv_rows.items():
        rs = by_key.get(key)
        if not rs:
            continue
        idx, r = rs[0]
        nr = _rename_and_insert(r, c)
        changelog.append((key, '_club->_draft_club', r.get('_club'), nr['_draft_club'], 'rename'))
        changelog.append((key, 'afl_club', '<absent>', nr['afl_club'], 'afl-club-import'))
        new_store[idx] = nr
        by_key[key] = [(idx, nr)]

    # ---- (c) rename _club -> _draft_club on EVERY OTHER row store-wide (consumer CAT_BY_CLUB reads it) ----
    renamed_hist = 0
    for i, r in enumerate(new_store):
        if r['key'] in csv_rows:
            continue
        if '_club' in r:
            nr = OrderedDict((('_draft_club', v) if k == '_club' else (k, v)) for k, v in r.items())
            new_store[i] = nr
            renamed_hist += 1
            by_key[r['key']] = [(i, nr)]

    # ---- (e) eligibilities: normalize (K/G law) then owner corrections, on the 804 ----
    for key, c in csv_rows.items():
        idx, r = by_key[key][0]
        before = r.get('eligibilities')
        after = normalize_elig(before)
        cause = 'kg-normalize'
        if key in ELIG_CORRECTIONS:
            after = ELIG_CORRECTIONS[key]
            cause = 'owner-correction'
        if after != before:
            elig_table.append((key, before, after, cause))
            setf(r, 'eligibilities', after, cause)

    # ---- (c) TEN-ROW draft backfill := afl_club (enumerated; owner one-club players) ----
    for key in TEN_DRAFT_BACKFILL:
        idx, r = by_key[key][0]
        assert r.get('_draft_club') in (None, '', '<absent>'), \
            "BACKFILL GUARD: %s expected null draft club, got %r" % (key, r.get('_draft_club'))
        setf(r, '_draft_club', r['afl_club'], 'ten-draft-backfill')

    # ---- (a) BRAMBLE value move ----
    idx, r = by_key[BRAMBLE][0]
    for s in r['scoring']:
        if s['year'] == 2026:
            setf_scoring(changelog, r, s, 'games', 15, 14)
            setf_scoring(changelog, r, s, 'avg', 62.4, 62.3)
    new_games = sum(s['games'] for s in r['scoring'])
    setf(r, 'games', new_games, 'bramble-career-games')

    # ---- STRICT-FENCE report: every OTHER null-draft row (never backfilled) ----
    null_draft_other = []
    for r in new_store:
        if r.get('_draft_club') in (None, '', '<absent>') and r['key'] not in TEN_DRAFT_BACKFILL:
            null_draft_other.append((r['key'], bool(r.get('_retired')), r['key'] in csv_rows))

    return new_store, changelog, elig_table, renamed_hist, null_draft_other


def setf_scoring(changelog, r, s, field, old_expect, new_val):
    old = s.get(field)
    assert old == old_expect, "BRAMBLE GUARD: expected %s=%r, store has %r" % (field, old_expect, old)
    changelog.append((r['key'], 'scoring2026.' + field, old, new_val, 'bramble'))
    s[field] = new_val


# ==== (f) ENTRY-BOUND ASSERTIONS — HALT with the row named ====
def assert_entry_bounds(store, csv_rows):
    halts = []
    active = {k for k in csv_rows}
    for r in store:
        k = r['key']
        # games <= rounds elapsed (2026 scoring rows)
        for s in (r.get('scoring') or []):
            if s.get('year') == 2026 and s.get('games', 0) > ROUNDS_ELAPSED:
                halts.append("GAMES>ROUNDS: %s 2026 games=%s > %d" % (k, s['games'], ROUNDS_ELAPSED))
        if k in active:
            # DOB within range
            by = r.get('_by')
            if by is None or not (DOB_LO <= by <= DOB_HI):
                halts.append("DOB-RANGE: %s _by=%r outside [%d,%d]" % (k, by, DOB_LO, DOB_HI))
            # club within the 18
            ac = r.get('afl_club')
            if ac not in CLUBS_18:
                halts.append("CLUB-NOT-IN-18: %s afl_club=%r" % (k, ac))
            # eligibility tags from the legal set
            for t in (r.get('eligibilities') or '').split(','):
                t = t.strip()
                if t and t not in LEGAL_TAGS:
                    halts.append("ILLEGAL-TAG: %s tag=%r not in %s" % (k, t, sorted(LEGAL_TAGS)))
    return halts


if __name__ == '__main__':
    store = json.load(open(sys.argv[1]))
    csv_rows = load_csv(sys.argv[2])
    CLUBS_18 = sorted({c['legacy_afl_club'] for c in csv_rows.values()})
    assert len(CLUBS_18) == 18, "expected 18 clubs, got %d: %s" % (len(CLUBS_18), CLUBS_18)

    new_store, changelog, elig_table, renamed_hist, null_draft_other = migrate(store, csv_rows)

    halts = assert_entry_bounds(new_store, csv_rows)
    if halts:
        print("ENTRY-BOUND ASSERTIONS HALTED THE IMPORT (%d):" % len(halts))
        for h in halts:
            print("  HALT:", h)
        sys.exit(1)
    print("(f) entry-bound assertions PASS: games<=%d, DOB in [%d,%d], afl_club in the 18, tags legal."
          % (ROUNDS_ELAPSED, DOB_LO, DOB_HI))

    json.dump(new_store, open(sys.argv[3], 'w'))       # single-line default (untouched rows byte-exact)

    print("\n== CHANGELOG ==")
    print("changelog rows:", len(changelog))
    print("by cause:", dict(Counter(c[4] for c in changelog)))
    print("historical rows _club->_draft_club renamed:", renamed_hist)
    print("\n== ELIGIBILITY before/after (n=%d) ==" % len(elig_table))
    print("by cause:", dict(Counter(e[3] for e in elig_table)))
    for k, b, a, c in elig_table:
        if c == 'owner-correction':
            print("  OWNER-CORRECTION %-16s %-24r -> %r" % (k, b, a))
    print("\n== STRICT-FENCE null-draft report (NOT backfilled) ==")
    print("rows with null _draft_club beyond the ten:", len(null_draft_other))
    print("  of which retired:", sum(1 for _, ret, _ in null_draft_other if ret),
          "| non-retired:", sum(1 for _, ret, _ in null_draft_other if not ret),
          "| in CSV(active):", sum(1 for _, _, inc in null_draft_other if inc))
    nonret = [k for k, ret, _ in null_draft_other if not ret]
    print("  non-retired names (owner rules if any):", nonret if nonret else "NONE")
    # named lines for the return
    bk = {r['key']: r for r in new_store}
    for k in ['dan-houston', 'ben-keays', BRAMBLE]:
        r = bk[k]
        print("  %-16s afl_club=%-12r _draft_club=%-14r affl_team=%-20r elig=%r games=%s"
              % (k, r.get('afl_club'), r.get('_draft_club'), r.get('affl_team'),
                 r.get('eligibilities'), r.get('games')))
