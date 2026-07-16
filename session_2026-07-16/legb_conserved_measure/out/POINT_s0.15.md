# LEG B CONSERVED — POINT s=0.15 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (127 lift / 79 cut) · net board SigmaD +1850 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +1752       9356       69
    GEN_FWD      183       -623       3139       30
    KEY_FWD      103        -65       1899       20
    GEN_DEF      176       +202       4834       48
    KEY_DEF       92       +166       1796       20
    RUC           55       +418       2348       19
    ALL          804      +1850      23372      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +1850 num-SCAR  (0.25% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3689 / 1838 = 2.007x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->4025 (+400, +11.0%)  rank 35->25 (-10)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=7
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0        +8     +0.9    240->245 (+5)
    Lachlan McAndrew        RUC     26.0        +4     +0.3    185->188 (+3)
    Jordan Ridley           GEN_DEF 28.0       +15     +1.3    206->209 (+3)
    Nick Madden             RUC     22.0       +30     +2.0    164->166 (+2)
    Brent Daniels           GEN_FWD 27.0       +29     +2.0    168->170 (+2)
    Willem Drew             MID     28.0       +18     +2.2    256->258 (+2)
    Timothy English         RUC     29.0       +34     +0.9     34->35  (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Ben Keays               GEN_FWD        +72    450->406 (-44)
    Jack Viney              MID            +74    440->396 (-44)
    Jarrod Witts            RUC            +79    414->371 (-43)
    Joshua Kelly            MID           +103    350->309 (-41)
    Milan Murdock           GEN_FWD       +189    265->226 (-39)
    Tom Atkins              MID            +55    495->456 (-39)
    Scott Pendlebury        MID           +115    340->305 (-35)
    Tom Papley              GEN_FWD        +80    389->357 (-32)
    Elliot Yeo              MID            +73    356->324 (-32)
    Patrick Lipinski        GEN_FWD        +83    343->313 (-30)
    Liam Duggan             GEN_DEF        +43    423->394 (-29)
    Jeremy Howe             GEN_DEF        +40    508->479 (-29)
    Rory Lobb               KEY_DEF        +52    455->427 (-28)
    Lachie Neale            MID           +267    118->91  (-27)
    Thomas Liberatore       MID           +277    113->86  (-27)
    Patrick Dangerfield     GEN_FWD        +31    655->629 (-26)
    Dayne Zorko             GEN_DEF       +221    207->183 (-24)
    Oliver Wines            MID            +61    383->360 (-23)
    Jack Gunston            KEY_FWD       +209    204->181 (-23)
    Jake Lever              KEY_DEF        +48    351->329 (-22)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Kieren Briggs           RUC           -232    102->128 (+26)
    Josh Rachele            GEN_FWD       -223     94->115 (+21)
    Tom De Koning           RUC           -216    111->132 (+21)
    Jack Ginnivan           GEN_FWD       -171     87->105 (+18)
    Nick Watson             GEN_FWD       -509     40->56  (+16)
    Dylan Moore             GEN_FWD        -79    144->159 (+15)
    Ryley Sanders           MID           -549     28->42  (+14)
    Connor MacDonald        GEN_FWD       -277     74->88  (+14)
    Trent Rivers            GEN_DEF       -143     96->110 (+14)
    Harvey Thomas           GEN_FWD       -198     84->97  (+13)
    Connor Idun             GEN_DEF       -128    101->113 (+12)
    Lloyd Meek              RUC            -60    189->201 (+12)
    Sam Durham              MID            -88    133->144 (+11)
    Jack Lukosius           KEY_FWD        -25    160->171 (+11)
    Jye Caldwell            MID            -70    167->178 (+11)
    Bailey J. Williams      RUC           -107     93->104 (+11)
    Kane Farrell            GEN_DEF        -45    149->160 (+11)
    Darcy Wilmot            GEN_DEF       -460     23->33  (+10)
    Aaron Naughton          KEY_FWD        -63    135->145 (+10)
    Alix Tauru              KEY_DEF         +0    158->167 (+9)
