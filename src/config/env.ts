import { config as loadEnv } from 'dotenv';
import { z } from 'zod';
import { RunMode } from '../types/index.js';

loadEnv();

const envSchema = z.object({
  NODE_ENV: z.string().default('development'),
  TIMEZONE: z.string().default(Intl.DateTimeFormat().resolvedOptions().timeZone),
  RUN_MODE: z.enum(['dry', 'write']).default('dry'),
  LOG_LEVEL: z.string().default('info'),
  HEADLESS: z.enum(['true', 'false']).default('false'),
  BROWSER_CHANNEL: z.string().default('chrome'),
  BROWSER_PROFILE_PATH: z.string().default('.profiles/main'),
  TARGET_DATE_OVERRIDE: z.string().optional(),
});

const parsed = envSchema.safeParse(process.env);
if (!parsed.success) {
  throw new Error(`Invalid environment variables: ${parsed.error.message}`);
}

export const env = {
  ...parsed.data,
  headless: parsed.data.HEADLESS === 'true',
};

export function resolveRunMode(cliArgs: string[]): RunMode {
  const argMode = cliArgs.find((arg) => arg.startsWith('--mode='))?.split('=')[1];
  if (argMode === 'dry' || argMode === 'write') {
    return argMode;
  }
  return parsed.data.RUN_MODE;
}
