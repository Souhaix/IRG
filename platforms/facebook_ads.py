"""Fetch yesterday's spend from Facebook / Meta Ads accounts."""

import logging
from datetime import date

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from config import FacebookAdsConfig
from normalize import normalize_spend

logger = logging.getLogger(__name__)


def _fetch_spend_single(cfg: FacebookAdsConfig, account_id: str, target_date: date) -> float:
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
        spend += normalize_spend(row.get("spend", 0))

    logger.info("Meta Ads %s — spend %s: %.2f", account_id, target_date, spend)
    return spend


def _fetch_and_sum(cfg: FacebookAdsConfig, accounts: dict[str, str], target_date: date) -> float:
    """Fetch spend for each account in the dict and return the sum."""
    total = 0.0
    for name, aid in accounts.items():
        if not aid:
            logger.warning("Meta Ads account '%s' has no account ID configured — skipping", name)
            continue
        try:
            total += _fetch_spend_single(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Meta Ads spend for '%s' (%s)", name, aid)
    return total


def fetch_all(cfg: FacebookAdsConfig, target_date: date) -> dict[str, float]:
    """Return aggregated spend per brand.

    Returns:
        {
            "facebook_ads_vosker": <sum of Vosker + Vosker-Québec>,
            "facebook_ads_spypoint": <sum of SPYPOINT + Spypoint-Québec>,
        }
    """
    results: dict[str, float] = {}

    logger.info("Fetching Meta Ads — Vosker (2 accounts)…")
    results["facebook_ads_vosker"] = _fetch_and_sum(cfg, cfg.vosker_accounts, target_date)

    logger.info("Fetching Meta Ads — SpyPoint (2 accounts)…")
    results["facebook_ads_spypoint"] = _fetch_and_sum(cfg, cfg.spypoint_accounts, target_date)

    return results
