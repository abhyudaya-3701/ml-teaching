#!/usr/bin/env python3
"""
Simple script to automatically update notebook links in quarto files.
Scans the notebooks directory and updates links in .qmd files accordingly.
"""

import os
from pathlib import Path
import re

def get_available_notebooks(notebooks_dir: Path) -> set:
    """Get all available notebook files (.ipynb) in the notebooks directory."""
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return set()
    
    notebooks = set()
    for nb_file in notebooks_dir.glob("*.ipynb"):
        # Remove .ipynb extension to get base name
        notebooks.add(nb_file.stem)
    
    print(f"📁 Found {len(notebooks)} notebooks in {notebooks_dir}")
    return notebooks

def update_qmd_file(qmd_file: Path, available_notebooks: set) -> dict:
    """Update notebook links in a single .qmd file."""
    
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    stats = {'fixed': 0, 'missing': 0, 'total_links': 0}
    
    # Find all notebook links: [text](notebooks/name.extension)
    pattern = r'\[([^\]]+)\]\(notebooks/([^)]+)\.(html|ipynb)\)'
    
    def replace_link(match):
        text = match.group(1)
        notebook_name = match.group(2)
        current_ext = match.group(3)
        
        stats['total_links'] += 1
        
        if notebook_name in available_notebooks:
            if current_ext == 'html':
                stats['fixed'] += 1
                print(f"  ✅ Fixed: {notebook_name}.html → {notebook_name}.ipynb")
            return f'[{text}](notebooks/{notebook_name}.ipynb)'
        else:
            stats['missing'] += 1
            print(f"  ⚠️  Missing notebook: {notebook_name}")
            # Keep the original link but mark as potentially broken
            return f'[{text}](notebooks/{notebook_name}.{current_ext})'
    
    content = re.sub(pattern, replace_link, content)
    
    # Only write if changes were made
    if content != original_content:
        with open(qmd_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📝 Updated {qmd_file.name}")
    else:
        print(f"ℹ️  No changes needed in {qmd_file.name}")
    
    return stats

def main():
    repo_root = Path.cwd()
    notebooks_dir = repo_root / 'notebooks'
    
    print("🔄 Updating notebook links based on available files...")
    
    # Get available notebooks
    available_notebooks = get_available_notebooks(notebooks_dir)
    if not available_notebooks:
        return
    
    # Process all .qmd files
    qmd_files = list(repo_root.glob("*.qmd"))
    total_stats = {'fixed': 0, 'missing': 0, 'total_links': 0}
    
    for qmd_file in qmd_files:
        print(f"\n🔍 Processing {qmd_file.name}...")
        stats = update_qmd_file(qmd_file, available_notebooks)
        
        for key, value in stats.items():
            total_stats[key] += value
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"  📁 Processed {len(qmd_files)} .qmd files")
    print(f"  🔗 Found {total_stats['total_links']} notebook links")
    print(f"  ✅ Fixed {total_stats['fixed']} links (.html → .ipynb)")
    print(f"  ⚠️  {total_stats['missing']} missing notebooks")
    
    if total_stats['missing'] > 0:
        print(f"\n💡 To fix missing notebooks:")
        print(f"  1. Add the missing notebooks to {notebooks_dir}")
        print(f"  2. Or remove the broken links from .qmd files")
        print(f"  3. Or update the link text if notebook was renamed")

if __name__ == "__main__":
    main()