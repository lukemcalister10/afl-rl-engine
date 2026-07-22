(function () {
  "use strict";
  var data = window.KINETIC_DEMO || {};
  var body = document.body;

  function comma(value) {
    return Number(value).toLocaleString("en-AU");
  }

  function signed(value) {
    if (value > 0) return "+" + comma(value);
    if (value < 0) return "−" + comma(Math.abs(value));
    return "— 0";
  }

  function movementClass(value) {
    return value > 0 ? "up" : value < 0 ? "down" : "flat";
  }

  function rankText(value) {
    if (value > 0) return "▲ " + value;
    if (value < 0) return "▼ " + Math.abs(value);
    return "— steady";
  }

  var currentBoardFilter = "all";

  function filteredBoard() {
    if (!data.board) return [];
    if (currentBoardFilter === "all") return data.board;
    return data.board.filter(function (player) {
      var pos = player.pos.toLowerCase();
      if (currentBoardFilter === "def") return pos.indexOf("def") !== -1;
      if (currentBoardFilter === "mid") return pos.indexOf("mid") !== -1;
      if (currentBoardFilter === "ruc") return pos.indexOf("ruc") !== -1;
      if (currentBoardFilter === "fwd") return pos.indexOf("fwd") !== -1;
      return true;
    });
  }

  function renderBoard() {
    var host = document.querySelector("[data-board-list]");
    if (!host || !data.board) return;
    var players = filteredBoard();
    host.innerHTML = players.map(function (player) {
      var cls = movementClass(player.delta);
      return '<a class="board-row" href="player_card_public.html" aria-label="Open ' + player.name + ' player card">' +
        '<span class="rank-big num">' + player.rank + '</span>' +
        '<span class="player-lockup"><span class="player-name">' + player.name + '</span><span class="player-meta">' + player.club + ' · public profile</span></span>' +
        '<span class="position">' + player.pos + '</span>' +
        '<span class="value-cell num">' + comma(player.value) + '</span>' +
        '<span class="power-cell"><span class="power-track"><span class="power-fill" style="--power:' + player.power + '%"></span></span><span class="power-label">' + player.power + '% of top</span></span>' +
        '<span class="move ' + cls + '"><span>' + signed(player.delta) + '</span><small>' + rankText(player.rankMove) + ' rank</small></span>' +
      '</a>';
    }).join("");
    var count = document.querySelector("[data-filter-count]");
    if (count) count.textContent = "SHOWING " + players.length + " / " + data.board.length;
  }

  function setupBoardFilters() {
    document.querySelectorAll("[data-board-filter]").forEach(function (button) {
      button.addEventListener("click", function () {
        currentBoardFilter = button.dataset.boardFilter;
        document.querySelectorAll("[data-board-filter]").forEach(function (peer) {
          var selected = peer === button;
          peer.classList.toggle("is-active", selected);
          peer.setAttribute("aria-pressed", selected ? "true" : "false");
        });
        renderBoard();
      });
    });
  }

  function renderPlayer() {
    var player = data.player;
    if (!player) return;
    document.querySelectorAll("[data-player-name]").forEach(function (el) { el.textContent = player.name; });
    document.querySelectorAll("[data-player-value]").forEach(function (el) { el.textContent = comma(player.value); });
    document.querySelectorAll("[data-player-rank]").forEach(function (el) { el.textContent = String(player.rank).padStart(2, "0"); });
    document.querySelectorAll("[data-player-delta]").forEach(function (el) { el.textContent = signed(player.delta); });
  }

  function renderMovers() {
    var host = document.querySelector("[data-mover-list]");
    if (!host || !data.movers) return;
    host.innerHTML = data.movers.map(function (mover) {
      var cls = movementClass(mover.delta);
      return '<a class="mover-card" href="player_card_public.html">' +
        '<span class="mover-rank num">' + String(mover.order).padStart(2, "0") + '</span>' +
        '<span class="mover-name"><strong>' + mover.name + '</strong><span>' + mover.pos + ' · public movement</span></span>' +
        '<span class="mover-reason"><b>' + mover.label + '</b><p>' + mover.reason + '</p></span>' +
        '<span class="mover-delta ' + cls + '"><span>' + signed(mover.delta) + '</span><small>vs round 18</small></span>' +
      '</a>';
    }).join("");
  }

  function setupMotionToggle() {
    var buttons = document.querySelectorAll("[data-motion-toggle]");
    if (!buttons.length) return;
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var stored = null;
    try { stored = window.sessionStorage.getItem("kinetic-motion"); } catch (error) { stored = null; }
    var paused = reduced || stored === "paused";

    function sync() {
      body.classList.toggle("motion-paused", paused);
      buttons.forEach(function (button) {
        button.setAttribute("aria-pressed", paused ? "true" : "false");
        button.textContent = paused ? "Play motion" : "Pause motion";
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        paused = !paused;
        try { window.sessionStorage.setItem("kinetic-motion", paused ? "paused" : "playing"); } catch (error) { /* storage is optional */ }
        sync();
      });
    });
    sync();
  }

  function duplicateMarqueeContent() {
    document.querySelectorAll("[data-marquee-track]").forEach(function (track) {
      if (track.dataset.duplicated === "true") return;
      track.innerHTML += track.innerHTML;
      track.dataset.duplicated = "true";
    });
  }

  function setCurrentNav() {
    var page = body.dataset.page;
    document.querySelectorAll("[data-nav]").forEach(function (link) {
      if (link.dataset.nav === page) link.setAttribute("aria-current", "page");
    });
  }

  renderBoard();
  setupBoardFilters();
  renderPlayer();
  renderMovers();
  duplicateMarqueeContent();
  setupMotionToggle();
  setCurrentNav();
})();
