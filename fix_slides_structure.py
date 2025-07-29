#!/usr/bin/env python3
"""Fix slide structure: reduce pauses, fix pop quiz positioning, update tcolorbox usage."""

import os
import re
from pathlib import Path

def fix_slide_content(content):
    """Fix various slide content issues."""
    
    # Fix pop quiz numbering issues - this is the main problem
    # Remove the old counter definitions since they're now in the theme
    content = re.sub(r'\\newcounter\{popquiz\}', '', content)
    content = re.sub(r'\\setcounter\{popquiz\}\{\d+\}', '', content)
    
    # Fix inconsistent pop quiz frame titles
    # Pattern 1: \begin{frame}{Pop Quiz \stepcounter{popquiz}#\thepopquiz}
    content = re.sub(r'\\begin\{frame\}\{Pop Quiz \\stepcounter\{popquiz\}\\?\#\\thepopquiz\}', 
                     r'\\begin{frame}{Quick Quiz}', content)
    
    # Fix inline stepcounter issues
    # Pattern: \stepcounter{popquiz} followed by tcolorbox
    def fix_quiz_pattern(match):
        # Extract the content between tcolorbox tags
        tcolorbox_content = match.group(1)
        # Remove the stepcounter since it's now handled by the theme
        return f'\\begin{{popquizbox}}{{}}\\n{tcolorbox_content}\\n\\end{{popquizbox}}'
    
    # Replace old tcolorbox pop quiz pattern
    tcolorbox_pattern = r'\\stepcounter\{popquiz\}\s*\\begin\{tcolorbox\}\[colback=blue!5!white,colframe=blue!75!black,title=Quick Question.*?\](.*?)\\end\{tcolorbox\}'
    content = re.sub(tcolorbox_pattern, fix_quiz_pattern, content, flags=re.DOTALL)
    
    # Replace remaining tcolorbox quiz patterns
    remaining_pattern = r'\\begin\{tcolorbox\}\[colback=blue!5!white,colframe=blue!75!black,title=Quick Question.*?\](.*?)\\end\{tcolorbox\}'
    content = re.sub(remaining_pattern, r'\\begin{popquizbox}{}\n\1\n\\end{popquizbox}', content, flags=re.DOTALL)
    
    # Remove excessive consecutive \pause commands (keep max 2)
    content = re.sub(r'(\\pause\s*){3,}', r'\\pause\n\\pause\n', content)
    
    # Remove \pause immediately before or after frame endings
    content = re.sub(r'\\pause\s*\\end\{frame\}', r'\\end{frame}', content)
    content = re.sub(r'\\begin\{frame\}.*?\\pause\s*', r'\\begin{frame}', content, flags=re.DOTALL)
    
    # Remove \pause before sections
    content = re.sub(r'\\pause\s*\\section', r'\\section', content)
    
    # Reduce excessive pauses in itemize environments
    # Replace patterns like \item ... \pause \item ... \pause with cleaner structure
    def clean_itemize_pauses(match):
        itemize_content = match.group(1)
        # Keep only strategic pauses (after every 2-3 items)
        items = re.split(r'\\item\s+', itemize_content)
        if len(items) <= 1:
            return match.group(0)
        
        cleaned_items = ['\\item ' + items[1]]  # First item
        for i, item in enumerate(items[2:], 2):
            # Add pause every 3rd item or before important items (those with textbf)
            if i % 3 == 0 or '\\textbf{' in item:
                cleaned_items.append('\\pause\n\\item ' + item)
            else:
                cleaned_items.append('\\item ' + item)
        
        return f"\\begin{{itemize}}\n{''.join(cleaned_items)}\\end{{itemize}}"
    
    # Apply itemize cleanup
    content = re.sub(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', clean_itemize_pauses, content, flags=re.DOTALL)
    
    # Fix pop quiz positioning - ensure they come after topic introduction
    # Look for patterns where pop quiz appears before substantial content
    
    # Remove empty lines and excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'\n{4,}', '\n\n', content)
    
    return content

def update_slide_file(filepath):
    """Update a single slide file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_slide_content(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⏭️  No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Process all slide files."""
    slide_files = []
    
    # Find all .tex files in */slides/ directories
    for root, dirs, files in os.walk('.'):
        if 'slides' in root and 'build' not in root and '.git' not in root:
            for file in files:
                if file.endswith('.tex') and not file.endswith('.backup'):
                    slide_files.append(os.path.join(root, file))
    
    slide_files.sort()
    
    print(f"Found {len(slide_files)} slide files to process:")
    
    fixed_count = 0
    for filepath in slide_files:
        if update_slide_file(filepath):
            fixed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Fixed: {fixed_count} files")
    print(f"   Total: {len(slide_files)} files")
    
    print(f"\n🧹 Files that could be removed (but not removing automatically):")
    
    # Find backup files
    backup_files = []
    for root, dirs, files in os.walk('.'):
        if 'slides' in root:
            for file in files:
                if file.endswith('.backup') or file.endswith('.tex.backup'):
                    backup_files.append(os.path.join(root, file))
    
    print(f"   📁 Backup files ({len(backup_files)}):")
    for f in sorted(backup_files)[:10]:  # Show first 10
        print(f"      {f}")
    if len(backup_files) > 10:
        print(f"      ... and {len(backup_files) - 10} more")
    
    # Find auxiliary files
    aux_files = []
    for root, dirs, files in os.walk('.'):
        if 'slides' in root:
            for file in files:
                if file.endswith(('.aux', '.log', '.nav', '.out', '.snm', '.toc', '.fls', '.fdb_latexmk')):
                    aux_files.append(os.path.join(root, file))
    
    print(f"\n   🗑️  LaTeX auxiliary files ({len(aux_files)}):")
    print(f"      These are regenerated during compilation")
    
    # Find potentially duplicate slides
    print(f"\n   🔄 Potentially redundant slides to review:")
    
    # Check for numbered sequences that might be redundant
    svm_files = [f for f in slide_files if 'svm' in f.lower()]
    if len(svm_files) > 4:
        print(f"      SVM slides ({len(svm_files)} files):")
        for f in sorted(svm_files):
            print(f"         {f}")
        print(f"      Consider consolidating if some cover the same material")

if __name__ == "__main__":
    main()