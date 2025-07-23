#!/usr/bin/env python3
"""
Comprehensive link checker for ml-teaching repository.
Checks all links in .qmd files and validates they point to existing files.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set

class LinkChecker:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.broken_links: List[Dict] = []
        self.total_links = 0
        
    def find_qmd_files(self) -> List[Path]:
        """Find all .qmd files in the repository."""
        return list(self.repo_root.glob("**/*.qmd"))
    
    def extract_links_from_qmd(self, file_path: Path) -> List[Tuple[str, str, int]]:
        """Extract markdown links from a .qmd file."""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Match markdown links [text](url)
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.finditer(link_pattern, content)
            
            for match in matches:
                text = match.group(1)
                url = match.group(2)
                line_number = content[:match.start()].count('\n') + 1
                links.append((text, url, line_number))
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
        return links
    
    def is_external_url(self, url: str) -> bool:
        """Check if URL is external (http/https)."""
        return url.startswith(('http://', 'https://'))
    
    def check_file_exists(self, url: str, qmd_file: Path) -> bool:
        """Check if a relative file path exists."""
        if self.is_external_url(url):
            return True  # Don't check external URLs for now
        
        # Handle anchor links
        if '#' in url:
            url = url.split('#')[0]
        
        if not url:  # Empty after removing anchor
            return True
            
        # Resolve relative path
        if url.startswith('/'):
            # Absolute path from repo root
            file_path = self.repo_root / url.lstrip('/')
        else:
            # Relative to the .qmd file
            file_path = qmd_file.parent / url
        
        return file_path.exists()
    
    def check_links_in_file(self, qmd_file: Path) -> List[Dict]:
        """Check all links in a single .qmd file."""
        broken_links = []
        links = self.extract_links_from_qmd(qmd_file)
        
        for text, url, line_number in links:
            self.total_links += 1
            
            if not self.check_file_exists(url, qmd_file):
                broken_link = {
                    'file': str(qmd_file.relative_to(self.repo_root)),
                    'line': line_number,
                    'text': text,
                    'url': url,
                    'type': self.categorize_broken_link(url)
                }
                broken_links.append(broken_link)
                
        return broken_links
    
    def categorize_broken_link(self, url: str) -> str:
        """Categorize the type of broken link."""
        if url.endswith('.html'):
            return 'missing_html'
        elif url.endswith('.pdf'):
            return 'missing_pdf'
        elif url.endswith('.ipynb'):
            return 'missing_notebook'
        elif any(url.endswith(ext) for ext in ['.tex', '.py', '.md']):
            return 'missing_source'
        else:
            return 'other'
    
    def check_all_links(self) -> Dict:
        """Check links in all .qmd files."""
        qmd_files = self.find_qmd_files()
        all_broken_links = []
        
        print(f"🔍 Checking links in {len(qmd_files)} .qmd files...")
        
        for qmd_file in qmd_files:
            print(f"  Checking {qmd_file.name}...")
            broken_links = self.check_links_in_file(qmd_file)
            all_broken_links.extend(broken_links)
        
        self.broken_links = all_broken_links
        
        return {
            'total_files': len(qmd_files),
            'total_links': self.total_links,
            'broken_links': len(all_broken_links),
            'broken_by_type': self.get_broken_by_type()
        }
    
    def get_broken_by_type(self) -> Dict[str, int]:
        """Get count of broken links by type."""
        type_counts = {}
        for link in self.broken_links:
            link_type = link['type']
            type_counts[link_type] = type_counts.get(link_type, 0) + 1
        return type_counts
    
    def suggest_fixes(self) -> Dict[str, List[str]]:
        """Suggest fixes for broken links."""
        suggestions = {
            'missing_html': [
                "• Convert .ipynb notebooks to .html using nbconvert",
                "• Set up GitHub Actions to auto-convert notebooks",
                "• Link directly to .ipynb files instead of .html"
            ],
            'missing_pdf': [
                "• Compile .tex files to .pdf using pdflatex",
                "• Add GitHub Actions to auto-compile LaTeX",
                "• Check if PDF exists in different location"
            ],
            'missing_notebook': [
                "• Verify notebook exists in /notebooks/ directory",
                "• Check for typos in filename",
                "• Ensure notebook was committed to repository"
            ]
        }
        return suggestions
    
    def print_report(self, summary: Dict):
        """Print a comprehensive report."""
        print("\n" + "="*60)
        print("📊 LINK CHECK REPORT")
        print("="*60)
        
        print(f"📁 Files checked: {summary['total_files']}")
        print(f"🔗 Total links: {summary['total_links']}")
        print(f"❌ Broken links: {summary['broken_links']}")
        
        if summary['broken_links'] == 0:
            print("✅ All links are working! 🎉")
            return
        
        print(f"💔 Success rate: {((summary['total_links'] - summary['broken_links']) / summary['total_links'] * 100):.1f}%")
        
        print("\n📋 BROKEN LINKS BY TYPE:")
        for link_type, count in summary['broken_by_type'].items():
            print(f"  {link_type}: {count}")
        
        print("\n🔍 DETAILED BREAKDOWN:")
        current_file = None
        for link in self.broken_links:
            if link['file'] != current_file:
                current_file = link['file']
                print(f"\n📄 {current_file}:")
            
            print(f"  Line {link['line']:3d}: [{link['text']}]({link['url']})")
            print(f"             Type: {link['type']}")
        
        print("\n💡 SUGGESTED FIXES:")
        suggestions = self.suggest_fixes()
        for link_type, count in summary['broken_by_type'].items():
            if link_type in suggestions:
                print(f"\n{link_type.upper()} ({count} issues):")
                for suggestion in suggestions[link_type]:
                    print(f"  {suggestion}")

def main():
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.getcwd()
    
    checker = LinkChecker(repo_root)
    summary = checker.check_all_links()
    checker.print_report(summary)
    
    # Exit with non-zero code if there are broken links
    if summary['broken_links'] > 0:
        print(f"\n❌ Found {summary['broken_links']} broken links!")
        sys.exit(1)
    else:
        print("\n✅ All links are working!")
        sys.exit(0)

if __name__ == "__main__":
    main()