#\!/bin/bash

echo "=== ML TEACHING REPOSITORY - REFINED COMPILATION STATUS ==="
echo "Generated: $(date)"
echo ""

real_failures=0
warning_failures=0
successes=0
total=0

analyze_compilation() {
    local dir=$1
    local file=$2
    local full_path="$dir/slides/$file"
    
    if [ \! -f "$full_path" ]; then
        return
    fi
    
    total=$((total + 1))
    cd "$dir/slides"
    
    # Capture compilation output
    output=$(pdflatex -interaction=nonstopmode "$file" 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ $dir/$file - SUCCESS"
        successes=$((successes + 1))
    elif echo "$output" | grep -q "Output written on"; then
        echo "⚠️  $dir/$file - WARNING (PDF generated but LaTeX warnings)"
        warning_failures=$((warning_failures + 1))
    else
        echo "❌ $dir/$file - REAL FAILURE"
        real_failures=$((real_failures + 1))
        # Show the actual error
        echo "   Error: $(echo "$output" | grep -E "(Fatal error|Error|\! )" | tail -1)"
    fi
    
    cd - >/dev/null
}

echo "### KEY SLIDES ANALYSIS ###"
echo ""

echo "## Includepdf Wrapper Slides ##"
analyze_compilation "neural-networks" "next-token-prediction.tex"
analyze_compilation "supervised" "movie-recommendation.tex"
analyze_compilation "neural-networks" "mlp.tex"
analyze_compilation "neural-networks" "cnn.tex"
analyze_compilation "advanced" "rl.tex"
analyze_compilation "maths" "constrained-1.tex"

echo ""
echo "## Standard LaTeX Slides ##"
analyze_compilation "supervised" "linear-regression.tex"
analyze_compilation "supervised" "ensemble.tex"
analyze_compilation "supervised" "bias-variance.tex"
analyze_compilation "basics" "shuffling.tex"
analyze_compilation "maths" "ml-maths-2-contour.tex"

echo ""
echo "## Known Problem Slides ##"
analyze_compilation "supervised" "knn.tex"
analyze_compilation "supervised" "lasso-regression.tex"
analyze_compilation "supervised" "decision-trees.tex"
analyze_compilation "supervised" "logistic-regression.tex"

echo ""
echo "=== REFINED SUMMARY ==="
echo "Total slides tested: $total"
echo "✅ Clean successes: $successes"
echo "⚠️  Warning failures (PDF generated): $warning_failures"
echo "❌ Real failures (no PDF): $real_failures"
echo ""
echo "Actual success rate (including warnings): $(echo "scale=1; ($successes + $warning_failures) * 100 / $total" | bc)%"
echo "Clean success rate: $(echo "scale=1; $successes * 100 / $total" | bc)%"
