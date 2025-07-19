#!/usr/bin/env python3
"""
Repository Structure Validator

This script validates that the ml-teaching repository follows the documented structure.
It checks for violations and provides specific remediation steps.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

class StructureViolation:
    def __init__(self, path: str, violation_type: str, description: str, fix: str):
        self.path = path
        self.violation_type = violation_type
        self.description = description
        self.fix = fix

class RepositoryStructureValidator:
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.violations: List[StructureViolation] = []
        
        # Expected main categories
        self.categories = ["basics", "maths", "optimization", "supervised", "unsupervised", "neural-networks", "advanced"]
        
    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"🔍 Validating repository structure at: {self.root}")
        
        self._check_main_structure()
        self._check_slide_structure()
        self._check_asset_organization() 
        self._check_shared_usage()
        self._check_notebook_structure()
        
        if self.violations:
            print(f"\n❌ Found {len(self.violations)} structure violations:")
            self._report_violations()
            return False
        else:
            print("\n✅ Repository structure is compliant!")
            return True
    
    def _check_main_structure(self):
        """Check that main categories exist and have correct subdirectories"""
        for category in self.categories:
            category_path = self.root / category
            if not category_path.exists():
                self.violations.append(StructureViolation(
                    path=str(category_path),
                    violation_type="MISSING_CATEGORY",
                    description=f"Missing main category directory: {category}/",
                    fix=f"mkdir -p {category}/{{slides,assets}}"
                ))
                continue
                
            # Check required subdirectories (notebooks are flat, not per-category)
            required_dirs = ["slides", "assets"]
            for req_dir in required_dirs:
                dir_path = category_path / req_dir
                if not dir_path.exists():
                    self.violations.append(StructureViolation(
                        path=str(dir_path),
                        violation_type="MISSING_SUBDIR",
                        description=f"Missing required subdirectory: {category}/{req_dir}/",
                        fix=f"mkdir -p {category}/{req_dir}"
                    ))
                    
            # Check that notebooks/ subdirectory does NOT exist (should be flat)
            notebooks_dir = category_path / "notebooks"
            if notebooks_dir.exists():
                notebook_files = list(notebooks_dir.glob("*.ipynb"))
                if notebook_files:
                    self.violations.append(StructureViolation(
                        path=str(notebooks_dir),
                        violation_type="NESTED_NOTEBOOKS", 
                        description=f"Notebooks should be in main /notebooks/, not {category}/notebooks/",
                        fix=f"mv {category}/notebooks/*.ipynb notebooks/ && rm -rf {category}/notebooks"
                    ))
                else:
                    # Empty notebooks directory - just remove it
                    self.violations.append(StructureViolation(
                        path=str(notebooks_dir),
                        violation_type="UNNECESSARY_DIR",
                        description=f"Empty notebooks/ directory should be removed: {category}/notebooks/",
                        fix=f"rm -rf {category}/notebooks"
                    ))
    
    def _check_slide_structure(self):
        """Check that slides are directly in category/slides/ not nested"""
        for category in self.categories:
            slides_path = self.root / category / "slides"
            if not slides_path.exists():
                continue
                
            # Check for nested slide directories (violation)
            for item in slides_path.iterdir():
                if item.is_dir() and item.name not in [".git", "__pycache__"]:
                    # Check if directory contains .tex files (nested slide violation)
                    tex_files = list(item.glob("*.tex"))
                    if tex_files:
                        self.violations.append(StructureViolation(
                            path=str(item),
                            violation_type="NESTED_SLIDES",
                            description=f"Slides should be directly in {category}/slides/, not nested: {item.name}/",
                            fix=f"mv {category}/slides/{item.name}/*.tex {category}/slides/ && mv {category}/slides/{item.name}/imgs/* {category}/assets/{item.name}/diagrams/ && rm -rf {category}/slides/{item.name}/"
                        ))
    
    def _check_asset_organization(self):
        """Check that assets are properly organized by topic"""
        for category in self.categories:
            assets_path = self.root / category / "assets"
            if not assets_path.exists():
                continue
                
            # Assets should be organized as topic-name/type/ 
            for item in assets_path.iterdir():
                if item.is_dir():
                    # Check that topic directories have proper subdirectories
                    expected_subdirs = ["figures", "diagrams", "notes"]
                    has_expected_subdir = any((item / subdir).exists() for subdir in expected_subdirs)
                    
                    if not has_expected_subdir:
                        # Check if there are files directly in topic dir (should be in subdirs)
                        direct_files = [f for f in item.iterdir() if f.is_file()]
                        if direct_files:
                            self.violations.append(StructureViolation(
                                path=str(item),
                                violation_type="ASSET_ORGANIZATION",
                                description=f"Assets should be in {item.name}/{{figures,diagrams,notes}}/, not directly in {item.name}/",
                                fix=f"mkdir -p {item}/figures && mv {item}/*.{{pdf,png,jpg,svg}} {item}/figures/ 2>/dev/null || true"
                            ))
    
    def _check_shared_usage(self):
        """Check that shared/ only contains truly shared resources"""
        shared_path = self.root / "shared"
        if not shared_path.exists():
            return
            
        # Check for topic-specific figures in shared/ (violation)
        figures_path = shared_path / "figures"
        if figures_path.exists():
            topic_specific_dirs = ["decision-trees", "ensemble", "linear-regression", "logistic-regression", "svm"]
            for topic_dir in topic_specific_dirs:
                topic_path = figures_path / topic_dir
                if topic_path.exists():
                    # Determine which category this belongs to
                    target_category = "supervised"  # Most are supervised learning topics
                    self.violations.append(StructureViolation(
                        path=str(topic_path),
                        violation_type="MISPLACED_ASSETS",
                        description=f"Topic-specific figures should not be in shared/: {topic_dir}",
                        fix=f"mkdir -p {target_category}/assets/{topic_dir}/figures && mv {topic_path}/* {target_category}/assets/{topic_dir}/figures/ && rm -rf {topic_path}"
                    ))
    
    def _check_notebook_structure(self):
        """Check that notebooks are in main /notebooks/ directory (flat structure)"""
        notebooks_path = self.root / "notebooks"
        if not notebooks_path.exists():
            self.violations.append(StructureViolation(
                path=str(notebooks_path),
                violation_type="MISSING_NOTEBOOKS",
                description="Missing main notebooks/ directory",
                fix="mkdir notebooks"
            ))
            return
        
        # Check for notebooks in category subdirectories (violation - should be flat)
        for category in self.categories:
            category_notebooks = self.root / category / "notebooks"
            if category_notebooks.exists():
                notebook_files = list(category_notebooks.glob("*.ipynb"))
                if notebook_files:
                    self.violations.append(StructureViolation(
                        path=str(category_notebooks),
                        violation_type="NESTED_NOTEBOOKS", 
                        description=f"Notebooks should be in main /notebooks/, not {category}/notebooks/",
                        fix=f"mv {category}/notebooks/*.ipynb notebooks/ && rm -rf {category}/notebooks"
                    ))
    
    def _report_violations(self):
        """Report all violations with fixes"""
        violation_types = {}
        for violation in self.violations:
            if violation.violation_type not in violation_types:
                violation_types[violation.violation_type] = []
            violation_types[violation.violation_type].append(violation)
        
        for violation_type, violations in violation_types.items():
            print(f"\n📋 {violation_type} ({len(violations)} issues):")
            for v in violations:
                print(f"   ❌ {v.description}")
                print(f"      📁 Path: {v.path}")
                print(f"      🔧 Fix: {v.fix}")
        
        print(f"\n💡 Quick fix script:")
        print("#!/bin/bash")
        print("# Auto-generated structure fixes")
        for violation in self.violations:
            print(f"# Fix: {violation.description}")
            print(f"{violation.fix}")
            print()

def main():
    """Main entry point"""
    validator = RepositoryStructureValidator()
    is_valid = validator.validate()
    
    if not is_valid:
        print(f"\n📊 Summary: {len(validator.violations)} violations found")
        print("🚀 Run the suggested fixes above to correct the structure")
        sys.exit(1)
    else:
        print("🎉 Repository structure validation passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()