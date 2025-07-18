#!/bin/bash

# Refined migration script based on current state
echo "=== Finishing ML Teaching Content Migration ==="

# Function to safely move content
safe_move() {
    local source="$1"
    local dest="$2"
    local desc="$3"
    
    if [ -e "$source" ]; then
        if [ -e "$dest" ]; then
            echo "  SKIP: $dest already exists"
        else
            echo "  MOVE: $source -> $dest"
            mv "$source" "$dest"
        fi
    else
        echo "  MISSING: $source"
    fi
}

# Continue moving remaining SUPERVISED content
echo ""
echo "=== Moving SUPERVISED Content ==="
safe_move "linear-reg" "supervised/slides/linear-regression"
safe_move "Lasso" "supervised/slides/lasso"
safe_move "ridge" "supervised/slides/ridge"
safe_move "naive-bayes" "supervised/slides/naive-bayes"
safe_move "knn" "supervised/slides/knn"
safe_move "SVM" "supervised/slides/svm"
safe_move "bias-variance" "supervised/slides/bias-variance"
safe_move "ensemble" "supervised/slides/ensemble"
safe_move "feature-selection" "supervised/slides/feature-selection"
safe_move "linear-regression-geometric" "supervised/slides/linear-regression-geometric"
safe_move "linear-regression-time-complexity" "supervised/slides/linear-regression-time-complexity"

# Move UNSUPERVISED content
echo ""
echo "=== Moving UNSUPERVISED Content ==="
safe_move "mvn" "unsupervised/slides/mvn"
safe_move "unsupervised" "unsupervised/slides/clustering"

# Move NEURAL NETWORKS content
echo ""
echo "=== Moving NEURAL NETWORKS Content ==="
safe_move "cnn" "neural-networks/slides/cnn"
safe_move "MLP.tex" "neural-networks/slides/mlp.tex"

# Move ADVANCED content
echo ""
echo "=== Moving ADVANCED Content ==="
safe_move "forecasting" "advanced/slides/forecasting"
safe_move "rl.tex" "advanced/slides/rl.tex"

# Move remaining math content
echo ""
echo "=== Moving Remaining MATHS Content ==="
safe_move "shuffling" "maths/slides/shuffling"

# Move individual SVM files to supervised
echo ""
echo "=== Moving Individual SVM Files ==="
mkdir -p supervised/slides/svm-individual
for file in svm-*.tex svm-*.pdf svm-*.nav svm-*.out svm-*.toc; do
    if [ -e "$file" ]; then
        safe_move "$file" "supervised/slides/svm-individual/$file"
    fi
done

# Move remaining LaTeX files from slides/ to appropriate topics
echo ""
echo "=== Moving LaTeX Files from slides/ ==="
if [ -d "slides" ]; then
    # Move remaining .tex files that are in slides/
    for file in slides/*.tex; do
        if [ -e "$file" ]; then
            basename_file=$(basename "$file")
            case "$basename_file" in
                "accuracy_convention.tex")
                    safe_move "$file" "basics/slides/accuracy_convention.tex"
                    ;;
                "ml-maths-2-contour.tex")
                    safe_move "$file" "maths/slides/ml-maths-2-contour.tex"
                    ;;
                "gradient-descent.tex")
                    safe_move "$file" "maths/slides/gradient-descent.tex"
                    ;;
                "convexity.tex")
                    safe_move "$file" "maths/slides/convexity.tex"
                    ;;
                "constrained-1.tex"|"constrained-2.tex")
                    safe_move "$file" "maths/slides/$basename_file"
                    ;;
                "linear-regression.tex")
                    safe_move "$file" "supervised/slides/linear-regression.tex"
                    ;;
                "logistic-1.tex")
                    safe_move "$file" "supervised/slides/logistic-1.tex"
                    ;;
                "bias-variance.tex")
                    safe_move "$file" "supervised/slides/bias-variance.tex"
                    ;;
                "decision-trees.tex"|"ensemble.tex"|"cross-validation.tex"|"find-widths.tex"|"time_complexity.tex")
                    safe_move "$file" "supervised/slides/$basename_file"
                    ;;
                "misc.tex")
                    safe_move "$file" "advanced/slides/misc.tex"
                    ;;
                *)
                    echo "  UNKNOWN: $file (needs manual categorization)"
                    ;;
            esac
        fi
    done
fi

# Move notebooks to appropriate topics
echo ""
echo "=== Moving Notebooks ==="
if [ -d "notebooks" ]; then
    # BASICS notebooks
    safe_move "notebooks/rule-based-vs-ml.ipynb" "basics/notebooks/rule-based-vs-ml.ipynb"
    safe_move "notebooks/numpy-pandas-basics.ipynb" "basics/notebooks/numpy-pandas-basics.ipynb"
    safe_move "notebooks/anscombe.ipynb" "basics/notebooks/anscombe.ipynb"
    safe_move "notebooks/dummy-baselines.ipynb" "basics/notebooks/dummy-baselines.ipynb"
    safe_move "notebooks/tips.ipynb" "basics/notebooks/tips.ipynb"
    
    # MATHS notebooks
    safe_move "notebooks/Maths for ML-2.ipynb" "maths/notebooks/maths-for-ml-2.ipynb"
    safe_move "notebooks/taylor-series.ipynb" "maths/notebooks/taylor-series.ipynb"
    safe_move "notebooks/contour.ipynb" "maths/notebooks/contour.ipynb"
    safe_move "notebooks/autodiff.ipynb" "maths/notebooks/autodiff.ipynb"
    safe_move "notebooks/Gradient Descent.ipynb" "maths/notebooks/gradient-descent.ipynb"
    safe_move "notebooks/Gradient Descent-2d.ipynb" "maths/notebooks/gradient-descent-2d.ipynb"
    
    # SUPERVISED notebooks
    safe_move "notebooks/Linear Regression Notebook.ipynb" "supervised/notebooks/linear-regression.ipynb"
    safe_move "notebooks/Ridge.ipynb" "supervised/notebooks/ridge.ipynb"
    safe_move "notebooks/geometric-linear-regression.ipynb" "supervised/notebooks/geometric-linear-regression.ipynb"
    safe_move "notebooks/logistic-*.ipynb" "supervised/notebooks/" 2>/dev/null || true
    safe_move "notebooks/svm*.ipynb" "supervised/notebooks/" 2>/dev/null || true
    safe_move "notebooks/decision-tree*.ipynb" "supervised/notebooks/" 2>/dev/null || true
    safe_move "notebooks/ensemble*.ipynb" "supervised/notebooks/" 2>/dev/null || true
    safe_move "notebooks/bias-variance.ipynb" "supervised/notebooks/bias-variance.ipynb"
    safe_move "notebooks/cross-validation*.ipynb" "supervised/notebooks/" 2>/dev/null || true
    safe_move "notebooks/SFS_and_BFS.ipynb" "supervised/notebooks/feature-selection.ipynb"
    safe_move "notebooks/hyperparameter-optimisation.ipynb" "supervised/notebooks/hyperparameter-optimisation.ipynb"
    
    # UNSUPERVISED notebooks
    safe_move "notebooks/pca.ipynb" "unsupervised/notebooks/pca.ipynb"
    safe_move "notebooks/curse-dimensionality.ipynb" "unsupervised/notebooks/curse-dimensionality.ipynb"
    
    # NEURAL NETWORKS notebooks
    safe_move "notebooks/cnn*.ipynb" "neural-networks/notebooks/" 2>/dev/null || true
    safe_move "notebooks/1d-cnn.ipynb" "neural-networks/notebooks/1d-cnn.ipynb"
    safe_move "notebooks/mnist-digits.ipynb" "neural-networks/notebooks/mnist-digits.ipynb"
    safe_move "notebooks/object-detection.ipynb" "neural-networks/notebooks/object-detection.ipynb"
    safe_move "notebooks/generate-image.ipynb" "neural-networks/notebooks/generate-image.ipynb"
    safe_move "notebooks/siren.ipynb" "neural-networks/notebooks/siren.ipynb"
    safe_move "notebooks/autoregressive_model.ipynb" "neural-networks/notebooks/autoregressive_model.ipynb"
    
    # ADVANCED notebooks
    safe_move "notebooks/rl-*.ipynb" "advanced/notebooks/" 2>/dev/null || true
    safe_move "notebooks/movie-recommendation*.ipynb" "advanced/notebooks/" 2>/dev/null || true
    safe_move "notebooks/ZeroShot_FewShot.ipynb" "advanced/notebooks/zero-shot-few-shot.ipynb"
    safe_move "notebooks/Sklearn_on_GPU.ipynb" "advanced/notebooks/sklearn-on-gpu.ipynb"
    safe_move "notebooks/guest-lecture" "advanced/notebooks/guest-lecture"
fi

echo ""
echo "=== Migration Complete ==="
echo "Check each topic with: make status"
echo "Build all: make all"
echo "Deploy to slides/: make deploy"