#!/usr/bin/env python3
"""
Script to check for broken links in QMD files
"""
import os
import re
import sys
from pathlib import Path

def extract_links(content):
    """Extract all links from markdown content"""
    # Pattern to match markdown links [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(pattern, content)
    return [(text.strip(), url.strip()) for text, url in links]

def check_link(link, base_path):
    """Check if a link is valid"""
    url = link[1]
    
    # Skip external links
    if url.startswith('http'):
        return True, "External link"
    
    # Handle relative paths
    if url.startswith('.'):
        full_path = (base_path.parent / url).resolve()
    else:
        full_path = (base_path.parent / url).resolve()
    
    # Check if file exists
    if full_path.exists():
        return True, f"File exists: {full_path}"
    else:
        return False, f"File not found: {full_path}"

def main():
    # Get all QMD files
    project_root = Path(__file__).parent
    qmd_files = list(project_root.glob('*.qmd'))
    
    # Also check slides and tutorials directories
    for dir_name in ['slides', 'tutorials']:
        qmd_files.extend(project_root.glob(f'{dir_name}/*.qmd'))
    
    broken_links = []
    
    for qmd_file in qmd_files:
        print(f"\nChecking {qmd_file.name}...")
        content = qmd_file.read_text()
        links = extract_links(content)
        
        for link in links:
            is_valid, message = check_link(link, qmd_file)
            if not is_valid:
                broken_links.append((qmd_file.name, link[0], link[1]))
                print(f"  ❌ BROKEN: [{link[0]}]({link[1]})")
            else:
                print(f"  ✅ OK: [{link[0]}]({link[1]}) - {message}")
    
    if broken_links:
        print(f"\n\nFound {len(broken_links)} broken links:")
        for file, text, url in broken_links:
            print(f"  - {file}: [{text}]({url})")
        return 1
    else:
        print("\n\nAll links are valid!")
        return 0

if __name__ == "__main__":
    sys.exit(main())