# #326 second rehearsal — HALT-and-ask

Three places where the record and the code do not agree. None of them stopped the work; all three are
above an implementer's pay grade, so they are recorded here rather than improvised around.

---

## HALT 1 — the floor's scope reaches pool players who DO have careers, and the attribution sentence says it should not

**The two sentences that disagree.** Addendum 6 item 3 rules the mechanism: the floor "fades on the ND
clock schedule, applying from the first year after entry — identical to national draftees, which is the
owner's instruction. No new fade is invented." Addendum 6's closing attribution restatement says: "pool
veterans with real careers move only through the ruck cap where enumerated."

Both cannot hold. The national floor is scoped by the YEAR CLOCK, not by record thinness: a national
draftee fifteen years in system still gets `0.05 x his year-zero value` as a lower bound, and that is
what the FLOOR-SAVES table has always listed. Inheriting it unchanged — which is what the ruling
requires — necessarily extends the same lower bound to pool players fifteen years in system.

**Measured on this build** (`gate6_attribution_classified.txt`): of 123 rows whose 2026 price moved,
26 moved through the floor and have 20 or more senior games. The longest careers among them:

| player | division | senior games | yrs in system | v before | v after |
|---|---|---|---|---|---|
| Dane Rampe | RD:SD | 284 | 14 | 1 | 12 |
| Harry Cunningham | PDA | 230 | 15 | 0 | 10 |
| Jed Bews | ND65+ | 175 | 15 | 33 | 10 |
| Daniel Butler | ND65+ | 159 | 12 | 17 | 10 |
| Mark Blicavs | UNR | 310 | 15 | 3 | 5 |

Their prices are tiny either way — these are players whose FORWARD value has run out, which is what the
floor exists to put a number under. Their prices move because the floor's basis moved, not because a
career was overwritten: every one of them is at the floor, and the floor is 5% of an entry level.

**What was implemented:** the ruled mechanism, unchanged — the ND floor inherited verbatim, scope widened
to pool entrants. The alternative (restricting the pool floor to thin records) would be inventing a new
fade, which the same addendum forbids in the same sentence.

**The ask:** confirm that the attribution sentence is the loose one and the mechanism ruling governs — or,
if the intent really was that established pool careers stay still, that is a NEW rule (a record test on
top of the year clock) and needs to be worded and audited as one.

---

## HALT 2 — the committed attribution instrument cannot attribute this act

`docs/evidence/landing_306_648fai/attribute_movers.py` holds `store`, `engine` and `band` constant by
construction: its completeness gate HALTs if any of the three moved, because its named cause set is
"curve + surface" and a moved engine would make a mover's cause unnameable.

This act moves the engine head by ruling (addendum 5 item 4: `_merged_recover.py` is in scope). So the
instrument, run unmodified with TRUTHFUL identities, halts — correctly (`gate6_attribution_instrument.txt`):

```
  engine   base 15525b03  cand 9f258a3b  DIFFERS -> UNNAMED CAUSE
  HALT — ['engine'] missing-or-moved …
```

Passing it `engine=15525b03` on both sides would make it print a clean attribution, and would be a lie.
It was not done.

**What was done instead:** the attribution is made against the engine's OWN pool classification
(`classify_movers.py`, `gate6_attribution_classified.txt`) — a stricter test than the instrument's, since
it asks the engine which rows are pool entrants rather than inferring a channel from a pick number. Result:
177 rows differ in any field, 0 of them non-pool. The ruck-cap route is enumerated separately by paired
build (`gate6_ruckcap_route_enumeration.txt`).

**The ask:** the instrument needs an ENGINE-DECLARED mode (name the engine change as a cause and keep the
gate honest) before any act that touches the engine head can use it. That is a change to a committed
instrument and was left alone here.

---

## HALT 3 — `ship_gates_check.py` cannot run on this tree at all, for a reason that pre-dates #326

Line 64 hard-sets `RL_GAMMA='0.85'`; the pinned manifest `data/model_config.json` carries `RL_GAMMA=1.0`;
line 69 then enforces the manifest in gate mode, which rejects the divergence and halts before any gate
runs. Both values are at the UNMODIFIED tip — proved by `git show HEAD:` in `gate9_B5_rescope.txt` — so
this is not something #326 did.

The B5 re-scope was therefore written and reviewed but could not be exercised through its own harness. It
was exercised directly instead (`b5_rescope_probe.py`, same scope test, same two bars, same basis):
scope 561 national-draft + 225 pool rows, 104 saves (42 of them pool), `lowered = 0`, `moved out of
scope = 0`, verdict FEATURE.

**The ask:** the γ propagation act left `ship_gates_check.py` behind. Fixing it is a one-line re-pin in
someone else's change, not this one.

---

## Two smaller notes, not halts

* **`ui/release_pick_curve.json`'s `_doc`** narrates "file md5 f1cf148e…" for the curve artifact, which
  matched neither the pre-change file md5 (`b7389fe4`) nor the new one (`988135ef`). Stale narrative
  authored by #328; the machine-read field `pick_curve_file_md5` was correct and was re-pinned. Left as
  found — correcting another act's prose is not this act's business.
* **Division counts have moved since the audits.** The store now yields RD:KPD 72 / RD:MID 176 (the audits
  recorded 73 / 177) and ND65+ 122 (the audits recorded 121). Nothing is hardcoded — every count in this
  rehearsal is re-derived at build time, which is exactly why the drift is visible rather than baked in.
