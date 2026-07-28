/* Matchday UI — MOVERS view (native section of the existing engine; no new framework, no new shell).
   Pure view: consumes the generated movers bundle (window.__MATCHDAY_MOVERS__), never re-valuing or
   re-ranking. All deltas come from the two committed consecutive-round boards (via the report). Reuses
   the existing masthead/nav/tier shell, CSS variables, cards, tables, pills, filters and the player-
   card link (MD.go("card", key)). Fail-closes (existing .failclosed style) on an invalid/incomplete/
   mismatched report. Dual-target: the browser view + pure helpers unit-tested under node. */
(function (root) {
  "use strict";

  /* #139 item 5 — the canonical AFFL club key, resolved DUAL-TARGET.
     In the browser this defers to MD.canonClub, which derives the canonical spelling from the board
     bundle (see ui/app/format.js) — that is the shipping path. Under node the pure-logic tests load
     this file with `require` and there is no MD global and no board, so a local fallback applies the
     same fold the extractor applies (`ui/tools/extract_board_view.py` norm_club): trim, collapse
     internal whitespace, and treat the Free-Agents pool's two authored spellings as one. Both paths
     agree on the case this item is about; neither ever renames one club into a different one. */
  function canonTeam(name) {
    var g = (typeof window !== "undefined" && window.MD && window.MD.canonClub) || null;
    if (g) return g(name);
    if (name == null) return null;
    var raw = String(name).trim().replace(/\s+/g, " ");
    if (!raw) return null;
    return /^free agents$/i.test(raw) ? "Free Agents" : raw;
  }

  /* #232 — a mover row's AFFL club, resolved DUAL-TARGET on the same pattern as canonTeam above.
     In the browser this defers to MD.ownership, so the row shows the LIVE sidecar's club with the
     board's stored affl_team as the fallback. Under node the pure-logic tests load this file with
     `require`: there is no MD, no board and no sidecar, so the row's own affl_team is all there is and
     is exactly what those filter tests mean by "his club".
     Why override at all on a historical view: the movers bundle's ownership is NOT a record of who owned
     him at the time. round_movers.py:279 builds it by copying the store's CURRENT affl_team at bake
     time, with no round dimension — so keeping it preserves a stale copy, not history. */
  function ownClub(p) {
    var o = (typeof window !== "undefined" && window.MD && window.MD.ownership) || null;
    return o ? o.clubOf(p) : (p ? p.affl_team : null);
  }

  /* ---- pure, dual-target logic (unit-tested under node) ------------------------------------ */
  var core = {
    /* Fail-closed integrity of ONE report: it must carry a committed board identity, a unique + full
       active-player set, and a release identity.

       NO CHAIN. The board-identity chain check was REMOVED here on the owner's word, 2026-07-28. It
       assumed the board only moves by applying a round; the D1/D2 restructure moved it without one,
       and the re-derivation and ITEM 412 will each do so again. The tab is a from/to comparison now
       and a comparison that names its own endpoints needs no chain. Removed, not loosened. */
    integrity: function (report, bundle) {
      if (!report || report.kind !== "weekly_movers_report") return { ok: false, why: "no movers report" };
      var players = report.players || [];
      if (!players.length) return { ok: false, why: "movers report has no players" };
      var keys = {}; for (var i = 0; i < players.length; i++) keys[players[i].key] = 1;
      if (Object.keys(keys).length !== players.length) return { ok: false, why: "duplicate player rows" };
      if (report.integrity && report.integrity.players_unique === false) return { ok: false, why: "player set not unique" };
      if (report.integrity && report.integrity.coverage_full === false) return { ok: false, why: "player coverage incomplete" };
      if (report.integrity && report.integrity.board_after_matches_committed === false)
        return { ok: false, why: "board identity does not match the committed board" };
      if (!report.board_md5_after) return { ok: false, why: "missing committed board id" };
      if (!report.release_identity) return { ok: false, why: "missing release identity" };
      return { ok: true };
    },

    /* The FIXED release-baseline identity fields — immutable across weekly rounds (owner ruling
       2026-07-20). balanced_board_md5 is the fixed PRESENT-LENS baseline anchor (not the final
       full-board hash); the model pins + release_version move only at a separately-approved
       valuation-changing release. They must be identical between every report and the loaded release.
       (board / store / as_of_round are the DYNAMIC weekly fields; `board` is the current artifact.) */
    RELEASE_FIXED: ["release_version", "balanced_board_md5", "engine_head", "rl_model", "fv", "config", "register"],

    sameFixed: function (a, b) {
      a = a || {}; b = b || {};
      for (var i = 0; i < core.RELEASE_FIXED.length; i++) {
        var k = core.RELEASE_FIXED[i];
        if (a[k] == null || b[k] == null || a[k] !== b[k]) return { ok: false, field: k, a: a[k], b: b[k] };
      }
      return { ok: true };
    },

    /* ---- owner-approved release-transition bridge (ITEM 408 Items 6-7, Option A) ---------------
       The R15-R19 production reports were generated under an EARLIER accepted release. When the loaded
       application has since advanced to a DIFFERENT current release, the bundle's terminal identity no
       longer equals the loaded release, so the generic lineage check fails closed. A historical bundle
       may still be displayed under the current release ONLY via a SEPARATELY-DECLARED, owner-approved
       provenance transition (window.__MATCHDAY_TRANSITION__ / data/release_lineage.json
       `release_transition`) whose SOURCE matches the reports EXACTLY, whose DESTINATION matches the
       loaded application EXACTLY, whose covered rounds == the bundle's rounds, and whose content digest
       matches the reports byte-for-byte. Absent / partial / wrong / reversed / tampered -> fail closed.
       This never weakens generic lineage validation, adds no wildcard, and treats no matching-board-alone
       as sufficient — the full owner-approved record is required. */

    /* The identity fields a transition must bind end-to-end (fixed pins + the dynamic board/store). */
    TRANSITION_ID_FIELDS: ["release_version", "balanced_board_md5", "engine_head", "rl_model", "fv",
                           "config", "register", "board", "store"],

    /* Exact equality over a field set (transition SOURCE vs the reports' terminal identity). */
    sameId: function (a, b, fields) {
      a = a || {}; b = b || {};
      for (var i = 0; i < fields.length; i++) {
        var k = fields[i];
        if (a[k] == null || b[k] == null || a[k] !== b[k]) return { ok: false, field: k, a: a[k], b: b[k] };
      }
      return { ok: true };
    },

    /* Deterministic canonical JSON: recursively key-sorted, arrays in order, compact. Mirrors the
       Python emitter round_movers.canonical_reports_digest so both compute the identical digest. */
    canonJSON: function (v) {
      if (v === null || typeof v !== "object") return JSON.stringify(v);
      if (Array.isArray(v)) { var a = []; for (var i = 0; i < v.length; i++) a.push(core.canonJSON(v[i])); return "[" + a.join(",") + "]"; }
      var ks = Object.keys(v).sort(), p = [];
      for (var j = 0; j < ks.length; j++) p.push(JSON.stringify(ks[j]) + ":" + core.canonJSON(v[ks[j]]));
      return "{" + p.join(",") + "}";
    },

    /* Synchronous pure-JS SHA-256 (identical in browser + node; verified against node crypto and the
       standard test vectors). Returns lowercase hex. */
    sha256hex: function (ascii) {
      function rotr(n, x) { return (x >>> n) | (x << (32 - n)); }
      var K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
      var H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
      var bytes = [], i, c;
      for (i = 0; i < ascii.length; i++) {
        c = ascii.charCodeAt(i);
        if (c < 0x80) bytes.push(c);
        else if (c < 0x800) bytes.push(0xc0 | (c >> 6), 0x80 | (c & 0x3f));
        else if (c < 0xd800 || c >= 0xe000) bytes.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 0x3f), 0x80 | (c & 0x3f));
        else { i++; var c2 = ascii.charCodeAt(i); var cp = 0x10000 + (((c & 0x3ff) << 10) | (c2 & 0x3ff));
          bytes.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3f), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f)); }
      }
      var bitLen = bytes.length * 8;
      bytes.push(0x80);
      while (bytes.length % 64 !== 56) bytes.push(0);
      var hi = Math.floor(bitLen / 0x100000000), lo = bitLen >>> 0;
      bytes.push((hi >>> 24) & 0xff, (hi >>> 16) & 0xff, (hi >>> 8) & 0xff, hi & 0xff);
      bytes.push((lo >>> 24) & 0xff, (lo >>> 16) & 0xff, (lo >>> 8) & 0xff, lo & 0xff);
      var w = new Array(64), off, t;
      for (off = 0; off < bytes.length; off += 64) {
        for (t = 0; t < 16; t++)
          w[t] = (bytes[off+t*4] << 24) | (bytes[off+t*4+1] << 16) | (bytes[off+t*4+2] << 8) | (bytes[off+t*4+3]);
        for (t = 16; t < 64; t++) {
          var s0 = rotr(7, w[t-15]) ^ rotr(18, w[t-15]) ^ (w[t-15] >>> 3);
          var s1 = rotr(17, w[t-2]) ^ rotr(19, w[t-2]) ^ (w[t-2] >>> 10);
          w[t] = (w[t-16] + s0 + w[t-7] + s1) | 0;
        }
        var a=H[0],b=H[1],cc=H[2],d=H[3],e=H[4],f=H[5],g=H[6],h=H[7];
        for (t = 0; t < 64; t++) {
          var S1 = rotr(6,e) ^ rotr(11,e) ^ rotr(25,e);
          var ch = (e & f) ^ (~e & g);
          var temp1 = (h + S1 + ch + K[t] + w[t]) | 0;
          var S0 = rotr(2,a) ^ rotr(13,a) ^ rotr(22,a);
          var maj = (a & b) ^ (a & cc) ^ (b & cc);
          var temp2 = (S0 + maj) | 0;
          h=g; g=f; f=e; e=(d + temp1)|0; d=cc; cc=b; b=a; a=(temp1 + temp2)|0;
        }
        H[0]=(H[0]+a)|0; H[1]=(H[1]+b)|0; H[2]=(H[2]+cc)|0; H[3]=(H[3]+d)|0;
        H[4]=(H[4]+e)|0; H[5]=(H[5]+f)|0; H[6]=(H[6]+g)|0; H[7]=(H[7]+h)|0;
      }
      var hex = "";
      for (i = 0; i < 8; i++) hex += ("00000000" + (H[i] >>> 0).toString(16)).slice(-8);
      return hex;
    },

    /* `sha256:<hex>` over the canonical form of exactly {String(round): report} for `rounds` — the
       content anchor that makes ANY report modification (identity OR player movement) fail closed. */
    reportsDigest: function (bundle, rounds) {
      var reports = (bundle || {}).reports || {}, sub = {}, rs = rounds || (bundle || {}).rounds || [];
      for (var i = 0; i < rs.length; i++) { var k = String(rs[i]); sub[k] = reports[k]; }
      return "sha256:" + core.sha256hex(core.canonJSON(sub));
    },

    /* The loaded application must EQUAL the transition DESTINATION. The app stamp exposes some ids in
       full (board, store, balanced_board_md5, release_version) and some truncated (engine_head,
       register); every field the app exposes must equal (full) or be a prefix of (truncated) the
       declared destination. When the full release contract is present, all fixed pins must match. */
    matchAppToDest: function (dest, appId) {
      dest = dest || {}; appId = appId || {};
      if (appId.board && dest.board !== appId.board) return { ok: false, field: "board" };
      if (appId.store && dest.store !== appId.store) return { ok: false, field: "store" };
      if (appId.balanced_board_md5 && dest.balanced_board_md5 !== appId.balanced_board_md5) return { ok: false, field: "balanced_board_md5" };
      if (appId.release_version && dest.release_version !== appId.release_version) return { ok: false, field: "release_version" };
      if (appId.engine_head && String(dest.engine_head || "").indexOf(appId.engine_head) !== 0) return { ok: false, field: "engine_head" };
      if (appId.register && String(dest.register || "").indexOf(appId.register) !== 0) return { ok: false, field: "register" };
      if (appId.release) { var sf = core.sameFixed(dest, appId.release); if (!sf.ok) return { ok: false, field: sf.field }; }
      return { ok: true };
    },

    /* `bridge()` WAS HERE and was REMOVED on the owner's word, 2026-07-28.

       It enforced the owner-approved provenance transition as a GATE: a historical bundle could only
       be displayed under a different current release if the transition's source matched the reports
       exactly, its destination matched the loaded app exactly, its covered rounds equalled the
       bundle's rounds, and a sha256 over the reports matched. Every one of those clauses assumes a
       fixed consecutive series that never gains a point — so it fails the moment the board moves
       outside a round, which is now expected rather than exceptional.

       `ui/data/movers_transition.js` IS NOT DELETED. It remains owner-approved and is now READ, not
       enforced: `round_movers.model_changes()` consults it to mark which boundaries between stored
       points are model changes, so the tab can LABEL a from/to range that spans one. It becomes the
       register of those moments. Future out-of-round board moves add an entry to it. A label never
       blocks a comparison. */

    /* Fail-closed LINEAGE anchoring of the WHOLE bundle against the CURRENT loaded application
       (corrective 2026-07-20, review directives D + E; owner ruling on balanced_board_md5). The bundle
       must sit on the SAME release lineage the working app is loaded at — validated against the FULL
       release contract (window.__MATCHDAY_WORKING__.stamp.release), never abbreviated / self-declared
       stamp fields. For a POPULATED bundle:
         - FIXED identity: every report + the loaded release carry the same balanced_board_md5, and the
           latest report's release_version + engine/rl_model/fv/config/register equal the loaded release;
         - baseline board + store anchor the first report;
         - board AND store continuity between every consecutive report; previous_round == round - 1;
         - the LATEST report board_md5_after == the loaded CURRENT board, and source_store_md5_after ==
           the loaded CURRENT store; as_of_round is coherent (latest report == latest round == loaded).
       For an EMPTY bundle the baseline identity (board, store, fixed pins) is validated against the
       loaded application BEFORE returning the honest empty state — an empty bundle on the wrong lineage
       (e.g. an empty 270a2c5f bundle loaded against a DIFFERENT present-lens baseline board) fails
       closed, it is not "empty". This is generic board/store/release lineage checking: balanced_board_md5
       is the fixed present-lens baseline anchor and the moving `board` field is the complete current
       artifact; it makes no assumption about final switch values or a final full-board hash.
       `app` = {board, store, release, ...} from the loaded working stamp. Absent app.release -> best-effort
       "unanchored" (board/store/chain only); the browser always supplies the full contract. `transition`
       is the owner-approved provenance transition (window.__MATCHDAY_TRANSITION__): required, and validated
       fail-closed, ONLY when a populated bundle's terminal identity differs from the loaded release. */
    lineage: function (bundle, app, transition) {
      if (!bundle || bundle.kind !== "matchday_movers_bundle") return { ok: false, state: "nobundle", why: "no movers bundle" };
      app = app || {};
      var appRel = app.release || null;
      var rounds = (bundle.rounds || []).slice();
      var reports = bundle.reports || {};
      var baseline = bundle.baseline || {};

      // ---- EMPTY bundle: validate the baseline identity vs the loaded app before the empty state ----
      if (!rounds.length) {
        if (app.board && baseline.board && baseline.board !== app.board)
          return { ok: false, state: "mismatch", why: "empty bundle baseline board " + String(baseline.board).slice(0, 8) +
                   " does not match the loaded app board " + String(app.board).slice(0, 8) };
        if (app.store && baseline.store && baseline.store !== app.store)
          return { ok: false, state: "mismatch", why: "empty bundle baseline store " + String(baseline.store).slice(0, 8) +
                   " does not match the loaded app store " + String(app.store).slice(0, 8) };
        if (appRel) {
          var sfE = core.sameFixed(baseline.release_identity, appRel);
          if (!sfE.ok) return { ok: false, state: "mismatch", why: "empty bundle baseline release identity differs at " + sfE.field };
        }
        return { ok: true, state: "empty", why: "no finalized round reports yet" };
      }

      // ---- POPULATED bundle ----
      var first = reports[String(rounds[0])];
      if (!first) return { ok: false, state: "mismatch", why: "bundle lists round " + rounds[0] + " but has no report for it" };
      if (baseline.board && first.board_md5_before && first.board_md5_before !== baseline.board)
        return { ok: false, state: "mismatch", why: "first report baseline board " + String(first.board_md5_before).slice(0, 8) +
                 " does not match the release baseline board " + String(baseline.board).slice(0, 8) };
      if (baseline.store && first.source_store_md5_before && first.source_store_md5_before !== baseline.store)
        return { ok: false, state: "mismatch", why: "first report baseline store does not match the release baseline store" };
      // fixed balanced_board_md5 identical across EVERY report
      for (var b = 0; b < rounds.length; b++) {
        var rb = reports[String(rounds[b])], rel = (rb || {}).release_identity || {};
        if (baseline.release_identity && baseline.release_identity.balanced_board_md5 &&
            rel.balanced_board_md5 !== baseline.release_identity.balanced_board_md5)
          return { ok: false, state: "mismatch", why: "R" + rounds[b] + " carries a different balanced_board_md5 than the baseline" };
      }
      // NO CONTINUITY LOOP. The consecutive board/store chain and the `previous_round == round - 1`
      // rule were REMOVED here on the owner's word, 2026-07-28, along with the two `integrity` flags.
      // They policed a fixed consecutive series. The board moves outside a round (the D1/D2
      // restructure did; the re-derivation and ITEM 412 will), so a chain can only be true until the
      // next such move. What replaces them is a single assert enforced at finalisation — the newest
      // stored comparison point is the live board — plus the fact that a from/to comparison states
      // its own two endpoints. Every report below is still checked for its own integrity.

      // REMOVED with the chain (2026-07-28), and NOT in the directive's enumerated list — recorded in
      // the hand-back. This required every report to carry an IDENTICAL fixed release identity to the
      // first. That is the same "one unchanging release across a fixed consecutive series" assumption
      // the chain made, and it is false for the same reason: the engine changed at D2, so R15's
      // engine_head (dc7e34b0) legitimately differs from R20's (7c452715). Left in place it fail-closes
      // the whole tab forever — it was survivable before ONLY because bridge() existed to work around
      // it, and bridge() is gone. A report keeping its OWN governing identity is deliberate
      // (round_movers.py:23); requiring them all to match contradicts that and contradicts labelling
      // model changes at all. Per-report integrity is still checked by core.integrity, and currency is
      // covered by the one assert below.

      var last = reports[String(rounds[rounds.length - 1])];
      var lastRel = last.release_identity || {};
      // as_of_round coherence (within the latest report)
      if (lastRel.as_of_round != null && lastRel.as_of_round !== last.submitted_round)
        return { ok: false, state: "mismatch", why: "latest report as_of_round " + lastRel.as_of_round + " != submitted round " + last.submitted_round };

      // The bundle's historical TERMINAL identity (the SOURCE side of any release transition): the
      // latest report's governing release + its committed terminal board/store.
      var histId = {
        release_version: lastRel.release_version, balanced_board_md5: lastRel.balanced_board_md5,
        engine_head: lastRel.engine_head, rl_model: lastRel.rl_model, fv: lastRel.fv,
        config: lastRel.config, register: lastRel.register,
        board: last.board_md5_after, store: last.source_store_md5_after, as_of_round: last.submitted_round,
      };

      // DIRECT lineage: the terminal identity already equals the loaded release (SAME lineage; no
      // transition needed). board/store must equal the loaded current; fixed pins + version + balanced
      // must equal whatever the loaded app exposes.
      var directBoard = !app.board || histId.board === app.board;
      var directStore = !app.store || histId.store === app.store;
      var directFixed = !appRel || core.sameFixed(lastRel, appRel).ok;
      var directBalanced = !app.balanced_board_md5 || histId.balanced_board_md5 === app.balanced_board_md5;
      var directVersion = !app.release_version || histId.release_version === app.release_version;
      if (directBoard && directStore && directFixed && directBalanced && directVersion) {
        if (appRel && appRel.as_of_round != null && lastRel.as_of_round != null && appRel.as_of_round !== lastRel.as_of_round)
          return { ok: false, state: "mismatch", why: "loaded as_of_round " + appRel.as_of_round + " != latest report as_of_round " + lastRel.as_of_round };
        return appRel ? { ok: true, state: "ok" } : { ok: true, state: "unanchored" };
      }

      // NOT the same lineage as the loaded release. That is now EXPECTED, not exceptional: historical
      // reports were generated under earlier releases and the board moves outside rounds. The
      // owner-approved transition is no longer consulted as a gate (see the note where `bridge()`
      // used to be) — it is read by the producer to LABEL model-change ranges.
      //
      // THE ONE ASSERT, browser side, mirroring round_finalize._newest_point_vs_live_board: the
      // NEWEST stored point must be the board the application is actually serving. Everything older
      // is history and needs no continuity. This is what keeps the removal from being a blanket
      // "always ok" — an out-of-date or foreign bundle still fails closed here.
      if (app.board) {
        var pts = core.points(bundle);
        var newestBoard = null;
        if (pts.length) {
          var np = pts[pts.length - 1];
          newestBoard = np.board || ((reports[String(np.id)] || {}).board_md5_after) || null;
        } else {
          newestBoard = histId.board;
        }
        if (newestBoard !== app.board)
          return { ok: false, state: "mismatch", why: "newest stored point is board " +
                   String(newestBoard).slice(0, 8) + " but the loaded board is " + String(app.board).slice(0, 8) };
      }
      return { ok: true, state: "bridged" };
    },

    /* ---- FROM/TO comparison (owner word 2026-07-28) -------------------------------------------
       Every stored point — numbered rounds plus out-of-round columns — is selectable as either end.
       Deltas are computed here from `bundle.values`, never stored, so adding a point can never
       invalidate an existing comparison and there is nothing to keep continuous. */

    points: function (bundle) { return ((bundle || {}).points || []).slice(); },

    /* Does the selected range cross a board move that happened outside a round? If so the tab must
       SAY so — part of the difference is the model, not the players. A label, never a gate. */
    spansModelChange: function (bundle, fromId, toId) {
      var pts = core.points(bundle), ids = pts.map(function (p) { return p.id; });
      var a = ids.indexOf(String(fromId)), b = ids.indexOf(String(toId));
      if (a < 0 || b < 0) return [];
      var lo = Math.min(a, b), hi = Math.max(a, b), out = [];
      var changes = (bundle || {}).model_changes || [];
      for (var i = 0; i < changes.length; i++) {
        var bd = changes[i].between || [];
        var x = ids.indexOf(String(bd[0])), y = ids.indexOf(String(bd[1]));
        if (x >= lo && y <= hi && x >= 0 && y >= 0) out.push(changes[i]);
      }
      return out;
    },

    /* A report-shaped object for any two stored points, so every view/sort/filter below works
       unchanged. When the range exactly reproduces a STORED round report, that report is returned
       as-is — it carries the played/score facts, which a bare value diff cannot know. */
    compare: function (bundle, fromId, toId) {
      bundle = bundle || {};
      var stored = (bundle.reports || {})[String(toId)];
      if (stored && String(stored.previous_round) === String(fromId)) return stored;

      var values = bundle.values || {}, players = [];
      for (var key in values) {
        if (!Object.prototype.hasOwnProperty.call(values, key)) continue;
        var rec = values[key], bp = rec.byPoint || {};
        var a = bp[String(fromId)], b = bp[String(toId)];
        if (!a || !b) continue;
        var dv = (a.v != null && b.v != null) ? (b.v - a.v) : null;
        players.push({
          key: key, name: rec.name, club: rec.club, affl_team: rec.affl_team,
          pos: rec.pos, posCode: rec.posCode,
          played: null, dnp: false, score: null,
          prev_value: a.v, cur_value: b.v, value_change: dv,
          value_change_pct: (dv != null && a.v) ? Math.round(dv / a.v * 10000) / 100 : null,
          prev_rank: a.rank, cur_rank: b.rank,
          rank_change: (a.rank != null && b.rank != null) ? (a.rank - b.rank) : null,
          prev_pos_rank: a.pos_rank, cur_pos_rank: b.pos_rank,
          pos_rank_change: (a.pos_rank != null && b.pos_rank != null) ? (a.pos_rank - b.pos_rank) : null,
        });
      }
      players.sort(function (x, y) { return x.key < y.key ? -1 : x.key > y.key ? 1 : 0; });

      function rankView(field, desc) {
        var e = players.filter(function (p) { return p[field] != null; });
        e.sort(function (x, y) {
          var d = desc ? y[field] - x[field] : x[field] - y[field];
          if (d) return d;
          var cv = (y.cur_value || 0) - (x.cur_value || 0);
          return cv || (x.key < y.key ? -1 : 1);
        });
        return e.slice(0, 50).map(function (p) { return p.key; });
      }
      return {
        kind: "weekly_movers_report", synthetic: true,
        submitted_round: toId, previous_round: fromId,
        players: players, player_count: players.length,
        views: {
          value_risers: rankView("value_change", true), value_fallers: rankView("value_change", false),
          rank_risers: rankView("rank_change", true), rank_fallers: rankView("rank_change", false),
          played_count: null, dnp_count: null,
        },
      };
    },

    /* Deterministic comparator: primary movement field (dir), then current value desc, then key asc. */
    cmp: function (field, dir) {
      var sgn = dir === "asc" ? 1 : -1;
      return function (a, b) {
        var av = a[field], bv = b[field];
        var an = (av === null || av === undefined), bn = (bv === null || bv === undefined);
        if (an && bn) { /* both null */ }
        else if (an) return 1;   // nulls sort last regardless of dir
        else if (bn) return -1;
        else if (av !== bv) return sgn * (av < bv ? -1 : 1);
        var acv = a.cur_value == null ? -Infinity : a.cur_value;
        var bcv = b.cur_value == null ? -Infinity : b.cur_value;
        if (acv !== bcv) return bcv - acv;              // current value descending
        return a.key < b.key ? -1 : (a.key > b.key ? 1 : 0);  // stable key ascending
      };
    },

    filter: function (players, f) {
      f = f || {};
      return players.filter(function (p) {
        // #139 item 5: match on the CANONICAL club key. The stored reports carry both authored
        // spellings of the Free-Agents pool, so an exact-string match selected only part of it.
        // #232: ownership comes from the live sidecar, not the row's baked affl_team. The movers
        // bundle's ownership is NOT history — round_movers.py:279 builds it by copying the store's
        // CURRENT affl_team at bake time, with no round dimension, so it was never "his club as at
        // R15". Keeping it would preserve a stale copy, not a record. Every mover row is keyed, so
        // this resolves without the name bridge.
        if (f.club && (canonTeam(ownClub(p)) || "—") !== (canonTeam(f.club) || "—")) return false;
        if (f.pos && p.pos !== f.pos) return false;
        if (f.status === "played" && !p.played) return false;
        if (f.status === "dnp" && p.played) return false;
        return true;
      });
    },

    /* The rows for a named view (value/rank risers/fallers, or all), filtered + deterministically sorted. */
    viewRows: function (report, view, f) {
      var players = core.filter(report.players || [], f);
      var spec = {
        value_risers: ["value_change", "desc"], value_fallers: ["value_change", "asc"],
        rank_risers: ["rank_change", "desc"], rank_fallers: ["rank_change", "asc"],
        all: ["cur_value", "desc"],
      }[view] || ["cur_value", "desc"];
      return players.slice().sort(core.cmp(spec[0], spec[1]));
    },

    /* The four summary headline movers (largest value inc/dec, largest overall-rank imp/decline). */
    summary: function (report) {
      var P = report.players || [];
      function top(field, dir) {
        var s = P.slice().sort(core.cmp(field, dir));
        return s.length ? s[0] : null;
      }
      return {
        value_increase: top("value_change", "desc"),
        value_decrease: top("value_change", "asc"),
        rank_improve: top("rank_change", "desc"),
        rank_decline: top("rank_change", "asc"),
      };
    },
  };

  /* ---- browser view ------------------------------------------------------------------------ */
  function makeView(MD) {
    var fmt = MD.fmt;
    var state = { round: null, from: null, to: null, view: "value_risers", club: null, pos: null, status: null, sort: null, dir: "desc" };

    function bundle() { return (typeof window !== "undefined" && window.__MATCHDAY_MOVERS__) || null; }

    /* The identity of the working board the app is CURRENTLY loaded at — the lineage anchor. Prefers
       the FULL release contract (stamp.release: full-length board/store + fixed pins) so lineage is
       validated against verified identity, not the abbreviated stamp fields. */
    function appIdentity() {
      var w = (typeof window !== "undefined") && window.__MATCHDAY_WORKING__;
      var st = w && w.stamp;
      if (!st) return null;
      var rel = st.release || null;
      // board/store/balanced/release_version are exposed in FULL by the stamp; engine_head/register may
      // be truncated (the transition destination check tolerates a prefix). Prefer the full release
      // contract (stamp.release) when present.
      return {
        board: (rel && rel.board) || st.srcmd5 || st.board,
        store: (rel && rel.store) || st.store_md5 || st.store,
        balanced_board_md5: (rel && rel.balanced_board_md5) || st.balanced_board_md5,
        release_version: (rel && rel.release_version) || st.releaseVersion || st.tag,
        engine_head: (rel && rel.engine_head) || st.engine,
        register: (rel && rel.register) || st.register,
        as_of_round: (rel && rel.as_of_round != null) ? rel.as_of_round : st.asOfRound,
        release: rel,
      };
    }

    /* The owner-approved provenance transition the browser loads alongside the working board + bundle. */
    function transitionRecord() { return (typeof window !== "undefined" && window.__MATCHDAY_TRANSITION__) || null; }

    function availableRounds(b) { return (b && b.rounds) ? b.rounds.slice() : []; }

    function reportFor(b, rnd) { return b && b.reports ? b.reports[String(rnd)] : null; }

    /* HONEST empty state — no finalized round reports yet. This is NOT an integrity alarm and NOT
       scratch data; a fresh baseline (e.g. Round 14) app renders exactly this. */
    function emptyState(holder, why) {
      var box = fmt.el("div", "moversempty");
      box.innerHTML = "<h1>Movers — no finalized round reports yet</h1>" +
        "<p>Weekly movers appear here once a round's scores are applied and <b>finalized</b>. There are " +
        "no finalized round reports on this build, so the view is intentionally empty rather than " +
        "showing placeholder or scratch data.</p>" +
        '<p class="mono">' + fmt.esc(why || "no finalized round reports") + "</p>";
      holder.appendChild(box);
    }

    function failState(holder, why) {
      var box = fmt.el("div", "failclosed");
      box.innerHTML = "<h1>■ Movers unavailable — integrity check failed</h1>" +
        "<p>The Movers view renders only a movers report whose transaction committed and whose board " +
        "identities sit on the SAME lineage as the loaded application. This bundle did not pass the " +
        "lineage / integrity check, so nothing is shown rather than showing stale, out-of-lineage or " +
        "partial data.</p>" +
        '<p class="mono">reason: ' + fmt.esc(why) + "</p>";
      holder.appendChild(box);
    }

    function metaStrip(report) {
      var s = fmt.el("div", "strip moversmeta");
      var rel = report.release_identity || {};
      s.innerHTML =
        '<span class="lbl">Round</span><b class="num">R' + report.submitted_round + "</b>" +
        '<span class="lbl">baseline</span><b class="num">R' + report.previous_round + "</b>" +
        '<span class="lbl">players</span><b class="num">' + fmt.n(report.player_count) + "</b>" +
        '<span class="lbl">played</span><b class="num">' + fmt.n((report.views || {}).played_count) + "</b>" +
        '<span class="lbl">DNP</span><b class="num">' + fmt.n((report.views || {}).dnp_count) + "</b>" +
        '<span class="lbl">board</span><b class="num">' + fmt.esc(String(report.board_md5_before || "").slice(0, 8)) +
          " → " + fmt.esc(String(report.board_md5_after || "").slice(0, 8)) + "</b>" +
        '<span class="lbl">release</span><b class="num">' + fmt.esc(rel.release_version || "—") + "</b>";
      return s;
    }

    function roundSelect(b, report) {
      const wrap = fmt.el("div", "strip moversbar");
      const pts = core.points(b);

      // TWO dropdowns — compare any two stored points. Rounds and out-of-round columns (e.g. the
      // post-restructure board) are equally selectable; the tab no longer assumes a fixed series.
      function pointSel(which, selected) {
        const sel = fmt.el("select", "boardsel");
        pts.forEach(function (p) {
          const o = fmt.el("option", "", p.label);
          o.value = String(p.id); if (String(p.id) === String(selected)) o.selected = true;
          sel.appendChild(o);
        });
        sel.addEventListener("change", function () {
          state[which] = sel.value; state.sort = null; render(MD.__moversHolder);
        });
        return sel;
      }
      wrap.appendChild(fmt.el("span", "lbl", "From"));
      wrap.appendChild(pointSel("from", state.from));
      wrap.appendChild(fmt.el("span", "lbl", "To"));
      wrap.appendChild(pointSel("to", state.to));

      // view toggle (value risers/fallers, rank risers/fallers, all)
      const seg = fmt.el("div", "seg");
      [["value_risers", "Value risers"], ["value_fallers", "Value fallers"], ["rank_risers", "Rank risers"],
       ["rank_fallers", "Rank fallers"], ["all", "All players"]].forEach(function (d) {
        const btn = fmt.el("button", state.view === d[0] ? "on" : "", d[1]);
        btn.addEventListener("click", function () { state.view = d[0]; state.sort = null; render(MD.__moversHolder); });
        seg.appendChild(btn);
      });
      wrap.appendChild(seg);
      return wrap;
    }

    function filterBar(report) {
      const row = fmt.el("div", "strip moversfilters");
      row.appendChild(fmt.el("span", "lbl", "Filter"));
      // club
      // #139 item 5: key the dropdown by the CANONICAL club name so the two authored spellings of the
      // Free-Agents pool collapse to one entry that selects the whole pool.
      const clubs = {}; (report.players || []).forEach(function (p) {
        const c = canonTeam(ownClub(p)); if (c) clubs[c] = 1;   // #232: live ownership
      });
      const csel = fmt.el("select", "boardsel");
      csel.appendChild(new Option("All clubs", ""));
      Object.keys(clubs).sort().forEach(function (c) { const o = new Option(fmt.club(c), c); if (c === state.club) o.selected = true; csel.appendChild(o); });
      csel.addEventListener("change", function () { state.club = csel.value || null; render(MD.__moversHolder); });
      row.appendChild(csel);
      // position
      const poss = {}; (report.players || []).forEach(function (p) { if (p.pos) poss[p.pos] = 1; });
      const psel = fmt.el("select", "boardsel");
      psel.appendChild(new Option("All positions", ""));
      Object.keys(poss).sort().forEach(function (c) { const o = new Option(c, c); if (c === state.pos) o.selected = true; psel.appendChild(o); });
      psel.addEventListener("change", function () { state.pos = psel.value || null; render(MD.__moversHolder); });
      row.appendChild(psel);
      // played / DNP
      const stseg = fmt.el("div", "seg");
      [["", "All"], ["played", "Played"], ["dnp", "DNP"]].forEach(function (d) {
        const btn = fmt.el("button", (state.status || "") === d[0] ? "on" : "", d[1]);
        btn.addEventListener("click", function () { state.status = d[0] || null; render(MD.__moversHolder); });
        stseg.appendChild(btn);
      });
      row.appendChild(stseg);
      return row;
    }

    function card(label, p, kind) {
      const c = fmt.el("div", "movercard");
      if (!p) { c.innerHTML = '<div class="mcl">' + label + '</div><div class="mcv">—</div>'; return c; }
      const isVal = kind === "value";
      const d = isVal ? p.value_change : p.rank_change;
      c.innerHTML = '<div class="mcl">' + label + "</div>" +
        '<div class="mcn">' + fmt.esc(p.name) + "</div>" +
        '<div class="mcv ' + fmt.cls(d) + '">' + (isVal ? fmt.signed(d) : (fmt.signed(d) + " places")) + "</div>" +
        '<div class="mcs num">' + (isVal ? (fmt.n(p.prev_value) + " → " + fmt.n(p.cur_value))
                                          : ("rank " + fmt.n(p.prev_rank) + " → " + fmt.n(p.cur_rank))) + "</div>";
      c.addEventListener("click", function () { MD.go("card", p.key); });
      c.style.cursor = "pointer";
      return c;
    }

    function summaryCards(report) {
      const s = core.summary(report);
      const grid = fmt.el("div", "movercards");
      grid.appendChild(card("Largest value increase", s.value_increase, "value"));
      grid.appendChild(card("Largest value decrease", s.value_decrease, "value"));
      grid.appendChild(card("Largest rank improvement", s.rank_improve, "rank"));
      grid.appendChild(card("Largest rank decline", s.rank_decline, "rank"));
      return grid;
    }

    function table(report) {
      let rows = core.viewRows(report, state.view, { club: state.club, pos: state.pos, status: state.status });
      var total = rows.length;
      // the focused views show the headline movers (not the whole ~800 board); "All players" is the
      // complete sortable/filterable table. Keeps the default view from overwhelming, per the spec.
      if (state.view !== "all" && !state.sort) rows = rows.slice(0, 60);
      if (state.sort) rows = rows.slice().sort(core.cmp(state.sort, state.dir));
      const wrap = fmt.el("div", "movertable");
      const head = fmt.el("div", "moverhead");
      const cols = [["cur_rank", "Rank"], ["name", "Player"], ["played", "P/DNP"], ["cur_value", "Value"],
                    ["value_change", "Δ value"], ["value_change_pct", "Δ%"], ["rank_change", "Δ rank"],
                    ["pos_rank_change", "Δ pos"]];
      cols.forEach(function (c) {
        const h = fmt.el("div", "mh" + (c[0] === "name" ? " l" : " r"), c[1]);
        h.setAttribute("data-sort", c[0]);
        h.addEventListener("click", function () {
          if (state.sort === c[0]) state.dir = state.dir === "desc" ? "asc" : "desc";
          else { state.sort = c[0]; state.dir = "desc"; }
          render(MD.__moversHolder);
        });
        head.appendChild(h);
      });
      wrap.appendChild(head);
      const body = fmt.el("div", "moverrows");
      rows.forEach(function (p) {
        const r = fmt.el("div", "moverrow" + (p.dnp ? " dnp" : ""));
        r.setAttribute("data-key", p.key);
        r.innerHTML =
          '<div class="mr rank num">' + fmt.n(p.cur_rank) + "</div>" +
          '<div class="mr who"><span class="nm">' + fmt.esc(p.name) + "</span>" +
            '<span class="sub">' + fmt.esc(p.pos || "—") + " · " +
              fmt.esc(ownClub(p) ? MD.ownership.labelOf(p) : fmt.club(p.club || "—")) + "</span></div>" +
          '<div class="mr pdn">' + (p.played
              ? '<span class="pill up">PLAYED ' + fmt.n(p.score) + "</span>"
              : '<span class="pill na">DNP</span>') + "</div>" +
          '<div class="mr val num">' + fmt.n(p.cur_value) + "</div>" +
          '<div class="mr dv"><span class="pill ' + fmt.cls(p.value_change) + '">' + fmt.signed(p.value_change) + "</span></div>" +
          '<div class="mr dvp num ' + fmt.cls(p.value_change) + '">' + (p.value_change_pct == null ? "—" : (p.value_change_pct > 0 ? "+" : "") + p.value_change_pct.toFixed(1) + "%") + "</div>" +
          '<div class="mr dr"><span class="pill ' + fmt.cls(p.rank_change) + '">' + fmt.signed(p.rank_change) + "</span></div>" +
          '<div class="mr dpr num ' + fmt.cls(p.pos_rank_change) + '">' + fmt.signed(p.pos_rank_change) + "</div>";
        r.addEventListener("click", function () { MD.go("card", p.key); });
        body.appendChild(r);
      });
      wrap.appendChild(body);
      const count = fmt.el("div", "movercount", fmt.n(rows.length) + " of " + fmt.n(total) +
        " shown · " + '<span class="num">' + fmt.n((report.views || {}).played_count) + "</span> played · " +
        '<span class="num">' + fmt.n((report.views || {}).dnp_count) + "</span> DNP" +
        (state.view !== "all" && !state.sort && total > rows.length ? " · switch to <b>All players</b> for the complete table" : ""));
      wrap.appendChild(count);
      return wrap;
    }

    function render(holder) {
      MD.__moversHolder = holder;
      holder.innerHTML = "";
      const b = bundle();
      // LINEAGE first: anchor the whole bundle to the loaded application before touching a report. A
      // populated historical bundle on a DIFFERENT current release is bridged only by the owner-approved
      // provenance transition (fail-closed inside core.lineage).
      const lin = core.lineage(b, appIdentity(), transitionRecord());
      if (lin.state === "empty") { emptyState(holder, lin.why); return; }   // honest empty, not an alarm
      if (!lin.ok) { failState(holder, lin.why); return; }                  // out-of-lineage -> fail closed
      // FROM/TO defaults: the two most recent stored points, so ordinary use is unchanged.
      const pts = core.points(b);
      if (pts.length >= 2) {
        if (state.to == null) state.to = pts[pts.length - 1].id;
        if (state.from == null) state.from = pts[pts.length - 2].id;
      } else if (pts.length === 1) {
        if (state.to == null) state.to = pts[0].id;
        if (state.from == null) state.from = pts[0].id;
      }
      const report = core.compare(b, state.from, state.to);
      // A synthetic comparison carries no committed-report identity; only a STORED report is checked.
      if (!report.synthetic) {
        const intg = core.integrity(report, b);
        if (!intg.ok) { failState(holder, intg.why); return; }
      } else if (!report.players.length) {
        failState(holder, "no players are recorded at both selected points"); return;
      }
      holder.appendChild(roundSelect(b, report));
      const spans = core.spansModelChange(b, state.from, state.to);
      if (spans.length) {
        const names = spans.map(function (s) { return s.label; }).join(", ");
        holder.appendChild(fmt.el("div", "note modelchange",
          "This range spans " + fmt.esc(names) + " — a change to the model itself, not to the players. " +
          "Part of every difference below comes from that redesign rather than from football."));
      }
      holder.appendChild(metaStrip(report));
      holder.appendChild(summaryCards(report));
      holder.appendChild(filterBar(report));
      holder.appendChild(table(report));
    }

    return { render: render, core: core, _state: state };
  }

  /* ---- registration: browser (window.MD) + node (module.exports for tests) ----------------- */
  if (typeof window !== "undefined") {
    window.MD = window.MD || {};
    // defer construction until MD.fmt exists (script order guarantees it, but be safe)
    window.MD.movers = (window.MD.fmt) ? makeView(window.MD) : { render: function (h) { window.MD.movers = makeView(window.MD); window.MD.movers.render(h); }, core: core };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { core: core, makeView: makeView };
  }
})(this);
