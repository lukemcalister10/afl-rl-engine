"""ORDER E — the counterfactual installers. READ-ONLY: every one of these is a monkeypatch on the
module already loaded in THIS process. Nothing is written to any engine file, board, store or law.
Each installer returns an uninstaller; the harness asserts the baseline price is restored exactly
after every experiment.

THE AGE BAR. Where a site is "age-corrected", the correction uses the ENGINE'S OWN measured
development gap, O32_GATE_DELTA (_merged_recover.py:3332-3335, the S1 C3 construction):
    bar(pos, age) = flat_bar(pos) - Delta[TALL|SMALL][clamp(int(age),18,23)],  Delta = 0 from age 24
so an age-24+ row is byte-identical by construction and every control must hold at 0.
"""
import io, contextlib
import numpy as np

MA = None
G = None
TALL = ('KPD', 'KPF', 'RUCK')


def bind(ma, g):
    global MA, G
    MA, G = ma, g


def delta(pos, age):
    """The C3 development gap in avg-points for a row of `pos` at `age`. 0 from 24; 0 if age unknown."""
    if age is None:
        return 0.0
    a = float(age)
    if a >= 24.0:
        return 0.0
    tab = G['O32_GATE_DELTA']['TALL' if pos in TALL else 'SMALL']
    return float(tab[max(18, min(23, int(a)))])


# ============================ S1 — the replacement bar in the projection loop ====================
# Verbatim copies of the four loops, with the ONE expression `MA.REPL[x]` replaced by `barf(x, age)`.
# barf = lambda pos, age: MA.REPL[pos]  reproduces the baseline BYTE-EXACT (the identity control).

def make_proj_w4(barf):
    _proj_w4_0 = make_proj_rl(barf)          # the ctx-None fallback must carry the same bar

    def _proj_w4(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0, grace=0):
        ctx = G['_W4CTX']['on']
        if ctx is None:
            return _proj_w4_0(g, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc, grace=grace)
        _off = (MA.AGE_REF - MA.BASE_REF) if G['_LEGF_ON'] else 0
        ah = a - _off if _off > 0 else a
        pa = MA.PEAK_AGE[g]
        d = MA.age_disc(ah, MA.LENS[lens], lens) + (MA.o33_fade(ah) if lens in ('bal', 'balanced') else 0.0)
        cl = cur if cur else lp * MA.frac(ah, pa, g)
        prod = 0.0
        if g0 is None:
            g0 = g
        if fut is None:
            fut = [(g, 1.0)]
        for k in range(18):
            ag = ah + k
            if ag > 38 or MA.frac(ag, pa, g) < 0.42:
                break
            lev = lp * MA.frac(ag, pa, g)
            if ag <= pa:
                lev = max(lev, cl)
            if k == 0:
                lev = max(lev, cl)
            if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
                lev *= (1 - pre_hc)
            if G['_BOARD_PATH'] and k == ctx.get('ret_k', -1) and ctx.get('ret_hc', 0.0) > 0:
                lev *= (1 - ctx['ret_hc'])
            base = lev + MA.capt_prem(lev)
            Wk = G['_w4_W'](k, ctx)
            _df = MA.disc_factor(ah, d, k, lens, grace)
            if k == 0:
                prod += Wk * MA.posval(base - barf(g0, ag)) * 21 / _df
            else:
                prod += Wk * sum(w * MA.posval(base - barf(gg, ag)) for gg, w in fut) * 21 / _df
        if g in ('KPF', 'KPD'):
            prod *= 1.05
        if MA._O33 and MA._O33S >= 1 and g in ('KPF', 'KPD'):
            prod *= MA.O33_SSTAR
        runway = MA.clamp((25 - ah) / 6.0, 0, 1)
        elite = MA.clamp((lp / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
        prod *= (1 + runway * elite * MA.PMAX)
        return prod
    return _proj_w4


def make_proj_rl(barf):
    """Copy of rl_model.proj_from_peak (the ctx-None / synth path)."""
    def proj_from_peak(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0, grace=0):
        pa = MA.PEAK_AGE[g]
        d = MA.age_disc(a, MA.LENS[lens], lens) + (MA.o33_fade(a) if lens in ('bal', 'balanced') else 0.0)
        cl = cur if cur else lp * MA.frac(a, pa, g)
        prod = 0.0
        if g0 is None:
            g0 = g
        if fut is None:
            fut = [(g, 1.0)]
        for k in range(18):
            ag = a + k
            if ag > 38 or MA.frac(ag, pa, g) < 0.42:
                break
            lev = lp * MA.frac(ag, pa, g)
            if ag <= pa:
                lev = max(lev, cl)
            if k == 0:
                lev = max(lev, cl)
            if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
                lev *= (1 - pre_hc)
            base = lev + MA.capt_prem(lev)
            _df = MA.disc_factor(a, d, k, lens, grace)
            if k == 0:
                prod += MA.posval(base - barf(g0, ag)) * 21 / _df
            else:
                prod += sum(w * MA.posval(base - barf(gg, ag)) for gg, w in fut) * 21 / _df
        if g in ('KPF', 'KPD'):
            prod *= 1.05
        if MA._O33 and MA._O33S >= 1 and g in ('KPF', 'KPD'):
            prod *= MA.O33_SSTAR
        runway = MA.clamp((25 - a) / 6.0, 0, 1)
        elite = MA.clamp((lp / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
        prod *= (1 + runway * elite * MA.PMAX)
        return prod
    return proj_from_peak


def make_floor_rl(barf):
    """Copy of rl_model.prod_floor."""
    def prod_floor(p, lens='bal'):
        g = MA.bnow(p); a = MA.age(p); pa_ = MA.PEAK_AGE[g]; cur = MA.level_now(p)
        if cur is None:
            return 0
        lowbar = MA.y0dpp_bar(p) if (MA.AGE_REF == MA.BASE_REF) else None
        _gr = MA.grace_years(p)
        d = MA.age_disc(a, MA.LENS[lens], lens) + (MA.o33_fade(a) if lens in ('bal', 'balanced') else 0.0)
        H = MA.clamp((40 - a) / 3.0, 1.0, 3.0); prod = 0.0; k = 0
        while k < H:
            ag = a + k; wt = min(1.0, H - k)
            lev = cur * min(1.0, MA.frac(ag, pa_, g) / max(MA.frac(a, pa_, g), 1e-6))
            if k == 0 and p.get('_avail_hc', 0) > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
                lev *= (1 - p['_avail_hc'])
            base = lev + MA.capt_prem(lev)
            if k == 0 and lowbar is not None:
                sp = MA.SEASON_PROG
                pv = sp * MA.posval(base - barf(g, ag)) + (1.0 - sp) * MA.posval(base - barf(lowbar, ag))
            else:
                pv = MA.posval(base - barf(g, ag))
            prod += wt * pv * 21 / MA.disc_factor(a, d, k, lens, _gr); k += 1
        return MA.val(prod)
    return prod_floor


def make_floor_w4(barf):
    _prod_floor_w4_0 = make_floor_rl(barf)

    def _prod_floor_w4(p, lens='bal'):
        ctx = G['_W4CTX']['on']
        if ctx is None or ctx.get('n', 0) < G['PROVEN_N'] or not G['_W4FWD']:
            return _prod_floor_w4_0(p, lens)
        g = MA.bnow(p); a = MA.age(p); pa_ = MA.PEAK_AGE[g]; cur = MA.level_now(p)
        if cur is not None and G['_lsym_active']():
            cur = G['_lsym_blend'](MA.level_demo(p), cur, G['_lsym_age'](p))
        if cur is None:
            return 0
        lowbar = MA.y0dpp_bar(p) if (MA.AGE_REF == MA.BASE_REF) else None
        _gr = MA.grace_years(p)
        d = MA.age_disc(a, MA.LENS[lens], lens) + (MA.o33_fade(a) if lens in ('bal', 'balanced') else 0.0)
        H = MA.clamp((40 - a) / 3.0, 1.0, 3.0); prod = 0.0; k = 0
        while k < H:
            ag = a + k; wt = min(1.0, H - k)
            lev = cur * min(1.0, MA.frac(ag, pa_, g) / max(MA.frac(a, pa_, g), 1e-6))
            if k == 0 and p.get('_avail_hc', 0) > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
                lev *= (1 - p['_avail_hc'])
            base = lev + MA.capt_prem(lev)
            if k == 0 and lowbar is not None:
                sp = MA.SEASON_PROG
                pv = sp * MA.posval(base - barf(g, ag)) + (1.0 - sp) * MA.posval(base - barf(lowbar, ag))
            else:
                pv = MA.posval(base - barf(g, ag))
            prod += G['_w4_W'](k, ctx) * wt * pv * 21 / MA.disc_factor(a, d, k, lens, _gr); k += 1
        return MA.val(prod)
    return _prod_floor_w4


def install_S1(agecorrect=True):
    """S1 — the replacement bar inside the projection loop and the demonstrated-production floor."""
    if agecorrect:
        def barf(pos, age):
            return MA.REPL[pos] - delta(pos, age)
    else:
        def barf(pos, age):
            return MA.REPL[pos]
    old_proj, old_floor = MA.proj_from_peak, MA.prod_floor
    MA.proj_from_peak = make_proj_w4(barf)
    MA.prod_floor = make_floor_w4(barf)

    def un():
        MA.proj_from_peak = old_proj
        MA.prod_floor = old_floor
    return un


# ============================ S2 — the flat future discount =====================================
def install_S2(mode='5'):
    old_on, old_mode = MA.AGE_DISC, MA.AGE_DISC_MODE
    MA.AGE_DISC = True
    MA.AGE_DISC_MODE = mode

    def un():
        MA.AGE_DISC = old_on
        MA.AGE_DISC_MODE = old_mode
    return un


# ============================ S3 — the v7 tail-taper relax gate ==================================
def install_S3():
    """Age-correct the `_lcr > 4` mature-REPL test inside the v7 form-conditioned relax."""
    old = G['_v7']
    _lvlcurr = G['_lvlcurr']; cp = G['cp']; _nqual = G['_nqual']

    def _v7(bb, p, Y):
        bb = list(bb); m = bb[2]; a = cp._age_asof(p, Y)
        asc = float(np.interp(a, [20, 22, 24, 27], [1.0, 0.76, 0.58, 0.40]))
        if G['_W4V7'] and asc < 1.0:
            pos = MA.gfut(p)
            _lcr = _lvlcurr(p, Y) - (MA.REPL.get(pos, 0.0) - delta(pos, a))   # <-- THE ONE CHANGE
            _nq = _nqual(p, Y)
            if _lcr > 4.0 and _nq >= 1:
                _phi = float(np.clip((_lcr - 4.0) / 26.0, 0.0, 1.0)) * min(_nq, 2) / 2.0 * G['V7_FORM_W']
                asc = asc + (1.0 - asc) * _phi
        bb[5] = m + asc * (bb[5] - m)
        return bb
    G['_v7'] = _v7

    def un():
        G['_v7'] = old
    return un


# ============================ S4 — the un-compress rho axis =====================================
def install_S4():
    """Age-correct the per-season above-replacement margin in rho_out. RHO_DEN untouched."""
    old = G['rho_out']

    def rho_out(p, pos):
        _num = 0.0; _den = 0.0
        by = p.get('_by')
        for x in p.get('scoring') or []:
            _gm = x.get('games', 0) or 0
            if _gm <= 0:
                continue
            _u = _gm * (MA.UNCOMP_DECAY ** (2026 - x['year']))
            age_s = (int(x['year']) - int(by)) if by else None                  # age in that season
            _num += _u * (x['avg'] - (MA.REPL[pos] - delta(pos, age_s)))        # <-- THE ONE CHANGE
            _den += _u
        if _den <= 0.0:
            return None
        return _num / _den
    G['rho_out'] = rho_out

    def un():
        G['rho_out'] = old
    return un


# ============================ S5 — the _lvl_eff exposure shrink ==================================
def install_S5():
    cp = G['cp']
    old = cp._lvl_eff

    def _lvl_eff(p, Y):
        return float(cp._lvl_wt(p, Y))
    cp._lvl_eff = _lvl_eff

    def un():
        cp._lvl_eff = old
    return un


# ============================ S6 — the _inferM1 upside-fade bar ==================================
def install_S6():
    cp = G['cp']
    old = cp._lvl_eff        # cp._lvl_eff IS _inferM1 (bound at _merged_recover.py:765)
    _coreM1 = G['_coreM1']; _eo = G['_eo']; _upS = G['_upS']; _lvlcurr = G['_lvlcurr']

    def _inferM1(p, Y):
        L0 = _coreM1(p, Y); eo = _eo(p, Y)
        if eo <= 0:
            return L0
        avs = [x['avg'] for x in p['scoring'] if x.get('games', 0) >= 6 and (cp.debutyr(p) - 1) < x['year'] <= Y]
        if not avs:
            return L0
        pos = MA.gfut(p); a = cp._age_asof(p, Y)
        bar = MA.REPL.get(pos, 0.0) - 3.0 - delta(pos, a)          # <-- THE ONE CHANGE
        N = Y - cp.debutyr(p) + 1
        T = max(_upS(max(avs) - bar, N), _lvlcurr(p, Y))
        return (1 - eo) * L0 + eo * (T if G['_EO2'] else min(L0, T))
    cp._lvl_eff = _inferM1

    def un():
        cp._lvl_eff = old
    return un


# ============================ S7 — the _est decliner shed ========================================
def install_S7():
    cp = G['cp']
    old = G['_est']
    _S_AGE = G['_S_AGE']; _agemult2 = G['_agemult2']; _radq = G['_radq']

    def _est(p, Y, Lo, Lc):
        if Lc >= Lo:
            s = (_S_AGE(cp._age_asof(p, Y)) if G['_L3_AGE'] else G['S_M1']); gap = Lc - Lo
            if not G['_LSYM']:
                return (Lo + s * gap) if (gap >= G['TOL_M1'] and _radq(p, Y, Lo)) else Lo
            if gap <= G['DOWN_TOL']:
                return Lo
            sw = float(np.clip((gap - G['DOWN_TOL']) / 5, 0, 1))
            return Lo + sw * s * gap
        drop = Lo - Lc
        if drop <= G['DOWN_TOL']:
            return Lo
        pos = MA.gfut(p); a = cp._age_asof(p, Y)
        sw = float(np.clip((drop - G['DOWN_TOL']) / 5, 0, 1))
        return (1 - sw) * Lo + sw * Lc * _agemult2(a, Lc - (MA.REPL.get(pos, 0.0) - delta(pos, a)))  # <-- CHANGE
    G['_est'] = _est

    def un():
        G['_est'] = old
    return un


# ============================ S18 — D8 graded staleness ==========================================
def install_S18():
    old = G['_staleness_grade']
    cp = G['cp']; _fEy = G['_fEy']

    def _staleness_grade(p, Y, pos):
        current = [x for x in p['scoring'] if x['year'] == Y]
        if any(x['games'] >= 6.0 * _fEy(Y, p) for x in current):
            return 1.0
        live = [x for x in current if x['games'] > 0]
        if not live:
            return 0.0
        prior_qual = [x['year'] for x in p['scoring'] if x['year'] < Y and x['games'] >= 6]
        if not prior_qual:
            return 0.0
        a = cp._age_asof(p, Y)
        qv = (live[0]['avg']) / max(MA.REPL.get(pos, 1e-9) - delta(pos, a), 1e-9)   # <-- THE ONE CHANGE
        gap = Y - max(prior_qual)
        return float(np.interp(qv, G['_D8Q'], G['_D8G1'] if gap == 1 else G['_D8G2']))
    G['_staleness_grade'] = _staleness_grade

    def un():
        G['_staleness_grade'] = old
    return un


# ====== S20 — ORDER C site 1: ITEM C's Q denominator, age-referenced ==============================
def install_S20():
    old_bars = dict(G['_O30BP_BARS'])
    old_cw = G['_c_w']
    cp = G['cp']

    def _c_w(p, Y, e_full, anchor):
        gt, sa = G['_c_career'](p)
        if gt <= 0 or anchor <= 0:
            return 0.0
        pos = MA.gfut(p); a = cp._age_asof(p, Y)
        par = old_bars[pos] - delta(pos, a)                    # <-- THE ONE CHANGE (ORDER C site 1)
        Gg = gt / (gt + G['_C_G0'])
        Q = float(np.clip(sa / par, 0.0, G['_C_QMAX'])) if par > 0 else 0.0
        gate = min(e_full / anchor, 1.0) if e_full > 0 else 0.0
        return Gg * Q * gate
    G['_c_w'] = _c_w

    def un():
        G['_c_w'] = old_cw
    return un


# ====== S19 — ORDER C site 2: the decay-gate denominator, age-referenced ==========================
def install_S19():
    """`pr = bestlvl(p,Y)/max(1,par)` with par = _O30BP_BARS[pos]. The engine's own comment at
    _merged_recover.py:2576-2578 asserts this par has EXACTLY ONE consumer, `pr`. Lowering the
    denominator to bar(pos,age) is therefore algebraically identical to scaling `bestlvl` by
    par_flat/par_age, which is how it is done here (the inline expression cannot be rebound).
    CAVEAT, disclosed: bestlvl has a SECOND consumer, `_ruc_ceiling` (:1503), which is reached only
    by RUCK rows. No row in this seat's measured set is a RUCK, so the isolation holds here and
    would NOT hold for a ruck."""
    old = G['bestlvl']
    cp = G['cp']

    def bestlvl(p, Y=2026):
        v = old(p, Y)
        pos = MA.gfut(p); a = cp._age_asof(p, Y)
        flat = G['_O30BP_BARS'].get(pos)
        if flat is None:
            return v
        aged = flat - delta(pos, a)
        return v * (flat / aged) if aged > 0 else v            # <-- equivalent to par -> aged
    G['bestlvl'] = bestlvl

    def un():
        G['bestlvl'] = old
    return un


# ============================ S22 — the L1c young credit =========================================
def install_S22(mode='off'):
    """mode='off'  -> neutralize the credit (multiplier 1.0): sizes what is currently PAID.
       mode='full' -> phi = 1 for rows under 24: sizes the headroom if it were age-keyed."""
    old = G['_ycred_mult']
    cp = G['cp']

    if mode == 'off':
        def _ycred_mult(p, Y):
            return 1.0
    else:
        _ycred_games = G['_ycred_games']

        def _ycred_mult(p, Y):
            if not G['_W4YNG'] or G['_YC_TAB'] is None or not G['_isreal'](p):
                return 1.0
            if p.get('type') not in ('ND', 'RD') or p.get('_pickless'):
                return 1.0
            pk = MA.effpk(p)
            if not pk:
                return 1.0
            g = _ycred_games(p, Y)
            a = cp._age_asof(p, Y)
            if g >= G['_YC_G0'] and (a is None or a >= 24):
                return 1.0
            T = int(Y)
            if T < G['_YC_TMIN']:
                return 1.0
            row = G['_YC_TAB'][str(min(T, G['_YC_TMAX']))].get(MA.gfut(p))
            if row is None:
                return 1.0
            lp = float(np.log(min(max(pk, 1), 90)))
            Rs = float(np.interp(lp, G['_YC_LGRID'], row['1'])); Rp = float(np.interp(lp, G['_YC_LGRID'], row['0']))
            s = min(g / 6.0, 1.0)
            R = max((1.0 - s) * Rs + s * Rp, 0.0)
            if MA.gfut(p) == 'KPF':
                R *= G['_YC_KPF']
            phi = 1.0 if (a is not None and a < 24) else (1.0 - g / G['_YC_G0']) ** 2   # <-- THE ONE CHANGE
            return 1.0 + G['_YC_W'] * R * phi
    G['_ycred_mult'] = _ycred_mult

    def un():
        G['_ycred_mult'] = old
    return un


# ============================ S25 — the re-mix bound (NOT a Phat site) ===========================
def install_S25_eta0():
    """Neutralize the g-keyed pedigree de-rate eta*m_d(g) inside o31_pi. BOUND ONLY."""
    old = G['O32_ETA']
    G['O32_ETA'] = 0.0

    def un():
        G['O32_ETA'] = old
    return un


def install_S25_rho1():
    """UPPER BOUND ONLY, explicitly not a proposal: give the production leg full weight while the
    pedigree leg is held at its current value. This double-counts by construction and is reported
    as a ceiling, never as a candidate."""
    old = G['rho31']

    def rho31(g):
        return 1.0 if float(g) > 0 else 0.0
    G['rho31'] = rho31

    def un():
        G['rho31'] = old
    return un
