#!/usr/bin/env python3
"""PROBE REPAIR SEAT — THE SHARED R3/O42/O43-AWARE PRICING MODEL.

WHAT THE OLD PROBE ASSUMED, AND WHAT RL_O42/RL_O43 BROKE.
cp_r3age.py (and its parent as_r3age.py) modelled the CAND-minus-PRE board delta as

    board_delta[k]  ==  -int(round( r3_take(k) / NUM ))

with NUM an INFERRED constant read off one row. That model carries two assumptions that were true
on the R3-era stack and are false on the candidate line:

  (A1) "every board point of difference between the two boards is R3's take ON THAT ROW."
       RL_O43 (the parity guard) makes the printed price a PER-ROW MAX over two regimes,
           price = max( v under the injury regime , v under the healthy counterpart ),
       and the HEALTHY counterpart is measured with o41_injured -> False, so the counterpart is NOT
       R3-exempt and DOES carry an R3 charge. Turning R3 off therefore lifts the COUNTERPART, which
       can flip which side of the max wins. On such a row the board moves while the row's own take
       is exactly 0.0000 (it is injured, and R3 exempts injured rows). The old probe scored those
       rows 0.0000 against a moving board and called itself wrong. It was not wrong about the take;
       it was wrong about what the delta IS.

  (A2) "the board integer is a linear image of the engine price through one inferred constant, and
       the delta of two board integers is the image of the delta."
       rl_export.py:187/660 is explicit: board v == int(round(ev(p,2026)/_F)) with _F the numeraire
       from pick_redenomination.json (1.0524), and the export enforces that at tolerance 0. Two
       independent roundings do not commute with subtraction: round(a) - round(b) != round(a-b).
       An inferred NUM read off one row absorbs that row's rounding error and spreads it over all
       the others.

WHAT THIS MODULE DOES INSTEAD. It prices rows through the ENGINE ITSELF in three R3 modes, applies
the parity max the way the engine's own D7 block applies it, and converts with the engine's OWN _F.
No inferred constant survives anywhere in the instrument.

    mode 'on'   the candidate's price  (R3 live)
    mode 'off'  the same row with R3's take added back at every blend call  (the R3-off price)
    mode 'p1'   the same row with R3's take re-evaluated ONE YEAR OLDER, and nothing else moved

The +1yr take comes from `reform(..., agedelta=1)`, the re-formed collector the ORIGINAL probe used,
kept byte-for-byte. Age reaches R3 through o32_age_credit and nothing else, so advancing the age
inside the collector is the isolation the continuity harness's age axis intends -- unchanged intent,
now carried all the way through to the printed board integer instead of stopping at the take.

NOTHING HERE IS A LOOSENING. SELF-CHECK 1 (the re-formed take must equal the engine's take at every
call, exactly) is carried verbatim. The old SELF-CHECK 2 -- 67 charged rows against an inferred
constant -- is REPLACED BY A STRICTLY HARDER ONE: reproduce BOTH WHOLE BOARDS, 804 rows each, at
tolerance 0, which additionally requires getting the parity max's side selection right on every one
of the 37 treated rows. A model that merely stopped scoring the 8 awkward rows would fail it.

READ-ONLY / SCRATCH ONLY. This file lives in a git-archive export under the seat's own scratch dir;
no file in /home/user/afl-rl-engine is read for anything but `git archive`, and none is written.
"""
import io, os, sys, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as L

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BOARDS = os.path.normpath(os.path.join(REPO, '..', 'boards'))

# THE CANDIDATE'S EXACT DIAL LINE, read from docs/evidence/parity_2026-08-19/build_D7B.sh
# ("run D7B_CAND $S RL_O42=1 RL_O43=1", where S = BASE + R3 + RAMP + BREAK=unwind + UNWIND=7).
DIALS = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
             RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
             RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
             RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7',
             RL_O42='1', RL_O43='1')

# THE PRE-D6 ASSEMBLY STACK LINE — the validation line. This is V755_CAND / V755_L5CR, the pair the
# ORIGINAL as_r3age.py ran on and read birthday +0 across 9 charged rows. RL_O42/RL_O43 unset, break
# at its default 'binary'. The repaired probe must reproduce that reading or the repair is not one.
DIALS_HIST = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
                  RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47',
                  RL_O40_PGMAT='1', RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1',
                  RL_O41_INJ='1', RL_O41_R3='1', RL_O41_RAMP='1')

_F = json.load(open(os.path.join(REPO, 'engine/rl_after/pick_redenomination.json')))['factor']


def board(tag):
    """A built board, by tag, out of THIS seat's own scratch board dir."""
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (BOARDS, tag)
    import hashlib
    return ({r['key']: r for r in json.load(open(p))['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


def bint(x):
    """rl_export.py:187 `_nb` and :660 verbatim — the board integer IS int(round(ev/_F))."""
    return int(round(float(x) / _F))


class Model(object):
    """The engine loaded on one dial line, with the three R3 modes and the parity max wired."""

    def __init__(self, dials, o43=True):
        self.NS = NS = L.load(**dials)
        self.MA = NS['_MA']
        self.o43 = bool(o43 and NS.get('_O43'))
        self.BY = {p['key']: p for p in self.MA.players}
        self.mode = 'on'
        self.CALLS = {}
        self.recording = True
        self._treated_set = set()

        # ---- the engine's own objects the collector is re-formed from (as the original probe) ----
        self.rho31 = NS['rho31']; self.o31_pi = NS['o31_pi']
        self.o32_ac = NS['o32_age_credit']
        self.depth = NS['o41_absence_depth']; self.cost = NS['o41_cost']
        self.compl = NS['o41_completed_absent']
        self.o41_inj = NS['o41_injured']
        self.PRED8 = NS['_O41_PRED8']
        self.r3take = NS['o41_r3_take']
        self.pv_games = NS['pv_games']; self.pv_ped = NS['pv_pedigree']

        # ---- the D7 objects. `_ev_pre43` / `_o31D_pre43` exist only when the dial is on. --------
        if self.o43:
            self.AVAIL = NS['_AVAIL_STATE']
            self.HEALTHY_KEYS = NS['_D7_HEALTHY_KEYS']
            self.D7_ROWS = NS['_D7_ROWS']
            self.D7_FLOOR = dict(NS['_D7_FLOOR'])
            self.TREATED = [r['key'] for r in self.D7_ROWS]
            self.raw_ev = NS['_ev_pre43']
            self.raw_o31D = NS['_o31D_pre43'] if NS.get('_D7_DFADE') else NS['o31_D']
            self.guard_o31D = NS['o31_D']
        else:
            self.AVAIL = NS.get('_AVAIL_STATE', {})
            self.HEALTHY_KEYS = NS.get('_D7_HEALTHY_KEYS', set())
            self.D7_ROWS = []; self.D7_FLOOR = {}; self.TREATED = []
            self.raw_ev = NS['ev']
            self.raw_o31D = self.guard_o31D = NS['o31_D']

        self._treated_set = set(self.TREATED)
        self._install()

    # ---- THE CALL-SITE RECORDER + THE R3 MODE SWITCH ------------------------------------------
    # WHY AT THE CALL SITE (carried from the original probe, and still true): a row can reach the
    # blend TWICE at one year — the M3 proportional-tenure blend — and the two calls carry different
    # games, different production input e, and a different stashed pre-cap value in _O41_PRED8 which
    # the second call overwrites. Anything read after the run sees only the last call's state.
    def _install(self):
        NS = self.NS
        inner = NS['_PV']['blend']
        self._inner_blend = inner

        def wrapped(p, Y, e):
            v = inner(p, Y, e)
            g = self.pv_games(p, Y)
            try:
                ped = self.pv_ped(p)
            except SystemExit:
                ped = None
            if self.recording:
                d = dict(g=float(g), e=float(e), pin=bool(NS['_M3PIN']['on']),
                         healthy=bool(self.HEALTHY_KEYS and p.get('key') in self.HEALTHY_KEYS))
                d['engine'] = self.r3take(p, Y, g, e, ped) if ped is not None else 0.0
                d['reform'] = self.reform(p, Y, g, e, ped)
                d['reform_p1'] = self.reform(p, Y, g, e, ped, agedelta=1)
                self.CALLS.setdefault((p.get('key'), int(Y)), []).append(d)
            if self.mode == 'on' or ped is None:
                return v
            # THE ENGINE SUBTRACTED EXACTLY o41_r3_take AT THIS CALL (_pv_order31, :5102). Add that
            # same quantity back, in the same call state, to get the R3-OFF price; for 'p1' put the
            # ONE-YEAR-OLDER take in its place. Nothing else in the expression is touched.
            t0 = self.r3take(p, Y, g, e, ped)
            if self.mode == 'off':
                return v + t0
            if self.mode == 'p1':
                return v + t0 - self.reform(p, Y, g, e, ped, agedelta=1)
            return v

        NS['_PV']['blend'] = wrapped

    # ---- THE RE-FORMED COLLECTOR — CARRIED BYTE-FOR-BYTE FROM cp_r3age.py::_reform -------------
    def reform(self, p, Y, g, e, ped, agedelta=0):
        """R3's take, re-formed from the engine's own objects, with the age credit optionally
        evaluated one year older. Age reaches this collector through o32_age_credit and nothing
        else. IDENTICAL to the original probe's _reform; SELF-CHECK 1 is the gate on it."""
        if ped is None:
            return 0.0
        if self.o41_inj(p):
            return 0.0
        cx = self.depth(p, Y)
        if cx < 2.0 or self.compl(p, Y) < 1:
            return 0.0
        tgt = self.cost(cx)
        if tgt <= 0.0:
            return 0.0
        ac = self.o32_ac(p, Y + agedelta, g) if agedelta else self.o32_ac(p, Y, g)
        prod = self.rho31(g) * float(e)
        if prod <= 0.0:
            return 0.0
        epre = self.PRED8.get((id(p), int(Y)), e)
        free = self.rho31(g) * float(epre) + self.o31_pi(p, Y, g, _Dov=1.0) * ped + ac
        if not (free > 0.0):
            return 0.0
        now = prod + self.o31_pi(p, Y, g) * ped + ac
        taken = max(0.0, (free - now) / free)
        resid = max(0.0, tgt - taken)
        if resid <= 0.0:
            return 0.0
        return min(resid * free, prod)

    # ---- THE HEALTHY COUNTERPART — the engine's OWN seven-site neutralisation, replicated ------
    # _merged_recover.py:6003-6013 verbatim in effect: pop _AVAIL_STATE (sites 1,2,3), zero
    # _avail_hc (site 4) and _lti_ret_hc (site 5), and enter _D7_HEALTHY_KEYS so o41_injured
    # answers False (sites 6,7 — the R3 exemption, the sitter-clock pause, the absence-depth
    # in-progress exemption). Restored in a finally, exactly as the engine restores it.
    @contextlib.contextmanager
    def healthy(self, p):
        k = p.get('key')
        sv_state = self.AVAIL.pop(k, None)
        sv_hc = p.get('_avail_hc', 0.0)
        sv_ret = p.get('_lti_ret_hc', 0.0)
        p['_avail_hc'] = 0.0
        p['_lti_ret_hc'] = 0.0
        self.HEALTHY_KEYS.add(k)
        try:
            yield
        finally:
            self.HEALTHY_KEYS.discard(k)
            if sv_state is not None:
                self.AVAIL[k] = sv_state
            p['_avail_hc'] = sv_hc
            p['_lti_ret_hc'] = sv_ret

    @contextlib.contextmanager
    def rawfade(self):
        """Un-wrap the D7b fade site for the duration. The D7 block measures v_injury and v_healthy
        BEFORE either wrapper is installed (:6003-6011), so a faithful re-measurement must see the
        fade the way that block saw it — otherwise a lifted row's guard is applied twice."""
        self.NS['o31_D'] = self.raw_o31D
        try:
            yield
        finally:
            self.NS['o31_D'] = self.guard_o31D

    # ---- THE BOARD PRICE, THE WAY THE ENGINE WRITES IT -----------------------------------------
    def price(self, p, mode='on', o43_blind=False):
        """(board price float, v_injury, v_healthy-or-None) for this row in this R3 mode.

        THE PARITY MAX IS APPLIED HERE THE WAY THE ENGINE APPLIES IT (:6036-6042): for a treated row
        the printed price is max(v_injury, v_healthy); for every other row it is the plain price.
        `o43_blind=True` reproduces the OLD probe's model — no max, injury regime only — and exists
        only so the repaired self-check can be shown to still FAIL under the old assumption."""
        k = p.get('key')
        prev, self.mode = self.mode, mode
        try:
            with self.rawfade():
                with contextlib.redirect_stdout(io.StringIO()):
                    vi = float(self.raw_ev(p, 2026))
                    vh = None
                    if self.o43 and not o43_blind and k in self.D7_FLOOR_KEYS:
                        with self.healthy(p):
                            vh = float(self.raw_ev(p, 2026))
        finally:
            self.mode = prev
        return (vi if vh is None else max(vi, vh)), vi, vh

    @property
    def D7_FLOOR_KEYS(self):
        """Every TREATED key — not only the ones the guard binds on TODAY. The set of rows the max
        can bind on is fixed by the owner's annotation sheet; WHICH SIDE WINS is what the modes and
        the birthday are allowed to move, so the max must be re-taken on every treated row in every
        mode. Restricting this to the CAND-line _D7_FLOOR would hard-code the answer to the very
        question the owner asked (can the max flip sides?) into the instrument."""
        return self._treated_set
