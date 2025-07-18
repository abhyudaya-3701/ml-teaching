#!/usr/bin/env python3
"""
Script to verify that all image assets referenced in notebooks actually exist.
"""

import os
import json
import glob
import re

def check_notebook_assets(notebook_path):
    """Check if all assets in a notebook exist."""
    
    print(f"Checking {notebook_path}")
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Get notebook directory for relative path resolution
    notebook_dir = os.path.dirname(notebook_path)
    
    # Process each cell
    for i, cell in enumerate(notebook['cells']):
        if 'source' in cell:
            source_lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
            source = ''.join(source_lines)
            
            # Look for image references
            patterns = [
                r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg))\)',  # ![alt](path)
                r"Image\(filename=['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]",  # Image(filename='path')
                r"imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]",  # imread('path')
                r"cv2\.imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]",  # cv2.imread('path')
                r"io\.imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]",  # io.imread('path')
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, source)
                
                for match in matches:
                    if isinstance(match, tuple):
                        image_path = match[1] if len(match) > 1 else match[0]
                    else:
                        image_path = match
                    
                    # Skip URLs and generated files
                    if image_path.startswith('http') or any(gen in image_path for gen in ['demo.gif', 'mnist.gif', 'algo.gif', 'dog.jpg']):
                        continue
                    
                    # Check if file exists
                    if image_path.startswith('../'):
                        # Relative path
                        abs_path = os.path.abspath(os.path.join(notebook_dir, image_path))
                        if not os.path.exists(abs_path):
                            print(f"  ❌ Missing: {image_path} (cell {i})")
                            print(f"      Resolved to: {abs_path}")
                        else:
                            print(f"  ✓ Found: {image_path}")
                    else:
                        # Relative to notebook directory
                        abs_path = os.path.abspath(os.path.join(notebook_dir, image_path))
                        if not os.path.exists(abs_path):
                            print(f"  ❌ Missing: {image_path} (cell {i})")
                            print(f"      Resolved to: {abs_path}")

def main():
    """Main function."""
    
    # Change to the ml-teaching directory
    os.chdir('/Users/nipun/git/ml-teaching')
    
    # Find all notebooks
    notebook_files = glob.glob('notebooks/*.ipynb')
    
    print(f"Checking {len(notebook_files)} notebooks for missing assets...")
    
    for notebook_path in notebook_files:
        check_notebook_assets(notebook_path)
    
    print("\nAsset verification complete!")

if __name__ == "__main__":
    main()