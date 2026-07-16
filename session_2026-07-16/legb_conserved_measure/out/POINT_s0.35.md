# LEG B CONSERVED — POINT s=0.35 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (127 lift / 79 cut) · net board SigmaD +4245 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +4223      22293       69
    GEN_FWD      183      -1632       7296       30
    KEY_FWD      103       -167       4579       20
    GEN_DEF      176       +410      11330       48
    KEY_DEF       92       +412       4240       20
    RUC           55       +999       5489       19
    ALL          804      +4245      55227      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +4245 num-SCAR  (0.58% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3709 / 1557 = 2.382x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->4610 (+985, +27.2%)  rank 35->18 (-17)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=9
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0       +14     +1.6    240->249 (+9)
    Lachlan McAndrew        RUC     26.0        +2     +0.2    185->192 (+7)
    Jordan Ridley           GEN_DEF 28.0       +26     +2.3    206->209 (+3)
    Daniel Rioli            GEN_DEF 29.0       +18     +2.3    270->273 (+3)
    Nick Madden             RUC     22.0       +61     +4.2    164->166 (+2)
    Brent Daniels           GEN_FWD 27.0       +50     +3.5    168->170 (+2)
    Ned Moyle               RUC     24.0       +50     +3.0    139->140 (+1)
    Lachlan Schultz         GEN_FWD 29.0       +21     +2.6    267->268 (+1)
    Josh Daicos             GEN_DEF 28.0       +17     +0.8     92->93  (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID           +197    440->347 (-93)
    Tom Atkins              MID           +143    495->403 (-92)
    Ben Keays               GEN_FWD       +181    450->361 (-89)
    Jarrod Witts            RUC           +204    414->327 (-87)
    Joshua Kelly            MID           +268    350->265 (-85)
    Scott Pendlebury        MID           +299    340->259 (-81)
    Tom Papley              GEN_FWD       +200    389->313 (-76)
    Milan Murdock           GEN_FWD       +495    265->191 (-74)
    Rory Lobb               KEY_DEF       +129    455->381 (-74)
    Jeremy Howe             GEN_DEF        +99    508->440 (-68)
    Patrick Dangerfield     GEN_FWD        +82    655->589 (-66)
    Patrick Lipinski        GEN_FWD       +201    343->283 (-60)
    Dayne Zorko             GEN_DEF       +574    207->147 (-60)
    Jeremy Cameron          KEY_FWD       +523    165->106 (-59)
    Oliver Wines            MID           +149    383->325 (-58)
    Jack Gunston            KEY_FWD       +538    204->146 (-58)
    Jackson Macrae          MID            +55    554->498 (-56)
    Elliot Yeo              MID           +182    356->300 (-56)
    Liam Duggan             GEN_DEF       +104    423->369 (-54)
    Jack Crisp              MID           +217    316->262 (-54)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Josh Rachele            GEN_FWD       -502     94->154 (+60)
    Kieren Briggs           RUC           -513    102->162 (+60)
    Tom De Koning           RUC           -479    111->168 (+57)
    Connor MacDonald        GEN_FWD       -625     74->129 (+55)
    Harvey Thomas           GEN_FWD       -460     84->128 (+44)
    Jack Ginnivan           GEN_FWD       -403     87->131 (+44)
    Nick Watson             GEN_FWD      -1109     40->77  (+37)
    Trent Rivers            GEN_DEF       -333     96->133 (+37)
    Ryley Sanders           MID          -1178     28->64  (+36)
    Connor Idun             GEN_DEF       -301    101->134 (+33)
    Dylan Moore             GEN_FWD       -199    144->176 (+32)
    Sam Durham              MID           -209    133->164 (+31)
    Bailey J. Williams      RUC           -256     93->123 (+30)
    Jye Caldwell            MID           -165    167->194 (+27)
    Sam Taylor              KEY_DEF       -204    104->130 (+26)
    Aaron Naughton          KEY_FWD       -152    135->160 (+25)
    Darcy Wilmot            GEN_DEF      -1018     23->46  (+23)
    Reuben Ginbey           KEY_DEF       -456     60->82  (+22)
    Kane Farrell            GEN_DEF       -115    149->171 (+22)
    Lloyd Meek              RUC           -146    189->211 (+22)
