import { chromium, BrowserContext, BrowserContextOptions, Page } from 'playwright';
import { env } from '../config/env.js';
import { workflowConfig } from '../config/accounts.js';

export async function launchPersistentContext(): Promise<BrowserContext> {
  const options: BrowserContextOptions = {
    viewport: { width: 1800, height: 1000 },
    timezoneId: process.env.TIMEZONE,
  };

  return chromium.launchPersistentContext(workflowConfig.browserProfilePath ?? env.BROWSER_PROFILE_PATH, {
    channel: env.BROWSER_CHANNEL,
    headless: env.headless,
    ...options,
  });
}

export async function newPage(context: BrowserContext): Promise<Page> {
  const page = context.pages()[0] ?? (await context.newPage());
  page.setDefaultTimeout(workflowConfig.timeouts.defaultMs);
  return page;
}
