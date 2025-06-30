# Generating open source commit statistics for the VEDA ODD team

## Setting up a fine-grained personal access token

1. Navigate to https://github.com/settings/personal-access-tokens/new
2. Select public repositories
3. Add new token as the environment variable `GH_ODD_PAT`

## Generating data

1. Copy email addressed from [the private google doc](https://docs.google.com/document/d/1EKswOI8TUYBF0Np-FHQyi3tjr_2yTrcufR2El--lOSk/edit?usp=sharing) to config.py
2. Add any new repositories to config.py
3. Run `uv run main.py`
