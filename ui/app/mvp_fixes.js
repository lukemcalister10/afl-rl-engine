/* Round 19 MVP review corrections: canonical free-agent label, arbitrary round comparison,
   and committed weekly history on player cards. Display-only; no valuation or ranking math. */
(function () {
  "use strict";
  window.MD = window.MD || {};
  var fmt = MD.fmt;
  var originalMovers = MD.movers;
  var moversCore = originalMovers && originalMovers.core;
  var originalCardRender = MD.card && MD.card.render;

  function teamName(value) {
    if (value == null) return value;
    var clean = String(value).trim();
    return clean.toLowerCase() === "free agents" ? "Free agents" : clean;
  }
  MD.teamName = teamName;

  /* Normalize the two source-case variants in the in-memory view only. The committed player/store facts
     are not rewritten; all filters and labels now use one canonical AFFL category. */
  function normalizeTeams() {
    [window.__MATCHDAY_WORKING__, window.__MATCHDAY_PUBLIC__].forEach(function (bundle) {
      if (!bundle) return;
      (bundle.players || []).forEach(function (p) { if (p.affl_team) p.affl_team = teamName(p.affl_team); });
      (bundle.back || []).forEach(function (p) { if (p.affl_team) p.affl_team = teamName(p.affl_team); });
    });
    var b = window.__MATCHDAY_MOVERS__;
    if (b && b.reports) Object.keys(b.reports).forEach(function (r) {
      (b.reports[r].players || []).forEach(function (p) { if (p.affl_team) p.affl_team = teamName(p.affl_team); });
    });
  }
  normalizeTeams();

  var oldClub = fmt.club;
  fmt.club = function (name) { return oldClub(teamName(name)); };

  function bundle() { return window.__MATCHDAY_MOVERS__ || null; }
  function appIdentity() {
    var w = window.__MATCHDAY_WORKING__, st = w && w.stamp, rel = st && st.release;
    if (!st) return null;
    return { board: (rel && rel.board) || st.srcmd5 || st.board,
             store: (rel && rel.store) || st.store_md5 || st.store,
             release: rel || null };
  }

  /* Reconstruct the durable R14..latest state from the chained adjacent-round reports. No value is
     calculated: each cell is copied from a committed report's prev_* or cur_* fields. */
  function buildHistory() {
    var b = bundle();
    var rounds = (b && b.rounds || []).slice().sort(function (a, z) { return a - z; });
    var states = {}, boards = {};
    if (!rounds.length) return { rounds: [], states: states, boards: boards };
    rounds.forEach(function (rnd, idx) {
      var rep = b.reports[String(rnd)];
      if (!rep) return;
      var base = Number(rep.previous_round);
      if (!states[base]) states[base] = {};
      if (!states[rnd]) states[rnd] = {};
      if (idx === 0) boards[base] = rep.board_md5_before;
      boards[rnd] = rep.board_md5_after;
      (rep.players || []).forEach(function (p) {
        if (!states[base][p.key]) states[base][p.key] = {
          key: p.key, name: p.name, pos: p.pos, affl_team: teamName(p.affl_team),
          value: p.prev_value, rank: p.prev_rank, pos_rank: p.prev_pos_rank,
          played: null, score: null
        };
        states[rnd][p.key] = {
          key: p.key, name: p.name, pos: p.pos, affl_team: teamName(p.affl_team),
          value: p.cur_value, rank: p.cur_rank, pos_rank: p.cur_pos_rank,
          played: !!p.played, score: p.score
        };
      });
    });
    return { rounds: Object.keys(states).map(Number).sort(function (a, z) { return a-z; }),
             states: states, boards: boards };
  }
  MD.roundHistory = buildHistory;

  function comparison(baseRound, comparisonRound) {
    var h = buildHistory(), base = h.states[baseRound] || {}, cur = h.states[comparisonRound] || {};
    var keys = Object.keys(cur).filter(function (k) { return base[k]; });
    return {
      baseRound: baseRound, comparisonRound: comparisonRound,
      baseBoard: h.boards[baseRound], comparisonBoard: h.boards[comparisonRound],
      players: keys.map(function (key) {
        var a = base[key], z = cur[key], dv = z.value - a.value;
        return {
          key: key, name: z.name || a.name, pos: z.pos || a.pos,
          affl_team: teamName(z.affl_team || a.affl_team),
          prev_value: a.value, cur_value: z.value, value_change: dv,
          value_change_pct: a.value ? (100 * dv / a.value) : null,
          prev_rank: a.rank, cur_rank: z.rank,
          rank_change: (a.rank == null || z.rank == null) ? null : a.rank - z.rank,
          prev_pos_rank: a.pos_rank, cur_pos_rank: z.pos_rank,
          pos_rank_change: (a.pos_rank == null || z.pos_rank == null) ? null : a.pos_rank - z.pos_rank,
          played: z.played, dnp: z.played === false, score: z.score
        };
      })
    };
  }
  MD.compareRounds = comparison;

  var mstate = { base: null, comparison: null, view: "value_risers", club: null, pos: null,
                 status: null, sort: null, dir: "desc" };

  function fail(holder, why) {
    holder.innerHTML = '<div class="failclosed"><h1>■ Movers unavailable — integrity check failed</h1>' +
      '<p>The committed round chain did not pass its lineage check, so no reconstructed comparison is shown.</p>' +
      '<p class="mono">reason: ' + fmt.esc(why) + '</p></div>';
  }

  function selectBox(rounds, value, label, allowed) {
    var wrap = fmt.el("label", "roundpick");
    wrap.appendChild(fmt.el("span", "lbl", label));
    var sel = fmt.el("select", "boardsel");
    rounds.filter(allowed || function () { return true; }).forEach(function (r) {
      var o = new Option("Round " + r, String(r));
      if (r === value) o.selected = true;
      sel.appendChild(o);
    });
    wrap.appendChild(sel);
    return { wrap: wrap, select: sel };
  }

  function cmp(field, dir) {
    var sign = dir === "asc" ? 1 : -1;
    return function (a, b) {
      var av=a[field], bv=b[field], an=av==null, bn=bv==null;
      if (an !== bn) return an ? 1 : -1;
      if (!an && av !== bv) return sign * (av < bv ? -1 : 1);
      if (a.cur_value !== b.cur_value) return b.cur_value-a.cur_value;
      return a.key < b.key ? -1 : a.key > b.key ? 1 : 0;
    };
  }

  function filteredRows(rep) {
    var rows = rep.players.filter(function (p) {
      if (mstate.club && teamName(p.affl_team) !== mstate.club) return false;
      if (mstate.pos && p.pos !== mstate.pos) return false;
      if (mstate.status === "played" && !p.played) return false;
      if (mstate.status === "dnp" && p.played !== false) return false;
      return true;
    });
    var spec = {
      value_risers:["value_change","desc"], value_fallers:["value_change","asc"],
      rank_risers:["rank_change","desc"], rank_fallers:["rank_change","asc"], all:["cur_value","desc"]
    }[mstate.view];
    return rows.slice().sort(cmp(mstate.sort || spec[0], mstate.sort ? mstate.dir : spec[1]));
  }

  function top(rows, field, dir) { return rows.slice().sort(cmp(field, dir))[0] || null; }
  function moverCard(label, p, field) {
    var c=fmt.el("div","movercard");
    if (!p) { c.innerHTML='<div class="mcl">'+label+'</div><div class="mcv">—</div>'; return c; }
    var d=p[field];
    c.innerHTML='<div class="mcl">'+label+'</div><div class="mcn">'+fmt.esc(p.name)+'</div>'+
      '<div class="mcv '+fmt.cls(d)+'">'+fmt.signed(d)+(field==="rank_change"?' places':'')+'</div>'+
      '<div class="mcs num">'+(field==="rank_change" ? 'rank '+fmt.n(p.prev_rank)+' → '+fmt.n(p.cur_rank)
        : fmt.n(p.prev_value)+' → '+fmt.n(p.cur_value))+'</div>';
    c.addEventListener("click",function(){MD.go("card",p.key);}); c.style.cursor="pointer"; return c;
  }

  function renderMoverTable(holder, rep) {
    var rows=filteredRows(rep), total=rows.length;
    if (mstate.view!=="all" && !mstate.sort) rows=rows.slice(0,60);
    var wrap=fmt.el("div","movertable"), head=fmt.el("div","moverhead");
    [["cur_rank","Rank"],["name","Player"],["played","At comparison"],["cur_value","Value"],
     ["value_change","Δ value"],["value_change_pct","Δ%"],["rank_change","Δ rank"],["pos_rank_change","Δ pos"]]
      .forEach(function(c){var h=fmt.el("div","mh"+(c[0]==="name"?" l":" r"),c[1]);
        h.addEventListener("click",function(){if(mstate.sort===c[0])mstate.dir=mstate.dir==="desc"?"asc":"desc";
          else{mstate.sort=c[0];mstate.dir="desc";} renderMovers(holder);}); head.appendChild(h);});
    wrap.appendChild(head); var body=fmt.el("div","moverrows");
    rows.forEach(function(p){var r=fmt.el("div","moverrow"+(p.dnp?" dnp":"")); r.dataset.key=p.key;
      r.innerHTML='<div class="mr rank num">'+fmt.n(p.cur_rank)+'</div>'+
       '<div class="mr who"><span class="nm">'+fmt.esc(p.name)+'</span><span class="sub">'+fmt.esc(p.pos||"—")+' · '+fmt.esc(fmt.club(p.affl_team||"—"))+'</span></div>'+
       '<div class="mr pdn">'+(p.played===true?'<span class="pill up">PLAYED '+fmt.n(p.score)+'</span>':p.played===false?'<span class="pill na">DNP</span>':'<span class="pill na">BASELINE</span>')+'</div>'+
       '<div class="mr val num">'+fmt.n(p.cur_value)+'</div><div class="mr dv"><span class="pill '+fmt.cls(p.value_change)+'">'+fmt.signed(p.value_change)+'</span></div>'+
       '<div class="mr dvp num '+fmt.cls(p.value_change)+'">'+(p.value_change_pct==null?'—':(p.value_change_pct>0?'+':'')+p.value_change_pct.toFixed(1)+'%')+'</div>'+
       '<div class="mr dr"><span class="pill '+fmt.cls(p.rank_change)+'">'+fmt.signed(p.rank_change)+'</span></div>'+
       '<div class="mr dpr num '+fmt.cls(p.pos_rank_change)+'">'+fmt.signed(p.pos_rank_change)+'</div>';
      r.addEventListener("click",function(){MD.go("card",p.key);}); body.appendChild(r);});
    wrap.appendChild(body); wrap.appendChild(fmt.el("div","movercount",fmt.n(rows.length)+' of '+fmt.n(total)+' shown · comparison R'+rep.comparisonRound));
    holder.appendChild(wrap);
  }

  function renderMovers(holder) {
    holder.innerHTML=""; MD.__moversHolder=holder;
    var b=bundle();
    if (!b || !moversCore) { fail(holder,"movers bundle or validator missing"); return; }
    var lin=moversCore.lineage(b,appIdentity());
    if (!lin.ok) { fail(holder,lin.why); return; }
    var h=buildHistory(), rounds=h.rounds;
    if (rounds.length<2) { holder.innerHTML='<div class="moversempty"><h1>No comparable rounds</h1></div>'; return; }
    if (mstate.comparison==null) mstate.comparison=rounds[rounds.length-1];
    if (mstate.base==null) mstate.base=rounds[rounds.length-2];
    if (mstate.base>=mstate.comparison) mstate.base=rounds[Math.max(0,rounds.indexOf(mstate.comparison)-1)];
    var rep=comparison(mstate.base,mstate.comparison);

    var bar=fmt.el("div","strip moversbar comparebar");
    bar.appendChild(fmt.el("span","lbl","Compare rounds"));
    var bp=selectBox(rounds,mstate.base,"Base",function(r){return r<mstate.comparison;});
    bp.select.classList.add("moverBaseRound");
    bp.select.addEventListener("change",function(){mstate.base=parseInt(bp.select.value,10);mstate.sort=null;renderMovers(holder);});
    bar.appendChild(bp.wrap);
    var cp=selectBox(rounds,mstate.comparison,"Comparison",function(r){return r>mstate.base;});
    cp.select.classList.add("moverComparisonRound");
    cp.select.addEventListener("change",function(){mstate.comparison=parseInt(cp.select.value,10);mstate.sort=null;renderMovers(holder);});
    bar.appendChild(cp.wrap);
    var seg=fmt.el("div","seg");
    [["value_risers","Value risers"],["value_fallers","Value fallers"],["rank_risers","Rank risers"],["rank_fallers","Rank fallers"],["all","All players"]]
      .forEach(function(d){var x=fmt.el("button",mstate.view===d[0]?"on":"",d[1]);x.addEventListener("click",function(){mstate.view=d[0];mstate.sort=null;renderMovers(holder);});seg.appendChild(x);});
    bar.appendChild(seg); holder.appendChild(bar);

    var meta=fmt.el("div","strip moversmeta");
    meta.innerHTML='<span class="lbl">Period</span><b class="num">R'+mstate.base+' → R'+mstate.comparison+'</b><span class="lbl">players</span><b class="num">'+fmt.n(rep.players.length)+'</b>'+
      '<span class="lbl">board</span><b class="num">'+fmt.esc(String(rep.baseBoard||"").slice(0,8))+' → '+fmt.esc(String(rep.comparisonBoard||"").slice(0,8))+'</b>';
    holder.appendChild(meta);
    var cards=fmt.el("div","movercards");
    cards.appendChild(moverCard("Largest value increase",top(rep.players,"value_change","desc"),"value_change"));
    cards.appendChild(moverCard("Largest value decrease",top(rep.players,"value_change","asc"),"value_change"));
    cards.appendChild(moverCard("Largest rank improvement",top(rep.players,"rank_change","desc"),"rank_change"));
    cards.appendChild(moverCard("Largest rank decline",top(rep.players,"rank_change","asc"),"rank_change"));
    holder.appendChild(cards);

    var filters=fmt.el("div","strip moversfilters"); filters.appendChild(fmt.el("span","lbl","Filter"));
    var clubs={}; rep.players.forEach(function(p){if(p.affl_team)clubs[teamName(p.affl_team)]=1;});
    var cs=fmt.el("select","boardsel moverClubFilter");cs.appendChild(new Option("All clubs",""));Object.keys(clubs).sort().forEach(function(c){var o=new Option(fmt.club(c),c);if(c===mstate.club)o.selected=true;cs.appendChild(o);});
    cs.addEventListener("change",function(){mstate.club=cs.value||null;renderMovers(holder);});filters.appendChild(cs);
    var poss={};rep.players.forEach(function(p){if(p.pos)poss[p.pos]=1;});var ps=fmt.el("select","boardsel");ps.appendChild(new Option("All positions",""));Object.keys(poss).sort().forEach(function(p){var o=new Option(p,p);if(p===mstate.pos)o.selected=true;ps.appendChild(o);});
    ps.addEventListener("change",function(){mstate.pos=ps.value||null;renderMovers(holder);});filters.appendChild(ps);
    var status=fmt.el("div","seg");[["","All"],["played","Played comparison"],["dnp","DNP comparison"]].forEach(function(d){var x=fmt.el("button",(mstate.status||"")===d[0]?"on":"",d[1]);x.addEventListener("click",function(){mstate.status=d[0]||null;renderMovers(holder);});status.appendChild(x);});filters.appendChild(status);holder.appendChild(filters);
    renderMoverTable(holder,rep);
  }

  MD.movers = { render: renderMovers, core: moversCore, _state: mstate };

  function weeklyPanel(key) {
    var h=buildHistory(), rows=[], prev=null;
    h.rounds.forEach(function(r){var p=h.states[r]&&h.states[r][key];if(!p)return;rows.push({round:r,value:p.value,rank:p.rank,pos_rank:p.pos_rank,
      dv:prev? p.value-prev.value:null, dr:prev&&p.rank!=null&&prev.rank!=null?prev.rank-p.rank:null,
      dp:prev&&p.pos_rank!=null&&prev.pos_rank!=null?prev.pos_rank-p.pos_rank:null});prev=p;});
    if (!rows.length) return '<div class="reserved">No committed weekly history for this player.</div>';
    return '<div class="roundhistory"><div class="rhhead"><span>Round</span><span>Value</span><span>Δ value</span><span>Overall rank</span><span>Δ rank</span><span>Pos rank</span></div>'+
      rows.map(function(r){return '<div class="rhrow'+(r.round===h.rounds[h.rounds.length-1]?' latest':'')+'"><span class="num">R'+r.round+'</span><span class="num">'+fmt.n(r.value)+'</span><span class="num '+fmt.cls(r.dv)+'">'+fmt.signed(r.dv)+'</span><span class="num">'+fmt.n(r.rank)+'</span><span class="num '+fmt.cls(r.dr)+'">'+fmt.signed(r.dr)+'</span><span class="num">'+fmt.n(r.pos_rank)+'</span></div>';}).join('')+'</div>';
  }

  if (originalCardRender) MD.card.render=function(container){
    originalCardRender(container);
    var card=container.querySelector('.card'), body=card&&card.querySelector('.body');
    if(!body)return;
    var headings=body.querySelectorAll('h2.sec'), target=null;
    for(var i=0;i<headings.length;i++)if(headings[i].textContent.toLowerCase().indexOf('round-by-round rating')>=0){target=headings[i];break;}
    if(target){var meta=target.querySelector('.meta');if(meta)meta.textContent='committed R14–R19 history';var next=target.nextElementSibling;if(next)next.outerHTML=weeklyPanel(MD.state.cardKey);}
    else {body.insertAdjacentHTML('beforeend','<h2 class="sec"><span>Round-by-round rating</span><span class="meta">committed history</span></h2>'+weeklyPanel(MD.state.cardKey));}
  };
})();
