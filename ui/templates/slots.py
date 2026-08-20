"""ui/templates/slots.py — THE SLOT CONTRACT. Seats inject data, never layout.

    from ui.templates import slots
    html = slots.render('tracker', {'as_of_round': 22, 'rows': [...], ...})

--------------------------------------------------------------------------------------------------
THE LAYOUT LAW (M1a deliverable 5)

    A SEAT INJECTS DATA. A SEAT NEVER INJECTS LAYOUT.

Every owner-facing page in this estate has been produced by a generator that owned BOTH its numbers
and its markup, and every act that touched a page therefore re-derived the page. The consequences
are visible across the evidence tree: the same table appears with different column orders, different
headers for the same quantity, and a different set of columns depending on which act last built it.
That is not a styling complaint — a column that silently changes meaning between two builds is a
correctness problem, and comparing two such pages is how a reader reaches a wrong conclusion
carefully.

These skeletons freeze the LAYOUT of the five owner-facing pages, extracted from the canonical
assembly-era pages of 2026-08-19. A seat supplies values for named slots. It cannot move a column,
rename a header, or drop a row block, because it never touches the markup at all.

--------------------------------------------------------------------------------------------------
THE ONE RULE THAT MATTERS MORE THAN THE REST

    A MISSING VALUE IS A LOUD FAILURE. IT IS NEVER A DASH.

This is not a stylistic preference either. The audit measured what a dash costs. AUDIT_CI.md section
1.1, on nine failing self-test probes:

    "9 x the #326 per-division pool-entry non-vacuity family — every one reports `board v=-`, i.e.
     the probe cannot reach a live entrant's board price at all (`0 of 14`, `0 of 28`, `0 of 16`)."

A dash is what a broken pipeline looks like when it is pretending to work. It renders, it aligns, it
sorts, and it says nothing — so nobody investigates, and the gap survives until someone happens to
ask why a column is empty. `render()` therefore refuses: an absent slot, a None, an empty string, or
any of the dash sentinels below HALTS with the template, the slot, and the row index named. A page
that cannot be filled honestly does not get produced.

The sentinels are rejected as VALUES, not as characters. A page may legitimately contain a dash in
prose or in a fixed header; what it may not do is fill a data slot with one and call it rendered.
Where "no value" is genuinely meaningful — a player with no draft pick — the slot manifest marks
that slot `nullable` and the seat must pass the explicit sentinel `slots.ABSENT`, which renders as
the page's own empty-marker. The difference between "we have no value for this" and "we could not
get a value for this" is the entire point, and it must be stated by the caller, not inferred from a
falsy variable.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, 'manifest.json')

#: Values that may never fill a data slot. A pipeline that produces one of these has failed.
DASH_SENTINELS = ('-', '--', '—', '–', 'n/a', 'N/A', 'na', 'null', 'None', 'nan', 'NaN', '?', 'TBD')


class ABSENT_TYPE(object):
    """The EXPLICIT 'this row genuinely has no such value' marker.

    Passing this is a positive statement by the caller. It is the only way a nullable slot renders
    empty, and it is deliberately not spelled `None` — `None` is what a bug produces, and the whole
    contract turns on being able to tell the two apart.
    """
    __slots__ = ()

    def __repr__(self):
        return 'slots.ABSENT'


ABSENT = ABSENT_TYPE()


class SlotError(RuntimeError):
    """A slot could not be filled honestly. Fail closed — never render, never substitute a dash."""


# ------------------------------------------------------------------------------------- the parser
# CASE-SENSITIVE, and that is not incidental: the frozen tracker/players/year1 layouts carry columns
# literally named K, P and R. The first draft of this pattern was lowercase-only, so those three were
# not recognised as slots at all — never validated, never filled, and `{{K}}` shipped verbatim into
# the rendered page. selftest.py PART C caught it on the first run ("no unfilled slot markers survive
# into the output"), which is the entire argument for writing the self-test before trusting the tool.
_SCALAR = re.compile(r'\{\{([A-Za-z0-9_.]+)\}\}')
_BLOCK = re.compile(r'\{\{#rows:([a-z0-9_]+)\}\}(.*?)\{\{/rows\}\}', re.S)


def _load_manifest():
    with open(MANIFEST, encoding='utf-8') as fh:
        return json.load(fh)


def template_path(name):
    return os.path.join(HERE, '%s.html' % name)


def parse(name):
    """Return (text, scalar_slots, {list_name: (block_text, [column_slots])}) for a template."""
    with open(template_path(name), encoding='utf-8') as fh:
        text = fh.read()
    blocks = {}
    for list_name, body in _BLOCK.findall(text):
        blocks[list_name] = (body, sorted(set(_SCALAR.findall(body))))
    outside = _BLOCK.sub('', text)
    return text, sorted(set(_SCALAR.findall(outside))), blocks


def _reject(value, where, nullable=False):
    """The single place a value is judged fit to render. Everything else delegates here."""
    if value is ABSENT:
        if nullable:
            return                               # an explicit, DECLARED absence — allowed
        raise SlotError('%s is slots.ABSENT, but that slot is not declared nullable in '
                        'manifest.json. Absence must be DECLARED, in the manifest, once — not '
                        'asserted ad hoc by whichever seat happened not to have the value.' % where)
    if value is None:
        raise SlotError('%s is None. A missing value is a loud failure, never a dash. If this row '
                        'genuinely has no such value, pass slots.ABSENT and mark the slot nullable '
                        'in manifest.json — say it, do not let it be inferred from a falsy variable.'
                        % where)
    s = str(value).strip()
    if s == '':
        raise SlotError('%s is empty. A missing value is a loud failure, never a dash.' % where)
    if s in DASH_SENTINELS:
        raise SlotError('%s is %r — a dash sentinel. This is exactly the failure mode the contract '
                        'exists to prevent: the audit found nine live probes reporting "board v=-" '
                        'because they could not reach a value at all, and every one of them '
                        'rendered cleanly. Fix the pipeline, or declare the slot nullable and pass '
                        'slots.ABSENT.' % (where, s))


def validate(name, data, manifest=None):
    """Check `data` fills every slot of template `name`. Returns [] or a list of problems.

    Deliberately collects ALL problems rather than raising on the first: a seat wiring up a new page
    should learn every slot it is missing in one run, not one per attempt.
    """
    man = (manifest or _load_manifest())[name]
    nullable = set(man.get('nullable') or ())
    allow_empty = set(man.get('allow_empty_lists') or ())
    _text, scalars, blocks = parse(name)
    problems = []

    declared = set(man.get('slots') or ())
    found = set(scalars) | {'%s[].%s' % (ln, c) for ln, (_b, cols) in blocks.items() for c in cols}
    found |= set(blocks)
    # The manifest and the markup must agree. A template slot nobody declared is a slot nobody
    # validates, and a declared slot with no markup is a value the page silently drops.
    for extra in sorted(found - declared):
        problems.append('template declares slot %r that manifest.json does not' % extra)
    for missing in sorted(declared - found):
        problems.append('manifest.json declares slot %r that the template does not use' % missing)

    for s in scalars:
        if s not in data:
            problems.append('missing slot %r' % s)
            continue
        try:
            _reject(data[s], 'slot %r' % s, s in nullable)
        except SlotError as e:
            problems.append(str(e))

    for list_name, (_body, cols) in blocks.items():
        rows = data.get(list_name)
        if rows is None:
            problems.append('missing row list %r' % list_name)
            continue
        if not isinstance(rows, (list, tuple)):
            problems.append('row list %r is %s, not a list' % (list_name, type(rows).__name__))
            continue
        if not rows and list_name not in allow_empty:
            problems.append('row list %r is EMPTY. An empty table is indistinguishable from a '
                            'broken query; declare it in allow_empty_lists if emptiness is a real '
                            'and expected state for this page.' % list_name)
        for i, row in enumerate(rows):
            for c in cols:
                if c not in row:
                    problems.append('row %d of %r is missing column %r' % (i, list_name, c))
                    continue
                try:
                    _reject(row[c], 'row %d of %r column %r' % (i, list_name, c),
                            '%s[].%s' % (list_name, c) in nullable)
                except SlotError as e:
                    problems.append(str(e))
    return problems


def _esc(v):
    if v is ABSENT:
        return '<span class="absent" title="no value exists for this row">&middot;</span>'
    return (str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def render(name, data, manifest=None):
    """Validate, then fill. Raises SlotError with EVERY problem if the page cannot be filled."""
    problems = validate(name, data, manifest)
    if problems:
        raise SlotError('template %r cannot be rendered honestly — %d problem(s):\n  - %s'
                        % (name, len(problems), '\n  - '.join(problems)))
    text, _scalars, blocks = parse(name)

    def _expand(m):
        list_name, body = m.group(1), m.group(2)
        return ''.join(_SCALAR.sub(lambda c, r=row: _esc(r[c.group(1)]), body)
                       for row in data[list_name])

    text = _BLOCK.sub(_expand, text)
    return _SCALAR.sub(lambda m: _esc(data[m.group(1)]), text)


def names():
    """The declared templates. Keys beginning with '_' are the manifest's own prose, not pages."""
    return sorted(k for k in _load_manifest() if not k.startswith('_'))
