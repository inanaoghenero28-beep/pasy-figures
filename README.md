# PASy figures

`make_figures.py` generates Figures 1–3 of the manuscript *Performance Modeling for Isolated Industrial Operations: A Data Envelopment Analysis Framework* (Inana, O.). It contains no hard-coded results. Every value it plots is read from the two result files in `runs/`.

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

The full dataset and results are in the Zenodo deposit cited in the manuscript.
