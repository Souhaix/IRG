"""Fetch yesterday's spend from Microsoft (Bing) Ads accounts via REST API."""

import logging
from datetime import date

import requests

from config import MicrosoftAdsConfig

logger = logging.getLogger(__name__)

REPORTING_URL = "https://reporting.api.bingads.microsoft.com/Reporting/v13/GenerateReport"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"


def _get_access_token(cfg: MicrosoftAdsConfig) -> str:
    """Exchange refresh token for a fresh access token."""
    resp = requests.post(TOKEN_URL, data={
        "client_id": cfg.client_id,
        "client_secret": cfg.client_secret,
        "refresh_token": cfg.refresh_token,
        "grant_type": "refresh_token",
        "scope": "https://ads.microsoft.com/.default",
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_spend(cfg: MicrosoftAdsConfig, account_id: str, target_date: date) -> float:
    """Return total spend for *target_date* using the Reporting API."""
    access_token = _get_access_token(cfg)
    date_str = target_date.isoformat()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "DeveloperToken": cfg.developer_token,
        "Content-Type": "application/json",
    }

    # Use the AccountPerformanceReport for daily spend
    body = {
        "ReportRequest": {
            "ExcludeColumnHeaders": False,
            "ExcludeReportFooter": True,
            "ExcludeReportHeader": True,
            "Format": "Csv",
            "ReturnOnlyCompleteData": False,
            "Type": "AccountPerformanceReportRequest",
            "Aggregation": "Daily",
            "Columns": ["AccountId", "TimePeriod", "Spend"],
            "Scope": {
                "AccountIds": [int(account_id)],
            },
            "Time": {
                "CustomDateRangeStart": {
                    "Day": target_date.day,
                    "Month": target_date.month,
                    "Year": target_date.year,
                },
                "CustomDateRangeEnd": {
                    "Day": target_date.day,
                    "Month": target_date.month,
                    "Year": target_date.year,
                },
            },
        }
    }

    resp = requests.post(REPORTING_URL, json=body, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # Parse CSV-style report rows
    spend = 0.0
    rows = data.get("ReportRows", [])
    for row in rows:
        spend += float(row.get("Spend", 0))

    logger.info("Microsoft Ads %s — spend %s: %.2f", account_id, target_date, spend)
    return spend


def fetch_all(cfg: MicrosoftAdsConfig, target_date: date) -> dict[str, float]:
    """Return spend keyed by account label."""
    results: dict[str, float] = {}

    for i, aid in enumerate(cfg.accounts, start=1):
        key = f"microsoft_{i}"
        try:
            results[key] = fetch_spend(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Microsoft Ads spend for %s (%s)", key, aid)
            results[key] = 0.0

    return results
