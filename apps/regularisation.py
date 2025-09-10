import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.linear_model import Ridge, Lasso
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# Set random seed for reproducibility
np.random.seed(42)

# Create a dataset in 1d
def f(x):
    return x * np.sin(x) + np.cos(4*x)

n_points = 50

# Create a dataset
x_plot = np.linspace(0, 10, 100)
x = np.linspace(0, 10, n_points)
y = f(x) + np.random.randn(n_points) * 1.5  # Increased noise from 1.0 to 1.5
m_y = np.mean(y)
s_y = np.std(y)
y = (y - m_y) / s_y

f_true = (f(x_plot) - m_y) / s_y

# Create a streamlit app
st.title("Regularization in Machine Learning")
st.write(
    "This app shows the fit of Ridge and Lasso regression with varying degrees and regularization strength."
)

# The sidebar contains the sliders and the regression type dropdown
with st.sidebar:
    st.header("Parameters")
    
    # Create a slider for degree
    degree = st.slider("Polynomial Degree", 1, 15, 5)

    # Create a slider for alpha (common parameter for both Ridge and Lasso)
    alpha = st.slider("Regularization Strength (α)", 0.0, 10.0, 1.0, step=0.1)

    # Create a dropdown for regression type
    regression_type = st.selectbox("Regression Type", ["Ridge", "Lasso"])
    
    # Add comparison option
    show_comparison = st.checkbox("Compare Both Methods", False)

# Create models
if show_comparison:
    ridge_model = make_pipeline(PolynomialFeatures(degree, include_bias=False), Ridge(alpha=alpha))
    lasso_model = make_pipeline(PolynomialFeatures(degree, include_bias=False), Lasso(alpha=alpha, max_iter=2000))
    
    # Fit both models
    ridge_model.fit(x[:, np.newaxis], y)
    lasso_model.fit(x[:, np.newaxis], y)
    
    # Predict
    ridge_pred = ridge_model.predict(x_plot[:, np.newaxis])
    lasso_pred = lasso_model.predict(x_plot[:, np.newaxis])
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, label="Training Data", alpha=0.7)
    ax.plot(x_plot, f_true, label="True Function", color="black", linestyle="--", linewidth=2)
    ax.plot(x_plot, ridge_pred, label="Ridge", color="red", linewidth=2)
    ax.plot(x_plot, lasso_pred, label="Lasso", color="green", linewidth=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylim(-3, 3)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    # Show coefficients comparison
    st.subheader("Coefficient Comparison")
    
    ridge_coef = ridge_model.steps[1][1].coef_
    lasso_coef = lasso_model.steps[1][1].coef_
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Ridge Coefficients:**")
        ridge_intercept = ridge_model.steps[1][1].intercept_
        st.write(f"Intercept: {ridge_intercept:.4f}")
        for i, coef in enumerate(ridge_coef, 1):
            st.write(f"x^{i}: {coef:.4f}")
        st.write(f"L2 norm: {np.sqrt(np.sum(ridge_coef**2) + ridge_intercept**2):.4f}")
    
    with col2:
        st.write("**Lasso Coefficients:**")
        lasso_intercept = lasso_model.steps[1][1].intercept_
        st.write(f"Intercept: {lasso_intercept:.4f}")
        for i, coef in enumerate(lasso_coef, 1):
            if abs(coef) > 1e-6:
                st.write(f"x^{i}: {coef:.4f}")
            else:
                st.write(f"x^{i}: 0.0000 (removed)")
        st.write(f"L1 norm: {np.sum(np.abs(lasso_coef)) + np.abs(lasso_intercept):.4f}")
        n_nonzero = np.sum(np.abs(lasso_coef) > 1e-6)
        st.write(f"Features selected: {n_nonzero}/{len(lasso_coef)}")

else:
    # Single model mode (original behavior)
    if regression_type == "Ridge":
        model = make_pipeline(PolynomialFeatures(degree, include_bias=False), Ridge(alpha=alpha))
        color = "red"
    else:
        model = make_pipeline(PolynomialFeatures(degree, include_bias=False), Lasso(alpha=alpha, max_iter=2000))
        color = "green"

    # Fit the model
    model.fit(x[:, np.newaxis], y)

    # Predict
    y_plot = model.predict(x_plot[:, np.newaxis])

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, label="Training Data", alpha=0.7)
    ax.plot(x_plot, y_plot, label=f"{regression_type} Prediction", color=color, linewidth=2)
    ax.plot(x_plot, f_true, label="True Function", color="black", linestyle="--", linewidth=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylim(-3, 3)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Show the model equation
    st.subheader("Model Equation")
    intercept = model.steps[1][1].intercept_
    coefficients = model.steps[1][1].coef_

    # Build equation string
    equation_parts = [f"{intercept:.4f}"]
    for i, coef in enumerate(coefficients, start=1):
        if abs(coef) > 1e-6:  # Only show non-zero coefficients
            sign = "+" if coef >= 0 else "-"
            if i == 1:
                equation_parts.append(f" {sign} {abs(coef):.4f}x")
            else:
                equation_parts.append(f" {sign} {abs(coef):.4f}x^{i}")

    equation = "y = " + "".join(equation_parts)
    equation = equation.replace(" + -", " - ")
    st.code(equation)

    # Show coefficient statistics
    st.subheader("Model Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("L1 norm", f"{np.sum(np.abs(coefficients)) + np.abs(intercept):.4f}")
    
    with col2:
        st.metric("L2 norm", f"{np.sqrt(np.sum(coefficients**2) + intercept**2):.4f}")
    
    with col3:
        if regression_type == "Lasso":
            n_nonzero = np.sum(np.abs(coefficients) > 1e-6)
            st.metric("Features selected", f"{n_nonzero}/{len(coefficients)}")
        else:
            st.metric("Max coefficient", f"{np.max(np.abs(coefficients)):.4f}")

# Educational notes
with st.expander("Understanding Regularization"):
    st.write("""
    **Ridge Regression (L2):**
    - Adds penalty: α × Σ(coefficients²)
    - Shrinks coefficients toward zero but never exactly to zero
    - Good when all features are somewhat relevant
    
    **Lasso Regression (L1):**
    - Adds penalty: α × Σ|coefficients|
    - Can set coefficients to exactly zero (feature selection)
    - Good when only some features are relevant
    
    **Alpha (α) parameter:**
    - Higher α = more regularization = simpler model
    - Lower α = less regularization = more complex model
    - α = 0 = no regularization (standard polynomial regression)
    
    **Why do coefficient magnitudes often increase with degree?**
    - Higher degree polynomials can oscillate more to fit noisy data
    - Without regularization, models overfit by using large coefficients
    - Large coefficients indicate the model is working hard to fit noise
    - Regularization prevents this by penalizing large coefficients
    """)