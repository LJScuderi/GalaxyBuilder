import numpy as np
import plotly.graph_objects as go


def randomize_pos_in_bin(bins: np.ndarray) -> np.ndarray:
    return [num + np.random.uniform(0, 1) for num in bins]


def main():
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


if __name__ == "__main__":
    main()
