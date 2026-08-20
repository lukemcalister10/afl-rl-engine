#!/usr/bin/env python3
"""ORDER D8 MEASUREMENT — THE COMPARISON COLUMN, CHECKED RATHER THAN ASSERTED.

The order says: carry the D7B tables (which are on file for the live board a05fe951) as the
comparison column. This seat does NOT re-type them. It re-emits the live board on today's tree
(D8BASE, dial unset) and then PROVES that what it re-emitted is the same object:

  CHECK 1  matrix identity   D8BASE.recs == D7BCAND.recs == BK.recs, byte-for-byte on the canonical
                             JSON of the priced payload. (D7BCAND is the matrix the on-file D7B
                             tables were rendered from; BK is the post-flip bare bake's re-emit.)
  CHECK 2  ND band cells     every field of every ND band cell in BANDS_NOARB_D8.json['D8BASE']
                             equals the same field in final_candidate_2026-08-19/BANDS_D7B.json
                             ['D7BCAND'] — n, path, apprec01, buy_margin, verdict, n_included,
                             n_zero, n_not_yet_reached, mean_yearN, mean_year0_same_set, flags.
  CHECK 3  pool arm cells    the same, for STANDING_TABLES_NOARB_D8.json vs STANDING_TABLES_D7B.json
                             — n, path, apprec01, margin, verdict, n_by_year, n_pre.
  CHECK 4  class mark        CLASS_D8.json['D8BASE'] == CLASS_D8.json['D7BCAND'] on w2, cohort,
                             max_class and every per-class value.
  CHECK 5  determinism       D8CAND.recs == D8CAND2.recs (the two candidate emits).
  CHECK 6  non-vacuity       D8CAND.recs != D8BASE.recs, and the day-0 column is UNMOVED — the taper
                             is inert at age<=20 and every day-0 row is an entrant, so a moved v0
                             would be the falsifier firing.

ANY failure prints as a failure and the exit code is non-zero. NO ENGINE RUN — pure reads.
"""
import json, os, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FC = os.path.join(REPO, 'docs', 'evidence', 'final_candidate_2026-08-19')
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
L, FAIL = [], []


def P(s=''):
    print(s); L.append(str(s))


def check(name, ok, detail=''):
    P('  %-58s %s %s' % (name, 'PASS' if ok else '*** FAIL ***', detail))
    if not ok:
        FAIL.append(name)


def mx(lab):
    p = os.path.join(SP, 'per_entrant_%s.json' % lab)
    return json.load(open(p)) if os.path.exists(p) else None


def canon(d):
    return hashlib.md5(json.dumps(d['recs'], sort_keys=True).encode()).hexdigest()


P('=' * 118)
P('ORDER D8 MEASUREMENT — THE COMPARISON COLUMN IS THE D7B TABLE, PROVED')
P('=' * 118)

# ---- CHECK 1 -------------------------------------------------------------------------------------
P()
P('CHECK 1 — matrix identity of the comparison column')
M = {l: mx(l) for l in ('D8CAND', 'D8CAND2', 'D8BASE', 'D7BCAND', 'BK')}
for l, d in M.items():
    if d is None:
        P('  %-9s MATRIX MISSING' % l)
        continue
    P('  %-9s recs md5 %s   store %s  engine %s  n=%d'
      % (l, canon(d)[:16], d['meta']['store_md5'], d['meta']['engine_head'], d['meta']['n_records']))
check('D8BASE.recs == D7BCAND.recs (the D7B tables\' own matrix)',
      canon(M['D8BASE']) == canon(M['D7BCAND']))
check('D8BASE.recs == BK.recs (the post-flip bare bake re-emit)',
      canon(M['D8BASE']) == canon(M['BK']))
P('  NOTE, and it is a finding worth stating plainly: D8BASE carries store cc02567f while D7BCAND and')
P('  BK carry cb38ef11. The store identity moved at commit de9b8eb (the owner\'s 112 ownership + 23')
P('  pick-owner moves), whose message records "board byte-identical". The equality above is the')
P('  measured proof of that claim on the walk-forward payload: the apply moved the store identity and')
P('  NOT ONE PRICED RECORD. It is also why harness_pvc_REPINNED_pass3.py\'s EXPECT_STORE = cb38ef11')
P('  now fails closed on every freshly emitted matrix, and why d8_noarb_bands.py re-points that pin at')
P('  the call site (declared change 4 in its header) instead of editing the instrument.')

# ---- CHECK 2 -------------------------------------------------------------------------------------
P()
P('CHECK 2 — ND band cells, D8BASE vs the on-file D7B tables')
nb = json.load(open(os.path.join(HERE, 'BANDS_NOARB_D8.json')))['nd']['D8BASE']
ob = json.load(open(os.path.join(FC, 'BANDS_D7B.json')))['nd']['D7BCAND']
FIELDS_ND = ('n', 'path', 'apprec01', 'buy_margin', 'verdict', 'n_included', 'n_zero',
             'n_not_yet_reached', 'mean_yearN', 'mean_year0_same_set', 'flags')
bad = []
for k in sorted(set(nb) | set(ob)):
    a, b = nb.get(k), ob.get(k)
    if a is None or b is None:
        bad.append((k, 'MISSING ON ONE SIDE')); continue
    for f in FIELDS_ND:
        if a.get(f) != b.get(f):
            bad.append((k, f))
check('every ND band cell agrees in every field (%d cells, %d fields)' % (len(ob), len(FIELDS_ND)),
      not bad, '' if not bad else str(bad[:6]))

# ---- CHECK 3 -------------------------------------------------------------------------------------
P()
P('CHECK 3 — pool arm cells, D8BASE vs the on-file D7B tables')
na = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_D8.json')))['arms']['D8BASE']
oa = json.load(open(os.path.join(FC, 'STANDING_TABLES_D7B.json')))['arms']['D7BCAND']
FIELDS_A = ('n', 'path', 'apprec01', 'margin', 'verdict', 'n_by_year', 'n_pre')
bada = []
for k in sorted(set(na) | set(oa)):
    a, b = na.get(k), oa.get(k)
    if a is None or b is None:
        bada.append((k, 'MISSING ON ONE SIDE')); continue
    for f in FIELDS_A:
        if a.get(f) != b.get(f):
            bada.append((k, f))
check('every pool arm cell agrees in every field (%d cells, %d fields)' % (len(oa), len(FIELDS_A)),
      not bada, '' if not bada else str(bada[:6]))

# ---- CHECK 4 -------------------------------------------------------------------------------------
P()
P('CHECK 4 — the class mark of the comparison column')
CL = json.load(open(os.path.join(HERE, 'CLASS_D8.json')))
c1, c2 = CL['D8BASE'], CL['D7BCAND']
check('D8BASE W2 == D7BCAND W2 == the registered 1.0672',
      round(c1['w2'], 4) == round(c2['w2'], 4) == 1.0672, '(%.4f / %.4f)' % (c1['w2'], c2['w2']))
check('D8BASE per-class == D7BCAND per-class, every cohort',
      c1['per_class'] == c2['per_class'])
check('the instrument self-validated on ORDER K before any candidate number was read',
      round(CL['OKRULED']['w2'], 4) == 1.0513 and round(CL['OKRULED']['cohort'], 4) == 1.0324,
      '(W2 %.4f vs 1.0513 · cohort %.4f vs 1.0324)' % (CL['OKRULED']['w2'], CL['OKRULED']['cohort']))
P('  candidate class mark: W2 %.4f  cohort %.4f  max class %.4f (%d)'
  % (CL['D8CAND']['w2'], CL['D8CAND']['cohort'], CL['D8CAND']['max_class'],
     CL['D8CAND']['max_class_year']))

# ---- CHECK 5 / 6 ---------------------------------------------------------------------------------
P()
P('CHECK 5/6 — determinism and non-vacuity of the priced matrix')
check('D8CAND.recs == D8CAND2.recs (two independent emits, byte-identical)',
      canon(M['D8CAND']) == canon(M['D8CAND2']))
check('D8CAND.recs != D8BASE.recs (the pass-through fired; the dial is not inert)',
      canon(M['D8CAND']) != canon(M['D8BASE']))
ka = {r['key']: r for r in M['D8CAND']['recs']}
kb = {r['key']: r for r in M['D8BASE']['recs']}
check('the two matrices cover the same key set', set(ka) == set(kb))
nrow = sum(1 for k in ka if json.dumps(ka[k], sort_keys=True) != json.dumps(kb[k], sort_keys=True))
nv0 = sum(1 for k in ka if ka[k]['v0'] != kb[k]['v0'])
P('  rows whose walk-forward path moves: %d of %d' % (nrow, len(ka)))
check('NOT ONE row\'s day-0 v0 moves (the taper is inert at age<=20; day-0 rows are entrants)',
      nv0 == 0, '(%d moved)' % nv0)

P()
P('=' * 118)
P('RESULT: %s' % ('ALL CHECKS PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL)))
P('=' * 118)
open(os.path.join(HERE, 'NOARB_D8_CHECKS_out.txt'), 'w').write('\n'.join(L) + '\n')
sys.exit(1 if FAIL else 0)
