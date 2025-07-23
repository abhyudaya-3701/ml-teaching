#!/usr/bin/env python3
"""
Fix broken notebook links by converting .html to .ipynb extensions.
"""

import re
from pathlib import Path

def fix_notebook_links_in_file(file_path: Path) -> int:
    """Fix notebook links in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match notebook links with .html extension
        pattern = r'\[([^\]]+)\]\(notebooks/([^)]+)\.html\)'
        
        # Replace .html with .ipynb
        def replace_link(match):
            text = match.group(1)
            notebook_name = match.group(2)
            return f'[{text}](notebooks/{notebook_name}.ipynb)'
        
        content = re.sub(pattern, replace_link, content)
        
        # Count how many replacements were made
        changes = content.count('.ipynb') - original_content.count('.ipynb')
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {changes} links in {file_path.name}")
        else:
            print(f"ℹ️  No notebook links to fix in {file_path.name}")
            
        return changes
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def verify_notebooks_exist(repo_root: Path) -> dict:
    """Verify which notebooks actually exist."""
    notebooks_dir = repo_root / 'notebooks'
    
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return {}
    
    # Get all .ipynb files
    ipynb_files = list(notebooks_dir.glob('*.ipynb'))
    notebook_names = {nb.stem for nb in ipynb_files}
    
    print(f"📁 Found {len(ipynb_files)} notebooks in {notebooks_dir}")
    
    return {
        'existing_notebooks': notebook_names,
        'total_count': len(ipynb_files)
    }

def main():
    repo_root = Path.cwd()
    
    print("🔧 Fixing notebook links in .qmd files...")
    
    # First, verify what notebooks exist
    notebook_info = verify_notebooks_exist(repo_root)
    
    if not notebook_info:
        print("❌ Cannot proceed without notebook directory")
        return
    
    # Find all .qmd files
    qmd_files = list(repo_root.glob("*.qmd"))
    
    total_fixes = 0
    for qmd_file in qmd_files:
        fixes = fix_notebook_links_in_file(qmd_file)
        total_fixes += fixes
    
    print(f"\n🎉 Fixed {total_fixes} notebook links across {len(qmd_files)} files!")
    
    # Verify the fixes by checking again
    print("\n🔍 Verifying fixes...")
    from check_links import LinkChecker
    
    checker = LinkChecker(str(repo_root))
    summary = checker.check_all_links()
    
    html_broken = sum(1 for link in checker.broken_links if link['type'] == 'missing_html')
    
    if html_broken == 0:
        print("✅ All notebook links are now fixed!")
    else:
        print(f"⚠️  Still {html_broken} broken HTML links remain")
        
    print(f"📊 Final stats: {summary['broken_links']} total broken links out of {summary['total_links']}")

if __name__ == "__main__":
    main()