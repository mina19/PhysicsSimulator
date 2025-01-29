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


# Create the nested defaultdict structure
def create_none_defaultdict():
    return defaultdict(lambda: None)


# Create frames
frames_dict = defaultdict(create_none_defaultdict)
initial_frames_dict = defaultdict(create_none_defaultdict)

# Initial frames dictionary
initial_frames_dict["frictionless_rail"].update(
    {
        "x": [-b * 1.5, b * 1.5],
        "y": [0, 0],
        "mode": "lines",
        "line": {"color": "black", "width": 3},
        "name": "frictionless rail",
    }
)

initial_frames_dict["m1_ellipse"].update(
    {
        "x": x1,
        "y": y1,
        "mode": "lines",
        "line": {"color": "gray", "width": 2},
        "name": "m1 path",
    }
)

initial_frames_dict["m1"].update(
    {
        "x": [x1[0]],
        "y": [y1[0]],
        "mode": "markers+text",
        "marker": {"symbol": "square", "size": 30, "color": "blue"},
        "text": ["m1"],
        "name": "m1",
    }
)

initial_frames_dict["m2"].update(
    {
        "x": [x2[0]],
        "y": [0],
        "mode": "markers+text",
        "marker": {"symbol": "square", "size": 30, "color": "red"},
        "text": ["m2"],
        "name": "m2",
    }
)

initial_frames_dict["center_of_mass"].update(
    {
        "x": [0],
        "y": [y_cm[0]],
        "mode": "markers+text",
        "marker": {"symbol": "circle", "size": 30, "color": "black"},
        "text": ["cm"],
        "name": "center of mass",
    }
)

initial_frames_dict["massless_rigid_rod"].update(
    {
        "x": [x1[0], x2[0]],
        "y": [y1[0], 0],
        "mode": "lines",
        "line": {"color": "black", "width": 1, "dash": "dot"},
        "name": "massless rigid rod",
    }
)

# Frames dictionary
frames_dict["frictionless_rail"].update(
    {
        "mode": "lines",
        "line": {"color": "black", "width": 3},
        "name": "frictionless rail",
    }
)

frames_dict["m1_path"].update(
    {
        "x": x1,
        "y": y1,
        "mode": "lines",
        "line": {"color": "gray", "width": 2},
        "name": "m1 path",
    }
)

frames_dict["m1"].update(
    {
        "mode": "markers+text",
        "marker": {"symbol": "square", "size": 30, "color": "blue"},
        "text": ["m1"],
        "textfont": {"color": "white"},
        "name": "m1",
    }
)

frames_dict["m2"].update(
    {
        "mode": "markers+text",
        "marker": {"symbol": "square", "size": 30, "color": "red"},
        "text": ["m2"],
        "textfont": {"color": "white"},
        "name": "m2",
    }
)

frames_dict["cm"].update(
    {
        "mode": "markers+text",
        "marker": {"symbol": "circle", "size": 30, "color": "black"},
        "text": ["cm"],
        "textfont": {"color": "white"},
        "name": "cm",
    }
)

frames_dict["massless_rigid_rod"].update(
    {
        "mode": "lines",
        "line": {"color": "black", "width": 1, "dash": "dot"},
        "name": "massless rigid rod",
    }
)

# Create frames
frames = []
for i in range(n_points):
    frame_data = [
        # Static elements
        go.Scatter(x=[-b * 1.5, b * 1.5], y=[0, 0], **frames_dict["frictionless_rail"]),
        go.Scatter(**frames_dict["m1_path"]),
        # Dynamic elements
        go.Scatter(x=[x1[i]], y=[y1[i]], **frames_dict["m1"]),
        go.Scatter(x=[x2[i]], y=[0], **frames_dict["m2"]),
        go.Scatter(x=[0], y=[y_cm[i]], **frames_dict["cm"]),
        go.Scatter(x=[x1[i], x2[i]], y=[y1[i], 0], **frames_dict["massless_rigid_rod"]),
    ]
    frames.append(go.Frame(data=frame_data))


# Create the figure
fig = go.Figure(
    data=[
        go.Scatter(
            x=specs["x"],
            y=specs["y"],
            mode=specs["mode"],
            marker=specs["marker"] if "marker" in specs["mode"] else None,
            line=specs["line"] if "line" in specs["mode"] else None,
            text=specs.get("text", None),
            textfont=dict(color="white") if specs.get("text", None) else None,
        )
        for specs in initial_frames_dict.values()
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
    annotations=[
        dict(
            text="Created by Min-A Cho Zeno, PhD",
            xref="x",
            yref="y",
            x=-b * 4,
            y=-a * 1.1,
            showarrow=False,
            font=dict(size=12),
            xanchor="left",
        )
    ],
)

fig.show()
