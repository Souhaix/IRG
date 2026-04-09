import { Page } from 'playwright';
import { AccountConfig, DateContext, SpendResult } from '../types/index.js';
import { UncertainStateError } from '../utils/errors.js';
import { makeSpendResult, readSpendTextBySelectors } from './common.js';
import { logStep } from '../utils/logger.js';

const selectors = {
  dateControl: '[aria-label*="Date range"], button:has-text("Yesterday")',
  yesterdayOption: 'text=Yesterday',
  reconnectIndicator: 'text=Sign in, text=Session expired',
  reconnectButton: 'button:has-text("Sign in"), a:has-text("Sign in")',
  brandRowValue: [
    'tr:has-text("Vosker Security") td:has-text("$")',
    'tr:has-text("SPYPOINT") td:has-text("$")',
    'table tr td:has-text("$")',
  ],
};

async function applyYesterday(page: Page): Promise<void> {
  const control = page.locator(selectors.dateControl).first();
  if (await control.isVisible().catch(() => false)) {
    await control.click();
    const yesterday = page.locator(selectors.yesterdayOption).first();
    if (await yesterday.isVisible().catch(() => false)) {
      await yesterday.click();
    }
  }
}

async function reconnectIfNeeded(page: Page, reconnectUsed: boolean): Promise<boolean> {
  const expired = await page.locator(selectors.reconnectIndicator).first().isVisible().catch(() => false);
  if (!expired) return reconnectUsed;
  if (reconnectUsed) {
    throw new UncertainStateError('Microsoft Ads session expired after reconnect attempt already used.', {
      module: 'platform/microsoftAds',
      action: 'reconnectIfNeeded',
      url: page.url(),
    });
  }
  const reconnect = page.locator(selectors.reconnectButton).first();
  if (!(await reconnect.isVisible().catch(() => false))) {
    throw new UncertainStateError('Microsoft Ads reconnect UI not found.', {
      module: 'platform/microsoftAds',
      action: 'reconnectMissing',
      url: page.url(),
    });
  }
  await reconnect.click();
  logStep('microsoft.reconnect.used');
  await page.waitForLoadState('domcontentloaded');
  return true;
}

async function collectSingle(
  page: Page,
  account: AccountConfig,
  dateContext: DateContext,
  reconnectUsed: boolean,
): Promise<{ result: SpendResult; reconnectUsed: boolean }> {
  await page.goto(account.accountUrl, { waitUntil: 'domcontentloaded' });
  const newReconnectUsed = await reconnectIfNeeded(page, reconnectUsed);
  await applyYesterday(page);
  const rowSelector = [`tr:has-text("${account.accountName}") td:has-text("$")`, ...selectors.brandRowValue];
  const raw = await readSpendTextBySelectors(page, rowSelector, 12_000);
  const result = makeSpendResult(account, raw, `Yesterday (${dateContext.isoDate})`);
  return { result, reconnectUsed: newReconnectUsed };
}

export async function collectMicrosoftAdsSpend(
  page: Page,
  accounts: AccountConfig[],
  dateContext: DateContext,
): Promise<SpendResult[]> {
  const out: SpendResult[] = [];
  let reconnectUsed = false;
  for (const account of accounts) {
    const collected = await collectSingle(page, account, dateContext, reconnectUsed);
    reconnectUsed = collected.reconnectUsed;
    out.push(collected.result);
  }
  return out;
}

export const microsoftSelectorTest = {
  platform: 'MicrosoftAds',
  selectors,
};
