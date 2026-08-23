#!/usr/bin/env python3
"""FORWARD-LENS ORACLE — GENERATED ARTIFACT. DO NOT EDIT BY HAND.

Regenerated in full by the advance transaction (engine/rl_after/ingestion/sibling_repin.py, ITEM 408 D2)
on every advance, from the freshly built sibling board. Every literal below was DERIVED from that build;
none was authored, transcribed or carried over from a previous round. Editing this file by hand makes it
disagree with the artifact it gates and the advance transaction will HALT on the next plan/check.

It gates the committed forward reference vector on the round's OWN board identity. It contains no
historical board id: forward_vector_6fd0f7de.json and the identity below are this round's.

Run:  python3 test_forward_lens_6fd0f7de.py      (exit 0 == the committed forward view matches this oracle)
"""
import hashlib
import json
import os
import sys

FORWARD_BOARD_MD5_GOOD = '6fd0f7ded2b280d1a90962c299a152e3'
FORWARD_REFERENCE = 'forward_vector_6fd0f7de.json'
FORWARD_VECTOR_SHA256 = '5d4b6c34353df16b35414e1820bcf17eb74463c847360e9f621a79ff34324b49'

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
    if _lens(doc, '+1').get('sum') != 640375:
        fails.append("lens('+1').get('sum') %r != 640375" % _lens(doc, '+1').get('sum'))
    if _lens(doc, '+2').get('sum') != 204020:
        fails.append("lens('+2').get('sum') %r != 204020" % _lens(doc, '+2').get('sum'))
    if _lens(doc, '+1').get('sheezel') != 10841:
        fails.append("lens('+1').get('sheezel') %r != 10841" % _lens(doc, '+1').get('sheezel'))
    if _lens(doc, '+2').get('sheezel') != 2605:
        fails.append("lens('+2').get('sheezel') %r != 2605" % _lens(doc, '+2').get('sheezel'))
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
    print('FORWARD ORACLE OK: board 6fd0f7de active 804 '
          '+1 sum 640375 sheezel 10841 | +2 sum 204020 sheezel 2605 '
          '| seal 5d4b6c34 (expect 6fd0f7de/804/640375/204020/0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
