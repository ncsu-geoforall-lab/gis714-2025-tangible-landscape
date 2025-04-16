#!/usr/bin/env python3

import os

import grass.script as gs


def run_dist_from_water(scanned_elev, env, **kwargs):
    """Distance to lakes is a proxy for distance to riparian areas. 
    This is important for understand impacts to insect growth, development, and establishment in the landscape.
    Using the HAND method, this function creates an innundation map and projects distance to flooding.
    """
    gs.run_command(
        'r.watershed',
        elevation=scanned_elev,
        accumulation='flowacc',
        drainage='drainage',
        stream='streams',
        threshold=100,
        overwrite=True,
        env=env
    )
    gs.run_command(
        'r.to.vect',
        input='streams',
        output='streams',
        type='line',
        env=env
    )
    gs.run_command(
        'r.stream.distance',
        stream_rast='streams',
        direction='drainage',
        elevation=scanned_elev,
        method='downstream',
        difference='above_stream',
        env=env
    )
    gs.run_command(
        'r.lake',
        elevation='above_stream',
        water_level=5,
        lake='flood',
        seed='streams',
        env=env
    )
    gs.run_command(
        "r.grow.distance",
        input="flood",
        distance="dist_to_lake",
        overwrite=True
    )

def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_dist_from_water(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
