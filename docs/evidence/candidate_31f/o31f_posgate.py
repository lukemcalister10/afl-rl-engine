#!/usr/bin/env python3
"""ORDER 31-F  --  F3: THE POSITION GATE (original Step 4, the Baker class).  READ-ONLY AUDIT.

Positions are price-critical twice over: `gfut(p)` picks the row's REPLACEMENT BAR and it picks the
POSITIONAL v0 CELL.  A row keyed to the wrong position is priced against the wrong bar AND the wrong v0.

WHAT IS AUDITED, on every active priced row:
  A  gfut(p) resolves and is one of the six groups the v0 surface publishes (a HALT class if not)
  B  the future position and the present position agree, or the disagreement is a declared flex row
  C  the `eligibilities` column collapses (R105.1: K-X absorbs G-X) to a set that CONTAINS gfut(p)
  D  THE BAKER CLASS -- the three rows the owner ruled to 'G-DEF,G-FWD' in item 217, verbatim
     ("Yes, G-DEF. Lock it in.", 2026-07-16): sam-flanders, oskar-baker, ed-langdon.  The store write
     was QUEUED TO LEG C AND NEVER EXECUTED.  This gate reports their CURRENT store state against the
     ruling and states precisely what is reachable from a pricing seat.

WHAT THIS GATE DOES NOT DO, AND WHY.  It does NOT write the store.  Issue #334's own line is binding:
"Store writes are an execution act with the owner's word, never a seam act."  The owner's word exists
for the Baker class, but the write belongs to the store writer, not to a pricing candidate; and a
lane-local re-key would put the board and the store into disagreement, which is the exact defect class
this project keeps closing.  So the gate MEASURES the price at stake for every reachable row and names
every residual, and the packet carries the number.
"""
import os, sys, json, io, contextlib, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f'

os.environ.update(RL_O31='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
BOARD = json.load(open(os.path.join(SP, 'bb_f2on', 'rl_after', 'rl_app_data.json')))
ROWS = {r['key']: r for r in BOARD['active']}
BARS = NSE['_O30BP_BARS']
pv_pedigree = NSE['pv_pedigree']; F = float(NSE['_PL_F'])

OUT = []
def P(s=''):
    OUT.append(s); print(s)

POS6 = sorted(BARS)
P('ORDER 31-F  F3 -- THE POSITION GATE (original Step 4).  READ-ONLY AUDIT.')
P('  board audited: %s   %d active rows' % (
    hashlib.md5(open(os.path.join(SP, 'bb_f2on', 'rl_after', 'rl_app_data.json'), 'rb').read()).hexdigest(),
    len(ROWS)))
P('  the six position groups the v0 surface publishes: %s' % ' '.join(POS6))
P('  the bars they key: %s' % '  '.join('%s %.1f' % (g, BARS[g]) for g in POS6))
P('')

AUD = []
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in ROWS:
        continue
    g = MA.gfut(p)
    pres = MA._pos_present(p)
    elig_raw = p.get('eligibilities')
    elig = sorted(MA._collapse_elig(elig_raw))
    AUD.append(dict(key=k, name=p.get('player'), pathway=p.get('type'), pick=p.get('pick'),
                    pool=bool(p.get('_pool')), gfut=g, present=pres,
                    futpos=p.get('_futpos'), altpos=p.get('_altpos'), pdual=p.get('_pdual') or 0.0,
                    elig_raw=elig_raw, elig=elig, price=ROWS[k]['v'],
                    v0=float(pv_pedigree(p)) / F, bar=BARS.get(g)))

P('CHECK A -- gfut resolves to one of the six published groups')
badA = [r for r in AUD if r['gfut'] not in POS6]
P('  rows audited %d   UNRESOLVED %d   %s' % (len(AUD), len(badA), 'PASS' if not badA else 'FAIL'))
for r in badA[:10]:
    P('    %-24s gfut %r present %r elig %r' % (r['key'], r['gfut'], r['present'], r['elig_raw']))
P('')

P('CHECK B -- future vs present position')
diff = [r for r in AUD if r['present'] and r['gfut'] != r['present']]
P('  rows where gfut != present: %d of %d (%.1f%%)' % (len(diff), len(AUD), 100.0 * len(diff) / len(AUD)))
P('  THIS IS NOT A DEFECT BY ITSELF: present != future is the taxonomy working as designed (item 216).')
P('  It is a defect only where the FUTURE key is unsupported by the eligibility column -- CHECK C.')
byd = collections.Counter('%s->%s' % (r['present'], r['gfut']) for r in diff)
for kk, vv in byd.most_common(12):
    P('    %-14s %4d' % (kk, vv))
P('')

P('CHECK C -- gfut is CONTAINED in the collapsed eligibility set (the owner-maintained declaration)')
noelig = [r for r in AUD if not r['elig']]
mismatch = [r for r in AUD if r['elig'] and r['gfut'] not in r['elig']]
P('  rows with an EMPTY eligibility column .......... %d   (bar falls back to present position, by law)'
  % len(noelig))
P('  rows where gfut is NOT in the collapsed set .... %d   <-- THE RESIDUAL CLASS' % len(mismatch))
P('')
if mismatch:
    P('  THE RESIDUALS, NAMED IN FULL (never summarised away). Each is a row whose FUTURE position key')
    P('  is outside its own CURRENT eligibility declaration. That is legitimate for a genuine positional')
    P('  move (a mid becoming a key defender) and is a DEFECT where the column is simply stale. This seat')
    P('  cannot tell those apart from the store alone, so it names every one and prices it.')
    P('    %-26s %-6s %-6s %-16s %8s %9s %7s' % ('key', 'gfut', 'pres', 'eligibilities', 'price', 'v0', 'bar'))
    for r in sorted(mismatch, key=lambda x: -x['price']):
        P('    %-26s %-6s %-6s %-16s %8d %9.1f %7.1f'
          % (r['key'], r['gfut'], r['present'] or '-', (r['elig_raw'] or '')[:16], r['price'], r['v0'],
             r['bar'] or 0))
    P('    TOTAL PRICE STANDING ON A RESIDUAL POSITION KEY: %d board points (%.2f%% of the book)'
      % (sum(r['price'] for r in mismatch),
         100.0 * sum(r['price'] for r in mismatch) / sum(r['price'] for r in AUD)))
P('')

P('CHECK D -- THE BAKER CLASS (owner item 217, verbatim "Yes, G-DEF. Lock it in.", 2026-07-16)')
P('  The ruling: sam-flanders / oskar-baker / ed-langdon carry eligibilities \'G-DEF,G-FWD\' -- NOT MID')
P('  ("a player should NOT have three positions"), plus sam-flanders present_position MID -> GDEF.')
P('  The store write was QUEUED TO LEG C and, on this branch, HAS NOT BEEN EXECUTED. Current state:')
BAKER = ['sam-flanders', 'oskar-baker', 'ed-langdon']
BK = []
for k in BAKER:
    r = next((x for x in AUD if x['key'] == k), None)
    if r is None:
        p = next((x for x in MA.data if (x.get('key') or MA.slug(x['player'])) == k), None)
        P('    %-16s NOT ON THE ACTIVE BOARD%s' % (k, '' if p is None else ' (in store, not priced)'))
        BK.append(dict(key=k, on_board=False))
        continue
    ruled_ok = set(r['elig']) == {'SD', 'SF'}
    BK.append(dict(key=k, on_board=True, gfut=r['gfut'], present=r['present'], elig_raw=r['elig_raw'],
                   elig=r['elig'], price=r['price'], v0=r['v0'], bar=r['bar'],
                   matches_ruling=ruled_ok))
    P('    %-16s gfut %-5s present %-5s eligibilities %-18s price %6d  v0 %8.1f  bar %.1f   ruling %s'
      % (k, r['gfut'], r['present'] or '-', repr(r['elig_raw']), r['price'], r['v0'], r['bar'] or 0,
         'ALREADY SATISFIED' if ruled_ok else 'NOT YET APPLIED IN THE STORE'))
P('')
P('  WHAT IS REACHABLE FROM THIS SEAT, STATED PRECISELY:')
P('    * The ruling is an ELIGIBILITY-COLUMN correction. In this engine the eligibility column drives the')
P('      YEAR-0 DPP bar (rl_model.py::_collapse_elig / _fit_bar), NOT gfut. gfut comes from')
P('      future_position, which the owner explicitly left untouched for these rows ("future stays per the')
P('      owner\'s flex register").')
P('    * So the v0 CELL of every Baker-class row is UNAFFECTED by the ruling, and the price at stake is')
P('      the year-0 bar only.')
P('    * The store write itself is an EXECUTION ACT and is NOT this candidate\'s to make (#334: "Store')
P('      writes are an execution act with the owner\'s word, never a seam act"). It is REPORTED, PRICED')
P('      AND LEFT FOR THE STORE WRITER. Nothing about it is applied silently.')
P('')

REKEYED = 0
P('THE GATE\'S VERDICT')
P('  rows audited ................................. %d' % len(AUD))
P('  rows with an UNRESOLVED position key ......... %d' % len(badA))
P('  rows re-keyed by this act .................... %d  (a store write is not a pricing act)' % REKEYED)
P('  rows flagged as RESIDUAL (gfut outside elig) . %d' % len(mismatch))
P('  Baker-class rows on the board ................ %d of 3' % sum(1 for b in BK if b.get('on_board')))
P('  Baker-class rows already satisfying the ruling %d' % sum(1 for b in BK if b.get('matches_ruling')))
P('')

json.dump(dict(order='ORDER 31-F F3 -- the position gate',
               board=hashlib.md5(open(os.path.join(SP, 'bb_f2on', 'rl_after', 'rl_app_data.json'), 'rb').read()).hexdigest(),
               n_audited=len(AUD), positions=POS6, bars={g: BARS[g] for g in POS6},
               unresolved=badA, n_future_ne_present=len(diff),
               future_ne_present_map=dict(byd), n_empty_eligibility=len(noelig),
               residuals=sorted(mismatch, key=lambda x: -x['price']),
               residual_price=sum(r['price'] for r in mismatch),
               residual_price_share=(sum(r['price'] for r in mismatch) / sum(r['price'] for r in AUD)),
               baker_class=BK, n_rekeyed=REKEYED,
               rekey_policy='NOT APPLIED -- an eligibility-column correction is a STORE WRITE and a store '
                            'write is an execution act with the owner\'s word, never a seam act (#334). '
                            'Reported and priced instead.',
               rows=AUD),
          open(os.path.join(HERE, 'POSGATE_31F.json'), 'w'), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, 'POSGATE_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: POSGATE_31F.json / POSGATE_31F_out.txt')
