#!/usr/bin/env python3
"""
Analyze download statistics before and after a given date using a pypistats report output from a command like:
pypistats overall virtualizarr -sd 2025-05-15 -ed 2025-11-11 --daily -f tsv --mirrors without > virtualizarr-report.tsv
"""

import csv
from datetime import datetime
from pathlib import Path


def analyze_downloads(tsv_file: str, cutoff_date: str = "2025-07-21"):
    """
    Calculate average daily downloads before and after a cutoff date.

    Args:
        tsv_file: Path to the TSV file
        cutoff_date: The date to split the data (format: YYYY-MM-DD)
    """
    cutoff = datetime.strptime(cutoff_date, "%Y-%m-%d")

    before_downloads = []
    after_downloads = []

    with open(tsv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            # Skip non-data rows
            if row['category'] == 'Total' or not row['date']:
                continue

            try:
                date = datetime.strptime(row['date'], "%Y-%m-%d")
                downloads = int(row['downloads'])

                if date < cutoff:
                    before_downloads.append(downloads)
                elif date > cutoff:
                    after_downloads.append(downloads)
                else:  # date == cutoff
                    # Include cutoff date in "before" period
                    before_downloads.append(downloads)

            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {e}")
                continue

    # Calculate averages
    avg_before = sum(before_downloads) / len(before_downloads) if before_downloads else 0
    avg_after = sum(after_downloads) / len(after_downloads) if after_downloads else 0

    # Calculate percentage change
    if avg_before > 0:
        percent_change = ((avg_after - avg_before) / avg_before) * 100
    else:
        percent_change = 0

    # Print results
    print(f"Download Analysis")
    print(f"=" * 60)
    print(f"Cutoff date: {cutoff_date}")
    print()
    print(f"Before {cutoff_date} (inclusive):")
    print(f"  - Number of days: {len(before_downloads)}")
    print(f"  - Total downloads: {sum(before_downloads):,}")
    print(f"  - Average daily downloads: {avg_before:.2f}")
    print()
    print(f"After {cutoff_date}:")
    print(f"  - Number of days: {len(after_downloads)}")
    print(f"  - Total downloads: {sum(after_downloads):,}")
    print(f"  - Average daily downloads: {avg_after:.2f}")
    print()
    print(f"Change: {percent_change:+.2f}%")
    print(f"Absolute difference: {avg_after - avg_before:+.2f} downloads/day")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze download statistics before and after a given date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s virtualizarr-report.tsv --cutoff-date 2025-07-21
        """
    )
    parser.add_argument(
        "tsv_file",
        help="Path to the TSV file containing download statistics"
    )
    parser.add_argument(
        "--cutoff-date",
        default="2025-07-21",
        help="Date to split the analysis (format: YYYY-MM-DD, default: 2025-07-21)"
    )

    args = parser.parse_args()

    tsv_path = Path(args.tsv_file)
    if not tsv_path.exists():
        print(f"Error: {tsv_path} not found")
        exit(1)

    analyze_downloads(str(tsv_path), args.cutoff_date)
