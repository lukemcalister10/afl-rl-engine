#!/usr/bin/env python3
"""FORWARD-LENS SIBLING — ITEM 408 D2 (issue #157 §1-§3).

The +1/+2 projection view (`vP1`/`vP2`) is a DERIVED artifact of the ONE store + the model + the PVC, in
exactly the sense the balanced/strict board and the FV present-value reference vector already are. Until
this module it was NOT a member of the advance transaction's sibling set, so it could lag the live board
across an advance (owner-DEFERRED at v422, with an expiry). This module supplies the derivation, the
serialization and the oracle text so `sibling_repin.RepinPlan` can carry the forward view as a MANDATORY
SIBLING inside the one staged, journalled, rollback-capable transaction.

WHAT IS DERIVED (never authored, never transcribed):
  Everything below is read out of the FRESHLY BUILT sibling board — the same board object the present-value
  reference vector is derived from — so the forward view cannot be current-looking while being stale:
    - the complete per-lens forward vector   {player key -> int(vP1)} and {player key -> int(vP2)}
    - the per-lens aggregates                active / sum / Sheezel
    - the per-lens conservation row          the board's OWN lensConservation +1/+2 rows
    - a content seal                         sha256 over the canonical (sort_keys) two-lens vector pair

WHAT IS ASSERTED (prose law 8 -> LENS-PROJECTION + G-Y0 + G-COHORT, per the v393 mapping) — CONTINUOUSLY,
on every plan / reconcile / verify / check, not at checkpoints:
  LENS-PROJECTION  every active row carries BOTH forward columns and both are integral; the forward
                   universe is exactly the active universe (no row silently dropped from a lens).
  G-COHORT         the +1 and +2 key sets are IDENTICAL to each other AND to the present-value reference
                   vector's key set — one cohort seen through three lenses, never three cohorts.
  G-Y0             year-0 continuity, rendered as arithmetic that must hold on the artifact itself:
                   each lens' conservation row satisfies players == sum(vector.values()),
                   total == players + picks, and nPlayers == active.

WHAT IS NOT TOUCHED (issue #157 §1 scope fence, §6):
  The vP1/vP2 MATH in engine/rl_after/rl_export.py is untouched. No forward SEMANTIC oracle is adopted:
  the forward valuation shape stays owner-deferred. Board B (70ef0ff) is never a build input. This module
  reads the built board and writes derived artifacts; it computes no valuation of its own.

NO HARDCODED BOARD ID: every filename and every asserted identity is keyed to the round's own freshly built
board md5, taken from the manifest of record's own build. There is no R19 (or any other) literal here.
"""
import hashlib
import json
import os
import re

# The two forward lenses, in fixed order. k=0 (balanced/present) is deliberately excluded: that lens IS the
# present-value reference vector, and duplicating it here would create a second authority for one truth.
FORWARD_LENSES = (("+1", "vP1", 1, 2027), ("+2", "vP2", 2, 2028))

# The conservation-row keys carried out of the built board's own lensConservation diagnostic.
_CONSERVATION_KEYS = ("lensYear", "nPicks", "nPlayers", "picks", "players", "total")

# --------------------------------------------------------------------------- authorities of record
# Repo-relative paths of the authorities the config-of-record forward build rests on. Every value taken
# from them is read and CROSS-CHECKED between independent records at build time — none is hardcoded here.
MODEL_CONFIG_REL = "data/model_config.json"
RELEASE_CONTRACT_REL_ = "data/release_contract.json"
EXPECTED_BOOT_REL_ = "data/expected_boot.json"
BOARD_OF_RECORD_REL_ = "data/rl_build/rl_app_data.json"
F5_SEALED_INPUT_REL = "session_2026-07-18/legf5/sealed_entrant_structure.json"

# The mode that makes config_manifest.enforce() clear ambient model env, reject unknown/divergent overrides
# and LOAD the manifest authoritatively. This is how the posture is obtained — never from code defaults,
# even where the defaults coincide (coincidence today is not provenance; the ad9ab59 defect is exactly what
# happens when live semantics resolve from unstamped defaults).
FORWARD_CONFIG_MODE = "canonical"


class ForwardLensError(RuntimeError):
    """Any fail-closed condition in the forward-lens sibling (derive / serialize / parse / compare)."""


class ForwardAuthorityError(ForwardLensError):
    """An authority of record is missing, unsealed or inconsistent. This is a STOP, never a substitution:
    the forward view is not built, nothing is regenerated, and the condition is reported upward."""


def f5_seal_of(struct):
    """Recompute the sealed-entrant-structure seal exactly as the engine does (rl_export.py §2.viii)."""
    chk = {k: v for k, v in struct.items() if k != "seal_sha256_8"}
    return hashlib.sha256(json.dumps(chk, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()[:8]


def verify_authorities(repo_root, env=None):
    """Verify — BEFORE any forward build — every authority the config-of-record posture rests on. Returns a
    provenance dict on success; raises ForwardAuthorityError (a STOP) on any mismatch.

    Nothing here is asserted against a literal in this file. Each value is cross-checked between two or more
    independent records, so this cannot pass merely by agreeing with a constant someone typed:
      config seal      model_config.config_sha256 == release_contract.config_sha256 == expected_boot.config
      switch posture   release_contract.switch_posture == the manifest's own vars
      override hooks   release_contract.must_be_unset are actually UNSET in the build environment
      F5 sealed input  RECOMPUTED seal == the file's stored seal == the seal stamped on the board of record
    """
    env = os.environ if env is None else env
    root = os.path.abspath(repo_root)

    def _load(rel):
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            raise ForwardAuthorityError("authority of record missing: %s" % rel)
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except ValueError as e:
            raise ForwardAuthorityError("authority of record unparseable: %s (%s)" % (rel, e))

    man, con, boot, f5 = (_load(MODEL_CONFIG_REL), _load(RELEASE_CONTRACT_REL_),
                          _load(EXPECTED_BOOT_REL_), _load(F5_SEALED_INPUT_REL))
    fails = []

    man_seal, con_seal, boot_seal = man.get("config_sha256"), con.get("config_sha256"), boot.get("config")
    if not (man_seal and man_seal == con_seal == boot_seal):
        fails.append("config seal disagreement: model_config=%s release_contract=%s expected_boot=%s"
                     % (str(man_seal)[:12], str(con_seal)[:12], str(boot_seal)[:12]))

    posture = con.get("switch_posture") or {}
    cvars = man.get("vars") or {}
    if not posture:
        fails.append("release_contract carries no switch_posture — the config of record is undeclared")
    for k, v in sorted(posture.items()):
        if k not in cvars:
            fails.append("switch_posture %s is not a manifest var" % k)
        elif str(cvars[k]) != str(v):
            fails.append("switch_posture %s=%r != manifest %r" % (k, v, cvars[k]))

    for k in (con.get("must_be_unset") or []):
        if k in env:
            fails.append("override hook %s is SET (%r) but the release contract declares it must_be_unset"
                         % (k, env[k]))

    recomputed, stored = f5_seal_of(f5), f5.get("seal_sha256_8")
    try:
        bor_meta = ((_load(BOARD_OF_RECORD_REL_).get("phantomTotals") or {}).get("_meta") or {})
        board_seal = bor_meta.get("seal_sha256_8")
    except ForwardAuthorityError:
        board_seal = None
    if recomputed != stored:
        fails.append("F5 sealed input SEAL DRIFT: recomputed %s != stored %s — the sealed entrant structure "
                     "has been edited; re-seal from intake history (never substitute, never regenerate here)"
                     % (recomputed, stored))
    elif board_seal is not None and board_seal != stored:
        fails.append("F5 sealed input seal %s != the seal stamped on the board of record %s"
                     % (stored, board_seal))

    if fails:
        raise ForwardAuthorityError("CONFIG OF RECORD NOT ESTABLISHED — refusing to build the forward "
                                    "view:\n  - " + "\n  - ".join(fails))

    return {"config_sha256": man_seal,
            "switch_posture": {k: str(v) for k, v in posture.items()},
            "must_be_unset": list(con.get("must_be_unset") or []),
            "f5_seal_sha256_8": stored, "f5_sealed_input": F5_SEALED_INPUT_REL,
            "board_of_record_md5": boot.get("board"), "store_md5": boot.get("store"),
            "config_mode": FORWARD_CONFIG_MODE}


# --------------------------------------------------------------------------- naming
def forward_vector_name(board_md5):
    """The forward reference vector's filename, keyed to the round's OWN board identity."""
    return "forward_vector_%s.json" % str(board_md5)[:8]


def forward_oracle_name(board_md5):
    """The forward oracle's filename, keyed to the round's OWN board identity."""
    return "test_forward_lens_%s.py" % str(board_md5)[:8]


# --------------------------------------------------------------------------- the seal
def vector_seal(lenses):
    """Deterministic content seal over the COMPLETE two-lens vector pair. sort_keys makes it independent of
    dict insertion order and of PYTHONHASHSEED; ensure_ascii + separators make it independent of locale."""
    payload = {lbl: lenses[lbl]["vector"] for lbl, _f, _k, _y in FORWARD_LENSES}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- derivation
def derive_forward(board, board_md5, present_vector=None):
    """Derive the complete forward view from a FRESHLY BUILT sibling board object.

    `present_vector` is the present-value (k=0) vector the caller derived from the SAME board; when given,
    G-COHORT is asserted against it. Raises ForwardLensError on any LENS-PROJECTION / G-COHORT / G-Y0
    violation — the forward view fails closed rather than emitting a partial projection."""
    active = board.get("active")
    if not isinstance(active, list) or not active:
        raise ForwardLensError("forward derive: built board has no active list")

    lenses = {}
    key_sets = []
    for lbl, fld, k, yr in FORWARD_LENSES:
        vector = {}
        for p in active:
            key = p.get("key")
            if not key:
                raise ForwardLensError("forward derive: active row without a key (LENS-PROJECTION)")
            if fld not in p or p[fld] is None:
                raise ForwardLensError("forward derive: active row %r has no %s column "
                                       "(LENS-PROJECTION)" % (key, fld))
            val = p[fld]
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise ForwardLensError("forward derive: %s of %r is not numeric (LENS-PROJECTION)"
                                       % (fld, key))
            if int(val) != val:
                raise ForwardLensError("forward derive: %s of %r is not integral (%r) — the forward view "
                                       "is an integer ladder (LENS-PROJECTION)" % (fld, key, val))
            vector[key] = int(val)
        if len(vector) != len(active):
            raise ForwardLensError("forward derive: %s vector has %d keys for %d active rows — duplicate "
                                   "player key (LENS-PROJECTION)" % (fld, len(vector), len(active)))
        key_sets.append(set(vector))

        cons_src = ((board.get("lensConservation") or {}).get(lbl) or {})
        if not cons_src:
            raise ForwardLensError("forward derive: built board carries no lensConservation row for the %s "
                                   "lens (G-Y0 cannot be established)" % lbl)
        cons = {ck: cons_src.get(ck) for ck in _CONSERVATION_KEYS}
        lenses[lbl] = {
            "field": fld,
            "lensYear": yr,
            "offset": k,
            "sum": sum(vector.values()),
            "sheezel": vector.get("harry-sheezel"),
            "conservation": cons,
            "vector": vector,
        }

    # --- G-COHORT: the two forward lenses see ONE cohort ---------------------------------------
    if key_sets[0] != key_sets[1]:
        d = sorted(key_sets[0] ^ key_sets[1])
        raise ForwardLensError("forward derive: +1 and +2 key sets differ at %d key(s) (e.g. %s) — G-COHORT"
                               % (len(d), d[:3]))
    # --- G-COHORT: the forward cohort IS the present cohort ------------------------------------
    if present_vector is not None:
        if key_sets[0] != set(present_vector):
            d = sorted(key_sets[0] ^ set(present_vector))
            raise ForwardLensError("forward derive: forward cohort differs from the present-value cohort at "
                                   "%d key(s) (e.g. %s) — G-COHORT" % (len(d), d[:3]))

    doc = {
        "board_md5": board_md5,
        "active": len(active),
        "lenses": lenses,
    }
    doc["vector_sha256"] = vector_seal(lenses)
    # --- G-Y0 continuity arithmetic, asserted on the artifact just built -----------------------
    for fail in continuity_fails(doc):
        raise ForwardLensError("forward derive: %s" % fail)
    return doc


def continuity_fails(doc):
    """Return a list of G-Y0 / LENS-PROJECTION / seal failure strings for a forward doc (empty == coherent).
    This is the SAME arithmetic on a freshly derived doc and on a doc read back off disk, so a tampered
    committed artifact fails the identical named invariant a bad build would."""
    fails = []
    active = doc.get("active")
    lenses = doc.get("lenses") or {}
    for lbl, fld, _k, yr in FORWARD_LENSES:
        L = lenses.get(lbl)
        if not isinstance(L, dict):
            fails.append("forward view: %s lens missing (LENS-PROJECTION)" % lbl)
            continue
        vec = L.get("vector")
        if not isinstance(vec, dict) or not vec:
            fails.append("forward view: %s vector missing or empty (LENS-PROJECTION)" % lbl)
            continue
        if L.get("field") != fld:
            fails.append("forward view: %s lens field %r != %r (LENS-PROJECTION)" % (lbl, L.get("field"), fld))
        if L.get("lensYear") != yr:
            fails.append("forward view: %s lensYear %r != %d (LENS-PROJECTION)" % (lbl, L.get("lensYear"), yr))
        if len(vec) != active:
            fails.append("forward view: %s vector has %d keys != active %r (LENS-PROJECTION)"
                         % (lbl, len(vec), active))
        try:
            real_sum = sum(int(x) for x in vec.values())
        except (TypeError, ValueError):
            fails.append("forward view: %s vector carries a non-integer value (LENS-PROJECTION)" % lbl)
            continue
        if L.get("sum") != real_sum:
            fails.append("forward view: %s sum %r != sum(vector.values()) %d (G-Y0)"
                         % (lbl, L.get("sum"), real_sum))
        if L.get("sheezel") != vec.get("harry-sheezel"):
            fails.append("forward view: %s sheezel %r != vector['harry-sheezel'] %r (G-Y0)"
                         % (lbl, L.get("sheezel"), vec.get("harry-sheezel")))
        cons = L.get("conservation") or {}
        if cons.get("players") != real_sum:
            fails.append("forward view: %s conservation players %r != sum(vector.values()) %d (G-Y0)"
                         % (lbl, cons.get("players"), real_sum))
        if cons.get("nPlayers") != active:
            fails.append("forward view: %s conservation nPlayers %r != active %r (G-Y0)"
                         % (lbl, cons.get("nPlayers"), active))
        try:
            if cons.get("total") != int(cons.get("players")) + int(cons.get("picks")):
                fails.append("forward view: %s conservation total %r != players + picks (G-Y0)"
                             % (lbl, cons.get("total")))
        except (TypeError, ValueError):
            fails.append("forward view: %s conservation row is not numeric (G-Y0)" % lbl)
        if cons.get("lensYear") != yr:
            fails.append("forward view: %s conservation lensYear %r != %d (G-Y0)"
                         % (lbl, cons.get("lensYear"), yr))

    va = (lenses.get("+1") or {}).get("vector")
    vb = (lenses.get("+2") or {}).get("vector")
    if isinstance(va, dict) and isinstance(vb, dict) and set(va) != set(vb):
        d = sorted(set(va) ^ set(vb))
        fails.append("forward view: +1 and +2 key sets differ at %d key(s) (e.g. %s) — G-COHORT"
                     % (len(d), d[:3]))
    if not fails:
        try:
            if doc.get("vector_sha256") != vector_seal(lenses):
                fails.append("forward view: vector_sha256 seal != recomputed seal over the two-lens vectors")
        except (TypeError, ValueError, KeyError):
            fails.append("forward view: vector_sha256 seal not recomputable")
    return fails


def cohort_fails(doc, present_vector):
    """G-COHORT against the present-value reference vector (the k=0 lens)."""
    lenses = doc.get("lenses") or {}
    fails = []
    for lbl, _f, _k, _y in FORWARD_LENSES:
        vec = (lenses.get(lbl) or {}).get("vector")
        if not isinstance(vec, dict):
            continue
        if set(vec) != set(present_vector or {}):
            d = sorted(set(vec) ^ set(present_vector or {}))
            fails.append("forward view: %s cohort differs from the present-value reference vector at %d "
                         "key(s) (e.g. %s) — G-COHORT" % (lbl, len(d), d[:3]))
    return fails


def compare_to_built(doc, built):
    """Rebuild-and-compare: the LIVE forward doc must equal the FRESHLY BUILT forward view EXACTLY. This is
    the gate that makes `check --full` build-and-compare rather than a stored-literal check — a sum-preserving
    forward corruption (A +1, B -1) leaves every aggregate intact and is caught ONLY here."""
    fails = []
    if doc.get("board_md5") != built.get("board_md5"):
        fails.append("forward view: live board_md5 %s != rebuilt %s"
                     % (str(doc.get("board_md5"))[:8], str(built.get("board_md5"))[:8]))
    if doc.get("active") != built.get("active"):
        fails.append("forward view: live active %r != rebuilt %r" % (doc.get("active"), built.get("active")))
    for lbl, _f, _k, _y in FORWARD_LENSES:
        lv = (doc.get("lenses") or {}).get(lbl) or {}
        bv = (built.get("lenses") or {}).get(lbl) or {}
        for field in ("sum", "sheezel", "lensYear", "field"):
            if lv.get(field) != bv.get(field):
                fails.append("forward view: live %s %s %r != rebuilt %r"
                             % (lbl, field, lv.get(field), bv.get(field)))
        if lv.get("conservation") != bv.get("conservation"):
            fails.append("forward view: live %s conservation row != rebuilt conservation row" % lbl)
        a, b = lv.get("vector") or {}, bv.get("vector") or {}
        if a != b:
            d = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            fails.append("forward view: EXACT-FORWARD-VECTOR MISMATCH on the %s lens — the live forward "
                         "vector differs from the freshly-rebuilt one at %d key(s) (e.g. %s); a "
                         "sum-preserving forward corruption the no-build gate cannot see"
                         % (lbl, len(d), d[:3]))
    if not fails and doc.get("vector_sha256") != built.get("vector_sha256"):
        fails.append("forward view: live vector_sha256 != rebuilt vector_sha256")
    return fails


# --------------------------------------------------------------------------- serialization
def forward_vector_doc(fwd, round_n=None):
    """The on-disk forward reference vector. Ordered/serialized deterministically by the dumper below."""
    doc = dict(fwd)
    doc["_doc"] = ("R%s forward-lens (+1/+2) reference vector — regenerated from the freshly built sibling "
                   "board by the advance transaction (ITEM 408 D2, build-and-compare). "
                   "lenses['+1'|'+2'].vector[key] = the player's vP1|vP2. Derived, never authored; the "
                   "vP1/vP2 math in rl_export.py is not touched by this artifact."
                   % (round_n if round_n is not None else "?"))
    doc["as_of_round"] = round_n
    return doc


def dumps_forward_vector(obj):
    """sort_keys + ensure_ascii + fixed indent => byte-identical output for identical content, independent
    of dict insertion order, PYTHONHASHSEED and locale. No trailing newline (matches the FV reference
    vector's convention so an UNCHANGED regeneration round-trips byte-exact)."""
    return json.dumps(obj, indent=2, ensure_ascii=True, sort_keys=True).encode("utf-8")


# --------------------------------------------------------------------------- the forward oracle
_ORACLE_TEMPLATE = '''#!/usr/bin/env python3
"""FORWARD-LENS ORACLE — GENERATED ARTIFACT. DO NOT EDIT BY HAND.

Regenerated in full by the advance transaction (engine/rl_after/ingestion/sibling_repin.py, ITEM 408 D2)
on every advance, from the freshly built sibling board. Every literal below was DERIVED from that build;
none was authored, transcribed or carried over from a previous round. Editing this file by hand makes it
disagree with the artifact it gates and the advance transaction will HALT on the next plan/check.

It gates the committed forward reference vector on the round's OWN board identity. It contains no
historical board id: %(ref_name)s and the identity below are this round's.

Run:  python3 %(oracle_name)s      (exit 0 == the committed forward view matches this oracle)
"""
import hashlib
import json
import os
import sys

FORWARD_BOARD_MD5_GOOD = '%(board_md5)s'
FORWARD_REFERENCE = '%(ref_name)s'
FORWARD_VECTOR_SHA256 = '%(seal)s'

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, 'fixtures')


def _lens(doc, label):
    return (doc.get('lenses') or {}).get(label) or {}


def main():
    path = os.path.join(FIXTURES, FORWARD_REFERENCE)
    if not os.path.exists(path):
        print('FORWARD ORACLE FAIL: %%s missing' %% FORWARD_REFERENCE)
        return 1
    doc = json.load(open(path, encoding='utf-8'))
    fails = []
    if doc.get('board_md5') != FORWARD_BOARD_MD5_GOOD:
        fails.append('board_md5 %%s != oracle %%s' %% (doc.get('board_md5'), FORWARD_BOARD_MD5_GOOD))
    if doc.get('active') != %(active)d:
        fails.append("doc.get('active') %%r != %(active)d" %% doc.get('active'))
    if _lens(doc, '+1').get('sum') != %(sum_p1)d:
        fails.append("lens('+1').get('sum') %%r != %(sum_p1)d" %% _lens(doc, '+1').get('sum'))
    if _lens(doc, '+2').get('sum') != %(sum_p2)d:
        fails.append("lens('+2').get('sum') %%r != %(sum_p2)d" %% _lens(doc, '+2').get('sum'))
    if _lens(doc, '+1').get('sheezel') != %(sheezel_p1)d:
        fails.append("lens('+1').get('sheezel') %%r != %(sheezel_p1)d" %% _lens(doc, '+1').get('sheezel'))
    if _lens(doc, '+2').get('sheezel') != %(sheezel_p2)d:
        fails.append("lens('+2').get('sheezel') %%r != %(sheezel_p2)d" %% _lens(doc, '+2').get('sheezel'))
    payload = {l: (_lens(doc, l).get('vector') or {}) for l in ('+1', '+2')}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
    seal = hashlib.sha256(blob.encode('utf-8')).hexdigest()
    if seal != FORWARD_VECTOR_SHA256:
        fails.append('vector_sha256 %%s != oracle %%s' %% (seal, FORWARD_VECTOR_SHA256))
    if doc.get('vector_sha256') != FORWARD_VECTOR_SHA256:
        fails.append('stored vector_sha256 %%s != oracle %%s'
                     %% (doc.get('vector_sha256'), FORWARD_VECTOR_SHA256))
    for f in fails:
        print('FORWARD ORACLE FAIL: %%s' %% f)
    if fails:
        return 1
    print('FORWARD ORACLE OK: board %(board8)s active %(active)d '
          '+1 sum %(sum_p1)d sheezel %(sheezel_p1)d | +2 sum %(sum_p2)d sheezel %(sheezel_p2)d '
          '| seal %(seal8)s (expect %(board8)s/%(active)d/%(sum_p1)d/%(sum_p2)d/0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''


def render_forward_oracle(fwd):
    """Render the forward oracle IN FULL from the freshly built forward view. Regeneration is always a
    complete rewrite from derived values — never a patch of the previous round's text — so there is no
    structural-repair failure mode and an unchanged regeneration is byte-identical."""
    l1 = fwd["lenses"]["+1"]
    l2 = fwd["lenses"]["+2"]
    md5 = fwd["board_md5"]
    return _ORACLE_TEMPLATE % {
        "board_md5": md5,
        "board8": md5[:8],
        "ref_name": forward_vector_name(md5),
        "oracle_name": forward_oracle_name(md5),
        "seal": fwd["vector_sha256"],
        "seal8": fwd["vector_sha256"][:8],
        "active": fwd["active"],
        "sum_p1": l1["sum"],
        "sum_p2": l2["sum"],
        "sheezel_p1": l1["sheezel"],
        "sheezel_p2": l2["sheezel"],
    }


def forward_oracle_aggregates(src):
    """Parse the tuple the forward oracle ACTUALLY asserts, out of its source text — so a drift in ANY token
    (even with a correct board id, and even when the forward vector itself is current) is detectable. Mirrors
    sibling_repin._fv_oracle_aggregates for the present lens. Fail closed on an absent/ambiguous token."""
    def one(pattern, what, cast=str):
        m = re.findall(pattern, src)
        uniq = sorted(set(m))
        if not m:
            raise ForwardLensError("forward oracle: token %r not present" % what)
        if len(uniq) != 1:
            raise ForwardLensError("forward oracle: ambiguous %r tokens %s" % (what, uniq[:4]))
        return cast(uniq[0])

    return {
        "board_md5": one(r"FORWARD_BOARD_MD5_GOOD\s*=\s*'([0-9a-fA-F]{32})'", "FORWARD_BOARD_MD5_GOOD"),
        "forward_vector": one(r"FORWARD_REFERENCE\s*=\s*'(forward_vector_[0-9a-fA-F]{8}\.json)'",
                              "FORWARD_REFERENCE"),
        "vector_sha256": one(r"FORWARD_VECTOR_SHA256\s*=\s*'([0-9a-fA-F]{64})'", "FORWARD_VECTOR_SHA256"),
        "active": one(r"doc\.get\('active'\)\s*!=\s*(\d+)", "active", int),
        "sum_p1": one(r"_lens\(doc, '\+1'\)\.get\('sum'\)\s*!=\s*(\d+)", "+1 sum", int),
        "sum_p2": one(r"_lens\(doc, '\+2'\)\.get\('sum'\)\s*!=\s*(\d+)", "+2 sum", int),
        "sheezel_p1": one(r"_lens\(doc, '\+1'\)\.get\('sheezel'\)\s*!=\s*(\d+)", "+1 sheezel", int),
        "sheezel_p2": one(r"_lens\(doc, '\+2'\)\.get\('sheezel'\)\s*!=\s*(\d+)", "+2 sheezel", int),
    }


def oracle_fails(src, fwd_doc):
    """Every way the forward ORACLE can disagree with the forward REFERENCE it gates, each named."""
    fails = []
    try:
        fo = forward_oracle_aggregates(src)
    except ForwardLensError as e:
        return ["forward oracle unreadable: %s" % e]
    l1 = (fwd_doc.get("lenses") or {}).get("+1") or {}
    l2 = (fwd_doc.get("lenses") or {}).get("+2") or {}
    if fo["board_md5"] != fwd_doc.get("board_md5"):
        fails.append("forward oracle FORWARD_BOARD_MD5_GOOD != forward reference board_md5")
    if fo["forward_vector"] != forward_vector_name(str(fwd_doc.get("board_md5"))):
        fails.append("forward oracle FORWARD_REFERENCE filename != regenerated forward vector")
    if fo["vector_sha256"] != fwd_doc.get("vector_sha256"):
        fails.append("forward oracle FORWARD_VECTOR_SHA256 != forward reference vector_sha256")
    if fo["active"] != fwd_doc.get("active"):
        fails.append("forward oracle active != forward reference active")
    if fo["sum_p1"] != l1.get("sum"):
        fails.append("forward oracle +1 sum != forward reference +1 sum")
    if fo["sum_p2"] != l2.get("sum"):
        fails.append("forward oracle +2 sum != forward reference +2 sum")
    if fo["sheezel_p1"] != l1.get("sheezel"):
        fails.append("forward oracle +1 sheezel != forward reference +1 sheezel")
    if fo["sheezel_p2"] != l2.get("sheezel"):
        fails.append("forward oracle +2 sheezel != forward reference +2 sheezel")
    return fails
