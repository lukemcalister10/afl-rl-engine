#!/usr/bin/env python3
"""tools/ingest — THE WEEKLY SCORE INGEST. One command, one file, no paperwork.

    tools/ingest scores/FW3.csv            # resolve, apply, build, check, commit, push, rebuild the app
    tools/ingest scores/FW3.csv --check    # resolve and show the edit only; writes nothing
    tools/ingest scores/FW3.csv --as "Bailey Williams=bailey-williams-wb"   # a one-off name ruling

WHY THIS EXISTS (owner, 2026-09-24, after a review of why FW2 took 27 hours and 13 attempts). A week
of scores had been going through the transaction built for MODEL changes, whose whole job is to prove
that nothing moved except what was predicted. A week of scores is the opposite — the store, the board
and everything built from them are supposed to move — so every safety check in that machinery fired
as a matter of course and each had to be satisfied by hand: a prereg, an owner-word field, a board
predicted in advance, a mover list that could only be measured by building the board first, and a
25-30 minute self-test on the first flight of every week. The owner ruled that weekly data takes its
own path without any of that.

WHAT IT STILL DOES, BECAUSE IT CHANGES WHAT THE OWNER RECEIVES:
  * every name is resolved to exactly one active player, or the run stops and lists the problems —
    including names that COLLIDE once a middle initial is dropped ("Bailey Williams" and "Bailey J.
    Williams" are two active players; FootyWire can print either as the first);
  * the averages are the ingestor's own arithmetic at the ingestor's own precision, called not copied;
  * the board is built by the same writers the lander uses — this tool orchestrates them, it does not
    own a second copy of any of them;
  * automatic limits on the result (tools/ingest_bounds.py, run as a gate): a week of football moves
    the players who played; if the players who did NOT play move by more than a whisker, something
    other than football moved the board and the week is refused;
  * every existing gate still runs, and the transaction still puts every file back exactly as it was
    if anything fails.

WHAT IT DOES NOT DO: advance the calendar. A finals week is football that does not advance the ladder
(the calendar holds at round 24, owner law 2026-09-02). Home-and-away rounds DO advance it and are not
handled here yet; the next one is 2027 round 1, which first needs the season rollover.

THE UNDO IS GIT. The scores and the resolved list are committed first (so a failed run leaves nothing
half-done and a re-run is safe), then the landing commits its own result. `git revert` undoes a week.
"""
import argparse
import collections
import csv
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))

STORE_REL = 'engine/rl_after/rl_model_data.json'
BOOT_REL = 'data/expected_boot.json'
MOVERS_REL = 'ui/data/movers.js'
OVERRIDES_REL = 'engine/rl_after/ingestion/catchup_identity_overrides.json'
PINNED_NUMPY = '2.4.4'
SEASON = 2026
RECORD_FILES = ('FLIGHT.log', 'REPORT.json', 'PREFLIGHT.json')   # what the lander files after its commit

#: THE OWNER'S NAMES FOR THE FINALS WEEKS -> the feed round each one is. The display names and column
#: prefixes come from round_movers (the one table the UI's copies are tested against).
WEEK_ALIASES = {'FW1': 25, 'FW2': 26, 'FW3': 27, 'FW4': 28, 'FW5': 29, 'GF': 29}


def say(msg=''):
    print(msg, flush=True)


def die(msg):
    say('')
    say('STOPPED: ' + msg)
    sys.exit(1)


def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def git(*argv, check=True):
    p = subprocess.run(['git'] + list(argv), cwd=REPO, capture_output=True, text=True)
    if check and p.returncode != 0:
        die('git %s failed:\n%s' % (' '.join(argv), (p.stdout + p.stderr)[-1500:]))
    return p.stdout


def load_movers():
    src = io.open(os.path.join(REPO, MOVERS_REL), encoding='utf-8').read()
    i = src.index('{', src.index('__MATCHDAY_MOVERS__'))
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return json.loads(src[i:j + 1])
    raise SystemExit('unterminated movers bundle')


# ------------------------------------------------------------------------------ the environment
def check_environment(need_build, src=None):
    """Everything that used to fail 45 seconds, or 70 minutes, into a flight — checked in seconds."""
    import importlib
    try:
        np = importlib.import_module('numpy')
        importlib.import_module('scipy')
        importlib.import_module('sklearn')
    except ImportError as e:
        die('this Python (%s) cannot import the pinned stack (%s). Run:\n'
            '  export PATH="$HOME/rl_venv312/bin:$PATH"   (or use the tools/ingest wrapper)'
            % (sys.executable, e))
    if np.__version__ != PINNED_NUMPY:
        die('numpy %s is not the pinned %s — the board does not reproduce off the pin '
            '(SHAKEDOWN.md: Maric 1426 vs 1409).' % (np.__version__, PINNED_NUMPY))
    if not need_build:
        return
    if os.path.exists(os.path.join(REPO, '.git', 'shallow')):
        say('  the clone is shallow; fetching full history (two gates need it) ...')
        p = subprocess.run(['git', 'fetch', '--unshallow', 'origin'], cwd=REPO,
                           capture_output=True, text=True)
        if p.returncode != 0:
            die('could not unshallow the clone:\n%s' % (p.stdout + p.stderr)[-800:])
    node_mod = os.path.join(os.path.dirname(REPO), 'node_modules', 'playwright-core')
    if not os.path.exists(node_mod):
        glob_pw = '/opt/node22/lib/node_modules/playwright/node_modules/playwright-core'
        if os.path.isdir(glob_pw):
            os.makedirs(os.path.dirname(node_mod), exist_ok=True)
            os.symlink(glob_pw, node_mod)
            say('  linked playwright-core for the browser gates')
    # The score file itself, dropped into scores/ and not yet committed, is the input — not dirt.
    mine = os.path.relpath(src, REPO) if src and src.startswith(REPO + os.sep) else None
    dirty = [l for l in git('status', '--porcelain', '--untracked-files=all').splitlines()
             if l.strip() and l[3:] != mine]
    if dirty:
        die('the tree has uncommitted changes. Commit or discard them first:\n  '
            + '\n  '.join(dirty[:12]))


def reseed_workspace():
    """The engine's harnesses run from a COPY of the repo in /home/claude. After every landing that
    copy is stale and the next engine run refuses (STALE BOOT). Re-seed it so it never is."""
    p = subprocess.run(['bash', os.path.join(REPO, 'bootstrap.sh')], cwd=REPO,
                       capture_output=True, text=True)
    if p.returncode != 0:
        die('bootstrap.sh failed:\n%s' % (p.stdout + p.stderr)[-1500:])


# ------------------------------------------------------------------------------ the week
def resolve_week(path, week_arg):
    import round_movers as RM
    label = (week_arg or os.path.splitext(os.path.basename(path))[0]).upper()
    if re.fullmatch(r'R\d+', label):
        die('%s is a home-and-away round. Rounds ADVANCE the calendar, which this path does not do '
            'yet; the next one is 2027 round 1, after the season rollover.' % label)
    if label not in WEEK_ALIASES:
        die('cannot tell which week %r is. Name the file FW3.csv / FW4.csv / GF.csv, or pass '
            '--week FW3.' % os.path.basename(path))
    feed = WEEK_ALIASES[label]
    name = RM.FINALS_WEEK_NAMES.get(feed)
    prefix = [k for k, v in RM.FINALS_COLUMN_PREFIXES.items() if v == name]
    if not name or len(prefix) != 1:
        die('round_movers has no finals name/prefix for feed round %d' % feed)
    reports = load_movers().get('reports') or {}
    if str(feed) in reports:
        die('%s (feed round %d) is already on the board — its weekly report exists. Nothing to do.'
            % (name.title(), feed))
    missing = [r for r in range(25, feed) if str(r) not in reports]
    if missing:
        die('%s cannot land before feed round(s) %s — the finals weeks go in order.'
            % (name.title(), missing))
    return {'label': 'GF' if feed == 29 else label, 'feed': feed, 'name': name,
            'prefix': prefix[0]}


# ------------------------------------------------------------------------------ the names
def _norm(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())


def _first_last(s):
    """'Bailey J. Williams' -> 'baileywilliams'. Drops middle names and initials."""
    toks = [t for t in re.split(r'\s+', str(s).strip()) if t]
    return _norm(toks[0] + toks[-1]) if len(toks) >= 2 else _norm(s)


def resolve_names(rows, store, rulings):
    """name -> store key, or a list of problems. Order: a one-off --as ruling; the standing alias file's
    map_all rules; an exact display-name match to exactly ONE active player whose first+last name is
    not shared with another active player. Anything else is a problem, listed, never guessed."""
    active = [p for p in store if p.get('key') and not p.get('_retired')]
    by_name = collections.defaultdict(list)
    by_fl = collections.defaultdict(list)
    for p in active:
        by_name[_norm(p.get('player'))].append(p)
        by_fl[_first_last(p.get('player'))].append(p)
    keys = {p['key'] for p in active}
    ov = json.load(io.open(os.path.join(REPO, OVERRIDES_REL), encoding='utf-8'))
    standing, needs_ruling = {}, {}
    for o in ov.get('overrides') or []:
        if o.get('rule') == 'map_all' and o.get('stable_key'):
            standing[o['name'].strip().lower()] = o['stable_key']
        else:
            needs_ruling[o['name'].strip().lower()] = o.get('rule')

    out, problems, via = {}, [], collections.Counter()
    for name, score in rows:
        low = name.strip().lower()
        if low in rulings:
            key, how = rulings[low], 'your --as ruling'
        elif low in standing:
            key, how = standing[low], 'the standing alias file'
        else:
            exact = by_name.get(_norm(name), [])
            clash = by_fl.get(_first_last(name), [])
            if low in needs_ruling or len(clash) > 1:
                who = ', '.join('%s (%s, %s)' % (p['key'], p.get('player'), p.get('afl_club'))
                                for p in (clash or exact))
                problems.append('%-22s more than one active player could be meant: %s. Say which with '
                                '--as "%s=<key>"' % (name, who, name))
                continue
            if len(exact) != 1:
                problems.append('%-22s matches no active player. If it is a short form, say which '
                                'with --as "%s=<key>" (and add it to %s so it sticks)'
                                % (name, name, OVERRIDES_REL))
                continue
            key, how = exact[0]['key'], 'exact name'
        if key not in keys:
            problems.append('%-22s maps to %r, which is not an active player' % (name, key))
            continue
        if key in out:
            problems.append('%-22s maps to %s, which another listed name already took' % (name, key))
            continue
        out[key] = (name, score)
        via[how] += 1
    return out, problems, via


# ------------------------------------------------------------------------------ the edit
def compute_edits(resolved, store):
    import score_ingestor as SI
    decimals = SI.ROUND_DECIMALS
    mean = types.SimpleNamespace(round_decimals=decimals)
    by_key = {p['key']: p for p in store if p.get('key')}
    edits, problems = [], []
    for key in sorted(resolved):
        name, score = resolved[key]
        rows = [s for s in (by_key[key].get('scoring') or []) if s.get('year') == SEASON]
        if len(rows) != 1:
            problems.append('%s has %d %d season rows; a week adds to exactly one'
                            % (key, len(rows), SEASON))
            continue
        g0, a0 = int(rows[0]['games']), float(rows[0]['avg'])
        a1 = SI.ScoreIngestor._mean(mean, a0 * g0 + float(score), g0 + 1)
        edits.append({'key': key, 'field': 'scoring[%d].games' % SEASON, 'old': g0, 'new': g0 + 1})
        if rows[0]['avg'] != a1:             # a no-op field is dropped, not declared (validator rule)
            edits.append({'key': key, 'field': 'scoring[%d].avg' % SEASON,
                          'old': rows[0]['avg'], 'new': a1})
    # CAREER GAMES IS THE SUM OF THE SEASON ROWS (owner ruling 2026-09-24). Every weekly write since
    # R19 updated the season rows and not the career field, so 509 players fell 1-7 games short and
    # the young-player floor on the +1/+2 year views read them as less proven than they are. Every
    # week re-asserts it for EVERY row, so it cannot drift again. Short is the known cause (a write
    # that missed the career field) and is corrected; career ABOVE the season sum has no known
    # cause, so it halts the week and is named.
    for p in store:
        key = p.get('key')
        if not key or not isinstance(p.get('games'), int):
            continue
        seasons = sum(int(s.get('games') or 0) for s in p.get('scoring') or [])
        if key in resolved:
            seasons += 1                     # this week's game, added to the season row above
        if p['games'] > seasons:
            problems.append('%s: career games %d is ABOVE the sum of its season rows (%d) — no known '
                            'cause; the week stops until it is explained' % (key, p['games'], seasons))
        elif p['games'] != seasons:
            edits.append({'key': key, 'field': 'games', 'old': p['games'], 'new': seasons})
    return edits, problems


# ------------------------------------------------------------------------------ the act
def build_spec(week, csv_rel, csv_sha, resolved, edits, resolved_rel, ev_rel):
    from tools.landing import steps as ST
    boot = json.load(io.open(os.path.join(REPO, BOOT_REL), encoding='utf-8'))
    today = datetime.date.today()
    col = '%s%s-%d-%d' % (week['prefix'], week['name'].lower().replace(' ', '-'), today.day,
                          today.month)
    n = len(resolved)
    what = '%s — %d players gain one game and a re-averaged %d season row' % (
        week['name'].title(), n, SEASON)
    gates = [dict(g) for g in ST.DEFAULT_GATES] + [
        {'name': 'ingest_bounds', 'argv': ['python3', 'tools/ingest_bounds.py', resolved_rel]}]
    return {
        'schema_version': 1,
        'act_kind': 'store-edit',
        'act': what.upper(),
        'date': today.isoformat(),
        'owner_word': ('Weekly scores supplied by the owner: %s (sha256 %s), ingested with '
                       'tools/ingest under the owner ruling of 2026-09-24 that weekly data takes its '
                       'own path.' % (csv_rel, csv_sha[:16])),
        'authority': 'owner ruling 2026-09-24 (the weekly ingest path)',
        'prereg': {'path': ev_rel + '/NOTE.md', 'board_before': boot['board'],
                   'board_after': None, 'reference_board': None, 'kill_switch': None},
        'edit': {'store': edits, 'expected_movers': None,
                 '_doc_expected_movers': ('not declared: a week of scores is checked by '
                                          'tools/ingest_bounds.py (a gate) instead of a mover list '
                                          'that could only be measured by building twice.')},
        'identities': {'moves': ['store', 'board'],
                       'unmoved': ['engine_head', 'rl_model', 'fv', 'config', 'register',
                                   'as_of_round']},
        'column': {'id': col, 'label': '%d/%d %s — %d players, one game each on the %d season row'
                                        % (today.day, today.month, week['name'], n, SEASON),
                   'after_round': int(boot['as_of_round'])},
        'lineage': {'doc': ev_rel + '/NOTE.md',
                    'owner_ruling_id': ['WEEKLY_INGEST_2026-09-24',
                                        'FINALS_LANE_2026-08-30_averages_and_game_counts_not_a_round',
                                        'CALENDAR_CEILING_2026-09-02_never_above_one'],
                    'owner_ruling': ('Finals scores are applied to the season row and the calendar '
                                     'holds at round 24; weekly data goes through tools/ingest.'),
                    'authority': 'owner ruling 2026-09-24', 'invariants': {}},
        'day0_rebase': {'state': 'off'},
        'evidence_dir': ev_rel,
        'gates': gates,
        'commit_message': '%s applied (tools/ingest) — %d players, %d store edits'
                          % (week['name'].title(), n, len(edits)),
    }


def WEEK_CARRIERS(CA):
    """The two files a week's movers point writes that `land edit` never declared. FW2 got past this
    only because its bank (values_r26.json) had been committed by hand during a failed flight; FW3's
    third run passed all 21 gates and was refused at the commit step for these two. A file the landing
    writes must be one it commits (and, on abort, puts back)."""
    retro = 'docs/evidence/walkforward_retro_2026-08-29/'
    return (CA.G(retro + 'values_r*.json', 'finals_report / bank_from_landed_board (writer 4c)',
                 "the week's point on the movers list, banked from the landed board"),
            CA.F(retro + 'CONTROL_FAIL.json', 'emit_retro_series control (writer 4b)',
                 'the retro control report: which rows the newest bank and the live board disagree on'))


def run_landing(spec_path, ev_dir):
    """The lander's own step functions, driven without the self-test and the claims echo. Every file
    is put back exactly as it was if any step fails."""
    from tools.landing import cli as CLI, spec as SP, steps as ST, txn as TX, carriers as CA
    doc = SP.load(spec_path)
    doc['_spec_rel'] = os.path.relpath(spec_path, REPO)
    a = types.SimpleNamespace(root=REPO, spec=spec_path, selftest=False, dry_run=False,
                              report=os.path.join(ev_dir, 'REPORT.json'),
                              log=os.path.join(ev_dir, 'FLIGHT.log'), keep_work=False)
    pf = CLI._run_cheap_preflight(a, doc)
    ctx = TX.Ctx(REPO, doc, TX.Options(), builder=TX.RealBuilder(),
                 carriers=CA.EDIT_CARRIERS + WEEK_CARRIERS(CA))
    seq = tuple(s for s in ST.EDIT_SEQUENCE if s[0] != 'claims')
    res = TX.run(ctx, seq)
    CLI._file_cheap_preflight(pf, ctx.evidence_dir)
    CLI._write_reports(a, ctx, res)
    return res


def put_tree_back(keep):
    """After a failed landing, return the tree to the inputs commit. The lander restores its carriers
    byte-exact, but some writers leave files beside them (a control report, a week's value bank, an
    abort note) — FW3's first run left four, and a dirty tree makes the re-run refuse. The run began
    on a clean tree, so every change here is the landing's own: copy it to `keep`, then undo it."""
    n = 0
    for line in git('status', '--porcelain', '--untracked-files=all').splitlines():
        if not line.strip():
            continue
        rel = line[3:]
        dst = os.path.join(keep, 'tree', rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(os.path.join(REPO, rel)):
            shutil.copyfile(os.path.join(REPO, rel), dst)
        if line.startswith('??'):
            os.remove(os.path.join(REPO, rel))
        else:
            git('checkout', 'HEAD', '--', rel)
        n += 1
    return n


# ------------------------------------------------------------------------------ the summary
def summarise(week):
    mv = load_movers()
    rep = (mv.get('reports') or {}).get(str(week['feed'])) or {}
    ps = rep.get('players') or []
    played = [p for p in ps if p.get('played')]
    moved = sorted((p for p in ps if p.get('value_change')), key=lambda p: -p['value_change'])
    say('')
    say('%s — %d played, %d did not' % (week['name'].title(), len(played), len(ps) - len(played)))
    say('  biggest rises : ' + ', '.join('%s %+d (%s)' % (p['name'], p['value_change'], p['score'])
                                         for p in moved[:6] if p['value_change'] > 0))
    say('  biggest falls : ' + ', '.join('%s %+d (%s)' % (p['name'], p['value_change'], p['score'])
                                         for p in moved[::-1][:6] if p['value_change'] < 0))


def rebuild_app():
    p = subprocess.run([sys.executable, 'ui/tools/bundle_standalone.py'], cwd=REPO,
                       capture_output=True, text=True)
    if p.returncode != 0:
        say('  valueboard.html NOT rebuilt:\n' + (p.stdout + p.stderr)[-800:])
        return False
    s = subprocess.run(['node', 'ui/tools/standalone_smoke.mjs', 'valueboard.html'], cwd=REPO,
                       capture_output=True, text=True)
    last = (s.stdout.strip().splitlines() or [''])[-1]
    say('  valueboard.html rebuilt — %s' % last)
    return s.returncode == 0


# ------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('scores', help='the week\'s name,score file, e.g. scores/FW3.csv')
    ap.add_argument('--week', help='FW3 / FW4 / GF (default: read from the file name)')
    ap.add_argument('--as', dest='rulings', action='append', default=[],
                    help='a one-off name ruling, "Listed Name=store-key" (repeatable)')
    ap.add_argument('--check', action='store_true',
                    help='resolve and show the edit, write nothing')
    ap.add_argument('--no-push', action='store_true', help='commit but do not push')
    a = ap.parse_args()
    os.chdir(REPO)

    src = os.path.abspath(a.scores)
    if not os.path.isfile(src):
        die('no such file: %s' % a.scores)
    say('WEEKLY INGEST — %s' % (os.path.relpath(src, REPO) if src.startswith(REPO + os.sep) else src))
    check_environment(need_build=not a.check, src=src)
    week = resolve_week(src, a.week)
    say('  week          %s (feed round %d; the calendar holds at 24)' % (week['name'].title(),
                                                                          week['feed']))
    import footywire_parser as FP
    parsed = FP.parse_round_file(src)
    store = json.load(io.open(os.path.join(REPO, STORE_REL), encoding='utf-8'))
    rulings = {}
    for r in a.rulings:
        if '=' not in r:
            die('--as takes "Listed Name=store-key", got %r' % r)
        n, k = r.split('=', 1)
        rulings[n.strip().lower()] = k.strip()
    resolved, problems, via = resolve_names(parsed['rows'], store, rulings)
    say('  names         %d listed, %d resolved (%s)'
        % (parsed['listed'], len(resolved), ', '.join('%d by %s' % (v, k) for k, v in via.items())))
    if problems:
        die('%d name(s) need a decision:\n  %s' % (len(problems), '\n  '.join(problems)))
    edits, eproblems = compute_edits(resolved, store)
    if eproblems:
        die('\n  '.join(eproblems))
    clubs = collections.Counter(p.get('afl_club') for p in store if p.get('key') in resolved)
    say('  clubs         ' + ', '.join('%s %d' % kv for kv in clubs.most_common() if kv[1] > 3))
    odd = ['%s (%s)' % (k, c) for k, c in clubs.items() if c <= 3]
    if odd:
        say('  also          %s — store club differs from the side they played for; harmless'
            % ', '.join(odd))
    n_career = sum(1 for e in edits if e['field'] == 'games')
    say('  edits         %d on %d players (games +1, average re-worked at 2 decimals)'
        % (len(edits) - n_career, len(resolved)))
    say('  career games  %d row(s) set to the sum of their seasons' % n_career)
    if a.check:
        say('\n--check: nothing written.')
        return 0

    # ---- inputs, committed first so a failed run leaves nothing half-done and a re-run is safe
    label = week['label']
    csv_rel = 'scores/%s.csv' % label
    if os.path.abspath(csv_rel) != src:
        shutil.copyfile(src, os.path.join(REPO, csv_rel))
    resolved_rel = 'scores/resolved/%d_%s.json' % (SEASON, label)
    os.makedirs(os.path.join(REPO, 'scores', 'resolved'), exist_ok=True)
    json.dump({'season': SEASON, 'week': week['name'], 'feed_round': week['feed'],
               'source': csv_rel, 'source_sha256': sha256(os.path.join(REPO, csv_rel)),
               'rulings': rulings,
               'players': [{'key': k, 'listed_as': resolved[k][0], 'score': resolved[k][1]}
                           for k in sorted(resolved)]},
              io.open(os.path.join(REPO, resolved_rel), 'w', encoding='utf-8'), indent=1)
    ev_rel = 'docs/evidence/ingest/%d_%s' % (SEASON, label)
    ev_dir = os.path.join(REPO, ev_rel)
    os.makedirs(ev_dir, exist_ok=True)
    io.open(os.path.join(ev_dir, 'NOTE.md'), 'w', encoding='utf-8').write(
        '# %s — weekly ingest\n\nScores: `%s`. Resolved list: `%s`. Applied by `tools/ingest` under '
        'the owner ruling of 2026-09-24. Checked by `tools/ingest_bounds.py` and the standing gates; '
        'no predicted board and no predicted movers — a week of football is supposed to move them.\n'
        % (week['name'].title(), csv_rel, resolved_rel))
    spec = build_spec(week, csv_rel, sha256(os.path.join(REPO, csv_rel)), resolved, edits,
                      resolved_rel, ev_rel)
    from tools.landing import spec as SP
    bad = SP.validate(spec)
    if bad:
        die('the generated spec does not validate:\n  ' + '\n  '.join(bad))
    spec_path = os.path.join(ev_dir, 'ACT_SPEC.json')
    json.dump(spec, io.open(spec_path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    git('add', csv_rel, resolved_rel, ev_rel)
    if git('diff', '--cached', '--name-only').strip():
        git('commit', '-q', '-m', '%s scores: the inputs (tools/ingest)' % week['name'].title())
        say('  inputs        committed')
    else:
        say('  inputs        already committed by an earlier run (unchanged)')

    say('\nBUILDING — the store edit, one board build, the UI writers, the gates ...')
    reseed_workspace()
    res = run_landing(spec_path, ev_dir)
    # The lander files its record (log, report, preflight) AFTER its own commit. Left untracked, it
    # would make the NEXT week refuse a dirty tree — so it is committed on success, and moved out of
    # the tree on failure (the re-run then starts clean).
    record = [os.path.join(ev_rel, f) for f in RECORD_FILES
              if os.path.exists(os.path.join(REPO, ev_rel, f))]
    if not res.ok:
        keep = os.path.join(tempfile.gettempdir(), 'ingest_failed_%s' % label)
        os.makedirs(keep, exist_ok=True)
        for r in record:
            shutil.move(os.path.join(REPO, r), os.path.join(keep, os.path.basename(r)))
        leftovers = put_tree_back(keep)
        if leftovers:
            say('  put back %d file(s) the landing wrote outside its carriers (kept in %s)'
                % (leftovers, keep))
        die('the landing stopped at step %r and put every file back as it was.\n%s\n'
            'Full log: %s/FLIGHT.log. The inputs commit stays; fix the cause and run the same '
            'command again.' % (res.failed_step, str(res.error)[:3000], keep))
    if record:
        git('add', *record)
        git('commit', '-q', '-m', '%s: the landing record (tools/ingest)' % week['name'].title())
    reseed_workspace()
    summarise(week)
    rebuild_app()
    if not a.no_push:
        p = subprocess.run(['git', 'push', 'origin', 'HEAD'], cwd=REPO, capture_output=True,
                           text=True)
        say('  pushed' if p.returncode == 0 else '  NOT pushed:\n' + (p.stdout + p.stderr)[-600:])
    say('\nDONE.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
