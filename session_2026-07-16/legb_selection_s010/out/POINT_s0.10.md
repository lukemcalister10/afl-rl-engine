# LEG B CONSERVED — POINT s=0.10 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (128 lift / 78 cut) · net board SigmaD +1231 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +1155       6201       69
    GEN_FWD      183       -404       2088       30
    KEY_FWD      103        -45       1261       20
    GEN_DEF      176       +148       3226       48
    KEY_DEF       92       +105       1189       20
    RUC           55       +272       1562       19
    ALL          804      +1231      15527      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +1231 num-SCAR  (0.17% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3679 / 1913 = 1.923x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->3888 (+263, +7.3%)  rank 35->26 (-9)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=10
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0        +6     +0.7    240->243 (+3)
    Timothy English         RUC     29.0       +24     +0.7     34->36  (+2)
    Jordan Ridley           GEN_DEF 28.0       +10     +0.9    206->208 (+2)
    Willem Drew             MID     28.0       +12     +1.4    256->258 (+2)
    Nick Madden             RUC     22.0       +20     +1.4    164->165 (+1)
    Jordon Sweet            RUC     28.0       +18     +0.7     72->73  (+1)
    Brent Daniels           GEN_FWD 27.0       +21     +1.5    168->169 (+1)
    Jake Waterman           KEY_FWD 28.0       +31     +1.7    125->126 (+1)
    Harry McKay             KEY_FWD 29.0       +28     +1.5    124->125 (+1)
    Ryan Lester             KEY_DEF 34.0       +27     +3.1    244->245 (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID            +49    440->408 (-32)
    Ben Keays               GEN_FWD        +47    450->419 (-31)
    Joshua Kelly            MID            +67    350->319 (-31)
    Jarrod Witts            RUC            +52    414->385 (-29)
    Scott Pendlebury        MID            +74    340->311 (-29)
    Milan Murdock           GEN_FWD       +122    265->240 (-25)
    Tom Atkins              MID            +36    495->470 (-25)
    Tom Papley              GEN_FWD        +52    389->366 (-23)
    Elliot Yeo              MID            +48    356->333 (-23)
    Patrick Lipinski        GEN_FWD        +54    343->321 (-22)
    Liam Duggan             GEN_DEF        +29    423->402 (-21)
    Thomas Liberatore       MID           +182    113->93  (-20)
    Rory Lobb               KEY_DEF        +34    455->436 (-19)
    Jeremy Howe             GEN_DEF        +27    508->489 (-19)
    Patrick Dangerfield     GEN_FWD        +20    655->636 (-19)
    Shaun Mannagh           GEN_FWD        +39    381->363 (-18)
    Oliver Wines            MID            +39    383->365 (-18)
    Jack Gunston            KEY_FWD       +136    204->187 (-17)
    Jack Steele             MID           +110    151->135 (-16)
    Lachie Neale            MID           +175    118->102 (-16)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Josh Rachele            GEN_FWD       -149     94->112 (+18)
    Tom De Koning           RUC           -146    111->128 (+17)
    Kieren Briggs           RUC           -157    102->115 (+13)
    Nick Watson             GEN_FWD       -345     40->52  (+12)
    Jack Ginnivan           GEN_FWD       -114     87->99  (+12)
    Dylan Moore             GEN_FWD        -51    144->155 (+11)
    Ryley Sanders           MID           -374     28->38  (+10)
    Trent Rivers            GEN_DEF        -96     96->106 (+10)
    Connor MacDonald        GEN_FWD       -186     74->83  (+9)
    Jye Caldwell            MID            -47    167->176 (+9)
    Connor Idun             GEN_DEF        -85    101->110 (+9)
    Lloyd Meek              RUC            -40    189->198 (+9)
    Bailey J. Williams      RUC            -71     93->101 (+8)
    Kane Farrell            GEN_DEF        -29    149->157 (+8)
    Jack Lukosius           KEY_FWD        -17    160->167 (+7)
    Sam Taylor              KEY_DEF        -57    104->111 (+7)
    Latrelle Pickett        GEN_FWD         +0    329->335 (+6)
    Zane Peucker            GEN_FWD         +0    337->343 (+6)
    Jack Dalton             GEN_FWD         +0    332->338 (+6)
    Alix Tauru              KEY_DEF         +0    158->164 (+6)

## A-PAIRS (scored on the wired-default board; num-SCAR)
    pair_2 reid/bont (PARITY): reid 3343 vs bont 3888 = -14.0%  [+/-10%: FAIL | +/-15% (item266): PASS]
    pair_3 sanders/bont (sit 0-10% below): sanders 3579 vs bont 3888 = -7.9%  [PASS]
