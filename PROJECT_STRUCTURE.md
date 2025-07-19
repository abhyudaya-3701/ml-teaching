# Project Structure

This document describes the organizational structure of the ml-teaching repository.

## Main Categories
- `basics/` - Fundamental concepts
- `maths/` - Mathematical foundations  
- `optimization/` - Optimization algorithms and theory
- `supervised/` - Supervised learning algorithms
- `unsupervised/` - Unsupervised learning algorithms
- `neural-networks/` - Neural network architectures
- `advanced/` - Advanced topics

## Content Organization Pattern

Each main category follows this structure:
```
category/
├── assets/
│   ├── topic-name/
│   │   ├── diagrams/
│   │   ├── figures/
│   │   └── notes/           # Handwritten PDFs and notes
│   └── another-topic/
│       ├── diagrams/
│       ├── figures/
│       └── notes/
└── slides/
    ├── topic-slide.tex
    ├── topic-slide.pdf
    ├── topic-slide.key        # Keynote presentations
    └── topic-slide.pptx       # PowerPoint presentations
```

**Note**: All notebooks are stored flat in the main `/notebooks/` directory, not organized by category.

## Key Points
1. **Slides (.tex files)** go directly in `category/slides/`
2. **Presentation files (.key, .pptx)** go directly in `category/slides/`
3. **Assets (figures, diagrams)** go in `category/assets/topic-name/`
4. **Handwritten notes/PDFs** go in `category/assets/topic-name/notes/`
5. **Notebooks** go in main `/notebooks/` directory (flat structure, not by category)
6. **PDFs** are generated from .tex files and kept with slides

## Examples
- `supervised/slides/decision-trees.tex` - Decision tree slides
- `supervised/assets/decision-trees/figures/` - Decision tree figures
- `optimization/slides/gradient-descent.tex` - Gradient descent slides  
- `optimization/assets/optimization/gradient-descent/` - Gradient descent assets
- `optimization/assets/optimization/gradient-descent/notes/` - Handwritten gradient descent notes
- `maths/slides/kkt-conditions.tex` - Mathematical foundations
- `notebooks/tensor-factorisation.ipynb` - Matrix factorization notebook (flat structure)

## Migration Rules
When moving content:
1. Move .tex files to appropriate `category/slides/`
2. Move supporting assets to `category/assets/topic-name/`
3. Move handwritten notes/PDFs to `category/assets/topic-name/notes/`
4. Move notebooks to main `/notebooks/` directory (flat structure)
5. Keep related content together by topic
6. Follow the existing naming conventions