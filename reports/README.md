# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable specified by `TOKEN_ENV_VAR` in `settings.py` (default: `GH_ODD_PAT`)

## Configuration

- `_objectives_data.py`: auto-generated `OBJECTIVES` dict (quarterly objectives with repos and contributors). Do not edit by hand.
- `objectives.py`: helper functions over `OBJECTIVES` — import from here.
- `constants.py`: `PI_DATES` and the `get_time_range` / `get_current_pi` helpers.

### Regenerating objectives from GitHub

To fetch the latest objectives from GitHub issues:

```bash
uv run generate_config.py
```

This regenerates `_objectives_data.py` with objectives and contributors from issues labeled `pi-*-objective`. Repos for each objective come from `repo:org/name` labels on the same issues.

## Generating data

1. Run `uv run main.py` (uses 10 parallel workers by default)
2. Run `uv run plot.py`

`TIME_RANGE` is automatically set to the current fiscal quarter (Q1: Oct-Dec, Q2: Jan-Mar, Q3: Apr-Jun, Q4: Jul-Sep).

The generated chart colors bars by PI objective (see the objectives page on the deployed site for details).

### Regenerating docs/objectives.md

To regenerate the objectives documentation page from config:

```bash
uv run generate_docs.py
```

## Performance

- **generate_config.py**: Uses GitHub search API to fetch only objective issues (~2-3 seconds)
- **main.py**: Parallelizes API calls with ThreadPoolExecutor (10x faster than sequential)
