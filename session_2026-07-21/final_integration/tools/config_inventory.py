#!/usr/bin/env python3
"""COMPLETE STATIC INVENTORY of every RL_*/PAR_* environment read reachable on the canonical
board-generation and release paths (AUDIT ADDENDUM, final integration 2026-07-21).

WHY THIS EXISTS
  The audit of ad9ab59 found a release-control defect: the stamped configuration identity
  (data/model_config.json -> config_sha256, pinned into data/expected_boot.json 'config') did NOT
  capture every live board-affecting model semantic. Kill-switches wired as `os.environ.get('RL_X','1')`
  (RL_PVC2 / RL_LEGE / RL_LEGF / RL_FLEX / RL_CAPT / RL_ISOFADE / RL_EVW / RL_DAMP / RL_SAGE29 /
  RL_LSYM / RL_EO2 / RL_ABSENCE / RL_UNCOMP ...) resolved from AMBIENT/CODE DEFAULTS, unrepresented in
  the jointly-stamped identity. Changing one silently changed the board with no identity movement.

WHAT IT DOES (no engine math; pure static read of the checked-out source + the manifest):
  1. Scans the release surface (engine/**.py, engine/forward_valuation/**.py, the root canonical-build
     + gate modules, ui/tools/**.py) for EVERY real (non-comment) `os.environ.get('RL_/PAR_...', d)`
     / `os.environ['RL_/PAR_...']` read; records name, file, line, default.
  2. Classifies every discovered variable against a curated table into EXACTLY one of:
       A  live board/release semantic
       B  infrastructure-only control (path/IO/mode) that cannot affect valuation/release-visible output
       C  diagnostic/test/bake-tool control unreachable from the canonical release path (or retired)
  3. Emits durable machine-readable evidence (config_inventory.json).
  4. FAIL-CLOSED assertions (exit non-zero):
       - ANY discovered live-path variable is UNCLASSIFIED  -> FAIL (addendum: "Unknown or
         unclassified live-path controls are a FAIL").
       - ANY class-A value-switch is NOT represented in the authoritative stamped identity
         (data/model_config.json 'vars', OR declared must-unset in data/release_contract.json).
       - ANY class-A override-hook (canonical = must-be-unset) is NOT declared must-unset.

USAGE
  python3 config_inventory.py            # print summary + write evidence next to this file; exit 0/1
  python3 config_inventory.py --json     # print the full JSON to stdout
  RL_REPO=/path python3 config_inventory.py
"""
import os, re, sys, json, glob

def repo_root():
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))):
        if cand and os.path.exists(os.path.join(cand, 'engine', 'rl_after', '_merged_recover.py')):
            return os.path.abspath(cand)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

ROOT = repo_root()

# ---- the release surface: files reachable on the canonical board-generation + release paths ----------
def surface_files():
    fs = []
    fs += sorted(glob.glob(os.path.join(ROOT, 'engine', 'rl_after', '*.py')))
    fs += sorted(glob.glob(os.path.join(ROOT, 'engine', 'forward_valuation', '*.py')))
    fs += sorted(glob.glob(os.path.join(ROOT, 'ui', 'tools', '*.py')))
    # Track B weekly live-scoring updater (release-adjacent path; gate-OFF in this build). Modules only.
    fs += sorted(glob.glob(os.path.join(ROOT, 'engine', 'rl_after', 'ingestion', '*.py')))
    fs += sorted(glob.glob(os.path.join(ROOT, 'tools', 'round_entry', '*.py')))
    for f in ('boot_guard.py', 'config_manifest.py', 'fv_provenance.py', 'ruling_config_check.py',
              'release_contract.py', 'refit_q97m.py'):
        p = os.path.join(ROOT, f)
        if os.path.exists(p): fs.append(p)
    # tests / proofs are class-C (off the canonical release path) by construction — excluded from the scan.
    fs = [p for p in fs if not os.path.basename(p).startswith('test_')
          and not os.path.basename(p).endswith('_test.py')]
    return fs

# ---- match REAL reads only (skip comment mentions: a '#' before the match on the line) ---------------
_READ = re.compile(r"""os\.environ\.get\(\s*['"]((?:RL_|PAR_)[A-Z0-9_]+)['"]\s*(?:,\s*(?P<d>[^)]*?))?\)"""
                   r"""|os\.environ\[\s*['"]((?:RL_|PAR_)[A-Z0-9_]+)['"]\s*\]""")

def scan(path):
    out = []
    with open(path) as fh:
        for i, line in enumerate(fh, 1):
            for m in _READ.finditer(line):
                # comment guard: real read only if no '#' precedes the match start on this line
                if '#' in line[:m.start()]:
                    continue
                name = m.group(1) or m.group(3)
                default = None
                if m.group(1) is not None:
                    d = (m.group('d') or '').strip()
                    if d and d[:1] in "'\"":
                        default = d.strip("'\"")
                    elif d == '':
                        default = None            # get('X') with no default -> None
                    else:
                        default = '<expr:%s>' % d  # non-literal default
                else:
                    default = '<required>'         # os.environ['X'] -> required, no default
                out.append({'var': name, 'file': os.path.relpath(path, ROOT),
                            'line': i, 'default': default})
    return out

# =====================================================================================================
# CURATED CLASSIFICATION  (var -> {cls, kind, canonical, note})
#   kind: 'switch'  = class-A value carrier, canonical value pinned in model_config.json 'vars'
#         'unset'   = class-A override hook, canonical = ABSENT (reject-if-set, declared in contract)
#         'infra'   = class-B path/IO/mode control
#         'diag'    = class-C diagnostic/test/bake-tool/retired control off the canonical board path
# Canonical values are the CODE DEFAULTS (== the posture that built the accepted board); owner-approved
# RL_PVC2=1 / RL_LEGE=1 / RL_LEGF=1 are those defaults. NO value is tuned here.
# =====================================================================================================
CLASSIFICATION = {
  # ---- class A value-switches ALREADY represented in model_config.json 'vars' (pre-addendum) ----------
  'RL_GAMMA':        ('A','switch','0.85',  'discount'),
  'RL_PICK1':        ('A','switch','3000',  'numeraire pick-1'),
  'RL_RUCK_TAX':     ('A','switch','0.25',  'official-env parity'),
  'RL_REPL_DROP':    ('A','switch','3',     'replacement drop'),
  'RL_RECENCY_DECAY':('A','switch','0.72',  'recency'),
  'RL_PRIOR_TREES':  ('A','switch','400',   'GBM trees'),
  'PAR_RAMPS':       ('A','switch','22',    'par ramps'),
  'PAR_BW':          ('A','switch','0.40',  'par bandwidth'),
  'PAR_MING':        ('A','switch','6',     'par min games'),
  'PAR_K':           ('A','switch','30',    'par k'),
  'RL_EXPO_F':       ('C','diag',  None,    'RETIRED -> DERIVED exposure_pace from data/season_state.json (supervisor 2nd review); no live env read'),
  'RL_EXPO_INPROG_Y':('A','switch','2026',  'exposure in-progress yr'),
  'RL_LEVEL_RAMP':   ('A','switch','14',    'level ramp'),
  'RL_M3_FE':        ('C','diag',  None,    'RETIRED -> DERIVED calendar_progress from data/season_state.json (supervisor 2nd review); no live env read'),
  'RL_M3_INPROG_Y':  ('A','switch','2026',  'm3 in-progress yr'),
  'RL_FORMDECL':     ('A','switch','1',     'form decline'),
  'RL_FWDRECAL':     ('A','switch','1',     'fwd recal'),
  'RL_YOUNG':        ('A','switch','1',     'young credit'),
  'RL_OVPX':         ('A','switch','1',     'overperformer px'),
  'RL_KPFFIX':       ('A','switch','1',     'kpf fix'),
  'RL_V7FORM':       ('A','switch','1',     'v7 form'),
  'RL_V7_FORM_W':    ('A','switch','0.6',   'v7 form weight'),
  'RL_W4_CRED':      ('A','switch','0.17',  'w4'),
  'RL_W4_KPFUP':     ('A','switch','1.6',   'w4'),
  'RL_W4_FADE':      ('A','switch','0.60',  'w4'),
  'RL_W4_OVPX':      ('A','switch','1.0',   'w4'),
  'RL_W4_KPFSH':     ('A','switch','0.55',  'w4'),
  'RL_W4_KPFSH_DEM': ('A','switch','0.70',  'w4'),
  'RL_W4_KPFTOP':    ('A','switch','0.4',   'w4'),
  'RL_W4_KPFM0':     ('A','switch','8.0',   'w4'),
  'RL_W4_KPFMS':     ('A','switch','16.0',  'w4'),
  'RL_W4_RUC':       ('A','switch','1',     'w4 ruck'),
  'RL_YCRED_W':      ('A','switch','0.9',   'young cred w'),
  'RL_YCRED_KPF':    ('A','switch','0.92',  'young cred kpf'),
  'RL_RUC_PRIOR_CAP':('A','switch','1.4',   'ruck prior cap'),
  'RL_RUC_CEIL_HEAD':('A','switch','0.80',  'ruck ceil head'),
  'RL_RUC_CEIL_REFPK':('A','switch','72',   'ruck ceil refpk'),
  'RL_RUC_YRH':      ('A','switch','0.35',  'ruck yr haircut'),
  'RL_PVCFIT':       ('A','switch','0',     'HELD OUT (R3); default 0'),
  'RL_LTI_CLOCK':    ('A','switch','advance','R-i owner ruling'),
  'RL_PVCADOPT':     ('A','switch','1',     'v2.9 L1'),
  'RL_MSD_POOL_EXCL':('A','switch','1',     'v2.9 L4'),
  'RL_DIAL14':       ('A','switch','1',     'v2.9 L2'),
  'RL_AGE':          ('A','switch','1',     'v2.9 L3'),
  'RL_L5_PICKLESS':  ('A','switch','1',     'v2.9 L5'),
  'RL_AVAIL':        ('A','switch','1',     'LTI/availability'),
  'RL_LTI_RETURN':   ('A','switch','1',     'LTI return arm'),
  # ---- class A value-switches MISSING pre-addendum (THE DEFECT — added by this integration) -----------
  'RL_PVC2':         ('A','switch','1',     'ADDENDUM: composed-pathway PVC ev-channel swap (Leg D Act-2); owner-approved ON'),
  'RL_LEGE':         ('A','switch','1',     'ADDENDUM: Leg E forward projection law (R103.3); owner-approved ON'),
  'RL_LEGF':         ('A','switch','1',     'ADDENDUM: Leg F forward/phantom-intake layer; owner-approved ON'),
  'RL_FLEX':         ('A','switch','1',     'ADDENDUM: Leg C flex positional machinery + §1b DPP law'),
  'RL_CAPT':         ('A','switch','1',     'ADDENDUM: ruled captain curve (L-CAPTAIN)'),
  'RL_DAMP':         ('A','switch','1',     'ADDENDUM: damping layer (kill-switch; RL_DAMP=0 => byte-exact base)'),
  'RL_EVW':          ('A','switch','1',     'ADDENDUM: continuous evidence weight (v2.10)'),
  'RL_ISOFADE':      ('A','switch','1',     'ADDENDUM: iso_corr evidence-fade + ISO monotonization (Leg A)'),
  'RL_SAGE29':       ('A','switch','1',     'ADDENDUM: S_AGE 29-tail'),
  'RL_LSYM':         ('A','switch','1',     'ADDENDUM: L-SYMMETRY'),
  'RL_EO2':          ('A','switch','1',     'ADDENDUM: two-directional anti-flattery (kill _eo min())'),
  'RL_ABSENCE':      ('A','switch','1',     'ADDENDUM: absence-penalty layer'),
  'RL_UNCOMP':       ('A','switch','1',     'ADDENDUM: uncompress output->price map (inert unless RL_UNCOMP_S set; canonical == default 1, RL_UNCOMP_S unset)'),
  'RL_UNCONSERVE':   ('A','switch','0',     'ADDENDUM: dev-shell UNFUNDED measurement override; canonical OFF (0)'),
  # ---- class A override HOOKS: canonical == must-be-UNSET (reject-if-set; declared in contract) --------
  'RL_UNCOMP_S':     ('A','unset', None,    'dev-shell grid-sweep s override; canonical ABSENT (keeps RL_UNCOMP inert)'),
  'RL_LSYM_TAB':     ('A','unset', None,    'L-SYMMETRY table path override; canonical ABSENT (sealed literal ships in source)'),
  'RL_V0SURF_REFIT': ('A','unset', None,    'forces a v0surf REFIT; canonical ABSENT (load the pinned pickle, never fit)'),
  # ---- class B infrastructure (path/IO/mode) ----------------------------------------------------------
  'RL_REPO':         ('B','infra', None,    'checkout locator'),
  'RL_FV':           ('B','infra', None,    'forward_valuation path (identity independently pinned as fv)'),
  'RL_APP_DATA':     ('B','infra','rl_app_data.json', 'board output filename'),
  'RL_CONFIG_MODE':  ('B','infra', None,    'manifest mode flag (bake|gate|canonical)'),
  'RL_VENV':         ('B','infra', None,    'pinned-venv path'),
  'RL_ALLOW_PVCFIT_BOARD':('B','infra','0', 'R3 bake-write escape hatch (governed by R3 bake guard + RULING-CONFIG)'),
  'RL_NO_OWNER_OVERRIDES':('B','infra','0', 'display-only Brodie override toggle; REJECTED in gate/bake/canonical'),
  'RL_Q97M_PKL':     ('B','infra', None,    'q97m pickle path override; loaded md5 pinned by boot_guard'),
  'RL_V0SURF_PKL':   ('B','infra', None,    'v0surf pickle path override; loaded md5 pinned by boot_guard'),
  # ---- Track B weekly-updater path (gate-OFF): infra/schedule controls, not board-valuation semantics ---
  'RL_VENDOR':       ('B','infra','/home/claude/rl_vendor', 'Track B updater vendor path (like RL_FV); staged_apply INFRA_ALLOW'),
  'RL_SEASON_ROUNDS':('B','infra', None,    'Track B updater season-round-count schedule control; not a valuation semantic; staged_apply INFRA_ALLOW'),
  # ---- class C diagnostic/test/bake-tool/retired (off the canonical board-generation path) ------------
  'RL_WS':           ('C','diag', '/home/claude/rl_workspace/rl_after', 'refit_q97m workspace (bake tool only)'),
  'RL_BAKE_REFIT':   ('C','diag',  None,    'refit_q97m trigger (bake tool only; produced pickle md5-pinned)'),
  # retired: now pinned literals in source; only comment mentions remain (guarded out by the scanner)
  'RL_ABS_LREF':     ('C','diag',  None,    'RETIRED -> pinned _ABS_L_REF=75.0 (comment-only; no live read)'),
  'RL_ABS_CAP':      ('C','diag',  None,    'RETIRED -> pinned _ABS_CAP=0.20 (comment-only; no live read)'),
  'RL_DAMP_K':       ('C','diag',  None,    'RETIRED -> pinned _DAMP_K=5.8 (audit-named; comment-only, no live read on the RC foundation)'),
}

def main(argv):
    reads = []
    for f in surface_files():
        reads.extend(scan(f))
    # RL_UI_* (ingest test overrides) — allow a family prefix as class B infra
    def classify(var):
        if var in CLASSIFICATION:
            return CLASSIFICATION[var]
        if var.startswith('RL_UI_'):
            return ('B','infra', None, 'ingest/UI test override (club_curve_provenance harness)')
        return None

    per_var = {}
    unclassified = []
    for r in reads:
        v = r['var']
        c = classify(v)
        if c is None:
            unclassified.append(r)
            cls = ('?','?', None, 'UNCLASSIFIED')
        else:
            cls = c
        pv = per_var.setdefault(v, {'var': v, 'cls': cls[0], 'kind': cls[1],
                                    'canonical': cls[2], 'note': cls[3], 'reads': []})
        pv['reads'].append({'file': r['file'], 'line': r['line'], 'default': r['default']})

    # load the authoritative stamped identity: model_config.json 'vars' + release_contract must_unset
    man_vars = {}
    try:
        man_vars = json.load(open(os.path.join(ROOT, 'data', 'model_config.json')))['vars']
    except Exception as e:
        man_vars = {}
    must_unset = []
    try:
        rc = json.load(open(os.path.join(ROOT, 'data', 'release_contract.json')))
        must_unset = rc.get('must_be_unset', [])
    except Exception:
        must_unset = []

    # representation check for class-A
    unrepresented = []
    for v, pv in per_var.items():
        if pv['cls'] != 'A':
            continue
        if pv['kind'] == 'switch':
            if v not in man_vars:
                unrepresented.append({'var': v, 'why': 'class-A switch absent from model_config.json vars'})
            elif str(man_vars[v]) != str(pv['canonical']):
                unrepresented.append({'var': v, 'why': 'manifest value %r != canonical %r'
                                      % (man_vars[v], pv['canonical'])})
        elif pv['kind'] == 'unset':
            if v not in must_unset:
                unrepresented.append({'var': v, 'why': 'class-A override hook not declared must_be_unset in release_contract.json'})

    classes = {k: sum(1 for pv in per_var.values() if pv['cls'] == k) for k in ('A', 'B', 'C', '?')}
    result = {
        'root': ROOT,
        'n_reads': len(reads),
        'n_vars': len(per_var),
        'class_counts': classes,
        'unclassified': unclassified,
        'class_A_unrepresented': unrepresented,
        'ok': (not unclassified) and (not unrepresented),
        'vars': sorted(per_var.values(), key=lambda x: (x['cls'], x['var'])),
        'surface_file_count': len(surface_files()),
    }
    if '--json' in argv:
        print(json.dumps(result, indent=2));
    outp = os.path.join(os.path.dirname(__file__), '..', 'evidence', 'config_inventory.json')
    outp = os.path.abspath(outp)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    with open(outp, 'w') as fh:
        json.dump(result, fh, indent=2, sort_keys=True)

    print("CONFIG INVENTORY  reads=%d vars=%d  A=%d B=%d C=%d unclassified=%d"
          % (len(reads), len(per_var), classes['A'], classes['B'], classes['C'], classes['?']))
    print("  evidence -> %s" % os.path.relpath(outp, ROOT))
    if unclassified:
        print("  UNCLASSIFIED live-path reads (FAIL):")
        for r in unclassified:
            print("    %(var)s  %(file)s:%(line)s" % r)
    if unrepresented:
        print("  class-A NOT in stamped identity (FAIL):")
        for u in unrepresented:
            print("    %(var)s  %(why)s" % u)
    if result['ok']:
        print("  RESULT: PASS  (zero unclassified live reads; every class-A semantic represented + stamped)")
        return 0
    print("  RESULT: FAIL")
    return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
