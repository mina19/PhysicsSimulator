from collections import defaultdict
from scipy.interpolate import CubicSpline

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

# Generate center of mass
y_cm = y1 / 2

# Create points for checking
t_check = np.array([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
y_check = np.array([-1, 1, 9, 1, -1])

# Create cubic spline interpolation
cs = CubicSpline(t_check, y_check, bc_type="periodic")
tension_magnitude = cs(t)


def tension_arrow(i):
    if tension_magnitude[i] > 0:
        # Calculate the direction vector of the rod
        dx = x1[i] - x2[i]
        dy = -y1[i]  # since y2 is always 0
    else:
        dx = x2[i] - x1[i]
        dy = y1[i]
    # Normalize and scale the vector
    magnitude = np.sqrt(dx**2 + dy**2)
    scale = 0.5 * np.abs(tension_magnitude[i])
    dx = scale * dx / magnitude
    dy = scale * dy / magnitude

    # Calculate the start point of the arrow
    start_x = x1[i]
    start_y = y1[i]
    return {
        "start_x": start_x,
        "start_y": start_y,
        "dx": dx,
        "dy": dy,
        "tension_magnitude": tension_magnitude[i],
        "ax": dx * 80,
        "ay": dy * 80,
    }


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
    {k: initial_frames_dict["frictionless_rail"][k] for k in ["mode", "line", "name"]}
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
        k: initial_frames_dict["m1"][k]
        for k in ["mode", "marker", "text", "textfont", "name"]
    }
)

frames_dict["m2"].update(
    {
        k: initial_frames_dict["m2"][k]
        for k in ["mode", "marker", "text", "textfont", "name"]
    }
)

frames_dict["center_of_mass"].update(
    {
        k: initial_frames_dict["center_of_mass"][k]
        for k in ["mode", "marker", "text", "textfont", "name"]
    }
)

frames_dict["massless_rigid_rod"].update(
    {k: initial_frames_dict["massless_rigid_rod"][k] for k in ["mode", "line", "name"]}
)


# Create frames
frames = []
for i in range(n_points):
    # Calculate angles for m1
    angle_m1 = -np.degrees(t[i])
    angle_m2 = -np.degrees(np.arctan2(-y1[i], x2[i] - x1[i]))

    frame_data = [
        # Static elements
        go.Scatter(x=[-b * 1.5, b * 1.5], y=[0, 0], **frames_dict["frictionless_rail"]),
        go.Scatter(**frames_dict["m1_path"]),
        # Dynamic elements
        go.Scatter(
            x=[x1[i]],
            y=[y1[i]],
            mode="markers+text",
            marker={
                "symbol": "square",
                "size": 30,
                "color": "blue",
                "angle": [angle_m1],
            },
            text=["m1"],
            name="m1",
        ),
        go.Scatter(
            x=[x2[i]],
            y=[0],
            mode="markers+text",
            marker={
                "symbol": "square",
                "size": 30,
                "color": "red",
                "angle": [angle_m2],
            },
            text=["m2"],
            name="m2",
        ),
        go.Scatter(x=[0], y=[y_cm[i]], **frames_dict["center_of_mass"]),
        go.Scatter(x=[x1[i], x2[i]], y=[y1[i], 0], **frames_dict["massless_rigid_rod"]),
    ]
    frames.append(
        go.Frame(
            data=frame_data,
            layout=go.Layout(
                annotations=[
                    {
                        "x": tension_arrow(i)["start_x"],
                        "y": tension_arrow(i)["start_y"],
                        "xref": "x",
                        "yref": "y",
                        "text": f"T: {tension_arrow(i)["tension_magnitude"]}",
                        "showarrow": True,
                        "arrowhead": 2,
                        "arrowsize": 1,
                        "arrowwidth": 2,
                        "ax": tension_arrow(i)["ax"],
                        "ay": tension_arrow(i)["ay"],
                    }
                ]
            ),
        )
    )

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


fig.add_trace(
    go.Scatter(
        x=[-b * 3.25],
        y=[-a * 1.1],
        mode="text",
        text=["Created by Min-A Cho Zeno, PhD"],
        showlegend=False,
        textfont=dict(size=12),
    )
)

fig.update_layout(
    font=dict(family="Arial", size=16, color="black"),
    title="Rigid Body Spatial Analysis: Two Masses + Rod System",
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
                            "frame": {"duration": 100, "redraw": False},
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
        {
            "x": tension_arrow(0)["start_x"],
            "y": tension_arrow(0)["start_y"],
            "xref": "x",
            "yref": "y",
            "text": "T",
            "showarrow": True,
            "arrowhead": 2,
            "arrowsize": 1,
            "arrowwidth": 2,
            "ax": tension_arrow(0)["dx"] * 80,
            "ay": tension_arrow(0)["dy"] * 80,
        }
    ],
)

fig.show()
