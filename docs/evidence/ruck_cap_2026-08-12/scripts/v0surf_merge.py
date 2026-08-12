"""ORDER 20C — build the v0surf pickle the NO-CAP arm needs, WITHOUT changing a single surface value.

WHY THIS IS NEEDED
  `RL_RUC_PRIOR_CAP` is a member of `_V0SURF_GATES` (`_merged_recover.py:1323`), so it enters
  `_v0surf_sig`. Move the cap and the build computes a signature that is not in `data/v0surf.pkl`, and
  `_merged_recover.py:1416` HALTs rather than silently re-fitting (measured: signature `2dff9ca1…`,
  prereg P3). The halt is correct — it is the freeze doing its job — but the no-cap arm cannot be built
  until the frozen surfaces are also reachable under the cap-99 signature.

WHAT THIS DOES, AND WHAT IT REFUSES TO DO
  Reads two `v0surf_fit_one.py` dumps — one declared refit at the shipped cap, one at cap 99 — purely
  to LEARN which signatures the cap-99 build will ask for. It pairs the cap-99 entries to the cap-1.4
  entries **by value**, and requires **exact** equality; a single differing float HALTs, because that
  would mean the ruck cap reaches the V0 surface and the re-keying would be a lie.

  It then writes: the ORIGINAL frozen entries, PLUS those same original objects re-keyed under the
  cap-99 signatures. The refit's own arrays are used only for the equality check and are discarded.
  The no-cap board therefore reads the SHIPPED surfaces, byte-for-byte, like every other board.

Usage: python3 v0surf_merge.py <fit_lo.pkl> <fit_hi.pkl> <frozen.pkl> <merged.pkl>
"""
import sys, json, pickle
import numpy as np

FIT_LO, FIT_HI, FROZEN, OUT = sys.argv[1:5]
lo = pickle.load(open(FIT_LO, 'rb'))
hi = pickle.load(open(FIT_HI, 'rb'))
frozen = pickle.load(open(FROZEN, 'rb'))
built_lo, built_hi = lo['built'], hi['built']


def flat(entry):
    """Every float in one surface entry, in a fixed order, for exact comparison."""
    out = []
    for part in ('c18', 'surfN', 'surfR'):
        d = entry[part]
        for k in sorted(d, key=repr):
            out.append((part, repr(k), tuple(float(x) for x in np.asarray(d[k]).ravel())))
    return out


print("frozen keys          : %s" % sorted(frozen))
print("refit @cap=%-6s    : %s   (shipped %s)" % (lo['cap'], sorted(built_lo), lo['shipped_sig'][:12]))
print("refit @cap=%-6s    : %s   (shipped %s)" % (hi['cap'], sorted(built_hi), hi['shipped_sig'][:12]))

# CHECK 1 — the refit at the shipped cap reproduces the FROZEN key set exactly.
assert sorted(built_lo) == sorted(frozen), "refit@%s keys != frozen keys — the re-keying premise is gone" % lo['cap']

# CHECK 2 — every frozen entry is value-identical to its refit counterpart on this box. (The committed
# --verify already showed the pickled payload md5 reproduces the pin; this restates it per surface.)
for k in frozen:
    assert flat(frozen[k]) == flat(built_lo[k]), "frozen[%s] != refit@%s[%s]" % (k[:12], lo['cap'], k[:12])
print("CHECK: frozen == refit@%s, value-for-value, on all %d entries." % (lo['cap'], len(frozen)))

# CHECK 3 — pair cap-99 to cap-1.4 BY VALUE and require exactly one match each.
lo_flat = {k: flat(v) for k, v in built_lo.items()}
hi_flat = {k: flat(v) for k, v in built_hi.items()}
pairing = {}
for hk, hv in hi_flat.items():
    match = [lk for lk, lv in lo_flat.items() if lv == hv]
    if len(match) != 1:
        raise SystemExit("HALT: cap-%s surface %s matches %d cap-%s surfaces (expected exactly 1). The ruck "
                         "cap reaches the V0 surface; the frozen artifact cannot be re-keyed and this "
                         "measurement stops here." % (hi['cap'], hk[:12], len(match), lo['cap']))
    pairing[hk] = match[0]
assert len(set(pairing.values())) == len(pairing), "two cap-99 signatures paired to the same cap-1.4 one"
print("PAIRING (cap-%s signature -> the cap-%s signature whose surfaces it EQUALS, value-for-value):" % (hi['cap'], lo['cap']))
for hk, lk in sorted(pairing.items()):
    print("   %s  ->  %s   IDENTICAL%s" % (hk, lk, ' (same key)' if hk == lk else ''))

# WRITE — frozen entries + the SAME OBJECTS re-keyed under the cap-99 signatures.
merged = dict(frozen)
added = []
for hk, lk in pairing.items():
    if hk in merged:
        continue
    merged[hk] = frozen[lk]
    added.append((hk, lk))
with open(OUT, 'wb') as f:
    pickle.dump(merged, f, protocol=pickle.DEFAULT_PROTOCOL)
print("MERGED -> %s   keys %d (was %d; added %d)" % (OUT, len(merged), len(frozen), len(added)))
for hk, lk in sorted(added):
    print("   ADDED %s  = frozen[%s]  (the shipped surface, re-keyed only)" % (hk, lk))
json.dump({'frozen_keys': sorted(frozen), 'refit_lo_keys': sorted(built_lo), 'refit_hi_keys': sorted(built_hi),
           'cap_lo': lo['cap'], 'cap_hi': hi['cap'], 'pairing': pairing,
           'added': [{'cap_hi_sig': a, 'source_frozen_sig': b} for a, b in added]},
          open(OUT + '.json', 'w'), indent=1)
