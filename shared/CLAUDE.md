# Shared Styles and Utilities

## Overview
Centralized styling system for all ML teaching materials, providing consistent themes, colorboxes, and mathematical notation.

## Key Files

### Core Styling
- `custom.sty`: Main style package that loads theme and utilities
- `theme-nipun.sty`: Primary theme with colors, fonts, and layout
- `common-boxes.sty`: Professional tcolorbox definitions
- `conventions.sty`: Mathematical notation and ML-specific symbols

### Available Colorboxes
All boxes use professional styling with proper colors, borders, and typography:

```latex
\begin{definitionbox}{Title}        % Blue boxes for definitions
\begin{examplebox}{Title}           % Orange boxes for examples  
\begin{keypointsbox}                % Purple boxes for key points
\begin{popquizbox}{Number}          % Blue quiz boxes with attached titles
\begin{alertbox}{Title}             % Red boxes for important notes
\begin{theorembox}{Title}           % Green boxes for theorems
\begin{codebox}{Title}              % Gray boxes for code
```

### Colorbox Features
- **Professional Design**: Clean, academic appearance
- **Consistent Styling**: 1.2pt borders, 3pt accent lines, 8pt padding
- **Beautiful Colors**: Blue, orange, purple, red, green palette
- **Enhanced Typography**: Bold titles, proper spacing
- **Pop Quiz Boxes**: Special attached title design with numbering

### Pop Quiz System
- Counter-based numbering: `\newcounter{popquiz}`
- Protected from `\pause` interference
- Usage pattern:
  ```latex
  \stepcounter{popquiz}
  \begin{frame}{Pop Quiz \#\thepopquiz}
  \begin{popquizbox}{\thepopquiz}
  Question...
  \end{popquizbox}
  \end{frame}
  ```

## Theme System
The theme system supports multiple themes (switch by commenting/uncommenting in custom.sty):
- `theme-nipun`: Active theme - clean, modern, academic
- `theme-sky`: Light blue elegance  
- `theme-modern`: Clean whites and grays
- `theme-elegant`: Navy/gold palette
- Other themes available but nipun is primary

## Usage
Include in any LaTeX document:
```latex
\usepackage{../../shared/styles/custom}
\usepackage{../../shared/styles/conventions}  % For math notation
```

## Recent Improvements
- Restored amazing colorbox styling from earlier successful version
- Fixed tcolorbox compatibility issues
- Removed FontAwesome dependencies for simplicity
- Enhanced pop quiz box design with attached titles
- Standardized all boxes to consistent professional appearance

## Technical Notes
- Uses tcolorbox with skins,breakable libraries
- XeLaTeX compatible
- Path resolution supports multiple directory levels
- Centralized to avoid code duplication across topics