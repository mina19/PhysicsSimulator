import numpy as np
import plotly.graph_objects as go

# Parameters for m1 ellipse
a = 2  # semi-major axis
b = 1  # semi-minor axis
n_points = 100

# Generate m1 ellipse path points
t = np.linspace(0, 2 * np.pi, n_points)
x1 = -b * np.sin(t)
y1 = a * np.cos(t)

# Generate m2 frictionless back-and-forth points
x2 = b * np.sin(t) 

# Create frames for animation
frames = []
for i in range(n_points):
    frames.append(
        go.Frame(
            data=[
                # static ellipse
                go.Scatter(
                    x=x1,
                    y=y1,
                    mode="lines",
                    line=dict(color="gray", width=2),
                    name="Path",
                ),
                # m1
                go.Scatter(
                    x=[x1[i]],
                    y=[y1[i]],
                    mode="markers+text",
                    marker=dict(symbol="square", size=30, color="blue"),
                    text=["m1"],
                    textfont=dict(color="white"),
                    name="m1",
                ),
                # m2
                go.Scatter(
                    x=[x2[i]],
                    y=[0] * n_points,
                    mode="markers+text",
                    marker=dict(symbol="square", size=30, color="red"),
                    text=["m2"],
                    textfont=dict(color="white"),
                    name="m2",
                ),
            ]
        )
    )

# Create the figure
fig = go.Figure(
    data=[
        # Initial ellipse path
        go.Scatter(
            x=x1, y=y1, mode="lines", line=dict(color="gray", width=2), name="Path"
        ),
        # Initial m1
        go.Scatter(
            x=[x1[0]],
            y=[y1[0]],
            mode="markers+text",
            marker=dict(symbol="square", size=30, color="blue"),
            text=["m1"],
            textfont=dict(color="white"),
            name="m1",
        ),
        # Initial m2
        go.Scatter(
            x=[x2[0]],
            y=[0],
            mode="markers+text",
            marker=dict(symbol="square", size=30, color="red"),
            text=["m2"],
            textfont=dict(color="white"),
            name="m2",
        ),
    ],
    frames=frames,
)

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=16, color="black"),
    title="Two Masses Rigid Body Rotation Problem Simulation",
    xaxis=dict(title="x", range=[-b * 0.5, b * 0.5]),
    yaxis=dict(title="y", range=[-a * 1.2, a * 1.2], scaleanchor="x", scaleratio=1),
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    updatemenus=[
        {
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": n_points/2, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0},
                        },
                    ],
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                },
            ],
        }
    ],
)

fig.show()
