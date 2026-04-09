import { Page } from 'playwright';
import { AccountConfig, DateContext, SpendResult } from '../types/index.js';
import { UncertainStateError } from '../utils/errors.js';
import { logStep } from '../utils/logger.js';
import { makeSpendResult, readSpendTextBySelectors } from './common.js';

const selectors = {
  dateButton: '[data-testid="date-picker-trigger"], button:has-text("Yesterday")',
  yesterdayPreset: 'text=Yesterday',
  totalRow: 'tr:has-text("Total of")',
  totalCostCells: [
    'tr:has-text("Total of") td:has-text("$")',
    'tr:has-text("Total of") td:nth-last-child(2)',
  ],
};

export async function collectTikTokSpend(page: Page, account: AccountConfig, dateContext: DateContext): Promise<SpendResult> {
  await page.goto(account.accountUrl, { waitUntil: 'domcontentloaded' });
  logStep('tiktok.opened', { account: account.accountName, url: page.url() });

  const dateTrigger = page.locator(selectors.dateButton).first();
  if (!(await dateTrigger.isVisible().catch(() => false))) {
    throw new UncertainStateError('TikTok date picker trigger not visible.', {
      module: 'platform/tiktok',
      action: 'verifyDateControl',
      url: page.url(),
    });
  }

  await dateTrigger.click();
  await page.locator(selectors.yesterdayPreset).first().click();

  const totalRow = page.locator(selectors.totalRow).first();
  if (!(await totalRow.isVisible().catch(() => false))) {
    throw new UncertainStateError('TikTok total campaigns row missing.', {
      module: 'platform/tiktok',
      action: 'findTotalRow',
      url: page.url(),
    });
  }

  const rawMoney = await readSpendTextBySelectors(page, selectors.totalCostCells, 10_000);
  return makeSpendResult(account, rawMoney, `Yesterday (${dateContext.isoDate})`);
}

export const tiktokSelectorTest = {
  platform: 'TikTok',
  selectors,
};
