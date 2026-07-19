#!/usr/bin/env python3
"""REFIT / FREEZE ENTRY POINT for the FROZEN V0 pick-curve surface (v0surf) — LEG F6, 2026-07-18 (item 381).

WHY THIS EXISTS
  _build_v0_curve() used to RE-FIT the shipped V0 pick-curve surface (three isotonic surfaces via _iso_dec)
  at every board/gate/panel import, over the REAL roster's _v0_raw. numpy's OpenBLAS is DYNAMIC_ARCH, so the
  same commit produced a slightly different surface per CPU on a mixed fleet — the whole board shifted
  coherently (the balanced-board 06d8af60 <-> 83a4b21d weather flip, Sheezel +/-95; item 380 diagnosis).
  q97m/cm are frozen pickles and the NW kernels are order-fixed (_det_*); _iso_dec/_build_v0_curve was the ONE
  live fit left on the value path. It now gets the q97m treatment: computed ONCE on a CLEAN instance, pickled
  to data/v0surf.pkl (keyed by a deterministic config signature), stamped in data/expected_boot.json 'v0surf',
  asserted by boot_guard on entry, and LOADED — never fitted at board-build.

  This is the ONE committed refit path (a silent refit is the defect being frozen out). It is GATED: an ordinary
  build/gate/panel run cannot trigger it, and --bake requires RL_BAKE_V0SURF=1.

PRECONDITION (MANDATORY): run ONLY on a CLEAN instance — one whose balanced board == 06d8af60 byte-exact.
  Freezing on a weather box would bake the flipped surface in permanently (item 380). The caller asserts the
  clean precondition BEFORE invoking --bake.

USAGE  (run from the workspace rl_after, single-thread, RL_REPO set):
  Verify (no write) — refit into memory on THIS box and compare to the committed pin:
      RL_V0SURF_REFIT=1 python3 <repo>/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify
  Bake (BAKE ONLY — writes data/v0surf.pkl + re-pins expected_boot.json 'v0surf' + provenance):
      RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 <repo>/session_2026-07-18/legf6/scripts/refit_v0surf.py --bake
  Both modes read the engine's OWN freshly-fit surfaces (exec _merged_recover.py with RL_V0SURF_REFIT=1, which
  forces the fit), so the frozen artifact and its regeneration are a single source.
"""
import os, sys, io, json, time, pickle, hashlib, contextlib

def _repo_root():
    for c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
              os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))):
        if c and os.path.exists(os.path.join(c, 'data', 'expected_boot.json')):
            return os.path.abspath(c)
    return os.getcwd()

def _md5_bytes(b): return hashlib.md5(b).hexdigest()

def _engine_surfaces():
    """Exec _merged_recover.py (from cwd = the workspace rl_after) with RL_V0SURF_REFIT=1 forced, so
    _build_v0_curve FITS; read the FINAL (shipped, RL_PVC2 default) surfaces + fit metas + config signature."""
    os.environ['RL_V0SURF_REFIT'] = '1'
    eng = '_merged_recover.py'
    if not os.path.exists(eng):
        raise SystemExit("refit HALT: _merged_recover.py not in cwd — run from the workspace rl_after (the refit "
                         "reads the engine's own freshly-fit surfaces).")
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(eng).read().split('print("=== AFTER')[0], g)
    META = g['_V0CURVE_META']
    c18 = META['_c18']; surfN = META['_surfN']; surfR = META['_surfR']; sig = META['_v0surf_sig']
    # the fit metas _v0_curve_assert() and reports read back on the LOAD path (ages etc.)
    meta = {k: v for k, v in META.items()
            if k in ('mature_nonRUC', 'mature_RUC') or (isinstance(k, tuple) and k and k[0] == 'age18')}
    return sig, {'c18': c18, 'surfN': surfN, 'surfR': surfR, 'meta': meta}

def main(argv):
    root = _repo_root()
    pkl_path = os.path.join(root, 'data', 'v0surf.pkl')
    boot_path = os.path.join(root, 'data', 'expected_boot.json')
    with open(boot_path) as f: boot = json.load(f)
    pinned = boot.get('v0surf')
    old_file_md5 = _md5_bytes(open(pkl_path, 'rb').read()) if os.path.exists(pkl_path) else None

    mode = '--verify'
    for a in argv[1:]:
        if a in ('--verify', '--bake'): mode = a

    sig, surfaces = _engine_surfaces()
    payload = {sig: surfaces}
    blob = pickle.dumps(payload, protocol=pickle.DEFAULT_PROTOCOL)
    new_md5 = _md5_bytes(blob)
    print("refit_v0surf: shipped-config signature %s | %d age18 pos, surfN %d ages, surfR %d ages | new md5 %s | "
          "committed pin %s" % (sig[:12], len(surfaces['c18']), len(surfaces['surfN']), len(surfaces['surfR']),
                                new_md5, pinned))

    if mode == '--verify':
        same = (new_md5 == pinned)
        print("VERIFY: refit %s the committed pin (%s)." % ("REPRODUCES" if same else "DIVERGES from", pinned))
        print("  (a divergence on a DIFFERENT CPU/BLAS kernel is EXPECTED and is exactly why v0surf is frozen "
              "and loaded, not fitted. It does NOT mean the shipped board is wrong; it means a refit must happen "
              "on a clean instance at a controlled bake, then be re-pinned + re-certified.)")
        return 0 if same else 3

    # --bake
    if os.environ.get('RL_BAKE_V0SURF') != '1':
        raise SystemExit("refit HALT: --bake requires RL_BAKE_V0SURF=1. This gate exists so an ordinary "
                         "build/gate/panel run cannot trigger a refit (silent refit is the defect being fixed). "
                         "Set it ONLY inside a controlled bake, on a CLEAN instance (balanced board == 06d8af60).")
    with open(pkl_path, 'wb') as f: f.write(blob)
    # SURGICAL pin write (the FENCE's "one pin add"): edit ONLY the v0surf line, byte-for-byte preserving the
    # rest of expected_boot.json (indent, \u escapes, key order, no trailing newline) — never a json round-trip,
    # which would reformat the whole file.
    import re as _re
    _s = open(boot_path, 'r', encoding='utf-8').read()
    if '"v0surf"' in _s:
        _s2 = _re.sub(r'"v0surf": "[0-9a-f]{32}"', '"v0surf": "%s"' % new_md5, _s, count=1)
    else:
        _m = _re.search(r'([ \t]*)"q97m": "[0-9a-f]{32}",\n', _s)
        if not _m:
            raise SystemExit("refit HALT: could not locate the q97m pin line to insert v0surf beside it.")
        _s2 = _s[:_m.start()] + _m.group(0) + '%s"v0surf": "%s",\n' % (_m.group(1), new_md5) + _s[_m.end():]
    open(boot_path, 'w', encoding='utf-8').write(_s2)
    prov_path = os.path.join(root, 'session_2026-07-18', 'legf6', 'v0surf_refit_log.json')
    log = []
    if os.path.exists(prov_path):
        try: log = json.load(open(prov_path))
        except Exception: log = []
    log.append({'ts_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'artifact': 'data/v0surf.pkl', 'signature': sig,
                'old_md5': old_file_md5, 'old_pin': pinned, 'new_md5': new_md5,
                'note': 'FREEZE _iso_dec (LEG F6, item 381); computed on a clean instance (balanced board 06d8af60)'})
    with open(prov_path, 'w') as f: json.dump(log, f, indent=2); f.write('\n')
    print("BAKE WRITTEN: data/v0surf.pkl md5 %s -> %s ; re-pinned expected_boot.json 'v0surf' ; provenance -> "
          "session_2026-07-18/legf6/v0surf_refit_log.json" % (old_file_md5, new_md5))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
