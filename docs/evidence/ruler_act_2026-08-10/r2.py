import lib2, json, numpy as np, collections
S5 = lib2.build('pe_stage5.json'); OS = lib2.outc(S5)
C = json.load(open('r1_cells.json'))
Z = [x for x in OS if x['leg'] == 'sit0']; Q = [x for x in OS if x['leg'] == 'quiet']
CAND = {
 'age23+ sitters':  [x for x in Z if x['age'] is not None and x['age'] >= 23],
 'IRE sitters':     [x for x in Z if x['typ'] == 'IRE'],
 'MSD sitters':     [x for x in Z if x['typ'] == 'MSD'],
 'UNION 23+/IRE/MSD': [x for x in Z if (x['age'] is not None and x['age'] >= 23) or x['typ'] in ('IRE', 'MSD')],
 'age21+ pooled':   [x for x in Z if x['age'] is not None and x['age'] >= 21],
 'age-unk RD gap':  [x for x in Z if x['age'] is None],
 'RD sitters (all)':[x for x in Z if x['typ'] == 'RD'],
 'sitters (all)':   Z,
}
print("=== F8 QUALIFICATION (eff-n >= 35 AND bootstrap CI upper < 1), re-derived stage-5-landed basis ===")
print("%-20s %5s %6s %8s %9s %9s %9s  %s" % ('cell', 'n', 'eff-n', 'F_s7', 'CI_lo', 'CI_hi', 'margin', 'verdict'))
QU = {}
for nm, rs in CAND.items():
    F = lib2.aggF(rs); lo, hi = lib2.ci(rs, B=20000); en = lib2.effn(rs)
    ok = en >= 35 and hi < 1.0
    QU[nm] = dict(n=len(rs), effn=en, F=F, lo=lo, hi=hi, named=ok)
    v = 'NAMED' if ok else ('STRUCK (eff-n %.1f < 35)' % en if en < 35 else 'STRUCK (CI straddles 1)')
    if ok and (1 - hi) < 0.10: v = 'NAMED* (margin %.3f — no real clearance)' % (1 - hi)
    print("%-20s %5d %6.1f %8.4f %9.4f %9.4f %+9.4f  %s" % (nm, len(rs), en, F, lo, hi, 1 - hi, v))

print("\n=== F3/F4 · FLOOR INTERACTION, ABSOLUTE UNITS (board points = engine value / 1.0524 not applied; ")
print("    engine currency, A = signed level x 1.0524). Depth = the year-1 evaluation, FLOOR_YRS[1]=0.45 ===")
print("%-20s %7s %8s %8s %8s %9s %9s %9s" %
      ('cell', 'meanA', 'price', 'honest', 'floor', 'gross gap', 'deliv.cut', 'clamped'))
for nm in ('age23+ sitters', 'IRE sitters', 'MSD sitters', 'UNION 23+/IRE/MSD'):
    rs = CAND[nm]; F = lib2.aggF(rs)
    A = np.mean([x['A'] for x in rs]); pr = np.mean([x['v1'] for x in rs])
    ho = np.mean([x['v4'] / lib2.HURDLE ** 3 for x in rs]); fl = np.mean([0.45 * x['A'] for x in rs])
    cand = [x['v1'] * F for x in rs]
    post = [min(x['v1'], max(c, 0.45 * x['A'])) for c, x in zip(cand, rs)]
    cl = sum(1 for c, x in zip(cand, rs) if c < 0.45 * x['A'])
    gross = np.mean([x['v1'] - c for c, x in zip(cand, rs)])
    dl = np.mean([x['v1'] - p for p, x in zip(post, rs)])
    QU[nm].update(A=A, price=pr, honest=ho, floor=fl, gross=gross, deliv=dl, clamp=cl)
    print("%-20s %7.1f %8.1f %8.1f %8.1f %9.1f %9.1f %6d/%d" % (nm, A, pr, ho, fl, gross, dl, cl, len(rs)))
print("  RANK, gross mis-pricing pts/player : %s" %
      ' > '.join('%s %.1f' % (n, QU[n]['gross']) for n in sorted(('age23+ sitters', 'IRE sitters', 'MSD sitters'),
                                                                key=lambda z: -QU[z]['gross'])))
print("  RANK, DELIVERABLE net of #326 floor: %s" %
      ' > '.join('%s %.1f (%.1f%% of price)' % (n, QU[n]['deliv'], 100 * QU[n]['deliv'] / QU[n]['price'])
                 for n in sorted(('age23+ sitters', 'IRE sitters', 'MSD sitters'), key=lambda z: -QU[z]['deliv'])))

print("\n=== F1 · LIFT DELIVERABILITY UNDER THE ENTRY-ANCHOR CAP ===")
print("%-22s %5s %8s %9s %10s %11s %10s" % ('lift cell', 'n', 'p/A now', 'honest/A', 'target x', 'CAPPED x', 'gap pp'))
for nm, rs in [('quiet gy>0 pooled', Q), ('  x RD', [x for x in Q if x['typ'] == 'RD']),
               ('  x ND65+', [x for x in Q if x['typ'] == 'ND']),
               ('  x age<=18', [x for x in Q if x['age'] is not None and x['age'] <= 18])]:
    pA = sum(x['v1'] for x in rs) / sum(x['A'] for x in rs)
    hA = sum(x['v4'] for x in rs) / lib2.HURDLE ** 3 / sum(x['A'] for x in rs)
    tgt = hA / pA
    capd = sum(min(x['v1'] * tgt, x['A']) for x in rs) / sum(x['v1'] for x in rs)
    print("%-22s %5d %8.4f %9.4f %10.4f %11.4f %10.2f" % (nm, len(rs), pA, hA, tgt, capd, 100 * (tgt - capd)))
json.dump(QU, open('r2_qual.json', 'w'), indent=1, default=float)
