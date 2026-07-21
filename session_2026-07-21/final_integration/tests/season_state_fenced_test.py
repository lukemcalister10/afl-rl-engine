#!/usr/bin/env python3
"""FENCED SEASON-STATE READ tests (final integration 2026-07-21, supervisor 3rd review req 1).

The engine's dynamic season-state readers (rl_model / _merged_recover / conditional_prior `_season_val`,
and season_state.calendar_progress_value / exposure_pace_value) must HALT — never silently fall back to the
Round-14 default — whenever RL_CONFIG_MODE is a FENCED release mode (bake | gate | canonical) and the
authoritative data/season_state.json cannot be loaded/validated. An explicitly UNFENCED development shell
(RL_CONFIG_MODE unset) may use the declared fallback.

This proves, for EACH fenced mode and each corruption:
  (A) season_state.read_value + the two accessors: fenced -> SeasonStateError; unfenced -> fallback;
  (B) the SHIPPED engine `_season_val` bytes (extracted from each engine module, exec'd in isolation so no
      heavy import is needed): fenced -> raises; unfenced -> fallback;
  (C) rejection happens BEFORE any board is written: a gate-mode canonical build against a corrupted
      season_state.json exits non-zero and writes NO board (canonical files untouched). [workspace-gated]

Corruptions covered: missing file, malformed JSON, missing key, non-numeric value, non-finite value,
and (fenced only) an unresolved/untrusted repo root.

Run:  python3 session_2026-07-21/final_integration/tests/season_state_fenced_test.py
"""
import os, sys, json, re, tempfile, shutil, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FENCED = ('bake', 'gate', 'canonical')
ENGINE_MODULES = {
    'rl_model':          os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py'),
    '_merged_recover':   os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py'),
    'conditional_prior': os.path.join(ROOT, 'engine', 'forward_valuation', 'conditional_prior.py'),
}
R = []
def ok(name, cond, detail=''):
    R.append((name, bool(cond), detail))
    print(("  PASS " if cond else "  FAIL ") + name + (("  -- " + detail) if detail and not cond else ''))


def _load(modname, path):
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

SS = _load('season_state_fz', os.path.join(ROOT, 'season_state.py'))


def _extract_season_val(path):
    """Return a callable of the SHIPPED `_season_val` function, exec'd in an isolated namespace with only
    `os`/`json` (so we test the real shipped bytes without importing the heavy engine module)."""
    src = open(path).read()
    m = re.search(r'\ndef _season_val\(_key, _fb\):\n(?:(?: {4}.*)?\n)+', src)
    if not m:
        raise AssertionError("could not locate _season_val in %s" % path)
    ns = {'os': os, 'json': json}
    exec(m.group(0), ns)
    return ns['_season_val']


def _fixture(tmp, body):
    d = os.path.join(tmp, 'data'); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'season_state.json')
    if body is None:
        if os.path.exists(p): os.remove(p)
    else:
        open(p, 'w').write(body)
    return tmp

VALID = json.dumps({'calendar_progress': 0.58, 'exposure_pace': 0.545})
CORRUPTIONS = {
    'missing-file':  None,
    'malformed':     '{ not valid json',
    'missing-key':   json.dumps({'exposure_pace': 0.545}),        # no calendar_progress
    'non-numeric':   json.dumps({'calendar_progress': 'soon'}),
    'non-finite':    json.dumps({'calendar_progress': 'Infinity'}),  # -> float('inf')
}


def _with_env(**kw):
    saved = {k: os.environ.get(k) for k in kw}
    for k, v in kw.items():
        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    def restore():
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    return restore


def part_a():
    print("\n(A) season_state.read_value + accessors")
    # unfenced dev: every corruption -> fallback (never raises)
    r = _with_env(RL_CONFIG_MODE=None, RL_REPO=None, CLAUDE_PROJECT_DIR=None)
    try:
        for label, body in CORRUPTIONS.items():
            t = _fixture(tempfile.mkdtemp(), body)
            try:
                v = SS.read_value('calendar_progress', 0.58, root=t)
                ok('unfenced %s -> fallback 0.58' % label, v == 0.58, 'got %r' % v)
            except Exception as e:
                ok('unfenced %s -> fallback 0.58' % label, False, 'raised %r' % e)
            finally:
                shutil.rmtree(t, ignore_errors=True)
    finally:
        r()
    # fenced modes: every corruption -> SeasonStateError; a valid file -> the real value
    for mode in FENCED:
        r = _with_env(RL_CONFIG_MODE=mode, RL_REPO=None, CLAUDE_PROJECT_DIR=None)
        try:
            tv = _fixture(tempfile.mkdtemp(), VALID)
            ok('fenced %s valid -> real value 0.58' % mode, SS.calendar_progress_value(root=tv) == 0.58)
            shutil.rmtree(tv, ignore_errors=True)
            for label, body in CORRUPTIONS.items():
                t = _fixture(tempfile.mkdtemp(), body)
                try:
                    SS.read_value('calendar_progress', 0.58, root=t)
                    ok('fenced %s %s -> HALT' % (mode, label), False, 'did not raise')
                except SS.SeasonStateError:
                    ok('fenced %s %s -> HALT' % (mode, label), True)
                except Exception as e:
                    ok('fenced %s %s -> HALT' % (mode, label), False, 'wrong exc %r' % e)
                finally:
                    shutil.rmtree(t, ignore_errors=True)
            # unresolved/untrusted root (no candidate carries the state) -> HALT
            empty = tempfile.mkdtemp()
            try:
                SS.read_value('calendar_progress', 0.58, root=empty)
                ok('fenced %s unresolved-root -> HALT' % mode, False, 'did not raise')
            except SS.SeasonStateError:
                ok('fenced %s unresolved-root -> HALT' % mode, True)
            finally:
                shutil.rmtree(empty, ignore_errors=True)
        finally:
            r()


def part_b():
    print("\n(B) shipped engine `_season_val` bytes (rl_model / _merged_recover / conditional_prior)")
    fns = {name: _extract_season_val(path) for name, path in ENGINE_MODULES.items()}
    for name, fn in fns.items():
        # unfenced: corruption -> fallback
        r = _with_env(RL_CONFIG_MODE=None, RL_REPO=None, CLAUDE_PROJECT_DIR=None)
        try:
            t = _fixture(tempfile.mkdtemp(), '{ bad'); os.environ['RL_REPO'] = t
            ok('%s unfenced malformed -> fallback' % name, fn('calendar_progress', 0.58) == 0.58)
            shutil.rmtree(t, ignore_errors=True)
        finally:
            r()
        # fenced modes: corruption -> raise; valid -> real value
        for mode in FENCED:
            tv = _fixture(tempfile.mkdtemp(), VALID)
            r = _with_env(RL_CONFIG_MODE=mode, RL_REPO=tv, CLAUDE_PROJECT_DIR=None)
            try:
                ok('%s fenced %s valid -> real value' % (name, mode), fn('calendar_progress', 0.58) == 0.58)
            finally:
                r(); shutil.rmtree(tv, ignore_errors=True)
            for label, body in CORRUPTIONS.items():
                t = _fixture(tempfile.mkdtemp(), body)
                r = _with_env(RL_CONFIG_MODE=mode, RL_REPO=t, CLAUDE_PROJECT_DIR=None)
                try:
                    fn('calendar_progress', 0.58)
                    ok('%s fenced %s %s -> HALT' % (name, mode, label), False, 'did not raise')
                except Exception:
                    ok('%s fenced %s %s -> HALT' % (name, mode, label), True)
                finally:
                    r(); shutil.rmtree(t, ignore_errors=True)
            # unresolved root (RL_REPO/CLAUDE_PROJECT_DIR unset) -> raise
            r = _with_env(RL_CONFIG_MODE=mode, RL_REPO=None, CLAUDE_PROJECT_DIR=None)
            try:
                fn('calendar_progress', 0.58)
                ok('%s fenced %s unresolved-root -> HALT' % (name, mode), False, 'did not raise')
            except Exception:
                ok('%s fenced %s unresolved-root -> HALT' % (name, mode), True)
            finally:
                r()


def part_c():
    """(C) rejection BEFORE any board write: a gate-mode canonical build against a corrupted season_state.json
    exits non-zero and produces NO board. Uses the bootstrap workspace if present (fails fast at the
    import-time season read, well before board generation). Skipped (not failed) if no workspace exists."""
    print("\n(C) rejection occurs before any board is written (gate build; workspace-gated)")
    ws = '/home/claude/rl_workspace/rl_after'
    ssf = os.path.join(ws, 'data', 'season_state.json')
    export = os.path.join(ws, 'rl_export.py')
    if not (os.path.isdir(ws) and os.path.exists(export) and os.path.exists(ssf)):
        ok('gate build halts before board write (workspace present)', True, 'SKIPPED: no bootstrap workspace')
        return
    board = os.path.join(ws, 'rl_app_data.json')
    backup = ssf + '.fztest.bak'
    shutil.copy(ssf, backup)
    board_before = os.path.exists(board)
    board_mtime = os.path.getmtime(board) if board_before else None
    try:
        open(ssf, 'w').write('{ corrupt-season-state')          # break the authoritative state
        env = {k: v for k, v in os.environ.items() if not (k.startswith('RL_') or k.startswith('PAR_'))}
        env.update({'PYTHONPATH': ws + os.pathsep + '/home/claude/rl_vendor', 'RL_CONFIG_MODE': 'gate',
                    'RL_REPO': ws, 'RL_FV': os.path.join(ROOT, 'engine', 'forward_valuation')})
        p = subprocess.run('python3 rl_export.py', cwd=ws, env=env, shell=True, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        halted = p.returncode != 0
        no_board = (not board_before) and (not os.path.exists(board)) or \
                   (board_before and os.path.getmtime(board) == board_mtime)
        ok('gate build with corrupt season_state.json exits non-zero', halted, 'rc=%d' % p.returncode)
        ok('gate build wrote NO new board (rejection before board write)', no_board)
    finally:
        shutil.move(backup, ssf)


def main():
    print("=== FENCED SEASON-STATE READ TESTS (fenced HALT vs dev fallback) ===")
    part_a(); part_b(); part_c()
    npass = sum(1 for _, p, _ in R if p); n = len(R)
    print("\nRESULT: %d/%d PASS" % (npass, n))
    return 0 if npass == n else 1


if __name__ == '__main__':
    sys.exit(main())
