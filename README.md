[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/i9Zy4NKR)

# Replication: Discrimination in the Formation of Academic Networks: A Field Experiment on #EconTwitter

**Paper:** Ajzenman, N., Ferman, B., & Sant'Anna, P. C. (2024). Discrimination in the
Formation of Academic Networks: A Field Experiment on #EconTwitter. *American Economic
Review: Insights*. https://www.aeaweb.org/articles?id=10.1257/aeri.20240298

## Description

A Python replication of the main figures and tables from Ajzenman, Ferman, and Sant'Anna
(2024), which studies whether economists on Twitter discriminate in follow-back behavior
based on the gender, race, and university affiliation of bot accounts. Replicated
outputs:

- Figure 1
- Figure 2
- Figure 3a
- Figure 3b
- Table 1a
- Table 1b

## Data

Raw data is not included due to file size. Download the raw data files from:

[Google Drive - Replication Data](https://drive.google.com/drive/folders/1YhsL6-wsv-rxwWQq2sp3aV1bPvUlOH2e?usp=sharing)

Alternatively, download from the official replication package:
https://www.openicpsr.org/openicpsr/project/210084/version/V1/view From the data folder,
download:

- follow_backs.csv
- subject_pool.csv
- subject_pool_scrambled.csv

Place all three data files in `src/final_project_aksoltans/data/raw/`

## Setup

Install [Pixi](https://pixi.sh/), then:

```bash
pixi install
pixi run pytask
pixi run pytest
```

Outputs are saved to `bld/figures/` and `bld/tables/`

## Project Structure

```
src/final_project_aksoltans/
├── config.py                  ← shared paths and constants
├── data_management/           ← data cleaning
│   ├── clean_follow_backs.py
│   ├── clean_subject_pool.py
│   └── task_clean_*.py
├── analysis/                  ← regression engine and data builders
│   ├── fe_ols.py              ← replicates R feols() from fixest
│   ├── fig*_data.py
│   ├── table1_data.py
│   └── task_fig*.py
└── final/                     ← plotting
    ├── plot_fig*.py
    └── task_plot_fig*.py

bld/                           ← generated outputs
├── data/                      ← cleaned parquet files
├── figures/                   ← PNG figures
└── tables/                    ← LaTeX tables

tests/
├── analysis/
└── data_management/
```

## Regression Engine

`fe_ols.py` replicates R's `feols()` from the `fixest` package, including the `ssc()`
small-sample correction for clustered standard errors and alternating projections for
fixed-effects absorption.

Python naming conventions differ from the paper's mathematical notation. The mapping is
as follows:

| Paper/R notation | Python variable |
| ---------------- | --------------- |
| Y                | `y_vec`         |
| X̃                | `x_full`        |
| X̃ (rank-reduced) | `x_mat`         |
| G                | `g_clusters`    |
| K_FE             | `k_fe`          |
| V̂_k              | `vcov_keep`     |
| V̂                | `vcov`          |

## Credits

Ajzenman, N., Ferman, B., & Sant'Anna, P. C. (2024). Discrimination in the Formation of
Academic Networks: A Field Experiment on #EconTwitter. *American Economic Review:
Insights*, 6(4), 501–519. Replication package:
https://www.openicpsr.org/openicpsr/project/210084/version/V1/view

Project template: https://github.com/OpenSourceEconomics/econ-project-templates
