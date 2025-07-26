#!/bin/bash

# Dry run script to check what would be moved
echo "=== ML Teaching Content Migration Check ==="
echo "This shows what WOULD be moved (dry run only)"
echo ""

# Function to check content without moving
check_content() {
    local source="$1"
    local dest="$2"
    local desc="$3"
    
    if [ -e "$source" ]; then
        if [ -e "$dest" ]; then
            echo "  CONFLICT: $source -> $dest (destination exists)"
        else
            echo "  OK: $source -> $dest"
        fi
    else
        echo "  MISSING: $source (not found)"
    fi
}

echo "=== Shared Resources ==="
check_content "datasets" "shared/datasets" "datasets"
check_content "figures" "shared/figures" "figures"
check_content "diagrams" "shared/diagrams" "diagrams"
check_content "styles.scss" "shared/styles/styles.scss" "light styles"
check_content "styles-dark.scss" "shared/styles/styles-dark.scss" "dark styles"
check_content "notation.sty" "shared/notation/notation.sty" "notation style"

echo ""
echo "=== MATHS Content ==="
check_content "ml-maths" "maths/slides/ml-maths" "ML maths slides"
check_content "convexity" "maths/slides/convexity" "convexity slides"
check_content "gradient-descent" "maths/slides/gradient-descent" "gradient descent slides"
check_content "coordinate-descent" "maths/slides/coordinate-descent" "coordinate descent slides"
check_content "subgradient" "maths/slides/subgradient" "subgradient slides"
check_content "kkt-conditions" "maths/slides/kkt-conditions" "KKT conditions slides"
check_content "shuffling" "maths/slides/shuffling" "shuffling slides"

echo ""
echo "=== SUPERVISED Content ==="
check_content "linear-reg" "supervised/slides/linear-regression" "linear regression slides"
check_content "Lasso" "supervised/slides/lasso" "Lasso regression slides"
check_content "ridge" "supervised/slides/ridge" "Ridge regression slides"
check_content "naive-bayes" "supervised/slides/naive-bayes" "Naive Bayes slides"
check_content "knn" "supervised/slides/knn" "KNN slides"
check_content "SVM" "supervised/slides/svm" "SVM slides"
check_content "bias-variance" "supervised/slides/bias-variance" "bias-variance slides"
check_content "ensemble" "supervised/slides/ensemble" "ensemble slides"
check_content "feature-selection" "supervised/slides/feature-selection" "feature selection slides"

echo ""
echo "=== Individual Files ==="
find . -maxdepth 1 -name "*.tex" | while read file; do
    echo "  STANDALONE: $file"
done

echo ""
echo "=== Summary ==="
echo "Run './migrate_content.sh' to perform the actual migration"
echo "Make sure to commit current state first: git add -A && git commit -m 'Before migration'"