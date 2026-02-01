from __future__ import annotations

import pandas as pd
from dateutil.parser import parse

REQUIRED_COLUMNS = [
    "company",
    "role",
    "location",
    "applied_date",
    "status",
    "last_contact_date",
    "contact_name",
    "contact_email",
    "job_posting_url",
    "notes",
]


def _safe_parse_date(value) -> str | None:
    """
    Parse many date formats into ISO (YYYY-MM-DD). Return None if blank/invalid.
    """
    if pd.isna(value) or str(value).strip() == "":
        return None
    try:
        dt = parse(str(value), fuzzy=True)
        return dt.date().isoformat()
    except Exception:
        return None


def clean_applications(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize schema and normalize common fields.
    - Ensures required columns exist
    - Trims whitespace, normalizes status
    - Parses dates to ISO format
    """
    # Ensure required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    out = df.copy()

    # Standardize text fields (avoid "nan" strings later)
    out["company"] = out["company"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    out["role"] = out["role"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    out["location"] = out["location"].astype(str).str.strip()

    # Normalize status
    out["status"] = out["status"].astype(str).str.strip().str.title()
    status_map = {
        "Applied": "Applied",
        "Interviewing": "Interviewing",
        "Offer": "Offer",
        "Rejected": "Rejected",
        "Withdrawn": "Withdrawn",
    }
    out["status"] = out["status"].map(lambda s: status_map.get(s, s))

    # Parse dates
    out["applied_date"] = out["applied_date"].map(_safe_parse_date)
    out["last_contact_date"] = out["last_contact_date"].map(_safe_parse_date)

    # Clean emails/urls/notes
    out["contact_name"] = out["contact_name"].astype(str).str.strip()
    out["contact_email"] = out["contact_email"].astype(str).str.strip()
    out["job_posting_url"] = out["job_posting_url"].astype(str).str.strip()
    out["notes"] = out["notes"].astype(str).str.strip()

    # Convert common string nulls back to None
    out = out.replace({"nan": None, "None": None, "": None})

    return out
