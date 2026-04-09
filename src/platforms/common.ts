import { Page } from 'playwright';
import { AccountConfig, SpendResult } from '../types/index.js';
import { parseMoney } from '../utils/normalize.js';
import { UncertainStateError } from '../utils/errors.js';
import { logStep } from '../utils/logger.js';

export async function readSpendTextBySelectors(
  page: Page,
  selectors: string[],
  timeoutMs: number,
): Promise<string> {
  for (const selector of selectors) {
    const node = page.locator(selector).first();
    if (await node.isVisible({ timeout: timeoutMs }).catch(() => false)) {
      const value = (await node.textContent())?.trim();
      if (value) {
        return value;
      }
    }
  }
  throw new UncertainStateError('No spend selector matched visible value.', {
    module: 'platform/common',
    action: 'readSpendTextBySelectors',
    url: page.url(),
    detail: { selectors },
  });
}

export function makeSpendResult(account: AccountConfig, rawMoney: string, observedDateText?: string): SpendResult {
  const parsed = parseMoney(rawMoney);
  logStep('spend.parsed', {
    platform: account.platform,
    brand: account.brand,
    account: account.accountName,
    rawMoney,
    parsed,
  });
  return {
    brand: account.brand,
    platform: account.platform,
    accountName: account.accountName,
    amount: parsed.amount,
    currency: parsed.currency,
    sourceUrl: account.accountUrl,
    observedDateText,
  };
}

export function sumResults(results: SpendResult[]): number {
  return Number(results.reduce((sum, r) => sum + r.amount, 0).toFixed(2));
}
