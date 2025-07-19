#!/usr/bin/env python3
r"""
Test validator for slide naming conventions in LaTeX files.
Validates that slide files follow lowercase-with-hyphens.tex naming convention.
"""

import re
from pathlib import Path


def find_slide_files():
    """Find all slide .tex files in the slides directories."""
    slide_files = []
    root_dir = Path(".")
    
    # Find all .tex files in slides directories
    for slides_dir in root_dir.rglob("slides"):
        if slides_dir.is_dir():
            for tex_file in slides_dir.glob("*.tex"):
                slide_files.append(tex_file)
    
    return slide_files


def validate_slide_naming_convention(slide_files):
    """Validate that slide files follow lowercase-with-hyphens.tex naming convention."""
    violations = []
    valid_files = []
    
    # Lowercase with hyphens pattern: allows letters, numbers, and hyphens
    # Must start with letter, can contain hyphens, ends with .tex
    valid_pattern = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*\.tex$')
    
    for slide_file in slide_files:
        filename = slide_file.name
        
        if valid_pattern.match(filename):
            valid_files.append(slide_file)
        else:
            # Suggest a corrected name
            suggested_name = suggest_slide_name(filename)
            violations.append({
                'file': str(slide_file),
                'current_name': filename,
                'suggested_name': suggested_name,
                'issue': get_naming_issue(filename)
            })
    
    return valid_files, violations


def suggest_slide_name(filename):
    """Suggest a valid slide name following the convention."""
    # Remove .tex extension
    name = filename.replace('.tex', '')
    
    # Convert to lowercase
    name = name.lower()
    
    # Replace underscores and spaces with hyphens
    name = name.replace('_', '-').replace(' ', '-')
    
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    # Ensure it starts with a letter
    if name and not name[0].isalpha():
        name = 'slide-' + name
    
    return name + '.tex'


def get_naming_issue(filename):
    """Identify the specific naming issue."""
    issues = []
    
    name_without_ext = filename.replace('.tex', '')
    
    if name_without_ext != name_without_ext.lower():
        issues.append("contains uppercase letters")
    
    if '_' in name_without_ext:
        issues.append("contains underscores (use hyphens)")
    
    if ' ' in name_without_ext:
        issues.append("contains spaces (use hyphens)")
    
    if '--' in name_without_ext:
        issues.append("contains multiple consecutive hyphens")
    
    if name_without_ext.startswith('-') or name_without_ext.endswith('-'):
        issues.append("starts or ends with hyphen")
    
    if name_without_ext and not name_without_ext[0].isalpha():
        issues.append("doesn't start with a letter")
    
    return "; ".join(issues) if issues else "unknown issue"


def main():
    """Main validation function."""
    print("🔍 Searching for slide .tex files...")
    
    slide_files = find_slide_files()
    
    if not slide_files:
        print("✅ No slide files found.")
        return True
    
    print(f"📄 Found {len(slide_files)} slide files")
    
    valid_files, violations = validate_slide_naming_convention(slide_files)
    
    print(f"\n📊 Slide Naming Convention Results:")
    print(f"   ✅ Valid: {len(valid_files)} slides")
    print(f"   ❌ Violations: {len(violations)} slides")
    
    if violations:
        print(f"\n❌ Slide Naming Convention Violations:")
        for i, violation in enumerate(violations, 1):
            print(f"   {i}. {violation['current_name']}")
            print(f"      📂 Path: {violation['file']}")
            print(f"      🔧 Issue: {violation['issue']}")
            print(f"      💡 Suggested: {violation['suggested_name']}")
            print()
        
        print(f"📋 Convention: Slide files should follow 'lowercase-with-hyphens.tex' format")
        print(f"   ✅ Good: 'linear-regression.tex', 'svm-intro.tex', 'ensemble.tex'")
        print(f"   ❌ Bad: 'Linear-Regression.tex', 'SVM_intro.tex', 'Ensemble.tex'")
        
        return False
    else:
        print("🎉 All slide naming conventions are valid! ✅")
        return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)