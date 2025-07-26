#!/usr/bin/env python3
"""Check coverage of Quarto metadata in notebooks."""

import json
from pathlib import Path

def has_quarto_metadata(notebook_path):
    """Check if notebook has Quarto metadata in first raw cell."""
    try:
        with open(notebook_path, 'r') as f:
            data = json.load(f)
        if not data.get('cells'):
            return False
        first_cell = data['cells'][0]
        if first_cell.get('cell_type') != 'raw':
            return False
        source = ''.join(first_cell.get('source', []))
        return source.strip().startswith('---') and 'title:' in source
    except:
        return False

def main():
    notebooks = list(Path('notebooks').glob('**/*.ipynb'))
    with_metadata = [nb for nb in notebooks if has_quarto_metadata(nb)]
    
    print(f'Coverage: {len(with_metadata)}/{len(notebooks)} notebooks have Quarto metadata ({len(with_metadata)/len(notebooks)*100:.1f}%)')
    print()
    print('Notebooks WITH metadata:')
    for nb in sorted(with_metadata):
        print(f'  ✓ {nb.name}')
    
    print()
    print('Notebooks WITHOUT metadata:')
    without_metadata = [nb for nb in notebooks if not has_quarto_metadata(nb)]
    for nb in sorted(without_metadata):
        print(f'  ✗ {nb.name}')

if __name__ == '__main__':
    main()