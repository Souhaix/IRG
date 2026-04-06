"""Fetch yesterday's spend from Google Ads accounts."""

import logging
from datetime import date

from google.ads.googleads.client import GoogleAdsClient

from config import GoogleAdsConfig
from normalize import normalize_spend

logger = logging.getLogger(__name__)


def _build_client(cfg: GoogleAdsConfig) -> GoogleAdsClient:
    return GoogleAdsClient.load_from_dict({
        "developer_token": cfg.developer_token,
        "client_id": cfg.client_id,
        "client_secret": cfg.client_secret,
        "refresh_token": cfg.refresh_token,
        "login_customer_id": cfg.login_customer_id,
        "use_proto_plus": True,
    })


def _fetch_spend_single(cfg: GoogleAdsConfig, customer_id: str, target_date: date) -> float:
    """Return total spend (in account currency) for *target_date* on one account."""
    client = _build_client(cfg)
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT metrics.cost_micros
        FROM customer
        WHERE segments.date = '{target_date.isoformat()}'
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)
    total_micros = 0
    for batch in response:
        for row in batch.results:
            total_micros += row.metrics.cost_micros

    spend = total_micros / 1_000_000
    logger.info("Google Ads %s — spend %s: %.2f", customer_id, target_date, spend)
    return normalize_spend(spend)


def _fetch_and_sum(cfg: GoogleAdsConfig, accounts: dict[str, str], target_date: date) -> float:
    """Fetch spend for each account in the dict and return the sum."""
    total = 0.0
    for name, cid in accounts.items():
        if not cid:
            logger.warning("Google Ads account '%s' has no customer ID configured — skipping", name)
            continue
        try:
            total += _fetch_spend_single(cfg, cid, target_date)
        except Exception:
            logger.exception("Failed to fetch Google Ads spend for '%s' (%s)", name, cid)
    return total


def fetch_all(cfg: GoogleAdsConfig, target_date: date) -> dict[str, float]:
    """Return aggregated spend per brand.

    Returns:
        {
            "google_ads_vosker": <sum of 3 Vosker accounts>,
            "google_ads_spypoint": <sum of 3 SpyPoint accounts>,
        }
    """
    results: dict[str, float] = {}

    logger.info("Fetching Google Ads — Vosker (3 accounts)…")
    results["google_ads_vosker"] = _fetch_and_sum(cfg, cfg.vosker_accounts, target_date)

    logger.info("Fetching Google Ads — SpyPoint (3 accounts)…")
    results["google_ads_spypoint"] = _fetch_and_sum(cfg, cfg.spypoint_accounts, target_date)

    return results
