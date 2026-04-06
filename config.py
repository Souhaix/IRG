"""Configuration — loads account IDs and credentials from .env."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Google Ads
# ---------------------------------------------------------------------------
@dataclass
class GoogleAdsConfig:
    developer_token: str = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    client_id: str = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
    client_secret: str = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")
    refresh_token: str = os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "")
    login_customer_id: str = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "")

    vosker_accounts: list[str] = field(default_factory=lambda: [
        os.getenv("GOOGLE_ADS_VOSKER_1", ""),
        os.getenv("GOOGLE_ADS_VOSKER_2", ""),
        os.getenv("GOOGLE_ADS_VOSKER_3", ""),
    ])
    spypoint_accounts: list[str] = field(default_factory=lambda: [
        os.getenv("GOOGLE_ADS_SPYPOINT_1", ""),
        os.getenv("GOOGLE_ADS_SPYPOINT_2", ""),
        os.getenv("GOOGLE_ADS_SPYPOINT_3", ""),
    ])


# ---------------------------------------------------------------------------
# Facebook / Meta Ads
# ---------------------------------------------------------------------------
@dataclass
class FacebookAdsConfig:
    access_token: str = os.getenv("FACEBOOK_ACCESS_TOKEN", "")

    vosker_accounts: list[str] = field(default_factory=lambda: [
        os.getenv("FACEBOOK_VOSKER_1", ""),
        os.getenv("FACEBOOK_VOSKER_2", ""),
    ])
    spypoint_accounts: list[str] = field(default_factory=lambda: [
        os.getenv("FACEBOOK_SPYPOINT_1", ""),
        os.getenv("FACEBOOK_SPYPOINT_2", ""),
    ])


# ---------------------------------------------------------------------------
# Microsoft (Bing) Ads
# ---------------------------------------------------------------------------
@dataclass
class MicrosoftAdsConfig:
    client_id: str = os.getenv("MICROSOFT_ADS_CLIENT_ID", "")
    client_secret: str = os.getenv("MICROSOFT_ADS_CLIENT_SECRET", "")
    refresh_token: str = os.getenv("MICROSOFT_ADS_REFRESH_TOKEN", "")
    developer_token: str = os.getenv("MICROSOFT_ADS_DEVELOPER_TOKEN", "")

    accounts: list[str] = field(default_factory=lambda: [
        os.getenv("MICROSOFT_ADS_ACCOUNT_1", ""),
        os.getenv("MICROSOFT_ADS_ACCOUNT_2", ""),
    ])


# ---------------------------------------------------------------------------
# TikTok Ads
# ---------------------------------------------------------------------------
@dataclass
class TikTokAdsConfig:
    access_token: str = os.getenv("TIKTOK_ACCESS_TOKEN", "")

    vosker_accounts: list[str] = field(default_factory=lambda: [
        os.getenv("TIKTOK_VOSKER_1", ""),
    ])


# ---------------------------------------------------------------------------
# SharePoint
# ---------------------------------------------------------------------------
@dataclass
class SharePointConfig:
    tenant_id: str = os.getenv("SHAREPOINT_TENANT_ID", "")
    client_id: str = os.getenv("SHAREPOINT_CLIENT_ID", "")
    client_secret: str = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
    site_name: str = os.getenv("SHAREPOINT_SITE_NAME", "")
    drive_id: str = os.getenv("SHAREPOINT_DRIVE_ID", "")
    file_path: str = os.getenv("SHAREPOINT_FILE_PATH", "/General/Ad_Spending.xlsx")


# ---------------------------------------------------------------------------
# Excel mapping — sheet name → list of (row_label, platform, brand, account_index)
#
# Adjust the CELL_MAP below to match your actual Excel layout.
# Each entry maps:  (sheet_name, cell) → description
# ---------------------------------------------------------------------------

# Which Excel sheet each brand uses
SHEET_VOSKER = "Vosker"
SHEET_SPYPOINT = "SpyPoint"

# Column where yesterday's spend is written (adapt to your layout).
# The script finds the column by matching yesterday's date in row 1.
# Row numbers per platform/account (adapt to your layout).
EXCEL_MAP = {
    # --- Vosker sheet ---
    "google_vosker_1":    {"sheet": SHEET_VOSKER, "row": 2},
    "google_vosker_2":    {"sheet": SHEET_VOSKER, "row": 3},
    "google_vosker_3":    {"sheet": SHEET_VOSKER, "row": 4},
    "facebook_vosker_1":  {"sheet": SHEET_VOSKER, "row": 5},
    "facebook_vosker_2":  {"sheet": SHEET_VOSKER, "row": 6},
    "microsoft_1":        {"sheet": SHEET_VOSKER, "row": 7},
    "microsoft_2":        {"sheet": SHEET_VOSKER, "row": 8},
    "tiktok_vosker_1":    {"sheet": SHEET_VOSKER, "row": 9},
    # --- SpyPoint sheet ---
    "google_spypoint_1":  {"sheet": SHEET_SPYPOINT, "row": 2},
    "google_spypoint_2":  {"sheet": SHEET_SPYPOINT, "row": 3},
    "google_spypoint_3":  {"sheet": SHEET_SPYPOINT, "row": 4},
    "facebook_spypoint_1": {"sheet": SHEET_SPYPOINT, "row": 5},
    "facebook_spypoint_2": {"sheet": SHEET_SPYPOINT, "row": 6},
}
