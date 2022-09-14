from string import ascii_lowercase as letters
import random
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from pathlib import Path

import star_utils as sutil
import planet_utils as putil
import constants as const
import atmospheres as atms
import positioner as posi
import visualize as vis
from utils import Star, Planet, StarSystem, write_pickle, Atmosphere


def gen_subearth(star: Star, sma: float, name: str, type: str) -> Planet:
    mass = np.random.uniform(0.001, 0.5)
    cmf = np.random.uniform(0.0, 0.1)
    radius = putil.rocky_radius(mass, cmf) * np.random.uniform(0.90, 1.00)
    density = putil.planet_density(mass, radius)
    surf_g = putil.surface_grav(mass, radius)
    p_atmos = 0.001
    atmos = atms.gen_terrestrial_atmos(star.luminosity, sma, p_atmos, surf_g)
    tilt, spin = putil.gen_tilt_spin(
        sma * const.au * 1000,
        radius * const.earth_radius,
        star.mass * const.sun_mass,
        mass * const.earth_mass,
        star.age,
    )
    nmoons = np.random.randint(0, 2)
    return Planet(name, star.name, type, mass, sma, tilt, spin, radius, density, atmos, nmoons, surf_g)


def gen_terrestrial(star: Star, sma: float, name: str, type: str) -> Planet:
    mass = np.random.uniform(0.1, 2.0)
    cmf = np.random.triangular(0.1, 0.26, 0.4)
    radius = putil.rocky_radius(mass, cmf) * np.random.uniform(0.95, 1.05)
    density = putil.planet_density(mass, radius)
    surf_g = putil.surface_grav(mass, radius)
    if star.hab_zone[0] < sma < star.hab_zone[1]:
        p_atmos = 0.95
    else:
        p_atmos = 0.01
    atmos = atms.gen_terrestrial_atmos(star.luminosity, sma, p_atmos, surf_g)

    tilt, spin = putil.gen_tilt_spin(
        sma * const.au * 1000,
        radius * const.earth_radius,
        star.mass * const.sun_mass,
        mass * const.earth_mass,
        star.age,
    )
    nmoons = np.random.randint(0, 2)

    return Planet(name, star.name, type, mass, sma, tilt, spin, radius, density, atmos, nmoons, surf_g)


def gen_neptune(star: Star, sma: float, name: str, type: str) -> Planet:
    mass = np.random.triangular(3.0, 10.0, 30.0)
    radius = mass**0.55 * np.random.uniform(0.95, 1.05)
    density = putil.planet_density(mass, radius)
    surf_g = putil.surface_grav(mass, radius)
    atmos = atms.gen_gas_atmos(star.luminosity, sma, surf_g)
    tilt, spin = putil.gen_tilt_spin(
        sma * const.au * 1000,
        radius * const.earth_radius,
        star.mass * const.sun_mass,
        mass * const.earth_mass,
        star.age,
    )
    nmoons = np.random.randint(5, 30)

    return Planet(name, star.name, type, mass, sma, tilt, spin, radius, density, atmos, nmoons, surf_g)


def gen_gas_giant(star: Star, sma: float, name: str, type: str) -> Planet:
    mass = np.random.triangular(30.0, 100.0, 600.0)
    radius = (138.6627041 * (mass**0.01) - 135.6762705) * np.random.uniform(0.98, 1.02)
    density = putil.planet_density(mass, radius)
    surf_g = putil.surface_grav(mass, radius)
    atmos = atms.gen_gas_atmos(star.luminosity, sma, surf_g)
    tilt, spin = putil.gen_tilt_spin(
        sma * const.au * 1000,
        radius * const.earth_radius,
        star.mass * const.sun_mass,
        mass * const.earth_mass,
        star.age,
    )
    nmoons = np.random.randint(30, 120)

    return Planet(name, star.name, type, mass, sma, tilt, spin, radius, density, atmos, nmoons, surf_g)


def generate_planet(star: Star, number: int, sma: float) -> Planet:
    name = star.name + str(number)

    # randomly pick if it's rocky or gas
    if star.mass < 0.5:
        planet_p = [0.3, 0.4, 0.2, 0.1]
    elif 0.5 <= star.mass <= 2.0:
        planet_p = [0.2, 0.4, 0.2, 0.2]
    elif 2.0 < star.mass:
        planet_p = [0.2, 0.2, 0.3, 0.3]
    planet_types = ["S", "T", "N", "G"]
    type = np.random.choice(planet_types, 1, p=planet_p)

    # based on type, generate planet
    match type:
        case "S":
            planet = gen_subearth(star=star, sma=sma, name=name, type=type)
        case "T":
            planet = gen_terrestrial(star=star, sma=sma, name=name, type=type)
        case "N":
            planet = gen_neptune(star=star, sma=sma, name=name, type=type)
        case "G":
            planet = gen_gas_giant(star=star, sma=sma, name=name, type=type)
    return planet


def generate_star(index: int) -> Star:
    # these random distributions are absolute trash, sorry
    mass = np.random.triangular(0.1, 0.4, 3.0)
    lifetime = sutil.stellar_lifespan(mass)
    age = random.uniform(0, lifetime)
    feh = np.random.triangular(left=-1.0, mode=0, right=0.5)
    temp = sutil.stellar_temp(mass)
    lum = sutil.calculate_luminosity(mass)
    mag = sutil.absolute_magnitude(lum)
    rad = sutil.star_radius(mass)
    hab_in, hab_out = sutil.habitable_zone(lum)
    star = Star(
        name=str(index).zfill(4) + "A",
        temperature=temp,
        mass=mass,
        age=age / 1e9,
        metallicity=feh,
        magnitude=mag,
        luminosity=lum,
        radius=rad,
        hab_zone=[hab_in, hab_out],
        lifespan=lifetime / 1e9,
        harv_class=sutil.stellar_class(temp),
    )
    return star


def generate_system(map_size: float, index: int) -> StarSystem:
    # generate coordinates
    sysx, sysy, sysz = posi.local_kpc(xymax=map_size)
    # generate star
    star = generate_star(index=index)
    # get number of planets
    nplanets = np.random.choice(15, p=const.n_p_prob) + 1
    planets = []
    smas = np.sort(np.random.exponential(0.8, nplanets) * 10) * np.sqrt(star.mass)
    # smas = np.sort(np.random.uniform(0.1, 60, nplanets))
    # make planets
    for sma, let in zip(smas, list(letters)):
        planet = generate_planet(star, let, sma)
        planets.append(planet)
    # generate/make asteroid belts
    # get number of stations
    # make stations
    # make star
    return StarSystem(sysx, sysy, sysz, star, planets)


def test_func() -> None:
    # testing for sma distribution
    # not bad
    # a = np.random.f(2.5, 25, 100000) * 10

    # weird but not horrible
    # a = np.abs(np.random.vonmises(1, 1, 100000) * 20)
    a = np.random.choice(15, size=100000, p=const.n_p_prob) + 1
    plt.hist(a, bins=200, density=True)
    plt.show()
    # for n in range(0, 10):
    #     b, c = putil.gen_tilt_spin(const.au * 1000, const.earth_radius, const.sun_mass, const.earth_mass, 5e9)
    #     print(b, c)
    # a = atms.gen_gas_atmos(1, 5.2, 2.36)
    # a.getitems()
    return


def generate_systems(nsystems: int) -> None:
    nsystems = 1000
    random.seed(a=4)
    galaxy = []
    # generate systems
    for n in tqdm(range(nsystems)):
        galaxy.append(generate_system(map_size=500.0, index=n))

    write_pickle(galaxy, Path("Data/gen_galaxy_a"))


def main():
    galaxy = vis.load_pickle(Path("Data/gen_galaxy_a"))
    sample: StarSystem = np.random.choice(galaxy)
    vis.solar_system_above(sample)


if __name__ == "__main__":
    main()
