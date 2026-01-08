# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable `GH_ODD_PAT`

## Configuration

The `config.py` file contains:
- `TIME_RANGE`: Start and end dates for commit analysis.
- `OBJECTIVES`: Quarterly objectives with repos and contributors per objective

### Regenerating objectives from GitHub

To fetch the latest objectives from GitHub issues:

```bash
uv run generate_config.py
```

This generates `objectives_config.py` with objectives and contributors from issues labeled `pi-*-objective`. You'll need to manually add repos to each objective, then copy to `config.py`.

### Regenerating docs/objectives.md

To regenerate the objectives documentation page from config:

```bash
uv run generate_docs.py
```

## Generating data

1. Run `uv run main.py` (uses 10 parallel workers by default)
2. Run `uv run plot.py`

`TIME_RANGE` is automatically set to the current fiscal quarter (Q1: Oct-Dec, Q2: Jan-Mar, Q3: Apr-Jun, Q4: Jul-Sep).

The generated chart colors bars by PI objective (see [objectives page](https://nasa-impact.github.io/veda-odd/objectives) for details).

## Performance

- **generate_config.py**: Uses GitHub search API to fetch only objective issues (~2-3 seconds)
- **main.py**: Parallelizes API calls with ThreadPoolExecutor (10x faster than sequential)
