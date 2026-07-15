# NEGATIVE TEST — orient.sh dies loud when docs/OPEN_ITEMS_REGISTER.md is absent

House law #3 (SILENCE IS A RED): a missing durable-register input must produce a loud FAIL and a
non-zero exit, never a silent omission. The real `docs/OPEN_ITEMS_REGISTER.md` is NEVER touched — the
test runs against a full copy of the checkout with the register removed FROM THE COPY ONLY.

## Method
```
TMP=<scratchpad>/orient_negtest2
cp -a . "$TMP/repo"                       # full checkout incl. .git so rev-parse HEAD (step 1) passes
rm "$TMP/repo/docs/OPEN_ITEMS_REGISTER.md"   # remove from COPY only; real file left untouched
bash "$TMP/repo/tools/seat/orient.sh"; echo "exit code = $?"
```

## Result — PROOF
```
real file untouched? YES
copy has register? NO-removed
exit code = 1
stderr: orient: FAIL — docs/OPEN_ITEMS_REGISTER.md missing (open-items register is the durable freshness input)
last stdout rung reached: -- open-items register header (docs/OPEN_ITEMS_REGISTER.md line 1) --
```

The script reaches the new open-items-register rung, finds the file absent, calls `die`, prints its
`orient: FAIL — …` line to stderr, and exits **non-zero (1)**. Confirmed.
