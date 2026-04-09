import { launchPersistentContext, newPage } from './utils/browser.js';
import { workflowConfig } from './config/accounts.js';
import { tiktokSelectorTest } from './platforms/tiktok.js';
import { googleSelectorTest } from './platforms/googleAds.js';
import { facebookSelectorTest } from './platforms/facebookAds.js';
import { microsoftSelectorTest } from './platforms/microsoftAds.js';
import { logger } from './utils/logger.js';

interface SelectorSuite {
  platform: string;
  url: string;
  selectors: Record<string, string | string[]>;
}

function flattenSelectors(record: Record<string, string | string[]>): string[] {
  return Object.values(record).flatMap((value) => (Array.isArray(value) ? value : [value]));
}

async function testSelectors(page: Awaited<ReturnType<typeof newPage>>, suite: SelectorSuite): Promise<void> {
  await page.goto(suite.url, { waitUntil: 'domcontentloaded' });
  for (const selector of flattenSelectors(suite.selectors)) {
    const visible = await page.locator(selector).first().isVisible().catch(() => false);
    logger.info({ platform: suite.platform, selector, visible }, 'Selector check');
  }
}

async function main(): Promise<void> {
  const context = await launchPersistentContext();
  const page = await newPage(context);

  const suites: SelectorSuite[] = [
    { platform: tiktokSelectorTest.platform, selectors: tiktokSelectorTest.selectors, url: workflowConfig.accounts.tiktok[0].accountUrl },
    { platform: googleSelectorTest.platform, selectors: googleSelectorTest.selectors, url: workflowConfig.accounts.googleAds[0].accountUrl },
    { platform: facebookSelectorTest.platform, selectors: facebookSelectorTest.selectors, url: workflowConfig.accounts.facebookAds[0].accountUrl },
    { platform: microsoftSelectorTest.platform, selectors: microsoftSelectorTest.selectors, url: workflowConfig.accounts.microsoftAds[0].accountUrl },
  ];

  for (const suite of suites) {
    await testSelectors(page, suite);
  }

  await context.close();
}

main().catch((err) => {
  logger.error({ err }, 'Selector test failed');
  process.exit(1);
});
