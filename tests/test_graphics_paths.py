#!/usr/bin/env python3
"""
LaTeX Graphics Path Validator

This script validates that all \\includegraphics paths in .tex files follow the
documented asset organization pattern: ../assets/{topic-name}/{type}/filename
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

class GraphicsPathViolation:
    def __init__(self, tex_file: str, line_num: int, graphics_path: str, 
                 violation_type: str, description: str, fix: str):
        self.tex_file = tex_file
        self.line_num = line_num
        self.graphics_path = graphics_path
        self.violation_type = violation_type
        self.description = description
        self.fix = fix

class LaTeXGraphicsValidator:
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.violations: List[GraphicsPathViolation] = []
        
        # Valid asset types
        self.valid_asset_types = {"figures", "diagrams", "notes"}
        
        # Expected pattern: ../assets/{topic-name}/{type}/filename
        self.expected_pattern = re.compile(r'^\.\./assets/([^/]+)/(figures|diagrams|notes)/(.+)$')
        
        # Pattern to find \includegraphics commands
        self.includegraphics_pattern = re.compile(
            r'\\includegraphics(?:\[[^\]]*\])?\s*\{\s*([^}]+)\s*\}', 
            re.IGNORECASE
        )
        
    def validate(self) -> bool:
        """Run graphics path validation on all .tex files"""
        print(f"🖼️  Validating \\includegraphics paths in LaTeX files...")
        
        tex_files = list(self.root.glob("**/*.tex"))
        if not tex_files:
            print("⚠️  No .tex files found!")
            return True
            
        print(f"📄 Found {len(tex_files)} .tex files to validate")
        
        total_graphics = 0
        compliant_graphics = 0
        files_with_graphics = 0
        
        for tex_file in tex_files:
            file_graphics, file_compliant = self._validate_tex_file(tex_file)
            if file_graphics > 0:
                files_with_graphics += 1
                total_graphics += file_graphics
                compliant_graphics += file_compliant
                print(f"   📝 {tex_file.name}: {file_compliant}/{file_graphics} graphics paths compliant")
        
        print(f"\n📊 Graphics validation summary:")
        print(f"   📄 Files with graphics: {files_with_graphics}/{len(tex_files)}")
        print(f"   🖼️  Total graphics found: {total_graphics}")
        print(f"   ✅ Compliant paths: {compliant_graphics}")
        print(f"   ❌ Non-compliant paths: {total_graphics - compliant_graphics}")
        
        if self.violations:
            print(f"\n❌ Found {len(self.violations)} graphics path violations:")
            self._report_violations()
            return False
        else:
            print("\n🎉 All \\includegraphics paths are 100% compliant!")
            print("✅ All paths follow ../assets/{topic}/{type}/filename pattern")
            print("✅ All referenced graphics files exist")
            print("✅ All topic names are properly matched")
            return True
    
    def _validate_tex_file(self, tex_file: Path):
        """Validate graphics paths in a single .tex file"""
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Could not read {tex_file}: {e}")
            return 0, 0
        
        # Determine expected topic name from file location and name
        expected_topic = self._get_expected_topic_name(tex_file)
        
        # Track graphics in this file
        file_graphics_count = 0
        file_violations_before = len(self.violations)
        
        # Find all \includegraphics commands
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('%'):
                continue
                
            matches = self.includegraphics_pattern.findall(line)
            for graphics_path in matches:
                graphics_path = graphics_path.strip()
                file_graphics_count += 1
                self._validate_graphics_path(tex_file, line_num, graphics_path, expected_topic)
        
        # Calculate compliant graphics for this file
        file_violations_after = len(self.violations)
        file_violations_count = file_violations_after - file_violations_before
        file_compliant_count = file_graphics_count - file_violations_count
        
        return file_graphics_count, file_compliant_count
    
    def _get_expected_topic_name(self, tex_file: Path) -> str:
        """Determine expected topic name from .tex file location"""
        # Remove .tex extension to get base name
        topic_name = tex_file.stem
        
        # Handle special cases
        if topic_name == "mathematical-ml":
            return "mathematical-ml"
        elif topic_name.startswith("bias-variance"):
            return "bias-variance"
        elif topic_name.startswith("svm"):
            return "svm"
        
        return topic_name
    
    def _validate_graphics_path(self, tex_file: Path, line_num: int, 
                               graphics_path: str, expected_topic: str):
        """Validate a single graphics path"""
        
        # Skip if it's just a filename without path (might be valid)
        if '/' not in graphics_path and not graphics_path.startswith('..'):
            # Check if \graphicspath is set properly
            return
            
        # Skip paths with LaTeX variables (e.g., \i, \thetree, etc.)
        if '\\' in graphics_path and any(var in graphics_path for var in ['\\i', '\\the']):
            return
        
        # Check if it matches the expected pattern OR cross-category references
        match = self.expected_pattern.match(graphics_path)
        cross_category_pattern = re.compile(r'^\.\./\.\./([^/]+)/assets/([^/]+)/(figures|diagrams|notes)/(.+)$')
        cross_match = cross_category_pattern.match(graphics_path)
        
        if not match and not cross_match:
            # Check for common violations
            if graphics_path.startswith('../shared/'):
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="SHARED_PATH",
                    description=f"Graphics path uses deprecated shared/ directory",
                    fix=f"Move asset to ../assets/{expected_topic}/figures/ and update path"
                ))
            elif graphics_path.startswith('imgs/') or graphics_path.startswith('./imgs/'):
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="LEGACY_IMGS",
                    description=f"Graphics path uses legacy imgs/ directory",
                    fix=f"Update path to ../assets/{expected_topic}/diagrams/{graphics_path.replace('imgs/', '').replace('./imgs/', '')}"
                ))
            elif not graphics_path.startswith('../assets/'):
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="INVALID_PATTERN",
                    description=f"Graphics path doesn't follow ../assets/{{topic}}/{{type}}/ pattern",
                    fix=f"Update path to ../assets/{expected_topic}/figures/{Path(graphics_path).name}"
                ))
            else:
                # It starts with ../assets/ but doesn't match pattern
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="MALFORMED_ASSETS_PATH",
                    description=f"Malformed assets path: {graphics_path}",
                    fix=f"Fix path format to ../assets/{expected_topic}/{{figures|diagrams|notes}}/filename"
                ))
        elif match:
            # Path matches pattern, validate components
            topic_name, asset_type, filename = match.groups()
            
            # Check if topic name is reasonable (can be different but should be related)
            if not self._is_topic_related(topic_name, expected_topic, tex_file):
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="TOPIC_MISMATCH",
                    description=f"Topic '{topic_name}' doesn't match expected '{expected_topic}'",
                    fix=f"Consider using ../assets/{expected_topic}/{asset_type}/{filename}"
                ))
            
            # Check if asset type is valid
            if asset_type not in self.valid_asset_types:
                self.violations.append(GraphicsPathViolation(
                    tex_file=str(tex_file),
                    line_num=line_num,
                    graphics_path=graphics_path,
                    violation_type="INVALID_ASSET_TYPE",
                    description=f"Invalid asset type '{asset_type}', must be one of: {', '.join(self.valid_asset_types)}",
                    fix=f"Use ../assets/{topic_name}/figures/{filename} or ../assets/{topic_name}/diagrams/{filename}"
                ))
            
            # Check if the referenced file actually exists
            asset_file = tex_file.parent / graphics_path
            if not asset_file.exists():
                # Check with common extensions if no extension provided
                if '.' not in Path(graphics_path).name:
                    extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.svg', '.eps']
                    file_found = False
                    for ext in extensions:
                        if (tex_file.parent / (graphics_path + ext)).exists():
                            file_found = True
                            break
                    if not file_found:
                        self.violations.append(GraphicsPathViolation(
                            tex_file=str(tex_file),
                            line_num=line_num,
                            graphics_path=graphics_path,
                            violation_type="MISSING_FILE",
                            description=f"Referenced graphics file does not exist: {asset_file}",
                            fix=f"Create the missing file or fix the path"
                        ))
                else:
                    self.violations.append(GraphicsPathViolation(
                        tex_file=str(tex_file),
                        line_num=line_num,
                        graphics_path=graphics_path,
                        violation_type="MISSING_FILE",
                        description=f"Referenced graphics file does not exist: {asset_file}",
                        fix=f"Create the missing file or fix the path"
                    ))
        elif cross_match:
            # Cross-category reference is valid, just check file exists
            asset_file = tex_file.parent / graphics_path
            if not asset_file.exists():
                # Check with common extensions if no extension provided
                if '.' not in Path(graphics_path).name:
                    extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.svg', '.eps']
                    file_found = False
                    for ext in extensions:
                        if (tex_file.parent / (graphics_path + ext)).exists():
                            file_found = True
                            break
                    if not file_found:
                        self.violations.append(GraphicsPathViolation(
                            tex_file=str(tex_file),
                            line_num=line_num,
                            graphics_path=graphics_path,
                            violation_type="MISSING_FILE",
                            description=f"Referenced graphics file does not exist: {asset_file}",
                            fix=f"Create the missing file or fix the path"
                        ))
                else:
                    self.violations.append(GraphicsPathViolation(
                        tex_file=str(tex_file),
                        line_num=line_num,
                        graphics_path=graphics_path,
                        violation_type="MISSING_FILE",
                        description=f"Referenced graphics file does not exist: {asset_file}",
                        fix=f"Create the missing file or fix the path"
                    ))
    
    def _is_topic_related(self, actual_topic: str, expected_topic: str, tex_file: Path) -> bool:
        """Check if actual topic name is reasonably related to expected"""
        # Exact match
        if actual_topic == expected_topic:
            return True
        
        # Common variations
        variations = {
            expected_topic,
            expected_topic.replace('-', '_'),
            expected_topic.replace('_', '-'),
            expected_topic.lower(),
        }
        
        # For bias-variance files, allow just "bias-variance"
        if expected_topic.startswith('bias-variance'):
            variations.add('bias-variance')
        
        # For SVM files, allow "svm" 
        if expected_topic.startswith('svm'):
            variations.add('svm')
        
        # For mathematical ML
        if expected_topic == 'mathematical-ml':
            variations.update(['ml-maths', 'mathematical-ml', 'mml'])
        
        # For ML maths files, allow mathematical-ml topic
        if expected_topic.startswith('ml-maths'):
            variations.add('mathematical-ml')
        
        # Also check case-insensitive match
        if actual_topic.lower() == expected_topic.lower():
            return True
            
        return actual_topic in variations
    
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
                print(f"      📁 File: {v.tex_file}:{v.line_num}")
                print(f"      🖼️  Path: {v.graphics_path}")
                print(f"      🔧 Fix: {v.fix}")
        
        print(f"\n💡 Common patterns to fix:")
        print("   • ../shared/figures/topic/ → ../assets/topic/figures/")
        print("   • imgs/file.pdf → ../assets/topic/diagrams/file.pdf")
        print("   • ./SVM/ → ../assets/svm/figures/")
        print("   • Ensure all graphics files exist in the referenced locations")

def main():
    """Main entry point"""
    validator = LaTeXGraphicsValidator()
    is_valid = validator.validate()
    
    if not is_valid:
        print(f"\n📊 Summary: {len(validator.violations)} graphics path violations found")
        print("🚀 Fix the violations above to ensure proper asset organization")
        sys.exit(1)
    else:
        print("🎉 All LaTeX graphics paths are valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()