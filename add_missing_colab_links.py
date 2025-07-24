#!/usr/bin/env python3
"""Add Colab links to notebooks that have metadata but are missing Colab links."""

import json
import shutil
from pathlib import Path

def has_quarto_metadata(notebook_data):
    """Check if notebook has Quarto metadata in first raw cell."""
    if not notebook_data.get('cells'):
        return False
    first_cell = notebook_data['cells'][0]
    if first_cell.get('cell_type') != 'raw':
        return False
    source = ''.join(first_cell.get('source', []))
    return source.strip().startswith('---') and 'title:' in source

def has_colab_link(notebook_data):
    """Check if notebook has Colab link in second cell."""
    if len(notebook_data.get('cells', [])) < 2:
        return False
    second_cell = notebook_data['cells'][1]
    if second_cell.get('cell_type') != 'markdown':
        return False
    source = ''.join(second_cell.get('source', []))
    return 'colab.research.google.com' in source and 'Open In Colab' in source

def create_colab_cell(notebook_path):
    """Create a markdown cell with Colab link."""
    github_path = str(notebook_path).replace('/Users/nipun/git/ml-teaching/', '')
    colab_url = f"https://colab.research.google.com/github/nipunbatra/ml-teaching/blob/master/{github_path}"
    colab_content = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [colab_content + "\n"]
    }

def add_colab_link(notebook_path, dry_run=False):
    """Add Colab link to notebook that has metadata but missing link."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Check if has metadata but missing Colab link
    if not has_quarto_metadata(notebook_data):
        return False, "No Quarto metadata"
    
    if has_colab_link(notebook_data):
        return False, "Already has Colab link"
    
    print(f"Adding Colab link to {notebook_path.name}")
    
    if dry_run:
        print("  [DRY RUN - no changes made]")
        return True, "Would add Colab link"
    
    # Backup original
    backup_path = notebook_path.with_suffix('.ipynb.backup-colab')
    shutil.copy2(notebook_path, backup_path)
    print(f"  Backup created: {backup_path.name}")
    
    # Insert Colab cell as second cell (after metadata)
    colab_cell = create_colab_cell(notebook_path)
    notebook_data['cells'].insert(1, colab_cell)
    
    # Save modified notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Added Colab link")
    return True, "Added Colab link"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Add Colab links to notebooks missing them")
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    args = parser.parse_args()
    
    notebooks = list(Path('notebooks').glob('**/*.ipynb'))
    print(f"Found {len(notebooks)} notebooks to check:")
    
    modified_count = 0
    
    for notebook in sorted(notebooks):
        try:
            modified, reason = add_colab_link(notebook, dry_run=args.dry_run)
            if modified:
                modified_count += 1
            elif reason != "Already has Colab link":
                print(f"Skipped {notebook.name}: {reason}")
            print()
        except Exception as e:
            print(f"  ✗ Error processing {notebook.name}: {e}")
            print()
    
    print(f"Summary: {modified_count} notebooks {'would be ' if args.dry_run else ''}modified")

if __name__ == '__main__':
    main()