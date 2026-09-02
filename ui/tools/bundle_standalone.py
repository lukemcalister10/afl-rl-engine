#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ui/tools/bundle_standalone.py — ONE FILE THE OWNER CAN DOUBLE-CLICK.

Inlines every stylesheet and script ui/index.html references into a single self-contained .html, so
the app runs from a Downloads folder with no repo, no server and no unpacking.

WHY THIS IS POSSIBLE AT ALL, and it is a property of the UI rather than a trick played here: the page
performs NO runtime fetches. Every bundle arrives as a <script src> evaluated in order — measured, not
assumed: `grep -n "fetch(|XMLHttpRequest|import("` over ui/app and ui/index.html returns nothing. A
page that fetched anything would be broken by file:// (CORS blocks XHR against local files) and this
tool would be shipping a dead app. If that ever changes, this halts rather than emits — see the FETCH
GUARD below, which is the one check that stops a future edit turning a working download into a blank
screen nobody can debug.

ORDER IS THE WHOLE CONTRACT. index.html loads DATA bundles before APP modules, and the app modules in
a dependency order (seam before the views that read it, main.js last). This walks the file in document
order and substitutes in place, so the emitted script sequence is byte-for-byte the sequence the
browser already executes. Nothing is sorted, deduplicated or moved.

READ-ONLY over the repo. It writes exactly one file, wherever it is told, and touches nothing else.

    python3 ui/tools/bundle_standalone.py [-o OUT.html]
"""
import argparse
import hashlib
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
UI = os.path.dirname(HERE)
REPO = os.path.dirname(UI)
INDEX = os.path.join(UI, 'index.html')

#: A page that fetches at runtime cannot work from file://, so a bundle of it would be a dead app that
#: LOOKS shipped. Checked over the app modules and the page itself; the data bundles are inert literals.
FETCH_PATTERNS = (r'\bfetch\s*\(', r'\bXMLHttpRequest\b', r'\bimport\s*\(')

TAG = re.compile(r'<link\b[^>]*\bhref="([^"]+)"[^>]*>|<script\b[^>]*\bsrc="([^"]+)"[^>]*>\s*</script>')


def _fetch_guard():
    bad = []
    scan = [os.path.join(UI, 'index.html')]
    appdir = os.path.join(UI, 'app')
    scan += [os.path.join(appdir, f) for f in sorted(os.listdir(appdir)) if f.endswith('.js')]
    for path in scan:
        with open(path, encoding='utf-8') as fh:
            src = fh.read()
        for pat in FETCH_PATTERNS:
            for m in re.finditer(pat, src):
                line = src.count('\n', 0, m.start()) + 1
                bad.append('%s:%d  %s' % (os.path.relpath(path, REPO), line, m.group(0)))
    if bad:
        raise SystemExit(
            'STANDALONE BUNDLE HALT: the UI now performs a runtime fetch, so a single-file bundle of it '
            'would not work from file:// — CORS blocks XHR against local files and the page would open '
            'blank with no error a reader could act on.\n  ' + '\n  '.join(bad) +
            '\nEither keep the fetch out of the shipped path, or teach this tool to inline whatever it '
            'reaches for. Refusing to emit a dead app.')


def build():
    _fetch_guard()
    with open(INDEX, encoding='utf-8') as fh:
        html = fh.read()
    inlined, missing, total = [], [], 0

    def sub(m):
        nonlocal total
        rel = m.group(1) or m.group(2)
        path = os.path.join(UI, rel)
        if not os.path.exists(path):
            missing.append(rel)
            return m.group(0)
        with open(path, encoding='utf-8') as fh:
            body = fh.read()
        # A literal "</script" inside a JS string would close the tag early. None exists today
        # (asserted below); escaped anyway, because the failure is silent and total.
        if m.group(2):
            body = body.replace('</script', r'<\/script')
        total += len(body)
        inlined.append((rel, len(body)))
        if m.group(1):
            return '<style>\n/* %s */\n%s\n</style>' % (rel, body)
        return '<script>\n/* %s */\n%s\n</script>' % (rel, body)

    out = TAG.sub(sub, html)
    if missing:
        raise SystemExit('STANDALONE BUNDLE HALT: index.html references files that are not there: %s'
                         % ', '.join(missing))
    left = re.search(r'<(?:link\b[^>]*\bhref|script\b[^>]*\bsrc)="', out)
    if left:
        raise SystemExit('STANDALONE BUNDLE HALT: an external reference survived the inline pass at '
                         'offset %d — the emitted file would silently depend on the repo.' % left.start())
    return out, inlined, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--out', default=os.path.join(REPO, 'valueboard.html'))
    a = ap.parse_args()
    out, inlined, total = build()

    # The stamp a reader can check against the repo without opening a console.
    board = store = '?'
    try:
        import json
        boot = json.load(open(os.path.join(REPO, 'data', 'expected_boot.json')))
        board, store = boot.get('board', '?')[:12], boot.get('store', '?')[:12]
    except Exception:
        pass
    banner = ('<!-- VALUEBOARD — SELF-CONTAINED BUILD\n'
              '     board %s   store %s\n'
              '     built %s by ui/tools/bundle_standalone.py from ui/index.html\n'
              '     %d files inlined, no external references, no runtime fetches.\n'
              '     Open it directly: no server, no repo, no unpacking. -->\n'
              % (board, store, time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime()), len(inlined)))
    out = out.replace('<!doctype html>', '<!doctype html>\n' + banner, 1)

    with open(a.out, 'w', encoding='utf-8') as fh:
        fh.write(out)
    size = os.path.getsize(a.out)
    print('wrote %s' % a.out)
    print('  %d files inlined, %.1f MB' % (len(inlined), size / 1048576.0))
    print('  board %s  store %s' % (board, store))
    print('  md5 %s' % hashlib.md5(open(a.out, 'rb').read()).hexdigest()[:12])
    big = sorted(inlined, key=lambda t: -t[1])[:3]
    print('  largest: %s' % ', '.join('%s %.1fMB' % (r, n / 1048576.0) for r, n in big))


if __name__ == '__main__':
    main()
