#!/usr/bin/env python3
"""SYNTHETIC R24 SCORE FILE GENERATOR — REHEARSAL ONLY. NEVER THE OWNER'S DATA.

Produces `scores/R24.csv` in EXACTLY the shape the owner couriers: a two-column CSV,
header `Player,2026 R24`, cp1252-encoded, CRLF line endings, trailing newline, names carried
byte-verbatim off the R23 export (including its trailing U+00A0 artefacts).

DETERMINISTIC: seeded, so the file's md5/sha256 are reproducible and can be pinned in an act spec.

WHAT IS SYNTHETIC ABOUT IT, stated so no reader mistakes it for a real round:
  * the participation set is R23's, minus 12 dropped names, plus 10 active-pool names who did not
    play R23, plus TWO players the pinned owner sheet marks injured=Y (deliberate: the H2 trip);
  * the Bailey pair is written APART ('Bailey Williams' / 'Bailey J. Williams'), the R20/R21 export
    shape, so R24 needs NO round-scoped identity override;
  * scores are R23's own values, re-dealt with a seeded permutation, plus TEN DECLARED RISERS and
    TEN DECLARED FALLERS so the movers direction is falsifiable rather than eyeballed.
"""
import csv, hashlib, json, os, random, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'scores', 'R24.csv')
SEED = 20260824

raw = open(os.path.join(ROOT, 'scores', 'R23.csv'), 'rb').read().decode('cp1252')
rows = [r for r in csv.reader(raw.splitlines())[1:] if r] if False else \
       [r for r in list(csv.reader(raw.splitlines()))[1:] if r]
r23 = [(r[0], int(r[1])) for r in rows]

# ---- the names R24 drops (omitted / rested / late out) ------------------------------------------
DROPPED = ['Bailey Williams WBD',      # the R23 export artefact; R24 writes the pair apart
           'Alex Pearce', 'Harry Armstrong', 'Jordan Croft', 'Louis Emmett', 'Liam Puncher',
           'Steely Green', 'Jordon Sweet', 'Bradley Hill', 'Jackson Macrae', 'Wil Powell\xa0',
           'James Jordon\xa0', 'Samuel Collins\xa0']
# ---- the names R24 adds, all from the ACTIVE pool, none injured=Y on the pinned sheet -----------
ADDED = ['Bailey Williams', 'Zeke Uwland', 'Sam Cumming', 'Xavier Taylor', 'Oskar Taylor',
         'Cameron Nairn', 'Jack Dalton', 'Charlie Banfield', 'Cody Curtin', 'Jack Ison',
         'Will Darcy']
# ---- THE H2 TRIP, deliberate: two players the pinned sheet marks injured=Y turn up in the file --
INJURED_RETURNS = ['Tom Green', 'Connor Rozee']

# ---- the declared risers/fallers: falsifiable movers direction ---------------------------------
RISERS = ['Zeke Uwland', 'Sam Cumming', 'Xavier Taylor', 'Oskar Taylor', 'Cameron Nairn',
          'Jack Dalton', 'Charlie Banfield', 'Cody Curtin', 'Jack Ison', 'Will Darcy']
FALLERS = ['Max Hall', 'Izak Rankine', 'Errol Gulden', 'Lachlan Ash', 'Levi Ashcroft',
           'Max Gawn', 'Kade Chandler', 'Isaac Heeney\xa0', 'Chad Warner\xa0', 'Nick Blakey\xa0']

drop = set(DROPPED)
kept = [(n, s) for n, s in r23 if n not in drop]
rnd = random.Random(SEED)
pool = [s for _n, s in kept]
rnd.shuffle(pool)
out = [(n, pool[i]) for i, (n, _s) in enumerate(kept)]
# the added names take realistic mid-pack scores off the same distribution
extra = ADDED + INJURED_RETURNS
add_scores = [rnd.choice(pool) for _ in extra]
out += list(zip(extra, add_scores))

hi = iter([148, 141, 137, 133, 130, 127, 124, 121, 118, 115])
lo = iter([31, 28, 26, 24, 22, 21, 19, 17, 15, 12])
forced = {}
for n in RISERS:
    forced[n] = next(hi)
for n in FALLERS:
    forced[n] = next(lo)
out = [(n, forced.get(n, s)) for n, s in out]
out.sort(key=lambda t: (-t[1], t[0]))

body = 'Player,2026 R24\r\n' + ''.join('%s,%d\r\n' % (n, s) for n, s in out)
data = body.encode('cp1252')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'wb').write(data)
meta = {'path': os.path.relpath(OUT, ROOT), 'bytes': len(data),
        'md5': hashlib.md5(data).hexdigest(), 'sha256': hashlib.sha256(data).hexdigest(),
        'listed': len(out), 'seed': SEED, 'dropped': DROPPED, 'added': ADDED,
        'injured_returns': INJURED_RETURNS, 'risers': RISERS, 'fallers': FALLERS,
        'SYNTHETIC': 'REHEARSAL ONLY — this is not owner data and never was.'}
print(json.dumps(meta, indent=2, ensure_ascii=False))
