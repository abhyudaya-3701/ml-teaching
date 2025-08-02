# Supervised Learning

## Content Overview
Comprehensive materials on supervised learning algorithms including linear models, tree-based methods, SVMs, and ensemble techniques.

## Key Topics
- Linear regression and ridge regression
- Logistic regression  
- Decision trees
- Ensemble methods
- k-NN algorithms
- Support Vector Machines (SVM)
- Naive Bayes
- Feature selection
- Cross-validation
- Bias-variance tradeoff

## Important Asset PDFs
The following PDFs are assets (stored in supervised/assets/) and should NOT be deleted:
- `coordinate-rho.pdf`
- `coordinate-thresholding.pdf` 
- `coordinate-vis.pdf`
- `coordinate-descent-fail.pdf`
- `lasso-sparse.pdf`
- `ridge-intercept.pdf`
- `ridge-cv.pdf`
- `ridge-gd.pdf`

These are figures/visualizations used in the slides and are automatically copied from:
- `supervised/assets/lasso-regression/figures/`
- `supervised/assets/ridge-regression/figures/`
- `optimization/assets/`

## Asset Management
- Assets are preserved during `make distclean`
- Missing asset PDFs are restored from their source directories
- Never manually delete files matching the above patterns
- If assets go missing, they can be restored using the backup copies

## Build System
- Standard Makefile with proper distclean target
- Preserves asset PDFs while cleaning generated ones
- Uses XeLaTeX for compilation
- Integrated with root rebuild_all.sh script

## Content Structure
Most slides use the shared styling system with professional colorboxes for:
- Definitions of algorithms
- Examples and case studies  
- Key algorithmic insights
- Mathematical formulations

## Recent Fixes
- Fixed Makefile distclean to preserve asset PDFs
- Restored missing coordinate descent and regression visualization PDFs
- Ensured 100% build success rate for all supervised learning slides
- Maintained proper asset-source directory relationships