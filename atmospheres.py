import numpy as np

import planet_utils as p_util
from generate_galaxy import Atmosphere


def gen_terrestrial_atmos(lum: float, sma: float, p_atmos: float, lil_g: float) -> Atmosphere:
    """Generate an atmosphere for a small, rocky planet

    Args:
        lum (float): Stellar luminosity in solar units
        sma (float): semimajor axis in au
        p_atmos (float): Probability of having an atmosphere
        lil_g (float): Surface gravity

    Returns:
        Atmosphere: A randomly generated terrestrial planet atmosphere
    """
    gasses = ["N2", "CO2", "O2", "CH4"]
    gas_p = [0.5, 0.3, 0.15, 0.05]
    if np.random.uniform(0, 1) > p_atmos:
        albedo = 0.2
        teff = p_util.teff(albedo, lum, sma)
        atmos = Atmosphere(scale_height=0, pressure=0, comp={"Other": 1}, eta=0, temp=teff, ocean=0, albedo=albedo)
        # this is a problem , we can't use tss
    else:
        species = np.random.choice(gasses, 2, replace=False, p=gas_p)
        frac_1 = np.random.uniform(0.5, 1)
        frac_2 = np.random.uniform((1 - frac_1) * 0.9, 1 - frac_1)
        other_frac = 1 - frac_1 - frac_2
        comp = {species[0]: frac_1, species[1]: frac_2, "Other": other_frac}
        pressure = np.random.wald(1, 5)

        if np.random.uniform(0, 100) > 99.9:
            pressure = 10**pressure
            eta = np.random.uniform(2, 3)
        else:
            eta = np.random.uniform(0.3, 1)

        clouds = np.random.uniform(0, 1)
        ocean = np.random.uniform(0, 1)
        land = 1 - ocean
        surf_alb = (0.2 * land) + (0.1 * ocean)
        albedo = (clouds * 0.8) + ((1 - clouds) * surf_alb)
        teff = p_util.teff(albedo, lum, sma)
        temp = p_util.atmos_temp(teff, eta)
        scale_h = p_util.scale_height(teff, lil_g, p_util.find_molecular_mass(comp))
        atmos = Atmosphere(
            scale_height=scale_h, pressure=pressure, comp=comp, eta=eta, temp=temp, ocean=ocean, albedo=albedo
        )
    return atmos


def gen_gas_atmos(lum: float, sma: float, lil_g: float) -> Atmosphere:
    """Generate a gas giant atmosphere

    Args:
        lum (float): Stellar luminosity in solar units
        sma (float): Semimajor axis in AU
        lil_g (float): Surface (1 bar) gravity

    Returns:
        Atmosphere: Randomly generated gas giant atmosphere
    """
    albedo = np.random.uniform(0.4, 0.6)
    teff = p_util.teff(albedo, lum, sma)
    other_frac = np.random.uniform(0, 0.03)
    H_frac = np.random.uniform(0.8, 0.98)
    He_frac = 1 - (H_frac + other_frac)
    comp = {"H2": H_frac, "He": He_frac, "Other": other_frac}
    eta = np.random.normal(1.65, 0.2)
    temp = p_util.atmos_temp(teff, eta)
    scale_h = p_util.scale_height(temp, lil_g, p_util.find_molecular_mass(comp))
    atmos = Atmosphere(scale_h, 1.0, comp, eta, temp, 0.0, albedo)
    return atmos
