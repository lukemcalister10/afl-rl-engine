#!/usr/bin/env python3
"""OUT-OF-ROUND HISTORY COLUMN for THE D8 ADOPTION (2026-08-20).

The standing owner rule (out_of_round_column.py, owner word 2026-07-28): "whenever the board moves
OUTSIDE a round, write a column at that point." THE D8 ADOPTION moved the live board a05fe951 ->
5ea978f7 at round 22 with no round applied. The column is written here so the boundary the lineage
entry names (applies_to.boundary = ["22","the-d8-adoption-20-8"]) exists in the three histories and the
Movers dropdown can name its endpoints honestly.

WRITER OF RECORD: engine/rl_after/ingestion/out_of_round_column.add_column — the same call
docs/evidence/landing_tail_2026-08-20/register_landing_column.py makes, in the same per-act-script
shape. No valuation: this reads the finished adopted board and writes JSON. It computes no value, tunes
no parameter, and touches neither the store nor the engine. add_column is append-only and idempotent:
re-registering the same id with DIFFERENT values raises rather than overwriting.
"""
import hashlib, json, os, sys
COLUMN_ID="the-d8-adoption-20-8"
LABEL="20/8 D8 ADOPTION — ceiling-only dial shipped default-on"
AFTER_ROUND=22
BOARD_MD5="5ea978f7b6a073abb2012f10cccbc3e3"
def main():
    root=os.path.abspath(sys.argv[1]); dry="--dry-run" in sys.argv
    sys.path.insert(0,os.path.join(root,"engine","rl_after","ingestion"))
    import out_of_round_column as OOC
    bp=os.path.join(root,"data","rl_build","rl_app_data.json")
    raw=open(bp,"rb").read(); got=hashlib.md5(raw).hexdigest()
    if got!=BOARD_MD5: raise SystemExit("HALT: board md5 %s != expected %s"%(got,BOARD_MD5))
    board=json.loads(raw)
    ev=OOC.add_column(root,column_id=COLUMN_ID,label=LABEL,after_round=AFTER_ROUND,
                      board=board,board_md5=BOARD_MD5,dry_run=dry)
    print(json.dumps(ev,indent=2,sort_keys=True))
if __name__=="__main__": main()
