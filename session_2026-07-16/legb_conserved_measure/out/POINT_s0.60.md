# LEG B CONSERVED — POINT s=0.60 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (121 lift / 85 cut) · net board SigmaD +7286 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +7606      39044       69
    GEN_FWD      183      -3112      12402       30
    KEY_FWD      103       -320       8134       20
    GEN_DEF      176       +553      19411       48
    KEY_DEF       92       +769       7347       20
    RUC           55      +1790       9516       19
    ALL          804      +7286      95854      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +7286 num-SCAR  (0.99% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3694 / 1252 = 2.950x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->5425 (+1800, +49.7%)  rank 35->11 (-24)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=6
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0        +9     +1.0    240->253 (+13)
    Lachlan Schultz         GEN_FWD 29.0       +11     +1.4    267->278 (+11)
    Daniel Rioli            GEN_DEF 29.0       +19     +2.5    270->280 (+10)
    Jordan Ridley           GEN_DEF 28.0       +26     +2.3    206->211 (+5)
    Ned Moyle               RUC     24.0       +60     +3.6    139->142 (+3)
    Willem Drew             MID     28.0       +52     +6.3    256->257 (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID           +395    440->286 (-154)
    Tom Atkins              MID           +277    495->349 (-146)
    Jarrod Witts            RUC           +396    414->276 (-138)
    Ben Keays               GEN_FWD       +341    450->314 (-136)
    Patrick Dangerfield     GEN_FWD       +168    655->521 (-134)
    Joshua Kelly            MID           +530    350->220 (-130)
    Scott Pendlebury        MID           +590    340->210 (-130)
    Milan Murdock           GEN_FWD       +973    265->138 (-127)
    Dayne Zorko             GEN_DEF      +1122    207->89  (-118)
    Tom Papley              GEN_FWD       +369    389->272 (-117)
    Jeremy Howe             GEN_DEF       +184    508->391 (-117)
    Rory Lobb               KEY_DEF       +240    455->339 (-116)
    Jack Gunston            KEY_FWD      +1042    204->93  (-111)
    Elliot Yeo              MID           +335    356->261 (-95)
    Patrick Lipinski        GEN_FWD       +359    343->252 (-91)
    Oliver Wines            MID           +276    383->292 (-91)
    George Hewett           MID           +906    172->83  (-89)
    Jeremy Cameron          KEY_FWD       +979    165->76  (-89)
    Sam De Koning           KEY_DEF       +838    205->118 (-87)
    Jackson Macrae          MID            +98    554->470 (-84)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Connor MacDonald        GEN_FWD      -1019     74->173 (+99)
    Kieren Briggs           RUC           -818    102->199 (+97)
    Josh Rachele            GEN_FWD       -824     94->189 (+95)
    Tom De Koning           RUC           -767    111->202 (+91)
    Nick Watson             GEN_FWD      -1621     40->123 (+83)
    Harvey Thomas           GEN_FWD       -781     84->163 (+79)
    Jack Ginnivan           GEN_FWD       -693     87->165 (+78)
    Trent Rivers            GEN_DEF       -562     96->159 (+63)
    Ryley Sanders           MID          -1730     28->90  (+62)
    Connor Idun             GEN_DEF       -515    101->157 (+56)
    Dylan Moore             GEN_FWD       -367    144->197 (+53)
    Bailey J. Williams      RUC           -445     93->143 (+50)
    Shannon Neale           KEY_FWD       -541     79->126 (+47)
    Sam Durham              MID           -361    133->179 (+46)
    Reuben Ginbey           KEY_DEF       -762     60->105 (+45)
    Lloyd Meek              RUC           -255    189->234 (+45)
    Darcy Wilmot            GEN_DEF      -1630     23->67  (+44)
    Hayden Young            MID           -621     66->110 (+44)
    Tom Powell              GEN_FWD       -454     78->119 (+41)
    Sam Taylor              KEY_DEF       -357    104->145 (+41)
