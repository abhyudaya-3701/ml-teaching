# Content Quality Review - Issues & Warnings Log

**Generated**: January 2025  
**Audit Tool**: `scripts/audit_content.py`  
**Files Analyzed**: 86 files (71 LaTeX, 18 Markdown)

## Executive Summary

- **Critical Issues**: 271 
- **Warnings**: 1,121
- **Overall Status**: Repository structure excellent, content quality needs attention

## Critical Issues Breakdown (271 total)

### Mathematical Notation Inconsistencies (78 issues)
Issues with mathematical notation not following conventions.sty standards:

**Files with vector notation issues** (inconsistent_vectors):
- `basics/slides/accuracy-convention.tex`: 2 instances of `\mathbf{x}` instead of `\vx`
- `basics/tutorials/mathematical-conventions.tex`: 10 instances
- `build-temp/conventions-sanitized.tex`: 39 instances
- `build-temp/conventions.tex`: 39 instances
- `docs/CONVENTIONS_LOG.md`: 11 instances
- `supervised/slides/decision-trees.tex`: 1 instance
- `supervised/slides/linear-regression.tex`: 1 instance
- `supervised/slides/logistic-regression.tex`: 3 instances

**Files with matrix notation issues** (inconsistent_matrices):
- `basics/slides/accuracy-convention.tex`: 13 instances of `\mathrm{A}` instead of `\mA`
- `maths/slides/mathematical-ml.tex`: 8 instances
- `optimization/slides/coordinate-descent.tex`: 4 instances
- `supervised/slides/logistic-regression.tex`: 2 instances

**Files with set notation issues** (inconsistent_sets):
- Multiple files using `\mathbb{R}` instead of `\Real`
- `supervised/slides/svm-*` files: Various instances

### Missing Figure Files (62 issues)
Referenced figures that don't exist in the repository:

**Advanced Topics**:
- `advanced/slides/forecasting.tex`: 11 missing figures (forecast, domain, properties, etc.)

**Mathematics**:
- `maths/slides/mvn.tex`: 5 missing figures (fig1, fig2, fig3, cross-non-zero, cross-0)
- `maths/slides/kkt-conditions.tex`: 3 missing figures (img1, img2, img3)

**Optimization**:
- `optimization/slides/convexity.tex`: 9 missing figures (y-x2, y-absx, y-ex, etc.)
- `optimization/slides/subgradient.tex`: 4 missing figures (subgradient_1-3.pdf)

**Supervised Learning**:
- `supervised/slides/bias-variance.tex`: 19 missing figures (dataset-1, decision boundaries, etc.)
- `supervised/slides/svm-kernel.tex`: 11 missing figures (pik1-11.png)
- `supervised/slides/lasso-regression.tex`: 2 missing figures (Lasso/lasso_2.png, Lasso/lasso_3.png)

**Unsupervised Learning**:
- `unsupervised/slides/unsupervised.tex`: 10 missing figures (gt_iris.png, k_1.png, etc.)

### Spelling & Terminology Issues (45 issues)
Inconsistent terminology usage:

**"gradient-descent" vs "gradient descent"** (21 instances):
- README.md: 1 instance
- docs/COMPILATION_ISSUES.md: 4 instances  
- docs/CONTENT_AUDIT_SUMMARY.md: 1 instance
- docs/CONVENTIONS_LOG.md: 7 instances
- docs/MIGRATION_LOG.md: 6 instances
- optimization/slides/gradient-descent.tex: 2 instances
- supervised/slides/lasso-regression.tex: 4 instances

**"data set" vs "dataset"** (5 instances):
- basics/slides/accuracy-convention.tex: 1 instance
- docs/CONTENT_AUDIT_SUMMARY.md: 1 instance  
- supervised/slides/ridge-regression.tex: 3 instances
- unsupervised/slides/unsupervised.tex: 1 instance

**Other terminology** (19 instances):
- "cross validation" vs "cross-validation": 3 instances
- "machine-learning" vs "machine learning": 2 instances
- "over-fitting"/"over fitting" vs "overfitting": 4 instances
- "hyper-parameter" vs "hyperparameter": 1 instance
- "crossvalidation" vs "cross-validation": 1 instance

### Math Formatting Issues (52 issues)
LaTeX mathematical formatting problems:

**Missing spaces around inline math**: 28 files affected
- Most `.tex` files have instances of `$math$text` instead of `$math$ text`

**Unmatched braces**: 8 files affected
- `advanced/slides/forecasting.tex`: -1 difference
- `maths/slides/mathematical-ml.tex`: -1 difference
- `supervised/slides/bayesian-nets.tex`: -2 difference
- `supervised/slides/lasso-regression.tex`: +1 difference
- etc.

### Missing Input Files (34 issues)
LaTeX files referencing non-existent includes:

**Missing conventions references**: 22 instances
- Multiple files referencing `../../conventions` or `../../conventions-sanitized.tex`

**Missing diagram files**: 12 instances
- Various `.tex` files in supervised/assets/ensemble/diagrams/

## Warnings Breakdown (1,121 total)

### Line Length Issues (892 warnings)
Lines exceeding 120 characters:

**Most problematic files**:
- `maths/slides/mvn2.tex`: 23 very long lines (max 850 chars)
- `basics/slides/accuracy-convention.tex`: 17 very long lines
- `basics/tutorials/accuracy-convention.tex`: 21 very long lines
- `neural-networks/slides/mlp.tex`: 26 very long lines

### LaTeX Package Warnings (45 warnings)
Missing package declarations:

**Common missing packages**:
- `\usepackage{graphicx}` for `\includegraphics`: 15 files
- `\usepackage{hyperref}` for `\href`: 8 files
- `\usepackage{amssymb}` for `\mathbb`: 12 files
- `\usepackage{tikz}` for TikZ diagrams: 10 files

### Formatting Issues (184 warnings)
LaTeX formatting and structure issues:

**Blank line issues**: 89 instances
- Too many consecutive blank lines in various files

**Math display issues**: 21 instances  
- Display math followed/preceded immediately by text

**Missing sections**: 74 instances
- Files without proper `\section{}` structure

## Priority Recommendations

### High Priority (Critical for Content Quality)

1. **Fix Mathematical Notation** (78 issues)
   - Replace `\mathbf{x}` with `\vx` throughout
   - Replace `\mathrm{A}` with `\mA` for matrices
   - Replace `\mathbb{R}` with `\Real` for sets
   - **Tool**: Create automated script using `shared/styles/conventions.sty`

2. **Standardize Terminology** (45 issues)
   - "gradient descent" (not "gradient-descent")
   - "dataset" (not "data set") 
   - "cross-validation" (not "cross validation")
   - **Tool**: Automated find-replace script

3. **Fix Math Spacing** (52 issues)
   - Add spaces around inline math: `$x$ and $y$` not `$x$and$y$`
   - **Tool**: Regex replacement in LaTeX files

### Medium Priority (Content Completeness)

4. **Create Missing Figures** (62 issues)
   - Generate placeholder figures for broken references
   - Update figure paths or create actual figures
   - **Tool**: `scripts/check_missing_figures.py`

5. **Fix Package Dependencies** (45 issues)
   - Add proper `\usepackage{}` declarations
   - **Tool**: LaTeX compilation testing

### Low Priority (Code Quality)

6. **Line Length Cleanup** (892 issues)
   - Break long lines for readability
   - **Tool**: Automated formatter

7. **LaTeX Structure** (184 issues)
   - Add proper sections to files
   - Clean up excessive blank lines
   - **Tool**: LaTeX formatter

## Automated Fixes Available

### Ready for Automation
- ✅ Terminology standardization (45 issues)
- ✅ Math notation consistency (78 issues)  
- ✅ Math spacing fixes (52 issues)
- ✅ Package declaration additions (45 issues)

### Requires Manual Review
- ❓ Missing figure creation (62 issues)
- ❓ Unmatched braces resolution (8 issues)
- ❓ Content structure improvements (184 warnings)

## Implementation Plan

### Phase 1: Critical Fixes (Week 1)
```bash
# Fix terminology
python scripts/fix_terminology.py

# Fix mathematical notation  
python scripts/fix_math_notation.py

# Fix math spacing
python scripts/fix_math_spacing.py
```

### Phase 2: Content Completeness (Week 2)
```bash
# Generate missing figure placeholders
python scripts/create_missing_figures.py

# Add missing package declarations
python scripts/fix_latex_packages.py
```

### Phase 3: Quality Improvements (Week 3)
```bash
# Format line lengths
python scripts/format_line_lengths.py

# Clean up structure
python scripts/fix_latex_structure.py
```

## Tracking Progress

- **Initial State**: 271 issues, 1,121 warnings
- **Target Goal**: <50 issues, <200 warnings
- **Success Metrics**: 
  - All mathematical notation consistent
  - All terminology standardized
  - All referenced figures exist
  - Clean LaTeX compilation

---

*This log will be updated as issues are resolved. Use `python scripts/audit_content.py` to regenerate current status.*