#!/usr/bin/env python3
"""PICK-CONVENTION REMEDIATION (ii) 2026-07-11 — RE-DERIVE the last-national-pick chain table
from the DATABASE's own National rows, under the owner data law.

OWNER DATA LAW (2026-07-11): store pick numbers are DATABASE-UNIVERSE ordinals — redrafted/
recycled players are EXCLUDED from the database's draft numbering; the rookie draft attaches
to the END of the national draft ("ND ends pick 54 => RD pick 1 = 55") — both sides counted
in the DATABASE's universe, NOT AFL official numbering. The correction build overrode 2010 to
the real-world "77 selections". Under the owner's law the real-world count is NOT the authority;
the database's own national end is. This re-derivation reverts that override.

BASIS DECISION (stated + reconciled):
  For every year, last_national_pick = the store's own MAX National (ND) pick ordinal — the
  database's ND END, which is exactly what the chaining convention ("ND ends pick N") names,
  and the only collision-free offset (rookie eff = last_nat + slot must sit ABOVE the last
  national ordinal actually present in the store; using the COUNT where count<max would place
  rookie picks BELOW real national players — an inversion).
  - 21 of 23 years are GAPLESS: count == max, so the two bases AGREE (unambiguous).
  - 2010 and 2011 have gaps (max > count): ordinals present in the store but with holes where
    excluded (recycled/redraft/out-of-database) players sat. Under the owner's law those holes
    do not lower the database's ND end. => 2010 = store max 93 (reverts the forbidden 77
    override), 2011 = store max 89 (already the store max in the correction table).

Writes engine/rl_after/national_draft_last_pick.json (data only — the engine already reads it).
"""
import json, collections, hashlib

STORE = 'engine/rl_after/rl_model_data.json'
TABLE = 'engine/rl_after/national_draft_last_pick.json'

def main():
    d = json.load(open(STORE))
    nd = collections.defaultdict(list)
    for p in d:
        if p['type'] == 'ND':
            nd[p['year']].append(p.get('pick'))

    last = {}
    per_year = {}
    for y in sorted(nd):
        picks = sorted(x for x in nd[y] if x is not None)
        cnt, mx = len(picks), max(picks)
        gaps = sorted(set(range(1, mx + 1)) - set(picks))
        dups = [x for x, c in collections.Counter(picks).items() if c > 1]
        last[str(y)] = mx  # OWNER LAW: database ND end = max ordinal present
        if cnt == mx and not gaps and not dups:
            per_year[str(y)] = ("store gapless national sequence 1..%d (count==max==last pick; "
                                "database universe internally consistent). max==count so the "
                                "MAX and COUNT bases agree." % mx)
        else:
            per_year[str(y)] = ("store national ordinals 1..%d with %d gap(s) at %s (count=%d). "
                                "Under the owner data law the gaps are EXCLUDED (recycled/redraft/"
                                "out-of-database) players that never consume numbering; the database's "
                                "ND END is the MAX ordinal present = %d. (The correction build's "
                                "real-world override is NOT the authority under the owner's law.)"
                                % (mx, len(gaps), gaps, cnt, mx))

    table = {
        "_doc": ("AUTHORITATIVE per-year LAST NATIONAL PICK (the database's own national END) — the "
                 "chaining offset for the rookie/pre-season drafts. Owner data law 2026-07-11: store "
                 "pick numbers are DATABASE-UNIVERSE ordinals; redrafted/recycled players are excluded "
                 "from the numbering and never consume it. First rookie pick of year Y = "
                 "last_national_pick[Y] + 1; PSD chains after national, before rookie. last_national_pick "
                 "= the store's own MAX National ordinal for the year (the database's ND end)."),
        "_provenance_summary": ("RE-DERIVED 2026-07-11 (PICK-CONVENTION REMEDIATION (ii)) from the store's "
                 "own National rows, under the owner data law. For every year last_national_pick = the "
                 "store MAX National ordinal. 21/23 years are gapless (count==max, unambiguous). 2010 and "
                 "2011 have gaps (max>count): the gaps are excluded players (never consume numbering) and "
                 "do NOT lower the database's ND end. This REVERTS the correction build's 2010->77 override "
                 "(which used the real-world selection count — NOT the authority under the owner's law): "
                 "2010 = store max 93; 2011 = store max 89. No external/AFL-official numbering is consulted; "
                 "the DATABASE is the authority per the owner's ruling."),
        "convention": ("rookie_effective_pick = last_national_pick[year] + rookie_slot; "
                 "psd_effective_pick = last_national_pick[year] + psd_slot (PSD chains after national, "
                 "before rookie). last_national_pick = database-universe ND end = store MAX National ordinal."),
        "basis": "store MAX National ordinal per year (database ND end); reconciled vs COUNT below.",
        "last_national_pick": {k: last[k] for k in sorted(last, key=int)},
        "reconcile_max_vs_count": {},
        "per_year_provenance": per_year,
        "sources": [
            "engine store rl_model_data.json National (ND) sequences — the DATABASE UNIVERSE (owner data "
            "law 2026-07-11: the database, not AFL official numbering, is the authority).",
            "Owner data law 2026-07-11 (supersedes the audit's Q5 reading): store ordinals are database-"
            "universe with redraft exclusions; real-world selection counts are NOT the authority.",
        ],
    }

    # reconciliation record (max vs count) for transparency
    for y in sorted(nd, key=int) if False else sorted(nd):
        picks = sorted(x for x in nd[y] if x is not None)
        cnt, mx = len(picks), max(picks)
        if cnt != mx:
            table["reconcile_max_vs_count"][str(y)] = {
                "max": mx, "count": cnt, "chosen": mx,
                "why": "gaps = excluded players (owner law); database ND end = MAX; COUNT would invert rookie chaining below real national ordinals."}
    if not table["reconcile_max_vs_count"]:
        table["reconcile_max_vs_count"] = {"_note": "all years gapless: max==count for every year; bases agree."}
    else:
        table["reconcile_max_vs_count"]["_note"] = ("only 2010/2011 differ (max>count); every other year is "
            "gapless (max==count). Chosen basis = MAX (database ND end) for ALL years, uniformly.")

    json.dump(table, open(TABLE, 'w'), indent=1)
    md5 = hashlib.md5(open(TABLE, 'rb').read()).hexdigest()[:8]
    print('chain table RE-DERIVED ->', TABLE, 'md5', md5)
    print('last_national_pick:', table['last_national_pick'])
    print('reconcile (max!=count):', {k: v for k, v in table['reconcile_max_vs_count'].items() if k != '_note'})

if __name__ == '__main__':
    main()
