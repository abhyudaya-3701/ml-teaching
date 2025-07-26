#!/usr/bin/env python3
"""Fix LaTeX quotes in .tex files throughout the repository."""

import os
import re
import glob

def fix_latex_quotes(content):
    """Fix straight quotes to proper LaTeX quotes."""
    # Fix quotes around words/phrases but not in code blocks or math
    # Pattern: "word" -> ``word''
    # But avoid fixing within \verb, \lstinline, math environments, etc.
    
    # First, protect code blocks and math environments
    protected_sections = []
    
    # Protect verbatim environments
    verbatim_pattern = r'\\begin\{(verbatim|lstlisting|Verbatim)\}.*?\\end\{\1\}'
    content = re.sub(verbatim_pattern, lambda m: f"__PROTECTED_{len(protected_sections)}__" + (protected_sections.append(m.group(0)) or ""), content, flags=re.DOTALL)
    
    # Protect inline code
    inline_code_pattern = r'\\verb\|[^|]*\||\\lstinline\{[^}]*\}|\\texttt\{[^}]*\}'
    content = re.sub(inline_code_pattern, lambda m: f"__PROTECTED_{len(protected_sections)}__" + (protected_sections.append(m.group(0)) or ""), content)
    
    # Protect math environments
    math_pattern = r'\$[^$]*\$|\\\[[^\]]*\\\]|\\begin\{(equation|align|gather|multline)\*?\}.*?\\end\{\1\*?\}'
    content = re.sub(math_pattern, lambda m: f"__PROTECTED_{len(protected_sections)}__" + (protected_sections.append(m.group(0)) or ""), content, flags=re.DOTALL)
    
    # Now fix quotes that are not in protected sections
    # Pattern: "text with spaces and words" -> ``text with spaces and words''
    quote_pattern = r'"([^"]+)"'
    content = re.sub(quote_pattern, r"``\1''", content)
    
    # Restore protected sections
    for i, section in enumerate(protected_sections):
        content = content.replace(f"__PROTECTED_{i}__", section)
    
    return content

def main():
    """Process all .tex files in the repository."""
    tex_files = []
    
    # Find all .tex files
    for root, dirs, files in os.walk('.'):
        # Skip build directories
        if 'build' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    
    fixed_files = []
    
    for tex_file in tex_files:
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            fixed_content = fix_latex_quotes(original_content)
            
            if fixed_content != original_content:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                fixed_files.append(tex_file)
                print(f"Fixed quotes in: {tex_file}")
        
        except Exception as e:
            print(f"Error processing {tex_file}: {e}")
    
    print(f"\nFixed quotes in {len(fixed_files)} files:")
    for f in fixed_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()