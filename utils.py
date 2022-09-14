import pickle
from dataclasses import dataclass
from typing import List, Any
import pickle
from pathlib import Path


def write_pickle(data: Any, file_path: Path) -> None:
    print("Writing data to file.")
    with file_path.open(mode="wb") as f:
        pickle.dump(data, f)


def load_pickle(load_file: Path) -> Any:
    print("Reading data from file.")
    with load_file.open(mode="rb") as f:
        return pickle.load(f)


@dataclass(frozen=True)
class Atmosphere:
    scale_height: float  # km
    pressure: float  # surface pressure in atmospheres
    comp: dict  # composition, two main species
    eta: float  # absorbtion factor
    temp: float  # average surface temp in K
    ocean: float  # surface ocean coverage fraction
    albedo: float  # surface albedo

    # def __post_init__(self):
    #     assert sum(self.comp.values()) == 1, "Composition percentages do not sum to 1"

    def getitems(self):
        print(vars(self))


@dataclass(frozen=True)
class Planet:
    name: str  # planet name
    parent: str  # Parent star
    type: str  # plaent type
    mass: float  # mass in earth masses
    sma: float  # semimajor axis in AU
    axial_tilt: float  # degrees
    rotation_period: float  # days
    radius: float  # earth units
    density: float  # kg/m^3
    atmos: Atmosphere  # a class holding atmosphere properties
    moons: dict  # dict of moon orbital distance (in planet radii) to mass (in planet masses)
    gravity: float  # surface/1bar gravity in g

    def getitems(self):
        print(vars(self))


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
