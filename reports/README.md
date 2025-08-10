# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable `GH_ODD_PAT`

## Generating data

1. Add any new contributors to config.py
2. Add any new repositories to config.py
3. Run `uv run main.py`
