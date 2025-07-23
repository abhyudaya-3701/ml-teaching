#!/usr/bin/env python3
"""
Generate a markdown report of broken links for GitHub Actions.
"""

import os
import sys
from check_links import LinkChecker

def generate_markdown_report(checker: LinkChecker, summary: dict) -> str:
    """Generate a markdown report of broken links."""
    
    if summary['broken_links'] == 0:
        return """## ✅ All Links Working!

All {total_links} links in {total_files} files are working correctly. Great job! 🎉

""".format(**summary)
    
    report = f"""## 📊 Link Check Results

- 📁 **Files checked**: {summary['total_files']}
- 🔗 **Total links**: {summary['total_links']}
- ❌ **Broken links**: {summary['broken_links']}
- 💔 **Success rate**: {((summary['total_links'] - summary['broken_links']) / summary['total_links'] * 100):.1f}%

### 📋 Broken Links by Type

"""
    
    for link_type, count in summary['broken_by_type'].items():
        report += f"- **{link_type}**: {count} issues\n"
    
    report += "\n### 🔍 Detailed Breakdown\n\n"
    
    current_file = None
    for link in checker.broken_links:
        if link['file'] != current_file:
            current_file = link['file']
            report += f"\n#### 📄 `{current_file}`\n\n"
        
        report += f"- **Line {link['line']}**: `[{link['text']}]({link['url']})` _(Type: {link['type']})_\n"
    
    report += "\n### 💡 Suggested Fixes\n\n"
    
    suggestions = checker.suggest_fixes()
    for link_type, count in summary['broken_by_type'].items():
        if link_type in suggestions:
            report += f"#### {link_type.upper()} ({count} issues)\n\n"
            for suggestion in suggestions[link_type]:
                report += f"{suggestion}\n"
            report += "\n"
    
    return report

def main():
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.getcwd()
    
    checker = LinkChecker(repo_root)
    summary = checker.check_all_links()
    
    report = generate_markdown_report(checker, summary)
    print(report)

if __name__ == "__main__":
    main()