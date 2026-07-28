"""ITEM 225 STAGE 2 — THE BOARD EFFECT, ON A SCRATCH BOARD ONLY.

NOTHING HERE IS ADOPTED, BAKED, RE-PINNED TO `main`, OR RELEASED. The checked-out engine is not
modified: the derived curve is written into a SCRATCH COPY of the workspace and the regenerated
v0surf goes to a SCRATCH pickle addressed by RL_V0SURF_PKL. `data/expected_boot.json` in the
checkout is untouched, the board of record does not move, and the shipped UI bundles are not
touched. (Addendum 2 §5 permits a local re-pin as a working necessity; this run does not even
need one, because the scratch pickle is addressed by env rather than by the pin.)

THE HALT IS THE DESIGN AND THIS SCRIPT EXPECTS IT (Addendum 2 §1). Changing the curve changes the
v0surf config signature, so loading the scratch workspace HALTs with FROZEN-SIGNATURE. That is
correct behaviour reporting itself. This script does NOT restore a fallback and does NOT widen the
accepted-signature set — it regenerates deliberately, under the declared RL_V0SURF_REFIT=1 entry
point, and records both signatures so every figure can name the surface it was measured on.
"""
import os, sys, io, json, shutil, contextlib, subprocess, hashlib

REPO  = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
BASE  = REPO + '/session_2026-07-28/item225_stage2'
OUT   = BASE + '/out'
WS    = '/home/claude/rl_workspace/rl_after'
SCR   = '/home/claude/rl_scratch225'
SCRPKL = SCR + '/v0surf_scratch.pkl'


def load_engine(cwd, extra_env=None):
    """Load the engine from `cwd` in a SUBPROCESS and return its ev-map + surface metadata.
    A subprocess because the engine is import-time-executed and cannot be loaded twice in one
    interpreter with different curves."""
    code = r'''
import io,contextlib,json,sys,os
g={}
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
try:
    with contextlib.redirect_stdout(io.StringIO()): exec(src,g)
except SystemExit as e:
    print(json.dumps({"halt":str(e)})); sys.exit(0)
MA=g['MA']; ev=g['ev']; META=g['_V0CURVE_META']
rows={}
for p in MA.data:
    if not MA.GRP.get(p.get('pos')): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()): v=ev(p)
    except Exception: v=None
    if v is not None: rows[p.get('key') or p['player']]=round(float(v),4)
print(json.dumps({"sig":META.get('_v0surf_sig'),"frozen":bool(META.get('_v0surf_frozen')),
                  "curve":{str(k):MA.PVC[k] for k in sorted(MA.PVC)},"ev":rows}))
'''
    env = dict(os.environ); env.update(extra_env or {})
    r = subprocess.run([sys.executable, '-c', code], cwd=cwd, env=env,
                       capture_output=True, text=True)
    tail = [l for l in r.stdout.strip().splitlines() if l.startswith('{')]
    if not tail:
        print("---- stdout ----\n" + r.stdout[-3000:]); print("---- stderr ----\n" + r.stderr[-3000:])
        raise SystemExit("engine load produced no JSON (cwd=%s)" % cwd)
    return json.loads(tail[-1])


def main():
    d = json.load(open(OUT + '/derived_split.json'))
    curve = d['curve_after']
    pool_level = int(round(d['same_footing']['pool']['realised_scar']))

    # ---------- 1. BASELINE: the checkout as it stands, frozen surface ----------------------
    print("== 1. BASELINE (main, untouched, frozen v0surf) ==")
    base = load_engine(WS)
    assert 'halt' not in base, base
    print("   surface %s frozen=%s   curve[1]=%s curve[64]=%s"
          % (base['sig'][:8], base['frozen'], base['curve']['1'], base['curve']['64']))

    # ---------- 2. SCRATCH WORKSPACE with the DERIVED curve ---------------------------------
    if os.path.isdir(SCR): shutil.rmtree(SCR)
    shutil.copytree(WS, SCR)
    doc = json.load(open(WS + '/pvc_curve_v2.json'))
    doc['curve'] = {str(k): int(curve[k - 1]) for k in range(1, 65)}
    doc['pool_value'] = pool_level
    doc['curve_md5'] = hashlib.md5(json.dumps(doc['curve'], sort_keys=True).encode()).hexdigest()[:8]
    doc['source'] = ('ITEM 225 STAGE 2 CANDIDATE — derived from scratch on store %s. '
                     'NOT ADOPTED. Scratch measurement only.' % d['meta']['store_md5'])
    doc['item225_stage2'] = dict(store=d['meta']['store_md5'], nd_fit_rows=d['populations']['nd_fit_rows'],
                                 pool_rows=d['populations']['pool_rows'],
                                 pool_level_basis='realised outcomes, never-established entered as 0.0',
                                 adopted=False)
    json.dump(doc, open(SCR + '/pvc_curve_v2.json', 'w'), indent=1)
    print("\n== 2. SCRATCH workspace written (curve 1-64 derived; pool_value=%d) ==" % pool_level)

    # ---------- 3. THE HALT. EXPECTED. NOT ROUTED AROUND. -----------------------------------
    print("\n== 3. LOADING THE SCRATCH WORKSPACE — the halt is the design, and it should fire ==")
    halted = load_engine(SCR, {'RL_V0SURF_PKL': REPO + '/data/v0surf.pkl'})
    if 'halt' in halted:
        print("   HALT FIRED, AS INTENDED:")
        for line in halted['halt'].strip().splitlines()[:4]:
            print("     " + line.strip())
    else:
        print("   !! NO HALT — signature %s was already in the pickle. Investigate before trusting "
              "any figure below." % halted.get('sig'))

    # ---------- 4. DELIBERATE REGENERATION, declared entry point ----------------------------
    print("\n== 4. REGENERATING v0surf DELIBERATELY (RL_V0SURF_REFIT=1), to a SCRATCH pickle ==")
    print("   the checkout's data/v0surf.pkl and data/expected_boot.json are NOT written")
    refit = load_engine(SCR, {'RL_V0SURF_REFIT': '1'})
    assert 'halt' not in refit, refit
    print("   refit surface signature: %s   frozen=%s" % (refit['sig'], refit['frozen']))

    # intra-box determinism: the cleanliness evidence that IS available
    refit2 = load_engine(SCR, {'RL_V0SURF_REFIT': '1'})
    same = (refit['ev'] == refit2['ev']) and (refit['sig'] == refit2['sig'])
    print("   intra-box determinism across repeated refits: %s" % ("IDENTICAL" if same else "DIVERGED"))

    # ---------- 5. THE BOARD EFFECT ---------------------------------------------------------
    a, b = base['ev'], refit['ev']
    keys = sorted(set(a) & set(b))
    movers = [(k, a[k], b[k], b[k] - a[k]) for k in keys if abs(b[k] - a[k]) > 1e-6]
    movers.sort(key=lambda x: -abs(x[3]))
    print("\n== 5. BOARD EFFECT (scratch board vs baseline board) ==")
    print("   players compared        : %d" % len(keys))
    print("   movers (|delta| > 1e-6) : %d  (%.1f%%)" % (len(movers), 100.0 * len(movers) / max(len(keys), 1)))
    if movers:
        import statistics as st
        deltas = [m[3] for m in movers]
        print("   mean delta %+.2f   median %+.2f   max %+.2f   min %+.2f"
              % (st.mean(deltas), st.median(deltas), max(deltas), min(deltas)))
        print("\n   largest 15 movers:")
        print("   %-28s %10s %10s %9s" % ('player', 'baseline', 'scratch', 'delta'))
        for k, x, y, dd in movers[:15]:
            print("   %-28s %10.1f %10.1f %+9.1f" % (k[:28], x, y, dd))

    json.dump(dict(baseline_sig=base['sig'], baseline_frozen=base['frozen'],
                   scratch_sig=refit['sig'], scratch_frozen=refit['frozen'],
                   halt_fired=('halt' in halted),
                   halt_text=halted.get('halt', '')[:600],
                   intra_box_deterministic=same,
                   pool_value_used=pool_level,
                   n_compared=len(keys), n_movers=len(movers),
                   movers=[dict(key=k, baseline=x, scratch=y, delta=round(dd, 3))
                           for k, x, y, dd in movers[:200]]),
              open(OUT + '/scratch_board.json', 'w'), indent=1)
    print("\nwrote out/scratch_board.json")
    print("NOTHING ADOPTED. checkout engine, data/v0surf.pkl, expected_boot.json, UI bundles: untouched.")


if __name__ == '__main__':
    main()
