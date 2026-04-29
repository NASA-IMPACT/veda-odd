"""Public API for accessing the OBJECTIVES dataset.

The raw data lives in the auto-generated `_objectives_data` module
(regenerated via `uv run generate_config.py`). Import from here, not from
the `_objectives_data` module directly.
"""

from _objectives_data import OBJECTIVES

__all__ = [
    "OBJECTIVES",
    "get_all_repos",
    "get_all_contributors",
    "get_repos_for_pi",
    "get_contributors_for_pi",
]


def get_all_repos():
    """Derive unique repos from all objectives."""
    repos = set()
    for pi_objectives in OBJECTIVES.values():
        for obj in pi_objectives:
            for repo in obj["repos"]:
                repos.add(repo)
    return sorted(repos)


def get_all_contributors():
    """Derive unique contributors from all objectives."""
    contributors = {}
    for pi_objectives in OBJECTIVES.values():
        for obj in pi_objectives:
            for name, username in obj["contributors"]:
                contributors[username] = name
    return [
        (name, username)
        for username, name in sorted(contributors.items(), key=lambda x: x[1])
    ]


def get_repos_for_pi(pi: str):
    """Get all repos for a specific PI."""
    repos = set()
    for obj in OBJECTIVES.get(pi, []):
        for repo in obj["repos"]:
            repos.add(repo)
    return sorted(repos)


def get_contributors_for_pi(pi: str):
    """Get all contributors for a specific PI."""
    contributors = {}
    for obj in OBJECTIVES.get(pi, []):
        for name, username in obj["contributors"]:
            contributors[username] = name
    return [
        (name, username)
        for username, name in sorted(contributors.items(), key=lambda x: x[1])
    ]
