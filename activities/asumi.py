#!/usr/bin/env python3

import os

import grass.script as gs


def run_slope(scanned_elev, env, **kwargs):
    gs.run_command("r.slope.aspect", elevation=scanned_elev, slope="slope", env=env)


def run_watershed(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.watershed",
        elevation=scanned_elev,
        threshold=5000,
        accumulation="accum_mfd5K",
        drainage="draindir_5K",
        basin="basin_mfd5K",
        env=env,
    )


def run_flow(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.flow",
        elevation=scanned_elev,
        flowline="flowlines",
        flowlength="flowlg_vb",
        flowaccumulation="flowacc_vb",
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_watershed(scanned_elev=elev_resampled, env=env)
    run_flow(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
