# Mathematical Foundations

## Content Overview
Mathematical prerequisites and foundations for machine learning, including optimization, linear algebra, and constrained optimization.

## Key Topics
- `mathematical-ml.tex`: Core mathematical foundations (successfully compiles to 45 pages)  
- `constrained-1.pdf`: Constrained optimization part 1
- `constrained-2.pdf`: Constrained optimization part 2
- `find-widths.pdf`: Width finding algorithms
- `kkt-conditions.pdf`: Karush-Kuhn-Tucker conditions

## Recent Fixes
- **mathematical-ml.tex**: Fixed include path from `../../../shared/styles/custom` to `../../shared/styles/custom`
- **Build Success**: Now compiles successfully to 45-page PDF (89KB)
- **Path Resolution**: Corrected relative path issues for shared styling

## Content Structure
The mathematical foundations slides cover:
- Linear algebra essentials
- Calculus and optimization
- Probability and statistics basics
- Mathematical notation conventions
- Geometric interpretations

## Build System
- Standard Makefile with XeLaTeX compilation
- Fixed include paths for shared styling system
- Integrated with root rebuild system
- Preserves generated mathematical figures

## Dependencies
- Heavy use of mathematical packages (amsmath, amssymb, mathtools)
- Custom mathematical notation from shared/styles/conventions.sty
- XeLaTeX for proper mathematical font rendering
- TikZ for mathematical diagrams and illustrations

## Usage Notes
- This folder provides the mathematical foundation for all other topics
- Mathematical notation defined here is used consistently across all slides
- Contains essential prerequisites that students should understand before diving into algorithms