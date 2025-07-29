#!/usr/bin/env python3
"""Fix structural issues in accuracy-convention.tex file"""

import re

def fix_latex_file(content):
    """Fix common LaTeX structural issues"""
    
    # Fix broken math environments
    content = re.sub(r'\\begin\{frame\}\\text\{([^}]+)\}', r'\\begin{frame}{\\1}', content)
    
    # Fix missing frame titles
    content = re.sub(r'\\begin\{frame\}([^{])', r'\\begin{frame}{Untitled Frame}\n\\1', content)
    
    # Fix incomplete align environments
    content = re.sub(r'\\begin\{frame\}([^\\]*?)&=([^\\]*?)\\end\{align', r'\\begin{frame}{Math}\n\\begin{align*}\n\\1 &= \\2\n\\end{align', content)
    
    # Fix lonely $$ 
    content = re.sub(r'^\\begin\{frame\}\$\$$', r'\\begin{frame}{Math Example}', content, flags=re.MULTILINE)
    
    # Remove stray \end{tcolorbox} without corresponding \begin{tcolorbox}
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for \end{tcolorbox} without matching \begin{tcolorbox}
        if '\\end{tcolorbox}' in line:
            # Look backward for matching \begin{tcolorbox} 
            found_begin = False
            for j in range(i-1, max(0, i-20), -1):
                if '\\begin{tcolorbox}' in lines[j] or '\\begin{popquizbox}' in lines[j]:
                    found_begin = True
                    break
            
            if not found_begin:
                # Remove this stray \end{tcolorbox}
                line = line.replace('\\end{tcolorbox}', '')
                if not line.strip():
                    i += 1
                    continue
        
        fixed_lines.append(lines[i])
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix quote marks - convert straight quotes to LaTeX quotes
    content = re.sub(r'"([^"]*)"', r"``\\1''", content)
    
    # Reduce excessive pauses - limit to max 2 consecutive pauses
    content = re.sub(r'(\\pause\s*){3,}', r'\\pause\n\\pause\n', content)
    
    return content

def main():
    input_file = '/Users/nipun/git/ml-teaching/basics/slides/accuracy-convention.tex'
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    fixed_content = fix_latex_file(content)
    
    with open(input_file, 'w') as f:
        f.write(fixed_content)
    
    print("Fixed accuracy-convention.tex file")

if __name__ == '__main__':
    main()