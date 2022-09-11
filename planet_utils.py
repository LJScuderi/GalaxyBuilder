from typing import Tuple
import numpy as np

import constants as const


# Source for some formulae: https://github.com/lortordermur/sfcalcsheet/wiki/Formulas


def calc_planet_radius(mass: float, density: float) -> float:
    """Calculate planet radius from mass and density

    Args:
        mass (float): planet mass in Earth units
        density (float): planet density in kg m^-3

    Returns:
        float: Planet radius in m
    """
    return np.cbrt((3 * mass) / (4 * np.pi * density))


def planet_density(mass: float, radius: float) -> float:
    """Return density in kg m^-3

    Args:
        mass (float): mass in earth units
        radius (float): radius in earth units

    Returns:
        float: Density in kg m^-3
    """

    return mass * const.earth_mass / ((4.0 / 3.0) * np.pi * (radius * const.earth_radius) ** 3.0)


def rocky_radius(mass: float, cmf: float) -> float:
    """Based on Seager et al. 2007, rocky planet mass-radius relation with average numbers for composition

    Args:
        mass (float): Planet mass in earth units

    Returns:
        float: planet radius in earth units
    """
    # ms = mass * const.earth_mass
    # terma = (1.0 / 3.0) * np.log10(ms)
    # termb = 0.8 * ms**0.394
    # print(((-0.20949 + terma - termb)))
    # return (10.0 ** (-0.20949 + terma - termb)) / const.earth_radius
    return (1.07 - (0.21 * cmf)) * (mass ** (1.0 / 3.7))


def surface_grav(mass: float, radius: float) -> float:
    """Calculate planet surface gravity from mass and radius

    Args:
        mass (float): Planet mass in earth units
        radius (float): Planet radius in earth units

    Returns:
        float: Planet surface gravity in earth units
    """
    return mass / radius**2


def escape_velocity(mass: float, radius: float) -> float:
    """Calculate escape velocity from mass and radius

    Args:
        mass (float): Planet mass in earth masses
        radius (float): Planet mass in earth radii

    Returns:
        float: Surface escape velocity in m/s
    """
    return np.sqrt(2 * mass * const.earth_mass * const.bigG / (radius * const.earth_radius))


def roche_rigid(radius: float, prime_density: float, secondary_density: float) -> float:
    """Compute roche radius for a rigid body

    Args:
        radius (float): Radius of the primary body in earth units
        prime_density (float): Density of the primary body in kg m^-3
        secondary_density (float): Density of the secondary body in kg m^-3

    Returns:
        float: Radius from primary in m
    """
    return radius * const.earth_radius * 1.26 * np.cbrt(prime_density / secondary_density)


def roche_liquid(radius: float, prime_density: float, secondary_density: float) -> float:
    """Compute roche radius for a liquid/loose body

    Args:
        radius (float): Radius of the primary body in earth units
        prime_density (float): Density of the primary body in kg m^-3
        secondary_density (float): Density of the secondary body in kg m^-3

    Returns:
        float: Radius from primary in m
    """
    return radius * const.earth_radius * 2.44 * np.cbrt(prime_density / secondary_density)


def orbital_period(sma: float, mass: float) -> float:
    """Find orbital period from semimajor axis and mass of primary

    Args:
        sma (float): Semimajor axis of orbit in m
        mass (float): Mass of primary in kg

    Returns:
        float: Orbital period in s
    """
    return np.sqrt(4 * (np.pi**2) * (sma**3) / (const.bigG * mass))


def sma_from_t(period: float, host_mass: float, scale_unit: float = const.au) -> float:
    """Get semimajor axis from orbital period

    Args:
        period (float): Period of orbit in s
        host_mass (float): Mass of host in kg
        scale_unit (float, optional): Output unit for SMA in meters. Defaults to AU.

    Returns:
        float: Semimajor axis in specified units
    """
    sma = np.cbrt(period**2 * const.bigG * host_mass / (4.0 * np.pi**2))
    return sma / scale_unit


def tss(lum: float, sma: float) -> float:
    return 0.5 * (lum * const.sun_luminosity / (np.pi * (sma * const.au) ** 2 * const.sigma_b)) ** (0.25)


def teff(albedo: float, luminosity: float, sma: float) -> float:
    """Compute the effective blackbody temperature of a planet

    Args:
        albedo (float): Albedo of planet
        luminosity (float): Luminosity of star in Solar units
        sma (float): Planet orbit semimajor axis in AU

    Returns:
        float: Effective Temperature K
    """
    numerator = (1 - albedo) * luminosity * const.sun_luminosity
    denominator = 16 * np.pi * (sma * const.au * 1000) ** 2.0 * const.sigma_b
    arg = numerator / denominator
    return arg**0.25


def atmos_temp(teff: float, eta: float) -> float:
    """Find atmospheric temperature based on incredibly simple model

    Args:
        teff (float): Planet effective temperature in K
        eta (float): Atmospheric absorbtion factor

    Returns:
        float: Rough temperature of the atmosphere in K
    """
    return teff * (1 / (1 - (eta / 2.0)) ** 0.25)


def find_molecular_mass(comp: dict) -> float:
    """Find mean molecular mass

    Args:
        comp (dict): Dict of primary atmosphere composition

    Returns:
        float: Mean molecular mass in kg
    """
    masses = {
        "N2": 4.6518e-26,
        "CO2": 7.3079e-26,
        "O2": 5.3134e-26,
        "CH4": 2.664e-26,
        "H2": 3.348e-27,
        "He": 6.646477e-27,
        "Other": 3e-26,
    }
    average_mass = 0.0
    for key in comp:
        average_mass += comp[key] * masses[key]
    return average_mass


def scale_height(temp: float, g: float, bigM: float) -> float:
    """Find atmosphere scale height

    Args:
        teff (float): Effective temperature in K
        g (float): Surface gravity in m/s^2
        mean_mass (float): Mean molecular mass of atmosphere in kg

    Returns:
        float: Atmosphere scale height in km
    """
    return (const.k_b * temp / (bigM * g * const.g)) / 1000.0


def gen_tilt_spin(sma: float, radius: float, smass: float, pmass: float, age: float) -> Tuple[float, float]:
    """Generate axial tilt and spin rate

    Args:
        sma (float): semimajor axis in m
        radius (float): planet radius in m
        smass (float): star mass in kg
        pmass (float): planet mass in kg
        age (float): planet age in years

    Returns:
        Tuple[float, float]: A Tuple with axial tilt in degrees and spin rate in days/revolution
    """
    tlock = 6.0 * 1e10 * ((sma**6.0) * radius * 3.0e10) / (smass * (pmass**2.0))
    if tlock <= age:
        return np.random.uniform(0, 5), orbital_period(sma, smass)
    else:
        tilt = np.random.triangular(0, 15, 55)
        if tilt > 40:
            tilt += np.random.uniform(25, 125)
        if pmass < 8.0 * const.earth_mass:
            spin = np.random.triangular(0.08, 0.7, 3.0)
        else:
            spin = np.random.triangular(0.08, 0.2, 1.0)
        return (tilt, spin)
