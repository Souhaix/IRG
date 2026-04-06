"""Load and validate the Excel mapping configuration.

The mapping is loaded from excel_mapping.json (created by copying
excel_mapping.template.json and filling in real values).

This module also provides the SPEND_KEY → (sheet, label) mapping
that sharepoint.py uses to write values.
"""

import json
import logging
import os

logger = logging.getLogger(__name__)

MAPPING_FILE = os.path.join(os.path.dirname(__file__), "excel_mapping.json")


def load_excel_mapping() -> dict:
    """Load excel_mapping.json and return the parsed dict.

    Raises FileNotFoundError with a clear message if the file doesn't exist.
    """
    if not os.path.exists(MAPPING_FILE):
        raise FileNotFoundError(
            f"Excel mapping file not found: {MAPPING_FILE}\n"
            f"Copy excel_mapping.template.json → excel_mapping.json and fill in real values."
        )

    with open(MAPPING_FILE, encoding="utf-8") as f:
        mapping = json.load(f)

    _validate(mapping)
    return mapping


def _validate(mapping: dict) -> None:
    """Warn about any fields that still contain TODO placeholders."""
    todo_fields = []
    _find_todos(mapping, "", todo_fields)
    if todo_fields:
        logger.warning(
            "excel_mapping.json has %d field(s) still containing TODO placeholders:",
            len(todo_fields),
        )
        for field_path in todo_fields:
            logger.warning("  → %s", field_path)


def _find_todos(obj, path: str, results: list[str]) -> None:
    """Recursively find values that start with 'TODO'."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            _find_todos(value, f"{path}.{key}" if path else key, results)
    elif isinstance(obj, str) and obj.startswith("TODO"):
        results.append(path)


def get_spend_to_cell_mapping(mapping: dict) -> dict[str, dict]:
    """Build the mapping from spend keys to Excel coordinates.

    Returns a dict like:
        {
            "google_ads_vosker": {
                "sheet": "Vosker",           # from mapping["vosker"]["sheet_name"]
                "label": "Google Ads",       # from mapping["vosker"]["google_ads_label"]
            },
            "facebook_ads_spypoint": {
                "sheet": "SpyPoint",
                "label": "Meta Ads",
            },
            ...
        }

    The sharepoint module uses this to:
      1. Find the sheet by name
      2. Find the row by matching the label in the labels column
      3. Find the column by matching yesterday's date in the date row
    """
    vosker = mapping.get("vosker", {})
    spypoint = mapping.get("spypoint", {})

    return {
        "google_ads_vosker": {
            "sheet": vosker.get("sheet_name", ""),
            "label": vosker.get("google_ads_label", ""),
        },
        "facebook_ads_vosker": {
            "sheet": vosker.get("sheet_name", ""),
            "label": vosker.get("facebook_ads_label", ""),
        },
        "microsoft_ads_vosker": {
            "sheet": vosker.get("sheet_name", ""),
            "label": vosker.get("microsoft_ads_label", ""),
        },
        "tiktok_ads_vosker": {
            "sheet": vosker.get("sheet_name", ""),
            "label": vosker.get("tiktok_ads_label", ""),
        },
        "google_ads_spypoint": {
            "sheet": spypoint.get("sheet_name", ""),
            "label": spypoint.get("google_ads_label", ""),
        },
        "facebook_ads_spypoint": {
            "sheet": spypoint.get("sheet_name", ""),
            "label": spypoint.get("facebook_ads_label", ""),
        },
        "microsoft_ads_spypoint": {
            "sheet": spypoint.get("sheet_name", ""),
            "label": spypoint.get("microsoft_ads_label", ""),
        },
    }
