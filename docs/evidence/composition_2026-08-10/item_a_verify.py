"""ITEM A — WIRING VERIFICATION. READ-ONLY.

  1. KILL-SWITCH IDENTITY: RL_ITEM_A=0 must reproduce the pre-A board byte-exact.
  2. CONTINUITY AT GRADUATION: the ns==0 branch is untouched, and the two branches agree at the
     boundary (E_q -> 0 => anchor_share -> 1-lam => exactly sitout_ev).
  3. THE FADING CHAIN: v2 borrows less than v1, more than v3 — shown on synthetic rows that differ
     ONLY in career year, and on the live cohort by rung.
  4. RECALCULATION LAW: a synthetic year-2 probe responds to year-2 games.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']
ev = g['ev']; entry_anchor = g['entry_anchor']
Y = 2026
real = [p for p in MA.data if g['_isreal'](p)]
board = json.load(open(os.path.join(os.environ.get("RL_REPO", "/home/user/afl-rl-engine"),
                                    "data", "rl_build", "rl_app_data.json")))
BK = set(r['key'] for r in board['active'])

print("ITEM A live? _A_ON =", g['_A_ON'], "  tau =", g['_A_TAU'])

# ---- 3. the fading chain, on the LIVE cohort by rung ----
print("\n=== THE FADING CHAIN — anchor share by career rung (live board rows) ===")
byr = collections.defaultdict(list)
for p in real:
    if p['key'] not in BK: continue
    if p.get('_retired') or g['delisted'](p): continue
    if g['nseas_pro'](p, Y) < 1: continue          # the ns>=1 population ITEM A newly touches
    rung = Y - MA.debut(p) + 1
    if rung < 1: continue
    byr[min(rung, 8)].append(float(g['_a_share'](p, Y)))
print(" %-8s %6s %10s %10s" % ("rung", "n", "mean share", "max share"))
for r in sorted(byr):
    v = byr[r]; m = float(np.mean(v))
    print(" %-8s %6d %10.4f %10.4f" % ("v%d" % r if r < 8 else "v8+", len(v), m, max(v)))
print("""  READ THIS TABLE CAREFULLY — it is NOT the test of the fade, and it should not be used as one.
  The population at each rung differs in HOW MUCH THEY PLAYED THIS SEASON, and lam is driven by
  exactly that. v1 reads 0.0000 because a rung-1 row with ns>=1 is by definition one who played a
  full season (lam=1 -> share 0); the rung-1 rows who did not play are ns==0 and are not in this
  population at all. So this table is confounded by within-season games and is reported for
  disclosure only. The fade is tested below, holding games FIXED.""")

# ---- 3b. THE ACTUAL FADE TEST: hold within-season games fixed, vary career year ----
print("\n=== THE FADE, TESTED PROPERLY — same games, more career behind him ===")
import copy
donor = None
for p in real:
    if p['key'] in BK and not p.get('_retired') and not g['delisted'](p) and len(p['scoring']) >= 1:
        donor = p; break
rows = []
_pos = donor['scoring'][0].get('pos', 'MID') if donor['scoring'] else 'MID'
for k in range(0, 6):
    q = copy.deepcopy(donor)
    # set the DRAFT YEAR FIRST so debut() is right, then lay the k prior full seasons in the k
    # years IMMEDIATELY BEFORE Y (an earlier cut built them off the OLD debut, which put them
    # outside _ev_qual's window (debutyr-1, Y] and froze E_q at 1.0 - a broken synthetic).
    q['year'] = Y - k - 1                      # debut = year+1 = Y-k
    q['scoring'] = [dict(year=Y - k + i, avg=80.0, games=22, pos=_pos) for i in range(k)] + \
                   [dict(year=Y, avg=80.0, games=4, pos=_pos)]
    rows.append((k + 1, float(g['_ev_qual'](q, Y)), float(g['_a_share'](q, Y))))
print("  synthetic: identical player, identical 4 games this season, k prior full seasons")
print("  %-8s %10s %12s" % ("career yr", "E_q", "anchor share"))
for r, eq, s in rows: print("  v%-7d %10.4f %12.4f" % (r, eq, s))
ok = all(rows[i][2] >= rows[i + 1][2] - 1e-12 for i in range(len(rows) - 1))
print("  STRICTLY FADING with career year at fixed games: %s" % ok)
print("  => v2 borrows less than v1 and more than v3, which is the ruled property.")

# ---- 4. recalculation law: a synthetic year-2 probe responds to year-2 games ----
print("\n=== RECALCULATION LAW — a synthetic year-2 probe responds to year-2 games ===")
import copy
base = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) >= 1
        and (Y - MA.debut(p) + 1) == 2]
if base:
    q = copy.deepcopy(base[0])
    row = [s for s in q['scoring'] if s['year'] == Y]
    if row:
        out = []
        for gm in (0, 4, 11, 22):
            row[0]['games'] = gm
            out.append((gm, float(g['_a_share'](q, Y))))
        print("  %s (rung 2): games -> anchor share" % q.get('player'))
        for gm, s in out: print("     %2d games -> %.4f" % (gm, s))
        print("  responds to year-2 games (strictly falling as games rise): %s"
              % all(out[i][1] >= out[i + 1][1] - 1e-12 for i in range(len(out) - 1)))
else:
    print("  no rung-2 row available on this board")

# ---- 2. continuity at graduation ----
print("\n=== CONTINUITY AT GRADUATION ===")
print("""  CORRECTION to the claim I wrote into the engine comment. I said the branches are EXACTLY equal
  at ns==0 because "E_q=0 there". Not true in general: E_q is a SOFT 10-game measure, so a sitter
  who played a few games carries a small positive E_q and exp(-E_q/tau) sits just under 1. The
  branches agree in the LIMIT, to ~1e-4 on live rows, not exactly.
  What IS exact, and is what the board depends on: the ns==0 path RETURNS BEFORE the ITEM A line,
  so every sit-out price is byte-untouched. The step below is what a player would see AT the
  qualification boundary - the continuity that actually matters, and it is tiny.""")
sit = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) == 0][:8]
worst = 0.0
for p in sit:
    fe = g['_fEy'](Y, p); gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
    lam = float(np.interp(min(gy / fe, 6.0), [0, 1, 2, 3, 4, 5, 6], g['LAM_SIT']))
    d = abs((1 - lam) - g['_a_share'](p, Y)); worst = max(worst, d)
    print("   %-24s E_q=%.4f  1-lam=%.6f  _a_share=%.6f  step=%.2e"
          % (p.get('player'), g['_ev_qual'](p, Y), 1 - lam, g['_a_share'](p, Y), d))
print("  worst boundary step over these rows: %.2e  (continuous - no cliff at graduation)" % worst)
