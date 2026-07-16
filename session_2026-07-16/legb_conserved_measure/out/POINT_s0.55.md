# LEG B CONSERVED — POINT s=0.55 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (122 lift / 84 cut) · net board SigmaD +6666 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +6889      35641       69
    GEN_FWD      183      -2794      11408       30
    KEY_FWD      103       -285       7405       20
    GEN_DEF      176       +532      17792       48
    KEY_DEF       92       +692       6726       20
    RUC           55      +1632       8686       19
    ALL          804      +6666      87658      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +6666 num-SCAR  (0.91% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3700 / 1310 = 2.824x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->5255 (+1630, +45.0%)  rank 35->12 (-23)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=7
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Brayden Maynard         GEN_DEF 30.0       +11     +1.2    240->252 (+12)
    Lachlan Schultz         GEN_FWD 29.0       +15     +1.9    267->276 (+9)
    Daniel Rioli            GEN_DEF 29.0       +20     +2.6    270->278 (+8)
    Jordan Ridley           GEN_DEF 28.0       +27     +2.4    206->210 (+4)
    Ned Moyle               RUC     24.0       +60     +3.6    139->141 (+2)
    Willem Drew             MID     28.0       +49     +5.9    256->258 (+2)
    Josh Daicos             GEN_DEF 28.0        +1     +0.1     92->93  (+1)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID           +351    440->302 (-138)
    Tom Atkins              MID           +247    495->364 (-131)
    Ben Keays               GEN_FWD       +308    450->321 (-129)
    Jarrod Witts            RUC           +355    414->285 (-129)
    Scott Pendlebury        MID           +526    340->218 (-122)
    Joshua Kelly            MID           +472    350->231 (-119)
    Milan Murdock           GEN_FWD       +869    265->147 (-118)
    Patrick Dangerfield     GEN_FWD       +149    655->540 (-115)
    Dayne Zorko             GEN_DEF      +1003    207->97  (-110)
    Tom Papley              GEN_FWD       +333    389->281 (-108)
    Jeremy Howe             GEN_DEF       +165    508->403 (-105)
    Rory Lobb               KEY_DEF       +216    455->352 (-103)
    Jack Gunston            KEY_FWD       +932    204->101 (-103)
    Elliot Yeo              MID           +302    356->267 (-89)
    Patrick Lipinski        GEN_FWD       +328    343->256 (-87)
    George Hewett           MID           +817    172->89  (-83)
    Jeremy Cameron          KEY_FWD       +882    165->82  (-83)
    Sam De Koning           KEY_DEF       +753    205->126 (-79)
    Jackson Macrae          MID            +89    554->476 (-78)
    Oliver Wines            MID           +248    383->305 (-78)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Connor MacDonald        GEN_FWD       -944     74->164 (+90)
    Josh Rachele            GEN_FWD       -762     94->183 (+89)
    Kieren Briggs           RUC           -760    102->188 (+86)
    Tom De Koning           RUC           -713    111->197 (+86)
    Nick Watson             GEN_FWD      -1544     40->117 (+77)
    Jack Ginnivan           GEN_FWD       -635     87->161 (+74)
    Harvey Thomas           GEN_FWD       -718     84->156 (+72)
    Trent Rivers            GEN_DEF       -518     96->155 (+59)
    Ryley Sanders           MID          -1652     28->83  (+55)
    Connor Idun             GEN_DEF       -472    101->154 (+53)
    Bailey J. Williams      RUC           -407     93->142 (+49)
    Dylan Moore             GEN_FWD       -332    144->191 (+47)
    Shannon Neale           KEY_FWD       -497     79->122 (+43)
    Darcy Wilmot            GEN_DEF      -1515     23->65  (+42)
    Sam Durham              MID           -330    133->175 (+42)
    Lloyd Meek              RUC           -233    189->229 (+40)
    Sam Taylor              KEY_DEF       -326    104->143 (+39)
    Jye Caldwell            MID           -262    167->205 (+38)
    Reuben Ginbey           KEY_DEF       -703     60->96  (+36)
    Hayden Young            MID           -570     66->102 (+36)
