# Machine Learning Course Materials

A comprehensive collection of lecture slides, interactive notebooks, and educational resources for machine learning. These materials have been developed over several years by Prof. Nipun Batra and teaching assistants at IIT Gandhinagar.

## Course Structure

- **[Slides](https://nipunbatra.github.io/ml-teaching/slides)** - LaTeX/Beamer presentations organized by topic
- **[Notebooks](https://nipunbatra.github.io/ml-teaching/notebooks)** - Interactive Jupyter notebooks with hands-on examples
- **[Course Website](https://nipunbatra.github.io/ml-teaching/)** - Complete online resource

## Topics Covered

- **Basics & Foundations** - Introduction, metrics, data handling
- **Mathematical Foundations** - Linear algebra, optimization, probability
- **Supervised Learning** - Regression, classification, model evaluation
- **Neural Networks** - Deep learning fundamentals and architectures
- **Advanced Topics** - Time series, reinforcement learning, modern techniques

## Getting Started

1. **Browse Materials**: Visit the [course website](https://nipunbatra.github.io/ml-teaching/)
2. **Run Notebooks**: Open any notebook in Google Colab or locally
3. **Build Slides**: Use `make` in any category folder to compile LaTeX slides

## For Instructors

Each topic is self-contained with slides, figures, and supporting materials. The modular structure allows flexible course design and easy customization.

## Directory Structure

The repository is organized with a clean, modular structure that separates content by topic and purpose:

### Organization Principles
- **Topic-based folders**: Each ML area has its own directory (supervised, neural-networks, etc.)
- **Consistent structure**: Each topic contains slides/, assets/, tutorials/, and Makefile
- **Clean root**: Only essential project files in the main directory
- **Organized utilities**: Scripts and documentation in dedicated folders
- **Self-contained**: Each topic can be built and used independently

```
ml-teaching/
├── _quarto.yml                 # Main website configuration
├── index.qmd                   # Homepage
├── acknowledgments.qmd         # Teaching assistants acknowledgments
├── courses.qmd                 # Course information and links
├── slides.qmd                  # Slides navigation page
├── tutorials.qmd               # Tutorials navigation page
├── notebooks.qmd               # Notebooks navigation page
├── assignments.qmd             # Assignments page
├── Makefile                    # Build automation for slides
├── README.md                   # This file
│
├── styles/                     # Website styling
│   ├── styles.scss             # Main light theme
│   ├── styles-dark.scss        # Dark theme
│   ├── custom.scss             # Custom styles
│   └── custom-dark.scss        # Custom dark styles
│
├── docs/                       # Project documentation
│   ├── BUILD_OPTIMIZATION.md   # Build system notes
│   ├── COMPILATION_ISSUES.md   # LaTeX compilation help
│   ├── CONTENT_AUDIT_SUMMARY.md # Quality assurance reports
│   └── ...                     # Other documentation files
│
├── scripts/                    # Automation and utility scripts
│   ├── audit_content.py        # Content quality checker
│   ├── add_notebook_metadata.py # Notebook enhancement tool
│   ├── check_links.py          # Link validation
│   └── ...                     # Other utility scripts
│
├── images/                     # Website assets
│   └── logo.svg                # Site logo
│
├── shared/                     # Common resources
│   ├── styles/                 # LaTeX style files (.sty)
│   ├── datasets/               # Sample datasets
│   └── figures/                # Shared figures and diagrams
│
├── basics/                     # Foundational ML concepts
│   ├── slides/                 # LaTeX slide sources (.tex)
│   ├── assets/                 # Figures and images
│   ├── tutorials/              # Written tutorials (.tex)
│   └── Makefile               # Build automation
│
├── maths/                      # Mathematical foundations
│   ├── slides/                 # Optimization, linear algebra
│   ├── assets/                 # Mathematical figures
│   └── Makefile               # Build automation
│
├── supervised/                 # Supervised learning
│   ├── slides/                 # Regression, classification, SVM
│   ├── assets/                 # Topic-specific figures
│   ├── tutorials/              # Written explanations
│   └── Makefile               # Build automation
│
├── neural-networks/            # Deep learning
│   ├── slides/                 # Neural networks, CNNs
│   ├── assets/                 # Network diagrams
│   ├── tutorials/              # Implementation guides
│   └── Makefile               # Build automation
│
├── optimization/               # Optimization methods
│   ├── slides/                 # Gradient descent, coordinate descent
│   ├── assets/                 # Optimization visualizations
│   ├── tutorials/              # Mathematical derivations
│   └── Makefile               # Build automation
│
├── unsupervised/              # Unsupervised learning
│   ├── slides/                 # Clustering, dimensionality reduction
│   ├── assets/                 # Algorithm visualizations
│   ├── tutorials/              # Implementation details
│   └── Makefile               # Build automation
│
├── advanced/                   # Advanced topics
│   ├── slides/                 # Time series, reinforcement learning
│   ├── assets/                 # Specialized figures
│   └── Makefile               # Build automation
│
├── notebooks/                  # Interactive Jupyter notebooks
│   ├── linear-regression.ipynb # Hands-on implementations
│   ├── gradient-descent.ipynb  # Algorithm demonstrations
│   ├── cnn.ipynb              # Deep learning examples
│   └── ...                    # 80+ educational notebooks
│
├── tests/                      # Quality assurance
│   ├── test_graphics_paths.py  # Figure path validation
│   ├── test_notebook_paths.py  # Notebook link checking
│   └── ...                    # Other validation tests
│
└── build-temp/                # Temporary build files
    ├── *.log                   # Compilation logs
    ├── *.aux                   # LaTeX auxiliary files
    └── ...                    # Other build artifacts
```

## Building from Source

```bash
# Build all slides
make

# Build specific category
cd supervised && make

# Preview website locally
quarto preview

# Run content quality checks
python scripts/audit_content.py

# Check all notebook links
python scripts/check_links.py
```

## Contributing

Found an issue or have suggestions for improvement? 

**Report Issues**: [Create a GitHub issue](https://github.com/nipunbatra/ml-teaching/issues/new/choose) to report bugs, suggest content improvements, or request new features.

## License

Educational materials developed for academic use at IIT Gandhinagar.