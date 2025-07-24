#!/usr/bin/env python3
"""Check if notebooks have Colab links in the second cell after metadata."""

import json
from pathlib import Path

def has_colab_link(notebook_path):
    """Check if notebook has Colab link in second cell."""
    try:
        with open(notebook_path, 'r') as f:
            data = json.load(f)
        
        if len(data.get('cells', [])) < 2:
            return False, "Less than 2 cells"
        
        # Check if first cell is raw metadata
        first_cell = data['cells'][0]
        if first_cell.get('cell_type') != 'raw':
            return False, "First cell is not raw metadata"
        
        # Check if second cell has Colab link
        second_cell = data['cells'][1]
        if second_cell.get('cell_type') != 'markdown':
            return False, "Second cell is not markdown"
        
        source = ''.join(second_cell.get('source', []))
        has_colab = 'colab.research.google.com' in source and 'Open In Colab' in source
        
        return has_colab, source.strip()[:100] + "..." if source else "Empty cell"
        
    except Exception as e:
        return False, f"Error: {e}"

def main():
    notebooks = list(Path('notebooks').glob('**/*.ipynb'))
    
    with_colab = []
    without_colab = []
    
    for notebook in sorted(notebooks):
        has_link, content = has_colab_link(notebook)
        if has_link:
            with_colab.append(notebook)
        else:
            without_colab.append((notebook, content))
    
    print(f'Coverage: {len(with_colab)}/{len(notebooks)} notebooks have Colab links ({len(with_colab)/len(notebooks)*100:.1f}%)')
    print()
    
    if without_colab:
        print('Notebooks WITHOUT Colab links:')
        for notebook, reason in without_colab:
            print(f'  ✗ {notebook.name}: {reason}')
    else:
        print('✅ All notebooks have Colab links!')
    
    if with_colab:
        print()
        print('Notebooks WITH Colab links:')
        for notebook in with_colab:
            print(f'  ✓ {notebook.name}')

if __name__ == '__main__':
    main()