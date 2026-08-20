#!/usr/bin/env python
# ORDER 32 SEAT S1 — STEPS 2-3: distributions, the three age-referenced constructions, and the
# predictive over/under-bar tables. READ-ONLY. Consumes SEASON_TABLE.json (step 1).
# All definitions per PREREG_S1.md (pushed before step 1 ran).
import json, os, math, collections

OUT = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(OUT, 'SEASON_TABLE.json')))
ROWS = T['rows']; BARS = T['meta']['bars']; FE26 = T['meta']['fe26']
POSL = ['KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF']
TALL = {'KPD', 'KPF', 'RUCK'}
CLS = lambda pos: 'TALL' if pos in TALL else 'SMALL'
FIT_LAST = 2021           # fitted window 2005-2021 (>=5 subsequent seasons)
DIST_LAST = 2025          # distribution tables: completed seasons only
MATURE = (24, 28)         # mature reference band
THIN = 15

L = []
P = L.append

def q(xs, p):
    """Type-7 linear-interpolation quantile."""
    xs = sorted(xs)
    if not xs: return float('nan')
    if len(xs) == 1: return xs[0]
    h = (len(xs) - 1) * p
    lo = int(math.floor(h)); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (h - lo) * (xs[hi] - xs[lo])

def ecdf_at(xs, v):
    """Share of xs strictly below v (the under-bar reading: avg < bar)."""
    xs = sorted(xs)
    return sum(1 for x in xs if x < v) / len(xs) if xs else float('nan')

def sd(xs):
    if len(xs) < 2: return float('nan')
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

full = [r for r in ROWS if r['full']]
dist_rows = [r for r in full if r['year'] <= DIST_LAST]           # distributions (no follow-through needed)
fit_rows = [r for r in full if r['year'] <= FIT_LAST]             # every predictive number

def band(age): return age if 18 <= age <= 23 else (18 if age < 18 else 24)
AGES = [18, 19, 20, 21, 22, 23]

# ================= SECTION A — DISTRIBUTIONS =================
P('=' * 100)
P('SECTION A — FULL-SEASON AVG DISTRIBUTIONS BY AGE x POS (completed seasons 2005-%d, games>=10)' % DIST_LAST)
P('  "pctl of flat bar" = share of the cell strictly under the flat Ruling-1 bar (the flag rate the')
P('  gate applies to that cell). THIN = n<%d.' % THIN)
P('=' * 100)
hdr = '%-5s %-5s %5s %7s %6s | %6s %6s %6s %6s %6s | %8s %10s %s'
P(hdr % ('pos', 'age', 'n', 'mean', 'sd', 'p10', 'p25', 'p50', 'p75', 'p90', 'flatbar', 'under-bar%', ''))
DIST = {}
for pos in POSL:
    for a in AGES + ['24-28', '24+']:
        if a == '24-28': sel = [r for r in dist_rows if r['pos'] == pos and MATURE[0] <= r['age'] <= MATURE[1]]
        elif a == '24+': sel = [r for r in dist_rows if r['pos'] == pos and r['age'] >= 24]
        else: sel = [r for r in dist_rows if r['pos'] == pos and band(r['age']) == a]
        xs = [r['avg'] for r in sel]
        DIST[(pos, a)] = xs
        if not xs:
            P(hdr % (pos, a, 0, '-', '-', '-', '-', '-', '-', '-', '%.1f' % BARS[pos], '-', 'EMPTY')); continue
        P(hdr % (pos, a, len(xs), '%.1f' % (sum(xs)/len(xs)), '%.1f' % sd(xs),
                 '%.1f' % q(xs, .10), '%.1f' % q(xs, .25), '%.1f' % q(xs, .50),
                 '%.1f' % q(xs, .75), '%.1f' % q(xs, .90),
                 '%.1f' % BARS[pos], '%.0f%%' % (100*ecdf_at(xs, BARS[pos])),
                 'THIN' if len(xs) < THIN else ''))
    P('-' * 100)

# class-pooled distributions (the thin-cell fallback basis)
P('')
P('CLASS-POOLED (TALL=KPD/KPF/RUCK, SMALL=MID/SD/SF) — same cut. NOTE: a class pools positions with')
P('different LEVELS, so pooled quantiles serve OFFSET/RATE constructions, never a level directly.')
P(hdr % ('class', 'age', 'n', 'mean', 'sd', 'p10', 'p25', 'p50', 'p75', 'p90', '-', '-', ''))
for cls in ['TALL', 'SMALL']:
    for a in AGES + ['24-28']:
        if a == '24-28': sel = [r for r in dist_rows if CLS(r['pos']) == cls and MATURE[0] <= r['age'] <= MATURE[1]]
        else: sel = [r for r in dist_rows if CLS(r['pos']) == cls and band(r['age']) == a]
        xs = [r['avg'] for r in sel]
        DIST[(cls, a)] = xs
        if not xs: P(hdr % (cls, a, 0, '-','-','-','-','-','-','-','-','-','EMPTY')); continue
        P(hdr % (cls, a, len(xs), '%.1f' % (sum(xs)/len(xs)), '%.1f' % sd(xs),
                 '%.1f' % q(xs, .10), '%.1f' % q(xs, .25), '%.1f' % q(xs, .50),
                 '%.1f' % q(xs, .75), '%.1f' % q(xs, .90), '-', '-',
                 'THIN' if len(xs) < THIN else ''))

# sensitivity: games>=6, and season-pos labelling
P('')
P('SENSITIVITY — under-flat-bar share by age (all positions pooled at each age):')
P('  basis                          ' + ''.join('%8s' % a for a in AGES) + '%8s' % '24+')
for name, rowsel, poskey in [
        ('FULL seasons, POS=future',  [r for r in ROWS if r['full'] and r['year'] <= DIST_LAST], 'pos'),
        ('games>=6,     POS=future',  [r for r in ROWS if r['games'] >= 6*r['u'] and r['year'] <= DIST_LAST], 'pos'),
        ('FULL seasons, POS=season',  [r for r in ROWS if r['full'] and r['year'] <= DIST_LAST], 'season_pos')]:
    cells = []
    for a in AGES + ['24+']:
        sel = [r for r in rowsel if (r['age'] >= 24 if a == '24+' else band(r['age']) == a)]
        u = [1 for r in sel if r['avg'] < BARS.get(r[poskey], BARS[r['pos']])]
        cells.append('%6.0f%%' % (100*len(u)/len(sel)) if sel else '     -')
    P('  %-30s' % name + ' '.join(cells))

# ================= SECTION B — THE CONSTRUCTIONS =================
P('')
P('=' * 100)
P('SECTION B — THE THREE AGE-REFERENCED CONSTRUCTIONS (values), CAP LAW bar<=flat applied everywhere')
P('=' * 100)

# --- C1: age-quantile-matched (distributions 2005-2025) ---
C1 = {}; C1meta = {}
P('')
P('C1 — AGE-QUANTILE-MATCHED. q*(pos) = flat bar\'s percentile inside the mature 24-28 distribution;')
P('bar(a,pos) = that percentile of the age-a distribution. Fallback chain when a cell is THIN:')
P('(pos,a) -> (pos, ages a..a+1 pooled) -> flat (no relief), each use printed.')
for pos in POSL:
    qstar = ecdf_at(DIST[(pos, '24-28')], BARS[pos])
    C1meta[pos] = dict(qstar=qstar, n_mature=len(DIST[(pos, '24-28')]))
    for a in AGES:
        xs = DIST[(pos, a)]; src = '%s,%d' % (pos, a)
        if len(xs) < THIN and a < 23:
            xs2 = DIST[(pos, a)] + DIST[(pos, a + 1)]
            if len(xs2) >= THIN: xs, src = xs2, '%s,%d-%d POOLED' % (pos, a, a+1)
        if len(xs) < THIN:
            C1[(pos, a)] = BARS[pos]; C1meta[(pos, a)] = dict(n=len(xs), src='FLAT (thin)'); continue
        v = min(q(xs, qstar), BARS[pos])
        C1[(pos, a)] = v; C1meta[(pos, a)] = dict(n=len(xs), src=src)
P('%-5s  q*     ' % 'pos' + ''.join('%14s' % a for a in AGES) + '%8s' % 'flat')
for pos in POSL:
    P('%-5s %5.2f  ' % (pos, C1meta[pos]['qstar']) +
      ''.join('%8.1f %-5s' % (C1[(pos, a)], '(n%d)' % C1meta[(pos, a)]['n']) for a in AGES) +
      '%8.1f' % BARS[pos])
    fb = ['age %d: %s' % (a, C1meta[(pos, a)]['src']) for a in AGES if 'POOLED' in C1meta[(pos, a)]['src'] or 'FLAT' in C1meta[(pos, a)]['src']]
    if fb: P('       fallbacks: ' + '; '.join(fb))

# --- C2: equal false-flag anchoring (fitted window, deliverer seasons) ---
P('')
P('C2 — EQUAL FALSE-FLAG ANCHORING (fitted 2005-%d). r_mature(pos) = share of age-24+ DELIVERER' % FIT_LAST)
P('seasons under the flat bar. bar(a,pos) = r_mature-quantile of age-a deliverer-season avgs.')
P('Deliverer season = a full season whose player posts a later delivered season (games>=10 &')
P('avg>=flat). Same THIN fallback chain as C1, on the deliverer populations.')
C2 = {}; C2meta = {}
DELIV = collections.defaultdict(list)
for r in fit_rows:
    if r['delivered_later']:
        DELIV[(r['pos'], band(r['age']))].append(r['avg'])
        DELIV[(r['pos'], '24+')] if False else None
for pos in POSL:
    mat = [r['avg'] for r in fit_rows if r['pos'] == pos and r['age'] >= 24 and r['delivered_later']]
    rmat = ecdf_at(mat, BARS[pos])
    C2meta[pos] = dict(r_mature=rmat, n_mature_deliv=len(mat))
    for a in AGES:
        xs = DELIV[(pos, a)]; src = '%s,%d' % (pos, a)
        if len(xs) < THIN and a < 23:
            xs2 = DELIV[(pos, a)] + DELIV[(pos, a + 1)]
            if len(xs2) >= THIN: xs, src = xs2, '%s,%d-%d POOLED' % (pos, a, a+1)
        if len(xs) < THIN:
            C2[(pos, a)] = BARS[pos]; C2meta[(pos, a)] = dict(n=len(xs), src='FLAT (thin)'); continue
        v = min(q(xs, rmat), BARS[pos])
        C2[(pos, a)] = v; C2meta[(pos, a)] = dict(n=len(xs), src=src)
P('%-5s r_mat  ' % 'pos' + ''.join('%14s' % a for a in AGES) + '%8s' % 'flat')
for pos in POSL:
    P('%-5s %5.2f  ' % (pos, C2meta[pos]['r_mature']) +
      ''.join('%8.1f %-5s' % (C2[(pos, a)], '(n%d)' % C2meta[(pos, a)]['n']) for a in AGES) +
      '%8.1f' % BARS[pos])
    fb = ['age %d: %s' % (a, C2meta[(pos, a)]['src']) for a in AGES if 'POOLED' in C2meta[(pos, a)]['src'] or 'FLAT' in C2meta[(pos, a)]['src']]
    if fb: P('       fallbacks: ' + '; '.join(fb))

# --- C3: development-curve offset, class-pooled (distributions 2005-2025) ---
P('')
P('C3 — DEVELOPMENT-CURVE OFFSET, CLASS-POOLED. delta(a,class) = mean(class 24-28) - mean(class,a),')
P('floored at 0 and made non-increasing in age (pool-adjacent-violators). bar(a,pos)=flat-delta.')
C3 = {}; C3meta = {}
for cls in ['TALL', 'SMALL']:
    mm = sum(DIST[(cls, '24-28')]) / len(DIST[(cls, '24-28')])
    raw = {}
    for a in AGES:
        xs = DIST[(cls, a)]
        raw[a] = (mm - sum(xs)/len(xs)) if xs else None
        C3meta[(cls, a)] = dict(n=len(xs))
    # fill empty from neighbour below (older) — disclosed
    for a in AGES:
        if raw[a] is None: raw[a] = raw.get(a + 1) or 0.0
    d = {a: max(0.0, raw[a]) for a in AGES}
    # enforce non-increasing in age by PAV (pool adjacent violators, averaging n-weighted)
    seq = [[a, d[a], max(1, len(DIST[(cls, a)]))] for a in AGES]
    i = 0
    while i < len(seq) - 1:
        if seq[i][1] < seq[i + 1][1] - 1e-12:
            n1, n2 = seq[i][2], seq[i+1][2]
            v = (seq[i][1]*n1 + seq[i+1][1]*n2) / (n1+n2)
            seq[i] = [seq[i][0], v, n1+n2]; del seq[i+1]
            i = max(0, i - 1)
        else: i += 1
    dd = {}
    for blk in seq:
        pass
    # expand pooled blocks back to ages
    ages_left = list(AGES); j = 0
    exp = {}
    k = 0
    for blk_i, blk in enumerate(seq):
        # each block covers ages from its start to just before next block's start
        start = blk[0]
        end = seq[blk_i + 1][0] - 1 if blk_i + 1 < len(seq) else AGES[-1]
        for a in range(start, end + 1):
            if a in AGES: exp[a] = blk[1]
    for a in AGES:
        C3meta[(cls, a)]['raw'] = raw[a]; C3meta[(cls, a)]['delta'] = exp[a]
    C3meta[cls] = dict(mature_mean=mm, n_mature=len(DIST[(cls, '24-28')]))
    for pos in (TALL if cls == 'TALL' else set(POSL) - TALL):
        for a in AGES:
            C3[(pos, a)] = max(0.0, BARS[pos] - exp[a])
P('class  mature-mean   ' + ''.join('%16s' % a for a in AGES))
for cls in ['TALL', 'SMALL']:
    P('%-5s  %8.1f     ' % (cls, C3meta[cls]['mature_mean']) +
      ''.join('  d=%5.1f (n%4d)' % (C3meta[(cls, a)]['delta'], C3meta[(cls, a)]['n']) for a in AGES))
    P('       raw offsets: ' + ' '.join('%s:%.1f' % (a, C3meta[(cls, a)]['raw']) for a in AGES))
P('bar table (flat - delta):')
P('%-5s' % 'pos' + ''.join('%8s' % a for a in AGES) + '%8s' % 'flat')
for pos in POSL:
    P('%-5s' % pos + ''.join('%8.1f' % C3[(pos, a)] for a in AGES) + '%8.1f' % BARS[pos])

# ================= SECTION C — PREDICTIVE EVALUATION =================
P('')
P('=' * 100)
P('SECTION C — DOES THE BAR SEPARATE FUTURES? Fitted full seasons 2005-%d.' % FIT_LAST)
P('  deliv%%|over  = share of over-bar seasons whose player later delivered (higher = good pass)')
P('  deliv%%|under = share of under-bar seasons whose player later delivered (a flag on these rows is')
P('                 a FALSE FLAG on an eventually-delivered career)')
P('  FF = false-flag rate: P(under-bar | eventual deliverer). MISS = P(over-bar | washout).')
P('  RR = relative risk of washout given under-bar vs over-bar (separation strength; 1.0 = none).')
P('  SDV = subsequent delivered value (v0-surplus points, median [mean]).')
P('=' * 100)
n_active_nondeliv = len(set(r['key'] for r in fit_rows if not r['delivered_later'] and not r['retired'] and r['last_played'] >= 2025))
P('Disclosure: %d players in the fitted window are counted washout-side on some seasons while still' % n_active_nondeliv)
P('active in 2025-26 without a later delivered season (>=5 years observed; prereg treats as final).')

def barof(C, pos, a):
    if C == 'C0': return BARS[pos]
    M = {'C1': C1, 'C2': C2, 'C3': C3}[C]
    return M[(pos, min(max(band(a), 18), 23))] if band(a) <= 23 else BARS[pos]

def evalrows(C, sel):
    over = [r for r in sel if r['avg'] >= barof(C, r['pos'], r['age'])]
    under = [r for r in sel if r['avg'] < barof(C, r['pos'], r['age'])]
    def dl(g): return sum(1 for r in g if r['delivered_later'])
    no, nu = len(over), len(under)
    do, du = dl(over), dl(under)
    ndeliv = do + du; nwash = no + nu - ndeliv
    ff = du / ndeliv if ndeliv else float('nan')
    miss = (no - do) / nwash if nwash else float('nan')
    p_wu = (nu - du) / nu if nu else float('nan')
    p_wo = (no - do) / no if no else float('nan')
    rr = p_wu / p_wo if no and nu and p_wo > 0 else float('nan')
    sdvo = [r['sdv'] for r in over]; sdvu = [r['sdv'] for r in under]
    return dict(n=no+nu, n_over=no, n_under=nu,
                deliv_over=100*do/no if no else float('nan'),
                deliv_under=100*du/nu if nu else float('nan'),
                FF=100*ff, MISS=100*miss, RR=rr,
                sdv_over='%.0f [%.0f]' % (q(sdvo,.5), sum(sdvo)/len(sdvo)) if sdvo else '-',
                sdv_under='%.0f [%.0f]' % (q(sdvu,.5), sum(sdvu)/len(sdvu)) if sdvu else '-')

def prow(tag, e):
    P('%-26s %5d %6d %6d %8s %8s %7s %7s %6s %14s %14s' % (
        tag, e['n'], e['n_over'], e['n_under'],
        '-' if e['deliv_over'] != e['deliv_over'] else '%.0f%%' % e['deliv_over'],
        '-' if e['deliv_under'] != e['deliv_under'] else '%.0f%%' % e['deliv_under'],
        '-' if e['FF'] != e['FF'] else '%.0f%%' % e['FF'],
        '-' if e['MISS'] != e['MISS'] else '%.0f%%' % e['MISS'],
        '-' if e['RR'] != e['RR'] else '%.2f' % e['RR'],
        e['sdv_over'], e['sdv_under']))

BANDS = [('18-19', lambda r: r['age'] <= 19), ('20', lambda r: band(r['age']) == 20),
         ('21', lambda r: band(r['age']) == 21), ('22', lambda r: band(r['age']) == 22),
         ('23', lambda r: band(r['age']) == 23), ('18-20 all', lambda r: r['age'] <= 20),
         ('21-23 all', lambda r: 21 <= r['age'] <= 23), ('24+ (flat by design)', lambda r: r['age'] >= 24)]
hdr2 = '%-26s %5s %6s %6s %8s %8s %7s %7s %6s %14s %14s' % (
    'cut', 'n', 'nOver', 'nUndr', 'dl|over', 'dl|under', 'FF', 'MISS', 'RR', 'SDV over', 'SDV under')
for C in ['C0', 'C1', 'C2', 'C3']:
    P('')
    P('CONSTRUCTION %s %s' % (C, '(current flat bar)' if C == 'C0' else ''))
    P(hdr2)
    for tag, f in BANDS:
        prow('ALL-POS ' + tag, evalrows(C, [r for r in fit_rows if f(r)]))
    for cls in ['TALL', 'SMALL']:
        for tag, f in BANDS[:1] + BANDS[5:7]:
            prow('%s %s' % (cls, tag), evalrows(C, [r for r in fit_rows if f(r) and CLS(r['pos']) == cls]))

# per-position young detail under C0 (the diagnosis) — full six, fitted
P('')
P('C0 PER-POSITION DETAIL, ages 18-20 (the diagnosis rows):')
P(hdr2)
for pos in POSL:
    prow('%s 18-20' % pos, evalrows('C0', [r for r in fit_rows if r['age'] <= 20 and r['pos'] == pos]))

# sensitivity: fitted window extended to 2022
P('')
P('SENSITIVITY — fitted window extended to 2022 (each season still has >=4 subsequent):')
fit22 = [r for r in full if r['year'] <= 2022]
P(hdr2)
for C in ['C0', 'C2', 'C3']:
    e = evalrows(C, [r for r in fit22 if r['age'] <= 20]); prow('%s ALL-POS 18-20 (<=2022)' % C, e)

json.dump(dict(C1={('%s|%d' % k): v for k, v in C1.items()},
               C2={('%s|%d' % k): v for k, v in C2.items()},
               C3={('%s|%d' % k): v for k, v in C3.items()},
               C1meta={str(k): v for k, v in C1meta.items()},
               C2meta={str(k): v for k, v in C2meta.items()},
               C3meta={str(k): v for k, v in C3meta.items()},
               bars_flat=BARS, thin=THIN, fitted_last=FIT_LAST),
          open(os.path.join(OUT, 'CONSTRUCTIONS_S1.json'), 'w'), indent=1)
open(os.path.join(OUT, 'MEASURE_S1_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
