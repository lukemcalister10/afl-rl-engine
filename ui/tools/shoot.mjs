// Screenshot driver for the Matchday UI. Node 22 built-ins only (global WebSocket + fetch).
// Drives headless Chromium over CDP: loads the app, applies a state-setup snippet, screenshots.
// NOT part of the shipped app; a dev/QA aid to produce the per-change screenshots. Reads only.
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL = process.argv[2];
const OUT = process.argv[3];
const SETUP = process.argv[4] || '';        // JS run after load, before capture (returns after render)
const W = parseInt(process.argv[5] || '1280', 10);
const H = parseInt(process.argv[6] || '2000', 10);
const PORT = 9333;

const proc = spawn(CHROME, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`, `--window-size=${W},${H}`,
  '--force-device-scale-factor=1', 'about:blank',
], { stdio: 'ignore' });

let ws;
try {
  let target;
  for (let i = 0; i < 50; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); const j = await r.json();
      target = j.find(t => t.type === 'page'); if (target) break; } catch {}
    await sleep(100);
  }
  if (!target) throw new Error('no CDP page target');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  let id = 0; const pend = new Map();
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
  const cmd = (method, params={}) => new Promise((res) => { const i = ++id;
    pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });

  await cmd('Page.enable'); await cmd('Runtime.enable');
  await cmd('Page.navigate', { url: URL });
  await sleep(900); // let scripts + DOMContentLoaded render
  if (SETUP) { await cmd('Runtime.evaluate', { expression: SETUP, awaitPromise: true }); await sleep(400); }
  // full-height capture
  const metrics = await cmd('Page.getLayoutMetrics');
  const h = Math.min(Math.ceil(metrics.result.cssContentSize?.height || H), 8000);
  await cmd('Emulation.setDeviceMetricsOverride', { width: W, height: h, deviceScaleFactor: 1, mobile: false });
  const shot = await cmd('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  const { writeFileSync } = await import('node:fs');
  writeFileSync(OUT, Buffer.from(shot.result.data, 'base64'));
  console.log('wrote', OUT, `(${W}x${h})`);
} finally {
  try { ws && ws.close(); } catch {}
  proc.kill('SIGKILL');
}
