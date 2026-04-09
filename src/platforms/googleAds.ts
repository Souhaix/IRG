import { Page } from 'playwright';
import { AccountConfig, DateContext, SpendResult } from '../types/index.js';
import { UncertainStateError } from '../utils/errors.js';
import { logStep } from '../utils/logger.js';
import { makeSpendResult, readSpendTextBySelectors } from './common.js';

const selectors = {
  dateRangeButton: 'button:has-text("Date range"), [aria-label*="Date range"]',
  yesterdayOption: 'text=Yesterday',
  applyButton: 'button:has-text("Apply")',
  costMetric: [
    '[aria-label="Cost"] .metric-value',
    'div:has-text("Cost") >> xpath=following::*[contains(@class,"value")][1]',
    'span:has-text("$")',
  ],
};

async function applyYesterday(page: Page, dateContext: DateContext): Promise<void> {
  const trigger = page.locator(selectors.dateRangeButton).first();
  if (!(await trigger.isVisible().catch(() => false))) {
    throw new UncertainStateError('Google Ads date range control missing.', {
      module: 'platform/googleAds',
      action: 'findDateRange',
      url: page.url(),
    });
  }
  await trigger.click();
  await page.locator(selectors.yesterdayOption).first().click();
  const apply = page.locator(selectors.applyButton).first();
  if (await apply.isVisible().catch(() => false)) {
    await apply.click();
  }
  logStep('google.date.applied', { date: dateContext.isoDate });
}

async function collectSingle(page: Page, account: AccountConfig, dateContext: DateContext): Promise<SpendResult> {
  let refreshUsed = false;
  for (;;) {
    await page.goto(account.accountUrl, { waitUntil: 'domcontentloaded' });
    try {
      await applyYesterday(page, dateContext);
      const candidate = page.locator(selectors.costMetric[0]).first();
      if (await candidate.isVisible().catch(() => false)) {
        await candidate.hover().catch(() => undefined);
      }
      const raw = await readSpendTextBySelectors(page, selectors.costMetric, 12_000);
      return makeSpendResult(account, raw, `Yesterday (${dateContext.isoDate})`);
    } catch (error) {
      if (!refreshUsed) {
        refreshUsed = true;
        logStep('google.refresh.retry', { account: account.accountName });
        await page.reload({ waitUntil: 'domcontentloaded' });
        continue;
      }
      throw new UncertainStateError('Google Ads account failed after 1 refresh retry.', {
        module: 'platform/googleAds',
        action: 'collectSingle',
        url: page.url(),
        detail: { account: account.accountName, originalError: String(error) },
      });
    }
  }
}

export async function collectGoogleAdsSpend(
  page: Page,
  accounts: AccountConfig[],
  dateContext: DateContext,
): Promise<SpendResult[]> {
  const out: SpendResult[] = [];
  for (const account of accounts) {
    out.push(await collectSingle(page, account, dateContext));
  }
  return out;
}

export const googleSelectorTest = {
  platform: 'GoogleAds',
  selectors,
};
