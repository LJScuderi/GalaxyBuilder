from generate_galaxy import Star, Planet, System, Atmosphere

sol = Star(name="Sol", temperature=5778, age=4.603, metallicity=1.0)
sun_planets = []
mercury = Planet(
    name="Mercury",
    parent=sol.name,
    type="rocky",
    orbit=0.38709893,
    axial_tilt=0.034,
    rotation_period=175.942,
    radius=0.383,
    density=5429,
    atmos=Atmosphere(10, 5e-15, 0.05, 0, 0, 0.01, 0, 0.94),
    ocean_coverage=0.0,
    moons=0,
)
sun_planets.append(mercury)

sun_stations = []
sun_belts = {1: [2.06, 3.27], 2: [30, 1000]}
sol_system = System(0, 0, 0, sol, sun_planets, sun_stations, sun_belts)
