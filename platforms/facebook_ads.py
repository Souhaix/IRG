"""Fetch yesterday's spend from Facebook / Meta Ads accounts."""

import logging
from datetime import date

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from config import FacebookAdsConfig

logger = logging.getLogger(__name__)


def fetch_spend(cfg: FacebookAdsConfig, account_id: str, target_date: date) -> float:
    """Return total spend for *target_date* on a single ad account."""
    FacebookAdsApi.init(access_token=cfg.access_token)

    account = AdAccount(account_id)
    date_str = target_date.isoformat()

    insights = account.get_insights(params={
        "time_range": {"since": date_str, "until": date_str},
        "level": "account",
    }, fields=["spend"])

    spend = 0.0
    for row in insights:
        spend += float(row.get("spend", 0))

    logger.info("Facebook Ads %s — spend %s: %.2f", account_id, target_date, spend)
    return spend


def fetch_all(cfg: FacebookAdsConfig, target_date: date) -> dict[str, float]:
    """Return spend keyed by account label."""
    results: dict[str, float] = {}

    for i, aid in enumerate(cfg.vosker_accounts, start=1):
        key = f"facebook_vosker_{i}"
        try:
            results[key] = fetch_spend(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Facebook spend for %s (%s)", key, aid)
            results[key] = 0.0

    for i, aid in enumerate(cfg.spypoint_accounts, start=1):
        key = f"facebook_spypoint_{i}"
        try:
            results[key] = fetch_spend(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Facebook spend for %s (%s)", key, aid)
            results[key] = 0.0

    return results
