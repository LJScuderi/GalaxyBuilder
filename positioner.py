from typing import Tuple
import numpy as np
import plotly.graph_objects as go


def randomize_pos_in_bin(bins: np.ndarray) -> np.ndarray:
    return [num + np.random.uniform(0, 1) for num in bins]


def find_prob_array(sig: float, arr: np.ndarray) -> np.ndarray:
    coeff = 1.0 / (sig * 2.0 * np.pi)
    coeff = 1.0 / (sig * 2.0 * np.pi)
    den = 2 * sig**2
    expo = [-0.5 * (elem / den) ** 2 for elem in arr]
    raw_prob = coeff * np.exp(expo)
    sump = np.sum(raw_prob)
    prob = [num / sump for num in raw_prob]
    return prob


def old_working():
    xbins = np.arange(11)
    ybins = np.arange(11)
    zbins = np.arange(11)
    prob = [1, 2, 8, 12, 16, 30, 16, 12, 8, 2, 1]
    sump = np.sum(prob)
    probx = [elem / sump for elem in prob]
    proby = probx
    pz = [0, 1, 1, 2, 10, 100, 10, 2, 1, 1, 0]
    sumz = np.sum(pz)
    probz = [num / sumz for num in pz]
    pos = np.array([xbins, ybins, zbins])
    probs = np.array([probx, proby, probz])
    xbin = np.random.choice(xbins, size=1000, p=probx)
    ybin = np.random.choice(ybins, size=1000, p=proby)
    zbin = np.random.choice(zbins, size=1000, p=probz)
    x = randomize_pos_in_bin(xbin)
    y = randomize_pos_in_bin(ybin)
    z = randomize_pos_in_bin(zbin)
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="markers", marker_size=2)])
    fig.show()


def generate_disc():
    bins = np.arange(-50, 51)
    xysig = 2.5
    zsig = 0.5
    probxy = find_prob_array(xysig, bins)
    probz = find_prob_array(zsig, bins)
    nstars = 10000
    xbin = np.random.choice(bins, size=nstars, p=probxy)
    ybin = np.random.choice(bins, size=nstars, p=probxy)
    zbin = np.random.choice(bins, size=nstars, p=probz)
    x = randomize_pos_in_bin(xbin)
    y = randomize_pos_in_bin(ybin)
    z = randomize_pos_in_bin(zbin)
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="markers", marker_size=1)])
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                range=[-100, 100],
            ),
            yaxis=dict(
                range=[-100, 100],
            ),
            zaxis=dict(
                range=[-100, 100],
            ),
        )
    )
    fig.show()


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


def local_kpc(xymax: float = 500.0, nstars: int = 1) -> tuple[float, float, float]:
    bins = np.arange(-xymax, xymax)
    xysig = 50.0
    zsig = 9
    probxy = find_prob_array(xysig, bins)
    probz = find_prob_array(zsig, bins)
    xbin = np.random.choice(bins, size=nstars, p=probxy)
    ybin = np.random.choice(bins, size=nstars, p=probxy)
    zbin = np.random.choice(bins, size=nstars, p=probz)
    x = randomize_pos_in_bin(xbin)
    y = randomize_pos_in_bin(ybin)
    z = randomize_pos_in_bin(zbin)
    return x, y, z


def main():
    x, y, z = local_kpc(xymax=500, nstars=1000)
    vis_gal(x, y, z, 500.0)


if __name__ == "__main__":
    main()
