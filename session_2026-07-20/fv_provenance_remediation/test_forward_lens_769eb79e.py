#!/usr/bin/env python3
"""FORWARD-LENS ORACLE — GENERATED ARTIFACT. DO NOT EDIT BY HAND.

Regenerated in full by the advance transaction (engine/rl_after/ingestion/sibling_repin.py, ITEM 408 D2)
on every advance, from the freshly built sibling board. Every literal below was DERIVED from that build;
none was authored, transcribed or carried over from a previous round. Editing this file by hand makes it
disagree with the artifact it gates and the advance transaction will HALT on the next plan/check.

It gates the committed forward reference vector on the round's OWN board identity. It contains no
historical board id: forward_vector_769eb79e.json and the identity below are this round's.

Run:  python3 test_forward_lens_769eb79e.py      (exit 0 == the committed forward view matches this oracle)
"""
import hashlib
import json
import os
import sys

FORWARD_BOARD_MD5_GOOD = '769eb79e6a70cd0417519d33de1bc8ff'
FORWARD_REFERENCE = 'forward_vector_769eb79e.json'
FORWARD_VECTOR_SHA256 = '3540880d070c7dce16f9ecb419eb26e663ee1918af9d9a0462816b3c6dad0102'

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
    if _lens(doc, '+1').get('sum') != 635134:
        fails.append("lens('+1').get('sum') %r != 635134" % _lens(doc, '+1').get('sum'))
    if _lens(doc, '+2').get('sum') != 593206:
        fails.append("lens('+2').get('sum') %r != 593206" % _lens(doc, '+2').get('sum'))
    if _lens(doc, '+1').get('sheezel') != 11167:
        fails.append("lens('+1').get('sheezel') %r != 11167" % _lens(doc, '+1').get('sheezel'))
    if _lens(doc, '+2').get('sheezel') != 11233:
        fails.append("lens('+2').get('sheezel') %r != 11233" % _lens(doc, '+2').get('sheezel'))
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
    print('FORWARD ORACLE OK: board 769eb79e active 804 '
          '+1 sum 635134 sheezel 11167 | +2 sum 593206 sheezel 11233 '
          '| seal 3540880d (expect 769eb79e/804/635134/593206/0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
