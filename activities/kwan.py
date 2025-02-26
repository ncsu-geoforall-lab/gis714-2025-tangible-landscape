#!/usr/bin/env python3

import os
import grass.script as gs


def run_contour(scanned_elev, env, step=5.0, minlevel=None, maxlevel=None, cut=2, **kwargs):

    params = {
        "input": scanned_elev,
        "output": "contour",
        "step": step,
        "cut": cut,  # Minimum number of points per contour
    }

    gs.run_command("r.contour", env=env, **params)


def main():

    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    input_elev = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=input_elev, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=input_elev, output=elev_resampled, env=env)
    run_contour(input_elev=elev_resampled, env=env, step=2.0, minlevel=0, maxlevel=100)


if __name__ == "__main__":
    main()
