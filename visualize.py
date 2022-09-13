import plotly.graph_objects as go
import matplotlib.pyplot as plt
from generate_galaxy import StarSystem
import numpy as np


def visualize_solar_system(ssystem: StarSystem):
    nplanets = len(ssystem.planets)
    x = []
    y = np.arange(nplanets)
    colors = []
    for planet in ssystem.planets:
        planet.getitems()
        x.append(planet.sma)
        if planet.type == "T":
            colors.append("green")
        elif planet.type == "S":
            colors.append("grey")
        elif planet.type == "N":
            colors.append("blue")
        else:
            colors.append("orange")

    plt.scatter(x, y, c=colors)
    plt.vlines(ssystem.star.hab_zone, 0, nplanets, colors=["green"])
    plt.show()


def vis_gal(x: np.ndarray, y: np.ndarray, z: np.ndarray, xymax: float):
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="markers", marker_size=1, marker_color="white")])
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                backgroundcolor="black",
                range=[-xymax, xymax],
            ),
            yaxis=dict(
                backgroundcolor="black",
                range=[-xymax, xymax],
            ),
            zaxis=dict(
                backgroundcolor="black",
                range=[-xymax, xymax],
            ),
            bgcolor="black",
        )
    )
    fig.show()
