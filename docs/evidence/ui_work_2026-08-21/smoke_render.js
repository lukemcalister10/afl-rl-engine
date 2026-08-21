/* Smoke render: load every shipped app file into a hand-rolled DOM and render each view.
   Purpose is only to catch reference errors / throws in the real render paths. Not a test of output. */
const fs = require("fs"), path = require("path"), vm = require("vm");
const UI = path.join(__dirname, "..", "..", "..", "..", "..", "home", "user", "afl-rl-engine", "ui");
const ROOT = "/home/user/afl-rl-engine/ui";

function El(tag) {
  this.tagName = tag; this.className = ""; this.style = {}; this.title = ""; this.disabled = false;
  this.children = []; this.innerHTML = ""; this.textContent = ""; this.value = "";
  this.attrs = {}; this._listeners = {};
  this.classList = {
    _s: {},
    add: (c) => { this.className = (this.className + " " + c).trim(); },
    remove: () => {}, contains: (c) => this.className.indexOf(c) >= 0,
  };
}
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
El.prototype.addEventListener = function (k, f) { (this._listeners[k] = this._listeners[k] || []).push(f); };
El.prototype.removeEventListener = function () {};
El.prototype.setAttribute = function (k, v) { this.attrs[k] = v; };
El.prototype.getAttribute = function (k) { return this.attrs[k]; };
El.prototype.querySelector = function () { return null; };
El.prototype.querySelectorAll = function () { return []; };
El.prototype.focus = function () {};
Object.defineProperty(El.prototype, "firstChild", { get: function () { return this.children[0] || null; } });

const sandbox = {
  console, Math, JSON, Object, Array, String, Number, Date, RegExp, isFinite, isNaN,
  parseInt, parseFloat, setTimeout: () => {}, clearTimeout: () => {}, Error, Promise,
};
sandbox.window = sandbox;
sandbox.Option = function (label, value) { const e = new El("option"); e.textContent = label; e.value = value; return e; };
sandbox.document = {
  readyState: "loading",
  addEventListener: () => {},
  getElementById: () => new El("div"),
  createElement: (t) => new El(t),
  body: new El("body"),
  documentElement: new El("html"),
};
sandbox.location = { hash: "", href: "file:///x" };
sandbox.history = { pushState: () => {}, replaceState: () => {} };
sandbox.requestAnimationFrame = (f) => f();
sandbox.navigator = { userAgent: "node" };
vm.createContext(sandbox);

function run(rel) {
  const p = path.join(ROOT, rel);
  vm.runInContext(fs.readFileSync(p, "utf8"), sandbox, { filename: rel });
}

const DATA = [
  "data/board_view_working.js", "data/board_view_public.js", "data/club_valuation.js",
  "data/ownership.js", "app/positions_data.js", "data_aux/v0.js",
  "data/movers.js", "data/movers_transition.js",
];
const APP = ["app/config.js", "app/format.js", "app/counting.js", "app/seam.js", "app/ownership.js",
  "app/v0.js", "app/club_totals.js", "app/history.js", "app/pocket.js", "app/board.js",
  "app/clubs.js", "app/card.js", "app/trade.js", "app/movers.js", "app/main.js"];

let bad = 0;
for (const f of DATA.concat(APP)) {
  try { run(f); } catch (e) { bad++; console.log("LOAD FAIL " + f + " :: " + e.message); }
}
if (bad) process.exit(1);
console.log("all files loaded");

const MD = sandbox.MD;
function render(name, fn) {
  const holder = new El("div");
  try { fn(holder); console.log("  render OK   " + name); }
  catch (e) { bad++; console.log("  render FAIL " + name + " :: " + e.message + "\n" + (e.stack || "").split("\n").slice(1, 4).join("\n")); }
}

console.log("ring-fence: " + JSON.stringify(MD.seam.ringFence()));
console.log("v0 status: " + JSON.stringify(MD.v0.status()));

MD.state.tier = "working"; MD.state.lens = 2;
render("board (working, default)", (h) => MD.board.render(h));
MD.state.lens = 3;
render("board (working, lens forced to +1 — must clamp)", (h) => MD.board.render(h));
console.log("    lens after clamp = " + MD.state.lens);
MD.board.restore({ cohortFilter: "2024", ageFilter: "b:-20", eligFilter: "KPF", v0Col: true });
render("board (working, cohort+age+elig+v0 column)", (h) => MD.board.render(h));
MD.board.restore({ cohortFilter: null, ageFilter: null, eligFilter: null, v0Col: false });
MD.state.tier = "public";
render("board (public)", (h) => MD.board.render(h));

MD.state.tier = "working";
const someKey = MD.seam.working.players[0].key;
MD.state.cardKey = someKey;
render("card (working) " + someKey, (h) => MD.card.render(h));
MD.state.tier = "public";
render("card (public) " + someKey, (h) => MD.card.render(h));
MD.state.tier = "working";

render("trade", (h) => MD.trade.render(h));
render("clubs", (h) => MD.clubs.render(h));
render("movers", (h) => MD.movers.render(h));
console.log("movers state after render: " + JSON.stringify(MD.movers._state ? { from: MD.movers._state.from, to: MD.movers._state.to } : "n/a"));

process.exit(bad ? 1 : 0);
