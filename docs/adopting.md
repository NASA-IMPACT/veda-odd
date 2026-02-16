# Adopting the VEDA-ODD Reporting Structure

This guide walks through how to adopt the automated reporting system used by VEDA-ODD for your own team or project. The system tracks open-source contributions across GitHub repositories, generates visualizations, and publishes a documentation site -- all driven by GitHub Issues and Actions.

## Overview

The reporting structure ties together four pieces:

1. **GitHub Issues** define quarterly objectives, contributors, and repositories.
2. **Python scripts** query the GitHub API for commit data and generate charts and documentation.
3. **GitHub Actions** run the scripts on a schedule and open a PR with the results.
4. **MkDocs** publishes the documentation site to GitHub Pages.

```
GitHub Issues (labeled objectives)
        │
        ▼
┌──────────────────┐   weekly cron
│  generate_config │◄──────────────── GitHub Actions
└────────┬─────────┘
         ▼
┌──────────────────┐
│     main.py      │  query commits via GitHub API
└────────┬─────────┘
         ▼
┌──────────────────┐
│     plot.py      │  create bar chart (matplotlib)
└────────┬─────────┘
         ▼
┌──────────────────┐
│  generate_docs   │  write objectives.md
└────────┬─────────┘
         ▼
   Pull Request ──► merge ──► MkDocs deploys to GitHub Pages
```

## Prerequisites

- A GitHub organization or repository where your team works
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- A GitHub fine-grained personal access token (PAT) with public repository read access

## Step 1: Fork or copy the repository structure

Start by reproducing this directory layout in your own repo:

```
your-repo/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── objective.md          # Issue template for objectives
│   └── workflows/
│       ├── deploy.yml            # MkDocs deployment
│       └── update-reports.yml    # Report generation
├── docs/
│   ├── index.md
│   ├── objectives.md             # Auto-generated (do not edit by hand)
│   └── images/                   # Auto-generated charts
├── reports/
│   ├── settings.py               # Team-specific settings (edit this first)
│   ├── config.py                 # Objectives, repos, contributors, dates
│   ├── main.py                   # Fetch commit data from GitHub
│   ├── plot.py                   # Generate visualization
│   ├── generate_config.py        # Regenerate config from GitHub issues
│   ├── generate_docs.py          # Generate objectives.md
│   ├── pyproject.toml            # Python dependencies for reports
│   └── output/                   # CSV output directory
├── mkdocs.yml
└── pyproject.toml                # Root project dependencies (MkDocs, etc.)
```

## Step 2: Set up issue-driven objectives

Objectives are GitHub Issues with a specific labeling convention. Each objective issue needs:

- **A label** matching the pattern `pi-{YY}.{Q}-objective` (e.g., `pi-26.2-objective` for FY26 Q2).
- **Assignees** set to the contributors working on that objective.
- **Repository labels** in the format `repo:org/repo-name` for each tracked repository.

### Create an issue template

Add `.github/ISSUE_TEMPLATE/objective.md` so team members can propose objectives with a consistent structure:

```markdown
---
name: Propose objective
about: Objective for the team
title: 'PI 26.2 Objective X: ...'
labels: pi-26.2-objective
assignees: ''
---

### Motivation

### Description

### Acceptance Criteria

- [ ] ...

### Sub-tasks

- [ ] ...
```

Update the `title` and `labels` fields each quarter to match the current PI.

### Label conventions

Create these labels in your repository:

| Label | Purpose |
|---|---|
| `pi-{YY}.{Q}-objective` | Tags an issue as a quarterly objective |
| `repo:org/repo-name` | Maps a repository to an objective |

The `generate_config.py` script searches for issues using the `pi-*-objective` label pattern, so sticking to this convention is required.

## Step 3: Configure team settings

Open `reports/settings.py` and update the values for your team:

```python
GITHUB_ORG = "your-org"                    # GitHub org that owns the repo
GITHUB_REPO = "your-repo"                  # repo where objective issues live
TEAM_NAME = "Your Team"                    # short name for chart titles
TEAM_DISPLAY_NAME = "Your Full Team Name"  # used in chart annotations
SITE_URL = "your-org.github.io/your-repo"  # GitHub Pages URL (no https://)
TOKEN_ENV_VAR = "GH_YOUR_TEAM_PAT"        # env var name for the GitHub PAT
```

This is the **only Python file** you need to edit to adopt the reporting system. All other scripts import their team-specific values from here. The derived values (`REPO_FULL_NAME`, `REPO_URL`, `OBJECTIVES_PAGE_URL`) are computed automatically.

You will also need to update the secret name in `.github/workflows/update-reports.yml` to match your `TOKEN_ENV_VAR` value, since the workflow YAML cannot import from Python.

## Step 4: Configure the reporting scripts

### Define PI date ranges

In `reports/config.py`, define the date ranges for each Program Increment (PI). VEDA-ODD uses a fiscal-quarter calendar:

```python
PI_DATES = {
    "pi-26.1": ("20251018", "20260117"),
    "pi-26.2": ("20260118", "20260425"),
    # Add your own quarters here
}
```

Dates are in `YYYYMMDD` format. The `get_current_pi()` helper determines which PI is active based on today's date.

### Define objectives

The `OBJECTIVES` dictionary in `config.py` is the source of truth for what gets tracked. Each entry maps a PI to a list of objectives:

```python
OBJECTIVES = {
    "pi-26.2": [
        {
            "issue_number": 304,
            "title": "Objective description",
            "state": "open",
            "contributors": [
                ("Display Name", "github_username"),
            ],
            "repos": [
                ("org-name", "repo-name"),
            ],
        },
        # more objectives ...
    ],
}
```

You can maintain this manually or auto-generate it with `generate_config.py` (see below).

### Auto-generate config from issues

Run `generate_config.py` to pull objectives, contributors, and repo mappings from your GitHub issues:

```bash
cd reports
export GH_YOUR_TEAM_PAT=ghp_your_token_here  # must match TOKEN_ENV_VAR in settings.py
uv run generate_config.py
```

This produces an `objectives_config.py` file. Review it, then copy the relevant sections into `config.py`. The script extracts:

- Objective metadata from issue titles
- Contributors from issue assignees
- Repository mappings from `repo:org/repo-name` labels

### Install Python dependencies

The reports scripts have their own `pyproject.toml`:

```toml
[project]
name = "reports"
requires-python = ">=3.11"
dependencies = [
    "matplotlib>=3.10.3",
    "pandas>=2.3.0",
    "pygithub>=2.6.1",
]
```

Run `uv sync` in the `reports/` directory to install them.

## Step 5: Run the reporting pipeline locally

The pipeline has four stages that must run in order:

```bash
cd reports

# 1. (Optional) Regenerate config from GitHub issues
uv run generate_config.py

# 2. Fetch commit data for the current PI
uv run main.py

# 3. Generate the bar chart
uv run plot.py

# 4. Generate the objectives documentation page
uv run generate_docs.py
```

After running, you will have:

| Output | Location |
|---|---|
| Commit CSV | `reports/output/pi-{PI}.csv` |
| Bar chart PNG | `docs/images/pi-{PI}.png` |
| Objectives page | `docs/objectives.md` |

### Environment variables

| Variable | Required | Description |
|---|---|---|
| Value of `TOKEN_ENV_VAR` in `settings.py` | Yes | Fine-grained PAT with public repo read access |
| `GITHUB_TOKEN` | In CI only | Automatically provided by GitHub Actions |

To create a PAT: go to [GitHub token settings](https://github.com/settings/personal-access-tokens/new), select **Public Repositories**, and generate the token.

## Step 6: Set up MkDocs

### Root `pyproject.toml`

The documentation site dependencies live in the root project file:

```toml
[dependency-groups]
dev = [
    "mkdocs>=1.6.1",
    "mkdocs-material[imaging]>=9.6.3",
    "mike>=2.1.3",
]
```

### `mkdocs.yml`

Configure your site. At a minimum, include the objectives page in your nav:

```yaml
site_name: Your Team Reports
nav:
  - "index.md"
  - PI Objectives: "objectives.md"

theme:
  name: material

plugins:
  - search
```

### Preview locally

```bash
uv run mkdocs serve
```

This starts a local dev server at `http://127.0.0.1:8000` with live reloading.

## Step 7: Automate with GitHub Actions

### Report generation workflow

Create `.github/workflows/update-reports.yml`:

```yaml
name: Update Reports

on:
  schedule:
    # Run every Monday at 9 AM ET (14:00 UTC)
    - cron: '0 14 * * 1'
  push:
    branches:
      - main
    paths:
      - 'reports/*.py'
      - 'reports/pyproject.toml'
  workflow_dispatch:

jobs:
  update-reports:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v5

      - uses: astral-sh/setup-uv@v7
        with:
          version: "0.9.*"
          enable-cache: true

      - name: Generate config data
        working-directory: reports
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_ODD_PAT: ${{ secrets.GH_ODD_PAT }}  # Rename to match TOKEN_ENV_VAR
        run: uv run generate_config.py

      - name: Generate commit data
        working-directory: reports
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_ODD_PAT: ${{ secrets.GH_ODD_PAT }}  # Rename to match TOKEN_ENV_VAR
        run: uv run main.py

      - name: Generate plot
        working-directory: reports
        run: uv run plot.py

      - name: Generate docs page
        working-directory: reports
        run: uv run generate_docs.py

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          commit-message: "Update reports"
          title: "Update reports"
          body: |
            Automated update of commit reports and visualization.
          branch: update-reports
          add-paths: |
            reports/output/
            docs/images/
            docs/objectives.md
```

### Deployment workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy docs

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: astral-sh/setup-uv@v7
        with:
          version: "0.9.*"
          enable-cache: true

      - run: uv run mkdocs gh-deploy --force --strict
```

### Repository secrets

Add the following secret in your repository settings (**Settings > Secrets and variables > Actions**):

| Secret | Value |
|---|---|
| Secret matching `TOKEN_ENV_VAR` in `settings.py` | Your fine-grained personal access token (default: `GH_ODD_PAT`) |

`GITHUB_TOKEN` is provided automatically by GitHub Actions.

## Step 8: Quarterly maintenance

At the start of each quarter:

1. **Update the issue template** -- change the label and title prefix to the new PI (e.g., `pi-26.3-objective`).
2. **Create objective issues** -- use the template to propose and finalize objectives. Assign contributors and add `repo:org/repo-name` labels.
3. **Add the new PI date range** to `PI_DATES` in `config.py`.
4. **Run `generate_config.py`** or wait for the weekly automation to pick up the new issues.

The weekly cron job handles everything else: fetching commit data, generating the chart, updating the docs page, and opening a PR for review.

## Customization

### Team settings

All team-specific values (org name, repo name, team display name, PAT variable name, site URL) are centralized in `reports/settings.py`. This is the first file to edit when adopting the system for a new team. The workflow YAML file (`.github/workflows/update-reports.yml`) must also be updated to use your team's secret name for the GitHub PAT.

### Adjusting the chart

`plot.py` generates a horizontal bar chart color-coded by objective. You can customize:

- **Colors**: Edit the `COLORS` list (10-color palette that cycles).
- **Figure size**: Change the `figsize` parameter (default: 16x10 inches).
- **DPI**: Adjust output resolution (default: 150).
- **Caveats text**: Update the annotation at the bottom of the chart.

Repositories that appear in multiple objectives get split bars showing proportional contribution.

### Tracking different metrics

`main.py` collects commit-level data including SHA, message, author, and total changes (additions + deletions). The output CSV can be extended or replaced with other metrics by modifying the `get_commits_for_repo_user` function.

### Changing the schedule

Edit the `cron` expression in `update-reports.yml`. For example, to run daily at noon UTC:

```yaml
schedule:
  - cron: '0 12 * * *'
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `generate_config.py` finds no issues | Verify your issues have labels matching `pi-*-objective` |
| Rate limiting errors in `main.py` | Ensure your PAT env var (see `TOKEN_ENV_VAR` in `settings.py`) is set. The script uses 10 parallel workers; reduce this if needed |
| Chart is empty | Check that `reports/output/pi-{PI}.csv` has data. Verify date ranges in `PI_DATES` |
| PR not created by Actions | Confirm the workflow has `contents: write` and `pull-requests: write` permissions |
| MkDocs build fails | Run `uv run mkdocs build --strict` locally to see errors |
