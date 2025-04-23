#!/usr/bin/env python3

import os
import grass.script as gs


def run_flood_sim(scanned_elev, env, **kwargs):
    print("I'm running emma_black.py!!")
    # clean DEM (fill nulls)
    gs.mapcalc("elev_clean = if(isnull({0}), 0, {0})".format(scanned_elev), env=env)

    # generate dx/dy slope components
    gs.run_command("r.slope.aspect", elevation="elev_clean", dx="dx", dy="dy", env=env)

    # run r.sim.water
    gs.run_command("r.sim.water", elevation="elev_clean", dx="dx", dy="dy",
                   rain_value=50, depth="flood_depth", niterations=30, nwalkers=1000,
                   env=env)

    # create binary flood mask
    gs.mapcalc("flood_mask = if(flood_depth > .01, flood_depth, null())", env=env, overwrite=True)

    gs.run_command("r.colors", map="flood_mask", color="water", env=env)


def main():
    env = os.environ.copy()
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"

    # set region and resample
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_flood_sim(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
