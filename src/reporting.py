from __future__ import annotations

import json
from pathlib import Path
import pandas as pd


def write_summary_md(df: pd.DataFrame, path: Path, followup_days: int, stale_days: int) -> None:
    total = len(df)
    by_status = df["status"].fillna("Unknown").value_counts().to_dict()

    followups = df[df["flag_followup_due"] == True]  # noqa: E712
    stales = df[df["flag_stale"] == True]  # noqa: E712

    lines: list[str] = []
    lines.append("# Job Application Tracker Summary\n")
    lines.append(f"- Total applications: **{total}**")
    lines.append(f"- Follow-up threshold: **{followup_days} days**")
    lines.append(f"- Stale threshold: **{stale_days} days**\n")

    lines.append("## Status Breakdown")
    for k, v in by_status.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    lines.append("## Follow-up Due")
    if followups.empty:
        lines.append("- None 🎉")
    else:
        for _, r in followups.iterrows():
            lines.append(
                f"- {r.get('company')} — {r.get('role')} "
                f"(days since applied: {r.get('days_since_applied')}, days since contact: {r.get('days_since_contact')})"
            )
    lines.append("")

    lines.append("## Stale Applications")
    if stales.empty:
        lines.append("- None 🎉")
    else:
        for _, r in stales.iterrows():
            lines.append(
                f"- {r.get('company')} — {r.get('role')} "
                f"(days since contact: {r.get('days_since_contact')})"
            )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_dashboard_json(df: pd.DataFrame, path: Path) -> None:
    payload = {
        "total": int(len(df)),
        "status_counts": df["status"].fillna("Unknown").value_counts().to_dict(),
        "followup_due_count": int((df["flag_followup_due"] == True).sum()),  # noqa: E712
        "stale_count": int((df["flag_stale"] == True).sum()),  # noqa: E712
        "missing_link_count": int((df["flag_missing_link"] == True).sum()),  # noqa: E712
        "missing_contact_count": int((df["flag_missing_contact"] == True).sum()),  # noqa: E712
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    