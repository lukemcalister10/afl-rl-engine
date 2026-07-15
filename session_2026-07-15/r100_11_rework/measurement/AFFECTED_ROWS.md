# AFFECTED-ROW LIST — R100.11 rework (schedule fade -> evidence fade) · candidate
Base board 800bf461 (schedule fade, the pinned base) -> Rework board 24159c49 (evidence fade pw(g)).
RAW board moves, numeraire SCAR = round(ev/1.0524). Sorted by |Δ|. Single lever => one leg (path-additive trivially).

## Separability / additivity
- total priced rows compared: 2652
- rows that MOVE base->rework: 28   (all carry a gap: True)
- NON-gap movers (must be 0 — separability): 0
- ΣΔ over all rows: +1652 num-SCAR   (raw ev +1739)   — the board's net move

## The complete affected list (28 rows), sorted |Δ| desc
player                    pos        base rework     Δ  gap(age_pre/ret/gpost) lvlB->lvlR
Bailey Smith              MID        4344   5152  +808  a23.0/ret2025/g37        104.8->111.0
Tanner Bruhn              MID         679   1080  +401  a22.0/ret2026/g13        66.9->72.7
Logan McDonald            KEY_FWD     646    815  +169  a22.0/ret2026/g14        56.0->60.6
Nikolas Cox               KEY_FWD     219    378  +159  a22.0/ret2026/g6         47.9->51.2
Leek Aleer                KEY_DEF     296    360   +64  a21.0/ret2024/g26        56.0->57.6
Brent Daniels             GEN_FWD    1243   1305   +62  a22.0/ret2023/g58        72.6->76.3
Todd Marshall             KEY_FWD     116    152   +36  a26.0/ret2026/g8         56.1->58.5
Zach Reid                 KEY_DEF    1633   1599   -34  a20.0/ret2024/g25        66.0->65.9
Charlie Curnow            KEY_FWD    1248   1231   -17  a22.0/ret2021/g104       73.5->73.4
Cody Weightman            GEN_FWD     307    321   +14  a23.0/ret2026/g2         56.3->57.7
Darcy Cameron             RUC        1485   1471   -14  a23.0/ret2020/g131       95.4->95.4
Willem Drew               MID         851    838   -13  a21.0/ret2021/g133       85.0->85.0
Jeremy Sharp              MID         123    134   +11  a21.0/ret2024/g39        55.3->57.2
Harvey Harrison           GEN_FWD      74     81    +7  a21.0/ret2026/g2         54.0->55.1
Andy Moniz-Wakefield      GEN_DEF      50     56    +6  a21.0/ret2026/g2         55.7->57.0
Ben King                  KEY_FWD     364    358    -6  a21.0/ret2023/g80        60.2->60.1
Jordon Sweet              RUC        2043   2037    -6  a24.0/ret2024/g48        90.5->90.3
Jack Buller               KEY_FWD      40     36    -4  a22.0/ret2025/g15        46.2->49.9
Jamarra Ugle-Hagan        KEY_FWD     484    480    -4  a22.0/ret2026/g3         54.0->54.3
Jy Farrar                 KEY_FWD      28     32    +4  a27.0/ret2025/g10        53.7->57.1
Oscar McDonald            KEY_DEF      44     48    +4  a26.0/ret2024/g13        53.7->57.4
Callum Coleman-Jones      KEY_FWD      54     57    +3  a20.0/ret2021/g35        54.6->55.5
Jack Buckley              KEY_DEF     732    729    -3  a24.0/ret2023/g77        71.2->71.2
Darragh Joyce             KEY_DEF       7     10    +3  a27.0/ret2026/g3         50.6->53.0
Jack Silvagni             KEY_DEF     606    609    +3  a26.0/ret2025/g27        67.6->69.7
Angus Sheldrick           MID         802    803    +1  a20.0/ret2025/g33        68.0->69.2
Cameron Rayner            GEN_FWD     478    477    -1  a21.0/ret2022/g118       70.3->70.2
Oscar Allen               KEY_FWD     195    194    -1  a22.0/ret2023/g53        59.0->58.9

## Named rows
- Bailey Smith: base 4344 -> rework 5152  (Δ +808)  lvl 104.84->110.97  gap(rework)={'age_pre': 23.0, 'ret': 2025, 'last': 2023, 'npost': 1, 'gpost': 37}
- Jack Buller: base 40 -> rework 36  (Δ -4)  lvl 46.24->49.85  gap(rework)={'age_pre': 22.0, 'ret': 2025, 'last': 2023, 'npost': 0, 'gpost': 15}
- Darcy Wilmot: base 3544 -> rework 3544  (Δ +0)  lvl 84.32->84.32  gap(rework)=None
