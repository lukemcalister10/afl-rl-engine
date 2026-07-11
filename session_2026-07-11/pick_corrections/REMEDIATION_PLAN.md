# PLAN — PICK-CONVENTION REMEDIATION (candidate) — 2026-07-11

Branch `claude/pick-convention-remediation-yidlbm`, re-based onto the candidate work (0166ecf) so all kept
(a)/(c)/(f) changes carry forward (owner chose this over continuing PR #59 in place). NOT a bake.

## OWNER DATA LAW (ground truth, 2026-07-11) — supersedes the audit's Q5 real-world reading
Store pick numbers are DATABASE-UNIVERSE ordinals, not AFL official numbering. "Players previously listed
are excluded when redrafted, and only their initial entry is recorded." Redrafts never consume numbering;
store ordinals deliberately differ from real-world numbers. The rookie draft chains onto the database's ND
end. The correction build's 190 "renumber to real-world" moves violated this and must be REVERTED.

## THE FOUR ITEMS
- **(i) REVERT the 190 rookie renumbers** to the original store ordinals — byte-restore `pick` from the
  pre-correction store (a2fbc9a0/main), drop the renumber's `_pick_source` stamp; treacy 7→5. KEEP the 325
  _draft fills, the 8 PSD splits, the (a) band-pool fix, and (f) re-denomination intact.
- **(ii) RE-DERIVE the last-national-pick chain table** from the database's own National rows (basis = the
  store MAX National ordinal = the database's ND end). 21/23 years gapless (max==count); 2010/2011 differ —
  choose MAX (2010 77→93 reverts the forbidden real-world override; 2011 stays 89). Re-judge the 42 flagged
  2010–11 tail rows against the database universe (expect: clear as intentional). Update the one misleading
  engine comment (comment-only; no logic).
- **(iii) CLEAR the 495 "unverifiable" rookie flags + the 42 tail flags** (never suspect under the
  convention); record the owner law in the pick-semantics schema note (canonical exclusion sentence verbatim);
  update the drafted SSI chaining-contract wording (in the RETURN, for the supervisor's pen).
- **(iv) REGENERATE everything derived** (board + walk-forward book + re-seal), full gate suite; re-measure
  the currency factor + delta; regenerate the EYEBALL LIST; expected reds exactly {A2, A3, A12}; report any
  G-FLOOR dips (≤5-SCAR dispensation governs; any dip beyond = STOP).

## FENCE
IN: the four items on the candidate branch. OUT: no other store fields; no engine changes beyond the chain
table + its comment; no doc-pack/constraint edits; no bake/tag/main merge; no force-pushes.

## VERIFICATION
Base ls-remote asserted: tag v2.7 == 8f8c00b, main == a6a8aa9c, candidate == 0166ecf. Boot-store candidate
md5 1a969d95 confirmed. Every revert asserted against the byte source; every derived artifact regenerated
and gate-checked; factor re-measured, not assumed.
