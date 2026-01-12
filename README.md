# UKRI Digital Research Skills Website

This repository holds the code for the UKRI Digital Research Skills website.
The site is written in [Quarto](https://quarto.org), and wraps a `.csv`-formatted list of available training in a github pages site.
The processing and searching of the training materials is performed by [ojs](https://observablehq.com/@observablehq/observable-javascript), as it is a simple and powerful system that is baked into quarto by default.

## Local Development

Local development requires an installation of quarto.
Please see Quarto's [Get Started](https://quarto.org/docs/get-started/) documentation to install a local copy.

Set up the correct UV environment with:

```bash
source ~/.venv/bin/activate.fish
```

A local preview of the code can be generated using:

```bash
quarto preview ./site/index.qmd
```
