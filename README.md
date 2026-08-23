# 🚀 OpportunityRadar

> **Find the right hackathon. Faster.**

OpportunityRadar is an intelligent hackathon discovery platform that turns live web data into a searchable, structured opportunity feed.

Instead of manually searching dozens of hackathon pages, users can discover opportunities through a single dashboard with search, filtering, sorting, live data refresh, scraper health monitoring, and an AI-assisted self-healing workflow.

---

## 🎯 The Problem

Hackathon opportunities are scattered across different pages and platforms.

Finding the right opportunity often means:

- Searching multiple websites
- Comparing different event pages
- Checking whether opportunities are still active
- Manually tracking dates and participation
- Repeating the process whenever the underlying websites change

OpportunityRadar turns this fragmented discovery process into a single intelligent interface.

---

## 💡 The Solution

OpportunityRadar transforms web data into structured hackathon opportunities.

The system:

1. Collects hackathon data through **Bright Data Scraper Studio**
2. Structures the collected records
3. Stores the resulting opportunity data
4. Presents the data through a searchable dashboard
5. Monitors scraper health and data quality
6. Detects degraded extraction
7. Initiates an AI-assisted scraper healing workflow
8. Requests human approval before committing a proposed repair
9. Applies the approved repair through the Bright Data CLI

### Core Workflow

```text
Web Discovery
      ↓
Bright Data Scraper Studio
      ↓
Structured Hackathon Records
      ↓
OpportunityRadar Dashboard
      ↓
Health Monitoring
      ↓
AI-Assisted Self-Healing
      ↓
Human Approval
      ↓
Bright Data Repair
      ↓
Healthy Scraper
```

---

## ⚡ Why OpportunityRadar?

OpportunityRadar isn't simply a list of scraped hackathons.

It combines **discovery + data quality + reliability** into one product.

The system is designed to answer two questions:

> **What opportunities are available?**

and

> **Can I trust the data powering this dashboard?**

That second question drives the self-healing architecture.

---

## 🛡️ Self-Healing Scraper

Web scrapers can break when websites change.

OpportunityRadar includes a health monitoring and self-healing workflow designed to detect these problems and recover the scraper.

### Healing Workflow

```text
Check & Repair Scraper
        ↓
Scraper Health Analysis
        ↓
AI Repair Proposal
        ↓
Human Review
        ↓
Approve Repair
        ↓
Bright Data CLI
        ↓
Repaired Scraper
```

The repair process intentionally includes a human approval gate.

This prevents an AI-generated scraper modification from being silently committed without user approval.

---

## 👤 Human-in-the-Loop Approval

When a repair is proposed, OpportunityRadar moves into a review state.

The user sees:

```text
AI repair is ready for review.
```

The user can then approve the proposed repair.

The application sends the approval to the backend, which invokes the Bright Data CLI:

```bash
bdata.cmd scraper approve
```

Once the operation succeeds, the dashboard reports:

```text
✅ AI repair approved successfully.
```

and the self-healing status becomes:

```text
Repaired
```

---

## 🌐 Bright Data Integration

Bright Data is a core part of OpportunityRadar's data infrastructure.

The project uses **Bright Data Scraper Studio** for web data collection and the **Bright Data CLI** for scraper healing and approval operations.

Bright Data provides the collection and recovery layer while OpportunityRadar provides the discovery experience, monitoring, and user-facing intelligence layer.

---

## 📊 Dashboard

The OpportunityRadar dashboard provides:

- 🔎 Hackathon search
- 🎛️ Mode filtering
- 🟢 Status filtering
- ↕️ Sorting
- 🔄 Live data refresh
- 📈 Scraper health visibility
- 🛡️ Self-healing status
- 🧩 Structured opportunity cards
- 📱 Responsive interface
- 🔗 Direct links to hackathon opportunities

### System Status

The dashboard exposes the health of the underlying data pipeline directly to the user.

Example:

```text
29 Opportunities
99% Scraper Health
Ready / Repaired
Bright Data
```

---

## 🔄 Live Data Pipeline

OpportunityRadar makes the underlying data flow visible:

```text
Web discovery
      →
Bright Data
      →
Structured records
      →
Health monitoring
      →
Self-healing
```

This makes the system's reliability understandable without exposing users to unnecessary implementation details.

---

## 🧰 Tech Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Data & Scraping

- Bright Data Scraper Studio
- Bright Data CLI
- Structured JSON data

### Reliability

- Scraper health monitoring
- Data-quality evaluation
- AI-assisted scraper healing
- Human approval workflow

---

## 🖥️ Running Locally

### Requirements

- Python 3
- Node.js / npm
- Bright Data CLI
- Bright Data credentials/configuration

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Bright Data CLI

```bash
npm install -g @brightdata/cli
```

Verify the CLI:

```bash
bdata --version
```

### Start the Application

Run the Flask application using the project's configured startup command.

Then open:

```text
http://127.0.0.1:5000/
```

---

## 🔐 Configuration

The application expects the required Bright Data configuration to be available through the project's environment/configuration setup.

Do not commit credentials or private API keys to the repository.

---

## 🎬 Demo Flow

The strongest way to demonstrate OpportunityRadar is:

### 1. Discover

Open the dashboard and show the live hackathon feed.

### 2. Search

Search for a specific opportunity or theme.

### 3. Filter

Use mode and status filters to narrow the results.

### 4. Refresh

Click:

**Refresh Data**

and demonstrate the live data refresh process.

### 5. Monitor

Show:

**Scraper Health — 99%**

and the live data pipeline.

### 6. Heal

Click:

**Check & Repair Scraper**

and show the system detecting that a repair is required.

### 7. Review

The system presents an AI-generated repair for human approval.

### 8. Approve

Approve the proposed repair through the OpportunityRadar interface.

### 9. Recover

Show:

**Self-Healing — Repaired**

This demonstrates the complete:

```text
Discover → Structure → Monitor → Detect → Heal → Approve → Recover
```

workflow.

---

## 🏆 What Makes It Different

OpportunityRadar combines a useful consumer-facing experience with infrastructure reliability.

Most opportunity discovery tools stop at:

```text
Scrape → Display
```

OpportunityRadar goes further:

```text
Scrape
  ↓
Structure
  ↓
Monitor
  ↓
Detect problems
  ↓
Generate repair
  ↓
Request approval
  ↓
Repair
  ↓
Recover
```

The result is an opportunity discovery system designed to remain useful even when the underlying web extraction process changes.

---

## 🌟 Product Experience

OpportunityRadar is designed to make complex data infrastructure understandable through a simple interface.

The dashboard provides:

- A live opportunity feed
- Visual scraper-health status
- Self-healing visibility
- Human-controlled repair approval
- Real-time refresh feedback
- Responsive opportunity cards
- Clear data pipeline visualization

The interface turns an otherwise invisible scraping infrastructure into something users can understand and trust.

---

## 🚀 Project Vision

OpportunityRadar can evolve beyond hackathons into a broader opportunity intelligence platform.

The same architecture can support discovery of:

- Hackathons
- Grants
- Fellowships
- Competitions
- Developer programs
- Startup opportunities
- Open-source programs

The long-term vision is an intelligent radar for opportunities across the web — with reliability built into the system rather than treated as an afterthought.

---

## 🏁 Current Implementation

The current implementation demonstrates a complete working loop:

```text
Live Web Data
      ↓
Bright Data Scraper Studio
      ↓
Structured Opportunities
      ↓
OpportunityRadar Dashboard
      ↓
Search / Filter / Sort
      ↓
Scraper Health Monitoring
      ↓
AI-Assisted Repair
      ↓
Human Approval
      ↓
Bright Data CLI
      ↓
Repaired Scraper
```

The complete self-healing workflow has been tested end-to-end, including the human approval step and successful repair confirmation.

---

## 📜 License

Add the project's chosen license here.
