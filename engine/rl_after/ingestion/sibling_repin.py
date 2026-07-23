#!/usr/bin/env python3
"""SIBLING ADVANCE-REPIN — ITEM 408 directive item 5 (R2 second half).

The balanced/strict board and the FV reference vector are DERIVED SIBLINGS of the ONE store: they track
the store exactly as the canonical board of record does. When the weekly transaction advances the store +
canonical board (staged_apply), these siblings go stale unless they are regenerated and their pins moved
in lockstep. This module is the scripted, fail-closed, atomic advance-repin that does exactly that — BY
BUILD-AND-COMPARE, never by editing an expectation to match an output that was not rebuilt behind it.

WHAT A `reconcile` DOES:
  1. rebuilds the balanced/strict SIBLING board from the SAME store/config/FV source the round's canonical
     board was built from (the accepted disposable FV builder, RL_PVC2=1/RL_LEGE=0/RL_LEGF=0), asserting
     the store it built from equals the canonical manifest's store pin;
  2. regenerates the COMPLETE FV reference vector from that freshly-built sibling board;
  3. derives the sibling identity + aggregates (board md5, active, present-v sum, sheezel, full vector)
     from the generated artifacts — never from a supplied constant;
  4. if the derived identity already equals the live pins -> NO-OP (idempotent); only the provenance
     sidecar is written if absent/stale;
  5. otherwise STAGES the coherent movement of every dependent pin/aggregate/reference/seal:
       - data/expected_boot.json                 balanced_board_md5 (raw-text move; layout preserved)
       - data/release_contract.json              identities.balanced_board_md5 + present_lens_baseline
                                                  {balanced_board_md5, active, present_value_total} + re-seal
       - fixtures/reference_vector_<md5>.json     regenerated from the built board
       - test_fv_provenance.py                    BOARD_MD5_GOOD + aggregates + reference path
       - ui/data/board_view_{working,public}.js   regenerated via extract_board_view (picks up the pin)
       - engine/rl_after/ingestion/sibling_repin_state.json   provenance sidecar (the cheap gate's record)
  6. VALIDATES the complete staged set on a throwaway OVERLAY BEFORE any live replacement (identity
     coherence across every staged target + the release-contract self-seal + a fail-closed
     release_contract.verify on the overlay);
  7. COMMITS by atomic os.replace of each changed live target, journaled, with a backup of every original;
  8. ROLLS BACK — restoring every original byte-for-byte — if a fault occurs during replacement;
  9. is IDEMPOTENT (a current tree is a no-op) and REPAIRABLE (an incomplete txn is rolled back on the
     next run / by `rollback`).

FENCES (absolute):
  - NEVER touches the board of record (data/rl_build/rl_app_data.json), the store, the frozen pick curve
    (engine/rl_after/pvc_curve_v2.json), the curve contract (ui/release_pick_curve.json), the committed
    per_entrant or the score ledger. All are asserted byte-unchanged before/after every reconcile.
  - NEVER arms or reads the score-write gate; it applies NO scores (derived-artifact repin only).
  - BUILD-AND-COMPARE ONLY: the pin is moved to a value that was just BUILT and derived from the built
    artifact.

CLI:
  python3 sibling_repin.py plan       [--repo R]              # build + derive + print the plan (no writes)
  python3 sibling_repin.py reconcile  [--repo R] [--round N]  # the transaction (no-op if current)
  python3 sibling_repin.py check      [--repo R] [--full]     # gate: exit != 0 if siblings stale
  python3 sibling_repin.py verify     [--repo R]              # assert live siblings coherent (no build)
  python3 sibling_repin.py rollback   [--repo R] [--txn D]    # roll back an incomplete txn
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

STORE_REL = "engine/rl_after/rl_model_data.json"
BOARD_OF_RECORD_REL = "data/rl_build/rl_app_data.json"
EXPECTED_BOOT_REL = "data/expected_boot.json"
RELEASE_CONTRACT_REL = "data/release_contract.json"
FV_TEST_REL = "session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py"
FV_FIX_REL = "session_2026-07-20/fv_provenance_remediation/fixtures"
BOARD_VIEW_WORKING_REL = "ui/data/board_view_working.js"
BOARD_VIEW_PUBLIC_REL = "ui/data/board_view_public.js"
EXTRACT_BOARD_VIEW_REL = "ui/tools/extract_board_view.py"
RELEASE_CONTRACT_TOOL_REL = "release_contract.py"
SIDECAR_REL = "engine/rl_after/ingestion/sibling_repin_state.json"
FORWARD_VALUATION_REL = "engine/forward_valuation"
TXN_DIRNAME = ".sibling_txn"

# Frozen artifacts this repin must NEVER mutate (asserted byte-unchanged before/after every reconcile).
FROZEN_REL = {
    "board_of_record": BOARD_OF_RECORD_REL,
    "store": STORE_REL,
    "curve": "engine/rl_after/pvc_curve_v2.json",
    "curve_contract": "ui/release_pick_curve.json",
    "per_entrant": "session_2026-07-17/legd_derivation/out/per_entrant.json",
    "score_ledger": "engine/rl_after/ingestion/applied_rounds_ledger.json",
    "season_state": "data/season_state.json",
}

SCHEMA_VERSION = 1
_TERMINAL = ("COMMITTED", "ROLLED_BACK", "ABORTED_PRECOMMIT")


class SiblingRepinError(RuntimeError):
    """Any fail-closed condition in the advance-repin (build/derive/validate/commit)."""


class SiblingStaleError(SiblingRepinError):
    """The live sibling identities are stale relative to a freshly-built sibling (the gate raises this)."""


class SiblingBuildError(SiblingRepinError):
    """The sibling board build did not complete (rc != 0 / no board)."""


class SiblingFault(RuntimeError):
    """A deliberately injected fault (failure-injection proof only)."""


# --------------------------------------------------------------------------- io + serialization
def _md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 16), b""):
            h.update(ch)
    return h.hexdigest()


def _md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def _read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def _atomic_write_bytes(path, data):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".sr_", dir=d)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# On-disk serialization is format-specific so an UNCHANGED reconcile is byte-identical:
#   release_contract.json  -> indent=2, ensure_ascii, trailing newline  (round-trips byte-exact)
#   reference_vector_*.json -> indent=2, ensure_ascii, NO trailing newline (round-trips byte-exact)
#   expected_boot.json      -> NOT re-serialized; a raw-text token move preserves its exact layout.
def _dumps_contract(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def _dumps_refvec(obj):
    return json.dumps(obj, indent=2, ensure_ascii=True).encode("utf-8")


def _dumps_sidecar(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _replace_once(text, old, new, what):
    if old == new:
        return text
    c = text.count(old)
    if c != 1:
        raise SiblingRepinError("FV-oracle edit '%s': expected 1 occurrence of %r, found %d"
                                % (what, old, c))
    return text.replace(old, new)


def _replace_required(text, old, new, what):
    if old == new:
        return text
    if old not in text:
        raise SiblingRepinError("FV-oracle edit '%s': token %r not present" % (what, old))
    return text.replace(old, new)


def _extract_fv_board_md5(fv_src):
    marker = "BOARD_MD5_GOOD = '"
    i = fv_src.index(marker) + len(marker)
    return fv_src[i:fv_src.index("'", i)]


def _extract_fv_int(fv_src, field):
    """Parse the FV oracle's `…get('<field>') == <int>` build-and-compare aggregate assertion."""
    m = re.search(r"'%s'\)\s*==\s*(\d+)" % re.escape(field), fv_src)
    if not m:
        raise SiblingRepinError("FV oracle: `'%s') == <int>` assertion not found" % field)
    return int(m.group(1))


def _fv_oracle_aggregates(fv_src):
    """The full build-and-compare tuple the FV oracle asserts — the accepted board id, the DERIVED active
    count, the present-v sum, the Sheezel value and the regenerated reference-vector filename. A drift in
    ANY of them (even with a correct board id) is therefore detectable (blocking correction 2)."""
    md5 = _extract_fv_board_md5(fv_src)
    ref = _reference_vector_name(md5)
    return {"board_md5": md5, "active": _extract_fv_int(fv_src, "active"),
            "sum_v": _extract_fv_int(fv_src, "sum_v"), "sheezel": _extract_fv_int(fv_src, "sheezel"),
            "reference_vector": ref, "reference_vector_present": ref in fv_src}


def _board_view_coherence(root, *, balanced_md5, canonical_board, store, as_of_round, release_version,
                          canonical_active=None):
    """Return a list of incoherence strings for the TWO board-view bundles under `root` (empty == coherent).
    Covers the FULL board-view set (blocking correction 2):
      - both working and public bundles exist and parse;
      - the working stamp's balanced-board, canonical-board, store, round and release identities agree with
        the supplied (staged manifest / built sibling) values;
      - the public bundle's player count and name/value rows agree with the working bundle (and, when given,
        the staged canonical board's active list);
      - the public bundle remains LEAK-FREE — no player identity (key/stable_player_id), no provenance
        stamp (srcmd5/store/board/balanced/register/guard5) — the two-tier UI law."""
    wp = os.path.join(root, BOARD_VIEW_WORKING_REL)
    pp = os.path.join(root, BOARD_VIEW_PUBLIC_REL)
    fails = []
    if not os.path.exists(wp):
        fails.append("working board view missing")
    if not os.path.exists(pp):
        fails.append("public board view missing")
    if fails:
        return fails
    try:
        w = _parse_bundle(wp)
    except (OSError, ValueError) as e:
        return ["working board view unparseable: %s" % e]
    try:
        p = _parse_bundle(pp)
    except (OSError, ValueError) as e:
        return ["public board view unparseable: %s" % e]
    st = w.get("stamp", {})
    if st.get("balanced_board_md5") != balanced_md5:
        fails.append("working balanced_board_md5 stamp != %s" % str(balanced_md5)[:8])
    if str(st.get("board", ""))[:8] != str(canonical_board)[:8]:
        fails.append("working canonical board stamp != %s" % str(canonical_board)[:8])
    if str(st.get("store", ""))[:8] != str(store)[:8]:
        fails.append("working store stamp != %s" % str(store)[:8])
    if as_of_round is not None and st.get("asOfRound") != as_of_round:
        fails.append("working asOfRound stamp %s != %s" % (st.get("asOfRound"), as_of_round))
    if release_version is not None and st.get("releaseVersion") != release_version:
        fails.append("working releaseVersion stamp %s != %s" % (st.get("releaseVersion"), release_version))
    wr, pr = w.get("players", []), p.get("players", [])
    if len(pr) != len(wr):
        fails.append("public player count %d != working %d" % (len(pr), len(wr)))
    else:
        mism = sum(1 for a, b in zip(wr, pr) if a.get("name") != b.get("name") or a.get("v") != b.get("v"))
        if mism:
            fails.append("public rows disagree with working on name/value for %d player(s)" % mism)
    if canonical_active is not None:
        if len(pr) != len(canonical_active):
            fails.append("public player count %d != canonical active %d" % (len(pr), len(canonical_active)))
        else:
            mism = sum(1 for a, b in zip(canonical_active, pr)
                       if a.get("name") != b.get("name") or a.get("v") != b.get("v"))
            if mism:
                fails.append("public rows disagree with the canonical board for %d player(s)" % mism)
    if any(k in (row or {}) for row in pr for k in ("key", "stable_player_id")):
        fails.append("public bundle leaks a player identity (key/stable_player_id)")
    if any(k in (p.get("stamp") or {}) for k in ("srcmd5", "store", "store_md5", "board", "board_md5",
                                                 "balanced_board_md5", "register", "guard5")):
        fails.append("public bundle stamp leaks provenance (srcmd5/store/board/register/guard5)")
    return fails


def _reference_vector_name(board_md5):
    return "reference_vector_%s.json" % board_md5[:8]


def _reference_vector_doc(sib, round_n=None):
    return {
        "_doc": ("R%s balanced/strict FV reference vector — regenerated from the freshly built sibling "
                 "board by sibling_repin.py (ITEM 408 item 5, build-and-compare). vector[key]=present-v."
                 % (round_n if round_n is not None else "?")),
        "active": sib["active"],
        "board_md5": sib["board_md5"],
        "sum_v": sib["sum_v"],
        "vector": sib["vector"],
    }


# --------------------------------------------------------------------------- the sibling build
def build_sibling(repo_root):
    """Rebuild the balanced/strict SIBLING board from repo_root's store/config/FV source via the accepted
    disposable FV builder (RL_PVC2=1/RL_LEGE=0/RL_LEGF=0). Returns a derived-identity dict. Fail-closed on
    a non-zero build. Writes NOTHING under repo_root (the builder stages into a throwaway dir)."""
    repo_root = os.path.abspath(repo_root)
    fv_test = os.path.join(repo_root, FV_TEST_REL)
    if not os.path.exists(fv_test):
        raise SiblingBuildError("FV builder missing: %s" % fv_test)
    store_md5 = _md5_file(os.path.join(repo_root, STORE_REL))
    prev = os.environ.get("RL_REPO")
    os.environ["RL_REPO"] = repo_root
    result = None
    try:
        mod = _load_module("sibling_fv_builder_%s" % _md5_bytes(repo_root.encode())[:8], fv_test)
        if os.path.abspath(mod.REPO) != repo_root:
            raise SiblingBuildError("FV builder resolved REPO %s != %s" % (mod.REPO, repo_root))
        result = mod._run_build({}, rl_fv=os.path.join(repo_root, FORWARD_VALUATION_REL), balanced=True)
        if result.get("rc") != 0 or not result.get("board_path"):
            tail = " | ".join((result.get("stderr") or "").strip().splitlines()[-4:])
            raise SiblingBuildError("sibling board build failed: rc=%s :: %s" % (result.get("rc"), tail))
        board = _read_json(result["board_path"])
        active = board["active"]
        vector = {p["key"]: int(p["v"]) for p in active}
        prov = result.get("prov") or {}
        return {
            "board_md5": result["board_md5"],
            "active": len(active),
            "sum_v": sum(int(p["v"]) for p in active),
            "sheezel": vector.get("harry-sheezel"),
            "vector": vector,
            "source_store_md5": store_md5,
            "fv_identity": prov.get("fv_identity"),
            "rl_model_md5": prov.get("rl_model_md5"),
        }
    finally:
        if result and result.get("base") and os.path.isdir(result["base"]):
            shutil.rmtree(result["base"], ignore_errors=True)
        if prev is None:
            os.environ.pop("RL_REPO", None)
        else:
            os.environ["RL_REPO"] = prev


# --------------------------------------------------------------------------- the repin plan
class RepinPlan:
    """A build-and-compare plan: the freshly-built sibling identity + the exact per-target new bytes and a
    SEMANTIC per-target `changed` flag. `changed` is True iff any dependent pin must actually move."""

    def __init__(self, repo_root, sib, round_n=None):
        self.repo_root = os.path.abspath(repo_root)
        self.sib = sib
        self.round_n = round_n
        self.new_md5 = sib["board_md5"]
        self.targets = {}          # name -> (repo_rel_path, new_bytes)
        self.changed_map = {}      # name -> bool
        self.live_balanced = None
        self._contract_seal = None
        self._compute()

    def _p(self, rel):
        return os.path.join(self.repo_root, rel)

    def _compute(self):
        sib = self.sib
        new_md5 = self.new_md5

        boot_raw = _read_bytes(self._p(EXPECTED_BOOT_REL))
        boot = json.loads(boot_raw)
        self.live_balanced = boot.get("balanced_board_md5")
        if sib["source_store_md5"] != str(boot.get("store")):
            raise SiblingRepinError("sibling built from store %s != canonical manifest store %s — refusing "
                                    "to repin siblings off a different store"
                                    % (sib["source_store_md5"][:8], str(boot.get("store"))[:8]))
        old_md5 = str(self.live_balanced)
        old8, new8 = old_md5[:8], new_md5[:8]

        # --- expected_boot: raw-text move of the balanced md5 token (layout preserved) ---
        boot_new = boot_raw
        if old_md5 != new_md5:
            boot_new = boot_raw.replace(old_md5.encode(), new_md5.encode()).replace(old8.encode(),
                                                                                    new8.encode())
        self.targets["manifest"] = (EXPECTED_BOOT_REL, boot_new)
        self.changed_map["manifest"] = (boot.get("balanced_board_md5") != new_md5)

        # --- release_contract: structural edit + byte-exact re-serialize + re-seal ---
        rc_tool = _load_module("sr_release_contract", self._p(RELEASE_CONTRACT_TOOL_REL))
        contract = _read_json(self._p(RELEASE_CONTRACT_REL))
        before_id = contract.get("identities", {}).get("balanced_board_md5")
        before_plb = dict(contract.get("present_lens_baseline", {}))
        contract.setdefault("identities", {})["balanced_board_md5"] = new_md5
        plb = contract.setdefault("present_lens_baseline", {})
        plb["balanced_board_md5"] = new_md5
        plb["active"] = sib["active"]
        plb["present_value_total"] = sib["sum_v"]
        if isinstance(plb.get("note"), str) and old_md5 != new_md5:
            plb["note"] = plb["note"].replace(old_md5, new_md5).replace(old8, new8)
        contract.pop("contract_sha256", None)
        contract["contract_sha256"] = rc_tool.contract_hash(contract)
        self._contract_seal = contract["contract_sha256"]
        self.targets["release_contract"] = (RELEASE_CONTRACT_REL, _dumps_contract(contract))
        self.changed_map["release_contract"] = (
            before_id != new_md5 or before_plb.get("balanced_board_md5") != new_md5
            or before_plb.get("active") != sib["active"]
            or before_plb.get("present_value_total") != sib["sum_v"])

        # --- FV reference vector (semantic: missing OR data differs) ---
        ref_name = _reference_vector_name(new_md5)
        ref_rel = os.path.join(FV_FIX_REL, ref_name)
        self.targets["reference_vector"] = (ref_rel, _dumps_refvec(_reference_vector_doc(sib, self.round_n)))
        ref_changed = True
        ref_live = self._p(ref_rel)
        if os.path.exists(ref_live):
            try:
                cur = _read_json(ref_live)
                ref_changed = not (cur.get("board_md5") == new_md5 and cur.get("active") == sib["active"]
                                   and cur.get("sum_v") == sib["sum_v"] and cur.get("vector") == sib["vector"])
            except (OSError, ValueError):
                ref_changed = True
        self.changed_map["reference_vector"] = ref_changed

        # --- FV test oracle constants (build-and-compare; anchored, fail-closed edits). EVERY generated
        #     assertion/expectation is derived from the built artifact — the ACTIVE COUNT, the present-v sum
        #     and the Sheezel value all come from the built sibling vector (never a literal 804). ---
        fv_src = open(self._p(FV_TEST_REL), encoding="utf-8").read()
        cur_md5 = _extract_fv_board_md5(fv_src)
        cur8 = cur_md5[:8]
        cur_ref = _reference_vector_name(cur_md5)
        cur_ref_doc = _read_json(self._p(os.path.join(FV_FIX_REL, cur_ref)))
        cur_active = cur_ref_doc["active"]
        cur_sumv, cur_sheez = cur_ref_doc["sum_v"], cur_ref_doc["vector"].get("harry-sheezel")
        new_active, new_sumv, new_sheez = sib["active"], sib["sum_v"], sib["sheezel"]
        new_src = fv_src
        new_src = _replace_required(new_src, cur_ref, ref_name, "reference filename")
        new_src = _replace_required(new_src, cur_md5, new_md5, "BOARD_MD5_GOOD/full md5")
        if cur8 != new8 and cur8 in new_src:                       # remaining 8-char refs (names/strings)
            new_src = new_src.replace(cur8, new8)
        new_src = _replace_once(new_src, "'active') == %d" % cur_active,
                                "'active') == %d" % new_active, "active aggregate")
        new_src = _replace_once(new_src, "'sum_v') == %d" % cur_sumv,
                                "'sum_v') == %d" % new_sumv, "sum_v aggregate")
        new_src = _replace_once(new_src, "'sheezel') == %d" % cur_sheez,
                                "'sheezel') == %d" % new_sheez, "sheezel aggregate")
        # the "(expect <md5>/<active>/<sum_v>/<sheezel>/0)" record + docstring triple — active derived too
        new_src = _replace_required(new_src, "%d/%d/%d" % (cur_active, cur_sumv, cur_sheez),
                                    "%d/%d/%d" % (new_active, new_sumv, new_sheez), "expect-string aggregate")
        self.targets["fv_test"] = (FV_TEST_REL, new_src.encode("utf-8"))
        self.changed_map["fv_test"] = (cur_md5 != new_md5 or cur_active != new_active
                                       or cur_sumv != new_sumv or cur_sheez != new_sheez)

        # --- board-view coherence (blocking correction 2): a view-only corruption (stale/tampered working
        #     OR public bundle) must NOT read as a no-op. `changed` here forces a reconcile that regenerates
        #     and re-commits both bundles even when the manifest/contract/FV board id are already current. ---
        self.changed_map["board_view"] = bool(_board_view_coherence(
            self.repo_root, balanced_md5=new_md5, canonical_board=boot.get("board"),
            store=boot.get("store"), as_of_round=boot.get("as_of_round"),
            release_version=boot.get("release_version")))

        # --- sidecar coherence (blocking correction 2): a sidecar-only aggregate/reference/seal drift must
        #     likewise force a repair, not a no-op. ---
        want_sc = {"source_store_md5": sib["source_store_md5"], "balanced_board_md5": new_md5,
                   "active": sib["active"], "present_value_total": sib["sum_v"],
                   "harry_sheezel": sib["sheezel"], "reference_vector": _reference_vector_name(new_md5),
                   "contract_sha256": self._contract_seal}
        sc_live = None
        scp = self._p(SIDECAR_REL)
        if os.path.exists(scp):
            try:
                sc_live = _read_json(scp)
            except (OSError, ValueError):
                sc_live = None
        self.changed_map["sidecar"] = (sc_live is None
                                       or any(sc_live.get(k) != v for k, v in want_sc.items()))

        self.changed = any(self.changed_map.values())

    def changed_targets(self):
        # ONLY the file-byte targets carried in self.targets (manifest / release_contract / reference_vector
        # / fv_test). The board_view + sidecar coherence flags also live in changed_map but are NOT
        # pre-computed byte targets — reconcile regenerates the board view via extract_board_view and writes
        # the sidecar from sidecar_doc — so they are committed separately and must be skipped here.
        return {n: self.targets[n] for n, c in self.changed_map.items() if c and n in self.targets}

    def sidecar_doc(self, generated_at_commit=None):
        return {
            "kind": "sibling_repin_state",
            "schema_version": SCHEMA_VERSION,
            "as_of_round": self.round_n,
            "source_store_md5": self.sib["source_store_md5"],
            "balanced_board_md5": self.new_md5,
            "active": self.sib["active"],
            "present_value_total": self.sib["sum_v"],
            "harry_sheezel": self.sib["sheezel"],
            "reference_vector": _reference_vector_name(self.new_md5),
            "contract_sha256": self._contract_seal,
            "fv_identity": self.sib.get("fv_identity"),
            "generated_at_commit": generated_at_commit,
        }


def _parse_bundle(path):
    s = open(path, encoding="utf-8").read()
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


# --------------------------------------------------------------------------- the transaction
class SiblingRepin:
    def __init__(self, repo_root=None, *, fault=None, txn_root=None):
        self.repo_root = os.path.abspath(repo_root or DEFAULT_REPO)
        self.fault = fault
        self.txn_root = txn_root or os.path.join(self.repo_root, "engine", "rl_after", "ingestion",
                                                 TXN_DIRNAME)

    def _p(self, rel):
        return os.path.join(self.repo_root, rel)

    def _fault(self, point):
        if self.fault is not None:
            self.fault(point)

    def _frozen_snapshot(self):
        return {n: (_md5_file(self._p(r)) if os.path.exists(self._p(r)) else None)
                for n, r in FROZEN_REL.items()}

    def _assert_frozen_unchanged(self, before):
        after = self._frozen_snapshot()
        moved = [n for n in FROZEN_REL if before.get(n) != after.get(n)]
        if moved:
            raise SiblingRepinError("FROZEN ARTIFACT MUTATED by advance-repin: %s (must never happen)"
                                    % moved)
        return after

    def _regen_board_view(self, root):
        """Regenerate ui/data/board_view_{working,public}.js under `root` from ITS expected_boot (which,
        in the overlay, already carries the advanced balanced pin). Returns the two paths."""
        ev = self._p(EXTRACT_BOARD_VIEW_REL)
        env = dict(os.environ)
        env["RL_UI_SRC"] = os.path.join(root, BOARD_OF_RECORD_REL)
        env["RL_UI_BOOT"] = os.path.join(root, EXPECTED_BOOT_REL)
        env["RL_UI_STORE"] = os.path.join(root, STORE_REL)
        env["RL_UI_OUT_DIR"] = os.path.join(root, "ui", "data")
        p = subprocess.run([sys.executable, ev], capture_output=True, text=True, env=env)
        if p.returncode != 0:
            raise SiblingRepinError("extract_board_view failed rc=%s :: %s"
                                    % (p.returncode, (p.stderr or "").strip()[-300:]))
        return (os.path.join(root, BOARD_VIEW_WORKING_REL), os.path.join(root, BOARD_VIEW_PUBLIC_REL))

    def _build_overlay(self):
        """A lightweight validation overlay: symlink every top-level repo entry into a temp root
        (read-only reuse of the large trees incl. `engine`/the store), then de-symlink into REAL copies
        only the small trees that receive staged writes (`data`, `ui`) and the written FV subtree. Writes
        during validation therefore never reach a live path; read-only validators resolve through the
        symlinks to the real (unchanged) bytes."""
        overlay = tempfile.mkdtemp(prefix="sibling_overlay_")
        for entry in os.listdir(self.repo_root):
            os.symlink(os.path.join(self.repo_root, entry), os.path.join(overlay, entry))
        for comp in ("data", "ui"):
            link = os.path.join(overlay, comp)
            if os.path.islink(link):
                os.unlink(link)
            shutil.copytree(os.path.join(self.repo_root, comp), link, symlinks=False)
        sess = "session_2026-07-20"
        sess_link = os.path.join(overlay, sess)
        if os.path.islink(sess_link):
            os.unlink(sess_link)
        os.makedirs(sess_link)
        for sub in os.listdir(os.path.join(self.repo_root, sess)):
            s_src = os.path.join(self.repo_root, sess, sub)
            s_dst = os.path.join(sess_link, sub)
            if sub == "fv_provenance_remediation":
                shutil.copytree(s_src, s_dst, symlinks=False)
            else:
                os.symlink(s_src, s_dst)
        return overlay

    def _validate_overlay(self, plan, overlay):
        """Assert full identity coherence across the overlay's staged set + the contract self-seal +
        py_compile of the FV test + a fail-closed release_contract.verify. Raises before any live write."""
        new_md5 = plan.new_md5

        boot = _read_json(os.path.join(overlay, EXPECTED_BOOT_REL))
        if boot.get("balanced_board_md5") != new_md5:
            raise SiblingRepinError("overlay expected_boot.balanced_board_md5 != built %s" % new_md5[:8])

        contract = _read_json(os.path.join(overlay, RELEASE_CONTRACT_REL))
        rc_tool = _load_module("sr_rc_validate", os.path.join(overlay, RELEASE_CONTRACT_TOOL_REL))
        if contract["identities"]["balanced_board_md5"] != new_md5:
            raise SiblingRepinError("overlay contract identities.balanced_board_md5 != built")
        plb = contract["present_lens_baseline"]
        if not (plb["balanced_board_md5"] == new_md5 and plb["active"] == plan.sib["active"]
                and plb["present_value_total"] == plan.sib["sum_v"]):
            raise SiblingRepinError("overlay contract present_lens_baseline incoherent with built sibling")
        if contract.get("contract_sha256") != rc_tool.contract_hash(contract):
            raise SiblingRepinError("overlay contract self-seal mismatch (re-seal failed)")

        ref = _read_json(os.path.join(overlay, FV_FIX_REL, _reference_vector_name(new_md5)))
        if not (ref["board_md5"] == new_md5 and ref["active"] == plan.sib["active"]
                and ref["sum_v"] == plan.sib["sum_v"] and ref["vector"] == plan.sib["vector"]):
            raise SiblingRepinError("overlay reference vector incoherent with built sibling")

        fv_src = open(os.path.join(overlay, FV_TEST_REL), encoding="utf-8").read()
        if _extract_fv_board_md5(fv_src) != new_md5:
            raise SiblingRepinError("overlay FV test BOARD_MD5_GOOD != built")
        if _reference_vector_name(new_md5) not in fv_src:
            raise SiblingRepinError("overlay FV test does not reference the regenerated vector")
        subprocess.run([sys.executable, "-m", "py_compile", os.path.join(overlay, FV_TEST_REL)],
                       check=True, capture_output=True)

        bvw = _parse_bundle(os.path.join(overlay, BOARD_VIEW_WORKING_REL))
        st = bvw.get("stamp", {})
        if st.get("balanced_board_md5") != new_md5:
            raise SiblingRepinError("overlay board_view balanced_board_md5 stamp != built")
        if str(st.get("board", ""))[:8] != str(boot.get("board", ""))[:8]:
            raise SiblingRepinError("overlay board_view board-of-record stamp drifted (must be unchanged)")

        env = dict(os.environ)
        env["RL_CONFIG_MODE"] = "gate"
        p = subprocess.run([sys.executable, os.path.join(overlay, RELEASE_CONTRACT_TOOL_REL), "check"],
                           capture_output=True, text=True, env=env, cwd=overlay)
        if p.returncode != 0:
            raise SiblingRepinError("overlay release_contract check FAILED: %s"
                                    % ((p.stdout + p.stderr).strip()[-300:]))
        return {"release_contract_check": (p.stdout or "").strip().splitlines()[-1:]}

    # -- the public transaction ------------------------------------------------------------------
    def reconcile(self, *, round_n=None, generated_at_commit=None):
        """Build -> derive -> (no-op | stage -> validate -> atomic commit). Idempotent + fail-closed."""
        frozen_before = self._frozen_snapshot()
        recovered = self._recover_incomplete()      # roll back any incomplete prior txn first (repairable)

        sib = build_sibling(self.repo_root)
        if round_n is None:
            round_n = _read_json(self._p(EXPECTED_BOOT_REL)).get("as_of_round")
        plan = RepinPlan(self.repo_root, sib, round_n=round_n)
        sidecar = plan.sidecar_doc(generated_at_commit)

        if not plan.changed:
            # NO-OP: dependent pins already equal the freshly-built sibling identity (idempotent). No pin
            # moves; only the provenance sidecar (the cheap gate's record) is written if absent/stale.
            self._assert_frozen_unchanged(frozen_before)
            wrote_sidecar = self._refresh_sidecar_if_stale(sidecar)
            return {"ok": True, "changed": False, "no_op": True, "balanced_board_md5": plan.new_md5,
                    "active": sib["active"], "sum_v": sib["sum_v"], "sheezel": sib["sheezel"],
                    "wrote_sidecar": wrote_sidecar, "recovered": recovered}

        # STALE -> stage changed targets on an overlay, validate, then commit atomically.
        overlay = self._build_overlay()
        txn_dir = None
        try:
            changed = plan.changed_targets()
            for name, (rel, data) in changed.items():
                _atomic_write_bytes(os.path.join(overlay, rel), data)
            self._regen_board_view(overlay)
            self._fault("before_validation")
            validation = self._validate_overlay(plan, overlay)

            commit_targets = dict(changed)
            # the balanced pin moved OR a view-only corruption was detected -> both board-view bundles are
            # regenerated on the overlay and committed (blocking correction 2: view-only repair, not a no-op).
            if plan.changed_map.get("manifest") or plan.changed_map.get("board_view"):
                for name, rel in (("board_view_working", BOARD_VIEW_WORKING_REL),
                                  ("board_view_public", BOARD_VIEW_PUBLIC_REL)):
                    commit_targets[name] = (rel, _read_bytes(os.path.join(overlay, rel)))
            commit_targets["sidecar"] = (SIDECAR_REL, _dumps_sidecar(sidecar))

            txn_dir = self._open_txn(plan, round_n)
            self._stage_and_backup(txn_dir, commit_targets)
            self._fault("after_stage_before_commit")
            self._commit(txn_dir, commit_targets)
            self._mark(txn_dir, "COMMITTED")
            self._assert_frozen_unchanged(frozen_before)
            return {"ok": True, "changed": True, "no_op": False, "balanced_board_md5": plan.new_md5,
                    "active": sib["active"], "sum_v": sib["sum_v"], "sheezel": sib["sheezel"],
                    "old_balanced_board_md5": plan.live_balanced, "txn_dir": txn_dir,
                    "committed_targets": sorted(commit_targets), "validation": validation,
                    "recovered": recovered}
        except BaseException as exc:
            if txn_dir is not None:
                self._handle_failure(txn_dir, exc)
            self._assert_frozen_unchanged(frozen_before)      # live frozen artifacts must be intact
            raise
        finally:
            shutil.rmtree(overlay, ignore_errors=True)

    # -- txn journal + commit + rollback ---------------------------------------------------------
    def _open_txn(self, plan, round_n):
        os.makedirs(self.txn_root, exist_ok=True)
        txn_id = "txn_%s_%s" % (round_n, plan.new_md5[:8])
        txn_dir = os.path.join(self.txn_root, txn_id)
        if os.path.isdir(txn_dir):
            shutil.rmtree(txn_dir)
        os.makedirs(os.path.join(txn_dir, "staged"))
        os.makedirs(os.path.join(txn_dir, "originals"))
        self._write_manifest(txn_dir, {"txn_id": txn_id, "round": round_n,
                                       "new_balanced_board_md5": plan.new_md5,
                                       "old_balanced_board_md5": plan.live_balanced, "status": "STAGING"})
        self._journal(txn_dir, "STAGE_BEGIN", round=round_n, new_md5=plan.new_md5)
        return txn_dir

    def _write_manifest(self, txn_dir, man):
        _atomic_write_bytes(os.path.join(txn_dir, "manifest.json"),
                            (json.dumps(man, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    def _read_manifest(self, txn_dir):
        p = os.path.join(txn_dir, "manifest.json")
        return _read_json(p) if os.path.exists(p) else None

    def _mark(self, txn_dir, status):
        man = self._read_manifest(txn_dir) or {}
        man["status"] = status
        self._write_manifest(txn_dir, man)
        self._journal(txn_dir, "STATUS", status=status)

    def _journal(self, txn_dir, event, **fields):
        line = {"event": event}
        line.update(fields)
        with open(os.path.join(txn_dir, "journal.jsonl"), "a") as f:
            f.write(json.dumps(line, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _stage_and_backup(self, txn_dir, targets):
        for name, (rel, data) in sorted(targets.items()):
            _atomic_write_bytes(os.path.join(txn_dir, "staged", name), data)
            live = self._p(rel)
            if os.path.exists(live):
                shutil.copy2(live, os.path.join(txn_dir, "originals", name))
            else:
                with open(os.path.join(txn_dir, "originals", name + ".ABSENT"), "w") as f:
                    f.write(rel)       # record ABSENT so rollback removes a first-time artifact
        man = self._read_manifest(txn_dir)
        man["targets"] = {name: rel for name, (rel, _d) in targets.items()}
        man["status"] = "VALIDATED"
        self._write_manifest(txn_dir, man)
        self._journal(txn_dir, "STAGED_AND_BACKED_UP", targets=sorted(targets))

    def _commit(self, txn_dir, targets):
        self._mark(txn_dir, "COMMITTING")
        self._journal(txn_dir, "COMMIT_BEGIN", order=sorted(targets))
        first = True
        for name, (rel, data) in sorted(targets.items()):
            _atomic_write_bytes(self._p(rel), data)
            self._journal(txn_dir, "REPLACED", target=name, path=rel)
            self._fault("after_first_replacement" if first else "after_subsequent_replacement")
            first = False
        self._journal(txn_dir, "COMMIT_OK")

    def _restore_from_txn(self, txn_dir):
        man = self._read_manifest(txn_dir) or {}
        for name, rel in sorted((man.get("targets") or {}).items()):
            orig = os.path.join(txn_dir, "originals", name)
            live = self._p(rel)
            if os.path.exists(orig):
                _atomic_write_bytes(live, _read_bytes(orig))
            elif os.path.exists(orig + ".ABSENT") and os.path.exists(live):
                os.remove(live)
            self._journal(txn_dir, "RESTORED", target=name)
        self._mark(txn_dir, "ROLLED_BACK")

    def _handle_failure(self, txn_dir, exc):
        man = self._read_manifest(txn_dir) or {}
        self._journal(txn_dir, "FAILURE", status=man.get("status"), error=repr(exc)[:200])
        if man.get("status") == "COMMITTING":
            self._restore_from_txn(txn_dir)
        else:
            self._mark(txn_dir, "ABORTED_PRECOMMIT")

    def _incomplete_txns(self):
        if not os.path.isdir(self.txn_root):
            return []
        out = []
        for d in sorted(os.listdir(self.txn_root)):
            td = os.path.join(self.txn_root, d)
            man = self._read_manifest(td)
            if man and man.get("status") not in _TERMINAL:
                out.append(td)
        return out

    def _recover_incomplete(self):
        recovered = []
        for td in self._incomplete_txns():
            self._restore_from_txn(td)
            recovered.append(os.path.basename(td))
        return recovered

    def rollback(self, txn_dir=None):
        if txn_dir is not None:
            td = txn_dir if os.path.isabs(txn_dir) else os.path.join(self.txn_root, txn_dir)
            self._restore_from_txn(td)
            return {"rolled_back": [os.path.basename(td)]}
        return {"rolled_back": self._recover_incomplete()}

    # -- the sidecar (provenance + the cheap gate) -----------------------------------------------
    def _sidecar_path(self):
        return self._p(SIDECAR_REL)

    def _load_sidecar(self):
        p = self._sidecar_path()
        return _read_json(p) if os.path.exists(p) else None

    def _sidecar_current(self, sidecar):
        cur = self._load_sidecar()
        return bool(cur) and all(cur.get(k) == sidecar.get(k) for k in
                                 ("source_store_md5", "balanced_board_md5", "active", "present_value_total"))

    def _refresh_sidecar_if_stale(self, sidecar):
        cur = self._load_sidecar() or {}
        keys = ("source_store_md5", "balanced_board_md5", "active", "present_value_total",
                "as_of_round", "reference_vector", "contract_sha256")
        if any(cur.get(k) != sidecar.get(k) for k in keys):
            _atomic_write_bytes(self._sidecar_path(), _dumps_sidecar(sidecar))
            return True
        return False

    # -- the gate --------------------------------------------------------------------------------
    def is_current_fast(self):
        """CHEAP gate: the recorded sibling source-store equals the current store AND the live balanced pin
        equals the recorded one. False (stale) if the sidecar is missing/mismatched."""
        cur = self._load_sidecar()
        if not cur:
            return False
        store_now = _md5_file(self._p(STORE_REL))
        boot = _read_json(self._p(EXPECTED_BOOT_REL))
        return (cur.get("source_store_md5") == store_now
                and cur.get("balanced_board_md5") == boot.get("balanced_board_md5"))

    def assert_current(self, *, full=False):
        """Raise SiblingStaleError unless the siblings are current AND fully coherent AND no sibling
        transaction is incomplete. Establishes coherence beyond the sidecar source-store (blocking-issue-3):
          (0) NO incomplete .sibling_txn (the next advance must not begin on an incomplete transaction);
          (1) the sidecar's source-store == the current store AND its balanced pin == expected_boot;
          (2) verify() — expected_boot / release_contract identities + present_lens / the reference vector /
              the FV oracle / the sidecar all agree, the contract self-seal is valid, and release_contract
              check passes (so a corrupted or partially-completed sibling set CANNOT pass the gate).
        `full` additionally REBUILDS the sibling and compares (authoritative build-and-compare)."""
        inc = self._incomplete_txns()
        if inc:
            raise SiblingStaleError("incomplete sibling transaction(s) present — recover/rollback before "
                                    "any advance: %s" % [os.path.basename(t) for t in inc])
        if not self.is_current_fast():
            cur = self._load_sidecar()
            raise SiblingStaleError("sibling provenance sidecar is missing or stale vs the current store — "
                                    "the last advance did not repin the siblings; run "
                                    "`sibling_repin.py reconcile` (sidecar=%s)"
                                    % ("present" if cur else "MISSING"))
        v = self.verify()
        if not v["ok"]:
            raise SiblingStaleError("sibling set is INCOHERENT (%s) — run `sibling_repin.py reconcile`"
                                    % v["fails"])
        if full:
            sib = build_sibling(self.repo_root)
            bal = _read_json(self._p(EXPECTED_BOOT_REL)).get("balanced_board_md5")
            if sib["board_md5"] != bal:
                raise SiblingStaleError("balanced sibling rebuilds to %s but the live pin is %s — a store "
                                        "advance left the siblings stale; run `sibling_repin.py reconcile`"
                                        % (sib["board_md5"][:8], str(bal)[:8]))
            return {"current": True, "mode": "full+coherence", "balanced_board_md5": sib["board_md5"]}
        return {"current": True, "mode": "coherence"}

    def verify(self):
        """Assert the LIVE siblings are internally coherent (no build) across the FULL sibling set
        (blocking correction 2). Fails on:
          - contract identities / present_lens balanced pin drift or a self-seal mismatch;
          - reference vector: board-id drift, active != len(vector), sum_v != sum(vector.values()), OR
            active/sum disagreement with the sealed present-lens (catches a value changed under a correct id);
          - FV oracle: board-id, active, sum, Sheezel OR regenerated-reference-filename drift;
          - EITHER board-view bundle stale/corrupt (working stamps, public parity, public leak-freedom);
          - sidecar: store / balanced / active / total / Sheezel / reference-filename / contract-seal drift;
          - release_contract check failing."""
        boot = _read_json(self._p(EXPECTED_BOOT_REL))
        contract = _read_json(self._p(RELEASE_CONTRACT_REL))
        bal = boot.get("balanced_board_md5")
        fails = []
        ids = contract.get("identities", {})
        plb = contract.get("present_lens_baseline", {})
        if ids.get("balanced_board_md5") != bal:
            fails.append("contract identities.balanced_board_md5 != expected_boot")
        if plb.get("balanced_board_md5") != bal:
            fails.append("contract present_lens_baseline.balanced_board_md5 != expected_boot")
        rc_tool = _load_module("sr_rc_verify", self._p(RELEASE_CONTRACT_TOOL_REL))
        if contract.get("contract_sha256") != rc_tool.contract_hash(contract):
            fails.append("contract self-seal mismatch")
        plb_active, plb_total = plb.get("active"), plb.get("present_value_total")

        # reference vector — board id + internal arithmetic + agreement with the sealed present-lens.
        ref_name = _reference_vector_name(str(bal))
        ref = self._p(os.path.join(FV_FIX_REL, ref_name))
        ref_sheezel = None
        if not os.path.exists(ref):
            fails.append("reference vector for %s missing" % str(bal)[:8])
        else:
            try:
                rv = _read_json(ref)
            except (OSError, ValueError) as e:
                rv = None
                fails.append("reference vector unparseable: %s" % e)
            if rv is not None:
                vec = rv.get("vector") or {}
                ref_sheezel = vec.get("harry-sheezel")
                if rv.get("board_md5") != bal:
                    fails.append("reference vector board_md5 != balanced pin")
                if rv.get("active") != len(vec):
                    fails.append("reference vector active %s != len(vector) %d" % (rv.get("active"), len(vec)))
                if rv.get("sum_v") != sum(int(x) for x in vec.values()):
                    fails.append("reference vector sum_v != sum(vector.values())")
                if rv.get("active") != plb_active:
                    fails.append("reference vector active != contract present_lens active")
                if rv.get("sum_v") != plb_total:
                    fails.append("reference vector sum_v != contract present_lens total")

        # FV oracle — board id + active + sum + Sheezel + regenerated reference filename.
        fv_src = open(self._p(FV_TEST_REL), encoding="utf-8").read()
        try:
            fo = _fv_oracle_aggregates(fv_src)
            if fo["board_md5"] != bal:
                fails.append("FV oracle BOARD_MD5_GOOD != balanced pin")
            if fo["active"] != plb_active:
                fails.append("FV oracle active != contract present_lens active")
            if fo["sum_v"] != plb_total:
                fails.append("FV oracle sum_v != contract present_lens total")
            if ref_sheezel is not None and fo["sheezel"] != ref_sheezel:
                fails.append("FV oracle sheezel != reference vector Sheezel")
            if not fo["reference_vector_present"] or fo["reference_vector"] != ref_name:
                fails.append("FV oracle reference-vector filename != regenerated reference vector")
        except SiblingRepinError as e:
            fails.append("FV oracle unreadable: %s" % e)

        # both board-view bundles — working stamps + public parity + public leak-freedom.
        try:
            live_board = _read_json(self._p(BOARD_OF_RECORD_REL))
            canon_active = live_board.get("active") if isinstance(live_board, dict) else live_board
        except (OSError, ValueError):
            canon_active = None
        fails.extend(_board_view_coherence(
            self.repo_root, balanced_md5=bal, canonical_board=boot.get("board"), store=boot.get("store"),
            as_of_round=boot.get("as_of_round"), release_version=boot.get("release_version"),
            canonical_active=canon_active))

        # sidecar — full aggregate + contract seal.
        sc = self._load_sidecar()
        if not sc:
            fails.append("provenance sidecar missing")
        else:
            if sc.get("source_store_md5") != _md5_file(self._p(STORE_REL)):
                fails.append("sidecar source_store_md5 != current store")
            if sc.get("balanced_board_md5") != bal:
                fails.append("sidecar balanced_board_md5 != expected_boot")
            if sc.get("active") != plb_active:
                fails.append("sidecar active != contract present_lens active")
            if sc.get("present_value_total") != plb_total:
                fails.append("sidecar present_value_total != contract present_lens total")
            if ref_sheezel is not None and sc.get("harry_sheezel") != ref_sheezel:
                fails.append("sidecar harry_sheezel != reference vector Sheezel")
            if sc.get("reference_vector") != ref_name:
                fails.append("sidecar reference_vector filename != regenerated reference vector")
            if sc.get("contract_sha256") != contract.get("contract_sha256"):
                fails.append("sidecar contract_sha256 != live contract seal")

        env = dict(os.environ)
        env["RL_CONFIG_MODE"] = "gate"
        p = subprocess.run([sys.executable, self._p(RELEASE_CONTRACT_TOOL_REL), "check"],
                           capture_output=True, text=True, env=env, cwd=self.repo_root)
        if p.returncode != 0:
            fails.append("release_contract check failed")
        return {"ok": not fails, "fails": fails, "balanced_board_md5": bal}


# --------------------------------------------------------------------------- CLI
def _cli(argv=None):
    ap = argparse.ArgumentParser(description="ITEM 408 item 5 — balanced/strict sibling advance-repin.")
    ap.add_argument("verb", choices=["plan", "reconcile", "repin", "check", "verify", "rollback"])
    ap.add_argument("--repo", default=None)
    ap.add_argument("--round", type=int, default=None)
    ap.add_argument("--commit", default=None, help="record this git commit in the provenance sidecar")
    ap.add_argument("--full", action="store_true", help="check: authoritative build-and-compare gate")
    ap.add_argument("--txn", default=None, help="rollback: a specific txn dir")
    args = ap.parse_args(argv)
    sr = SiblingRepin(args.repo)

    if args.verb == "plan":
        sib = build_sibling(sr.repo_root)
        plan = RepinPlan(sr.repo_root, sib, round_n=args.round)
        print(json.dumps({"balanced_board_md5": plan.new_md5, "active": sib["active"],
                          "sum_v": sib["sum_v"], "sheezel": sib["sheezel"],
                          "live_balanced_board_md5": plan.live_balanced, "changed": plan.changed,
                          "changed_map": plan.changed_map}, indent=2, sort_keys=True))
        return 0

    if args.verb in ("reconcile", "repin"):
        print(json.dumps(sr.reconcile(round_n=args.round, generated_at_commit=args.commit),
                         indent=2, sort_keys=True))
        return 0

    if args.verb == "check":
        try:
            res = sr.assert_current(full=args.full)
            print("SIBLING CHECK: CURRENT  (%s)" % json.dumps(res))
            return 0
        except SiblingStaleError as e:
            print("SIBLING CHECK: STALE — %s" % e)
            return 2

    if args.verb == "verify":
        res = sr.verify()
        print(json.dumps(res, indent=2, sort_keys=True))
        return 0 if res["ok"] else 1

    if args.verb == "rollback":
        print(json.dumps(sr.rollback(args.txn), indent=2, sort_keys=True))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
