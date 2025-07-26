#!/usr/bin/env python3
"""
Script to add Quarto metadata and Colab links to Jupyter notebooks.

Usage:
    python add_notebook_metadata.py <notebook_path> --title "Title" --description "Description" --tags "tag1,tag2" [--dry-run]

Features:
- Checks if notebook already has raw metadata cell at the beginning
- Adds Quarto YAML metadata in raw cell if missing
- Adds Colab link in the second cell
- Backs up original notebook before making changes
- Dry-run mode to preview changes without modifying files
"""

import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import re

def has_quarto_metadata(notebook_data):
    """Check if notebook already has Quarto metadata in first cell."""
    if not notebook_data.get('cells'):
        return False
    
    first_cell = notebook_data['cells'][0]
    if first_cell.get('cell_type') != 'raw':
        return False
    
    source = ''.join(first_cell.get('source', []))
    return source.strip().startswith('---') and 'title:' in source

def create_metadata_cell(title, description, tags, author="Nipun Batra"):
    """Create a raw cell with Quarto metadata."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Convert tags string to YAML array format
    if isinstance(tags, str):
        tag_list = [tag.strip() for tag in tags.split(',')]
    else:
        tag_list = tags
    
    tags_yaml = '[' + ', '.join(f'"{tag}"' for tag in tag_list) + ']'
    
    metadata_content = f"""---
author: {author}
date: {today}
description: {description}
tags: {tags_yaml}
title: '{title}'
---"""
    
    return {
        "cell_type": "raw",
        "metadata": {},
        "source": [metadata_content + "\n"]
    }

def create_colab_cell(notebook_path):
    """Create a markdown cell with Colab link."""
    # Convert absolute path to relative GitHub path
    github_path = str(notebook_path).replace('/Users/nipun/git/ml-teaching/', '')
    colab_url = f"https://colab.research.google.com/github/nipunbatra/ml-teaching/blob/master/{github_path}"
    
    colab_content = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [colab_content + "\n"]
    }

def infer_metadata_from_filename(notebook_path):
    """Infer basic metadata from notebook filename."""
    stem = notebook_path.stem
    
    # Clean up filename for title
    title = stem.replace('-', ' ').replace('_', ' ').title()
    
    # Infer tags based on filename patterns
    tags = []
    
    # ML concept tags
    if any(word in stem.lower() for word in ['linear', 'regression']):
        tags.extend(['linear-regression', 'supervised-learning'])
    if any(word in stem.lower() for word in ['logistic', 'classification']):
        tags.extend(['logistic-regression', 'classification'])
    if 'gradient' in stem.lower():
        tags.append('optimization')
    if any(word in stem.lower() for word in ['cnn', 'conv', 'neural']):
        tags.extend(['deep-learning', 'neural-networks'])
    if 'svm' in stem.lower():
        tags.extend(['svm', 'supervised-learning'])
    if any(word in stem.lower() for word in ['decision', 'tree']):
        tags.extend(['decision-trees', 'supervised-learning'])
    if any(word in stem.lower() for word in ['ensemble', 'random', 'forest']):
        tags.extend(['ensemble-methods', 'supervised-learning'])
    if any(word in stem.lower() for word in ['bias', 'variance']):
        tags.extend(['model-evaluation', 'bias-variance'])
    if 'pca' in stem.lower():
        tags.extend(['dimensionality-reduction', 'unsupervised-learning'])
    if any(word in stem.lower() for word in ['kmeans', 'cluster']):
        tags.extend(['clustering', 'unsupervised-learning'])
    
    # Technical tags
    if any(word in stem.lower() for word in ['visualization', 'plot', 'chart']):
        tags.append('visualization')
    if any(word in stem.lower() for word in ['numpy', 'pandas', 'sklearn']):
        tags.append('python-libraries')
    
    # Default tags if none found
    if not tags:
        tags = ['machine-learning', 'tutorial']
    
    # Create description
    description = f"Interactive tutorial on {title.lower()} with practical implementations and visualizations"
    
    return title, description, tags

def add_notebook_metadata(notebook_path, title=None, description=None, tags=None, dry_run=False):
    """Add Quarto metadata and Colab link to notebook."""
    notebook_path = Path(notebook_path)
    
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")
    
    # Load notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Check if already has metadata
    if has_quarto_metadata(notebook_data):
        print(f"✓ {notebook_path.name} already has Quarto metadata")
        return False
    
    # Infer metadata if not provided
    if not title or not description or not tags:
        inferred_title, inferred_desc, inferred_tags = infer_metadata_from_filename(notebook_path)
        title = title or inferred_title
        description = description or inferred_desc
        tags = tags or inferred_tags
    
    print(f"Adding metadata to {notebook_path.name}:")
    print(f"  Title: {title}")
    print(f"  Description: {description}")
    print(f"  Tags: {tags}")
    
    if dry_run:
        print("  [DRY RUN - no changes made]")
        return True
    
    # Backup original
    backup_path = notebook_path.with_suffix('.ipynb.backup')
    shutil.copy2(notebook_path, backup_path)
    print(f"  Backup created: {backup_path.name}")
    
    # Create new cells
    metadata_cell = create_metadata_cell(title, description, tags)
    colab_cell = create_colab_cell(notebook_path)
    
    # Insert at beginning
    notebook_data['cells'].insert(0, colab_cell)
    notebook_data['cells'].insert(0, metadata_cell)
    
    # Save modified notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Added metadata and Colab link")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Add Quarto metadata and Colab links to Jupyter notebooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add to single notebook with custom metadata
  python add_notebook_metadata.py notebooks/linear-regression.ipynb --title "Linear Regression" --description "Learn linear regression" --tags "regression,ml"
  
  # Add to single notebook with auto-inferred metadata  
  python add_notebook_metadata.py notebooks/linear-regression.ipynb
  
  # Dry run to preview changes
  python add_notebook_metadata.py notebooks/linear-regression.ipynb --dry-run
  
  # Process all notebooks in directory
  python add_notebook_metadata.py notebooks/ --batch
        """
    )
    
    parser.add_argument('path', help='Path to notebook file or directory')
    parser.add_argument('--title', help='Notebook title')
    parser.add_argument('--description', help='Notebook description')
    parser.add_argument('--tags', help='Comma-separated tags')
    parser.add_argument('--author', default='Nipun Batra', help='Author name')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    parser.add_argument('--batch', action='store_true', help='Process all notebooks in directory')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        # Single notebook
        add_notebook_metadata(
            path, 
            title=args.title, 
            description=args.description, 
            tags=args.tags.split(',') if args.tags else None,
            dry_run=args.dry_run
        )
    elif path.is_dir() and args.batch:
        # Batch process directory
        notebooks = list(path.glob('**/*.ipynb'))
        if not notebooks:
            print(f"No notebooks found in {path}")
            return
        
        print(f"Found {len(notebooks)} notebooks to process:")
        modified_count = 0
        
        for notebook in sorted(notebooks):
            try:
                if add_notebook_metadata(notebook, dry_run=args.dry_run):
                    modified_count += 1
                print()
            except Exception as e:
                print(f"  ✗ Error processing {notebook.name}: {e}")
                print()
        
        print(f"Summary: {modified_count} notebooks modified")
    else:
        print("Error: Path must be a notebook file or use --batch for directories")

if __name__ == '__main__':
    main()