#!/bin/bash
# rebuild_all.sh - Script to rebuild all PDFs and report failures

echo "=== ML Teaching Repository - Rebuild All Slides ==="
echo "Starting full rebuild at $(date)"
echo ""

# Clean everything first
echo "🧹 Cleaning all build artifacts..."
make clean

# Build all and capture results
echo "🔨 Building all slides..."
if make all > build_results.log 2>&1; then
    echo "✅ All slides built successfully!"
    BUILD_SUCCESS=true
else
    echo "❌ Some slides failed to build"
    BUILD_SUCCESS=false
fi

# Analyze results
echo ""
echo "=== BUILD SUMMARY ==="
echo ""

# Count successes
SUCCESS_COUNT=$(find . -name "*.pdf" -path "*/slides/*" | wc -l)
echo "📊 Generated PDFs: $SUCCESS_COUNT"

# List successful builds
echo ""
echo "✅ SUCCESSFUL BUILDS:"
find . -name "*.pdf" -path "*/slides/*" | sort | while read pdf; do
    echo "  ✓ $pdf"
done

# Find failures by looking for error messages in the log
echo ""
echo "❌ FAILED BUILDS:"
if grep -q "make.*Error" build_results.log; then
    grep "make.*Error" build_results.log | while read error; do
        echo "  ✗ $error"
    done
else
    echo "  (None - all builds succeeded!)"
fi

# Show last part of log if there were failures
if [ "$BUILD_SUCCESS" = false ]; then
    echo ""
    echo "🔍 LAST 20 LINES OF BUILD LOG:"
    echo "----------------------------------------"
    tail -20 build_results.log
    echo "----------------------------------------"
    echo ""
    echo "💡 Full build log saved in: build_results.log"
fi

echo ""
echo "=== REBUILD COMPLETE ==="
echo "Finished at $(date)"

# Exit with same code as make
if [ "$BUILD_SUCCESS" = true ]; then
    exit 0
else
    exit 1
fi