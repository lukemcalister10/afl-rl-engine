#!/usr/bin/env python3
"""ORDER 23 -- RETIRE H_POOLSIT AND H_UNION TO 1.0 AS SHIPPED DEFAULTS.

  usage: o23_land_config.py <tree>

The third lever of the pool update, and the only one that is a configuration change rather than a
derivation. Owner ruling, directive D8 (#334 comment 5253173347): *"the pool sitter on top penalty
should go, and the pool index should be rederived in the same way the ND one is where possible"*.
The two surviving ITEM H cells are the "on top penalty": they multiply the FINISHED price of a pool
sitter, on top of the retention the pool surface now derives from pool history. Retiring them and
wiring the derived surface are one act, which is why they land together.

IT WRITES IN BOTH PLACES A DEFAULT LIVES, which is what "shipped default" means here:
  data/model_config.json          the manifest value gate/bake mode pins (and its var_notes)
  engine/rl_after/_merged_recover.py   the code default a non-gate run would otherwise read

Following the ORDER 9 precedent for H_MATNONRD exactly (retired to 1.0 in both places, with the
ruling recorded beside the number). The config hash is recomputed from the manifest vars, so the
expected_boot `config` pin moves in the same act -- asserted by the restamp, never assumed.
"""
import sys, json, pathlib

TREE = sys.argv[1]
sys.path.insert(0, TREE)
import config_manifest as CM

RULING = ("RETIRED TO 1.0 BY OWNER RULING, directive D8 (#334 comment 5253173347), landed by ORDER 23 "
          "with the derived pool retention surface and the derived pool entry levels as ONE act. "
          "OWNER, VERBATIM: \"the pool sitter on top penalty should go, and the pool index should be "
          "rederived in the same way the ND one is where possible not for pick 65, but for the pool\". "
          "THE GROUNDS: this cell was a flat END-multiplier on the finished production-led price of a "
          "pool sitter, reading only _pool / type / draft age and never games, level or establishment "
          "-- exactly the shape of cut the same ruling retired H_MATNONRD for. What replaces it is not "
          "nothing: the pool sit-out retention is now DERIVED from pool history "
          "(engine/rl_after/pool_retention_surface.json) and applied at the v0/prior side, which is the "
          "owner's own stated design direction for a pool discount. Kill-switch behaviour is unchanged: "
          "RL_ITEM_H=0 still disables the composed factor entirely. PREVIOUS VALUE: %s.")

m = pathlib.Path(TREE + '/data/model_config.json')
d = json.loads(m.read_text())
before = {k: d['vars'][k] for k in ('RL_H_POOLSIT', 'RL_H_UNION')}
for k in ('RL_H_POOLSIT', 'RL_H_UNION'):
    d['vars'][k] = '1.0'
    d['var_notes'][k] = RULING % before[k]
m.write_text(json.dumps(d, indent=1) + "\n")
H = CM.canonical_hash(CM.load(TREE)['vars'])
d = json.loads(m.read_text()); d['config_sha256'] = H
m.write_text(json.dumps(d, indent=1) + "\n")
print("  [C] manifest: RL_H_POOLSIT %s -> 1.0 · RL_H_UNION %s -> 1.0" % (before['RL_H_POOLSIT'], before['RL_H_UNION']))
print("      config_sha256 -> %s" % H)

f = pathlib.Path(TREE + '/engine/rl_after/_merged_recover.py')
s = f.read_text()
OLD = ("H_UNION=float(os.environ.get('RL_H_UNION','0.280'))\n"
       "H_POOLSIT=float(os.environ.get('RL_H_POOLSIT','0.804'))\n")
NEW = ("# ===== #334 ORDER 23 -- THE LAST TWO ITEM H CELLS ARE RETIRED TO 1.0 (owner ruling, directive D8,\n"
       "# comment 5253173347; landed 2026-08-12 with the derived pool retention surface and the derived\n"
       "# pool entry levels, as ONE act -- the three levers are separated in the movers ledger, not in time).\n"
       "# OWNER, VERBATIM: \"the pool sitter on top penalty should go, and the pool index should be rederived\n"
       "# in the same way the ND one is where possible not for pick 65, but for the pool\".\n"
       "# SUPERSEDED SHIPPED DEFAULTS, preserved here as history: H_UNION 0.280 · H_POOLSIT 0.804. Both were\n"
       "# flat END-multipliers on the finished price of a pool sitter, reading only _pool / type / draft age\n"
       "# and never games, level or establishment -- the same shape of cut the same ruling retired\n"
       "# H_MATNONRD for, and the reason the union factor composed to an 86%% cut on a row in both cells.\n"
       "# WHAT REPLACES THEM IS NOT NOTHING: the pool sit-out retention is now DERIVED from pool history\n"
       "# (engine/rl_after/pool_retention_surface.json, wired at both pool read sites below) and applied on\n"
       "# the v0/prior side, which is the owner's own recorded design direction for a pool discount.\n"
       "# The manifest carries the same 1.0 in data/model_config.json; this is the non-gate default.\n"
       "H_UNION=float(os.environ.get('RL_H_UNION','1.0'))\n"
       "H_POOLSIT=float(os.environ.get('RL_H_POOLSIT','1.0'))\n")
assert s.count(OLD) == 1, "the H default site is not where it was"
f.write_text(s.replace(OLD, NEW))
print("  [C] engine defaults retired to 1.0 in _merged_recover.py")
