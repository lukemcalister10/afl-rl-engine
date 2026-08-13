#!/usr/bin/env python3
"""ORDER 29B -- STEP 2: SIGN THE TWO BORROWED POOL v0 CELLS (owner ruling, OPTION A).

OWNER RULING (#334 comment 5280881134), OPTION A: the two n=0 cells PDN|KPF and PDS|KPF take the
K-SHRINK LIMITING CASE -- 100% borrow -- i.e. the pathway level x the pool-wide KPF positional
relativity.

THE VALUE IS DERIVED, NEVER TYPED. o28_derive.py:250-256 is the cell derivation, verbatim:

    path[m]['shrunk'] = w_m*raw_m + (1-w_m)*pool_aggregate ,  w_m = n_m/(n_m+K)
    lens[g]           = mean(value | position g) / mean(value)        <- the pool-wide relativity
    cells[(m,g)]      = w*own + (1-w)*path[m]['shrunk']*lens[g] ,      w = n_mg/(n_mg+K)

At n_mg = 0 the weight w is 0 and the expression COLLAPSES to  path[m]['shrunk'] * lens[g]. The
K-shrink limiting case IS the owner's Option A -- the ruling names the arithmetic the derivation
already runs, so nothing new is invented here and nothing is back-filled by hand. This script
re-derives lens[KPF] and path['PDN'|'PDS']['shrunk'] from the SAME inputs o28_derive.py read
(LAYER2::fit_pool_keys x Layer-1 position_group x the scoring totals), reproduces DERIVE28's own
cell values bit-for-bit as its control, and only then writes.

EACH CELL IS FLAGGED AS BORROWED ON THE CELL -- `cell_signature` carries 'borrowed' or 'fitted' for
every one of the 54 cells, and `borrowed_cells` carries the full per-cell disclosure (the ruling, the
basis, n=0, the pathway level, the relativity, the arithmetic). A disclosed field, never a silent number.

  usage: python3 o29b_sign_cells.py <in_artifact.json> <out_artifact.json>
"""
import os, sys, json, math, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
D28 = ROOT + '/docs/evidence/grace_adoption_2026-08-13/DERIVE28.json'
INP = ROOT + '/docs/evidence/grace_adoption_2026-08-13/inputs'
IN, OUT = sys.argv[1], sys.argv[2]

LOG = []
def P(s=''):
    print(s); LOG.append(s)

POSN = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
K = 15
BORROW = ['PDN|KPF', 'PDS|KPF']

art = json.loads(open(IN).read(), object_pairs_hook=collections.OrderedDict)
CAND = json.load(open(D28))['candidate']
AF = float(CAND['anchor_factor'])

P("=" * 112)
P("ORDER 29B  --  STEP 2: THE TWO BORROWED POOL v0 CELLS, SIGNED UNDER OWNER OPTION A")
P("=" * 112)
P()
P("  in  artifact  %s  (pool_v0 unsigned_cells %s)"
  % (hashlib.md5(open(IN, 'rb').read()).hexdigest()[:8], art['pool_v0']['unsigned_cells']))
P("  anchor_factor %.16f   (== the numeraire s; the cells are ANCHORED board points)" % AF)

# ---- RE-DERIVE lens[] and path[]['shrunk'] FROM THE SAME INPUTS o28_derive.py READ ------------------
# EXACTLY the inputs o28_derive.py reads (o28_derive.py:51-55, 237, 311): the grace-A scored career
# values, the attribution, and the Layer-1 day-0 position groups. Nothing is re-scored here.
L2 = json.load(open(INP + '/LAYER2.json'))
L1 = json.load(open(INP + '/layer1_player_seasons.json'))
SC = L2['grace_a']
ATTR = L2['attribution']
E = {x['key']: x for x in L1['entries']}

pool = [dict(key=k, mech=ATTR[k]['mechanism'], pos=E[k]['position_group'], value=SC[k]['total'])
        for k in L2['fit_pool_keys']]
ap = sum(r['value'] for r in pool) / len(pool)
lens = {}
for g in POSN:
    sub = [r for r in pool if r['pos'] == g]
    lens[g] = (sum(r['value'] for r in sub) / len(sub) / ap) if sub and ap else 1.0
path = {}
for m in POOLM:
    sub = [r for r in pool if r['mech'] == m]
    n = len(sub); a = (sum(r['value'] for r in sub) / n) if n else 0.0
    w = n / float(n + K)
    path[m] = dict(n=n, raw=a, shrunk=w * a + (1 - w) * ap)

P()
P("  RE-DERIVED FROM THE FIT POPULATION (%d pool rows, pool aggregate %.10f):" % (len(pool), ap))
P("    %-6s %6s %14s %14s %14s" % ('pos', 'n', 'mean', 'lens[g]', ''))
for g in POSN:
    _s = [r for r in pool if r['pos'] == g]
    P("    %-6s %6d %14.6f %14.16f" % (g, len(_s), sum(r['value'] for r in _s) / len(_s), lens[g]))

# ---- CONTROL: the re-derivation must reproduce DERIVE28's OWN cells bit-for-bit, all 54 -------------
_worst = 0.0; _worstk = None
for m in POOLM:
    for g in POSN:
        sub = [r for r in pool if r['mech'] == m and r['pos'] == g]
        n = len(sub); w = n / float(n + K)
        own = (sum(r['value'] for r in sub) / n) if n else 0.0
        mine = w * own + (1 - w) * path[m]['shrunk'] * lens[g]
        theirs = CAND['cells']['%s|%s' % (m, g)]
        d = abs(mine - theirs)
        if d > _worst: _worst, _worstk = d, '%s|%s' % (m, g)
P()
P("  CONTROL -- the re-derivation reproduces DERIVE28's OWN 54 cells: max |mine - theirs| = %.3e at %s"
  % (_worst, _worstk))
assert _worst < 1e-9, 'ORDER 29B HALT: the cell re-derivation does not reproduce DERIVE28; do not write.'

# ---- THE LIMITING CASE, STATED AS ARITHMETIC BEFORE IT IS A NUMBER ---------------------------------
P()
P("  OPTION A -- THE K-SHRINK LIMITING CASE. n = 0  =>  w = n/(n+K) = 0  =>  the derivation's own")
P("  expression  w*own + (1-w)*path*lens  COLLAPSES to  path[m]['shrunk'] * lens['KPF'].  100% borrow.")
P()
P("  %-10s %6s %16s %20s %18s %14s" % ('cell', 'n', 'pathway shrunk', 'x lens[KPF]', 'x anchor_factor', 'prints'))
signed = {}
disclosure = collections.OrderedDict()
for key in BORROW:
    m, g = key.split('|')
    n_mg = len([r for r in pool if r['mech'] == m and r['pos'] == g])
    assert n_mg == 0, 'ORDER 29B HALT: %s has n=%d, it is not an empty cell' % (key, n_mg)
    raw = path[m]['shrunk'] * lens[g]
    anch = raw * AF
    signed[key] = anch
    P("  %-10s %6d %16.10f %20.10f %18.14f %14d" % (key, n_mg, path[m]['shrunk'], raw, anch, int(round(anch))))
    disclosure[key] = collections.OrderedDict([
        ('value_anchored', anch),
        ('borrowed', True),
        ('fit_n', 0),
        ('ruling', 'OWNER OPTION A, #334 comment 5280881134 — an empty cell takes the K-shrink LIMITING '
                   'CASE (100% borrow): the pathway level x the pool-wide positional relativity. It is not '
                   'a measurement of this cell and is not presented as one.'),
        ('basis', "o28_derive.py:250-256 verbatim. cells[(m,g)] = w*own + (1-w)*path[m]['shrunk']*lens[g] "
                  "with w = n/(n+K), K=15. At n=0, w=0, so the expression IS pathway_level x lens[g]. The "
                  "ruling names the arithmetic the derivation already runs; nothing is back-filled by hand."),
        ('pathway', m),
        ('position', g),
        ('pathway_level_shrunk_preanchor', path[m]['shrunk']),
        ('pathway_level_anchored', path[m]['shrunk'] * AF),
        ('pool_wide_positional_relativity', lens[g]),
        ('anchor_factor', AF),
        ('arithmetic', '%.10f * %.16f * %.16f = %.14f' % (path[m]['shrunk'], lens[g], AF, anch)),
        ('supersedes_declined_unsigned', art['pool_v0']['declined_unsigned'].get(key)),
        ('signed_by', 'ORDER 29B, the entry wiring — signed BECAUSE pool_v0 is now CONSUMED by the day-0 '
                      'print. Under ORDER 29 no pricing leg read pool_v0, so declining a number cost nothing; '
                      'once the cell is a price, an entrant standing in it must have an answer or the build '
                      'must halt. The owner ruled the answer rather than the halt.'),
    ])

# ---- THE PROOF THAT THIS IS THE SAME NUMBER ORDER 29 DECLINED, NOT A NEW ONE -----------------------
P()
P("  P29B-13 -- these must reproduce ORDER 29's published `declined_unsigned` EXACTLY at its own 1dp:")
_dec_bad = []
for key in BORROW:
    dec = float(art['pool_v0']['declined_unsigned'][key])
    ok = abs(round(signed[key], 1) - dec) < 1e-12
    if not ok: _dec_bad.append(key)
    P("     %-10s declined_unsigned %6.1f   signed %20.14f   round1 %6.1f   %s"
      % (key, dec, signed[key], round(signed[key], 1), 'HELD' if ok else '*** BREACH ***'))
assert not _dec_bad, 'P29B-13 BREACH: %s — the Option-A borrow is NOT the declined number' % _dec_bad

# ---- WRITE ----------------------------------------------------------------------------------------
pv = art['pool_v0']
cells = pv['cells']
for key in BORROW:
    assert cells[key] is None, 'ORDER 29B HALT: %s is not null on entry — refusing to overwrite a value' % key
    cells[key] = signed[key]
assert not [k for k, v in cells.items() if v is None], 'ORDER 29B HALT: a cell is still null after signing'

pv['unsigned_cells'] = []
pv['cell_signature'] = collections.OrderedDict(
    ('%s|%s' % (m, g), ('borrowed' if '%s|%s' % (m, g) in BORROW else 'fitted'))
    for m in POOLM for g in POSN)
pv['borrowed_cells'] = disclosure
pv['_doc'] = (
    'PREREG P8/P9 / ORDER 29 STEP 5, AMENDED BY ORDER 29B STEP 2 (owner OPTION A, #334 comment '
    '5280881134). The POOL day-0 object: per pathway x day-0 position cells on the MSD Way A basis, '
    'K-shrunk toward the pathway level (K=15), anchored into board points by the ladder anchor factor. '
    'THIS OBJECT IS NOW CONSUMED: ORDER 29B wires the printed day-0 price of a pool entrant to his own '
    'cell, so every cell an active entrant maps to must carry a signed value. THE TWO n=0 CELLS '
    '(PDN|KPF, PDS|KPF) ARE SIGNED BY OWNER RULING AS BORROWED -- the K-shrink limiting case, 100% '
    'borrow: pathway level x pool-wide KPF positional relativity. They are FLAGGED AS BORROWED ON THE '
    'CELL (`cell_signature`) with full per-cell disclosure in `borrowed_cells`; they are not '
    'measurements of those cells and are not presented as such. The values reproduce ORDER 29\'s '
    '`declined_unsigned` exactly, which is the proof that the ruling signed the arithmetic the '
    'derivation had already run and declined, rather than back-filling a new number. THE UNSIGNED-CELL '
    'HALT IS RETIRED for cells signed this way and REPLACED by a coverage assert (rl_model.py): every '
    'pathway x position cell an ACTIVE entrant maps to must carry a signed value, borrowed or fitted. '
    'pool_v0_of() remains the ONE accessor and still raises on a null, so a future unsigned cell is '
    'still fail-closed. The #326 signed `pool_levels` block above is UNTOUCHED and still carries the '
    'year-1+ entry anchors (the floor, the thin-record blend and the ruck cap basis).')
pv['consumed_by'] = ('ORDER 29B — the printed day-0 price of a pool entrant IS cells[pathway|position] '
                     '(board currency; the numeraire s is already inside via anchor_factor).')

open(OUT, 'w').write(json.dumps(art, indent=1) + '\n')
P()
P("  WROTE %s   md5 %s" % (os.path.basename(OUT), hashlib.md5(open(OUT, 'rb').read()).hexdigest()))
P("     curve_md5 %s  (UNCHANGED — the curve payload is not touched by this act)" % art['curve_md5'])
P("     unsigned_cells now %s ; borrowed %s" % (pv['unsigned_cells'], list(disclosure)))

open(HERE + '/SIGN29B_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'borrowed': {k: signed[k] for k in BORROW},
           'lens_KPF': lens['KPF'],
           'pathway_shrunk': {m: path[m]['shrunk'] for m in ('PDN', 'PDS')},
           'pathway_anchored': {m: path[m]['shrunk'] * AF for m in ('PDN', 'PDS')},
           'anchor_factor': AF, 'K': K,
           'rederivation_max_abs_err_vs_DERIVE28': _worst,
           'artifact_md5': hashlib.md5(open(OUT, 'rb').read()).hexdigest()},
          open(HERE + '/SIGN29B.json', 'w'), indent=1)
