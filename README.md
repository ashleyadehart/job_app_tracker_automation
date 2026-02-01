# Job Application Tracker Automation (Python)

## Overview
This project is a **Python-based automation tool** that helps track and manage job applications using a simple CSV file.  
It automates data cleaning, validation, rule-based flagging, and report generation to provide clear insights into a job search pipeline.

The tool is designed to be run from the command line and produces clean, shareable outputs that summarize application status, follow-up needs, and stale applications.

---

## Features
- Command-line interface (CLI) using `argparse`
- Automated data cleaning and normalization
- Rule-based flags for:
  - Follow-up due
  - Stale applications
  - Missing recruiter/contact information
- Generates multiple outputs:
  - Cleaned CSV file
  - Human-readable Markdown summary
  - Machine-readable JSON dashboard
- Structured logging for traceability and debugging
- Modular, reusable Python codebase

---

## Project Structure
```text
job-app-tracker-automation/
├─ data/
│  └─ applications.csv          # Sample (anonymized) input data
├─ outputs/
│  ├─ cleaned_applications.csv  # Cleaned and enriched dataset
│  ├─ summary.md                # Human-readable report
│  └─ dashboard.json            # Aggregated metrics (JSON)
├─ logs/
│  └─ job_tracker.log           # Execution logs
├─ src/
│  ├─ __init__.py
│  ├─ job_tracker.py            # CLI entry point
│  ├─ cleaning.py               # Data cleaning and normalization
│  ├─ rules.py                  # Business logic and flags
│  ├─ reporting.py              # Report generation
│  └─ utils.py                  # Logging and utilities
├─ tests/
│  └─ (unit tests)
├─ requirements.txt
└─ README.md

---

## How It Works
```markdown
## How It Works
1. Reads a CSV file of job applications.
2. Standardizes column structure and cleans text fields.
3. Parses dates into a consistent ISO format.
4. Calculates:
   - Days since application
   - Days since last contact
5. Flags applications that:
   - Need follow-up
   - Are stale
   - Are missing key information
6. Writes cleaned data, summary reports, and logs to disk.

---

## How to Run
### 1. Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

---

## Install the Dependencies
This project uses a Python virtual environment to isolate dependencies.
### 1. From the project root:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
### 2. Install required packages
python -m pip install -r requirements.txt

---

## Run the Automation
Once dependencies are installed and the virtual environment is active, run the automation from the project root:
```powershell
python -m src.job_tracker --input data/applications.csv --output outputs

---

## Example Output
After running the script, the `outputs/summary.md` file includes:
- Total number of applications
- Status breakdown (Applied, Interviewing, Rejected, etc.)
- List of applications that require follow-up
- List of stale applications
This provides a quick, readable snapshot of the job search pipeline.

---

## Data Privacy
- The included `applications.csv` file contains **fully anonymized, sample data**.
- Personal job search data should **not** be committed to version control.
- Users are encouraged to keep real data local only.

---

## Skills Demonstrated
- Python automation and scripting
- CLI development with `argparse`
- Data processing with `pandas`
- Rule-based logic and validation
- File system operations
- Logging and debugging
- Modular project design
- Virtual environment management
- Git and GitHub workflow

---

## Future Enhancements
- Email follow-up template generation
- CSV export of follow-ups due
- Visualization dashboard (charts)
- Google Sheets integration
- GitHub Actions for automated testing
- Configuration via YAML or JSON