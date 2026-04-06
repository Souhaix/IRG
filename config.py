"""Configuration — loads account IDs and credentials from .env.

All account IDs and tokens are loaded from environment variables.
No real values are hardcoded here.
"""

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

    # Vosker: 3 comptes à sommer
    vosker_accounts: dict[str, str] = field(default_factory=lambda: {
        "Vosker - CA-EN": os.getenv("GOOGLE_ADS_VOSKER_CA_EN", ""),
        "Vosker - Québec": os.getenv("GOOGLE_ADS_VOSKER_QUEBEC", ""),
        "Vosker Products": os.getenv("GOOGLE_ADS_VOSKER_PRODUCTS", ""),
    })

    # SpyPoint: 3 comptes à sommer
    spypoint_accounts: dict[str, str] = field(default_factory=lambda: {
        "SPYPOINT Google Ads": os.getenv("GOOGLE_ADS_SPYPOINT_MAIN", ""),
        "Spypoint - Québec": os.getenv("GOOGLE_ADS_SPYPOINT_QUEBEC", ""),
        "Spypoint - CA-EN": os.getenv("GOOGLE_ADS_SPYPOINT_CA_EN", ""),
    })


# ---------------------------------------------------------------------------
# Facebook / Meta Ads
# ---------------------------------------------------------------------------
@dataclass
class FacebookAdsConfig:
    access_token: str = os.getenv("FACEBOOK_ACCESS_TOKEN", "")

    # Vosker: 2 comptes à sommer
    vosker_accounts: dict[str, str] = field(default_factory=lambda: {
        "Vosker": os.getenv("FACEBOOK_VOSKER_MAIN", ""),
        "Vosker - Québec": os.getenv("FACEBOOK_VOSKER_QUEBEC", ""),
    })

    # SpyPoint: 2 comptes à sommer
    spypoint_accounts: dict[str, str] = field(default_factory=lambda: {
        "SPYPOINT": os.getenv("FACEBOOK_SPYPOINT_MAIN", ""),
        "Spypoint - Québec": os.getenv("FACEBOOK_SPYPOINT_QUEBEC", ""),
    })


# ---------------------------------------------------------------------------
# Microsoft (Bing) Ads
# ---------------------------------------------------------------------------
@dataclass
class MicrosoftAdsConfig:
    client_id: str = os.getenv("MICROSOFT_ADS_CLIENT_ID", "")
    client_secret: str = os.getenv("MICROSOFT_ADS_CLIENT_SECRET", "")
    refresh_token: str = os.getenv("MICROSOFT_ADS_REFRESH_TOKEN", "")
    developer_token: str = os.getenv("MICROSOFT_ADS_DEVELOPER_TOKEN", "")

    # 1 compte Vosker, 1 compte SpyPoint (pas d'agrégation, 1 valeur chacun)
    vosker_account: dict[str, str] = field(default_factory=lambda: {
        "Vosker Security": os.getenv("MICROSOFT_ADS_VOSKER", ""),
    })
    spypoint_account: dict[str, str] = field(default_factory=lambda: {
        "SPYPOINT": os.getenv("MICROSOFT_ADS_SPYPOINT", ""),
    })


# ---------------------------------------------------------------------------
# TikTok Ads — Vosker uniquement (pas de SpyPoint)
# ---------------------------------------------------------------------------
@dataclass
class TikTokAdsConfig:
    access_token: str = os.getenv("TIKTOK_ACCESS_TOKEN", "")

    # 1 seul compte Vosker
    vosker_account: dict[str, str] = field(default_factory=lambda: {
        "Vosker": os.getenv("TIKTOK_VOSKER_ADVERTISER_ID", ""),
    })


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
    file_path: str = os.getenv("SHAREPOINT_FILE_PATH", "")
