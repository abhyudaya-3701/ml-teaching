# app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# function
def f(x, y):
    return np.abs(x + y) + 3*np.abs(y - x)

# grid for contours
X = np.linspace(-3, 3, 200)
Y = np.linspace(-3, 3, 200)
XX, YY = np.meshgrid(X, Y)
ZZ = f(XX, YY)

st.set_page_config(layout="wide")
st.title("Coordinate Descent Failure (Interactive Demo)")

# --- Choose start point ---
x0 = st.sidebar.slider("Start x", -3.0, 3.0, -2.0, 0.1)
y0 = st.sidebar.slider("Start y", -3.0, 3.0, -2.0, 0.1)
z0 = f(x0, y0)

# --- Plot ---
fig = go.Figure()

# filled contours with colorbar
fig.add_trace(go.Contour(
    z=ZZ, x=X, y=Y,
    contours=dict(start=0, end=12, size=1),
    colorscale="Viridis", showscale=True,
    hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>f=%{z:.2f}<extra></extra>"
))

# start point
fig.add_trace(go.Scatter(
    x=[x0], y=[y0],
    mode="markers+text",
    marker=dict(size=14, color="red"),
    text=[f"({x0:.1f},{y0:.1f}), f={z0:.1f}"],
    textposition="top right",
    hovertext=f"x={x0:.2f}, y={y0:.2f}, f={z0:.2f}",
    hoverinfo="text"
))

# dotted vertical line (fix x, vary y)
fig.add_trace(go.Scatter(
    x=[x0]*2, y=[-3,3],
    mode="lines",
    line=dict(dash="dot", color="red"),
    hoverinfo="skip"
))

# dotted horizontal line (fix y, vary x)
fig.add_trace(go.Scatter(
    x=[-3,3], y=[y0]*2,
    mode="lines",
    line=dict(dash="dot", color="red"),
    hoverinfo="skip"
))

# global optimum
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode="markers+text",
    marker=dict(size=14, color="green", symbol="x"),
    text=["Global Min f=0"],
    textposition="bottom right",
    hovertext="(0,0), f=0",
    hoverinfo="text"
))

fig.update_layout(
    width=900, height=800,
    xaxis=dict(scaleanchor="y", range=[-3,3]),
    yaxis=dict(range=[-3,3]),
    title="f(x,y) = |x+y| + 3|y-x|"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"**Current point:** ({x0:.2f}, {y0:.2f}), f = {z0:.2f}")
st.markdown(
    "👉 Move your mouse along the **red dotted vertical/horizontal lines**. "
    "You’ll see that $f(x,y)$ does **not decrease** when you restrict to one coordinate — "
    "illustrating why coordinate descent fails here."
)
