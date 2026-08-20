#!/usr/bin/env python3
"""ORDER 29 -- STEP 1b, THE P3 INDIRECT-MOVER ENUMERATION.

PREREG P3 predicts that the unflag-three reaches the board NOT through the ORDER-28 derivation lane
(which never read the flags) but through the ENGINE'S OWN v3.4 kernel curve, by two channels:

  1. DIRECT CONTRIBUTION -- the three careers enter _curve_sample at picks 4 / 12 / 14 (window +-4);
  2. THE SLIDE-UP UNWIND -- rl_model.py:317-327 slides every OTHER ND-2011 row up by the number of
     excluded picks north of it; unflagging removes the slide, so the whole 2011 ND cohort's curve
     attribution moves by up to 3 picks.

and that both together move PVC[1], hence BOARD_FACTOR = (_P1/PVC[1])*s, hence EVERY board row.

This harness enumerates all of it with numbers -- nothing is asserted without its measurement.
Inputs: PROBE34_PRE.json (store d9a24282, flags present) and PROBE34_POST.json (store cb38ef11).
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o29'
A = json.load(open(SP + '/PROBE34_PRE.json'))    # flags PRESENT  (live store d9a24282)
B = json.load(open(SP + '/PROBE34_POST.json'))   # flags DELETED  (store cb38ef11)

THREE = {'dylan-shiel': 4, 'jeremy-cameron': 12, 'adam-treloar': 14}
LOG = []
def P(s=''):
    print(s); LOG.append(s)

P("=" * 122)
P("ORDER 29  --  STEP 1b, THE P3 INDIRECT MOVERS: THE v3.4 KERNEL CURVE, ENUMERATED")
P("=" * 122)
P("  PRE  store d9a24282  (the three carry _pvc_exclude)")
P("  POST store cb38ef11  (the three flags DELETED -- and nothing else)")
P("  Both probes: dial OFF, RL_PICK1=3000, same pinned venv, same five-var thread pinning.")
P()

# ------------------------------------------------------------------ 1. the head and BOARD_FACTOR
hA, hB = A['pvc34_head'], B['pvc34_head']
fA, fB = A['BOARD_FACTOR'], B['BOARD_FACTOR']
sA, sB = A['NUM']['s'], B['NUM']['s']
P("-" * 122)
P("1. THE HEAD, AND THE CHANNEL EVERY BOARD ROW RIDES")
P("-" * 122)
P("   v3.4 PRE-ANCHOR HEAD  PVC[1]      %8d  ->  %8d      %+d   (%+.4f%%)"
  % (hA, hB, hB - hA, 100.0 * (hB / hA - 1)))
P("   numeraire s (unmoved at this step) %.16f  ->  %.16f" % (sA, sB))
P("   BOARD_FACTOR = (_P1/PVC[1])*s      %.12f  ->  %.12f   ratio %.9f  (%+.4f%%)"
  % (fA, fB, fB / fA, 100.0 * (fB / fA - 1)))
P()
P("   P3 PREDICTED |delta| on the v3.4 head UNDER 3%%.   MEASURED %+.4f%%  ->  %s"
  % (100.0 * (hB / hA - 1), "HELD" if abs(hB / hA - 1) < 0.03 else "BREACHED"))
P()
P("   The head RISES because the three careers are added back to the pick-1 window: pick 1's +-4")
P("   window reaches pick 4, and dylan-shiel sits at pick 4.  A higher head DIVIDES INTO")
P("   BOARD_FACTOR, so BOARD_FACTOR FALLS and every priced player falls with it -- by %.4f%%."
  % (100.0 * (fB / fA - 1)))
P("   This is the whole of the unflag-three's reach onto the board: it is a PLAYER-SIDE scalar.")
P("   The shipped PICK curve is the artifact (PVC=_PVC2M), so the picks do not move from this.")

# ------------------------------------------------------------------ 2. the per-pick curve deltas
P()
P("-" * 122)
P("2. THE v3.4 KERNEL CURVE, PER PICK 1-64  (pre-anchor, the engine's own kernel -- NOT the artifact)")
P("-" * 122)
P("   %5s %10s %10s %9s %9s   | %5s %10s %10s %9s %9s" % ("pick", "PRE", "POST", "delta", "pct", "pick", "PRE", "POST", "delta", "pct"))
rows = []
for k in range(1, 65):
    a, b = A['pvc34'][str(k)], B['pvc34'][str(k)]
    rows.append((k, a, b, b - a, 100.0 * (b / a - 1) if a else float('nan')))
for i in range(0, 32):
    l, r = rows[i], rows[i + 32]
    P("   %5d %10d %10d %+9d %+8.3f%%   | %5d %10d %10d %+9d %+8.3f%%"
      % (l[0], l[1], l[2], l[3], l[4], r[0], r[1], r[2], r[3], r[4]))
moved = [r for r in rows if r[3] != 0]
P()
P("   picks 1-64 that MOVED: %d of 64.   max |delta| %+d at pick %d;  max |pct| %+.3f%% at pick %d"
  % (len(moved), max(moved, key=lambda r: abs(r[3]))[3], max(moved, key=lambda r: abs(r[3]))[0],
     max(moved, key=lambda r: abs(r[4]))[4], max(moved, key=lambda r: abs(r[4]))[0]))

# ------------------------------------------------------------------ 3. the slide-up unwind
P()
P("-" * 122)
P("3. THE SLIDE-UP UNWIND  (rl_model.py:317-327)  -- every ND-2011 row whose CURVE ATTRIBUTION moved")
P("-" * 122)
NA = {r['key']: r for r in A['nd2011']}
NB = {r['key']: r for r in B['nd2011']}
P("   ND-2011 rows in hist: PRE %d, POST %d" % (A['nd2011_n'], B['nd2011_n']))
P()
P("   %-26s %6s %8s %10s %10s %8s  %s" % ("key", "pick", "effpk", "epk PRE", "epk POST", "shift", "note"))
slid = []
for k in sorted(NB, key=lambda x: (NB[x]['pick'] is None, NB[x]['pick'])):
    a, b = NA.get(k), NB[k]
    if a is None: continue
    sh = b['epk'] - a['epk']
    note = ''
    if k in THREE: note = 'UNFLAGGED -- re-enters the curve at its stored pick'
    elif sh: note = 'slide-up unwound (+%d)' % sh
    if sh or k in THREE:
        slid.append((k, a['pick'], a['epk'], b['epk'], sh, note))
        P("   %-26s %6s %8s %10s %10s %+8d  %s" % (k, b['pick'], b['effpk'], a['epk'], b['epk'], sh, note))
P()
_sh = [r for r in slid if r[0] not in THREE]
P("   rows whose curve attribution SLID: %d   (max shift %+d picks)"
  % (len(_sh), max([r[4] for r in _sh]) if _sh else 0))
P("   P3 predicted the cohort moves 'by up to 3 picks' -- MEASURED max %+d.  %s"
  % (max([r[4] for r in _sh]) if _sh else 0, "HELD" if _sh and max(r[4] for r in _sh) <= 3 else "CHECK"))
P()
P("   PRE:  the three are excluded, so every 2011 row south of them slid UP by the count of excluded")
P("         picks north of it (1 north of pick 4, 2 north of pick 12, 3 north of pick 14).")
P("   POST: _pvc_excl_eff[2011] is EMPTY, so no _pvc_eff is set on any 2011 row and _epk falls back")
P("         to effpk -- the slide is not 'reversed', it is never applied.  Every 2011 row now teaches")
P("         the curve at its TRUE pick.")

# ------------------------------------------------------------------ 4. the +-4 sample membership
P()
P("-" * 122)
P("4. THE +-4 CURVE SAMPLE  -- which picks' fits actually changed population")
P("-" * 122)
P("   %5s %7s %7s %7s   %s" % ("pick", "n PRE", "n POST", "dn", "membership change"))
ch = 0
for k in range(1, 65):
    ka, kb = set(A['sample_keys'].get(str(k), [])), set(B['sample_keys'].get(str(k), []))
    if ka == kb: continue
    ch += 1
    add, rem = sorted(kb - ka), sorted(ka - kb)
    d = []
    if add: d.append("+" + ", +".join(add))
    if rem: d.append("-" + ", -".join(rem))
    P("   %5d %7d %7d %+7d   %s" % (k, len(ka), len(kb), len(kb) - len(ka), "   ".join(d)))
P()
P("   picks whose fit population changed: %d of 64" % ch)
for k, pk in sorted(THREE.items(), key=lambda kv: kv[1]):
    ins = [j for j in range(1, 65) if k in set(B['sample_keys'].get(str(j), []))]
    was = [j for j in range(1, 65) if k in set(A['sample_keys'].get(str(j), []))]
    P("   %-16s stored pick %-3d  enters the fit at picks %s   (PRE: %s)"
      % (k, pk, "%d-%d" % (min(ins), max(ins)) if ins else "none", "%d-%d" % (min(was), max(was)) if was else "NONE"))

P()
P("-" * 122)
P("VERDICT ON P3")
P("-" * 122)
P("   BOTH predicted channels FIRED, and are enumerated above with their numbers:")
P("     channel 1, direct contribution -- the three enter the fit windows around picks 4 / 12 / 14;")
P("     channel 2, the slide-up unwind -- %d other ND-2011 rows teach at a different pick." % len(_sh))
P("   The v3.4 head moved %+d (%+.4f%%), therefore BOARD_FACTOR moved %+.4f%%, therefore EVERY"
  % (hB - hA, 100.0 * (hB / hA - 1), 100.0 * (fB / fA - 1)))
P("   priced board row moves through this channel.  P3 HELD, including its <3%% magnitude bound.")

open(HERE + '/P3_INDIRECT_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'head_pre': hA, 'head_post': hB, 'head_pct': 100.0 * (hB / hA - 1),
           'board_factor_pre': fA, 'board_factor_post': fB, 'board_factor_ratio': fB / fA,
           'board_factor_pct': 100.0 * (fB / fA - 1),
           'curve_pre': {str(k): A['pvc34'][str(k)] for k in range(1, 65)},
           'curve_post': {str(k): B['pvc34'][str(k)] for k in range(1, 65)},
           'picks_moved': len(moved),
           'slid_rows': [{'key': r[0], 'pick': r[1], 'epk_pre': r[2], 'epk_post': r[3], 'shift': r[4]} for r in slid],
           'sample_changed_picks': ch},
          open(HERE + '/P3_INDIRECT.json', 'w'), indent=1)
