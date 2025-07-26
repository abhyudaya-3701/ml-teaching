#!/usr/bin/env python3
"""
Comprehensive content audit for slides and tutorials.

This script performs thorough checks for:
- Mathematical notation consistency
- Spelling and grammar errors
- LaTeX compilation issues
- Content accuracy and completeness
- Formatting consistency
- Reference validity
"""

import re
import subprocess
from pathlib import Path
from collections import defaultdict
import json

class ContentAuditor:
    def __init__(self):
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.stats = defaultdict(int)
        
        # Common LaTeX/Math notation patterns to check
        self.notation_patterns = {
            'inconsistent_vectors': [
                (r'\\mathbf\{([^}]+)\}', r'\\v\1'),  # Should use \v prefix
                (r'\\vec\{([^}]+)\}', r'\\v\1'),     # Should use \v prefix
            ],
            'inconsistent_matrices': [
                (r'\\mathbf\{([A-Z][^}]*)\}', r'\\m\1'),  # Should use \m prefix
                (r'\\mathrm\{([A-Z][^}]*)\}', r'\\m\1'),  # Should use \m prefix
            ],
            'inconsistent_sets': [
                (r'\\mathbb\{([^}]+)\}', r'\\s\1'),  # Should use \s prefix for sets
            ],
            'math_mode_issues': [
                (r'\$([^$]*[a-zA-Z][^$]*)\$(?=[a-zA-Z])', 'Missing space after inline math'),
                (r'(?<=[a-zA-Z])\$([^$]*[a-zA-Z][^$]*)\$', 'Missing space before inline math'),
            ]
        }
        
        # Common spelling/grammar issues in ML content
        self.common_errors = {
            'hyperparameter': ['hyper-parameter', 'hyper parameter'],
            'overfitting': ['over-fitting', 'over fitting'],
            'underfitting': ['under-fitting', 'under fitting'],
            'cross-validation': ['crossvalidation', 'cross validation'],
            'preprocessing': ['pre-processing', 'pre processing'],
            'dataset': ['data set', 'data-set'],
            'gradient descent': ['gradient-descent'],
            'machine learning': ['machine-learning', 'machinelearning'],
        }
        
        # LaTeX commands that should be consistent
        self.latex_consistency = {
            'argmin': r'\\argmin',
            'argmax': r'\\argmax', 
            'minimize': r'\\minimize',
            'subject to': r'\\text{subject to}',
        }

    def audit_file(self, file_path):
        """Audit a single file for issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.issues[file_path].append(f"Cannot read file: {e}")
            return
        
        self.stats['files_checked'] += 1
        
        # Check mathematical notation
        self._check_math_notation(file_path, content)
        
        # Check spelling and common errors
        self._check_spelling(file_path, content)
        
        # Check LaTeX specific issues
        if file_path.suffix == '.tex':
            self._check_latex_issues(file_path, content)
        
        # Check content structure
        self._check_content_structure(file_path, content)
        
        # Check references and citations
        self._check_references(file_path, content)

    def _check_math_notation(self, file_path, content):
        """Check mathematical notation consistency."""
        for category, patterns in self.notation_patterns.items():
            for pattern, suggestion in patterns:
                if isinstance(suggestion, str) and suggestion.startswith('\\'):
                    # Pattern replacement suggestion
                    matches = re.findall(pattern, content)
                    if matches:
                        self.issues[file_path].append(
                            f"Inconsistent notation ({category}): Found {len(matches)} instances of {pattern}"
                        )
                else:
                    # Issue description
                    if re.search(pattern, content):
                        self.issues[file_path].append(f"Math formatting issue: {suggestion}")
        
        # Check for common math notation errors
        if re.search(r'\$\$[^$]*[a-zA-Z][^$]*\$\$\n*[a-zA-Z]', content):
            self.warnings[file_path].append("Display math followed immediately by text (missing newline)")
        
        if re.search(r'[a-zA-Z]\$\$', content):
            self.warnings[file_path].append("Display math preceded immediately by text (missing newline)")

    def _check_spelling(self, file_path, content):
        """Check for common spelling and terminology errors."""
        for correct, incorrect_list in self.common_errors.items():
            for incorrect in incorrect_list:
                # Case-insensitive search
                pattern = re.compile(re.escape(incorrect), re.IGNORECASE)
                matches = pattern.findall(content)
                if matches:
                    self.issues[file_path].append(
                        f"Spelling/terminology: '{incorrect}' should be '{correct}' ({len(matches)} instances)"
                    )

    def _check_latex_issues(self, file_path, content):
        """Check LaTeX-specific issues."""
        # Check for missing packages
        packages_used = set()
        packages_included = set()
        
        # Find package inclusions
        for match in re.finditer(r'\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}', content):
            packages_included.update(match.group(1).split(','))
        
        # Check for common commands that need packages
        package_commands = {
            'amsmath': [r'\\align', r'\\equation', r'\\matrix'],
            'amssymb': [r'\\mathbb', r'\\mathfrak'],
            'graphicx': [r'\\includegraphics'],
            'hyperref': [r'\\href', r'\\url'],
            'tikz': [r'\\begin\{tikzpicture\}'],
            'booktabs': [r'\\toprule', r'\\midrule', r'\\bottomrule'],
        }
        
        for package, commands in package_commands.items():
            for cmd_pattern in commands:
                if re.search(cmd_pattern, content) and package not in packages_included:
                    self.warnings[file_path].append(f"May need \\usepackage{{{package}}} for {cmd_pattern}")
        
        # Check for unmatched braces/environments
        brace_count = content.count('{') - content.count('}')
        if brace_count != 0:
            self.issues[file_path].append(f"Unmatched braces: {brace_count} difference")
        
        # Check for common LaTeX errors
        if re.search(r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}', content, re.DOTALL):
            # Find mismatched environments
            begin_envs = re.findall(r'\\begin\{([^}]+)\}', content)
            end_envs = re.findall(r'\\end\{([^}]+)\}', content)
            
            if len(begin_envs) != len(end_envs):
                self.issues[file_path].append("Mismatched \\begin and \\end environments")

    def _check_content_structure(self, file_path, content):
        """Check content structure and organization."""
        lines = content.split('\n')
        
        # Check for overly long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.warnings[file_path].append(f"Line {i}: Very long line ({len(line)} chars)")
        
        # Check for consecutive blank lines
        blank_count = 0
        for i, line in enumerate(lines, 1):
            if line.strip() == '':
                blank_count += 1
                if blank_count > 2:
                    self.warnings[file_path].append(f"Line {i}: Too many consecutive blank lines")
            else:
                blank_count = 0
        
        # Check for proper section structure in LaTeX
        if file_path.suffix == '.tex':
            sections = re.findall(r'\\(sub)*section\{([^}]+)\}', content)
            if len(sections) == 0 and '\\documentclass' in content:
                self.warnings[file_path].append("No sections found in document")

    def _check_references(self, file_path, content):
        """Check references and citations."""
        # Find citations
        citations = re.findall(r'\\cite\{([^}]+)\}', content)
        
        # Find bibliography entries  
        bib_entries = re.findall(r'\\bibitem\{([^}]+)\}', content)
        
        # Check for uncited references
        cited = set()
        for cite_list in citations:
            cited.update(cite_list.split(','))
        
        bib_keys = set(bib_entries)
        
        uncited = bib_keys - cited
        if uncited:
            self.warnings[file_path].append(f"Uncited bibliography entries: {uncited}")
        
        missing = cited - bib_keys
        if missing:
            self.issues[file_path].append(f"Missing bibliography entries: {missing}")
        
        # Check for missing file references
        self._check_file_references(file_path, content)

    def _check_file_references(self, file_path, content):
        """Check for missing figure files, graphics, etc."""
        import os
        
        # Get directory of the current file
        base_dir = file_path.parent
        
        # Find includegraphics references
        graphics_matches = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', content)
        for graphic_file in graphics_matches:
            # Handle different possible paths
            possible_paths = [
                base_dir / graphic_file,
                base_dir / f"{graphic_file}.pdf",
                base_dir / f"{graphic_file}.png", 
                base_dir / f"{graphic_file}.jpg",
                base_dir / f"{graphic_file}.eps",
            ]
            
            # Check for assets/figures directories
            if 'assets' in str(base_dir) or 'figures' in str(base_dir):
                pass  # Already in figures directory
            else:
                # Look for common figure directories
                for fig_dir in ['figures', 'assets', 'diagrams', 'imgs']:
                    possible_paths.extend([
                        base_dir / fig_dir / graphic_file,
                        base_dir / fig_dir / f"{graphic_file}.pdf",
                        base_dir / fig_dir / f"{graphic_file}.png",
                        base_dir / fig_dir / f"{graphic_file}.jpg",
                    ])
            
            # Check if any path exists
            if not any(path.exists() for path in possible_paths):
                self.issues[file_path].append(f"Missing figure file: {graphic_file}")
        
        # Find graphicspath specifications
        graphicspaths = re.findall(r'\\graphicspath\{\s*\{([^}]+)\}\s*\}', content)
        for graphics_path in graphicspaths:
            full_path = base_dir / graphics_path
            if not full_path.exists():
                self.warnings[file_path].append(f"Graphics path does not exist: {graphics_path}")
        
        # Find input/include file references
        input_matches = re.findall(r'\\(?:input|include)\{([^}]+)\}', content)
        for input_file in input_matches:
            # Skip if it looks like a package
            if not input_file.endswith('.tex') and '/' not in input_file:
                continue
                
            possible_paths = [
                base_dir / input_file,
                base_dir / f"{input_file}.tex",
            ]
            
            if not any(path.exists() for path in possible_paths):
                self.issues[file_path].append(f"Missing input file: {input_file}")
                
        # Find usepackage with file paths (local packages)
        package_matches = re.findall(r'\\usepackage\{([^}]*[./][^}]*)\}', content)
        for package_file in package_matches:
            possible_paths = [
                base_dir / package_file,
                base_dir / f"{package_file}.sty",
            ]
            
            if not any(path.exists() for path in possible_paths):
                self.warnings[file_path].append(f"Local package file not found: {package_file}")
                
        # Check for TikZ external files
        tikz_matches = re.findall(r'\\tikzsetnextfilename\{([^}]+)\}', content)
        for tikz_file in tikz_matches:
            tikz_path = base_dir / f"{tikz_file}.pdf"
            if not tikz_path.exists():
                self.warnings[file_path].append(f"TikZ external file missing: {tikz_file}.pdf")

    def audit_all_content(self):
        """Audit all slides and tutorials."""
        print("🔍 Starting comprehensive content audit...\n")
        
        # Find all LaTeX files
        latex_files = []
        for pattern in ['**/*.tex', '**/*.latex']:
            latex_files.extend(Path('.').glob(pattern))
        
        # Find all markdown files
        md_files = list(Path('.').glob('**/*.md'))
        
        all_files = latex_files + md_files
        
        print(f"Found {len(all_files)} files to audit:")
        print(f"  - LaTeX files: {len(latex_files)}")
        print(f"  - Markdown files: {len(md_files)}")
        print()
        
        for file_path in sorted(all_files):
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '_site', 'figures']):
                continue
                
            print(f"Auditing: {file_path}")
            self.audit_file(file_path)
        
        self._print_report()

    def _print_report(self):
        """Print comprehensive audit report."""
        print("\n" + "="*80)
        print("📋 COMPREHENSIVE CONTENT AUDIT REPORT")
        print("="*80)
        
        total_issues = sum(len(issues) for issues in self.issues.values())
        total_warnings = sum(len(warnings) for warnings in self.warnings.values())
        
        print(f"\n📊 SUMMARY:")
        print(f"  Files checked: {self.stats['files_checked']}")
        print(f"  Issues found: {total_issues}")
        print(f"  Warnings: {total_warnings}")
        
        if total_issues == 0 and total_warnings == 0:
            print("\n✅ No issues or warnings found! Content is in excellent condition.")
            return
        
        # Print issues by severity
        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES ({total_issues}):")
            print("-" * 40)
            for file_path, file_issues in sorted(self.issues.items()):
                if file_issues:
                    print(f"\n📄 {file_path}:")
                    for issue in file_issues:
                        print(f"  ❌ {issue}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({total_warnings}):")
            print("-" * 40)
            for file_path, file_warnings in sorted(self.warnings.items()):
                if file_warnings:
                    print(f"\n📄 {file_path}:")
                    for warning in file_warnings:
                        print(f"  ⚠️  {warning}")
        
        # Print recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 40)
        
        if total_issues > 0:
            print("1. Address critical issues first - these may prevent compilation or cause confusion")
        
        if total_warnings > 0:
            print("2. Review warnings to improve consistency and readability")
        
        print("3. Run this audit regularly to maintain content quality")
        print("4. Consider adding automated checks to your build process")
        
        # Save detailed report
        report_data = {
            'summary': {
                'files_checked': self.stats['files_checked'],
                'total_issues': total_issues,
                'total_warnings': total_warnings,
            },
            'issues': {str(k): v for k, v in self.issues.items()},
            'warnings': {str(k): v for k, v in self.warnings.items()},
        }
        
        with open('content_audit_report.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: content_audit_report.json")

def main():
    auditor = ContentAuditor()
    auditor.audit_all_content()

if __name__ == '__main__':
    main()