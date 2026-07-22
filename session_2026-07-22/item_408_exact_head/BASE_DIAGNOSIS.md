# ITEM 408 exact-head base diagnosis

- Head SHA: `a0df29c6ebf911a31cb517294786593c5000c0f6`
- Event: `push`
- Evidence lane: exact branch head; PR synthetic merge lane excluded

## CI Guards

- Conclusion: **failure**
- Run: `29930019510`

### Job: guards

- Conclusion: `failure`
- Failed steps:
  - `9` Guards 1/2/3/5 + F1/F2 parity (one_source_selftest.py): `failure`

Failure signals:

```text
LOG DOWNLOAD ERROR: <HTTPError 401: 'Server failed to authenticate the request. Please refer to the information in the www-authenticate header.'>
```

## FV Provenance

- Conclusion: **failure**
- Run: `29930019626`

### Job: fv-provenance

- Conclusion: `failure`
- Failed steps:
  - `9` FV provenance red/green suite (strict board 06d8af60 + fail-closed red paths): `failure`

Failure signals:

```text
LOG DOWNLOAD ERROR: <HTTPError 401: 'Server failed to authenticate the request. Please refer to the information in the www-authenticate header.'>
```

## Final Integration

- Conclusion: **failure**
- Run: `29930019442`

### Job: final-integration

- Conclusion: `failure`
- Failed steps:
  - `11` Season-state — derivation, wiring, behaviour, stale rejection + FENCED reads halt (req 1/2/4/5/7): `failure`

Failure signals:

```text
LOG DOWNLOAD ERROR: <HTTPError 401: 'Server failed to authenticate the request. Please refer to the information in the www-authenticate header.'>
```

## Live Scoring Updater

- Conclusion: **failure**
- Run: `29930019353`

### Job: live-scoring

- Conclusion: `failure`
- Failed steps:
  - `12` Sequential two-round proof (R15 -> R16, history integrity, restart, UI, no-prod-touch): `failure`

Failure signals:

```text
LOG DOWNLOAD ERROR: <HTTPError 401: 'Server failed to authenticate the request. Please refer to the information in the www-authenticate header.'>
```
