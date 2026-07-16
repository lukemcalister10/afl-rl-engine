# LEG B CONSERVED — POINT s=0.70 (shipped C applied)  ·  OFF (board 8d90c9ac) -> ON (conserved map at s)
active-804: 804 rows · 206 movers (121 lift / 85 cut) · net board SigmaD +8478 num-SCAR

## POSITION-POOL Δ TOTALS (which pools re-rate, by how much)
    pos            n      ΣΔnum       Σ|Δ|   movers
    MID          195      +9025      45919       69
    GEN_FWD      183      -3794      14374       30
    KEY_FWD      103       -389       9619       20
    GEN_DEF      176       +568      22616       48
    KEY_DEF       92       +940       8588       20
    RUC           55      +2128      11196       19
    ALL          804      +8478     112312      206

## CENSUS / RESIDUAL GAUGE (conserved production-side map; per-position renorm recycles value within pool)
    net board residual SigmaD = +8478 num-SCAR  (1.15% of the 734044 active-804 baseline sum)
    (frozen census-v2 cell-gate (global<=15612 + cells) runs bake/gate-mode only; fenced OUT of this
     measurement — the net residual above is the honest ledger reading of the conserved re-rate.)

## English/Briggs priced ratio (owner hard floor 1.75; captain lift IN via ev())
    OFF: 3655 / 2070 = 1.766x     ON: 3675 / 1144 = 3.212x   => PASS >= 1.75

## BONTEMPELLI (owner's sincerity test: SCAR up AND rank up, else FAILURE)
    Marcus Bontempelli  SCAR 3625->5775 (+2150, +59.3%)  rank 35->10 (-25)  => PASS (SCAR up AND rank up)

## SINCERITY FAILURES (item 256): SCAR RISES while RANK FALLS — count=6
    player                  pos      age     ΔSCAR       Δ%      rank Δ
    Lachlan Schultz         GEN_FWD 29.0        +1     +0.1    267->285 (+18)
    Daniel Rioli            GEN_DEF 29.0       +16     +2.1    270->284 (+14)
    Brayden Maynard         GEN_DEF 30.0        +4     +0.4    240->254 (+14)
    Jordan Ridley           GEN_DEF 28.0       +22     +2.0    206->212 (+6)
    Willem Drew             MID     28.0       +55     +6.7    256->262 (+6)
    Ned Moyle               RUC     24.0       +58     +3.5    139->141 (+2)

## TOP-20 RANK GAINERS (rank moved UP most; Δrank most negative)
    player                  pos          ΔSCAR      rank Δ
    Jack Viney              MID           +492    440->267 (-173)
    Tom Atkins              MID           +339    495->329 (-166)
    Patrick Dangerfield     GEN_FWD       +209    655->490 (-165)
    Ben Keays               GEN_FWD       +411    450->290 (-160)
    Jarrod Witts            RUC           +486    414->256 (-158)
    Milan Murdock           GEN_FWD      +1195    265->116 (-149)
    Joshua Kelly            MID           +655    350->201 (-149)
    Scott Pendlebury        MID           +727    340->192 (-148)
    Jeremy Howe             GEN_DEF       +220    508->373 (-135)
    Dayne Zorko             GEN_DEF      +1379    207->72  (-135)
    Tom Papley              GEN_FWD       +439    389->257 (-132)
    Rory Lobb               KEY_DEF       +289    455->325 (-130)
    Jack Gunston            KEY_FWD      +1278    204->76  (-128)
    Elliot Yeo              MID           +403    356->246 (-110)
    Sam De Koning           KEY_DEF      +1018    205->97  (-108)
    Patrick Lipinski        GEN_FWD       +424    343->237 (-106)
    George Hewett           MID          +1090    172->68  (-104)
    Oliver Wines            MID           +330    383->280 (-103)
    Jeremy Cameron          KEY_FWD      +1180    165->65  (-100)
    Jack Crisp              MID           +486    316->218 (-98)

## TOP-20 RANK LOSERS (rank moved DOWN most; Δrank most positive)
    player                  pos          ΔSCAR      rank Δ
    Connor MacDonald        GEN_FWD      -1159     74->187 (+113)
    Josh Rachele            GEN_FWD       -943     94->204 (+110)
    Kieren Briggs           RUC           -926    102->210 (+108)
    Tom De Koning           RUC           -869    111->215 (+104)
    Nick Watson             GEN_FWD      -1766     40->136 (+96)
    Jack Ginnivan           GEN_FWD       -806     87->178 (+91)
    Harvey Thomas           GEN_FWD       -906     84->173 (+89)
    Ryley Sanders           MID          -1875     28->104 (+76)
    Trent Rivers            GEN_DEF       -651     96->168 (+72)
    Darcy Wilmot            GEN_DEF      -1848     23->86  (+63)
    Connor Idun             GEN_DEF       -598    101->164 (+63)
    Bailey J. Williams      RUC           -521     93->154 (+61)
    Reuben Ginbey           KEY_DEF       -867     60->120 (+60)
    Dylan Moore             GEN_FWD       -439    144->202 (+58)
    Shannon Neale           KEY_FWD       -628     79->135 (+56)
    Hayden Young            MID           -718     66->122 (+56)
    Tom Powell              GEN_FWD       -549     78->129 (+51)
    Sam Durham              MID           -422    133->184 (+51)
    Lloyd Meek              RUC           -299    189->240 (+51)
    Jye Caldwell            MID           -335    167->216 (+49)
