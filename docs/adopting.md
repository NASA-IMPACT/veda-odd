# Adopting the VEDA-ODD Reporting Structure

The reporting pipeline that powers this site's [Objectives](objectives.md) page is provided by [`dse-oss-reports`](https://github.com/NASA-IMPACT/dse-oss-reports), a shared library used by multiple NASA-ODSI DSE teams. The adoption guide — how to set up issue-driven objectives, wire the four pipeline scripts, configure GitHub Actions, and deploy with MkDocs — lives in that repo's [README](https://github.com/NASA-IMPACT/dse-oss-reports#adoption-guide).

For a working reference implementation, see [`reports/`](https://github.com/NASA-IMPACT/veda-odd/tree/main/reports) in this repo:

- [`settings.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/settings.py) — VEDA-ODD's `TeamSettings` instance
- [`constants.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/constants.py) — VEDA-ODD's `PI_DATES`
- [`main.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/main.py), [`plot.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/plot.py), [`generate_config.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/generate_config.py), [`generate_docs.py`](https://github.com/NASA-IMPACT/veda-odd/blob/main/reports/generate_docs.py) — thin wrappers around `dse_oss_reports.cli`
- [`update-reports.yml`](https://github.com/NASA-IMPACT/veda-odd/blob/main/.github/workflows/update-reports.yml) and [`deploy.yml`](https://github.com/NASA-IMPACT/veda-odd/blob/main/.github/workflows/deploy.yml) — the weekly cron and MkDocs deploy
