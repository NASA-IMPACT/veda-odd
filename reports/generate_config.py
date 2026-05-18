#!/usr/bin/env python3
"""Generate _objectives_data.py from GitHub issues with pi-*-objective labels."""

import argparse
import logging
import os

from dse_oss_reports.cli import run_generate_config

from settings import TEAM_SETTINGS, TOKEN_ENV_VAR


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    token = os.environ.get(TOKEN_ENV_VAR) or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit(f"Set {TOKEN_ENV_VAR} or GITHUB_TOKEN environment variable")

    run_generate_config(token, TEAM_SETTINGS, long_org_name_mapping={})
