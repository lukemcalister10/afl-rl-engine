#!/usr/bin/env python3
"""ORDER D8 — F2 (the ladder must not fire) and F4 (ceiling v-inversions), measured on the engine.

READ-ONLY. Stages the engine into a throwaway dir exactly as the accepted FV builder does
(test_fv_provenance._staging), loads it there, and writes NOTHING under the repo. The staging tree is
deleted on exit.

  D8REPO   worktree root
  D8TAPER  '1' -> RL_O33_TAPEROFF=1 (the priced posture); anything else -> the dial UNSET (the base)
  D8OUT    output JSON path

A v-INVERSION is band[5] < band[4] — the ceiling below the band beneath it. `_b6_core` returns
band[5] = max(pred, b[4]) >= b[4], so a PRE-taper inversion is impossible and every inversion on the
live board is the v7 age-taper's (PREREG_W6.md §C2; PACKET_W6.md).
"""
import os, sys, io, json, time, shutil, importlib.util, contextlib

REPO   = os.path.abspath(os.environ['D8REPO'])
TAPER  = os.environ.get('D8TAPER', '0') == '1'
OUT    = os.environ['D8OUT']
os.environ.pop('RL_BUILD_LOCK_HELD', None)

# ---- stage, exactly as the accepted builder stages -------------------------------------------------
spec = importlib.util.spec_from_file_location(
    'fvb_d8b', os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'test_fv_provenance.py'))
fvb = importlib.util.module_from_spec(spec); sys.modules['fvb_d8b'] = fvb; spec.loader.exec_module(fvb)
assert os.path.abspath(fvb.REPO) == REPO, 'builder resolved REPO %s != %s' % (fvb.REPO, REPO)
BASE, WS = fvb._staging()
fvb._seed_pkls()
try:
    # ---- the build's own dev-shell environment (mirrors _run_build, balanced=False, config_mode=None)
    for k in ('RL_PVC2', 'RL_LEGE', 'RL_LEGF', 'RL_V0SURF_REFIT', 'RL_CONFIG_MODE'):
        os.environ.pop(k, None)
    os.environ['RL_REPO'] = REPO
    os.environ['PYTHONHASHSEED'] = '0'
    for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS'):
        os.environ[k] = '1'
    os.environ['RL_PRIOR_TREES'] = '400'
    os.environ['RL_FV'] = os.path.join(REPO, 'engine', 'forward_valuation')
    if TAPER:
        os.environ['RL_O33_TAPEROFF'] = '1'
    else:
        os.environ.pop('RL_O33_TAPEROFF', None)
    sys.path[:0] = [WS, REPO, os.path.join(REPO, 'vendor'), os.path.join('/home/claude', 'rl_vendor')]
    cwd = os.getcwd(); os.chdir(WS)
    NSE = {}
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()) as _so:
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
    load_stdout = _so.getvalue()
    os.chdir(cwd)

    MA = NSE['MA']; g = MA.__dict__
    b6 = NSE['b6']
    g['BASE_REF'] = g['AGE_REF'] = 2026; g['_pe_clear']()      # pin the clock to the present (mirrors rl_export)
    players = g['players']; age = g['age']; gfut = g['gfut']; PEAK_AGE = g['PEAK_AGE']

    res = {'taper_dial': bool(TAPER), 'load_s': round(time.time() - t0, 1),
           'flags': {'_O33': bool(MA._O33), '_O33S': int(MA._O33S),
                     '_O33_TAPEROFF': bool(NSE['_O33_TAPEROFF']),
                     'RL_O33_env': os.environ.get('RL_O33'),
                     'RL_O33_STAGE_env': os.environ.get('RL_O33_STAGE'),
                     'RL_O33_TAPEROFF_env': os.environ.get('RL_O33_TAPEROFF')}}

    # ---- F2 (a+b): the B-1 ladder is unreachable, tested over the ENTIRE reachable frac() domain ----
    # frac(a,pa,g) clamps j = round(a-pa) into [-8,14]; the ladder branch can only fire for j>0 and
    # g in {KPD,KPF}. Compare against the shared DELTAS path at every j, for every position label.
    frac = MA.frac; DELTAS = MA.DELTAS
    dom = []
    for gg in ('KPD', 'KPF', 'MID', 'SD', 'SF', 'RUCK', None):
        for j in range(-8, 15):
            got = frac(27.0 + j, 27.0, gg) if gg is not None else frac(27.0 + j, 27.0)
            dom.append({'g': gg, 'j': j, 'frac': got, 'deltas': DELTAS[j], 'same': got == DELTAS[j]})
    res['frac_domain_rows'] = len(dom)
    res['frac_domain_divergences'] = [d for d in dom if not d['same']]

    # per-row, at the board's own ages and at the +1/+2 projection horizons
    rowdiv = []; rowchk = 0
    for p in players:
        gg = gfut(p); pa = PEAK_AGE.get(gg)
        if gg not in ('KPD', 'KPF') or pa is None:
            continue
        a0 = age(p)
        if a0 is None:
            continue
        for k in range(0, 15):                       # every horizon the projection stream can reach
            ah = a0 + k
            j = max(-8, min(14, int(round(ah - pa))))
            if j <= 0:
                continue
            rowchk += 1
            got = frac(ah, pa, gg)
            if got != DELTAS[j]:
                rowdiv.append({'key': p['key'], 'g': gg, 'ah': ah, 'j': j,
                               'frac': got, 'deltas': DELTAS[j]})
    res['frac_row_checks'] = rowchk
    res['frac_row_divergences'] = rowdiv

    # ---- F4: the ceiling bands, per active row ------------------------------------------------------
    rows = []
    for p in players:
        bb = b6(p, 2026)
        rows.append({'key': p['key'], 'name': p['player'], 'age': age(p), 'pos': gfut(p),
                     'b4': float(bb[4]), 'b5': float(bb[5]), 'nb': len(bb)})
    res['n_rows'] = len(rows)
    inv = [r for r in rows if r['b5'] < r['b4']]
    res['inversions'] = len(inv)
    res['inversion_rows'] = sorted(inv, key=lambda r: r['b5'] - r['b4'])
    res['rows'] = rows
    res['uncomp_cal'] = [l for l in load_stdout.splitlines()
                         if 'RL_UNCOMP' in l or 'V_ref_b=' in l]

    with open(OUT, 'w') as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print('D8 BANDS taper=%s rows=%d inversions=%d frac_domain_div=%d frac_row_div=%d (%.0fs)'
          % (TAPER, res['n_rows'], res['inversions'], len(res['frac_domain_divergences']),
             len(res['frac_row_divergences']), res['load_s']))
    for l in res['uncomp_cal']:
        print('   ' + l)
finally:
    shutil.rmtree(BASE, ignore_errors=True)
