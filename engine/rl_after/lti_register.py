#!/usr/bin/env python3
"""LTI & AVAILABILITY REGISTER CONSUMER (Chapter-3 injury build, 2026-07-09).

The register (`LTI_REGISTER.md`) is OWNER-AUTHORED ground truth, pinned as a versioned engine INPUT
(R-REG=R2). This module is the ENGINE side: it READS the committed register, VALIDATES it (halt-not-warn on
structural errors; report-only on content anomalies — the engine never re-diagnoses a row), and derives the
per-player availability STATE the RL_AVAIL / RL_LTI_RETURN levers consume. It writes NOTHING to the register
and does NO engine pricing math (that lives in _merged_recover.py).

SCHEMA (one row per injury WINDOW; repeat-LTI players get two rows):
    key | player | section (A|B) | window_id | designation | status | returned_year | notes
    designation ∈ {2025, 2026_preseason, 2026}   status ∈ {out_until_2027, may_return_2026, returned}

DERIVED STATE per key (see player_state):
    out        : True if the name is out-for-remainder-2026 (any window not 'returned'; R-iii default OUT)
    section    : 'A' (return-haircut arm applies) | 'B' (return arm STRUCTURALLY ABSENT)
    L          : lost-season fraction 1 − min(g2026/G_FULL, 1)   (the Part-1 present haircut _avail_hc)
    return_arm : section=='A' and out   (Section B never gets the return haircut)
    ret_year   : 2027 for 2026/2026_preseason and default-out 2025 names (flip status→returned to price 2026)
    repeat     : two windows present (fork ii on-sight flag)
"""
import os, re

REGISTER_FILENAME = 'LTI_REGISTER.md'
G_FULL = 22            # season-length games constant; ASSERTED == conditional_prior.SEASON at wire time
VALID_DESIG  = {'2025', '2026_preseason', '2026'}
VALID_STATUS = {'out_until_2027', 'may_return_2026', 'returned'}
_COLS = ['key', 'player', 'section', 'window_id', 'designation', 'status', 'returned_year', 'notes']


def register_path(start=None):
    """Locate the committed register. Search cwd (the bootstrapped workspace rl_after), this file's dir, and
    the repo checkout (RL_REPO/CLAUDE_PROJECT_DIR root). ONE file only (lookalike tripwire enforces that)."""
    cands = [start, os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    for r in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR')):
        if r:
            cands.append(r)
    for c in cands:
        if not c:
            continue
        p = c if c.endswith('.md') else os.path.join(c, REGISTER_FILENAME)
        if os.path.exists(p):
            return p
    return None


def parse(path):
    """Parse the pipe-table body into a list of window dicts (ignores the header + any '###'/'##' prose)."""
    rows = []
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if not s.startswith('|'):
                continue
            cells = [c.strip() for c in s.strip('|').split('|')]
            if len(cells) < len(_COLS):
                continue
            if cells[0] in ('key', ':---', '---') or set(cells[0]) <= {'-', ':'}:
                continue      # header row / md separator
            d = dict(zip(_COLS, cells[:len(_COLS)]))
            try:
                d['window_id'] = int(d['window_id'])
            except ValueError:
                continue
            rows.append(d)
    return rows


def validate(rows, store_keys):
    """Structural validation (HALT via ValueError) + content anomalies (report-only list returned).
    store_keys: a set/dict of keys present in the store exactly once."""
    halts, anomalies = [], []
    seen = {}
    for d in rows:
        k = d['key']
        if k not in store_keys:
            halts.append("unknown register key %r is not in the store (a mis-keyed haircut is worse than none)" % k)
        if d['section'] not in ('A', 'B'):
            halts.append("%s: section must be A|B, got %r" % (k, d['section']))
        if d['designation'] not in VALID_DESIG:
            halts.append("%s: designation %r not in %s" % (k, d['designation'], sorted(VALID_DESIG)))
        if d['status'] not in VALID_STATUS:
            halts.append("%s: status %r not in %s" % (k, d['status'], sorted(VALID_STATUS)))
        seen.setdefault(k, []).append(d['window_id'])
    for k, wins in seen.items():
        if sorted(wins) != list(range(1, len(wins) + 1)):
            halts.append("%s: window_ids must be 1..n contiguous, got %s" % (k, sorted(wins)))
    if halts:
        raise ValueError("LTI REGISTER VALIDATION HALT (halt-not-warn):\n  - " + "\n  - ".join(halts))
    return anomalies


def store_anomalies(rows, store_by_key):
    """Report-only designation-vs-store consistency (the engine LISTS, never re-diagnoses). Returns lines."""
    out = []
    for d in rows:
        p = store_by_key.get(d['key'])
        if not p:
            continue
        yrs = sorted(r['year'] for r in p.get('scoring', []))
        last = max(yrs) if yrs else None
        g26 = next((r['games'] for r in p.get('scoring', []) if r['year'] == 2026), 0)
        if d['designation'] == '2025' and last is not None and last < 2025:
            out.append("%s designated '2025' but last store season is %s (register governs; report-only)" % (d['key'], last))
        if d['designation'] == '2025' and g26 > 0:
            out.append("%s designated '2025' (0 g so far) but store carries %d 2026 games (register governs)" % (d['key'], g26))
        if d['designation'] == '2026' and g26 == 0 and last == 2026:
            out.append("%s designated '2026' but store shows 0 2026 games (register governs; report-only)" % d['key'])
    return out


def player_state(rows_for_key, store_player):
    """Derive the availability state for ONE key from its window row(s) + store record."""
    g26 = next((r['games'] for r in (store_player or {}).get('scoring', []) if r['year'] == 2026), 0)
    section = rows_for_key[0]['section']
    out = any(w['status'] != 'returned' for w in rows_for_key)
    L = 1.0 - min(g26 / float(G_FULL), 1.0)
    ret_year = 2026 if any(w['status'] == 'returned' for w in rows_for_key) else 2027
    return {
        'out': out,
        'section': section,
        'L': max(0.0, L),
        'return_arm': (section == 'A' and out),
        'ret_year': ret_year,
        'repeat': len(rows_for_key) > 1,
        'designations': [w['designation'] for w in rows_for_key],
        'g2026': g26,
    }


def build_state(store_by_key, path=None, report=None):
    """Full pipeline: locate + parse + validate + derive per-key state. Returns {key: state}. HALT (ValueError)
    on structural error or a missing register. `report` (optional list) collects report-only anomaly lines."""
    p = path or register_path()
    if p is None:
        raise ValueError("LTI REGISTER HALT: %s not found (RL_AVAIL is ON but the pinned register is absent — "
                         "re-run bootstrap.sh to seed the workspace)" % REGISTER_FILENAME)
    rows = parse(p)
    validate(rows, store_by_key)
    anoms = store_anomalies(rows, store_by_key)
    if report is not None:
        report.extend(anoms)
    by_key = {}
    for d in rows:
        by_key.setdefault(d['key'], []).append(d)
    return {k: player_state(v, store_by_key.get(k)) for k, v in by_key.items()}


def file_md5(path=None):
    import hashlib
    p = path or register_path()
    if not p:
        return None
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


if __name__ == '__main__':
    import json, sys
    _p = register_path()
    if not _p:
        print("register not found", file=sys.stderr); sys.exit(2)
    _rows = parse(_p)
    print("register: %s  md5=%s  rows=%d  keys=%d" % (_p, file_md5(_p)[:8], len(_rows), len({r['key'] for r in _rows})))
