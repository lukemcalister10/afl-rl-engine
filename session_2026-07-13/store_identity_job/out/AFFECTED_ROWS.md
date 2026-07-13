# ITEM 20 — THE COMPLETE AFFECTED-ROW LIST (board 81e48293 → 3dc19fbb)

Store b0c39d78 → 340a7a32. Engine ev()/config/band UNCHANGED. Two kinds of change:
a VALUE move (bramble's games feed ev) and DISPLAY corrections (club field repointed to the
current AFL club). Eligibility changes are store-only (not shipped on the board) — see
ELIGIBILITY_TABLE.md.

## A. VALUE MOVERS (`v`) — the COMPLETE list

| key | before | after | Δ |
|---|---:|---:|---:|
| lachlan-bramble | 92 | 93 | +1 |

**1 value mover(s) total.** Sum v 696247 → 696248 (+1). The feared collateral ripple did NOT materialise — bramble's 2024 peak season is unchanged, so
the load-time calibration/cohort statistics did not move any other row. Bramble's own +1 is his
current-season (2026) level read shifting on 15→14 games @ 62.4→62.3.

## B. CLUB-DISPLAY CORRECTIONS (display-only; `club` repointed draft → current AFL club)

These are NOT value moves — the board now shows each player's CURRENT AFL club (afl_club) instead
of his DRAFT club (_draft_club). 172 rows change club, 10 formerly-blank rows fill.

### B1. The ten formerly-blank rows filled (register item 33 red-path test)

| key | now displays |
|---|---|
| ben-murphy | Brisbane |
| cillian-bourke | Essendon |
| dayne-zorko | Brisbane |
| indy-cotton | Adelaide |
| jamie-elliott | Collingwood |
| kobe-mcdonald | St Kilda |
| oscar-berry | Melbourne |
| patrick-carr | Richmond |
| scott-pendlebury | Collingwood |
| wil-parker | Collingwood |

### B2. Draft-club → current-club corrections (172 rows)

| key | was (draft club) | now (current AFL club) |
|---|---|---|
| adam-cerra | Fremantle | Carlton |
| adam-saad | Gold Coast | Carlton |
| adam-treloar | GWS | Western Bulldogs |
| aidan-corr | GWS | North Melbourne |
| alex-neal-bullen | Melbourne | Adelaide |
| aliir-aliir | Sydney | Port Adelaide |
| bailey-smith | Western Bulldogs | Geelong |
| ben-ainsworth | Gold Coast | Carlton |
| ben-keays | Brisbane | Adelaide |
| ben-long | St Kilda | Gold Coast |
| ben-mckay | North Melbourne | Essendon |
| billy-frampton | Port Adelaide | Collingwood |
| blake-acres | St Kilda | Carlton |
| bobby-hill | GWS | Collingwood |
| bradley-hill | Hawthorn | St Kilda |
| brayden-fiorini | Gold Coast | Essendon |
| brodie-grundy | Collingwood | Sydney |
| brody-mihocek | Collingwood | Melbourne |
| caleb-daniel | Western Bulldogs | North Melbourne |
| callum-ah-chee | Gold Coast | Adelaide |
| callum-coleman-jones | Richmond | North Melbourne |
| campbell-chesser | West Coast | Carlton |
| changkuoth-jiath | Hawthorn | Melbourne |
| charlie-cameron | Adelaide | Brisbane |
| christian-petracca | Melbourne | Gold Coast |
| clayton-oliver | Melbourne | GWS |
| connor-budarick | Gold Coast | Western Bulldogs |
| conor-mckenna | Essendon | Brisbane |
| corey-wagner | North Melbourne | Fremantle |
| dan-houston | Port Adelaide | Collingwood |
| daniel-butler | Richmond | St Kilda |
| daniel-mcstay | Brisbane | Collingwood |
| daniel-rioli | Richmond | Gold Coast |
| darcy-cameron | Sydney | Collingwood |
| darragh-joyce | St Kilda | Brisbane |
| deven-robertson | Brisbane | West Coast |
| dion-prestia | Gold Coast | Richmond |
| dougal-howard | Port Adelaide | St Kilda |
| dylan-stephens | Sydney | North Melbourne |
| ed-langdon | Fremantle | Melbourne |
| elijah-hollands | Gold Coast | Carlton |
| elliot-yeo | Brisbane | West Coast |
| esava-ratugolea | Geelong | Port Adelaide |
| finlay-macrae | Collingwood | West Coast |
| finnbar-maley | North Melbourne | Adelaide |
| flynn-perez | North Melbourne | Hawthorn |
| francis-evans | Geelong | Carlton |
| george-hewett | Sydney | Carlton |
| griffin-logue | Fremantle | North Melbourne |
| harry-perryman | GWS | Collingwood |
| hugo-hall-kahan | Sydney | Adelaide |
| isaac-cumming | GWS | Adelaide |
| izak-rankine | Gold Coast | Adelaide |
| jack-bowes | Gold Coast | Geelong |
| jack-buller | Sydney | Collingwood |
| jack-carroll | Carlton | St Kilda |
| jack-crisp | Brisbane | Collingwood |
| jack-darling | West Coast | North Melbourne |
| jack-graham | Richmond | West Coast |
| jack-gunston | Adelaide | Hawthorn |
| jack-higgins | Richmond | St Kilda |
| jack-lukosius | Gold Coast | Port Adelaide |
| jack-martin | Gold Coast | Geelong |
| jack-scrimshaw | Gold Coast | Hawthorn |
| jack-silvagni | Carlton | St Kilda |
| jack-steele | GWS | Melbourne |
| jackson-macrae | Western Bulldogs | St Kilda |
| jacob-hopper | GWS | Richmond |
| jacob-konstanty | Sydney | North Melbourne |
| jacob-wehr | GWS | Port Adelaide |
| jade-gresham | St Kilda | Essendon |
| jaeger-o-meara | Gold Coast | Fremantle |
| jai-culley | West Coast | Melbourne |
| jai-serong | Hawthorn | Sydney |
| jake-lever | Adelaide | Melbourne |
| jake-melksham | Essendon | Melbourne |
| jake-stringer | Western Bulldogs | GWS |
| jamarra-ugle-hagan | Western Bulldogs | Gold Coast |
| james-jordon | Melbourne | Sydney |
| james-peatling | GWS | Adelaide |
| james-worpel | Hawthorn | Geelong |
| jamie-cripps | St Kilda | West Coast |
| jarman-impey | Port Adelaide | Hawthorn |
| jarrod-witts | Collingwood | Gold Coast |
| jason-horne-francis | North Melbourne | Port Adelaide |
| jayden-nguyen | Essendon | GWS |
| jeremy-cameron | GWS | Geelong |
| jeremy-howe | Melbourne | Collingwood |
| jeremy-sharp | Gold Coast | Fremantle |
| jesse-hogan | Melbourne | GWS |
| joe-richards | Collingwood | Port Adelaide |
| joel-hamling | Geelong | Sydney |
| john-noble | Collingwood | Gold Coast |
| jordan-clark | Geelong | Fremantle |
| jordan-dawson | Sydney | Adelaide |
| jordon-sweet | Western Bulldogs | Port Adelaide |
| josh-dunkley | Western Bulldogs | Brisbane |
| judd-mcvee | Melbourne | Fremantle |
| jye-caldwell | GWS | Essendon |
| karl-amon | Port Adelaide | Hawthorn |
| lachie-neale | Fremantle | Brisbane |
| lachlan-fogarty | Geelong | Carlton |
| lachlan-mcandrew | Sydney | Adelaide |
| lachlan-weller | Fremantle | Gold Coast |
| lewis-young | Western Bulldogs | Carlton |
| liam-baker | Richmond | West Coast |
| liam-henry | Fremantle | St Kilda |
| liam-mcmahon | Collingwood | Essendon |
| liam-reidy | Fremantle | Carlton |
| liam-ryan | West Coast | St Kilda |
| liam-stocker | Carlton | St Kilda |
| lincoln-mccarthy | Geelong | Brisbane |
| lloyd-meek | Fremantle | Hawthorn |
| luke-jackson | Melbourne | Fremantle |
| luke-parker | Sydney | North Melbourne |
| mabior-chol | Richmond | Hawthorn |
| malcolm-rosas | Gold Coast | Sydney |
| marc-pittonet | Hawthorn | Carlton |
| mark-keane | Collingwood | Adelaide |
| mason-cox | Collingwood | Fremantle |
| mason-wood | North Melbourne | St Kilda |
| massimo-d-ambrosio | Essendon | Hawthorn |
| matthew-flynn | GWS | West Coast |
| matthew-kennedy-1 | GWS | Western Bulldogs |
| max-heath | St Kilda | Melbourne |
| max-knobel | Fremantle | Gold Coast |
| mitch-mcgovern | Adelaide | Carlton |
| mitchell-hinge | Brisbane | Adelaide |
| ned-long | Hawthorn | Collingwood |
| nic-newman | Sydney | Carlton |
| nicholas-coffield | St Kilda | Western Bulldogs |
| nicholas-holman | Carlton | Gold Coast |
| nick-haynes | GWS | Carlton |
| oliver-florent | Sydney | Carlton |
| oliver-henry | Collingwood | Geelong |
| oscar-adams | St Kilda | Gold Coast |
| oscar-mcdonald | Melbourne | Fremantle |
| oskar-baker | Melbourne | Western Bulldogs |
| paddy-dow | Carlton | St Kilda |
| patrick-dangerfield | Adelaide | Geelong |
| patrick-lipinski | Western Bulldogs | Collingwood |
| patrick-voss | Essendon | Fremantle |
| peter-ladhams | Port Adelaide | Sydney |
| peter-wright | Gold Coast | Essendon |
| rhys-stanley | St Kilda | Geelong |
| rory-lobb | GWS | Western Bulldogs |
| ryan-gardner | Geelong | Western Bulldogs |
| sam-draper | Essendon | Brisbane |
| sam-flanders | Gold Coast | St Kilda |
| samuel-collins | Fremantle | Gold Coast |
| sandy-brock | Gold Coast | West Coast |
| shai-bolton | Richmond | Fremantle |
| tanner-bruhn | GWS | Geelong |
| tim-kelly | Geelong | West Coast |
| tim-membrey | Sydney | St Kilda |
| tim-taranto | GWS | Richmond |
| toby-bedford | Melbourne | GWS |
| toby-nankervis | Sydney | Richmond |
| toby-pink | Sydney | North Melbourne |
| tom-barrass | West Coast | Hawthorn |
| tom-de-koning | Carlton | St Kilda |
| tom-doedee | Adelaide | Brisbane |
| tom-lynch-1 | Gold Coast | Richmond |
| tylar-young | Richmond | West Coast |
| tyler-brockman | Hawthorn | West Coast |
| wade-derksen | GWS | Carlton |
| will-brodie | Gold Coast | Port Adelaide |
| will-hayward | Sydney | Carlton |
| will-setterfield | GWS | Essendon |
| xavier-duursma | Port Adelaide | Essendon |
| zac-fisher | Carlton | North Melbourne |
| zachary-williams | GWS | Carlton |

## C. UNCHANGED (verified)

- Back-catalogue rows: **0 club movers, 0 v movers** (fall back to draft club; retired, no current club).
- CAT_BY_CLUB: byte-identical (rename only). CAT_BY_RANGE: byte-identical.
- Panel 10/10 names: unmoved (no panel name is a v mover).
- lensConservation diagnostic: +1 (reflects bramble's lens values).
