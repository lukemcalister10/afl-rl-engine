"""acceptance/known_red.py — read the RULED-RED ledger, and refuse to let it go stale.

See acceptance/ruled_red.json for the ledger itself and the rules for adding to it.

THE LEDGER KEYS TWO KINDS OF THING (schema 2, PLAN_v6 1a).

  CARRIERS  — a named upstream fact (`release_contract:engine_head`). Schema 1, unchanged. A
              carrier entry expires by MEASUREMENT: the carrier becomes coherent, the entry stops
              matching, and the runner FAILS on the stale entry itself.

  STEPS     — a WORKFLOW STEP or a named check (`ci-guards.yml::Guards 1/2/3/5 …`,
              `acceptance::rulebook_lint`). Added here because 1a arms loud-red on workflow steps
              and a workflow step HAS no carrier: keyed the old way it would have matched nothing,
              been reported stale on entry one, and reded the runner for existing.

THE EXPIRY PROBE — the acceptance criterion for this extension (REVIEW_COLD_OPUS.md O1, verbatim:
*"a workflow-step entry expires when its step stops failing"*). A carrier entry gets its liveness
free, because coherence is a thing you can read off a file. A step entry does not: nothing about a
committed workflow file says whether its step still fails. So EVERY step entry MUST carry a
`probe` — an argv the ledger runs to ask the step "are you still broken?" — and the four answers
are the whole mechanism:

    LIVE        the probe still fails, with the recorded signature      -> RULED-RED stands
    EXPIRED     the probe now SUCCEEDS                                  -> FAIL: retire the entry
    DRIFTED     the probe still fails, but NOT the recorded way         -> FAIL: re-adjudicate
    UNPROBED    a `heavy` probe not run within `probe_max_age_days`     -> FAIL: nobody has looked

UNPROBED is the one that matters over time, and it is why `probe_max_age_days` is mandatory on a
heavy entry. A cheap probe runs on every runner invocation and cannot rot. A heavy probe (one that
needs a board build, a seeded workspace, a GitHub runner) cannot run on every invocation, so the
ledger demands a DATED probe result instead and reds when that date goes out of window. An entry
nobody has re-measured inside its own declared window is exactly the panel-10/10 failure mode the
`_self_expiry` note names, and it fails here rather than being believed.
"""

import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, 'ruled_red.json')
ROOT = os.path.dirname(HERE)

#: probe states
LIVE, EXPIRED, DRIFTED, UNPROBED, BROKEN = 'LIVE', 'EXPIRED', 'DRIFTED', 'UNPROBED', 'BROKEN-PROBE'


def load(path=None):
    with open(path or LEDGER, encoding='utf-8') as fh:
        return json.load(fh).get('entries') or []


# ------------------------------------------------------------------------------ carriers (schema 1)
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
    """CARRIER entries that describe drift which is no longer measurable — i.e. entries to RETIRE.

    An entry goes stale when EVERY carrier it names has become coherent. That is good news about
    the tree and bad news about the ledger, and the runner treats it as a FAIL so the good news
    gets acted on instead of accumulating. An entry whose carriers are only PARTLY repaired is not
    stale — it is still doing real work for the rest.

    ONLY entries that DECLARE carriers are considered. A step entry declares none, and reading its
    empty carrier list as "all its carriers are coherent" would report every step entry stale the
    moment it was written — the exact defect the schema-2 extension had to avoid.
    """
    entries = entries if entries is not None else load()
    live = set(halted_carriers)
    return [e for e in entries
            if (e.get('carriers') or ()) and not (set(e['carriers']) & live)]


# --------------------------------------------------------------------------------- steps (schema 2)
def step_entries(entries=None):
    """Every entry that keys a workflow step / named check rather than a carrier."""
    return [e for e in (entries if entries is not None else load()) if e.get('steps')]


def covering_step_entry(step_id, entries=None):
    """The presented ruling that covers this step id, or None."""
    for e in step_entries(entries):
        if step_id in e['steps']:
            return e
    return None


def _iso_days_ago(stamp):
    """Whole days between `stamp` (YYYY-MM-DD) and today, or None if unreadable."""
    try:
        t = time.mktime(time.strptime(str(stamp)[:10], '%Y-%m-%d'))
    except (ValueError, TypeError):
        return None
    return int((time.time() - t) // 86400)


def probe(entry, root=None, run_heavy=False, timeout=None):
    """Ask one step entry's probe whether its step still fails. -> (state, detail).

    The probe is declared BY THE ENTRY, not by this module — a ledger that hard-codes how to test
    each red is a second implementation of every red it carries. This function only runs what the
    entry declares and reads the answer off the exit code plus the recorded signature.
    """
    p = entry.get('probe') or {}
    argv = p.get('argv')
    if not argv:
        return BROKEN, 'entry %r declares steps but no probe.argv — an unprobeable step entry ' \
                       'cannot expire, so it is refused' % entry.get('id')
    heavy = (p.get('cost') or 'cheap').lower() == 'heavy'
    if heavy and not run_heavy:
        age = _iso_days_ago(p.get('last_probed'))
        maxage = p.get('probe_max_age_days')
        if age is None or maxage is None:
            return UNPROBED, 'heavy probe not run this invocation and entry %r carries no readable ' \
                             'probe.last_probed / probe.probe_max_age_days' % entry.get('id')
        if age > int(maxage):
            return UNPROBED, 'heavy probe last measured %s (%d days ago), window is %s days — ' \
                             're-measure or retire' % (p.get('last_probed'), age, maxage)
        return LIVE, 'heavy probe: last measured %s (%d days ago, window %s) — %s' \
                     % (p.get('last_probed'), age, maxage, p.get('last_result') or 'still failing')
    root = root or ROOT
    # A PROBE MUST NOT CHANGE WHAT IT MEASURES, and the environment is part of that. Anything a
    # probe child inherits that config_manifest.enforce() would reject as an unknown RL_*/PAR_*
    # override makes the child fail for OUR reason instead of its own. The entry may declare the
    # env the real step runs under; nothing else about this process's env is invented for it.
    env = dict(os.environ)
    for k in list(env):
        if k.startswith(('RL_ACCEPT', 'SGC_')):
            env.pop(k, None)
    env['RL_REPO'] = root
    env.update({str(k): str(v) for k, v in (p.get('env') or {}).items()})
    try:
        r = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                           timeout=timeout or int(p.get('timeout_s') or 300),
                           env=env)
        out = (r.stdout or '') + (r.stderr or '')
        rc = r.returncode
    except subprocess.TimeoutExpired:
        return DRIFTED, 'probe TIMED OUT after %ss — the recorded failure was fast; a hang is a ' \
                        'different fact and needs re-adjudication' % (p.get('timeout_s') or 300)
    except OSError as e:
        return BROKEN, 'probe could not be run: %s' % e
    if rc == 0:
        return EXPIRED, 'the probe now SUCCEEDS (exit 0) — the step has stopped failing, so this ' \
                        'entry no longer describes anything real. RETIRE IT.'
    sig = p.get('match')
    if sig and sig not in out:
        return DRIFTED, 'probe still fails (exit %d) but the recorded signature %r is GONE — the ' \
                        'red changed underneath the ruling' % (rc, sig)
    return LIVE, 'probe still fails (exit %d)%s' % (rc, ', signature matched' if sig else '')


def probe_all(entries=None, root=None, run_heavy=False):
    """-> [(entry, state, detail)] for every step entry, in ledger order."""
    return [(e,) + probe(e, root=root, run_heavy=run_heavy) for e in step_entries(entries)]
