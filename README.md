# PASy Figure Generation Script

This repository contains the figure generation script (Cell 6) for the manuscript:

**"Performance Modeling for Isolated Industrial Operations: A Data Envelopment 
Analysis Framework"**  
Oghenero Orevaoghene Inana  
Adlore Business Enterprise Limited, Benin City, Nigeria  
Submitted to: Operations Research Forum (Springer Nature)

## Script

`cell6_figure_generation.py` produces the three manuscript figures:

- **Fig1.eps / Fig1.png** — PASy framework pipeline architecture diagram (Section 3.3)
- **Fig2.eps / Fig2.png** — Daily geometric efficiency score timeline by quartile 
  classification (Section 4.2)
- **Fig3.eps / Fig3.png** — Monthly distribution of geometric efficiency scores, 
  box plots (Section 4.5.1)

## Requirements

- Python 3 (Google Colab environment)
- matplotlib, pandas, numpy (pre-installed in Colab)
- Access to the PASy Google Sheets workbook (COMPUTATION_SHEET and 
  EFFICIENCY_RATINGS worksheets)
- Cells 1, 2, and 4 of the PASy implementation notebook must be run before Cell 6

## Data

The underlying dataset is publicly available on Zenodo:  
**DOI: https://doi.org/10.5281/zenodo.20218539**

The supplementary extended file is available at:  
**DOI: https://doi.org/10.5281/zenodo.17281985**

## Journal Compliance

Figures are exported as EPS (vector, primary submission format) and PNG (preview).  
Font: DejaVu Sans. Width: 6.85 inches (174 mm). No titles embedded in artwork.  
File naming follows Springer Nature guidelines: Fig1, Fig2, Fig3.

## Contact

frontdesk@adlorebusiness.ng
