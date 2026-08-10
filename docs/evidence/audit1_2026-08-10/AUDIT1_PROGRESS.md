# Audit 1 progress (year-0 surface, origin/landing/334-stage-b @ e8c772c)

- 2026-08-10 start: audit seat opened. Reading brief at issue #334 comment 5235093657.
- 2026-08-10 step 1: got the two matrices from branch origin/landing/334-stage-b. md5 of the stage-4 amend-1 matrix is b564b12e. Correct file.
- 2026-08-10 step 2b: checked the statistic against the act's own stage-6 code. Same formula, same year lookup. No difference in any of the 2198 records.
- 2026-08-10 step 2: instrument reproduced. ND picks 1-64, classes 2004-2022, n=1197. Aggregate vpath[3]/v0 = 1.4321 (target 1.4327). Aggregate F0 = 1.0001 (target 1.0006). The measure is correct. Cells can now be trusted.
- 2026-08-10 step 3: population built. All entrants, classes 2004-2022, n=2198 (ND 1310, pool routes 888). Busts kept in at zero.
- 2026-08-10 step 4: headline levels measured. Whole book F0 = 0.939. ND alone 0.991 (honest). Pool routes alone 0.725 - clearly over-priced, CI does not touch 1.
- 2026-08-10 step 5: position x pick band grid done (36 cells). Two ND cells clear 1: KPD picks 41-64 is under-priced, KPD picks 65+ is over-priced.
- 2026-08-10 step 6: pool route x age grid done. The big miss is draft age. Pool entrants aged 18 or less deliver 0.56 of price. Pool entrants aged 21+ deliver 2.07 of price. Both CIs are clear of 1.
- 2026-08-10 step 7: KPD measured. I reproduced the act's filed year-1 numbers exactly from its own file (KPD 0.6680, n=35). On the same 35 players the YEAR-0 price is not the problem. Year 0 reads 1.574 against a leg par of 1.671, that is 0.94 of par. Year 1 reads 0.668 against 1.136, that is 0.59 of par. The KPD error is made between year 0 and year 1, not at year 0.
- 2026-08-10 step 8: band scan done. I rebuilt the year-0 surface by hand from the branch's own frozen file and it matches the matrix to the decimal. The surface has 446 inverted steps across position, age and pick. On real players in the matrix there are 29 inverted adjacent pairs, named.
- 2026-08-10 step 9: Grlj/Cumming taken apart exactly. The pick curve falls 1507 to 1503, which is minus 5.5 points. The position/age lens rises 1.3784 to 1.4096, which is plus 46.9 points. Net plus 41.4 points. There is NO band step in the number. The inversions are mostly INSIDE bands, not at band seams. 11 of the 12 inverted pick seams are inside a band.
- 2026-08-10 step 10: found a second year-0 defect. Any national draftee with no date of birth is priced as if he is 18, the most expensive age. There are 175 such players in picks 1-64. As a group the MIDs among them deliver 0.68 of price and the KPDs 0.44.
- 2026-08-10 step 11: compared the branch surface with main. Same defect, same places. Main has 437 inverted steps, the branch has 446. The branch neither causes nor fixes it.
- 2026-08-10 step 12: era check done. Grouping by draft class does not change any verdict except one. The KPD picks 41-64 cell stops clearing 1 once class era is held constant. Marked marginal.
- 2026-08-10 step 13: audit finished. Writing the report.
