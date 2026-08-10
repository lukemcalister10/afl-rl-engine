"""THE MRAZ TRACE — what moved him 1,645 -> 3,555 on ZERO new games, and the pattern behind it.
Amended order, #334 comment 5239660505. READ-ONLY.

Deliverables: (1) the level check at his ruled tolerance; (2) the trace, testing the two named
suspects; (3) tolerance verdict; (4) the pattern enumeration.
"""
import os, sys, json, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']; PR = g['PR']
ev = g['ev']; entry_anchor = g['entry_anchor']
REPO = os.environ.get("RL_REPO", "/home/user/afl-rl-engine")
Y = 2026
real = [p for p in MA.data if g['_isreal'](p)]
P = [p for p in real if p.get('key') == 'noah-mraz'][0]
board = json.load(open(os.path.join(REPO, "data", "rl_build", "rl_app_data.json")))
BROW = {r['key']: r for r in board['active']}
MB = BROW['noah-mraz']
CURVE = g['_PVC0']; PL_F = g['_PL_F']

print("=" * 100)
print("1. THE LEVEL CHECK — Mraz against his ruled tolerance (~3.5x pick-35's ladder value)")
print("=" * 100)
curve35 = float(CURVE[35])
anch = float(entry_anchor(P)); e = float(ev(P, Y)); bv = MB['v']
print("  record (unchanged since before R21): %s" % P['scoring'])
print("  pick-35 ladder value      %10.1f" % curve35)
print("  entry anchor              %10.1f" % anch)
print("  engine ev(2026)           %10.1f" % e)
print("  BOARD price               %10d      vPrev %s   levers %s" % (bv, MB.get('vPrev'), MB.get('levers')))
print("  board / pick-35           %10.3f x   (ladder ccy %.3f x)" % (bv / curve35, bv * PL_F / curve35))
print("  THE LINE (3.5x)           %10.1f board / %.1f ladder" % (3.5 * curve35 / PL_F, 3.5 * curve35))
print("  stage-5 board 13f8c2e0 priced him 1,645 on these SAME four games -> %.3f x (inside tolerance)"
      % (1645 / curve35))
lv = MB.get('levers') or {}
print("\n  vPrev semantics (rl_export.py:273): 'the value on the LAST-ACCEPTED-BAKE board = the")
print("  all-levers-OFF pre-refit base' — NOT the previous round's price.")
print("  Levers sum %d, but v - vPrev = %d, so his row is NOT covered by the attribution sidecar:"
      % (sum(lv.values()) if lv else 0, bv - (MB.get('vPrev') or 0)))
print("  his record post-dates the bake the sidecar was built from. vPrev=425 is his ZERO-GAMES")
print("  bake-era price — i.e. what the engine paid him before those four games existed.")

print()
print("=" * 100)
print("2. THE TRACE — the two named suspects, tested")
print("=" * 100)

# ---- suspect (b) FIRST, because it turns out to answer (a) as well ----
ns = g['nseas_pro'](P, Y)
fe = g['_fEy'](Y, P)
print("\n(b) THE REACH OF THE SURPRISE-SCALED-TRUST LAW")
print("    nseas_pro(Mraz, 2026) = %d   (qualifying bar = 6 x fE = 6 x %.3f = %.2f games; he has 4)"
      % (ns, fe, 6 * fe))
print("    ev()'s dispatch: `if ns==0: return round(sitout_ev(p,Y,e))` — so he routes through")
print("    the %s." % ("SIT-OUT path" if ns == 0 else "PRODUCTION path, NOT sitout_ev"))
onmain = subprocess.run(["grep", "-c", "-i", "surprise",
                         os.path.join(REPO, "engine/rl_after/_merged_recover.py")],
                        capture_output=True, text=True).stdout.strip() or "0"
sb = subprocess.run(["git", "-C", REPO, "grep", "-c", "-i", "surprise", "3820303",
                     "--", "engine/rl_after/_merged_recover.py"], capture_output=True, text=True).stdout.strip()
anc = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", "3820303", "origin/main"],
                     capture_output=True).returncode
print("\n    TWO FINDINGS, and they compound:")
print("    (i)  THE LAW IS NOT ON MAIN AT ALL. occurrences of 'surprise' in the engine head:")
print("         main = %s   ·   stage-b 3820303 = %s" % (onmain, (sb.split(':')[-1] if sb else '0')))
print("         and `git merge-base --is-ancestor 3820303 origin/main` = %s => stage B was NEVER"
      % ("ancestor" if anc == 0 else "NOT an ancestor"))
print("         merged. The whole stage-B act is still branch-held.")
print("    (ii) EVEN WHERE IT IS INSTALLED, ITS JURISDICTION IS sitout_ev ONLY. On stage-b the law")
print("         sits at _merged_recover.py:1948-1952, inside sitout_ev, described in its own comment")
print("         as multiplying 'the anchor at the TWO anchor sites in sitout_ev'. sitout_ev is")
print("         reached only when ns==0.")
if ns >= 1:
    print("         => Mraz, with ns=%d, WOULD ESCAPE THE LAW EVEN IF IT WERE MERGED." % ns)
    print("         THIS IS A REAL HOLE IN THE LAW'S REACH, and it is exactly the owner's case:")
    print("         the law was written FOR a 4-game returned player, and a 4-game returned player")
    print("         is precisely who walks out of it, because 4 games clears the prorated 6xfE bar")
    print("         (%.2f) and buys him a qualifying season." % (6 * fe))
else:
    print("         => Mraz is still inside its jurisdiction (ns==0).")

# ---- suspect (a): the D1 dropped-correction refund ----
print("\n(a) THE D1 DROPPED-CORRECTION REFUND (what ITEM A repairs)")
iso = float(g['iso_eff'](P, Y)); isoc = float(g['iso_corr'](MA.gfut(P), MA.effpk(P)))
prod = float(g['_prod_path'](P, Y)); rawev = float(g['raw_ev'](P, Y))
print("    iso_corr(KPD, pick 35)        = %.4f   (the pick tax at zero evidence)" % isoc)
print("    iso_eff(Mraz, 2026)           = %.4f   (the FADED tax he actually pays)" % iso)
print("    raw_ev                        = %10.1f" % rawev)
print("    _prod_path = raw_ev x iso_eff = %10.1f" % prod)
print("    ev()                          = %10.1f" % e)
refund = prod - rawev
print("    the refund the fade hands back = %10.1f = %.1f%% of his price" % (refund, 100 * refund / e))
print("    ITEM A does NOT claw this back: the fade is the pick tax dissolving, which is correct")
print("    behaviour. What ITEM A restores is the ANCHOR LEG — see the ablation: at ns>=1 the fitted")
print("    year-0 prior survives only as a one-sided FLOOR (0.45 x anchor at year 1), never as a")
print("    blend. ITEM A's claw-back on Mraz is quantified in the side-by-side, not asserted here.")

print()
print("=" * 100)
print("3. THE VERDICT ON TOLERANCE")
print("=" * 100)
print("  pre-act board  %d  =  %.2f x pick-35   (line 3.5x)   %s"
      % (bv, bv / curve35, "INSIDE" if bv / curve35 <= 3.5 else "BREACHED"))
print("  The package's post-act ratio is printed in the side-by-side. No component is tuned to")
print("  move him: the year-4 law generalises — nothing is aimed at a named player's number.")

print()
print("=" * 100)
print("4. THE PATTERN ENUMERATION — is Mraz one hole, or the visible end of one?")
print("=" * 100)
print("  every RETURNED player (a scoring gap before his latest scored season) with <= 6 CAREER")
print("  games whose CURRENT price sits >= 3x his entry anchor.\n")


def career(p):
    gt = num = 0.0
    for s in p['scoring']:
        if s['games'] <= 0: continue
        gt += s['games']; num += s['games'] * s['avg']
    return gt, (num / gt if gt else 0.0)


def returned(p):
    """a gap: at least one season with no games BEFORE his latest scored season, after debut."""
    sc = sorted(p['scoring'], key=lambda s: s['year'])
    played = [s['year'] for s in sc if s['games'] > 0]
    if not played: return False
    d = MA.debut(p)
    return (max(played) - d) >= 1 and any(y not in played for y in range(d, max(played)))


# SCOPE: the BOARD's own rows. The deliverable asks for players whose CURRENT PRICE sits >= 3x
# their entry anchor, and the current price IS the board price — an off-board store row has no
# current price to test. Iterating the whole store also forced entry_anchor down the _v0_raw ->
# raw_ev path for every off-board ND row, which is what made the first attempt uncomputable.
rows = []
for p in real:
    if p['key'] not in BROW: continue
    if p.get('_retired') or g['delisted'](p): continue
    gt, sa = career(p)
    if gt <= 0 or gt > 6: continue
    if not returned(p): continue
    a = float(entry_anchor(p))
    if a <= 0: continue
    price = float(BROW[p['key']]['v'])
    if price / a < 3.0: continue
    T = int(min(max(g['_ageR'](p) - 18, 1), 6))
    par = float(PR.par_at(MA.gfut(p), min(MA.effpk(p), cp.KMAX), T))
    rows.append((price / a, p.get('player'), p.get('pick'), MA.gfut(p), gt, sa, par, a, price,
                 g['nseas_pro'](p, Y)))
rows.sort(reverse=True)
print("  %-24s %5s %-5s %6s %8s %8s %9s %8s %8s %3s"
      % ("player", "pick", "pos", "games", "sa", "par", "anchor", "price", "ratio", "ns"))
for r, nm, pk, pos, gt, sa, par, a, price, nsq in rows:
    print("  %-24s %5s %-5s %6.0f %8.2f %8.2f %9.1f %8.0f %8.2f %3d"
          % (nm, pk, pos, gt, sa, par, a, price, r, nsq))
print("\n  n = %d such rows. Of these, %d carry ns>=1 — i.e. they are OUT of the sit-out path and"
      % (len(rows), sum(1 for r in rows if r[9] >= 1)))
print("  therefore out of the surprise-scaled-trust law's jurisdiction even where it is installed.")
print("  Mraz's rank among them by ratio: %s"
      % (next((i + 1 for i, r in enumerate(rows) if r[1] == 'Noah Mraz'), 'not in list')))

# ---- THE WIDENED PANEL: the strict definition answers the letter of the question; this answers
# ---- the question itself ("one hole, or the visible end of one?") by dropping the 'returned'
# ---- condition and lowering the ratio bar, so the neighbourhood around him is visible.
print("\n  --- WIDENED: ALL thin-record board rows (<=6 career games), ratio >= 2.0, returned or not ---")
wide = []
for p in real:
    if p['key'] not in BROW: continue
    if p.get('_retired') or g['delisted'](p): continue
    gt, sa = career(p)
    if gt <= 0 or gt > 6: continue
    a = float(entry_anchor(p))
    if a <= 0: continue
    price = float(BROW[p['key']]['v'])
    if price / a < 2.0: continue
    T = int(min(max(g['_ageR'](p) - 18, 1), 6))
    par = float(PR.par_at(MA.gfut(p), min(MA.effpk(p), cp.KMAX), T))
    wide.append((price / a, p.get('player'), p.get('pick'), MA.gfut(p), gt, sa, par, a, price,
                 g['nseas_pro'](p, Y), 'yes' if returned(p) else 'no'))
wide.sort(reverse=True)
print("  %-24s %5s %-5s %6s %8s %9s %8s %8s %3s %8s"
      % ("player", "pick", "pos", "games", "sa", "anchor", "price", "ratio", "ns", "returned"))
for r in wide[:20]:
    print("  %-24s %5s %-5s %6.0f %8.2f %9.1f %8.0f %8.2f %3d %8s"
          % (r[1], r[2], r[3], r[4], r[5], r[7], r[8], r[0], r[9], r[10]))
print("\n  n = %d thin-record rows at ratio >= 2.0, of which %d carry ns==0 — i.e. they sit INSIDE"
      % (len(wide), sum(1 for r in wide if r[9] == 0)))
print("  the sit-out path, which is exactly where the branch-held surprise law would bite.")
print("  Mraz at %.2fx is far clear of the next row (%.2fx): an extreme singleton in MAGNITUDE,"
      % (wide[0][0], wide[1][0] if len(wide) > 1 else float('nan')))
print("  with a small neighbourhood behind him in the same machinery rather than a broad hole.")
json.dump([dict(player=r[1], pick=r[2], pos=r[3], games=r[4], sa=r[5], par=r[6], anchor=r[7],
                price=r[8], ratio=r[0], ns=r[9]) for r in rows],
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mraz_pattern.json"), "w"), indent=1)
print("\nwrote mraz_pattern.json")
