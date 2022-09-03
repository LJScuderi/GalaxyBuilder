from dataclasses import dataclass
from typing import List, Tuple

import random
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import star_utils as sutil
import planet_utils as putil
import constants as const


@dataclass(frozen=True)
class oElements:
    sma: float
    ecc: float
    inc: float
    aop: float
    raan: float
    mano: float


@dataclass(frozen=True)
class Atmosphere:
    scale_height: float  # km
    surface_pressure: float  # atmospheres
    oxy: float
    nitro: float
    carbon_dioxide: float
    methane: float
    hydrogen: float
    helium: float
    others: float

    def __post_init__(self):
        assert (
            sum(self.oxy, self.nitro, self.carbon_dioxide, self.methane, self.hydrogen, self.helium, self.others) == 1
        ), "Composition percentages do not sum to 1"

    def getitems(self):
        print(vars(self))


@dataclass(frozen=True)
class Planet:
    name: str
    parent: str
    type: str
    sma: float
    axial_tilt: float  # degrees
    rotation_period: float  # days
    radius: float  # earth units
    density: float  # kg/m^3
    atmos: Atmosphere
    ocean_coverage: float  # percent
    moons: int

    def getitems(self):
        print(vars(self))

    # derived elements:
    # subsolar temperature
    # mass
    # surface gravity
    # mineral abundance
    # temperature/climate
    # population
    # habitability
    # life development


@dataclass(frozen=True)
class Station:
    population: float
    name: str
    type: str
    parent: str

    def getitems(self):
        print(vars(self))


@dataclass(frozen=True)
class Star:
    name: str
    temperature: float  # Surface temp in Kelvin
    mass: float  # mass in solar masses
    age: float  # Age in GYr
    metallicity: float  # Metallicity in solar units
    magnitude: float
    luminosity: float
    radius: float
    hab_zone: List[float]
    lifespan: float
    harv_class: str

    def getitems(self):
        print(vars(self))


@dataclass(frozen=True)
class StarSystem:
    gal_x: float  # Galactic X position in pc from Earth (spin/antispin)
    gal_y: float  # Galactic Y position in pc from Earth (coreward/rimward)
    gal_z: float  # Galactic Z position in pc from Earth (north/south polar)
    star: Star
    planets: List[Planet]

    def getitems(self):
        print("X: ", self.gal_x)
        print("Y: ", self.gal_y)
        print("Z: ", self.gal_z)
        print("N_planets: ", len(self.planets))

    # stations: List[Station]
    # asteroid_belts: dict  # dict of asteroid belts listing belt number and distance from star (AU)


def generate_planet(star: Star, number: int) -> Planet:
    name = star.name + str(number)
    # randomly pick if it's rocky or gas
    midpoint = (((star.mass - 0.1) / 2.9) * 0.6) + 0.2
    ntype = np.random.uniform(0, 1)
    # randomly generate mass from distribution
    if ntype > midpoint:
        mass = np.random.wald(0.8, 6.0, 1)
        type = "Rocky"
    if ntype <= midpoint:
        mass = np.random.triangular(4.0, 17.1, 600.0)
        type = "Gas"
    print(name, type, float(mass))
    # randomly generate density from distribution
    # randomly generate atmosphere (?)
    # randomly generate orbital parameters
    # randomly generate moon(s)
    # compute surface gravity
    # compute surface temperature
    # compute volatiles
    # compute atmosphere?
    pass


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
    sysx = random.uniform(0, map_size)
    sysy = random.uniform(0, map_size)
    sysz = random.uniform(0, map_size)
    # generate star
    star = generate_star(index=index)
    # get number of planets
    nplanets = random.randrange(0, 3)
    planets = []
    # make planets
    for num in range(nplanets):
        planet = generate_planet(star)
        planets.append(planet)
    # generate/make asteroid belts
    # get number of stations
    # make stations
    # make star
    return StarSystem(sysx, sysy, sysz, star, planets)


def main():
    # generate systems
    # generate ISM
    # save results
    random.seed(a=4)
    test1: StarSystem = generate_system(map_size=1000, index=0)
    test1.star.getitems()

    for num in range(1, 9):
        generate_planet(test1.star, num)
    # a =
    # plt.hist(a, bins=100, density=True)
    # plt.show()


if __name__ == "__main__":
    main()
