from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from .cleaning import clean_applications
from .rules import add_flags
from .reporting import write_summary_md, write_dashboard_json
from .utils import get_logger, ensure_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Job Application Tracker Automation: clean, flag, and report on your job applications CSV."
    )
    parser.add_argument("--input", required=True, help="Path to applications CSV (e.g., data/applications.csv)")
    parser.add_argument("--output", required=True, help="Output folder (e.g., outputs)")
    parser.add_argument("--followup-days", type=int, default=10, help="Days after applying to flag follow-up due")
    parser.add_argument("--stale-days", type=int, default=21, help="Days since last contact to flag stale")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger = get_logger(log_path="logs/job_tracker.log")
    ensure_dirs(["outputs", "logs"])

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    logger.info("Loading input CSV: %s", input_path)
    df = pd.read_csv(input_path)

    logger.info("Cleaning/standardizing fields...")
    df_clean = clean_applications(df)

    logger.info("Applying rules & flags...")
    df_flagged = add_flags(df_clean, followup_days=args.followup_days, stale_days=args.stale_days)

    output_dir.mkdir(parents=True, exist_ok=True)

    cleaned_path = output_dir / "cleaned_applications.csv"
    summary_path = output_dir / "summary.md"
    dashboard_path = output_dir / "dashboard.json"

    logger.info("Saving cleaned CSV: %s", cleaned_path)
    df_flagged.to_csv(cleaned_path, index=False)

    logger.info("Writing summary report: %s", summary_path)
    write_summary_md(df_flagged, summary_path, followup_days=args.followup_days, stale_days=args.stale_days)

    logger.info("Writing dashboard JSON: %s", dashboard_path)
    write_dashboard_json(df_flagged, dashboard_path)

    logger.info("Done. Outputs saved to: %s", output_dir.resolve())


if __name__ == "__main__":
    main()
