"""Fetch yesterday's spend from Microsoft (Bing) Ads accounts.

Uses the official bingads SDK with the proper async reporting flow:
  1. Submit a report request
  2. Poll until the report is ready
  3. Download and parse the CSV result
"""

import csv
import io
import logging
import time
import zipfile
from datetime import date

from bingads.service_client import ServiceClient
from bingads.authorization import AuthorizationData, OAuthDesktopMobileAuthCodeGrant

from config import MicrosoftAdsConfig
from normalize import normalize_spend

logger = logging.getLogger(__name__)

# Polling config for async report
POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 60  # 5 min max


def _get_authorization(cfg: MicrosoftAdsConfig) -> AuthorizationData:
    """Build AuthorizationData with OAuth refresh token."""
    authentication = OAuthDesktopMobileAuthCodeGrant(
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
    )
    authentication.token_refresh_callback = lambda _oauth, _token: None
    # Set the refresh token so the SDK can exchange it for an access token
    authentication.request_oauth_tokens_by_refresh_token(cfg.refresh_token)

    authorization_data = AuthorizationData(
        developer_token=cfg.developer_token,
        authentication=authentication,
    )
    return authorization_data


def _fetch_spend_single(cfg: MicrosoftAdsConfig, account_id: str, target_date: date) -> float:
    """Return total spend for *target_date* using the Reporting API async flow."""
    authorization_data = _get_authorization(cfg)
    authorization_data.account_id = account_id

    reporting_service = ServiceClient(
        service="ReportingService",
        version=13,
        authorization_data=authorization_data,
        environment="production",
    )

    # Build report request
    report_request = reporting_service.factory.create("AccountPerformanceReportRequest")
    report_request.Format = "Csv"
    report_request.Aggregation = "Daily"
    report_request.ExcludeColumnHeaders = False
    report_request.ExcludeReportFooter = True
    report_request.ExcludeReportHeader = True
    report_request.ReturnOnlyCompleteData = False

    # Columns
    columns = reporting_service.factory.create("ArrayOfAccountPerformanceReportColumn")
    columns.AccountPerformanceReportColumn = ["AccountId", "TimePeriod", "Spend"]
    report_request.Columns = columns

    # Scope
    scope = reporting_service.factory.create("AccountReportScope")
    account_ids = reporting_service.factory.create("ns1:ArrayOflong")
    account_ids.long = [int(account_id)]
    scope.AccountIds = account_ids
    report_request.Scope = scope

    # Time period
    report_time = reporting_service.factory.create("ReportTime")
    custom_start = reporting_service.factory.create("Date")
    custom_start.Day = target_date.day
    custom_start.Month = target_date.month
    custom_start.Year = target_date.year
    custom_end = reporting_service.factory.create("Date")
    custom_end.Day = target_date.day
    custom_end.Month = target_date.month
    custom_end.Year = target_date.year
    report_time.CustomDateRangeStart = custom_start
    report_time.CustomDateRangeEnd = custom_end
    report_time.PredefinedTime = None
    report_request.Time = report_time

    # Step 1: Submit the report request
    response = reporting_service.SubmitGenerateReport(ReportRequest=report_request)
    report_request_id = response

    logger.info("Microsoft Ads %s — submitted report request: %s", account_id, report_request_id)

    # Step 2: Poll until the report is ready
    report_url = None
    for attempt in range(MAX_POLL_ATTEMPTS):
        poll_response = reporting_service.PollGenerateReport(
            ReportRequestId=report_request_id,
        )
        status = poll_response.Status

        if status == "Success":
            report_url = poll_response.ReportDownloadUrl
            break
        elif status == "Error":
            raise RuntimeError(
                f"Microsoft Ads report failed for account {account_id}"
            )
        else:
            # "Pending" — wait and retry
            time.sleep(POLL_INTERVAL_SECONDS)

    if report_url is None:
        raise TimeoutError(
            f"Microsoft Ads report timed out for account {account_id} "
            f"after {MAX_POLL_ATTEMPTS * POLL_INTERVAL_SECONDS}s"
        )

    # Step 3: Download and parse the CSV
    import requests
    resp = requests.get(report_url, timeout=60)
    resp.raise_for_status()

    # The report is a ZIP containing a single CSV file
    spend = 0.0
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_filename = zf.namelist()[0]
        with zf.open(csv_filename) as csv_file:
            reader = csv.DictReader(io.TextIOWrapper(csv_file, encoding="utf-8"))
            for row in reader:
                spend += normalize_spend(row.get("Spend", 0))

    logger.info("Microsoft Ads %s — spend %s: %.2f", account_id, target_date, spend)
    return spend


def fetch_all(cfg: MicrosoftAdsConfig, target_date: date) -> dict[str, float]:
    """Return spend per brand (1 account each, no aggregation needed).

    Returns:
        {
            "microsoft_ads_vosker": <Vosker Security spend>,
            "microsoft_ads_spypoint": <SPYPOINT spend>,
        }
    """
    results: dict[str, float] = {}

    # Vosker Security — 1 account
    for name, aid in cfg.vosker_account.items():
        if not aid:
            logger.warning("Microsoft Ads account '%s' has no ID configured — skipping", name)
            results["microsoft_ads_vosker"] = 0.0
            continue
        try:
            results["microsoft_ads_vosker"] = _fetch_spend_single(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Microsoft Ads spend for '%s' (%s)", name, aid)
            results["microsoft_ads_vosker"] = 0.0

    # SPYPOINT — 1 account
    for name, aid in cfg.spypoint_account.items():
        if not aid:
            logger.warning("Microsoft Ads account '%s' has no ID configured — skipping", name)
            results["microsoft_ads_spypoint"] = 0.0
            continue
        try:
            results["microsoft_ads_spypoint"] = _fetch_spend_single(cfg, aid, target_date)
        except Exception:
            logger.exception("Failed to fetch Microsoft Ads spend for '%s' (%s)", name, aid)
            results["microsoft_ads_spypoint"] = 0.0

    return results
