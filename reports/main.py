#!/usr/bin/env python3
"""
Query GitHub API for commits to a given repository
"""

from github import Github, Auth
from datetime import datetime
from typing import List
import os
import pandas as pd
from config import USERS, REPOS, QUARTER_START, QUARTER_END


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
    try:
        # Get commits with filters using the existing repository connection
        commits = repository.get_commits(
            author=author, since=start_date, until=end_date
        )

        # Convert PaginatedList to regular list
        commit_list = list(commits)
        return commit_list

    except Exception as e:
        print(f"    Error getting commits for author {author}: {e}")
        return []


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
    quarter_start = datetime.strptime(QUARTER_START, "%Y%m%d")
    quarter_end = datetime.strptime(QUARTER_END, "%Y%m%d")
    all_commits = []

    # Initialize GitHub client once
    if token:
        auth = Auth.Token(token)
        g = Github(auth=auth)
    else:
        g = Github()  # Unauthenticated (lower rate limits)

    # Iterate through repositories first
    for owner, repo in REPOS:
        print(f"Processing repository: {owner}/{repo}")

        # Get repository object once per repository
        repository = g.get_repo(f"{owner}/{repo}")

        # Iterate through all users and their emails for this repository
        for username, emails, start_date_str, end_date_str in USERS:
            # Parse dates for this user
            start_date = (
                datetime.strptime(start_date_str, "%Y%m%d")
                if start_date_str
                else quarter_start
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y%m%d")
                if end_date_str
                else quarter_end
            )

            print(f"  Processing user: {username}")
            for email in emails:
                commits = get_commits_for_author(
                    repository=repository,
                    author=email,
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
    csv_filename = f"output/{QUARTER_START}-{QUARTER_END}.csv"
    df.to_csv(csv_filename, index=False)

    return df


if __name__ == "__main__":
    token = os.environ["GH_ODD_PAT"]
    main(token=token)
