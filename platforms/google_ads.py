"""Fetch yesterday's spend from Google Ads accounts."""

import logging
from datetime import date

from google.ads.googleads.client import GoogleAdsClient

from config import GoogleAdsConfig

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


def fetch_spend(cfg: GoogleAdsConfig, customer_id: str, target_date: date) -> float:
    """Return total spend (in account currency) for *target_date*."""
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
    return spend


def fetch_all(cfg: GoogleAdsConfig, target_date: date) -> dict[str, float]:
    """Return spend keyed by account label (e.g. 'google_vosker_1')."""
    results: dict[str, float] = {}

    for i, cid in enumerate(cfg.vosker_accounts, start=1):
        key = f"google_vosker_{i}"
        try:
            results[key] = fetch_spend(cfg, cid, target_date)
        except Exception:
            logger.exception("Failed to fetch Google Ads spend for %s (%s)", key, cid)
            results[key] = 0.0

    for i, cid in enumerate(cfg.spypoint_accounts, start=1):
        key = f"google_spypoint_{i}"
        try:
            results[key] = fetch_spend(cfg, cid, target_date)
        except Exception:
            logger.exception("Failed to fetch Google Ads spend for %s (%s)", key, cid)
            results[key] = 0.0

    return results
