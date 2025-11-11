# VEDA ODD

This repository hosts documentation for contributing to and interacting with the Optimized Data Delivery team of NASA's VEDA project.

## Building the Documentation

```bash
git clone https://github.com/NASA-IMPACT/veda-odd.git
cd veda-odd
# Serve the documentation
uv run -- mkdocs serve
# Deploy the documentation
# This will build the site and push it to the gh-pages branch of this repo
uv run mkdocs gh-deploy
```
