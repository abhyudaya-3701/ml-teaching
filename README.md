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

## Building from Source

```bash
# Build all slides
make

# Build specific category
cd supervised && make

# Preview website locally
quarto preview
```

## Contributing

Found an issue or have suggestions for improvement? 

**Report Issues**: [Create a GitHub issue](https://github.com/nipunbatra/ml-teaching/issues/new/choose) to report bugs, suggest content improvements, or request new features.

## License

Educational materials developed for academic use at IIT Gandhinagar.