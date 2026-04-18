# Project Management Dashboard

A web-based project management tool built with Flask and Dash. It provides an interactive dashboard for tracking milestones, managing project documents, and generating downloadable reports.

## Features

- **Project Charter** — View project status and milestone overview
- **Interactive Gantt Chart** — Add and visualize tasks on a timeline using Plotly/Dash
- **Milestones Tracker** — Monitor project phases and completion status
- **Budget, WBS, AOA, SOW** — Dedicated pages for core project management artifacts
- **Risk Register** — Track project risks
- **Team Management** — View and manage team members
- **Report Generation** — Generate and download Word (.docx) reports:
  - Status Report
  - Progress Report
- **Project Review** — Consolidated review page

## Tech Stack

- **Backend:** Python, Flask
- **Dashboard:** Dash, Plotly
- **UI:** Bootstrap (via dash-bootstrap-components)
- **Data:** pandas
- **Document Export:** python-docx

## Getting Started

### Prerequisites

```bash
pip install flask dash dash-bootstrap-components pandas plotly python-docx
```

### Run the App

```bash
python app.py
```

The app runs at `http://localhost:5000` by default. The interactive Gantt dashboard is available at `/dashboard/`.

## Pages

| Route | Description |
|---|---|
| `/index.html` | Home |
| `/charter.html` | Project charter and status |
| `/milestones.html` | Milestone tracker |
| `/budget.html` | Budget overview |
| `/wbs.html` | Work Breakdown Structure |
| `/aoa.html` | Activity on Arrow diagram |
| `/sow.html` | Statement of Work |
| `/risks.html` | Risk register |
| `/reports.html` | Report generation |
| `/team.html` | Team page |
| `/review.html` | Project review |
| `/dashboard/` | Interactive Gantt chart (Dash) |
