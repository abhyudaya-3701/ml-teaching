#!/usr/bin/env python3
"""
Audit notebook coverage - find notebooks that exist but aren't linked in notebooks.qmd
"""

import re
from pathlib import Path

def get_linked_notebooks(qmd_file: Path) -> set:
    """Get all notebooks that are linked in the .qmd file."""
    with open(qmd_file, 'r') as f:
        content = f.read()
    
    # Find all notebook links
    pattern = r'notebooks/([^)]+)\.ipynb'
    matches = re.findall(pattern, content)
    
    return set(matches)

def get_existing_notebooks(notebooks_dir: Path) -> set:
    """Get all existing notebook files."""
    if not notebooks_dir.exists():
        return set()
    
    return {nb.stem for nb in notebooks_dir.glob("*.ipynb")}

def main():
    repo_root = Path.cwd()
    notebooks_dir = repo_root / 'notebooks'
    notebooks_qmd = repo_root / 'notebooks.qmd'
    
    existing = get_existing_notebooks(notebooks_dir)
    linked = get_linked_notebooks(notebooks_qmd)
    
    missing_from_qmd = existing - linked
    broken_links = linked - existing
    
    print(f"📊 NOTEBOOK COVERAGE AUDIT")
    print(f"=" * 50)
    print(f"📁 Total notebooks in directory: {len(existing)}")
    print(f"🔗 Total notebooks linked in QMD: {len(linked)}")
    print(f"✅ Coverage: {len(linked)}/{len(existing)} ({len(linked)/len(existing)*100:.1f}%)")
    
    if missing_from_qmd:
        print(f"\n⚠️  MISSING FROM ORGANIZED LIST ({len(missing_from_qmd)} notebooks):")
        for notebook in sorted(missing_from_qmd):
            print(f"  • {notebook}.ipynb")
    
    if broken_links:
        print(f"\n❌ BROKEN LINKS ({len(broken_links)} links):")
        for notebook in sorted(broken_links):
            print(f"  • {notebook}.ipynb (linked but doesn't exist)")
    
    if not missing_from_qmd and not broken_links:
        print(f"\n🎉 Perfect! All notebooks are properly linked and organized!")
    
    # Suggest where missing notebooks might fit
    if missing_from_qmd:
        print(f"\n💡 SUGGESTIONS:")
        print(f"  1. Add missing notebooks to appropriate sections in notebooks.qmd")
        print(f"  2. Or create a 'Miscellaneous' section for unorganized notebooks")
        print(f"  3. Or add them to an auto-generated 'All Notebooks' section")

if __name__ == "__main__":
    main()