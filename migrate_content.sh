#!/bin/bash

# Content Migration Script for ML Teaching Repository
# This script safely moves content to the new topic-based structure

echo "=== ML Teaching Content Migration ==="
echo "This script will move content to the new topic structure"
echo "Current slides/ will be preserved as slides-backup/"
echo ""

# Create backup of current slides
if [ -d "slides" ]; then
    echo "Creating backup of current slides..."
    cp -r slides slides-backup
fi

# Function to move content with conflict checking
move_content() {
    local source="$1"
    local dest="$2"
    local desc="$3"
    
    if [ -e "$source" ]; then
        echo "Moving $desc: $source -> $dest"
        if [ -e "$dest" ]; then
            echo "  WARNING: $dest already exists, skipping..."
        else
            mv "$source" "$dest"
        fi
    else
        echo "  $source not found, skipping..."
    fi
}

# Move shared resources
echo ""
echo "=== Moving Shared Resources ==="
move_content "datasets" "shared/datasets" "datasets"
move_content "figures" "shared/figures" "figures"
move_content "diagrams" "shared/diagrams" "diagrams"
move_content "styles.scss" "shared/styles/styles.scss" "light styles"
move_content "styles-dark.scss" "shared/styles/styles-dark.scss" "dark styles"
move_content "notation.sty" "shared/notation/notation.sty" "notation style"

# Move MATHS content
echo ""
echo "=== Moving MATHS Content ==="
move_content "ml-maths" "maths/slides/ml-maths" "ML maths slides"
move_content "convexity" "maths/slides/convexity" "convexity slides"
move_content "gradient-descent" "maths/slides/gradient-descent" "gradient descent slides"
move_content "coordinate-descent" "maths/slides/coordinate-descent" "coordinate descent slides"
move_content "subgradient" "maths/slides/subgradient" "subgradient slides"
move_content "kkt-conditions" "maths/slides/kkt-conditions" "KKT conditions slides"
move_content "shuffling" "maths/slides/shuffling" "shuffling slides"

# Move SUPERVISED content
echo ""
echo "=== Moving SUPERVISED Content ==="
move_content "linear-reg" "supervised/slides/linear-regression" "linear regression slides"
move_content "linear-regression-geometric" "supervised/slides/linear-regression-geometric" "geometric linear regression"
move_content "linear-regression-time-complexity" "supervised/slides/linear-regression-time-complexity" "time complexity"
move_content "Lasso" "supervised/slides/lasso" "Lasso regression slides"
move_content "ridge" "supervised/slides/ridge" "Ridge regression slides"
move_content "naive-bayes" "supervised/slides/naive-bayes" "Naive Bayes slides"
move_content "knn" "supervised/slides/knn" "KNN slides"
move_content "SVM" "supervised/slides/svm" "SVM slides"
move_content "bias-variance" "supervised/slides/bias-variance" "bias-variance slides"
move_content "ensemble" "supervised/slides/ensemble" "ensemble slides"
move_content "feature-selection" "supervised/slides/feature-selection" "feature selection slides"

# Move UNSUPERVISED content
echo ""
echo "=== Moving UNSUPERVISED Content ==="
move_content "unsupervised" "unsupervised/slides/clustering" "unsupervised slides"
move_content "mvn" "unsupervised/slides/mvn" "multivariate normal slides"

# Move NEURAL NETWORKS content
echo ""
echo "=== Moving NEURAL NETWORKS Content ==="
move_content "cnn" "neural-networks/slides/cnn" "CNN slides"
move_content "MLP.tex" "neural-networks/slides/mlp.tex" "MLP slides"

# Move ADVANCED content
echo ""
echo "=== Moving ADVANCED Content ==="
move_content "forecasting" "advanced/slides/forecasting" "forecasting slides"
move_content "rl.tex" "advanced/slides/rl.tex" "reinforcement learning slides"

# Move individual LaTeX files from slides/
echo ""
echo "=== Moving Individual LaTeX Files ==="
if [ -d "slides" ]; then
    # BASICS
    move_content "slides/accuracy_convention.tex" "basics/slides/accuracy_convention.tex" "accuracy convention"
    
    # MATHS
    move_content "slides/ml-maths-2-contour.tex" "maths/slides/ml-maths-2-contour.tex" "ML maths contour"
    move_content "slides/gradient-descent.tex" "maths/slides/gradient-descent.tex" "gradient descent"
    move_content "slides/convexity.tex" "maths/slides/convexity.tex" "convexity"
    move_content "slides/constrained-1.tex" "maths/slides/constrained-1.tex" "constrained optimization 1"
    move_content "slides/constrained-2.tex" "maths/slides/constrained-2.tex" "constrained optimization 2"
    
    # SUPERVISED
    move_content "slides/linear-regression.tex" "supervised/slides/linear-regression.tex" "linear regression"
    move_content "slides/logistic-1.tex" "supervised/slides/logistic-1.tex" "logistic regression"
    move_content "slides/bias-variance.tex" "supervised/slides/bias-variance.tex" "bias variance"
    move_content "slides/decision-trees.tex" "supervised/slides/decision-trees.tex" "decision trees"
    move_content "slides/ensemble.tex" "supervised/slides/ensemble.tex" "ensemble"
    move_content "slides/cross-validation.tex" "supervised/slides/cross-validation.tex" "cross validation"
    move_content "slides/find-widths.tex" "supervised/slides/find-widths.tex" "find widths"
    move_content "slides/time_complexity.tex" "supervised/slides/time_complexity.tex" "time complexity"
    
    # ADVANCED
    move_content "slides/misc.tex" "advanced/slides/misc.tex" "miscellaneous"
fi

echo ""
echo "=== Migration Summary ==="
echo "Content has been moved to topic-based structure"
echo "Original slides/ backed up to slides-backup/"
echo "Run 'make status' to see what's in each topic"
echo "Run 'make all' to build all LaTeX files"
echo "Run 'make deploy' to copy PDFs back to slides/ for Quarto"
echo ""
echo "=== Next Steps ==="
echo "1. Check each topic directory for correct content"
echo "2. Move any remaining notebooks to appropriate topics"
echo "3. Update any hardcoded paths in LaTeX files"
echo "4. Test compilation with 'make all'"