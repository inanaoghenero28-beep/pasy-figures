# PASy figures

`make_figures.py` generates Figures 1–3 of the manuscript *Performance Modeling for Isolated Industrial Operations: A Data Envelopment Analysis Framework* (Inana, O.). Every result and setting it shows (test days, quartile thresholds, AHP weights, design settings, variable roles and day counts) is read from the two result files in `runs/`. The only values set in the script are three descriptions of the input data that the result files do not contain: the date of the lost-time incident, the wording of the test-day legend and the dry-season months. They are listed at the top of the script.

## Files

| File | Contents |
|---|---|
| `PASy_Figures.ipynb` | Colab notebook that runs the figure script and shows the figures |
| `make_figures.py` | Figure script |
| `runs/paper_results.json` | Every statistic reported in the manuscript, for all 12 runs, with the run metadata |
| `runs/baseline_s42/daily_classified.csv` | Daily scores and annual-quartile classes of the 336 steady-state days |

## Run in Colab

Open the notebook in Colab:
https://colab.research.google.com/github/inanaoghenero28-beep/pasy-figures/blob/main/PASy_Figures.ipynb

Then choose Runtime → Run all.

## Run locally

Requirements: Python 3.10 or later, numpy, pandas and matplotlib.

```bash
python make_figures.py runs figs
```

This writes `Fig1`, `Fig2` and `Fig3` to `figs/` in EPS, PDF and PNG format.

The full dataset and results are in the Zenodo deposit cited in the manuscript: Inana, O. (2026). PASY IMPLEMENTATION DATA (Version 3) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.23926688

The two result files in `runs/` were written by the run that produced that deposit.
