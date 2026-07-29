#!/usr/bin/env python3
"""
ITEM 262 — positional data landing + vocabulary replacement.

Committed as evidence per acceptance criterion 2: "Transcription is by script, never by hand;
the script and its inputs are committed as evidence."

Two stages, run separately so the proof can separate them (owner ruling Q1, 2026-07-29):

  stage1  vocabulary replacement ONLY. No owner edits, no new per-season data.
          The board must come out byte-identical modulo the relabel: zero value movers,
          zero rank movers.

  stage2  the owner's edits (43 present_position, 12 future_position, 1 alternate_position,
          2 p_dual_stream) + the new per-season eligibility column.
          Movers are EXPECTED here and every one is reported and attributed.

Usage:
    python3 migrate_positions.py stage1 [--check]
    python3 migrate_positions.py stage2 [--check]

--check writes nothing and reports what would change.

VOCABULARY (owner ruling 2026-07-29, issue #262 §4). Replaced, not merged, so any un-migrated
site fails visibly instead of half-matching:

    K-FWD / KFWD / KEY_FWD  -> KPF
    K-DEF / KDEF / KEY_DEF  -> KPD
    G-DEF / GDEF / GEN_DEF  -> SD
    G-FWD / GFWD / GEN_FWD  -> SF
    MID                     -> MID
    RUC  / RUCK             -> RUCK
    DEF                     -> SD      (Q3: the engine's existing rl_model.py:67
                                        GRP {'DEF':'GEN_DEF'} alias, made explicit)

Three spellings were live before this migration and collapse to one here:
  * concatenated  (GDEF)   — the store's *_position fields
  * hyphenated    (G-DEF)  — the store's `eligibilities` string, and the owner's CSV inputs
  * underscored   (GEN_DEF)— the engine's group names (rl_model.py GRP values)
After migration all three are the same six codes, so rl_model.py's GRP and _ELIG_MAP become
identity maps over the new vocabulary. That is intended, not an accident.
"""
import json, os, re, sys, hashlib, collections

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.environ.get('ITEM262_SHEET',
    '/root/.claude/uploads/d4971030-9bc2-5f7f-83bc-62264dc5aff4/1317070f-rl_model_data_editable_1.xlsx')
STORE = os.path.join(REPO, 'engine/rl_after/rl_model_data.json')

# ---------------------------------------------------------------- vocabulary

NEW = {'KPF', 'KPD', 'SD', 'SF', 'MID', 'RUCK'}

# Longest-first so GEN_DEF is consumed before DEF, KFWD before FWD, RUCK before RUC.
TOKEN_MAP = [
    ('GEN_DEF', 'SD'),  ('GEN_FWD', 'SF'),  ('KEY_DEF', 'KPD'), ('KEY_FWD', 'KPF'),
    ('G-DEF',   'SD'),  ('G-FWD',   'SF'),  ('K-DEF',   'KPD'), ('K-FWD',   'KPF'),
    ('GDEF',    'SD'),  ('GFWD',    'SF'),  ('KDEF',    'KPD'), ('KFWD',    'KPF'),
    ('RUCK',    'RUCK'),('RUC',     'RUCK'),
    ('MID',     'MID'),
    ('DEF',     'SD'),  # Q3 alias — only ever reached after the compound forms above
]
_ALT = '|'.join(re.escape(k) for k, _ in TOKEN_MAP)
_TOKEN_RE = re.compile(r'(?<![A-Za-z0-9_])(' + _ALT + r')(?![A-Za-z0-9_])')
_LOOKUP = dict(TOKEN_MAP)

# For JSON files: match a token ONLY when it is a complete quoted string (a dict key or a
# bare-token value), optionally behind a '<prefix>|' composite as in rl_passmark's "3|GEN_DEF".
# This deliberately does NOT match tokens inside prose. ycred_table.json carries a 2KB `note`
# describing the L1c derivation that mentions GEN_DEF and RUC; rewriting it would falsify a
# historical record, and the structural cross-check below fails loudly if the two ever disagree.
_JSON_TOKEN_RE = re.compile(r'"((?:[^"\\]*\|)?)(' + _ALT + r')"')


def remap_token(tok):
    """Map one bare position token. Raises on anything unrecognised — never guesses."""
    if tok in NEW:
        return tok
    if tok not in _LOOKUP:
        raise KeyError('unmapped position token %r' % tok)
    return _LOOKUP[tok]


def remap_text(s):
    """Replace every position token in a string, leaving all other text byte-identical."""
    return _TOKEN_RE.sub(lambda m: _LOOKUP[m.group(1)], s)


def remap_csv_field(s):
    """A comma-separated eligibility string, e.g. 'MID,G-FWD' -> 'MID,SF'. Order preserved."""
    if s is None:
        return None
    parts = [p.strip() for p in str(s).split(',') if p.strip()]
    out, seen = [], set()
    for p in parts:
        v = remap_token(p)
        if v not in seen:          # K-X absorbs G-X can produce a duplicate; keep first
            seen.add(v); out.append(v)
    return ','.join(out)


# ------------------------------------------------------- file classification
#
# Measured, not assumed: the live-input set is every file the board build actually OPENS
# (audit-hook trace of `python3 rl_export.py`, 998 opens) that also carries an old token.
# Everything else carrying a token is historical and is enumerated as exempt below.

STORE_POSITION_FIELDS = ('drafted_position', 'present_position', 'future_position',
                         'alternate_position')

# JSON files whose position tokens are dispatch keys/values the engine reads.
JSON_DATA_FILES = [
    'engine/rl_after/params.json',
    'engine/rl_after/rl_passmark.json',
    'engine/rl_after/bust_prior_table.json',
    'engine/rl_after/lti_return_table.json',
    'engine/rl_after/ycred_table.json',
]

# Python/JS sources whose position tokens are literals the engine dispatches on.
#
# pgrid.py earns its place the expensive way. It was MISSING from the first live-input set
# because that set was measured with an audit hook listening only for `open` — which never
# fires for a module pulled in through the import machinery. pgrid is imported by rl_model,
# so it was invisible. It also carries the second half of a DUPLICATED grp3(): rl_model.py:954
# and pgrid.py:55 independently compute the same coarse GEN/KEY/RUC bucket, one READING the
# grid the other BUILDS. Migrating one side and not the other produced KeyError 'RUCK' at
# pgrid.Praw — hazard 2 (duplicated assertion) meeting hazard 7 (build-on-one-axis,
# read-on-the-other). The replaced-vocabulary design is what made it fail loudly instead of
# half-matching; a merged vocabulary would have silently bucketed every ruck as GEN.
CODE_FILES = [
    'engine/rl_after/rl_model.py',
    'engine/rl_after/pgrid.py',
    'engine/rl_after/_merged_recover.py',
    'engine/rl_after/rl_export.py',
    'engine/forward_valuation/build_cohort_book.py',
    'engine/forward_valuation/build_peak_model_v4.py',
    'engine/forward_valuation/conditional_prior.py',
    'engine/forward_valuation/dist_redesign.py',
    'engine/forward_valuation/par_build.py',
    'engine/forward_valuation/par_redesign.py',
    'engine/forward_valuation/tail_restore.py',
]

# The two translation tables in rl_model.py collapse to identity maps under the rename,
# because the three spellings they used to translate between are now one vocabulary. A blind
# token replace would leave DUPLICATE dict keys behind ('GDEF' and the 'DEF' alias both map to
# 'SD'; 'RUC' and 'RUCK' both to 'RUCK') — legal Python, but sloppy in source and it hides the
# fact that the DEF alias is now dead. These two lines are rewritten explicitly instead.
#
# Each pattern must match EXACTLY ONCE or the migration halts (anchoring sentinel, hazard 14).
SPECIAL_REWRITES = {
    'engine/rl_after/rl_model.py': [
        (r"^GRP=\{'MID':'MID','RUC':'RUC','GFWD':'GEN_FWD','KFWD':'KEY_FWD',"
         r"'GDEF':'GEN_DEF','DEF':'GEN_DEF','KDEF':'KEY_DEF'\}",
         "GRP={'MID':'MID','RUCK':'RUCK','SF':'SF','KPF':'KPF','SD':'SD','KPD':'KPD'}"
         "   # ITEM 262: identity since the store now speaks the engine's own vocabulary."
         " Kept as the dispatch boundary, NOT redundant. The pre-262 'DEF'->'GEN_DEF'"
         " back-catalogue alias is retired: all 136 rows were migrated to SD."),
        (r"^_ELIG_MAP=\{'MID':'MID','RUC':'RUC','RUCK':'RUC','G-FWD':'GEN_FWD',"
         r"'K-FWD':'KEY_FWD','G-DEF':'GEN_DEF','K-DEF':'KEY_DEF'\}",
         "_ELIG_MAP={'MID':'MID','RUCK':'RUCK','SF':'SF','KPF':'KPF','SD':'SD','KPD':'KPD'}"
         "   # ITEM 262: identity — `eligibilities` no longer uses a separate hyphenated"
         " spelling. Kept so _collapse_elig still validates its input."),
    ],
}

# EXEMPT AND ENUMERATED (acceptance criterion 2 requires the list, not a blanket).
#
#  (a) prose notes describing past events. Renaming them would falsify the historical
#      record — the note says what the vocabulary WAS at the time it was written.
EXEMPT_PROSE = {
    'data/expected_boot.json':        ['_engine_head_note', '_legc_note',
                                       '_legd_act2_note', '_r1067_note'],
    'data/model_config.json':         ['var_notes.RL_PVCADOPT'],
    'engine/rl_after/pvc_curve_L1b.json': ['note'],
    'engine/rl_after/ycred_table.json':   ['note'],   # 2KB L1c derivation narrative
}
#  (b) hash-named frozen snapshots. The hash in the FILENAME identifies the engine head or
#      config that produced the contents; rewriting the contents would make the name a lie.
#      This is hazard class 1 (right-name-wrong-file) and the rename must not touch them.
EXEMPT_FROZEN_GLOBS = [
    'data/gates_snapshots/gates_*.json',       # 23 files
    'data/s4_matrix_baked_*.json',
    'data/s4_matrix_control_*.json',
    'data/s4_matrix_gradedfix_*.json',
    'data/s4_matrix_v2*_*.json',
    'data/s4_matrix_v2_*.json',
    'data/s4_matrix_nogames.json',
    'engine/rl_after/ingestion/movers/movers_R*.json',
    'engine/rl_after/s4_matrix_M1v7*.json',
]
#  (c) archives and the register — exempt by directive.
EXEMPT_TREES = ('session_', 'backups/', 'evidence/', 'docs/archive/')
EXEMPT_FILES = ('docs/OPEN_ITEMS_REGISTER.md', 'LTI_REGISTER.md')
#  (d) regenerated, never hand-edited — the board is rebuilt by rl_export.py.
REGENERATED = ('data/rl_build/rl_app_data.json',)


# ------------------------------------------------------------------ stage 1

def json_remap_keys_and_values(obj, touched):
    """Walk a JSON structure remapping bare position tokens in dict KEYS and in string
    VALUES that are wholly position tokens (or '<n>|<TOKEN>' composites). Numbers, prose
    and everything else are left byte-identical."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            nk = k
            if isinstance(k, str):
                if '|' in k:
                    head, _, tail = k.rpartition('|')
                    if tail in _LOOKUP or tail in NEW:
                        nk = head + '|' + remap_token(tail);
                elif k in _LOOKUP or k in NEW:
                    nk = remap_token(k)
            if nk != k:
                touched.append(('key', k, nk))
            out[nk] = json_remap_keys_and_values(v, touched)
        return out
    if isinstance(obj, list):
        return [json_remap_keys_and_values(v, touched) for v in obj]
    if isinstance(obj, str) and (obj in _LOOKUP or obj in NEW):
        nv = remap_token(obj)
        if nv != obj:
            touched.append(('val', obj, nv))
        return nv
    return obj


def stage1_store(check):
    """Rename the store's own position vocabulary. Nothing else in the store moves."""
    with open(STORE) as f:
        players = json.load(f)
    counts = collections.Counter()
    for p in players:
        for fld in STORE_POSITION_FIELDS:
            if p.get(fld):
                old = p[fld]
                p[fld] = remap_token(old)
                if p[fld] != old:
                    counts[(fld, old, p[fld])] += 1
        if p.get('eligibilities'):
            old = p['eligibilities']
            p['eligibilities'] = remap_csv_field(old)
            if p['eligibilities'] != old:
                counts[('eligibilities', old, p['eligibilities'])] += 1
    if not check:
        # PROVEN byte-exact: json.dumps(obj) on the UNMODIFIED store reproduces the file
        # md5 e3aaba77 exactly, so this encoder is the one that wrote it. Anything other
        # than the position fields above is therefore byte-identical by construction.
        with open(STORE, 'w') as f:
            json.dump(players, f)
    return counts, len(players)


def stage1_files(check):
    """The small JSON tables carry position tokens ONLY as dict keys (verified by walking
    each file), so they are migrated by format-preserving TEXTUAL replacement rather than a
    JSON round-trip. params.json uses a hand-rolled indent that no json.dumps setting
    reproduces byte-exact; a structural rewrite would reformat all 1,689 bytes of it and
    bury the 15 real changes."""
    report = {}
    for rel in JSON_DATA_FILES + CODE_FILES:
        path = os.path.join(REPO, rel)
        with open(path) as f:
            src = f.read()
        if rel.endswith('.json'):
            changed = sum(1 for m in _JSON_TOKEN_RE.finditer(src)
                          if _LOOKUP[m.group(2)] != m.group(2))
            new = _JSON_TOKEN_RE.sub(
                lambda m: '"%s%s"' % (m.group(1), _LOOKUP[m.group(2)]), src)
            a, b = json.loads(src), json.loads(new)
            if json.dumps(json_remap_keys_and_values(a, []), sort_keys=True) != \
               json.dumps(b, sort_keys=True):
                raise SystemExit('HALT: textual migration of %s does not match the '
                                 'structural migration — stop and look' % rel)
            if not check and new != src:
                with open(path, 'w') as f:
                    f.write(new)
            report[rel] = changed
            continue
        changed = sum(1 for m in _TOKEN_RE.finditer(src) if _LOOKUP[m.group(1)] != m.group(1))
        # explicit rewrites first, so the blind pass never sees these lines
        for pat, repl in SPECIAL_REWRITES.get(rel, []):
            hits = len(re.findall(pat, src, flags=re.M))
            if hits != 1:
                raise SystemExit('HALT: %s special rewrite expected exactly 1 match, '
                                 'found %d for %r' % (rel, hits, pat[:60]))
            src = re.sub(pat, lambda _m: repl, src, flags=re.M)
        new = remap_text(src)
        if SPECIAL_REWRITES.get(rel):
            for _pat, repl in SPECIAL_REWRITES[rel]:
                if repl.split('   #')[0] not in new:
                    raise SystemExit('HALT: %s special rewrite did not survive the '
                                     'token pass' % rel)
        if not check and new != src:
            with open(path, 'w') as f:
                f.write(new)
        report[rel] = changed
    return report


# ------------------------------------------------------------------- driver

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('stage1', 'stage2'):
        print(__doc__); return 2
    stage, check = sys.argv[1], '--check' in sys.argv
    print('ITEM 262 %s%s' % (stage, '  [--check, writing nothing]' if check else ''))
    print('repo   : %s' % REPO)
    print('store  : %s  md5 %s' % (STORE, hashlib.md5(open(STORE,'rb').read()).hexdigest()))
    if stage == 'stage1':
        counts, n = stage1_store(check)
        print('\n-- store: %d player records --' % n)
        for (fld, old, new), c in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            print('   %-20s %-14s -> %-14s %5d' % (fld, old, new, c))
        print('   total field values remapped: %d' % sum(counts.values()))
        rep = stage1_files(check)
        print('\n-- engine data + code --')
        for rel, c in rep.items():
            print('   %-52s %5d tokens' % (rel, c))
        print('\nEXEMPT, enumerated:')
        print('   prose notes            : %d fields across %d files'
              % (sum(len(v) for v in EXEMPT_PROSE.values()), len(EXEMPT_PROSE)))
        print('   hash-named snapshots   : %d glob patterns (contents frozen; renaming '
              'would falsify the filename hash — hazard 1)' % len(EXEMPT_FROZEN_GLOBS))
        print('   archives + register    : %s %s' % (EXEMPT_TREES, EXEMPT_FILES))
        print('   regenerated by build   : %s' % (REGENERATED,))
        if not check:
            print('\nstore md5 after: %s'
                  % hashlib.md5(open(STORE,'rb').read()).hexdigest())
    else:
        print('stage2 is HELD pending the owner ruling on Ryan Lester / Jake Lever / '
              'Jack Lukosius (see OPEN_QUESTIONS_ROUND2.md R2-1).')
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
