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
#   B2 leakage tol 0.5 %-pts — SET 02/07/2026 (supervisor ruling under Luke's delegation; measured N=5 spread
#     = 0.00 %-pts, so any gap >=0.5 is signal; rationale in CHANGELOG). Supersedes the provisional 5.0.
#   A2 AMENDED 02/07/2026 (Luke, in writing): Curtis leg = Curtis >= 0.90 x Ward (verbatim reason in CHANGELOG).
#   D4 AUDIT 02/07/2026 (full gate-line audit vs frozen 764a0d91 + logged amendments — session_2026-07-02/
#     d4_instrument_audit.md): A8 expression confirmed the literal 2x test (Berry=3473, Tsatas=1083 — both
#     reported passes GENUINE); defect was DISPLAY AMBIGUITY ("vs 2x Tsatas=2166" read as raw Tsatas) —
#     detail string de-ambiguated + comparison > -> >= per frozen "at least 2x". No missing-2x, no tolerance leak.
#   A10 AMENDED 02/07/2026 (Luke, in writing, D4): threshold 0.70 -> 0.50, DATA-CAUSED (Curnow has banked 13
#     games of 2026 — his level is 2026 form, not an engine artifact), PROVISIONAL + review at season-complete.
#   A3 ANNOTATED 02/07/2026 (Luke, D4): evaluated PRE-LTI-layer (the pre-LTI engine ratio is what A3 tests;
#     the future LTI overlay must not be the thing that passes it).
#   B5 YEAR-SCHEDULE SIGNED 02/07/2026 (Luke, in writing, D4): floors by years-in-system replace the 0.25x
#     proxy — see the B5 block for constants, population, and the generating rule.
#   B1 REDEFINED 02/07/2026 (Luke, in writing, confirmed, D5): the gate tests the CROSS-COHORT UNWEIGHTED
#     AVERAGE of indexed cohort value at each year-depth (rise from yr1 to a peak in yrs 4-6; <5% pre-peak
#     dips of the average tolerated). Per-cohort curves UNGATED by design but printed as a pipe table on
#     every gates-board run. The old per-cohort rise backstop is RETIRED — obituary in CHANGELOG (D5).
#   A3 AMENDED 02/07/2026 (Luke, in writing, D7): threshold 0.80 -> 0.75, DATA-CAUSED — Rozee out for the
#     remainder of 2026 (LTI register Section B); Luke verbatim: "Happy to adjust Rozee to 75%". The bar
#     deliberately sits at reality's edge (same design as A10/Curnow).
#   A2 UNCHANGED at 0.90 by ruling (Luke, D7): ships red at the v2 config (Curtis 0.822 measured at
#     candidate-minus-cB); Luke verbatim: "we can look at Curtis down the line".
#   B5 AMENDED 02/07/2026 (Luke-ruled; text prepared D6, committed D7): retired as a pass/fail ALARM;
#     replaced by the floor-as-pricing-feature at the ev() boundary (flat .05 yrs-7+ tail, VARIANT A as
#     signed) + the MANDATORY FLOOR-SAVES table printed on every board run (the new alarm surface) + the
#     pure-lower-bound re-verify (0 lowered, 0 non-ND moved). At heads that do not carry the floor feature
#     (canonical pre-v2), the line reports the legacy offender count INFORMATIONALLY — never FAIL.
import os, sys, io, json, copy, math, time, hashlib, subprocess, contextlib
ROOT = os.path.dirname(os.path.abspath(__file__))
RA = '/home/claude/rl_workspace/rl_after'
# GUARD 5 (boot-store) — PRE-FLIGHT, before the engine loads. The frozen acceptance suite must never run
# against a store the caller has not verified is the checked-out, pinned one. The four data guards validate
# whichever dir they are imported from (RA here, the workspace), so a stale-but-self-consistent workspace
# passes them silently — this closes that hole by asserting RA's store+head == data/expected_boot.json ==
# the repo checkout, and HALTS otherwise. This is a pre-flight ADDITION only: no gate's assertion, threshold,
# or value is touched; on the correct store the board is byte-identical to before. (Stale-boot hardening
# 2026-07-05.) OWNER RULING 2026-07-05 (Luke, in writing): "the Guard 5 pre-flight is a safety addition,
# not a frozen-gate amendment; apply and keep it." — recorded per the A7 precedent; the frozen suite 764a0d91
# is unamended. This pre-flight does not alter gate behaviour on the pinned store; it only refuses to run on
# any other store.
sys.path.insert(0, ROOT)
import boot_guard as _bg
_bg.assert_boot('ship_gates_check', store_path=os.path.join(RA, 'rl_model_data.json'),
                engine_head_path=os.path.join(RA, '_merged_recover.py'))
os.environ.update(PYTHONHASHSEED='0', RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25',
                  RL_RECENCY_DECAY='0.72', RL_PRIOR_TREES='400', PAR_RAMPS='22')
# GATE-INTEGRITY (e): the frozen suite is a GATE — pin the model configuration to the versioned manifest
# (data/model_config.json) BEFORE the engine loads. enforce('gate') clears the ambient model env, REJECTS any
# unknown/divergent RL_*/PAR_* override (the config-drift hole that let the held-out PVC fit ride into a board),
# loads the manifest (values == code defaults ⇒ board/gates byte-identical), and returns the canonical config
# hash stamped into the gate report so every verdict names WHICH config it certifies. Halts (not warns) on drift.
import config_manifest as _CFG
CONFIG_HASH = _CFG.enforce('gate')
sys.path[:0] = [RA, '/home/claude/rl_workspace/forward_valuation', os.path.join(ROOT, 'vendor')]
os.environ['PYTHONPATH'] = ':'.join(sys.path[:3])          # subprocesses (B4 export) need it too
os.chdir(RA)
import numpy as np
SKIP = set(os.environ.get('SGC_SKIP', '').upper().split(',')) - {''}
# ---- rev143 HYGIENE RIDER (Leg A 2026-07-16; items 149/151/169) — SGC_* env-LEAKAGE tripwire ----
# SGC_* are ship_gates RED-PATH PROOF inputs (SGC_SKIP / SGC_B1_MATRIX / SGC_REPORT_DIR). An SGC_* inherited
# from an orchestrator's environment silently redirected the report auto-write and tripped three builds. Two
# one-shot fixes: (1) REJECT any UNRECOGNIZED SGC_* here (unhandled leakage HALTs — halt-not-warn); (2) the
# report write is pinned IN-FENCE below (a leaked/foreign SGC_REPORT_DIR can never write outside the checkout).
# No gate assertion, threshold or verdict is touched (SHIP_GATES §RED-PATH; the frozen suite 764a0d91 unamended).
_SGC_OK = {'SGC_SKIP', 'SGC_B1_MATRIX', 'SGC_REPORT_DIR'}
_sgc_leak = sorted(k for k in os.environ if k.startswith('SGC_') and k not in _SGC_OK)
if _sgc_leak:
    sys.exit('!! SHIP-GATES SGC LEAKAGE (rev143 rider): unrecognized SGC_* env %s — not ship_gates red-path '
             'inputs; unset them (they must never leak in from a build orchestrator).' % _sgc_leak)
def _subenv(**kw):
    """rev143 rider (the actual three-build tripwire, items 149/151/169): the GATE-MODE regeneration
    subprocesses (B1/B3 matrix, B4 export, gate1) must NOT inherit ship_gates' own SGC_* red-path inputs.
    A leaked SGC_* into a gate-mode child (RL_CONFIG_MODE=gate set below) is rejected by config_manifest's
    gate-seam scan and the child HALTs (exit 1) — the exact failure that tripped three builds. Strip every
    SGC_* from the child env; ship_gates' SGC_* stay local to this process (report dir, B1 injection, skips)."""
    e = {k: v for k, v in os.environ.items() if not k.startswith('SGC_')}
    e.update(kw); return e
HEAD = hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]
# ---- BINDING REPORTING RULES (Luke's word, D10 03/07/2026 — see BAKE_CHECKLIST.md §REPORTING) ----
# 5a: every gates/board output reports THREE COLUMNS — CONTROL / PREVIOUS / CURRENT, deltas explicit.
# 5b: every board/report carries a LOUD state label; no unlabelled player value anywhere Luke-facing.
try:
    _REG = json.load(open(os.path.join(ROOT, 'data', 'report_states.json')))
except Exception:
    _REG = {'states': {}}
STATE_LABEL = _REG.get('states', {}).get(HEAD, f'PROTOTYPE/UNREGISTERED @ {HEAD} — NOT AN ENDORSED STATE')
def _load_snap(key):
    try:
        return json.load(open(os.path.join(ROOT, _REG[key]['gates'])))
    except Exception:
        return {'head': '????????', 'gates': {}}
SNAP_CTL, SNAP_PREV = _load_snap('control'), _load_snap('previous')
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
# A2 AMENDED (Luke, in writing, 02/07/2026 — verbatim reason logged in CHANGELOG per the SHIP_GATES amendment
# process): Curtis leg re-scripted from Ward < Curtis to Curtis >= 0.90 x Ward; Weddle leg + A9 unchanged.
# A2 UNCHANGED at 0.90 by ruling (Luke, D7 02/07): ships red at the v2 config (Curtis/Ward 0.822 measured);
# Luke verbatim: "we can look at Curtis down the line".
try:
    _cu, _wa, _we = E('Paul Curtis'), E('Josh Ward'), E('Joshua Weddle')
    _ok = (_cu >= 0.90 * _wa) and (_we > _wa)
    gate('A2', False, 'PASS' if _ok else 'FAIL',
         f'Curtis>=0.90xWard: {_cu:.0f} vs {0.90*_wa:.0f} (Ward={_wa:.0f}, ratio={_cu/max(_wa,1e-9):.3f}) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: {_we:.0f} vs {_wa:.0f}')
except LookupError as ex:
    gate('A2', False, 'ERROR', str(ex))
# A3 ANNOTATED (Luke 02/07, D4): evaluated PRE-LTI-layer. A10 AMENDED (Luke, in writing, 02/07, D4):
# 0.70 -> 0.50, DATA-CAUSED (13g of 2026 banked), PROVISIONAL — review at season-complete; CHANGELOG logged.
# A3 AMENDED (Luke, in writing, D7 02/07): 0.80 -> 0.75, DATA-CAUSED (Rozee out for the remainder of 2026,
# register-confirmed); "Happy to adjust Rozee to 75%". Knife-edge by design (same as A10/Curnow).
for gid, nm, frac, note in [('A3', 'Connor Rozee', 0.75, ' [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]'),
                            ('A10', 'Charlie Curnow', 0.50, ' [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]')]:
    try:
        v26, v25 = E(nm, 2026), E(nm, 2025)
        r = v26 / max(v25, 1e-9)
        gate(gid, True, 'PASS' if r >= frac else 'FAIL', f'{nm}: 2026={v26:.0f} 2025={v25:.0f} ratio={r:.2f} (need >={frac:.2f}){note}')
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
# A7 — position poles hold. AMENDED 2026-07-05 (Luke, owner-authorised in writing): the 2026-07-05 DPP strip
# (final consolidation) DELETED the multi-position _fut weighted-blend from engine + store (0/2652 records carry
# _fut). A7's protected-pole read is re-pointed from the stripped p.get('_fut')-dominant label to the live single
# settled-future position p.get('future_position') (the source gfut() prices the years-1+ leg from). CHANNEL SWAP
# ONLY — same protected players, same pass condition (fine future_position == dom AND gfut(p) == grp), tolerance
# UNCHANGED; A7 still tests "did a protected position pole silently revert?" against the CURRENT data model.
# See CHANGELOG 2026-07-05 (frozen-suite amendment) + SHIP_GATES.md A7.
try:
    ok, det = True, []
    for nm, dom, grp in [('Ryan Maric', 'MID', 'MID'), ('Ed Langdon', 'GDEF', 'GEN_DEF')]:
        p, err = byname(nm)
        if err: raise LookupError(err)
        lab = p.get('future_position')            # AMENDED 2026-07-05: was sorted(p['_fut'])-dominant; _fut blend stripped by the DPP consolidation
        g_ = MA.gfut(p)
        ok &= (lab == dom and g_ == grp)
        det.append(f'{nm}: future_position={lab} gfut={g_} (need {dom}/{grp}) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]')
    gate('A7', False, 'PASS' if ok else 'FAIL', '; '.join(det))
except LookupError as ex:
    gate('A7', False, 'ERROR', str(ex))
# A8 AUDITED D4 02/07 (Luke's arithmetic catch): expression was and is the literal 2x test; the old detail
# string "Berry=N vs 2x Tsatas=M" invited reading M as raw Tsatas (M was 2xTsatas). De-ambiguated to raw
# values + explicit ratio; comparison > -> >= per the frozen wording "by at least 2x".
try:
    b, t = E('Sam Berry'), E('Elijah Tsatas')
    gate('A8', True, 'PASS' if b >= 2 * t else 'FAIL',
         f'Berry={b:.0f} Tsatas={t:.0f} ratio={b/max(t,1e-9):.2f}x (need >=2.00x) [display de-ambiguated D4 02/07]')
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
# CANDIDATE MATRIX REGENERATION (gate-integrity a, 2026-07-09) — B1/B3 must certify the CANDIDATE, not the
# baked v2.5 matrix. Regenerate the candidate walk-forward book in a CLEAN subprocess (gate mode: config
# pinned; ~3 min) and REQUIRE its embedded code/store/config hashes to equal the candidate under test — a
# mismatch is a gate FAIL, not a warning. The baked v2.5 matrix is kept ONLY as an explicitly NAMED
# regression comparator (never "current"); B3's seal is re-pointed to the candidate. The gate report states
# WHICH artifact each verdict certifies.
V25_COMPARATOR = os.path.join(ROOT, 'data', 's4_matrix_baked_efea88e5.json')   # v2.5 comparator — NAMED, never "current"
CAND_MATRIX = None; CAND_MATRIX_ERR = None
# RED-PATH TEST SEAM (item-38 proofs; see SHIP_GATES.md §RED-PATH TEST SEAM). If SGC_B1_MATRIX is set, that
# path is used as the candidate matrix INSTEAD of regenerating — so a proof can feed a doctored (breaching),
# missing, or unreadable matrix and exercise B1's real HALT paths + the real suite exit code. UNSET in
# production ⇒ the block regenerates exactly as before. The injected matrix is validated by the SAME meta/
# hash checks below (no weakening): a valid-meta doctored matrix is honoured; a missing/garbage one HALTs B1.
_B1_INJECT = os.environ.get('SGC_B1_MATRIX')
# FAIL-CLOSE (item-38 fail-close, owner-ruled Option B 2026-07-13): if the seam is set this is a PROOF RUN,
# never a certification. B1 is stamped INJECTED (never a bare PASS), a loud banner tops and tails the
# report, and the suite exits NON-ZERO regardless of gate results. Everything below is guarded on
# INJECT_RUN, so a normal run (seam UNSET) is byte-identical to before. See SHIP_GATES.md §RED-PATH TEST SEAM.
INJECT_RUN = _B1_INJECT is not None
INJECT_BANNER = '################  INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION  ################'
if not ('B1' in SKIP and 'B3' in SKIP):
    try:
        if _B1_INJECT is not None:
            CAND_MATRIX = _B1_INJECT; _mrun = None
        else:
            import tempfile as _tf
            _mfd, CAND_MATRIX = _tf.mkstemp(prefix='s4_cand_', suffix='.json'); os.close(_mfd)
            _menv = _subenv(S4_MATRIX=CAND_MATRIX, RL_CONFIG_MODE='gate', RL_REPO=ROOT)   # rev143: strip SGC_* from the gate-mode child
            _mrun = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=RA, env=_menv,
                                   capture_output=True, text=True, timeout=1800)
        _meta = json.load(open(CAND_MATRIX)).get('__meta__', {}) if (CAND_MATRIX and os.path.exists(CAND_MATRIX)) else {}
        _mok = bool(_meta) and _meta.get('engine_head_md5', '')[:8] == HEAD and _meta.get('store_md5', '')[:8] == STORE
        if CONFIG_HASH is not None:
            _mok = _mok and (_meta.get('config_sha256') == CONFIG_HASH)
        if not _meta:
            if _mrun is None:
                CAND_MATRIX_ERR = f'candidate matrix missing/unreadable or carries no __meta__ (injected path: {_B1_INJECT})'
            else:
                CAND_MATRIX_ERR = f'candidate matrix carries no __meta__ (exit={_mrun.returncode}; stderr tail: {_mrun.stderr[-300:]})'
            CAND_MATRIX = None
        elif not _mok:
            CAND_MATRIX_ERR = ('candidate matrix hashes != candidate under test — engine %s=%s? store %s=%s? config %s=%s?'
                               % (_meta.get('engine_head_md5', '?')[:8], HEAD, _meta.get('store_md5', '?')[:8], STORE,
                                  (_meta.get('config_sha256') or '-')[:8], (CONFIG_HASH or '-')[:8]))
            CAND_MATRIX = None
    except Exception as _mex:
        CAND_MATRIX_ERR = f'{type(_mex).__name__}: {_mex}'; CAND_MATRIX = None

def _b1_july8(mpath):
    """THE GATED construction (owner-ruled July-8, 2026-07-13; register v52; CONSTRAINTS v1.8 G-COHORT):
    the UNWEIGHTED average, across the draft classes observed at each career year N, of that class's RAW
    class-year SUM of Vpath at N. Population: incurve (type in {ND,RD}) AND draft class 2004-2020. N=1 ==
    end of calendar Yr1 (=C+1). NO per-class yr1=100 renormalisation and NO mean-of-ratios — that indexed
    reading is DEMOTED (see _b1_rows, kept only as a non-gating shape diagnostic). Skips '__'-meta keys.
    Returns (SUM, classes): SUM[N] is the avg-of-raw-class-sums at year N; classes is the sorted class list."""
    _m = json.load(open(mpath)); _S = {}
    for _k, _v in _m.items():
        if _k.startswith('__'):
            continue
        _C = int(_v['year'])
        if not _v['incurve'] or not (2004 <= _C <= 2020):
            continue
        for _i in range(len(_v['yrs'])):
            _N = _i + 1
            if _N > 7:
                break
            _S[(_C, _N)] = _S.get((_C, _N), 0.0) + float(_v['Vpath'][_i] or 0.0)
    _co = sorted({c for c, _ in _S})
    _SUM = {N: float(np.mean([_S[(C, N)] for C in _co if (C, N) in _S]))
            for N in range(1, 8) if any((C, N) in _S for C in _co)}
    return _SUM, _co

def _b1_rows(mpath):
    """DEMOTED INDEXED reading (2026-07-13) — kept ONLY as B1's non-gating SHAPE diagnostic, never the gate.
    per-class indexed curves R (each class' own Yr1 = 100) + cross-class AVERAGE-of-indexed row (mean-of-
    ratios). This is the owner's superseded 02/07 D5 wording; the historic headline 126.8/125.2/116.1 is
    THIS row and must not be quoted as the gated number. Skips '__'-meta keys."""
    _m = json.load(open(mpath)); _S = {}
    for _k, _v in _m.items():
        if _k.startswith('__'):
            continue
        _C = int(_v['year'])
        if not _v['incurve'] or not (2004 <= _C <= 2020):
            continue
        for _i, _yy in enumerate(_v['yrs']):
            _N = _i + 1
            if _N > 7:
                break
            _S[(_C, _N)] = _S.get((_C, _N), 0.0) + float(_v['Vpath'][_i] or 0.0)
    _co = sorted({c for c, _ in _S})
    _R = {C: {N: 100.0 * _S[(C, N)] / max(_S[(C, 1)], 1e-9) for N in range(1, 8) if (C, N) in _S} for C in _co}
    _AVG = {N: float(np.mean([_R[C][N] for C in _co if N in _R[C]])) for N in range(1, 8) if any(N in _R[C] for C in _co)}
    return _R, _AVG, _co

# B1 — G-COHORT growth law. CODE-CONFORMED 2026-07-13 (owner-ruled, register v52; CONSTRAINTS v1.8): the
# gate IS the JULY-8 CONSTRUCTION — for each draft class the RAW class-year SUM of Vpath at each career year
# N (N=1 == end of calendar Yr1 = C+1), averaged UNWEIGHTED across the classes observed at N (population:
# incurve type in {ND,RD} AND draft class 2004-2020). den = min(y1,y2). Each of y4/y5/y6 INDIVIDUALLY vs
# hard <= 1.30; a breach HALTS. The 1.20-1.25 guide is ADVISORY (margin reported, never gates). NO per-class
# yr1=100 renormalisation, NO mean-of-ratios — that INDEXED reading is DEMOTED to the non-gating SHAPE
# diagnostic below (owner 08/07: "no need to rescale... sounds silly"; the historic headline 126.8/125.2/
# 116.1 is the indexed row, NOT the gated number). SILENT-GATE RULE (item-38 fix): a missing/unreadable
# matrix, a raised exception, or a None/absent figure is a HALT (RED) — never a skip, never a silent pass.
# Computed on the CANDIDATE regenerated this run.
B1_TABLE = None
try:
    if 'B1' in SKIP:
        gate('B1', False, 'HALT', 'SGC_SKIP=B1 — B1 is a BINDING gate (G-COHORT) and MUST NOT be skipped '
             'silently; an absent result is a FAILURE, not a pass (item-38 rule). Treated as HALT.')
    elif CAND_MATRIX is None:
        gate('B1', False, 'HALT', f'candidate matrix unavailable — B1 produced NO result and HALTS rather '
             f'than pass silently (the v2.5 comparator is NOT substituted): {CAND_MATRIX_ERR}')
    else:
        SUM, cohorts = _b1_july8(CAND_MATRIX)
        for _rq in (1, 2, 4, 5, 6):
            if SUM.get(_rq) is None:
                raise ValueError(f'July-8 construction incomplete on this matrix — missing year-{_rq} '
                                 f'class-sum (an absent figure HALTS, never passes)')
        den = min(SUM[1], SUM[2]); den_src = 'y1' if SUM[1] <= SUM[2] else 'y2'
        ratios = {N: SUM[N] / den for N in (4, 5, 6)}
        breaches = [N for N in (4, 5, 6) if ratios[N] > 1.30]
        ok = not breaches
        def _guide(r):                                       # advisory band 1.20-1.25 — NEVER gates
            return 'in-guide' if 1.20 <= r <= 1.25 else ('above-guide' if r > 1.25 else 'below-guide')
        # FAIL-CLOSE: a clean, non-breaching INJECTED matrix is stamped INJECTED (never a bare PASS) — it is
        # a proof, not a certification. A breach still HALTs (HALT wins). See SHIP_GATES.md §RED-PATH TEST SEAM.
        _b1_status = ('INJECTED' if INJECT_RUN else 'PASS') if ok else 'HALT'
        gate('B1', False, _b1_status,
             ('[INJECTED MATRIX — NOT A CERTIFICATION; run exits non-zero] ' if INJECT_RUN else '') +
             f'JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of '
             f'Vpath averaged UNWEIGHTED across {len(cohorts)} classes 2004-2020 incurve ND+RD; CANDIDATE '
             f'regenerated this run — engine {HEAD} store {STORE} config {(CONFIG_HASH or "-")[:12]}): '
             + ' '.join(f'y{N}={SUM[N]:.1f}' for N in sorted(SUM)) +
             f'; den=min(y1,y2)={den_src}={den:.1f}; ratios ' +
             ' '.join(f'y{N}={ratios[N]:.4f}({_guide(ratios[N])})' for N in (4, 5, 6)) +
             '; hard<=1.30 -> ' + ('PASS x3' if ok else f'BREACH at y{breaches} (HALT)') +
             '; guide 1.20-1.25 ADVISORY (margin reported, never gates)')
        # ---- SHAPE DIAGNOSTIC (DEMOTED indexed reading — NOT the gate; structurally cannot fail the build) --
        # Computed in its own guarded block that NEVER calls gate() and NEVER affects the exit code. It reports
        # the indexed shape (peak position + pre-peak dip) only. If it errors, it is silently downgraded to a
        # note — a diagnostic must not be able to red or green the build.
        try:
            R, AVG, _co = _b1_rows(CAND_MATRIX)
            ppk = max(AVG, key=AVG.get)
            predip = min((AVG[N] for N in range(1, ppk) if N in AVG), default=AVG.get(1))
            _t = ['| class | peakN | ' + ' | '.join(f'd{N}' for N in range(1, 8)) + ' |',
                  '|---|---|' + '---|' * 7]
            for C in cohorts:
                if C in R:
                    pk = max(R[C], key=R[C].get)
                    _t.append(f'| {C} | {pk} | ' + ' | '.join((f'{R[C][N]:.0f}' if N in R[C] else '—') for N in range(1, 8)) + ' |')
            _t.append(f'| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _{ppk}_ | ' +
                      ' | '.join((f'_{AVG[N]:.0f}_' if N in AVG else '—') for N in range(1, 8)) + ' |')
            _t.append(f'| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | ' +
                      ' | '.join((f'**{SUM[N]:.0f}**' if N in SUM else '—') for N in range(1, 8)) + ' |')
            B1_TABLE = '\n'.join(_t)
            NOTES.append(
                'B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a '
                'NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic '
                f'headline 126.8/125.2/116.1 is NOT the gate.\n  SHAPE read (indexed, advisory): peak at yr{ppk}, '
                f'pre-peak low {predip:.1f} (index yr1=100).\n' + B1_TABLE)
        except Exception as _dex:
            NOTES.append(f'B1 SHAPE diagnostic (indexed, non-gating) unavailable: {type(_dex).__name__}: {_dex} '
                         '(diagnostic only — does NOT affect the B1 verdict or the build)')
except Exception as ex:
    gate('B1', False, 'HALT', f'B1 EXCEPTION — an errored/absent result is a FAILURE, never a pass '
         f'(item-38 rule): {type(ex).__name__}: {ex}')
# B2 — GATE-1 leakage + separation. RE-WIRED (gate-integrity b, 2026-07-09): B2 INVOKES the producer
# (_gate1_wf.py) itself and reads its STRUCTURED JSON certificate — UNROUNDED observations + code/store/config
# hashes — instead of parsing an unauthenticated, integer-rounded text file at a fixed path (the old
# /home/claude/gate1_out.txt: a true 0.98 %-pt gap parsed as 0, and a handcrafted four-line file passed).
# B2 asserts the certificate's hashes == the candidate under test, then computes the leakage gap at FULL
# precision (tol 0.5 UNCHANGED — a frozen-gate number, never amended here) and reports per-cell gaps beside
# the pooled median. Labelled honestly as LEAVE-COHORT-OUT sensitivity (its true construction).
try:
    if 'B2' in SKIP:
        gate('B2', False, 'NOT-RUN', 'SGC_SKIP=B2')
    else:
        import tempfile
        _fd, _cert_path = tempfile.mkstemp(prefix='gate1_cert_', suffix='.json')
        os.close(_fd); os.remove(_cert_path)                       # fresh path; the producer writes it this run
        _env = _subenv(GATE1_JSON=_cert_path, RL_REPO=ROOT)   # rev143: strip SGC_* from the child
        _r = subprocess.run([sys.executable, '_gate1_wf.py'], cwd=RA, env=_env,
                            capture_output=True, text=True, timeout=2400)
        if not os.path.exists(_cert_path):
            gate('B2', False, 'FAIL', f'producer _gate1_wf.py emitted no certificate (exit={_r.returncode}); stderr tail: {_r.stderr[-300:]}')
        else:
            _cert = json.load(open(_cert_path)); os.remove(_cert_path)
            # (i) PROVENANCE: the certificate must be THIS candidate — code + store + config together.
            _prov = [f'engine {_cert.get("engine_head_md5","?")[:8]}={HEAD}?',
                     f'store {_cert.get("store_md5","?")[:8]}={STORE}?']
            _ok_prov = (_cert.get('engine_head_md5', '')[:8] == HEAD and _cert.get('store_md5', '')[:8] == STORE)
            if CONFIG_HASH is not None:
                _ok_prov = _ok_prov and (_cert.get('config_sha256') == CONFIG_HASH)
                _prov.append(f'config {(_cert.get("config_sha256") or "-")[:8]}={CONFIG_HASH[:8]}?')
            if not _ok_prov:
                gate('B2', False, 'FAIL', 'certificate provenance MISMATCH — not this candidate (handcrafted/stale cert rejected): ' + '; '.join(_prov))
            else:
                _cells = _cert.get('cells', {})
                # (ii) FULL-PRECISION per-cell leakage gap = |WF.median - IS.median| (no integer rounding)
                _percell = [(k, abs(_cells[k]['WF']['median'] - _cells[k]['IS']['median']))
                            for k in sorted(_cells) if 'WF' in _cells[k] and 'IS' in _cells[k]]
                leak = float(np.median([g for _, g in _percell])) if _percell else float('nan')
                # (iii) GOOD>BUST separation per position (median over tenures of the WF cell medians)
                _bypos = {}
                for k in _cells:
                    _pos, _tag, _T = k.split('|')
                    if 'WF' in _cells[k]:
                        _bypos.setdefault((_pos, _tag), []).append(_cells[k]['WF']['median'])
                seps = {p: (float(np.median(_bypos[(p, 'GOOD')])), float(np.median(_bypos[(p, 'BUST')])))
                        for p in {q for q, _ in _bypos} if (p, 'GOOD') in _bypos and (p, 'BUST') in _bypos}
                sep_ok = bool(seps) and all(g_ > b_ for g_, b_ in seps.values())
                ok = sep_ok and leak <= 0.5
                _worst = sorted(_percell, key=lambda t: -t[1])[:4]
                gate('B2', False, 'PASS' if ok else 'FAIL',
                     f'leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage={leak:.3f} %-pts '
                     f'(FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells ' +
                     ', '.join(f'{k}:{g:.2f}' for k, g in _worst) + '; GOOD>BUST sep ' +
                     ', '.join(f'{p} {g_:.1f}/{b_:.1f}' for p, (g_, b_) in sorted(seps.items())) +
                     f' [cert engine {_cert["engine_head_md5"][:8]} store {_cert["store_md5"][:8]} config {(_cert.get("config_sha256") or "-")[:8]}]')
except subprocess.TimeoutExpired:
    gate('B2', False, 'FAIL', 'producer _gate1_wf.py timed out (2400s)')
except Exception as ex:
    gate('B2', False, 'ERROR', f'{type(ex).__name__}: {ex}')
# B3 — walk-forward book FREEZE-STAMP (wired at the v2.4 bake 2026-07-04). The book (s4 matrix) is
# id(p)-keyed (str(id(p)) memory addresses -> raw bytes non-deterministic), so the seal hashes the
# STABLE-keyed content (player,type,year,pick), NOT raw bytes. Compares the current matrix's stable-key
# sha256 to the baked baseline data/book_stable_seal.json. Raw-file sha will differ every regen BY DESIGN.
try:
    _seal_path = os.path.join(ROOT, 'data', 'book_stable_seal.json')
    _mpath_b3 = CAND_MATRIX     # gate-integrity (a): seal the CANDIDATE (regenerated this run), not the baked v2.5
    if 'B3' in SKIP:
        gate('B3', False, 'NOT-RUN', 'SGC_SKIP=B3')
    elif not os.path.exists(_seal_path):
        gate('B3', False, 'NOT-RUN', f'no book seal baseline at {os.path.relpath(_seal_path, ROOT)} — run the freeze-stamp to seal the baked book')
    elif _mpath_b3 is None:
        gate('B3', False, 'FAIL', f'candidate matrix unavailable — B3 cannot seal the candidate: {CAND_MATRIX_ERR}')
    else:
        def _b3_stable_sha(path):
            _d = json.load(open(path)); _by = {}
            for _idk, _rec in _d.items():
                if _idk.startswith('__'):        # skip the gate-integrity __meta__ record (not a player row)
                    continue
                _by[(_rec.get('player'), _rec.get('type'), _rec.get('year'), _rec.get('pick'))] = _rec
            _h = hashlib.sha256()
            for _k in sorted(_by.keys(), key=lambda t: json.dumps(t, sort_keys=True)):
                _h.update(json.dumps(_k, sort_keys=True).encode())
                _h.update(json.dumps(_by[_k], sort_keys=True, separators=(',', ':')).encode())
            return _h.hexdigest(), len(_by)
        _seal = json.load(open(_seal_path))
        _cur_sha, _cur_n = _b3_stable_sha(_mpath_b3)
        _sealed_head = str(_seal.get('head_md5', ''))[:8]
        _match = (_cur_sha == _seal.get('stable_sha256'))
        # The seal binds the stable-keyed FULL book content, so a value-moving candidate legitimately DIFFERS.
        # Immutability is checked WITHIN a head: same sealed head + different content = a real violation (FAIL);
        # a NEW head vs the sealed head = differs-by-design (the book must be RE-SEALED at the v2.6 bake — an
        # owner-only bake action, flagged, NOT performed here). This is the (a) re-point: B3 now certifies the
        # CANDIDATE and states which artifact it certifies, instead of silently sealing the v2.5 matrix.
        if _match:
            _st3, _verdict = 'PASS', 'MATCHES the sealed baseline'
        elif _sealed_head != HEAD:
            _st3, _verdict = 'DIFFERS-BY-DESIGN', ('candidate head %s != sealed head %s — new version; the v2.6 book '
                                                   'must be RE-SEALED at the bake (owner action)' % (HEAD, _sealed_head))
        else:
            _st3, _verdict = 'FAIL', 'IMMUTABILITY VIOLATION: same sealed head %s but book content changed' % _sealed_head
        gate('B3', False, _st3,
             f"CANDIDATE book stable seal (regenerated this run — engine {HEAD} store {STORE} config {(CONFIG_HASH or '-')[:12]}): "
             f"{_verdict}. current={_cur_sha[:16]}.. ({_cur_n} players) vs baseline={str(_seal.get('stable_sha256'))[:16]}.. "
             f"({_seal.get('n_players')} players, sealed head {_sealed_head}) [full stable-keyed content seal; "
             f"raw-file sha is id(p)-keyed / non-deterministic by design]")
except Exception as ex:
    gate('B3', False, 'ERROR', f'{type(ex).__name__}: {ex}')
if CAND_MATRIX and _B1_INJECT is None and os.path.exists(CAND_MATRIX):
    try: os.remove(CAND_MATRIX)          # ephemeral gate artifact — not a committed data file (SSI-safe).
    except OSError: pass                 # NEVER delete a caller-injected matrix (SGC_B1_MATRIX): the caller owns it.
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
        # S1 fix (register item 24, 2026-07-13): pass RL_REPO + gate mode so the B4 regen resolves the repo-homed
        # display inputs (data/owner_overrides.json) EXACTLY as the shipped board is built — the matrix subprocess
        # already sets RL_REPO=ROOT (above). Without it the override file was unresolvable from the workspace and
        # load_overrides() returned a SILENT [] (the S1 root cause): B4 then compared two override-LESS boards and
        # passed BLIND to the override. With the override now ON the shipped board, B4 must build WITH it to agree.
        _b4env = _subenv(RL_REPO=ROOT, RL_CONFIG_MODE='gate')   # rev143: strip SGC_* from the gate-mode child
        r = subprocess.run([sys.executable, 'rl_export.py'], cwd=RA, env=_b4env, capture_output=True, text=True, timeout=1800)
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
# B5 — AMENDED 02/07/2026 (Luke-ruled, in writing; text prepared D6, committed D7; verbatim in CHANGELOG):
# retired as a pass/fail ALARM. The signed year-schedule floor is now a PRICING FEATURE at the ev() boundary
# (wired in the v2 candidate engine: ev = max(ev_prefloor, floor_yrs x draftval), ND entrants only, FLAT .05
# yrs-7+ tail — VARIANT A as signed). This block does, on every board run:
#   (1) FLOOR-SAVES TABLE (player · club · yrs-in-system · raw ev · floor · saved-to · lift · register
#       status) — the new alarm surface: a list that grows unexpectedly is the old gate's signal; mispricings
#       stay VISIBLE, never silently clamped.
#   (2) PURE-LOWER-BOUND RE-VERIFY: 0 lowered, 0 non-ND moved (full non-retired population).
# At a head WITHOUT the floor feature (canonical pre-v2), the legacy offender count prints INFORMATIONALLY.
# Status is FEATURE / FEATURE-ABSENT — never FAIL (the alarm is retired). GENERATING RULE + RE-BASE-AT-PVC
# reminder unchanged in SHIP_GATES.md (floor ~= 0.9 x smoothed clean p5 ND-only; re-derive at the PVC stage).
B5_FLOORS = {1: 0.45, 2: 0.35, 3: 0.28, 4: 0.21, 5: 0.13, 6: 0.09}   # yrs 7+ -> tail (VARIANT A, as signed)
B5_TAIL = 0.05
B5_TABLE = None
def _b5_scope(p):
    return not (p.get('_retired') or p.get('_pickless') or delisted(p) or p.get('type') != 'ND') \
        and (2026 - int(p.get('year') or 0)) >= 1
try:
    ev_pre = G.get('ev_prefloor')
    if ev_pre is not None:
        # register status column (LTI register — same parse as the D6 annotated table)
        import re as _re
        _reg = {}
        try:
            _rtxt = open(os.path.join(ROOT, 'LTI_REGISTER_2026-07-02.md')).read()
            _secA = _rtxt.split('## SECTION A')[1].split('## SECTION B')[0]
            for _m in _re.finditer(r'^\| ([^|]+) \| ([^|]+) \|', _secA, _re.M):
                if _m.group(1).strip() != 'player':
                    _reg[_m.group(1).strip()] = f'LTI ({_m.group(2).strip()})'
            _secB = _rtxt.split('## SECTION B')[1].split('---')[0]
            for _nm in _re.findall(r"[A-Z][\w'\-\.]+(?: [A-Z][\w'\-\.]+)+", _secB.replace('**', '')):
                _reg.setdefault(_nm, 'OUT-2026')
        except Exception:
            pass
        PRE = {}
        with contextlib.redirect_stdout(io.StringIO()):
            for p in MA.data:
                if p.get('_retired'):
                    continue
                try:
                    PRE[id(p)] = float(ev_pre(p, 2026))
                except Exception:
                    PRE[id(p)] = None
        lowered = [p['player'] for p in MA.data if not p.get('_retired')
                   and PRE.get(id(p)) is not None and EV.get(id(p)) is not None
                   and EV[id(p)] < PRE[id(p)] - 1e-9]
        nonnd_moved = [p['player'] for p in MA.data if not p.get('_retired') and not _b5_scope(p)
                       and PRE.get(id(p)) is not None and EV.get(id(p)) is not None
                       and abs(EV[id(p)] - PRE[id(p)]) > 1e-9]
        saves = []
        for p in MA.data:
            if p.get('_retired') or not _b5_scope(p):
                continue
            v0, v1 = PRE.get(id(p)), EV.get(id(p))
            if v0 is None or v1 is None or v1 <= v0 + 1e-9:
                continue
            yis = 2026 - int(p.get('year') or 0)
            fl = B5_FLOORS.get(yis, B5_TAIL) * draftval(p)
            saves.append((p['player'], p.get('_club') or '—', yis, v0, fl, v1, v1 - v0,
                          _reg.get(p['player'], 'clear')))
        saves.sort(key=lambda r: -r[6])
        _t = ['| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |',
              '|---|---|---|---|---|---|---|---|']
        for nm, cl, yis, v0, fl, v1, lift, rg in saves:
            _t.append(f'| {nm} | {cl} | {yis} | {v0:.0f} | {fl:.1f} | {v1:.0f} | +{lift:.0f} | {rg} |')
        B5_TABLE = '\n'.join(_t)
        NOTES.append(f'B5 FLOOR-SAVES table (n={len(saves)}, aggregate lift={sum(r[6] for r in saves):+.0f} — '
                     'printed every gates-board run, the new alarm surface):\n' + B5_TABLE)
        ok_bound = not lowered and not nonnd_moved
        gate('B5', False, 'FEATURE' if ok_bound else 'FAIL',
             f'floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): {len(saves)} saves, '
             f'aggregate lift {sum(r[6] for r in saves):+.0f}; pure lower bound: lowered={len(lowered)} (bar 0), '
             f'non-ND moved={len(nonnd_moved)} (bar 0); saves table printed below (the new alarm surface)')
    else:
        off = []
        for p in MA.data:
            if not _b5_scope(p):
                continue
            v = EV.get(id(p))
            if v is None:
                continue
            fl = B5_FLOORS.get(2026 - int(p.get('year') or 0), B5_TAIL)
            if v < fl * draftval(p):
                off.append(p['player'])
        gate('B5', False, 'FEATURE-ABSENT',
             f'floor feature not wired at this head (v2 candidate carries it); legacy offender count = '
             f'{len(off)} (INFORMATIONAL — the alarm is retired, Luke-ruled 02/07 D7)')
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
        # top-level 'games' carried per the M3 wiring-time note (D4 backtest, m3_design §1): the age pin
        # activates _dev_advance's roll, which reads p['games'] — real store rows all carry it; the synth
        # must too. Byte-inert at heads without the M3 pin (the roll never activates there).
        return {'player': 'b6-synth', 'pos': GRPPOS.get('MID'), 'pick': 10.0, 'year': 2025, 'dob': '2006-03-01',
                'type': 'ND', 'scoring': ([{'year': 2026, 'games': gm, 'avg': 85.0}] if gm > 0 else []),
                'games': gm, '_pos_now': None, '_fut': []}
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
# ---------- D14 BY-CONSTRUCTION LAWS (Luke's amended V0 board law + owner override O1) ----------
# Wired PERMANENT gates (D14 1c/2a), board path: (D14a) same pos×draft-age×recorded-pick ⇒ IDENTICAL V0*
# across draft years (Luke's amended law); (D14b) within-cell V0 inversions = 0 roster-wide (the D13 pick-
# order guard TRANSFORM converted to this ASSERTION — obituary E5); (D14c) KPP retention floor O1 preserves
# depth monotonicity (max of two isotonic-non-increasing curves). Only present on a D14+ engine (board path).
try:
    _a = G['_v0_curve_assert']()
    gate('D14a', False, 'PASS' if _a['cross_draft_maxdisp'] < 1e-6 else 'FAIL',
         f"same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion={_a['cross_draft_maxdisp']:.4f} SCAR (Luke's amended law; board path)")
    gate('D14b', False, 'PASS' if _a['within_cell_inversions'] == 0 else 'FAIL',
         f"within (pos×draft-age×draft-year) V0 inversions under V0* = {_a['within_cell_inversions']} roster-wide (D13 guard-transform → assertion; obituary E5)")
    gate('D14c', False, 'PASS' if _a['kpp_depth_monotone'] else 'FAIL',
         f"KPP retention floor O1 depth-monotone = {_a['kpp_depth_monotone']} (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)")
except Exception as ex:
    gate('D14a', False, 'PENDING', f'D14 laws absent (pre-D14 engine): {type(ex).__name__}')

gate('C1', False, 'PENDING', 'naive-baseline book not yet built — definition proposal in report (needs its own directive)')
gate('C2', False, 'PENDING', 'V1-pick-model book not yet built — definition proposal in report (needs its own directive)')

# ---------- BOARD + REPORT ----------
order = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15',
         'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'D14a', 'D14b', 'D14c', 'C1', 'C2']
RES.sort(key=lambda r: order.index(r[0]))
cnt = {}
lines = [f'=== STATE: {STATE_LABEL} ===',
         f'=== SHIP GATES BOARD — head {HEAD} store {STORE} config {(CONFIG_HASH or "-")[:12]} — suite 764a0d91 — {time.strftime("%Y-%m-%d")} ===',
         f'=== CONFIG MANIFEST (gate mode): data/model_config.json hash {(CONFIG_HASH or "UNSET")[:16]} — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===',
         f'=== THREE-COLUMN RULE (Luke, binding D10): CONTROL={SNAP_CTL.get("head")} · PREVIOUS={SNAP_PREV.get("head")} · CURRENT={HEAD} ===']
if INJECT_RUN:
    lines.insert(0, INJECT_BANNER)
    lines.insert(1, f'=== SGC_B1_MATRIX SET -> candidate matrix INJECTED ({_B1_INJECT}); this is a PROOF RUN, '
                    'NOT a certification. B1 is stamped INJECTED and the suite EXITS NON-ZERO regardless of gate results. ===')
for gid, dc, st, det in RES:
    cnt[st] = cnt.get(st, 0) + 1
    tag = ' [DC]' if dc else ''
    c_st = SNAP_CTL['gates'].get(gid, {}).get('status', '—')
    p_st = SNAP_PREV['gates'].get(gid, {}).get('status', '—')
    delta = '' if (c_st == p_st == st) else '  <- MOVED'
    lines.append(f'{gid:4s}{tag:5s} {c_st:8s}| {p_st:8s}| {st:8s} {det}{delta}')
    if dc and st == 'FAIL':
        lines.append(f'{"":9s} triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)')
lines.append(f'{"":9s} columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)')
summary = 'VERDICT: ' + '  '.join(f'{k}={v}' for k, v in sorted(cnt.items())) + f'  ({time.time()-t0:.0f}s)'
lines.append(summary)
if INJECT_RUN:
    lines.append(INJECT_BANNER)
print('\n'.join(lines))
# persist this run as a snapshot (future runs' PREVIOUS/CONTROL columns read these)
try:
    os.makedirs(os.path.join(ROOT, 'data', 'gates_snapshots'), exist_ok=True)
    _snap = {'head': HEAD, 'store': STORE, 'config': CONFIG_HASH,
             'gates': {gid: {'dc': dc, 'status': st, 'detail': det[:200]} for gid, dc, st, det in RES}}
    if INJECT_RUN:            # stamp the snapshot as a non-certifying proof run (B1 status is already INJECTED)
        _snap['injected'] = True
        _snap['injected_matrix'] = _B1_INJECT
        _snap['NOT_A_CERTIFICATION'] = True
    json.dump(_snap, open(os.path.join(ROOT, 'data', 'gates_snapshots', f'gates_{HEAD}.json'), 'w'), indent=1)
except Exception:
    pass
if B1_TABLE:      # the July-8 GATED row (bold) + the DEMOTED indexed SHAPE diagnostic print on every board run
    print('\nB1 — July-8 raw-sum GATE (bold row) + indexed SHAPE diagnostic (DEMOTED 2026-07-13, NOT the gate):\n' + B1_TABLE)
if B5_TABLE:      # Luke's ruling (02/07/2026, committed D7): the FLOOR-SAVES table prints on EVERY board run
    print('\nB5 FLOOR-SAVES (the new alarm surface — mispricings stay visible, never silently clamped):\n' + B5_TABLE)
_rep_dir = os.environ.get('SGC_REPORT_DIR', 'session_2026-07-02')
# rev143 rider: keep the report IN-FENCE — a leaked/foreign (absolute or parent-escaping) SGC_REPORT_DIR wrote
# reports outside the checkout and tripped three builds; resolve under ROOT and assert containment (halt else).
_rep_abs = os.path.realpath(os.path.join(ROOT, _rep_dir)); _root_abs = os.path.realpath(ROOT)
if _rep_abs != _root_abs and not _rep_abs.startswith(_root_abs + os.sep):
    sys.exit('!! SHIP-GATES SGC_REPORT_DIR OUT OF FENCE (rev143 rider): %r resolves to %s, outside the checkout '
             '%s — the gate report must be written in-fence.' % (_rep_dir, _rep_abs, _root_abs))
rep = os.path.join(_rep_abs, f'ship_gates_report_{HEAD}.md')
os.makedirs(os.path.dirname(rep), exist_ok=True)
def _matcur(key):
    out = {}
    try:
        for r in json.load(open(os.path.join(ROOT, _REG[key]['matrix']))).values():
            out[f"{r['player']}|{r['year']}|{r['pick']}"] = r.get('cur')
    except Exception:
        pass
    return out
_MC, _MP = _matcur('control'), _matcur('previous')
with open(rep, 'w') as f:
    f.write(f'# ship_gates_check report — STATE: {STATE_LABEL} — head {HEAD} store {STORE} config {(CONFIG_HASH or "-")[:12]}\n')
    if INJECT_RUN:            # TOP banner — loud, above everything
        f.write(f'\n> ⛔ **INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION.** `SGC_B1_MATRIX` was set '
                f'(`{_B1_INJECT}`), so the candidate matrix was supplied by the caller, not regenerated. '
                'B1 is stamped **INJECTED** and the suite exits **non-zero**. No injected run can produce a '
                'certification.\n')
    f.write('_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._\n')
    f.write('```\n' + '\n'.join(lines) + '\n```\n')
    f.write('\n## Supporting detail\n')
    for n in NOTES:
        f.write('\n' + n + '\n')
    f.write(f'\n## Board top-50 (A4 context) — CONTROL {SNAP_CTL.get("head")} · PREVIOUS {SNAP_PREV.get("head")} · CURRENT {HEAD}\n')
    f.write('| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |\n|---|---|---|---|---|---|---|---|\n')
    for i, (v, p) in enumerate(board[:50], 1):
        k = f"{p['player']}|{p.get('year')}|{p.get('pick')}"
        c, q = _MC.get(k), _MP.get(k)
        dc_ = f'{v-c:+.0f}' if isinstance(c, (int, float)) else '—'
        dq = f'{v-q:+.0f}' if isinstance(q, (int, float)) else '—'
        f.write(f'| {i} | {p["player"]} | {MA.gfut(p)} | {c if c is not None else "—"} | {q if q is not None else "—"} | {v:.0f} | {dc_} | {dq} |\n')
    f.write('\n## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)\n'
            'Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:\n'
            '(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;\n'
            '(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.\n'
            'Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,\n'
            'leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);\n'
            '(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.\n')
    if INJECT_RUN:            # BOTTOM banner — tail the report as loudly as it is topped
        f.write('\n---\n> ⛔ **INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION.** The candidate matrix was '
                'caller-supplied via `SGC_B1_MATRIX`; B1 is stamped **INJECTED** and this run exited '
                '**non-zero**. A run using the seam is a red-path proof, never a certification.\n')
print(f'report: {rep}  md5={hashlib.md5(open(rep,"rb").read()).hexdigest()[:8]}')
# LOUD anti-leakage guard (folded at the v2.4 bake 2026-07-04): B2 (GATE-1 leakage) is MANDATORY. A
# NOT-RUN B2 (SGC_SKIP=B2) must NOT pass silently — it counts as a FAILURE for the exit code. SCOPED to B2
# only: other NOT-RUN/PENDING gates (A13/A14 PVC-staged, B4 skip) keep their semantics. (Gate-integrity b:
# B2 now RUNS the producer itself, so a "producer not run" state no longer exists — only an explicit skip.)
_b2st = [st for gid, _, st, _ in RES if gid == 'B2']
_b2_notrun = bool(_b2st) and _b2st[0] == 'NOT-RUN'
if _b2_notrun:
    print('\n!! LOUD FAIL: B2 anti-leakage gate NOT EVALUATED (NOT-RUN via SGC_SKIP=B2) — the MANDATORY '
          'leakage gate cannot be skipped silently. Treated as FAILURE.')
# ---- SILENT-GATE COMPLETENESS NET (item-38 fix, 2026-07-13). An ABSENT result is a FAILURE, not a pass.
# Every gate in `order` MUST have produced a verdict; a gate whose block raised BEFORE appending (or whose
# output a caller swallowed) leaves a hole here. That hole is caught, named, and HALTS the suite. This is the
# structural guarantee that a gate can no longer pass by saying nothing — the exact item-38 defect (the cohort
# gate crashed with IndexError, printed nothing behind a `| tail` pipe, and the suite reported PASS anyway).
_have = {gid for gid, _, _, _ in RES}
_missing = [g for g in order if g not in _have]
if _missing:
    print('\n!! SUITE HALT (silent-gate net): the following gate(s) produced NO verdict — an absent result '
          'is a FAILURE, not a pass: ' + ', '.join(_missing) + '. Suite exits non-zero.')
# A gate that turned an exception / missing input / breach / None into a named RED reports status HALT. Every
# HALT (like FAIL/ERROR) is a hard failure for the exit code. See SHIP_GATES.md §INVOCATION RULE: a gate's
# output must NEVER be piped through tail/head without checking its exit code.
_halts = [gid for gid, _, st, _ in RES if st == 'HALT']
if _halts:
    print('\n!! SUITE HALT: gate(s) ' + ', '.join(_halts) + ' produced a HALT (exception / missing input / '
          'breach / absent result — named RED, never a silent pass). Suite exits non-zero.')
# FAIL-CLOSE (item-38 fail-close, owner-ruled Option B 2026-07-13): an INJECTED run is a PROOF, never a
# certification. It exits NON-ZERO regardless of gate results — there is NO path by which a caller-supplied
# matrix yields a green, zero-exit certification, even when every gate passes on a clean, valid, non-breaching
# injected matrix. See SHIP_GATES.md §RED-PATH TEST SEAM.
if INJECT_RUN:
    print('\n' + INJECT_BANNER + '\n!! INJECTED MATRIX — THIS RUN IS NOT A CERTIFICATION. SGC_B1_MATRIX was set, '
          'so the candidate matrix was caller-supplied, not regenerated. The suite EXITS NON-ZERO regardless '
          'of gate results; no injected run can yield a green, zero-exit certification.\n' + INJECT_BANNER)
_hard_fail = any(st in ('FAIL', 'ERROR', 'HALT') for _, _, st, _ in RES) or _b2_notrun or bool(_missing) or INJECT_RUN
sys.exit(1 if _hard_fail else 0)
