"""LEG-D ACT-2 — the item-256 LEDGERS (positional-rank tie-break) + the NAMED ROWS deliverable.
Compares the prev board 9829d01a (/tmp/board_prev.json) vs the candidate 270a2c5f (/tmp/board_v2.json).
Ledger 1 = movement (all active movers). Ledger 2 = value-UP / rank-DOWN subset. Writes out/ledgers.json."""
import json
PREV = json.load(open('/tmp/board_prev.json'))
V2 = json.load(open('/tmp/board_v2.json'))
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'

def rank_map(bd):
    # board rank by value desc; item-256 tie-break = POSITIONAL rank (stable secondary key on group then name)
    rows = [r for r in bd['active']]
    rows.sort(key=lambda r: (-r['v'], r.get('grp', ''), r['name']))
    return {r['name']: i + 1 for i, r in enumerate(rows)}, {r['name']: r for r in bd['active']}

pr_rank, PR = rank_map(PREV)
v2_rank, VV = rank_map(V2)

# --- Ledger 1: movement (all active movers) ---
movers = []
for nm in PR:
    if nm in VV and PR[nm]['v'] != VV[nm]['v']:
        movers.append(dict(name=nm, grp=PR[nm].get('grp'), pk=PR[nm].get('ep') or PR[nm].get('pk'),
                           v_prev=PR[nm]['v'], v_new=VV[nm]['v'], dv=VV[nm]['v'] - PR[nm]['v'],
                           rank_prev=pr_rank[nm], rank_new=v2_rank[nm], d_rank=v2_rank[nm] - pr_rank[nm]))
movers.sort(key=lambda m: -abs(m['dv']))

# --- Ledger 2: value-UP / rank-DOWN subset (positional-rank tie-break already in rank_map) ---
up_down = [m for m in movers if m['dv'] > 0 and m['d_rank'] > 0]

# --- named rows ---
def find(bd_map, sub):
    c = [n for n in bd_map if sub.lower() in n.lower()]
    return c[0] if c else None
named = {}
for label in ('Marcus Bontempelli', 'Harley Reid', 'Ryley Sanders', 'Max Gawn', 'Christian Petracca',
              'Harry Sheezel', 'Nick Daicos'):
    n = find(PR, label)
    if n: named[label] = dict(v_prev=PR[n]['v'], v_new=VV[n]['v'], dv=VV[n]['v'] - PR[n]['v'],
                              rank_prev=pr_rank[n], rank_new=v2_rank[n])
two_young = [dict(name=m['name'], v_prev=m['v_prev'], v_new=m['v_new'], dv=m['dv']) for m in movers[:2]]

# top-10 picks old(L1b) -> new(v2) — the pick currency itself
L1b = {int(k): int(v) for k, v in json.load(open('/home/user/afl-rl-engine/engine/rl_after/pvc_curve_L1b.json'))['curve'].items()}
V2C = {int(k): int(v) for k, v in json.load(open('/home/user/afl-rl-engine/engine/rl_after/pvc_curve_v2.json'))['curve'].items()}
top10_picks = [dict(pick=p, L1b=L1b[p], v2=V2C[p], dv=V2C[p] - L1b[p]) for p in range(1, 11)]
held_picks = V2.get('pick_band_mean', {})   # held pick = mean of live curve over ladder band

out = dict(
    _doc="item-256 ledgers (positional-rank tie-break) + named rows. prev 9829d01a -> candidate 270a2c5f.",
    ledger1_movement=dict(n_active_movers=len(movers), rows=movers),
    ledger2_value_up_rank_down=dict(n=len(up_down), tie_break='POSITIONAL rank (grp,name secondary key)', rows=up_down),
    named_rows=named, two_largest_young_movers=two_young,
    top10_picks_L1b_to_v2=top10_picks, held_pick_band_mean=held_picks,
    posture_2027_discounts=V2.get('posture_2027_discounts'),
)
json.dump(out, open(BASE + '/out/ledgers.json', 'w'), indent=1)
print("=== item-256 LEDGERS (9829d01a -> 270a2c5f) ===")
print("Ledger 1 (movement): %d active movers" % len(movers))
print("Ledger 2 (value-up/rank-down): %d  (tie-break POSITIONAL rank)" % len(up_down))
print("\n=== NAMED ROWS ===")
for k, v in named.items():
    print("  %-20s %5d -> %5d (%+d)  rank %d->%d" % (k, v['v_prev'], v['v_new'], v['dv'], v['rank_prev'], v['rank_new']))
print("  two largest young movers:", [(m['name'], '%d->%d' % (m['v_prev'], m['v_new'])) for m in two_young])
print("  top-10 picks L1b->v2:", [(d['pick'], d['L1b'], d['v2']) for d in top10_picks])
print("  held pick-band mean (live curve):", held_picks)
print("wrote out/ledgers.json")
