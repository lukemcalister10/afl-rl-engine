#!/usr/bin/env python3
"""THE LOAD-ONCE HARNESS — the engine loads ONCE, every instrument pass runs in-process.

OWNER DIRECTIVE (2026-08-25, standing): "We don't unnecessarily run machine time or actual
time when it could be made efficient. Parallelise. Load things once." The measured reality
behind this file (register v858): one 591-second engine load, then the day-0 population scan
0.4s, the W2 class marks 0.4s (reproducing the filed 1.0637 exactly), ev() at ~8/second —
versus a fresh multi-minute boot per instrument, which is how a battery used to spend hours.

WHAT A PASS IS. A pass is a python file defining run(ns). It receives the loaded namespace
and returns a JSON-serializable verdict (dict preferred; None is allowed for pure asserts —
an exception is the failure channel). ns carries:
    ns['G']     the engine module globals (everything _merged_recover.py defines)
    ns['MA'],
    ns['ev']    the two names every instrument reaches for, hoisted
    ns['repo']  the repo root (RL_REPO)
    ns['T']     the shared wall-clock timer: ns['T']('label') prints elapsed-since-load-start
Passes run SEQUENTIALLY on the one load — after the load they cost seconds, so in-process
sequencing beats parallel processes that would each pay the load again. Long independent
jobs that genuinely need hours still get their own processes; this harness is for batteries.

DISCIPLINE (inherited, not reinvented): invoke through `tools/harness`, which takes the
build lock, runs Guard 5 (P2: never boot on an unverified store), binds RL_FV to the
checkout, and enters the workspace under RL_CONFIG_MODE=gate before this file runs. Invoking
this file directly is for candidate roots that carry their own discipline (the run_o45_emits
pattern: env RL_CONFIG_MODE=gate RL_REPO=<root> RL_FV=<root>/engine/forward_valuation).

LAW 2, SILENCE IS A RED: every pass prints a timed verdict line or the run exits non-zero.
A pass that raises marks the RUN failed but the remaining passes still execute (their
verdicts are worth having); the exit code carries the failure.
"""
import contextlib, importlib.util, io, json, os, sys, time

USAGE = "usage: harness_run.py [--emit-json OUT.json] PASS1.py [PASS2.py ...]"

# The engine file carries a demo script tail below this marker; the harness loads everything
# above it, exactly as the measured prototype did. The marker is ASSERTED — a refactor that
# drops it must come here and say what the new boundary is, not silently exec the tail.
TAIL_MARKER = 'print("=== AFTER'

def main(argv):
    out_path = None
    args = list(argv)
    if args and args[0] == '--emit-json':
        if len(args) < 2:
            raise SystemExit(USAGE)
        out_path = args[1]; args = args[2:]
    if not args:
        raise SystemExit(USAGE)
    passes = [os.path.abspath(a) for a in args]
    for p in passes:
        if not os.path.exists(p):
            raise SystemExit("harness: no such pass file: %s" % p)

    t0 = time.time()
    def T(label):
        print('%8.1fs  %s' % (time.time() - t0, label), flush=True)

    os.environ.setdefault('RL_CONFIG_MODE', 'gate')
    repo = os.environ.get('RL_REPO')
    if not repo:
        raise SystemExit("harness: RL_REPO is not set — invoke through tools/harness, or "
                         "export the discipline yourself (see the module docstring).")
    sys.path.insert(0, repo)
    sys.path.insert(0, os.getcwd())      # the engine workdir: _merged_recover imports rl_model et al from HERE
    import config_manifest
    config_manifest.enforce(os.environ['RL_CONFIG_MODE'])
    T('config enforced (%s mode)' % os.environ['RL_CONFIG_MODE'])

    src = open('_merged_recover.py').read()
    if TAIL_MARKER not in src:
        raise SystemExit("harness: the script-tail marker %r is not in _merged_recover.py — "
                         "the load boundary moved; fix the harness deliberately, do not exec "
                         "the tail by accident." % TAIL_MARKER)
    G = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src.split(TAIL_MARKER)[0], G)
    ns = {'G': G, 'MA': G['MA'], 'ev': G['ev'], 'repo': repo, 'T': T}
    T('ENGINE LOADED (the once-only cost)')

    results, failed = {}, []
    for p in passes:
        name = os.path.splitext(os.path.basename(p))[0]
        t_pass = time.time()
        try:
            spec = importlib.util.spec_from_file_location('harness_pass_' + name, p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if not hasattr(mod, 'run'):
                raise RuntimeError("pass defines no run(ns)")
            verdict = mod.run(ns)
            results[name] = verdict
            T('PASS %-28s ok in %.1fs  %s' % (name, time.time() - t_pass,
                json.dumps(verdict)[:120] if verdict is not None else ''))
        except SystemExit:
            raise
        except Exception as e:
            failed.append(name)
            results[name] = {'error': repr(e)}
            T('PASS %-28s FAILED in %.1fs  %r' % (name, time.time() - t_pass, e))
    if out_path:
        json.dump({'passes': results, 'failed': failed,
                   'workdir': os.getcwd(), 'wall_s': round(time.time() - t0, 1)},
                  open(out_path, 'w'), indent=1)
        T('verdicts written: %s' % out_path)
    if failed:
        T('RUN FAILED — passes red: %s' % ', '.join(failed))
        return 1
    T('RUN GREEN — %d passes on one load' % len(results))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
