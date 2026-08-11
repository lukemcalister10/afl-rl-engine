"""ORDER 20 — THE `daniel-butler` FIX: ARM MEMBERSHIP IS THE ENGINE'S, NOT THE SLIDE'S.

Run as a build mutator:  python3 fix_matrix_membership.py <TREEDIR>
(it patches the STAGED copy of `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py`; the checked-in
emitter — filed evidence of a landed act — is never written).

THE RECORD, AND IT SETTLES IT (no ruling needed, and none is asked for):

    store `engine/rl_after/rl_model_data.json`, key `daniel-butler`:
        player 'Daniel Butler' · type 'ND' · year 2014 · pick 65 · _pickless False
        draft_stream 'ND' · stream_pick 65 · stream_year 2014

    the owner's ruling, in the engine's own words (rl_model.py:264-268, RULEBOOK v2.1 law 4):
        "the national curve covers picks 1-64. A national selection at 65 or deeper is NOT on the
         curve — it enters the pool with every other pool entrant."
    so the engine classifies him:  _eff 65 · _pool True · is_pool True · _teaches_curve False.

    the matrix says otherwise ONLY because of the Quinton-Boyd force-majeure slide: paddy-mccartin is the
    excluded 2014 pick-1 row, so every 2014 ND pick > 1 slides up one, butler's 65 becomes 64, and
    `slid_membership` (emit_matrix_338.py:101-110) re-derives `is_pool=False` from the SLID pick, which
    `teaches_curve` (:243) then consumes.

THE EMITTER ALREADY CONTRADICTS ITSELF ON THIS, IN ITS OWN HEADER (:49-52):

    "the Q-B slide is a fit-population device for the curve, not an assertion that anyone was drafted a
     slot earlier"

It applies that principle to `_min_tenure` (which bands on `MA.effpk`, the engine's pick, and says so),
and then breaks it for ARM MEMBERSHIP one screen later. A device that may not assert a different draft
position also may not move a player from one ARM to the other — the arm IS the draft position, under the
ruling. The emitter's own `crossers` line (:298) has been printing the consequence all along:
`boundary crossers (pool -> ND fit via the slide): ['Daniel Butler']` — 1 row, every emit.

THE FIX: `is_pool` and `teaches_curve` are quoted from the ENGINE (the fields the emitter ALREADY
records at :240 as `is_pool_engine` / `teaches_curve_engine`). The slid pick keeps its job — it is still
computed, still published as `pick_slid`, and still what the curve's fit population uses for ATTRIBUTION
inside 1..64. It simply stops deciding which side of the wall a player lives on.

VERDICT: daniel-butler is a POOL row (division ND65+). Not a blocker. The record settles it.
"""
import sys, pathlib

TREE = sys.argv[1]
f = pathlib.Path(TREE) / 'docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py'
src = f.read_text()

OLD = """        is_pool=pool_slid,
        teaches_curve=bool(p.get('type') == 'ND' and not pool_slid and MA._in_pvc(p)),"""
NEW = """        is_pool=bool(MA.is_pool(p)),                       # ORDER 20: ARM MEMBERSHIP IS THE ENGINE'S.
        teaches_curve=bool(MA._teaches_curve(p)),          # The Q-B slide is a fit-population device for
        # the curve (this file's own header, :49-52) and may not move a player from one ARM to the other.
        # `pick_slid` is unchanged and still published; only the membership fields stop reading it.
        is_pool_slid=pool_slid,                            # the old reading, KEPT and disclosed, never consumed
        teaches_curve_slid=bool(p.get('type') == 'ND' and not pool_slid and MA._in_pvc(p)),"""

assert src.count(OLD) == 1, "membership anchor not unique/found (%d)" % src.count(OLD)
f.write_text(src.replace(OLD, NEW))
print("  PATCHED emit_matrix_338.py: is_pool/teaches_curve now quote the ENGINE; the slid reading is kept "
      "as is_pool_slid/teaches_curve_slid, disclosed and unconsumed.")
