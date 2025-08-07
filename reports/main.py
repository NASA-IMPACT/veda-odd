#!/usr/bin/env python3
"""
Query GitHub API for commits to a given repository
"""

from github import Github, Auth
from datetime import datetime
from typing import List
import os
import pandas as pd
from config import USERS, REPOS, TIME_RANGE


def get_commits_for_author(
    repository,
    author: str,
    start_date: datetime,
    end_date: datetime,
) -> List:
    """
    Query GitHub API for commits by a specific author within a date range

    Args:
        repository: GitHub repository object (already connected)
        author: GitHub username/email to filter commits by
        start_date: Start date for commit search (inclusive)
        end_date: End date for commit search (inclusive)

    Returns:
        List of commit objects
    """
    # Get commits with filters using the existing repository connection
    commits = repository.get_commits(author=author, since=start_date, until=end_date)
    # Group commits by PR
    prs = []
    pr_commits = []
    standalone_commits = []

    for commit in commits:
        # Get PRs associated with this commit
        pulls = commit.get_pulls()

        if pulls.totalCount == 1:
            # Commit is part of one or more PRs
            if (number := pulls[0].number) not in prs:
                pr_commits.append(commit)
                prs.append(number)
        elif pulls.totalCount == 0:
            # Commit is not part of any PR (direct to branch)
            standalone_commits.append(commit)
        else:
            raise ValueError(f"Unexpected pulls.totalCount: {pulls.totalCount}")
    # Convert PaginatedList to regular list
    commit_list = pr_commits + standalone_commits
    return commit_list


def get_commit_details(commit) -> dict:
    """Extract detailed commit information"""
    return {
        "sha": commit.sha,
        "message": commit.commit.message.split("\n")[0],
        "author": commit.commit.author.name,
        "committer": commit.commit.committer.name,
        "url": commit.html_url,
        "total_changes": commit.stats.total if commit.stats else 0,
    }


def main(token: str = None):
    time_start = datetime.strptime(TIME_RANGE[0], "%Y%m%d")
    time_end = datetime.strptime(TIME_RANGE[1], "%Y%m%d")
    all_commits = []

    # Initialize GitHub client once
    if token:
        auth = Auth.Token(token)
        g = Github(auth=auth)
    else:
        g = Github()  # Unauthenticated (lower rate limits)

    if len(USERS) < 1:
        raise ValueError(
            "No users were included in the config. See README for instructions on populating the USER list."
        )

    # Iterate through repositories first
    for owner, repo in REPOS:
        print(f"Processing repository: {owner}/{repo}")

        # Get repository object once per repository
        repository = g.get_repo(f"{owner}/{repo}")

        # Iterate through all users and their emails for this repository
        for name, username, start_date_str, end_date_str in USERS:
            # Parse dates for this user
            start_date = (
                datetime.strptime(start_date_str, "%Y%m%d")
                if start_date_str
                else time_start
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y%m%d") if end_date_str else time_end
            )

            print(f"  Processing user: {username}")
            commits = get_commits_for_author(
                repository=repository,
                author=username,
                start_date=start_date,
                end_date=end_date,
            )
            for commit in commits:
                commit_details = get_commit_details(commit)
                commit_details.update(
                    {
                        "organization": owner,
                        "repository": repo,
                    }
                )
                all_commits.append(commit_details)

    g.close()

    df = pd.DataFrame(all_commits)
    csv_filename = (
        f"output/{time_start.strftime('%Y-%m-%d')}-{time_end.strftime('%Y-%m-%d')}.csv"
    )
    df.to_csv(csv_filename, index=False)

    return df


if __name__ == "__main__":
    token = os.environ["GH_ODD_PAT"]
    main(token=token)
