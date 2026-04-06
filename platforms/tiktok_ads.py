"""Fetch yesterday's spend from TikTok Ads accounts."""

import logging
from datetime import date

import requests

from config import TikTokAdsConfig

logger = logging.getLogger(__name__)

REPORTING_URL = "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/"


def fetch_spend(cfg: TikTokAdsConfig, advertiser_id: str, target_date: date) -> float:
    """Return total spend for *target_date*."""
    date_str = target_date.isoformat()

    headers = {
        "Access-Token": cfg.access_token,
        "Content-Type": "application/json",
    }

    params = {
        "advertiser_id": advertiser_id,
        "report_type": "BASIC",
        "data_level": "AUCTION_ADVERTISER",
        "dimensions": '["advertiser_id"]',
        "metrics": '["spend"]',
        "start_date": date_str,
        "end_date": date_str,
    }

    resp = requests.get(REPORTING_URL, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    spend = 0.0
    if data.get("code") == 0:
        for row in data.get("data", {}).get("list", []):
            spend += float(row.get("metrics", {}).get("spend", 0))
    else:
        logger.error("TikTok API error: %s", data.get("message"))

    logger.info("TikTok Ads %s — spend %s: %.2f", advertiser_id, target_date, spend)
    return spend


def fetch_all(cfg: TikTokAdsConfig, target_date: date) -> dict[str, float]:
    """Return spend keyed by account label."""
    results: dict[str, float] = {}

    for i, aid in enumerate(cfg.vosker_accounts, start=1):
        key = f"tiktok_vosker_{i}"
        try:
            results[key] = fetch_spend(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch TikTok spend for %s (%s)", key, aid)
            results[key] = 0.0

    return results
