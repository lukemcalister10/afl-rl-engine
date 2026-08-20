"""acceptance/checks/ledger.py — the RULED-RED ledger's own liveness check.

ONE registered check, `ruled_red_ledger`, and it exists because of a single sentence in the review
record (REVIEW_COLD_OPUS.md O1): *the workflow-step keys must bring a liveness probe with them, or
the extension loses the self-expiry that is the ledger's entire value.*

Carrier entries police themselves — `known_red.stale()` runs inside the manifest check, and an
entry whose carriers went coherent reds the run there. Step entries have no carrier to go coherent,
so their liveness has to be ASKED, and this check is the asking. It runs every step entry's declared
probe and reds the run on any answer other than "still failing, the recorded way":

    EXPIRED   the probe now succeeds        the step is fixed; the entry is a lie by omission
    DRIFTED   it fails, but differently     the ruling was given about a red that no longer exists
    UNPROBED  a heavy probe out of window   nobody has measured this inside its own declared window
    BROKEN    the probe cannot be run       an unprobeable entry can never expire, so it is refused

This check HALTS NO CARRIER. It is a statement about the ledger, not about the tree, and nothing
downstream reads it.
"""

import os

from acceptance import contract as C
from acceptance import known_red as K

#: heavy probes run only when the caller says so — see known_red.probe's UNPROBED branch for what
#: happens the rest of the time (a dated measurement, and a red when the date leaves its window).
_HEAVY_ENV = 'RL_ACCEPT_HEAVY'

_BAD = (K.EXPIRED, K.DRIFTED, K.UNPROBED, K.BROKEN)


def check(ctx):
    """every step-keyed RULED-RED entry is still failing, the way its ruling says it fails."""
    run_heavy = os.environ.get(_HEAVY_ENV) == '1'
    entries = K.load()
    results = K.probe_all(entries, root=ctx.root, run_heavy=run_heavy)

    lines = ['RULED-RED LEDGER — step-keyed entries and their expiry probes',
             '  tree: %s   heavy probes: %s' % (ctx.root, 'RUN' if run_heavy else 'dated'),
             '']
    bad = []
    for entry, state, detail in results:
        lines.append('%-34s %-12s %s' % (entry.get('id'), state, detail))
        for s in entry.get('steps') or ():
            lines.append('%-34s %-12s %s' % ('', '', 'step: ' + s))
        lines.append('')
        if state in _BAD:
            bad.append((entry.get('id'), state, detail))

    carrier_only = [e.get('id') for e in entries if not e.get('steps')]
    if carrier_only:
        lines.append('carrier-keyed entries (policed by the manifest check, not here): %s'
                     % ', '.join(carrier_only))
    ev = C.write_evidence(ctx, 'ruled_red_ledger.txt', '\n'.join(lines))

    if not results:
        return C.Verdict('ruled_red_ledger', C.PASS, ev,
                         'no step-keyed RULED-RED entries — nothing to keep honest')
    if bad:
        first = bad[0]
        return C.Verdict('ruled_red_ledger', C.FAIL, ev,
                         '%d of %d step entries no longer describe reality — %s is %s: %s'
                         % (len(bad), len(results), first[0], first[1], first[2]))
    return C.Verdict('ruled_red_ledger', C.PASS, ev,
                     '%d step entries probed, all still failing exactly as their ruling records'
                     % len(results))


check.HALTS = ()
check.PROFILE = 'host-insensitive'
