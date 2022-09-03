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
    return np.cbrt((3 * mass * const.earth_mass) / (4 * np.pi * density))


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


def teff(albedo: float, luminosity: float, sma: float) -> float:
    """Compute the effective blackbody temperature of a planet

    Args:
        albedo (float): Albedo of planet
        luminosity (float): Luminosity of star in Solar units
        sma (float): Planet orbit semimajor axis in AU

    Returns:
        float: Effective Temperature K
    """
    arg = ((1 - albedo) * luminosity * const.sun_luminosity) / (16 * np.pi * sma * const.au * const.sigma_b)
    return np.power(arg, 0.25)


def atmos_temp(teff: float, eta: float) -> float:
    """Find atmospheric temperature based on incredibly simple model

    Args:
        teff (float): Planet effective temperature in K
        eta (float): Atmospheric absorbtion factor

    Returns:
        float: Rough temperature of the atmosphere in K
    """
    return teff * np.power(1 / (1 - (eta / 2.0)), 0.25)


# need to generate a planet atmosphere
# need to generate an ocean

# randomly generate mass, density, orbit
# calculate radius
#
