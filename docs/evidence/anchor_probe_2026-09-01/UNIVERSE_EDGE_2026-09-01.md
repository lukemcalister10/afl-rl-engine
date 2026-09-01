# The current-model universe has no live tail, and that is the ruling working — not a bug

**Date:** 2026-09-01 · maintainer note. Needs an owner ruling; nothing changed.

## What happened

Adding `universe.test.js` to the landing gate set immediately produced three reds on the freshly
landed board:

```
[FAIL] ...and forward to the newest stored point (bust-exclusion-live-fit-1-9)
[FAIL] an out-of-round column DOES sit at the same after_round as a round point
[FAIL] could not locate the retro/live handover in the current-model universe
```

## What I nearly did, and why it was wrong

The CURRENT-MODEL universe is built as *the retro series + every stored point after the last model
change*:

```js
const cut = lastModelChangeIndex(b);
const live = cut < 0 ? stored : stored.slice(cut + 1);
```

`modelChangeIds()` keys on `mc.between[1]` — the TO point, whose board is the POST-change board. So
`cut` indexes a point that WAS produced under the live model, and I read the `+ 1` as an off-by-one
dropping it. The evidence looked strong: measured on the shipped bundle, that point's `byPoint` values
are the landed board `b005096b` on **804 of 804 players, 0 differing**. It is the live model's answer
by construction.

I changed it to `slice(cut)` and the suite refused, on the owner's own defining property:

```
[FAIL] NO model change is in the current-model universe (1 found)
[FAIL] ...and the handover carries real football, not a copy (0 of 804 moved)
```

Both are right and the change was wrong. `universe.js` states the ruling at the top: *"no model change
is inside the current-model universe, so a span across it is football and nothing else."* Admitting the
change point makes a span across it a model move, which is the one thing the universe exists to
exclude — and the second red proves it empirically: retro-r24 and that point are value-identical on
all 804, so the "handover" would have been a copy of itself. **Reverted.**

## The actual state, and it is coherent

The bust exclusion is the NEWEST stored point and it is a model change. So:

```
stored points        29     last model change at index 28
live tail            stored.slice(29) = []
current-model universe = retro-r14 .. retro-r24, and nothing else
```

Eleven points, every one the live model's answer for its round. That is a correct universe. It simply
has no live tail, because no football has landed since the model moved.

## The ruling needed

`cur[cur.length - 1] === newestStored` asserts the universe reaches forward to the newest stored point.
That holds only while a ROUND has landed after the last model change. It cannot hold in the window
between a model change and the next round, and this is the first time the estate has been in that
window with the test watching.

So the assertion is asserting a temporary state as an invariant. Three ways out, and the choice is the
owner's because it is about his selector:

1. **Say so in the test.** The universe reaches the newest stored point that is not itself a model
   change; when a model change is newest, the universe legitimately ends at the last retro point.
   Nothing in the app changes and the window is simply named.
2. **Let the change point in when it is the newest.** Cheap to write, but it breaks the defining
   property in exactly the window where the property matters most, and the handover check would be
   comparing a point with itself.
3. **Re-price a retro point for the new board.** retro-r24 already IS the new board (0 diffs), so
   there is nothing to re-price — this is the same as option 1 with extra steps.

**Recommendation: option 1.** It is the only one that leaves the ruling intact, and the situation it
names is real and recurring: every model change opens this window until the next round lands.

I have NOT loosened the test. It is red, and it is red for a true reason.
