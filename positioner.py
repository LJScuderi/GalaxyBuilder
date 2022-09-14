import numpy as np

import visualize as vis


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


def generate_disc() -> tuple[float, float, float]:
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
    return x, y, z


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
    vis.vis_gal(x, y, z, 500.0)


if __name__ == "__main__":
    main()
