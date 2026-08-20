"""acceptance/known_red.py — read the RULED-RED ledger, and refuse to let it go stale.

See acceptance/ruled_red.json for the ledger itself and the rules for adding to it.

The two functions here are the whole mechanism:

    classify(halted)    given the carriers a check found halted, decide whether the drift is
                        entirely covered by presented rulings (-> RULED-RED) or contains at least
                        one carrier nobody has ruled on (-> FAIL).

    stale(halted)       the other direction, and the one that matters more over time: which ledger
                        entries no longer describe anything real. A known-red list is only honest
                        while it is still true, and nothing decays faster than a list of things
                        that were broken once.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, 'ruled_red.json')


def load(path=None):
    with open(path or LEDGER, encoding='utf-8') as fh:
        return json.load(fh).get('entries') or []


def covering_entry(carrier, entries=None):
    """The presented ruling that covers this carrier, or None."""
    for e in (entries if entries is not None else load()):
        if carrier in (e.get('carriers') or ()):
            return e
    return None


def classify(halted_carriers, entries=None):
    """Split halted carriers into (ruled, unruled).

    `ruled` is [(carrier, entry)]; `unruled` is [carrier]. A check whose drift is entirely `ruled`
    reports RULED-RED and does not red the run — the fork is already with the owner and the seat's
    job is to leave it alone. A check with ANY unruled carrier reports FAIL, no matter how many of
    its other carriers are excused. One un-presented drift is a red; being mostly-known is not a
    defence.
    """
    entries = entries if entries is not None else load()
    ruled, unruled = [], []
    for carrier in halted_carriers:
        e = covering_entry(carrier, entries)
        (ruled.append((carrier, e)) if e else unruled.append(carrier))
    return ruled, unruled


def stale(halted_carriers, entries=None):
    """Ledger entries that describe drift which is no longer measurable — i.e. entries to RETIRE.

    An entry goes stale when EVERY carrier it names has become coherent. That is good news about
    the tree and bad news about the ledger, and the runner treats it as a FAIL so the good news
    gets acted on instead of accumulating. An entry whose carriers are only PARTLY repaired is not
    stale — it is still doing real work for the rest.
    """
    entries = entries if entries is not None else load()
    live = set(halted_carriers)
    return [e for e in entries if not (set(e.get('carriers') or ()) & live)]
