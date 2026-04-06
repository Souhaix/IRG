#!/usr/bin/env python3
"""
Fetch yesterday's ad spend from all platforms and write to SharePoint Excel.

Platforms:
  - Google Ads   : 3 Vosker + 3 SpyPoint accounts
  - Facebook Ads : 2 Vosker + 2 SpyPoint accounts
  - Microsoft Ads: 2 accounts
  - TikTok Ads   : 1 Vosker account

Usage:
    python main.py              # defaults to yesterday
    python main.py 2026-04-01   # specific date
"""

import logging
import sys
from datetime import date, timedelta

from config import (
    GoogleAdsConfig,
    FacebookAdsConfig,
    MicrosoftAdsConfig,
    TikTokAdsConfig,
    SharePointConfig,
)
from platforms import google_ads, facebook_ads, microsoft_ads, tiktok_ads
from sharepoint import download_workbook, write_spend_to_workbook, upload_workbook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    # Determine target date
    if len(sys.argv) > 1:
        target_date = date.fromisoformat(sys.argv[1])
    else:
        target_date = date.today() - timedelta(days=1)

    logger.info("Fetching ad spend for %s", target_date)

    # ── 1. Fetch spend from all platforms ──────────────────────────
    all_spend: dict[str, float] = {}

    logger.info("── Google Ads ──")
    all_spend.update(google_ads.fetch_all(GoogleAdsConfig(), target_date))

    logger.info("── Facebook Ads ──")
    all_spend.update(facebook_ads.fetch_all(FacebookAdsConfig(), target_date))

    logger.info("── Microsoft Ads ──")
    all_spend.update(microsoft_ads.fetch_all(MicrosoftAdsConfig(), target_date))

    logger.info("── TikTok Ads ──")
    all_spend.update(tiktok_ads.fetch_all(TikTokAdsConfig(), target_date))

    # ── 2. Summary ─────────────────────────────────────────────────
    logger.info("── Spend summary ──")
    for key, value in sorted(all_spend.items()):
        logger.info("  %-25s %10.2f", key, value)
    logger.info("  %-25s %10.2f", "TOTAL", sum(all_spend.values()))

    # ── 3. Write to SharePoint Excel ──────────────────────────────
    sp_cfg = SharePointConfig()
    logger.info("Downloading workbook from SharePoint…")
    wb = download_workbook(sp_cfg)

    write_spend_to_workbook(wb, all_spend, target_date)

    logger.info("Uploading workbook to SharePoint…")
    upload_workbook(sp_cfg, wb)

    logger.info("Done ✓")


if __name__ == "__main__":
    main()
