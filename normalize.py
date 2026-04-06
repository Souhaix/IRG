"""Normalize spend values to clean floats.

Handles various locale-specific formats:
  "1 228,25"  → 1228.25
  "1,228.25"  → 1228.25
  "1228.25"   → 1228.25
  "1228,25"   → 1228.25
  "$1,228.25" → 1228.25
"""


def normalize_spend(value) -> float:
    """Convert a raw spend value (str, int, float) to a clean float.

    Rules:
    - Strip any currency symbols and whitespace
    - Detect comma-as-decimal vs comma-as-thousands
    - Return a plain float with dot as decimal separator
    - Never apply currency conversion
    """
    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        return 0.0

    s = value.strip()
    if not s:
        return 0.0

    # Remove currency symbols and non-breaking spaces
    for char in ("$", "€", "£", "\u00a0", "\u202f"):
        s = s.replace(char, "")

    # Remove regular spaces (thousands separator like "1 228,25")
    s = s.replace(" ", "")

    # Determine if comma is decimal separator or thousands separator
    has_comma = "," in s
    has_dot = "." in s

    if has_comma and has_dot:
        # Both present: whichever comes last is the decimal separator
        last_comma = s.rfind(",")
        last_dot = s.rfind(".")
        if last_comma > last_dot:
            # "1.228,25" → comma is decimal
            s = s.replace(".", "").replace(",", ".")
        else:
            # "1,228.25" → dot is decimal
            s = s.replace(",", "")
    elif has_comma and not has_dot:
        # Only comma: check if it's a decimal separator
        # "1228,25" → decimal  |  "1,228" → thousands (no decimals)
        parts = s.split(",")
        if len(parts) == 2 and len(parts[1]) <= 2:
            # Likely decimal separator: "1228,25"
            s = s.replace(",", ".")
        else:
            # Likely thousands separator: "1,228,000"
            s = s.replace(",", "")
    # If only dot or neither: no transformation needed

    return float(s)
