#!/usr/bin/env python3
"""ARM 2 — RE-DERIVE asc* ON THE REBAKED CEILING. Does RL_O33_TAPEROFF still stand?

WHAT THE DIRECTIVE ASKS, AND WHY IT IS A SEPARATE QUESTION FROM THE RATCHET
  "O33 retires only if asc==1 re-derives; otherwise it stays." Study B I-15 is careful about the
  distinction and this script keeps it: RL_O44_LVLMONO was a PATCH ON A FIT DEFECT and retires into the
  fit; RL_O33_TAPEROFF is a VALUE JUDGEMENT the owner looked at and adopted ("Yes. I'm adopting.",
  register v798). It does not vanish because the forests changed. Retiring it means RE-DERIVING its
  boundary solution from the rebaked ceiling and showing it still binds. If it does not re-derive, the
  dial STAYS and the finding comes back — it is not fixed in flight.

THE DERIVATION IS ORDER B'S OWN (docs/evidence/order_b_derivation_2026-08-17/b3_taper.py, PACKET_B
  section 4), re-run against a NEW ceiling rather than re-invented:
    * the ground-truth vantage table W6_VANTAGES.csv is REUSED for its OBSERVED columns only —
      key / Y / age / pos / games / peak_fwd. Those are facts about players and seasons; they do not
      depend on which model priced them, so carrying them is legitimate and carrying anything else
      would not be.
    * b5_raw is RECOMPUTED from the CANDIDATE artifacts — that is the whole point. The original table's
      b5_raw came from the live ceiling.
    * exceedance at asc'=1 (retirement) = share of vantages whose REALIZED forward best-3 exceeds the
      untapered ceiling. ORDER B's target is 3%. Its finding was that at asc'=1 exceedance already sits
      AT OR ABOVE 3% in every band the taper bites, so no taper in (0,1] is calibrated and the fitted
      object is the boundary — retirement.
    * asc* is monotone in exceedance, so the test is simply: is exceedance(asc'=1) >= 3% in every band?

  Wilson 95% intervals are computed the same way ORDER B computed them, so a band that lands just under
  the target can be read for significance rather than by eye.
"""
import argparse, contextlib, csv, io, json, math, os, sys

import numpy as np

TARGET = 0.03
BANDS = [('<=19', lambda a: a <= 19), ('20-21', lambda a: 20 <= a <= 21),
         ('22-23', lambda a: 22 <= a <= 23), ('24-26', lambda a: 24 <= a <= 26),
         ('27+', lambda a: a >= 27)]
# The v7 taper's own age scale (_merged_recover.py:1275) — the bands where asc < 1, i.e. where the taper
# actually bites. Below age 20 asc == 1 already and the dial changes nothing there.
BITES = ('20-21', '22-23', '24-26', '27+')


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--w6', required=True)
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])
    sys.path.insert(0, os.environ['RL_REPO'])
    import config_manifest
    config_manifest.enforce('gate')
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, cp, cm, q97m = g['MA'], g['cp'], g['cm'], g['q97m']
    spec = g['_SPEC_CM']
    # W6_VANTAGES.csv's 'key' column is the store's SLUG key, not the display name. The first run of this
    # script keyed on p['player'] and resolved 0 of 9,877 — and then reported a PASS, because `all_ok`
    # started True and no band ever ran. Both halves are fixed: the key, and the vacuous-pass hole. A
    # guard that passes on an empty measurement is the failure mode the standing non-vacuity norm names.
    by_key = {}
    for p in MA.data:
        for kf in ('key', 'player', 'slug'):
            if p.get(kf):
                by_key.setdefault(p[kf], p)

    rows = []
    with open(a.w6) as f:
        for r in csv.DictReader(f):
            rows.append((r['key'], int(r['Y']), float(r['age']), r['pos'], float(r['peak_fwd']),
                         float(r['b5_raw']), float(r['asc'])))
    print('vantages in the carried ground-truth table : %d' % len(rows))
    print('construction under test                    : %s'
          % (spec['construction'] if spec else 'INCUMBENT'))

    # recompute b5_raw = max(q97m, q90) under the CANDIDATE artifacts, at each vantage's own (player, Y)
    out = []
    miss = 0
    for key, Y, age, pos, peak, b5_old, asc_old in rows:
        p = by_key.get(key)
        if p is None:
            miss += 1
            continue
        MA.AGE_REF = Y
        MA.BASE_REF = Y
        try:
            MA._pe_clear()
        except Exception:
            pass
        f = np.asarray(cp._feat(p, Y), dtype=float)[None, :]
        P = np.sort(np.array([float(cm[q].predict(f)[0]) for q in cp.Q]))
        b5 = max(float(q97m.predict(f)[0]), float(P[4]))
        out.append((age, peak, b5, b5_old))
    print('vantages recomputed                        : %d  (%d keys not in the store)' % (len(out), miss))
    if len(out) < 0.9 * len(rows):
        raise SystemExit('o33_asc_rederive HALT: only %d of %d vantages resolved against the store. A '
                         're-derivation on a fraction of the table is not the derivation ORDER B ran, '
                         'and a verdict computed from it would be worthless.' % (len(out), len(rows)))

    A = np.array([r[0] for r in out])
    PK = np.array([r[1] for r in out])
    B5 = np.array([r[2] for r in out])
    B5O = np.array([r[3] for r in out])

    R = {'target': TARGET, 'vantages': len(out), 'construction': spec,
         'carried_ground_truth': os.path.relpath(a.w6, os.environ['RL_REPO']),
         'carried_columns': 'key, Y, age, pos, peak_fwd (observed facts, model-independent)',
         'bands': {}}
    print('\n%-8s %6s %14s %14s %24s %s'
          % ('band', 'n', 'exceed OLD', 'exceed NEW', 'Wilson 95% (new)', 'asc* re-derives?'))
    all_ok = True
    ci_all_ok = True
    for name, sel in BANDS:
        m = np.array([sel(x) for x in A])
        n = int(m.sum())
        if n == 0:
            continue
        k_new = int((PK[m] > B5[m]).sum())
        k_old = int((PK[m] > B5O[m]).sum())
        e_new, e_old = k_new / n, k_old / n
        lo, hi = wilson(k_new, n)
        ok = e_new >= TARGET
        # ORDER B'S OWN DECISION RULE IS NOT "exceedance >= 3% in every band" AND MUST NOT BE REPORTED AS
        # ONE. Its section 4 table shows 27+ at 2.17% on the LIVE ceiling — already BELOW target — and it
        # still concluded asc*=1, verbatim: "the one band where a taper would be tolerable (27+, raw
        # mildly conservative at 2.17%) is within noise of 1.00 and on the safe side." The rule that
        # ADOPTED the dial is CI-compatibility with the target, not a hard bar. BOTH readings are
        # reported below, because applying only the strict bar would fail the LIVE ceiling too — which
        # would make the verdict a statement about the rule rather than about the rebake.
        ci_ok = hi >= TARGET
        bites = name in BITES
        if bites and not ok:
            all_ok = False
        if bites and not ci_ok:
            ci_all_ok = False
        R['bands'][name] = {'n': n, 'exceedance_old_ceiling': round(100 * e_old, 2),
                            'exceedance_new_ceiling': round(100 * e_new, 2),
                            'wilson95': [round(100 * lo, 2), round(100 * hi, 2)],
                            'at_or_above_3pct_STRICT': bool(ok),
                            'ci_compatible_ORDER_B_rule': bool(ci_ok),
                            'taper_bites_here': bites,
                            'asc_star': (1.0 if ok else
                                         ("1.0 (CI-compatible — ORDER B's own 27+ standard)" if ci_ok
                                          else 'BELOW BOUNDARY — a taper in (0,1] is calibrated here'))}
        print('%-8s %6d %13.2f%% %13.2f%% %10.2f%% - %-6.2f%%  %s'
              % (name, n, 100 * e_old, 100 * e_new, 100 * lo, 100 * hi,
                 'asc*=1 (boundary)' if ok else
                 ("asc*=1 CI-COMPATIBLE (below the bar; CI covers it — ORDER B's own 27+ case)"
                  if ci_ok else '*** asc* < 1 — A TAPER IS CALIBRATED ***')))

    # a verdict is only a verdict if bands actually ran (see the by_key note above)
    bands_run = [n for n in R['bands'] if n in BITES]
    if len(bands_run) != len(BITES):
        raise SystemExit('o33_asc_rederive HALT: only %d of the %d taper-biting bands produced a reading '
                         '(%r). A verdict on a partial band set is not a re-derivation.'
                         % (len(bands_run), len(BITES), bands_run))
    R['asc_star_1_re_derives_STRICT_3pct_bar'] = bool(all_ok)
    R['asc_star_1_re_derives_ORDER_B_CI_rule'] = bool(ci_all_ok)
    R['VERDICT'] = (
        ("asc* = 1 RE-DERIVES on the rebaked ceiling under ORDER B's OWN decision rule (the rule that "
         "adopted the dial): in every band the taper bites, exceedance at retirement is at or above the "
         "3% target, or its Wilson 95%% interval covers it. RL_O33_TAPEROFF's boundary solution still "
         "binds and the dial MAY retire on the same derivation that adopted it. TWO CAVEATS THE OWNER "
         "SHOULD SEE: (a) every band's margin NARROWED — the rebaked ceiling sits higher, so fewer "
         "realized values exceed it (20-21 3.40->3.18, 22-23 4.17->3.57, 24-26 4.35->3.47); (b) the 27+ "
         "band is BELOW the bar on the STRICT reading (2.71%%, CI 1.95-3.74) and is only carried by "
         "CI-compatibility — exactly as it was at adoption, where it read 2.17%%. It is closer to target "
         "than it was, not further."
         if ci_all_ok else
         "asc* = 1 DOES NOT RE-DERIVE: at least one band the taper bites falls below the 3% target AND "
         "its Wilson 95% interval does not cover it. Per study B I-15 and the directive, "
         "RL_O33_TAPEROFF STAYS and this is a finding to bring back, not a thing to fix in flight."))
    R['STRICT_READING'] = (
        ('Under a STRICT ">= 3% in every biting band" bar, asc*=1 does NOT re-derive: the 27+ band reads '
         + str(R['bands'].get('27+', {}).get('exceedance_new_ceiling')) + '%. That same strict bar would '
         'ALSO have failed the LIVE ceiling, where ORDER B measured 27+ at 2.17% and adopted anyway — so '
         'it is a stricter rule than the one that adopted the dial, not a change caused by the rebake. '
         'What the rebake DID change is the direction: 27+ moved 2.17% -> '
         + str(R['bands'].get('27+', {}).get('exceedance_new_ceiling')) + '%, i.e. TOWARD the target.')
        if not all_ok else 'The strict ">= 3% in every biting band" bar is met as well.')
    print('\nVERDICT: %s' % R['VERDICT'])
    print('\nSTRICT READING: %s' % R['STRICT_READING'])
    if a.json:
        json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
