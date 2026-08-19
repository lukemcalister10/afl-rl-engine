#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE STANDING "WHAT IS IN THIS BOARD AND WHAT IS STILL BROKEN" BOX.

One object, imported by every owner document, so the three pages cannot drift apart and so nothing
that is broken can be on one page and missing from another. PLAIN WORDS ONLY.
"""

TITLE = 'WHAT IS IN THIS BOARD, AND WHAT IS STILL BROKEN'

IN_IT = [
    ('The pedigree-conditional charge (ORDER P)',
     'a player is charged against a bar set by what his entry price implies, not by games alone.'),
    ('FIX A — the pick reversal repaired',
     'a more expensive row can no longer come out cheaper than a less expensive one on the same play.'),
    ('B1 — the age-24 cliff deleted',
     'the charge runs at every age on the same bar instead of switching off at a birthday.'),
    ('The mature refit',
     'each season is measured against the ruler for the age it was actually played at.'),
    ('The compressed cap at the 20th percentile',
     'the old hard ceiling is replaced by a smooth one, so worse play always costs at least '
     'slightly more and nobody sits on a flat segment.'),
    ('The softened slope 0.105',
     'the charge responds less steeply to shortfall, inside the measured interval.'),
    ('Recency 0.47',
     'a season two years ago counts less than this one; the weight was fitted out of sample.'),
    ('The SD level offset, 2.98 points a game',
     'small defenders were measured to be over-barred by that much, flat at every age, and the bar '
     'is lowered by exactly the measured amount. Nothing was moved to offset it.'),
    ('The deep sitter schedule is KEPT AS MEASURED — the rise at depth 4 stays',
     'The sitting clock is counted as a DEPTH. The measured schedule falls from depth 1 to depth 3 '
     'and then RISES at depth 4, so a player standing at depth 4 who is still on a list is priced '
     'slightly above one standing at depth 3. That is not a glitch: clubs cut the sitters at depths '
     '2 and 3 who are not up to it, so a player still contracted at depth 4 has survived a cut that '
     'others did not, and that survival is itself a signal. The depth-4 cell is thin — eleven '
     'players — and stays documented as thin. ONE CONSEQUENCE, STATED PLAINLY: because the schedule '
     'rises there, anything that pulls a player DOWN across that rise (an injury pause, a returning '
     'season) can lower his price rather than raise it. One row on this board does exactly that.'),
    ('The absence package',
     'a short season now earns the credit it was measured to earn instead of a full pass at two '
     'games; a delivered season restores only part of the accrued sitting clock instead of wiping '
     'it; a logged-injured absence pauses the clock for a player who has delivered; and the '
     'production leg fades when a player is out for more than one season with no explanation.'),
]

BROKEN = [
    ('MODERN PICKS 1-10 — A DOCUMENTED STANDING RED',
     'This cell fails the no-arb test even on the loosened reading, and NO LEVER IN THIS BOARD '
     'REACHES IT. It was inherited from ORDER P, the level cannot fix it, and the recency dial '
     'structurally cannot. THE OWNER HAS ACCEPTED IT AS A STANDING RED: it rides every table '
     'flagged, it is not chased and it is not capped. It is printed on every page for that reason.'),
    ('SSP — an inherited breach, worsened',
     'The supplementary-selection arm was already breaching before this board and ORDER P made it '
     'worse. IT IS NOT REPAIRED HERE. It is parked, named, and reported separately so it cannot be '
     'read as fixed.'),
    ('THE TAIL CALIBRATION — READ THE BUILT NUMBER, NOT THE ESTIMATE',
     'The charge on the worst underperformers is measured against what they actually went on to '
     'deliver. The compression anchor was moved to the 15th percentile precisely to bring this back '
     'toward 1.00 after the 20th-percentile version read 0.74. THE BUILT NUMBER FOR THIS BOARD IS '
     'PRINTED IN THE PACKET AND IT RULES; no other dial was touched to chase it. What has NOT '
     'changed is the shape of the evidence: the deep cell is option-shaped, about half of those '
     'players deliver almost nothing and a few deliver a lot, so the typical one is charged more '
     'generously than the average one.'),
    ('RUCK IS STILL MIS-BARRED AND NOTHING WAS DONE ABOUT IT',
     'Rucks measure 5.57 points a game over-barred, but the error SWINGS with age — heavily '
     'over-barred at 21, slightly under-barred at 23 — so it is not a level and a level offset '
     'would have been wrong at both ends. The misfiring object is the class-pooled age-development '
     'delta, which rucks share with key forwards and key defenders. It is diagnosed, not repaired, '
     'and THE REPAIR IS PARKED FOR AFTER THIS CANDIDATE by owner ruling. It rides the tables flagged, '
     'exactly like the modern 1-10 red.'),
    ('SF WAS DELIBERATELY LEFT ALONE',
     'Small forwards measure UNDER-barred by 2.71, which would mean charging them more. It was not '
     'wired, because the measurement carries a survivor-bias caveat and it would penalise exactly '
     'the kind of row this engine has most trouble with.'),
    ('THE VETERAN BOARD HAS NOT BEEN TESTED AGAINST THIS ONE',
     'A separate veteran-board change was built before B1 existed. B1 moves a lot of mature rows. '
     'Nobody has yet looked at the two together, and that must happen before the veteran board '
     'goes in behind this one.'),
    ('THE CHARGE STILL CONVICTS SOMEWHAT FAST ON VERY FEW GAMES',
     'A player with one or two games is charged on less evidence than the outcomes support. It was '
     'measured, it was left alone deliberately — repairing it would reopen the level the whole '
     'board is anchored on — and it stays on the record as an open finding.'),
    ('THE DEEP CELL IS OPTION-SHAPED, AND THE MEAN HIDES THAT',
     'Among the worst underperformers, about half deliver almost nothing and a few deliver a lot. '
     'The board prices the average, which is the right thing for a price, but the typical player in '
     'that group is charged GENEROUSLY rather than harshly.'),
]

FOOT = ('This board is a CANDIDATE FOR REVIEW. It has not been adopted, it has not been merged, and '
        'the live board is untouched.')


def html_box(css_class='box'):
    h = ['<div class="%s">' % css_class, '<h3>%s</h3>' % TITLE,
         '<p class="boxsub">What this board now does that the last one did not:</p><ul>']
    for a, b in IN_IT:
        h.append('<li><b>%s</b> — %s</li>' % (a, b))
    h.append('</ul><p class="boxsub boxred">What is still broken, in plain words:</p><ul>')
    for a, b in BROKEN:
        h.append('<li><b>%s</b> — %s</li>' % (a, b))
    h.append('</ul><p class="boxfoot">%s</p></div>' % FOOT)
    return '\n'.join(h)


BOX_CSS = """
.box{border:1px solid var(--line);border-left:4px solid var(--acc);background:var(--hd);
     padding:14px 18px;margin:0 0 22px;border-radius:0 6px 6px 0;max-width:78em}
.box h3{margin:0 0 8px;font-size:14px;letter-spacing:.03em}
.box ul{margin:4px 0 10px;padding-left:20px}
.box li{margin:3px 0;font-size:13px;line-height:1.45}
.boxsub{margin:8px 0 2px;font-weight:600;font-size:13px}
.boxred{color:var(--dn)}
.boxfoot{margin:10px 0 0;font-size:12px;color:var(--mut);font-style:italic}
"""
