import os, sys
if os.environ.get('PYTHONHASHSEED') != '0':   # determinism: pin hash seed so set()/dict iteration order is stable across runs (no value impact)
    os.environ['PYTHONHASHSEED'] = '0'; os.execv(sys.executable, [sys.executable] + sys.argv)
import json, numpy as np, math
from collections import defaultdict
import io as _io, contextlib as _ctx
import single_source as _SS
import fv_provenance as _FVP     # the ONE canonical FV selector / identity + fail-closed provenance helpers
# ==== PROVENANCE + CONFIG FAIL-CLOSED PREAMBLE (fv-provenance remediation 2026-07-20; corrective 2026-07-20) =
# GREEN 2: record the full forward-valuation + rl_model + config provenance BEFORE any board is generated
# (RL_FV, resolved dir, FV source-set identity, distribution_pricing.py path+hash, rl_model path+hash,
# config_manifest path+identity) — written to an rl_app_data.provenance.json sidecar and a one-line stderr
# marker, so the import state that made the board is fingerprinted (closes the audit's "no import-state record").
# JOB 4 / C1: in a CANONICAL board build (RL_CONFIG_MODE=bake|gate) config-manifest enforcement is FAIL-CLOSED
# and NON-CIRCULAR — the trusted checkout root is derived INDEPENDENTLY from the environment, the EXACT
# <root>/config_manifest.py is executed by path (never a sys.path shadow), and this runs BEFORE anything
# (incl. the provenance report) can import/cache an unverified config_manifest. Dev-shell (no RL_CONFIG_MODE)
# stays available for exploration (enforce is a no-op) but still emits the provenance record.
def _emit_provenance():
    try:
        _prov = _FVP.provenance_report()
    except Exception as _e:
        _prov = {'error': repr(_e)}
    try:
        with open('rl_app_data.provenance.json', 'w') as _pf:
            json.dump(_prov, _pf, indent=2, sort_keys=True)
    except Exception:
        pass
    sys.stderr.write("PROVENANCE " + json.dumps({_k: _prov.get(_k) for _k in
        ('RL_FV_env', 'resolved_fv_dir', 'fv_identity', 'fv_identity_expected',
         'distribution_pricing_md5', 'rl_model_path', 'rl_model_md5',
         'config_manifest_path', 'config_manifest_identity')}, sort_keys=True) + "\n")
    return _prov
_CANON_MODE = os.environ.get('RL_CONFIG_MODE')
_TROOT = _FVP.env_root(halt=False)          # trusted checkout root from RL_REPO/CLAUDE_PROJECT_DIR (env only)
if _CANON_MODE in ('bake', 'gate', 'canonical'):   # 'canonical' = the fenced release board build; same fail-closed treatment
    # (1+2) C1: verify+execute the trusted config_manifest by path and enforce — BEFORE _emit_provenance can
    #       import/cache an unverified one. Missing / shadowed-on-path / already-cached-foreign / data-missing /
    #       hash-mismatch / enforce-no-identity all HALT here, before board generation.
    _cfg_hash, _TROOT = _FVP.verify_config_manifest(_CANON_MODE)
    sys.stderr.write("CONFIG ACCEPTED %s  (trusted %s)\n" % (_cfg_hash[:12], os.path.join(_TROOT, 'config_manifest.py')))
    # (3) forward-valuation checkout + resolved-dir provenance fail-closed BEFORE board generation.
    import boot_guard as _BG
    _BG.assert_fv_provenance(_TROOT)
else:
    # dev-shell: config manifest is a NO-OP (enforce returns None outside bake/gate); exploration stays available.
    try:
        import config_manifest as _CFG; _CFG.enforce()
    except ImportError:
        pass
_PROV = _emit_provenance()                  # config_manifest, if imported, is now the TRUSTED one in bake/gate
# ========================================================================================================
_SS.assert_startup()            # GUARDS 3 + 3b (lookalike tripwire + engine-opens) before the board is built
_SS.lock_tier2()               # stamp + read-only-lock the frozen train-time caches (peak model + pvc_snapshot)
# ==== ONE ENGINE INSTANCE (F1 FIX 2026-07-05, Luke one-source rewire) ====================================
# BEFORE: rl_export exec'd rl_model.py into its OWN namespace for the display fields, while _merged_recover
# imported a SEPARATE rl_model as MA for the values -- TWO live instances whose player objects differed by
# id(). The valuation gate was `id(p) in _REAL`, and _REAL held the ids of MA's objects, so it matched 0/805
# of the objects rl_export priced -> the ruck cap, v7 age-taper and B5 floor were SILENTLY DROPPED from the
# shipped board (over-pricing ~2/3 of players; Emmett shipped 1361 vs engine 855). F1.
# AFTER: the board is built from THE SAME instance the values come from. _merged_recover imports rl_model as
# MA and wires ev(); we take `players` AND every display fn from that MA, and price MA's own player objects,
# so every _REAL layer fires on the board exactly as in the engine. Belt-and-suspenders: the _REAL gate is
# now keyed by stable key (not id, see _merged_recover), and a hard export<->engine parity gate runs at build
# end (below, before json.dump) -- the build FAILS if any board value != the engine's gated ev().
_ens = {}
with _ctx.redirect_stdout(_io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], _ens)
_ev = _ens['ev']; g = _ens['MA'].__dict__          # THE engine instance (rl_model imported as MA, valuation-wired)
# ==== ACTUAL-LOADED PROVENANCE PROOF (C2/C3, corrective 2026-07-20) — BEFORE any board is written ==========
# Prove the FV modules + rl_model the engine ACTUALLY loaded are the pinned/trusted sources (not a constructed
# path). The spec-loaded FV siblings are reached via wire_redesign's bound namespace (PR/TR/rd/cp/dp + PR.pb),
# the bare-imported ones (e.g. conditional_prior) via sys.modules; each must be a member of the resolved pinned
# forward_valuation tree with the pinned bytes, and the loaded rl_model must be byte-identical to the trusted
# checkout. A HALT here occurs before json.dump, so no board / pin / production file is written or mutated.
if _FVP.expected_identity(_TROOT) is not None:
    if _TROOT is None:
        raise SystemExit("CANONICAL BUILD HALT: cannot verify loaded provenance — set RL_REPO / CLAUDE_PROJECT_DIR "
                         "to the checkout (env-anchored trusted root required for the actual-loaded proof; fail-closed).")
    _loaded_fv = {}
    _W = sys.modules.get('wire_redesign') or _ens.get('W')
    if _W is not None:
        for _nm in ('PR', 'TR', 'rd', 'cp', 'dp'):
            _m = getattr(_W, _nm, None)
            if _m is not None and getattr(_m, '__file__', None):
                _loaded_fv['wire_redesign.' + _nm] = _m.__file__
        _pr = getattr(_W, 'PR', None)
        _pb = getattr(_pr, 'pb', None) if _pr is not None else None
        if _pb is not None and getattr(_pb, '__file__', None):
            _loaded_fv['par_redesign.pb'] = _pb.__file__
    _fv_basenames = set(_FVP.fv_source_files(_FVP.checkout_fv_dir(_TROOT)))
    for _mn, _mod in list(sys.modules.items()):
        _f = getattr(_mod, '__file__', None)
        if _f and os.path.basename(_f) in _fv_basenames:
            _loaded_fv['sys.modules[%s]' % _mn] = _f
    _FVP.assert_loaded_fv(_loaded_fv, _TROOT)
    _FVP.assert_loaded_rl_model(getattr(_ens['MA'], '__file__', None), _TROOT)
    sys.stderr.write("LOADED-PROVENANCE OK  fv_modules=%d rl_model=%s\n"
                     % (len(_loaded_fv), os.path.abspath(getattr(_ens['MA'], '__file__', '') or '?')))
# ==== R3 BAKE GUARD (2026-07-09) — the PVC fit is HELD OUT of the baked board by owner ruling R3 ==========
# The shipped board's pick currency (PVC / picks / intake*) MUST be the frozen v3.4 curve (_PVC0), never the
# fitted candidate curve. RL_PVCFIT now defaults 0 (compliant-by-default); this guard makes a fitted board
# UNBAKEABLE-WRONG: if the fit is active (_W4PVC True) the export HALTS rather than write an R3-non-compliant
# board. An operator deliberately inspecting the fit sets RL_ALLOW_PVCFIT_BOARD=1 to write a clearly labelled
# experimental board that is never used for a bake. Origin: the pre-2026-07-09 default '1' silently baked the
# held-out fit into board bcd81363 (picks 3-60 down 18-42%); this guard + the flipped default close that hole.
if _ens.get('_W4PVC') and os.environ.get('RL_ALLOW_PVCFIT_BOARD', '0') == '0':
    raise SystemExit(
        "R3 BAKE GUARD: RL_PVCFIT is ON (fitted PVC curve loaded) — writing rl_app_data.json would embed the "
        "held-out fit into the board's pick currency, violating owner ruling R3 (RL_PVCFIT=0 at bake). "
        "Refusing to write the board. Unset RL_PVCFIT (default 0) to bake the compliant frozen-v3.4 board, or "
        "set RL_ALLOW_PVCFIT_BOARD=1 for an explicitly non-bakeable PVC-fit experiment.")
g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()  # _merged_recover's load left MA's clock at a historical V0-build year; pin to the present before pulling AGE_REF / building display fields
players=g['players']; GRP=g['GRP']; bnow=g['bnow']; effpk=g['effpk']; age=g['age']; level_now=g['level_now']
level_stable=g['level_stable']; seasons=g['seasons']; srel=g['srel']; peak_est=g['peak_est']
basepk_c=g['basepk_c']; bandof=g['bandof']; survival=g['survival']; track_delta=g['track_delta']
los_decay=g['los_decay']; clamp=g['clamp']; hist=g['hist']; pkbest=g['pkbest']; PEAK_AGE=g['PEAK_AGE']
PVC=g['PVC']; SCALE=g['SCALE']; debut=g['debut']; data=g['data']; BANDS=g['BANDS']; NB=len(BANDS)
# ==== (f) L7 NUMÉRAIRE — ADOPTED-CURVE REPOINT (register item 26 / S5; owner "Rebase, 3000 is it.") ======
# The board ships in the NUMÉRAIRE (pick 1 = 3000). Two coupled DISPLAY-LAYER moves; the engine ev() is
# untouched (store/engine/config frozen — this is a value-presentation re-base, not a valuation change):
#   (1) PICK SIDE (here): the shipped pick curve BECOMES the adopted curve (engine/rl_after/pvc_curve_L1b.json
#       — the same L1 ev-channel curve players are already priced off), replacing the frozen v3.4 × 1.0524
#       display curve which diverged from adopted at 98/99 picks (the "two currencies" oddity A13/A14).
#       adopted pick-1 == 3000 natively (pinned) — no rescale; monotone non-increasing (asserted).
#   (2) PLAYER SIDE (at the ev-read, below): every displayed player value ÷ F, so players and picks live in
#       ONE currency off ONE curve. F = the certified 1.0524 (pick_redenomination.json), retained here ONLY as
#       the numéraire divisor; the old frozen-v3.4 × F redenomination is RETIRED (no legacy path remains).
_NUM=json.load(open('pick_redenomination.json')); _F=_NUM['factor']
# LEG D ACT-2 (RL_PVC2, job 8): the HELD-PICK LADDER currency reads the LIVE re-derived curve (the ev-channel
# basis _PVC0 == pvc_curve_v2.json). RL_PVC2=0 => stays the L1b adopted artifact => board 9829d01a byte-exact.
_pvc_art='pvc_curve_v2.json' if os.environ.get('RL_PVC2','1')!='0' else 'pvc_curve_L1b.json'
_adopted_doc=json.load(open(_pvc_art))
_ADOPTED={int(k):int(v) for k,v in _adopted_doc['curve'].items()}
assert _ADOPTED.get(1)==3000, 'L7 HALT: adopted_curve[1] != 3000 (%s)'%_pvc_art
_akeys=sorted(_ADOPTED)
assert all(_ADOPTED[_akeys[i]]>=_ADOPTED[_akeys[i+1]] for i in range(len(_akeys)-1)), 'L7 HALT: adopted curve not monotone non-increasing'
PVC={k:_ADOPTED[k] for k in PVC if k in _ADOPTED}                 # shipped PVC IS the adopted curve (the stamped pvc_curve artifact)
print('L7 ADOPTED-CURVE REPOINT: shipped PVC = %s (pick1=%d, %d picks, monotone, ÷F=%.4f on players)'%(_pvc_art,PVC[1],len(PVC),_F))
# ==== (g) NUMÉRAIRE ASSERT — UNCONDITIONAL STANDING LAW (register v30 item 17; L7 baked 2026-07-13) =======
# "PICK 1 = 3000 IS THE NUMÉRAIRE." The dormant legacy (×1.0524, factor≠1.0) branch is RETIRED at the bake:
# no pre-L7 path remains, so the assert is UNCONDITIONAL — a shipped board with pick-1 ≠ 3000 HALTS, always.
# The pick curve is the adopted artifact (repointed in (f)); this re-asserts the numéraire anchor at write.
# Future scale drift re-bases the CURRENCY to the anchor (L7 ÷ the drift), never the anchor to the drift.
if PVC[1] != 3000:
    raise SystemExit('NUMÉRAIRE HALT (register v30 item 17): shipped pick-1 = %d ≠ 3000. A numéraire board '
                     'MUST anchor pick-1 to 3000 — re-base the CURRENCY to the anchor (L7 ÷ the scale drift), '
                     'never the anchor to the drift. Refusing to write the board.'%PVC[1])
print('NUMÉRAIRE GUARD: PASS — shipped pick-1 = 3000 (UNCONDITIONAL standing law, register v30 item 17)')
expected_c=g['expected_c']; realized_cv=g['realized_cv']; natcv=g['_natcv']; PICKEQ=g['PICKEQ']; MECH_STATS=g['MECH_STATS']
P_estab=g['P_estab']; established=g['established']; _durable=g['_durable']; _recent_starter=g['_recent_starter']; level_now=g['level_now']; AGE_REF=g['AGE_REF']  # establishment-P + Brodie (JS-parity bake)
val=g['val']; proj_from_peak=g['proj_from_peak']; gfut=g['gfut']; futblend=g['futblend']; futstreams=g['futstreams']  # futstreams = the board LABEL blend (TRUE alternate; item 271 fut-label fix)

# ONE PRICE (D4, Luke's ruling 02/07/2026): the board renders engine ev() -- _merged_recover is the single
# valuation source. The forward/backward season view asks the engine the as-of-year question:
# vM2/vM1/v/vP1/vP2 = ev(p, 2024/2025/2026/2027/2028); the view owns no math.
# L7 NUMÉRAIRE (player side): the displayed player values are re-based to the numéraire by the uniform ÷F.
# This divides ONLY the '_v*' display caches — engine ev() is untouched, and the display fns (peak_est/
# level_now/track/...) read the engine objects, never these caches. _raw2026 keeps the pre-rebase 2026 ev
# for the order/ratio verification (below) and the numéraire parity gate.
_nb = lambda x: int(round(x / _F))
_raw2026 = {}
with _ctx.redirect_stdout(_io.StringIO()):
    for _p in players:
        _r = _ev(_p, 2026); _raw2026[_p['key']] = _r; _p['_v'] = _nb(_r)
        _p['_vM2'], _p['_vM1'] = _nb(_ev(_p, 2024)), _nb(_ev(_p, 2025))   # backward = REAL past re-values (byte-exact; no form-anchor)
        # LEG E projection law (R103.3): the FORWARD lens sets the form anchor to true-now (2026) so the +1/+2
        # view credits EXPECTED production (age+k, _dev_advance up the map's OWN growth curve — the Reid
        # constraint; no lens-only term). RL_LEGE=0 => _LENS_FORM stays None => old ev(p,2027/2028) => 06d8af60
        # byte-exact. LTI truncation is honoured automatically: demonstrated form/games stay at 2026 (BASE_REF).
        if os.environ.get('RL_LEGE', '1') != '0': g['_LENS_FORM'] = 2026
        _p['_vP1'], _p['_vP2'] = _nb(_ev(_p, 2027)), _nb(_ev(_p, 2028))
        g['_LENS_FORM'] = None
        # ==== LEG F3 §2.vi — RE-SUPPLY THE PEDIGREE ANCHOR AT +k (MEMO_LEGF v1.1; ruling item 353 pt 4:
        # rl_export:96 is STILL IMPLICATED after the true-site clock cure in _merged_recover). The item-352
        # verdict: the forward lens "re-prices on the production map without re-supplying the pedigree anchor at
        # +k", so a zero/low-evidence young pick (priced today on the Leg-D V0 pedigree blend) collapses forward.
        # CURE: floor the +k value at the NOW value _v decayed by PROJECTED EVIDENCE φ(g)=(1-g/G0)^2 — the
        # engine's OWN young-credit decay (G0=46 career games; _merged L1c _ycred φ), so the pedigree weight
        # decays ONLY as projected evidence accrues (smooth in games, no cliff; g>=G0 => φ=0 => byte-exact).
        # REID: the anchor is the SAME map's now value _v (no separate young multiplier, no lens-only growth
        # term — a floored DECLINE, the mirror of "no lens-only growth"). FORWARD-ONLY (never _v/_vM1/_vM2);
        # k=0-safe (φ<=1 => the max is inert on _v); rides RL_LEGF (=0 => skipped => the RL_LEGF=0 chain
        # byte-exact) AND RL_LEGE (the forward lens). Strawman φ SEALED in the PLAN; [OWNER] at the viewing.
        if os.environ.get('RL_LEGF', '1') != '0' and os.environ.get('RL_LEGE', '1') != '0':
            _gc = _p.get('games')
            if _gc is None: _gc = sum(int(x.get('games', 0) or 0) for x in (_p.get('scoring') or []))
            if _gc < 46:
                _fl = int(round(((1.0 - _gc / 46.0) ** 2) * _p['_v']))
                if _p['_vP1'] < _fl: _p['_vP1'] = _fl
                if _p['_vP2'] < _fl: _p['_vP2'] = _fl
        _p['_cvx'] = 1.0
    for _p in g['back_extra']:
        _p['_v'] = _p['_vM2'] = _p['_vM1'] = _p['_vP1'] = _p['_vP2'] = _nb(_ev(_p, 2026))
        _p['_cvx'] = 1.0
g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()  # the ev loop advanced the clock to the last as-of year; re-pin to the present so the DISPLAY layer (peak_est/level_now/track/...) reads 2026, as the prior 2-instance display did
# ==== (g2) L7 RE-BASE VERIFICATION — order preserved + anchor-pair ratios (register v30, l7_rebase.py) =====
# A uniform ÷F with round() is monotone (never a STRICT inversion) but can TIE two formerly-distinct values
# (a rounding artifact, reported not failed). Assert: along the pre-rebase order (desc), the rebased values
# are non-increasing (no strict inversion); and all 10 anchor-pair ratios match to <0.2%.
_l7_order = [k for k, _ in sorted(_raw2026.items(), key=lambda kv: -kv[1])]
_reb2026 = {_p['key']: _p['_v'] for _p in players}
_l7_seq = [_reb2026[k] for k in _l7_order]
_l7_order_ok = all(_l7_seq[i] >= _l7_seq[i + 1] for i in range(len(_l7_seq) - 1))
_l7_ties = sum(1 for i in range(len(_l7_order) - 1)
               if _raw2026[_l7_order[i]] > _raw2026[_l7_order[i + 1]] and _l7_seq[i] == _l7_seq[i + 1])
_l7_anchors = ['marcus-bontempelli', 'max-gawn', 'kieren-briggs', 'sam-darcy', 'louis-emmett']
_l7_rc = []
for _i in range(len(_l7_anchors)):
    for _j in range(_i + 1, len(_l7_anchors)):
        _a, _b = _l7_anchors[_i], _l7_anchors[_j]
        if _a in _raw2026 and _b in _reb2026 and _reb2026[_b]:
            _rb = _raw2026[_a] / _raw2026[_b]; _ra = _reb2026[_a] / _reb2026[_b]
            # RELATIVE <0.2% (the directive's tolerance): a uniform ÷F preserves ratios exactly; the residual
            # is round() error, which is RELATIVE to the ratio. An absolute 0.002 is too tight for large
            # anchor ratios (bont/emmett ~4.3) once the store is perturbed (e.g. the correction canary).
            _l7_rc.append((f'{_a}/{_b}', round(_rb, 4), round(_ra, 4), abs(_rb - _ra) / _rb < 0.002))
if not _l7_order_ok:
    raise SystemExit('L7 HALT: uniform ÷%.4f STRICTLY inverted a pair (not a tie) — ratios NOT preserved.' % _F)
if not all(x[3] for x in _l7_rc):
    raise SystemExit('L7 HALT: anchor-pair ratio drift > 0.2%%: %s' % [x for x in _l7_rc if not x[3]])
print('L7 NUMÉRAIRE RE-BASE ÷%.4f: order preserved (no strict inversion; %d rounding ties), %d/%d anchor ratios <0.2%%'
      % (_F, _l7_ties, sum(1 for x in _l7_rc if x[3]), len(_l7_rc)))

# ==== CONSUMER-WIRING FIX — lti_reg tag on first-year no-scoring-row register rows (2026-07-13) ==========
# The RL_AVAIL layer stamps the register disposition `_lti_reg` on the MA.data records. For MOST register
# names the board `players` object IS that same MA.data object, so the tag rides through. But for the two
# first-year (no store scoring row) register rows — harley-barker, blake-thredgold — the board `players`
# list holds a SEPARATE synthesized object than the one RL_AVAIL mutated, so `_lti_reg` never reaches the
# board object and both tags exported NULL (verified STILL NULL after the migration/refit regens: a regen
# alone does not close it — the fix is CONSUMER WIRING). Resolve the register-disposition tag by STABLE KEY
# from the engine records here. DISPLAY-ONLY: this reads the register tag (a fact from LTI_REGISTER.md),
# never `v` — every board value is the already-computed `_v` and is untouched (zero EV movers by
# construction). The board-native availability ATTRIBUTION fields (avail_hc / avail_nerf / lti_return_hc)
# are left as the board object's own values; for these two the shipped board applied no availability
# haircut — a valuation-path matter OUTSIDE this export/display fence, returned as a finding, not fixed.
_lti_reg_by_key = {p.get('key'): p.get('_lti_reg') for p in data if p.get('_lti_reg') is not None}

def _lti_reg_of(p):   # board tag if present, else the engine record's tag resolved by stable key (never None-drops a live register row)
    return p.get('_lti_reg') if p.get('_lti_reg') is not None else _lti_reg_by_key.get(p.get('key'))

# ==== (h) EXPORT ATTRIBUTION SIDECAR — vPrev (last-accepted-bake value) + per-lever G-ATTR deltas =========
# Certified per-player attribution, committed as engine/rl_after/export_attribution.json and seeded to cwd
# by bootstrap exactly like pick_redenomination.json / lti_return_table.json. It is DERIVED FROM the
# certified G-ATTR stage boards (base → +L1 → +L1+L4 → +L1+L4+L2 → +L1+L4+L2+L3 → FULL), reproduced to the
# dollar by the committed gen_gattr_chain.sh — i.e. taken from the certified attribution, NOT a new method.
#   vPrev[key]  = the player's value on the last-accepted-bake board = the all-levers-OFF pre-refit base
#                 (de4baef9 lineage, sum 723075 — the board on main this refit replaces) -> Δ-vs-bake column.
#   levers[key] = {L1,L4,L2,L3,L5} cumulative deltas that sum EXACTLY to v-vPrev -> the per-lever hover.
# Absent -> both ship null (forward-safe; the UI renders "awaiting", never a fabricated Δ). DISPLAY-ONLY:
# neither field feeds `v` (every board value is the already-computed engine ev; zero EV movers).
_EXPORT_ATTR={}
if os.path.exists('export_attribution.json'):
    _EXPORT_ATTR=json.load(open('export_attribution.json'))
    print('EXPORT ATTRIBUTION: loaded vPrev/levers for %d keys (base sum=%s, from certified stage boards)'
          %(len(_EXPORT_ATTR.get('vPrev',{})), _EXPORT_ATTR.get('base_sum')))
_vprev_by_key=_EXPORT_ATTR.get('vPrev',{})
_levers_by_key=_EXPORT_ATTR.get('levers',{})

def player_rec(p):
    grp=bnow(p); gf=gfut(p); fb=futstreams(p); ep=effpk(p); b=bandof(ep); ln=level_now(p); lns=level_stable(p)   # fut-label fix (item 271): the board 'fut' carries the TRUE primary/alternate label (futstreams), NOT the value blend (futblend, whose MAX law collapses alt->pri when REPL[alt]>=REPL[pri]); VALUE already priced into _v via futblend upstream
    g['STBL']=False; pn=peak_est(p); g['STBL']=True; ps=peak_est(p); g['STBL']=False
    dlt,_=track_delta(gf,ep,srel(p)); surv=survival(b,dlt if dlt is not None else 0,p['games'])
    cg=sum(r['games'] for r in p['scoring']); sr=srel(p)
    track=[{'s':s,'a':round(sr[s][0],2)} for s in sorted(sr) if s<=10]
    has26=any(r['year']==2026 and r['games']>=3 for r in p['scoring'])
    mech=p['type'] if p['type'] in PICKEQ else None
    return {'name':p['player'],'key':p['key'],'grp':grp,'gf':gf,'fut':[[gg,round(w,4)] for gg,w in fb],'age':age(p),'ln':(round(ln,6) if ln is not None else None),'h26':bool(has26),
            'lns':(round(lns,6) if lns is not None else None),'pn':round(pn,6),'ps':round(ps,6),'ep':ep,'band':b,
            'surv':1.0,'pedDecay':round(max(0.0,1-(seasons(p)-1)/4.5),6),'losd':round(los_decay(p),6),
            'g':p['games'],'cg':cg,'yr':p['year'],'pk':p['pick'],'ty':p['type'],'unpl':bool(p.get('_unplayed')),
            'lnNull':level_now(p) is None,'track':track,'v':p['_v'],'bk':bool(p.get('_backonly')),
            'vP1':p.get('_vP1'),'vP2':p.get('_vP2'),'vM1':p.get('_vM1'),'vM2':p.get('_vM2'),'cvx':p.get('_cvx',1.0),
            'avail_hc':p.get('_avail_hc',0.0),                       # RL_AVAIL present haircut L_p (register out-names; was b2hc)
            'avail_nerf':p.get('_avail_nerf',0),                     # Part-1 attribution: ev(layer)-ev(no-layer) per player (G-ATTR)
            'lti_return_hc':p.get('_lti_return_hc',0.0),             # Part-2 attribution: derived return-season haircut (own column, G-ATTR)
            'lti_reg':_lti_reg_of(p),                                # register disposition tag (section/designation/on-sight flags), resolved by key for first-year no-scoring-row rows; or None
            'vPrev':_vprev_by_key.get(p['key']),                     # §7.3 last-accepted-bake value (all-off base) -> Δ-vs-bake column; None if the row is new since the bake
            'vRaw':None,                                             # §7.3 pre-override model figure; stamped (=v) only for owner-overridden rows, post-application below
            'levers':_levers_by_key.get(p['key']),                   # per-lever G-ATTR cumulative deltas {L1,L4,L2,L3,L5} (sum == v-vPrev); None if attribution sidecar absent
            'P':1.0,   # establishment prob, FROZEN (draft-cohort property, not the SuperCoach toggle); 1.0 = established/inert
            'pedOnly':bool(p.get('_unplayed') and (debut(p)>AGE_REF or p.get('_pedonly'))),   # pure-pedigree no-P case (genuine pre-debut); in-window 0-game players are NOT pedOnly -> they get P
            'brodieBase':bool(seasons(p)>=5 and not _durable(p) and not _recent_starter(p) and (level_now(p) is not None) and level_now(p)>=80),  # Brodie signal minus the RUC bit (JS applies RUC exemption live)
            'cat':p.get('_cat'),'draft':p.get('_draft'),'club':p.get('afl_club') or p.get('_draft_club'),'mech':mech}
            # (d) shipped `club` = the CURRENT AFL club (afl_club, imported item 20b), with a _draft_club fall-back
            # for retired back-catalogue rows that carry no current club (never in the active player-ranking the
            # owner views). Active 804 all carry afl_club -> houston displays Collingwood, not Port Adelaide; the
            # ten club-less rows fill. affl_team (the AFFL keeper side) is a SEPARATE field, untouched.
active=[player_rec(p) for p in players]
back=[player_rec(p) for p in g['back_extra']]   # board-history-only rows (retired players recalled for -1/-2)
# ==== FUT-LABEL PER-ROW ASSERTION (item 271) — the board 'fut' stream carries the store's TRUE primary/
# alternate on EVERY dual row (labels, not the value-collapsed bar). RL_FLEX-gated: with RL_FLEX=0 the board
# is byte-exact base (futstreams => single), so the store's dual data is intentionally not rendered. A
# regression HALTs (SILENCE IS A RED).
if os.environ.get('RL_FLEX','1')!='0':
    _by_key={r['key']:r for r in active}
    _flexrows=[p for p in players if p.get('alternate_position') and p.get('p_dual_stream')]
    _futmis=[]
    for p in _flexrows:
        r=_by_key.get(p['key'])
        if r is None: continue
        q=float(p['p_dual_stream'])/100.0
        want=[[gfut(p),round(1.0-q,4)],[GRP.get(p['alternate_position'],gfut(p)),round(q,4)]]
        if r.get('fut')!=want: _futmis.append((p['key'],r.get('fut'),want))
    if _futmis:
        raise SystemExit('FUT-LABEL HALT (item 271): %d dual rows board-label != store primary/alternate: %s'
                         % (len(_futmis), _futmis[:5]))
    print('FUT-LABEL ASSERTION: PASS — %d dual rows carry the true primary/alternate on the board' % len(_flexrows))
# ==== (d) ZERO-EMPTY-CLUB ACCEPTANCE (register v59, item 20/33) — HALT on any blank `club` on the board ====
# After the afl_club import (b) + the club repoint (d), EVERY exported row must display a club: active rows
# carry the current AFL club (afl_club); back rows fall back to their draft club. The ten formerly-blank
# rows (zorko/pendlebury/ben-murphy/kobe-mcdonald/patrick-carr/oscar-berry/indy-cotton/cillian-bourke/
# wil-parker/jamie-elliott) are the natural red-path test. A blank here means the import missed a row.
_club_blank=[r['key'] for r in active+back if not r.get('club')]
if _club_blank:
    raise SystemExit('ZERO-EMPTY-CLUB HALT (register v59): %d exported rows have an empty `club`: %s'
                     % (len(_club_blank), _club_blank[:25]))
print('ZERO-EMPTY-CLUB ACCEPTANCE: PASS — 0 blank club across %d exported rows (active %d + back %d)'
      % (len(active)+len(back), len(active), len(back)))
coh=[]
for p in hist:
    grp=GRP[p['pos']]; ep=effpk(p); pk=pkbest(p); rec={'grp':grp,'ep':ep,'pkbest':(round(pk,6) if pk else None)}
    if pk: rec['relc']=round(clamp((pk/max(basepk_c(grp,ep),40.0))**2.2,0.40,3.0),6)
    coh.append(rec)
def pct(a,q):
    a=sorted(a)
    if not a: return None
    i=(len(a)-1)*q; lo=int(i); f=i-lo; return a[lo]*(1-f)+a[min(lo+1,len(a)-1)]*f

# ===== ANALYTICS A: bid categories (Father-Son / Academy / Next Gen) vs normal, by pick range + by club =====
# Use NATIONAL picks with matured careers (drafted <= 2021) so realised value is meaningful.
def cat_of(p):
    c=(p.get('_cat') or '')
    if 'Father-Son' in c: return 'Father-Son'
    if 'Academy' in c: return 'Academy'
    if 'Next Gen' in c: return 'Next Gen'
    return 'Open'
RANGES=[(1,10),(11,20),(21,30),(31,45),(46,99)]
def rlabel(pk):
    for lo,hi in RANGES:
        if lo<=pk<=hi: return '%d-%d'%(lo,hi if hi<99 else 99)
    return '46-99'
# matured cohort: national + rookie picks, drafted 2008-2023, who played a senior game.
# MATURITY FLOOR (time-based): a career is only judged once it's had 3+ seasons to develop. We do NOT
# use "played a 10+ game season" as the gate, because realized_cv reads a young player's current
# output as his career peak -- a 19yo key forward who plays 15 low-scoring games passes a games test
# but his value is understated, not settled. Time is the only fair gate, applied to academy and open alike.
MATURITY_SEASONS=3
def judgeable(p): return (2026-debut(p))>=MATURITY_SEASONS
matured=[p for p in data if p['type'] in ('ND','RD') and p['pick'] and 2008<=p['year']<=2023 and p['pos'] in GRP and judgeable(p)]
def EP(p): return effpk(p)
_openp=[p for p in matured if cat_of(p)=='Open']
open_base=[None]*100
for k in range(1,100):
    vs=[realized_cv(p) for p in _openp if abs(EP(p)-k)<=6]
    open_base[k]=float(np.mean(vs)) if vs else None
_last=open_base[1] or 300.0
for k in range(1,100):
    if open_base[k] is None: open_base[k]=_last
    else: _last=open_base[k]
def overshoot(p):  # realised value minus what an OPEN pick at the same effective slot returns (>0 = beat the slot)
    return realized_cv(p)-open_base[min(99,EP(p))]
CAT_BY_RANGE={}
for cat in ['Open','Father-Son','Academy','Next Gen']:
    row={}
    for lo,hi in RANGES:
        grp=[p for p in matured if cat_of(p)==cat and lo<=EP(p)<=hi]
        key='%d-%d'%(lo,hi if hi<99 else 99)
        if not grp: row[key]=None; continue
        played=[p for p in grp if pkbest(p) is not None]
        row[key]={'n':len(grp),'hit':round(100*len(played)/len(grp)),
            'mean_val':round(float(np.mean([realized_cv(p) for p in grp]))),
            'mean_over':round(float(np.mean([overshoot(p) for p in grp]))),
            'open_val':round(float(np.mean([open_base[min(99,EP(p))] for p in grp])))}
    CAT_BY_RANGE[cat]=row
# club-level: which clubs over/undershoot expected value with academy / father-son / next-gen
CAT_BY_CLUB={}
for cat in ['Father-Son','Academy','Next Gen']:
    cl=defaultdict(list)
    for p in matured:
        if cat_of(p)==cat: cl[p['_draft_club']].append(p)   # (c) CAT_BY_CLUB groups by DRAFT club (producing club) — its correct input; field renamed _club->_draft_club (item 20c). Output identical.
    rows=[]
    for club,grp in cl.items():
        if len(grp)<2: continue
        played=[p for p in grp if pkbest(p) is not None]
        rows.append({'club':club,'n':len(grp),'hit':round(100*len(played)/len(grp)),
            'mean_over':round(float(np.mean([overshoot(p) for p in grp]))),
            'mean_val':round(float(np.mean([realized_cv(p) for p in grp])))})
    rows.sort(key=lambda r:-r['mean_over'])
    CAT_BY_CLUB[cat]=rows

# ===== ANALYTICS B: entry mechanisms (pickless) -> outcomes + pick-equivalent (from the model) =====
MECH=sorted(MECH_STATS.values(), key=lambda m:m['pick_equiv'])

# ---- standard curve/projector exports (ported; cohort defs use real ND+RD) ----
ftcoh=[p for p in data if p.get('_ft') and p.get('_grp') in ('ND','RD') and 2008<=p['year']<=2021 and p['pos'] in GRP]
PROJ2={}
band_peaks={b:[pkbest(p) for p in ftcoh if bandof(p['pick'])==b and pkbest(p)] for b in range(NB)}
band_nb={b:sum(1 for p in ftcoh if bandof(p['pick'])==b and not pkbest(p)) for b in range(NB)}
for pos in sorted(set(GRP.values())):
    for b in range(NB):
        grp=[p for p in ftcoh if GRP[p['pos']]==pos and bandof(p['pick'])==b]
        pk=[pkbest(p) for p in grp if pkbest(p)]; nb=sum(1 for p in grp if not pkbest(p))
        if len(pk)>=4: pk_use=pk; nb_use=nb; src='cohort'
        else: pk_use=(pk+band_peaks[b]); nb_use=nb+band_nb[b]; src='mixed'
        if not pk_use: pk_use=band_peaks[b] or [70.0]
        n=len(pk); tot=n+nb
        PROJ2[pos+'|'+str(b)]={'p10':round(pct(pk_use,0.10),2),'p50':round(pct(pk_use,0.50),2),'p90':round(pct(pk_use,0.90),2),
            'peak_age':PEAK_AGE[pos],'n':n,'src':src,'nb':nb_use,'establish':int(round(100*n/tot)) if tot else 0}
devcoh=[p for p in data if p.get('_ft') and p.get('_grp') in ('ND','RD') and 2008<=p['year']<=2025 and p['pos'] in GRP]
cellP=defaultdict(list); cellB=defaultdict(list)
for p in devcoh:
    pos=GRP[p['pos']]; b=bandof(p['pick']); d=debut(p)
    for r in p['scoring']:
        s=r['year']-d+1
        if 1<=s<=10 and r['games']>=4: cellP[(pos,b,s)].append(r['avg']); cellB[(b,s)].append(r['avg'])
def trcol(getter,minn):
    p10=[];p50=[];p90=[];par=[];nn=[]
    for s in range(1,11):
        vals=getter(s)
        if len(vals)>=minn:
            p10.append(round(pct(vals,0.10),1)); p50.append(round(pct(vals,0.50),1)); p90.append(round(pct(vals,0.90),1))
            par.append(round(float(np.mean(vals)),1)); nn.append(len(vals))
        else: p10.append(None);p50.append(None);p90.append(None);par.append(None);nn.append(len(vals))
    return {'p10':p10,'p50':p50,'p90':p90,'par':par,'n':nn}
TRAJ={}; TRAJB={}
for b in range(NB): TRAJB[str(b)]=trcol(lambda s,b=b:cellB[(b,s)],8)
for pos in sorted(set(GRP.values())):
    for b in range(NB):
        col=trcol(lambda s,pos=pos,b=b:cellP[(pos,b,s)],4)
        if any(v is not None for v in col['p50']): TRAJ[pos+'|'+str(b)]=col
CENTERS=[(lo+hi)/2.0 for lo,hi in BANDS]
# Pick Projector (ported)
devall=[p for p in data if p.get('_ft') and p.get('_grp') in ('ND','RD') and 2008<=p['year']<=2025 and p.get('pos') in GRP and effpk(p) is not None]
recs=[]
for p in devall:
    d=debut(p); seas={}; ever11=False
    for r in p['scoring']:
        ss=r['year']-d+1
        if 1<=ss<=10 and r['games']>=4: seas[ss]=r['avg']
        if r['games']>=11: ever11=True
    recs.append({'pos':GRP[p['pos']],'ep':effpk(p),'seas':seas,'ever':ever11})
def wq(vals,wts,q):
    if not vals: return None
    o=sorted(zip(vals,wts)); v=[a for a,_ in o]; w=[b for _,b in o]; cw=[];c=0.0
    for x in w: c+=x; cw.append(c)
    tot=cw[-1]
    if tot<=0: return None
    t=q*tot
    for i in range(len(v)):
        if cw[i]>=t:
            if i==0 or cw[i]==cw[i-1]: return v[i]
            return v[i-1]+(v[i]-v[i-1])*((t-cw[i-1])/(cw[i]-cw[i-1]))
    return v[-1]
def kern(dpk,h): return math.exp(-0.5*(dpk/h)**2)
def bw(pk): return min(9.0,max(2.0,2.0+0.10*pk))
QS=[0.02,0.10,0.25,0.50,0.75,0.90,0.98]; PICKS=range(1,61); SEAS=range(1,11); MINEFF=10.0
posset=sorted(set(GRP.values())); recs_by_pos={ps:[r for r in recs if r['pos']==ps] for ps in posset}
def collect(rset,pk,ss):
    h=bw(pk); va=[]; wa=[]
    for r in rset:
        if ss in r['seas']:
            w=kern(abs(r['ep']-pk),h)
            if w>1e-4: va.append(r['seas'][ss]); wa.append(w)
    return va,wa
def wavg(va,wa): return sum(v*w for v,w in zip(va,wa))/sum(wa)
PJALL={}
for ss in SEAS:
    for pk in PICKS:
        va,wa=collect(recs,pk,ss)
        if va: PJALL[(pk,ss)]={'q':[wq(va,wa,q) for q in QS],'par':wavg(va,wa)}
PJ={}
for pos in posset:
    arr=[]
    for pk in PICKS:
        h=bw(pk); denom=0.0; ever=0.0
        for r in recs_by_pos[pos]:
            w=kern(abs(r['ep']-pk),h); denom+=w
            if r['ever']: ever+=w
        est=round(100*ever/denom) if denom>0 else None
        qs=[]; par=[]; nn=[]
        for ss in SEAS:
            vp,wp=collect(recs_by_pos[pos],pk,ss); eff=sum(wp) if wp else 0.0; allc=PJALL.get((pk,ss))
            if eff>=MINEFF and vp: q=[wq(vp,wp,qq) for qq in QS]; pr=wavg(vp,wp)
            elif vp and allc:
                a=clamp(eff/MINEFF,0,1); q=[a*wq(vp,wp,QS[i])+(1-a)*allc['q'][i] for i in range(len(QS))]; pr=a*wavg(vp,wp)+(1-a)*allc['par']
            elif allc: q=allc['q'][:]; pr=allc['par']
            else: q=None; pr=None
            qs.append([round(x,1) for x in q] if q else None); par.append(round(pr,1) if pr is not None else None); nn.append(round(eff,1))
        arr.append({'q':qs,'par':par,'n':nn,'est':est})
    PJ[pos]=arr
DEBUT_AGE={'ND':19,'RD':19,'SSP':19,'MSD':19,'PSD':19,'IRE':19,'UNR':19,'PDA':19,'PDN':19,'PDS':19}
_ndc=g['_NDC']; _medNDC=int(round(float(np.median(list(_ndc.values())))))
TYPEOFF={'ND':0,'RD':_medNDC}   # rookie picks sit after the national draft on the projector's pick scale
TILT={k:g[k] for k in ['TILT_REF','GAIN_UP','W_UP','UP_MAX','TILT_HI','GAIN_DN','W_DN','DN_MAX','TILT_LO','NBAD_REF','SUS_MIN']}
try:
    import lti_register as _LTIREG; _reg_md5=_LTIREG.file_md5()
except Exception: _reg_md5=None

# ==== (i) FUTURE-LENS PHANTOM PICK ENTRIES (items 12+14, owner-worded 2026-07-12) =========================
# The current cycle's remaining picks are the next-EOY National Draft class — a class already in the league
# whose players are not yet individually known. Per the owner's appearance law those lines belong on the +1
# and +2 lenses ONLY: "the phantom entry for those picks should be in the +1 and 2 lens" — NEVER on the
# current / −1 / −2 player ladder (item-14: "current board = PLAYER ranking only"; that exclusion is already
# live and is NOT disturbed here — these entries are a SEPARATE lens-scoped array the ladder never reads).
# Once the class is drafted the actual players carry the value and the line retires (Duursma precedent).
# Value = entering-class PVC FACE value (the board's official 15%/yr time-discount view stands; no unruled
# future-pick discount is invented — item 12 defers that dial). labelYear rolls with the view. The picks are
# ND-scaled off the shipped PVC exactly like the trade-desk `picks` array. DISPLAY-ONLY: no player `v` moves.
_EOY_CLS='%d-EOY-ND'%2026            # the next National Draft class (drafted end of 2026; plays from 2027)
lensPicks=[{'n':n,'v':PVC[n],'lens':off,'labelYear':2026+off,'cls':_EOY_CLS,'kind':'phantom_pick'}
           for off in (1,2) for n in range(1,31)]   # +1 (2027) and +2 (2028) lenses only

# ==== (j) LENS-CONSERVATION DIAGNOSTIC (item 12; REPORT-ONLY, NOT a gate) =================================
# The owner's year-0 continuity law rendered as a check: "−2 through today through +2 lens should have
# similar-ish total value on each board" — value CONVERTS (classes enter as phantom picks; players fade out
# the bottom / retire), it does not vanish. Each lens' total = Σ players' as-of value shown on that lens
# (active carry vM2/vM1/v/vP1/vP2; backward-only rows surface on the −1/−2 lenses) + Σ phantom picks on that
# lens. Declared caveats (owner): unexercised-pick face value with no future-discount + scrap-floor leakage
# at retirements make the future lenses run slightly under — small and explainable, or itself a finding.
_LENS_FIELD=[('-2','vM2',-2),('-1','vM1',-1),('now','v',0),('+1','vP1',1),('+2','vP2',2)]
lensConservation={}
for _lbl,_fld,_off in _LENS_FIELD:
    _psum=sum((r.get(_fld) or 0) for r in active)
    _nb=0
    if _off<0:                                        # backward-only recalled players appear on −1/−2
        _psum+=sum((r.get(_fld) or r.get('v') or 0) for r in back); _nb=len(back)
    _pk=sum(pp['v'] for pp in lensPicks if pp['lens']==_off)
    lensConservation[_lbl]={'lensYear':2026+_off,'players':_psum,'picks':_pk,'total':_psum+_pk,
                            'nPlayers':len(active)+_nb,'nPicks':sum(1 for pp in lensPicks if pp['lens']==_off)}
_cons_now=lensConservation['now']['total'] or 1
lensConservation['_meta']={'principle':'year-0 continuity: value converts, does not vanish (item 12)',
    'report_only':True,'basis':'PVC face value on future picks; no future-discount dial (deferred, item 12)',
    'spread_vs_now':{_l:round(100*(lensConservation[_l]['total']-_cons_now)/_cons_now,2) for _l,_,_ in _LENS_FIELD}}

out={'active':active,'back':back,'cohort':coh,
     'lensPicks':lensPicks,'lensConservation':lensConservation,   # items 12/14: future-lens phantom picks + conservation diagnostic (report-only)
     'lti_register_md5':_reg_md5,   # R-REG=R2: stamp the availability input's identity into the derived board
     'BASEPK_REG':{f'{k[0]}|{k[1]}':round(v,3) for k,v in g['BASEPK_REG'].items()},
     'POOL':{str(k):round(v,3) for k,v in g['POOL'].items()},
     'MIX':{str(b):{gg:round(w,4) for gg,w in g['MIX'][b].items()} for b in g['MIX']},
     'BAND_ANCHOR':g['BAND_ANCHOR'],'bands':g['BANDS'],'CENTERS':[round(c,2) for c in CENTERS],'PJ':PJ,'DEBUT_AGE':DEBUT_AGE,
     'PEAK':g['PEAK'],'PEAK_AGE':g['PEAK_AGE'],'REPL':g['REPL'],'DELTAS':{str(k):v for k,v in g['DELTAS'].items()},
     'pm_pos':g['pm_pos'],'pm_band':{str(k):v for k,v in g['pm_band'].items()},
     'GAMMA':g['GAMMA'],'PMAX':g['PMAX'],'S_SH':g['S_SH'],'BETA_POS':g['BETA_POS'],'ICPT_POS':g['ICPT_POS'],
     'BUST_BAND':{str(k):v for k,v in g['BUST_BAND'].items()},'GRACE':g['GRACE'],'LOS_C':g['LOS_C'],'LOS_P':g['LOS_P'],
     'CAPT_THRESH':g['CAPT_THRESH'],'CAPT_GAIN':g['CAPT_GAIN'],'CAPT_EXP':g['CAPT_EXP'],'CAPT_CAP':g['CAPT_CAP'],
     'ALPHA':g['ALPHA'],'CURVE_H':g['CURVE_H'],'LENS':g['LENS'],'SEASON_PROG':g['SEASON_PROG'],
     'PICKEQ':PICKEQ,'MECH':MECH,'TYPEOFF':TYPEOFF,'CAT_BY_RANGE':CAT_BY_RANGE,'CAT_BY_CLUB':CAT_BY_CLUB,'RANGES':['%d-%d'%(lo,hi if hi<99 else 99) for lo,hi in RANGES],
     **TILT,'SCALE':round(SCALE,5),'PVC':{str(k):v for k,v in PVC.items()},
     'BASE_YEAR':2026,                                                  # board view N maps to draft year BASE_YEAR+N
     'intake':int(round(105000/_F)),                                   # Luke ground-truth entry+1 class value ~105000 (×1.0524 world); L7-rebased to the numéraire so it stays comparable with the (now-numéraire) pick-sum it supersedes. Supersedes the durable pick-sum (under-counts vs the convex board value).
     'intakePickSum':round(sum((PVC[k] if k in PVC else PVC[max(PVC)]) for k in range(1,61)) + 6*PVC.get(80,PVC[max(PVC)]) + 13*PVC.get(90,PVC[max(PVC)]) + 9*PVC.get(84,PVC[max(PVC)])),   # durable per-season pick-equiv replenishment (60 ND +6 RD +13 post-draft +9 SSP), ex-transient MSD — reference only
     'intakeFull':round(sum((PVC[k] if k in PVC else PVC[max(PVC)]) for k in range(1,61)) + 6*PVC.get(80,PVC[max(PVC)]) + 13*PVC.get(90,PVC[max(PVC)]) + 27*PVC.get(84,PVC[max(PVC)])),  # + transient MSD (9 SSP+18 MSD = 27 at pick-84 equiv)
     'picks':[{'n':n,'v':PVC[n]} for n in range(1,31)]}                 # Option-A replenishment: future-draft picks as board assets (value=PVC, label year rolls with the view)
# ==== LEG D ACT-2 (job 8): PICK-BAND WIRING on the LIVE re-derived curve (PVC == the ev-channel basis _PVC0).
# GATED on RL_PVC2 so RL_PVC2=0 stays board 9829d01a byte-exact. posture 2027 discounts are R104.5/§6.3 BINDING
# (acceptance leg_d_placeholders.posture_2027_discounts) — EXACTLY these three values. 2027 (+1 lens) held picks
# x (1 - discount), ONE application (no double-count: the +1 lensPicks carry FACE value; this is the posture view).
if os.environ.get('RL_PVC2','1')!='0':
    out['posture_2027_discounts']={'balanced':0.10,'contender':0.15,'rebuilder':0.05}
    out['picks_2027']={_post:[{'n':n,'v':int(round(PVC[n]*(1-_d)))} for n in range(1,31)]
                       for _post,_d in (('balanced',0.10),('contender',0.15),('rebuilder',0.05))}
    # held pick = the LIVE curve over its ladder band [low,high], taken as the equal-weight MEAN (memo §5)
    out['pick_band_mean']={'%d-%d'%(lo,hi):int(round(sum(PVC[min(k,max(PVC))] for k in range(lo,hi+1))/(hi-lo+1)))
                           for lo,hi in ((1,3),(4,7),(8,12),(13,20),(21,27),(28,35),(36,48),(49,99))}
# ==== PERMANENT EXPORT<->ENGINE VALUE-PARITY GATE (F1 regression tripwire, 2026-07-05) ==================
# Every board value MUST equal the engine's gated ev() for that player, recomputed INDEPENDENTLY here and
# matched by STABLE KEY. This is exactly the check the shipped board silently failed (2nd rl_model instance
# -> id-gate matched 0/805 -> ruck cap / age-taper / floor dropped). If any active player diverges beyond
# epsilon, the build FAILS LOUDLY -- no mispriced board is ever written. eps=0: ev() is integer-valued and
# the board renders it verbatim, so parity is exact by construction on this single-instance build.
_PARITY_EPS=0
_by_key={r['key']:r for r in active}
_parity_fail=[]
with _ctx.redirect_stdout(_io.StringIO()):
    for _p in players:
        _bv=_by_key.get(_p['key'],{}).get('v'); _gv=int(round(_ev(_p,2026)/_F))   # numéraire: board v == round(engine ev / F)
        if _bv is None or abs(_bv-_gv)>_PARITY_EPS: _parity_fail.append((_p['key'],_bv,_gv))
g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()
if _parity_fail:
    raise SystemExit("EXPORT<->ENGINE PARITY GATE FAILED for %d/%d players (board v != engine gated ev, eps=%s):\n  "%(len(_parity_fail),len(active),_PARITY_EPS)
                     + "\n  ".join("%s: board=%s engine=%s"%(k,b,gg) for k,b,gg in _parity_fail[:25]))
print('PARITY GATE PASS: all %d active board values == engine gated ev() (matched by key, eps=%s)'%(len(active),_PARITY_EPS))

# ==== OWNER OVERRIDES — DISPLAY-ONLY, APPLIED LAST (2026-07-09, Brodie ×0.50 wiring) ======================
# Applied AFTER the export<->engine parity gate (so it can never move a value a guard measures) and BEFORE
# the board is written. owner_overrides.apply_to_board ONLY ADDS an `ov` block to a matched row — it never
# touches `v`, so every guard / aggregate / book (F2) / board parity (B4) / JS parity, all of which read
# `v` or the engine's gated ev(), is byte-identical with the override on vs off. The overrides come from the
# repo-homed data/owner_overrides.json (owner adds a row, no code change). RL_NO_OWNER_OVERRIDES=1 skips it.
import owner_overrides as _OV
_ov_applied, _ov_warn = _OV.apply_to_board(active)
for _w in _ov_warn:
    print('OWNER-OVERRIDE WARNING:', _w)
_ov_keys={_k for _k,_f,_dv in _ov_applied}
for _r in active:
    if _r['key'] in _ov_keys: _r['vRaw']=_r['v']   # §7.3 pre-override model figure = the engine value (v is never overridden); UI hover shows it vs the overridden rail
for _k, _f, _dv in _ov_applied:
    print('OWNER OVERRIDE applied (display-only): %s ×%.2f -> displayed %d (of the REBASED value; engine v untouched; vRaw model figure stamped)'%(_k,_f,_dv))
# POST-EXPORT PRESENCE ASSERTION (S1 finding, register item 24): every key in owner_overrides.json MUST
# carry its `ov` block on the exported board — a listed-but-unapplied override (key drift / silent drop)
# HALTS in gate/bake mode. Closes the hole where a silent [] shipped an override-less board.
_OV.assert_presence(active)

# ==== LEG F5 — §2.viii THE ENTRANT LAYER (+1/+2 · MEMO_LEGF v1.3 §2.viii · gate RL_LEGF, default ON) =======
# Report/view ONLY. k=0 carries ZERO phantom content; the balanced board's per-player `v` is byte-identical
# with RL_LEGF on vs off — the phantom keys are ADDITIVE lens-scoped arrays and the engine ev() is UNTOUCHED
# (this block reads only PVC + the already-computed forward columns vP1/vP2 + the `club` field + the SEALED
# structure file), so the balanced board cannot move by construction (the checkpoint law). RL_LEGF=0 => none
# of the §2.viii layer is emitted => the Leg-E board is byte-exact.
#
# §2.viii (owner item 359): the phantom layer carries the FULL expected annual intake (~103 slots) — the real
# draft pick structure at v2-curve PVC per EFFECTIVE pick, plus mechanisms at their measured pick-equivalents
# (MSD 90, all others 92 — item 341). The slot structure is measured from recorded store intake history and
# SEALED before this render (session_2026-07-18/legf5/sealed_entrant_structure.json, seal a17aafed) — NOT
# tuned against the §2.x gate (the LAW: sealed from history first). phantom=true; never at k=0; never gates/bakes.
#
# OBITUARY — F1's §2.i/§2.ii sizing is SUPERSEDED (delete, don't disable; CORE rule 7). The F1 phantom intake
# was picks 1..30 in natural-order round-robin (`_lf_pick_of`) + a flat free-intake at `_LF_R=207` per expected
# exit slot + an exit bar X=207 (the register item-343 R-candidate frame 207 / R_owner 220 / R_curve 471). That
# pick-slot strawman RETIRES: the entrant side is now the full sealed intake at PVC (§2.viii); exit risk already
# lives in r_pop (§2.ix, F4 — one carrier, no double-count). The owner's ratification list updates (§2.viii
# supersedes the item-343 R slot). Resurrection ref: git show a9570cb5:engine/rl_after/rl_export.py.
if os.environ.get('RL_LEGF', '1') != '0':
    import hashlib as _hl
    _LF_LENS = [(1, 'vP1', 2027), (2, 'vP2', 2028)]           # the forward lenses (k=0 excluded: no phantom at balanced)
    # -- load + SEAL-VERIFY the sealed entrant structure (the §6 seal-first law; HALT on drift) --------------
    _lf_seal_path = os.path.join(os.environ.get('RL_REPO', '.'),
                                 'session_2026-07-18', 'legf5', 'sealed_entrant_structure.json')
    _lf_struct = json.load(open(_lf_seal_path))
    _lf_chk = {_kk: _vv for _kk, _vv in _lf_struct.items() if _kk != 'seal_sha256_8'}
    _lf_seal = _hl.sha256(json.dumps(_lf_chk, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]
    if not (_lf_seal == _lf_struct.get('seal_sha256_8') == 'a17aafed'):
        raise SystemExit('LEG F5 HALT (§2.viii): sealed entrant structure seal drift — recomputed %s vs stored '
                         '%s vs pinned a17aafed. Re-seal from intake history before rendering.'
                         % (_lf_seal, _lf_struct.get('seal_sha256_8')))
    _PVCMAX = max(PVC)
    def _lf_pvc(_e): return PVC.get(min(int(_e), _PVCMAX), PVC[_PVCMAX])   # v2-curve PVC of an effective pick
    # -- §2.viii THE SEALED ENTRANT SLOT STRUCTURE: expected per-year occupancy per effective pick ----------
    # draft = ND + RD/PSD chained onto the national draft; mech = pickless at PICKEQ (90/92). Each priced at
    # the v2-curve PVC of its effective pick (GROSS). The sealed counts are the frozen measurement; the price
    # is re-read from the stamped curve here (identical v2 curve, so the total re-derives to the sealed 83,538).
    _lf_draft = sorted(((int(_e), _c, _lf_pvc(_e)) for _e, _c in _lf_struct['draft_occupancy'].items()),
                       key=lambda t: t[0])                   # [(effpk, expected slots/yr, pvc)] natural draft order
    _lf_mech = sorted(((int(_e), _c, _lf_pvc(_e)) for _e, _c in _lf_struct['mech_occupancy'].items()),
                      key=lambda t: t[0])                    # [(effpk 90/92, expected slots/yr, pvc)]
    _lf_draft_pvc = sum(_c * _p for _e, _c, _p in _lf_draft)
    _lf_mech_pvc = sum(_c * _p for _e, _c, _p in _lf_mech)
    _lf_ent_pvc = _lf_draft_pvc + _lf_mech_pvc               # the sealed league entrant layer (~83,538)
    # -- per-club allocation (report-only; the §2.x gate is LEAGUE-level so the split is presentational):
    # draft slots round-robin across the 18 clubs in natural draft order; mechanisms split evenly. -----------
    _lf_clubs = sorted({r['club'] for r in active if r.get('club')})
    _lf_nc = len(_lf_clubs) or 1
    _lf_draft_of = {c: [] for c in _lf_clubs}                # club -> [(effpk, count, pvc)]
    for _i, _slot in enumerate(_lf_draft):
        _lf_draft_of[_lf_clubs[_i % _lf_nc]].append(_slot)
    _lf_mech_share = _lf_mech_pvc / _lf_nc                   # even mechanism value per club
    _lf_mech_cnt_share = sum(_c for _e, _c, _p in _lf_mech) / _lf_nc
    def _lf_entval(_cl):                                     # this club's annual entrant-layer value (one class)
        return sum(_c * _p for _e, _c, _p in _lf_draft_of[_cl]) + _lf_mech_share
    # -- per club per forward lens: retained forward (r_pop-damped) + one annual entrant class ---------------
    _by_club = {}
    for _r in active:
        if _r.get('club'):
            _by_club.setdefault(_r['club'], []).append(_r)
    phantomLayer = {}; phantomPicks = []
    _cl_tot = {}                                              # club -> lens-str -> {with,without,...}
    _lg = {'0': {'with': 0, 'without': 0, 'draftValue': 0, 'freeValue': 0, 'entrantValue': 0}}
    for _k, _fld, _yr in _LF_LENS:
        _lg[str(_k)] = {'with': 0, 'without': 0, 'draftValue': 0, 'freeValue': 0, 'entrantValue': 0}
    # league phantomPicks: the sealed draft slot structure (one row per occupied effective pick, per lens)
    for _k, _fld, _yr in _LF_LENS:
        for _e, _c, _p in _lf_draft:
            phantomPicks.append({'kind': 'draft', 'effpk': _e, 'count': round(_c, 4), 'v': _p,
                                 'value': round(_c * _p), 'lens': _k, 'labelYear': _yr, 'phantom': True})
    for _cl in _lf_clubs:
        _rows = _by_club.get(_cl, [])
        _cdraft = _lf_draft_of[_cl]
        _cdraft_val = sum(_c * _p for _e, _c, _p in _cdraft)
        _cent_val = _cdraft_val + _lf_mech_share
        phantomLayer[_cl] = {}; _cl_tot[_cl] = {}
        # lens 0 (balanced): report-only echo — WITH == WITHOUT == Σ v (ZERO phantom at k=0, the invariant)
        _v0 = sum((_r.get('v') or 0) for _r in _rows)
        _cl_tot[_cl]['0'] = {'withPhantom': _v0, 'withoutPhantom': _v0, 'delta': 0, 'nPlayers': len(_rows)}
        _lg['0']['with'] += _v0; _lg['0']['without'] += _v0
        for _k, _fld, _yr in _LF_LENS:
            _proj = [_r for _r in _rows if _r.get(_fld) is not None]
            _ret_sum = sum((_r.get(_fld) or 0) for _r in _proj)             # retained forward value (exit risk already in r_pop, §2.ix)
            _with = _ret_sum + _cent_val                                    # + one annual entrant class (§2.viii)
            _without = _ret_sum
            _intake = [{'kind': 'draft', 'effpk': _e, 'count': round(_c, 4), 'v': _p, 'club': _cl,
                        'lens': _k, 'labelYear': _yr, 'phantom': True} for _e, _c, _p in _cdraft] \
                    + [{'kind': 'free', 'effpk': _e, 'count': round(_c / _lf_nc, 4), 'v': _p, 'club': _cl,
                        'lens': _k, 'labelYear': _yr, 'phantom': True} for _e, _c, _p in _lf_mech]
            phantomLayer[_cl][str(_k)] = {'retained': len(_proj), 'retainedSum': _ret_sum,
                'draftValue': round(_cdraft_val), 'freeValue': round(_lf_mech_share),
                'entrantValue': round(_cent_val), 'draftSlots': round(sum(_c for _e, _c, _p in _cdraft), 3),
                'freeSlots': round(_lf_mech_cnt_share, 3), 'intake': _intake,
                'withPhantom': _with, 'withoutPhantom': _without, 'delta': _with - _without}
            _cl_tot[_cl][str(_k)] = {'withPhantom': _with, 'withoutPhantom': _without,
                'delta': _with - _without, 'nPlayers': len(_proj)}
            _s = _lg[str(_k)]; _s['with'] += _with; _s['without'] += _without
            _s['draftValue'] += _cdraft_val; _s['freeValue'] += _lf_mech_share; _s['entrantValue'] += _cent_val
    # -- §2.viii TOTALS REPORT: per club + league, per lens (bal/+1/+2), WITH vs WITHOUT the phantom layer ---
    phantomTotals = {'_meta': {
        'law': 'MEMO_LEGF v1.3 §2.viii (owner item 359): FULL expected annual intake at v2-curve PVC per effective pick',
        'sealed_structure': 'session_2026-07-18/legf5/sealed_entrant_structure.json',
        'seal_sha256_8': _lf_struct['seal_sha256_8'],
        'entrant_layer_pvc': round(_lf_ent_pvc), 'draft_pvc': round(_lf_draft_pvc), 'mech_pvc': round(_lf_mech_pvc),
        'expected_slots_per_year': _lf_struct['expected_slots_per_year'],
        'pickeq': _lf_struct['pickeq'],
        'exit_model': 'exit risk carried by r_pop (§2.ix, F4 — incl exiters residuals); no §2.iii haircut, no double-count',
        'per_lens': 'each forward lens carries ONE annual entrant class on top of the r_pop-retained roster; +2 is the marginal-annual view and runs slightly under now (declared caveat, item-12 lens-conservation)',
        'basis': 'per club + league, per lens (bal/+1/+2), WITH vs WITHOUT the phantom layer',
        'report_only': True, 'gates': False, 'k0_phantom': 'none',
        'note': 'draft slots priced off PVC per effective pick (v2 curve, GROSS); mechanisms at PICKEQ 90/92; no wide/decile bins (CORE rule 7); sealed from intake history, NOT tuned against the §2.x gate'},
        'clubs': _cl_tot, 'league': {_lk: {'withPhantom': round(_lv['with']), 'withoutPhantom': round(_lv['without']),
            'delta': round(_lv['with'] - _lv['without']), 'draftValue': round(_lv['draftValue']),
            'freeValue': round(_lv['freeValue']), 'entrantValue': round(_lv['entrantValue'])} for _lk, _lv in _lg.items()}}
    out['phantomLayer'] = phantomLayer
    out['phantomPicks'] = phantomPicks
    out['phantomTotals'] = phantomTotals
    # ==== VISIBLE FUTURE-DRAFT ASSET LADDER (final integration 2026-07-21; canonical, RL_LEGF=1) ==========
    # The owner-facing +1/+2 views are UNIFIED asset ladders: the 804 known players (vP1/vP2) ranked together
    # with the 64 anonymous national-draft placeholders per lens (2027/2028 Draft Pick 1..64 at the EXACT
    # release-active PVC[n]). Emitted HERE (in the canonical engine build) so a plain re-run — and the Track B
    # weekly updater's board regen — reproduces the presentation with NO post-processing. The visible 64 picks
    # are the rankable assets (lensPicks); the two F5 residual aggregates are held OUT of the ranking and live
    # in draftAssetTotals for a separate reconciliation panel (they are not single tradeable assets). All three
    # reconcile EXACTLY to the sealed F5 entrant layer. Player v/vP1/vP2 are untouched (this reads only PVC +
    # the already-computed forward columns + the sealed F5 draft/mech totals). RL_LEGF=0 => this block is
    # skipped and the pre-F5 30-pick lensPicks/lensConservation stand (kill-switch clean).
    _PVC64 = sum(PVC[_n] for _n in range(1, 65))                     # Σ release-active PVC[1..64] = 64617
    _draft_r = round(_lf_draft_pvc); _mech_r = round(_lf_mech_pvc)   # sealed F5 draft / mech totals (PVC-face)
    _res_nd = _draft_r - _PVC64                                      # national-draft deep tail + partial occupancy
    _res_mech = _mech_r                                              # non-national-draft entry mechanisms
    _visible = []
    for _k, _fld, _yr in _LF_LENS:                                   # (1,'vP1',2027) , (2,'vP2',2028)
        for _n in range(1, 65):
            _visible.append({'lens': _k, 'labelYear': _yr, 'n': _n, 'v': PVC[_n],
                             'kind': 'pick', 'asset': 'pick', 'assetType': 'future_national_draft_pick',
                             'label': '%d Draft Pick %d' % (_yr, _n), 'id': 'draft-pick:%d:%d' % (_yr, _n),
                             'club': None, 'affl_team': None, 'phantom': True})
    out['lensPicks'] = _visible                                      # 64 rankable picks per lens (supersedes the 30-pick ladder)
    # recompute the lens-conservation diagnostic against the visible 64-pick ladder (report-only)
    _LF2 = [('-2', 'vM2', -2), ('-1', 'vM1', -1), ('now', 'v', 0), ('+1', 'vP1', 1), ('+2', 'vP2', 2)]
    _lc = {}
    for _lbl, _fld, _o in _LF2:
        _ps = sum((_r.get(_fld) or 0) for _r in active); _nb = 0
        if _o < 0:
            _ps += sum((_r.get(_fld) or _r.get('v') or 0) for _r in back); _nb = len(back)
        _pk = sum(pp['v'] for pp in _visible if pp['lens'] == _o)
        _lc[_lbl] = {'lensYear': 2026 + _o, 'players': _ps, 'picks': _pk, 'total': _ps + _pk,
                     'nPlayers': len(active) + _nb, 'nPicks': sum(1 for pp in _visible if pp['lens'] == _o)}
    _cn = _lc['now']['total'] or 1
    _lc['_meta'] = {'principle': 'year-0 continuity: value converts, does not vanish (item 12)',
                    'report_only': True,
                    'basis': 'visible national-draft picks 1-64 at release-active PVC face value (the ranked assets)',
                    'spread_vs_now': {_l: round(100 * (_lc[_l]['total'] - _cn) / _cn, 2) for _l, _, _ in _LF2}}
    out['lensConservation'] = _lc
    # draftAssetTotals: the visible+residual -> F5 reconciliation (residuals separate; not ranked)
    _dat = {}
    for _k, _fld, _yr in _LF_LENS:
        _dat['+%d' % _k] = {'lensYear': _yr, 'nVisiblePicks': 64, 'visible_1_64': _PVC64,
                            'residual_nd_tail': _res_nd, 'residual_mech': _res_mech,
                            'residual_total': _res_nd + _res_mech, 'total': _PVC64 + _res_nd + _res_mech,
                            'f5_entrant_layer_pvc': round(_lf_ent_pvc), 'f5_draft_pvc': _draft_r,
                            'f5_mech_pvc': _mech_r,
                            'reconciled_to_f5': (_PVC64 + _res_nd + _res_mech == _draft_r + _mech_r),
                            'players_sum': sum((_r.get(_fld) or 0) for _r in active)}
    _dat['_meta'] = {
        'basis': 'owner-facing visible future-draft asset ladder: picks 1-64 at exact release-active PVC[n], '
                 'RANKED among players in the +1/+2 lens; the two residual aggregates are held OUT of the '
                 'ranking (a separate reconciliation panel), not single tradeable assets',
        'reconciliation': 'Σ PVC[1..64] + residual_nd(draft_pvc - ΣPVC[1..64]) + residual_mech == sealed F5 '
                          'entrant layer (draft + mech); no value added on top of F5',
        'no_double_count': 'lensPicks (visible face) and phantomPicks (occupancy) are two views of the same F5 '
                           'draft and are never summed; club-held real picks are a separate owned-asset namespace',
        'report_only': True}
    out['draftAssetTotals'] = _dat
    print('LEG F5 ENTRANT LAYER (RL_LEGF=1): %d clubs · §2.viii sealed intake %d PVC (draft %d + mech %d, %.1f slots/yr, seal %s) · +1 Δ=%+d · +2 Δ=%+d · k=0 phantom=NONE'
          % (len(_lf_clubs), round(_lf_ent_pvc), round(_lf_draft_pvc), round(_lf_mech_pvc),
             _lf_struct['expected_slots_per_year'], _lf_struct['seal_sha256_8'],
             phantomTotals['league']['1']['delta'], phantomTotals['league']['2']['delta']))
else:
    print('LEG F5 ENTRANT LAYER: RL_LEGF=0 — layer NOT emitted (Leg-E board byte-exact)')

_SS.prepare_write('rl_app_data.json')                       # clear the read-only bit from a prior guarded build
json.dump(out,open('rl_app_data.json','w'),sort_keys=True)   # sort_keys: byte-deterministic output regardless of PYTHONHASHSEED (key order no longer jitters)
_srcmd5=_SS.stamp_derived('rl_app_data.json',tier=1)        # GUARD 1: stamp with source md5 + set read-only (generator is the only writer)
print('exported active=%d cohort=%d | mechanisms=%d categories analysed | board stamped src=%s (read-only)'%(len(active),len(coh),len(MECH),_srcmd5[:8]))
print('CAT_BY_RANGE Academy:',{k:(v['mean_over'] if v else None) for k,v in CAT_BY_RANGE['Academy'].items()})
print('CAT_BY_RANGE Open   :',{k:(v['mean_over'] if v else None) for k,v in CAT_BY_RANGE['Open'].items()})
