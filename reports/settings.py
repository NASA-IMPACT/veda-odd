"""
Team-specific settings for the reporting system.

When adopting this reporting structure for a new team, edit the values
below. These are the ONLY values you need to change in the Python
scripts. See docs/adopting.md for the full adoption guide.
"""

# ── Core identifiers ──────────────────────────────────────────────
GITHUB_ORG = "NASA-IMPACT"
GITHUB_REPO = "veda-odd"  # repo where objective issues live
TEAM_NAME = "ODD"  # short name, used in chart titles
TEAM_DISPLAY_NAME = "VEDA/EODC ODD"  # full name, used in chart caveats
SITE_URL = "nasa-impact.github.io/veda-odd"  # GitHub Pages URL (no https://)

# ── Authentication ────────────────────────────────────────────────
TOKEN_ENV_VAR = "GH_ODD_PAT"  # env var name for the GitHub PAT
# Also update the secret name in .github/workflows/update-reports.yml

# ── Derived values (do not edit) ──────────────────────────────────
REPO_FULL_NAME = f"{GITHUB_ORG}/{GITHUB_REPO}"
REPO_URL = f"https://github.com/{GITHUB_ORG}/{GITHUB_REPO}"
OBJECTIVES_PAGE_URL = f"https://{SITE_URL}/objectives"
