#!/usr/bin/env python3

import os

import grass.script as gs

def create_end_points(env):
    info = gs.raster_info("scan")
    y1 = info["south"] + 2 * (info["north"] - info["south"]) / 10.0
    y2 = info["south"] + 8 * (info["north"] - info["south"]) / 10.0
    x1 = info["west"] + 2 * (info["east"] - info["west"]) / 10.0
    x2 = info["west"] + 8 * (info["east"] - info["west"]) / 10.0
    gs.write_command(
        "v.in.ascii",
        input="-",
        stdin="{x1}|{y1}\n{x2}|{y2}".format(x1=x1, x2=x2, y1=y1, y2=y2),
        output="points",
        env=env,
    )
    return ((x1, y1), (x2, y2))

def run_viewshed(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.viewshed.cva", input=scanned_elev, vector=points, output="viewshed", env=env
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_viewshed(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
