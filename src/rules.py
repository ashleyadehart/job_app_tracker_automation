from __future__ import annotations

from datetime import date, datetime
import pandas as pd

ACTIVE_STATUSES = {"Applied", "Interviewing", "Offer"}


def _to_date(iso_str: str | None) -> date | None:
    if not iso_str or pd.isna(iso_str):
        return None
    try:
        return datetime.fromisoformat(str(iso_str)).date()
    except Exception:
        return None


def add_flags(df: pd.DataFrame, followup_days: int = 10, stale_days: int = 21) -> pd.DataFrame:
    """
    Adds computed columns and flags:
    - days_since_applied
    - days_since_contact
    - missing fields flags
    - followup due flag
    - stale flag
    """
    out = df.copy()
    today = date.today()

    applied = out["applied_date"].map(_to_date)
    last_contact = out["last_contact_date"].map(_to_date)

    out["days_since_applied"] = applied.map(lambda d: (today - d).days if d else None)
    out["days_since_contact"] = last_contact.map(lambda d: (today - d).days if d else None)

    # Missing info flags
    out["flag_missing_link"] = out["job_posting_url"].isna() | (out["job_posting_url"].astype(str).str.strip() == "")
    out["flag_missing_status"] = out["status"].isna() | (out["status"].astype(str).str.strip() == "")
    out["flag_missing_contact"] = out["contact_email"].isna() | (out["contact_email"].astype(str).str.strip() == "")

    def followup_due(row) -> bool:
        status = str(row.get("status") or "").strip()
        if status not in ACTIVE_STATUSES:
            return False

        dsa = row.get("days_since_applied")
        dsc = row.get("days_since_contact")

        if dsa is None:
            return False

        # If never contacted since applying, use days since applied
        if dsc is None:
            return dsa >= followup_days

        # Otherwise, use days since contact
        return dsc >= followup_days

    out["flag_followup_due"] = out.apply(followup_due, axis=1)

    def stale(row) -> bool:
        status = str(row.get("status") or "").strip()
        if status not in ACTIVE_STATUSES:
            return False

        dsa = row.get("days_since_applied")
        dsc = row.get("days_since_contact")

        if dsc is not None:
            return dsc >= stale_days

        return (dsa is not None) and (dsa >= stale_days)

    out["flag_stale"] = out.apply(stale, axis=1)

    return out
