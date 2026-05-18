# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable specified by `TOKEN_ENV_VAR` in `settings.py` (default: `GH_ODD_PAT`)

## Configuration

- `_objectives_data.py`: auto-generated `OBJECTIVES` dict (quarterly objectives with repos and contributors). Do not edit by hand.
- `objectives.py`: helper functions over `OBJECTIVES` — import from here.
- `constants.py`: `PI_DATES` and the `get_time_range` / `get_current_pi` helpers.

## Run the full pipeline

This mirrors the [update-reports workflow](../.github/workflows/update-reports.yml) — regenerates objectives, fetches commit data, plots charts, and rewrites the objectives docs page:

```bash
uv run generate_config.py && uv run main.py && uv run plot.py && uv run generate_docs.py
```

`TIME_RANGE` / PI defaults to the current fiscal quarter (Q1: Oct-Dec, Q2: Jan-Mar, Q3: Apr-Jun, Q4: Jul-Sep). Pass `--pi pi-26.2` to `main.py` / `plot.py` to target a specific PI.

## Running individual steps

- `uv run generate_config.py` — refresh `_objectives_data.py` from GitHub issues labeled `pi-*-objective`.
- `uv run main.py` — fetch authored commits and resolved issues/PRs (10 parallel workers by default).
- `uv run plot.py` — render charts (colored by PI objective).
- `uv run generate_docs.py` — regenerate `docs/objectives.md` from `OBJECTIVES`.

## Performance

- **generate_config.py**: Uses GitHub search API to fetch only objective issues (~2-3 seconds)
- **main.py**: Parallelizes API calls with ThreadPoolExecutor (10x faster than sequential)
