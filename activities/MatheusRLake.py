#!/usr/bin/env python3

import os
import grass.script as gs


def run_flood_simulation(elevation, env, **kwargs):
    gs.run_command(
        "r.lake",
        elevation=elevation,
        water_level=121.0,
        lake="flood1",
        coordinates=(638728, 220278),
        env=env,
    )
    print("Lake flooding simulation completed!")


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"

    gs.run_command("g.region", raster=elevation, res=2, flags="a", env=env)

    run_flood_simulation(elevation=elevation, env=env)


if __name__ == "__main__":
    main()
