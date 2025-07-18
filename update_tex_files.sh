#!/bin/bash

# Script to update all .tex files to use unified custom.sty

echo "Starting LaTeX file updates..."

# Find all .tex files
find . -name "*.tex" -type f | while read -r file; do
    echo "Processing: $file"
    
    # Create backup
    cp "$file" "$file.backup"
    
    # Calculate relative path to shared/styles/custom.sty
    dir=$(dirname "$file")
    
    # Count directory depth to determine relative path
    depth=$(echo "$dir" | tr -cd '/' | wc -c)
    
    # Generate relative path
    if [ "$depth" -eq 1 ]; then
        # Top level directories (basics/, maths/, etc.)
        relative_path="../shared/styles/custom"
    elif [ "$depth" -eq 2 ]; then
        # Second level (basics/slides/, maths/slides/, etc.)
        relative_path="../../shared/styles/custom"
    elif [ "$depth" -eq 3 ]; then
        # Third level (maths/slides/kkt-conditions/, etc.)
        relative_path="../../../shared/styles/custom"
    else
        # Default fallback
        relative_path="../../shared/styles/custom"
    fi
    
    # Create temporary file for processing
    temp_file=$(mktemp)
    
    # Process the file
    {
        # Keep document class
        grep "^\\\\documentclass" "$file" | head -1
        
        # Add unified custom package
        echo "\\usepackage{$relative_path}"
        echo ""
        
        # Skip old package imports and common definitions, keep everything else
        awk '
        BEGIN { 
            in_preamble = 1 
            skip_next = 0
        }
        
        # Document class line - already handled above
        /^\\documentclass/ { next }
        
        # Start of document - end preamble processing
        /^\\begin{document}/ { in_preamble = 0 }
        
        # Skip common packages that are now in custom.sty
        in_preamble && /^\\usepackage.*{graphicx}/ { next }
        in_preamble && /^\\usepackage.*{amsmath}/ { next }
        in_preamble && /^\\usepackage.*{amssymb}/ { next }
        in_preamble && /^\\usepackage.*{tcolorbox}/ { next }
        in_preamble && /^\\usepackage.*{xcolor}/ { next }
        in_preamble && /^\\usepackage.*{tikz}/ { next }
        in_preamble && /^\\usepackage.*{pgfplots}/ { next }
        in_preamble && /^\\usepackage.*{bm}/ { next }
        in_preamble && /^\\usepackage.*{hyperref}/ { next }
        in_preamble && /^\\usepackage.*{booktabs}/ { next }
        in_preamble && /^\\usepackage.*{multirow}/ { next }
        in_preamble && /^\\usepackage.*{subcaption}/ { next }
        in_preamble && /^\\usepackage.*{makecell}/ { next }
        in_preamble && /^\\usepackage.*{adjustbox}/ { next }
        in_preamble && /^\\usepackage.*{caption}/ { next }
        in_preamble && /^\\usepackage.*{color}/ { next }
        in_preamble && /^\\usepackage.*{colortbl}/ { next }
        in_preamble && /^\\usepackage.*{pdfpages}/ { next }
        in_preamble && /^\\usepackage.*{forloop}/ { next }
        in_preamble && /^\\usepackage.*{siunitx}/ { next }
        in_preamble && /^\\usepackage.*{forest}/ { next }
        in_preamble && /^\\usepackage.*{calculator}/ { next }
        in_preamble && /^\\usepackage.*{mathtools}/ { next }
        in_preamble && /^\\usepackage.*{url}/ { next }
        
        # Skip old style file imports
        in_preamble && /^\\usepackage.*{notation}/ { next }
        in_preamble && /^\\usepackage.*{mycommonstyle}/ { next }
        in_preamble && /^\\usepackage.*{mycustomstyle}/ { next }
        in_preamble && /^\\usepackage.*{\.\.\/\.\.\/shared\/notation\/notation}/ { next }
        in_preamble && /^\\usepackage.*{\.\.\/\.\.\/shared\/styles\/mycommonstyle}/ { next }
        
        # Skip theme declarations (now in custom.sty)
        in_preamble && /^\\usetheme{metropolis}/ { next }
        
        # Skip common command redefinitions (now in custom.sty)
        in_preamble && /^\\newcommand{\\data}/ { next }
        in_preamble && /^\\newcommand\\Item/ { next }
        in_preamble && /^\\DeclareMathOperator.*{\\argmin}/ { next }
        in_preamble && /^\\DeclareMathOperator.*{\\argmax}/ { next }
        in_preamble && /^\\definecolor{myblue}/ { next }
        in_preamble && /^\\hypersetup/ { skip_next = 5; next }
        
        # Skip hypersetup block
        skip_next > 0 { skip_next--; next }
        
        # Skip TikZ library imports (now in custom.sty)
        in_preamble && /^\\usetikzlibrary/ { next }
        
        # Skip TikZ styles (now in custom.sty)
        in_preamble && /^\\tikzstyle/ { next }
        
        # Skip pgfplots settings (now in custom.sty)
        in_preamble && /^\\pgfplotsset/ { next }
        
        # Skip common spacing settings
        in_preamble && /^\\setlength{\\abovedisplayskip}/ { next }
        in_preamble && /^\\setlength{\\belowdisplayskip}/ { next }
        
        # Keep everything else
        { print }
        ' "$file"
    } > "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$file"
    
    echo "Updated: $file"
done

echo "LaTeX file updates complete!"
echo "Original files backed up with .backup extension"