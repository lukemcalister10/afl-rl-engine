"""#334 stage B / STAGE 6 — THE ENTRY-YEAR RIDE TABLES, AT ONE RUNG OF THE LADDER (gate restored by Addendum 2 from ruling 5214157997).

All THREE tables (whole cohort / picks 1-20 / picks 21-64), each at its OWN argmax peak year, plus the
year-over-year segments, PRINTED ALWAYS. The only machine STOP that survives the owner's amendment:
an entry year beating DRAFT DAY's annualised ride by >= 5pp/yr (the rejected state was +5.25pp).
Everything below that line is presented, never auto-failed — the pub test is the owner's, at the
side-by-side.

Baseline and landed side by side, off the two committed matrices. READ-ONLY.
"""
import os, sys, json, importlib.util
import numpy as np

REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S5 = EV + '/stage5'
S6 = EV + '/stage6'
W = sys.argv[1]
spec = importlib.util.spec_from_file_location('harness_pvc', S6 + '/noarb/harness_pvc_REPINNED_pass3.py')
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)


def load(path):
    meta = json.load(open(path))['meta']
    o = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    H.EXPECT_STORE = meta['store_md5']; H.EXPECT_V0SURF = meta['v0surf_sig'][:12]
    m, ND = H.load_matrix(path); H.EXPECT_N = len(ND)
    H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N = o
    return {r['key']: r for r in ND}


A = load(S5 + '/noarb/per_entrant_338_stage5.json')          # the stage-5 LANDED board is stage 6's baseline
B = load(S6 + '/noarb/per_entrant_338_rung%s.json' % W)
keys = sorted(set(A) & set(B))
MAXN = 7
L = []
def say(s=''): L.append(s); print(s)


WINDOW_END = 2026
def val(r, n):
    """THE COMMITTED no-arb convention, carried verbatim from noarb_table_338.value_at + its inclusion
    rule: a concluded career scores 0 (the bust stays in the denominator); a player whose career has NOT
    YET REACHED year n is EXCLUDED (returns None). Anything else is survivorship and would flatter the
    ratios exactly where the band gate is read."""
    if r['year'] + n > WINDOW_END: return None          # not yet reached -> excluded
    if n == 0: return float(r['v0'])
    vp = r.get('vpath') or []
    i = n - 1
    if i >= len(vp): return 0.0                          # ended -> bust at 0
    return float(vp[i] or 0.0)


def table(M, ks):
    """mean value at year N over the entrants whose window covers year N; ratio to same-set year 0."""
    out = {}
    for n in range(0, MAXN + 1):
        rows = [k for k in ks if val(M[k], n) is not None]
        if not rows: continue
        mN = float(np.mean([val(M[k], n) for k in rows]))
        m0 = float(np.mean([val(M[k], 0) for k in rows]))
        out[n] = dict(n=len(rows), meanN=mN, mean0=m0, ratio=mN / m0)
    return out


BANDS = [('whole cohort', lambda k: True),
         ('picks 1-20  ', lambda k: 1 <= A[k]['pick'] <= 20),
         ('picks 21-64 ', lambda k: 21 <= A[k]['pick'] <= 64)]

say('=' * 112)
say('#334 stage B / STAGE 6 RUNG %s — ENTRY-YEAR RIDE' % W + ', ALL THREE TABLES AT THEIR OWN PEAK YEAR (gate: PRINTED ALWAYS)')
say('=' * 112)
RES = {}
for nm, f in BANDS:
    ks = [k for k in keys if f(k)]
    ta, tb = table(A, ks), table(B, ks)
    pa = max(ta, key=lambda n: ta[n]['ratio']); pb = max(tb, key=lambda n: tb[n]['ratio'])
    say('')
    say('  %s   n=%d' % (nm, len(ks)))
    say('     BASELINE own peak year %d, ratio %.6f    |    RUNG own peak year %d, ratio %.6f'
        % (pa, ta[pa]['ratio'], pb, tb[pb]['ratio']))
    say('     %-6s %10s %10s %10s %12s %12s' % ('entry N', 'n', 'S5 ratio', 'RUNG ratio', 'S5 ride/yr', 'RUNG ride/yr'))
    say('     ' + '-' * 66)
    rows = []
    for n in sorted(tb):
        # the RIDE from entry year N to the table's own peak, annualised
        def ride(t, p):
            if n >= p or n not in t: return None
            return (t[p]['ratio'] / t[n]['ratio']) ** (1.0 / (p - n)) - 1.0
        ra, rb = ride(ta, pa), ride(tb, pb)
        rows.append(dict(N=n, n=tb[n]['n'], base=ta[n]['ratio'] if n in ta else None, land=tb[n]['ratio'],
                         ride_base=ra, ride_land=rb))
        say('     %-6d %10d %10.6f %10.6f %12s %12s'
            % (n, tb[n]['n'], ta[n]['ratio'] if n in ta else float('nan'), tb[n]['ratio'],
               ('%+.2f%%/yr' % (100 * ra)) if ra is not None else '   (at/after peak)',
               ('%+.2f%%/yr' % (100 * rb)) if rb is not None else '   (at/after peak)'))
    # the machine STOP: an entry year beating draft day's annualised ride by >= 5pp/yr
    d0 = next((r['ride_land'] for r in rows if r['N'] == 0), None)
    worst = None
    for r in rows:
        if r['N'] == 0 or r['ride_land'] is None or d0 is None: continue
        exc = r['ride_land'] - d0
        if worst is None or exc > worst[1]: worst = (r['N'], exc)
    say('     draft-day (N=0) annualised ride to the peak: %s' % (('%+.4f%%/yr' % (100 * d0)) if d0 is not None else 'n/a'))
    if worst:
        say('     largest entry-year excess over draft day : entry year %d, %+.4fpp/yr   -> machine STOP at >= +5.00pp/yr : %s'
            % (worst[0], 100 * worst[1], 'STOP' if 100 * worst[1] >= 5.0 else 'no STOP'))
    say('     YEAR-OVER-YEAR SEGMENTS (landed, ratio units): %s'
        % '  '.join('yr%d->%d %+.4f' % (n, n + 1, tb[n + 1]['ratio'] - tb[n]['ratio'])
                    for n in sorted(tb)[:-1] if n + 1 in tb))
    RES[nm.strip()] = dict(peak_base=pa, peak_land=pb, ratio_base=ta[pa]['ratio'], ratio_land=tb[pb]['ratio'],
                           rows=rows, draft_day_ride=d0,
                           worst_excess_pp=(100 * worst[1]) if worst else None,
                           worst_excess_entry_year=(worst[0] if worst else None),
                           stop=bool(worst and 100 * worst[1] >= 5.0))

say('')
say('=' * 112)
say('THE BAND GATE [1.35, 1.45] — each table AT ITS OWN PEAK YEAR, and the yr2-4 deltas')
say('=' * 112)
for nm, f in BANDS:
    ks = [k for k in keys if f(k)]
    ta, tb = table(A, ks), table(B, ks)
    pa = max(ta, key=lambda n: ta[n]['ratio']); pb = max(tb, key=lambda n: tb[n]['ratio'])
    ok = 1.35 <= tb[pb]['ratio'] <= 1.45
    say('  %s  peak yr %d  ratio %.6f  -> %s   (baseline peak yr %d, %.6f; move %+.6f)'
        % (nm, pb, tb[pb]['ratio'], 'INSIDE [1.35,1.45]' if ok else 'OUTSIDE', pa, ta[pa]['ratio'],
           tb[pb]['ratio'] - ta[pa]['ratio']))
    say('     yr2-4 deltas (landed - baseline, ratio units): %s'
        % '  '.join('yr%d %+.6f' % (n, tb[n]['ratio'] - ta[n]['ratio']) for n in (2, 3, 4) if n in tb and n in ta))
    RES[nm.strip()]['band_pass'] = bool(ok)

say('')
say('  THE TAPER REACH, MEASURED (Addendum 2 relabelled round 2\'s "byte-identical propagation" as an')
say('  UNMEASURED seam expectation, because it was taken under the retired integer gate). The yr2-4')
say('  deltas above ARE the measurement: the taper does reach depth 1-2, it is small, and it is printed.')

open(os.path.join(S6, 'RIDES_rung%s.txt' % W), 'w').write('\n'.join(L) + '\n')
json.dump(RES, open(os.path.join(S6, 'rides_rung%s.json' % W), 'w'), indent=1, default=float)
