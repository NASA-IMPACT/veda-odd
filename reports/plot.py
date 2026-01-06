import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator

from config import get_current_pi, OBJECTIVES


# Color palette for objectives (cycles if more than 10 objectives)
COLORS = [
    "#e74c3c",  # red
    "#3498db",  # blue
    "#2ecc71",  # green
    "#9b59b6",  # purple
    "#f39c12",  # orange
    "#1abc9c",  # teal
    "#e91e63",  # pink
    "#00bcd4",  # cyan
    "#ff5722",  # deep orange
    "#607d8b",  # blue grey
]


def get_repo_objectives(pi: str) -> dict:
    """
    Build a mapping from repo to list of objectives it belongs to.

    Returns:
        Dict mapping "org/repo" to list of (issue_number, title) tuples
    """
    repo_to_objectives = {}
    for obj in OBJECTIVES.get(pi, []):
        for org, repo in obj["repos"]:
            key = f"{org}/{repo}"
            if key not in repo_to_objectives:
                repo_to_objectives[key] = []
            repo_to_objectives[key].append((obj["issue_number"], obj["title"]))
    return repo_to_objectives


def get_objective_colors(pi: str) -> dict:
    """Generate color mapping for objectives in a PI."""
    objectives = OBJECTIVES.get(pi, [])
    return {
        obj["issue_number"]: COLORS[i % len(COLORS)] for i, obj in enumerate(objectives)
    }


def get_objective_titles(pi: str) -> dict:
    """Get short titles for objectives (strip PI prefix and emojis)."""
    objectives = OBJECTIVES.get(pi, [])
    titles = {}
    length = 100
    for obj in objectives:
        title = obj["title"]
        # Strip "ODD PI X.Y Objective N: " prefix if present
        if ": " in title:
            title = title.split(": ", 1)[1]
        # Strip emojis (unicode emoji ranges)
        title = re.sub(r"[\U0001F300-\U0001F9FF]", "", title).strip()
        # Truncate if too long
        if len(title) > length:
            title = title[: length - 3] + "..."
        titles[obj["issue_number"]] = title
    return titles


def main(pi: str = None, show_labels: bool = False):
    # Default to current PI if not specified
    if pi is None:
        pi = get_current_pi()

    csv_filename = f"output/{pi}.csv"
    df = pd.read_csv(csv_filename)

    # Build repo to objectives mapping and colors
    repo_to_objectives = get_repo_objectives(pi)
    objective_colors = get_objective_colors(pi)

    # Get commits per repo with full path
    df["full_repo"] = df["organization"] + "/" + df["repository"]
    commits_per_repo = df["repository"].value_counts()
    full_repo_map = df.groupby("repository")["full_repo"].first().to_dict()

    fig, ax = plt.subplots(1, 1, figsize=(16, 10))

    # Plot bars with objective-based coloring
    for i, (repo, count) in enumerate(commits_per_repo.items()):
        full_repo = full_repo_map.get(repo, repo)
        objectives = repo_to_objectives.get(full_repo, [])

        if len(objectives) == 0:
            # No objective mapping - gray
            ax.barh(
                i, count, color="#95a5a6", alpha=0.8, edgecolor="black", linewidth=1.2
            )
        elif len(objectives) == 1:
            # Single objective - solid color
            color = objective_colors.get(objectives[0][0], "#95a5a6")
            ax.barh(i, count, color=color, alpha=0.8, edgecolor="black", linewidth=1.2)
        else:
            # Multiple objectives - split bar by color
            width_per_obj = count / len(objectives)
            current_x = 0
            for j, (issue_num, _) in enumerate(objectives):
                color = objective_colors.get(issue_num, "#95a5a6")
                ax.barh(
                    i,
                    width_per_obj,
                    left=current_x,
                    color=color,
                    alpha=0.8,
                    edgecolor="black",
                    linewidth=1.2,
                )
                current_x += width_per_obj

    ax.set_yticks(range(len(commits_per_repo)))
    ax.set_yticklabels(commits_per_repo.index)
    ax.set_xlabel("Number of Commits", fontsize=16, loc="left")
    ax.tick_params(axis="y", labelsize=13)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", alpha=0.3)

    # Add value labels if requested
    if show_labels:
        for i, v in enumerate(commits_per_repo.values):
            ax.text(
                v + 0.5,
                i,
                str(v),
                ha="left",
                va="center",
                fontweight="bold",
                fontsize=11,
            )

    plt.subplots_adjust(left=0.3)

    ax.set_title(
        f"{pi.upper()} ODD's commits to open source repositories",
        fontsize=24,
        fontweight="bold",
    )

    # Legend for objectives with titles
    objective_titles = get_objective_titles(pi)
    legend_elements = [
        Patch(
            facecolor=color,
            edgecolor="black",
            label=objective_titles.get(num, f"#{num}"),
        )
        for num, color in objective_colors.items()
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper right",
        fontsize=9,
        title=f"{pi.upper()} Objectives",
        title_fontsize=10,
    )

    # Caveats and link in bottom right of plot area
    caveats = (
        "Caveats:\n"
        "- Merged PRs counted as one commit\n"
        "- Individual changes may span multiple PRs\n"
        "- Split bars indicate repos in multiple objectives\n"
        "- Includes all open source work by VEDA/EODC ODD team members, not only ODSI-funded work\n\n"
        "Objective details: nasa-impact.github.io/veda-odd/objectives"
    )
    ax.text(
        1.0,
        -0.06,
        caveats,
        fontsize=8,
        style="italic",
        horizontalalignment="right",
        verticalalignment="top",
        transform=ax.transAxes,
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8
        ),
    )

    # Save to docs for website
    docs_images = Path(__file__).parent.parent / "docs" / "images"
    docs_images.mkdir(exist_ok=True)
    plt.savefig(
        docs_images / f"{pi}.png",
        bbox_inches="tight",
        dpi=150,
    )


if __name__ == "__main__":
    main()
