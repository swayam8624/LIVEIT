/**
 * Automated LIVEIT browser visual smoke review.
 *
 * Run after launching Expo web on port 8081 and Creator Studio on port 3000.
 * Screenshots are REVIEW ARTIFACTS, not proof of artistic quality or native QA.
 */
import { strict as assert } from 'node:assert';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const out = path.resolve('artifacts/visual-smoke');
await mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless: true });

async function inspect(label, viewport) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('http://127.0.0.1:8081/', { waitUntil: 'networkidle', timeout: 60000 });
  const character = page.getByRole('textbox', { name: 'Character name' });
  await character.waitFor({ timeout: 25000 });
  await page.screenshot({ path: path.join(out, `onboard-${label}.png`), fullPage: true });
  await character.fill('Alex Morgan');
  await page.getByRole('button', { name: /Begin your life/i }).click();
  await page.getByRole('button', { name: /THE CAFÉ/ }).waitFor({ timeout: 15000 });
  await page.screenshot({ path: path.join(out, `free-life-${label}.png`), fullPage: true });
  for (let day = 0; day < 3; day++) {
    await page.getByRole('button', { name: /STUDY/ }).click();
  }
  await page.getByText('1 waiting').waitFor({ timeout: 12000 });
  await page.getByText('At a crossroads.').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(out, `city-decision-${label}.png`), fullPage: true });
  const decision = page.getByRole('button', { name: /Take the workshop|Find its owner|Help, even if it takes the evening/ });
  await decision.first().click();
  await page.getByText('0 waiting').waitFor({ timeout: 12000 });
  await page.getByText('At a crossroads.').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(out, `city-after-choice-${label}.png`), fullPage: true });
  await page.getByRole('button', { name: /THE CAFÉ/ }).click();
  await page.getByText('The Space Between').first().waitFor({ timeout: 15000 });
  await page.screenshot({ path: path.join(out, `story-${label}.png`), fullPage: true });
  assert.equal(errors.length, 0, `Browser exception in ${label}: ${errors.join('; ')}`);
  await context.close();
}

try {
  await inspect('mobile-390', { width: 390, height: 844 });
  await inspect('desktop-1440', { width: 1440, height: 900 });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  await page.goto('http://localhost:3000/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.getByText('Creator Studio', { exact: false }).first().waitFor();
  await page.screenshot({ path: path.join(out, 'creator-studio-desktop.png'), fullPage: true });
  await page.waitForTimeout(900); // Allow Next.js client hydration before editing.
  // Verify that the studio calls the exact player narrative core rather than
  // merely hopping to a hard-coded destination node.
  assert.equal((await page.getByTestId('preview-trust').innerText()).trim(), '35/100');
  await page.getByRole('button', { name: /I should have called/i }).click();
  await page.getByTestId('preview-trust').getByText('47/100').waitFor();
  await page.getByRole('button', { name: /I was afraid I'd let you down/i }).click();
  await page.getByTestId('preview-trust').getByText('57/100').waitFor();
  assert.equal((await page.getByTestId('preview-memory-count').innerText()).trim(), '2');
  await page.getByRole('button', { name: /Restart/i }).click();
  await page.getByTestId('preview-trust').getByText('35/100').waitFor();

  await page.getByRole('button', { name: /New story/i }).click();
  await page.getByRole('heading', { name: 'Untitled story' }).waitFor({ timeout: 10000 });
  await page.getByRole('button', { name: '+5 trust' }).click();
  await page.getByRole('button', { name: '+ Memory' }).click();
  await page.getByRole('button', { name: 'See what happens' }).click();
  await page.getByTestId('preview-trust').getByText('40/100').waitFor();
  assert.equal((await page.getByTestId('preview-memory-count').innerText()).trim(), '1');
  await page.screenshot({ path: path.join(out, 'creator-studio-new-story.png'), fullPage: true });
  assert.equal(errs.length, 0, `Creator Studio browser exceptions: ${errs.join('; ')}`);
  await page.close();
  assert.ok(out.length > 0); // Captured screenshots are uploaded by the workflow.
} finally {
  await browser.close();
}
