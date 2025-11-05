# Reusable cleaning utility to clean phone numbers, dates, ect...

import re 
import pandas as pd

# 1) Clean Phone Numbers

# Precompile: replace any non-digit character with nothing
_DIGIT_RE = re.compile(r"\D+")

# keep only the digits from a value (handles None/NaN)
def only_digits(v) -> str:
    """Return only the digits; missing values become ''."""
    if pd.isna(v):
        return ""
    return _DIGIT_RE.sub("", str(v))

# Normalize a US phone to E.164 + display + validity
def normalize_us_phone(raw, country_code: str = "1") -> dict:
    """Return dict: e164, display, is_valid, digits."""
    d = only_digits(raw)

    # Strip leading country code if present
    if len(d) == 11 and d.startswith(country_code):
        d = d[1:]

    # Valid US number = exactly 10 digits
    is_valid = len(d) == 10

    # Build outputs only if valid
    e164 = f"+{country_code}{d}" if is_valid else ""
    display = f"+({d[0:3]}) {d[3:6]}-{d[6:10]}" if is_valid else ""

    return {"e164": e164, "display": display, "is_valid": is_valid, "digits": d}

# 2) Clean Dates

# Parse mixed date strings to pandas datetime; invalid -> NaT
def parse_subscription_date(values):
    """Return pandas datetime Series/Index; bad inputs become NaT."""
    return pd.to_datetime(values, errors="coerce")

# 3) Data Health Check

# Build a quick text summary of invalid phones and dates
def dq_summary(df,
               phone1_flag="phone1_is_valid",
               phone2_flag="phone2_is_valid",
               dt_col="subscription_dt") -> str:
    """Return a one-block text summary of key DQ rates."""
    total = len(df)
    bad_p1 = (~df[phone1_flag]).sum() if phone1_flag in df else 0
    bad_p2 = (~df[phone2_flag]).sum() if phone2_flag in df else 0
    bad_dt = df[dt_col].isna().sum() if dt_col in df else 0

    pct = lambda n: f"{(n/total if total else 0):.2%}"
    return (
        "=== DQ Summary ===\n"
        f"Rows: {total:,}\n"
        f"Phone1 invalid: {bad_p1:,} ({pct(bad_p1)})\n"
        f"Phone2 invalid: {bad_p2:,} ({pct(bad_p2)})\n"
        f"Subscription Date null/invalid: {bad_dt:,} ({pct(bad_dt)})"
    )
