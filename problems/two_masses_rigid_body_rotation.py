import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

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

# Generate center of mass
y_cm = y1 / 2


# Create the outer dictionary
initial_frames_dict = {}

# Create the nested defaultdict structure
def create_none_defaultdict():
    return defaultdict(lambda: None)

initial_frames_dict = defaultdict(create_none_defaultdict)

# Add the data
# For frictionless rail
initial_frames_dict["frictionless_rail"]["x"] = [-b * 1.5, b * 1.5]
initial_frames_dict["frictionless_rail"]["y"] = [0, 0]
initial_frames_dict["frictionless_rail"]["mode"] = "lines"
initial_frames_dict["frictionless_rail"]["color"] = "black"
initial_frames_dict["frictionless_rail"]["width"] = 3

# For m1 ellipse
initial_frames_dict["m1_ellipse"]["x"] = x1
initial_frames_dict["m1_ellipse"]["y"] = y1
initial_frames_dict["m1_ellipse"]["mode"] = "lines"
initial_frames_dict["m1_ellipse"]["color"] = "gray"
initial_frames_dict["m1_ellipse"]["width"] = 2

# For m1
initial_frames_dict["m1"]["x"] = [x1[0]]
initial_frames_dict["m1"]["y"] = [y1[0]]
initial_frames_dict["m1"]["mode"] = "markers+text"
initial_frames_dict["m1"]["marker"] = {"symbol": "square", "size": 30, "color": "blue"}
initial_frames_dict["m1"]["text"] = ["m1"]

# For m2
initial_frames_dict["m2"]["x"] = [x2[0]]
initial_frames_dict["m2"]["y"] = [0]
initial_frames_dict["m2"]["mode"] = "markers+text"
initial_frames_dict["m2"]["marker"] = {"symbol": "square", "size": 30, "color": "red"}
initial_frames_dict["m2"]["text"] = ["m2"]

# For center of mass
initial_frames_dict["center_of_mass"]["x"] = [0]
initial_frames_dict["center_of_mass"]["y"] = [y_cm[0]]
initial_frames_dict["center_of_mass"]["mode"] = "markers+text"
initial_frames_dict["center_of_mass"]["marker"] = {"symbol": "circle", "size": 30, "color": "black"}
initial_frames_dict["center_of_mass"]["text"] = ["cm"]

# For massless rigid rod
initial_frames_dict["massless_rigid_rod"]["x"] = [x1[0], x2[0]]
initial_frames_dict["massless_rigid_rod"]["y"] = [y1[0], 0]
initial_frames_dict["massless_rigid_rod"]["mode"] = "lines"
initial_frames_dict["massless_rigid_rod"]["line"] = {"color": "black", "width": 1, "dash": "dot"}


# Create frames for animation
frames = []
for i in range(n_points):
    frames.append(
        go.Frame(
            data=[
                # horizontal axis
                go.Scatter(
                    x=[-b * 1.5, b * 1.5],
                    y=[0, 0],
                    mode="lines",
                    line=dict(color="black", width=3),
                    name="frictionless rail",
                ),
                # static ellipse
                go.Scatter(
                    x=x1,
                    y=y1,
                    mode="lines",
                    line=dict(color="gray", width=2),
                    name="m1 path",
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
                # center of mass
                go.Scatter(
                    x=[0] * n_points,
                    y=[y_cm[i]],
                    mode="markers+text",
                    marker=dict(symbol="circle", size=30, color="black"),
                    text=["cm"],
                    textfont=dict(color="white"),
                    name="cm",
                ),
                # rod
                go.Scatter(
                    x=[x1[i], x2[i]],
                    y=[y1[i], 0],
                    mode="lines",
                    line=dict(color="black", width=1, dash="dot"),
                    name="massless rigid rod",
                ),
            ]
        )
    )

# Create the figure
fig = go.Figure(
    data=[ go.Scatter(
        x = specs["x"],
        y = specs["y"],
        mode = specs["mode"],
        marker = specs["marker"] if "marker" in specs["mode"] else None,
        line = specs["line"] if "line" in specs["mode"] else None,
        text = specs.get("text", None),
        textfont=dict(color="white") if specs.get("text", None) else None
    ) for specs in initial_frames_dict.values()],
    frames = frames)


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
            "x": 0.02,
            "xanchor": "left",
            "y": 1.0,
            "yanchor": "top",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 40, "redraw": False},
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {"duration": 0}
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
                            "transition": {"duration": 0}
                        },
                    ],
                },
            ],
        }
    ],
    annotations=[
        dict(
            text="Created by Min-A Cho Zeno, PhD",
            xref="x",  
            yref="y",  
            x=-b * 4,
            y=-a * 1.1,
            showarrow=False,
            font=dict(size=12),
            xanchor="left"
        )
    ]
)

fig.show()
