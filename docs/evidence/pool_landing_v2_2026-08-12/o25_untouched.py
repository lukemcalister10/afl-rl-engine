#!/usr/bin/env python3
"""ORDER 25 -- THE SCOPE GUARDS, asserted as NUMBERS at exit and diffed against origin/main.

Descended from ORDER 20C's untouched.py. No pin hex is taken on trust from any order text: every
value here is computed from the file on disk and compared with origin/main's own copy of the same
file. The instrument md5s are COMPUTED, never hardcoded.

CARRIED FROM ORDER 23's o23_untouched.py. The H-lever block below still asserts H_POOLSIT /
H_UNION at 1.0 -- but for ORDER 25 that is a NO-CHANGE assertion, not a change assertion: ORDER 23
retired them, this branch inherits that, and ORDER 25 must leave them exactly where it found them.
The check is kept rather than deleted precisely so a silent regression of ORDER 23's lever would go
red inside ORDER 25's own guard.

TWO ARTIFACTS ARE ADDED TO THE UNTOUCHED LIST that ORDER 23 could not list, because ORDER 23 was the
act that moved them: rl_model.py (ORDER 25 has NO code change) and data/model_config.json (ORDER 25
touches no manifest var). Both are asserted against THIS BRANCH'S PARENT rather than against main,
since ORDER 23 legitimately moved them there.
"""
import hashlib, os, subprocess, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))


def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def show_main(rel):
    out = subprocess.run(['git', '-C', ROOT, 'show', 'origin/main:' + rel], capture_output=True)
    return None if out.returncode else out.stdout


def md5_main(rel):
    b = show_main(rel)
    return None if b is None else hashlib.md5(b).hexdigest()


UNTOUCHED = [
    ('STORE', 'engine/rl_after/rl_model_data.json'),
    ('pickle v0surf', 'data/v0surf.pkl'),
    ('pickle q97m', 'data/q97m.pkl'),
    ('pickle peak_model_v4', 'engine/rl_after/peak_model_v4.pkl'),
    ('pvc_snapshot.json', 'engine/rl_after/pvc_snapshot.json'),
    ('bust_prior_table.json', 'engine/rl_after/bust_prior_table.json'),
    ('INSTRUMENT noarb_table_338.py', 'docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py'),
    ('INSTRUMENT noarb_table_allarm.py', 'docs/evidence/composition_2026-08-10/noarb/noarb_table_allarm.py'),
    ('harness_pvc_REPINNED_pass3.py', 'docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py'),
    ('harness_armsplit.py', 'docs/evidence/par_adoption_2026-08-12/ndprofile/harness_armsplit.py'),
    ('o21_patch.py (the carried patcher)', 'docs/evidence/pool_final_2026-08-12/o21_patch.py'),
    ('pool_retention_derive.py (ORDER 21)', 'docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py'),
    ('LTI_REGISTER.md', 'LTI_REGISTER.md'),
    ('season_state.json', 'data/season_state.json'),
    ('rl_export.py', 'engine/rl_after/rl_export.py'),
    ('s4_matrix_M1v7.py (the book builder)', 'engine/rl_after/s4_matrix_M1v7.py'),
    ('o22_next_levels.py (carried step)', 'docs/evidence/pool_final_2026-08-12/o22_next_levels.py'),
]

# artifacts ORDER 23 legitimately moved, which ORDER 25 must NOT move: compared against this
# branch's parent (the ORDER 24B tip), not against main.
PARENT = 'b3bf20b'   # the ORDER 24B tip this branch was cut from; resolved via HEAD~5 below
UNTOUCHED_VS_PARENT = [
    ('rl_model.py (ORDER 25 has no code change)', 'engine/rl_after/rl_model.py'),
    ('data/model_config.json (no manifest var)', 'data/model_config.json'),
    ('the ORDER 23 landing scripts', 'docs/evidence/pool_landing_2026-08-12/o23_stage.py'),
    ('the ORDER 24B par derivation', 'docs/evidence/pool_quality_2026-08-12/o24b_par.py'),
    ('the ORDER 24B U derivation', 'docs/evidence/pool_quality_2026-08-12/o24b_uderive.py'),
    ('o24b_stage_surface.py (carried stager)', 'docs/evidence/pool_quality_2026-08-12/o24b_stage_surface.py'),
    ('o24b_uharvest.py (carried harvest)', 'docs/evidence/pool_quality_2026-08-12/o24b_uharvest.py'),
    ('the ORDER 24B psi surface', 'docs/evidence/pool_quality_2026-08-12/SURFACE_psi.json'),
    ('the ORDER 24B par table', 'docs/evidence/pool_quality_2026-08-12/par.json'),
]

bad = []
print("%-38s %-34s %-34s %s" % ("artifact", "landed md5", "origin/main md5", "verdict"))
print("-" * 122)
for label, rel in UNTOUCHED:
    p = os.path.join(ROOT, rel)
    got = md5f(p) if os.path.exists(p) else 'ABSENT'
    exp = md5_main(rel) or 'ABSENT-ON-MAIN'
    ok = got == exp
    if not ok:
        bad.append(label)
    print("%-38s %-34s %-34s %s" % (label, got, exp, "UNMOVED" if ok else "*** MOVED ***"))

print()
print("%-44s %-34s %-34s %s" % ("artifact (vs this branch's parent)", "landed md5", "parent md5", "verdict"))
print("-" * 122)
for label, rel in UNTOUCHED_VS_PARENT:
    p = os.path.join(ROOT, rel)
    got = md5f(p) if os.path.exists(p) else 'ABSENT'
    out = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD~5:' + rel], capture_output=True)
    exp = 'ABSENT-ON-PARENT' if out.returncode else hashlib.md5(out.stdout).hexdigest()
    ok = got == exp
    if not ok:
        bad.append(label)
    print("%-44s %-34s %-34s %s" % (label, got, exp, "UNMOVED" if ok else "*** MOVED ***"))

# the band pickle lives outside the checkout, on the engine's own load path
band = '/home/claude/cm_400.pkl'
BANDPIN = '34faa8659cc8f19794f5cb9584fa19b2'
print()
if os.path.exists(band):
    ok = md5f(band) == BANDPIN
    print("band pickle (engine load path) %s  md5 %s  %s"
          % (band, md5f(band), "== its pin, and this landing never writes it" if ok else "*** MISMATCH ***"))
    if not ok:
        bad.append('band')
else:
    print("band pickle %s ABSENT on this box (the boot guard's load-path check covers it)" % band)

# ---- THE NATIONAL SIDE OF THE CURVE ARTIFACT MUST NOT HAVE MOVED --------------------------------
print()
now = json.load(open(os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')))
was = json.loads(show_main('engine/rl_after/pvc_curve_v2.json'))
for k in ('curve', 'curve_md5', 'pool_value', 'domain', 'split', 'numeraire_pin1_3000',
          'r104_9_strict_descent', 'stamp', 'source', 'derived_from', 'pin', 'construction'):
    ok = now.get(k) == was.get(k)
    print("pvc_curve_v2.%-24s %s" % (k, "UNCHANGED" if ok else "*** MOVED ***"))
    if not ok:
        bad.append('pvc_curve_v2.' + k)
moved_keys = sorted(k for k in set(now) | set(was) if now.get(k) != was.get(k))
print("pvc_curve_v2 top-level keys that moved: %s" % moved_keys)
if moved_keys != ['pool_levels']:
    bad.append('pvc_curve_v2 scope')

# ---- THE SITTER LEVER: ASSERTED MOVED, in exactly the two places a default lives -----------------
print()
cfg = json.load(open(os.path.join(ROOT, 'data/model_config.json')))['vars']
eng = open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py')).read()
checks = [("manifest RL_H_POOLSIT == 1.0 (ORDER 23's, INHERITED not re-moved)", cfg['RL_H_POOLSIT'] == '1.0'),
          ("manifest RL_H_UNION == 1.0", cfg['RL_H_UNION'] == '1.0'),
          ("engine default H_POOLSIT == 1.0", "os.environ.get('RL_H_POOLSIT','1.0')" in eng),
          ("engine default H_UNION == 1.0", "os.environ.get('RL_H_UNION','1.0')" in eng),
          ("H_MATNONRD untouched at 1.0", cfg['RL_H_MATNONRD'] == '1.0'),
          ("the RL_ITEM_H kill-switch is untouched", "H_ON=os.environ.get('RL_ITEM_H','1')!='0'" in eng),
          ("the composed _h_cut cell logic is untouched", "f*=H_POOLSIT" in eng and "f*=H_UNION" in eng)]
for lab, ok in checks:
    print("sitter lever: %-45s %s" % (lab, "YES" if ok else "*** NO ***"))
    if not ok:
        bad.append(lab)

# ---- THE FULL DIFF ------------------------------------------------------------------------------
print()
out = subprocess.run(['git', '-C', ROOT, 'diff', 'origin/main', '--name-only'], capture_output=True, text=True)
changed = [x for x in out.stdout.split() if x]
print("FILES THIS BRANCH CHANGES vs origin/main (%d):" % len(changed))
for c in changed:
    print("   ", c)

print()
print("SCOPE GUARDS: ALL HELD" if not bad else "*** SCOPE BREACH: %s ***" % bad)
sys.exit(0 if not bad else 1)
