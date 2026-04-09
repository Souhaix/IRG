import { AccountConfig } from '../types/index.js';

export interface WorkflowConfig {
  sharePointUrl: string;
  browserProfilePath: string;
  timeouts: {
    defaultMs: number;
    longMs: number;
    selectorMs: number;
  };
  accounts: {
    tiktok: AccountConfig[];
    googleAds: AccountConfig[];
    facebookAds: AccountConfig[];
    microsoftAds: AccountConfig[];
  };
  sharePoint: {
    sheetNamePatterns: {
      vosker: string;
      spyPoint: string;
    };
    dateRows: {
      vosker: number;
      spyPoint: number;
    };
    rows: {
      vosker: {
        googleAds: { row: number; label: string };
        facebookAds: { row: number; label: string };
        microsoftAds: { row: number; label: string };
        tiktokAds: { row: number; label: string };
      };
      spyPoint: {
        googleAds: { row: number; label: string };
        facebookAds: { row: number; label: string };
        microsoftAds: { row: number; label: string };
      };
    };
  };
}

export const workflowConfig: WorkflowConfig = {
  sharePointUrl:
    process.env.SHAREPOINT_URL ??
    'https://vosker.sharepoint.com/:x:/r/sites/Marketing793/_layouts/15/doc2.aspx?sourcedoc=%7B65f2efcf-5a9c-4154-8cbc-ad3353849de6%7D&action=edit&wdinitialsession=7369b1f7-433a-2d74-e100-ea6460a8b379&wdrldsc=240&wdrldc=1&wdrldr=UserInteraction%2CBootTimeMismatch',
  browserProfilePath: process.env.BROWSER_PROFILE_PATH ?? '.profiles/main',
  timeouts: {
    defaultMs: 20_000,
    longMs: 60_000,
    selectorMs: 15_000,
  },
  accounts: {
    tiktok: [
      {
        brand: 'Vosker',
        platform: 'TikTok',
        accountName: 'VOSKER 9381-9506 QC',
        accountUrl:
          'https://ads.tiktok.com/i18n/manage/campaign?aadvid=7130750043740553217&st=2026-04-05&et=2026-04-05',
      },
    ],
    googleAds: [
      {
        brand: 'Vosker',
        platform: 'GoogleAds',
        accountName: 'Vosker Google #1',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=6780551929&euid=1421512265&__u=4034737985&uscid=6780551929&__c=2124932721&authuser=0&workspaceId=0',
      },
      {
        brand: 'Vosker',
        platform: 'GoogleAds',
        accountName: 'Vosker Google #2',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=6774175198&euid=1421512265&__u=4034737985&uscid=6774175198&__c=6986133102&authuser=0&workspaceId=0',
      },
      {
        brand: 'Vosker',
        platform: 'GoogleAds',
        accountName: 'Vosker Google #3',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=301083792&euid=1421512265&__u=4034737985&uscid=301083792&__c=3280699408&authuser=0&workspaceId=0',
      },
      {
        brand: 'SpyPoint',
        platform: 'GoogleAds',
        accountName: 'SpyPoint Google #1',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=376814306&euid=1421512265&__u=4034737985&uscid=376814306&__c=5250675794&authuser=0&workspaceId=0',
      },
      {
        brand: 'SpyPoint',
        platform: 'GoogleAds',
        accountName: 'SpyPoint Google #2',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=6780526313&euid=1421512265&__u=4034737985&uscid=6780526313&__c=6098304737&authuser=0&workspaceId=0',
      },
      {
        brand: 'SpyPoint',
        platform: 'GoogleAds',
        accountName: 'SpyPoint Google #3',
        accountUrl:
          'https://ads.google.com/aw/overview?ocid=6780555040&euid=1421512265&__u=4034737985&uscid=6780555040&__c=8458428960&authuser=0&workspaceId=0',
      },
    ],
    facebookAds: [
      {
        brand: 'Vosker',
        platform: 'FacebookAds',
        accountName: 'Vosker Facebook #1',
        accountUrl:
          'https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=2953829494893178&business_id=135477984102975&global_scope_id=135477984102975&columns=name%2Cdelivery%2Crecommendations_guidance%2Cresults%2Ccost_per_result%2Cbudget%2Cspend%2Cimpressions%2Creach%2Cschedule%2Cend_time%2Cattribution_setting%2Cbid%2Clast_significant_edit%2Cquality_score_organic%2Cquality_score_ectr%2Cquality_score_ecvr%2Ccampaign_name%2Ccpm%2Cpurchase_roas%3Aomni_purchase%2Cfrequency%2Cactions%3Aomni_purchase&attribution_windows=default&date=2026-04-05_2026-04-06%2Cyesterday&comparison_date=&insights_date=2026-04-05_2026-04-06%2Cyesterday&insights_comparison_date=',
      },
      {
        brand: 'Vosker',
        platform: 'FacebookAds',
        accountName: 'Vosker Facebook #2',
        accountUrl:
          'https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=323426190336235&business_id=135477984102975&global_scope_id=135477984102975&date=2026-04-05_2026-04-06%2Cyesterday&comparison_date=&insights_date=2026-04-05_2026-04-06%2Cyesterday&insights_comparison_date=',
      },
      {
        brand: 'SpyPoint',
        platform: 'FacebookAds',
        accountName: 'SpyPoint Facebook #1',
        accountUrl:
          'https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=805565676576814&business_id=135477984102975&global_scope_id=135477984102975&columns=name%2Cdelivery%2Crecommendations_guidance%2Cresults%2Ccost_per_result%2Cbudget%2Cspend%2Cimpressions%2Creach%2Cfrequency%2Ccpm%2Cactions%3Aomni_purchase%2Cschedule%2Cend_time%2Cattribution_setting%2Cbid%2Clast_significant_edit%2Cquality_score_organic%2Cquality_score_ectr%2Cquality_score_ecvr%2Ccampaign_name%2Cpurchase_roas%3Aomni_purchase&attribution_windows=default&date=2026-04-05_2026-04-06&comparison_date=&insights_date=2026-04-05_2026-04-06&insights_comparison_date=',
      },
      {
        brand: 'SpyPoint',
        platform: 'FacebookAds',
        accountName: 'SpyPoint Facebook #2',
        accountUrl:
          'https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=308379728486265&business_id=135477984102975&global_scope_id=135477984102975&columns=name%2Cdelivery%2Crecommendations_guidance%2Cresults%2Ccost_per_result%2Cbudget%2Cspend%2Cimpressions%2Creach%2Cschedule%2Cend_time%2Cattribution_setting%2Cbid%2Clast_significant_edit%2Cquality_score_organic%2Cquality_score_ectr%2Cquality_score_ecvr%2Ccampaign_name%2Ccpm%2Cpurchase_roas%3Aomni_purchase%2Cfrequency%2Cactions%3Aomni_purchase&attribution_windows=default&date=2026-04-05_2026-04-06&comparison_date=&insights_date=2026-04-05_2026-04-06&insights_comparison_date=',
      },
    ],
    microsoftAds: [
      {
        brand: 'Vosker',
        platform: 'MicrosoftAds',
        accountName: 'Vosker Security',
        accountUrl:
          'https://ui.ads.microsoft.com/campaign/vnext/accounts/overview?cid=250990724&uid=157033100',
      },
      {
        brand: 'SpyPoint',
        platform: 'MicrosoftAds',
        accountName: 'SPYPOINT',
        accountUrl:
          'https://ui.ads.microsoft.com/campaign/vnext/accounts/overview?cid=250990724&uid=157033100',
      },
    ],
  },
  sharePoint: {
    sheetNamePatterns: {
      vosker: 'VK [MON] [YEAR] Budget Pacing',
      spyPoint: 'SP [MON] [YEAR] Budget Pacing',
    },
    dateRows: {
      vosker: 13,
      spyPoint: 11,
    },
    rows: {
      vosker: {
        googleAds: { row: 15, label: 'Google Ads Spend' },
        facebookAds: { row: 16, label: 'Facebook Ads Spend' },
        microsoftAds: { row: 17, label: 'Microsoft Ads' },
        tiktokAds: { row: 18, label: 'TikTok Ads' },
      },
      spyPoint: {
        googleAds: { row: 13, label: 'Google Ads Spend actual' },
        facebookAds: { row: 14, label: 'Facebook Ads Spend actual' },
        microsoftAds: { row: 18, label: 'Microsoft Ads' },
      },
    },
  },
};
