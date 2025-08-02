# ML Teaching Repository - Claude Assistant Guide

## Repository Overview
This is a comprehensive machine learning teaching materials repository containing LaTeX/Beamer slides, PDFs, and build systems for ML course content.

## Structure
```
ml-teaching/
├── basics/           # Fundamental ML concepts
├── maths/           # Mathematical foundations  
├── supervised/      # Supervised learning algorithms
├── neural-networks/ # Deep learning and neural networks
├── optimization/    # Optimization techniques
├── advanced/        # Advanced ML topics
├── unsupervised/    # Unsupervised learning
├── shared/         # Common styles, themes, and utilities
└── rebuild_all.sh  # Master build script
```

## Key Components

### Build System
- **rebuild_all.sh**: Master script that builds all PDFs across all topics
- **Makefiles**: Each topic has a Makefile with targets:
  - `make` or `make all`: Build all PDFs in the topic
  - `make clean`: Remove auxiliary files
  - `make distclean`: Remove PDFs with corresponding .tex files (preserves assets)
- **XeLaTeX**: All slides use XeLaTeX for compilation

### Styling System
- **shared/styles/**: Centralized styling system
  - `custom.sty`: Main style package
  - `theme-nipun.sty`: Primary theme
  - `common-boxes.sty`: Beautiful colorboxes (Definition, Example, Key Points, Pop Quiz, etc.)
  - `conventions.sty`: Mathematical notation and conventions
- **Colorboxes**: Professional tcolorbox-based containers with:
  - Clean design with proper colors (blue, orange, purple, red, green)
  - 1.2pt borders, 3pt accent lines, 8pt padding
  - Pop quiz boxes with attached titles and numbering

### Pop Quiz System
- Counter: `\newcounter{popquiz}` defined in each file
- Usage: `\stepcounter{popquiz}` before frame, then `\thepopquiz` in title and box
- Structure: Question frame + separate answer frame
- No `\pause` in quiz options - show all options immediately

## Common Tasks

### Building
- Single topic: `cd topic/slides && make`
- All topics: `./rebuild_all.sh` (from root)
- Clean: `make distclean` (preserves asset PDFs)

### Adding Content
- New slides: Create .tex files in appropriate topic/slides/
- Assets: Store in topic/assets/ (won't be deleted by distclean)
- Figures: Use topic/slides/ for generated figures

### Styling
- Use existing colorboxes: `\begin{definitionbox}{title}`, `\begin{examplebox}{title}`, etc.
- Pop quizzes: Follow the established pattern with separate answer frames
- Mathematical notation: Defined in conventions.sty

## Important Notes
- **Never delete asset PDFs**: distclean only removes PDFs with corresponding .tex files
- **Counter protection**: Pop quiz counters are protected from \pause interference
- **Consistent styling**: All boxes use the same professional design language
- **XeLaTeX required**: TinyTeX with XeLaTeX engine for font support

## Recent Improvements
- Fixed rebuild_all.sh to not delete asset PDFs
- Restored amazing colorbox styling with professional appearance
- Fixed pop quiz counter issues with \pause commands
- Separated quiz questions and answers into different frames
- Maintained 100% build success rate across all topics

## Git Integration
- All PDFs are tracked in git
- Missing PDFs are restored from assets/ directories when needed
- Commit messages follow pattern: "TOPIC: Brief description"