#\!/bin/bash

echo "=== ML TEACHING REPOSITORY COMPILATION STATUS REPORT ==="
echo "Generated: $(date)"
echo ""

total_tex=0
successful=0
failed=0

test_file() {
    local dir=$1
    local file=$2
    local full_path="$dir/slides/$file"
    
    if [ -f "$full_path" ]; then
        total_tex=$((total_tex + 1))
        cd "$dir/slides"
        if pdflatex -interaction=batchmode "$file" >/dev/null 2>&1; then
            echo "✅ $dir/$file"
            successful=$((successful + 1))
        else
            echo "❌ $dir/$file"
            failed=$((failed + 1))
        fi
        cd - >/dev/null
    fi
}

echo "### BASICS ###"
test_file "basics" "accuracy-convention.tex"
test_file "basics" "misc.tex" 
test_file "basics" "shuffling.tex"

echo ""
echo "### MATHEMATICS ###"
test_file "maths" "constrained-1.tex"
test_file "maths" "constrained-2.tex"
test_file "maths" "ml-maths-2-contour.tex"
test_file "maths" "mvn.tex"
test_file "maths" "mvn2.tex"

echo ""
echo "### NEURAL NETWORKS ###"
test_file "neural-networks" "next-token-prediction.tex"
test_file "neural-networks" "movie-recommendation.tex" # This should be in supervised
test_file "neural-networks" "mlp.tex"
test_file "neural-networks" "cnn.tex"
test_file "neural-networks" "autograd.tex"
test_file "neural-networks" "1d-cnn.tex"

echo ""
echo "### SUPERVISED LEARNING ###"
test_file "supervised" "movie-recommendation.tex"
test_file "supervised" "linear-regression.tex"
test_file "supervised" "logistic-regression.tex"
test_file "supervised" "knn.tex"
test_file "supervised" "naive-bayes.tex"
test_file "supervised" "decision-trees.tex"
test_file "supervised" "ensemble.tex"
test_file "supervised" "bias-variance.tex"
test_file "supervised" "lasso-regression.tex"
test_file "supervised" "ridge-regression.tex"
test_file "supervised" "svm-intro.tex"
test_file "supervised" "svm-soft-margin.tex"
test_file "supervised" "svm-kernel.tex"

echo ""
echo "### ADVANCED ###"
test_file "advanced" "rl.tex"
test_file "advanced" "forecasting.tex"

echo ""
echo "### UNSUPERVISED ###"
test_file "unsupervised" "unsupervised.tex"

echo ""
echo "=== SUMMARY ==="
echo "Total .tex files tested: $total_tex"
echo "Successful compilations: $successful"
echo "Failed compilations: $failed"
echo "Success rate: $(echo "scale=1; $successful * 100 / $total_tex" | bc)%"
