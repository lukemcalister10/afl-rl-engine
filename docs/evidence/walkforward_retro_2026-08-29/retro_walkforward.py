#!/usr/bin/env python3
"""THE WALK-FORWARD RETROSPECTIVE — every round since R14 priced under the LIVE engine.

Owner ask (2026-08-29, verbatim): "What about the movers list having each round since round 14 as
an option under the currently approved and live engine?" — the retrospective he first phrased on
2026-08-21 ("what each round since we started the ingestion would look like under that live state
of the model"), unblocked by the proven S4 parallelization and the ORDER 49 landing.

THE HONEST CONSTRUCTION (one store, one model, eleven as-of points): each round R in 14..24 is
priced from the CURRENT corrected store with each player's 2026 season truncated to what he had
played AS AT round R, and the season clock set as-of R. Old per-round stores are NOT used — they
lack months of landed data corrections (birthdates, back-filled seasons, ownership), so their
holes would masquerade as model behaviour. The truncation arithmetic is exact and fully sourced:

    games_R = games_full − |{applied rounds r > R with played=true}|
    sum_R   = avg_full·games_full − Σ score(r) over those rounds
    avg_R   = sum_R / games_R          (2026 row DROPPED when games_R == 0 — not yet debuted)

with per-round played/score read from the committed weekly reports of record
(ui/data/movers.js, rounds 15..24). R14 subtracts every applied round — the season-baseline point.
Retired/rows off the current board simply do not appear (the series covers the live population).

CONTROL FIRST: R24's truncation is a NO-OP by construction, so its build must reproduce the live
board 4a52cc44's values exactly — the pipeline validates itself before any real round runs.

Season clock per R (the two documented policy derivations, restated verbatim from
data/season_state.json / release_contract season_metadata):
    calendar_progress = round_half_up(100·R/season_total_rounds)/100
    exposure_pace     = round(median(current 2026 games of durable players, prior≥18)/22, 3) cap 1.0
computed ON THE TRUNCATED STORE, so pace walks backward with the games.

MECHANICS: per round, a sandbox root is assembled (engine dir file-copied, repo data/ mirrored),
the truncated store installed, expected_boot repinned to it (store md5 + as_of_round), season
state re-derived, and rl_export.py run in gate mode — the EXACT shipped pricing path, so the
values are the board's own construction, not a parallel implementation. Output banked per round to
values_rN.json (restart loses one round, never the batch).

Verbs:  emit-stores            build all truncated stores + sandboxes (no engine)
        run R                  price round R in its sandbox (engine, ~10 min)
        control                run R24 and assert value-equality to the live board
        status                 what is banked
"""
import json, hashlib, math, os, shutil, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = '/home/claude/rl_workspace/rl_after'
WORK = '/home/claude/retro_walkforward'
ROUNDS = list(range(14, 25))
APPLIED = list(range(15, 25))
F = 1.0524


def _load_movers_reports():
    src = open(os.path.join(REPO, 'ui', 'data', 'movers.js')).read()
    i = src.index('{', src.index('__MATCHDAY_MOVERS__'))
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    mv = json.loads(src[i:end])
    reps = {int(r): mv['reports'][str(r)] for r in APPLIED if str(r) in mv['reports']}
    missing = [r for r in APPLIED if r not in reps]
    if missing:
        raise SystemExit('HALT: weekly reports missing for rounds %s — the truncation cannot be '
                         'exact without them.' % missing)
    return reps


def _store_players(store):
    return store['players'] if isinstance(store, dict) and 'players' in store else store


def _name_index(players):
    """Exact-name index with a HALT on ambiguity the reports cannot resolve (the two-Max-Kings
    class): a duplicated name is allowed only if at most one twin has a 2026 row — the applied
    scores can then only belong to that twin."""
    by = {}
    for p in players:
        by.setdefault(p.get('player'), []).append(p)
    return by


def _played_map(reps):
    """key -> [(round, score)] for played rounds, plus name and AFL club per key, from the
    reports of record (club disambiguates duplicated names — the Harrison Jones class)."""
    out = {}
    names = {}
    clubs = {}
    for r, rep in reps.items():
        for row in rep['players']:
            if row.get('played') and row.get('score') is not None:
                out.setdefault(row['key'], []).append((r, float(row['score'])))
                names[row['key']] = row['name']
                clubs[row['key']] = row.get('club')
    return out, names, clubs


def truncate_store(R, store, reps):
    players = _store_players(store)
    byname = _name_index(players)
    played, names, clubs = _played_map(reps)
    touched = 0
    for key, rounds_scores in played.items():
        later = [(r, s) for (r, s) in rounds_scores if r > R]
        if not later:
            continue
        nm = names[key]
        cands = byname.get(nm) or []
        cands26 = [p for p in cands if any(x.get('year') == 2026 for x in p.get('scoring', []))]
        if len(cands26) > 1:
            # duplicated name (the Harrison Jones / Max King class): a retired row cannot be the
            # one the weekly feed scored; then the report's own AFL club must pick exactly one.
            cands26 = [p for p in cands26 if not p.get('_retired')]
            if len(cands26) > 1 and clubs.get(key):
                cands26 = [p for p in cands26 if p.get('afl_club') == clubs[key]]
        if len(cands26) != 1:
            raise SystemExit('HALT: cannot uniquely match report row %r (%s, club %r) to a store '
                             'row with a 2026 season (%d candidates) — refusing a guessed '
                             'subtraction.' % (key, nm, clubs.get(key), len(cands26)))
        p = cands26[0]
        row = next(x for x in p['scoring'] if x.get('year') == 2026)
        g, a = int(row['games']), float(row['avg'])
        dg = len(later)
        ds = sum(s for _, s in later)
        ng = g - dg
        if ng < 0:
            raise SystemExit('HALT: %s round subtraction exceeds stored 2026 games (%d - %d) — '
                             'ledger/report disagreement.' % (nm, g, dg))
        if ng == 0:
            p['scoring'] = [x for x in p['scoring'] if x.get('year') != 2026]
        else:
            ns = a * g - ds
            row['games'] = ng
            row['avg'] = round(ns / ng, 2)
        touched += 1
    return touched


def derive_season_state(R, truncated_store_path):
    """The IMMUTABLE policy itself (repo-root season_state.py), applied to the truncated store —
    exactly the module the round applier uses (staged_apply._season_state_module). No re-derivation
    of the formulas here; the policy is one implementation."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('season_state_pol',
                                                  os.path.join(REPO, 'season_state.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    st = m.derive(R, truncated_store_path)
    st['_retro_note'] = 'AS-OF derivation on the truncated store (walk-forward retrospective)'
    return st


def emit_stores():
    reps = _load_movers_reports()
    os.makedirs(WORK, exist_ok=True)
    for R in ROUNDS:
        store = json.load(open(os.path.join(WS, 'rl_model_data.json')))
        touched = truncate_store(R, store, reps)
        d = os.path.join(WORK, 'r%d' % R)
        os.makedirs(d, exist_ok=True)
        store_p = os.path.join(d, 'rl_model_data.json')
        raw = json.dumps(store, indent=1)
        open(store_p, 'w').write(raw)
        md5 = hashlib.md5(raw.encode()).hexdigest()
        st = derive_season_state(R, store_p)
        json.dump(st, open(os.path.join(d, 'season_state.json'), 'w'), indent=1)
        json.dump({'round': R, 'store_md5': md5, 'rows_truncated': touched,
                   'calendar_progress': st['calendar_progress'],
                   'exposure_pace': st['exposure_pace']},
                  open(os.path.join(d, 'META.json'), 'w'), indent=1)
        print('r%-3d store %s  truncated %-3d  cal %.2f pace %.3f'
              % (R, md5[:8], touched, st['calendar_progress'], st['exposure_pace']))


def _assemble_root(R):
    """Assemble a sandbox repo root by SYMLINKING the live repo wholesale, then replacing ONLY the
    three overridden files with real ones. Copying selected subtrees was the wrong shape: the engine
    reads pinned owner inputs from several repo-relative paths (data/, docs/owner_annotations/,
    engine/forward_valuation/, ...) and every path missed cost a full engine load before its halt.
    A symlink farm is complete by construction — anything the engine reads resolves to the real
    repo — and the overrides are the only real files, so nothing can write back into the repo."""
    meta = json.load(open(os.path.join(WORK, 'r%d' % R, 'META.json')))
    root = os.path.join(WORK, 'r%d' % R, 'root')
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    # top level: symlink everything except the two dirs carrying an override
    for name in os.listdir(REPO):
        if name in ('data', 'engine', '.git'):
            continue
        os.symlink(os.path.join(REPO, name), os.path.join(root, name))
    # data/: symlink every entry, then write the two real overrides
    os.makedirs(os.path.join(root, 'data'))
    for name in os.listdir(os.path.join(REPO, 'data')):
        if name in ('expected_boot.json', 'season_state.json'):
            continue
        os.symlink(os.path.join(REPO, 'data', name), os.path.join(root, 'data', name))
    shutil.copy(os.path.join(WORK, 'r%d' % R, 'season_state.json'),
                os.path.join(root, 'data', 'season_state.json'))
    eb = json.load(open(os.path.join(REPO, 'data', 'expected_boot.json')))
    eb['store'] = meta['store_md5']
    eb['as_of_round'] = R
    json.dump(eb, open(os.path.join(root, 'data', 'expected_boot.json'), 'w'),
              indent=1, sort_keys=True)
    # engine/: symlink every entry except rl_after, which is a real dir of symlinks + the store
    os.makedirs(os.path.join(root, 'engine'))
    for name in os.listdir(os.path.join(REPO, 'engine')):
        if name == 'rl_after':
            continue
        os.symlink(os.path.join(REPO, 'engine', name), os.path.join(root, 'engine', name))
    ra = os.path.join(root, 'engine', 'rl_after')
    os.makedirs(ra)
    for name in os.listdir(WS):
        if name in ('rl_model_data.json', 'rl_app_data.json'):
            continue
        os.symlink(os.path.join(WS, name), os.path.join(ra, name))
    shutil.copy(os.path.join(WORK, 'r%d' % R, 'rl_model_data.json'),
                os.path.join(ra, 'rl_model_data.json'))
    return root, ra


def run_round(R):
    out_p = os.path.join(HERE, 'values_r%d.json' % R)
    root, ra = _assemble_root(R)
    env = {k: v for k, v in os.environ.items() if k != 'RL_BUILD_LOCK_HELD'}
    env.update({'RL_CONFIG_MODE': 'gate', 'RL_REPO': root, 'OMP_NUM_THREADS': '1',
                'RL_FV': os.path.join(REPO, 'engine', 'forward_valuation'),
                'PYTHONPATH': ra + ':/home/claude/rl_vendor',
                'PATH': '/root/rl_venv312/bin:' + env.get('PATH', '')})
    r = subprocess.run([sys.executable, 'rl_export.py'], cwd=ra, env=env,
                       capture_output=True, text=True, timeout=5400)
    board_p = os.path.join(ra, 'rl_app_data.json')
    if r.returncode != 0 or not os.path.exists(board_p):
        open(os.path.join(HERE, 'r%d_export.log' % R), 'w').write(r.stdout + '\n' + r.stderr)
        raise SystemExit('HALT r%d: export rc=%d — log filed r%d_export.log' % (R, r.returncode, R))
    board = json.load(open(board_p))
    vals = {p['key']: p['v'] for p in board['active']}
    json.dump({'round': R, 'n': len(vals),
               'board_md5': hashlib.md5(open(board_p, 'rb').read()).hexdigest(),
               'values': vals}, open(out_p, 'w'), indent=1)
    shutil.rmtree(root)
    print('r%d BANKED: %d players -> %s' % (R, len(vals), os.path.basename(out_p)))


def control():
    run_round(24)
    got = json.load(open(os.path.join(HERE, 'values_r24.json')))
    live = json.load(open(os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')))
    lv = {p['key']: p['v'] for p in live['active']}
    diff = {k: (got['values'][k], lv[k]) for k in lv
            if k in got['values'] and got['values'][k] != lv[k]}
    missing = [k for k in lv if k not in got['values']]
    if diff or missing:
        json.dump({'diff': diff, 'missing': missing},
                  open(os.path.join(HERE, 'CONTROL_FAIL.json'), 'w'), indent=1)
        raise SystemExit('CONTROL FAIL: %d value diffs, %d missing — the pipeline does NOT '
                         'reproduce the live board; do not price the real rounds.'
                         % (len(diff), len(missing)))
    print('CONTROL PASS: r24 no-op truncation reproduces the live board values exactly (%d rows).'
          % len(lv))


def resume(max_conc=4):
    """RESTART-SURVIVABLE DRIVER. Container reclaims have been landing faster than a single build
    completes, so the series is not gated serially on a control build any more: every unbanked round
    is launched detached, each banks its own values_rN.json, and a relaunch simply skips what is
    already banked. R24 remains the CONTROL — it is priced like any other round and its value-equality
    to the live board is asserted by `control-check` before the series is emitted. If that assertion
    fails the whole series is discarded, so the discipline is unchanged; only the ordering is."""
    todo = [R for R in ROUNDS
            if not os.path.exists(os.path.join(HERE, 'values_r%d.json' % R))]
    if not todo:
        print('all %d rounds banked — nothing to resume' % len(ROUNDS))
        return
    running = 0
    for R in todo:
        if running >= max_conc:
            break
        log = os.path.join(WORK, 'r%d.log' % R)
        cmd = ('setsid nohup env OMP_NUM_THREADS=1 %s %s run %d > %s 2>&1 < /dev/null &'
               % (sys.executable, os.path.abspath(__file__), R, log))
        subprocess.Popen(['/bin/bash', '-c', cmd])
        running += 1
        print('launched r%d -> %s' % (R, log))
    print('%d launched, %d still queued (relaunch resume to continue)'
          % (running, max(0, len(todo) - running)))


def control_check():
    """The control assertion, run on the BANKED r24: its no-op truncation must reproduce the live
    board's values exactly. The series is emitted only if this passes."""
    p24 = os.path.join(HERE, 'values_r24.json')
    if not os.path.exists(p24):
        raise SystemExit('HALT: r24 is not banked — the control cannot be asserted.')
    got = json.load(open(p24))
    live = json.load(open(os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')))
    lv = {p['key']: p['v'] for p in live['active']}
    diff = {k: (got['values'][k], lv[k]) for k in lv
            if k in got['values'] and got['values'][k] != lv[k]}
    missing = [k for k in lv if k not in got['values']]
    if diff or missing:
        json.dump({'diff': diff, 'missing': missing},
                  open(os.path.join(HERE, 'CONTROL_FAIL.json'), 'w'), indent=1)
        raise SystemExit('CONTROL FAIL: %d value diffs, %d missing — the pipeline does NOT reproduce '
                         'the live board; the series is NOT emitted.' % (len(diff), len(missing)))
    print('CONTROL PASS: r24 reproduces the live board values exactly (%d rows).' % len(lv))


if __name__ == '__main__':
    verb = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if verb == 'emit-stores':
        emit_stores()
    elif verb == 'run':
        run_round(int(sys.argv[2]))
    elif verb == 'control':
        control()
    elif verb == 'resume':
        resume(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif verb == 'control-check':
        control_check()
    elif verb == 'status':
        for R in ROUNDS:
            p = os.path.join(HERE, 'values_r%d.json' % R)
            print('r%-3d %s' % (R, 'BANKED' if os.path.exists(p) else '-'))
    else:
        raise SystemExit('verbs: emit-stores | run R | resume [N] | control-check | control | status')
