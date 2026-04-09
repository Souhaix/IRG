export type RunMode = 'dry' | 'write';

export type Brand = 'Vosker' | 'SpyPoint';
export type Platform = 'TikTok' | 'GoogleAds' | 'FacebookAds' | 'MicrosoftAds';

export interface AccountConfig {
  brand: Brand;
  platform: Platform;
  accountName: string;
  accountUrl: string;
}

export interface SpendResult {
  brand: Brand;
  platform: Platform;
  accountName: string;
  currency?: string;
  amount: number;
  sourceUrl: string;
  observedDateText?: string;
}

export interface BrandTotals {
  brand: Brand;
  googleAds: number;
  facebookAds: number;
  microsoftAds: number;
  tiktokAds?: number;
}

export interface WorkflowTotals {
  targetDate: string;
  vosker: BrandTotals;
  spyPoint: BrandTotals;
}

export interface DateContext {
  targetDate: Date;
  isoDate: string;
  uiMonthShort: string;
  uiYear: string;
}

export interface ErrorContext {
  module: string;
  action: string;
  url?: string;
  detail?: unknown;
}
