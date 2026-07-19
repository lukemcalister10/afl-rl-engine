#!/usr/bin/env python3
# LEG F5 — SEAL THE ENTRANT-SLOT STRUCTURE (MEMO_LEGF v1.3 §2.viii, owner item 359).
# Measured from RECORDED intake history in the store; smoothed (per-slot mean occupancy over the window,
# no wide bins — CORE rule 7); committed + SEALED BEFORE any render (the §6 seal-first law). The structure
# is NOT tuned against any gate (LAW: no entrant-count tuning). Pricing basis = the engine's OWN effective
# pick effpk(p): ND=pick, RD/PSD=chained after the national draft (_NDC[year]+pick), pickless mechanisms =
# their measured pick-equivalents PICKEQ (MSD=90, others=92, item 341). Each expected slot credited at the
# v2-curve PVC of its effective pick. Run single-thread from the F5 workspace rl_after.
import io, contextlib, json, hashlib, sys
import statistics as st
from collections import Counter, defaultdict

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; data = MA.data; effpk = MA.effpk; GRP = MA.GRP
PVC = {int(k): v for k, v in MA.PVC.items()}; PICKEQ = dict(MA.PICKEQ)
PVCMAX = max(PVC)

# ---- measurement window: complete draft years only (2026 is a partial mid-season cohort -> excluded) ----
WINDOW = list(range(2019, 2026))            # 7 years (rule-7 span)
nY = len(WINDOW)
DRAFT_TYPES = {'ND', 'RD', 'PSD'}           # real pick space (RD/PSD chained onto national by the engine)

def pvc(e): return PVC[min(e, PVCMAX)]

# ---- gather every board-eligible (GRP-priced) entrant per year, keyed by effective pick ----
draft_effpk = defaultdict(list)             # year -> [effpk...]  (draft rounds)
mech_effpk  = defaultdict(list)             # year -> [effpk...]  (pickless mechanisms)
mech_type   = defaultdict(Counter)          # year -> {type: n}
for p in data:
    y = p.get('year')
    if y not in WINDOW or p.get('pos') not in GRP:
        continue
    e = effpk(p)
    if (p.get('type') in PICKEQ) or p.get('_pickless'):
        mech_effpk[y].append(e); mech_type[y][p['type']] += 1
    else:
        draft_effpk[y].append(e)            # ND + RD + PSD (real / chained pick)

# ---- SMOOTH (rule 7): expected per-year occupancy per effective-pick slot = mean count over the window ----
def occupancy(byyear):
    tally = defaultdict(int)
    for y in WINDOW:
        for e in byyear[y]:
            tally[e] += 1
    return {e: tally[e] / nY for e in sorted(tally)}     # fractional expected slots per year (the smoother)

draft_occ = occupancy(draft_effpk)
mech_occ  = occupancy(mech_effpk)

def occ_value(occ): return sum(cnt * pvc(e) for e, cnt in occ.items())
def occ_count(occ): return sum(occ.values())

draft_pvc = occ_value(draft_occ); draft_n = occ_count(draft_occ)
mech_pvc  = occ_value(mech_occ);  mech_n  = occ_count(mech_occ)
total_pvc = draft_pvc + mech_pvc; total_n = draft_n + mech_n

# ---- per-mechanism summary (mean count/yr + pick-equivalent + face value) ----
mech_summary = {}
for t, eq in sorted(PICKEQ.items(), key=lambda kv: kv[1]):
    n = sum(mech_type[y].get(t, 0) for y in WINDOW) / nY
    if n > 0:
        mech_summary[t] = {'mean_per_year': round(n, 4), 'pick_equiv': eq,
                           'pvc_each': pvc(eq), 'pvc_total': round(n * pvc(eq))}

# ---- per-round pick counts (draft side, readability): AFL round bands on the effective pick ----
ROUNDS = [(1, 18), (19, 36), (37, 54), (55, 72), (73, 90), (91, 99)]
round_counts = {}
for lo, hi in ROUNDS:
    n = sum(cnt for e, cnt in draft_occ.items() if lo <= e <= hi)
    v = sum(cnt * pvc(e) for e, cnt in draft_occ.items() if lo <= e <= hi)
    round_counts['%d-%d' % (lo, hi)] = {'mean_slots': round(n, 3), 'pvc': round(v)}

structure = {
    'name': 'F5_ENTRANT_SLOT_STRUCTURE',
    'law': 'MEMO_LEGF v1.3 §2.viii (owner item 359)',
    'basis': ('FULL expected annual intake measured from recorded store intake history; each board-eligible '
              '(GRP) entrant credited at the v2-curve PVC of its engine effective pick effpk(p) '
              '(ND=pick, RD/PSD=chained _NDC[year]+pick, pickless=PICKEQ 90/92, item 341). Smoothed = '
              'per-effective-pick mean per-year occupancy over the window (no wide/decile bins, CORE rule 7). '
              'Measured ONCE, sealed pre-render, NOT tuned against the conservation gate.'),
    'window': [WINDOW[0], WINDOW[-1]], 'n_years': nY,
    'pickeq': {t: PICKEQ[t] for t in sorted(PICKEQ)},
    'expected_slots_per_year': round(total_n, 2),
    'entrant_pvc': {'draft': round(draft_pvc), 'mech': round(mech_pvc), 'total': round(total_pvc)},
    'expected_counts': {'draft': round(draft_n, 2), 'mech': round(mech_n, 2)},
    'draft_occupancy': {str(e): round(c, 4) for e, c in draft_occ.items()},   # effpk -> mean slots/yr
    'mech_occupancy':  {str(e): round(c, 4) for e, c in mech_occ.items()},
    'round_counts': round_counts,
    'mech_summary': mech_summary,
    'per_club': {'n_clubs': 18,
                 'rule': ('league expected structure allocated across the 18 clubs in natural draft order '
                          '(round-robin over the sorted effective-pick slot list); mechanisms split evenly. '
                          'Report/view only — the §2.x gate is LEAGUE-level, so the club split is presentational.')},
    'stamp': {'store_md5': '968de0c7', 'curve_file_md5': '56dd7a7b', 'curve_payload_md5': '89c14729',
              'board_balanced_md5': '06d8af60'},
}
payload = json.dumps(structure, sort_keys=True, separators=(',', ':')).encode()
structure['seal_sha256_8'] = hashlib.sha256(payload).hexdigest()[:8]

out = sys.argv[1] if len(sys.argv) > 1 else 'sealed_entrant_structure.json'
json.dump(structure, open(out, 'w'), indent=1, sort_keys=True)
print('SEALED ENTRANT STRUCTURE -> %s' % out)
print('  window %s (%d yrs) · expected %.1f slots/yr' % (structure['window'], nY, total_n))
print('  entrant PVC: draft %d + mech %d = TOTAL %d' % (round(draft_pvc), round(mech_pvc), round(total_pvc)))
print('  seal sha256_8 = %s' % structure['seal_sha256_8'])
