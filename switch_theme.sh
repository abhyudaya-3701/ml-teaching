#!/bin/bash
# Theme Switcher for ML Teaching Slides 🎨
# Usage: ./switch_theme.sh [default|ocean|sunset|forest|cosmic]

CUSTOM_FILE="shared/styles/custom.sty"

if [ ! -f "$CUSTOM_FILE" ]; then
    echo "❌ Error: $CUSTOM_FILE not found!"
    exit 1
fi

# Function to comment out all themes
comment_all_themes() {
    sed -i '' 's/^\\usetheme{metropolis}/% \\usetheme{metropolis}/' "$CUSTOM_FILE"
    sed -i '' 's/^\\definecolor{m/% \\definecolor{m/' "$CUSTOM_FILE"
    sed -i '' 's/^\\setbeamercolor{/% \\setbeamercolor{/' "$CUSTOM_FILE"
}

case "$1" in
    "default"|"")
        echo "🎯 Switching to Default Metropolis theme..."
        comment_all_themes
        # Uncomment only the default theme
        sed -i '' 's/% Default Metropolis (current)/% Default Metropolis (current)/' "$CUSTOM_FILE"
        sed -i '' 's/% \\usetheme{metropolis}/\\usetheme{metropolis}/' "$CUSTOM_FILE" | head -1
        ;;
    
    "ocean")
        echo "🌊 Switching to Deep Ocean theme..."
        comment_all_themes
        # Uncomment Deep Ocean theme
        sed -i '' '/% Theme Variant 1: "Deep Ocean"/,/% Theme Variant 2:/ s/% \\usetheme{metropolis}/\\usetheme{metropolis}/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 1: "Deep Ocean"/,/% Theme Variant 2:/ s/% \\definecolor{/\\definecolor{/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 1: "Deep Ocean"/,/% Theme Variant 2:/ s/% \\setbeamercolor{/\\setbeamercolor{/' "$CUSTOM_FILE"
        ;;
        
    "sunset")
        echo "🌅 Switching to Sunset Academia theme..."
        comment_all_themes
        # Uncomment Sunset theme
        sed -i '' '/% Theme Variant 2: "Sunset Academia"/,/% Theme Variant 3:/ s/% \\usetheme{metropolis}/\\usetheme{metropolis}/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 2: "Sunset Academia"/,/% Theme Variant 3:/ s/% \\definecolor{/\\definecolor{/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 2: "Sunset Academia"/,/% Theme Variant 3:/ s/% \\setbeamercolor{/\\setbeamercolor{/' "$CUSTOM_FILE"
        ;;
        
    "forest")
        echo "🌲 Switching to Forest Night theme..."
        comment_all_themes
        # Uncomment Forest theme
        sed -i '' '/% Theme Variant 3: "Forest Night"/,/% Theme Variant 4:/ s/% \\usetheme{metropolis}/\\usetheme{metropolis}/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 3: "Forest Night"/,/% Theme Variant 4:/ s/% \\definecolor{/\\definecolor{/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 3: "Forest Night"/,/% Theme Variant 4:/ s/% \\setbeamercolor{/\\setbeamercolor{/' "$CUSTOM_FILE"
        ;;
        
    "cosmic")
        echo "🌌 Switching to Cosmic Purple theme..."
        comment_all_themes
        # Uncomment Cosmic theme
        sed -i '' '/% Theme Variant 4: "Cosmic Purple"/,/% Basic spacing control/ s/% \\usetheme{metropolis}/\\usetheme{metropolis}/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 4: "Cosmic Purple"/,/% Basic spacing control/ s/% \\definecolor{/\\definecolor{/' "$CUSTOM_FILE"
        sed -i '' '/% Theme Variant 4: "Cosmic Purple"/,/% Basic spacing control/ s/% \\setbeamercolor{/\\setbeamercolor{/' "$CUSTOM_FILE"
        ;;
        
    *)
        echo "🎨 ML Teaching Slides Theme Switcher"
        echo ""
        echo "Usage: ./switch_theme.sh [theme]"
        echo ""
        echo "Available themes:"
        echo "  default  - Standard Metropolis (clean & minimal)"
        echo "  ocean    - Deep Ocean (dark blue with cyan accents)"
        echo "  sunset   - Sunset Academia (warm orange/pink on cream)"
        echo "  forest   - Forest Night (deep green with mint accents)"
        echo "  cosmic   - Cosmic Purple (vibrant purple with gold)"
        echo ""
        echo "Examples:"
        echo "  ./switch_theme.sh ocean"
        echo "  ./switch_theme.sh sunset"
        echo ""
        exit 1
        ;;
esac

echo "✅ Theme switched! Recompile your slides to see the changes."
echo "💡 Tip: Try running 'pdflatex your_slide_file.tex' from the slides directory"