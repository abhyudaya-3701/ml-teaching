# Notebook Rendering Fixes

This document summarizes the fixes applied to resolve Quarto notebook rendering issues.

## Issues Fixed

### 1. Missing Image Files
**Problem**: Notebooks referenced image files with incorrect paths, causing "File not found" errors during Quarto rendering.

**Root Cause**: Image paths in notebooks pointed to `../figures/` or `../datasets/` but files were actually in `../shared/figures/` or `../shared/datasets/`.

**Files Fixed**:
- `notebooks/ensemble-feature-importance.ipynb`:
  - Fixed: `../figures/ensemble/feature-imp-0.png` → `../shared/figures/ensemble/feature-imp-0.png`
  - Fixed: `../figures/ensemble/feature-imp-forest.pdf` → `../shared/figures/ensemble/feature-imp-forest.pdf`
  - Fixed: `../diagrams/ensemble/bootstrap_code.png` → `../shared/figures/diagrams/ensemble/bootstrap_code.png`

- `notebooks/confusion-mnist.ipynb`:
  - Fixed: `../figures/mnist-cm.png` → `../shared/figures/mnist-cm.png`

- `notebooks/object-detection.ipynb`:
  - Fixed: `../datasets/images/office.jpg` → `../shared/datasets/images/office.jpg`

- `notebooks/convolution-operation-stride.ipynb`:
  - Fixed: `beach.jpg` → `../neural-networks/assets/cnn/beach.jpg`
  - Fixed: `buildings.jpg` → `../neural-networks/assets/cnn/buildings.jpg`

### 2. Execution vs Rendering Configuration
**Problem**: Notebooks were being executed during rendering instead of just being converted to HTML.

**Solution**: Updated `_quarto.yml` with proper execution settings:
```yaml
execute:
  freeze: auto      # Don't execute if outputs exist
  echo: true        # Show code
  warning: false    # Hide warnings
  error: false      # Hide errors
```

### 3. Notebook-Specific Format Settings
**Enhancement**: Added dedicated notebook formatting in `_quarto.yml`:
```yaml
ipynb:
  code-fold: false  # Show code by default in notebooks
  fig-width: 8      # Better figure sizing
  fig-height: 6
  fig-dpi: 300
```

## Verification Scripts

### 1. Path Fixing Script
Created `fix_notebook_paths.py` to systematically fix image paths across all notebooks.

### 2. Asset Verification Script
Created `verify_notebook_assets.py` to check that all referenced assets exist.

## File Structure

The correct file structure for assets is:
```
ml-teaching/
├── shared/
│   ├── figures/           # Common figures
│   ├── datasets/          # Common datasets
│   └── assets/            # Other shared assets
├── [domain]/assets/       # Domain-specific assets
│   ├── [topic]/
│   └── figures/
└── notebooks/             # All notebooks
    └── *.ipynb
```

## Quarto Rendering

With these fixes:
- ✅ Notebooks are converted to HTML without execution
- ✅ All image references resolve correctly
- ✅ Code is shown by default in notebooks
- ✅ Styling matches the modern theme
- ✅ No missing file errors during build

## Backup Policy

All modified notebooks have `.backup` files created before changes:
- `ensemble-feature-importance.ipynb.backup`
- `confusion-mnist.ipynb.backup`
- `object-detection.ipynb.backup`
- `convolution-operation-stride.ipynb.backup`

## Testing

Run the verification script to ensure all assets are accessible:
```bash
python verify_notebook_assets.py
```

All notebooks should now render successfully with `quarto render` or `quarto publish`.