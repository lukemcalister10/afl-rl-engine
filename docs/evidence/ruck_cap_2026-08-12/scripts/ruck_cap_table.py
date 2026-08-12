"""ORDER 20C — THE OWNER'S TABLE.

For every ruck whose `_ruc_prior_cap` binds under the FIX engine, three BOARD values read out of three
BUILT boards (never re-derived): BEFORE (the live board `94f1fec5`, HEAD engine, shipped defaults),
AFTER (the ORDER 20 par fix, `1dbd1480`), NO-CAP (the fix with `RL_RUC_PRIOR_CAP=99`).

CLASSIFICATION — the rule fixed in PREREG_RUCK_CAP.md, applied mechanically:
  PRIOR-DOMINATED   NO-CAP board value != AFTER board value.  The cap is load-bearing on his price.
  PRODUCTION-LED    NO-CAP board value == AFTER board value.  The cap binds only on the latent V0
                    scaffold `_v0_raw`, which the board does not read for him.
`bestlvl26` / `in_v0curve` are reported alongside as the mechanism, NOT used to classify.

Usage: python3 ruck_cap_table.py <SPdir> <outprefix>
"""
import json, sys, collections

SP, PRE = sys.argv[1].rstrip('/') + '/', sys.argv[2]

BOARDS = {'BEFORE': SP + 'board_HEAD_gate.json',
          'AFTER':  SP + 'board_FIX_gate.json',
          'NOCAP':  SP + 'board_FIX_dev_cap99.json'}
MD5 = {'BEFORE': '94f1fec59f99c59d5890d5975c79fa9b', 'AFTER': '1dbd1480a34c7823f330273211cbb76a',
       'NOCAP': None}

import hashlib
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

B = {}
for tag, path in BOARDS.items():
    d = json.load(open(path))
    rows = {}
    for st in ('active', 'back'):
        for r in d.get(st, []):
            rows[(st, r['key'])] = r
    B[tag] = rows
MD5['NOCAP'] = md5(BOARDS['NOCAP'])

probeH = json.load(open(SP + 'probe_HEAD.json'))
probeF = json.load(open(SP + 'probe_FIX.json'))
probeN = json.load(open(SP + 'probe_FIX_nocap.json'))
rowF = {r['key']: r for r in probeF['rows']}
rowN = {r['key']: r for r in probeN['rows']}


def channel(key):
    """WHICH consumer of the cap actually moved this row's price. Not a guess: the delisted remnant is
    `ev = round(0.02*v0_start)` (_merged_recover.py:2230), so a row whose ev equals that law at BOTH
    caps is priced by the scrap remnant and by nothing else."""
    a, b = rowF.get(key), rowN.get(key)
    if not a or not b or a['v'] == b['v']:
        return ''
    scrap = (abs(a['ev26'] - round(0.02 * a['v0_start'])) < 0.51 and
             abs(b['ev26'] - round(0.02 * b['v0_start'])) < 0.51)
    return 'DELISTED-SCRAP' if scrap else 'LIVE (sit-out blend)'
xH = {r['key']: r for r in json.load(open(SP + 'extra_HEAD.json'))['rows']}
xF = {r['key']: r for r in json.load(open(SP + 'extra_FIX.json'))['rows']}
capH = {r['key']: r for r in probeH['ruc_prior_cap'] if 'key' in r}
capF = {r['key']: r for r in probeF['ruc_prior_cap'] if 'key' in r}

OUT = {'board_md5': MD5, 'boards': {k: v for k, v in BOARDS.items()}}
L = []
P = L.append


def _pos(r):
    """The board writes `fut` as the SHARE VECTOR [[pos, w], ...], not a string. Take the top-weighted
    label. (Getting this wrong is what made the first run of this script report 17 phantom NON-RUCK
    movers; the guard below asserts against the engine's own ruck set instead of trusting this.)"""
    f = r.get('fut')
    if isinstance(f, str):
        return f
    if isinstance(f, list) and f:
        try:
            return max(f, key=lambda t: t[1])[0]
        except Exception:
            return str(f)
    return str(f)


def val(tag, key):
    for st in ('active', 'back'):
        r = B[tag].get((st, key))
        if r is not None:
            return r
    return None


# ---------------------------------------------------------------- board totals + the full-board diff
tot = {}
for tag in ('BEFORE', 'AFTER', 'NOCAP'):
    tot[tag] = {'all': 0, 'active': 0, 'back': 0, 'n': 0}
    for (st, k), r in B[tag].items():
        tot[tag]['all'] += r['v']; tot[tag][st] += r['v']; tot[tag]['n'] += 1
OUT['totals'] = tot

# every row that moves AFTER -> NOCAP (this is the P10 check: it must be rucks and only rucks)
movers_nocap = []
for (st, k), r in B['AFTER'].items():
    o = B['NOCAP'].get((st, k))
    if o is None:
        movers_nocap.append({'key': k, 'set': st, 'name': r.get('name'), 'MISSING_IN_NOCAP': True}); continue
    if o['v'] != r['v']:
        movers_nocap.append({'key': k, 'set': st, 'name': r.get('name'), 'pos': _pos(r),
                             'ep': r.get('ep'), 'after': r['v'], 'nocap': o['v'], 'd': o['v'] - r['v'],
                             'binds_fix': bool(capF.get(k, {}).get('binds')),
                             'pool': capF.get(k, {}).get('pool'), 'channel': channel(k)})
missing_in_after = [k for k in B['NOCAP'] if k not in B['AFTER']]
OUT['nocap_movers'] = movers_nocap
# AUTHORITATIVE non-ruck test: `capF` is the engine's OWN real-RUCK population from engine_probe.py
# (`_isreal(p) and MA.gfut(p)=='RUCK'`, n=71). A mover whose key is not in it is a row the ruck cap has
# no business touching. The board's `fut` label is only printed, never trusted, for this check.
OUT['nocap_movers_nonruck'] = [m for m in movers_nocap if m['key'] not in capF]
OUT['population_mismatch'] = {'missing_in_nocap': [m for m in movers_nocap if m.get('MISSING_IN_NOCAP')],
                              'missing_in_after': missing_in_after}

movers_fix = [k for (st, k), r in B['AFTER'].items() if B['BEFORE'].get((st, k), {}).get('v') != r['v']]
OUT['fix_movers_n'] = len(movers_fix)

P("=" * 132)
P("ORDER 20C — THE RUCK-CAP TABLE.  Three BUILT boards, board values read out, never re-derived.")
P("=" * 132)
P("  BEFORE  (HEAD engine, shipped defaults, the live board)      md5 %s   %s" % (MD5['BEFORE'], 'PIN OK'))
P("  AFTER   (ORDER 20 par separation fix)                        md5 %s   %s" % (MD5['AFTER'], 'PIN OK'))
P("  NO-CAP  (the fix, RL_RUC_PRIOR_CAP=99 via the env dial)      md5 %s" % MD5['NOCAP'])
P("")
P("  BOARD TOTALS (sum of `v` over all %d rows the board carries; active + back)" % tot['BEFORE']['n'])
P("    %-8s %12s %12s %12s   %s" % ('config', 'ALL', 'active', 'back', 'vs BEFORE'))
for tag in ('BEFORE', 'AFTER', 'NOCAP'):
    d = tot[tag]['all'] - tot['BEFORE']['all']
    P("    %-8s %12d %12d %12d   %+8d  (%+.4f%%)"
      % (tag, tot[tag]['all'], tot[tag]['active'], tot[tag]['back'], d,
         100.0 * d / tot['BEFORE']['all']))
P("    AFTER -> NO-CAP delta: %+d  (%+.4f%%)"
  % (tot['NOCAP']['all'] - tot['AFTER']['all'],
     100.0 * (tot['NOCAP']['all'] - tot['AFTER']['all']) / tot['AFTER']['all']))
P("")
P("  ROWS THAT MOVE WHEN THE CAP IS LIFTED (AFTER -> NO-CAP): %d of %d" % (len(movers_nocap), tot['AFTER']['n']))
P("    of which NON-RUCK (key absent from the engine's own n=%d real-RUCK set): %d   %s"
  % (len(capF), len(OUT['nocap_movers_nonruck']),
     '(P10 HOLDS — the cap has NO channel outside the ruck rows)'
     if not OUT['nocap_movers_nonruck'] else '*** P10 BREACHED ***'))
for m in OUT['nocap_movers_nonruck'][:40]:
    P("      NON-RUCK MOVER  %-26s %-5s ep=%-4s  %6s -> %6s  (%+d)"
      % (m.get('name'), m.get('pos'), m.get('ep'), m.get('after'), m.get('nocap'), m.get('d')))
P("    EVERY mover, in full, WITH THE CHANNEL THAT MOVED IT:")
P("      %-26s %-5s %5s %6s %8s %8s %8s  %s" % ('player', 'arm', 'epk', 'binds', 'AFTER', 'NO-CAP', 'delta', 'channel'))
for m in sorted(movers_nocap, key=lambda z: -abs(z.get('d', 0))):
    P("      %-26s %-5s %5s %6s %8s %8s %+8d  %s"
      % (m.get('name'), 'POOL' if m.get('pool') else 'NAT', m.get('ep'), m.get('binds_fix'),
         m.get('after'), m.get('nocap'), m.get('d'), m.get('channel')))
_scrap = [m for m in movers_nocap if m.get('channel') == 'DELISTED-SCRAP']
P("    of the %d movers, %d are DELISTED remnants (price == round(0.02 x v0_start), :2230) worth %+d"
  % (len(movers_nocap), len(_scrap), sum(m['d'] for m in _scrap)))
P("    the other %d are live rows worth %+d"
  % (len(movers_nocap) - len(_scrap),
     sum(m['d'] for m in movers_nocap if m.get('channel') != 'DELISTED-SCRAP')))
OUT['nocap_movers_delisted'] = _scrap
P("")


def rows_for(pool):
    out = []
    for key, cf in capF.items():
        if cf.get('pool') != pool or not cf.get('binds'):
            continue
        ch = capH.get(key, {})
        bb, ba, bn = val('BEFORE', key), val('AFTER', key), val('NOCAP', key)
        eF, eH = xF.get(key, {}), xH.get(key, {})
        rec = {'key': key, 'name': cf.get('name'), 'ep': cf.get('ep'),
               'age': (bb or {}).get('age'), 'cg': (bb or {}).get('cg'), 'ty': (bb or {}).get('ty'),
               'club': (bb or {}).get('club'),
               'v_before': (bb or {}).get('v'), 'v_after': (ba or {}).get('v'), 'v_nocap': (bn or {}).get('v'),
               'u_head': ch.get('v0_uncapped'), 'u_fix': cf.get('v0_uncapped'),
               'ceil_head': ch.get('ceiling'), 'ceil_fix': cf.get('ceiling'),
               'binds_head': bool(ch.get('binds')), 'cut_fix': cf.get('cut'),
               'bestlvl26': eF.get('bestlvl26'), 'nqual26': eF.get('nqual26'),
               'in_v0curve': eF.get('in_v0curve'),
               'ruc_ceiling26_fix': eF.get('ruc_ceiling26'),
               'v0_start_fix': eF.get('v0_start'), 'v0_start_head': eH.get('v0_start')}
        rec['d_fix'] = rec['v_after'] - rec['v_before']
        rec['d_nocap'] = rec['v_nocap'] - rec['v_after']
        rec['class'] = 'PRIOR-DOMINATED' if rec['d_nocap'] != 0 else 'PRODUCTION-LED'
        rec['channel'] = channel(key)
        out.append(rec)
    out.sort(key=lambda r: (r['ep'] if r['ep'] is not None else 999, r['name']))
    return out


def emit(title, recs, arm):
    P("=" * 132)
    P("%s — %d rucks, `_ruc_prior_cap` BINDING under the FIX engine" % (title, len(recs)))
    P("=" * 132)
    P("  %-24s %4s %5s %5s | %7s %7s %7s | %7s %7s | %10s %10s %8s | %s"
      % ('player', 'epk', 'age', 'games', 'BEFORE', 'AFTER', 'NO-CAP', 'd_fix', 'd_cap',
         'v0u HEAD', 'v0u FIX', 'ceiling', 'classification'))
    P("  " + "-" * 128)
    for r in recs:
        P("  %-24s %4s %5.1f %5s | %7s %7s %7s | %+7d %+7d | %10.1f %10.1f %8.1f | %-15s %-24s %s"
          % (r['name'], r['ep'], r['age'] if r['age'] is not None else -1, r['cg'],
             r['v_before'], r['v_after'], r['v_nocap'], r['d_fix'], r['d_nocap'],
             r['u_head'], r['u_fix'], r['ceil_fix'], r['class'],
             ('NEWLY BINDING' if not r['binds_head'] else 'already binding on HEAD'), r['channel']))
    P("  " + "-" * 128)
    sb = sum(r['v_before'] for r in recs); sa = sum(r['v_after'] for r in recs); sn = sum(r['v_nocap'] for r in recs)
    P("  %-24s %4s %5s %5s | %7d %7d %7d | %+7d %+7d |" % ('TOTAL (%d)' % len(recs), '', '', '', sb, sa, sn, sa - sb, sn - sa))
    nprior = sum(1 for r in recs if r['class'] == 'PRIOR-DOMINATED')
    P("  classification: PRIOR-DOMINATED %d   PRODUCTION-LED %d" % (nprior, len(recs) - nprior))
    P("  newly binding under the fix: %d   already binding on HEAD: %d"
      % (sum(1 for r in recs if not r['binds_head']), sum(1 for r in recs if r['binds_head'])))
    P("  ceiling moved HEAD->FIX on %d of %d rows"
      % (sum(1 for r in recs if abs((r['ceil_fix'] or 0) - (r['ceil_head'] or 0)) > 1e-9), len(recs)))
    P("")
    P("  MECHANISM (reported, NOT used to classify):")
    P("  %-24s %10s %7s %8s %11s %11s %10s" % ('player', 'bestlvl26', 'nqual', 'in_curve',
                                               'v0start HEAD', 'v0start FIX', 'ev ceil'))
    for r in recs:
        P("  %-24s %10.2f %7s %8s %11.1f %11.1f %10.1f"
          % (r['name'], r['bestlvl26'] if r['bestlvl26'] is not None else -1, r['nqual26'],
             r['in_v0curve'], r['v0_start_head'], r['v0_start_fix'], r['ruc_ceiling26_fix']))
    P("")
    OUT[arm] = recs


nat = rows_for(False)
pool = rows_for(True)
emit("NATIONAL", nat, 'national')
emit("POOL", pool, 'pool')

# ---------------------------------------------------------------- cross-checks
P("=" * 132)
P("CROSS-CHECKS")
P("=" * 132)
for arm, recs, allrows in (('NATIONAL', nat, [r for r in capF.values() if not r.get('pool')]),
                           ('POOL', pool, [r for r in capF.values() if r.get('pool')])):
    hb = sum(1 for r in (capH.values()) if r.get('pool') == (arm == 'POOL') and r.get('binds'))
    P("  %-9s ruck rows %2d | binds HEAD %2d -> binds FIX %2d | total cut FIX %10.1f"
      % (arm, len(allrows), hb, len(recs), sum(r['cut_fix'] for r in recs)))
nonbind_move = []
for key, cf in capF.items():
    if cf.get('binds'):
        continue
    ba, bn = val('AFTER', key), val('NOCAP', key)
    if ba and bn and ba['v'] != bn['v']:
        nonbind_move.append({'name': cf.get('name'), 'pool': cf.get('pool'), 'after': ba['v'], 'nocap': bn['v']})
OUT['nonbinding_ruck_movers'] = nonbind_move
P("  rucks NOT binding under FIX that still move on cap lift: %d %s"
  % (len(nonbind_move), '' if not nonbind_move else str(nonbind_move)))
P("")

txt = "\n".join(L)
open(PRE + '.txt', 'w').write(txt + "\n")
json.dump(OUT, open(PRE + '.json', 'w'), indent=1)
print(txt)
