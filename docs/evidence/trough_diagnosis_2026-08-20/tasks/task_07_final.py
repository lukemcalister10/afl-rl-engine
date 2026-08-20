"""(a) why Cootee is immune; (b) the EXACT tree thresholds under the anchored kinks."""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']
Y = 2026; F = 1.052329
QK = sorted(cm.keys())
SP = os.path.dirname(os.path.dirname(OUTBASE))

print('=== (a) the ITEM A anchor share — why a band jump does or does not reach the price ===')
for nm in ['Billy Cootee', 'Will Hayes', 'Charlie West', 'Max Kondogiannis', 'Josh Dolan',
           'Marcus Herbert', 'Sam Lalor']:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        continue
    e = G['_prod_path'](p, Y) * G['_h_cut'](p, Y)
    tau = max(0.0, Y - cp.debutyr(p)) + (G['_fEy'](Y, p) ** 1.5)
    R = G['_R_surf'](G['_sitout_cls'](MA.gfut(p)), MA.effpk(p), tau)
    if p.get('_pool'):
        R = G['_pr_mult'](p, Y, tau)
    anch0 = R * G['entry_anchor'](p)
    w = G['_c_w'](p, Y, e, G['entry_anchor'](p))
    anch = anch0 * (1.0 + w * (G['C_H'] - 1.0))
    s = G['_a_share'](p, Y)
    blend = (1 - s) * e + s * anch
    print('  %-18s  prod-leg e=%8.1f   anchor=%8.1f   anchor share s=%.4f   blend=%8.1f   ev=%8.1f'
          '   -> a 10%% band move shifts the price by %.2f%%'
          % (nm, e, anch, s, blend, ev(p, Y), 100 * 0.10 * (1 - s) * e / max(blend, 1e-9)))

print()
print('=== (b) the exact feature-9 tree thresholds under the anchored kinks ===')
th = {}
for q in QK:
    t = []
    for est in np.asarray(cm[q].estimators_).ravel():
        tr = est.tree_
        t += [float(x) for f, x in zip(tr.feature, tr.threshold) if f == 9]
    th['q%s' % q] = sorted(set(t))
t = []
for est in np.asarray(q97m.estimators_).ravel():
    tr = est.tree_
    t += [float(x) for f, x in zip(tr.feature, tr.threshold) if f == 9]
th['q97m'] = sorted(set(t))

for lab, L in [('Dolan  score 38->40 (bb[5] 82.84->80.52)', 48.44),
               ('Dolan  score 40->42 (bb[2],bb[4] fall)', 48.51),
               ('Kondo  score 74->75 (bb[4] 85.93->81.43)', 48.55),
               ('Kondo  score 52->53 (bb[3],bb[4] fall)', 47.48)]:
    print('  %s   nearest thresholds below L=%.3f:' % (lab, L))
    for k, v in th.items():
        c = [x for x in v if x <= L]
        if c:
            print('       %-6s  %.6f   (gap %.4f)' % (k, c[-1], L - c[-1]))

print()
print('=== (c) the band is NOT monotone in the level: magnitude at fixed everything-else ===')
for nm in ['Max Kondogiannis', 'Josh Dolan']:
    p = next(x for x in MA.data if x['player'] == nm)
    feat = [float(x) for x in cp._feat(p, Y)]
    grid = np.arange(44.0, 56.0, 0.02)
    X = np.tile(np.array(feat, float), (len(grid), 1)); X[:, 9] = grid
    pr = {q: cm[q].predict(X) for q in QK}
    pr97 = q97m.predict(X)
    print('  %s (other features frozen):' % nm)
    for q in QK:
        v = pr[q]
        mx = np.maximum.accumulate(v)
        drop = (mx - v)
        i = int(np.argmax(drop))
        print('     q=%.1f   worst fall below its own running max over L in [44,56]:  %.2f pts '
              '(at L=%.2f, running max set at L=%.2f)' %
              (q, drop[i], grid[i], grid[int(np.argmax(v[:i + 1]))]))
    v = pr97; mx = np.maximum.accumulate(v); drop = mx - v; i = int(np.argmax(drop))
    print('     q97m   worst fall: %.2f pts (at L=%.2f)' % (drop[i], grid[i]))
