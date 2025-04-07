#!/usr/bin/env python3

import os
import grass.script as gs


def run_flood_simulation(env):
    # Set computational region based on the elevation raster
    gs.run_command("g.region", raster="elev_lid792_1m", flags="p", env=env)

    # Simulate lake flooding from given coordinates
    gs.run_command(
        "r.lake",
        elevation="elev_lid792_1m",
        water_level=120.5,
        lake="flood1",
        coordinates=(638728, 220278),
        env=env,
    )
    print("Lake flooding simulation completed!")


def display_flood_result():
    img = gj.Map(use_region=True)
    img.d_rast(map="elev_lid792_1m")
    img.d_rast(map="flood1")
    img.show()


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"

    run_flood_simulation(env)
    display_flood_result()


if __name__ == "__main__":
    main()
