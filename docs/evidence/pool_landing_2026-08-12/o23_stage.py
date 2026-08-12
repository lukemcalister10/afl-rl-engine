#!/usr/bin/env python3
"""ORDER 23 -- THE POOL-UPDATE STAGER. One script, used for BOTH jobs, which is the point.

  usage: o23_stage.py <tree> <levels.json>

Applied to a SCRATCHPAD WORKTREE during the iteration, and applied to the LANDING TREE when the
iteration has converged. Because it is the same script and the same bytes, the landing tree IS the
staged tree, and the two boards are byte-identical BY CONSTRUCTION rather than by hope. That identity
is still verified by rebuild, never assumed.

WHAT IT WRITES, AND NOTHING ELSE:

  1. engine/rl_after/pvc_curve_v2.json      the signed pool_levels -- the final DERIVED levels, and the
                                            AMENDED signed_nd65_plus law. Every block annotated with
                                            its owner ruling and date; the superseded cap text is
                                            PRESERVED as history, never deleted.
  2. engine/rl_after/rl_model.py            the one code amendment: `_ND65 = min(measured_k15,
                                            curve[64])` becomes `_ND65 = measured_k15`.
  3. ui/release_pick_curve.json             the provenance contract's pool_levels mirror and its
                                            pick_curve_file_md5, both of which the self-test binds.
  4. engine/rl_after/one_source_selftest.py the N43 literals RE-SIGNED, the ND65+ check rewritten to
                                            the amended law, and the contract md5 re-pinned. The
                                            selftest's structure is kept exactly; only the values and
                                            the one law it asserts move, each with a dated annotation.

WHAT IT DOES NOT WRITE: the store, any pickle, any instrument, _merged_recover.py (that is
o21_patch.py's job, carried verbatim), data/model_config.json (the H dials are the caller's), the
board, the book, or data/expected_boot.json.

THE ND>64 AMENDMENT, IN THE OWNER'S OWN WORDS (#334 comment 5262928754, 2026-08-12):
    "Happy to amend the law for ND > 64. As it's not going to impact many players anymore, only
     historical ones, as the ND never goes beyond pick 64 these days. So very few live players draw
     from that, and those who do would either have been delisted or have production determine their
     price now."
"""
import sys, json, pathlib, hashlib

TREE = sys.argv[1]
LEV = json.load(open(sys.argv[2]))
RULING = "#334 comment 5262928754, owner ruling 2026-08-12"


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

assert set(LEV['signed_flat']) == set(pl['signed_flat']), "flat key set moved"
assert set(LEV['signed_rd_positional']) == set(pl['signed_rd_positional']), "rd positional key set moved"

OLD_RULE = pl['signed_nd65_plus'].get('_rule')
assert OLD_RULE and 'CAP IS A LAW' in OLD_RULE, "the superseded ND65+ law text is not where it was"
OLD_CAPPK = int(pl['signed_nd65_plus']['cap_against_curve_pick'])

before = dict(flat=dict(pl['signed_flat']), rd=dict(pl['signed_rd_positional']),
              nd65=pl['signed_nd65_plus']['measured_k15'])

DERIV = ("DERIVED, NOT PASTED. These levels are the fixed point of ORDER 23's iterate-to-tolerance "
         "step: each pathway's level is what it must be for that pathway's realised careers, valued "
         "through the engine's own walk-forward, to return the same value per point of ENTRY PRICE "
         "as the national draft's picks 1-64 (the measured ND-parity target, arm-split). Owner "
         "framing, ruled at %s: THE PRICE IS AN OUTCOME OF THE CAREERS, NEVER A RATIO OF OLD PRICES "
         "-- at the fixed point the level that produced the matrix has washed out. Written as "
         "INTEGERS because rl_model.py builds its lookup with int(float(v)) and truncates: the signed "
         "table and the engine's table are now the same object. Evidence: "
         "docs/evidence/pool_landing_2026-08-12/ (iteration, controls and verification) and "
         "docs/evidence/pool_final_2026-08-12/SHIPPING_PACKET.md (the derivation this converges)." % RULING)

pl['signed_flat'] = {k: num(v) for k, v in LEV['signed_flat'].items()}
pl['signed_rd_positional'] = {k: num(v) for k, v in LEV['signed_rd_positional'].items()}
pl['_signed_flat_ruling_2026_08_12'] = (
    "THE SEVEN FLAT PATHWAY LEVELS, RE-DERIVED AND OWNER-RULED (%s). " % RULING + DERIV +
    " Superseded N43 values (2026 signature, #306 comment 5179992080): " +
    " · ".join("%s %.1f" % (k, float(before['flat'][k])) for k in sorted(before['flat'])) + ".")
pl['_signed_rd_positional_ruling_2026_08_12'] = (
    "THE SIX ROOKIE-DRAFT POSITIONAL LEVELS, RE-DERIVED AND OWNER-RULED (%s). " % RULING +
    "Layer 2 of the same derivation: pathway x position, cells at n>=20 deriving on their own "
    "outcomes, thin cells borrowing the whole-pool positional shape at K=10, the unsampled remainder "
    "priced as its own residual group, and EVERY pathway renormalised after borrowing so the "
    "entry-weighted mean of the cells equals the pathway's all-in value exactly. Superseded N43 "
    "values: " + " · ".join("%s %.1f" % (k, float(before['rd'][k])) for k in sorted(before['rd'])) + ".")

pl['signed_nd65_plus'] = {
    "_rule": ("AMENDED %s: THE CAP IS REMOVED. ND65+ prices at its DERIVED level -- `measured_k15`, "
              "read verbatim, exactly like every other signed division. There is no min against the "
              "pick curve any more. OWNER, VERBATIM: \"Happy to amend the law for ND > 64. As it's not "
              "going to impact many players anymore, only historical ones, as the ND never goes beyond "
              "pick 64 these days. So very few live players draw from that, and those who do would "
              "either have been delisted or have production determine their price now.\" GROUNDS ON "
              "THE RECORD: ORDER 22 measured this pathway returning 1.53x the target and measured the "
              "cap to be the SOLE cause of the residual on every other pathway (pool aggregate 1.0389 "
              "with it, 0.9969 without). CONSEQUENCE ACCEPTED BY THE OWNER: a post-64 selection may now "
              "price above pick 64's curve value; the draft-boundary tension the cap guarded is queued "
              "for the pick-curve re-derivation." % RULING),
    "_rule_SUPERSEDED_2026_08_12": OLD_RULE,
    "_cap_removal_note": ("The cap's pick is preserved below under a RETIRED key name rather than "
                          "deleted, so the history stays readable AND any code still reaching for "
                          "`cap_against_curve_pick` fails loudly instead of silently re-capping. "
                          "rl_model.py's read site carries the same amendment and the same history."),
    "cap_against_curve_pick_REMOVED_2026_08_12": OLD_CAPPK,
    "measured_k15": num(LEV['nd65_measured_k15']),
}
pl['_pool_levels_ruling_2026_08_12'] = (
    "THE POOL UPDATE (%s). The whole signed table above is replaced by ORDER 23's derived fixed "
    "point, landed together with two other levers in one act: H_POOLSIT/H_UNION retired to 1.0 "
    "(directive D8) and the derived pool sit-out retention surface wired as the engine's source. "
    "Layer 1 shrinks every pathway uniformly at K=15 toward the whole-pool aggregate (owner verbatim, "
    "2026-08-12: \"K=15 was across the board, not PDS\"); layer 2 is wirable for the rookie draft "
    "alone, which is a limit of this table's structure and an open owner question, not a silence. "
    "%s" % (RULING, DERIV))
cp.write_text(json.dumps(doc, indent=1) + "\n")
CURVE_MD5 = md5(cp)

print("  [1] SIGNED TABLE WRITTEN  (engine truncates to int; these are integers, so the cost is 0.000%)")
print("      %-10s %10s %10s %10s" % ('key', 'before', 'written', 'engine int'))
for k in sorted(before['flat']):
    print("      %-10s %10.1f %10s %10d" % (k, float(before['flat'][k]), pl['signed_flat'][k],
                                            int(float(pl['signed_flat'][k]))))
for k in sorted(before['rd']):
    print("      RD:%-7s %10.1f %10s %10d" % (k, float(before['rd'][k]), pl['signed_rd_positional'][k],
                                              int(float(pl['signed_rd_positional'][k]))))
print("      %-10s %10.1f %10s %10d   [CAP REMOVED -- the derived level IS the price]"
      % ('ND65+', float(before['nd65']), pl['signed_nd65_plus']['measured_k15'],
         int(float(pl['signed_nd65_plus']['measured_k15']))))
print("      pvc_curve_v2.json md5 -> %s" % CURVE_MD5)

# =====================================================================================
# 2. THE ONE CODE AMENDMENT
# =====================================================================================
rp = pathlib.Path(TREE + '/engine/rl_after/rl_model.py')
src = rp.read_text()

OLD_READ = ("_ND65=min(float(_PL_DOC['signed_nd65_plus']['measured_k15']),\n"
            "          float(_PVC2M[int(_PL_DOC['signed_nd65_plus']['cap_against_curve_pick'])]))\n")
NEW_READ = (
    "# ===== #334 ORDER 23 -- THE ND65+ CAP IS AMENDED AWAY (owner ruling, %s) ======================\n"
    "# OWNER, VERBATIM: \"Happy to amend the law for ND > 64. As it's not going to impact many players\n"
    "# anymore, only historical ones, as the ND never goes beyond pick 64 these days. So very few live\n"
    "# players draw from that, and those who do would either have been delisted or have production\n"
    "# determine their price now.\"\n"
    "# THE SUPERSEDED LAW, PRESERVED HERE AS HISTORY RATHER THAN DELETED:\n"
    "#     _ND65 = min(measured_k15, _PVC2M[cap_against_curve_pick])    # \"THE CAP IS A LAW, NOT A NUMBER\"\n"
    "# It held a post-64 selection at the curve's pick-64 value so a pick-65 row could never outprice\n"
    "# pick 64. ORDER 22 measured that this one blocked pathway was the SOLE cause of the residual on\n"
    "# every other pathway. The owner removed it on the grounds above and accepted the consequence; the\n"
    "# draft-boundary tension it guarded is queued for the pick-curve re-derivation. The signed block's\n"
    "# `cap_against_curve_pick` key is retired under a dated name, so this file cannot silently re-cap.\n"
    "# ND65+ NOW PRICES AT ITS DERIVED LEVEL, READ VERBATIM, LIKE EVERY OTHER SIGNED DIVISION.\n"
    "_ND65=float(_PL_DOC['signed_nd65_plus']['measured_k15'])\n" % RULING)
assert src.count(OLD_READ) == 1, "the ND65+ cap read site is not where it was (%d)" % src.count(OLD_READ)
src = src.replace(OLD_READ, NEW_READ)

OLD_PRT = ("print('#326 POOL LEVELS (N43 signed, read verbatim, LADDER currency; "
           "ND65+ = min(%.1f, curve[%d]=%d) = %d): %s'\n")
NEW_PRT = ("print('#326 POOL LEVELS (N43 signed, read verbatim, LADDER currency; ND65+ = %.1f DERIVED, "
           "the cap against curve[%d]=%d REMOVED by owner ruling 2026-08-12 -> %d): %s'\n")
assert src.count(OLD_PRT) == 1, "the pool-levels print site is not where it was"
src = src.replace(OLD_PRT, NEW_PRT)
rp.write_text(src)
print("  [2] rl_model.py AMENDED: _ND65 = measured_k15 (cap removed)   md5 -> %s" % md5(rp))

# =====================================================================================
# 3. THE UI PROVENANCE CONTRACT -- the mirror the self-test binds
# =====================================================================================
up = pathlib.Path(TREE + '/ui/release_pick_curve.json')
uc = json.loads(up.read_text())
uc['pool_levels'] = json.loads(json.dumps(pl))
uc['pick_curve_file_md5'] = CURVE_MD5
uc['_pool_levels_note'] = (uc['_pool_levels_note'] +
                           "  [ORDER 23, %s: the mirrored block now carries the DERIVED pool levels and the "
                           "AMENDED ND65+ law (cap removed). It is still a verbatim mirror -- the artifact "
                           "remains the one authority -- and pick_curve_file_md5 moves with the artifact's "
                           "bytes in this same commit.]" % RULING)
up.write_text(json.dumps(uc, indent=1) + "\n")
CONTRACT_MD5 = md5(up)
print("  [3] ui/release_pick_curve.json mirrored   md5 -> %s" % CONTRACT_MD5)

# =====================================================================================
# 4. THE N43 SIGNATURE, RE-SIGNED (the packet's flag d -- adoption requires it)
# =====================================================================================
sp = pathlib.Path(TREE + '/engine/rl_after/one_source_selftest.py')
s = sp.read_text()

OLD_LIT = ("_N43_FLAT={'MSD':286.8,'SSP':252.8,'PDA':194.3,'PDS':145.0,'IRE':133.4,'PDN':123.0,'UNR':103.7}\n"
           "_N43_RD={'KPD':300.3,'MID':294.8,'RUCK':282.5,'SD':246.9,'SF':231.5,'KPF':216.0}\n"
           "_N43_ND65_K15=266.1; ")
F = pl['signed_flat']; R = pl['signed_rd_positional']
NEW_LIT = (
    "# ===== RE-SIGNED BY #334 ORDER 23 (owner ruling, %s) ==========================================\n"
    "# The literals below are no longer the 2026 N43 signature -- they are the POOL UPDATE's derived\n"
    "# fixed point, and they are written out here for exactly the reason the original ones were: the\n"
    "# artifact cannot be its own authority. THE SUPERSEDED SIGNATURE, kept as history:\n"
    "#   _N43_FLAT={'MSD':286.8,'SSP':252.8,'PDA':194.3,'PDS':145.0,'IRE':133.4,'PDN':123.0,'UNR':103.7}\n"
    "#   _N43_RD={'KPD':300.3,'MID':294.8,'RUCK':282.5,'SD':246.9,'SF':231.5,'KPF':216.0}\n"
    "#   _N43_ND65_K15=266.1, capped against curve[64]\n"
    "# The four reference quantities below it (rd_division_level, rd_positional_shrink_target,\n"
    "# measured_pool_aggregate, K) are N43 CONSTRUCTION constants, are unchanged in the artifact, and\n"
    "# are therefore unchanged here.\n"
    "_N43_FLAT={'MSD':%s,'SSP':%s,'PDA':%s,'PDS':%s,'IRE':%s,'PDN':%s,'UNR':%s}\n"
    "_N43_RD={'KPD':%s,'MID':%s,'RUCK':%s,'SD':%s,'SF':%s,'KPF':%s}\n"
    "_N43_ND65_K15=%s; " % (RULING, F['MSD'], F['SSP'], F['PDA'], F['PDS'], F['IRE'], F['PDN'], F['UNR'],
                            R['KPD'], R['MID'], R['RUCK'], R['SD'], R['SF'], R['KPF'],
                            pl['signed_nd65_plus']['measured_k15']))
assert s.count(OLD_LIT) == 1, "the N43 literal block is not where it was"
s = s.replace(OLD_LIT, NEW_LIT)

OLD_CHK = """    check(float(_pl['signed_nd65_plus']['measured_k15'])==_N43_ND65_K15
          and int(_pl['signed_nd65_plus']['cap_against_curve_pick'])==MA.ND_CURVE_LAST,
          "#326 ND65+ is stored as the LAW: measured %.1f capped against curve pick %d (never a literal price)"
          %(float(_pl['signed_nd65_plus']['measured_k15']),int(_pl['signed_nd65_plus']['cap_against_curve_pick'])))
"""
NEW_CHK = """    # #334 ORDER 23 (owner ruling 2026-08-12): THE CAP IS REMOVED and ND65+ prices at its derived
    # level. The check keeps its job -- the artifact still cannot be its own authority -- and now also
    # asserts the RETIREMENT: the live key must be GONE and the dated historical key must be present,
    # so a silent restoration of the cap goes red here.
    check(float(_pl['signed_nd65_plus']['measured_k15'])==_N43_ND65_K15
          and 'cap_against_curve_pick' not in _pl['signed_nd65_plus']
          and int(_pl['signed_nd65_plus']['cap_against_curve_pick_REMOVED_2026_08_12'])==MA.ND_CURVE_LAST,
          "#326/ORDER23 ND65+ prices at its DERIVED level %.1f; the min-against-curve[%d] cap is REMOVED "
          "(owner ruling 2026-08-12) and preserved only as dated history"
          %(float(_pl['signed_nd65_plus']['measured_k15']),MA.ND_CURVE_LAST))
"""
assert s.count(OLD_CHK) == 1, "the ND65+ law check is not where it was"
s = s.replace(OLD_CHK, NEW_CHK)

OLD_WANT = "    _want['ND65+']=int(min(_N43_ND65_K15,float(MA._PVC2M[MA.ND_CURVE_LAST])))\n"
NEW_WANT = ("    _want['ND65+']=int(_N43_ND65_K15)   # ORDER 23: UNCAPPED -- the derived level itself\n")
assert s.count(OLD_WANT) == 1, "the resolved-table expectation is not where it was"
s = s.replace(OLD_WANT, NEW_WANT)

OLD_MSG = ('          "#326 the engine\'s resolved pool levels == the signed table '
           '(ND65+ = min(%.1f, curve[%d]=%d) = %d)"\n')
NEW_MSG = ('          "#326 the engine\'s resolved pool levels == the signed table '
           '(ND65+ = %.1f DERIVED, curve[%d]=%d NOT applied -> %d)"\n')
assert s.count(OLD_MSG) == 1, "the resolved-table message is not where it was"
s = s.replace(OLD_MSG, NEW_MSG)

OLD_CM = "    _contract_md5='eae593f220460d880be20da38e3de39d'   # RE-PINNED by #326"
NEW_CM = ("    _contract_md5='%s'   # RE-PINNED by #334 ORDER 23 (the pool\n"
          "    # update: derived pool levels + the amended ND65+ law move the artifact's bytes, so the\n"
          "    # contract's mirror and its pick_curve_file_md5 move with them, and this pin moves in the\n"
          "    # same commit exactly as prior acts did). PREVIOUS PIN: eae593f220460d880be20da38e3de39d,\n"
          "    # which was RE-PINNED by #326" % CONTRACT_MD5)
assert s.count(OLD_CM) == 1, "the contract md5 pin is not where it was"
s = s.replace(OLD_CM, NEW_CM)
sp.write_text(s)
print("  [4] one_source_selftest.py RE-SIGNED   md5 -> %s" % md5(sp))
print("  STAGED: pvc_curve_v2 %s · contract %s" % (CURVE_MD5[:8], CONTRACT_MD5[:8]))
