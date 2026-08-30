/* THE OWNER'S CONSTRAINT, CHECKED: "as long as it doesn't impact the movers list still being
   accurate as of each round since round 14."  Compares the shipped bundle against the baseline
   taken before the act, and reports on the two things that could go wrong.  */
var fs = require('fs');
function P(p){var g={window:{}};(new Function('window',fs.readFileSync(p,'utf8')))(g.window);return g.window.__MATCHDAY_MOVERS__;}
var base = P(process.argv[2]), now = P(process.argv[3]);
var fail = 0;
function ok(c,l){ console.log((c?'  [PASS] ':'  [FAIL] ')+l); if(!c) fail++; }

ok(JSON.stringify(base.rounds)===JSON.stringify(now.rounds),
   'the round series is unchanged: '+JSON.stringify(now.rounds));
var moved = base.rounds.filter(function(r){
  return JSON.stringify(base.reports[String(r)])!==JSON.stringify(now.reports[String(r)]); });
ok(moved.length===0, 'every per-round report R'+base.rounds[0]+'-R'+base.rounds[base.rounds.length-1]+
   ' is byte-identical'+(moved.length?' (MOVED: '+moved+')':''));

function retro(x){return (x.points||[]).filter(function(p){return p.kind==='retro';});}
ok(retro(now).length===retro(base).length,
   'the retrospective series is still '+retro(base).length+' points (got '+retro(now).length+')');
ok(JSON.stringify(retro(now))===JSON.stringify(retro(base)),
   'every retro point R14-R24 is byte-identical to before the act');

/* per-player retro readings, not just the point headers */
var vb=base.values||{}, vn=now.values||{}, bad=0, checked=0;
Object.keys(vb).forEach(function(k){
  var a=(vb[k]||{}).byPoint||{}, b=(vn[k]||{}).byPoint||{};
  Object.keys(a).filter(function(id){return id.indexOf('retro-r')===0;}).forEach(function(id){
    checked++; if(JSON.stringify(a[id])!==JSON.stringify(b[id])) bad++; });
});
ok(bad===0, 'every banked retro reading is unchanged ('+checked+' player-round values checked, '+bad+' moved)');

var newPts=now.points.filter(function(p){return !base.points.some(function(q){return q.id===p.id;});});
console.log('  [info] new point(s) this act: '+(newPts.map(function(p){return p.id;}).join(', ')||'none'));
console.log(fail?('MOVERS HISTORY: '+fail+' FAIL'):'MOVERS HISTORY: ALL PASS');
process.exit(fail?1:0);
