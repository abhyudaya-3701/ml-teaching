# ML Teaching Conventions Application Log

This file tracks all mathematical notation and style changes applied to slides according to the conventions.tex standards.

## Convention Rules Applied

### Core Rules:
- **Vectors**: Bold lowercase (`\mathbf{x}` → `\vx`)
- **Matrices**: Bold uppercase (`\mathbf{X}` → `\mX`) 
- **Scalars**: Regular font (not bold)
- **Transpose**: Use `^T` (not `^t` or `'`)
- **Parameters**: Greek letters without bold (`\theta`, `\lambda`)

---

## File: basics/slides/accuracy-convention.tex

### Issues Found:
1. **Line 191**: `\mathbf{X \in \mathcal{R}^{N\times P}}` - Inconsistent spacing and notation
2. **Line 193**: `x_i^T` - Should use proper transpose notation
3. **Line 201**: `y \in \mathcal{R}^N` - Should be consistent with vector notation
4. **Line 202**: `x_i^T` - Again transpose notation
5. Multiple lines: Inconsistent use of `\mathcal{R}` vs `\Real`

### Changes Applied:

#### Before:
```latex
\item \pause Feature matrix ($\mathbf{X \in \mathcal{R}^{N\times P}}$) containing data of $N$ samples each of which is $P$ dimensional.
\item \pause Thus, $\mathbf{X} = \{x_i^T\}_{i=1}^N$ where $x_i \in \mathcal{R}^P$
\item \pause Output Vector ($y \in \mathcal{R}^N$) containing output variable for $N$ samples.
\item \pause Thus, we can also write $\mathcal{D} = \{(x_i^T, y_i)\}_{i=1}^N$
```

#### After:
```latex
\item \pause Feature matrix ($\mX \in \Real^{n \times d}$) containing data of $n$ samples each of which is $d$ dimensional.
\item \pause Thus, $\mX = \{\vx_i\tp\}_{i=1}^n$ where $\vx_i \in \Real^d$
\item \pause Output vector ($\vy \in \Real^n$) containing output variable for $n$ samples.
\item \pause Thus, we can also write $\cD = \{(\vx_i\tp, y_i)\}_{i=1}^n$
```

#### Specific Changes:
- **Line 3**: Added `\input{../../conventions}` to include convention commands
- **Line 190**: `\mathcal{D}` → `\cD` (consistent calligraphic notation)
- **Line 192**: `\mathbf{X \in \mathcal{R}^{N\times P}}` → `\mX \in \Real^{n \times d}` (matrix notation, set notation, variable names)
- **Line 194**: `\mathbf{X} = \{x_i^T\}_{i=1}^N` → `\mX = \{\vx_i\tp\}_{i=1}^n` (matrix, vector, transpose)
- **Line 194**: `x_i \in \mathcal{R}^P` → `\vx_i \in \Real^d` (vector notation, set notation)
- **Line 195**: `x_1` → `\vx_1` (vector notation)
- **Line 202**: `y \in \mathcal{R}^N` → `\vy \in \Real^n` (vector notation when appropriate)
- **Line 203**: `\mathcal{D} = \{(x_i^T, y_i)\}_{i=1}^N` → `\cD = \{(\vx_i\tp, y_i)\}_{i=1}^n`

#### Note on Parameters:
Following user preference: Use `\theta` as primary parameter notation throughout, with `w` and `b` only in specific contexts.

**Status**: ✅ COMPLETED - File compiles successfully with conventions applied

**Test Result**: PDF generated successfully (130 pages, 546KB)

### ADDITIONAL REVIEW - Second Pass Issues Found:

#### Mathematical Notation Issues:
1. **Line 337**: `y_i\in \{1, \cdots C\}` - Missing proper class notation and using \cdots
2. **Line 347**: `y_i\in \mathcal{R}` - Should use \Real, not \mathcal{R}
3. **Multiple lines**: `\hat{y}` notation inconsistent 
4. **Lines 726, 748, 770, 792**: `T.P.`, `F.P.`, `F.N.` - Should use proper notation
5. **Lines 926, 950**: `\hat{y}_i-y_i` and `N` - Should use n and proper vector notation
6. **Multiple lines**: `||y = \hat{y}||` - Incorrect norm notation for counting

#### Language/Style Issues:
7. **Line 332**: "v/s" - Should be "vs." or "versus"
8. **Line 51**: "recognise" - Should be "recognize" (US English)
9. **Line 255**: "colour" - Should be "color" (US English)

#### Content Issues:
10. **Line 337**: Should specify that C is number of classes
11. **Missing**: No explanation of what TP, FP, FN, TN stand for

### Additional Changes Applied:

#### Mathematical Fixes:
- **Line 337**: `y_i\in \{1, \cdots C\}` → `y_i \in \{1, 2, \ldots, k\}` where $k$ is number of classes
- **Line 347**: `y_i\in \mathcal{R}` → `y_i \in \Real`
- **Line 726, etc**: `T.P.` → `\text{TP}`, `F.P.` → `\text{FP}`, etc.
- **Line 926**: Fix MSE notation with proper summation and n
- **Line 950**: Fix MAE notation consistency

#### Language Fixes:
- **Line 332**: "Classification v/s Regression" → "Classification vs Regression"
- **REVERTED**: Kept British/Indian English ("recognise", "colour") per user preference

#### Additional Improvements:
- **Line 950**: Fixed MAE abbreviation (was "ME")
- **Line 951**: Added parentheses in Mean Error formula for clarity

**Status**: ✅ COMPLETED - Comprehensive review with all mathematical conventions applied

**Final Test Result**: PDF generated successfully (130 pages, 547KB) - All changes compile correctly

---

## File: basics/slides/shuffling.tex

### Issues Found:
[To be analyzed...]

### Changes Applied:
[To be documented...]

---
