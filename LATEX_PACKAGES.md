# Required LaTeX Packages

This document lists the LaTeX packages needed for compiling the lecture slides.

## TinyTeX Package Requirements

Install these packages using `tlmgr install <package-name>`:

```bash
# Core packages (usually included with TinyTeX)
tlmgr install beamer
tlmgr install beamertheme-metropolis
tlmgr install pgfplots
tlmgr install tcolorbox
tlmgr install hyperref
tlmgr install graphicx
tlmgr install amsmath
tlmgr install amsfonts
tlmgr install subcaption
tlmgr install makecell
tlmgr install booktabs
tlmgr install multirow
tlmgr install adjustbox
tlmgr install siunitx
tlmgr install forest
tlmgr install tikz
tlmgr install xcolor

# Additional packages needed for ensemble slides
tlmgr install forloop

# If you encounter missing packages during compilation, install them:
# tlmgr install <package-name>
```

## Package Installation Script

You can also run this script to install all required packages:

```bash
#!/bin/bash
# install_latex_packages.sh

packages=(
    "beamer"
    "beamertheme-metropolis" 
    "pgfplots"
    "tcolorbox"
    "hyperref"
    "graphicx"
    "amsmath"
    "amsfonts"
    "subcaption"
    "makecell"
    "booktabs"
    "multirow"
    "adjustbox"
    "siunitx"
    "forest"
    "xcolor"
    "forloop"
)

for package in "${packages[@]}"; do
    echo "Installing $package..."
    tlmgr install "$package"
done

echo "All packages installed!"
```

## Compilation

After installing the packages, compile LaTeX files with:

```bash
pdflatex filename.tex
```

Some files may require multiple runs for proper cross-references:

```bash
pdflatex filename.tex
pdflatex filename.tex  # Second run for references
```