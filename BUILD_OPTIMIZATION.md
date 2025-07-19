# Build Optimization Guide

The repository contains 84 notebooks, which can make builds very slow. Here are optimizations to speed up the build process.

## Current Issues

1. **Double Rendering**: Notebooks are rendered twice during GitHub Actions (once for build, once for publish)
2. **No Caching**: Each build re-processes all notebooks from scratch
3. **Unnecessary Files**: Script files and documentation are being processed

## Optimizations Applied

### 1. Freeze Configuration
Changed from `freeze: auto` to `freeze: true` to prevent re-execution:

```yaml
execute:
  freeze: true     # Never re-execute notebooks
  cache: true      # Enable caching
  echo: true       # Show code
  warning: false   # Hide warnings
  error: false     # Hide errors
```

### 2. Render Exclusions
Added more files to exclude from rendering:

```yaml
render:
  - "*.qmd"
  - "notebooks/*.ipynb"
  - "!MIGRATION*.md"
  - "!PROJECT_STRUCTURE.md"
  - "!LATEX_PACKAGES.md"
  - "!NOTEBOOK_FIXES.md"
  - "!*.py"
  - "!*.sh"
```

### 3. Separate Publish Config
Created `_quarto-publish.yml` for optimized GitHub Actions builds.

## Expected Performance Improvements

- **First Build**: ~2 minutes (was 3-4 minutes)
- **Subsequent Builds**: ~30 seconds (only changed files)
- **GitHub Actions**: ~1 minute (with caching)

## Recommendations

### For Development
- Use `quarto preview` for fast local development
- Only run `quarto render` when needed
- Consider using `quarto render --cache-refresh` only when notebook content changes

### For Production
- GitHub Actions should cache the `.quarto/` directory
- Use `freeze: true` to prevent unnecessary re-execution
- Consider splitting large notebooks into smaller ones

### Cache Management
The build cache is stored in `.quarto/_freeze/` and should be:
- ✅ Cached in GitHub Actions
- ✅ Ignored in git (already in .gitignore)
- 🔄 Refreshed only when notebook content changes

## Monitoring Build Performance

Track build times:
- Local builds: Use `time quarto render`
- GitHub Actions: Monitor the workflow duration
- Target: <1 minute for incremental builds

## Advanced Optimizations

If builds are still slow:

1. **Selective Rendering**: Only render changed notebooks
2. **Pre-rendered Notebooks**: Check in rendered outputs
3. **Parallel Processing**: Use multiple workers
4. **Content Splitting**: Break large notebooks into smaller pieces