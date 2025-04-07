#!/usr/bin/env python3

import os
import grass.script as gs


def run_flood_simulation(scanned_elev, env, **kwargs):

    # Simulate lake flooding from given coordinates
    gs.run_command(
        "r.lake",
        elevation=scanned_elev,
        water_level=120.5,
        lake="flood1",
        coordinates=(638728, 220278),
        env=env,
    )
    print("Lake flooding simulation completed!")



def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"

    run_flood_simulation(env)
    display_flood_result()


if __name__ == "__main__":
    main()
