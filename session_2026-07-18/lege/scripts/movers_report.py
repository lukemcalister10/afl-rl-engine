#!/usr/bin/env python3
"""LEG E MOVERS REPORT (memo §6.3): top-20 risers/fallers per FORWARD lens vs balanced-now, the posture
2027-pick discounts, and the named LTI rows (Rozee mandatory). Rendered for the owner to ratify the
§6.2 preset numbers (tuned from evidence, not a priori). Balanced is the ONLY board that gates/bakes/seals."""
import json, sys

def main(path, out=None):
    b = json.load(open(path))
    rows = [p for p in b['active'] if p.get('key') and p.get('v') is not None]
    L = []
    for lens, fld in (('+1 yr', 'vP1'), ('+2 yr', 'vP2')):
        mv = []
        for p in rows:
            v0, vk = p.get('v'), p.get(fld)
            if v0 is None or vk is None or v0 == 0:
                continue
            mv.append((p.get('name', p['key']), p.get('age'), v0, vk, vk - v0, round(100 * (vk - v0) / v0, 1)))
        risers = sorted(mv, key=lambda x: -x[4])[:20]
        fallers = sorted(mv, key=lambda x: x[4])[:20]
        L.append("\n=== FORWARD LENS %s vs balanced-now (top-20 each; value credited via R103.3) ===" % lens)
        L.append("  RISERS (production credited — pre-peak accrual):")
        L.append("  %-24s %4s %7s %7s %7s %7s" % ('player', 'age', 'now', lens, 'd', 'd%'))
        for nm, ag, v0, vk, d, pc in risers:
            L.append("    %-22s %4s %7d %7d %+7d %+6.1f%%" % (nm[:22], ag, v0, vk, d, pc))
        L.append("  FALLERS (projected decline — L-SYMMETRY, same bar as improvement):")
        for nm, ag, v0, vk, d, pc in fallers:
            L.append("    %-22s %4s %7d %7d %+7d %+6.1f%%" % (nm[:22], ag, v0, vk, d, pc))

    # posture 2027-pick discounts (composition law; one application)
    L.append("\n=== POSTURE 2027-PICK DISCOUNTS (composition law §4; one application, BINDING) ===")
    L.append("  discounts: %s" % json.dumps(b.get('posture_2027_discounts')))
    p27 = b.get('picks_2027', {})
    face = {pp['n']: pp['v'] for pp in b.get('picks', [])}
    L.append("  %-10s %8s %8s %8s %8s %8s" % ('posture', 'pick1', 'pick2', 'pick3', 'pick5', 'pick10'))
    L.append("  %-10s %8s %8s %8s %8s %8s" % ('FACE', face.get(1), face.get(2), face.get(3), face.get(5), face.get(10)))
    for post in ('balanced', 'contender', 'rebuilder'):
        r = {x['n']: x['v'] for x in p27.get(post, [])}
        L.append("  %-10s %8s %8s %8s %8s %8s" % (post, r.get(1), r.get(2), r.get(3), r.get(5), r.get(10)))

    # named LTI rows — Rozee mandatory (memo §5)
    L.append("\n=== NAMED LTI ROWS (memo §5; magnitude is an [OWNER] ruling at THIS report) ===")
    L.append("  LTI truncation honoured: demonstrated form/games held at true-now (2026) under the forward lens.")
    L.append("  %-24s %4s %7s %7s %7s" % ('player', 'age', 'now', '+1', '+2'))
    for target in ('rozee', 'reid'):
        hits = [p for p in rows if target in (p.get('name') or '').lower()]
        for p in hits[:3]:
            L.append("    %-22s %4s %7s %7s %7s   %s" % ((p.get('name') or '')[:22], p.get('age'),
                     p.get('v'), p.get('vP1'), p.get('vP2'),
                     'LTI/avail row' if target == 'rozee' else 'R103.6 watch row'))

    text = "\n".join(L)
    print(text)
    if out:
        open(out, 'w').write(text + "\n")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
