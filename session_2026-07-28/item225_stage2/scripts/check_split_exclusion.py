"""ITEM 225 STAGE 2 — THE CHECK THAT DECIDES WHETHER THIS JOB SUCCEEDED.

Addendum 1 §B requires the exclusion to run BOTH WAYS and the check to prove both. Addendum 2 §2
records that only one direction exists on `main` — "no pool row teaches the national curve", five
in-engine fit sites registering their actual sampled rows, seam-verified to fail by name. The other
direction is this seat's, to the same standard.

AND (owner ruling, 2026-07-28) IT MUST CATCH CONTAMINATION THROUGH THE POOLING TERM, NOT ONLY
THROUGH THE SAMPLED ROWS. A pooled average computed over the combined population and blended into a
prior is a row from the other population teaching that fit, by a quieter route. The priors blend
w*posfit + (1-w)*pool with w = min(n_pos/200,1)*0.6 <= 0.6, so AT LEAST 40% of every prior is the
pooled term. Cross that term and every sampled row stays clean while the fit is taught by the other
population — a sampled-rows check reads green throughout. That is the same shape as the defect #217
shipped once (a check watching its own copy of the rule rather than what the fit consumed), and it
is why this check reads the RECORDED populations rather than re-deriving them.

WHAT IT ASSERTS, per fit site, on the rows THAT SITE ACTUALLY CONSUMED:
  (a) every expected site registered both a 'sample' and a 'pooling' population
      — deleting a registration must not buy silence
  (b) ND sites  : no pool row in the sample, and none in the pooling term
  (c) POOL sites: no national 1-64 row in the sample, and none in the pooling term

NON-VACUITY. Run with --prove-fails: the derivation is re-run once per (site x kind), each time with
that one population crossed, and the check must FAIL NAMING THAT SITE AND THAT KIND every time. A
check that cannot fail proves nothing.
"""
import os, sys, json, subprocess
from collections import Counter

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
BASE = REPO + '/session_2026-07-28/item225_stage2'
DERIVE = BASE + '/scripts/derive_split.py'
PER = BASE + '/out/per_entrant_split.json'

ND_SITES   = ('nd_curve', 'priors_ND_1_64')     # must never see a POOL row
POOL_SITES = ('pool_level', 'priors_POOL')      # must never see a NATIONAL 1-64 row
ALL_SITES  = ND_SITES + POOL_SITES
KINDS      = ('sample', 'pooling')

_fails = []
def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: _fails.append(msg)


def classify(recs):
    """The two truth sets, taken from the engine's OWN predicates as emitted (is_pool / type),
    never re-derived here."""
    pool_keys, nd_keys = set(), set()
    for r in recs:
        k = r['key'] or r['player']
        if r['is_pool']: pool_keys.add(k)
        elif r['type'] == 'ND': nd_keys.add(k)
    return pool_keys, nd_keys


def run_check(derived, recs, label):
    pool_keys, nd_keys = classify(recs)
    obs = derived.get('fit_observations') or {}
    print("\n--- %s ---" % label)

    # (a) registration completeness
    missing = [(s, k) for s in ALL_SITES for k in KINDS if k not in (obs.get(s) or {})]
    check(not missing, "every fit site registered BOTH its sample and its pooling population "
                       "(missing: %s)" % missing)

    # (b) + (c) per site, per kind, on what that site actually consumed
    for site in ALL_SITES:
        forbidden, what = (pool_keys, 'POOL row') if site in ND_SITES else (nd_keys, 'NATIONAL 1-64 row')
        for kind in KINDS:
            rows = (obs.get(site) or {}).get(kind)
            if rows is None:
                check(False, "site '%s' [%s] registered NOTHING — cannot be verified" % (site, kind))
                continue
            bad = sorted(set(rows) & forbidden)
            check(not bad,
                  "site '%s' [%s]: no %s among the %d keys it consumed%s"
                  % (site, kind, what, len(rows),
                     "" if not bad else "  <-- %d found, e.g. %s" % (len(bad), bad[:4])))
    return not _fails


def main():
    prove = '--prove-fails' in sys.argv
    recs = json.load(open(PER))['recs']

    # ---- the live check, on the production derivation -------------------------------------
    out = BASE + '/out/derived_split.json'
    subprocess.run([sys.executable, DERIVE, '--out', out, '--quiet'], check=True,
                   stdout=subprocess.DEVNULL)
    derived = json.load(open(out))
    print("STORE %s   surface %s (%s)"
          % (derived['meta']['store_md5'], derived['meta']['surface'], derived['meta']['v0surf_sig'][:8]))
    ok = run_check(derived, recs, "THE PRODUCTION DERIVATION (exclusion IN, both directions)")

    if not prove:
        print("\nRESULT: %s" % ("PASS" if ok else "FAIL"))
        sys.exit(0 if ok else 1)

    # ---- NON-VACUITY: cross ONE population at a time; each must fail BY NAME --------------
    print("\n" + "=" * 78)
    print("NON-VACUITY — cross one population at a time. Each MUST fail, naming that site and kind.")
    print("The 'pooling' rows are the ones a sampled-rows check cannot see.")
    print("=" * 78)
    results = []
    for site in ALL_SITES:
        for kind in KINDS:
            tmp = BASE + '/out/_broken_%s_%s.json' % (site, kind)
            subprocess.run([sys.executable, DERIVE, '--out', tmp, '--quiet',
                            '--break-site', site, '--break-kind', kind],
                           check=True, stdout=subprocess.DEVNULL)
            d = json.load(open(tmp))
            global _fails; _fails = []
            run_check(d, recs, "BROKEN: %s [%s]" % (site, kind))
            named = [m for m in _fails if ("'%s'" % site) in m and ("[%s]" % kind) in m]
            results.append((site, kind, bool(_fails), bool(named)))
            os.remove(tmp)

    print("\n" + "=" * 78)
    print("NON-VACUITY SUMMARY")
    print("%-18s %-9s %-10s %s" % ('site', 'kind', 'failed?', 'failed BY NAME?'))
    allgood = True
    for site, kind, failed, named in results:
        print("%-18s %-9s %-10s %s" % (site, kind, 'YES' if failed else 'NO -- VACUOUS',
                                       'YES' if named else 'NO -- WRONG SITE NAMED'))
        allgood &= (failed and named)
    print("=" * 78)
    print("RESULT: %s" % ("PASS — the check fails, by name, on every crossed population, in both "
                          "directions and through the pooling term" if (ok and allgood)
                          else "FAIL — see above"))
    sys.exit(0 if (ok and allgood) else 1)


if __name__ == '__main__':
    main()
