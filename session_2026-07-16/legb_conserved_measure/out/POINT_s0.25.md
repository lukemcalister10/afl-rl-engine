# LEG B CONSERVED — POINT s=0.25 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (127 lift / 79 cut) · net board SigmaD +3080 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +2970      15760       69
    GEN_FWD      183      -1095       5223       30
    KEY_FWD      103       -110       3220       20
    GEN_DEF      176       +319       8077       48
    KEY_DEF       92       +291       3015       20
    RUC           55       +705       3917       19
    ALL          804      +3080      39212      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +3080 num-SCAR  (0.42% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3702 / 1693 = 2.187x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->4310 (+685, +18.9%)  rank 35->21 (-14)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=7
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0       +12     +1.3    240->247 (+7)
    Lachlan McAndrew        RUC     26.0        +5     +0.4    185->191 (+6)
    Brent Daniels           GEN_FWD 27.0       +42     +2.9    168->171 (+3)
    Jordan Ridley           GEN_DEF 28.0       +21     +1.9    206->209 (+3)
    Willem Drew             MID     28.0       +28     +3.4    256->259 (+3)
    Nick Madden             RUC     22.0       +47     +3.2    164->166 (+2)
    Josh Daicos             GEN_DEF 28.0       +18     +0.8     92->94  (+2)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Ben Keays               GEN_FWD       +124    450->376 (-74)
    Jack Viney              MID           +132    440->368 (-72)
    Scott Pendlebury        MID           +201    340->276 (-64)
    Tom Atkins              MID            +97    495->433 (-62)
    Tom Papley              GEN_FWD       +139    389->330 (-59)
    Jarrod Witts            RUC           +138    414->355 (-59)
    Joshua Kelly            MID           +181    350->292 (-58)
    Rory Lobb               KEY_DEF        +89    455->401 (-54)
    Milan Murdock           GEN_FWD       +334    265->212 (-53)
    Elliot Yeo              MID           +125    356->309 (-47)
    Jeremy Howe             GEN_DEF        +69    508->462 (-46)
    Jackson Macrae          MID            +39    554->510 (-44)
    Liam Duggan             GEN_DEF        +74    423->380 (-43)
    Patrick Dangerfield     GEN_FWD        +54    655->612 (-43)
    Patrick Lipinski        GEN_FWD       +141    343->304 (-39)
    Oliver Wines            MID           +104    383->344 (-39)
    Jack Crisp              MID           +150    316->277 (-39)
    Jack Gunston            KEY_FWD       +366    204->167 (-37)
    Dayne Zorko             GEN_DEF       +389    207->170 (-37)
    Jeremy Cameron          KEY_FWD       +361    165->129 (-36)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Josh Rachele            GEN_FWD       -364     94->136 (+42)
    Tom De Koning           RUC           -351    111->150 (+39)
    Kieren Briggs           RUC           -377    102->140 (+38)
    Connor MacDonald        GEN_FWD       -454     74->104 (+30)
    Jack Ginnivan           GEN_FWD       -287     87->113 (+26)
    Nick Watson             GEN_FWD       -820     40->65  (+25)
    Trent Rivers            GEN_DEF       -238     96->121 (+25)
    Connor Idun             GEN_DEF       -214    101->126 (+25)
    Dylan Moore             GEN_FWD       -137    144->169 (+25)
    Ryley Sanders           MID           -878     28->52  (+24)
    Sam Durham              MID           -148    133->157 (+24)
    Harvey Thomas           GEN_FWD       -329     84->106 (+22)
    Aaron Naughton          KEY_FWD       -107    135->154 (+19)
    Jye Caldwell            MID           -117    167->185 (+18)
    Darcy Wilmot            GEN_DEF       -747     23->40  (+17)
    Kane Farrell            GEN_DEF        -79    149->165 (+16)
    Lloyd Meek              RUC           -102    189->205 (+16)
    Daniel Turner           KEY_DEF        -58    148->163 (+15)
    Bailey J. Williams      RUC           -181     93->108 (+15)
    Reuben Ginbey           KEY_DEF       -329     60->74  (+14)
