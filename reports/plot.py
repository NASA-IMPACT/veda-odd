#!/usr/bin/env python3
"""Render per-PI charts for authored commits and resolved issues/PRs."""

import argparse
import logging

from dse_oss_reports.cli import run_plot_report

from constants import PI_DATES
from objectives import OBJECTIVES
from settings import TEAM_SETTINGS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pi", help="PI name (e.g. pi-26.2). Defaults to current PI.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    run_plot_report(TEAM_SETTINGS, OBJECTIVES, pi=args.pi, pi_dates=PI_DATES)
