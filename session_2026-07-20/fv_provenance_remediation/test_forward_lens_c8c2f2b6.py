#!/usr/bin/env python3
"""FORWARD-LENS ORACLE — GENERATED ARTIFACT. DO NOT EDIT BY HAND.

Regenerated in full by the advance transaction (engine/rl_after/ingestion/sibling_repin.py, ITEM 408 D2)
on every advance, from the freshly built sibling board. Every literal below was DERIVED from that build;
none was authored, transcribed or carried over from a previous round. Editing this file by hand makes it
disagree with the artifact it gates and the advance transaction will HALT on the next plan/check.

It gates the committed forward reference vector on the round's OWN board identity. It contains no
historical board id: forward_vector_c8c2f2b6.json and the identity below are this round's.

Run:  python3 test_forward_lens_c8c2f2b6.py      (exit 0 == the committed forward view matches this oracle)
"""
import hashlib
import json
import os
import sys

FORWARD_BOARD_MD5_GOOD = 'c8c2f2b6f99445484fadaa8c44afe609'
FORWARD_REFERENCE = 'forward_vector_c8c2f2b6.json'
FORWARD_VECTOR_SHA256 = '91f53f752234bb1030326e8a2622915327cb6b8d9fd5c47575204fb58f2e51ae'

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, 'fixtures')


def _lens(doc, label):
    return (doc.get('lenses') or {}).get(label) or {}


def main():
    path = os.path.join(FIXTURES, FORWARD_REFERENCE)
    if not os.path.exists(path):
        print('FORWARD ORACLE FAIL: %s missing' % FORWARD_REFERENCE)
        return 1
    doc = json.load(open(path, encoding='utf-8'))
    fails = []
    if doc.get('board_md5') != FORWARD_BOARD_MD5_GOOD:
        fails.append('board_md5 %s != oracle %s' % (doc.get('board_md5'), FORWARD_BOARD_MD5_GOOD))
    if doc.get('active') != 804:
        fails.append("doc.get('active') %r != 804" % doc.get('active'))
    if _lens(doc, '+1').get('sum') != 640876:
        fails.append("lens('+1').get('sum') %r != 640876" % _lens(doc, '+1').get('sum'))
    if _lens(doc, '+2').get('sum') != 205147:
        fails.append("lens('+2').get('sum') %r != 205147" % _lens(doc, '+2').get('sum'))
    if _lens(doc, '+1').get('sheezel') != 11460:
        fails.append("lens('+1').get('sheezel') %r != 11460" % _lens(doc, '+1').get('sheezel'))
    if _lens(doc, '+2').get('sheezel') != 2733:
        fails.append("lens('+2').get('sheezel') %r != 2733" % _lens(doc, '+2').get('sheezel'))
    payload = {l: (_lens(doc, l).get('vector') or {}) for l in ('+1', '+2')}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
    seal = hashlib.sha256(blob.encode('utf-8')).hexdigest()
    if seal != FORWARD_VECTOR_SHA256:
        fails.append('vector_sha256 %s != oracle %s' % (seal, FORWARD_VECTOR_SHA256))
    if doc.get('vector_sha256') != FORWARD_VECTOR_SHA256:
        fails.append('stored vector_sha256 %s != oracle %s'
                     % (doc.get('vector_sha256'), FORWARD_VECTOR_SHA256))
    for f in fails:
        print('FORWARD ORACLE FAIL: %s' % f)
    if fails:
        return 1
    print('FORWARD ORACLE OK: board c8c2f2b6 active 804 '
          '+1 sum 640876 sheezel 11460 | +2 sum 205147 sheezel 2733 '
          '| seal 91f53f75 (expect c8c2f2b6/804/640876/205147/0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
