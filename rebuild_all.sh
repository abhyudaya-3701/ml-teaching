#!/bin/bash
# rebuild_all.sh - Script to rebuild all PDFs and report failures with detailed timing

SCRIPT_START_TIME=$(date +%s)
SCRIPT_START_DATE=$(date)

echo "=== ML Teaching Repository - Rebuild All Slides ==="
echo "🕐 Starting full rebuild at $SCRIPT_START_DATE"
echo ""

# Initialize timing arrays
declare -A TOPIC_START_TIMES
declare -A TOPIC_END_TIMES
declare -A TOPIC_DURATIONS

# Clean everything first AND remove all PDFs to force complete rebuild
echo "🧹 Cleaning all build artifacts and existing PDFs..."
CLEAN_START=$(date +%s)
make clean
make distclean
CLEAN_END=$(date +%s)
CLEAN_DURATION=$((CLEAN_END - CLEAN_START))
echo "   ⏱️  Cleaning completed in ${CLEAN_DURATION}s"

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
    
    # Start timing for this topic
    TOPIC_START_TIMES[$topic]=$(date +%s)
    TOPIC_START_DATE=$(date)
    echo "    🕐 Started ${topic} at $(date +'%H:%M:%S')"
    
    # Count .tex files in this topic
    if [ -d "$topic/slides" ]; then
        TOPIC_TEX_COUNT=$(find "$topic/slides" -name "*.tex" | wc -l)
        echo "    📄 Processing $TOPIC_TEX_COUNT .tex files..."
    fi
    
    # Build topic with detailed logging
    echo "    🔨 Building ${topic}..."
    if make -C "$topic" all >> build_results.log 2>&1; then
        TOPIC_END_TIMES[$topic]=$(date +%s)
        TOPIC_DURATIONS[$topic]=$((TOPIC_END_TIMES[$topic] - TOPIC_START_TIMES[$topic]))
        MINUTES=$((TOPIC_DURATIONS[$topic] / 60))
        SECONDS=$((TOPIC_DURATIONS[$topic] % 60))
        
        # Count generated PDFs
        TOPIC_PDF_COUNT=$(find "$topic/slides" -name "*.pdf" | wc -l)
        
        echo "  ✅ ${topic} completed successfully in ${MINUTES}m ${SECONDS}s"
        echo "     📊 Generated ${TOPIC_PDF_COUNT}/${TOPIC_TEX_COUNT} PDFs"
    else
        TOPIC_END_TIMES[$topic]=$(date +%s)
        TOPIC_DURATIONS[$topic]=$((TOPIC_END_TIMES[$topic] - TOPIC_START_TIMES[$topic]))
        MINUTES=$((TOPIC_DURATIONS[$topic] / 60))
        SECONDS=$((TOPIC_DURATIONS[$topic] % 60))
        
        echo "  ❌ ${topic} build failed after ${MINUTES}m ${SECONDS}s"
        BUILD_SUCCESS=false
    fi
    echo ""
done

if [ "$BUILD_SUCCESS" = true ]; then
    echo "🎉 All slides built successfully!"
else
    echo "❌ Some slides failed to build"
fi

# Calculate total script time
SCRIPT_END_TIME=$(date +%s)
TOTAL_SCRIPT_DURATION=$((SCRIPT_END_TIME - SCRIPT_START_TIME))
TOTAL_MINUTES=$((TOTAL_SCRIPT_DURATION / 60))
TOTAL_SECONDS=$((TOTAL_SCRIPT_DURATION % 60))

# Analyze results
echo ""
echo "=== BUILD SUMMARY ==="
echo "🕐 Started at: $SCRIPT_START_DATE"
echo "🕐 Completed at: $(date)"
echo "⏱️  Total time: ${TOTAL_MINUTES}m ${TOTAL_SECONDS}s"
echo ""

# Timing breakdown by topic
echo "⏱️  TIMING BREAKDOWN:"
for topic in "${TOPICS[@]}"; do
    if [ "${TOPIC_DURATIONS[$topic]}" ]; then
        MINUTES=$((TOPIC_DURATIONS[$topic] / 60))
        SECONDS=$((TOPIC_DURATIONS[$topic] % 60))
        echo "   ${topic}: ${MINUTES}m ${SECONDS}s"
    fi
done
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