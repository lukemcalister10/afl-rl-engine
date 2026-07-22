const { chromium, devices } = require('playwright');

function assert(ok, msg) { if (!ok) throw new Error(msg); }

const profiles = [
  { name: 'desktop', options: { viewport: { width: 1366, height: 900 } } },
  { name: 'mobile', options: { ...devices['iPhone 12'] } },
];

(async () => {
  for (const profile of profiles) {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext(profile.options);
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle' });
    await page.locator('.row.working').first().waitFor({ state: 'attached', timeout: 15000 });

    const tabs = (await page.locator('.tabs button').allTextContents()).map(x => x.trim().toUpperCase());
    assert(!tabs.includes('ROUND REVIEW'), profile.name + ': redundant Round Review tab remains');
    assert(tabs.includes('MOVERS'), profile.name + ': Movers tab missing');

    const teamFacts = await page.evaluate(() => {
      const ps = window.__MATCHDAY_WORKING__.players;
      const stocker = ps.find(p => p.key === 'liam-stocker');
      const brockman = ps.find(p => p.key === 'tyler-brockman');
      const variants = [...new Set(ps.map(p => p.affl_team).filter(x => String(x).toLowerCase() === 'free agents'))];
      return { stocker: stocker && stocker.affl_team, brockman: brockman && brockman.affl_team, variants };
    });
    assert(teamFacts.stocker === 'Free agents', profile.name + ': Stocker category ' + teamFacts.stocker);
    assert(teamFacts.brockman === 'Free agents', profile.name + ': Brockman category ' + teamFacts.brockman);
    assert(teamFacts.variants.length === 1 && teamFacts.variants[0] === 'Free agents', profile.name + ': duplicate free-agent categories');

    const teamSelect = page.locator('select.boardsel').nth(1);
    const freeOptions = (await teamSelect.locator('option').allTextContents()).filter(x => x.toLowerCase() === 'free agents');
    assert(freeOptions.length === 1, profile.name + ': board filter shows ' + freeOptions.length + ' Free agents options');

    await page.getByRole('button', { name: 'Movers', exact: true }).click();
    await page.locator('.moverBaseRound').waitFor({ state: 'visible', timeout: 10000 });
    const baseOptions = await page.locator('.moverBaseRound option').allTextContents();
    const compareOptions = await page.locator('.moverComparisonRound option').allTextContents();
    assert(baseOptions.includes('Round 14'), profile.name + ': base R14 absent');
    assert(compareOptions.includes('Round 19'), profile.name + ': comparison R19 absent');

    await page.locator('.moverBaseRound').selectOption('14');
    await page.locator('.moverComparisonRound').selectOption('19');
    await page.waitForFunction(() => document.body.innerText.includes('R14 → R19'));
    const comparison = await page.evaluate(() => {
      const x = MD.compareRounds(14, 19);
      const p = x.players.find(r => r.key === 'phoenix-gothard');
      return { n: x.players.length, p, base: x.baseRound, comparison: x.comparisonRound };
    });
    assert(comparison.n === 804, profile.name + ': arbitrary comparison coverage ' + comparison.n);
    assert(comparison.base === 14 && comparison.comparison === 19, profile.name + ': wrong comparison rounds');
    assert(comparison.p.value_change === comparison.p.cur_value - comparison.p.prev_value,
      profile.name + ': comparison arithmetic mismatch');

    await page.evaluate(() => MD.go('review'));
    await page.locator('.moverBaseRound').waitFor({ state: 'visible', timeout: 10000 });
    assert((await page.getByRole('button', { name: 'Movers', exact: true }).getAttribute('class') || '').split(/\s+/).includes('on'),
      profile.name + ': stale review route did not resolve to Movers');

    await page.evaluate(() => MD.go('card', 'phoenix-gothard'));
    await page.locator('.roundhistory .rhrow').first().waitFor({ state: 'visible', timeout: 10000 });
    const historyRows = await page.locator('.roundhistory .rhrow').allTextContents();
    assert(historyRows.length === 6, profile.name + ': player history rows ' + historyRows.length);
    assert(historyRows[0].includes('R14') && historyRows[5].includes('R19'), profile.name + ': card history not R14-R19');

    await page.getByRole('button', { name: 'Clubs', exact: true }).click();
    assert(await page.locator('.ctable tbody tr').count() === 16, profile.name + ': club table regressed');

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    assert(!overflow, profile.name + ': horizontal document overflow');
    assert(errors.length === 0, profile.name + ': page errors: ' + errors.join(' | '));
    await browser.close();
  }
  console.log('R19 CANDIDATE UI PASS');
})().catch(err => { console.error(err); process.exit(1); });
