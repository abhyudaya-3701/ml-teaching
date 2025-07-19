# Repository Restructuring Plan

## Issues Found

### 1. PROJECT_STRUCTURE.md Errors (FIXED)
- Line 52: `maths/slides/kkt-conditions/kkt-conditions.tex` → Fixed to `maths/slides/kkt-conditions.tex`

### 2. Current Structure Violations

#### maths/ folder
- **VIOLATION**: `maths/slides/kkt-conditions/kkt-conditions.tex` (should be `maths/slides/kkt-conditions.tex`)
- **VIOLATION**: `maths/slides/ml-maths/` folder with nested files (should be `maths/slides/ml-maths.tex`)

#### optimization/ folder  
- **VIOLATION**: `optimization/slides/convexity/convexity.tex` (should be `optimization/slides/convexity.tex`)

#### shared/ folder misuse
- **VIOLATION**: `shared/figures/logistic-regression/` → should be `supervised/assets/logistic-regression/figures/`
- **VIOLATION**: `shared/figures/linear-regression/` → should be `supervised/assets/linear-regression/figures/`
- **VIOLATION**: `shared/figures/ensemble/` → should be `supervised/assets/ensemble/figures/`
- **VIOLATION**: `shared/figures/decision-trees/` → should be `supervised/assets/decision-trees/figures/`

#### unsupervised/ folder issues
- **ISSUE**: Has `unsupervised/assets/clustering/` but no `clustering.tex` slide file
- **ISSUE**: Only has `unsupervised.tex` - should be broken into subtopics (clustering, pca, etc.)

#### advanced/ folder
- **ISSUE**: Has `advanced/assets/matrix-factorization/` but matrix factorization slides/content not properly organized

## Restructuring Tasks

### Phase 1: Fix Slide Structure Violations

#### maths/ folder fixes
```bash
# Move kkt-conditions slides to correct location
mv maths/slides/kkt-conditions/kkt-conditions.tex maths/slides/kkt-conditions.tex
mv maths/slides/kkt-conditions/imgs/ maths/assets/kkt-conditions/diagrams/

# Move ml-maths slides to correct location  
mv maths/slides/ml-maths/ maths/assets/mathematical-ml/legacy/
# Create proper maths slides from existing content
```

#### optimization/ folder fixes
```bash
# Move convexity slides to correct location
mv optimization/slides/convexity/convexity.tex optimization/slides/convexity.tex
mv optimization/slides/convexity/imgs/ optimization/assets/convexity/diagrams/
```

### Phase 2: Move shared/ figures to proper locations

#### supervised/ assets reorganization
```bash
# Move logistic regression figures
mv shared/figures/logistic-regression/ supervised/assets/logistic-regression/figures/

# Move linear regression figures  
mv shared/figures/linear-regression/ supervised/assets/linear-regression/figures/

# Move ensemble figures
mv shared/figures/ensemble/ supervised/assets/ensemble/figures/

# Move decision trees figures
mv shared/figures/decision-trees/ supervised/assets/decision-trees/figures/
```

### Phase 3: Fix unsupervised/ structure

Break `unsupervised.tex` into proper subtopics:
- `unsupervised/slides/clustering.tex`
- `unsupervised/slides/pca.tex` 
- `unsupervised/slides/kmeans.tex`

Move assets accordingly:
- `unsupervised/assets/clustering/` (already exists)
- Create `unsupervised/assets/pca/`

### Phase 4: Clean up shared/ folder

After moving topic-specific figures, shared/ should only contain:
- `shared/datasets/` (global datasets)
- `shared/styles/` (LaTeX styles)
- `shared/notation/` (notation files)
- Generic cross-topic diagrams if any

### Phase 5: Update notebook references

Update notebook image paths after moving figures:
- Change `../shared/figures/ensemble/` → `../supervised/assets/ensemble/figures/`
- Change `../shared/figures/decision-trees/` → `../supervised/assets/decision-trees/figures/`
- etc.

### Phase 6: Update LaTeX \graphicspath commands

Update all .tex files to point to new asset locations:
```latex
% Old
\graphicspath{ {../shared/figures/ensemble/} }

% New  
\graphicspath{ {../assets/ensemble/figures/} }
```

## Expected Final Structure

```
maths/
├── slides/
│   ├── kkt-conditions.tex          # Fixed: was in subdirectory
│   ├── ml-maths.tex               # Fixed: consolidated from subdirectory
│   └── mvn.tex
└── assets/
    ├── kkt-conditions/
    │   └── diagrams/               # Moved from slides/kkt-conditions/imgs/
    └── mathematical-ml/
        └── figures/

optimization/
├── slides/
│   ├── convexity.tex              # Fixed: was in subdirectory
│   ├── gradient-descent.tex
│   └── coordinate-descent.tex
└── assets/
    ├── convexity/
    │   └── diagrams/               # Moved from slides/convexity/imgs/
    └── subgradient/
        └── figures/

supervised/
├── slides/
│   ├── decision-trees.tex
│   ├── ensemble.tex
│   ├── linear-regression.tex
│   └── logistic-regression.tex
└── assets/
    ├── decision-trees/
    │   ├── figures/                # Moved from shared/figures/
    │   └── diagrams/
    ├── ensemble/
    │   └── figures/                # Moved from shared/figures/
    ├── linear-regression/
    │   └── figures/                # Moved from shared/figures/
    └── logistic-regression/
        └── figures/                # Moved from shared/figures/

unsupervised/
├── slides/
│   ├── clustering.tex             # New: split from unsupervised.tex
│   ├── pca.tex                    # New: split from unsupervised.tex
│   └── kmeans.tex                 # New: split from unsupervised.tex
└── assets/
    ├── clustering/                # Already exists
    └── pca/                       # New

shared/                            # Cleaned up
├── datasets/                      # Global datasets only
├── styles/                        # LaTeX styles
└── notation/                      # Notation files
```

## Benefits

1. **Consistent Structure**: All categories follow the same pattern
2. **Easy Navigation**: Assets are co-located with their slides
3. **Clear Ownership**: Each topic owns its assets
4. **Simplified shared/**: Only truly shared resources remain
5. **Maintainable**: Easy to find and update related content

## Implementation Order

1. Fix PROJECT_STRUCTURE.md guide (✅ DONE)
2. Move slides out of subdirectories (maths, optimization)
3. Move shared figures to appropriate category assets
4. Split unsupervised.tex into subtopics
5. Update all \graphicspath references
6. Update notebook image paths
7. Clean up empty directories
8. Test builds

This restructuring will make the repository much more organized and easier to maintain while following the documented structure consistently.