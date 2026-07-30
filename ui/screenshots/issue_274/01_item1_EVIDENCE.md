# #274 item 1 — ERA SUCCESSION: measured evidence

Measured 2026-07-30 against main tip `f1557b2`. BEFORE = a clean worktree at `f1557b2`; AFTER = this branch.

## Why there is no before/after screenshot PAIR for the flag itself

`owner_approved_record` is a provenance field. Nothing in the UI renders it, and #271 A22 said so
explicitly when it accepted the red: "No value, board, ingestion, or display behaviour is affected."
So item 1's acceptance is carried by the two validators, not by pixels, and the honest evidence for the
flag is the measured JSON below rather than an image. The one screenshot committed here
(`01_item1_card_history_two_model_changes.png`) shows the surface that IS visible: the player-card
history table carrying nine points and both out-of-round rows tagged "model change".

A before/after pair WAS captured first and came out **pixel-identical** (byte-for-byte, 209,950 bytes
each), because the corrected text lives in a `title` attribute that headless capture does not render.
Shipping that pair as "before/after" would have been a false success signal, so it was dropped and this
note records the measurement instead.

## The boundary flag — the acceptance criterion

BEFORE (at `f1557b2`) — the 30/7 boundary unapproved, ruling id null. This is #271 A22's declared
known-false flag:

```json
[
 {
  "between": [
   "19",
   "post-r19-redesign-1"
  ],
  "label": "Post R19 Redesign 1",
  "to_board": "fa172ac1c90ab84e5044d3e9907c5819",
  "owner_approved_record": true,
  "owner_ruling_id": [
   "ITEM_408_items_6_7_option_A",
   "ITEM_411_D1_restatement_v467"
  ]
 },
 {
  "between": [
   "20",
   "rederivation-30-7"
  ],
  "label": "30/7 rederivation",
  "to_board": "f2df6e0a2902f48e1df36f35493ba8c1",
  "owner_approved_record": false,
  "owner_ruling_id": null
 }
]
```

AFTER — both boundaries owner-approved, each naming its own ruling:

```json
[
 {
  "between": [
   "19",
   "post-r19-redesign-1"
  ],
  "label": "Post R19 Redesign 1",
  "to_board": "fa172ac1c90ab84e5044d3e9907c5819",
  "owner_approved_record": true,
  "owner_ruling_id": [
   "ITEM_408_items_6_7_option_A",
   "ITEM_411_D1_restatement_v467"
  ]
 },
 {
  "between": [
   "20",
   "rederivation-30-7"
  ],
  "label": "30/7 rederivation",
  "to_board": "f2df6e0a2902f48e1df36f35493ba8c1",
  "owner_approved_record": true,
  "owner_ruling_id": [
   "ITEM_271_Addendum_17"
  ]
 }
]
```

## The card tooltip — a real display defect found while doing item 1

The tooltip text was one hard-coded sentence naming the ITEM 411 restructure, written when that was the
only out-of-round column. With two columns it told the owner that the 30/7 column was the ITEM 411
restructure — wrong, on a live surface. Measured strings, both rows of the card history table:

BEFORE (at `f1557b2`) — both rows claim to be the same change:

1. `A model change, not a week of football: the ITEM 411 restructure. Value and rank move here because the model changed, not because anyone played.`
2. `A model change, not a week of football: the ITEM 411 restructure. Value and rank move here because the model changed, not because anyone played.`

AFTER — each row names the change it actually is, and its owner ruling:

1. `A model change, not a week of football: Post R19 Redesign 1. Value and rank move here because the model changed, not because anyone played. This change is on the record as owner-approved (ITEM_408_items_6_7_option_A, ITEM_411_D1_restatement_v467).`
2. `A model change, not a week of football: 30/7 rederivation. Value and rank move here because the model changed, not because anyone played. This change is on the record as owner-approved (ITEM_271_Addendum_17).`

The shipped `ui/index.html` was loaded from `file://` with no server for every capture above, with
**zero page errors** reported in each run.
