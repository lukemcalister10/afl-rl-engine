# LEG B CONSERVED — POINT s=0.65 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (121 lift / 85 cut) · net board SigmaD +7884 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +8317      42463       69
    GEN_FWD      183      -3445      13393       30
    KEY_FWD      103       -353       8875       20
    GEN_DEF      176       +557      21015       48
    KEY_DEF       92       +850       7966       20
    RUC           55      +1958      10352       19
    ALL          804      +7884     104064      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +7884 num-SCAR  (1.07% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3685 / 1197 = 3.079x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->5599 (+1974, +54.5%)  rank 35->11 (-24)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=6
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Lachlan Schultz         GEN_FWD 29.0        +6     +0.8    267->281 (+14)
    Daniel Rioli            GEN_DEF 29.0       +17     +2.2    270->284 (+14)
    Brayden Maynard         GEN_DEF 30.0        +6     +0.7    240->253 (+13)
    Jordan Ridley           GEN_DEF 28.0       +24     +2.1    206->212 (+6)
    Ned Moyle               RUC     24.0       +60     +3.6    139->142 (+3)
    Willem Drew             MID     28.0       +54     +6.5    256->258 (+2)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID           +443    440->275 (-165)
    Tom Atkins              MID           +307    495->339 (-156)
    Patrick Dangerfield     GEN_FWD       +187    655->500 (-155)
    Ben Keays               GEN_FWD       +376    450->300 (-150)
    Jarrod Witts            RUC           +439    414->270 (-144)
    Milan Murdock           GEN_FWD      +1082    265->124 (-141)
    Scott Pendlebury        MID           +657    340->201 (-139)
    Joshua Kelly            MID           +590    350->213 (-137)
    Jeremy Howe             GEN_DEF       +202    508->382 (-126)
    Rory Lobb               KEY_DEF       +263    455->331 (-124)
    Tom Papley              GEN_FWD       +404    389->266 (-123)
    Dayne Zorko             GEN_DEF      +1248    207->84  (-123)
    Jack Gunston            KEY_FWD      +1158    204->87  (-117)
    Elliot Yeo              MID           +369    356->255 (-101)
    Sam De Koning           KEY_DEF       +926    205->105 (-100)
    Jeremy Cameron          KEY_FWD      +1078    165->66  (-99)
    Patrick Lipinski        GEN_FWD       +391    343->245 (-98)
    Oliver Wines            MID           +302    383->287 (-96)
    George Hewett           MID           +997    172->78  (-94)
    Josh Dunkley            MID           +814    216->125 (-91)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Josh Rachele            GEN_FWD       -884     94->199 (+105)
    Connor MacDonald        GEN_FWD      -1091     74->179 (+105)
    Kieren Briggs           RUC           -873    102->204 (+102)
    Tom De Koning           RUC           -819    111->207 (+96)
    Nick Watson             GEN_FWD      -1695     40->131 (+91)
    Harvey Thomas           GEN_FWD       -844     84->168 (+84)
    Jack Ginnivan           GEN_FWD       -750     87->170 (+83)
    Ryley Sanders           MID          -1804     28->97  (+69)
    Trent Rivers            GEN_DEF       -607     96->163 (+67)
    Connor Idun             GEN_DEF       -556    101->162 (+61)
    Dylan Moore             GEN_FWD       -403    144->200 (+56)
    Reuben Ginbey           KEY_DEF       -816     60->115 (+55)
    Shannon Neale           KEY_FWD       -585     79->133 (+54)
    Bailey J. Williams      RUC           -483     93->147 (+54)
    Hayden Young            MID           -670     66->118 (+52)
    Darcy Wilmot            GEN_DEF      -1741     23->74  (+51)
    Sam Durham              MID           -391    133->183 (+50)
    Jye Caldwell            MID           -312    167->214 (+47)
    Lloyd Meek              RUC           -277    189->236 (+47)
    Darcy Wilson            GEN_FWD       -481     76->121 (+45)
