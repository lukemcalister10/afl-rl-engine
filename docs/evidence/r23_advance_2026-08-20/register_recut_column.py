#!/usr/bin/env python3
"""OUT-OF-ROUND HISTORY COLUMN for THE INJURY-SHEET RE-CUT (2026-08-20).

The standing owner rule (out_of_round_column.py, owner word 2026-07-28): "whenever the board moves
OUTSIDE a round, write a column at that point." The re-cut moved the live board 5ea978f7 -> 1d5c9f7a
at round 22 with no round applied, so a column is owed.

IT IS ALSO WHAT RULE M0 REQUIRES OF THE R23 MOVERS. round_finalize builds the round-23 report against
MV.previous_point(repo, 23) — the stored point IMMEDIATELY BEFORE round 23. Without this column that
point is an earlier out-of-round board and the round-23 movers would silently report the re-cut (and
the D8 adoption) as round 23's own work. M0: "every diff/mover baseline must share as_of_round with
the candidate." This column IS that baseline, B0, at round 22.

THE COLUMN ID IS CHOSEN, NOT ARBITRARY — AND THE CHOICE IS DISCLOSED. out_of_round_column._register
sorts columns by (after_round, id), i.e. ALPHABETICALLY within a round, not chronologically. The four
existing round-22 columns therefore sit as dob-courier-10-8 < g1-never-rises-10-8 <
the-d8-adoption-20-8 < the-landing-20-8 — which puts THE LANDING (a05fe951, the RETIRED pre-D8 board)
last, after the D8 adoption that superseded it. That ordering defect is PRE-EXISTING and is not this
seat's to repair (fixing the sort is an engine change, out of scope for a round advance). Its
consequence, however, IS this seat's: the point immediately before round 23 must be B0. The id
`the-sheet-recut-20-8` sorts after all four, and the script ASSERTS that outcome by calling
round_movers.previous_point after the write rather than trusting the alphabet.

WRITER OF RECORD: engine/rl_after/ingestion/out_of_round_column.add_column — the same call
docs/evidence/d8_adoption_2026-08-20/register_d8_column.py and the landing tail's
register_landing_column.py make. No valuation: this reads a finished board and writes JSON. It
computes no value, tunes no parameter, and touches neither the store nor the engine. add_column is
append-only and idempotent: re-registering the same id with DIFFERENT values raises.
"""
import hashlib, json, os, sys
COLUMN_ID="the-sheet-recut-20-8"
LABEL="20/8 INJURY-SHEET RE-CUT — armstrong + clarke de-listed"
AFTER_ROUND=22
BOARD_MD5="1d5c9f7a3898c7cc62d0e91787ee2606"
def main():
    root=os.path.abspath(sys.argv[1]); dry="--dry-run" in sys.argv
    sys.path.insert(0,os.path.join(root,"engine","rl_after","ingestion"))
    import out_of_round_column as OOC
    import round_movers as MV
    bp=os.path.join(root,"data","rl_build","rl_app_data.json")
    raw=open(bp,"rb").read(); got=hashlib.md5(raw).hexdigest()
    if got!=BOARD_MD5: raise SystemExit("HALT: board md5 %s != expected %s"%(got,BOARD_MD5))
    board=json.loads(raw)
    ev=OOC.add_column(root,column_id=COLUMN_ID,label=LABEL,after_round=AFTER_ROUND,
                      board=board,board_md5=BOARD_MD5,dry_run=dry)
    print(json.dumps(ev,indent=2,sort_keys=True))
    vh=json.load(open(os.path.join(root,"engine","rl_after","ingestion","value_history.json")))
    pts=OOC.selectable_points(vh)
    print("\nselectable points, in display order:")
    for p in pts: print("   %-24s %-12s after_round=%s board=%s"%(p['id'],p['kind'],p['after_round'],p['board']))
    last=pts[-1]
    print("\nLAST STORED POINT (the R23 movers baseline, rule M0): %s  board=%s"%(last['id'],last['board']))
    if not dry:
        if last['id']!=COLUMN_ID:
            raise SystemExit("HALT: the last stored point is %r, not this column. The round-23 movers "
                             "would be measured from the wrong board."%last['id'])
        if last['board']!=BOARD_MD5:
            raise SystemExit("HALT: the last stored point names board %s, not B0"%last['board'])
        print("ASSERTED: the point immediately before round 23 is B0 %s at as_of_round 22."%BOARD_MD5)
if __name__=="__main__": main()
