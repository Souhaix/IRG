import { Page } from 'playwright';
import { WorkflowTotals, DateContext } from '../types/index.js';
import { workflowConfig } from '../config/accounts.js';
import { UncertainStateError } from '../utils/errors.js';
import { logStep } from '../utils/logger.js';

function resolveSheetName(pattern: string, dateContext: DateContext): string {
  return pattern.replace('[MON]', dateContext.uiMonthShort).replace('[YEAR]', dateContext.uiYear);
}

async function openSheet(page: Page, sheetName: string): Promise<void> {
  const tab = page.locator(`button:has-text("${sheetName}")`).first();
  if (!(await tab.isVisible().catch(() => false))) {
    throw new UncertainStateError('SharePoint month tab not found.', {
      module: 'sharepoint/writer',
      action: 'openSheet',
      url: page.url(),
      detail: { sheetName },
    });
  }
  await tab.click();
}

async function findDateColumnByRow(page: Page, dateRow: number, isoDate: string): Promise<number> {
  const cells = page.locator(`[data-row="${dateRow}"] [role="gridcell"]`);
  const count = await cells.count();
  for (let i = 0; i < count; i += 1) {
    const text = (await cells.nth(i).textContent())?.trim();
    if (text?.includes(isoDate) || text?.includes(isoDate.slice(-2))) {
      return i + 1;
    }
  }
  throw new UncertainStateError('SharePoint target date column not found in expected date row.', {
    module: 'sharepoint/writer',
    action: 'findDateColumnByRow',
    url: page.url(),
    detail: { dateRow, isoDate },
  });
}

async function fillCellByLabelAndRow(page: Page, row: number, label: string, column: number, value: number): Promise<void> {
  const rowLocator = page.locator(`[data-row="${row}"]`).first();
  if (!(await rowLocator.isVisible().catch(() => false))) {
    throw new UncertainStateError('SharePoint row is not visible.', {
      module: 'sharepoint/writer',
      action: 'fillCellByLabelAndRow',
      url: page.url(),
      detail: { row, label },
    });
  }

  const rowText = (await rowLocator.textContent()) ?? '';
  if (!rowText.toLowerCase().includes(label.toLowerCase())) {
    const byLabelRow = page.locator(`[role="row"]:has-text("${label}")`).first();
    if (!(await byLabelRow.isVisible().catch(() => false))) {
      throw new UncertainStateError('SharePoint row label mismatch and label fallback missing.', {
        module: 'sharepoint/writer',
        action: 'labelMismatch',
        url: page.url(),
        detail: { row, label, rowText },
      });
    }
    await byLabelRow.locator(`[role="gridcell"]:nth-child(${column})`).click();
  } else {
    await rowLocator.locator(`[role="gridcell"]:nth-child(${column})`).click();
  }
  await page.keyboard.type(String(value));
  await page.keyboard.press('Enter');
}

async function waitForAutosave(page: Page): Promise<void> {
  const autosave = page.locator('text=Saved, text=All changes saved').first();
  if (!(await autosave.isVisible({ timeout: 20_000 }).catch(() => false))) {
    throw new UncertainStateError('SharePoint autosave confirmation not detected.', {
      module: 'sharepoint/writer',
      action: 'waitForAutosave',
      url: page.url(),
    });
  }
}

export async function writeTotalsToSharePoint(page: Page, totals: WorkflowTotals, dateContext: DateContext): Promise<void> {
  await page.goto(workflowConfig.sharePointUrl, { waitUntil: 'domcontentloaded' });

  const vkSheet = resolveSheetName(workflowConfig.sharePoint.sheetNamePatterns.vosker, dateContext);
  await openSheet(page, vkSheet);
  const vkColumn = await findDateColumnByRow(page, workflowConfig.sharePoint.dateRows.vosker, dateContext.isoDate);

  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.vosker.googleAds.row, workflowConfig.sharePoint.rows.vosker.googleAds.label, vkColumn, totals.vosker.googleAds);
  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.vosker.facebookAds.row, workflowConfig.sharePoint.rows.vosker.facebookAds.label, vkColumn, totals.vosker.facebookAds);
  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.vosker.microsoftAds.row, workflowConfig.sharePoint.rows.vosker.microsoftAds.label, vkColumn, totals.vosker.microsoftAds);
  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.vosker.tiktokAds.row, workflowConfig.sharePoint.rows.vosker.tiktokAds.label, vkColumn, totals.vosker.tiktokAds ?? 0);

  const spSheet = resolveSheetName(workflowConfig.sharePoint.sheetNamePatterns.spyPoint, dateContext);
  await openSheet(page, spSheet);
  const spColumn = await findDateColumnByRow(page, workflowConfig.sharePoint.dateRows.spyPoint, dateContext.isoDate);

  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.spyPoint.googleAds.row, workflowConfig.sharePoint.rows.spyPoint.googleAds.label, spColumn, totals.spyPoint.googleAds);
  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.spyPoint.facebookAds.row, workflowConfig.sharePoint.rows.spyPoint.facebookAds.label, spColumn, totals.spyPoint.facebookAds);
  await fillCellByLabelAndRow(page, workflowConfig.sharePoint.rows.spyPoint.microsoftAds.row, workflowConfig.sharePoint.rows.spyPoint.microsoftAds.label, spColumn, totals.spyPoint.microsoftAds);

  await waitForAutosave(page);
  logStep('sharepoint.write.complete', { totals });
}
