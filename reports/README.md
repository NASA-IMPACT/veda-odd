# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable `GH_ODD_PAT`

## Generating data

1. Update the dates in config.py
2. Add any new contributors to config.py
3. Add any new repositories to config.py
4. Run `uv run main.py`
5. Run `uv run plot.py`

## Running a report to get download stats from pypi

Pypi stats only go back 180 days. After installing the pypistats package you can run a command to get daily downloads:

```bash
pypistats overall virtualizarr -sd 2025-05-15 -ed 2025-11-11 --daily -f tsv --mirrors without > virtualizarr-report.tsv
```
And then generate more informative stats using the analyze_downloads.py script:

```bash
  # With default cutoff date (2025-07-21)
  python analyze_downloads.py virtualizarr-report.tsv

  # With custom cutoff date
  python analyze_downloads.py virtualizarr-report.tsv --cutoff-date 2025-08-15

  # Show help
  python analyze_downloads.py --help
  ```

  Using the previous pypi command as an example, the following is output from the script:

  ```bash
$ python analyze_downloads.py virtualizarr-report.tsv
  Download Analysis
============================================================
Cutoff date: 2025-07-21

Before 2025-07-21 (inclusive):
  - Number of days: 64
  - Total downloads: 3,822
  - Average daily downloads: 59.72

After 2025-07-21:
  - Number of days: 113
  - Total downloads: 20,682
  - Average daily downloads: 183.03

Change: +206.48%
Absolute difference: +123.31 downloads/day
```
