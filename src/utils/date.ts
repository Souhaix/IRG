import { format, subDays } from 'date-fns';
import { DateContext } from '../types/index.js';

export function getTargetDateContext(override?: string): DateContext {
  const base = override ? new Date(`${override}T00:00:00`) : subDays(new Date(), 1);
  if (Number.isNaN(base.getTime())) {
    throw new Error(`Invalid TARGET_DATE_OVERRIDE: ${override}`);
  }
  return {
    targetDate: base,
    isoDate: format(base, 'yyyy-MM-dd'),
    uiMonthShort: format(base, 'MMM').toUpperCase(),
    uiYear: format(base, 'yyyy'),
  };
}
