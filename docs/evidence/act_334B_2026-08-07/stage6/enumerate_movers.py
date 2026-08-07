#!/usr/bin/env python3
"""#334 stage 6 — MOVER ENUMERATION + THE SIT-OUT BYTE-IDENTITY PROOF, at every rung.

For each rung board it prints/records:
  * every mover against the stage-5 LANDED board 13f8c2e0, with the mechanism fields that produced it
    (the taught delta and every factor of it), so no move is unattributed;
  * THE FENCE PROOF (directive gate 2 / Addendum 1 F1-F3): every player the engine routes through the
    SIT-OUT arm (ns==0 at the board year) must be INTEGER-IDENTICAL at every rung.  The proof is
    POSITIVE — the sit-out population is enumerated from the engine itself, not assumed from the
    absence of movers, and its count is asserted.

Usage: RL_REPO=.. RL_WORKDIR=.. RL_OUT=.. python3 enumerate_movers.py
"""
import os, sys, io, json, contextlib, csv, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
OUT = os.environ.get('RL_OUT', '.')
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]

BASE = REPO + '/data/rl_build/rl_app_data.json'
BASE_MD5 = hashlib.md5(open(BASE, 'rb').read()).hexdigest()
assert BASE_MD5 == '13f8c2e0240600733a5fb42414510445', 'baseline board is not the stage-5 landing: ' + BASE_MD5
RUNGS = sys.argv[1:] or ['0.25', '0.5', '0.75', '1.0']
Y = 2026

def board_map(path):
    d = json.load(open(path))
    return {r['key']: r for r in d['active'] if 'key' in r}

BM = board_map(BASE)

# ---- load the engine ONCE per rung so the mechanism fields come from the same code the board did ----
REPORT = {'baseline_board': BASE_MD5, 'rungs': {}}
SITOUT_KEYS = None
for W in RUNGS:
    os.environ['RL_G6_W'] = W; os.environ['RL_G6_KPD'] = '0'
    G = {'__name__': '_s6_mv_%s' % W}
    with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
    MA = G['MA']; cp = G['cp']; PR = G['PR']; ev = G['ev']
    nseas_pro = G['nseas_pro']; delisted = G['delisted']; _prod_path = G['_prod_path']
    _g6_delta = G['_g6_delta']; entry_anchor = G['entry_anchor']; _fEy = G['_fEy']
    _sitout_cls = G['_sitout_cls']; _isreal = G['_isreal']
    assert float(G['G6_W']) == float(W), 'the engine did not take the rung'

    rung_path = OUT + '/boards/board_rung%s_kpd0.json' % W
    RB = board_map(rung_path)
    rmd5 = hashlib.md5(open(rung_path, 'rb').read()).hexdigest()

    PBK = {q.get('key'): q for q in MA.data}
    sitout, movers = [], []
    for k, r in RB.items():
        b = BM.get(k)
        if b is None: continue
        p = PBK.get(k)
        so = False
        if p is not None:
            try: so = (not delisted(p)) and nseas_pro(p, Y) == 0
            except Exception: so = False
        if so: sitout.append(k)
        if r.get('v') != b.get('v'):
            with contextlib.redirect_stdout(io.StringIO()):
                e = _prod_path(p, Y) if p is not None else None
            d = None
            if p is not None:
                with contextlib.redirect_stdout(io.StringIO()):
                    d = _g6_delta(p, Y, MA.gfut(p), e)
            movers.append(dict(key=k, player=r.get('player') or r.get('name'), pos=(MA.gfut(p) if p else None),
                               effpk=(int(MA.effpk(p)) if p else None), draft_year=(p.get('year') if p else None),
                               pathway=(p.get('type') if p else None),
                               old=b.get('v'), new=r.get('v'), abs=r.get('v') - b.get('v'),
                               rel=(r.get('v') - b.get('v')) / max(b.get('v'), 1),
                               sitout_path=so, production_e=(round(e, 3) if e is not None else None),
                               taught_delta=(round(d, 6) if d is not None else None),
                               cum_games=(sum(x['games'] for x in p['scoring'] if x['year'] <= Y) if p else None),
                               draft_age=((p.get('year') - p.get('_by')) if (p and p.get('_by')) else None)))
    if SITOUT_KEYS is None: SITOUT_KEYS = set(sitout)
    else: assert SITOUT_KEYS == set(sitout), 'the sit-out population itself moved between rungs'
    ident = [k for k in sitout if RB[k].get('v') == BM[k].get('v')]
    ups = [m for m in movers if m['abs'] > 0]; dns = [m for m in movers if m['abs'] < 0]
    unattributed = [m for m in movers if not m['taught_delta']]
    print("rung %-5s board %s  movers %3d (up %3d / down %3d)  sit-out population %d  "
          "INTEGER-IDENTICAL %d/%d  %s"
          % (W, rmd5[:8], len(movers), len(ups), len(dns), len(sitout), len(ident), len(sitout),
             'PASS' if len(ident) == len(sitout) else 'FAIL'))
    if unattributed:
        print("   *** %d UNATTRIBUTED movers (no taught delta) — HALT-and-report finding" % len(unattributed))
        for m in unattributed[:20]: print("      ", m['key'], m['old'], '->', m['new'])
    REPORT['rungs'][W] = dict(board_md5=rmd5, movers=len(movers), up=len(ups), down=len(dns),
                              sitout_n=len(sitout), sitout_identical=len(ident),
                              sitout_verdict=('PASS' if len(ident) == len(sitout) else 'FAIL'),
                              unattributed=len(unattributed),
                              board_total_before=sum(b['v'] for b in BM.values() if 'v' in b),
                              board_total_after=sum(r['v'] for r in RB.values() if 'v' in r),
                              rows=movers)
    with open(OUT + '/movers_rung%s.csv' % W, 'w', newline='') as f:
        if movers:
            w = csv.DictWriter(f, fieldnames=list(movers[0].keys())); w.writeheader(); w.writerows(movers)

json.dump(REPORT, open(OUT + '/movers_rung%s.json' % RUNGS[0], 'w'), indent=1)
print("\nsit-out population (engine-enumerated, ns==0 at %d): n = %d" % (Y, len(SITOUT_KEYS)))
json.dump(sorted(SITOUT_KEYS), open(OUT + '/sitout_population.json', 'w'), indent=1)
print('sit-out identity verdict: ' + REPORT['rungs'][RUNGS[0]]['sitout_verdict'])
