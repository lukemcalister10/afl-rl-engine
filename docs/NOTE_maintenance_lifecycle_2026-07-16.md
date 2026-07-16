# NOTE — MAINTENANCE, UPKEEP & THE SEASON ROLLOVER · 2026-07-16 · seat 9 (Fable)
### Owner-raised (six questions, register item 218). Answers grounded in the code/runbooks as they
### exist; the two named GAPS are design proposals, not rulings. Shapes the ingestion go-live
### chapter + adds ONE small chapter (the rollover runbook) to the roadmap.

## THE ORGANIZING PRINCIPLE — THE OWNER-INPUT CLASS (proposed, for ratification at go-live)
Five inputs are the OWNER'S DECLARED FACTS about the world: round scores · the LTI register ·
player ownership (locations CSV) · pick ownership (pick workbook) · future positioning (his flex
register). REFRESHING any of them is DATA-REFRESH: local, one deterministic validate-or-halt
command, no Claude seat, no ladder — values move because reality moved. The FULL LADDER remains
reserved for MODEL changes (pricing rules moving). The five SSI guards protect both paths equally.

## STATE PER QUESTION
1. **Self-sufficiency:** the UI is a static file:// app — view forever with zero dependencies.
   Input refreshes = the existing no-LLM flow (HOW_TO_UPDATE_INPUTS.md: edit three files, one
   command, reload). Re-valuation = the engine, plain Python, runs locally via bootstrap.sh.
2. **Scores:** plumbing BUILT + dry-run-proven (engine/rl_after/ingestion/), double-switch OFF,
   write code deliberately absent (GO_LIVE runbook). Go-live adds the store-write under the five
   guards; thereafter weekly = one local command. No agent per week by design.
3. **LTI register:** owner-edited, availability-layer-consumed, Guard-5-pinned. **GAP (named
   go-live requirement): the sanctioned re-pin tool** — validate the register format → re-pin the
   md5 → rebuild — so an owner edit doesn't HALT the next build unmediated.
4. **Trades:** DONE — the v1.2 no-LLM flow covers player + pick ownership end to end. Local.
5. **Future positions:** the flex register CSV; Leg C ships the validate-or-halt ingest; post-
   chapter amendments = edit → re-ingest → rebuild. Owner-input class; local.

## 6 — THE SEASON-ROLLOVER RUNBOOK (proposed chapter; small; schedule AFTER go-live, BEFORE season end)
VERIFIED HARD-CODES: BASE_REF=AGE_REF=2026 module constants; literal `==2026` in the availability
haircuts (rl_model.py:354/368) + `r['year']==2026` season-progress (:676/:810) + a `finally:` reset
(:921). Rolling the year is a DESIGNED EVENT. Five acts, each validate-or-halt, owner-triggered once
per off-season:
  (i) SEAL the completed season's book (the walk-forward matrix becomes history-of-record).
  (ii) ROLL the reference year — after a small hygiene leg converts the ==2026 literals to config
       (pinned in the manifest; byte-identity proof at the old year).
  (iii) INTERIM POSITIONS — between season end and club announcements, the year-0 leg reads the
       FUTURE primary (owner's projected positions). One ruled convention, reversible at (v).
  (iv) DRAFT INTAKE — new players minted (stable afl-player-v1 IDs), priced at V0 off the live
       curve (the G-Y0 identity, machinery already real in value()'s pre-debut branch); drafted
       picks retire into players; next-year picks enter with the future discount rolling.
  (v) ANNOUNCED POSITIONS — the normal locations refresh; present positions land; the future blend
       pushes to +1/2028+.
OPEN CONSIDERATIONS RECORDED: LTI `out_until_<year>` resolution at (ii) · pick-ledger year shift
(2027 picks become current; discounts re-anchor) · evidence semantics automatic once scores are in ·
rehearse the runbook BEFORE it is needed (a dry-run on a copy, guards green).
