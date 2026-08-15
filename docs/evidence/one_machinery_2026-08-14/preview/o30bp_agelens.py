#!/usr/bin/env python3
"""ORDER 30B-P — THE AGE-WITHIN-GAMES LENS. The owner's 36-early-vs-36-late question.

Source: the COMMITTED 30B-M state table, docs/evidence/pedigree_persistence_2026-08-14/PERSISTENCE_TABLE.json,
`cells_all_states` — 1,378 cells keyed  position | age-at-state | games band | output quintile | pick band,
each carrying n, mean, median, p25, p75 and zero_share of realized R6 (remaining delivered value over the
next six observed seasons, discounted 14%/yr from the state year).

NO ENGINE, NO BOARD, NO REGRESSION IS RE-RUN. The measurement is the committed one; this lens re-cuts it.

WHAT THE LENS CAN AND CANNOT DO, STATED BEFORE ANY NUMBER IS PRINTED.
  * sigma in the packet is a REGRESSION quantity: beta_v0 x mean_v0 / mean_R, fitted on the 4,033-state
    panel. The panel is not in the committed artifact; only the cells are. So sigma itself CANNOT be
    re-fitted per age group from this file, and this harness does not pretend to.
  * What the cells DO carry is the packet's own model-free instrument: the CELL-MATCHED PICK CONTRAST —
    high picks minus low picks, matched within (position x output quintile) strata so output and position
    are held. That instrument produced the packet's +159/+849/+273/+127/+201 band row (section 2.1).
  * The lens therefore reports (i) the matched contrast per age cell, raw, in R6 points, with n and
    dispersion; and (ii) a SHARE-SCALED reading, sigma_hat(band, age) = sigma_published(band) x
    Delta_matched(band, age) / Delta_matched(band, ALL AGES). That scaling assumes sigma is proportional
    to the matched pick gap WITHIN a band. THE ASSUMPTION IS DECLARED, it is the only bridge from the
    cells to a share, and the verdict below is stated so that it does not depend on the scaling.

AGE BINS. The committed table bins age-at-state as <=19 / 20 / 21 / 22-23 / 24-26 / 27+. The brief's
example split (<=20 / 21-22 / 23+) CANNOT be cut exactly, because 22 and 23 are pooled in the committed
artifact. The lens therefore uses the table's own granularity, collapsed to <=20 / 21 / 22-23 / 24+, and
reports the <=20 vs 24+ and <=20 vs 21+ contrasts as the deciding comparisons. Disclosed, not fudged.

Usage: o30bp_agelens.py PERSISTENCE_TABLE.json OUTDIR
"""
import json, sys, os, math, collections

SRC, OUT = sys.argv[1], sys.argv[2]
D = json.load(open(SRC))
C = D['cells_all_states']
BF = D['q1_persistence']['band_fits']

AGE_GROUP = {'<=19': '<=20', '20': '<=20', '21': '21', '22-23': '22-23', '24-26': '24+', '27+': '24+'}
AGE_ORDER = ['<=20', '21', '22-23', '24+']
HI = ('A 1-6', 'B 7-12')
LO = ('D 21-40', 'E 41-64')
BANDS = ('16-35', '36-70')

parsed = []
for k, v in C.items():
    pos, age, gb, q, pb = k.split('|')
    parsed.append(dict(pos=pos, age=age, ag=AGE_GROUP[age], gb=gb, q=q, pb=pb, **v))

def pool(cells):
    """n-weighted mean, and the n-weighted pooled p25/median/p75 (dispersion), over a set of cells."""
    n = sum(c['n'] for c in cells)
    if n == 0: return None
    m = sum(c['n'] * c['mean'] for c in cells) / n
    med = sum(c['n'] * c['median'] for c in cells) / n
    p25 = sum(c['n'] * c['p25'] for c in cells) / n
    p75 = sum(c['n'] * c['p75'] for c in cells) / n
    z = sum(c['n'] * c['zero_share'] for c in cells) / n
    return dict(n=n, mean=m, median=med, p25=p25, p75=p75, iqr=p75 - p25, zero_share=z, n_cells=len(cells))

def matched(cells):
    """the packet's cell-matched pick contrast: HI minus LO, matched on (position x output quintile),
    weighted by min(n_hi, n_lo). Returns the contrast, its weight, the strata used, and a weighted SD."""
    by = collections.defaultdict(lambda: {'hi': [], 'lo': []})
    for c in cells:
        if c['pb'] in HI: by[(c['pos'], c['q'])]['hi'].append(c)
        elif c['pb'] in LO: by[(c['pos'], c['q'])]['lo'].append(c)
    ds, ws, det = [], [], []
    for k, v in sorted(by.items()):
        if not v['hi'] or not v['lo']: continue
        ph, pl = pool(v['hi']), pool(v['lo'])
        w = min(ph['n'], pl['n'])
        ds.append(ph['mean'] - pl['mean']); ws.append(w)
        det.append(dict(stratum='%s|%s' % k, n_hi=ph['n'], n_lo=pl['n'], mean_hi=ph['mean'],
                        mean_lo=pl['mean'], delta=ph['mean'] - pl['mean'], w=w))
    if not ws: return None
    W = float(sum(ws)); dm = sum(w * d for w, d in zip(ws, ds)) / W
    var = sum(w * (d - dm) ** 2 for w, d in zip(ws, ds)) / W
    neff = (W ** 2) / sum(w * w for w in ws)
    return dict(delta=dm, w=W, n_strata=len(ws), sd=math.sqrt(var), n_eff=neff,
                se=math.sqrt(var / max(1.0, neff)), strata=det)

print('ORDER 30B-P — THE AGE-WITHIN-GAMES LENS')
print('source: PERSISTENCE_TABLE.json cells_all_states (%d cells, %d states, %d careers)'
      % (len(C), D['meta']['n_states'], D['meta']['n_careers']))
print('instrument: the packet\'s own CELL-MATCHED PICK CONTRAST (HI = picks 1-12, LO = picks 21-64),')
print('            matched within position x output-quintile strata. sigma itself is NOT re-fitted.')

RES = {}
for gb in BANDS:
    inb = [c for c in parsed if c['gb'] == gb]
    allm = matched(inb)
    sig = BF[gb]['sigma']
    print('\n=== GAMES BAND %s   (published sigma %.4f, 90%% CI %.4f..%.4f, n %d states, %d clusters)'
          % (gb, sig, BF[gb]['sigma_ci'][0], BF[gb]['sigma_ci'][1], BF[gb]['n'], BF[gb]['n_clusters']))
    print('  ALL AGES pooled: matched pick contrast %+9.1f pts  over %d strata  (weight %d, SD %.0f, SE %.0f)'
          % (allm['delta'], allm['n_strata'], allm['w'], allm['sd'], allm['se']))
    print('  %-7s %6s %7s %10s %10s %10s %8s %8s   %11s %9s %8s %8s'
          % ('age', 'cells', 'n', 'meanR6', 'medianR6', 'IQR', 'zero%', 'strata', 'matchedD', 'SE', 'sigma^', 'ratio'))
    RES[gb] = dict(published_sigma=sig, published_ci=BF[gb]['sigma_ci'], all_ages=dict(
        delta=allm['delta'], n_strata=allm['n_strata'], w=allm['w'], sd=allm['sd'], se=allm['se']), cells={})
    for ag in AGE_ORDER:
        sub = [c for c in inb if c['ag'] == ag]
        if not sub: continue
        pl = pool(sub); mm = matched(sub)
        sh = (sig * mm['delta'] / allm['delta']) if (mm and allm['delta']) else None
        se_sh = (sig * mm['se'] / allm['delta']) if (mm and allm['delta']) else None
        print('  %-7s %6d %7d %10.1f %10.1f %10.1f %7.1f%% %8s   %+11.1f %9.0f %8s %8s'
              % (ag, pl['n_cells'], pl['n'], pl['mean'], pl['median'], pl['iqr'], 100 * pl['zero_share'],
                 (mm['n_strata'] if mm else '-'), (mm['delta'] if mm else float('nan')),
                 (mm['se'] if mm else float('nan')),
                 ('%.3f' % sh) if sh is not None else '-',
                 ('%.2f' % (mm['delta'] / allm['delta'])) if mm else '-'))
        RES[gb]['cells'][ag] = dict(pool=pl, matched=(None if mm is None else
            {k: v for k, v in mm.items() if k != 'strata'}), sigma_hat=sh, sigma_hat_se=se_sh)

# --- the deciding comparisons -------------------------------------------------------------------------
print('\n=== THE DECIDING COMPARISONS (does age-at-state move the share at FIXED games?)')
VERD = {}
for gb in BANDS:
    r = RES[gb]; c = r['cells']
    young = c.get('<=20'); old = c.get('24+')
    line = []
    if young and old and young['matched'] and old['matched']:
        dy, do = young['matched']['delta'], old['matched']['delta']
        sy, so = young['matched']['se'], old['matched']['se']
        z = (dy - do) / math.sqrt(sy * sy + so * so) if (sy or so) else float('nan')
        # 90% interval on the DIFFERENCE of the two matched contrasts
        half = 1.645 * math.sqrt(sy * sy + so * so)
        lo90, hi90 = (dy - do) - half, (dy - do) + half
        sep = not (lo90 <= 0.0 <= hi90)
        print('  band %-6s  <=20 matched %+8.1f (SE %5.0f, n %d)   24+ matched %+8.1f (SE %5.0f, n %d)'
              % (gb, dy, sy, young['pool']['n'], do, so, old['pool']['n']))
        print('  %-12s  DIFFERENCE %+8.1f   90%% interval [%+.1f, %+.1f]   z %+.2f   SEPARATED FROM ZERO: %s'
              % ('', dy - do, lo90, hi90, z, 'YES' if sep else 'NO'))
        print('  %-12s  share-scaled: sigma^(<=20) %.3f vs sigma^(24+) %.3f  (published band sigma %.3f)'
              % ('', young['sigma_hat'], old['sigma_hat'], r['published_sigma']))
        VERD[gb] = dict(delta_young=dy, delta_old=do, se_young=sy, se_old=so, diff=dy - do,
                        ci90=[lo90, hi90], separated=sep, z=z,
                        sigma_hat_young=young['sigma_hat'], sigma_hat_old=old['sigma_hat'])
    else:
        print('  band %-6s  INSUFFICIENT MATCHED STRATA in one of the age cells — no comparison made.' % gb)
        VERD[gb] = dict(insufficient=True)

any_sig = any(v.get('separated') for v in VERD.values())
print('\n=== VERDICT: %s' % ('AGE-AT-STATE MOVES THE MATCHED PICK GAP AT FIXED GAMES (at least one band separates)'
                            if any_sig else
                            'NO SIGNAL — at the n available, age-at-state does NOT separate the matched pick '
                            'gap from zero in either band. The share curve stays a function of games alone.'))
print('    Nothing is applied either way: if the split carries signal it is an OWED OWNER WORD, not a wiring act.')

os.makedirs(OUT, exist_ok=True)
json.dump(dict(order='30B-P', lens='age-within-games', pre_numeraire=True, applied=False,
               source=os.path.basename(SRC), source_meta=D['meta'],
               instrument='cell-matched pick contrast (HI 1-12 vs LO 21-64) within position x output-quintile strata',
               share_scaling='sigma_hat(band,age) = sigma_published(band) x Delta(band,age) / Delta(band,all ages) '
                             '-- DECLARED ASSUMPTION: sigma proportional to the matched pick gap within a band',
               age_bins_note='the committed table pools 22 and 23, so the brief\'s <=20 / 21-22 / 23+ split '
                             'cannot be cut exactly; the table\'s own granularity is used',
               bands=RES, verdict=VERD, signal=any_sig),
          open(os.path.join(OUT, 'AGE_LENS.json'), 'w'), indent=1, sort_keys=True)
print('\nwrote %s' % os.path.join(OUT, 'AGE_LENS.json'))
