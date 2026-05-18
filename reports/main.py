#!/usr/bin/env python3
"""Fetch authored commits and resolved issues/PRs for one PI."""

import argparse
import logging
import os

from dse_oss_reports.cli import run_commits_report

from constants import PI_DATES
from objectives import OBJECTIVES
from settings import TEAM_SETTINGS, TOKEN_ENV_VAR


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pi", help="PI name (e.g. pi-26.2). Defaults to current PI.")
    parser.add_argument("--max-workers", type=int, default=3)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    token = os.environ.get(TOKEN_ENV_VAR) or os.environ.get("GITHUB_TOKEN")
    run_commits_report(
        token,
        TEAM_SETTINGS,
        PI_DATES,
        OBJECTIVES,
        pi=args.pi,
        max_workers=args.max_workers,
    )
