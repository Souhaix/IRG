"""Download / upload an Excel file from SharePoint via Microsoft Graph API."""

import io
import logging
from datetime import date

import msal
import openpyxl
import requests

from config import SharePointConfig, EXCEL_MAP

logger = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _get_access_token(cfg: SharePointConfig) -> str:
    """Acquire an app-only token via client credentials flow."""
    authority = f"https://login.microsoftonline.com/{cfg.tenant_id}"
    app = msal.ConfidentialClientApplication(
        cfg.client_id,
        authority=authority,
        client_credential=cfg.client_secret,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"SharePoint auth failed: {result.get('error_description')}")
    return result["access_token"]


def _get_site_id(token: str, site_name: str) -> str:
    """Resolve the SharePoint site ID from its name."""
    resp = requests.get(
        f"{GRAPH_BASE}/sites?search={site_name}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    sites = resp.json().get("value", [])
    if not sites:
        raise RuntimeError(f"SharePoint site '{site_name}' not found")
    return sites[0]["id"]


def _file_url(site_id: str, drive_id: str, file_path: str) -> str:
    if drive_id:
        return f"{GRAPH_BASE}/sites/{site_id}/drives/{drive_id}/root:{file_path}:"
    return f"{GRAPH_BASE}/sites/{site_id}/drive/root:{file_path}:"


def download_workbook(cfg: SharePointConfig) -> openpyxl.Workbook:
    """Download the Excel file from SharePoint and return an openpyxl Workbook."""
    token = _get_access_token(cfg)
    site_id = _get_site_id(token, cfg.site_name)
    url = _file_url(site_id, cfg.drive_id, cfg.file_path) + "/content"

    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    resp.raise_for_status()

    wb = openpyxl.load_workbook(io.BytesIO(resp.content))
    logger.info("Downloaded workbook from SharePoint (%d bytes)", len(resp.content))
    return wb


def upload_workbook(cfg: SharePointConfig, wb: openpyxl.Workbook) -> None:
    """Upload the modified workbook back to SharePoint."""
    token = _get_access_token(cfg)
    site_id = _get_site_id(token, cfg.site_name)
    url = _file_url(site_id, cfg.drive_id, cfg.file_path) + "/content"

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
        data=buf.read(),
        timeout=60,
    )
    resp.raise_for_status()
    logger.info("Uploaded workbook to SharePoint")


def _find_date_column(ws, target_date: date) -> int | None:
    """Find column in row 1 that matches *target_date*."""
    for col in range(1, ws.max_column + 1):
        cell_value = ws.cell(row=1, column=col).value
        if cell_value is None:
            continue
        # Handle both datetime objects and strings
        if hasattr(cell_value, "date"):
            if cell_value.date() == target_date:
                return col
        elif isinstance(cell_value, date):
            if cell_value == target_date:
                return col
        elif str(cell_value).strip() == target_date.isoformat():
            return col
    return None


def write_spend_to_workbook(
    wb: openpyxl.Workbook,
    spend_data: dict[str, float],
    target_date: date,
) -> None:
    """Write spend values into the correct sheet/cell of the workbook."""
    for key, spend in spend_data.items():
        mapping = EXCEL_MAP.get(key)
        if mapping is None:
            logger.warning("No Excel mapping for key '%s' — skipping", key)
            continue

        sheet_name = mapping["sheet"]
        row = mapping["row"]

        if sheet_name not in wb.sheetnames:
            logger.warning("Sheet '%s' not found in workbook — skipping %s", sheet_name, key)
            continue

        ws = wb[sheet_name]
        col = _find_date_column(ws, target_date)

        if col is None:
            logger.warning(
                "Date %s not found in row 1 of sheet '%s' — skipping %s",
                target_date, sheet_name, key,
            )
            continue

        ws.cell(row=row, column=col, value=round(spend, 2))
        logger.info("Wrote %.2f → %s!%s%d", spend, sheet_name, _col_letter(col), row)


def _col_letter(col: int) -> str:
    """Convert 1-based column number to Excel letter (1→A, 27→AA)."""
    result = ""
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        result = chr(65 + remainder) + result
    return result
