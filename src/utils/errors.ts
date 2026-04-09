import { Page } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { format } from 'date-fns';
import { ErrorContext } from '../types/index.js';

export class UncertainStateError extends Error {
  constructor(message: string, public context: ErrorContext) {
    super(message);
    this.name = 'UncertainStateError';
  }
}

export async function captureErrorArtifacts(page: Page | null, err: unknown, context: ErrorContext): Promise<void> {
  await mkdir('screenshots', { recursive: true });
  await mkdir('logs', { recursive: true });

  const stamp = format(new Date(), "yyyy-MM-dd'T'HH-mm-ss");
  const screenshotPath = `screenshots/error-${stamp}.png`;
  let url: string | undefined;

  if (page) {
    try {
      url = page.url();
      await page.screenshot({ path: screenshotPath, fullPage: true });
    } catch {
      // best effort
    }
  }

  const payload = {
    timestamp: new Date().toISOString(),
    context,
    url,
    error: err instanceof Error ? { name: err.name, message: err.message, stack: err.stack } : String(err),
    screenshotPath,
  };

  const date = format(new Date(), 'yyyy-MM-dd');
  await writeFile(`logs/error-${date}.json`, `${JSON.stringify(payload, null, 2)}\n`, 'utf-8');
}
