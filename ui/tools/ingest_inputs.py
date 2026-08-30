#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI v1.2 — THE INPUTS INGEST (items 178(2)/(3)/(4), 180, 181(2)).  Directive:
docs/DIRECTIVE_UI_v1_2_club_valuation_2026-07-16.md.

The no-LLM pipeline's deterministic half: read the owner's authored input files under docs/inputs/
STRICTLY READ-ONLY, VALIDATE-OR-HALT (halt, never guess/warn-and-continue), price every held draft
pick off the SHIPPED engine's canonical pick curve, aggregate a per-club valuation, and emit the
committed view bundle ui/data/club_valuation.js (window.__CLUB_VALUATION__ = {...}).

FENCE: ui/-only + read-only reads of docs/inputs/ and the shipped board bundle + the engine curve
file (for the stamp cross-check only).  NO value is recomputed here — a pick's price is a MEAN of the
engine's own curve; a player's value is the stamped board `v`, only summed/greedily selected.  Values
from the pick workbook (Raw Value / Value (counted) / Pick Values tab) are NEVER ingested.

Run:  python3 ui/tools/ingest_inputs.py         (exit 0 = clean bundle written; exit 2 = HALT)

THE MIRROR LANE (added 2026-08-21, closing the missing-writer class on ui/data/ownership.js)
--------------------------------------------------------------------------------------------
  python3 ui/tools/ingest_inputs.py --mirror-only   writes ONLY ui/data/ownership.js
  python3 ui/tools/ingest_inputs.py --check         writes NOTHING; regenerates the mirror into a
                                                    scratch dir and byte-compares it with the
                                                    shipped one (exit 1 on drift)

THE CLUBS LANE (added 2026-08-21, closing the SAME class on ui/data/club_valuation.js — v827)
--------------------------------------------------------------------------------------------
  python3 ui/tools/ingest_inputs.py --clubs-only    writes ONLY ui/data/club_valuation.js
  python3 ui/tools/ingest_inputs.py --clubs-check   writes NOTHING; regenerates the picks bundle
                                                    into a scratch dir and byte-compares it with
                                                    the shipped one (exit 1 on drift)

WHY THE CLUBS LANE EXISTS, AND WHY IT IS A FENCE AND NOT A SHORTCUT.  ui/data/club_valuation.js is
the PICK-LOCATIONS bundle, and on 2026-08-21 it was found SILENTLY STALE: generated 2026-08-20 from
board a05fe951 / R22 while the tree stood on b3e8da99 / R23, with NO identity guard in the reader and
no writer inside the landing.  Owner's word the same night: "It is essential that the UI displays the
correct player locations and pick locations."  `MD.clubTotals.pin()` now refuses a bundle whose
board+store stamp is not the loaded app's (the #232 mirror law, applied one carrier along), and the
lander runs THIS tool as its SIXTH UI writer (`tools/landing/steps.ui`).  That lane must write the
picks bundle WITHOUT the step-0 store apply, for the same reason `--mirror-only` must: step 0 is an
identity-moving write with its own writer of record, and a landing is not it.  The stamp's wall clock
was dropped in the same act, which is what makes the bundle byte-provable and therefore a carrier.

WHY THE LANE EXISTS.  ui/data/ownership.js is a MIRROR of the store's `affl_team`, pinned to the
board + store identity it was generated from, and `MD.ownership.pin()` REFUSES a mirror whose pin
does not match the loaded app.  So every landing that moves the board or the store retires the
shipped mirror — and until now no landing regenerated it.  On 2026-08-21 the tree stood on board
b3e8da99 / store b745002e (R23) while the shipped mirror still carried a05fe951 / cc02567f (R22):
the live ownership lane had been switched off since the R23 advance, and three suites said so.  The
lever/round lander now runs THIS tool as its fifth UI writer (`tools/landing/steps.ui`), which is
why the lane has to be able to write the mirror WITHOUT the club-valuation bundle: that bundle
carries a wall-clock `generated` stamp, is not a landing carrier, and cannot be byte-proved.

WHY `--mirror-only` DOES NOT RUN THE STORE APPLY.  Step 0 couriers the owner's CSV INTO the store.
That is an identity-moving write with its own writer of record (ui/tools/ownership_store_apply.py)
and a landing is not it.  In this lane the store is READ, never written: if the CSV carries
authorship the store has not been given, the single-source check below HALTs and names it, which is
the correct verdict for a landing rather than a silent mid-flight store move.
"""
# `datetime` is deliberately NOT imported: neither bundle carries a wall clock any more, and an
# import kept "for later" is how one comes back.
import csv, json, os, sys, collections, hashlib, zipfile, shutil, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xlsx_read          # stdlib-only .xlsx reader (#232) — see its module docstring for why

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
# Production paths are the defaults; each may be redirected via an env var so a FIXTURE run (a temp board
# bundle / temp contract / temp engine-curve dir / temp boot manifest / temp out) exercises the SAME
# fail-closed resolver and asserts without touching production data. Overrides change WHERE we read/write,
# never WHAT we assert — every ring-fence + curve-provenance HALT below stays live regardless of the paths.
INPUTS = os.environ.get("RL_UI_INPUTS", os.path.join(ROOT, "docs", "inputs"))
UI_DATA = os.path.join(ROOT, "ui", "data")
BOARD_BUNDLE = os.environ.get("RL_UI_BOARD_BUNDLE", os.path.join(UI_DATA, "board_view_working.js"))
# Engine curve DIR (not a single hardcoded file): the release-active curve is resolved from the contract.
ENGINE_DIR = os.environ.get("RL_UI_ENGINE_DIR", os.path.join(ROOT, "engine", "rl_after"))
# The explicit, fail-closed release-metadata contract that declares the release-active pick curve.
CURVE_CONTRACT = os.environ.get("RL_UI_CURVE_CONTRACT", os.path.join(ROOT, "ui", "release_pick_curve.json"))
# The accepted release manifest — read STRICTLY READ-ONLY for the store + release_version cross-check.
BOOT = os.environ.get("RL_UI_BOOT", os.path.join(ROOT, "data", "expected_boot.json"))
OUT = os.environ.get("RL_UI_OUT", os.path.join(UI_DATA, "club_valuation.js"))
# #232 — the LIVE-lane ownership sidecar. Second output of the SAME command: one edit to the owner's
# sheet, one run, both bundles. Kept a separate file because club_valuation.js is the picks bundle and
# #222 deliberately narrowed the UI to read it for picks only; folding ownership back into it would undo
# that narrowing for no gain.
#
# The default FOLLOWS `OUT` rather than pointing at ui/data/ unconditionally. Every fixture harness here
# redirects RL_UI_OUT to a temp path to keep production untouched — club_curve_provenance.test.py says so
# in its own docstring — and it drives dozens of DELIBERATE halts. A second output anchored to ui/data/
# would have those halts overwrite the production sidecar with a halted, empty one; it did exactly that
# once before this line existed. Deriving the path means redirecting the bundle redirects the sidecar,
# and no existing harness has to learn about a file that did not exist when it was written.
OUT_OWNERSHIP = os.environ.get(
    "RL_UI_OUT_OWNERSHIP", os.path.join(os.path.dirname(os.path.abspath(OUT)), "ownership.js"))

#: `--mirror-only` / `--check` set this instead of exporting RL_OSA_SKIP. A landing runs this tool as
#: a child, and an RL_-prefixed variable in a landing's environment is inherited by every probe the
#: gate step spawns, where `config_manifest.enforce()` rejects it as a divergent model override. That
#: hazard is written down twice in this estate (tools/landing/carriers.py header; ONE incident cost a
#: whole acceptance run) — so this flag is a module attribute, not an environment variable.
SKIP_STORE_APPLY = False

EXPECTED_BOARD = None      # ui/app/config.js EXPECTED_BOARD — v2.11-final-rc board of record (Board B + visible future-draft ladder; balanced_board_md5 06d8af60 preserved as lineage)
# R104.5's flat 10% future discount is SUPERSEDED for pick valuation by the owner's year rule of
# 2026-08-28 (three draft years now issued): 2026 = 100% the pick's own projected band value ·
# 2027 = 50% own band value + 50% the round's average value · 2028 = 100% the round's average.
# The uncertainty discount now lives in the regression-to-round-mean, not a flat multiplier.
BASE_YEAR = 2026
PICK_YEARS = (BASE_YEAR, BASE_YEAR + 1, BASE_YEAR + 2)
SLOT_VALUE = 150                 # the owner's vacant-slot allowance (per vacant player or pick slot)
PLAYER_SLOTS = 41                # the required player list
PICK_SLOTS_PER_YEAR = 5          # the required picks per draft year

# Known release pick-curve pathways -> the engine curve FILENAME each pathway loads. The contract's
# adopted_pathway MUST be one of these; the resolver cross-checks the contract's declared path AND the
# curve file's OWN self-declared gate token against this registry. An unknown pathway HALTs.
KNOWN_PATHWAYS = {
    "RL_PVC2": "pvc_curve_v2.json",       # v2.9+ composed pathway (the v2.11 adopted curve)
    "RL_PVCADOPT": "pvc_curve_L1b.json",  # prior v2.9 L1b adopt curve (superseded by RL_PVC2)
}
# Best-23 positional structure (item 178(3)). Slot legality is drawn from the store's ELIGIBILITIES
# column, carried on the board bundle as `elig` (#274 item 2 / #271 Addendum 19) — NOT from `posCode`,
# which is the modelling axis and cannot see DPP.
SLOTS = [("KPD", 2), ("SD", 4), ("MID", 5), ("SF", 4), ("KPF", 2), ("RUCK", 1)]
BENCH = 5
TARGET = 23   # the 18 positional slots + BENCH(5)
FREE_AGENTS = "Free Agents"

verdicts = []   # [(check, ok, detail)]
notes = []


def check(name, ok, detail=""):
    verdicts.append((name, bool(ok), detail))
    return bool(ok)


class HaltError(Exception):
    """Raised by halt(); caught in main() -> renders the verdict table, writes a HALTED overlay bundle
    (so the UI refuses to render) and exits 2. Making halt() RAISE rather than sys.exit lets the
    curve-provenance resolver + guards be unit-tested for fail-closed behaviour (import + assert-raises)."""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


def halt(reason):
    """Fail closed. Nothing is ever guessed; the overlay refuses to render on an ambiguous ingest."""
    raise HaltError(reason)


def _emit_halt(reason):
    """Render the verdict table + the halt reason and write the HALTED bundle (overlay refuses). Called
    once, from main(), when any guard raises HaltError."""
    _print_verdicts()
    print("\n■ HALT — %s" % reason)
    print("  The club-valuation overlay refuses to render on this ingest.  Nothing is guessed.")
    payload = {
        # NO WALL CLOCK, on the halt path either — see the note on the clean stamp in run(). A halted
        # bundle that carried a timestamp could not be byte-compared, and the halt overlay is exactly
        # the bundle a drift guard most needs to be able to re-derive.
        "stamp": {"expectedBoard": _expected_board_short()},
        "halt": {"reason": reason, "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts]},
        "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts],
        "clubs": [], "picksByTeam": {}, "notes": notes,
    }
    _write(payload)
    # #232: the sidecar fails closed on the SAME halt. A half-written live lane is worse than none —
    # it would show a traded player's new club on the board while the picks overlay refused, which is
    # the "one player, two clubs" state this job exists to prevent.
    _write_ownership({
        "stamp": {"expectedBoard": _expected_board_short(),
                  "lane": "live — ownership only; positions are batched and are NOT in this file"},
        "halt": {"reason": reason},
        "byKey": {}, "stableIdByKey": {}, "overriding": [],
    })
    print("  The ownership sidecar refuses on the same halt (ui/data/ownership.js).")


# The master store — the ownership mirror's actual source, and therefore its provenance (#283).
STORE = os.environ.get("RL_UI_STORE", os.path.join(ROOT, "engine", "rl_after", "rl_model_data.json"))


def _store_md5_full():
    """Full md5 of the store the mirror was generated FROM. Deterministic by construction, which is
    what lets the mirror be regenerated and byte-compared (#283 acceptance 4)."""
    h = hashlib.md5()
    with open(STORE, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def readcsv(path):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return list(csv.reader(f)), enc
        except UnicodeDecodeError:
            continue
    halt("could not decode %s as utf-8/cp1252/latin-1" % os.path.basename(path))


def normt(t):
    """DISPLAY canonicalisation of a club string — casing only, and applied on the way OUT to the
    bundles ONLY.  The store deliberately carries the owner's exact bytes and holds BOTH 'Free agents'
    (x73) and 'Free Agents' (x2); the CSV carries the same split, aligned row-for-row.  Folding them on
    the way IN would rewrite 2 rows the owner never edited — seat authorship where the ruling requires
    owner authorship by courier — and inflate the change set from 18 to 20 (#283 finding F3, seam-
    binding 2026-07-30).  So: canonicalise for the mirror, NEVER for the store.  Mirrors
    ui/tools/extract_board_view.py norm_club(), which does the same job on the same values.
    Module-level because the ownership mirror is written outside validate_csvs()."""
    return FREE_AGENTS if str(t).strip().lower() == "free agents" else str(t).strip()


def nkey(s):
    """Normalised name join key: collapse whitespace + casefold.  Resolves the 5 case-only surname
       variants (MacDonald/Macdonald, DeMattia/Demattia, …) between the board and the owner's CSVs
       without guessing; still keeps the two Max Kings distinct ('max king' != 'maxwell king')."""
    return " ".join(str(s).strip().split()).casefold()


# ---------------------------------------------------------------------------- load the shipped board
def load_board():
    if not os.path.exists(BOARD_BUNDLE):
        halt("board bundle missing: %s" % BOARD_BUNDLE)
    s = open(BOARD_BUNDLE, encoding="utf-8").read()
    try:
        obj = json.loads(s[s.index("{"): s.rindex("}") + 1])
    except Exception as e:
        halt("board bundle is not parseable JSON: %s" % e)
    stamp = obj.get("stamp", {})
    board = str(stamp.get("board", ""))
    boot = _release_manifest()
    expected_board = str(boot["board"])
    board_ok = board == expected_board
    check("board id ring-fence == current release manifest", board_ok,
          "bundle board %s vs manifest %s" % (board[:8], expected_board[:8]))
    if not board_ok:
        halt("board id mismatch — bundle %s != current release board %s (regenerate board_view)"
             % (board[:8], expected_board[:8]))
    round_ok = stamp.get("asOfRound") == boot["as_of_round"]
    check("board asOfRound == current release manifest", round_ok,
          "bundle %s vs manifest %s" % (stamp.get("asOfRound"), boot["as_of_round"]))
    if not round_ok:
        halt("board round mismatch — bundle R%s != current release R%s"
             % (stamp.get("asOfRound"), boot["as_of_round"]))
    bundle_store = str(stamp.get("store_md5") or stamp.get("store") or "")
    store_ok = bundle_store == str(boot["store"])
    check("board source store == current release manifest", store_ok,
          "bundle %s vs manifest %s" % (bundle_store[:8], str(boot["store"])[:8]))
    if not store_ok:
        halt("board store mismatch — bundle %s != current release store %s"
             % (bundle_store[:8], str(boot["store"])[:8]))
    pvc = {int(k): v for k, v in obj.get("pvc", {}).items()}
    return obj, stamp, pvc


def _md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_json(path, what):
    if not os.path.exists(path):
        halt("%s missing: %s (HALT-AND-ASK on provenance)" % (what, path))
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        halt("%s is not parseable JSON: %s (%s)" % (what, path, e))



def _release_manifest():
    """Dynamic weekly authority: board, store and round move together after every apply."""
    boot = _read_json(BOOT, "release manifest (expected_boot)")
    missing = [k for k in ("board", "store", "as_of_round", "release_version")
               if boot.get(k) in (None, "")]
    check("release manifest has current board/store/round/version", not missing,
          "missing: %s" % (missing or "none"))
    if missing:
        halt("release manifest lacks current weekly identity fields: %s" % missing)
    return boot


def _expected_board_short():
    try:
        return str(json.load(open(BOOT, encoding="utf-8")).get("board", ""))[:8]
    except Exception:
        return "unknown"


def _gate_token(curve_doc):
    """The first whitespace token of a curve file's self-declared 'gate' string is its pathway id
    (e.g. 'RL_PVC2 (parallel of RL_PVCADOPT) ...' -> 'RL_PVC2'). Absent gate -> None (fails closed later)."""
    g = str(curve_doc.get("gate", "")).strip()
    return g.split()[0] if g else None


# --------------------------------------------- release-active pick curve: deterministic + fail-closed (S5)
def load_curve_contract():
    """Read the EXPLICIT release-metadata contract (ui/release_pick_curve.json) and cross-check it against
    the ACCEPTED release manifest (data/expected_boot.json, read-only): store + release_version must agree,
    pin1 must be 3000, adopted_pathway must be KNOWN. Missing / unknown / conflicting -> HALT. This is the
    single deterministic source of the release-active pathway: the config manifest pins RL_PVCADOPT but does
    NOT carry the RL_PVC2 default-ON kill-switch, so the pathway cannot be read from the config alone."""
    c = _read_json(CURVE_CONTRACT, "release pick-curve contract")
    need = ("release_version", "adopted_pathway", "pick_curve_path",
            "pick_curve_file_md5", "pick_curve_curve_md5", "curve_source_store_md5", "numeraire_pin1")
    miss = [k for k in need if k not in c]
    check("release pick-curve contract has all required fields", not miss, "missing: %s" % (miss or "none"))
    if miss:
        halt("release pick-curve contract is incomplete (missing %s) — cannot resolve the release-active "
             "curve (HALT-AND-ASK)" % miss)
    pathway = c["adopted_pathway"]
    check("contract adopted_pathway is a known pathway", pathway in KNOWN_PATHWAYS,
          "%s (known: %s)" % (pathway, sorted(KNOWN_PATHWAYS)))
    if pathway not in KNOWN_PATHWAYS:
        halt("UNKNOWN curve-selection: adopted_pathway '%s' is not a known pathway %s — refusing to guess "
             "(HALT-AND-ASK)" % (pathway, sorted(KNOWN_PATHWAYS)))
    boot = _release_manifest()
    rv_ok = str(c["release_version"]) == str(boot.get("release_version"))
    check("curve contract release_version == current release version", rv_ok,
          "contract %s vs manifest %s" % (c["release_version"], boot.get("release_version")))
    if not rv_ok:
        halt("CONFLICTING curve-selection: contract release_version %s != release %s (HALT-AND-ASK)"
             % (c["release_version"], boot.get("release_version")))
    source_store = str(c["curve_source_store_md5"])
    source_ok = len(source_store) == 32 and all(ch in "0123456789abcdef" for ch in source_store.lower())
    check("curve contract carries a full immutable source-store identity", source_ok,
          "curve source store %s" % source_store[:8])
    if not source_ok:
        halt("curve_source_store_md5 is not a full md5 identity (HALT-AND-ASK)")
    pin_ok = int(c["numeraire_pin1"]) == 3000
    check("contract numeraire pin1 == 3000", pin_ok, "pin1 = %s" % c["numeraire_pin1"])
    if not pin_ok:
        halt("contract numeraire pin1 != 3000 — numeraire drift; refusing to resolve a drifted ruler")
    return c


def resolve_release_curve(contract):
    """Resolve the release-active engine pick curve DETERMINISTICALLY from the contract, cross-checking the
    curve file's OWN self-declared identity: the filename the pathway must load, full-file md5, curve_md5,
    gate token, and store binding. Any drift/conflict -> HALT. Returns {'curve': {pick:int}, 'gate','path',...}."""
    pathway = contract["adopted_pathway"]
    want_name = KNOWN_PATHWAYS[pathway]
    got_name = os.path.basename(str(contract["pick_curve_path"]))
    name_ok = got_name == want_name
    check("contract pick_curve_path matches the adopted pathway", name_ok,
          "%s expects %s, contract points at %s" % (pathway, want_name, got_name))
    if not name_ok:
        halt("CONFLICTING curve-selection: adopted_pathway %s must load %s but the contract points at %s "
             "(e.g. L1b supplied while RL_PVC2 is active) — HALT-AND-ASK" % (pathway, want_name, got_name))
    path = os.path.join(ENGINE_DIR, want_name)
    doc = _read_json(path, "release-active engine curve %s" % want_name)
    file_md5 = _md5_file(path)
    md5_ok = file_md5 == str(contract["pick_curve_file_md5"])
    check("release-active curve file md5 == contract", md5_ok,
          "file %s vs contract %s" % (file_md5[:8], str(contract["pick_curve_file_md5"])[:8]))
    if not md5_ok:
        halt("CURVE DRIFT: %s md5 %s != contract %s — the engine curve file changed under the contract "
             "(HALT-AND-ASK)" % (want_name, file_md5[:8], str(contract["pick_curve_file_md5"])[:8]))
    cmd5_ok = str(doc.get("curve_md5")) == str(contract["pick_curve_curve_md5"])
    check("release-active curve curve_md5 == contract", cmd5_ok,
          "curve %s vs contract %s" % (doc.get("curve_md5"), contract["pick_curve_curve_md5"]))
    if not cmd5_ok:
        halt("CURVE DRIFT: %s curve_md5 %s != contract %s (HALT-AND-ASK)"
             % (want_name, doc.get("curve_md5"), contract["pick_curve_curve_md5"]))
    gate = _gate_token(doc)
    gate_ok = gate == pathway
    check("engine curve self-declares gate == adopted pathway", gate_ok,
          "curve gate '%s' vs pathway '%s'" % (gate, pathway))
    if not gate_ok:
        halt("CONFLICTING curve-selection: %s self-declares gate '%s' != adopted pathway '%s' — refusing "
             "to price on a curve from the wrong pathway (HALT-AND-ASK)" % (want_name, gate, pathway))
    # If the curve self-declares a store binding it must equal the release store (v2 carries stamp.store_md5;
    # L1b does not — an ABSENT binding is permitted, a PRESENT-and-WRONG one HALTs).
    curve_store = str(((doc.get("stamp") or {}).get("store_md5")) or "")
    if curve_store:
        cs_ok = curve_store[:8] == str(contract["curve_source_store_md5"])[:8]
        check("engine curve store binding == release store", cs_ok,
              "curve %s vs release %s" % (curve_store[:8], str(contract["curve_source_store_md5"])[:8]))
        if not cs_ok:
            halt("CONFLICTING curve-selection: %s binds store %s != release store %s (HALT-AND-ASK)"
                 % (want_name, curve_store[:8], str(contract["curve_source_store_md5"])[:8]))
    if int(doc.get("pin", 0)) != 3000:
        halt("release-active curve %s pin != 3000 — numeraire drift (HALT-AND-ASK)" % want_name)
    eng = {int(k): int(v) for k, v in doc["curve"].items()}
    # ITEM 271 Addendum 23 fix 1: publish the ruled POOL index alongside the curve. The split-era
    # curve prices 1-64 only (RULEBOOK v2.1 law 4), and the pick workbook carries ranges past 64 —
    # price_pick used to KeyError on them (latent since the split, masked by the ring-fence halt).
    global _POOL_VALUE
    _POOL_VALUE = int(doc["pool_value"]) if doc.get("pool_value") is not None else None
    return {"curve": eng, "pool_value": _POOL_VALUE, "gate": pathway, "path": "engine/rl_after/" + want_name,
            "file_md5": file_md5, "curve_md5": str(doc.get("curve_md5")), "curve_source_store_md5": str(contract["curve_source_store_md5"])}


# ---------------------------------------- board PVC == release-active curve (S5 stamp-assert, corrected)
def assert_pvc(pvc, resolved):
    """Cross-check the INSTALLED board's PVC against the release-active curve resolved above: full shared-pick
    byte equality + pin1 + monotone. A board built on any OTHER pathway (e.g. an L1b / RL_PVC2=0 board while
    the contract adopts RL_PVC2) fails this equality and HALTs. Same S5 doctrine, on the CORRECT curve."""
    if not pvc:
        halt("no PVC in the board bundle — cannot locate the canonical pick curve (HALT-AND-ASK)")
    eng = resolved["curve"]
    shared = [k for k in pvc if k in eng]
    bytematch = bool(shared) and all(pvc[k] == eng[k] for k in shared)
    check("board PVC == release-active %s (%s, over %d shared picks)"
          % (resolved["path"], resolved["gate"], len(shared)), bytematch)
    if not bytematch:
        halt("STALE-CURVE GUARD: the board's PVC does not byte-match the release-active curve %s "
             "(%s, curve_md5 %s) — provenance ambiguous (the S5 failure). HALT-AND-ASK."
             % (resolved["path"], resolved["gate"], resolved["curve_md5"]))
    check("PVC numeraire anchor pick1 == 3000", pvc.get(1) == 3000, "pick1 = %s" % pvc.get(1))
    if pvc.get(1) != 3000:
        halt("PVC pick1 != 3000 — numeraire drift; refusing to price picks against a drifted ruler")
    # monotone non-increasing (the curve is a ruler) — OVER THE CURVE DOMAIN ONLY. RULEBOOK law 4
    # (v2.1 amendment) defines the national curve as picks 1-64 and rules that selections past 64 are
    # NOT on the curve and carry no ordering: the pool sits at ONE index (POOL_PICK=65) whose level is
    # a position-blind ladder value, lawfully ABOVE pick 64. Scoring key 65 as a curve step read the
    # pool index as a ruler point and failed a lawful board (seam ruling 2026-08-06).
    ks = sorted(k for k in pvc if int(k) <= 64)
    mono = all(pvc[ks[i]] >= pvc[ks[i + 1]] for i in range(len(ks) - 1))
    check("PVC monotone non-increasing (picks 1-64)", mono)
    if not mono:
        halt("PVC is not monotone non-increasing — not a valid pick ruler")
    return pvc


# ----------------------------------------------------------------------------------- price one pick
_POOL_VALUE = None   # the ruled pool index value, published by resolve() from the release-active curve
_YEAR_MULTIPLIERS = {}  # the owner's Ladder-sheet distance discounts, published when the workbook is read

def price_pick(pvc, lo, hi, year, pool_value=None, rnd=None, year_multipliers=None):
    # THE RULED SPLIT (RULEBOOK v2.1 law 4): the national curve prices picks 1-64; EVERYTHING past 64
    # is the pool at ONE index, valued at the curve artifact's committed pool_value. No new decision is
    # taken here — both halves are read from the release-active artifact.
    def _v(pk):
        if pk in pvc: return pvc[pk]
        _pv = pool_value if pool_value is not None else _POOL_VALUE
        if _pv is None:
            halt("pick %d is past the curve domain and the release-active curve publishes no "
                 "pool_value — cannot price it (HALT-AND-ASK)" % pk)
        return _pv

    def _mean(a, b):
        vals = [_v(p) for p in range(a, b + 1)]
        return sum(vals) / len(vals)

    # ROUND 5 IS WORTH ZERO IN THIS LANE (owner word 2026-08-28, his Carlton example): only
    # rounds 1-4 are eligible assets in the club rating, so an R5 pick prices 0 here and a club
    # short of five R1-4 picks in a year carries 150-phantoms instead. The engine's law-4 pool
    # pricing (trade/entry currency at the pool index) is a DIFFERENT lane and is untouched.
    if rnd is not None and int(rnd) == 5:
        return 0.0

    own = _mean(lo, hi)
    # THE OWNER'S YEAR RULE (2026-08-30, verbatim and complete — this supersedes BOTH earlier
    # readings, each of which had half of it):
    #
    #     "2026 picks - based on finishing positions, at full price
    #      2027 picks - 1/3 projected finish, 2/3 'average' round value, then x0.9
    #      2028 - 100% average round value, then x0.8"
    #
    # TWO THINGS ARE HAPPENING AT ONCE, and taking either for the whole rule is what went wrong
    # twice. (1) CERTAINTY ABOUT WHERE THE PICK LANDS decays with distance: 2026 positions are
    # nearly known, so a 2026 pick is its own projected band; 2027 is mostly unknown, so it is
    # one third its own projection and two thirds the round's average; 2028 is unknown outright,
    # so every pick in a round is that round's average and each 2028 first is worth the same as
    # every other 2028 first. (2) SEPARATELY, THE ASSET IS WORTH LESS FOR BEING FURTHER AWAY —
    # his 0.9 and 0.8, which multiply the result of (1). The 2026-08-28 rule had only the decay;
    # the 2026-08-30 first pass had only the discount. Both are his, and both apply.
    #
    # The two multipliers are READ FROM HIS SHEET (Ladder!B2 / Ladder!B3), never written here, so
    # moving a cell moves the rating. The 1/3-2/3 weight is the ruling above and is stated here.
    if year == BASE_YEAR:
        return own
    if rnd is None:
        halt("a %s pick needs its round to price the round average (HALT-AND-ASK)" % year)
    m = (year_multipliers or {}).get(int(year))
    if m is None:
        halt("no workbook multiplier for %s — the Ladder sheet must carry a \"%s value "
             "multiplier\" cell (HALT-AND-ASK)" % (year, year))
    r_lo, r_hi = (int(rnd) - 1) * 16 + 1, int(rnd) * 16
    r_avg = _mean(r_lo, r_hi)
    if year == BASE_YEAR + 1:
        return m * (own / 3.0 + 2.0 * r_avg / 3.0)
    if year == BASE_YEAR + 2:
        return m * r_avg
    halt("pick year %s is outside the issued windows %s (HALT-AND-ASK)" % (year, list(PICK_YEARS)))

# ----------------------------------------------------------------------------------------- the picks
def load_picks(pvc, affl_teams):
    # #232: read with the STDLIB reader, not openpyxl. The live lane is "edit the sheet, run one
    # command" — a lane that halts wherever a third-party wheel is absent is not an edit path, and it
    # halted exactly that way on a bare seat. ui/tools/xlsx_read.py reproduces the openpyxl typing and
    # refuses (rather than returning None) on an uncached formula or a cached error.
    path = os.path.join(INPUTS, "AFFL_Pick_Locations.xlsx")
    if not os.path.exists(path):
        halt("pick workbook missing: %s" % path)
    try:
        sheets = xlsx_read.sheet_names(path)
        ladder_rows = xlsx_read.rows(path, "Ladder") if "Ladder" in sheets else []
        picks_rows = xlsx_read.rows(path, "Picks") if "Picks" in sheets else None
    except xlsx_read.XlsxCellError as e:
        halt("UNREADABLE CELL in AFFL_Pick_Locations.xlsx — %s" % e)
    except xlsx_read.XlsxStructureError as e:
        halt("AFFL_Pick_Locations.xlsx is not shaped like a workbook — %s" % e)
    except zipfile.BadZipFile:
        halt("AFFL_Pick_Locations.xlsx is not a readable .xlsx (not a zip container)")

    # --- Ladder: THE YEAR MULTIPLIERS ARE INGESTED (owner word 2026-08-30: "I ruled 0.8x for a
    # reason, because the pick is so far in the future the asset is worth less. Like 2027 picks are
    # worth 0.9x. It is simple. I ruled it"). They are read from HIS sheet rather than written into
    # this file, so the rating follows the workbook: move Ladder!B2 or B3 and the next ingest moves
    # with it. Until 2026-08-30 these cells were read and REPORTED but deliberately not applied —
    # that was the defect, and it is the reason a 2028 wooden-spooner's first priced the same as a
    # premier's. A missing or out-of-range cell HALTS: pricing three draft years off a sheet whose
    # discount cells cannot be read is exactly the silent-default class this estate refuses.
    mults = {}
    for row in ladder_rows:
        if row and row[0] and "value multiplier" in str(row[0]):
            label = str(row[0]).split()[0]
            try:
                yr = int(label)
            except (TypeError, ValueError):
                halt("ladder multiplier row %r does not start with a year (HALT-AND-ASK)" % (row[0],))
            try:
                mults[yr] = float(row[1])
            except (TypeError, ValueError):
                halt("ladder %s multiplier is not a number: %r (HALT-AND-ASK)" % (yr, row[1]))
    need = [y for y in PICK_YEARS if y != BASE_YEAR]
    missing = [y for y in need if y not in mults]
    check("ladder carries a value multiplier for every discounted year %s" % need,
          not missing, "read %s" % ({k: mults[k] for k in sorted(mults)} or "none"))
    if missing:
        halt("the Ladder sheet has no value multiplier for %s — every issued year after %d must "
             "carry one (HALT-AND-ASK)" % (missing, BASE_YEAR))
    bad = {y: m for y, m in mults.items() if not (0.0 < m <= 1.0)}
    check("every ladder multiplier is a discount in (0, 1]", not bad, "offending = %s" % (bad or "none"))
    if bad:
        halt("ladder multiplier(s) outside (0, 1]: %s — a future pick may not be worth more than "
             "its own projected value (HALT-AND-ASK)" % bad)
    if BASE_YEAR in mults and mults[BASE_YEAR] != 1.0:
        halt("the sheet carries a %d multiplier of %s; the base year is undiscounted by the owner's "
             "own note on that sheet (HALT-AND-ASK)" % (BASE_YEAR, mults[BASE_YEAR]))
    global _YEAR_MULTIPLIERS
    _YEAR_MULTIPLIERS = dict(mults)

    # --- Picks ledger ---
    if picks_rows is None:
        halt("pick workbook has no 'Picks' sheet")
    picks = []
    for i, row in enumerate(picks_rows):
        if i < 2 or row[0] is None:   # rows 0-1 are title+header
            continue
        pid, yr, rnd, orig, owner, lo, hi = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        picks.append(dict(id=pid, year=int(yr), rnd=rnd, orig=str(orig).strip(),
                          owner=str(owner).strip(), lo=int(lo), hi=int(hi)))

    # 16 clubs x 5 rounds x 3 issued years (2026/2027/2028 — the third year issued 2026-08-28)
    expected_n = 16 * 5 * len(PICK_YEARS)
    check("pick ledger row count == %d" % expected_n, len(picks) == expected_n, "%d rows" % len(picks))
    if len(picks) != expected_n:
        halt("pick ledger carries %d rows, expected %d (16 clubs x 5 rounds x %d years)"
             % (len(picks), expected_n, len(PICK_YEARS)))

    # bands 1..80, low <= high
    band_ok = all(1 <= p["lo"] <= 80 and 1 <= p["hi"] <= 80 and p["lo"] <= p["hi"] for p in picks)
    bad = [p["id"] for p in picks if not (1 <= p["lo"] <= 80 and 1 <= p["hi"] <= 80 and p["lo"] <= p["hi"])]
    check("all bands within 1-80 and low <= high", band_ok, "offenders: %s" % (bad or "none"))
    if not band_ok:
        halt("band violation on pick ids %s (out of 1-80 or low>high)" % bad)

    # the three issued draft years, exactly (owner word 2026-08-28: THREE years of picks issued)
    yrs = sorted({p["year"] for p in picks})
    yr_ok = yrs == sorted(PICK_YEARS)
    check("the issued draft years are exactly %s" % (list(PICK_YEARS),), yr_ok, "years=%s" % yrs)
    if not yr_ok:
        halt("draft years %s != the issued windows %s" % (yrs, list(PICK_YEARS)))

    # every Owner + Origin joins to exactly one AFFL club (Free Agents permitted)
    club_set = set(affl_teams) | {FREE_AGENTS}

    def join_club(short):
        if short in club_set:
            return [short]
        cand = [t for t in affl_teams if t == short or t.startswith(short + " ")]
        return cand

    omap = {}
    for field in ("owner", "orig"):
        for p in picks:
            v = p[field]
            c = join_club(v)
            if len(c) != 1:
                check("%s '%s' joins to exactly one AFFL club" % (field, v), False,
                      "candidates: %s" % c)
                halt("%s '%s' does not join to a unique AFFL club (candidates %s)" % (field, v, c))
            omap[v] = c[0]
    check("every pick Owner + Origin joins to exactly one AFFL club (+Free Agents)", True,
          "%d distinct owners+origins" % len(omap))

    # price + attach the joined team
    for p in picks:
        p["team"] = omap[p["owner"]]
        p["origin_team"] = omap[p["orig"]]
        p["rnd"] = int(p["rnd"])
        if not (1 <= p["rnd"] <= 5):
            halt("pick id %s carries round %s (rounds are 1-5)" % (p["id"], p["rnd"]))
        p["value"] = round(price_pick(pvc, p["lo"], p["hi"], p["year"], rnd=p["rnd"],
                                      year_multipliers=mults))
        p["band"] = "#%d-%d" % (p["lo"], p["hi"]) if p["lo"] != p["hi"] else "#%d" % p["lo"]

    # THE OWNER'S OWN TWO CHECKS ON THE YEAR RULE (2026-08-30), asserted rather than asserted-about.
    # He stated the rule and then stated what it should produce: "the total value of all 2028 picks
    # should be 80% of the round average of all 2026 picks", and "each 2028 first is worth the same".
    # Both are properties of the whole priced set, not of one formula, so they catch a class the
    # per-pick re-derivation cannot: a discount applied to the wrong leg, a round average taken over
    # the wrong span, or a 2028 pick that kept any trace of its own projected position.
    #
    # WHY THE COMPARISON IS A RATIO AND CARRIES SLACK. Within a round the sixteen 2026 projections
    # tile the sixteen slots, so their sum IS sixteen round averages, which is what makes his check
    # exact in principle. In practice two things move it by a handful of points on ~47,000: each
    # pick is rounded to a whole number, and a club whose projection is a RANGE (low != high) prices
    # the mean of its band rather than one slot, so the tiling is near-exact rather than exact. The
    # bar is 1%, which is ~40x the observed slack and still far tighter than any real rule error.
    r14 = [p for p in picks if 1 <= p["rnd"] <= 4]
    base_total = sum(p["value"] for p in r14 if p["year"] == BASE_YEAR)
    for yr in sorted(y for y in PICK_YEARS if y != BASE_YEAR):
        yr_total = sum(p["value"] for p in r14 if p["year"] == yr)
        want = mults[yr]
        got = (yr_total / base_total) if base_total else 0.0
        ok = abs(got - want) <= 0.01
        check("R1-4 %d pick value is %.2f of %d's (the owner's conservation check)" % (yr, want, BASE_YEAR),
              ok, "%d / %d = %.4f vs %.2f" % (yr_total, base_total, got, want))
        if not ok:
            halt("the %d total is %.4f of the %d total, not the ruled %.2f — the year rule is not "
                 "producing what the owner's check says it must (HALT-AND-ASK)" % (yr, got, BASE_YEAR, want))

    # "each 2028 first is worth the same" — the LAST issued year is pure round average, so within a
    # round every pick in it must carry one identical value. This is the strongest statement of the
    # decay half of the rule and it is checked directly, per round, not inferred from the formula.
    last_year = max(PICK_YEARS)
    for rr in (1, 2, 3, 4):
        vals = sorted({p["value"] for p in r14 if p["year"] == last_year and p["rnd"] == rr})
        check("every %d round-%d pick carries one identical value (pure round average)" % (last_year, rr),
              len(vals) == 1, "distinct values = %s" % vals)
        if len(vals) != 1:
            halt("%d round %d prices %d distinct values %s — a %d pick must not carry any trace of "
                 "its own projected position (HALT-AND-ASK)" % (last_year, rr, len(vals), vals, last_year))

    # pick-count conservation (the Dashboard convention): ledger == Sum per-owner counts == 160
    per_owner = collections.Counter(p["team"] for p in picks)
    conserved = sum(per_owner.values()) == len(picks) == expected_n
    check("pick-count conservation (Sum per-club == ledger == %d)" % expected_n, conserved,
          "sum=%d ledger=%d" % (sum(per_owner.values()), len(picks)))
    if not conserved:
        halt("pick-count conservation failed")
    check("all %d picks priced off the canonical curve (owner year rule: own projected band, x0.9 for 2027 and x0.8 for 2028, read from the Ladder sheet — 2026-08-30)" % expected_n,
          all("value" in p for p in picks), "priced=%d" % sum(1 for p in picks if "value" in p))
    return picks


# ---------------------------------------------------------------- the CSV validations (name -> id)
def validate_csvs(board_by_nkey, affl_teams):
    loc, lenc = readcsv(os.path.join(INPUTS, "AFFL_Player_Locations.csv"))
    pos, penc = readcsv(os.path.join(INPUTS, "AFFL_Future_Positioning.csv"))
    loc_rows = [r for r in loc[1:] if r and r[0]]
    pos_rows = [r for r in pos[1:] if r and r[0]]

    # normalised-key uniqueness within each source (zero ambiguity)
    loc_by = collections.defaultdict(list)
    for r in loc_rows:
        loc_by[nkey(r[0])].append(r)
    pos_by = collections.defaultdict(list)
    for r in pos_rows:
        pos_by[nkey(r[1])].append(r)   # positioning col1 = player_name, col0 = stable_player_id
    loc_dups = [k for k, v in loc_by.items() if len(v) > 1]
    pos_dups = [k for k, v in pos_by.items() if len(v) > 1]
    check("player names unambiguous in Player_Locations.csv (normalised)", not loc_dups,
          "dups: %s" % (loc_dups or "none"))
    check("player names unambiguous in Future_Positioning.csv (normalised)", not pos_dups,
          "dups: %s" % (pos_dups or "none"))
    if loc_dups or pos_dups:
        halt("ambiguous player name(s) in the input CSVs: %s" % (loc_dups + pos_dups))

    # every location name joins to exactly one stable id via positioning, and to exactly one board row
    unmatched_pos = [r[0] for r in loc_rows if nkey(r[0]) not in pos_by]
    unmatched_board = [r[0] for r in loc_rows if nkey(r[0]) not in board_by_nkey]
    check("every Player_Locations name -> a unique stable_player_id (positioning join)",
          not unmatched_pos, "unmatched: %s" % (unmatched_pos or "none"))
    check("every Player_Locations name -> a unique board player (name join)",
          not unmatched_board, "unmatched: %s" % (unmatched_board or "none"))
    if unmatched_pos or unmatched_board:
        halt("player name(s) fail the id/board join: %s" % (unmatched_pos + unmatched_board))

    # the two Max Kings asserted distinct by name
    mk, mxk = nkey("Max King"), nkey("Maxwell King")
    distinct = (mk != mxk and mk in pos_by and mxk in pos_by
                and pos_by[mk][0][0] != pos_by[mxk][0][0])
    check("the two Max Kings are distinct by name (assert)", distinct,
          "Max King=%s · Maxwell King=%s" % (
              pos_by.get(mk, [["?"]])[0][0], pos_by.get(mxk, [["?"]])[0][0]))
    if not distinct:
        halt("the two Max Kings failed the distinctness assertion")

    # 5 case-only surname variants: reconciled by the normalised key, recorded (not a halt)
    exact_board_names = {rows[0]["name"].strip() for rows in board_by_nkey.values()}
    variants = sorted({r[0] for r in loc_rows
                       if r[0].strip() not in exact_board_names and nkey(r[0]) in board_by_nkey})
    if variants:
        notes.append("case-only name variants reconciled by the normalised join key (not halted): "
                     + ", ".join(variants))
        check("case-only name variants reconciled by normalised key", True,
              "%d reconciled: %s" % (len(variants), ", ".join(variants)))

    # authored-ownership vs the stamped board (agreement report; board is the display membership source)
    mismatch = []
    for r in loc_rows:
        bp = board_by_nkey.get(nkey(r[0]))
        if bp:
            ct, bt = normt(r[1]), bp[0]["affl_team"]
            if ct != bt:
                mismatch.append((r[0], ct, bt))
    check("authored CSV ownership agrees with the stamped board affl_team", not mismatch,
          "%d mismatch(es)%s" % (len(mismatch), ("" if not mismatch else ": " + str(mismatch[:5]))))
    if mismatch:
        # #232: this is no longer "the board rides one bake behind". The sidecar below carries the
        # authored ownership straight to the browser, so these ARE the live overrides — the board is
        # simply the fallback for anything the sheet does not name. Recorded, never halted.
        notes.append("sidecar overrides the stamped board for %d player(s) — this is the live lane "
                     "working, not a defect. First few: %s" % (len(mismatch), mismatch[:5]))

    # ---- the ownership sidecar's rows (#232) ----------------------------------------------------
    # Every club the sheet names must be one the board already spells, or MD.canonClub would pass the
    # unknown spelling through verbatim and silently split one club into two. Halt rather than ship that.
    club_set = set(affl_teams) | {FREE_AGENTS}
    unknown = sorted({normt(r[1]) for r in loc_rows if normt(r[1]) not in club_set})
    check("every AFFL Team in Player_Locations.csv is a known club spelling", not unknown,
          "unknown: %s" % (unknown or "none"))
    if unknown:
        halt("AFFL Team value(s) %s are not one of the %d board club spellings (+%s) — fix the "
             "spelling; an unknown club would split silently in the UI" % (unknown, len(affl_teams), FREE_AGENTS))

    own = {}
    for r in loc_rows:
        bp = board_by_nkey.get(nkey(r[0]))
        if not bp:
            continue                      # already halted above if unmatched; defensive
        pos_rows = pos_by.get(nkey(r[0])) or []
        own[bp[0]["key"]] = {
            "club": normt(r[1]),
            "name": bp[0]["name"],
            "stableId": pos_rows[0][0] if pos_rows else None,
        }
    check("ownership sidecar rows built from the authored sheet", True,
          "%d player(s) authored" % len(own))

    loc_enc_note(lenc, penc)
    return own


def loc_enc_note(lenc, penc):
    notes.append("input encodings: Player_Locations=%s · Future_Positioning=%s" % (lenc, penc))
    return True


# -------------------------------------------------------------------------- per-club valuation
def best23_of(roster):
    """The value-maximal legal 23 (#271 Addendum 19). See the full note at MD.clubTotals.best23Of in
    ui/app/club_totals.js — this is the SAME algorithm, transliterated line-for-line so the selection
    itself (not merely its total) is reproducible across the two languages. Same node numbering, same
    edge insertion order, same Bellman-Ford relaxation order, same strict-improvement rule.

    Slots come from the store's ELIGIBILITIES column, DPP players are assignable to either eligible
    slot, and the selection is an exact min-cost max-flow rather than a greedy: a greedy can spend a
    dual-eligible player on a slot a single-eligible player could have filled and strand the slot only
    that player covered. Returns (total, keys) with keys in roster order (descending v).
    """
    n = len(roster)
    SRC = 0                                  # 1..len(SLOTS) are the slot nodes
    BENCH_NODE = 1 + len(SLOTS)
    P0 = BENCH_NODE + 1                      # P0 + j is player j
    SINK = P0 + n
    N = SINK + 1

    e_from, e_to, e_cap, e_cost = [], [], [], []

    def add_edge(u, v, c, w):
        e_from.append(u); e_to.append(v); e_cap.append(c); e_cost.append(w)      # forward
        e_from.append(v); e_to.append(u); e_cap.append(0); e_cost.append(-w)     # residual

    for i, slot in enumerate(SLOTS):
        add_edge(SRC, 1 + i, slot[1], 0)
    add_edge(SRC, BENCH_NODE, BENCH, 0)
    for j in range(n):
        el = roster[j].get("elig") or []
        for i, slot in enumerate(SLOTS):
            if slot[0] in el:
                add_edge(1 + i, P0 + j, 1, 0)
    for j in range(n):
        add_edge(BENCH_NODE, P0 + j, 1, 0)
    sink_edge = []
    for j in range(n):
        sink_edge.append(len(e_cap)); add_edge(P0 + j, SINK, 1, -(roster[j].get("v") or 0))

    E = len(e_cap)
    INF = float("inf")
    flow = 0
    while flow < TARGET:
        # Bellman-Ford over the residual graph, edges relaxed in INSERTION order and only on strict
        # improvement, so the augmenting path is deterministic.
        dist = [INF] * N
        prev = [-1] * N
        dist[SRC] = 0
        for _ in range(N):
            changed = False
            for e in range(E):
                if e_cap[e] <= 0:
                    continue
                u = e_from[e]
                if dist[u] == INF:
                    continue
                nd = dist[u] + e_cost[e]
                if nd < dist[e_to[e]]:
                    dist[e_to[e]] = nd; prev[e_to[e]] = e; changed = True
            if not changed:
                break
        if dist[SINK] == INF:
            break                            # eligibility cannot fill another place — stop honestly
        # every player->sink edge has capacity 1, so the bottleneck is always exactly one unit
        v = SINK
        while v != SRC:
            e = prev[v]
            e_cap[e] -= 1
            e_cap[e ^ 1] += 1                # forward/residual are inserted as pairs
            v = e_from[e]
        flow += 1

    total = 0
    keys = []
    for j in range(n):
        if e_cap[sink_edge[j]] == 0:
            total += (roster[j].get("v") or 0); keys.append(roster[j]["key"])
    return total, keys


def rating56(roster, team_picks):
    """THE OWNER'S CLUB RATING (his formula, 2026-08-28): the sum of 56 selected assets.

    Best 41 player slots + best 5 picks per issued year (3 years) = 56. Every VACANT required
    slot counts SLOT_VALUE (150). Then every surplus R1-4 pick, best first, REPLACES the lowest
    counted player slot while it is worth more (his words: "those picks only earn additional
    credit when they are actually better than one of the players occupying its 41-player
    allowance"). A vacant player slot is the degenerate lowest counted slot (value 150), so a
    surplus pick worth more than 150 fills a vacancy before it displaces a real player.

    Deterministic: every sort is (-value, key/id) so the three transliterations (this, the
    browser's club_totals.js, the parity oracle) tie-break identically.

    Returns (rating, facts) where facts carries the phantom/excluded accounting the owner asked
    to see: phantomAdded (150s counted), materialExcludedPlayers / materialExcludedPicks (real
    asset value the allowance rules cut).
    """
    roster = sorted(roster, key=lambda x: (-x["v"], x.get("key") or ""))
    counted_players = [{"kind": "player", "key": p.get("key"), "v": p["v"]}
                      for p in roster[:PLAYER_SLOTS]]
    excluded_players = roster[PLAYER_SLOTS:]
    vacant_player = max(0, PLAYER_SLOTS - len(roster))
    player_slots = counted_players + [{"kind": "phantom", "key": None, "v": SLOT_VALUE}
                                      for _ in range(vacant_player)]

    counted_picks, surplus, vacant_pick = [], [], 0
    for yr in PICK_YEARS:
        # ELIGIBLE = ROUNDS 1-4 ONLY (owner word 2026-08-28): an R5 pick is worth 0 and never
        # occupies a counted slot — 3 eligible picks in a year means 2 phantom slots, not 2 R5s.
        ps = sorted([p for p in team_picks if p["year"] == yr and 1 <= int(p["rnd"]) <= 4],
                    key=lambda x: (-x["value"], str(x["id"])))
        counted_picks += ps[:PICK_SLOTS_PER_YEAR]
        vacant_pick += max(0, PICK_SLOTS_PER_YEAR - len(ps))
        surplus += ps[PICK_SLOTS_PER_YEAR:]

    # surplus R1-4 replacement, best surplus pick first, greedy until no improvement
    rescued, displaced = [], []
    surplus_r14 = sorted([p for p in surplus if 1 <= int(p["rnd"]) <= 4],
                         key=lambda x: (-x["value"], str(x["id"])))
    for pk in surplus_r14:
        lo_i = min(range(len(player_slots)), key=lambda i: (player_slots[i]["v"],
                                                            player_slots[i]["key"] or ""))
        if pk["value"] > player_slots[lo_i]["v"]:
            displaced.append(player_slots[lo_i])
            player_slots[lo_i] = {"kind": "pick", "key": str(pk["id"]), "v": pk["value"]}
            rescued.append(pk)
        else:
            break

    rescued_ids = {str(p["id"]) for p in rescued}
    cut_picks = [p for p in surplus if str(p["id"]) not in rescued_ids]
    phantom = (SLOT_VALUE * sum(1 for s in player_slots if s["kind"] == "phantom")
               + SLOT_VALUE * vacant_pick)
    excl_players = (sum(p["v"] for p in excluded_players)
                    + sum(s["v"] for s in displaced if s["kind"] == "player"))
    excl_picks = sum(p["value"] for p in cut_picks)
    rating = (sum(s["v"] for s in player_slots) + sum(p["value"] for p in counted_picks)
              + SLOT_VALUE * vacant_pick)
    facts = {
        "phantomAdded": phantom,
        "materialExcludedPlayers": excl_players,
        "materialExcludedPicks": excl_picks,
        "countedPicksTotal": sum(p["value"] for p in counted_picks),
        "vacantPlayerSlots": sum(1 for s in player_slots if s["kind"] == "phantom"),
        "vacantPickSlots": vacant_pick,
        "rescuedPickIds": sorted(rescued_ids),
        "nExcludedPlayers": len(excluded_players) + sum(1 for s in displaced if s["kind"] == "player"),
        "nCutPicks": len(cut_picks),
    }
    return rating, facts


def build_clubs(players, picks, affl_teams):
    picks_by_team = collections.defaultdict(list)
    for p in picks:
        picks_by_team[p["team"]].append(p)

    roster_by = collections.defaultdict(list)
    for p in players:
        t = p.get("affl_team")
        if t and t != FREE_AGENTS:
            roster_by[t].append(p)

    clubs = []
    for team in affl_teams:
        roster = sorted(roster_by.get(team, []), key=lambda x: -x["v"])
        total_player = sum(p["v"] for p in roster)
        top5 = sum(p["v"] for p in roster[:5])
        top10 = sum(p["v"] for p in roster[:10])

        # Best-23: the ruled value-maximal legal 23 from the ELIGIBILITIES column (see best23_of).
        best23, best23_keys = best23_of(roster)

        tp = [t for t in picks_by_team[team]]
        total_picks = sum(p["value"] for p in tp)
        # THE OWNER'S 56-ASSET RATING (2026-08-28) — `overall` IS this rating now; the raw sums
        # stay exported for display and for the note the owner asked for.
        overall, r56 = rating56(roster, tp)
        clubs.append({
            "team": team,
            "display": DISPLAY.get(team, team),
            "overall": overall,
            "rating56": r56,
            "totalPlayer": total_player,
            "totalPicks": total_picks,
            "top5": top5, "top10": top10,
            "best23": best23, "nonBest23": total_player - best23,
            "nRoster": len(roster), "nPicks": len(tp),
            "best23Keys": best23_keys,
        })
    clubs.sort(key=lambda c: -c["overall"])
    return clubs, picks_by_team


# ---------------------------------------------------------------------------------------- output
def _write(payload):
    body = ("// GENERATED by ui/tools/ingest_inputs.py — the no-LLM VALIDATE-OR-HALT club-valuation\n"
            "// ingest.  DO NOT hand-edit; regenerate after any docs/inputs/ change (see\n"
            "// ui/HOW_TO_UPDATE_INPUTS.md).  Pick prices are the engine's canonical PVC evaluated over\n"
            "// each band; no sheet value is ingested; no player value is recomputed.\n"
            "window.__CLUB_VALUATION__ = " + json.dumps(payload, ensure_ascii=False, sort_keys=True) + ";\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)


def _write_ownership(payload):
    body = ("// GENERATED by ui/tools/ingest_inputs.py — the LIVE-lane ownership MIRROR (#232, redesigned\n"
            "// by #283 under the owner ruling of 2026-07-30).\n"
            "//\n"
            "// THE STORE IS THE SINGLE SOURCE OF OWNERSHIP TRUTH.  The owner edits\n"
            "// docs/inputs/AFFL_Player_Locations.csv; the same command couriers that authorship into the\n"
            "// store's affl_team and then rebuilds THIS FILE FROM THE STORE.  It is a generated mirror and\n"
            "// is NEVER independently authoritative — it cannot override anything, because it is\n"
            "// downstream of the very field the clubs parity oracle reads.  Reader and oracle are\n"
            "// provably the same source and cannot disagree.\n"
            "//\n"
            "// HAND-EDITING IS BARRED AND ENFORCED.  This file carries the board + store identity it was\n"
            "// generated from; MD.ownership refuses a sidecar whose pin does not match the loaded app\n"
            "// (ui/app/ownership.js, pin()).  Editing it by hand does not change a club — it disables the\n"
            "// mirror.  Change ownership in the CSV and re-run; nothing here is authored.\n"
            "//\n"
            "// WHAT THIS REPLACED.  #232 shipped the inverse — the sidecar overrode and the store was the\n"
            "// fallback — which put two sources of truth behind one fact.  They agreed only while no\n"
            "// override existed; the owner's 2026-07-29 CSV moved 18 of 804 and turned the parity suite\n"
            "// red.  See ui/screenshots/issue_274/02_item2_FINDING_ownership.md.\n"
            "//\n"
            "// Ownership is not in the valuation path, so a trade still costs an edit and a reload, never\n"
            "// an engine run.  Positions are NOT here and never will be — they feed valuation and ride\n"
            "// the batched lane.\n"
            "window.__OWNERSHIP__ = " + json.dumps(payload, ensure_ascii=False, sort_keys=True) + ";\n")
    with open(OUT_OWNERSHIP, "w", encoding="utf-8") as f:
        f.write(body)


def _print_verdicts():
    print("\n  VALIDATION VERDICTS")
    print("  " + "-" * 72)
    for c, ok, d in verdicts:
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", c, ("  (%s)" % d) if d else ""))


# DISPLAY map mirrors ui/app/config.js CLUB_DISPLAY (display-only; long name stays the join key).
DISPLAY = {
    "North Melbourne Kangaroos": "North Melbourne",
    "Collingwood Magpies": "Collingwood",
    "Port Adelaide Power": "Port Adelaide",
}


def _store_apply_step0():
    """STEP 0 (#283) — courier the owner's authored ownership into the store, and move every identity
    pin the store md5 ripples into, atomically, BEFORE anything downstream reads a bundle.

    This is what makes the store the single source: by the time load_board() runs, the store already
    carries the owner's CSV and the board_view bundles have been regenerated from it, so every reader
    below is downstream of one field. Ordering is forced by two guards that already existed —
    extract_board_view ring-fences the store against expected_boot.store (so the pin must move before
    the bundles regenerate), and load_board() halts unless the bundle's store_md5 equals that pin (so
    the bundles must regenerate before this file writes its mirrors).

    A no-op when the CSV is already in the store, which is what makes re-running safe. Skipped under
    RL_OSA_SKIP=1 — the transaction invokes THIS script on its overlay to produce the two mirrors, and
    that inner run must not recurse into another transaction.

    Skipped for the same reason — and WITHOUT an environment variable, so nothing can leak into a
    child the landing spawns — under `--mirror-only` / `--check` / `--clubs-only` / `--clubs-check`:
    see SKIP_STORE_APPLY."""
    if SKIP_STORE_APPLY or os.environ.get("RL_OSA_SKIP") == "1":
        return None
    import ownership_store_apply as OSA
    try:
        return OSA.apply(ROOT)
    except OSA.Halt as e:
        halt("ownership store apply refused: %s" % e)


def run():
    step0 = _store_apply_step0()
    obj, stamp, pvc = load_board()
    players = obj.get("players", [])
    # Curve provenance: resolve the release-active pick curve from the explicit contract (deterministic,
    # fail-closed) BEFORE cross-checking the board PVC against it. Replaces the stale hardcoded L1b rule.
    contract = load_curve_contract()
    resolved = resolve_release_curve(contract)
    pvc = assert_pvc(pvc, resolved)

    board_by_nkey = collections.defaultdict(list)
    for p in players:
        board_by_nkey[nkey(p["name"])].append(p)
    check("board name-join keys unambiguous (normalised)",
          all(len(v) == 1 for v in board_by_nkey.values()),
          "dups: %s" % [k for k, v in board_by_nkey.items() if len(v) > 1])

    affl_teams = sorted({p["affl_team"] for p in players
                         if p.get("affl_team") and p["affl_team"] != FREE_AGENTS})
    check("AFFL club count", True, "%d clubs (+ Free Agents pool)" % len(affl_teams))

    own = validate_csvs(board_by_nkey, affl_teams)
    picks = load_picks(pvc, affl_teams)
    clubs, picks_by_team = build_clubs(players, picks, affl_teams)

    payload = {
        "stamp": {
            "board": stamp.get("board"), "engine": stamp.get("engine"), "store": stamp.get("store"),
            "tag": stamp.get("tag"), "expectedBoard": _expected_board_short(), "baseYear": BASE_YEAR,
            "releaseVersion": contract.get("release_version"), "asOfRound": stamp.get("asOfRound"),
            # Provenance of the release-active pick curve, resolved (never hardcoded) from the contract.
            "pvcSource": "%s (%s composed pathway; adopted %s; == rl_app_data PVC; pick1=3000)"
                         % (resolved["path"], resolved["gate"], contract.get("release_version")),
            "pvcPathway": resolved["gate"], "pvcCurveMd5": resolved["curve_md5"],
            "pvcCurveFileMd5": resolved["file_md5"], "releaseCurveContract": "ui/release_pick_curve.json",
            "pvcOk": True,
            "yearRule": "2026 = own projected band at full price; 2027 = (1/3 own + 2/3 round "
                        "average) x 0.9; 2028 = round average x 0.8. Two effects, both his: "
                        "certainty about where the pick lands decays with distance, and the asset "
                        "is discounted for being further away. The two multipliers are READ FROM "
                        "the workbook's Ladder sheet (owner word 2026-08-30).",
            "yearMultipliers": {str(y): _YEAR_MULTIPLIERS[y] for y in sorted(_YEAR_MULTIPLIERS)},
            "posture": "owner year rule 2026-08-30 (own projected band, workbook distance discount)",
            "nPicks": len(picks), "nClubs": len(clubs),
            # NO WALL CLOCK. This stamp carried a `generated` ISO timestamp until 2026-08-21 and it
            # was the ONE field that made this bundle impossible to byte-prove: "regenerate and
            # compare" can never be an equality while a field always differs, so real drift hides
            # behind it (hazard class 5, vacuity — the same argument #283 made for the ownership
            # mirror). Nothing read it as a clock: the reader that did (ui/app/club_totals.js
            # picksSource) wanted PROVENANCE, and the identity fields above are the provenance —
            # board / store / engine / asOfRound / tag pin the tree this was generated from, and
            # pvcCurveMd5 + pvcCurveFileMd5 pin the ruler the picks were priced with. That is what
            # makes this bundle a landing CARRIER (writer 6, tools/landing/steps.ui) rather than a
            # file no drift guard could ever check.
        },
        "halt": None,
        "verdicts": [{"check": c, "ok": o, "detail": d} for c, o, d in verdicts],
        "notes": notes,
        "clubs": clubs,
        "picksByTeam": {t: [{"id": p["id"], "year": p["year"], "round": p["rnd"],
                             "origin": p["origin_team"], "originDisplay": DISPLAY.get(p["origin_team"], p["origin_team"]),
                             "low": p["lo"], "high": p["hi"], "band": p["band"], "value": p["value"]}
                            for p in sorted(picks_by_team[t], key=lambda x: (x["year"], -x["value"]))]
                        for t in picks_by_team},
    }
    _write(payload)

    # ---- the LIVE-lane ownership MIRROR (#232, redesigned by #283) -------------------------------
    # THE SOURCE IS THE STORE, NOT THE CSV. `players[].affl_team` is joined from the master store by
    # extract_board_view under a store-md5 ring-fence, so writing the mirror from it — rather than from
    # the sheet a second time — is what makes reader and oracle the SAME source rather than two readers
    # that happen to agree. build_clubs() (and therefore the parity oracle transcribed from it) reads
    # this same field; there is now one field behind both.
    board_own = {p["key"]: p.get("affl_team") for p in players if p.get("key")}
    # The same-source proof, in-band on every run: after step 0 the store carries the owner's authored
    # ownership, so the authored sheet and the store-derived board MUST agree on all 804. If they do
    # not, the courier did not land and the mirror would be about to disagree with the oracle — halt
    # rather than ship the divergence this job exists to abolish. (normt() reconciles the display
    # canonicalisation the store deliberately does not apply: the store keeps the owner's exact bytes,
    # 'Free agents' and 'Free Agents' both, and the display lane folds them to one bucket.)
    drift = sorted(k for k, v in own.items() if normt(board_own.get(k)) != normt(v["club"]))
    check("authored CSV ownership == the store-derived board (single source proven)", not drift,
          "%d divergence(s)%s" % (len(drift), ("" if not drift else ": " + str(drift[:5]))))
    if drift:
        halt("SINGLE-SOURCE VIOLATION: %d player(s) differ between the owner's authored sheet and the "
             "store-derived board after the store apply: %s. The mirror is NOT written." % (len(drift), drift[:10]))
    # The mirror's rows, generated FROM the store-derived board. Display canonicalisation is applied
    # here and only here (the store keeps the owner's exact bytes; see #283 F3).
    mirror = {k: normt(board_own[k]) for k in own if board_own.get(k) is not None}
    # `overriding` was #232's count of rows where the sidecar overrode the store. Under #283 the mirror
    # IS the store, so it is structurally empty — retained as a live invariant, not as a statistic: a
    # non-zero value here would mean the mirror had stopped being generated from the store.
    diffs = sorted(k for k, v in mirror.items() if v != normt(board_own.get(k)))
    if diffs:
        halt("MIRROR DIVERGED FROM ITS SOURCE on %d row(s): %s — the #283 redesign has come undone."
             % (len(diffs), diffs[:10]))
    _write_ownership({
        "stamp": {
            # NO WALL CLOCK. #283 acceptance 4 requires this file to regenerate BYTE-DETERMINISTICALLY
            # from the store, and a timestamp makes that unassertable: "regenerate and compare" can
            # never be an equality, so real drift hides behind a field that always differs (hazard
            # class 5, vacuity). The mirror is a pure function of the store, so its provenance IS the
            # store identity — which is also the pin MD.ownership authenticates. `generatedFromStore`
            # carries it in full. (club_valuation.js kept a timestamp of its own until 2026-08-21,
            # when the same argument was applied to it and it became writer 6's carrier.)
            "generatedFromStore": _store_md5_full(),
            "source": "engine/rl_after/rl_model_data.json (affl_team), via the store-md5 ring-fenced "
                      "board join; authored by the owner in docs/inputs/AFFL_Player_Locations.csv",
            # The pin MD.ownership authenticates. A mirror that does not name the identity it was
            # generated from cannot be told apart from a stale one — that was the #232 hole.
            "board": stamp.get("board"), "store": stamp.get("store"),
            "expectedBoard": _expected_board_short(), "asOfRound": stamp.get("asOfRound"),
            "nAuthored": len(mirror), "nOverriding": len(diffs), "nBoardPlayers": len(board_own),
            "lane": "live — ownership only; positions are batched and are NOT in this file",
            "sourceOfTruth": "store",
        },
        "halt": None,
        "byKey": mirror,
        "stableIdByKey": {k: v["stableId"] for k, v in own.items() if v["stableId"]},
        "overriding": diffs,
    })
    check("ownership mirror written from the store", True,
          "%d mirrored of %d board players · %d overriding (structurally 0 since #283)"
          % (len(mirror), len(board_own), len(diffs)))

    _print_verdicts()
    print("\n  CLEAN INGEST — %d picks priced off %s (%s), %d clubs.  Bundle: %s"
          % (len(picks), resolved["path"], resolved["gate"], len(clubs), OUT))
    print("  LIVE MIRROR    — %d players mirrored FROM THE STORE, %d overriding (0 by construction "
          "since #283).  Bundle: %s" % (len(mirror), len(diffs), OUT_OWNERSHIP))
    if step0 == "APPLIED":
        print("  STORE APPLY    — the owner's authored ownership was couriered into the store and every "
              "identity pin moved with it (see the transaction log above).")
    print("\n  TOP-3 CLUBS BY OVERALL VALUE:")
    for c in clubs[:3]:
        print("    %-18s overall %s  (players %s + picks %s)" %
              (c["display"], f"{c['overall']:,}", f"{c['totalPlayer']:,}", f"{c['totalPicks']:,}"))
    return 0


FLAGS = ("--mirror-only", "--check", "--clubs-only", "--clubs-check")

USAGE = ("usage: python3 ui/tools/ingest_inputs.py "
         "[--mirror-only | --check | --clubs-only | --clubs-check]\n"
         "  (no flag)      the full ingest: club_valuation.js + ownership.js, store apply as step 0\n"
         "  --mirror-only  write ONLY ui/data/ownership.js; no store apply, no club_valuation write\n"
         "  --check        write NOTHING; regenerate the mirror and byte-compare the shipped one\n"
         "  --clubs-only   write ONLY ui/data/club_valuation.js; no store apply, no mirror write\n"
         "  --clubs-check  write NOTHING; regenerate the picks bundle and byte-compare the shipped\n"
         "                 one\n")


def main(argv=None):
    """The CLI. Five lanes, and the four fenced ones NEVER run the step-0 store apply.

    `--check` is the mirror's OWN DRIFT GUARD, and it is the same instrument writers 3 and 4 of the
    landing's `ui` step already carry (`generate_movers_transition.py --check`,
    `rebuild_movers_derived.py --check`): run the writer, then ask the writer's own checker whether
    what is on disk is what the tree now projects. A writer that reports success has proved nothing
    until something re-derives its output. It is a pure byte comparison — which is only possible
    because the mirror carries NO wall clock (#283 acceptance 4).

    `--clubs-check` is the SAME instrument, one carrier along, and it exists because the picks bundle
    stopped carrying a wall clock in the same act that made it writer 6's carrier (v827). Before that
    this lane could not have existed: a byte comparison against a file with a timestamp in it can only
    ever report drift.

    THE TWO LANES ARE MUTUALLY EXCLUSIVE, BY REFUSAL. Each exists to move exactly one file, and a run
    that claimed both would be the full ingest minus its store apply under another name — which is not
    a lane anybody asked for and would leave "which file did this move?" unanswerable at the landing.
    """
    global OUT, OUT_OWNERSHIP, SKIP_STORE_APPLY
    argv = list(sys.argv[1:] if argv is None else argv)
    unknown = [a for a in argv if a not in FLAGS]
    if unknown:
        sys.stderr.write("unknown argument(s): %s\n%s" % (", ".join(unknown), USAGE))
        return 2
    check_only = "--check" in argv
    mirror_only = check_only or "--mirror-only" in argv
    clubs_check = "--clubs-check" in argv
    clubs_only = clubs_check or "--clubs-only" in argv
    if mirror_only and clubs_only:
        sys.stderr.write("the mirror lane and the clubs lane are mutually exclusive — each writes "
                         "exactly one file; run the tool twice, or with no flag at all.\n%s" % USAGE)
        return 2

    scratch = None
    shipped = OUT_OWNERSHIP if mirror_only else OUT
    if mirror_only or clubs_only:
        SKIP_STORE_APPLY = True
        scratch = tempfile.mkdtemp(prefix="ingest_mirror_" if mirror_only else "ingest_clubs_")
    if mirror_only:
        # The club-valuation bundle is COMPUTED (its verdicts are half this job's guards) and then
        # DISCARDED: this lane exists to move exactly one file. Redirecting the global is what every
        # fixture harness in ui/tests/club_curve_provenance.test.py already does, via the same two
        # module paths.
        OUT = os.path.join(scratch, "club_valuation.js")
        if check_only:
            OUT_OWNERSHIP = os.path.join(scratch, "ownership.js")
    elif clubs_only:
        # The MIRROR is computed and discarded here, for the mirror-lane reason in reverse: the
        # single-source proof that guards it ("authored CSV ownership == the store-derived board")
        # is one of this job's guards, so it is run and its verdict kept — only the file is dropped.
        OUT_OWNERSHIP = os.path.join(scratch, "ownership.js")
        if clubs_check:
            OUT = os.path.join(scratch, "club_valuation.js")
    try:
        try:
            rc = run()
        except HaltError as e:
            _emit_halt(e.reason)
            return 2
        if clubs_check:
            want = open(OUT, "rb").read()
            have = open(shipped, "rb").read() if os.path.exists(shipped) else b""
            if want == have:
                print("\n  PICKS DRIFT GUARD — ui/data/club_valuation.js is byte-identical to what "
                      "this tree projects (%d bytes)." % len(want))
                return 0
            print("\n  PICKS DRIFT — ui/data/club_valuation.js is NOT what this tree projects "
                  "(shipped %d bytes, projected %d bytes). Re-run with --clubs-only."
                  % (len(have), len(want)))
            return 1
        if clubs_only:
            print("  CLUBS-ONLY     — the ownership mirror was computed and DISCARDED; the store "
                  "apply did not run (this lane reads the store, never writes it).")
            return rc
        if check_only:
            want = open(OUT_OWNERSHIP, "rb").read()
            have = open(shipped, "rb").read() if os.path.exists(shipped) else b""
            if want == have:
                print("\n  MIRROR DRIFT GUARD — ui/data/ownership.js is byte-identical to what this "
                      "tree projects (%d bytes)." % len(want))
                return 0
            print("\n  MIRROR DRIFT — ui/data/ownership.js is NOT what this tree projects "
                  "(shipped %d bytes, projected %d bytes). Re-run with --mirror-only."
                  % (len(have), len(want)))
            return 1
        if mirror_only:
            print("  MIRROR-ONLY    — the club-valuation bundle was computed and DISCARDED; the store "
                  "apply did not run (this lane reads the store, never writes it).")
        return rc
    finally:
        if scratch:
            shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
