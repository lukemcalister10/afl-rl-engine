# P5 — THE BOOK: REBUILT, OR RE-STAMPED?

## One word: **NEITHER.**

The freeze commit `f14710d` **did not touch the book at all** — it neither rebuilt it nor re-stamped its
seal. And that is the *safe* outcome G-BOOK protects: **it did not re-stamp a book it did not rebuild.**

## Show it

1. **The freeze commit touches no book artifact.** `git diff --name-only ed13177 f14710d`:
   ```
   SHIP_GATES.md  boot_guard.py  bootstrap.sh  data/expected_boot.json
   data/q97m.pkl  engine/rl_after/_merged_recover.py  engine/rl_after/wire_redesign.py  refit_q97m.py
   ```
   No `book_stable_seal.json`, no `*WALKFORWARD_book*.xlsx`, no `s4_matrix*`. The book was left untouched.

2. **The seal still carries the PRE-FREEZE head.** `data/book_stable_seal.json`:
   ```
   head_md5:      2030e5df   <-- the engine head BEFORE the freeze (freeze moved it to 2334f570)
   store_md5:     340a7a32
   stable_sha256: d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f   n_players: 2649
   sealed_by:     "CONFIG-MANIFEST v2.9 COMPLETION re-seal 2026-07-14 (engine 2030e5df; ...)"  <-- the #74 job, not the freeze
   ```
   Nobody advanced `head_md5` to `2334f570`. So there was **no re-stamp** — the guard against the exact
   G-BOOK sin ("re-stamping a book you did not rebuild") held.

3. **The book content is INVARIANT to the freeze — measured, not assumed.** I rebuilt the walk-forward book
   on the freeze engine `2334f570` (`s4_matrix_M1v7.py`, gate mode) and hashed the B3 stable seal:
   ```
   regenerated on 2334f570 / store 340a7a32 / config c2d233ae:
     stable_sha256 = d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f   n=2649
     sealed baseline (head 2030e5df)   = d371a27c...871bc44f   n=2649      MATCH: True
   ```
   Because the freeze only swapped the q97m runtime-fit for a load of the identical pickle (`cfdc7321` on
   this box), the book content does not move: regenerating on `2334f570` reproduces the `2030e5df` seal
   byte-for-byte. So on this box **B3 PASSes by content** (`_cur_sha == sealed stable_sha256`), independent
   of the stale head field.

## The residual caveat (ties to P3)
"Invariant to the freeze" is true only *at fixed environment*. P3 measures the book across CPU kernels: on
an SSE (Prescott) BLAS kernel the board moves (`3dc19fbb`→`935c2c29`), and the walk-forward book is built by
the same `_iso_dec` machinery — see `P3_crossenv/isolation.txt` for the SSE book seal. The freeze did not
make the book environment-invariant; it removed one mover (q97m), not the residual 72 (P2).

## What is owed (flagged, NOT done — outside this job's fence)
The seal's `head_md5` should be advanced `2030e5df`→`2334f570` at the next bake re-seal (an owner-only bake
action; `data/book_stable_seal.json` is not in my fence). Until then B3 reports **PASS by content** on this
box but would read **DIFFERS-BY-DESIGN** on any environment where the book content moves.
