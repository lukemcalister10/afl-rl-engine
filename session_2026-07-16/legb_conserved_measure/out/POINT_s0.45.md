# LEG B CONSERVED — POINT s=0.45 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 205 movers (123 lift / 82 cut) · net board SigmaD +5409 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +5517      28905       68
    GEN_FWD      183      -2218       9400       30
    KEY_FWD      103       -226       5970       20
    GEN_DEF      176       +474      14564       48
    KEY_DEF       92       +550       5478       20
    RUC           55      +1312       7066       19
    ALL          804      +5409      71383      205

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +5409 num-SCAR  (0.74% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3709 / 1429 = 2.596x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->4925 (+1300, +35.9%)  rank 35->15 (-20)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=7
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0       +13     +1.4    240->250 (+10)
    Daniel Rioli            GEN_DEF 29.0       +20     +2.6    270->275 (+5)
    Jordan Ridley           GEN_DEF 28.0       +27     +2.4    206->210 (+4)
    Lachlan Schultz         GEN_FWD 29.0       +20     +2.5    267->270 (+3)
    Willem Drew             MID     28.0       +43     +5.2    256->259 (+3)
    Ned Moyle               RUC     24.0       +57     +3.4    139->140 (+1)
    Josh Daicos             GEN_DEF 28.0       +12     +0.6     92->93  (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Tom Atkins              MID           +193    495->375 (-120)
    Jack Viney              MID           +270    440->322 (-118)
    Ben Keays               GEN_FWD       +243    450->334 (-116)
    Jarrod Witts            RUC           +276    414->311 (-103)
    Scott Pendlebury        MID           +406    340->238 (-102)
    Joshua Kelly            MID           +364    350->251 (-99)
    Milan Murdock           GEN_FWD       +673    265->171 (-94)
    Tom Papley              GEN_FWD       +265    389->298 (-91)
    Rory Lobb               KEY_DEF       +170    455->366 (-89)
    Jeremy Howe             GEN_DEF       +131    508->420 (-88)
    Dayne Zorko             GEN_DEF       +778    207->122 (-85)
    Patrick Dangerfield     GEN_FWD       +113    655->571 (-84)
    Jack Gunston            KEY_FWD       +726    204->124 (-80)
    Patrick Lipinski        GEN_FWD       +264    343->267 (-76)
    Elliot Yeo              MID           +240    356->282 (-74)
    Jeremy Cameron          KEY_FWD       +697    165->92  (-73)
    George Hewett           MID           +647    172->100 (-72)
    Oliver Wines            MID           +198    383->315 (-68)
    Jackson Macrae          MID            +73    554->489 (-65)
    Jack Crisp              MID           +289    316->253 (-63)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Josh Rachele            GEN_FWD       -635     94->168 (+74)
    Connor MacDonald        GEN_FWD       -788     74->148 (+74)
    Kieren Briggs           RUC           -641    102->175 (+73)
    Tom De Koning           RUC           -599    111->182 (+71)
    Jack Ginnivan           GEN_FWD       -519     87->149 (+62)
    Harvey Thomas           GEN_FWD       -590     84->141 (+57)
    Nick Watson             GEN_FWD      -1377     40->91  (+51)
    Trent Rivers            GEN_DEF       -425     96->145 (+49)
    Connor Idun             GEN_DEF       -386    101->147 (+46)
    Ryley Sanders           MID          -1454     28->73  (+45)
    Dylan Moore             GEN_FWD       -265    144->184 (+40)
    Bailey J. Williams      RUC           -331     93->131 (+38)
    Sam Durham              MID           -269    133->169 (+36)
    Jye Caldwell            MID           -214    167->200 (+33)
    Darcy Wilmot            GEN_DEF      -1274     23->55  (+32)
    Sam Taylor              KEY_DEF       -265    104->134 (+30)
    Shannon Neale           KEY_FWD       -408     79->108 (+29)
    Aaron Naughton          KEY_FWD       -198    135->164 (+29)
    Lloyd Meek              RUC           -189    189->218 (+29)
    Reilly O'Brien          RUC           -170    197->225 (+28)
