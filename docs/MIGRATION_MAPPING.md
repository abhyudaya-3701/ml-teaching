# Migration Mapping

This document tracks the migration of files from the old flat structure to the new topic-based organization.

## Completed Migrations

### Decision Trees (slides/decision-trees.*)
- **LaTeX**: `slides/decision-trees.tex` → `supervised/slides/decision-trees.tex`
- **PDF**: `slides/decision-trees.pdf` → `supervised/slides/decision-trees.pdf` (auto-generated)
- **Assets**: 
  - `shared/figures/diagrams/decision-trees/` → `supervised/assets/decision-trees/diagrams/`
  - `shared/figures/decision-trees/` → `supervised/assets/decision-trees/figures/`
  - `shared/figures/dt_weighted/` → `supervised/assets/decision-trees/figures/dt_weighted/`

### Shared Resources
- **Style**: `slides/mycommonstyle.sty` → `shared/styles/mycommonstyle.sty`
- **Datasets**: `datasets/` → `shared/datasets/`
- **Figures**: `figures/` → `shared/figures/`
- **Styles**: `styles.scss`, `styles-dark.scss` → `shared/styles/`
- **Notation**: `notation.sty` → `shared/notation/`

## New Topic Structure

```
ml-teaching/
├── shared/
│   ├── datasets/
│   ├── figures/
│   ├── styles/
│   │   ├── mycommonstyle.sty
│   │   ├── styles.scss
│   │   └── styles-dark.scss
│   └── notation/
│       └── notation.sty
├── notebooks/               # ← KEEP FLAT (all notebooks here)
│   ├── decision-tree-*.ipynb
│   ├── entropy.ipynb
│   ├── logistic-*.ipynb
│   └── ...
├── supervised/
│   ├── assets/
│   │   └── decision-trees/
│   │       ├── diagrams/
│   │       └── figures/
│   └── slides/
│       └── decision-trees.tex
├── maths/
│   └── slides/
│       ├── convexity/
│       ├── coordinate-descent/
│       ├── gradient-descent/
│       ├── kkt-conditions/
│       ├── ml-maths/
│       └── subgradient/
└── [other topics...]
```

## Path Updates Made

### decision-trees.tex
- Style: `mycommonstyle` → `../../shared/styles/mycommonstyle`
- Diagrams: `../diagrams/decision-trees/` → `../assets/decision-trees/diagrams/`
- Figures: `../figures/decision-trees/` → `../assets/decision-trees/figures/`
- Weighted: `../figures/dt_weighted/` → `../assets/decision-trees/figures/dt_weighted/`

## What You Want to Move

### LaTeX Files (slides/*.tex → topic/slides/)
- `slides/accuracy_convention.tex` → `basics/slides/`
- `slides/bias-variance.tex` → `supervised/slides/`
- `slides/cross-validation.tex` → `supervised/slides/`
- `slides/ensemble.tex` → `supervised/slides/`
- `slides/gradient-descent.tex` → `maths/slides/`
- `slides/linear-regression.tex` → `supervised/slides/`
- `slides/logistic-1.tex` → `supervised/slides/`
- `slides/ml-maths-2-contour.tex` → `maths/slides/`
- `slides/misc.tex` → `advanced/slides/`

### Root LaTeX Files (need PDF generation first)
- `MLP.tex` → `neural-networks/slides/`
- `rl.tex` → `advanced/slides/`
- `svm-*.tex` → `supervised/slides/svm/`

### Folders with Assets (folder/ → topic/assets/)
- `bias-variance/` → `supervised/assets/bias-variance/`
- `cnn/` → `neural-networks/assets/cnn/`
- `ensemble/` → `supervised/assets/ensemble/`
- `feature-selection/` → `supervised/assets/feature-selection/`
- `forecasting/` → `advanced/assets/forecasting/`
- `knn/` → `supervised/assets/knn/`
- `Lasso/` → `supervised/assets/lasso/`
- `linear-reg/` → `supervised/assets/linear-regression/`
- `mvn/` → `unsupervised/assets/mvn/`
- `naive-bayes/` → `supervised/assets/naive-bayes/`
- `ridge/` → `supervised/assets/ridge/`
- `SVM/` → `supervised/assets/svm/`

### Keep As-Is
- `notebooks/` → **KEEP FLAT** (all notebooks stay here)
- `shared/` → **KEEP** (datasets, figures, styles, notation)
- `slides/` → **KEEP DURING MIGRATION** (original location preserved)

## Build System

Each topic has its own Makefile:
- `make all` - builds all LaTeX files in the topic
- `make clean` - removes temporary files
- `make status` - shows topic contents

Master Makefile:
- `make all` - builds all topics
- `make supervised` - builds specific topic
- `make clean` - cleans all topics

## Notes

- All notebook links in LaTeX files point to `https://nipunbatra.github.io/ml-teaching/notebooks/`
- Assets are now topic-specific, not shared (better organization)
- Style files and common resources remain in `shared/`
- Original `slides/` folder preserved during migration