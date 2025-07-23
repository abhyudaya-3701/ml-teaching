#!/usr/bin/env python3
"""
Smart notebook link fixer that handles filename variations and adds missing notebooks.
"""

import re
from pathlib import Path
from difflib import get_close_matches

def normalize_name(name: str) -> str:
    """Normalize notebook name for comparison."""
    return name.lower().replace('_', '-').replace(' ', '-')

def get_existing_notebooks(notebooks_dir: Path) -> dict:
    """Get all existing notebooks with their actual filenames."""
    if not notebooks_dir.exists():
        return {}
    
    notebooks = {}
    for nb_file in notebooks_dir.glob("*.ipynb"):
        normalized = normalize_name(nb_file.stem)
        notebooks[normalized] = nb_file.stem
    
    return notebooks

def find_best_match(target: str, available: dict) -> str:
    """Find the best matching notebook filename."""
    normalized_target = normalize_name(target)
    
    # Exact match
    if normalized_target in available:
        return available[normalized_target]
    
    # Close match using difflib
    normalized_names = list(available.keys())
    matches = get_close_matches(normalized_target, normalized_names, n=1, cutoff=0.8)
    
    if matches:
        return available[matches[0]]
    
    return None

def fix_notebook_links(qmd_file: Path, available_notebooks: dict) -> dict:
    """Fix notebook links with smart matching."""
    
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    stats = {'fixed': 0, 'missing': 0, 'total_links': 0}
    
    # Find all notebook links
    pattern = r'\[([^\]]+)\]\(notebooks/([^)]+)\.ipynb\)'
    
    def replace_link(match):
        text = match.group(1)
        notebook_name = match.group(2)
        
        stats['total_links'] += 1
        
        # Try to find the best match
        best_match = find_best_match(notebook_name, available_notebooks)
        
        if best_match:
            if best_match != notebook_name:
                stats['fixed'] += 1
                print(f"  ✅ Fixed: {notebook_name} → {best_match}")
            return f'[{text}](notebooks/{best_match}.ipynb)'
        else:
            stats['missing'] += 1
            print(f"  ❌ No match found: {notebook_name}")
            return match.group(0)  # Keep original
    
    content = re.sub(pattern, replace_link, content)
    
    # Write back if changes were made
    if content != original_content:
        with open(qmd_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📝 Updated {qmd_file.name}")
    
    return stats

def add_missing_notebooks_section(qmd_file: Path, available_notebooks: dict) -> int:
    """Add a section for notebooks not yet organized."""
    
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get currently linked notebooks
    linked_pattern = r'notebooks/([^)]+)\.ipynb'
    linked_notebooks = set(re.findall(linked_pattern, content))
    
    # Find unlinked notebooks
    all_notebooks = set(available_notebooks.values())
    unlinked = all_notebooks - linked_notebooks
    
    if not unlinked:
        print("✅ All notebooks are already linked!")
        return 0
    
    # Create section for unlinked notebooks
    unlinked_section = f"""
### Other Notebooks

The following notebooks are available but not yet categorized:

"""
    
    for notebook in sorted(unlinked):
        # Create a nice display name from filename
        display_name = notebook.replace('-', ' ').replace('_', ' ').title()
        unlinked_section += f"- [{display_name}](notebooks/{notebook}.ipynb)\n"
    
    # Add before the "Getting Started" section
    if "## Getting Started" in content:
        content = content.replace("## Getting Started", unlinked_section + "\n---\n\n## Getting Started")
    else:
        # Add at the end before any existing footer
        if "---" in content:
            parts = content.rsplit("---", 1)
            content = parts[0] + unlinked_section + "\n---" + parts[1]
        else:
            content += unlinked_section
    
    with open(qmd_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📝 Added 'Other Notebooks' section with {len(unlinked)} notebooks")
    return len(unlinked)

def main():
    repo_root = Path.cwd()
    notebooks_dir = repo_root / 'notebooks'
    notebooks_qmd = repo_root / 'notebooks.qmd'
    
    print("🔧 Smart notebook link fixing...")
    
    available_notebooks = get_existing_notebooks(notebooks_dir)
    print(f"📁 Found {len(available_notebooks)} notebooks")
    
    # Fix existing links
    print(f"\n🔍 Fixing links in {notebooks_qmd.name}...")
    stats = fix_notebook_links(notebooks_qmd, available_notebooks)
    
    # Add missing notebooks
    print(f"\n📋 Adding unlinked notebooks...")
    added = add_missing_notebooks_section(notebooks_qmd, available_notebooks)
    
    print(f"\n📊 SUMMARY:")
    print(f"  🔗 Total notebook links: {stats['total_links']}")
    print(f"  ✅ Fixed mismatched names: {stats['fixed']}")
    print(f"  ❌ Still missing: {stats['missing']}")
    print(f"  ➕ Added to 'Other' section: {added}")
    
    if stats['missing'] == 0 and added >= 0:
        print(f"\n🎉 All notebooks are now properly linked!")

if __name__ == "__main__":
    main()