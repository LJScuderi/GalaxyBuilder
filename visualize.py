import numpy as np
from pathlib import Path

import plotly.graph_objects as go
import matplotlib.pyplot as plt

from utils import load_pickle, StarSystem
import constants as const


def visualize_solar_system(ssystem: StarSystem):
    nplanets = len(ssystem.planets)
    x = []
    y = np.arange(nplanets)
    colors = []
    for planet in ssystem.planets:
        planet.getitems()
        x.append(planet.sma)
        if planet.type == "T":
            colors.append("blue")
        elif planet.type == "S":
            colors.append("grey")
        elif planet.type == "N":
            colors.append("#17becf")
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


def solar_system_above(syst: StarSystem) -> None:
    fig = go.Figure()
    fig.update_layout(title=syst.star.name)
    star_rad = syst.star.radius * const.sun_radius / (const.au * 10)
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-star_rad,
        y0=-star_rad,
        x1=star_rad,
        y1=star_rad,
        line_color="yellow",
        fillcolor="yellow",
    )
    inner = syst.star.hab_zone[0]
    outer = syst.star.hab_zone[1]
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-inner,
        y0=-inner,
        x1=inner,
        y1=inner,
        line_color="green",
        fillcolor="red",
        layer="below",
        opacity=0.2,
    )
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-outer,
        y0=-outer,
        x1=outer,
        y1=outer,
        line_color="green",
        fillcolor="green",
        layer="below",
        opacity=0.1,
    )

    for planet in syst.planets:
        if planet.type == "T":
            col = "blue"
        elif planet.type == "S":
            col = "grey"
        elif planet.type == "N":
            col = "teal"
        else:
            col = "orange"

        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=-planet.sma,
            y0=-planet.sma,
            x1=planet.sma,
            y1=planet.sma,
            line_color=col,
        )
        maxrange = planet.sma * 1.1
    fig.update_xaxes(range=[-maxrange, maxrange])
    fig.update_yaxes(range=[-maxrange, maxrange])
    fig.show()


def main():
    galaxy = load_pickle(Path("Data/gen_galaxy_a"))
    sample: StarSystem = np.random.choice(galaxy)
    solar_system_above(sample)


if __name__ == "__main__":
    main()
