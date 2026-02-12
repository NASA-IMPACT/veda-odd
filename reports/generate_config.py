#!/usr/bin/env python3
"""
Generate OBJECTIVES config from GitHub issues with pi-*-objective labels.

Data sources:
- Objectives: Issues with `pi-X.Y-objective` labels
- Contributors: Issue assignees
- Repos: Labels matching `repo:org/repo-name` pattern

Usage:
    uv run generate_config.py
"""

import os
import re
from github import Github, Auth


def get_objective_issues(g: Github, repo_name: str = "NASA-IMPACT/veda-odd"):
    """Fetch all issues with pi-*-objective labels using search API."""
    objectives_by_pi = {}

    # Use search API - much faster than iterating all issues
    # Search for issues with any pi-*-objective label
    query = f"repo:{repo_name} is:issue label:pi-25.2-objective,pi-25.3-objective,pi-25.4-objective,pi-26.1-objective,pi-26.2-objective,pi-26.3-objective,pi-26.4-objective"
    issues = g.search_issues(query)

    if issues.totalCount < 1:
        raise (ValueError, "No PI issue found")
    for issue in issues:
        pi = None
        repos = []

        for label in issue.labels:
            # Check for PI objective label
            match = re.match(r"pi-(\d+\.\d+)-objective", label.name)
            if match:
                pi = f"pi-{match.group(1)}"

            # Check for repo label (format: repo:org/repo-name)
            if label.name.startswith("repo:"):
                repo_str = label.name[5:]  # Remove "repo:" prefix
                if "/" in repo_str:
                    org, repo_name_part = repo_str.split("/", 1)
                    repos.append((org, repo_name_part))

        if pi:
            if pi not in objectives_by_pi:
                objectives_by_pi[pi] = []

            # Get assignees
            contributors = [
                (assignee.name or assignee.login, assignee.login)
                for assignee in issue.assignees
            ]

            objectives_by_pi[pi].append(
                {
                    "issue_number": issue.number,
                    "title": issue.title,
                    "contributors": contributors,
                    "state": issue.state,
                    "repos": repos,
                }
            )

    return objectives_by_pi


def generate_config(objectives_by_pi: dict) -> str:
    """Generate Python config code from objectives data."""
    lines = [
        "from datetime import date",
        "",
        "# Manually maintained PI date ranges",
        "# Update these when new PIs are planned",
        "PI_DATES = {",
        '    "pi-25.2": ("20250119", "20250418"),',
        '    "pi-25.3": ("20250419", "20250718"),',
        '    "pi-25.4": ("20250719", "20251018"),',
        '    "pi-26.1": ("20251019", "20260117"),',
        '    "pi-26.2": ("20260118", "20260425"),',
        "}",
        "",
        "",
        "def get_current_pi():",
        '    """Find the current PI based on today\'s date."""',
        '    today = date.today().strftime("%Y%m%d")',
        "    for pi_name, (start, end) in PI_DATES.items():",
        "        if start <= today <= end:",
        "            return pi_name",
        "    return None",
        "",
        "",
        "def get_time_range(pi: str = None):",
        '    """Get date range for a PI, or current PI if not specified."""',
        "    if pi:",
        "        return PI_DATES.get(pi)",
        "    current = get_current_pi()",
        "    if current:",
        "        return PI_DATES[current]",
        "    # Fallback to most recent PI if not in any range",
        "    return list(PI_DATES.values())[-1]",
        "",
        "",
        "TIME_RANGE = get_time_range()",
        "",
        "# Quarterly objectives with repos and contributors per objective",
        "# Run `uv run generate_config.py` to regenerate from GitHub issues",
        "# - Objectives: Issues with pi-X.Y-objective labels",
        "# - Contributors: Issue assignees",
        "# - Repos: Labels matching repo:org/repo-name",
        "OBJECTIVES = {",
    ]

    # Sort PIs chronologically
    sorted_pis = sorted(objectives_by_pi.keys(), key=lambda x: float(x.split("-")[1]))

    for pi in sorted_pis:
        objectives = objectives_by_pi[pi]
        lines.append(f'    "{pi}": [')

        # Sort objectives by issue number
        for obj in sorted(objectives, key=lambda x: x["issue_number"]):
            lines.append("        {")
            lines.append(f'            "issue_number": {obj["issue_number"]},')
            title = obj["title"].replace('"', '\\"')
            lines.append(f'            "title": "{title}",')
            lines.append(f'            "state": "{obj["state"]}",')
            lines.append('            "contributors": [')
            for name, username in obj["contributors"]:
                name = (name or username).replace('"', '\\"')
                lines.append(f'                ("{name}", "{username}"),')
            lines.append("            ],")
            lines.append('            "repos": [')
            for org, repo in obj.get("repos", []):
                lines.append(f'                ("{org}", "{repo}"),')
            lines.append("            ],")
            lines.append("        },")

        lines.append("    ],")

    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def get_all_repos():")
    lines.append('    """Derive unique repos from all objectives."""')
    lines.append("    repos = set()")
    lines.append("    for pi_objectives in OBJECTIVES.values():")
    lines.append("        for obj in pi_objectives:")
    lines.append('            for repo in obj["repos"]:')
    lines.append("                repos.add(repo)")
    lines.append("    return sorted(repos)")
    lines.append("")
    lines.append("")
    lines.append("def get_all_contributors():")
    lines.append('    """Derive unique contributors from all objectives."""')
    lines.append("    contributors = {}")
    lines.append("    for pi_objectives in OBJECTIVES.values():")
    lines.append("        for obj in pi_objectives:")
    lines.append('            for name, username in obj["contributors"]:')
    lines.append("                contributors[username] = name")
    lines.append(
        "    return [(name, username) for username, name in sorted(contributors.items(), key=lambda x: x[1])]"
    )
    lines.append("")
    lines.append("")
    lines.append("def get_repos_for_pi(pi: str):")
    lines.append('    """Get all repos for a specific PI."""')
    lines.append("    repos = set()")
    lines.append("    for obj in OBJECTIVES.get(pi, []):")
    lines.append('        for repo in obj["repos"]:')
    lines.append("            repos.add(repo)")
    lines.append("    return sorted(repos)")
    lines.append("")
    lines.append("")
    lines.append("def get_contributors_for_pi(pi: str):")
    lines.append('    """Get all contributors for a specific PI."""')
    lines.append("    contributors = {}")
    lines.append("    for obj in OBJECTIVES.get(pi, []):")
    lines.append('        for name, username in obj["contributors"]:')
    lines.append("            contributors[username] = name")
    lines.append(
        "    return [(name, username) for username, name in sorted(contributors.items(), key=lambda x: x[1])]"
    )

    return "\n".join(lines)


def main():
    token = os.environ.get("GH_ODD_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("Set GH_ODD_PAT or GITHUB_TOKEN environment variable")

    auth = Auth.Token(token)
    g = Github(auth=auth)

    print("Fetching objective issues from GitHub (using search API)...")
    objectives_by_pi = get_objective_issues(g)

    g.close()

    print(f"Found {len(objectives_by_pi)} PIs:")
    for pi, objs in sorted(objectives_by_pi.items()):
        repos_count = sum(len(o["repos"]) for o in objs)
        print(f"  {pi}: {len(objs)} objectives, {repos_count} repo mappings")

    config_code = generate_config(objectives_by_pi)

    output_file = "config.py"
    with open(output_file, "w") as f:
        f.write(config_code)
    print(f"\nGenerated config written to {output_file}")
    print("\nTo add repos to an objective, add labels like:")
    print("  repo:zarr-developers/VirtualiZarr")
    print("  repo:developmentseed/titiler-cmr")


if __name__ == "__main__":
    main()
