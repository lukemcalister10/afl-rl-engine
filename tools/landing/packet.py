"""tools/landing/packet.py — THE DECISION-PACKET TEMPLATE AND ITS SLOT VALIDATOR (PLAN_v6 2a.2).

    tools/land packet --template            print the template
    tools/land packet --check <PACKET.md>   validate a packet against the fixed slots

THE SLOTS ARE FIXED, and the argument is the one `ui/templates/slots.py` already makes for pages and
`tools/claims.py` makes for claims: a free-form packet is prose with headings, and a seat under
pressure writes down what went well. THE SLOT NOBODY FILLED IS THE ONE THAT MATTERED. Fixing the
slots makes an unfilled one VISIBLE — which is a different and much cheaper thing than trusting
everyone to remember.

WHERE THE SLOTS COME FROM. The list is PLAN_v6 2a.2's, verbatim and closed: what changes; who moves
AND who doesn't, by name; cost; standing-table impacts; what-would-make-it-silly; recommendation;
falsifiers. The plan's own rule for adding one is carried into the template: A QUESTION EARNS A
PERMANENT SLOT ONLY WHEN THE OWNER HAS ASKED IT TWICE — so this list does not grow because a seat
thought of something.

THE CONTENT PRECEDENT IS `docs/evidence/d8_ceiling_2026-08-20/PACKET_D8.md`, and the mapping is
worth stating because it is the evidence that the slot list describes a real deliverable rather than
a wish:

    what changes        <- §1 the entanglement and the cut, §2 the wiring (one file, one hunk)
    who moves           <- §4 THE MOVERS LIST, the owner's probation look, by band and by name
    who does NOT move   <- §2 "rl_model.py is byte-unmoved", §2.1 the identity restamp, §5's "no
                           row's ceiling moved DOWN — 0 of 804"
    cost                <- §2.1 / §9's measured figures
    standing tables     <- STANDING_TABLES_NOARB_D8.json and its printed check
    falsifiers          <- §3 THE FALSIFIERS — all six, measured
    open findings       <- §7 findings this seat did not go looking for, §8 what this seat did NOT do

MEASURED, NOT ASSUMED: PACKET_D8 does NOT pass this validator, and that is recorded rather than
smoothed. It predates the template and numbers its sections its own way, so the structural check
reports eight missing headings against it. The slot list is the PLAN's, not D8's; D8 is where the
CONTENT of each slot is shown to exist. Re-heading a filed packet to make an instrument green would
be exactly the re-basing this estate has ruled against.

WHAT THE VALIDATOR CHECKS, AND WHAT IT DOES NOT. It checks STRUCTURE and HONEST FILLING: every slot
present, in order, non-empty, not a dash, not left as template commentary, and — for the two slots
that say "by name" — that names actually appear. It does not and cannot check whether the packet is
TRUE. Judgment review is not retired by anything in PACKAGE 2a and is not touched here.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(HERE, 'PACKET_TEMPLATE.md')

#: (slot key, heading regex, minimum words, needs_names). ORDER IS PART OF THE CONTRACT: a packet
#: that answers "recommendation" before "what would make this silly" is a packet that decided first.
#: The heading patterns are WORD-ANCHORED. An early draft matched `cost` as a prefix and accepted a
#: section headed "Costing" as the cost slot — caught by this module's own self-test, which is the
#: argument for writing the negative control before trusting the instrument.
SLOTS = (
    ('what_changes',    r'^##\s*\d*\.?\s*what changes\b',                     40, False),
    ('who_moves',       r'^##\s*\d*\.?\s*who moves\b',                        20, True),
    ('who_does_not',    r'^##\s*\d*\.?\s*who does\s*not\s*move\b',            20, True),
    ('cost',            r'^##\s*\d*\.?\s*cost\b',                             15, False),
    ('standing_tables', r'^##\s*\d*\.?\s*standing[- ]tables?\b',              20, False),
    ('silly',           r'^##\s*\d*\.?\s*what would make (this|it) silly\b',  25, False),
    ('recommendation',  r'^##\s*\d*\.?\s*recommendation\b',                   15, False),
    ('falsifiers',      r'^##\s*\d*\.?\s*falsifiers\b',                       25, False),
    ('open_findings',   r'^##\s*\d*\.?\s*findings this seat did not\b',        5, False),
)

#: Values that may never fill a slot. Carried from ui/templates/slots.py, whose header explains what
#: a dash costs: the audit found nine live probes reporting "board v=-" and every one rendered
#: cleanly, so nobody investigated.
DASH_SENTINELS = ('-', '--', '—', '–', 'n/a', 'N/A', 'na', 'none', 'tbd', 'TBD', 'todo', 'TODO',
                  'nothing', '?')

_NAME = re.compile(r'`[a-z0-9][a-z0-9._-]*`|\b[a-z]+-[a-z]+\b|\b[A-Z][a-z]+ [A-Z][a-z]+\b')
_COMMENT = re.compile(r'<!--.*?-->', re.S)


class PacketError(RuntimeError):
    pass


def _sections(text):
    """-> [(heading_line, body_text)] for every level-2 heading, in document order."""
    lines = text.splitlines()
    idx = [i for i, ln in enumerate(lines) if ln.startswith('## ')]
    out = []
    for n, i in enumerate(idx):
        end = idx[n + 1] if n + 1 < len(idx) else len(lines)
        out.append((lines[i], '\n'.join(lines[i + 1:end])))
    return out


def validate_text(text, path='(text)'):
    """-> [problems]. Empty means the packet fills every fixed slot honestly."""
    problems = []
    if text.strip().startswith('# PACKET') is False and not re.search(r'^#\s*PACKET', text, re.M):
        problems.append('the packet has no `# PACKET` title line')
    if not re.search(r'\*\*Owner word:\*\*|\*\*Prereg:\*\*', text):
        problems.append('the header names neither the owner word nor the prereg — a packet is a '
                        'decision document and must say what authorised the act and what predicted it')

    secs = _sections(text)
    found_order = []
    for key, pattern, min_words, needs_names in SLOTS:
        hit = None
        for i, (head, body) in enumerate(secs):
            if re.search(pattern, head, re.I):
                hit = (i, head, body)
                break
        if hit is None:
            problems.append('MISSING SLOT %r — no heading matching /%s/i' % (key, pattern))
            continue
        i, head, body = hit
        found_order.append((key, i))
        clean = _COMMENT.sub('', body).strip()
        if not clean:
            problems.append('slot %r is EMPTY. A missing value is a loud failure, never a dash.' % key)
            continue
        if clean.strip().strip('.').strip() in DASH_SENTINELS or \
                clean.strip().lower().strip('.') in [s.lower() for s in DASH_SENTINELS]:
            problems.append('slot %r is filled with %r — a dash sentinel. Fill it or say why the '
                            'question does not arise, in a sentence that a reader can disagree with.'
                            % (key, clean.strip()[:40]))
            continue
        words = len(clean.split())
        if words < min_words:
            problems.append('slot %r has %d words (the floor for this slot is %d). A one-line answer '
                            'to "%s" is the shape of a slot that was filled to pass a check.'
                            % (key, words, min_words, key.replace('_', ' ')))
        if needs_names and not _NAME.search(clean):
            problems.append('slot %r must answer BY NAME and no name appears in it. The plan says '
                            '"who moves AND who doesn\'t (by name)"; a count is a summary of an '
                            'answer, not the answer.' % key)
    # ORDER: the section INDEX of each slot must increase in the slot list's own order. Comparing
    # the key list against itself (an early draft's mistake) can never fail, because found_order is
    # built by iterating SLOTS — the check has to look at where each heading actually sits.
    positions = [i for _k, i in found_order]
    if positions != sorted(positions):
        problems.append('the slots appear out of order (document order: %s). Order is part of the '
                        'contract: a packet that recommends before it states what would make the act '
                        'silly is a packet that decided first.'
                        % ' -> '.join(k for k, _i in sorted(found_order, key=lambda x: x[1])))
    return problems


def validate_file(path):
    with open(path, encoding='utf-8') as fh:
        return validate_text(fh.read(), path)


def render_report(path, problems):
    out = ['=' * 100, 'DECISION-PACKET SLOT CHECK — %s' % path, '=' * 100]
    filled = len(SLOTS) - len([p for p in problems if p.startswith('MISSING SLOT')])
    for key, _pat, _w, _n in SLOTS:
        bad = [p for p in problems if repr(key) in p]
        out.append('  %-4s %-18s %s' % ('OK' if not bad else 'FAIL', key,
                                        bad[0] if bad else 'filled'))
    out.append('')
    for p in problems:
        out.append('  PROBLEM  %s' % p)
    out.append('SLOTS: %d of %d present; %d problem(s)' % (filled, len(SLOTS), len(problems)))
    out.append('VERDICT: %s' % ('GREEN — every fixed slot is filled' if not problems else
                                'RED — the packet does not fill its fixed slots'))
    return '\n'.join(out)


with open(TEMPLATE_PATH, encoding='utf-8') as _fh:
    TEMPLATE = _fh.read()


def selftest():
    """The negative control: a packet missing a slot, or dashing one, MUST fail."""
    ok = bad = 0

    def a(cond, msg):
        nonlocal ok, bad
        if cond:
            ok += 1
            print('  PASS  %s' % msg)
        else:
            bad += 1
            print('  FAIL  %s' % msg)

    good = _EXAMPLE_PACKET
    a(not validate_text(good), 'a fully filled packet validates GREEN')
    a(any('MISSING SLOT' in p for p in validate_text(good.replace('## 4. Cost', '## 4. Costing'))),
      'a packet missing a fixed slot FAILS')
    dashed = re.sub(r'(## 3\. Who does NOT move — by name\n)(.*?)(\n## 4)', r'\1\nn/a\n\3', good, flags=re.S)
    a(any("'who_does_not'" in p for p in validate_text(dashed)),
      'a slot filled with a dash sentinel FAILS')
    nameless = re.sub(r'(## 2\. Who moves — by name\n)(.*?)(\n## 3)',
                      r'\1\neight rows moved up and none moved down across the whole board today\n\3',
                      good, flags=re.S)
    a(any("'who_moves'" in p and 'BY NAME' in p for p in validate_text(nameless)),
      'a by-name slot answered only with a count FAILS')
    swapped = good.replace('## 6. What would make this silly', '## Z_TMP') \
                  .replace('## 7. Recommendation', '## 6. What would make this silly') \
                  .replace('## Z_TMP', '## 7. Recommendation')
    a(any('out of order' in p for p in validate_text(swapped)),
      'slots out of order FAIL (recommendation before what-would-make-it-silly)')
    print('')
    print('PACKET SELF-TEST: %d PASS / %d FAIL' % (ok, bad))
    return 1 if bad else 0


#: A WORKED EXAMPLE, assembled from the F5 rounding act's own recorded evidence
#: (docs/evidence/f5_and_sort_2026-08-20/FINAL_STATE.md). It is a FIXTURE for the negative control
#: below, not a filed packet: no packet in this shape was delivered to the owner for that act.
_EXAMPLE_PACKET = """# PACKET — THE EXAMPLE ACT (a worked fixture, not a filed packet)

**Seat:** example · **Date:** 2026-08-20 · **Base:** `main` @ `0000000` · **Prereg:** `PREREG.md`
**Owner word:** "launch the ready items please"

## 1. What changes
One statement in `engine/rl_after/rl_export.py`, the exporter, inside the F5 seal boundary. The parts
become the primitive and the integer total is definitionally their sum, never rounded a third time.
No valuation code is touched, no manifest dial is added, and `engine/rl_after/rl_model.py` is
byte-unmoved. The declared entrant layer moves 56772 to 56773 and nothing else in the block moves.

## 2. Who moves — by name
`f5_entrant_layer_pvc` at both forward lenses, `phantomTotals._meta.entrant_layer_pvc`, the seal id
`cbb7c431` to `ccc26a9e`, and league `delta` / `entrantValue` / `withPhantom` at lenses 1 and 2. Ten
fields, all report-only. charlie-dean and jacob-bauer are unaffected and are named because a reader
of the prior probe would look for them.

## 3. Who does NOT move — by name
All 804 active rows (`v`, `vM2`, `vM1`, `vP1`, `vP2`) and all 198 back rows are byte-identical,
measured by full recursive diff. Lens 0, the balanced board, holds at 692,296 — the k=0 zero-phantom
invariant. PICK 1 stays the numeraire at 3,000. `store` b745002e, `engine_head` 1867e953, `config`,
`rl_model`, `fv`, `register` and `balanced_board_md5` are all unmoved, each re-measured from the
checkout rather than read back from the manifest.

## 4. Cost
Measured, not estimated: three bare builds at 100.5s, 100.3s and 101.3s, the landing transaction at
just under four minutes, and the full gate set at four and a half. One seat-session end to end.

## 5. Standing-table impacts
The published standing tables are unmoved: the ladder, the residual table and the parts table were
each re-derived from the new board and compared cell for cell against the control build. The no-arb
page moves only where the entrant layer prints, which is the report-only block named in slot 1.

## 6. What would make this silly
If the declared layer is a display artifact nobody reads, this is a day spent moving a number that
changes no decision. The case against is that the true defect is the three-independent-roundings
pattern, and fixing one boundary while the pattern lives elsewhere buys a clean board and a false
sense that the class is closed.

## 7. Recommendation
Land it as its own isolated act with its own prereg. This seat is not asking for the book re-seal,
which stays owner-pending, and is not asking for the AGE_REF residue to be ruled here.

## 8. Falsifiers
F1 the control build reproduces the pre-act board exactly — met, so every later diff is attributable.
F2 dev equals canonical byte for byte — met. F3 no player value moves — met, 804 of 804 and 198 of
198 byte-identical. F4 lens 0 unmoved — met. F5 the diff is exactly the predicted ten fields — met.
F6 the strengthened cross-check is non-vacuous, proved in both directions.

## 9. Findings this seat did not go looking for
`r15_ladder_survival_proof.py` cannot run on this tree (`KeyError: 'GFWD'`), proved pre-existing from
a clean worktree. Referred, not repaired.
"""
