"""Team-specific settings for the VEDA ODD reporting system."""

from dse_oss_reports.settings import TeamSettings

TOKEN_ENV_VAR = "GH_PAT"

TEAM_SETTINGS = TeamSettings(
    team_name="ODD",
    team_display_name="VEDA/EODC ODD",
    github_org="NASA-IMPACT",
    github_repo="veda-odd",
    site_url="nasa-impact.github.io/veda-odd",
    objectives_page_url="https://nasa-impact.github.io/veda-odd/objectives",
    token_env_var=TOKEN_ENV_VAR,
)
