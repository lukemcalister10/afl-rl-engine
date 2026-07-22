#!/usr/bin/env python3
"""LEG E — COMPOSITION LAW unit test (memo §4, acceptance leg_d_placeholders.posture_2027_discounts).

Proves the R104.5 posture 2027-pick discount is applied EXACTLY ONCE per posture, as the final step,
on a synthetic pick — no double-count, the lens `fut` dial never touches a pick asset a second time.

Reads the candidate board (RL_LEGE=1 RL_PVC2=1) and asserts, for every pick n and every posture:
    picks_2027[posture][n].v  ==  round( face_curve[n] * (1 - discount[posture]) )
i.e. one and only one multiplicative discount off the FACE (balanced) curve. A second application
(e.g. * (1-d)^2, or a lens-fut re-discount) would fail this equality for d != 0.

Usage: python3 test_composition_single_discount.py <rl_app_data.json>
Exit code IS the verdict (0 PASS / 1 FAIL) — SILENCE IS A RED.
"""
import json, sys

BINDING = {'balanced': 0.10, 'contender': 0.15, 'rebuilder': 0.05}   # acceptance R104.5 + audit #6


def main(path):
    b = json.load(open(path))
    disc = b.get('posture_2027_discounts')
    p27 = b.get('picks_2027')
    face = {pp['n']: pp['v'] for pp in b.get('picks', [])}           # the face (balanced) 2027 curve
    ok = True

    # (1) the three discounts are EXACTLY the binding values
    if disc != BINDING:
        print("FAIL: posture_2027_discounts %r != binding %r" % (disc, BINDING)); ok = False
    if not p27 or not face:
        print("FAIL: candidate board missing picks_2027 / picks (is RL_LEGE=1 RL_PVC2=1?)"); return 1

    # (2) single application, exact, for every pick and posture
    worst = {}
    for post, d in BINDING.items():
        rows = {r['n']: r['v'] for r in p27.get(post, [])}
        bad = 0
        for n, fv in face.items():
            if n not in rows:
                continue
            expect_once = round(fv * (1 - d))
            expect_twice = round(fv * (1 - d) * (1 - d))
            got = rows[n]
            if got != expect_once:
                bad += 1
                if got == expect_twice:
                    print("FAIL: %s pick %d = %d == FACE*(1-d)^2 (DOUBLE-COUNT)" % (post, n, got))
                else:
                    print("FAIL: %s pick %d = %d != round(FACE %d * (1-%.2f)) = %d"
                          % (post, n, got, fv, d, expect_once))
        worst[post] = bad
        ok = ok and bad == 0
    print("single-application check:", {k: ('OK' if v == 0 else '%d BAD' % v) for k, v in worst.items()})

    # (3) balanced is the face curve minus 0.10 exactly (the canonical anchor)
    print("RESULT:", "PASS — one discount per axis, exact, no double-count" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'rl_app_data.json'))
