#!/bin/bash
# rebuild_all.sh - Script to rebuild all PDFs and report failures

echo "=== ML Teaching Repository - Rebuild All Slides ==="
echo "Starting full rebuild at $(date)"
echo ""

# Clean everything first AND remove all PDFs to force complete rebuild
echo "🧹 Cleaning all build artifacts and existing PDFs..."
make clean
make distclean

# Count total topics and tex files for progress tracking
TOPICS=(basics maths supervised unsupervised neural-networks advanced optimization)
TOTAL_TOPICS=${#TOPICS[@]}

# Count total .tex files across all topics
TOTAL_TEX_FILES=0
for topic in "${TOPICS[@]}"; do
    if [ -d "$topic/slides" ]; then
        TEX_COUNT=$(find "$topic/slides" -name "*.tex" | wc -l)
        TOTAL_TEX_FILES=$((TOTAL_TEX_FILES + TEX_COUNT))
        echo "📄 Found $TEX_COUNT .tex files in $topic"
    fi
done

echo "📊 Building ${TOTAL_TOPICS} topics with ${TOTAL_TEX_FILES} total .tex files..."
echo ""

# Build all with progress reporting - Force rebuild by using clean + all
echo "🔨 Building all slides with progress (FORCED REBUILD)..."
BUILD_SUCCESS=true
CURRENT_TOPIC=0

for topic in "${TOPICS[@]}"; do
    CURRENT_TOPIC=$((CURRENT_TOPIC + 1))
    PROGRESS=$(( (CURRENT_TOPIC * 100) / TOTAL_TOPICS ))
    
    echo "[${CURRENT_TOPIC}/${TOTAL_TOPICS}] (${PROGRESS}%) Building ${topic}..."
    
    # Force clean rebuild: clean PDFs first, then rebuild
    if make -C "$topic" distclean >> build_results.log 2>&1 && make -C "$topic" all >> build_results.log 2>&1; then
        echo "  ✅ ${topic} completed successfully"
    else
        echo "  ❌ ${topic} failed to build"
        BUILD_SUCCESS=false
    fi
    echo ""
done

if [ "$BUILD_SUCCESS" = true ]; then
    echo "🎉 All slides built successfully!"
else
    echo "❌ Some slides failed to build"
fi

# Analyze results
echo ""
echo "=== BUILD SUMMARY ==="
echo "Completed at $(date)"
echo ""

# Count successes and show detailed breakdown
SUCCESS_COUNT=$(find . -name "*.pdf" -path "*/slides/*" | wc -l)
echo "📊 Generated PDFs: $SUCCESS_COUNT out of $TOTAL_TEX_FILES .tex files"

# Show breakdown by topic
echo ""
echo "📊 BREAKDOWN BY TOPIC:"
for topic in "${TOPICS[@]}"; do
    if [ -d "$topic/slides" ]; then
        TEX_COUNT=$(find "$topic/slides" -name "*.tex" | wc -l)
        PDF_COUNT=$(find "$topic/slides" -name "*.pdf" | wc -l)
        if [ "$PDF_COUNT" -eq "$TEX_COUNT" ]; then
            echo "  ✅ $topic: $PDF_COUNT/$TEX_COUNT PDFs generated"
        else
            echo "  ❌ $topic: $PDF_COUNT/$TEX_COUNT PDFs generated"
        fi
    fi
done

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