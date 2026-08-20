#!/usr/bin/env python3
"""ORDER D8 — THE MOVERS LIST. Base board (dial unset) -> priced board (RL_O33_TAPEROFF=1).

READ-ONLY over two built board artifacts. Emits MOVERS_D8.json, MOVERS_D8.md, and the band
attribution. Names illustrate; they never gate.

  D8BASE   base board json      D8PRICED  priced board json
  D8BANDS_OFF / D8BANDS_ON      the band/inversion measurements (d8_bands.py output)
  D8EVID   evidence directory to write into
"""
import os, sys, json, hashlib, datetime, collections

BASE = os.environ['D8BASE']; PRICED = os.environ['D8PRICED']
EVID = os.environ['D8EVID']
BOFF = os.environ.get('D8BANDS_OFF'); BON = os.environ.get('D8BANDS_ON')

md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()


def load(p):
    d = json.load(open(p))
    return d, {r['key']: r for r in d['active']}, {r['key']: r for r in d.get('back', [])}


bd, ba, bb_ = load(BASE)
pd_, pa, pb_ = load(PRICED)
assert set(ba) == set(pa), 'row universe moved: %d vs %d' % (len(ba), len(pa))

AGE_BANDS = [('<=19', lambda a: a is not None and a <= 19),
             ('20-21', lambda a: a is not None and 20 <= a <= 21),
             ('22-23', lambda a: a is not None and 22 <= a <= 23),
             ('24-26', lambda a: a is not None and 24 <= a <= 26),
             ('27+',   lambda a: a is not None and a >= 27)]
POS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']


def band_of(a):
    for nm, f in AGE_BANDS:
        if f(a):
            return nm
    return 'unknown'


rows = []
for k in sorted(ba):
    b, p = ba[k], pa[k]
    d = p['v'] - b['v']
    rows.append({'key': k, 'name': p['name'], 'age': p.get('age'), 'pos': p.get('gf'),
                 'grp': p.get('grp'), 'club': p.get('club'), 'games': p.get('g'),
                 'before': b['v'], 'after': p['v'], 'delta': d,
                 'pct': (100.0 * d / b['v']) if b['v'] else None,
                 'band': band_of(p.get('age'))})

# ranks on each side (overall and within position) — meaningful across a lever, ties by key
for fld, val in (('_prev_rank', 'before'), ('_cur_rank', 'after')):
    for i, r in enumerate(sorted(rows, key=lambda r: (-r[val], r['key'])), 1):
        r[fld] = i
for ps in set(r['pos'] for r in rows):
    sub = [r for r in rows if r['pos'] == ps]
    for fld, val in (('_prev_pos_rank', 'before'), ('_cur_pos_rank', 'after')):
        for i, r in enumerate(sorted(sub, key=lambda r: (-r[val], r['key'])), 1):
            r[fld] = i

movers = [r for r in rows if r['delta'] != 0]
up = [r for r in movers if r['delta'] > 0]
dn = [r for r in movers if r['delta'] < 0]
movers.sort(key=lambda r: (-r['delta'], r['key']))

sum_b = sum(r['before'] for r in rows); sum_p = sum(r['after'] for r in rows)

# back rows (board-history-only; not the owner's ranking)
back = []
for k in sorted(set(bb_) & set(pb_)):
    d = pb_[k]['v'] - bb_[k]['v']
    if d:
        back.append({'key': k, 'name': pb_[k]['name'], 'age': pb_[k].get('age'),
                     'pos': pb_[k].get('gf'), 'before': bb_[k]['v'], 'after': pb_[k]['v'], 'delta': d})

# ---- attribution: age band x position ----------------------------------------------------------
att = collections.OrderedDict()
for nm, _ in AGE_BANDS:
    for ps in POS:
        att[(nm, ps)] = {'n': 0, 'movers': 0, 'up': 0, 'down': 0, 'delta': 0, 'before': 0}
for r in rows:
    k = (r['band'], r['pos'])
    if k not in att:
        att[k] = {'n': 0, 'movers': 0, 'up': 0, 'down': 0, 'delta': 0, 'before': 0}
    c = att[k]; c['n'] += 1; c['before'] += r['before']; c['delta'] += r['delta']
    if r['delta']:
        c['movers'] += 1
        c['up' if r['delta'] > 0 else 'down'] += 1

by_band = collections.OrderedDict()
for nm, _ in AGE_BANDS:
    s = [r for r in rows if r['band'] == nm]
    m = [r for r in s if r['delta']]
    by_band[nm] = {'n': len(s), 'movers': len(m), 'up': sum(1 for r in m if r['delta'] > 0),
                   'down': sum(1 for r in m if r['delta'] < 0),
                   'delta': sum(r['delta'] for r in s), 'before': sum(r['before'] for r in s)}
by_pos = collections.OrderedDict()
for ps in POS:
    s = [r for r in rows if r['pos'] == ps]
    m = [r for r in s if r['delta']]
    by_pos[ps] = {'n': len(s), 'movers': len(m), 'up': sum(1 for r in m if r['delta'] > 0),
                  'down': sum(1 for r in m if r['delta'] < 0),
                  'delta': sum(r['delta'] for r in s), 'before': sum(r['before'] for r in s)}

bands = {}
for tag, pth in (('off', BOFF), ('on', BON)):
    if pth and os.path.exists(pth):
        bands[tag] = json.load(open(pth))

out = {
    'base_board_md5': md5(BASE), 'priced_board_md5': md5(PRICED),
    'n_active': len(rows), 'sum_before': sum_b, 'sum_after': sum_p,
    'sum_delta': sum_p - sum_b, 'sum_pct': 100.0 * (sum_p - sum_b) / sum_b,
    'n_movers': len(movers), 'n_up': len(up), 'n_down': len(dn),
    'n_unmoved': len(rows) - len(movers),
    'total_up': sum(r['delta'] for r in up), 'total_down': sum(r['delta'] for r in dn),
    'by_age_band': by_band, 'by_position': by_pos,
    'by_band_x_pos': {'%s|%s' % k: v for k, v in att.items() if v['n']},
    'back_movers': back,
    'movers': movers, 'all_rows': rows,
    'inversions': {t: {'count': bands[t]['inversions'], 'rows': bands[t]['inversion_rows']}
                   for t in bands},
    'frac_check': {t: {'domain_rows': bands[t]['frac_domain_rows'],
                       'domain_divergences': bands[t]['frac_domain_divergences'],
                       'row_checks': bands[t]['frac_row_checks'],
                       'row_divergences': bands[t]['frac_row_divergences'],
                       'flags': bands[t]['flags']} for t in bands},
    'uncomp_cal': {t: bands[t]['uncomp_cal'] for t in bands},
}
json.dump(out, open(os.path.join(EVID, 'MOVERS_D8.json'), 'w'), indent=1, sort_keys=True)

# ---- the ceiling delta per row, for the explanation column --------------------------------------
ceil = {}
if 'off' in bands and 'on' in bands:
    o = {r['key']: r for r in bands['off']['rows']}
    n = {r['key']: r for r in bands['on']['rows']}
    for k in o:
        if k in n:
            ceil[k] = {'b5_before': o[k]['b5'], 'b5_after': n[k]['b5'],
                       'b5_delta': n[k]['b5'] - o[k]['b5']}
for r in rows:
    r.update(ceil.get(r['key'], {}))

L = []
P = lambda s='': L.append(s)
P('=' * 118)
P('ORDER D8 — THE MOVERS LIST.  base (dial unset) -> priced (RL_O33_TAPEROFF=1).  PRICED, NOT ADOPTED.')
P('=' * 118)
P('base board   %s   total %d   n=%d' % (out['base_board_md5'], sum_b, len(rows)))
P('priced board %s   total %d   n=%d' % (out['priced_board_md5'], sum_p, len(rows)))
P('delta        %+d  (%+.4f%%)' % (out['sum_delta'], out['sum_pct']))
P('movers       %d   UP %d   DOWN %d   unmoved %d' % (len(movers), len(up), len(dn), out['n_unmoved']))
P('total up     %+d      total down %+d' % (out['total_up'], out['total_down']))
P()
P('AGE BAND'.ljust(10) + 'n'.rjust(5) + 'movers'.rjust(8) + 'up'.rjust(6) + 'down'.rjust(6)
  + 'delta'.rjust(10) + '%band'.rjust(9))
for nm, c in by_band.items():
    P(nm.ljust(10) + str(c['n']).rjust(5) + str(c['movers']).rjust(8) + str(c['up']).rjust(6)
      + str(c['down']).rjust(6) + ('%+d' % c['delta']).rjust(10)
      + ('%+.2f%%' % (100.0 * c['delta'] / c['before']) if c['before'] else '-').rjust(9))
P()
P('POSITION'.ljust(10) + 'n'.rjust(5) + 'movers'.rjust(8) + 'up'.rjust(6) + 'down'.rjust(6)
  + 'delta'.rjust(10) + '%pos'.rjust(9))
for ps, c in by_pos.items():
    P(ps.ljust(10) + str(c['n']).rjust(5) + str(c['movers']).rjust(8) + str(c['up']).rjust(6)
      + str(c['down']).rjust(6) + ('%+d' % c['delta']).rjust(10)
      + ('%+.2f%%' % (100.0 * c['delta'] / c['before']) if c['before'] else '-').rjust(9))
P()
P('AGE BAND x POSITION  (n / movers / delta)')
P(' ' .ljust(10) + ''.join(ps.rjust(18) for ps in POS))
for nm, _ in AGE_BANDS:
    line = nm.ljust(10)
    for ps in POS:
        c = att.get((nm, ps), {'n': 0, 'movers': 0, 'delta': 0})
        line += ('%d/%d/%+d' % (c['n'], c['movers'], c['delta'])).rjust(18)
    P(line)
P()
P('THE FULL MOVERS LIST — sorted by delta')
P('%-4s %-26s %-4s %-5s %8s %8s %8s %8s %10s' % ('#', 'name', 'age', 'pos', 'before', 'after',
                                                 'delta', '%', 'ceil d b5'))
for i, r in enumerate(movers, 1):
    P('%-4d %-26s %-4s %-5s %8d %8d %+8d %+7.2f%% %10s'
      % (i, r['name'][:26], r['age'], r['pos'], r['before'], r['after'], r['delta'], r['pct'],
         ('%+.1f' % r['b5_delta']) if 'b5_delta' in r else '?'))
P()
if back:
    P('BACK ROWS (board-history-only, not the owner ranking): %d movers' % len(back))
    for r in back:
        P('   %-26s %-4s %-5s %8d -> %8d  %+d' % (r['name'][:26], r['age'], r['pos'],
                                                  r['before'], r['after'], r['delta']))
else:
    P('BACK ROWS (board-history-only): 0 movers')
P()
for t in ('off', 'on'):
    if t in bands:
        P('CEILING v-INVERSIONS (band[5] < band[4])  dial %-3s : %d of %d rows'
          % (t, bands[t]['inversions'], bands[t]['n_rows']))
P()
for t in ('off', 'on'):
    if t in bands:
        P('RL_UNCOMP load-time calibration, dial %s:' % t)
        for l in bands[t]['uncomp_cal']:
            P('   ' + l)
open(os.path.join(EVID, 'MOVERS_D8_out.txt'), 'w').write('\n'.join(L) + '\n')

# ---- the owner-facing markdown (house / v757 movers format) ---------------------------------------
M = []
Q = lambda s='': M.append(s)
Q('# THE MOVERS — ORDER D8, THE CEILING-ONLY LEG (B-3 alone, the tall ladder dead)')
Q()
Q('> **PRICED, NOT ADOPTED. NOTHING IS GREENLIT.** The live board is **unmoved**. This table is the')
Q('> owner\'s probation look (register v772: *"happy to look at still boosting the younger players')
Q('> pending a look at the movers list"*), sequenced ahead of the R23 ingestion by v793 so the round')
Q('> movers are lever-constant. With the dial `RL_O33_TAPEROFF` unset the live board')
Q('> `a05fe951f78482c70520480e184c80ec` reproduces **BYTE-EXACT** (PREREG_D8 F1, measured twice).')
Q('>')
Q('> **WHAT MOVED, MECHANICALLY.** ORDER B\'s v7 ascending age-taper on the q97 **ceiling band** is not')
Q('> applied: `asc == 1`, so `band[5]` stays `max(q97m, q90)` exactly as `_b6_core` emits it. That is')
Q('> the derivation\'s own fitted answer — the boundary solution `asc*=1` in **every** band the taper')
Q('> bites. **No constant was fitted here and no parameter was added.** The OWNER-KILLED B-1 tall')
Q('> ladder does **not** fire: it is gated on `RL_O33`, which this dial never sets (F2, tested).')
Q()
Q('| | |')
Q('|---|---|')
Q('| base board (= the live board of record) | `%s` — total **%d** |' % (out['base_board_md5'], sum_b))
Q('| **PRICED** (`RL_O33_TAPEROFF=1`) | **`%s`** — total **%d** (%+d, %+.4f%%) |'
  % (out['priced_board_md5'], sum_p, out['sum_delta'], out['sum_pct']))
Q('| movers | **%d of %d** — **%d up**, **%d down**, %d unmoved |'
  % (len(movers), len(rows), len(up), len(dn), out['n_unmoved']))
Q('| total up / total down | **%+d** / **%+d** |' % (out['total_up'], out['total_down']))
for t, lbl in (('off', 'base'), ('on', 'priced')):
    if t in bands:
        Q('| ceiling v-inversions (`band[5] < band[4]`), %s | **%d** of %d rows |'
          % (lbl, bands[t]['inversions'], bands[t]['n_rows']))
Q('| store / as-of round | `cc02567f80bef39228f25854d121a766` / 22 |')
Q('| q97m | `cfdc73216c099e5e8f1fda3968f31c00` — **FROZEN**, not refitted (R-W6 is bake-time) |')
Q()
Q('**Columns.** `before` = the live board. `after` = the priced board. `Δ` and `%` are against the')
Q('live board. `Δ ceiling` is the row\'s own movement in `band[5]` (the object the dial acts on), in')
Q('band units — a row with `Δ ceiling = 0` did not have its ceiling touched and moved for the')
Q('second-order reason named in the summary. Names illustrate; they never gate.')
Q()
Q('## Summary by age band')
Q()
Q('| age band | n | movers | up | down | Δ | % of band |')
Q('|---|---:|---:|---:|---:|---:|---:|')
for nm, c in by_band.items():
    Q('| %s | %d | %d | %d | %d | %+d | %s |'
      % (nm, c['n'], c['movers'], c['up'], c['down'], c['delta'],
         ('%+.2f%%' % (100.0 * c['delta'] / c['before'])) if c['before'] else 'n/a'))
Q()
Q('## Summary by position')
Q()
Q('| position | n | movers | up | down | Δ | % of position |')
Q('|---|---:|---:|---:|---:|---:|---:|')
for ps, c in by_pos.items():
    Q('| %s | %d | %d | %d | %d | %+d | %s |'
      % (ps, c['n'], c['movers'], c['up'], c['down'], c['delta'],
         ('%+.2f%%' % (100.0 * c['delta'] / c['before'])) if c['before'] else 'n/a'))
Q()
Q('## Per-band attribution — age band x position (n / movers / Δ)')
Q()
Q('| age band | ' + ' | '.join(POS) + ' |')
Q('|---|' + '---:|' * len(POS))
for nm, _ in AGE_BANDS:
    cells = []
    for ps in POS:
        c = att.get((nm, ps), {'n': 0, 'movers': 0, 'delta': 0})
        cells.append('%d / %d / %+d' % (c['n'], c['movers'], c['delta']))
    Q('| %s | %s |' % (nm, ' | '.join(cells)))
Q()
Q('## THE FULL MOVERS LIST — every mover, sorted by Δ')
Q()
Q('| # | name | age | pos | before | after | Δ | % | Δ ceiling |')
Q('|---:|---|---:|---|---:|---:|---:|---:|---:|')
for i, r in enumerate(movers, 1):
    Q('| %d | %s | %s | %s | %d | %d | **%+d** | %+.2f%% | %s |'
      % (i, r['name'], r['age'], r['pos'], r['before'], r['after'], r['delta'], r['pct'],
         ('%+.1f' % r['b5_delta']) if 'b5_delta' in r else '?'))
Q()
if back:
    Q('## Back rows (board-history-only; NOT the owner ranking)')
    Q()
    Q('| name | age | pos | before | after | Δ |')
    Q('|---|---:|---|---:|---:|---:|')
    for r in back:
        Q('| %s | %s | %s | %d | %d | %+d |' % (r['name'], r['age'], r['pos'],
                                                r['before'], r['after'], r['delta']))
else:
    Q('## Back rows (board-history-only): **0 movers**')
Q()
open(os.path.join(EVID, 'MOVERS_D8.md'), 'w').write('\n'.join(M) + '\n')

print('\n'.join(L[:60]))
print('... full text at %s' % os.path.join(EVID, 'MOVERS_D8_out.txt'))
