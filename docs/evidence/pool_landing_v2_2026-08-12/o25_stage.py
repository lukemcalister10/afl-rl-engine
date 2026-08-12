#!/usr/bin/env python3
"""ORDER 25 -- THE LEVEL STAGER. One script, used for BOTH jobs, which is the point.

  usage: o25_stage.py <tree> <levels.json>

Descended from docs/evidence/pool_landing_2026-08-12/o23_stage.py, and it keeps that file's central
property: it is applied to a SCRATCHPAD WORKTREE during the iteration and to the LANDING TREE when
the iteration has converged, so the landing tree IS the staged tree and the two boards are
byte-identical BY CONSTRUCTION. That identity is still verified by rebuild, never assumed.

WHAT IS DIFFERENT FROM o23_stage.py, AND WHY. ORDER 23 landed three things at once: the derived
levels, the ND65+ CAP AMENDMENT (a code change in rl_model.py) and the re-signature of the selftest's
law check. Those are ALREADY LANDED on this branch -- `rl_model.py` reads `_ND65 = measured_k15`
verbatim, the retired `cap_against_curve_pick` key is already renamed, and the selftest already
asserts the retirement. **ORDER 25 has no code change at all.** It moves NUMBERS: the signed levels,
their two mirrors, and (via o24b_stage_surface.py, separately) the par and U literals.

Re-running o23_stage.py here would fail at its first assertion, correctly -- it asserts the
PRE-amendment state. This file asserts the POST-amendment state instead, so it cannot be run on a
tree that has not already had ORDER 23 landed.

WHAT IT WRITES, AND NOTHING ELSE:
  1. engine/rl_after/pvc_curve_v2.json      the signed pool_levels -- ORDER 25's derived fixed point.
                                            The `curve` block is NEVER touched (pick curve 0/64).
  2. ui/release_pick_curve.json             the provenance contract's pool_levels mirror and its
                                            pick_curve_file_md5, both of which the self-test binds.
  3. engine/rl_after/one_source_selftest.py the N43 literals RE-SIGNED to the new levels, and the
                                            contract md5 re-pinned. Structure untouched; the ND65+
                                            law check is ORDER 23's and is left exactly as it is.

WHAT IT DOES NOT WRITE: the store, any pickle, any instrument, `rl_model.py`, `_merged_recover.py`
(the par/U literals are o24b_stage_surface.py's job, carried), `data/model_config.json`, the board,
the book, or `data/expected_boot.json`.
"""
import sys, json, pathlib, hashlib, re

TREE = sys.argv[1]
LEV = json.load(open(sys.argv[2]))
RULING = "#334 comment 5267147448, owner ruling 2026-08-12 (the landing word)"


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def num(v):
    f = float(v)
    return int(f) if f == int(f) else round(f, 4)


# =====================================================================================
# 1. THE SIGNED TABLE
# =====================================================================================
cp = pathlib.Path(TREE + '/engine/rl_after/pvc_curve_v2.json')
doc = json.loads(cp.read_text())
pl = doc['pool_levels']
CURVE_BEFORE = json.dumps(doc['curve'], sort_keys=True)

assert set(LEV['signed_flat']) == set(pl['signed_flat']), "flat key set moved"
assert set(LEV['signed_rd_positional']) == set(pl['signed_rd_positional']), "rd positional key set moved"
# ORDER 23's amendment must ALREADY be landed on the tree this file is handed.
assert 'cap_against_curve_pick' not in pl['signed_nd65_plus'], \
    "the ND65+ cap key is still live -- this tree has not had ORDER 23 landed; refusing to stage"
assert 'cap_against_curve_pick_REMOVED_2026_08_12' in pl['signed_nd65_plus'], \
    "the retired ND65+ cap key is missing -- this tree is not the ORDER 23 landing"

before = dict(flat=dict(pl['signed_flat']), rd=dict(pl['signed_rd_positional']),
              nd65=pl['signed_nd65_plus']['measured_k15'])

DERIV = ("DERIVED, NOT PASTED, AND RE-DERIVED UNDER THE LANDED DELIVERY. These levels are the fixed "
         "point of ORDER 25's iterate-to-tolerance step, run on the engine that actually ships: "
         "current-state delivery at alpha=1.0 with the quality-conditioned premium "
         "M = (1-phi)*R + phi*(1 + q*(U-1)), q measured against a playing par shrunk toward the "
         "ALL-POOL SAME-DEPTH par at K=10 (the owner's amendment, %s). Each pathway's level is what "
         "it must be for that pathway's realised careers, valued through the engine's own "
         "walk-forward, to return the same value per point of ENTRY PRICE as the national draft's "
         "picks 1-64 (the measured ND-parity target, arm-split, re-measured fresh every round). "
         "Owner framing: THE PRICE IS AN OUTCOME OF THE CAREERS, NEVER A RATIO OF OLD PRICES -- at "
         "the fixed point the level that produced the matrix has washed out. Written as INTEGERS "
         "because rl_model.py builds its lookup with int(float(v)) and truncates. Evidence: "
         "docs/evidence/pool_landing_v2_2026-08-12/ (pre-registration, amended pars, U, the full "
         "iteration trajectory, controls and the shipping packet)." % RULING)

pl['signed_flat'] = {k: num(v) for k, v in LEV['signed_flat'].items()}
pl['signed_rd_positional'] = {k: num(v) for k, v in LEV['signed_rd_positional'].items()}
pl['_signed_flat_ruling_2026_08_12'] = (
    "THE SEVEN FLAT PATHWAY LEVELS, RE-DERIVED UNDER THE LANDED DELIVERY (%s). " % RULING + DERIV +
    " SUPERSEDED by this act -- ORDER 23's values (the #469 signature): " +
    " · ".join("%s %s" % (k, before['flat'][k]) for k in sorted(before['flat'])) +
    ". SUPERSEDED BEFORE THAT -- the 2026 N43 signature (#306 comment 5179992080): "
    "MSD 286.8 · SSP 252.8 · PDA 194.3 · PDS 145.0 · IRE 133.4 · PDN 123.0 · UNR 103.7.")
pl['_signed_rd_positional_ruling_2026_08_12'] = (
    "THE SIX ROOKIE-DRAFT POSITIONAL LEVELS, RE-DERIVED UNDER THE LANDED DELIVERY (%s). " % RULING +
    "Layer 2 of the same derivation: pathway x position, cells at n>=20 deriving on their own "
    "outcomes, thin cells borrowing the whole-pool positional shape at K=10, the unsampled remainder "
    "priced as its own residual group, and EVERY pathway renormalised after borrowing so the "
    "entry-weighted mean of the cells equals the pathway's all-in value exactly. SUPERSEDED by this "
    "act -- ORDER 23's values: " +
    " · ".join("%s %s" % (k, before['rd'][k]) for k in sorted(before['rd'])) +
    ". SUPERSEDED BEFORE THAT -- N43: KPD 300.3 · MID 294.8 · RUCK 282.5 · SD 246.9 · SF 231.5 · KPF 216.0.")

nd = pl['signed_nd65_plus']
nd['measured_k15'] = num(LEV['nd65_measured_k15'])
nd['_rule'] = (nd['_rule'] +
               "  [ORDER 25, %s: the cap stays REMOVED and the value below is ORDER 25's re-found "
               "fixed point under the landed delivery, superseding ORDER 23's %s. The amended law is "
               "min(measured fixed point, curve[64] chain) with the chain retired, which reads the "
               "derived level verbatim; the fixed point was re-found by iteration, not carried.]"
               % (RULING, before['nd65']))
pl['_pool_levels_ruling_2026_08_12'] = (
    "THE POOL UPDATE v2 (%s). Owner's word: \"Land\". The whole signed table above is replaced by "
    "ORDER 25's derived fixed point, measured on the LANDED delivery rather than on the delivery "
    "ORDER 23 measured. Three things sit under it, all already owner-ruled: H_POOLSIT/H_UNION retired "
    "to 1.0 (directive D8); the derived pool sit-out retention surface wired as the engine's source "
    "(ORDER 21); and the pool multiplier's current-state, quality-conditioned form (ORDERS 24/24B) "
    "with the par donor amended to the all-pool same-depth par. Layer 1 shrinks every pathway "
    "uniformly at K=15 toward the whole-pool aggregate (owner verbatim, 2026-08-12: \"K=15 was across "
    "the board, not PDS\"); layer 2 is wirable for the rookie draft alone, which is a limit of this "
    "table's structure and an open owner question, not a silence. %s" % (RULING, DERIV))
cp.write_text(json.dumps(doc, indent=1) + "\n")
CURVE_MD5 = md5(cp)

# THE PICK CURVE IS UNTOUCHED -- asserted on the bytes, not claimed.
after_doc = json.loads(cp.read_text())
assert json.dumps(after_doc['curve'], sort_keys=True) == CURVE_BEFORE, \
    "THE PICK CURVE MOVED -- this act writes pool_levels and nothing else"

print("  [1] SIGNED TABLE WRITTEN  (engine truncates to int; these are integers, so the cost is 0.000%)")
print("      %-10s %10s %10s %10s" % ('key', 'before', 'written', 'engine int'))
for k in sorted(before['flat']):
    print("      %-10s %10s %10s %10d" % (k, before['flat'][k], pl['signed_flat'][k],
                                          int(float(pl['signed_flat'][k]))))
for k in sorted(before['rd']):
    print("      RD:%-7s %10s %10s %10d" % (k, before['rd'][k], pl['signed_rd_positional'][k],
                                            int(float(pl['signed_rd_positional'][k]))))
print("      %-10s %10s %10s %10d   [cap already REMOVED by ORDER 23 -- the derived level IS the price]"
      % ('ND65+', before['nd65'], nd['measured_k15'], int(float(nd['measured_k15']))))
print("      pick curve block: UNCHANGED (asserted on bytes)")
print("      pvc_curve_v2.json md5 -> %s" % CURVE_MD5)

# =====================================================================================
# 2. THE UI PROVENANCE CONTRACT -- the mirror the self-test binds
# =====================================================================================
up = pathlib.Path(TREE + '/ui/release_pick_curve.json')
uc = json.loads(up.read_text())
uc['pool_levels'] = json.loads(json.dumps(pl))
uc['pick_curve_file_md5'] = CURVE_MD5
uc['_pool_levels_note'] = (uc['_pool_levels_note'] +
                           "  [ORDER 25, %s: the mirrored block now carries the RE-TRUED pool levels "
                           "measured on the landed delivery. It is still a verbatim mirror -- the "
                           "artifact remains the one authority -- and pick_curve_file_md5 moves with "
                           "the artifact's bytes in this same commit.]" % RULING)
up.write_text(json.dumps(uc, indent=1) + "\n")
CONTRACT_MD5 = md5(up)
print("  [2] ui/release_pick_curve.json mirrored   md5 -> %s" % CONTRACT_MD5)

# =====================================================================================
# 3. THE N43 SIGNATURE, RE-SIGNED (the artifact cannot be its own authority)
# =====================================================================================
sp = pathlib.Path(TREE + '/engine/rl_after/one_source_selftest.py')
s = sp.read_text()
F = pl['signed_flat']; R = pl['signed_rd_positional']

OLD_FLAT = re.search(r"^_N43_FLAT=\{.*\}$", s, re.M)
OLD_RD = re.search(r"^_N43_RD=\{.*\}$", s, re.M)
OLD_ND = re.search(r"^_N43_ND65_K15=[0-9.]+;", s, re.M)
assert OLD_FLAT and OLD_RD and OLD_ND, "the N43 literal block is not where it was"
NEW_FLAT = ("_N43_FLAT={'MSD':%s,'SSP':%s,'PDA':%s,'PDS':%s,'IRE':%s,'PDN':%s,'UNR':%s}"
            % (F['MSD'], F['SSP'], F['PDA'], F['PDS'], F['IRE'], F['PDN'], F['UNR']))
NEW_RD = ("_N43_RD={'KPD':%s,'MID':%s,'RUCK':%s,'SD':%s,'SF':%s,'KPF':%s}"
          % (R['KPD'], R['MID'], R['RUCK'], R['SD'], R['SF'], R['KPF']))
NEW_ND = "_N43_ND65_K15=%s;" % nd['measured_k15']
s = s[:OLD_FLAT.start()] + NEW_FLAT + s[OLD_FLAT.end():]
OLD_RD = re.search(r"^_N43_RD=\{.*\}$", s, re.M)
s = s[:OLD_RD.start()] + NEW_RD + s[OLD_RD.end():]
OLD_ND = re.search(r"^_N43_ND65_K15=[0-9.]+;", s, re.M)
s = s[:OLD_ND.start()] + NEW_ND + s[OLD_ND.end():]

OLD_CM = re.search(r"^    _contract_md5='([0-9a-f]{32})'.*$", s, re.M)
assert OLD_CM, "the contract md5 pin is not where it was"
prev_cm = OLD_CM.group(1)
s = s[:OLD_CM.start()] + ("    _contract_md5='%s'   # RE-PINNED by #334 ORDER 25 (THE POOL\n"
                          "    # UPDATE v2: the re-trued pool levels move the artifact's bytes, so the contract's\n"
                          "    # mirror and its pick_curve_file_md5 move with them, and this pin moves in the same\n"
                          "    # commit exactly as prior acts did). PREVIOUS PIN: %s, which was\n"
                          "    # RE-PINNED by #334 ORDER 23 (the pool"
                          % (CONTRACT_MD5, prev_cm)) + s[OLD_CM.end():]
sp.write_text(s)
print("  [3] one_source_selftest.py RE-SIGNED   md5 -> %s" % md5(sp))
print("  STAGED: pvc_curve_v2 %s · contract %s" % (CURVE_MD5[:8], CONTRACT_MD5[:8]))
