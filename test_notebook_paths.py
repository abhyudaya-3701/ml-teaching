#!/usr/bin/env python3
"""
Notebook Image Path Validator

This script validates that image paths in Jupyter notebooks follow the
reorganized asset structure and don't reference deprecated shared/ paths.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict

class NotebookPathViolation:
    def __init__(self, notebook: str, cell_id: str, old_path: str, 
                 violation_type: str, description: str, fix: str):
        self.notebook = notebook
        self.cell_id = cell_id
        self.old_path = old_path
        self.violation_type = violation_type
        self.description = description
        self.fix = fix

class NotebookPathValidator:
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.violations: List[NotebookPathViolation] = []
        
        # Patterns for deprecated paths
        self.deprecated_patterns = {
            r'\.\./shared/figures/ensemble/': '../supervised/assets/ensemble/figures/',
            r'\.\./shared/figures/diagrams/ensemble/': '../supervised/assets/ensemble/diagrams/',
            r'\.\./shared/figures/decision-trees/': '../supervised/assets/decision-trees/figures/',
            r'\.\./shared/figures/linear-regression/': '../supervised/assets/linear-regression/figures/',
            r'\.\./shared/figures/logistic-regression/': '../supervised/assets/logistic-regression/figures/',
            r'\.\./diagrams/ensemble/': '../supervised/assets/ensemble/diagrams/',
            r'\.\./figures/ensemble/': '../supervised/assets/ensemble/figures/',
        }
    
    def validate(self) -> bool:
        """Run validation on all notebook files"""
        print(f"📓 Validating image paths in Jupyter notebooks...")
        
        notebook_files = list(self.root.glob("**/*.ipynb"))
        if not notebook_files:
            print("⚠️  No .ipynb files found!")
            return True
            
        print(f"📄 Found {len(notebook_files)} notebook files to validate")
        
        for notebook_file in notebook_files:
            self._validate_notebook(notebook_file)
        
        if self.violations:
            print(f"\n❌ Found {len(self.violations)} notebook path violations:")
            self._report_violations()
            return False
        else:
            print("\n✅ All notebook image paths are compliant!")
            return True
    
    def _validate_notebook(self, notebook_file: Path):
        """Validate image paths in a single notebook"""
        try:
            with open(notebook_file, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
        except Exception as e:
            print(f"⚠️  Could not read {notebook_file}: {e}")
            return
        
        for cell in notebook.get('cells', []):
            cell_id = cell.get('id', 'unknown')
            source = cell.get('source', [])
            
            # Join source lines if it's a list
            if isinstance(source, list):
                source_text = ''.join(source)
            else:
                source_text = source
            
            self._check_cell_for_deprecated_paths(notebook_file, cell_id, source_text)
    
    def _check_cell_for_deprecated_paths(self, notebook_file: Path, cell_id: str, source_text: str):
        """Check a cell's source for deprecated image paths"""
        for deprecated_pattern, replacement in self.deprecated_patterns.items():
            matches = re.finditer(deprecated_pattern, source_text)
            for match in matches:
                old_path = match.group(0)
                self.violations.append(NotebookPathViolation(
                    notebook=str(notebook_file),
                    cell_id=cell_id,
                    old_path=old_path,
                    violation_type="DEPRECATED_PATH",
                    description=f"Uses deprecated path: {old_path}",
                    fix=f"Replace with: {replacement}"
                ))
    
    def _report_violations(self):
        """Report all violations"""
        violation_types = {}
        for violation in self.violations:
            if violation.violation_type not in violation_types:
                violation_types[violation.violation_type] = []
            violation_types[violation.violation_type].append(violation)
        
        for violation_type, violations in violation_types.items():
            print(f"\n📋 {violation_type} ({len(violations)} issues):")
            for v in violations:
                print(f"   ❌ {v.description}")
                print(f"      📓 Notebook: {v.notebook}")
                print(f"      🔢 Cell: {v.cell_id}")
                print(f"      📁 Old path: {v.old_path}")
                print(f"      🔧 Fix: {v.fix}")

def main():
    """Main entry point"""
    validator = NotebookPathValidator()
    is_valid = validator.validate()
    
    if not is_valid:
        print(f"\n📊 Summary: {len(validator.violations)} notebook path violations found")
        print("🚀 Update the notebook paths to use the new asset organization")
        sys.exit(1)
    else:
        print("🎉 All notebook image paths are valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()