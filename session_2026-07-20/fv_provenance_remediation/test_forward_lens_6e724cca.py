#!/usr/bin/env python3
"""FORWARD-LENS ORACLE — GENERATED ARTIFACT. DO NOT EDIT BY HAND.

Regenerated in full by the advance transaction (engine/rl_after/ingestion/sibling_repin.py, ITEM 408 D2)
on every advance, from the freshly built sibling board. Every literal below was DERIVED from that build;
none was authored, transcribed or carried over from a previous round. Editing this file by hand makes it
disagree with the artifact it gates and the advance transaction will HALT on the next plan/check.

It gates the committed forward reference vector on the round's OWN board identity. It contains no
historical board id: forward_vector_6e724cca.json and the identity below are this round's.

Run:  python3 test_forward_lens_6e724cca.py      (exit 0 == the committed forward view matches this oracle)
"""
import hashlib
import json
import os
import sys

FORWARD_BOARD_MD5_GOOD = '6e724cca2bb2fb118ff7ad6ed1f8a4b6'
FORWARD_REFERENCE = 'forward_vector_6e724cca.json'
FORWARD_VECTOR_SHA256 = '6a6bc8e6a430e9de8a67ed6fcbe062e632db13e8a2a6aaefbd4f15f2313c8709'

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
    if _lens(doc, '+1').get('sum') != 708338:
        fails.append("lens('+1').get('sum') %r != 708338" % _lens(doc, '+1').get('sum'))
    if _lens(doc, '+2').get('sum') != 655251:
        fails.append("lens('+2').get('sum') %r != 655251" % _lens(doc, '+2').get('sum'))
    if _lens(doc, '+1').get('sheezel') != 12519:
        fails.append("lens('+1').get('sheezel') %r != 12519" % _lens(doc, '+1').get('sheezel'))
    if _lens(doc, '+2').get('sheezel') != 12764:
        fails.append("lens('+2').get('sheezel') %r != 12764" % _lens(doc, '+2').get('sheezel'))
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
    print('FORWARD ORACLE OK: board 6e724cca active 804 '
          '+1 sum 708338 sheezel 12519 | +2 sum 655251 sheezel 12764 '
          '| seal 6a6bc8e6 (expect 6e724cca/804/708338/655251/0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
