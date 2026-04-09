import { env, resolveRunMode } from './config/env.js';
import { workflowConfig } from './config/accounts.js';
import { getTargetDateContext } from './utils/date.js';
import { captureErrorArtifacts, UncertainStateError } from './utils/errors.js';
import { launchPersistentContext, newPage } from './utils/browser.js';
import { logStep, logger } from './utils/logger.js';
import { collectTikTokSpend } from './platforms/tiktok.js';
import { collectGoogleAdsSpend } from './platforms/googleAds.js';
import { collectFacebookAdsSpend } from './platforms/facebookAds.js';
import { collectMicrosoftAdsSpend } from './platforms/microsoftAds.js';
import { sumResults } from './platforms/common.js';
import { writeTotalsToSharePoint } from './sharepoint/writer.js';
import { WorkflowTotals } from './types/index.js';

async function run(): Promise<void> {
  const mode = resolveRunMode(process.argv.slice(2));
  const dateContext = getTargetDateContext(env.TARGET_DATE_OVERRIDE);
  logStep('workflow.start', { mode, targetDate: dateContext.isoDate });

  const context = await launchPersistentContext();
  const page = await newPage(context);

  try {
    const tikTokResults = await Promise.all(
      workflowConfig.accounts.tiktok.map((account) => collectTikTokSpend(page, account, dateContext)),
    );

    const googleResults = await collectGoogleAdsSpend(page, workflowConfig.accounts.googleAds, dateContext);
    const facebookResults = await collectFacebookAdsSpend(page, workflowConfig.accounts.facebookAds, dateContext);
    const microsoftResults = await collectMicrosoftAdsSpend(page, workflowConfig.accounts.microsoftAds, dateContext);

    const totals: WorkflowTotals = {
      targetDate: dateContext.isoDate,
      vosker: {
        brand: 'Vosker',
        googleAds: sumResults(googleResults.filter((x) => x.brand === 'Vosker')),
        facebookAds: sumResults(facebookResults.filter((x) => x.brand === 'Vosker')),
        microsoftAds: sumResults(microsoftResults.filter((x) => x.brand === 'Vosker')),
        tiktokAds: sumResults(tikTokResults.filter((x) => x.brand === 'Vosker')),
      },
      spyPoint: {
        brand: 'SpyPoint',
        googleAds: sumResults(googleResults.filter((x) => x.brand === 'SpyPoint')),
        facebookAds: sumResults(facebookResults.filter((x) => x.brand === 'SpyPoint')),
        microsoftAds: sumResults(microsoftResults.filter((x) => x.brand === 'SpyPoint')),
      },
    };

    logStep('workflow.totals', totals as unknown as Record<string, unknown>);

    if (mode === 'write') {
      await writeTotalsToSharePoint(page, totals, dateContext);
    } else {
      logStep('workflow.dry_run', { message: 'Dry-run enabled: SharePoint write skipped.' });
    }
  } catch (error) {
    await captureErrorArtifacts(page, error, {
      module: 'workflow',
      action: 'run',
      url: page.url(),
      detail: error instanceof Error ? error.message : String(error),
    });
    if (error instanceof UncertainStateError) {
      logger.error({ err: error, context: error.context }, 'Stopped due to uncertain state.');
    } else {
      logger.error({ err: error }, 'Workflow failed.');
    }
    process.exitCode = 1;
  } finally {
    await context.close();
  }
}

run().catch((error) => {
  logger.fatal({ err: error }, 'Fatal startup failure.');
  process.exit(1);
});
