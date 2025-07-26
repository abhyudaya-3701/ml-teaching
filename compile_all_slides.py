#!/usr/bin/env python3
"""Compile all LaTeX slide files to PDFs."""

import os
import subprocess
import glob
from pathlib import Path

def compile_tex_to_pdf(tex_file):
    """Compile a single .tex file to PDF using pdflatex."""
    directory = os.path.dirname(tex_file)
    filename = os.path.basename(tex_file)
    
    print(f"Compiling: {tex_file}")
    
    try:
        # Change to the directory containing the .tex file
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", filename],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout per file
        )
        
        if result.returncode == 0:
            print(f"✅ Success: {tex_file}")
            return True
        else:
            print(f"❌ Failed: {tex_file}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {tex_file}")
        return False
    except Exception as e:
        print(f"💥 Exception: {tex_file} - {str(e)}")
        return False

def main():
    """Find and compile all LaTeX slide files."""
    # Find all .tex files in */slides/ directories
    slide_files = []
    for root, dirs, files in os.walk('.'):
        if 'slides' in root and 'build' not in root and '.git' not in root:
            for file in files:
                if file.endswith('.tex'):
                    slide_files.append(os.path.join(root, file))
    
    slide_files.sort()
    
    print(f"Found {len(slide_files)} slide files to compile:")
    for f in slide_files:
        print(f"  {f}")
    
    print("\n" + "="*60)
    print("Starting compilation...")
    print("="*60)
    
    successful = 0
    failed = 0
    
    for tex_file in slide_files:
        if compile_tex_to_pdf(tex_file):
            successful += 1
        else:
            failed += 1
        print()  # Empty line for readability
    
    print("="*60)
    print(f"Compilation complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(slide_files)}")
    print("="*60)
    
    if failed > 0:
        print("\nNote: Some files failed to compile. This is normal for files with")
        print("missing figures or dependencies. The important slides should work.")

if __name__ == "__main__":
    main()