#!/usr/bin/env python3
# ship_gates_check.py — scripted PASS/FAIL for the FROZEN acceptance suite (SHIP_GATES.md, frozen ref 764a0d91).
# Run at each candidate head and mandatorily at any bake:  python3 ship_gates_check.py
# Requires the bootstrap layout (/home/claude/...) + pinned env (setup_env.sh). One engine load per process.
# SCRIPTING NOTES honoured: EXACT full-name matching (no substrings; ambiguity -> ERROR, never a silent pick);
# line-ball = +/-20%; A13/A14 staged PENDING until the PVC stage; A6 kernel-smoothed pick-matching with the thin
# RUC slice pooled deliberately (yrs 1-3 together); [DC] tags carried into output for failure triage.
# THRESHOLD REGISTER (updated 2026-07-02, DIRECTIVE 2, Luke's rulings turns 09-10):
#   A6 kernel bw 0.6 on log-pick — RATIFIED (via Luke's delegation to supervisor, 02/07/2026).
#   B1 rule — RE-SCRIPTED per Luke: PASS = pooled cohort value rises from draft to a peak by yr4-5 (yr6
#     acceptable); interim pre-peak dips <5% tolerated (year 2 explicitly named); level need NOT hold in yr6.
#   B6 rule — RE-SCRIPTED per Luke: gate tests the WHOLE 0->6 ramp (<=5g players were dumped into the sit-out
#     stream, so 0g and 5g got identical treatment; flat-then-step IS the violation); value must progress
#     smoothly from the 0-game anchor to the 6-game production value. Monotone-in-evidence clause UNCHANGED.
#     Smoothness thresholds below are DECLARED pending ratification. Prior "seam 10%/3x" shorthand superseded.
#   B5 floor 0.25x draftval — PROVISIONAL this run (year-schedule crater-floor PROPOSAL with Luke to sign:
#     session_2026-07-02/directive2_notes.md). POPULATION CONVENTION (Luke, verbatim intent): ACTIVE/LISTED
#     players only; once inactive, value = 0; in backtests inactive players REMAIN in denominators while
#     contributing 0 to numerators for that year.
#   B2 leakage tol 5.0 %-pts — PROVISIONAL pending the noise-floor spread (Directive 2 Task E; supervisor sets).
import os, sys, io, json, copy, math, time, hashlib, subprocess, contextlib
ROOT = os.path.dirname(os.path.abspath(__file__))
RA = '/home/claude/rl_workspace/rl_after'
os.environ.update(PYTHONHASHSEED='0', RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25',
                  RL_RECENCY_DECAY='0.72', RL_PRIOR_TREES='400', PAR_RAMPS='22')
sys.path[:0] = [RA, '/home/claude/rl_workspace/forward_valuation', os.path.join(ROOT, 'vendor')]
os.environ['PYTHONPATH'] = ':'.join(sys.path[:3])          # subprocesses (B4 export) need it too
os.chdir(RA)
import numpy as np
SKIP = set(os.environ.get('SGC_SKIP', '').upper().split(',')) - {''}
HEAD = hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]
t0 = time.time()
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
ev, MA, cp = G['ev'], G['MA'], G['cp']
GRPPOS, draftval, delisted = G['GRPPOS'], G['draftval'], G['delisted']

# SHIP_GATES shorthand -> exact store ID (pinned; EXACT-name discipline, never substring)
ALIAS = {'Josh Weddle': 'Joshua Weddle', 'Dan Annable': 'Daniel Annable'}

def byname(name):
    name = ALIAS.get(name, name)
    hits = [p for p in MA.data if p['player'] == name and not p.get('_retired')]
    if len(hits) == 1:
        return hits[0], None
    if not hits:
        return None, f'no exact active match for "{name}"'
    return None, f'AMBIGUOUS "{name}": ' + '; '.join(f"pick={h.get('pick')} yr={h.get('year')}" for h in hits)

def E(name, yr=2026):
    p, err = byname(name)
    if err:
        raise LookupError(err)
    with contextlib.redirect_stdout(io.StringIO()):
        return float(ev(p, yr))

RES, NOTES = [], []
def gate(gid, dc, status, detail):
    RES.append((gid, dc, status, detail))

def cmp_gate(gid, dc, pairs, fmt):        # pairs: list of (label, lhs, rhs) requiring lhs > rhs
    try:
        vals = [(lb, E(a), E(b)) for lb, a, b in pairs]
        ok = all(x > y for _, x, y in vals)
        gate(gid, dc, 'PASS' if ok else 'FAIL', '; '.join(fmt.format(lb, x, y) for lb, x, y in vals))
    except LookupError as ex:
        gate(gid, dc, 'ERROR', str(ex))

# ---------- SECTION A ----------
cmp_gate('A1', False, [('Duursma>Uwland', 'Willem Duursma', 'Zeke Uwland')], '{}: {:.0f} vs {:.0f}')
cmp_gate('A2', False, [('Curtis>Ward', 'Paul Curtis', 'Josh Ward'), ('Weddle>Ward', 'Josh Weddle', 'Josh Ward')], '{}: {:.0f} vs {:.0f}')
for gid, nm, frac in [('A3', 'Connor Rozee', 0.80), ('A10', 'Charlie Curnow', 0.70)]:
    try:
        v26, v25 = E(nm, 2026), E(nm, 2025)
        r = v26 / max(v25, 1e-9)
        gate(gid, True, 'PASS' if r >= frac else 'FAIL', f'{nm}: 2026={v26:.0f} 2025={v25:.0f} ratio={r:.2f} (need >={frac:.2f})')
    except LookupError as ex:
        gate(gid, True, 'ERROR', str(ex))
# EV sweep (non-retired) for A4/A6/B5 + board context
EV = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_retired'):
            continue
        try:
            EV[id(p)] = float(ev(p, 2026))
        except Exception:
            EV[id(p)] = None
board = sorted(((v, p) for p in MA.data if not p.get('_retired') and (v := EV.get(id(p))) is not None),
               key=lambda t: -t[0])
try:
    hr, err = byname('Harley Reid')
    if err: raise LookupError(err)
    rank = next(i for i, (_, p) in enumerate(board, 1) if p is hr)
    gate('A4', False, 'PASS' if rank <= 40 else 'FAIL', f'Harley Reid board rank={rank} ev={EV[id(hr)]:.0f} (need TOP 40)')
except LookupError as ex:
    gate('A4', False, 'ERROR', str(ex))
try:
    a5 = [('Jack Ginnivan', 1600), ('Jake Bowey', 2100), ('Nick Blakey', 2600)]
    vals = [(nm, E(nm), fl) for nm, fl in a5]
    gate('A5', False, 'PASS' if all(v > fl for _, v, fl in vals) else 'FAIL',
         '; '.join(f'{nm}={v:.0f} (floor {fl})' for nm, v, fl in vals) + ' [SCAR floors — RE-BASE if PVC re-levels]')
except LookupError as ex:
    gate('A5', False, 'ERROR', str(ex))
# A6 — yrs 1-3 (drafted 2023-2025, pooled deliberately: thin RUC slice), kernel-smoothed pick-matched MID medians
def cohort(grp):
    out = []
    for p in MA.data:
        if p.get('_retired') or p.get('_pickless') or EV.get(id(p)) is None:
            continue
        if MA.gfut(p) == grp and (2026 - int(p.get('year') or 0)) in (1, 2, 3):
            out.append((math.log(float(MA.effpk(p))), EV[id(p)]))
    return out
rucs, mids = cohort('RUC'), cohort('MID')
if len(rucs) >= 3 and len(mids) >= 10:
    mx = np.array([x for x, _ in mids]); mv = np.array([v for _, v in mids])
    def ksm(x, bw=0.6):
        w = np.exp(-0.5 * ((mx - x) / bw) ** 2)
        return float(np.dot(w, mv) / w.sum())
    med_ruc = float(np.median([v for _, v in rucs]))
    med_mid = float(np.median([ksm(x) for x, _ in rucs]))
    gate('A6', False, 'PASS' if med_ruc <= med_mid else 'FAIL',
         f'yr1-3 RUC median={med_ruc:.0f} (n={len(rucs)}, pooled — thin slice) vs pick-matched MID kernel median={med_mid:.0f} (n={len(mids)}, bw=0.6 log-pick, RATIFIED 02/07)')
else:
    gate('A6', False, 'ERROR', f'thin cohorts: RUC n={len(rucs)} MID n={len(mids)}')
# A7 — position poles hold
try:
    ok, det = True, []
    for nm, dom, grp in [('Ryan Maric', 'MID', 'MID'), ('Ed Langdon', 'GDEF', 'GEN_DEF')]:
        p, err = byname(nm)
        if err: raise LookupError(err)
        fut = sorted(p.get('_fut') or [], key=lambda t: -t[1])
        lab = fut[0][0] if fut else None
        g_ = MA.gfut(p)
        ok &= (lab == dom and g_ == grp)
        det.append(f'{nm}: fut-dominant={lab}({fut[0][1] if fut else 0:.0f}%) gfut={g_} (need {dom}/{grp})')
    gate('A7', False, 'PASS' if ok else 'FAIL', '; '.join(det))
except LookupError as ex:
    gate('A7', False, 'ERROR', str(ex))
try:
    b, t = E('Sam Berry'), E('Elijah Tsatas')
    gate('A8', True, 'PASS' if b > 2 * t else 'FAIL', f'Berry={b:.0f} vs 2x Tsatas={2*t:.0f} (Tsatas={t:.0f})')
except LookupError as ex:
    gate('A8', True, 'ERROR', str(ex))
cmp_gate('A9', False, [('Ginnivan>Ward', 'Jack Ginnivan', 'Josh Ward')], '{}: {:.0f} vs {:.0f}')
cmp_gate('A11', True, [('Farrow>Patterson', 'Jacob Farrow', 'Dylan Patterson'), ('Cumming>Annable', 'Sam Cumming', 'Dan Annable')], '{}: {:.0f} vs {:.0f}')
cmp_gate('A12', True, [('Travaglia>Moraes', 'Tobie Travaglia', 'Christian Moraes'), ('Smillie>Retschko', 'Josh Smillie', 'Patrick Retschko')], '{}: {:.0f} vs {:.0f}')
# A13/A14 — PVC-coupled: staged PENDING (advisory numbers vs the CURRENT stand-in PVC, not the future curve)
def lineball(v, ref):
    return abs(v - ref) <= 0.20 * ref
try:
    pk1, pk8 = float(MA.PVC[1]), float(MA.PVC[8])
    a13 = [(nm, E(nm)) for nm in ('George Wardlaw', 'Levi Ashcroft')]
    a14 = [(nm, E(nm)) for nm in ('Trent Rivers', 'Zach Reid', 'Jase Burgoyne')]
    gate('A13', False, 'PENDING', f'PVC stage not run; advisory vs stand-in PVC[1]={pk1:.0f}: ' + '; '.join(f'{nm}={v:.0f} lineball={lineball(v,pk1)}' for nm, v in a13))
    gate('A14', False, 'PENDING', f'PVC stage not run; advisory vs stand-in PVC[8]={pk8:.0f}: ' + '; '.join(f'{nm}={v:.0f} lineball={lineball(v,pk8)}' for nm, v in a14))
except LookupError as ex:
    gate('A13', False, 'ERROR', str(ex)); gate('A14', False, 'ERROR', str(ex))
gate('A15', False, 'STRUCK', 'Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1')
# ---------- SECTION B ----------
# B1 — cohort growth law from the walk-forward matrix (SUM-RATIO, yr1=100, busts=0; cohorts 2004-2020, incurve only)
# RE-SCRIPTED (Luke 02/07, turns 09-10): PASS = POOLED value rises from draft to a peak by yr4-5 (yr6 acceptable);
# interim pre-peak dips <5% are tolerated (year 2 explicitly named); the level need NOT still hold in yr6.
# Per-cohort rise-to-yr4-6-above-yr1 kept as the backstop condition (17/17 at re-script).
try:
    mpath = os.environ.get('S4_MATRIX', os.path.join(ROOT, 'data', 's4_matrix_nogames.json'))
    mat = json.load(open(mpath))
    S = {}
    for v in mat.values():
        C = int(v['year'])
        if not v['incurve'] or not (2004 <= C <= 2020):
            continue
        for i, _yy in enumerate(v['yrs']):
            N = i + 1
            if N > 7:
                break
            S[(C, N)] = S.get((C, N), 0.0) + float(v['Vpath'][i] or 0.0)
    rises, peaks, tbl = [], [], []
    for C in sorted({c for c, _ in S}):
        R = {N: 100.0 * S[(C, N)] / max(S[(C, 1)], 1e-9) for N in range(1, 8) if (C, N) in S}
        pkN = max(R, key=R.get)
        rises.append(max(R.get(N, 0) for N in (4, 5, 6)) > 100.0)
        peaks.append(pkN)
        tbl.append(f'  cohort {C}: peakN={pkN} R={{{", ".join(f"{N}:{R[N]:.0f}" for N in sorted(R))}}}')
    pooled = {N: 100.0 * sum(S.get((C, N), 0.0) for C in set(c for c, _ in S)) /
                 max(sum(S.get((C, 1), 0.0) for C in set(c for c, _ in S)), 1e-9) for N in range(1, 8)}
    ppk = max(pooled, key=pooled.get)
    path_ok = all(pooled[N + 1] >= 0.95 * pooled[N] for N in range(1, ppk) if N + 1 in pooled)
    ok = all(rises) and ppk in (4, 5, 6) and pooled[ppk] > 100.0 and path_ok
    gate('B1', False, 'PASS' if ok else 'FAIL',
         f'pooled peak N={ppk} R(peak)={pooled[ppk]:.0f} (need peak by yr4-5, yr6 acceptable, >100; pre-peak dips <5% tolerated, path_ok={path_ok}; no yr6-hold required — Luke 02/07); cohorts rising to yr4-6 above yr1: {sum(rises)}/{len(rises)}; matrix={os.path.basename(mpath)}')
    NOTES.append('B1 per-cohort table:\n' + '\n'.join(tbl))
except Exception as ex:
    gate('B1', False, 'ERROR', f'{type(ex).__name__}: {ex}')
# B2 — GATE-1 leakage + separation, parsed from the harness output (_gate1_wf.py run this session)
try:
    g1p = '/home/claude/gate1_out.txt'
    if 'B2' in SKIP or not os.path.exists(g1p):
        gate('B2', False, 'NOT-RUN', 'run _gate1_wf.py first (writes /home/claude/gate1_out.txt)')
    else:
        import re
        rows, cur = {}, None
        for ln in open(g1p):
            ls = ln.strip()
            if ls.startswith(('MID', 'GEN_', 'KEY_')) and 'WF[' in ls:
                pos, tag = ls.split()[0], ls.split()[1]
                cur = (pos, tag)
                rows[cur] = {'WF': [float(x) for x in re.findall(r'T\d+:\s*(-?\d+)', ls.split('WF[')[1])]}
            elif ls.startswith('IS[') and cur:
                rows[cur]['IS'] = [float(x) for x in ls[3:ls.index(']')].split()]
        gaps = [abs(i - w) for r in rows.values() if 'IS' in r for w, i in zip(r['WF'], r['IS'])]
        leak = float(np.median(gaps)) if gaps else float('nan')
        seps = {pos: (np.median(rows[(pos, 'GOOD')]['WF']), np.median(rows[(pos, 'BUST')]['WF']))
                for pos in {p for p, _ in rows} if (pos, 'GOOD') in rows and (pos, 'BUST') in rows}
        sep_ok = all(g_ > b_ for g_, b_ in seps.values()) and bool(seps)
        ok = sep_ok and leak <= 5.0
        gate('B2', False, 'PASS' if ok else 'FAIL',
             f'median |IS-WF| leakage={leak:.1f} %-pts (DECLARED tol 5.0); GOOD>BUST separation: ' +
             ', '.join(f'{p} {g_:.0f}/{b_:.0f}' for p, (g_, b_) in sorted(seps.items())))
except Exception as ex:
    gate('B2', False, 'ERROR', f'{type(ex).__name__}: {ex}')
gate('B3', False, 'PENDING', 'book-gate set not yet enumerated as scripted checks — definition proposal in report; book headline shape covered by B1')
# B4 — board parity: regenerate rl_app_data.json (subprocess: one-engine-load rule) and byte-compare to shipped
try:
    if 'B4' in SKIP:
        gate('B4', False, 'NOT-RUN', 'SGC_SKIP=B4')
    else:
        shipped = '/home/claude/rl_build/rl_app_data.json'
        prev = os.path.join(RA, 'rl_app_data.json')
        bak = prev + '.sgc_bak'
        if os.path.exists(prev):
            os.replace(prev, bak)
        r = subprocess.run([sys.executable, 'rl_export.py'], cwd=RA, capture_output=True, text=True, timeout=1800)
        m_new = hashlib.md5(open(prev, 'rb').read()).hexdigest()[:8] if os.path.exists(prev) else 'MISSING'
        m_ship = hashlib.md5(open(shipped, 'rb').read()).hexdigest()[:8]
        if os.path.exists(prev):
            os.remove(prev)
        if os.path.exists(bak):
            os.replace(bak, prev)
        gate('B4', False, 'PASS' if m_new == m_ship else 'FAIL',
             f'regenerated rl_app_data.json md5={m_new} vs shipped {m_ship} (byte-agree gate; export exit={r.returncode})')
except Exception as ex:
    gate('B4', False, 'ERROR', f'{type(ex).__name__}: {ex}')
# B5 — no-crater guard (0.25x floor = DECLARED proxy, PROVISIONAL this run; year-schedule replacement PROPOSED
# in session_2026-07-02/directive2_notes.md — Luke signs). POPULATION CONVENTION (Luke 02/07, verbatim intent):
# ACTIVE/LISTED players only; once inactive, value = 0, and in backtests inactive players REMAIN in denominators
# while contributing 0 to numerators for that year.
try:
    off = []
    for p in MA.data:
        if p.get('_retired') or p.get('_pickless') or delisted(p) or int(p.get('year') or 0) not in (2024, 2025):
            continue
        v = EV.get(id(p))
        if v is None:
            continue
        dv = draftval(p)
        if v < 0.25 * dv:
            off.append((p['player'], v, dv))
    gate('B5', False, 'PASS' if not off else 'FAIL',
         f'{len(off)} yr1-2 LISTED picked players below 0.25x draftval (floor PROVISIONAL; listed-only per Luke 02/07); worst: ' +
         ('; '.join(f'{n}={v:.0f}/dv{d:.0f}' for n, v, d in sorted(off, key=lambda t: t[1] / t[2])[:3]) if off else 'none'))
except Exception as ex:
    gate('B5', False, 'ERROR', f'{type(ex).__name__}: {ex}')
# B6 — games-ramp continuity, RE-SCRIPTED (Luke 02/07, turns 09-10): the gate tests the WHOLE 0->6 ramp.
# <=5g players were dumped into the sit-out stream, so 0g and 5g got identical treatment; flat-then-step IS the
# violation. Value must progress smoothly from the 0-game anchor (empty scoring -> sit-out dv*retain path) to the
# 6-game production value. Monotone-in-evidence clause UNCHANGED (covers the 9->10g dip separately).
# DECLARED smoothness thresholds pending ratification: no single 0->6 step > 50% of the total 0->6 rise T,
# AND cumulative rise by 3g >= 25% of T (anti-flat-start). Prior "seam 10%/3x" shorthand superseded.
try:
    def ramp_p(gm):
        return {'player': 'b6-synth', 'pos': GRPPOS.get('MID'), 'pick': 10.0, 'year': 2025, 'dob': '2006-03-01',
                'type': 'ND', 'scoring': ([{'year': 2026, 'games': gm, 'avg': 85.0}] if gm > 0 else []),
                '_pos_now': None, '_fut': []}
    with contextlib.redirect_stdout(io.StringIO()):
        vals = [float(ev(ramp_p(gm), 2026)) for gm in range(0, 15)]
    steps = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    dips = [(i, s) for i, s in enumerate(steps) if s < -1.0]          # label = start game of the step
    T = vals[6] - vals[0]
    big = [(i, round(s)) for i, s in enumerate(steps[:6]) if s > 0.50 * max(T, 1.0)]
    rise3 = vals[3] - vals[0]
    smooth_bad = (T <= 0) or big or (rise3 < 0.25 * T)
    gate('B6', False, 'PASS' if not dips and not smooth_bad else 'FAIL',
         f'ramp(0..14g)={[round(v) for v in vals]}; dips(more games worth less)={dips or "none"}; '
         f'0->6 rise T={T:+.0f}; 0->6 steps>50%T={big or "none"}; rise by 3g={rise3:+.0f} (need >={0.25*T:.0f}) '
         f'[whole-ramp re-spec, DECLARED thresholds]')
except Exception as ex:
    gate('B6', False, 'ERROR', f'{type(ex).__name__}: {ex}')
# ---------- SECTION C ----------
gate('C1', False, 'PENDING', 'naive-baseline book not yet built — definition proposal in report (needs its own directive)')
gate('C2', False, 'PENDING', 'V1-pick-model book not yet built — definition proposal in report (needs its own directive)')

# ---------- BOARD + REPORT ----------
order = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15',
         'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'C1', 'C2']
RES.sort(key=lambda r: order.index(r[0]))
cnt = {}
lines = [f'=== SHIP GATES BOARD — head {HEAD} store {STORE} — suite 764a0d91 — {time.strftime("%Y-%m-%d")} ===']
for gid, dc, st, det in RES:
    cnt[st] = cnt.get(st, 0) + 1
    tag = ' [DC]' if dc else ''
    lines.append(f'{gid:4s}{tag:5s} {st:8s} {det}')
    if dc and st == 'FAIL':
        lines.append(f'{"":9s} triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)')
summary = 'VERDICT: ' + '  '.join(f'{k}={v}' for k, v in sorted(cnt.items())) + f'  ({time.time()-t0:.0f}s)'
lines.append(summary)
print('\n'.join(lines))
rep = os.path.join(ROOT, 'session_2026-07-02', f'ship_gates_report_{HEAD}.md')
os.makedirs(os.path.dirname(rep), exist_ok=True)
with open(rep, 'w') as f:
    f.write('# ship_gates_check report — head ' + HEAD + ' store ' + STORE + '\n```\n' + '\n'.join(lines) + '\n```\n')
    f.write('\n## Supporting detail\n')
    for n in NOTES:
        f.write('\n' + n + '\n')
    f.write('\n## Board top-50 (A4 context)\n')
    for i, (v, p) in enumerate(board[:50], 1):
        f.write(f'{i:3d}. {p["player"]:24s} {MA.gfut(p):8s} {v:7.0f}\n')
    f.write('\n## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)\n'
            'Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:\n'
            '(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;\n'
            '(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.\n'
            'Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,\n'
            'leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);\n'
            '(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.\n')
print(f'report: {rep}  md5={hashlib.md5(open(rep,"rb").read()).hexdigest()[:8]}')
sys.exit(1 if any(st in ('FAIL', 'ERROR') for _, _, st, _ in RES) else 0)
