# RadarDev

> **Self-healing hackathon opportunity intelligence powered by Bright Data**

**RadarDev** or **OpportunityRadar** discovers hackathon opportunities from the public web, turns them into structured records, monitors the quality of the collected data, and provides an approval-based self-healing workflow when the scraper needs repair.

**Live demo:** https://radardev.onrender.com/

---

## What RadarDev does

RadarDev is built around a simple pipeline:

```text
Public Hackathon Web
        │
        ▼
Bright Data Scraper Studio
        │
        ▼
Structured Hackathon Records
        │
        ▼
RadarDev Health Monitoring
        │
        ├── Healthy ───────────────► Dashboard
        │
        └── Degraded
                │
                ▼
        AI-assisted self-healing
                │
                ▼
        Human approval
                │
                ▼
        Bright Data CLI
                │
                ▼
        Repaired scraper
```

The application currently demonstrates this workflow with hackathon data, including fields such as title, dates, organizer, location, participation information, and source links.

---

## Key features

- **Hackathon discovery** from public web pages through Bright Data Scraper Studio.
- **Structured records** consumed by the RadarDev application.
- **Search, filtering, and sorting** for hackathon opportunities.
- **Data-quality monitoring** with a visible health score.
- **Self-healing workflow** for scraper degradation.
- **Human-in-the-loop approval** before a proposed repair is accepted.
- **Bright Data CLI integration** for scraper operations and healing.
- **Production deployment** on Render.
- **Environment-based secrets** so API credentials are not committed to Git.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Frontend | HTML, CSS, JavaScript |
| Web extraction | Bright Data Scraper Studio |
| Scraper control / healing | Bright Data CLI |
| Configuration | `.env` / environment variables |
| Dependency management | `requirements.txt` |
| Deployment | Render |
| Containerization | Docker |

---

## Repository structure

```text
RADARDEV/
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── .env
├── .env.sample
├── .gitignore
├── app.py
├── approve.json
├── Dockerfile
├── heal.json
├── opportunities.json
├── README.md
└── requirements.txt
```

### Generated/runtime files

`heal.json`, `approve.json`, and similar generated output files are runtime artifacts from the self-healing workflow. They should not contain secrets.

The `.gitignore` also protects local development artifacts such as:

```text
.venv/
__pycache__/
*.pyc
.env
.vscode/
heal.json
approve.json
```

---

# Setup

## 1. Prerequisites

Install:

- Python 3.10+ (the project was developed and tested with Python 3.10/3.11)
- Node.js 20+ for the Bright Data CLI
- Git
- A Bright Data account
- A Bright Data Scraper Studio collector configured for the target hackathon pages

The Bright Data CLI documentation currently recommends Node.js 20+ and supports Windows, macOS, Linux, and WSL.

Bright Data CLI:
https://brightdata.com/blog/ai/bright-data-cli

Scraper Studio:
https://brightdata.com/products/web-scraper/studio

---

## 2. Clone the repository

```bash
git clone https://github.com/KamranX07/RadarDev.git
cd RadarDev
```

---

## 3. Create a Python virtual environment

### Windows — Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### Windows — PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

The current dependency file contains:

```text
Flask==3.1.3
python-dotenv
requests
```

---

# Bright Data configuration

RadarDev needs the Bright Data credentials and collector identifier used by the application.

Create a local `.env` file from the provided example:

```bash
cp .env.sample .env
```

On Windows, you can also simply copy `.env.sample` to `.env` using your editor.

Set the required values:

```env
BRIGHTDATA_API_KEY=your_bright_data_api_key
BRIGHTDATA_COLLECTOR_ID=your_bright_data_collector_id
```

### Important

**Never commit `.env` to Git.**

The repository's `.gitignore` excludes it intentionally.

Use `.env.sample` as the template for another developer or judge.

---

# Install and verify the Bright Data CLI

RadarDev invokes the Bright Data CLI from Python during the scraper healing workflow.

On Windows:

```bash
npm install -g @brightdata/cli
```

Then authenticate/configure the CLI:

```bash
brightdata login
```

Verify that the CLI is available:

```bash
bdata --version
```

or:

```bash
brightdata --version
```

The RadarDev backend also performs executable discovery so that Windows installations exposing `bdata.cmd` can be found correctly.

Bright Data's current CLI documentation:
https://brightdata.com/blog/ai/bright-data-cli

---

# Run RadarDev locally

With the virtual environment activated:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

If your environment uses a different Flask startup command, use the command defined by the current `Dockerfile`/application entry point.

---

# Verify the health endpoint

RadarDev exposes a health endpoint:

```text
GET /health
```

For a local server:

```text
http://127.0.0.1:5000/health
```

A healthy response looks like:

```json
{
  "checked_at": "2026-08-23T10:37:10",
  "data_quality": 99.0,
  "missing_required_fields": [],
  "optional_missing": 6,
  "records": 29,
  "status": "healthy"
}
```

The exact values will change as the underlying data changes.

The health monitor is responsible for checking the quality of the structured records rather than simply assuming that a scraper succeeded because a command returned data.

---

# Self-healing workflow

The self-healing feature is the core reliability feature of RadarDev.

The workflow is:

```text
1. Detect degraded scraper output
              ↓
2. Set healing state to "healing"
              ↓
3. Invoke Bright Data CLI
              ↓
4. Run the scraper healing operation
              ↓
5. Save the proposed repair
              ↓
6. Set state to "approval_required"
              ↓
7. Human reviews the repair
              ↓
8. Human approves
              ↓
9. Bright Data CLI applies the approval
              ↓
10. Set state to "done"
              ↓
11. Dashboard reports the scraper as repaired
```

### Why approval is required

RadarDev deliberately does not silently modify the scraper.

The proposed repair is first surfaced for review:

```text
AI repair is ready for review.
```

After approval:

```text
AI repair approved successfully.
```

The dashboard then reflects the repaired state.

This gives the system an explicit **human-in-the-loop safety boundary** between automated repair generation and applying that repair.

---

# How the healing integration works

The Flask application resolves the Bright Data CLI executable before invoking it.

Conceptually:

```python
bdata_command = (
    shutil.which("bdata")
    or shutil.which("bdata.cmd")
)
```

The healing command is then assembled and executed through Python's subprocess support.

The important properties are:

- No hard-coded path to the developer's local Bright Data installation.
- Windows `.cmd` resolution is supported.
- CLI stdout/stderr are captured.
- Non-zero return codes become visible application errors.
- Successful healing transitions the application into an approval-required state.
- Approval is a separate explicit operation.

This was important during development because the CLI worked directly in the terminal while Python initially could not resolve the same executable on Windows.

---

# Scraper health

RadarDev separates **scraper execution** from **data quality**.

A scraper can technically return data while still producing incomplete records.

For example, during development we encountered a situation where `start_date` was intermittently missing even though the scraper continued to return records.

The health monitor therefore checks the resulting structured dataset and reports:

- record count
- data-quality percentage
- missing required fields
- optional missing fields
- health status
- check timestamp

This makes silent scraper degradation visible to the application.

---

# API endpoints

The Flask application provides the dashboard and backend endpoints used by the frontend.

The health endpoint is:

```text
GET /health
```

The self-healing workflow includes:

```text
POST /api/scraper-heal/approve
```

and a progress/status endpoint under:

```text
/api/scraper-heal/progress
```

The exact implementation is available directly in `app.py`.

---

# Deployment

RadarDev is deployed on Render.

Production:

https://radardev.onrender.com/

The deployment requires the same runtime configuration as local execution, especially:

```text
BRIGHTDATA_API_KEY
BRIGHTDATA_COLLECTOR_ID
```

These should be configured as **Render environment variables**, not committed to the repository.

The repository also includes:

```text
Dockerfile
```

for container-based deployment.

---

# Docker

Docker support is included in the repository.

Build:

```bash
docker build -t radardev .
```

Run:

```bash
docker run --env-file .env -p 5000:5000 radardev
```

Then open:

```text
http://127.0.0.1:5000/
```

> If you are using the Render deployment, you do not need Docker locally. The production deployment can build from the repository's Docker configuration.

---

# Reproducing the demo

After configuring Bright Data and starting RadarDev:

### 1. Open the dashboard

```text
http://127.0.0.1:5000/
```

### 2. Verify the data

Confirm that hackathon opportunity cards are displayed.

### 3. Check health

Open:

```text
http://127.0.0.1:5000/health
```

Confirm that the endpoint returns JSON with a health status and data-quality score.

### 4. Run the scraper/healing workflow

Use the dashboard's scraper health/self-healing controls.

When a repair is generated, RadarDev should transition to:

```text
approval_required
```

### 5. Review and approve

Review the proposed repair and approve it.

The successful state is:

```text
status: done
```

and the dashboard reports:

```text
AI repair approved successfully.
```

The self-healing card can then show the repaired state.

---

# Troubleshooting

## `bdata` is not recognized

Check:

```bash
bdata --version
```

and:

```bash
brightdata --version
```

On Windows, verify that the npm global binary directory is on `PATH`.

RadarDev also checks for:

```text
bdata
bdata.cmd
```

because Windows may expose the executable as a `.cmd` shim.

---

## Bright Data collector ID is missing

Verify that `.env` contains:

```env
BRIGHTDATA_COLLECTOR_ID=...
```

and restart the Flask application after changing environment variables.

---

## Bright Data API key is missing

Verify:

```env
BRIGHTDATA_API_KEY=...
```

Do not paste the key into `app.py` or commit it to Git.

---

## `/health` shows an error

Open the endpoint directly:

```text
http://127.0.0.1:5000/health
```

The JSON response includes diagnostic information such as missing required fields and the current record count.

---

## Self-healing takes a long time

Healing is an external operation and can take longer than normal application requests.

Check the dashboard's healing/progress state and inspect the CLI output captured by the Flask application.

Do not assume that a long-running operation means that the underlying scraper is permanently broken.

---

# Security

Never commit:

```text
.env
```

or API credentials.

Use environment variables for:

```text
BRIGHTDATA_API_KEY
BRIGHTDATA_COLLECTOR_ID
```

The repository intentionally excludes `.env` through `.gitignore`.

If an API key is accidentally exposed, rotate it immediately in Bright Data.

---

# Design principles

RadarDev follows a few principles that shaped the implementation:

### 1. Don't trust scraper success blindly

A successful scraper process does not necessarily mean that the data is complete.

### 2. Preserve existing fields

The healing prompt explicitly asks the repair process to preserve existing fields and avoid renaming/removing them.

### 3. Human approval before repair

Automated repair generation is useful, but applying a scraper change is a meaningful production operation. RadarDev therefore puts a human approval step between proposed repair and application.

### 4. Keep environment-specific configuration outside the code

Credentials and local executable paths should never be hard-coded.

### 5. Handle platform differences

The Bright Data CLI is discovered dynamically rather than relying on a developer-specific Windows path.

---

# Why Bright Data Scraper Studio?

Scraper Studio is the extraction layer that turns the public hackathon web into structured data consumed by RadarDev.

Its self-healing capability is particularly important to this project because the scraper is treated as a living component of the application rather than a one-time script.

Bright Data describes Scraper Studio as supporting AI-generated scrapers, structured data delivery, monitoring, and self-healing workflows.

Learn more:

https://brightdata.com/products/web-scraper/studio

---

# Project outcome

RadarDev demonstrates a complete data reliability loop:

```text
DISCOVER
   ↓
SCRAPE
   ↓
STRUCTURE
   ↓
MONITOR
   ↓
DETECT
   ↓
HEAL
   ↓
APPROVE
   ↓
RECOVER
```

The result is a hackathon opportunity platform where the data collection layer is not treated as a fragile black box.

---

# Live project

**Production:** https://radardev.onrender.com/

**Source:** https://github.com/KamranX07/RadarDev

---

## Built for Scrape Verse Hackathon

RadarDev was built to demonstrate practical use of Bright Data Scraper Studio, the Bright Data CLI, structured web data, and an approval-based self-healing workflow.
