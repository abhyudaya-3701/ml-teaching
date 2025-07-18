# LaTeX Package Dependencies

This document lists all the LaTeX packages required for building the ML teaching materials using the unified `custom.sty`.

## Required Packages

The following packages are needed for the unified `custom.sty` to work properly:

### Core LaTeX Packages
```bash
tlmgr install latex-bin
tlmgr install amsmath
tlmgr install amssymb
tlmgr install amsfonts
tlmgr install amsthm
```

### Graphics and Visualization
```bash
tlmgr install graphicx
tlmgr install xcolor
tlmgr install tikz
tlmgr install pgf
tlmgr install pgfplots
```

### Typography and Formatting
```bash
tlmgr install bm
tlmgr install mathtools
tlmgr install siunitx
tlmgr install xspace
```

### Tables and Layout
```bash
tlmgr install booktabs
tlmgr install multirow
tlmgr install makecell
tlmgr install adjustbox
tlmgr install array
tlmgr install colortbl
```

### Boxes and Styling
```bash
tlmgr install tcolorbox
tlmgr install caption
tlmgr install subcaption
```

### References and Links
```bash
tlmgr install hyperref
tlmgr install url
```

### Beamer and Presentation
```bash
tlmgr install beamer
tlmgr install beamertheme-metropolis
```

### Specialized Packages
```bash
tlmgr install pdfpages
tlmgr install forloop
tlmgr install calc
tlmgr install forest
tlmgr install calculator
```

## Complete Installation Script

You can install all required packages at once using:

```bash
#!/bin/bash
# install_latex_packages.sh
# Install all required LaTeX packages for ML teaching materials

echo "Installing LaTeX packages for ML teaching materials..."

# Core packages
tlmgr install latex-bin amsmath amssymb amsfonts amsthm

# Graphics and visualization
tlmgr install graphicx xcolor tikz pgf pgfplots

# Typography and formatting
tlmgr install bm mathtools siunitx xspace

# Tables and layout
tlmgr install booktabs multirow makecell adjustbox array colortbl

# Boxes and styling
tlmgr install tcolorbox caption subcaption

# References and links
tlmgr install hyperref url

# Beamer and presentation
tlmgr install beamer beamertheme-metropolis

# Specialized packages
tlmgr install pdfpages forloop calc forest calculator

echo "All LaTeX packages installed successfully!"
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