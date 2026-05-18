#!/usr/bin/env python3
"""Render docs/objectives.md from the OBJECTIVES dataset."""

import argparse
import logging
import re
from pathlib import Path

from dse_oss_reports.cli import run_generate_docs

from objectives import OBJECTIVES
from settings import TEAM_SETTINGS

# Drops past-PI image references whose target file was never generated
# (e.g. PIs that predate the per-PI chart tooling). The upstream generator
# emits an image link for every PI unconditionally.
_IMAGE_LINE_RE = re.compile(r"^!\[[^\]]*\]\((images/[^)]+)\)\s*$")


def _strip_missing_image_lines(md_path: Path) -> None:
    docs_dir = md_path.parent
    kept = []
    for line in md_path.read_text().splitlines():
        match = _IMAGE_LINE_RE.match(line)
        if match and not (docs_dir / match.group(1)).exists():
            continue
        kept.append(line)
    md_path.write_text("\n".join(kept) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    output_path = run_generate_docs(TEAM_SETTINGS, OBJECTIVES)
    _strip_missing_image_lines(output_path)
