import pandas as pd
import matplotlib.pyplot as plt
from config import QUARTER_START, QUARTER_END


def main():
    csv_filename = f"output/{QUARTER_START}-{QUARTER_END}.csv"
    df = pd.read_csv(csv_filename)

    commits_per_repo = df["repository"].value_counts()

    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.barh(
        commits_per_repo.index,
        commits_per_repo.values,
        color=["#9b59b6", "#f39c12", "#1abc9c"],
        alpha=0.8,
        edgecolor="black",
        linewidth=1.2,
    )
    ax.set_xlabel("Number of Commits", fontsize=12)
    ax.grid(axis="x", alpha=0.3)

    for i, v in enumerate(commits_per_repo.values):
        ax.text(
            v + 0.5, i, str(v), ha="left", va="center", fontweight="bold", fontsize=11
        )
    plt.subplots_adjust(left=0.2)
    # Bold title
    fig.text(
        0.5,
        0.93,
        "Commits per Repository",
        fontsize=16,
        fontweight="bold",
        horizontalalignment="center",
        transform=fig.transFigure,
    )

    # Regular subtitle
    fig.text(
        0.5,
        0.90,
        "Merged pull requests are counted as one commit",
        fontsize=12,
        style="normal",
        horizontalalignment="center",
        transform=fig.transFigure,
    )

    plt.savefig(f"output/{QUARTER_START}-{QUARTER_END}_commits_per_repo_hist.png")


if __name__ == "__main__":
    main()
