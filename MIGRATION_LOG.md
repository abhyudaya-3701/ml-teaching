# Migration Log

This file documents all content movements during the repository reorganization.

## Completed Movements

### Optimization Content → optimization/
- `slides/gradient-descent.tex` → `optimization/slides/gradient-descent.tex`
- `slides/gradient-descent.pdf` → `optimization/assets/optimization/gradient-descent/notes/Gradient-descent.pdf`
- `coordinate-descent/coordinate_descent.tex` → `optimization/slides/coordinate_descent.tex`
- `subgradient/subgradient.tex` → `optimization/slides/subgradient.tex`
- `subgradient/subgradient_*.pdf` → `optimization/assets/optimization/subgradient/notes/`
- `subgradient/subgradient_1.jpg` → `optimization/assets/optimization/subgradient/notes/`
- `convexity/` → `optimization/slides/convexity/` (convexity is optimization-related)

### Mathematical Content → maths/
- `kkt-conditions/` → `maths/slides/kkt-conditions/`
- `ml-maths/` → `maths/slides/ml-maths/`
- `slides/ml-maths-2-contour.tex` → `maths/slides/ml-maths-2-contour.tex`
- `slides/find-widths.tex` → `maths/slides/find-widths.tex`

### Supervised Learning Content → supervised/
- `slides/bias-variance.tex` → `supervised/slides/bias-variance.tex` (removed duplicate)
- `slides/cross-validation.tex` → `supervised/slides/cross-validation.tex` (removed duplicate)
- `slides/ensemble.tex` → `supervised/slides/ensemble.tex` (removed duplicate)
- `slides/linear-regression.tex` → `supervised/slides/linear-regression.tex` (removed duplicate)
- `slides/logistic-1.tex` → `supervised/slides/logistic-1.tex`

### Neural Networks Content → neural-networks/
- `slides/next-token.pdf` → `neural-networks/assets/next-token-prediction/notes/next-token.pdf`

### Advanced Topics Content → advanced/
- `cnn/tensor-factorisation.ipynb` → `notebooks/tensor-factorisation.ipynb`

### Previously Migrated (from earlier sessions)
- Decision trees content → `supervised/`
- Ensemble content → `supervised/`
- Cross-validation content → `supervised/`
- Bias-variance content → `supervised/`

## Final Cleanup Phase

### PDFs Moved to Proper Categories:
- `1-introduction-ml.pdf` → `basics/slides/`
- `CNN.pdf`, `1d-cnn.pdf`, `mlp.pdf`, `autograd.pdf` → `neural-networks/slides/`
- `KNN-approx.pdf`, `knn.pdf`, `Logistic-*.pdf`, `MovieRecommendation.pdf` → `supervised/slides/`
- `lasso-regression.pdf`, `ridge-regression.pdf`, `Weighted-least.pdf` → `supervised/slides/`
- `svm-intro.pdf`, `svm-soft-margin.pdf` → `supervised/slides/`
- `SGD.pdf` → `optimization/slides/`
- `ml-maths.pdf`, `constrained-*.pdf`, `time_complexity.pdf` → `maths/slides/`
- `unsupervised.pdf` → `unsupervised/slides/`
- `rl.pdf`, `rl.key` → `advanced/slides/`
- `cross-validation.key`, `cross-validation.pdf` → `supervised/slides/`
- `accuracy_convention.pdf` → `basics/slides/`

### Generated PDFs Removed:
- `bias-variance.pdf`, `ensemble.pdf`, `linear-regression.pdf` → Removed (generated from moved .tex files)
- `convexity.pdf`, `find-widths.pdf`, `logistic-1.pdf` → Removed (generated from moved .tex files)
- `ml-maths-2-contour.pdf` → Removed (generated from moved .tex files)

### Auxiliary Files Cleaned:
- All `decision-trees.*` auxiliary files → Removed (.tex moved to supervised/)

### Style Files Moved:
- `mycommonstyle.sty` → `shared/styles/`

## Final Structure Created ✅

### New Category: optimization/
- `optimization/slides/` - All optimization-related .tex files
- `optimization/assets/optimization/` - Optimization figures and diagrams
- `optimization/assets/optimization/*/notes/` - Handwritten optimization notes

### Final slides/ directory contains only:
- `misc.tex` and `misc.pdf` - General miscellaneous content
- `misc/` folder - Guest lectures, quizzes, and other misc presentations

## Complete Reorganization Achieved ✅

## Rules Applied
1. **Slides** (.tex files) → `category/slides/`
2. **Assets** (figures, diagrams) → `category/assets/topic-name/`
3. **Handwritten notes** → `category/assets/topic-name/notes/`
4. **Notebooks** → main `/notebooks/` directory (flat structure)
5. **Presentations** (.key, .pptx) → `category/slides/`

## Cleanup Actions
- Remove duplicate .tex files from slides/ after moving to proper locations
- Clean up empty directories
- Ensure all assets follow proper folder structure