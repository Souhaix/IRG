import { Page } from 'playwright';
import { AccountConfig, DateContext, SpendResult } from '../types/index.js';
import { UncertainStateError } from '../utils/errors.js';
import { makeSpendResult, readSpendTextBySelectors } from './common.js';

const selectors = {
  dateButton: '[aria-label*="Date"]',
  yesterdayOption: 'text=Yesterday',
  applyButton: 'button:has-text("Apply")',
  primarySpend: [
    '[data-testid="insights-card"]:has-text("Amount spent") [data-testid="value"]',
    '[aria-label*="Amount spent"]',
  ],
  fallbackOpenReports: 'a:has-text("Reports"), button:has-text("Reports")',
  fallbackSpend: [
    'table tr:has-text("Amount spent") td:last-child',
    'div:has-text("Amount spent") >> xpath=following::*[contains(text(),"$")][1]',
  ],
};

async function enforceYesterday(page: Page, dateContext: DateContext): Promise<void> {
  const trigger = page.locator(selectors.dateButton).first();
  if (!(await trigger.isVisible().catch(() => false))) {
    throw new UncertainStateError('Facebook date picker missing.', {
      module: 'platform/facebookAds',
      action: 'findDatePicker',
      url: page.url(),
    });
  }
  await trigger.click();
  await page.locator(selectors.yesterdayOption).first().click();
  const apply = page.locator(selectors.applyButton).first();
  if (await apply.isVisible().catch(() => false)) {
    await apply.click();
  }
  const dateMarker = await trigger.textContent();
  if (!dateMarker?.toLowerCase().includes('yesterday') && !dateMarker.includes(dateContext.isoDate)) {
    throw new UncertainStateError('Facebook date verification failed for yesterday.', {
      module: 'platform/facebookAds',
      action: 'verifyDate',
      url: page.url(),
      detail: { dateMarker, expected: dateContext.isoDate },
    });
  }
}

async function readWithPrimaryThenFallback(page: Page): Promise<string> {
  try {
    return await readSpendTextBySelectors(page, selectors.primarySpend, 10_000);
  } catch {
    const reports = page.locator(selectors.fallbackOpenReports).first();
    if (await reports.isVisible().catch(() => false)) {
      await reports.click();
    }
    return await readSpendTextBySelectors(page, selectors.fallbackSpend, 10_000);
  }
}

async function collectSingle(page: Page, account: AccountConfig, dateContext: DateContext): Promise<SpendResult> {
  await page.goto(account.accountUrl, { waitUntil: 'domcontentloaded' });
  await enforceYesterday(page, dateContext);
  const raw = await readWithPrimaryThenFallback(page);
  return makeSpendResult(account, raw, `Yesterday (${dateContext.isoDate})`);
}

export async function collectFacebookAdsSpend(
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

export const facebookSelectorTest = {
  platform: 'FacebookAds',
  selectors,
};
