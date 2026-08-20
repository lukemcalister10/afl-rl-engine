#!/usr/bin/env python3
"""ORDER M — fill the two ladder tables into PACKET_M.md from LADDER_M.json.

The packet carries `<!--LADDER_A-->` and `<!--LADDER_B-->` placeholders so the ladder tables are
GENERATED from the built boards rather than retyped by hand. Running this twice is safe: it replaces
the block between the marker and the next heading.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
LD = json.load(open(os.path.join(HERE, 'LADDER_M.json')))
BM = json.load(open(os.path.join(HERE, 'BOARDS_M.json')))
P = os.path.join(HERE, 'PACKET_M.md')
s = open(P).read()
BASE = dict(dean=2400, cdt=1572, xavier=1176, annable=1530, patterson=1467)


def flag(v, target, want_ge=True):
    if want_ge:
        return '**%d**' % v if v >= target else '%d' % v
    return '**%d**' % v if v > target else '%d' % v


A = ['| eta | harry-dean (want ~2,600) | duff-tytler (want ~1,800) | xavier-taylor (must not rise) '
     '| daniel-annable (must not rise) | dylan-patterson (must not rise) | board legal? |',
     '|---:|---:|---:|---:|---:|---:|---|',
     '| *landing candidate* | 2,400 | 1,572 | 1,176 | 1,530 | 1,467 | — |']
for r in sorted(LD['ladderA'], key=lambda x: x['eta']):
    A.append('| %.2f | %s | %s | %s | %s | %s | %s |'
             % (r['eta'],
                flag(r['dean'], 2600), flag(r['cdt'], 1800),
                flag(r['xavier'], BASE['xavier'], False),
                flag(r['annable'], BASE['annable'], False),
                flag(r['patterson'], BASE['patterson'], False),
                'LEGAL' if r['eta'] >= 0.50 else 'illegal'))
A.append('')
A.append('Bold means the cell is on the wrong side of the rule it is being read against: bold in the '
         'first two columns means the row **reaches** the owner\'s reference, bold in the last three '
         'means the row **rises** when it must not.')

B = ['| board | S1 dose | smallest legal eta | harry-dean | duff-tytler | xavier-taylor '
     '| daniel-annable | dylan-patterson | veteran net move (cap 668) |',
     '|---|---:|---:|---:|---:|---:|---:|---:|---:|',
     '| *landing candidate* | — | — | 2,400 | 1,572 | 1,176 | 1,530 | 1,467 | 0 |']
for r in LD['ladderB']:
    B.append('| %s | %.2f | %s | %d | %d | %d | %d | %d | %+d |'
             % (r['tag'], r['dose'], '%.2f' % r['eta'] if r['eta'] > 0 else '**none — ILLEGAL**',
                r['dean'], r['cdt'], r['xavier'], r['annable'], r['patterson'], r['vet_net']))
B.append('')
B.append('`MLO` is the top row and it is the odd one out: it is dose 0 with **no eta at all**, and its '
         'kappa is 0.15 / gamma_u 16 rather than the ruled 0.20 / 8, because that is the coolest point '
         'the whole eta = 0 grid reaches. It is illegal, and it is in the table as the far end of the '
         'curve rather than as an option. Every other row is a cheapest-legal-eta point at the ruled '
         'knobs.')

K = ['| board | dose | kappa | gamma_u | eta | xavier-taylor | daniel-annable | dylan-patterson |',
     '|---|---:|---:|---:|---:|---:|---:|---:|',
     '| *landing candidate* | — | — | — | — | 1,176 | 1,530 | 1,467 |']
for r in LD.get('kappa_max', []):
    K.append('| %s | %.2f | %.2f | %.0f | %.2f | %d | %d | %d |'
             % (r['tag'], r['dose'], r['kappa'], r['gamma_u'], r['eta'],
                r['xavier'], r['annable'], r['patterson']))


def put(marker, lines):
    global s
    i = s.index(marker)
    j = s.index('\n###', i) if '\n###' in s[i:] else s.index('\n---', i)
    s = s[:i] + '\n'.join(lines) + '\n' + s[j:]


put('<!--LADDER_A-->', A)
put('<!--LADDER_B-->', B)
if K and len(K) > 3 and '<!--KAPPAMAX-->' in s:
    put('<!--KAPPAMAX-->', K)
open(P, 'w').write(s)
print('PACKET_M.md ladder tables filled from LADDER_M.json (%d + %d + %d rows)'
      % (len(LD['ladderA']), len(LD['ladderB']), len(LD.get('kappa_max', []))))
