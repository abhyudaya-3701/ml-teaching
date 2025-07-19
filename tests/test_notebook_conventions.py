#!/usr/bin/env python3
"""
Notebook Convention Validator

This script validates:
1. Notebook naming conventions (lowercase, hyphens, no spaces)
2. LaTeX notebookbox links match existing notebooks
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set

class NotebookConventionViolation:
    def __init__(self, file_path: str, violation_type: str, description: str, fix: str):
        self.file_path = file_path
        self.violation_type = violation_type
        self.description = description
        self.fix = fix

class NotebookConventionValidator:
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.violations: List[NotebookConventionViolation] = []
        
        # Expected naming pattern: lowercase-with-hyphens.ipynb
        self.valid_notebook_pattern = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*\.ipynb$')
        
        # Pattern to find notebookbox references in LaTeX
        self.notebookbox_pattern = re.compile(
            r'\\begin\{notebookbox\}\{([^}]+)\}',
            re.IGNORECASE
        )
        
    def validate(self) -> bool:
        """Run all notebook convention validations"""
        print(f"📓 Validating notebook conventions...")
        
        # Get all notebooks
        notebook_files = list((self.root / "notebooks").glob("*.ipynb"))
        tex_files = list(self.root.glob("**/*.tex"))
        
        print(f"📄 Found {len(notebook_files)} notebooks and {len(tex_files)} LaTeX files")
        
        # Validate naming conventions
        print(f"\n📋 Checking notebook naming conventions...")
        naming_issues = len(self.violations)
        self._validate_notebook_naming(notebook_files)
        print(f"   ✅ Naming convention check: {len(self.violations) - naming_issues} issues found")
        
        # Validate notebookbox references
        print(f"\n🔗 Checking LaTeX notebookbox references...")
        reference_issues = len(self.violations)
        self._validate_notebookbox_references(tex_files, notebook_files)
        print(f"   ✅ Reference validation check: {len(self.violations) - reference_issues} issues found")
        
        # Report results
        if self.violations:
            print(f"\n❌ Found {len(self.violations)} notebook convention violations:")
            self._report_violations()
            return False
        else:
            print(f"\n🎉 All notebook conventions are 100% compliant!")
            print(f"✅ All {len(notebook_files)} notebooks follow naming conventions")
            print(f"✅ All notebookbox references match existing notebooks")
            return True
    
    def _validate_notebook_naming(self, notebook_files: List[Path]):
        """Validate that all notebooks follow naming conventions"""
        for notebook in notebook_files:
            filename = notebook.name
            
            if not self.valid_notebook_pattern.match(filename):
                # Determine specific violation type
                if ' ' in filename:
                    violation_type = "SPACES_IN_NAME"
                    description = f"Notebook name contains spaces: {filename}"
                    fix = f"Rename to: {filename.replace(' ', '-').lower()}"
                elif filename != filename.lower():
                    violation_type = "UPPERCASE_LETTERS"
                    description = f"Notebook name contains uppercase letters: {filename}"
                    fix = f"Rename to: {filename.lower()}"
                elif '_' in filename:
                    violation_type = "UNDERSCORES_USED"
                    description = f"Notebook name uses underscores instead of hyphens: {filename}"
                    fix = f"Rename to: {filename.replace('_', '-')}"
                else:
                    violation_type = "INVALID_FORMAT"
                    description = f"Notebook name doesn't follow a-b-c.ipynb pattern: {filename}"
                    fix = f"Rename to follow lowercase-with-hyphens.ipynb pattern"
                
                self.violations.append(NotebookConventionViolation(
                    file_path=str(notebook),
                    violation_type=violation_type,
                    description=description,
                    fix=fix
                ))
    
    def _validate_notebookbox_references(self, tex_files: List[Path], notebook_files: List[Path]):
        """Validate that notebookbox references match existing notebooks"""
        # Create set of available notebook names (without .ipynb extension)
        available_notebooks = {nb.stem for nb in notebook_files}
        
        for tex_file in tex_files:
            try:
                with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️  Could not read {tex_file}: {e}")
                continue
            
            # Find all notebookbox references
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                matches = self.notebookbox_pattern.findall(line)
                for url in matches:
                    self._validate_notebookbox_url(tex_file, line_num, url, available_notebooks)
    
    def _validate_notebookbox_url(self, tex_file: Path, line_num: int, url: str, available_notebooks: Set[str]):
        """Validate a single notebookbox URL reference"""
        # Extract notebook name from URL
        # Expected format: https://nipunbatra.github.io/ml-teaching/notebooks/NOTEBOOK_NAME.html
        
        if not url.startswith('https://nipunbatra.github.io/ml-teaching/notebooks/'):
            self.violations.append(NotebookConventionViolation(
                file_path=f"{tex_file}:{line_num}",
                violation_type="INVALID_NOTEBOOK_URL",
                description=f"Notebookbox URL doesn't follow expected pattern: {url}",
                fix="Use https://nipunbatra.github.io/ml-teaching/notebooks/NOTEBOOK_NAME.html format"
            ))
            return
        
        # Extract notebook name
        url_path = url.replace('https://nipunbatra.github.io/ml-teaching/notebooks/', '')
        if not url_path.endswith('.html'):
            self.violations.append(NotebookConventionViolation(
                file_path=f"{tex_file}:{line_num}",
                violation_type="INVALID_NOTEBOOK_URL",
                description=f"Notebookbox URL should end with .html: {url}",
                fix="Ensure URL ends with .html"
            ))
            return
        
        notebook_name = url_path[:-5]  # Remove .html extension
        
        # Check if corresponding notebook exists
        if notebook_name not in available_notebooks:
            self.violations.append(NotebookConventionViolation(
                file_path=f"{tex_file}:{line_num}",
                violation_type="MISSING_NOTEBOOK",
                description=f"Notebookbox references non-existent notebook: {notebook_name}.ipynb",
                fix=f"Create notebooks/{notebook_name}.ipynb or fix the reference"
            ))
        
        # Check if notebook name follows naming conventions
        if not self.valid_notebook_pattern.match(f"{notebook_name}.ipynb"):
            suggested_name = self._suggest_notebook_name(notebook_name)
            self.violations.append(NotebookConventionViolation(
                file_path=f"{tex_file}:{line_num}",
                violation_type="INCONSISTENT_NAMING",
                description=f"Notebookbox references notebook with non-standard name: {notebook_name}",
                fix=f"Rename notebook to: {suggested_name} and update URL"
            ))
    
    def _suggest_notebook_name(self, name: str) -> str:
        """Suggest a properly formatted notebook name"""
        # Convert to lowercase, replace spaces/underscores with hyphens
        suggested = name.lower().replace(' ', '-').replace('_', '-')
        # Remove any non-alphanumeric characters except hyphens
        suggested = re.sub(r'[^a-z0-9-]', '', suggested)
        # Remove multiple consecutive hyphens
        suggested = re.sub(r'-+', '-', suggested)
        # Remove leading/trailing hyphens
        suggested = suggested.strip('-')
        return f"{suggested}.ipynb"
    
    def _report_violations(self):
        """Report all violations grouped by type"""
        violation_types = {}
        for violation in self.violations:
            if violation.violation_type not in violation_types:
                violation_types[violation.violation_type] = []
            violation_types[violation.violation_type].append(violation)
        
        for violation_type, violations in violation_types.items():
            print(f"\n📋 {violation_type} ({len(violations)} issues):")
            for v in violations:
                print(f"   ❌ {v.description}")
                print(f"      📁 File: {v.file_path}")
                print(f"      🔧 Fix: {v.fix}")
        
        print(f"\n💡 Notebook naming conventions:")
        print(f"   ✅ Good: entropy.ipynb, decision-trees.ipynb, k-means-clustering.ipynb")
        print(f"   ❌ Bad: Entropy.ipynb, Decision Trees.ipynb, k_means_clustering.ipynb")
        print(f"\n💡 Notebookbox URL format:")
        print(f"   ✅ Good: https://nipunbatra.github.io/ml-teaching/notebooks/entropy.html")
        print(f"   ❌ Bad: different domain or path format")

def main():
    """Main entry point"""
    validator = NotebookConventionValidator()
    is_valid = validator.validate()
    
    if not is_valid:
        print(f"\n📊 Summary: {len(validator.violations)} notebook convention violations found")
        print(f"🚀 Fix the violations above to ensure consistent notebook organization")
        sys.exit(1)
    else:
        print(f"🎉 All notebook conventions are valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()