"""JOB 4(a) — INPUT VERIFICATION: national_draft_last_pick.json vs the store's OWN per-year National max.
Pure store read (no engine). Emits every year, every mismatch NAMED. The owner's bug-class argument:
if the chaining offset file disagrees with the store's own National MAX ordinal, the pickless (rookie/PSD)
_eff derivation chains off a wrong base. This script does NOT rule; it reports the reconciliation.
"""
import json, collections
STORE = '/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'
NDLP = '/home/user/afl-rl-engine/engine/rl_after/national_draft_last_pick.json'
OUT = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation/out/job4a_national_last_pick.json'

store = json.load(open(STORE))
ndlp = json.load(open(NDLP))['last_national_pick']

# store's own National rows: type == 'ND', with a pick, per draft year
by_year = collections.defaultdict(list)
for p in store:
    if p.get('type') == 'ND' and p.get('pick') and p.get('year'):
        by_year[p['year']].append(int(p['pick']))

rows = []
for y in sorted(set(list(by_year.keys()) + [int(k) for k in ndlp])):
    picks = sorted(by_year.get(y, []))
    smax = max(picks) if picks else None
    scount = len(picks)
    file_val = ndlp.get(str(y))
    gaps = [n for n in range(1, (smax or 0) + 1) if n not in set(picks)] if smax else []
    match_max = (file_val == smax)
    rows.append(dict(year=y, file_last_national_pick=file_val, store_national_MAX=smax,
                     store_national_COUNT=scount, n_gaps=len(gaps), gaps=gaps,
                     file_eq_store_max=match_max,
                     file_eq_store_count=(file_val == scount)))

mismatch_max = [r for r in rows if not r['file_eq_store_max']]
out = dict(
    _doc="Job 4(a): national_draft_last_pick.json vs store MAX National ordinal per year. "
         "The file DECLARES basis = store MAX (database ND end). This verifies that claim row by row.",
    basis_declared_by_file="store MAX National ordinal (database ND end); owner data law 2026-07-11",
    rows=rows,
    n_years=len(rows),
    n_mismatch_vs_store_max=len(mismatch_max),
    mismatch_years=[r['year'] for r in mismatch_max],
    years_with_gaps=[r['year'] for r in rows if r['n_gaps'] > 0],
)
json.dump(out, open(OUT, 'w'), indent=1)
print("=== JOB 4(a) national_draft_last_pick vs store MAX ===")
print(f"{'yr':>4} {'file':>5} {'sMAX':>5} {'sCNT':>5} {'gaps':>5} {'==MAX':>6} {'==CNT':>6}")
for r in rows:
    print(f"{r['year']:>4} {str(r['file_last_national_pick']):>5} {str(r['store_national_MAX']):>5} "
          f"{r['store_national_COUNT']:>5} {r['n_gaps']:>5} {str(r['file_eq_store_max']):>6} {str(r['file_eq_store_count']):>6}")
print(f"\nmismatches vs store MAX: {len(mismatch_max)}  years={[r['year'] for r in mismatch_max]}")
print(f"years with gaps (MAX>COUNT): {[r['year'] for r in rows if r['n_gaps']>0]}")
print("wrote out/job4a_national_last_pick.json")
