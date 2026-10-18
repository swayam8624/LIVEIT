import { strict as assert } from 'node:assert';
import { mkdir } from 'node:fs/promises';
import { chromium } from 'playwright';

await mkdir('artifacts/appearance-life', { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  for (const width of [390, 1440]) {
    const page = await browser.newPage({
      viewport: { width, height: width < 500 ? 844 : 900 },
    });
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto('http://127.0.0.1:8081/', {
      waitUntil: 'networkidle',
      timeout: 60000,
    });
    await page
      .getByRole('textbox', { name: 'Character name' })
      .waitFor({ timeout: 30000 });
    await page.getByRole('tab', { name: 'Skin tone' }).click();
    await page.getByRole('radio', { name: 'Skin tone: espresso' }).click();
    await page.getByRole('tab', { name: 'Hairstyle' }).click();
    await page.getByRole('radio', { name: 'Hairstyle: afro' }).click();
    await page.getByRole('tab', { name: 'Clothing style' }).click();
    await page.getByRole('radio', { name: 'Clothing style: formal' }).click();
    await page.screenshot({
      path: `artifacts/appearance-life/creator-${width}.png`,
      fullPage: true,
    });
    await page.getByRole('button', { name: 'Begin your life' }).click();
    await page
      .getByRole('button', { name: 'Age up one year' })
      .waitFor({ timeout: 16000 });
    await page.getByRole('button', { name: 'Age up one year' }).click();
    await page.getByText(/Age 24: a year passes/).waitFor({ timeout: 10000 });
    await page.screenshot({
      path: `artifacts/appearance-life/life-aged-${width}.png`,
      fullPage: true,
    });
    await page.getByRole('tab', { name: 'PEOPLE' }).click();
    await page.getByRole('button', { name: /Customize my look/ }).click();
    await page.getByRole('tab', { name: 'Accessories' }).click();
    await page.getByRole('radio', { name: 'Accessories: glasses' }).click();
    await page.getByRole('button', { name: 'Save appearance' }).click();
    await page.reload({ waitUntil: 'networkidle' });
    await page.getByRole('tab', { name: 'PEOPLE' }).click();
    await page.getByRole('button', { name: /Customize my look/ }).click();
    await page.getByRole('tab', { name: 'Accessories' }).click();
    assert.equal(
      await page
        .getByRole('radio', { name: 'Accessories: glasses' })
        .getByText('✓')
        .count(),
      1,
    );
    await page.getByRole('button', { name: 'Close appearance editor' }).click();
    await page.getByRole('tab', { name: 'FREE LIFE' }).click();
    await page.getByRole('button', { name: 'Search available jobs' }).click();
    await page.getByRole('button', { name: 'Apply for Community' }).click();
    await page.getByRole('button', { name: 'Attend job interview' }).click();
    await page
      .getByRole('button', { name: 'Request promotion' })
      .waitFor({ timeout: 10000 });
    await page.screenshot({
      path: `artifacts/appearance-life/career-${width}.png`,
      fullPage: true,
    });
    assert.deepEqual(errors, [], errors.join('; '));
    await page.close();
  }
} finally {
  await browser.close();
}
