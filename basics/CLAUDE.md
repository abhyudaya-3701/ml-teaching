# Basics - ML Fundamentals

## Content Overview
This folder contains fundamental machine learning concepts and introductory materials.

## Key Slides
- `accuracy-convention.tex`: Conventions, accuracy metrics, classification vs regression
- `1-introduction-ml.pdf`: Introduction to machine learning (asset file - do not delete)
- `shuffling.pdf`: Data shuffling concepts
- `misc.pdf`: Miscellaneous fundamental concepts

## Features in accuracy-convention.tex
- **Professional Colorboxes**: Definition, Example, Key Points boxes with amazing styling
- **Pop Quiz System**: 5 interactive quizzes with separate answer frames
- **Mathematical Notation**: Proper ML conventions and notation
- **Comprehensive Coverage**: 
  - ML definitions and concepts
  - Classification vs regression
  - Accuracy metrics (precision, recall, F1-score)
  - Confusion matrices
  - Regression metrics (MSE, MAE, R²)

## Pop Quiz Structure
Each quiz follows this pattern:
```latex
\stepcounter{popquiz}
\begin{frame}{Pop Quiz \#\thepopquiz}
\begin{popquizbox}{\thepopquiz}
Question text with options...
\end{popquizbox}
\end{frame}

\begin{frame}{Pop Quiz \#\thepopquiz{} - Answer}
\textbf{Answer:} Explanation...
\end{frame}
```

## Building
- `make` or `make all`: Build all PDFs
- `make clean`: Remove auxiliary files
- `make distclean`: Remove generated PDFs (preserves asset PDFs)

## Dependencies
- XeLaTeX engine
- Custom styling system from ../shared/styles/
- tcolorbox for beautiful boxes
- Standard math packages (amsmath, amssymb, etc.)