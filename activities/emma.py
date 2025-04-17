#!/usr/bin/env python3

import os
import grass.script as gs

def run_hand_model(env):
    gs.run_command("r.hydrodem", input="elev_lid792_1m", output="hydro_dem", env=env)
    gs.run_command("r.stream.extract", elevation="hydro_dem", threshold=5000, output="streams", env=env)
    gs.run_command("r.stream.distance", stream_rast="streams", direction="flow_dir", elevation="hydro_dem", output="HAND", env=env)

def run_surface_water(env):
    gs.run_command("r.sim.water", elevation="elev_lid792_1m", rain_value=20, depth="flow_depth", output="water_flow", env=env)

def run_flood_inundation(env):
    gs.run_command("r.lake", elevation="elev_lid792_1m", water_level=5, output="flood_area", env=env)

def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"

    run_hand_model(env)
    run_surface_water(env)
    run_flood_inundation(env)

if __name__ == "__main__":
    main()
