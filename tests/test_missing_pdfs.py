#!/usr/bin/env python3
r"""
Test validator for missing PDFs referenced by \includepdf commands in LaTeX files.
Validates that all PDFs referenced by \includepdf exist in the expected locations.
"""

import os
import re
from pathlib import Path


def find_includepdf_references():
    r"""Find all \includepdf references in LaTeX files."""
    references = []
    root_dir = Path(".")
    
    # Find all .tex files
    tex_files = list(root_dir.rglob("*.tex"))
    
    for tex_file in tex_files:
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find \includepdf commands
            # Pattern matches: \includepdf[options]{path/to/file.pdf}
            pattern = r'\\includepdf(?:\[[^\]]*\])?\s*\{([^}]+)\}'
            matches = re.findall(pattern, content)
            
            for match in matches:
                pdf_path = match.strip()
                # Skip LaTeX variables like \i, \thetree
                if '\\' in pdf_path:
                    continue
                    
                references.append({
                    'tex_file': str(tex_file),
                    'pdf_path': pdf_path,
                    'line_context': None  # Could add line number context if needed
                })
                
        except Exception as e:
            print(f"Warning: Could not read {tex_file}: {e}")
    
    return references


def validate_pdf_existence(references):
    """Validate that referenced PDFs exist."""
    missing_pdfs = []
    found_pdfs = []
    
    for ref in references:
        tex_file = Path(ref['tex_file'])
        pdf_path = ref['pdf_path']
        
        # Handle relative paths from the tex file's directory
        tex_dir = tex_file.parent
        
        # Try multiple possible paths
        possible_paths = [
            tex_dir / pdf_path,  # Relative to tex file
            Path(pdf_path),      # Absolute or root-relative
        ]
        
        # If path doesn't have extension, try adding .pdf
        if not pdf_path.endswith('.pdf'):
            for base_path in possible_paths.copy():
                possible_paths.append(base_path.with_suffix('.pdf'))
        
        # Check if any of the possible paths exist
        pdf_exists = False
        actual_path = None
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                pdf_exists = True
                actual_path = str(path)
                break
        
        if pdf_exists:
            found_pdfs.append({
                'tex_file': ref['tex_file'],
                'pdf_path': pdf_path,
                'actual_path': actual_path
            })
        else:
            missing_pdfs.append({
                'tex_file': ref['tex_file'],
                'pdf_path': pdf_path,
                'searched_paths': [str(p) for p in possible_paths]
            })
    
    return found_pdfs, missing_pdfs


def main():
    """Main validation function."""
    print("🔍 Searching for \\includepdf references in LaTeX files...")
    
    references = find_includepdf_references()
    
    if not references:
        print("✅ No \\includepdf references found in LaTeX files.")
        return True
    
    print(f"📄 Found {len(references)} \\includepdf references")
    
    found_pdfs, missing_pdfs = validate_pdf_existence(references)
    
    print(f"\n📊 PDF Reference Validation Results:")
    print(f"   ✅ Found: {len(found_pdfs)} PDFs")
    print(f"   ❌ Missing: {len(missing_pdfs)} PDFs")
    
    if missing_pdfs:
        print(f"\n❌ Missing PDFs:")
        for missing in missing_pdfs:
            print(f"   📄 {missing['pdf_path']}")
            print(f"      Referenced in: {missing['tex_file']}")
            print(f"      Searched paths:")
            for path in missing['searched_paths']:
                print(f"        - {path}")
            print()
        
        print(f"💡 Suggestions:")
        print(f"   - Check if these PDFs need to be generated from LaTeX sources")
        print(f"   - Verify the file paths are correct in the LaTeX files")
        print(f"   - Consider if these are build artifacts that need compilation")
        
        return False
    else:
        print("🎉 All PDF references are valid! ✅")
        return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)