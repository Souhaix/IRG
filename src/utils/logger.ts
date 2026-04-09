import pino from 'pino';
import { mkdirSync } from 'node:fs';
import { env } from '../config/env.js';

mkdirSync('logs', { recursive: true });

const streams: pino.StreamEntry[] = [
  { stream: pino.destination({ dest: 1, sync: false }) },
  { stream: pino.destination({ dest: `logs/run-${new Date().toISOString().slice(0, 10)}.jsonl`, mkdir: true, sync: false }) },
];

export const logger = pino(
  {
    level: env.LOG_LEVEL,
    base: undefined,
    formatters: {
      level: (label) => ({ level: label }),
    },
  },
  pino.multistream(streams),
);

export function logStep(event: string, metadata?: Record<string, unknown>): void {
  logger.info({ event, ...metadata });
}
