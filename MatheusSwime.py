#!/usr/bin/env python3

import os
import grass.script as gs
import grass.jupyter as gj


def set_region(env):
    gs.run_command("g.region", region="rural_1m", res=2, flags="p", env=env)
    print("Computational region set to 'rural_1m' with 2m resolution.")


# Function to interpolate elevation and generate slope/aspect
def interpolate_elevation(env):
    gs.run_command(
        "v.surf.rst",
        input="elev_lid792_bepts",
        elevation="elev_lid792_2m",
        slope="dx_2m",
        aspect="dy_2m",
        tension=15,
        smooth=1.5,
        npmin=150,
        flags="d",
        env=env,
    )
    print("Elevation interpolation completed!")


# Function to convert streams vector to raster using direction
def convert_streams_to_raster(env):
    gs.run_command(
        "v.to.rast",
        input="streams@PERMANENT",
        output="streams_dir_2m",
        use="dir",
        env=env,
    )
    print("Streams converted to raster!")


# Function to compute stream-based flow gradients
def compute_stream_gradients(env):
    gs.mapcalc("dx_stream = tan(dx_2m) * cos(streams_dir_2m)", env=env)
    gs.mapcalc("dy_stream = tan(dx_2m) * sin(streams_dir_2m)", env=env)
    print("Stream-based gradient vectors calculated!")


# Function to merge stream and DEM-based gradients
def merge_gradients(env):
    gs.mapcalc("dx_dem_str = if(isnull(dx_stream), dx_2m, dx_stream)", env=env)
    gs.mapcalc("dy_dem_str = if(isnull(dy_stream), dy_2m, dy_stream)", env=env)
    print("Gradient merging completed!")


# Function to run the overland flow model
def run_overland_flow(env):
    gs.run_command(
        "r.sim.water",
        elevation="elev_lid792_2m",
        dx="dx_dem_str",
        dy="dy_dem_str",
        rain_value=50,
        infil_value=0,
        man_value=0.05,
        depth="wdpstr_2m",
        discharge="dischstr_2m",
        nwalkers=100000,
        niterations=30,
        output_step=2,
        flags="t",
        env=env,
    )
    print("Overland flow model completed!")


def display_results(env):
    img = gj.Map(use_region=True)
    img.d_rast(map="disch_2m.30")
    img.d_legend(raster="disch_2m.30", at=(55, 95, 85, 90), flags="b")
    img.show()
    # print("Results displayed!")


# Main function
def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"

    # Run processes in order
    set_region(env)
    interpolate_elevation(env)
    convert_streams_to_raster(env)
    compute_stream_gradients(env)
    merge_gradients(env)
    run_overland_flow(env)
    display_results(env)  # ✅ Calls the function safely


if __name__ == "__main__":
    main()
