# Regularization App

A simple Streamlit app to explore Ridge and Lasso regression with polynomial features.

## Features

- **Interactive sliders**: Adjust polynomial degree and regularization strength
- **Model comparison**: Compare Ridge vs Lasso or view them side-by-side
- **Visual feedback**: See how regularization affects model fit
- **Educational content**: Brief explanations of key concepts

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run regularisation.py`
3. Adjust the parameters in the sidebar and observe the effects

## Key Improvements from Original

- Better plot styling with grid and improved colors
- Comparison mode to see both Ridge and Lasso together
- Cleaner coefficient display showing which features are removed
- Educational explanations in an expandable section
- Better equation formatting and statistics display

## Understanding the Parameters

- **Polynomial Degree**: Controls model complexity (higher = more complex)
- **Regularization Strength (α)**: Controls how much to penalize large coefficients
- **Ridge**: Shrinks coefficients but keeps all features
- **Lasso**: Can completely remove features by setting coefficients to zero