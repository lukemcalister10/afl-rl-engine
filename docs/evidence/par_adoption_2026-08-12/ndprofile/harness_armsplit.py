"""ORDER 20 — THE ARM-SPLIT COMPLETION STRATA.

`harness_pvc_REPINNED_pass3.structural_values` (:339) builds its career-COMPLETION strata

    S[(pos, tenure)] -> (sum realised_full, sum sofar, n)

over WHATEVER population it is handed. Its callers hand it `elig` — pool rows AND national rows
together (`profile_measure.py:66`, `derive_vs_scale.py:36`, `phase1_derive.py`). A live national
career is therefore completed with a ratio taught partly by POOL careers, so moving a pool price moves
the completed value of a national row, and therefore moves `nd_profile`, the calibration target every
lambda is measured against. ORDER 19 measured that drift at -0.1939% (PR #455, POOL_SITTER_LIFT_SUMMARY
section 4).

THIS FILE DOES NOT MODIFY THE PINNED HARNESS. `harness_pvc_REPINNED_pass3.py` is filed evidence of a
landed act (composition_2026-08-10) and this order does not write filed evidence. Everything except
the stratum KEY is imported from it and called, not re-implemented — `concluded`, `depth`,
`realised_full`, `sofar` are the pinned functions, so this cannot drift from the curve.

THE FIX, stated exactly: the stratum key gains the ARM.

    contaminated :  S[(pos, t)]
    arm-split    :  S[(arm, pos, t)]        arm = 'POOL' | 'ND'

Nothing is deleted and no row is dropped. Both arms still get completion strata; each is taught by its
own arm's careers. This is the "split the shared population per arm rather than delete the sharing"
shape the order asks for. Fallback behaviour (thin stratum -> the row's own v0 prior) is unchanged, so
a thinner per-arm stratum degrades to the SAME declared fallback the pinned function already uses, and
the fallback share is counted and returned exactly as before.
"""
import collections, os, sys

_NOARB = os.environ.get('RL_O20_NOARB') or (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../composition_2026-08-10/noarb')))
if _NOARB not in sys.path:
    sys.path.insert(0, _NOARB)
import harness_pvc_REPINNED_pass3 as H            # the PINNED harness, imported and never written


def arm_of(r):
    """WHICH ARM A MATRIX ROW BELONGS TO — the ENGINE's own classification, quoted, not re-derived.

    `emit_matrix_338.py:240` records the engine's own predicates on every row as `is_pool_engine` /
    `teaches_curve_engine`, ALONGSIDE the slide-derived `is_pool` / `teaches_curve` it publishes at
    :242-243. This function reads the ENGINE fields. That is the whole `daniel-butler` question and it
    is answered here in one line: the slide is a fit-population device for the curve, which the
    emitter's own header states at :49-52; it is NOT an assertion that a player was drafted a slot
    earlier, so it may not move a player from one ARM to the other.

    Falls back to the published `is_pool` only for a matrix emitted before the engine fields existed,
    and says so loudly rather than guessing silently.
    """
    if 'is_pool_engine' in r:
        return 'POOL' if r['is_pool_engine'] else 'ND'
    raise KeyError("matrix row %r carries no `is_pool_engine` — this matrix predates the engine-predicate "
                   "disclosure and the arm cannot be established without guessing. Re-emit." % r.get('key'))


def structural_values(rows, split=True, armfn=arm_of):
    """The pinned :339 body with ONE change: the stratum key carries the arm when split=True.

    split=False reproduces the pinned function EXACTLY (asserted by the caller against
    H.structural_values on the same input), so the arm split's effect is isolated by construction.
    """
    S = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for r in rows:
        if not H.concluded(r):
            continue
        T = H.depth(r)
        if T <= 0:
            continue
        f = H.realised_full(r)
        for t in range(1, T + 1):
            e = S[((armfn(r) if split else '*'), r['pos'], t)]
            e[0] += f; e[1] += H.sofar(r, t); e[2] += 1
    out = []; c = collections.Counter()
    for r in rows:
        if H.concluded(r):
            c['concluded_realised'] += 1
            out.append({'key': r['key'], 'pick': r['pick'], 'value': H.realised_full(r),
                        'concluded': True, 'how': 'concluded_realised'}); continue
        T = H.depth(r)
        if T <= 0:
            c['prior_fallback_no_written'] += 1
            out.append({'key': r['key'], 'pick': r['pick'], 'value': float(r['v0']),
                        'concluded': False, 'how': 'prior_fallback_no_written'}); continue
        e = S.get(((armfn(r) if split else '*'), r['pos'], T))
        if e is None or e[2] < H.MIN_STRATUM or e[1] <= 0:
            c['prior_fallback_thin'] += 1
            out.append({'key': r['key'], 'pick': r['pick'], 'value': float(r['v0']),
                        'concluded': False, 'how': 'prior_fallback_thin'}); continue
        c['completed'] += 1
        out.append({'key': r['key'], 'pick': r['pick'],
                    'value': H.sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2])),
                    'concluded': False, 'how': 'completed'})
    fb = c['prior_fallback_thin'] + c['prior_fallback_no_written']
    assert c['concluded_realised'] + c['completed'] + fb == len(rows), \
        "provenance counts do not sum to population"
    return out, {'counts': dict(c), 'fallback_rows': fb, 'of_population': len(rows),
                 'fallback_share_pct': round(100.0 * fb / len(rows), 3), 'split': split}
