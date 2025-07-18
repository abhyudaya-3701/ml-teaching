#!/usr/bin/env python3
"""
Script to fix image paths in Jupyter notebooks for Quarto rendering.
This script will update paths to point to the correct locations in the repository.
"""

import os
import json
import glob
import shutil

def find_actual_path(filename, search_dirs):
    """Find the actual path of a file in the repository."""
    for search_dir in search_dirs:
        for root, dirs, files in os.walk(search_dir):
            if filename in files:
                # Return relative path from notebooks directory
                rel_path = os.path.relpath(os.path.join(root, filename), 'notebooks')
                return rel_path
    return None

def fix_notebook_paths(notebook_path):
    """Fix image paths in a single notebook."""
    
    # Common search directories for assets
    search_dirs = [
        '../shared/figures',
        '../supervised/assets', 
        '../unsupervised/assets',
        '../neural-networks/assets',
        '../maths/assets',
        '../optimization/assets',
        '../datasets',
        '../shared/assets'
    ]
    
    print(f"Processing {notebook_path}")
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    modified = False
    
    # Process each cell
    for cell in notebook['cells']:
        if 'source' in cell:
            source_lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
            new_source = []
            
            for line in source_lines:
                original_line = line
                
                # Look for image references in various formats
                import re
                
                # Pattern 1: ![alt](path) - Markdown images
                markdown_pattern = r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg))\)'
                
                # Pattern 2: Image(filename='path') - IPython display
                ipython_pattern = r"Image\(filename=['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]"
                
                # Pattern 3: imread('path') - Image loading
                imread_pattern = r"imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]"
                
                # Pattern 4: plt.savefig('path') - Matplotlib save
                savefig_pattern = r"plt\.savefig\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]"
                
                # Pattern 5: cv2.imread('path') - OpenCV
                cv2_pattern = r"cv2\.imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]"
                
                # Pattern 6: io.imread('path') - skimage
                skimage_pattern = r"io\.imread\(['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|svg))['\"]"
                
                patterns = [
                    (markdown_pattern, r'![\1]({})', 2),
                    (ipython_pattern, r"Image(filename='{}')", 1),
                    (imread_pattern, r"imread('{}')", 1),
                    (savefig_pattern, r"plt.savefig('{}'", 1),
                    (cv2_pattern, r"cv2.imread('{}')", 1),
                    (skimage_pattern, r"io.imread('{}')", 1)
                ]
                
                for pattern, replacement_template, path_group in patterns:
                    matches = re.findall(pattern, line)
                    
                    for match in matches:
                        if isinstance(match, tuple):
                            image_path = match[path_group - 1]
                        else:
                            image_path = match
                        
                        # Extract just the filename
                        filename = os.path.basename(image_path)
                        
                        # Skip if it's a generated file (common in notebooks)
                        if any(gen_name in filename for gen_name in ['demo.gif', 'mnist.gif', 'algo.gif', 'temp.png']):
                            continue
                        
                        # Find the actual path
                        actual_path = find_actual_path(filename, search_dirs)
                        
                        if actual_path and actual_path != image_path:
                            print(f"  Fixing: {image_path} -> {actual_path}")
                            
                            if pattern == markdown_pattern:
                                line = re.sub(pattern, replacement_template.format(actual_path), line)
                            else:
                                line = re.sub(pattern, replacement_template.format(actual_path), line)
                            
                            modified = True
                
                new_source.append(line)
            
            if new_source != source_lines:
                cell['source'] = new_source
    
    # Write back if modified
    if modified:
        # Create backup
        backup_path = notebook_path + '.backup'
        shutil.copy2(notebook_path, backup_path)
        
        # Write fixed notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Fixed and backed up to {backup_path}")
    else:
        print(f"  ✓ No changes needed")

def main():
    """Main function to process all notebooks."""
    
    # Change to the ml-teaching directory
    os.chdir('/Users/nipun/git/ml-teaching')
    
    # Find all notebooks
    notebook_files = glob.glob('notebooks/*.ipynb')
    
    print(f"Found {len(notebook_files)} notebooks to process")
    
    for notebook_path in notebook_files:
        fix_notebook_paths(notebook_path)
    
    print("\nDone! All notebooks have been processed.")
    print("Original files have been backed up with .backup extension.")

if __name__ == "__main__":
    main()