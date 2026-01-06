#!/usr/bin/env python3
"""
Query GitHub API for commits to repositories in parallel.
"""

from github import Github, Auth
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd
from config import (
    get_time_range,
    get_current_pi,
    get_repos_for_pi,
    get_contributors_for_pi,
)


def get_commits_for_repo_author(
    g: Github,
    owner: str,
    repo: str,
    author: str,
    start_date: datetime,
    end_date: datetime,
) -> List[dict]:
    """
    Query GitHub API for commits by a specific author in a repo.

    Returns list of commit detail dicts (not commit objects) to avoid
    thread safety issues with PyGithub objects.
    """
    try:
        repository = g.get_repo(f"{owner}/{repo}")
        commits = repository.get_commits(
            author=author, since=start_date, until=end_date
        )

        # Group commits by PR
        prs = []
        pr_commits = []
        standalone_commits = []

        for commit in commits:
            pulls = commit.get_pulls()
            if pulls.totalCount == 1:
                if (number := pulls[0].number) not in prs:
                    pr_commits.append(commit)
                    prs.append(number)
            elif pulls.totalCount == 0:
                standalone_commits.append(commit)

        # Extract details immediately (avoid returning PyGithub objects)
        results = []
        for commit in pr_commits + standalone_commits:
            results.append(
                {
                    "sha": commit.sha,
                    "message": commit.commit.message.split("\n")[0],
                    "author": commit.commit.author.name,
                    "committer": commit.commit.committer.name,
                    "url": commit.html_url,
                    "total_changes": commit.stats.total if commit.stats else 0,
                    "organization": owner,
                    "repository": repo,
                }
            )
        return results
    except Exception as e:
        print(f"  Error processing {owner}/{repo} for {author}: {e}")
        return []


def main(token: str = None, pi: str = None, max_workers: int = 10):
    """
    Query GitHub for commits using parallel requests.

    Args:
        token: GitHub personal access token
        pi: Optional PI to filter repos/contributors (e.g., "pi-26.1").
            If None, uses current PI based on today's date.
        max_workers: Number of parallel threads (default 10)
    """
    # Default to current PI if not specified
    if pi is None:
        pi = get_current_pi()

    time_range = get_time_range(pi)
    if not time_range:
        raise ValueError(f"No date range found for PI: {pi}")

    time_start = datetime.strptime(time_range[0], "%Y%m%d")
    time_end = datetime.strptime(time_range[1], "%Y%m%d")

    # Get repos and contributors for the PI
    repos = get_repos_for_pi(pi)
    contributors = get_contributors_for_pi(pi)
    print(
        f"PI: {pi} ({time_start.strftime('%Y-%m-%d')} to {time_end.strftime('%Y-%m-%d')})"
    )
    print(f"  {len(repos)} repos, {len(contributors)} contributors")

    if len(contributors) < 1:
        raise ValueError("No contributors found in config.")

    # Build list of (repo, contributor) tasks
    tasks = []
    for owner, repo in repos:
        for name, username in contributors:
            tasks.append((owner, repo, username))

    print(
        f"Querying {len(tasks)} repo×contributor combinations with {max_workers} workers..."
    )

    all_commits = []

    # Use thread pool for parallel API calls
    # Each thread gets its own Github client to avoid rate limit issues
    def process_task(task):
        owner, repo, username = task
        if token:
            auth = Auth.Token(token)
            g = Github(auth=auth)
        else:
            g = Github()
        try:
            return get_commits_for_repo_author(
                g, owner, repo, username, time_start, time_end
            )
        finally:
            g.close()

    completed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_task, task): task for task in tasks}
        for future in as_completed(futures):
            completed += 1
            if completed % 50 == 0:
                print(f"  Progress: {completed}/{len(tasks)}")
            commits = future.result()
            all_commits.extend(commits)

    print(f"Found {len(all_commits)} commits")

    df = pd.DataFrame(all_commits)
    csv_filename = f"output/{pi}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved to {csv_filename}")

    return df


if __name__ == "__main__":
    token = os.environ.get("GH_ODD_PAT") or os.environ.get("GITHUB_TOKEN")
    main(token=token)
