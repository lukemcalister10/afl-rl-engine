"""Persistent in-process engine host (READ-ONLY diagnosis).

Loads _merged_recover.py exactly as probe3.py does (cwd = ws_r23 copy, RL_REPO = repo_r23),
then serves task files dropped into TASKDIR. Each task_*.py is exec'd with G = engine globals.
Nothing in the real repo is written.
"""
import io, contextlib, os, sys, time, traceback, glob

TASKDIR = os.environ['TASKDIR']
os.makedirs(TASKDIR, exist_ok=True)

t0 = time.time()
G = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
print("LOADED %.1fs SEASON_FE=%r" % (time.time() - t0, G.get('SEASON_FE')), flush=True)
open(os.path.join(TASKDIR, 'READY'), 'w').write('%.1f\n' % (time.time() - t0))

done = set()
while not os.path.exists(os.path.join(TASKDIR, 'STOP')):
    for f in sorted(glob.glob(os.path.join(TASKDIR, 'task_*.py'))):
        if f in done:
            continue
        done.add(f)
        out = f[:-3] + '.out'
        buf = io.StringIO()
        t = time.time()
        try:
            with contextlib.redirect_stdout(buf):
                exec(open(f).read(), {'G': G, '__name__': '__task__', 'OUTBASE': f[:-3]})
        except Exception:
            buf.write('\n!!! EXCEPTION\n' + traceback.format_exc())
        open(out, 'w').write(buf.getvalue())
        open(f[:-3] + '.done', 'w').write('%.1fs\n' % (time.time() - t))
        print("RAN %s (%.1fs)" % (os.path.basename(f), time.time() - t), flush=True)
    time.sleep(1.0)
print("STOPPED", flush=True)
