from ast import Raise
from typing import Tuple
import numpy as np

import constants as const


def apparent_magnitude(abs_mag: float, dist: float) -> float:
    """Find apparent magnitude of a star.
    m = M - 5 + 5*log10(d)

    Args:
        abs_mag (float): Absolute magnitude
        dist (float): Distance in pc

    Returns:
        float: _description_
    """
    return abs_mag - 5 + (5 * np.log10(dist))


def absolute_magnitude(luminosity: float) -> float:
    """Get stellar absolute magnitude from luminosity

    Args:
        luminosity (float): Stellar luminosity (solar units)

    Returns:
        float: Stellar absolute magnitude
    """

    return const.mag_sun - (2.5 * np.log10(luminosity))


def calculate_luminosity(mass: float) -> float:
    """Calcuate stellar luminosity based on mass

    Args:
        mass (float): Stellar mass in solar units

    Returns:
        float: Stellar luminosity in solar units
    """
    if mass < 0.43:
        return 0.23 * (mass**2.3)
    elif 0.43 <= mass <= 2.0:
        return mass**4.0
    elif mass > 2.0:
        return 1.4 * (mass**3.5)


def star_radius(mass: float) -> float:
    """Calculate stellar radius from mass

    Args:
        mass (float): Stellar mass in solar units

    Returns:
        float: Stellar radius in solar units
    """
    if mass <= 1.0:
        return mass**0.8
    else:
        return mass**0.57


def stellar_temp(mass: float) -> float:
    """Calcualate stellar surface temperature from mass

    Args:
        mass (float): Stellar mass (solar units)

    Returns:
        float: Temperature (Kelvin)
    """
    return 5778 * (mass**0.54)


def habitable_zone(luminosity: float) -> Tuple[float, float]:
    """Find inner and outer edges of habitable zone based on stellar luminosity

    Args:
        luminosity (float): Stellar luminosity in solar units

    Returns:
        Tuple[float, float]: Inner and outer edges in AU
    """
    rin = np.sqrt(luminosity / 1.1)
    rout = np.sqrt(luminosity / 0.53)
    return rin, rout


def stellar_lifespan(mass: float) -> float:
    """Compute stellar lifespan from mass

    Args:
        mass (float): Stellar mass in solar units

    Returns:
        float: Life span in years
    """
    return 1e10 * (1 / mass) ** 2.5


def stellar_class(temp: float) -> str:
    """Classify a star based on its characteristics

    Args:
        temp (float): star temperature in K
        mass (float): Star mass in km
        lum (float): Star luminosity in W

    Returns:
        str: Stellar classification
    """
    if 7300 <= temp < 10000:
        type = "A"
        mint = 7300.0
        trange = 10000 - mint
        stage = "V"
    elif 6000 <= temp < 7300:
        type = "F"
        mint = 6000
        trange = 7300.0 - mint
    elif 5300 <= temp < 6000:
        type = "G"
        mint = 5300
        trange = 6000.0 - mint
    elif 3800 <= temp < 5300:
        type = "K"
        mint = 3800
        trange = 5300.0 - mint
    elif 2500 <= temp < 3800:
        type = "M"
        mint = 2500.0
        trange = 3800.0 - mint
    elif 1300 <= temp < 2500:
        type = "L"
        mint = 1300.0
        trange = 2500.0 - mint
    elif 600 <= temp < 1300:
        type = "T"
        mint = 600.0
        trange = 1300.0 - mint
    else:
        raise ValueError("Star Temperature out of bounds for habitability")
        # then subtract min & divide by span & * 10 floor
        # then 9-floor
    stype = int(9 - 10 * (temp - mint) / trange)
    return type + str(stype)


# main sequence
# O 0.00001
# B 0.1
# A 0.7
# F 2
# G 3.5
# K 8
# M 80
# Giants 0.4 GKM
# WD 5
