# Controlled five-round catch-up proof — R14 → R15 → R16 → R17 → R18 → R19 (gate OFF, scratch)

Owner's genuine R15-R19 files, applied on a **disposable copy of the accepted Round-14 state**. Gate armed in-process against the scratch only; the real store / RC / production UI are byte-untouched. One consolidated preflight + approval; every round is its own sequential staged transaction.

## RESULT: **ALL PASS**  (525.2s)

| proof | result |
|---|---|
| gate OFF: real-store apply refused | ✅ |
| A · preflight (encoding, counts, listed-zero, overrides, halt conditions) | ✅ |
| B · participation (listed=+1 game, R19 zero legit, absent unchanged) | ✅ |
| C · identity by stable key (Callum Brown, the two Bailey Williams) | ✅ |
| D · sequential per-round transactions (store/board/hashes/ledger/txn/3 histories/movers) | ✅ |
| E · restart/resume + duplicate-execution refusal | ✅ |
| F · no production / RC files touched | ✅ |

### Preflight (consolidated)
| round | encoding | listed=played | listed-zero | absent/DNP | file sha256 |
|---|---|---|---|---|---|
| R15 | cp1252 | 318 | 0 | — | `20d138b35237` |
| R16 | cp1252 | 319 | 0 | — | `c4d5b3cf5e1f` |
| R17 | cp1252 | 410 | 0 | — | `11797f6e33c1` |
| R18 | utf-8 | 406 | 0 | — | `8d0b8ae0e9f8` |
| R19 | utf-8 | 405 | 1 | — | `463fbb451c24` |

### Per-round store / board / history hashes (the sequential chain)
| round | players | store | board | ledger | value-hist | rank-hist | pos-rank-hist | movers→UI |
|---|---|---|---|---|---|---|---|---|
| R15 | 318 | `968de0c7->692d6302` | `270a2c5f->10708265` | 318 | `1ec5b07f048f` | `9bbee088c49d` | `1c3ff3a3241b` | 804 |
| R16 | 319 | `692d6302->0b951852` | `10708265->9cadb4a3` | 637 | `42bbc5b34eb2` | `ff3db990fa4e` | `13af85413d72` | 804 |
| R17 | 410 | `0b951852->c312eb5b` | `9cadb4a3->674b3c3a` | 1047 | `d526cbad57a4` | `fc76e9e40e11` | `ea4697945c73` | 804 |
| R18 | 406 | `c312eb5b->64795076` | `674b3c3a->4377574d` | 1453 | `25629905cf85` | `8d02a55e5d5b` | `a353b855b320` | 804 |
| R19 | 405 | `64795076->f37d9716` | `4377574d->d3ae2462` | 1858 | `d69c308620c9` | `168c0960129d` | `9cdc15b8cc99` | 804 |

Final histories carry rounds {'value': [14, 15, 16, 17, 18, 19], 'rank': [14, 15, 16, 17, 18, 19], 'pos_rank': [14, 15, 16, 17, 18, 19]} for value, overall-rank and positional-rank.

### Participation (owner ruling)
| stable key | baseline (games, avg) | after (games, avg) | rounds listed | games ✓ | avg ✓ |
|---|---|---|---|---|---|
| `callum-brown-ire` | [8, 41.4] | [13, 56.09] | [15, 16, 17, 18, 19] | ✅ | ✅ |
| `jordan-croft` | [9, 43.2] | [13, 38.82] | [15, 17, 18, 19] | ✅ | ✅ |
| `bailey-williams-wb` | [10, 84.1] | [12, 86.08] | [18, 19] | ✅ | ✅ |
| `bailey-williams-wc` | [9, 93.9] | [13, 90.62] | [16, 17, 18, 19] | ✅ | ✅ |

> Jordan Croft R19 = 0 is a legitimate played zero (+1 game, +0 to the numerator); absent R16 adds no game. The two Bailey Williams resolve by stable key and never collapse.
> Crash-mid-commit detection + byte-identical recovery is proven by the shared staged transaction machinery (../weekly_updater_hardening/, ../live_scoring_two_round/).
